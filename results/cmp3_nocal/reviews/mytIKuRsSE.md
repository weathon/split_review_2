## Summary

The paper identifies and formalizes Dual-level Noisy Correspondence (DNC) in Multi-modal Entity Alignment — noise in both intra-entity (entity-attribute) and inter-graph (entity-entity, attribute-attribute) correspondences — and proposes RULE. RULE uses a two-fold reliability principle (uncertainty via Dempster-Shafer Theory / Dirichlet evidence, plus consensus via similarity-to-annotation agreement) to partition pairs into clean, uncertain, and inconsistent subsets. It then applies a dually robust loss and reliability-weighted fusion to mitigate noise during training, and a test-time correspondence reasoning (TTR) module using Qwen2.5-VL-72B to further refine alignment.

## Strengths

1. **Novel and well-motivated problem formulation.** The DNC problem — simultaneous noise in intra-entity and inter-graph correspondences — is genuinely under-explored in MMEA. The paper provides concrete examples (Fig. 1) and cites empirical evidence that real benchmarks contain over 50% DNC, making a convincing case that this is not an incremental problem statement.

2. **Principled two-fold reliability estimation.** The combination of uncertainty (via Dirichlet evidence / Dempster-Shafer Theory) and consensus (via similarity-to-annotation agreement) is theoretically grounded. Theorem 1 correctly identifies the limitation of using uncertainty alone — low uncertainty does not imply correct annotation — and the consensus term explicitly addresses this gap. The scatter plot in Fig. 4 validates that the joint design cleanly separates the three subsets (S_U, S_I, S_C).

3. **Consistently strong empirical results across an extensive evaluation grid.** RULE outperforms 7 baselines on 5 datasets under 2 evaluation protocols and 3 noise levels (inherent, 20%, 50%) — 15 distinct experimental conditions for each of two protocols. Gains are often large (e.g., 58.2 vs. 42.4 H@1 on ICEWS-WIKI Non-name at 50% DNC).

4. **Ablation study isolates the main contributions.** Table 3 shows that removing Dually Robust Loss (DRL) drops Non-name H@1 from 58.2 to 31.6, and removing Dually Robust Fusion (DRF) drops it to 50.4. These large margins confirm that the training-time robustness mechanisms carry the bulk of the improvement.

## Weaknesses

### Fatal
None.

### Major

- **Unexplained inconsistency in the TTR module's effectiveness across protocols.** From Table 3, using only the MLLM re-ranking scores ("MLLM Enhance") improves over "w/o TTR" by only **0.1 H@1** on Non-name (56.5→56.6) but by **3.6 H@1** on All-attributes (94.0→97.6) — a dramatic difference that is not discussed or analyzed. The paper claims the TTR module "significantly improves alignment performance by uncovering latent semantic connections," but the Non-name results suggest the MLLM adds essentially nothing when entity names are unavailable. Understanding when this module helps and when it does not is essential for assessing the method's general utility and for readers to interpret the main results correctly.

### Minor

- **The "same backbone" framing conflates training-time and test-time contributions.** Section 3.2 states "For fair comparisons, we adopt the same backbone (i.e., CLIP) for all baselines and our method." This is accurate for feature extraction, but the reported "Ours" results in Tables 1–2 include the TTR module, which uses Qwen2.5-VL-72B — a 72B MLLM that none of the baselines have access to at inference. While the paper is transparent about using this model (Section 3.1) and the ablation (Table 3) shows that even w/o TTR, RULE beats all baselines by wide margins (e.g., 56.5 vs. 52.5 H@1 on Non-name), the main comparison does not flag this asymmetry. The core training-time contribution is strong enough on its own; the presentation would benefit from making this separation clearer.

- **No variance or statistical significance reported.** Across all experiments (7 baselines × 5 datasets × 3 noise levels × 2 protocols), not a single confidence interval, standard deviation, or statistical test is reported. On the Non-name setting, margins are large enough that significance seems plausible. But on the All-attributes setting at 50% DNC, where baselines reach 91.9–94.7 H@1 and RULE achieves 97.7, the gaps are smaller and variance matters. Reporting means over multiple random seeds is standard practice for empirical ML papers.

- **Assumption 1 (marginal contribution for consensus estimation) is unverified.** The greedy strategy for estimating correct correspondences at inference (Eq. 6–7) relies on Assumption 1 — that correct attributes have Δ ≥ 0 and incorrect ones have Δ < 0. No theoretical or empirical analysis is provided for when this assumption might break (e.g., when multiple attributes are jointly noisy but individually appear beneficial). While a reasonable heuristic, a brief discussion of its limitations would strengthen the paper.

### Trivial
None.

## Nice-to-Haves

- **Hyperparameter sensitivity:** λ = 1e-4 and β = 0.3 are fixed across all datasets. A sensitivity plot for one dataset would establish robustness.
- **Expand w/o TTR results to all datasets:** Table 3 reports w/o TTR only on ICEWS-WIKI at 50% DNC. Reporting w/o TTR across all five datasets would cleanly separate the core method's contribution from the MLLM augmentation.
- **Baseline with MLLM re-ranking:** Applying the same Qwen2.5-VL-72B to baselines' output rankings would isolate whether training-time robustness drives the gains or whether any method benefits similarly from MLLM re-ranking.
- **Computational cost:** The paper uses a 72B-parameter MLLM at test time; reporting GPU-hours or inference latency would inform practitioners about real-world applicability.

## Removed Points
Points from the input review that were removed with justification:
- **MLLM prompting details in the appendix:** The parser strips appendix content; these details exist in the original submission. Removed per instruction.
- **Missing Related Work section:** May be in stripped portions; cannot verify absence from the parsed file alone. Removed per instruction.
- **Table 2 garbled column headers ("DBP15K <sub>GEN</sub>"):** Parser artifact, not a paper presentation issue. Removed per instruction.
- **Fig. 1(b) not being a controlled experiment:** The figure is presented as motivation/illustration ("Observations"), not as a formal comparison. Removed as a strawman.
- **Criticism that methods cited may not be available:** All cited works are assumed released per guidelines. Removed per hard rules.

## Novel Insights
"None beyond the paper's own contributions."

## Suggestions

1. **Reorganize the main comparison** to clearly separate the core training-time method (DRL + DRF) from the MLLM-based test-time augmentation. Either report RULE w/o TTR as the primary method with TTR as a separate augmentation table, or explicitly annotate Tables 1–2 to indicate which results include the MLLM.

2. **Analyze the TTR module's behavior** across the two protocols. A brief discussion (or small table) explaining why the MLLM-only re-ranking gains are 0.1 H@1 on Non-name vs. 3.6 H@1 on All-attributes would help readers understand the module's value proposition and limitations.

3. **Add statistical reporting** — at minimum, report means and standard deviations over 3 random seeds for the main experimental conditions in Tables 1–2.

4. **Discuss the limitations of Assumption 1** and the greedy consensus strategy — even a brief caveat about when noisy attributes could individually pass the Δ ≥ 0 test would strengthen the methodological exposition.

---

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>