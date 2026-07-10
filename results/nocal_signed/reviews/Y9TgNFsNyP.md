## Summary

This paper identifies machine unlearning for Forward-Forward (FF) models as a previously unexplored problem. It proposes FF-Erase, an unlearning method that uses a guidance model (ignorant of forgetting data) to provide goodness targets via KL divergence, steering the original model away from forgetting data without causing the collapse suffered by gradient ascent. It also proposes G-MIA, a membership inference attack that leverages per-layer goodness vectors to verify unlearning effectiveness. Experiments show 1.9–3.1× speedup over retraining with moderate utility degradation.

## Strengths

- **Genuinely novel problem formulation.** The paper formalizes a real gap: machine unlearning for Forward-Forward models is unexplored. The motivation in Section 1 explains *why* standard unlearning (gradient ascent) breaks under FF's layer-wise independent training — parameter update directions diverge across layers, and it is unclear how much each layer should be penalized. This is not a repackaging of known challenges.

- **Clean method design consistent with the FF training paradigm.** The core idea — using a guidance model ignorant of forgetting data to provide goodness targets via KL divergence (Section 4.1, Equations 5–6) — is a natural adaptation of unlearning to the FF setting. Rather than forcing the model toward a universal "low goodness" state, it shifts each layer's goodness distribution toward a target distribution that simply has no knowledge of the forgetting data.

- **G-MIA identifies a genuinely useful leakage channel.** The observation that FF models expose per-layer goodness vectors, and that these are more informative for membership inference than final-layer outputs (Section 6.1, Figure 3), is well supported. In the VGG13/CIFAR-100 setting, G-MIA outperforms white-box attacks that use gradients or average-pooled layer outputs.

- **Comprehensive ablation on guidance model quality (Table 1).** The ablation systematically varies α₁ (data proportion) and α₂ (epoch proportion) for both the distilled and mini-retrained strategies, and includes a randomly-initialized guidance model (R.G.M.) as a control. The R.G.M. row shows that a poor guidance model leads to collapse, demonstrating that the guidance model is doing real work.

## Weaknesses

### Fatal

None.

### Major

- **The claim that existing unlearning methods are infeasible for FF models is empirically tested against only one baseline: gradient ascent (GA).** While the paper makes a conceptual argument that BP-based methods (influence functions, Hessian-based approaches) rely on mechanisms FF models lack, it does not test any other approximate unlearning baseline. Notably, distillation-based methods like the "incompetent teacher" (Chundawat et al. 2023a) share structural similarities with FF-Erase (guidance/teacher model, KL divergence) but are not compared. The sweeping assertion that prior unlearning methods collectively fail is extrapolated beyond the evidence presented. Testing even one additional baseline would substantially strengthen the paper's claim about why FF-specific design is necessary.

### Minor

- **The utility degradation is understated in the paper's framing.** The paper describes the accuracy drop as "only a minor 1.6–3.3% degradation," but FF-Erase variants consistently achieve *worse* (higher) G-MIA scores than retraining from scratch (RE): RE achieves G-MIA ACC = 0.551, while FF-Erase variants range from 0.556 to 0.577. This means FF-Erase leaves more membership signal than the gold standard. The "comparable effectiveness" characterization is accurate when comparing to collapsed GA models but deserves a clearer caveat when compared to RE.

- **No sensitivity analysis reported for ε₁, ε₂, or K.** Algorithm 1 includes early-stopping thresholds ε₁, ε₂ and recovery step K. The paper states that K is "determined by the dataset" (footnote 2) but reports no specific values, how they were chosen, or how performance varies with them. This weakens reproducibility.

- **G-MIA's synthetic data assumption is not validated for complex datasets.** G-MIA assumes the attacker can synthesize data with similar distribution to the training data (Section 5, line 200), citing model inversion (Fredrikson et al., 2015). This is reasonable for MNIST but is not validated for CIFAR-100, where model inversion is known to produce low-fidelity synthetic data. The impact of synthetic data quality on G-MIA's performance is untested.

- **The guidance model overhead could be discussed more clearly.** In many configurations the guidance model training time dominates (e.g., D-(0.5,0.5): t₀ = 410.5s out of 583.5s total, ≈70%). The speedup comes from using fractionally less data and fewer epochs for the guidance model, plus a short forgetting/recovering phase. Section 4.3 covers this briefly, but a clearer framing of this trade-off would help readers evaluate the efficiency claims.

### Trivial

None.

## Nice-to-Haves

- Testing at least one additional unlearning baseline (e.g., a distillation-based method) to further validate the claimed infeasibility of prior methods or reveal what design choices make FF-Erase effective.
- Validating G-MIA's synthetic data assumption empirically for complex datasets by comparing performance with real vs. synthetic shadow data.
- Adding a "same-cost" baseline comparing FF-Erase to a model trained from scratch for the same wall-clock time as FF-Erase's total compute.

## Removed Points

These points are flagged to be removed; treat them with caution:
- "G-MIA requires per-layer goodness vectors and is not truly black-box" — REMOVED because in FF models, goodness vectors are part of the standard inference output (line 88: "FF models output the goodness vectors from all layers ... for inference"). This is standard black-box access within the FF paradigm, not a stronger access model.
- "Experimental evaluation shown for only one dataset/architecture pair in main text" — REMOVED per Hard Rules: the paper explicitly states additional results are in Appendix C (line 242), which was stripped by the parser.
- "Introduction states black-box attacks are not accurate enough without citation" — REMOVED because the paper supports this claim experimentally later (Section 6.1, Figure 3).
- "GA comparison uses λ=10 which is worst case" — REMOVED because the paper addresses this with a full λ sweep in Section 6.3 (Figure 5).
- Various presentation and notation nitpicks — REMOVED per Hard Rules as parser artifacts or trivial.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Compare against at least one additional unlearning baseline — particularly a distillation-based approach like the "incompetent teacher" — to either confirm that prior methods cannot be adapted for FF or reveal which design choices are critical. This would substantiate the paper's central motivation.
- Report the specific values used for ε₁, ε₂, and K, and provide a sensitivity analysis for these hyperparameters.
- Clarify in the main text that in FF models, goodness vectors are the standard inference output, which justifies G-MIA's classification as a black-box attack.
- Add a brief discussion of how synthetic data quality affects G-MIA for complex datasets, or empirically validate this.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>