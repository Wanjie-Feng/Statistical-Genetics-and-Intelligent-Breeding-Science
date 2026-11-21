# 《统计遗传与智能育种学》电子资源

本目录为书中全部实践的可运行 Jupyter Notebook。每个 notebook 的代码与书中“完整Python代码”逐字一致，均使用模拟数据，固定随机种子，无需下载外部数据。

## 运行环境

书中输出在 Python 3.12.13、numpy 2.3.5、pandas 2.2.3、scikit-learn 1.8.0 下得到。建议用 conda / micromamba 建立相同环境：

```bash
micromamba create -f environment.yml   # 或 conda env create -f environment.yml
micromamba activate stat-breeding-book
jupyter lab notebooks/
```

运行检查：打开 notebook 后选择“重启内核并运行全部单元”（Restart Kernel and Run All）。

一次性运行全部 notebook 并与书中输出比对：

```bash
python run_all.py
```

结果写入 `核对报告.md`。

### 关于跨平台差异

书中输出在 Linux x86_64 上得到。在 macOS（Apple 芯片）上运行时，41 个 notebook 的输出与书中完全一致；`05d_bsa_design` 从“深度 100”一行起数值略有不同，原因是不同平台数学库在生成大均值泊松随机数时存在末位差异，结论不受影响。在 Linux x86_64 电脑上运行，05d 的输出与书中逐位一致。

不用 conda 时也可 `pip install -r requirements.txt`。`expected_outputs/` 中保存的是书中印出的“本书验证环境实际运行输出”。

## 外部软件模板

部分实践附有 PLINK 2.0、Beagle、rMVP、QTG-seq、MACS2、SIMER、HIBLUP、SoyDNGPNext 等外部工具的命令或 R 代码模板，以 Markdown 代码块保留在对应 notebook 中，不在 notebook 内执行；使用时请按所用软件版本的官方文档核对参数。

## 目录

