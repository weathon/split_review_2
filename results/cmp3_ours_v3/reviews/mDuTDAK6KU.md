Now I have sufficient calibration data. Let me compile the final review.

## Summary

KOALA proposes an adversarial detector that flags inputs when predictions from two complementary metrics—KL divergence (sensitive to dense, low-amplitude perturbations) and an L₀-based metric (sensitive to sparse, high-impact changes)—disagree. It provides a formal theorem specifying conditions for guaranteed detection, uses only clean-image fine-tuning (no adversarial training), and evaluates on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet.

## Strengths

1. **Well-motivated complementary detection principle.** The pairing of KL divergence (sensitive to broad, small-magnitude shifts) with an L₀-based metric (sensitive to few, large-magnitude changes) is grounded in a clear geometric intuition about how norm-bounded attacks manifest (Sec. 3.1, Fig. 1). This is a genuinely novel framing for adversarial detection.

2. **No adversarial training required.** The fine-tuning procedure uses only clean images and a composite loss (Eq. 6), making the approach computationally lightweight compared to methods that train on adversarial examples (Sec. 2, Sec. 3.3).

3. **Formal detection guarantee (conditional).** Theorem 1 provides explicit conditions under which disagreement—and thus detection—is guaranteed. Formal guarantees are rare in the reactive detection literature, and the proof sketch (Sec. 3.2) lays out a plausible structural argument.

4. **Informative ablation study.** Table 2 systematically compares multiple metric combinations (KL+L₀, L₀+Cosine, KL+Cosine, KL+L₀+Cosine), providing evidence for the paper's central design choice on ResNet/CIFAR-10.

## Weaknesses

### Major

1. **Non-standard evaluation metrics make reported detection scores uninterpretable.** The confusion matrix (Sec. 4.2, lines 187–191) defines a True Positive as an attacked input that is *either* detected by the detector *or* undetected but correctly classified by the nearest-prototype classifier. Concretely: `TP := [a=1] ∧ [(â, ŷ) = (1, ⊥) ∨ (â, ŷ) = (0, y*)]`. This means an undetected attack counts as a True Positive as long as the classifier happens to predict the correct class. Under the standard detection definition (flag=positive), every undetected attack is a False Negative regardless of classification outcome. This definition systematically inflates recall and F1. The headline numbers (recall 0.81, 0.85 in the abstract) are not comparable with any prior detection work. The paper must report standard detection metrics or at minimum report both definitions side by side.

2. **No evaluation against adaptive attacks.** The paper evaluates PGD, CW, and AutoAttack as attacks on the classifier, but never considers an adversary aware of the KOALA detector who crafts perturbations to evade it (e.g., optimizing a loss to force agreement between KL and L₀ predictions on a wrong class). This is a standard expectation in adversarial detection papers (Carlini & Wagner, 2017; Athalye et al., 2018; Tramer et al., 2020), because detectors with strong non-adaptive results can fail catastrophically under adaptive evaluation. Without this, the claim of "robust attack identification" (line 27) is unsupported.

### Minor

3. **The "Theorem-Compliant" partition is post-hoc and not operationally usable.** Experiment 1 partitions test samples into "Theorem-Compliant" and "Non-Compliant" subsets based on knowledge of the true class and inter-prototype separation, reporting perfect detection (1.0 on all metrics) on the compliant subset. However, this partition cannot be computed at inference time (the true class and attack status are unknown). The non-compliant subset, which constitutes 33–44% of CIFAR-10 and ~90% of Tiny-ImageNet samples (Table 1), shows much weaker performance (e.g., recall 0.42–0.45 on CIFAR-10). The headline "1.0 detection" applies only to a subset that cannot be identified at run time, and the full-set results are more modest.

4. **Norm ambiguity between theory and experiments.** Assumption A2 (line 114) states "‖δ‖ ≤ ε" without specifying the norm. Figure 1 (line 40) mentions "‖δ‖₂ ≤ ε," suggesting ℓ₂, but all experiments (line 178) use ℓ∞-bounded attacks. The threshold Γᵢ(ε) in Theorem 1 depends on the norm, which is never specified. It is unclear whether the theory and experiments operate under the same perturbation model.

5. **KL+L₀ underperforms its individual components on CLIP/Tiny-ImageNet for adversarial accuracy.** Table 4 shows the KL+L₀ fine-tuned model achieves only 26.50% PGD accuracy (ε=2/255) on CLIP/Tiny-ImageNet, compared to 60.02% for KL-only and 53.31% for L₀-only. The paper acknowledges this (lines 264–276) but attributes it to different pre-training without deeper analysis. This weakens the generality of the claim that KL+L₀ is the "right" combination.

6. **"No architectural changes" is overstated.** The abstract (line 9) and introduction (line 25) claim the method "requires no architectural changes," but Section 3.1 (line 58) states KOALA "replaces this conventional classifier head." The backbone is unchanged, but swapping the head is an architectural change. This should be clarified to "no changes to the backbone encoder."

