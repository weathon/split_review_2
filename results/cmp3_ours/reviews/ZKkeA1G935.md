Now I have enough calibration context. Let me write the final review.

## Summary

The paper introduces LLM4GCL, a systematic benchmark evaluating whether LLMs can alleviate catastrophic forgetting in Graph Continual Learning (GCL). Its contributions are: (1) identifying a task-ID leakage flaw in prior GCL evaluation protocols (local testing), (2) providing a comprehensive benchmark evaluating 9 methods across 7 textual-attributed graph datasets under two continual learning settings (NCIL and FSNCIL), and (3) proposing SimGCL, a method combining ego-graph-derived prompts, one-shot instruction tuning via LoRA, and training-free prototype classification. SimGCL outperforms prior GNN-based methods by roughly 20% on several datasets.

## Strengths

1. **Clear identification of a genuine evaluation flaw in prior GCL work (Section 3.1, Table 1).** The paper convincingly shows that the "local testing" setup used by prior GCL benchmarks degrades class-incremental learning into task-incremental learning. Even basic mean-pooling achieves 100% task ID prediction accuracy with 0% forgetting across all 7 datasets. This is the strongest single piece of evidence in the paper and a concrete, actionable contribution to the community.

2. **Comprehensive empirical scope.** The paper evaluates 9 methods spanning GNN-based, LLM-based (encoder-only and decoder-only), and GLM-based categories across 7 datasets in two continual learning settings. The systematic coverage gives the benchmark breadth that prior GCL work lacked.

3. **SimGCL achieves strong results on most datasets.** In NCIL, SimGCL achieves 84.6% vs. the next best (SimpleCIL at 70.8%) on Cora, and 82.1% vs. 66.8% on Photo. On Products, the improvement is dramatic (71.1% vs. 36.1% for the best GNN method). These margins are meaningful and demonstrate practical value.

4. **Rehearsal-free constraint is well-motivated.** The paper correctly notes that privacy and storage constraints often prevent access to historical task data, making rehearsal-free approaches practically important.

## Weaknesses

### Fatal

None.

### Major

1. **No variance or statistical significance reporting.** All results in Tables 2, 3, and 4 are reported as single numbers with no standard deviations, confidence intervals, or multiple-seed averages. For a benchmark paper where establishing reliable rankings is a primary goal, this is a significant omission. Several performance gaps between methods are modest (e.g., SimGCL at 73.5% vs. SimpleCIL at 71.4% on WikiCS NCIL; SimGCL at 68.8% vs. SimpleCIL at 73.2% on WikiCS FSNCIL), and without variance information it is impossible to assess whether these differences are meaningful or within noise. The paper's central evidence for ranking methods would be substantially strengthened by adding this information.

2. **The framing overclaims what the evidence supports.** The title asks "Can LLMs alleviate catastrophic forgetting in GCL?" which implies the LLM itself is the source of forgetting resistance. The evidence tells a more nuanced story: plain LLMs (BERT, RoBERTa, LLaMA) used without any continual learning technique perform poorly, matching or barely exceeding GNNs. What works is combining an LLM backbone with a *prototype-based architecture that does not update parameters after the first session*. The paper's own Obs. ❻ acknowledges this: "Prototype-based learning improves cross-task generalization for GNNs and LLMs." Cosine (GNN + frozen prototypes) also significantly outperforms standard GNN methods, confirming that the prototype mechanism—not the LLM per se—is the primary driver of forgetting mitigation. The paper's central finding would be more precisely stated as "LLMs provide better frozen representations than GNNs for prototype-based GCL."

### Minor

3. **SimGCL underperforms on Arxiv-23 with an incomplete explanation.** In NCIL (Table 2), SimGCL achieves 38.7% average accuracy on Arxiv-23, well below SimpleCIL's 52.4%. In FSNCIL (Table 3), the gap is even larger (31.8% vs. 49.8%). The paper attributes this to the "sparse graph structure of Arxiv-23" limiting topological information. However, SimpleCIL does not use any graph structure at all and succeeds on this dataset precisely because it ignores structure. This implies that SimGCL's ego-graph prompts are *actively harmful* on sparse graphs, injecting noise that degrades performance below what a structure-agnostic LLM method achieves. The paper does not engage with this implication, which weakens the generality of claims about SimGCL's graph-prompting design.

4. **No ablation of SimGCL's components in the main text.** SimGCL has three design choices: (a) ego-graph-derived prompts, (b) LoRA instruction tuning in the first session, and (c) training-free prototype classification. Without isolating their contributions, it is unclear which elements drive performance. Since SimpleCIL (prototype + frozen LLM, no tuning, no graph prompts) is already competitive on most datasets, the marginal value of the graph prompts and instruction tuning needs to be established. This may appear in the appendix (which was stripped by the parser), but it is absent from the main paper.

