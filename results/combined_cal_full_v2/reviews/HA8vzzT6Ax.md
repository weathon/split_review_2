Now I have all the calibration data I need. Let me write the final review.

## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency in LLMs, showing it is not absolute. The authors introduce a continuous measure of watermark strength (expected KL divergence), formulate the trade-off as a Pareto frontier over a constrained optimization problem, and propose a mechanism — pseudorandom draft-token acceptance — that provably achieves both maximal watermark strength and maximal speculative sampling efficiency simultaneously. Experiments on Gumbel-max and SynthID watermarks (Llama-68M/7B, Gemma-2B/7B) demonstrate improved detectability at matching efficiency.

## Strengths

- **Genuinely insightful reframing via a continuous measure of watermark strength (Section 3.1).** The paper identifies that Hu & Huang's binary definition (preserved iff the final distribution exactly matches the watermarked distribution) is overly restrictive. Replacing it with expected KL divergence, WS = E_ζ[D_KL(P_ζ ∥ P)], is natural and productive. Theorem 3.2 (WS ≤ Ent(P), with equality iff P_ζ is degenerate) provides a clean characterization, and Theorem 3.1 linking WS to p-value decay rates grounds the measure in detection theory. The mutual information equivalence (I(w; ζ)) under unbiasedness is also insightful.

- **Clean theoretical resolution of the apparent impossibility (Theorem 4.1).** The proposed mechanism — making the acceptance decision pseudorandom rather than truly random — is simple, well-motivated, and provably achieves all three desiderata (unbiasedness, maximal SSE, maximal WS) simultaneously. The reasoning is sound: by replacing the stochastic acceptance coin flip with a pseudorandom one (ζ^R) that is recoverable at detection time, the entire generation becomes a deterministic function of ζ, making P'_ζ degenerate and hence achieving WS = Ent(P).

- **Principled Pareto-curve formulation (Definition 3.2 and Eq. 10).** Casting the trade-off as a constrained optimization problem over watermark strength vs. sampling efficiency, with Lemma 3.1 showing speculative sampling is the optimal transition kernel, organizes the design space cleanly. This framework is general enough to apply to any watermarking scheme, not just the two examples shown.

## Weaknesses

### Fatal
None.

### Major

- **Baseline comparisons are essentially ablations, not external baselines.** The paper compares Ars-τ to Ars-Prior and Bayes-MLP to Bayes-Prior. Both Ars-Prior and Bayes-Prior are variants of the proposed method that do not use ζ^R — they are not independent baselines from prior work. A proper evaluation would include (a) standard watermarking without speculative sampling (to quantify the efficiency gain), (b) speculative sampling with standard watermarking (to show the previous trade-off), and (c) alternative approaches from the literature. Without these, the reader cannot assess whether Algorithm 1 genuinely beats alternatives or just outperforms a deliberately weakened version of itself.

- **The paper's framing overclaims relative to what the experiments show.** The abstract and introduction state that the method "breaks" or "overcomes" the trade-off. In the narrow theoretical sense — achieving WS = Ent(P) and SSE = 1 − TV(Q,P) simultaneously — this is correct. However, the paper's own Remark 3.1 and Section 4.2 acknowledge that "watermark strength is conceptually distinct from detection efficiency (detectability)" and that maximal WS "does not guarantee optimal detection efficiency." The headline claim refers to WS, but what practitioners care about is detectability at practical token lengths, where the improvement is real but incomplete (a gap to the Oracle remains in Fig. 2, with overlapping confidence intervals at short token lengths). The framing should more honestly reflect that the theoretical maximum of the *proposed WS measure* is achieved, while the practical detectability-vs-efficiency trade-off is merely *improved*, not eliminated.

### Minor

- **Main detectability results shown only at lower-than-standard temperatures (0.5 for Gumbel-max, 0.7 for SynthID),** explicitly stated as chosen "to make the results more pronounced" (line 259). As the paper's own theory shows, lower temperatures reduce distribution entropy and cap maximum possible WS at Ent(P). The reader cannot tell whether the improvement holds at temperature 1.0, where distributions are more diffuse and watermarking is genuinely harder. Evaluating at the standard temperature would be more informative even if the improvement is smaller.

- **The trade-off curves in Figure 1 are computed for simulated (Q,P) pairs** whose nature is not adequately described in the main text (details deferred to Appendix C.1). Since these curves are central to the paper's characterization contribution, the reader cannot assess whether the simulated pairs are representative of real model distributions. Computing these curves for the actual model pairs used in experiments (Llama-68M/7B, Gemma-2B/7B) and overlaying the operating points would directly connect the theoretical Pareto analysis to the empirical results.

- **Detection evaluation scope is limited.** Only one dataset (EL15) is used in the main text for detection experiments; C4 results appear only in the appendix. Two model pairs are tested but one pair's (Gemma) results are deferred to the appendix. Confidence intervals for TPR@FPR=1% in Fig. 2 overlap substantially at short token lengths (e.g., 50 tokens), so the statistical significance of the claimed improvement at practical token lengths (50–100) is unclear.

- **Detection methods lack sensitivity analysis.** For Ars-τ, it is unclear how sensitive performance is to the choice of τ or how large the validation set must be. For Bayes-MLP, the architecture and training-set size are presented as a single operating point without exploring robustness.

- **Only two model pairs, both relatively small** (Llama-68M/7B and Gemma-2B/7B). While the theory is general, empirical demonstration across more model scales and families would strengthen confidence.

### Trivial

- **Per Token Time (PTT) results, central to the efficiency claim, are only mentioned in passing** in the main text (line 265) and reported in the appendix. Given that speculative sampling is motivated by speed, the main text should report actual speedups.

## Nice-to-Haves

