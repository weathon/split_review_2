Now let me write the final consolidated review.

## Summary

The paper identifies and formalizes the Dual-level Noisy Correspondence (DNC) problem in multi-modal entity alignment (MMEA), where noisy correspondences exist at both intra-entity (entity-attribute) and inter-graph (entity-entity and attribute-attribute) levels. The proposed method, RULE, addresses this through: (1) a two-fold reliability estimation (uncertainty + consensus) that divides pairs into clean, uncertain, and low-consensus subsets; (2) a dually robust loss (DRL) with tailored training strategies for each subset; (3) a robust fusion mechanism (DRF) that weights attributes by estimated reliability; and (4) a test-time correspondence reasoning (TTR) module using an MLLM with chain-of-thought to uncover latent attribute-attribute connections. Experiments on five benchmarks across three noise levels show consistent improvements over seven baselines.

## Strengths

1. **Problem identification is well-motivated and practical.** The paper is the first to explicitly study noisy correspondences at both intra-entity and inter-graph levels in MMEA. The concrete examples (Elvis Tsui/Jason Momoa visual confusion, Mr. & Mrs. Smith entity confusion) ground the problem in real annotation failure modes, and the claim that real ICEWS benchmarks contain over 50% noise makes the problem urgent rather than academic.

2. **The uncertainty + consensus two-fold principle is theoretically thoughtful.** Theorem 1 correctly identifies that low uncertainty alone is insufficient (an entity could be confidently matched to the wrong counterpart). Adding consensus as a second principle directly addresses this gap and leads to a clean three-way partition (S_U, S_I, S_C) with tailored loss treatments for each subset. This is a principled design rather than a bag of heuristics.

3. **Ablation is well-structured and informative.** Table 3 cleanly separates train-stage and test-stage contributions. The "w/o DRL" baseline (Non-name H@1 dropping from 58.2 to 31.6) establishes that the dually robust loss is doing the heavy lifting, while comparing "MLLM Enhance" vs. "w/o TTR" isolates the incremental value of test-time reasoning (+1.7 H@1 on Non-name).

4. **Results are strong and consistent across noise levels.** On ICEWS datasets in the Non-name setting, RULE outperforms all seven baselines by substantial margins (e.g., H@1 of 64.2 vs. next-best 52.6 on ICEWS-WIKI under inherent DNC — an 11.6-point gap). The performance degradation curve under increasing noise (Fig. 3a) is markedly shallower than any baseline, which is exactly the right evidence for a method claiming robustness.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Ablation is limited to a single dataset (ICEWS-WIKI).** The paper explicitly states this on line 304. The relative contribution of components (especially the TTR module and the DRF module) may vary across datasets with different noise structures, modality characteristics, and baseline performance levels. On DBP15K datasets, where Non-name H@1 is already in the 80s for several methods, the TTR module could provide a smaller or larger relative gain than the 1.7-point improvement shown on ICEWS-WIKI. Ablation results on at least one additional dataset (preferably from the DBP15K family) are needed to establish that the ablation conclusions generalize.

2. **No variance or significance reporting.** Results in Tables 1-2 are reported as point estimates without standard deviations or significance tests. Given that some inter-method gaps are modest (e.g., 0.2–0.5 points on some DBP15K All-attributes settings), it is unclear whether these differences are stable. At minimum, results over multiple runs (or a note on whether a single run was used) should be reported.

3. **Computational cost of the TTR module is not discussed.** The method uses Qwen2.5-VL-72B-Instruct (72B parameters) for test-time reasoning with chain-of-thought over candidate entities. No information about inference time per query, total GPU-hours, or API cost is provided. Since the TTR module contributes meaningful gains (3.7 points on All-attributes H@1 under 50% DNC in Table 3), practitioners need this information to assess whether the performance gains justify the expense. This omission does not affect validity but is important for a methods paper whose contribution includes a test-time component.

4. **The self-adaptive pair-division threshold has a circular dependency.** The thresholds β_u and β_c in Eq. 8 depend on S^TP = {i | argmax(s_i) = argmax(y_i)}, which is defined using the model's own predictions. At high noise levels (50%+), these predictions may themselves be corrupted, and the paper does not analyze how the quality of the S_U/S_I/S_C division degrades with noise. Reporting precision/recall of the pair division at different noise levels would strengthen this component.

5. **Several design choices in the consensus estimation lack justification.** The initial subset size |π_0| = ⌊M/2 + 1⌋ (Eq. 7) and the use of max in the value function v(π) (Eq. 6) are presented without theoretical rationale or empirical sensitivity analysis. The paper references Appendix F.3, which is stripped, but these choices appear somewhat arbitrary as presented.

6. **The reliability estimation's internal dependency is not clarified.** Training-time reliability estimates (w_i^m) depend on the current entity representations (z_i), which in turn depend on the fusion weights (w_i^m). The paper does not discuss whether estimation and fusion are updated alternately or jointly, or whether convergence is affected by this circularity.

7. **The headline results include contributions from the TTR module without quantifying its system-level asymmetry.** While the ablation (Table 3) shows that even without TTR, RULE's training components outperform baselines (e.g., 56.5 vs. 52.6 Non-name H@1 on ICEWS-WIKI 50% DNC), the main tables present numbers that include the full 72B MLLM. All baselines use only CLIP-scale models. Making the non-TTR results more prominent in the main table (or comparing against MLLM-augmented baselines) would give readers a clearer picture of what the training-time framework alone achieves.

