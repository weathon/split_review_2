Now let me compose my final integrated review.

## Summary

This paper investigates whether LLMs can mitigate catastrophic forgetting in Graph Continual Learning (GCL). It makes three main contributions: (1) identifying a task-ID leakage flaw in the widely-used "local testing" evaluation protocol for Node-level Class-Incremental Learning; (2) introducing LLM4GCL, a benchmark evaluating 9+ LLM/GLM-based methods across 7 text-attributed graphs under two paradigms (NCIL and FSNCIL); and (3) proposing SimGCL, a method combining first-session graph-prompted instruction tuning (LoRA) with training-free prototype matching for subsequent sessions.

## Strengths

- **Clean identification of a genuine evaluation flaw (Section 3.1, Table 1).** The paper demonstrates convincingly that the commonly-used "local testing" protocol in NCIL inadvertently leaks task IDs. Table 1 shows that even simple mean-pooling achieves 100% task ID accuracy and 0% forgetting—matching the prior SOTA method TPP—and even an MLP without graph structure produces comparable results. This is a clean, reproducible finding that calls into question a non-trivial portion of prior GCL evaluation work and stands as a legitimate contribution regardless of the paper's other elements.

- **Comprehensive empirical scope.** The benchmark evaluates 9+ methods across 7 datasets spanning multiple domains (citation, web link, e-commerce), two learning paradigms, and multiple session/class configurations. Design choices—removing inter-task edges, handling label imbalance, adopting global testing—are principled and well-motivated. This is a solid benchmarking effort that should be useful to the community.

- **SimGCL is clean and principled in design.** The method (first-session instruction tuning with LoRA + training-free prototype matching) is simple, interpretable, and directly addresses the core tension in continual learning. On datasets where it works well (Cora, Citeseer, Photo, Products), the gains over non-graph LLM baselines are substantial (e.g., 84.6 vs. 70.8 AA on Cora NCIL).

## Weaknesses

### Fatal
None.

### Major

- **SimGCL underperforms the simpler, graph-unaware SimpleCIL on the Arxiv-23 dataset by large margins (38.7 vs. 52.4 AA in NCIL; 31.8 vs. 49.8 AA in FSNCIL) and on Arxiv FSNCIL (36.3 vs. 46.4 AA).** The paper's explanation attributes this to "sparse graph structure" (Obs. ❽), but SimpleCIL does not use graph structure at all and performs substantially better, so the explanation does not account for why adding graph information actively hurts performance. This means the claimed benefit of graph-aware instruction tuning does not hold universally, and the paper does not establish what property of the graph determines when it helps vs. hurts. The lack of a principled characterization of SimGCL's failure boundary undermines confidence in the method's generality.

- **No ablation isolating the role of graph structure vs. instruction tuning.** SimGCL differs from SimpleCIL in two ways simultaneously: (1) LoRA instruction tuning on the first session, and (2) ego-graph-derived prompts encoding graph structure. Without an ablation that separates these factors (e.g., SimpleCIL → SimpleCIL + instruction tuning (text-only) → SimGCL), the paper's attribution of gains to "topological understanding" (Section 3.3) is speculative. The improvements could primarily come from first-session fine-tuning alone—which any LLM baseline could incorporate—rather than from graph-structural information.

- **No variance or statistical significance reporting.** None of the tables report standard deviations, confidence intervals, or number of runs. LLMs can be sensitive to seed (especially with LoRA tuning), and some of the smaller claimed improvements (e.g., 1.5–3.1 point gaps on WikiCS in both paradigms) could fall within variance. The complete absence of uncertainty measures weakens the evidence for all reported comparisons, which is particularly important for a benchmark paper that future work will cite as a reference.

### Minor

- **The "around 20% improvement" claim in the abstract and contributions (Section 1) compares against GNN-based SOTA, but the simpler LLM baseline SimpleCIL also achieves substantial improvements over the same GNN baselines (e.g., 70.8 vs. 65.4 on Cora).** The more informative comparison—SimGCL vs. the best LLM baseline (SimpleCIL)—tells a more mixed story: large gains on some datasets and significant losses on others. The framing somewhat overstates what is uniquely attributable to SimGCL's design vs. the general advantage of using LLMs.

- **No limitations section and limited discussion of failure modes.** The paper acknowledges the Arxiv-23 shortfall in Obs. ❽ but does not deeply analyze why graph information hurts there. The hyperparameter τ in Eq. (2) is mentioned only as a "scaling hyperparameter controlling the weight distribution" with no discussion of how it was set, whether results are sensitive to it, or whether it varies by dataset.

### Trivial

- The observation numbering has gaps (❶→❷→❸→❹→❻→❽→7→8, with ❺ and ❼ missing and inconsistent formatting between circled and uncircled numerals).