5. **The justification for excluding inter-task edges conflates edge structure with label data (Section 3.1).** The paper argues that inter-task edges are excluded during training because "real-world scenarios often prohibit access to previous task data." However, edges between old and new nodes are naturally observable (e.g., a new paper citing existing work) even when old labels are unavailable. The design choice may be reasonable, but it is not defended against the alternative of training on the full observed graph and handling leakage via regularization.

### Trivial

6. **Observation about scaling LLM parameters is overstated.** "Obs. 7" claims that "increased parameter counts consistently enhance generalization." But in Figure 3, BERT-large (439M) and BERT-medium (41.7M) show barely distinguishable performance across all sessions. The evidence within the BERT architecture family does not support a claim of consistent improvement from scaling, and the cross-architecture comparison (BERT vs. RoBERTa) confounds architecture with parameter count.

## Nice-to-Haves

- Report forgetting-forward transfer matrices or per-task accuracy trajectories to complement aggregate metrics.
- Include wall-clock time or parameter count comparisons to substantiate the "efficiency" claim for SimGCL.
- Analyze the Arxiv-23 failure case more deeply: an ablation running SimGCL without the ego-graph prompt component on Arxiv-23 would cleanly separate whether structural information helps or harms on sparse graphs.

## Removed Points

The following points from the input review were removed:

1. **Criticism about missing efficiency/wall-clock numbers.** Removed because the paper states time-efficiency analysis exists in Appendix E, which was stripped by the parser.

2. **Observation numbering glitch (❺ and ❼ missing).** Removed per the formatting/parser-artifact rule. The paper uses "Obs. 7" and "Obs. 8" in the text directly.

3. **Claim that Eq. 1 uses notation $|\mathcal{Y}_b|$ without formal definition.** The variable $b$ for session is clear from context and the text in Section 3.3 defines it. This is a marginal nitpick.

4. **The "Strengthening the Paper on Its Own Terms" suggestions** that duplicated already-captured weaknesses (ablation, variance, Arxiv-23 analysis) were merged into the weaknesses/nice-to-haves above rather than listed separately.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add variance information (standard deviations from multiple runs, at least 3 seeds) to all main result tables. This is the single most important change for the benchmark aspect of the paper.
2. Include an ablation study isolating the contributions of (a) graph prompts, (b) instruction tuning, and (c) prototype classification for SimGCL.
3. Reframe the title and central claim to better match the evidence. For example, "Do LLMs Provide Better Representations for Prototype-Based Graph Continual Learning?" or clarify that the answer is "Yes, when combined with a prototype-based architecture that freezes parameters after the first session."
4. Analyze the Arxiv-23 results more carefully: compare SimGCL with and without graph prompts on sparse datasets to determine whether structural information helps or harms.

## Score and Decision

**Round 1 bracket:** 5.5 – 6.5

**Anchor papers used for calibration:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4sJJixGIZX.md` (Online Continual Graph Learning) | 5.00 | R1 bracketing | Less contribution — no method, no evaluation flaw identification |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/PQStRgYfuJ.md` (Topology-aware Embedding Memory) | 5.40 | R1 bracketing | Has theory + method but memory claim unvalidated; our paper's empirical work is more grounded |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RnxwxGXxex.md` (CLDyB) | 5.67 | R1 bracketing | Benchmark paper accepted at similar venue; our paper has extra contributions (flaw ID + method) |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/om5z1n0mXA.md` (Rethinking Graph Classification Datasets) | 6.00 | R2 narrowing | Similar evaluation-flaw critique; rejected for limited novelty; our paper has more contributions |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/g90RNzs8wX.md` (Unifying GLAD/GLOD) | 6.50 | R2 narrowing | Benchmark paper accepted with expected findings; our paper has stronger novel findings |

**Final score determination:** The paper's core contributions — identifying the task-ID leakage flaw, providing a comprehensive benchmark, and demonstrating that LLM backbones with prototype-based classification achieve strong GCL results — are genuine and valuable. The task-ID leakage finding alone is a significant service to the community. SimGCL's results on most datasets are impressive. However, the absence of any variance/statistical significance reporting is a meaningful gap for a benchmark paper that aims to establish method rankings, and the framing overstates what the evidence supports. Compared to accepted benchmarks at similar venues (e.g., CLDyB at 5.67, Unifying GLAD/GLOD at 6.50), this paper has stronger novel findings but also more notable weaknesses. The net assessment places it in the borderline accept range.

**Calibrated score: 6.0** — The paper has real contributions that warrant publication, but the lack of statistical rigor in the core benchmarking results and the framing gap are notable issues that prevent a higher score and require attention.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>