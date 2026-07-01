I have all the information I need. Let me now produce the final consolidated review.

## Summary

This paper introduces LLM4GCL, a benchmark for evaluating large language models (LLMs) and graph-enhanced LLMs on graph continual learning (GCL) tasks. It identifies a critical flaw in prior GCL evaluation — task ID leakage in the local testing setup (Table 1) — which collapses class-incremental learning into task-incremental learning. The paper then benchmarks 9 methods across 7 textual-attributed graph datasets under a corrected global testing protocol, and proposes SimGCL, which combines a single-session LoRA fine-tuning of an LLM with ego-graph-driven prompts and training-free prototype classification.

## Strengths

- **Sharp identification of task ID leakage in GCL evaluation (Section 3.1, Table 1).** The paper demonstrates that simple mean pooling achieves 100% task-ID prediction accuracy under the local testing protocol, matching prior SOTA (TPP) and achieving zero forgetting. This is a clear, reproducible, and consequential finding that should change how GCL experiments are designed. It is the paper's most important contribution.

- **Comprehensive and well-structured benchmark (Tables 2, 3, 4).** The paper evaluates 9 methods (GNN-based, LLM-based, GLM-based) across 7 diverse datasets (citation networks, web links, e-commerce) spanning different scales, densities, and session configurations. The coverage supports meaningful comparative statements and provides useful infrastructure for the community.

- **Code release and platform development.** The paper explicitly commits to releasing an easy-to-use platform, which is essential for a benchmark contribution to have lasting value.

## Weaknesses

### Fatal
None.

### Major

- **Framing mismatch between the titular question and what the experiments actually test.** The paper asks "Can LLMs alleviate catastrophic forgetting in GCL?" but the headline method, SimGCL, answers this by *avoiding incremental learning entirely* — it fine-tunes once on session 1 and then freezes the model, accumulating prototypes without any parameter updates. Under this design there is nothing to forget, so the method cannot speak to whether LLMs are *more robust to forgetting* when they *do* continue to learn across sessions. The benchmark does include BERT, RoBERTa, and LLaMA baselines that appear to learn incrementally, and those results show that plain LLM fine-tuning also forgets badly. But the paper's framing consistently suggests SimGCL itself addresses the forgetting problem, when in reality it sidesteps it. The comparison to GNN-based methods that *do* learn each session is informative but asymmetric on the forgetting axis, and the paper does not sufficiently acknowledge this distinction.

- **No variance or statistical reliability information in the main paper.** None of the tables report standard deviations, confidence intervals, or number of random seeds. For a benchmark paper aiming to establish reference results for future work, the reader cannot assess whether gaps between methods (e.g., SimGCL 84.6 vs. SimpleCIL 70.8 on Cora) are stable or reflect a single run. This is a significant evidential gap. (If multi-seed results appear in the appendix, the main text should at minimum reference and summarize them.)

- **SimGCL underperforms the simpler SimpleCIL baseline on 2 of 7 datasets, and this is minimally discussed.** On Arxiv-23 in NCIL (Table 2), SimGCL achieves 38.7% AA and 13.6% A_N versus SimpleCIL's 52.4% AA and 38.8% A_N. In FSNCIL (Table 3), the same pattern holds on both Arxiv-23 (SimGCL: 31.8/10.3 vs. SimpleCIL: 49.8/40.0) and Arxiv (SimGCL: 36.3/6.8 vs. SimpleCIL: 46.4/36.6). The paper attributes this to "sparse graph structure" and "expanded tuning set" in a single sentence but provides no investigation or ablation. This directly undermines the abstract's claim of "around 20% improvement" (which is stated as a general characterization but is selective — it applies to some datasets but not others, as the contribution list more accurately notes with "on certain datasets"). The failure pattern is also informative: if graph prompts hurt on these datasets, that finding deserves in-depth analysis, not a one-line dismissal.

- **SimGCL's LLM backbone is not specified for the main results (Tables 2, 3).** The paper does not state which LLM backbone SimGCL uses in the primary experiments. Figure 3 (which studies scaling) uses BERT and RoBERTa variants, but the corresponding backbone for the main tables is not identified in the method description, table captions, or experiment section. This is a basic missing specification for reproducibility.

### Minor

- **Missing ablation study for SimGCL components.** The method combines three components: (a) LoRA instruction tuning on session 1, (b) ego-graph-derived prompts (closely following Wang et al., 2025), and (c) training-free prototype classification. Without ablations, it is unclear what each component contributes, whether the combination is synergistic, and whether the graph prompts actually help on denser graphs (as claimed) while hurting on sparser ones (as the Arxiv-23 results suggest).

