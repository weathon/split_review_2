Now I have the full picture. Let me write the final consolidated review.

## Summary

KOALA proposes a reactive adversarial detector based on a simple but well-motivated principle: two complementary similarity metrics (KL divergence for dense/low-amplitude perturbations and an L₀-based metric for sparse/high-impact perturbations) are used as nearest-prototype classifiers, and an attack is flagged when these two classifiers disagree. The paper provides a formal theorem stating conditions under which this disagreement is guaranteed, and a lightweight fine-tuning procedure that requires only clean images. Experiments on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet are presented.

## Strengths
- **Well-motivated core intuition (Section 3.1, Figure 1).** The observation that adversarial perturbations under an energy budget manifest as either dense/low-amplitude or sparse/high-impact changes, and that these call for different similarity metrics, is clearly articulated and provides a genuinely useful conceptual lens for detection.
- **Informative ablation study (Experiment 2, Table 2).** Testing multiple metric combinations (KL+L0, L0+Cosine, KL+Cosine, KL+L0+Cosine) is the right experimental design. On ResNet/CIFAR-10, KL+L0 outperforms alternatives across all metrics, substantiating the claimed complementarity.
- **Practical advantage (Section 3.3).** KOALA fine-tunes only on clean images with no adversarial training and no architectural changes, making it a lightweight, plug-and-play option for existing models. This is a genuine practical advantage over methods requiring expensive adversarial example generation.

## Weaknesses

### Fatal
None.

### Major
- **Evaluation metrics conflate detection with classification (Section 4.2, lines 188–191).** The confusion matrix definitions are non-standard in a way that inflates apparent detection performance. An attacked input is counted as a True Positive even when the detector fails to flag it (â=0), as long as the nearest-prototype classifiers happen to predict the correct class. Conversely, a clean image correctly not flagged (â=0) is counted as a False Positive if the prototypes predict the wrong class. This means the headline precision (0.94) and recall (0.81) do not measure detection performance in the standard sense. A reader would reasonably expect these to mean something else, and the paper does not justify this departure. This is the most serious weakness because it undermines the interpretability of the paper's primary quantitative claims.

- **No evaluation against adaptive attacks.** KOALA's detection rule is simply checking for disagreement between two nearest-prototype classifiers. An attacker aware of the defense would optimize a perturbation that keeps both KL and L0 predictions in agreement on a wrong class, directly bypassing the detection mechanism. The paper mentions adaptive adversaries in its related work discussion (line 48) but provides no evaluation against them. For a detection paper, this is a structural gap — the claimed detection performance cannot be assumed to hold under an informed adversary.

- **Table 4 caption is factually incorrect.** The caption states "The KL+L0 objective demonstrates superior adversarial accuracy" for CLIP/Tiny-ImageNet, but the table data shows the opposite: KL+L0 achieves lower adversarial accuracy than KL-only or L0-only under multiple settings (e.g., PGD ε=2/255: KL+L0 26.50% vs KL-only 60.02%; CW ε=2/255: KL+L0 11.91% vs L0-only 37.49%). The caption appears to be a copy-paste error from Table 3.

### Minor
- **Compliance partition not reproducible (Experiment 1, line 185).** The test set is split into "Theorem-Compliant" and "Non-Compliant" samples based on "sufficient inter-class prototype separation," but the specific threshold or measure used is never stated. Without this information, the experiment cannot be replicated, and the reported perfect scores on the compliant subset cannot be independently evaluated.
- **L₀ threshold τ=0.75 (Equation 2) is used with no sensitivity analysis.** Results may depend on this choice, but the paper provides no sweep or justification.
- **Connection between input-space ℓ∞ bounds (used in experiments) and feature-space energy bounds (Assumption A2) relies on an unquantified Lipschitz constant.** For CLIP ViT-B/32, the Lipschitz constant could be large enough that an ℓ∞ bound of 4/255 in pixels corresponds to a substantial ||δ|| in embedding space, potentially violating A2.
- **The "semantics-free" claim (Abstract, Section 1) is ambiguous.** The ResNet setup (mean of training embeddings) qualifies, but the CLIP setup obtains prototypes from a text encoder using semantic prompts ("a photo of [CLASS]"), which injects semantic information — contradicting the strict "semantics-free" framing.
- **Test set composition (clean-to-attacked ratio) is not reported.** Since precision depends on this ratio, the reported precision numbers cannot be properly contextualized.

### Trivial
None.

## Nice-to-Haves
- Sensitivity analysis for τ over a reasonable range (e.g., {0.25, 0.5, 0.75, 0.9}).
- Separate reporting of false positive rate on clean images, which is the most important single metric for a practical detector.
- Reporting detection performance broken down by attack type (PGD, CW, AutoAttack).

## Removed Points
*These points are flagged to be removed; treat them with caution.*

1. **Γ_i(ε) not defined in main text** — REMOVED because the full proof is in Appendix B, which is stripped by the PDF parser. Per policy, the original submission contains this content.
2. **Requiring knowledge of ĉ at inference** — REMOVED because this is a theoretical condition in the theorem's premise, not an inference-time requirement. The related reproducibility concern about the experimental partition is already captured elsewhere.
3. **L₀ metric having "circular dependency"** — REMOVED because using mean absolute deviation as an adaptive threshold is a deliberate and sensible design choice, not a flaw.
4. **KL asymmetry not discussed** — REMOVED: the choice of KL(c||p) over KL(p||c) is a design decision for a nearest-prototype comparison; with normalized positive features it is stable and reasonable.
5. **Assumption A3 factor 3/2 being arbitrary** — REMOVED because the full derivation is in the parser-stripped appendix; the factor cannot be assessed without the proof.
6. **Not reporting per-attack-type detection results** — REMOVED because Table 1 reports under PGD specifically, and Tables 3–4 break down adversarial accuracy by attack type. The claim that results are "aggregated" is not supported.
7. **Compliant subset experiment being a "tautology"** — REMOVED because empirically verifying that the theorem's conditions are met on real data and that detection works as predicted is a meaningful validation step.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Replace the evaluation metrics with standard detection-only definitions (TP = attacked input correctly flagged, â=1; FP = clean input incorrectly flagged, â=1) and report classification accuracy separately. This would give an honest picture of detection performance.
2. Evaluate against adaptive attacks that jointly optimize against both KL and L0 nearest-prototype classifiers.
3. Specify the precise criterion used for the Theorem-Compliant partition in Experiment 1.
4. Correct Table 4's caption to accurately reflect the CLIP results.
5. Add sensitivity analysis for τ and report the clean-to-attacked ratio in the test set.

## Score and Decision

The paper presents a genuinely well-motivated core idea and a practical method that avoids adversarial training. The ablation study on ResNet/CIFAR-10 provides meaningful support for the claimed metric complementarity. However, the evaluation has two structural problems: (1) the detection metrics are non-standard in a way that inflates the headline numbers, and (2) there is no evaluation against adaptive attacks — a standard requirement for detection papers. Additionally, Table 4 contains a factual caption error that misrepresents results. These issues are addressable but as presented, the paper's central claims are not adequately supported by the evidence.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>