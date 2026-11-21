"""从头运行全部 notebook，并与书中印出的“本书验证环境实际运行输出”逐行比对。

用法（在 stat-breeding-book 环境中）：
    python run_all.py              # 运行全部，执行结果写回 notebooks/
    python run_all.py 07c 11       # 只运行名称以这些前缀开头的 notebook
    python run_all.py --inprocess  # 不启动 Jupyter 内核，在当前 Python 进程中依次执行代码单元
                                   # （用于无法启动 Jupyter 内核的环境）
输出：核对报告.md
"""
import difflib
import re
import sys
import time
from pathlib import Path

import platform

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).parent
NB, EXP = HERE / "notebooks", HERE / "expected_outputs"
IGNORE = re.compile(r"^(Platform|Python)\b|^<Figure size")   # 平台字符串与图形对象描述不参与比对


def stdout_of(nb):
    out = []
    for c in nb.cells:
        if c.cell_type != "code":
            continue
        for o in c.get("outputs", []):
            if o.get("output_type") == "stream" and o.get("name") == "stdout":
                out.append(o["text"])
            elif o.get("output_type") in ("execute_result", "display_data") and "text/plain" in o.get("data", {}):
                out.append(o["data"]["text/plain"] + "\n")
    return "".join(out)


def run_inprocess(nb):
    """不经 Jupyter 内核，按顺序在同一命名空间中执行代码单元，标准输出写回 notebook。"""
    import contextlib, io, os, traceback
    import matplotlib
    matplotlib.use("Agg")
    ns, cwd = {"__name__": "__main__"}, os.getcwd()
    os.chdir(NB)
    try:
        for k, c in enumerate(nb.cells):
            if c.cell_type != "code":
                continue
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(compile(c.source, f"<cell {k}>", "exec"), ns)
            finally:
                c.execution_count = k
                if buf.getvalue():
                    c.outputs = [nbformat.v4.new_output("stream", name="stdout", text=buf.getvalue())]
        import matplotlib.pyplot as plt
        plt.close("all")
    except Exception:                                # noqa: BLE001
        raise RuntimeError(traceback.format_exc().strip().splitlines()[-1])
    finally:
        os.chdir(cwd)


def norm(text):
    return [re.sub(r"\s+", " ", l).strip() for l in text.splitlines() if l.strip() and not IGNORE.match(l.strip())]


def main():
    inproc = "--inprocess" in sys.argv
    pick = [a for a in sys.argv[1:] if not a.startswith("--")]
    rows = []
    for path in sorted(NB.glob("*.ipynb")):
        if pick and not any(path.stem.startswith(p) for p in pick):
            continue
        nb = nbformat.read(path, as_version=4)
        for c in nb.cells:                           # 先清空旧输出，执行失败时不会沿用旧结果
            if c.cell_type == "code":
                c.outputs, c.execution_count = [], None
        t0 = time.time()
        err = ""
        try:
            if inproc:
                run_inprocess(nb)
            else:
                NotebookClient(nb, timeout=1800, startup_timeout=600, kernel_name="python3",
                               resources={"metadata": {"path": str(NB)}}).execute()
        except Exception as e:                       # noqa: BLE001
            err = str(e).strip().splitlines()[-1][:200] if str(e).strip() else type(e).__name__
        nbformat.write(nb, path)
        got, exp = norm(stdout_of(nb)), norm((EXP / f"{path.stem}.txt").read_text(encoding="utf-8"))
        ratio = difflib.SequenceMatcher(None, got, exp).ratio()
        diff = [l for l in difflib.unified_diff(exp, got, "书中输出", "本次运行", n=0, lineterm="")
                if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        rows.append((path.stem, err, ratio, len(exp), diff, time.time() - t0))
        print(f"{path.stem:32s} {'出错 ' + err if err else '运行完成'}  一致行比例 {ratio:.3f}  {time.time() - t0:.0f}s",
              flush=True)
    with open(HERE / "核对报告.md", "w", encoding="utf-8") as f:
        import numpy, pandas, sklearn
        f.write("# 电子资源运行核对报告\n\n"
                f"运行平台：{platform.platform()}（Python {platform.python_version()}、numpy {numpy.__version__}、"
                f"pandas {pandas.__version__}、scikit-learn {sklearn.__version__}；执行方式：{'进程内依次执行代码单元' if inproc else 'Jupyter 内核'}）。\n\n比对对象：书中“本书验证环境实际运行输出”。平台行（Python/Platform）不参与比对。\n\n")
        f.write("| notebook | 运行 | 与书中输出一致 | 耗时 |\n|---|---|---|---|\n")
        for nbn, err, ratio, n, diff, sec in rows:
            ok = "完全一致" if not diff else f"{ratio:.1%}（{len(diff)} 行差异）"
            f.write(f"| {nbn} | {'出错：' + err if err else '通过'} | {ok} | {sec:.0f}s |\n")
        for nbn, err, ratio, n, diff, sec in rows:
            if diff:
                f.write(f"\n## {nbn}\n\n```diff\n" + "\n".join(diff[:40]) + "\n```\n")
    print("报告：", HERE / "核对报告.md")


if __name__ == "__main__":
    main()