| 章 | notebook | 实践 |
|---|---|---|
| 第一章 | `01_data_reproducibility.ipynb` | 实践 1.1  从样本表到可建模数据 |
| 第一章 | `01b_workflow_manifest.ipynb` | 实践 1.2  文件校验、样本映射与批量任务表 |
| 第二章 | `02_vcf_qc.ipynb` | 实践 2.1  VCF解析与基本基因型质控 |
| 第三章 | `03_mixed_model_gblup.ipynb` | 实践 3.2  从基因型矩阵构建G矩阵并完成GBLUP |
| 第三章 | `03b_heritability_shrinkage.ipynb` | 实践 3.1  遗传力、重复数与BLUP收缩的虚拟试验 |
| 第四章 | `04_gwas_population_structure.ipynb` | 实践 4.1  群体结构如何制造GWAS假阳性 |
| 第四章 | `04b_gwas_toolchain.ipynb` | 实践 4.2  从PLINK质控到rMVP输入：基因型数据迁移链 |
| 第四章 | `04c_gwas_power.ipynb` | 实践 4.3  GWAS功效评估：样本量×MAF×效应大小 |
| 第五章 | `05_bsa_poolseq.ipynb` | 实践 5.1  从混池读段计数定位模拟QTL |
| 第五章 | `05b_qtgseq_smoothlod.ipynb` | 实践 5.2  QTG-seq输入格式与平滑教学示例 |
| 第五章 | `05c_bsa_advanced.ipynb` | 实践 5.3  DeepBSA与QTG-Miner：从分析流程到可计算练习 |
| 第五章 | `05d_bsa_design.ipynb` | 实践 5.4  BSA设计敏感性：池大小×深度×窗口 |
| 第六章 | `06_twas_grex.ipynb` | 实践 6.1  实测表达与遗传预测表达为什么不同 |
| 第七章 | `07_phenomics_rgb.ipynb` | 实践 7.1  RGB分割验证与动态表型计算 |
| 第七章 | `07b_phenomics_feature_qc.ipynb` | 实践 7.2  高维图像性状的筛选与共线性诊断 |
| 第七章 | `07c_field_spatial_qc.ipynb` | 实践 7.3  田间空间趋势对基因型效应估计的影响 |
| 第八章 | `08_enviromics_gxe.ipynb` | 实践 8.1  G×E反应规范与单环境留出 |
| 第九章 | `09_multiomics_qc.ipynb` | 实践 9.1  组学矩阵的QC、缺失值与批次效应 |
| 第九章 | `09b_missing_imputation.ipynb` | 实践 9.2  MCAR与低丰度缺失下的插补比较 |
| 第九章 | `09c_metabolite_mgwas.ipynb` | 实践 9.3  模拟mGWAS与候选基因证据汇总 |
| 第九章 | `09d_proteomics_fdr_inference.ipynb` | 实践 9.4  靶标—诱饵FDR与共享肽段的蛋白推断 |
| 第十章 | `10_epigenomics_atac.ipynb` | 实践 10.1  ATAC-seq差异可及性分析与表达关联 |
| 第十章 | `10b_chip_atac_toolchain.ipynb` | 实践 10.2  ChIP-seq/ATAC-seq命令模板与TSS质控 |
| 第十章 | `10c_peak_consensus_diff.ipynb` | 实践 10.3  共识峰、重复一致性与差异峰的联合判定 |
| 第十一章 | `11_hic_contactmap.ipynb` | 实践 11.1  模拟Hi-C矩阵的距离衰减、区室与候选染色质环 |
| 第十一章 | `11b_hic_depth_resolution.ipynb` | 实践 11.2  测序深度和分箱宽度对模拟结构检出的影响 |
| 第十二章 | `12_gs_training_set.ipynb` | 实践 12.1  GBLUP、训练群体关系与跨群体验证 |
| 第十二章 | `12b_gs_gxe_validation.ipynb` | 实践 12.2  多环境预测的随机记录验证与留一环境验证 |
| 第十三章 | `13_soydngp_virtual.ipynb` | 实践 13.1  用模拟基因型比较岭回归与MLP |
| 第十三章 | `13b_ai_foundations.ipynb` | 实践 13.2  梯度下降与不平衡分类评价 |
| 第十三章 | `13c_family_leakage.ipynb` | 实践 13.3  随机划分与整家系留出对模型评价的影响 |
| 第十四章 | `14_dh_top_potential.ipynb` | 实践 14.1  DH测交性状预测与组合潜力排序 |
| 第十四章 | `14b_simer_selection.ipynb` | 实践 14.2  标准化加权指数与多世代遗传响应 |
| 第十五章 | `15_hiblup_virtual.ipynb` | 实践 15.1  系谱与基因组信息的模拟群体遗传评估 |
| 第十六章 | `16_lowcov_imputation.ipynb` | 实践 16.1  0.5×、1×与2×模拟测序的后验剂量估计 |
| 第十六章 | `16b_genotyping_strategy.ipynb` | 实践 16.2  同一育种群比较芯片、GBS、靶向面板和低深度全基因组测序 |
| 第十七章 | `17_regulatory_variant.ipynb` | 实践 17.1  模拟序列的变异效应评分与饱和突变扫描 |
| 第十七章 | `17b_epigs_virtual.ipynb` | 实践 17.2  SNP与甲基化联合预测：增益、冗余与环境泄漏 |
| 第十七章 | `17c_epigenetic_breeding.ipynb` | 实践 17.3  稳定表观等位基因与环境诱导甲基化的跨代选择价值 |
| 第十八章 | `18_design_to_edit.ipynb` | 18.9 综合实践一：编辑候选的多层证据与优先级 |
| 第十八章 | `18b_edit_validation.ipynb` | 18.10 综合实践二：独立编辑事件与多环境因果验证 |
| 第十八章 | `18c_breeding_decision.ipynb` | 18.11 综合实践三：编辑效应与基因组预测的多性状综合选择 |

运行时各 notebook 会在 `notebooks/` 下生成 `outputs_*` 目录或图片文件，可随时删除后重新运行。
