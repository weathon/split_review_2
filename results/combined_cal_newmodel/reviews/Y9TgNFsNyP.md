Now I have all the data I need. Let me compile the final review.

## Calibration Summary

**Anchors retrieved across rounds:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| 5lUdTogEL3.md | 1.00 | R1 | No | Unrelated topic (person re-id) |
| Xagys9QD3T.md (PPU) | 3.00 | R1 | Yes | Weaker method, severe presentation issues; our paper is clearly stronger |
| drrXhD2r8V.md (SPE-Unlearn) | 5.00 | R1 | Yes | Comparable method quality, more baselines tested; our paper has stronger novelty |
| KvFk356RpR.md (UMA) | 4.80 | R1 | Yes | Attack paper with missing standard deviations (-3.77); similar evaluation gaps |
| OHOmpkGiYK.md (Decoupling) | 5.75 | R1 | Yes | Extensive experiments, slightly lower novelty; our evaluation is less thorough |
| lgnAEBE1Xq.md (Contrastive Unlearn) | 5.00 | R2 | Yes | Similar novelty level, better experiments; our paper has more evaluation gaps |
| nb3VjILNVs.md (Low Compute Unlearn) | 5.75 | R2 | Yes | Strong multi-dataset evaluation including ImageNet; our experiments are narrower |

**Round-1 bracket:** The paper sits between 3.0 and 5.75. Clearly stronger than the 3.0 PPU paper (which had fundamental algorithmic and presentation issues) but weaker than the 5.75 Decoupling or Low Compute papers (which have more thorough evaluations).

**Round-2 narrowing:** Compared to the Contrastive Unlearning paper (5.0), our paper has comparable novelty (first FF unlearning vs. contrastive paradigm for unlearning) but weaker evaluation (circularity concern, thinner baselines, no error bars). The favorability of our weakest items (-1.13 for limited visible results, -0.96 for thin baselines, -0.61 for no stats) are less extreme in magnitude than the Contrastive paper's worst items (-3.51 for lack of theory, -1.20 for presentation), but our paper has more distinct evaluation gaps. This places it below 5.0.

**Final placement:** 4.0. The evaluation gaps are systematic enough to prevent acceptance but the core contribution (first FF unlearning method with a principled design) is genuine and the method is not fatally flawed.

---

## Summary

This paper proposes FF-Erase, the first machine unlearning method for Forward-Forward (FF) models — a biologically plausible alternative to backpropagation. The method uses a guidance model to define target goodness distributions and performs KL-divergence minimization to remove forgetting data's influence. The paper also proposes G-MIA, a membership inference attack using per-layer goodness vectors for verifying unlearning. Experiments on CIFAR-10 with VGG13 show 1.9–3.1× speedup over retraining with comparable effectiveness.

## Strengths

- **Novel problem identification.** The paper correctly identifies that FF models are gaining traction and that unlearning for FF models is entirely unexplored. The introduction (Section 1) provides a specific, mechanistic analysis of why standard BP-based unlearning would fail on FF models (sensitivity to parameter tuning, layer-wise independent training) — this is grounded and not a generic gap statement. [favorability=12.28]

- **Principled method design.** Using a guidance model to define a target goodness distribution and minimizing KL-divergence instead of directly suppressing goodness naturally addresses the instability problem. The "recovering forward" mechanism is a straightforward but sensible complementary mechanism. The method matches its stated motivation. [favorability=12.94]

- **Informative ablation study.** Table 1 systematically varies guidance model acquisition strategies (mini-retrained vs. fast-distilled), data/epoch fractions (α₁, α₂), and includes a critical R.G.M control condition (random guidance model). The R.G.M collapse (Acc_f dropping to 55.53%) cleanly validates the core thesis. [favorability=10.80]

- **G-MIA's feature design is sensible.** Using per-layer goodness vectors — which FF models expose by design — is a natural adaptation of MIA to the FF setting. The evaluation in Figure 3 shows G-MIA consistently outperforms the final-layer FL baseline across architectures, indicating the multi-layer signal carries more membership information. [favorability=11.62]

## Weaknesses

### Fatal
None.

### Major

- **Circular dependency in evaluation.** G-MIA is used as a primary quantitative metric to evaluate FF-Erase's unlearning effectiveness (Figure 4c, Table 1), but G-MIA is only validated on original (non-unlearned) models in Section 6.1 — distinguishing training members from non-members before any unlearning occurs. The attack model f_G-MIA is trained on goodness vectors from shadow models that are standard FF models, not unlearned models whose goodness distributions have been deliberately shifted. The paper provides no validation that G-MIA reliably detects residual membership in perturbed models, creating a logical gap. The comparison against retraining (RE) partially mitigates this but does not fully resolve the concern, since the paper's own verification tool has not been independently validated on the setting where it is applied. [favorability=-0.57]