- Compare against standard watermarking without speculative sampling as a baseline.
- Evaluate at temperature 1.0 as a primary setting, even if the improvement is smaller.
- Compute the trade-off curves (Figure 1) for the actual model pairs used in the experiments and overlay the operating points achieved by the proposed method and baselines.
- Add sensitivity analysis for detection hyperparameters (τ threshold, MLP architecture, training set size).
- Report PTT speedup numbers in the main text.

## Removed Points

These points were raised in the input but are removed:

1. **"The acceptance criterion in Alg. 1 uses original P and Q, not watermarked versions — this should be explicitly discussed."** — Removed because the paper already explicitly discusses this design choice: Algorithm 1 line 9 and the surrounding text explain the key insight is using pseudorandom acceptance with the original distributions, which is the core of the contribution.

2. **"The detection methods feel like engineering workarounds rather than principled solutions."** — Removed as an opinion, not a verifiable weakness. The paper presents these as practical detection strategies consistent with the theoretical framework (Section 4.2).

3. **Missing proofs / appendix content concerns.** — Removed per hard rules: the parser strips appendices and references; they exist in the original submission.

4. **"Whether simulated pairs are cherry-picked."** — Removed as speculation about appendix content. The retained weakness focuses on the verifiable issue (insufficient main-text description).

5. **Generality concerns about "only two model pairs" being "too small."** — Downgraded from the harsher framing. The concern about limited evaluation is valid but softened: the models used are reasonable for academic compute budgets and the theory is architecture-agnostic.

## Novel Insights

The input review surfaced the core tension between the theoretical WS measure (the paper's main contribution) and practical detectability (what users care about). This tension is already acknowledged in Remark 3.1 and Section 4.2, but the abstract and introduction do not adequately signal it. The review's framing of this as a "heads I win, tails you lose" situation — where the headline result uses a new theoretical measure while the practical metric shows only incremental improvement — is a genuine observation that the authors should address by adjusting their narrative.

## Suggestions

1. **Add proper external baselines.** Include standard watermarking without speculative sampling (to quantify the efficiency advantage) and alternative approaches from the watermarking + speculative sampling literature.
2. **Evaluate at temperature 1.0** as a primary setting. If the improvement is smaller, report it honestly — this is more convincing than showing a large improvement at an atypical temperature.
3. **Compute the trade-off curves (Figure 1) for the actual model pairs** used in experiments and overlay the operating points of the proposed method and baselines. This directly connects the Pareto analysis to the empirical results.
4. **Adjust the framing** to accurately reflect that the theoretical maximum of the proposed WS measure is achieved, while the practical detectability-vs-efficiency trade-off is improved but not eliminated.
5. **Report PTT speedups and sensitivity analyses** in the main text.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5kMwiMnUip.md | 1.40 | R1 | No | Unrelated; strong reject |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated; strong reject |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jbfDg4DgAk.md | 3.00 | R1 | Yes | Sparse Watermarking — much weaker theory, no formal characterization of trade-off |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/n7iwmPacDt.md | 3.00 | R1 | No | Polybasic Speculative Decoding — different focus, weaker theory |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eKGEsFdpin.md | 3.67 | R1 | No | Sampling-based watermarking — less rigorous theoretical framing |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0koPj0cJV6.md | 4.60 | R1 | No | Black-box watermark — good but different problem setting |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jln7IcheW6.md | 4.33 | R1 | No | Pseudo- vs true-randomness — related but less comprehensive |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8o6LdeVi1K.md | 3.75 | R1 | No | Finetuned watermark — different problem |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LdIlnsePNt.md | 6.00 | R1/R2 | Yes | **SEAL** — most directly comparable (watermark + spec sampling). Has severe theoretical gaps (-3.96, -4.76), weak theory-experiment link. **Current paper is stronger** (cleaner theory, less severe weaknesses). |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9k0krNzvlV.md | 5.75 | R1/R2 | Yes | Learnability of watermarks — modest novelty (-6.07 weakness). **Current paper has stronger theory.** |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/E4LAVLXAHW.md | 7.00 | R1 | Yes | **Black-Box Detection** — thorough empirical work, well-executed. **Current paper is below** due to weaker experiments, but has stronger theory. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jlhBFm7T2J.md | 6.50 | R2 | Yes | Undetectable image watermark — different domain, comparable overall quality. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xOtOfdbBqK.md | 5.75 | R2 | Yes | Drop-in speculative decoding — marginal improvement (-1.80), weak baselines (-2.66). **Current paper has stronger theory.** |

**Weighted-item comparison:** My strengths (9.85–10.87) are comparable to or stronger than SEAL's best (9.34, 9.00) and Black-Box Detection's best (11.99). My most severe weakness (-1.46, baselines are ablations) is notably less damaging than SEAL's worst (-4.76, -3.96). This places the paper clearly above SEAL (6.00). However, Black-Box Detection (7.00) has no severely negative items and its experiments are more thorough, placing my paper below it.

**Round 1 bracket:** [5.5, 7.5] — The paper sits between SEAL (6.00) and Black-Box Detection (7.00).

**Round 2 narrowing:** Item comparison against the SEAL anchor shows the paper has stronger theory (strength weights 10+ vs 8–9) and less severe weaknesses (-1.46 vs -4.76). Comparison against Black-Box Detection shows that anchor has more thorough experiments and no severely negative items. The paper is most comparable to the Undetectable Image Watermark (6.50) in terms of having strong theory with some experimental limitations.

**Final score:** 6.5. The theoretical contributions are genuinely strong and novel enough to warrant acceptance. The experimental validation has one notable shortcoming (baseline comparison) and several minor issues that should be addressed but do not invalidate the core contribution.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>