## Summary

This paper introduces LLM4GCL, the first comprehensive benchmark for evaluating LLM-based methods in Graph Continual Learning (GCL), and proposes SimGCL, a simple method combining LoRA-based instruction tuning with training-free prototype classification. A key methodological contribution is the identification of task ID leakage in the commonly-used local testing evaluation protocol for Node-level Class-Incremental Learning (NCIL), which the authors demonstrate allows even trivial methods to achieve near-perfect performance. The paper evaluates 9 LLM/GLM-based and 7 GNN-based methods across 7 datasets, finding that SimGCL significantly outperforms prior methods on most benchmarks.

## Strengths

- **Genuine methodological critique of evaluation practices.** The paper convincingly demonstrates that local testing in NCIL enables task ID leakage, degrading class-incremental to task-incremental learning. Table 1 is compelling: even MLP + mean pooling achieves 0% forgetting and matches TPP's reported performance. This is an important corrective for the GCL community and the shift to global testing is well-motivated.

- **Comprehensive and practically valuable benchmark.** The benchmark spans 7 datasets across citation, web, and e-commerce domains with varying scales (thousands to hundreds of thousands of nodes), 9 diverse baselines (GNN, LLM, and GLM categories), and two learning paradigms (NCIL and FSNCIL). The consistent experimental protocol, removal of inter-task edges to prevent knowledge leakage, and class imbalance correction demonstrate thoughtful benchmark design.

- **Surprising and actionable finding that simple LLM methods outperform complex GLMs.** Observation ❸ reveals that deliberately designed GLM methods like GraphPrompter, GraphGPT, and LLaGA consistently underperform pure LLM methods like SimpleCIL. This is counterintuitive and valuable, suggesting the GNN-LLM architectural gap creates representation misalignment that harms continual learning. The observation that prototype-based learning naturally provides the right balance between plasticity and generalization (Observation ❻) is also well-supported across all datasets.

- **Clear and reproducible method design.** SimGCL's two-stage pipeline (instruction tuning → prototype generation) is simple, efficient, and achieves strong results. The paper provides code and an easy-to-use platform.

## Weaknesses

### Fatal

None.

### Major

- **Inconsistent SimGCL improvements over SimpleCIL.** The headline claim of ~20% improvement over previous SOTA is selective. Comparing SimGCL to SimpleCIL (the strongest non-SimGCL method) in Table 2: Cora +13.8%, Citeseer +10.7%, WikiCS +2.1%, Photo +20.0%, Products +4.3%, Arxiv-23 -13.7%, Arxiv +9.3%. On Arxiv-23 (NCIL) and across FSNCIL results, SimGCL actually underperforms SimpleCIL significantly (e.g., Arxiv-23: 31.8% vs. 49.8% in FSNCIL). The paper acknowledges sparse graph structure as a factor but does not provide systematic analysis of when graph structure genuinely helps. This undermines the claim that graph-aware prompting is consistently beneficial.

- **Lack of ablation studies.** The paper does not ablate the key components of SimGCL: (1) the contribution of ego-graph-derived prompts vs. simple text prompts, (2) the effect of LoRA rank and tuning hyperparameters, (3) the scaling temperature τ sensitivity, (4) the impact of prompt design choices (number of neighbors, prompt template). Without these, it is unclear whether SimGCL's gains come from graph-aware prompting, prototype matching, or simply the choice of LLM backbone.

- **No variance or statistical significance reported.** All results appear to be from single runs. Given the sensitivity of continual learning to class ordering, initialization, and data splits, confidence intervals or multiple-seed results are essential for reliable claims, particularly given the modest margins between SimGCL and SimpleCIL on several datasets.

### Minor

- **Prototype methods from CV continual learning are not novel.** The observation that training-free prototypes after initial tuning are effective has been well-established in vision continual learning (e.g., Zhou et al. 2025 referenced in Section 5). The paper does not sufficiently discuss this prior work or clarify what is genuinely novel about SimGCL beyond applying known techniques to graphs.

- **The "20% improvement" framing is misleading.** The 20% figure applies to specific datasets (Photo, Products) compared to the best GNN baselines, not to SimpleCIL or other LLM-based methods. The paper's abstract and contribution list use this number prominently, which overstates the general advantage.

- **Limited discussion of computational costs.** While SimGCL is described as efficient, no training/inference time comparisons are provided. LLM inference on large ego-graph prompts for graphs with hundreds of thousands of nodes could be substantial, and this should be quantified.

### Trivial

None.

## Nice-to-Haves

- Analysis of when graph structure actually helps vs. hurts in GCL (the Arxiv-23 failure case deserves deeper investigation)
- Comparison with rehearsal-based methods to understand the gap between replay-free and replay-based approaches
- Per-session accuracy curves for all methods (only shown for SimpleCIL and SimGCL in Figure 3)

## Novel Insights

The identification of task ID leakage in local testing protocols for NCIL is a genuinely novel and impactful contribution that should reshape how the GCL community evaluates methods. The finding that GLM-based methods with graph structure integration perform worse than pure LLM methods with prototypes is surprising and suggests fundamental architectural incompatibilities between GNNs and LLMs in continual learning settings. The observation that prototype-based methods exhibit consistent stability across varying session numbers (Table 4) while other methods degrade is also practically valuable.

## Suggestions

- Add ablation experiments for SimGCL components (prompt design, LoRA rank, temperature τ)
- Report results over multiple seeds with standard deviations
- Include computational cost comparisons (training time, inference time, memory) across methods
- Analyze SimGCL's failure cases (Arxiv-23, FSNCIL) more systematically to characterize when graph-aware prompting provides genuine value

## Score and Decision

The paper makes a meaningful contribution by identifying a real methodological flaw in GCL evaluation and establishing the first comprehensive LLM-based GCL benchmark with diverse datasets and baselines. However, the core proposed method (SimGCL) shows inconsistent improvements over the simple SimpleCIL baseline, lacks ablation studies to justify its design choices, and presents no variance estimates. The benchmark itself has clear practical value for the community, but the paper overstates SimGCL's novelty and effectiveness relative to existing techniques.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>