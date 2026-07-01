Now let me write the final consolidated review.

## Summary

This paper identifies a genuine flaw in prior Graph Continual Learning (GCL) evaluation—task ID leakage in local testing—and proposes LLM4GCL, a benchmark that evaluates 9 LLM/GLM methods across 7 text-attributed graph datasets under a corrected global-testing protocol. It also introduces SimGCL, a method combining first-session LoRA fine-tuning with ego-graph prompts and training-free prototypes, which achieves strong results on several datasets.

## Strengths

1. **Task ID leakage diagnosis (Section 3.1, Table 1).** The demonstration that simple mean pooling achieves 100% task ID prediction accuracy and 0% forgetting under local testing is clean and compelling. This identifies a real flaw that invalidates prior GCL evaluation results and provides strong motivation for adopting global testing.

2. **Breadth of the benchmark.** Evaluating 9 methods (GNN, LLM, GLM) across 7 datasets under two CL paradigms (NCIL and FSNCIL) fills a genuine gap—no prior work systematically evaluated LLMs for GCL. The standardized protocols and code release are practical contributions.

3. **SimGCL results are strong on several datasets.** On Cora (84.6% vs. 70.8% SimpleCIL), Photo (82.1% vs. 62.1%), and Products (71.1% vs. 66.8%), the improvements are substantial. The ego-graph prompt design is well-motivated by the cross-modal alignment issues observed in other GLMs.

## Weaknesses

### Major

1. **SimGCL backbone LLM is not specified for the main results (Tables 2, 3).** The paper never states which backbone model produced the headline numbers in the main comparison tables. Figure 3 tests SimGCL with multiple backbones (BERT variants, RoBERTa-large) but only on one dataset (Arxiv) and for a subset of settings. Without knowing the backbone used in Tables 2 and 3, the core comparison is uninterpretable: the reported gains over SimpleCIL could be driven by model scale rather than method design. SimpleCIL is specified as using "RoBERTa" but not which variant (base vs. large). This is a fundamental reproducibility gap.

2. **No statistical variance reported for any result (Tables 2, 3, 4).** Every number is a single-point figure with no standard deviation, no indication of multiple runs, and no description of how many random seeds were used. Given known LLM inference variability (temperature effects, LoRA training stochasticity, seed sensitivity), single-point numbers do not constitute sufficient evidence for the claimed improvements. This applies to both the proposed method and all baselines.

### Minor

3. **Title/abstract center on "catastrophic forgetting" but main experiments do not measure forgetting.** The paper asks whether LLMs can *alleviate catastrophic forgetting*, yet Tables 2 and 3 report only average accuracy (Ā) and final accuracy (A_N)—neither is a forgetting metric. The forgetting ratio (AF) appears only in Table 1 (the local-testing critique). Adding per-task backward transfer or average forgetting would directly address the paper's central question and clarify whether SimGCL's advantage is in accuracy, forgetting, or both.

4. **No ablation isolating SimGCL's components.** SimGCL differs from SimpleCIL in (a) ego-graph-derived text prompts vs. text-only prompts, and (b) first-session LoRA instruction tuning vs. frozen backbone. Without an ablation separating these, it is impossible to determine whether the prompt design or the tuning is the main driver of improvement, or whether the method could be simplified.

5. **Selective reporting of the "~20% improvement."** The abstract and contributions claim "an absolute increase of nearly 20%." But on Arxiv-23, SimGCL (38.7/13.6) is substantially below SimpleCIL (52.4/38.8). The improvement is not uniform across settings, and the headline number overstates the method's general advantage.

6. **τ (scaling hyperparameter in Equation 2) is never quantified.** Its value and selection procedure are not reported, which is a minor reproducibility gap.

### Trivial

- Observation numbering in Section 4 is inconsistent (❶❷❸❹ then ❻ then ❽ then 7, 8), suggesting hasty editing.

## Nice-to-Haves

- Report forgetting metrics (AF or backward transfer) in Tables 2 and 3.
- Add ablation experiments separating prompt design from LoRA tuning (e.g., SimGCL with text-only prompts + LoRA, and ego-graph prompts + frozen backbone).
- Report τ and its selection method.
- The paper's inter-task edge exclusion (Section 3.1) is justified for privacy-preserving rehearsal-free settings but likely disadvantages GNN methods more than LLM methods; a brief discussion of this asymmetry would strengthen the evaluation.

## Removed Points

These points from the harsh critic input are removed as they are not valid weaknesses:

- **"Existing methods trained from scratch" criticism**: The critic misreads the sentence—line 15-16 refers to existing GCL methods (GNN-based), not LLMs. The context makes this clear.
- **Equation (1) notation critique**: The critic claims the sum index is wrong, but the notation is standard—summing over labeled nodes indexed 1 to |Y_b|.
- **Disjointness assumption**: Standard in class-incremental learning; criticizing it is scope creep.
- **Observation 7 being "well-known"**: The paper reports an empirical finding; this is not a weakness—it is a descriptive observation.
- **Missing baseline checkpoint details**: Standard to cite the source papers.
- **Reproducibility concerns about undisclosed hyperparameters beyond τ**: The appendix (removed by parser) likely contains implementation details.
- **Observation numbering inconsistency is not a formatting nitpick**: It's kept but downgraded to Trivial.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **State the SimGCL backbone for every main experiment.** Specify the exact model (architecture and parameter count) used in Tables 2 and 3. Ideally, also report SimGCL results with multiple backbones in the main comparison (as in Figure 3 but extended to all datasets).
2. **Report standard deviations from multiple runs (≥3 seeds) for all main results.**
3. **Add a forgetting metric** (e.g., average forgetting AF from Table 1) to Tables 2 and 3 to directly address the title's question.
4. **Add ablations** that decompose the contributions of ego-graph prompts and LoRA tuning.

## Score and Decision

**Round 1 Bracket:** 3.0 – 6.0

**Calibration anchors:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4sJJixGIZX.md` — "Online Continual Graph Learning" (avg 5.00, Reject) — Also a GCL benchmark paper with a new framework, but criticized for lacking a novel method. Current paper has stronger contributions (task ID leakage + method) but weaker empirical transparency (missing backbone).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/PQStRgYfuJ.md` — "Topology-aware Embedding Memory" (avg 5.40, Reject) — Solid experimental evidence with variance, but limited novelty. Current paper has stronger conceptual contribution but weaker reporting.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RnxwxGXxex.md` — "CLDyB" (avg 5.67, Accept) — Benchmark paper with clear framing. Current paper has more severe reporting gaps (no backbone specified, no variance).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eXrUdcxfCw.md` — "Continual Test-Time Adaptation" (avg 4.80, Reject) — Method paper with prototype approach. Similar type of weakness (no variance reported).

The paper has a genuine and valuable core contribution (task ID leakage diagnosis), but the missing backbone specification makes its main empirical claims unverifiable, and the lack of statistical variance undermines the reported comparisons. These issues are fixable but prevent the paper from meeting the bar for acceptance in its current form.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>