### Trivial

- The formal definition of attribute-attribute correspondence (line 54) means entity-entity noise automatically cascades to attribute-attribute noise by definition. This is a deliberate and reasonable modeling choice but should be explicitly noted.

## Nice-to-Haves

- Present results without TTR as a primary row in the main tables (not just ablation), so readers can assess the training-time contribution independently.
- Provide a comparison where baselines are also augmented with the same MLLM (even if only for re-ranking without CoT), to establish that the *way* RULE uses the MLLM matters.
- Clarify whether reliability estimation and fusion are updated alternately or jointly during training.

## Removed Points

These points were flagged by the harsh critic but are removed from the main review for the following reasons:

- **"DBP15K_GEN label in Table 2"**: This is a parser artifact from PDF extraction, not an author error. The submitted PDF presumably uses the correct ZH-EN/JA-EN/FR-EN labels. (Hard rule: formatting artifacts.)
- **"Hyperparameters λ=1e^{-4} and β=0.3 fixed without tuning"**: The paper explicitly references Appendix G.10 for sensitivity analysis of these parameters. The appendix was stripped from the parsed version; this is not an author omission. (Hard rule: stripped appendix content.)
- **"TTR asymmetry is a critical/fatal flaw"**: The paper already provides ablation showing the method without TTR (Table 3), and even without TTR, RULE's training components outperform baselines. The asymmetry is a legitimate concern but not fatal, as the ablation cleanly separates contributions. Demoted to Minor weakness #7.
- **"The paper should clarify Section 2.1 cascading noise"**: The critic acknowledges this is "deliberate and reasonable." It is a clarification, not a weakness. Moved to Trivial.

## Novel Insights

The insight that low uncertainty alone is insufficient for detecting noisy correspondences (Theorem 1) — because an entity could be confidently matched to the *wrong* counterpart — is the key theoretical observation. It directly motivates the consensus principle and the three-way pair partition, which is the conceptual core of the training-time framework. The observation that seemingly dissimilar but inherently identical attributes (the Cristiano Ronaldo/Mexico example in Fig. 1c) cause test-time misidentification is also a genuine insight that motivates the TTR module. None of the other insights from the reviews go beyond what the paper itself articulates.

## Suggestions

1. Run the ablation study (Table 3) on at least one DBP15K dataset to verify that component contributions generalize beyond ICEWS-WIKI.
2. Add standard deviation or confidence intervals for all main results, or note explicitly if they are single-run.
3. Analyze and report the precision/recall of the S_U/S_I/S_C pair division at different noise levels to validate the self-adaptive threshold.
4. Report the computational cost of the TTR module (inference time per query, total GPU-hours, or API cost).
5. Add a row to the main tables showing RULE without TTR, so readers can directly assess the training-only contribution.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>

**Calibration**: I retrieved 24 anchor papers across six score bands using `calibration_search`. The most informative anchors for comparison are:

| Anchor | Avg Score | Comparison |
|--------|-----------|------------|
| Revisit and Outstrip Entity Alignment (z3dfuRcGAK) | 6.67 (Accept) | Entity alignment paper with novel theoretical framing (M-VAE for entity synthesis) but limited experiments. RULE has stronger experimental evaluation (5 datasets, 3 noise levels vs. single setting) and a more clearly motivated problem, making it comparable or slightly stronger. |
| Neuro-symbolic Entity Alignment (NNUiUwQWx6) | 5.75 (Reject) | Another EA paper with a neuro-symbolic framework. Rejected partly due to insufficient complexity analysis and hyperparameter sensitivity concerns. RULE's experiments are more comprehensive and its ablation is cleaner. |
| MOFI: Noisy Entity Annotations (QQYpgReSRk) | 6.25 (Accept) | Large-scale noisy-label vision-language model with limited technical novelty. RULE has stronger technical novelty (the two-fold principle) but is evaluated at a much smaller scale. Comparable quality. |
| Multi-granularity Correspondence Learning (9Cu8MRmhq2) | 8.00 (Accept) | Also addresses noisy correspondence but with more rigorous evaluation and no asymmetric comparison issues. RULE's problem framing is equally novel but its evaluation has more gaps (single-dataset ablation, no variance), placing it below this level. |
| Test-time Adaptation: Multi-modal Reliability Bias (TPZRq4FALB) | 8.00 (Accept) | Very clean, well-motivated paper with extensive evaluation. RULE addresses a related but different problem (noisy correspondence vs. distribution shift). RULE's evaluation is less complete. |

**Initial bracket (Round 1)**: Narrowest plausible range was [5.5, 7.5]. After comparing against the rejected 5.75 anchor (which had similar-scale experiments on entity alignment but weaker motivation) and the accepted 6.25–6.67 anchors (which had comparable or weaker problem framing but fewer evaluation gaps), I settled on 6.5. The paper's most significant evaluation gaps (single-dataset ablation, no variance reporting, unquantified TTR cost) prevent it from reaching the 7.5–8.0 range of the top-cited papers, but its novel problem identification, principled methodology, and strong results clearly place it above the reject-level 5.75 anchor.