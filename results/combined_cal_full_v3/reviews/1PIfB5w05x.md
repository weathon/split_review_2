Now I have all the information I need for a calibrated assessment. Let me write the final review.

## Summary

This paper studies sparse signal support recovery when observations come from two sources with different noise variances (heteroscedastic noise). It derives asymptotic sufficient conditions for information-theoretic recovery in both agnostic and informed settings, introducing a "Price of Quality" concept that quantifies how many low-quality samples replace one high-quality sample. It also extends the LASSO phase transition (Wainwright, 2009) to the heterogeneous-noise, agnostic setting via QR decomposition and Haar-measure arguments. The paper is purely theoretical, with results organized around three regimes (high SNR, low SNR₂/high SNR₁, low SNR).

## Strengths

- **Well-motivated and timely problem.** The mixed-quality data setting (Section 1.1.2) is genuinely relevant given the rise of LLM-annotated data combined with smaller human gold-standard sets. The paper formalizes this for sparse recovery in a clean way connected to established literature.

- **Non-trivial LASSO extension (Theorem 3).** Extending Wainwright (2009) to heterogeneous noise is a genuine technical contribution. The paper correctly identifies that the heterogeneous covariance matrix Σ destroys the Wishart structure and addresses this via QR decomposition and Haar-measure arguments (Section 4, proof sketch). This is the strongest contribution.

- **Clean conceptual distillation via the Price of Quality (Section 3, eqs. 12, 18).** Summarizing the high/low-quality trade-off into a single number γ depending on noise levels and SNR regime is pedagogically valuable and enables crisp comparison between agnostic and informed settings.

- **Informative contrast between information-theoretic and algorithmic thresholds (Sections 3 and 4).** The finding that the information-theoretic Price of Quality can be arbitrarily large (informed setting) while the LASSO threshold is effectively noise-level-agnostic is a genuinely interesting juxtaposition suggesting a qualitative difference in how heterogeneous noise affects statistical possibility vs. computational tractability.

- **Transparent discussion of limitations (Remarks 3.2, 3.3, 4.1, 4.2).** The paper is unusually candid about what it does not establish: the agnostic sufficient condition is not proven sharp; LASSO in the informed setting is not analyzed; the independent-feature assumption is acknowledged as restrictive.

## Weaknesses

### Major

**1. Internal mathematical inconsistency in equation (12) — the σ₁⁴ term is incompatible with the rest of the paper.**

Equation (9) (the agnostic sufficient condition) defines coefficient α₁ = log(1 + δ(2σ₂² − σ₁²)s/(2σ₂²)). Equation (12) then writes the Price of Quality with σ₁⁴ in the denominator of the numerator:

γ = log(1 + δ(2σ₂² − σ₁²)s/(2σ₁⁴)) / log(1 + δs/(2σ₂²)).

This σ₁⁴ does not match (9)'s σ₂². Moreover, the generalization to arbitrary noise structures in equation (22) uses σ_max⁴ = σ₂⁴, introducing a third variant. As a result, the low-SNR₂ expansion in equation (14) — which claims γ ≃ 2 − σ₁²/σ₂² — is **mathematically incompatible with (12) as written**: plugging σ₁⁴ into the expansion does NOT simplify to 2 − σ₁²/σ₂². (It would simplify correctly if the denominator were σ₂² (as in (9)) or σ₂⁴ (as in (22)), but not σ₁⁴.) This is a clear mathematical error in a core definition that must be corrected for the paper to be evaluable as a coherent theoretical work. The good news is that the expansion (14) shows the authors **do** know the correct simplification — the error is almost certainly a typo — but as published, equations (9), (12), (14), and (22) cannot all be simultaneously correct.

### Minor

**2. The LASSO result requires n₁, n₂ = ω(s), which is in tension with the motivating scenario of scarce high-quality data.**

Theorem 3 (line 284) assumes n₁, n₂ = ω(s). In the paper's motivating narrative, n₁ is "a small collection of high-quality measurements." But ω(s) means n₁/s → ∞ — i.e., the high-quality collection must be larger than the sparsity level by an arbitrarily large factor. For growing s, this conflicts with the notion of scarce high-quality data. The LASSO result is mathematically valid, but its scope is narrower than the narrative suggests. The paper would benefit from explicitly discussing this tension.

**3. The γ ≤ 2 bound is a property of a non-sharp sufficient condition, not a proven property of the recovery problem itself.**

Remark 3.2 acknowledges that Theorem 1's condition is sufficient and "is not expected to be information-theoretically sharp." The cubic equation (37) whose exact solution would give a tighter condition is mentioned but not solved. Therefore the γ ≤ 2 bound (and the linear trade-off structure itself) may be artifacts of the relaxation. The paper does qualify its claims with "under our sufficient condition" in most places (abstract, introduction, conclusion), but the prominence of "one high-quality sample is never worth more than two low-quality samples" in these high-level summaries could mislead readers about what is proven vs. what follows from a particular proof technique.