7. **KL divergence asymmetry not discussed.** Equation (1) uses KL(c||p) (forward KL from prototype to embedding). The choice of direction is not justified, and the asymmetry of KL could affect nearest-prototype behavior. The paper also does not explain how the "strictly positive" condition (A1) is enforced at test time when embeddings may have near-zero entries.

### Trivial

None.

## Nice-to-Haves

- Report standard detection metrics (flag=positive) for comparability with prior work.
- Include statistical significance across multiple runs or seeds.
- Add explicit quantitative comparison to prior detectors (LID, Mahalanobis, feature squeezing).
- Report clean-image false positive rate (the cost of deploying the detector).
- Sensitivity analysis on L₀ threshold τ and training loss weights ω_KL, ω_L₀.
- Analyze the train-test mismatch between the sigmoid surrogate for L₀ (φ=0.5 during training) and the hard threshold (τ=0.75 at inference).

## Removed Points

These are flagged for removal from the input review; treat with caution.

- *Criticism about missing quantitative comparison to prior detectors in Section 2*: The paper's Section 2 surveys related work but does not include a head-to-head comparison table. This is a reasonable suggestion but the paper's evaluation focus is on its own framework, and the absence does not invalidate results. Moved to Nice-to-Haves.
- *Criticism about Theorem 1 being "vague" and "partially circular"*: The theorem says "there exists a coordinate i where the gap between the true class prototype c*_i and the predicted adversarial class prototype ĉ_i is sufficiently large." For a given attack targeting class j, ĉ_i = c^j_i, which is not circular—it refers to the prototype of the class the attack pushes toward. The critic's claim of circularity is not supported as written.
- *Criticism that the L₀ metric definition creates "circular dependency"*: The L₀ metric uses μ(c,p) = (1/d) Σ|c_i - p_i| as a threshold reference point. This is a common normalization technique, not a circular dependency. The dependence on average deviation is by design (determining which coordinates are "significantly" perturbed relative to the background level).
- *Criticism about "no statistical significance / variance"*: Conflating "not reported" with "not done." Many papers in this field report single-run results. This is a nice-to-have, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the evaluation metrics.** Adopt standard detection definitions (flag=positive) or at minimum report both the paper's definition and the standard definition side by side so readers can compare with prior work.

2. **Evaluate against an adaptive attack.** Construct an attack objective that directly minimizes disagreement between KL and L₀ predictions while targeting a wrong class. This is the single most important missing experiment for establishing practical value.

3. **Clarify the norm used in the theory.** Specify the norm in Assumption A2 and reconcile it with the ℓ∞-bounded attacks used in experiments. If the theory holds for ℓ∞, state this explicitly.

4. **Report full-set detection as the primary result.** Position the Theorem-Compliant results as supporting analysis rather than headline numbers, since the compliant partition cannot be identified at inference time.

5. **Quantify what fraction of attacks/classes satisfy the theorem's conditions in practice.** This would help readers understand the coverage of the theoretical guarantee.

## Score and Decision

### Calibration

**Round 1 bracket:** I estimate the paper sits between 4.0 and 5.5 based on comparison with anchors.

**Anchor comparisons (all from calibration retrieval):**

| Path | Avg Human Score | Round | Comparison to KOALA |
|------|----------------|-------|---------------------|
| Statistical Compressive Sensing Detection (kz78RIVL7G) | 2.60 | R1 | Weaker method, no theory, similar lack of adaptive attacks — KOALA is stronger |
| Multi-Task Consistency Detection (adhxppqQAn) | 3.75 | R1 | Similar detection-via-inconsistency paradigm, no theory, only PGD — KOALA is stronger |
| CARSO (xdnoULh5Sv) | 4.00 | R1 | Adversarial defense with adaptive attacks but unclear novelty — comparable quality |
| Prototype OOD Detection (J2we1sVd9m) | 4.60 | R2 | Prototype-based detection, mixed reviews — comparable, KOALA has clearer novelty |
| Cluster-Driven Adversarial Contrastive (rlsWIBDWhW) | 5.50 | R2 | Stronger empirical evaluation but limited theoretical contribution — different area |
| DDAD Two-Pronged Defense (RzdtpxL0H5) | 6.20 | R1 | Theory + adaptive attacks + comprehensive evaluation — stronger than KOALA |
| Certified Calibration (uuPkll6i7m) | 6.75 | R1 | Strong theoretical contribution, accepted — stronger than KOALA |

**Narrowing:** KOALA has a genuinely novel core idea (complementary KL+L₀ metrics) and a formal theorem, which place it above the 2.6–3.75 detection papers. However, the non-standard evaluation metrics and lack of adaptive attacks are more serious flaws than the issues in the ~5.0–5.5 papers. The paper sits between the 4.0 (CARSO) and 4.6 (Prototype OOD Detection) anchors.

**Final score: 4.5**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>