- **Temperature hyperparameter τ (Eq. 2) is introduced but never discussed.** The paper does not state how τ is chosen, whether it is dataset-dependent, or how sensitive results are to its value. For a prototype-based classifier, the temperature scaling of cosine similarities directly affects predictions and should be specified.

- **Observation numbering inconsistency.** The main observations skip from ❹ to ⑥ (no Obs. ❺), and subsequent observations shift from circled numbers to Arabic numerals (7, 8). This suggests either missing content or a numbering error.

- **The "around 20% improvement" claim in the abstract is stated without the qualification that it applies only to certain datasets.** The contribution list (line 30) correctly says "on certain datasets," but the abstract presents the 20% figure as a general characterization (line 9). This is misleading to a reader who skims the abstract.

### Trivial

- In Equation (1), the definition of K is notationally circular: K is used in the denominator before its definition is completed. The equation is technically correct but could be presented more clearly.

## Nice-to-Haves

- **Ablation of SimGCL components** across all datasets (especially on the two where it fails) to understand when graph prompts help vs. hurt.
- **Multi-seed experiments and variance reporting** to establish the reliability of the reported numbers.
- **Discussion of τ selection** and its sensitivity.
- **An explicit incremental-fine-tuning LLM baseline** where an LLM is continuously updated (with or without regularization) to directly test whether pretrained representations resist forgetting during sequential learning — the paper's titular question. (Note: BERT/RoBERTa/LLaMA baselines are included but their training protocol is unclear; making this explicit would directly address the framing concern.)

## Removed Points

- **"Missing baseline: LLM + incremental learning":** REMOVED because the benchmark includes BERT, RoBERTa, and LLaMA as baselines, which are LLMs tested in the GCL setting. Even if their training protocol could be clearer, the claim that the benchmark "never tests" this is inaccurate.
- **"SimGCL technical novelty is thin":** REMOVED as a weakness — the paper positions SimGCL as "simple yet effective" and is transparent about building on prior work. A simple method is not a flaw; the missing ablations (retained above) are the genuine issue.
- **Framing concern about task-IL vs class-IL being well-known in broader CL literature:** REMOVED because the paper still makes a concrete contribution by documenting this specific collapse in the GCL evaluation protocol, which had not been previously identified despite years of published work using it. Contextualizing within broader CL literature would strengthen the paper but the omission is not a weakness.
- **"No discussion of computational cost":** REMOVED — the paper mentions efficiency advantages of SimGCL (single-session tuning) and references time-efficiency analysis in Appendix E.
- **"Doesn't say which LLM backbone for Figure 3":** The figure caption clarifies that "B" and "Ro" refer to BERT and RoBERTa. The backbone *for the main results* is the specification issue retained above.

## Novel Insights

The strongest insight from this review is that the paper's most important contribution — the task ID leakage critique — and its headline method are somewhat in tension. The task ID leakage finding shows that the existing GCL evaluation protocol is broken; fixing it with global testing reveals that all methods that learn incrementally forget catastrophically. The paper then proposes SimGCL, which avoids learning incrementally. This indirectly suggests that the correct answer to "can LLMs alleviate forgetting in GCL?" may be "only if you don't learn," which is a useful but deflationary result. The failure of graph prompts on sparse datasets (Arxiv-23) further suggests that the benefit of encoding graph structure via text prompts is dataset-dependent and not universally positive. These patterns are more interesting than the paper's headline of "20% improvement" but are not developed.

## Suggestions

1. Add a sentence to the abstract and introduction clarifying that SimGCL avoids forgetting by not updating parameters after session 1, and that the benchmark's main finding about LLMs and forgetting is that frozen LLM representations + prototypes outperform methods that learn incrementally.
2. Report multi-seed statistics (mean ± std) or at minimum state the number of seeds used, either in the main tables or with a clear reference to the appendix.
3. Add an ablation table showing: (a) SimGCL without graph prompts (flat text only), (b) without instruction tuning, and (c) with a learned classifier instead of prototypes — on both the 5 datasets where SimGCL succeeds and the 2 where it fails.
4. Specify the LLM backbone used for SimGCL in the Table 2 and Table 3 captions, and state the value or selection procedure for τ.
5. Discuss the Arxiv-23 and Arxiv FSNCIL failures more thoroughly — this is where the method's limitations reveal the most about when graph prompts are beneficial.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>