### Trivial

None.

## Nice-to-Haves

- **Quantify the looseness of the agnostic sufficient condition.** Even a bound like "the sufficient condition is at most a factor C from the optimal threshold" would strengthen the γ ≤ 2 claim considerably.
- **Numerical simulations.** Synthetic experiments showing the LASSO threshold's behavior outside the ω(s) regime would bridge the gap between theory and application.
- **Clarify the eq (9) vs (22) denominator inconsistency** by stating which is the correct form derived from the Chernoff bound.

## Removed Points

These points were raised in the input review but are removed with justification:
- *Claim that the informed threshold is described as "sharp" without qualification.* — The paper qualifies this ("within the Gaussian design framework considered here" on line 340) and discusses the necessity gap in Remark 3.3. The reviewer overstates the issue.
- *Y_i² proxy for noise estimation being impractical.* — Remark 3.2 frames this as a speculative future direction; criticizing its practicality is scope creep.
- *Requests for partial-information settings.* — The paper explicitly defines two clean settings; demanding a third is scope expansion, not a flaw.
- *Missing experimental validation as a weakness.* — For a purely theoretical paper extending known results, this is not a weakness; it is a nice-to-have.
- *Formatting/style nitpicks.* — Parser artifacts, not author errors.

## Novel Insights

The reviewer's discovery that the paper contains a **triple inconsistency** (eqs. 9, 12, and 22 all disagree on the denominator) is sharper than the paper's own self-diagnosis. While the σ₁⁴ in (12) is the most obvious error, there is also a σ₂² vs σ₂⁴ inconsistency between (9) and the generalization (22). This suggests the paper's derivation chain has not been fully checked for numerical consistency, which is a significant concern for a purely theoretical paper.

## Suggestions

1. **Fix the mathematical inconsistency.** Determine the correct form of the denominator in equation (12) — whether it should be σ₂² (consistent with (9)) or σ₂⁴ (consistent with the generalization (22)) — and propagate the correction through equations (12), (13), and (14). Verify that the generalization (22) is consistent with the two-source special case.
2. **Explicitly discuss the ω(s) assumption** in Theorem 3 and its relationship to the motivating story of scarce high-quality data.
3. **Tone down the prominence of the γ ≤ 2 claim** in the abstract and conclusion, or add a one-sentence caveat that it applies to the paper's sufficient condition and may not be the true information-theoretic limit.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gVVoZtiQlt.md (Phase Transition of Shuffled Regression) | 5.00 | 1 | Yes | Similar theory paper about phase transitions. Had more severe weaknesses (assumption realism scored -6.10, heuristic derivation -5.56) but compensated with experiments (9.68). Our paper has a cleaner problem framing but a mathematical inconsistency (-1.65) and no experiments. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TKRIRI9tQv.md (Nonlinear System ID) | 5.00 | 1 | Yes | Theory paper with recovery guarantees. Had comparable strengths but was rejected due to concerns about assumption strength. Our paper has similar structure (sufficient conditions, recovery guarantees) but clearer motivation. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NHhjczmJjo.md (In-Context Sparse Recovery) | 7.00 | 1 | Yes | Higher-scored paper with both theory and experiments. More applied and less directly comparable. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wpXGPCBOTX.md (Sparsistency for iOT) | 6.75 | 1 | Yes | Accepted theory paper with strong contributions and minor notation issues. Our paper has a more serious mathematical inconsistency. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ghH6YYDs15.md (Compute Optimal SAEs) | 4.67 | 2 | Yes | Theory+experiments paper about sparse coding. Had theoretical claims questioned by reviewers. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/L0pMPCmEfN.md (Splitted Wavelet DI) | 4.33 | 2 | No | Less relevant (wavelet signal processing). |

**Round-1 bracket:** 3.5–5.5 (based on the Phase Transition paper at 5.00 and the SAEs paper at 4.67 being the most structurally comparable).

**Final placement:** The paper sits near the top of the 3.5–5.5 bracket. Its strongest items (motivation 11.12, LASSO extension 9.92, Price of Quality 9.67) compare favorably with the Phase Transition paper's strongest items (novelty 10.40, experiments 9.68). Its weakest item (σ₁⁴ inconsistency at -1.65) is substantially less damaging than the Phase Transition paper's weakest items (unrealistic assumption -6.10, heuristic derivation -5.56). However, unlike the Phase Transition paper, our paper has **no experiments** and its motivating claim (γ ≤ 2) depends on a non-sharp sufficient condition. The mathematical inconsistency, while likely a typo, is a real error in a core equation of a theory paper. This places the paper marginally below the Phase Transition paper's 5.00, at **4.5**. A corrected version that fixes the inconsistency and acknowledges the scope limitations could reach 6+.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>