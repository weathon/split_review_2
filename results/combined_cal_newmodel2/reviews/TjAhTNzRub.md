Now I have all the evidence I need. Let me write the final consolidated review.

## Summary

This paper proposes MoRE (Mixture of Remapping Experts), a training-free framework for feature-level machine unlearning. It introduces three innovations: (1) prototype-orthogonal (PO) projection that decorrelates forget and remain prototypes before erasure, preventing collateral damage to remain utility; (2) remapping with a mixture of experts that redirects forget features toward multiple remain prototypes, disrupting residual separability; and (3) activation-mean prototypes that reduce unlearning to lightweight linear algebra. Experiments on CIFAR-10/100, Tiny-ImageNet, and diffusion models show strong utility preservation and that linear probing recovers near-zero forget accuracy — often outperforming retrain-from-scratch on the KR metric.

## Strengths

- **Principled PO projection with clear empirical motivation.** Section 3.1 shows forget and remain prototypes have cosine similarities ~0.5–0.77 and that ESC's erasure damages remain prototypes (autocorrelation drops from 1.0 to 0.52). The pseudoinverse solution via SVD (Eq. 2) is mathematically sound, explicitly justified over the normal-equation form (line 146), and validated by ablation (Table 3: without PO, remapping degrades D_r to 89.52 vs. 99.87 with PO).

- **Remapping + MoE is a genuine conceptual advance over ESC.** ESC erases but leaves forget features as a separable cluster. MoRE detects forget-prototype activation and redirects it toward remain prototypes (Eq. 6), then scatters features across multiple remain prototypes. The t-SNE in Figure 1 and the quantitative KR metric confirm the effect.

- **Strong empirical results on the KR metric.** On CIFAR-100 (KR setting), ESC achieves HM_f = 99.60 while MoRE achieves 0.07; on Tiny-ImageNet, ESC scores 15.78 and MoRE scores 0.50. The retrain baseline falls between (CIFAR-100: 52.96), meaning MoRE prevents linear-probe recovery *better than retraining from scratch*.

- **Efficiency is genuinely demonstrated.** The method requires one forward pass + activation means + a pseudoinverse on a small (d × k) matrix. Table 1 and Figure 5 show competitive results in under 10 seconds and ~540 MB (see weakness below for the text/figure discrepancy).

## Weaknesses

### Fatal
None.

### Major

1. **The "irreversible" claim is not supported by the tested evidence.** The word "irreversible" appears 15+ times (abstract, introduction, method, conclusion). The paper claims its method "significantly impedes recovery of forgotten knowledge through fine-tuning" (line 82) and motivates the problem by noting ESC leaves knowledge "vulnerable to recovery through light fine-tuning" (line 58). Yet the paper never runs a fine-tuning recovery attack. The only evidence is (a) t-SNE visualizations (non-linear, can create or destroy structure) and (b) the KR metric, which tests *linear probing on frozen features*. An adversary who can fine-tune the full model (even briefly) might re-separate remapped features or re-form the forget cluster. Without this experiment, "irreversible" overstates what is tested. The paper would be stronger by either adding fine-tuning recovery experiments or precisely qualifying the claim to what is actually measured.

2. **Clear text/figure discrepancy in memory consumption.** The text states MoRE consumes "less than 200 MB of GPU memory" (line 255), but Figure 5 shows MoRE at 540 MB of GPU memory. Every other method in the figure also ranges 447–566 MB, making 200 MB implausible for this setting. This is a factual error that must be corrected or clarified.

### Minor

3. **The complement-space projection (I − PD)z in Eq. 4 preserves all information orthogonal to the k class prototypes.** Since d ≫ k, the complement spans most of the feature space. The paper presents this as a solution to preserve utility, but does not discuss the corollary: any forget-relevant information encoded outside the prototype subspace survives unlearning untouched. The abstract's claim of "exact feature-level unlearning" is misleading given this structural limitation. The method removes forget-class *prototype* information but cannot address information outside that subspace.

4. **Comparison with ESC is confounded by different prototype definitions.** ESC uses SVD-based prototypes (principal components of forget features capturing directions of maximum variance), while MoRE uses class-wise activation means (one vector per class). These are fundamentally different entities. Performance differences could partly reflect this choice rather than erasure vs. remapping. The ablation (Table 3) partially addresses this by including an "Erase" variant within MoRE's framework, but a cleaner comparison would isolate prototype definition from erasure/remapping.

5. **The full mutual orthogonality condition (footnote, line 168) removes remain-to-remain correlations as well.** The paper acknowledges that only forget–remain orthogonality is strictly needed but adopts full orthogonality "for mathematical brevity." The potential impact on remain-class discrimination is not analyzed or ablated.

6. **The stochastic router is input-independent and routes each input randomly (lines 179–182).** The paper does not clarify whether the unlearned model's inference becomes non-deterministic. If the MoRE layer stays in the inference pipeline, the same input could map to different remapping experts on different passes. This warrants clarification.