- **The baseline set is too thin to support the claim that existing methods categorically fail.** The paper tests exactly one existing unlearning approach adapted to FF: direct gradient ascent (GA). While Section 6.3 varies λ across several orders of magnitude (which is helpful), GA is only one of many approximate unlearning families. The paper mentions influence-function methods (Qiao et al., Liu et al., Wu et al.) and bad-teacher unlearning (Chundawat et al. 2023a) in references but never adapts or tests any of them. Critically, per-layer independent GA — the most natural adaptation of existing methods to the layer-wise FF training — is not tested. For a paper whose motivation rests on "existing methods fail for FF models," testing only raw GA is insufficient evidence. [favorability=-0.96]

- **No statistical significance is reported for any experimental result.** No standard deviations, confidence intervals, error bars, or multiple-run information appear in Sections 6.1–6.4. Table 1 reports single values. Differences as small as 0.005 (G-MIA ACC 0.551 vs 0.556) and 0.03 (Acc_f 81.61 vs 81.58) are used to draw conclusions. Without multiple trials or variance measures, the reader cannot assess whether these differences are meaningful or reflect random seed or initialization noise. This is especially concerning because the paper's central unlearning claims hinge on small-magnitude comparisons (e.g., FF-Erase G-MIA ACC = 0.5245 vs. RE = 0.532 in Figure 4c). [favorability=-0.61]

### Minor

- **G-MIA is mischaracterized as a "black-box attack."** The abstract, contributions, and Section 5 call G-MIA black-box, but it requires access to goodness vectors from all layers — internal representations the model exposes by design. In the standard security taxonomy the paper itself cites (Shokri et al. 2017; Nasr et al. 2019), black-box means access only to the model's final prediction/logits. Access to per-layer features is at minimum gray-box. The paper's own comparison uses final-layer MIA (FL) as the black-box baseline, which uses strictly less information. This conflates access levels and inflates the apparent improvement over FL. [favorability=1.83]

- **The main text presents unlearning results for only one model-dataset pair (VGG13 on CIFAR-10).** The paper acknowledges this in Section 6.2 and defers other results to the appendix (which is stripped by the parser). While G-MIA evaluation (Figure 3) covers multiple architectures, the core unlearning effectiveness/efficiency claims visible in the main paper rest on a single configuration. [favorability=-1.13]

- **Termination conditions in Algorithm 1 could silently mask collapse.** The condition checks if ℓ₁ < ε₁ (forgetting loss low enough) **or** ℓ₂ > ε₂ (recovery loss too high). If both trigger simultaneously — which is precisely when the model has collapsed — the algorithm exits normally without signaling failure. [favorability=2.65]

### Trivial

- The notation in Equation (1) is ambiguous: the main text treats 𝐠ˡ as a vector but the computation uses ‖𝐡ˡ‖₁ (L1 norm of a J×dˡ matrix). The clarifying footnote should be part of the main formalism.

## Nice-to-Haves

- Validate G-MIA on unlearned models (e.g., by checking whether G-MIA scores correlate with direct measures like prediction-distribution divergence from RE on 𝔻_forget) to break the circularity.
- Adapt 2–3 additional approximate unlearning methods for FF (e.g., per-layer GA with independent learning rates, bad-teacher distillation) to strengthen the empirical foundation for the "existing methods fail" claim.
- Report all key results with confidence intervals over at least 5 random seeds.
- Clarify the relationship between t_ret scaling and the recovery forward term in Equation (9) when |𝔻_remain| ≫ |𝔻_forget|.

## Removed Points

These points were considered but removed per filtering rules:

- "The paper does not discuss what happens when the guidance model is poor (beyond the R.G.M control)" — **Removed:** The R.G.M control in Table 1 explicitly evaluates this scenario.
- "Efficiency analysis assumption undercounts recovery forward cost" — **Removed:** A mathematical subtlety that is not central; moved to Nice-to-Haves.
- "No discussion of limitations in conclusion" — **Removed:** Common for conference papers; relevant challenges are discussed throughout.
- "Guidance model ignorant of forgetting data is misleading phrasing" — **Removed:** The paper correctly explains the guidance model is trained only on remaining data, making it ignorant of forgetting data in the relevant sense.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Decouple the validation of FF-Erase from G-MIA by including direct model-behavior comparisons (e.g., KL divergence between FF-Erase and RE outputs on 𝔻_forget) before introducing G-MIA as a verification tool.
2. Expand the baseline set to include at least per-layer independent GA and one method from a different unlearning family (e.g., bad-teacher distillation or an influence-function adaptation).
3. Add confidence intervals or error bars over multiple runs for all reported metrics.
4. Acknowledge that G-MIA operates with gray-box (per-layer goodness) rather than strict black-box access, and justify why this access level is reasonable in the intended deployment scenario.
5. Move the clarifying footnote about the 𝐠ˡ computation from a footnote into the main equation description.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>