## Nice-to-Haves

- An ablation study with four conditions: SimpleCIL (frozen, text-only), SimpleCIL + instruction tuning (text-only), SimpleCIL + instruction tuning (graph-prompted), and full SimGCL. This would directly isolate whether gains come from fine-tuning or graph information.
- A systematic analysis correlating graph properties (density, homophily, degree distribution) with SimGCL's relative improvement over SimpleCIL to characterize when graph information helps vs. hurts.
- Sensitivity analysis for the τ hyperparameter in Eq. (2).

## Removed Points

These points from the input review are removed (full details preserved for reference but not included in the assessment):

- The harsh critic's claim that SimGCL underperforms SimpleCIL on **Arxiv NCIL** specifically — in Table 2 (NCIL Arxiv), SimGCL achieves higher AA (59.9 vs. 50.6) even though AN is slightly lower (33.8 vs. 36.5). The claim is partially inaccurate as stated.
- Generic framing of the problem as "important" — removed as not specific enough.
- The harsh critic's recommendation framing ("Accept on the strength of...") — this is a recommendation, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add the four-condition ablation study described above to isolate the effect of graph structure from instruction tuning.
2. Report results with standard deviations over multiple random seeds (at least 3 runs).
3. Add a systematic analysis correlating graph properties with SimGCL's relative performance to turn the Arxiv-23 failure into a source of insight about boundary conditions.
4. Include a limitations section discussing when SimGCL is expected to underperform baselines.
5. Discuss the τ hyperparameter: how it was set, sensitivity analysis, and whether it varies per dataset.

## Score and Decision

**Round-1 bracket estimate: 5.0 – 6.5.** Based on comparing to anchors: Online Continual Graph Learning (avg 5.0, rejected) had a similar scope (GCL benchmark) but weaker contributions; CLDyB (avg 5.67, accepted) had comparable contribution magnitude; TiC-LM (avg 6.25, rejected) had a larger-scale benchmark but was criticized for lacking novel findings; How Do LLMs Understand Graph Patterns (avg 7.0, accepted) had thorough evaluation but fewer substantive weaknesses. Our paper sits between the 5.0 and 5.67 anchors in terms of overall contribution-to-weakness balance.

**Round-2 narrowing:** Comparing favorability-rated items against CLDyB (accepted at 5.67) and OCGL (rejected at 5.0): Our paper's strongest item (task-ID leakage, favorability 8.56) is stronger than CLDyB's top strengths. However, our weakest item (SimGCL failure on Arxiv-23, favorability -2.59) is more negative than any weakness in CLDyB (whose most negative was ~1.34). This places the paper below CLDyB's 5.67 in net assessment. The paper is above OCGL (5.0), which had weaker contributions (no novel method, no evaluation flaw discovery) and comparable methodological issues. The missing ablation and variance reporting are substantive gaps that, while not fatal to the paper's strongest contribution, prevent confident validation of the method claims.

**Final score: 5.5.** The paper makes a genuine, independently-valuable contribution (the task-ID leakage finding) and provides a useful benchmark. However, the SimGCL method validation has three significant gaps—unexplained failure on a key dataset, missing ablation, and no variance reporting—that prevent full acceptance. The paper would benefit substantially from revisions addressing these issues.

**Anchors consulted:**
| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4sJJixGIZX.md | 5.00 | R1 | Yes | OCGL (GCL benchmark, no novel method or flaw discovery) — our paper is stronger |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/MB53uAZKSc.md | 6.25 | R1 | Yes | TiC-LM (larger-scale benchmark, but criticized for lacking novel findings) — our paper has more novel findings |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CkKEuLmRnr.md | 7.00 | R1 | Yes | LLM Graph Pattern benchmark (accepted, comprehensive evaluation, fewer substantive weaknesses) — our paper is weaker |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RnxwxGXxex.md | 5.67 | R2 | Yes | CLDyB (dynamic CL benchmark, accepted, comparable contribution but fewer major weaknesses) — our paper is slightly weaker |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/PQStRgYfuJ.md | 5.40 | R2 | Yes | TEM for GCL (rejected, had memory explosion solution but limited novelty) — comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aqvf3R48pl.md | 4.40 | R1 | No | Data Efficient CL of LLMs — less relevant |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rwmwFnmjAX.md | 4.75 | R1 | No | Continual LLaVA — different domain |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5twh6pM4SR.md | 5.33 | R2 | No | Automating CL — different approach |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JIlIYIHMuv.md | 2.50 | R1 | No | LVLM-CL — different domain |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/h5xc46rWcZ.md | 3.00 | R1 | No | Lost-in-Distance — different focus |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gNoqEdT2wO.md | 2.33 | R1 | No | Multimodal CIL benchmark — different domain |

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>