7. **The random data forgetting experiment (Table 4) is a mismatch for the class-wise design.** MoRE achieves MIA = 79.31, underperforming simpler methods (Prototype: 87.73, SCRUB: 86.41) and only marginally beating Retrain (74.64). The paper acknowledges it was "not explicitly designed for random data forgetting" (line 360). This experiment does not support the paper's main claims and the space could be better used for irreversibility experiments.

### Trivial
None.

## Nice-to-Haves

- Run fine-tuning recovery experiments (varying epochs of fine-tuning on the forget set after MoRE unlearning). If recovery is not possible, this would genuinely support the irreversibility claim; if it is possible, the claim should be qualified.
- Add an ablation of the complement-space projection term (I − PD)z to demonstrate its effect on both utility and the survival of non-prototype forget information.
- Discuss or ablate the impact of the full orthogonality assumption on remain-class discrimination.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **KR metric definition deferred to appendix**: Removed per hard rule — the appendix exists in the original submission; the parser strips it.
- **Missing std for MoRE entries**: Removed — Table 1 formatting is garbled by the parser; the header states "mean ± std across three trials."
- **ImageNet results deferred**: Removed per hard rule — results are in the appendix which exists in the original submission.
- **Various formatting and typo nitpicks**: Removed per hard rule — these are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the memory consumption discrepancy between the text (200 MB) and Figure 5 (540 MB).
2. Add fine-tuning recovery experiments or qualify the "irreversible" claim precisely to what is tested (resistance to linear probing).
3. Acknowledge the structural limitation that non-prototype forget information is untouched, and qualify "exact feature-level unlearning" accordingly.
4. Clarify whether the stochastic router makes inference non-deterministic after unlearning.
5. Consider replacing or strengthening the random data forgetting experiment with experiments that directly support the irreversibility claim.

---

**Calibration Report**

Anchors retrieved across all rounds:

| Path | Avg Score | Round | Itemized | Comparison to this paper |
|---|---|---|---|---|
| `pUOesbrlw4.md` (Deep Unlearning) | 5.25 | R1 | Yes | Similar training-free class unlearning via SVD. MoRE's PO + remapping + MoE is more sophisticated; MoRE has better ablations but similar overclaiming issues. |
| `p7mgNvOD9Q.md` (SUN) | 4.00 | R1 | Yes | Training-free subspace removal. Less novel than MoRE; MoRE has stronger empirical validation and clearer motivation. |
| `nb3VjILNVs.md` (Low Compute Unlearning) | 5.75 | R1 | Yes | Low-compute unlearning via sparse bottleneck. Different mechanism. Comparable rigor. |
| `OHOmpkGiYK.md` (Decoupling Class Label) | 5.75 | R2 | Yes | Broader unlearning framework with mixed reviews (3–8). MoRE has stronger technical focus and cleaner results. |
| `SIZWiya7FE.md` (Label-Agnostic Forgetting) | 6.00 | R2 | Yes | Accepted paper on supervision-free unlearning. MoRE's contribution is different in nature but similarly novel. |
| `Xagys9QD3T.md` (Pseudo-Probability Unlearning) | 3.00 | R1 | No | Lower-scored unlearning paper; MoRE is substantially stronger. |
| `7tpMhoPXrL.md` (Forget Vectors) | 4.80 | R2 | No | Different approach (input perturbation); less relevant. |
| `wAemQcyWqq.md` (Oblivious Unlearning) | 5.67 | R2 | No | Privacy-focused unlearning; different framing. |
| `caY45V0dYt.md` (RealEra) | 3.40 | R1 | No | Concept erasure in diffusion models; narrower scope. |

**Round-1 bracket:** [4.0, 7.0] — The paper is clearly above the 3–4 range (where papers have weak or unclear contributions) and below the 7+ range (where claims are fully supported by evidence).

**Narrowing to final score (5.5):** The closest anchors are *Deep Unlearning* (5.25, Reject) and *Label-Agnostic Forgetting* (6.00, Accept). MoRE has a more novel and principled technical contribution than Deep Unlearning (PO projection with clear motivation vs. basic SVD-based subspace removal) and better ablation studies. However, MoRE shares a similar pattern of overclaiming — Deep Unlearning's reviewers flagged "lack of theoretical guarantees" (favorability -0.40) and "missing MIA evaluation" (favorability -1.56), while MoRE's most negative-rated weakness is the unsupported "irreversible" claim (favorability -2.30). Compared to LAF (6.00), which was accepted despite efficiency concerns identified by some reviewers, MoRE has a more concretely demonstrated efficiency advantage but a clearer overclaiming gap. The favorability comparison places MoRE below LAF's strongest items (which had multiple weaknesses with favorability 2–4) and closer to Deep Unlearning's profile where the core contribution is solid but the strength of the claims exceeds the evidence. The balance yields 5.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>