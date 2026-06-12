## Summary
This paper introduces PI-CCA (Prompt-Invariant CCA Certificates), a replay-free continual learning framework for vision-language models that preserves cross-modal alignment by maintaining a compact "certificate" of top-k canonical correlations and subspaces via random sketches. The method constrains spectral and subspace-angle invariants during adaptation using only mini-batch statistics, achieves prompt robustness through projector averaging over perturbations, and demonstrates state-of-the-art results among replay-free methods across four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL).

## Strengths
- **Novel conceptual reframing**: Treating VL-CL forgetting as alignment-geometry drift rather than proxy signal matching (logits, similarities, parameters) is a genuine insight. Prior work (ZSCL, Mod-X, CTP, DKR) regularizes outcomes; PI-CCA targets the invariants of the whitened cross-modal covariance directly. This is a principled and elegant perspective.

- **Constant-memory, replay-free design**: The certificate stores only k canonical correlations and h×k sketched bases (e.g., (64,256) yields tiny memory), avoiding generators, replay buffers, or teacher ensembles. This is practically important given privacy/licensing constraints on real VLM deployments.

- **Comprehensive experimental evaluation**: Experiments span four diverse tracks—classification (MTIL, X-TAIL), retrieval (VLCL), and structured concepts (ConStruct-VL)—with consistent SOTA among replay-free methods. Table 1 shows improvements over 10+ strong baselines; Table 2 shows PI-CCA even outperforming the synthetic-replay method GIFT on retrieval.

- **Thorough ablations and analyses**: Table 3 systematically isolates each component's contribution (spectral, subspace, prompt invariance, EMA variants, sketch types, pairing surrogates). The geometry→performance correlation analysis (Fig 3) and prompt invariance stress tests (Fig 4) provide genuine explanatory value beyond pure benchmark numbers. Task-order sensitivity over 20 random permutations (Fig 5) with narrow IQRs strengthens confidence.

## Weaknesses
### Fatal
None.

### Major
- **Margin over strongest baselines is sometimes narrow**: On MTIL, PI-CCA (76.8) vs. C-CLIP (75.2) and DIKI (74.9) yields ~1.6–1.9 pp gains; on X-TAIL, PI-CCA (68.1) vs. RAIL (67.4) gives 0.7 pp. While consistent across benchmarks, these margins are modest and leave open whether the geometric regularization provides substantial practical gains beyond what well-tuned proxy methods already achieve.

- **Suspiciously perfect geometry–performance correlations**: All four panels in Figure 3 report Pearson r=1.00 and Spearman ρ=1.00. Perfect correlation across multiple scatter plots with presumably diverse perturbation types is extraordinary and warrants deeper scrutiny. If the perturbation sweep is small or the drift metric is definitionally tied to the outcome, the analysis may be circular rather than independently predictive.

- **Streaming EMA covariance validity under severe domain shift**: The method relies on EMA-smoothed covariance matrices (Eq 12) to track alignment over time. Under large domain shifts (e.g., from natural images to satellite or medical imagery), the EMA may blend incompatible statistics, and the paper does not characterize when this assumption breaks down or how to detect/correct such failures.

### Minor
- **Prompt perturbation distribution underspecified**: The distribution P over δ is referenced but not formally characterized in the main text. The stress test mentions "token-level synonym swap/back-translation/template jitter ratio" with strength s∈[0,1], but the exact mechanism, vocabulary size, and how s maps to perturbation severity are unclear without consulting the appendix.

- **Task-order sensitivity is tested only on MTIL**: The 20-order evaluation (Fig 5) covers only MTIL. VLCL and ConStruct-VL may have different sensitivity profiles, especially since retrieval and structured tasks have different task structures.

- **No analysis of failure modes**: The paper does not discuss cases where PI-CCA underperforms or when the CCA approximation (top-k SVD of batch statistics) may be unreliable (e.g., very small batches, high-dimensional settings with few samples).

### Trivial
None beyond parser artifacts.

## Nice-to-Haves
- A comparison of wall-clock training time and total compute against baselines would strengthen the efficiency narrative.
- Analysis of how performance degrades as the number of sequential tasks grows much beyond 11 (the current maximum).
- Discussion of sensitivity to LoRA rank and whether the method's gains are orthogonal to adapter capacity.

## Novel Insights
The core insight—that VL-CL forgetting is better understood as drift of the canonical alignment geometry rather than loss of proxy signals—is genuinely valuable. The paper convincingly argues that existing methods, while effective, operate on downstream consequences (logit distributions, parameter magnitudes) rather than the structural object (whitened cross-covariance spectrum and subspaces) that underlies CLIP's zero-shot ability. The projector-averaging mechanism for prompt invariance is also novel: averaging over randomized text-side canonical projectors eliminates sign/rotation ambiguity and naturally induces robustness without requiring task metadata or prompt engineering.

## Suggestions
- Provide the exact perturbation distribution P and its parametrization in the main text rather than deferring to the appendix.
- Add an experiment showing behavior under progressively harder domain shifts (e.g., increasingly out-of-distribution tasks) to stress-test the EMA covariance assumption.
- Report training wall-clock time and FLOPs alongside accuracy to give a complete efficiency picture, especially since different methods may use different adapter capacities.

## Score and Decision
The paper presents a well-motivated, technically sound framework with a novel conceptual angle on VL-CL forgetting. Experiments are thorough across four benchmarks with consistent improvements. However, margins over strong baselines are modest, and some analytical results (r=1.00 correlations) raise questions. The conceptual contribution of targeting alignment invariants directly is valuable for the community.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>