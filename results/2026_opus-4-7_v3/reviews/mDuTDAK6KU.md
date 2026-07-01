Now let me read the remaining experimental tables to verify CLIP results and the confusion matrix definitions more carefully.Now I have a thorough understanding of the paper. Let me submit the draft review before calibration.Now let me calibrate with Round 1 — bracketing across score bands.Let me read key anchor papers to calibrate the score.Now I have enough calibration data. Let me form my bracket and finalize.

**Round 1 Bracket Analysis:**

| Band | Anchor | Score | Comparison to KOALA |
|------|--------|-------|---------------------|
| Strong reject (<1.5) | Various non-papers | 1.0 | KOALA is far above these — has real theory and experiments |
| Reject (1.5-3.5) | KAWlH5pfQu "Detecting Adversarial Examples" | 3.0 | Very similar weaknesses (no baselines, no adaptive attacks), but KOALA has stronger theory and more honest experimental design |
| Reject (1.5-3.5) | kz78RIVL7G "Statistical Adversarial Detection" | 2.6 | Similar gaps; KOALA is more theoretically grounded |
| Borderline (3.5-5.5) | EWP9BVRRbA "NEARSIDE" | 4.0 | Similar profile: novel idea, no adaptive attacks, limited baselines (NEARSIDE has 1 baseline, KOALA has 0) |
| Borderline (3.5-5.5) | V4oQAR8uoE "RPD Textual Defense" | 5.33 | Different domain; more complete evaluation |
| Weak Accept (5.5-7.5) | RzdtpxL0H5 "DDAD" | 6.2 | Has theory AND baselines AND adaptive attacks — much more complete than KOALA |
| Accept (7.5-8.5) | IGzaH538fz "GNNCert" | 8.0 | Deterministic certification with comprehensive evaluation |

**Initial bracket: 3.5 – 5.0**

KOALA is clearly above the 3.0 papers (better theory, more honest methodology) but below the 6.2 DDAD which has comparable theoretical motivation plus proper baselines and adaptive evaluation. The absence of ANY baseline comparison and ANY adaptive attack evaluation are the most damaging gaps — the same weaknesses that anchored KAWlH5pfQu at 3.0 and kz78RIVL7G at 2.6. KOALA's stronger theory pushes it into the 4.0 range. The CLIP results partially undermining the narrative push against a higher score.

Now let me write the final review.Now I have all the information needed. Let me compose the final consolidated review.

---

## Summary
KOALA proposes a reactive adversarial detector based on disagreement between two complementary nearest-prototype classifiers: one using KL divergence (sensitive to dense, low-amplitude perturbation shifts) and one using an L0-based metric (sensitive to sparse, high-impact changes). The paper provides a formal detection guarantee (Theorem 1) showing that under sufficient inter-class prototype separation, no single perturbation can simultaneously fool both classifiers. Experiments on ResNet-18/CIFAR-10 and CLIP ViT-B/32/Tiny-ImageNet evaluate the approach with PGD, CW, and AutoAttack.

## Strengths

- **Well-motivated geometric intuition with formal backing.** The core observation — that energy-bounded perturbations must trade off between sparse high-impact and dense low-amplitude manifestations, captured by complementary KL and L0 metrics — is clean and elegantly communicated (Figure 1, Section 3.1). Theorem 1 provides an explicit, falsifiable detection guarantee, and the proof sketch through Propositions 2–4 showing the incompatibility of KL-flip and L0-flip conditions is logically structured. This is a genuine theoretical contribution beyond the empirical-only detection literature.

- **Honest experimental methodology for theorem validation.** Partitioning test data into theorem-compliant and non-compliant subsets (Table 1) and reporting both is a commendable methodological choice. Perfect recall on compliant subsets (all 1.0) provides direct empirical support for the theoretical claim, and the explicit reporting of degraded performance on non-compliant subsets shows intellectual honesty.

- **Informative ablation study with candid analysis.** The comparison of metric combinations in Table 2 isolates the contribution of the KL+L0 pairing vs. alternatives (L0+Cosine, KL+Cosine, all three). The discussion of the anomalous CLIP result — where L0+KL+Cosine achieves high detection by breaking classification rather than preserving it (Section 4.3) — is a notable instance of self-critical analysis.

- **Lightweight and practical design.** The method requires only fine-tuning with clean images (no adversarial examples needed) and no architectural changes, which is a practical advantage over many detection approaches.

## Weaknesses

### Fatal
None.

### Major

- **Complete absence of comparison to existing adversarial detectors.** The related work section (Section 2) explicitly positions KOALA against Feature Squeezing, LID, MagNet, NIC, Mahalanobis, and CADet, yet the experimental section contains zero head-to-head comparisons with any of these methods. This means the reader cannot assess whether KOALA's reported numbers (e.g., 0.94 precision / 0.81 recall on ResNet/CIFAR-10, Table 2) are competitive, state-of-the-art, or below existing methods. For a paper proposing a new detection method, establishing comparative standing is essential.

- **No evaluation against adaptive attacks.** All attacks (PGD, CW, AutoAttack) target the original classifier's loss, not KOALA's disagreement mechanism. An adaptive adversary aware of KOALA would craft perturbations that keep both KL and L0 classifiers in agreement on the wrong class — particularly targeting the non-compliant subset where the theorem provides no guarantee (~90% of CLIP samples, ~33–40% of ResNet samples per Table 1). The adversarial detection literature has repeatedly shown that non-adaptive evaluations are insufficient (Carlini & Wagner, 2017; Tramer et al., 2020). A paper emphasizing formal guarantees should be especially rigorous about delineating where those guarantees end.

- **Disconnect between embedding-space theory and pixel-space threat model.** Theorem 1 operates on perturbation δ in embedding space with budget ‖δ‖ ≤ ε, while all experiments use pixel-space perturbation budgets (ε ∈ {2/255, 4/255} in ℓ∞). Assumption A2 invokes Lipschitz continuity of the encoder but neither estimates the encoder's Lipschitz constant nor verifies empirically that pixel-space perturbation budgets map to the theorem's embedding-space regime. Without this bridge, the theorem's guarantee is not directly connected to the experimental threat model.

### Minor

- **Low theorem compliance rate for CLIP undermines generality.** Table 1 shows only ~10% of CLIP/Tiny-ImageNet samples (510–556 out of 5000) satisfy Theorem 1's conditions. On the non-compliant ~90%, precision drops to 0.62–0.63. This sharply limits the practical utility of the theoretical guarantee for transformer-based architectures with contrastive pre-training.

- **CLIP results partially undermine the KL+L0 complementarity narrative.** In Table 4, the KL+L0 combination achieves only 26.5% adversarial accuracy under PGD for CLIP, worse than L0-only (53.31%) or KL-only (60.02%). The paper offers a post-hoc explanation about CLIP's pre-training structure (Section 4.4), but this means the core claimed mechanism does not hold for one of the two tested architectures. The contribution should be scoped more carefully.

- **Conflated evaluation metrics.** The TP definition (Section 4.2) counts as correct both detected attacks (â=1, ⊥) and adversarial examples that the model happens to classify correctly (â=0, y*). Similarly, FP includes clean examples that are misclassified. This conflation blurs the detector's standalone contribution with the classifier's inherent robustness, making it difficult to isolate KOALA's detection mechanism.

- **No sensitivity analysis for threshold τ.** τ = 0.75 is set for ResNet (Section 4.1) without reporting how detection performance varies with τ. Since Proposition 4 requires finding a τ that forces the incompatibility condition, the theoretical-to-practical relationship of this parameter deserves attention.

### Trivial
None.

## Nice-to-Haves
- Estimate or bound the encoder's Lipschitz constant to connect pixel-space ε to the embedding-space budget assumed by Theorem 1.
- Demonstrate that the fine-tuning procedure can increase the fraction of theorem-compliant samples (e.g., pushing CLIP compliance above 10%).
- Report sensitivity of detection performance to τ and the loss weights ω_{L0}, ω_{KL}.
- Scope the claims more precisely to architectures/training regimes where KL+L0 complementarity is demonstrated.
- The abstract claim of suitability for "various data modalities" should be tempered — only image classification on two datasets is evaluated.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Assumption A3 is unjustified as mild"** — The reviewer noted that if a clean embedding has a near-zero coordinate, |δ_i| ≤ 3/2|p_i*| becomes very restrictive. While a fair theoretical observation, this is standard in the sense that the theorem explicitly conditions on its assumptions, and the compliance-partition experiment honestly reports when they fail. Demoted from substantive weakness to a theoretical sharpening suggestion.

- **"Various data modalities" overclaim as a weakness** — Moved to Nice-to-Have since it is a presentation/framing issue, not a core methodological flaw.

- **Formatting/style concerns** — Removed per filtering rules.

## Novel Insights
The core insight that KL divergence and L0-based similarity create complementary "stability bands" in embedding space — where energy-bounded attacks that escape one band necessarily remain within the other — is a genuinely novel geometric perspective on adversarial detection. The formal proof structure (showing incompatibility of flip conditions via Propositions 2–4) provides a principled framework that could inspire future work on multi-metric detection, even though the current experimental validation has significant gaps. The honest partitioning into theorem-compliant vs. non-compliant subsets is also a methodological contribution worth emulating.

## Suggestions
1. Add head-to-head comparisons with at least 2–3 existing adversarial detectors (e.g., Feature Squeezing, LID, Mahalanobis) on the same models and attacks to establish competitive standing.
2. Evaluate under adaptive attacks that jointly optimize against both the KL and L0 classifiers — even if only on the non-compliant subset — to delineate the method's actual robustness boundaries.
3. Quantify the Lipschitz constant of the fine-tuned encoder (empirically or via bounds) to connect the pixel-space threat model to the embedding-space theory.
4. Separate detection accuracy from classification accuracy in the evaluation metrics so the detector's standalone contribution is measurable.
5. Explicitly scope the paper's claims to architectures where KL+L0 complementarity is demonstrated (ResNet-style models), and discuss CLIP as a case where the approach's assumptions are not well-met.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to KOALA |
|-------|------|-----------|-------|---------------------|
| NEMESIS (LLM jailbreaking) | 5kMwiMnUip | 1.40 | R1 | Not a real research contribution; KOALA far above |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Minimal paper; KOALA far above |
| All Pairs Minimax Path | bEgDEyy2Yk | 1.00 | R1 | Code implementation report; KOALA far above |
| Lifelong Person ReID | 5lUdTogEL3 | 1.00 | R1 | Different domain; KOALA far above |
| **Detecting Adversarial Examples (LR)** | KAWlH5pfQu | **3.00** | R1 | **Most comparable: adversarial detection with theory, but also lacks baselines and adaptive attacks. KOALA has stronger theory and more honest methodology.** |
| **Statistical Adversarial Detection** | kz78RIVL7G | **2.60** | R1 | **Similar adversarial detection paper lacking adaptive attacks and strong baselines. KOALA has cleaner theory.** |
| LeBD Backdoor Detection | 7vKWg2Vdrs | 3.25 | R1 | Backdoor domain; limited evaluation; KOALA has stronger theoretical contribution |
| Information-theoretic Safe Classifier | lEsNGN1SjG | 2.00 | R1 | Much weaker paper; flawed theoretical claims |
| RPD Textual Defense | V4oQAR8uoE | 5.33 | R1 | Different domain (NLP); more complete evaluation |
| Adversarial Audio Detection | R1crLHQ4kf | 5.00 | R1 | Audio domain; empirical comparison present |
| **NEARSIDE VLM Detection** | EWP9BVRRbA | **4.00** | R1 | **Similar profile: novel idea, lacks adaptive attacks, but has at least one baseline comparison (JailGuard). KOALA has zero.** |
| REAL Test-Time Defense | Oi6BhzIu7R | 4.67 | R1 | More complete evaluation with baselines |
| **DDAD Distributional Defense** | RzdtpxL0H5 | **6.20** | R1 | **Has theory AND baselines AND adaptive attacks — much more complete than KOALA. Shows what KOALA's evaluation should include.** |
| Illusory Attacks | F5dhGCdyYh | 7.33 | R1 | Accepted; comprehensive evaluation and novel formulation |
| Robust RL Adaptive Defense | DFTHW0MyiW | 7.00 | R1 | Accepted; different domain, thorough evaluation |
| Tree-based RL Attack | HZnnHDrBXD | 5.75 | R1 | Different domain; more complete experiments |
| GNNCert | IGzaH538fz | 8.00 | R1 | Deterministic certification with comprehensive evaluation; much stronger |
| Robust Diffusion Classifier | I5lcjmFmlc | 8.00 | R1 | Comprehensive evaluation with adaptive attacks; much stronger |
| Hölder Stability GNNs | P7KIGdgW8S | 8.00 | R1 | Strong theoretical contribution with thorough evaluation |
| Deep Orthogonal Hypersphere | cJs4oE4m9Q | 8.00 | R1 | Strong method with comprehensive experiments |

**Round 1 bracket: 3.5 – 5.0**

KOALA sits above the 3.0 "Detecting Adversarial Examples" paper (stronger theory, more honest experimental design) but clearly below the 6.2 DDAD (which includes baselines and adaptive attacks). Compared to NEARSIDE (4.0), KOALA has a more rigorous theoretical contribution but NEARSIDE at least compared against one baseline (JailGuard), while KOALA compares against none. The two major experimental gaps — no baselines and no adaptive attacks — are the same weaknesses that drove similar detection papers to scores of 2.6–3.0. KOALA's genuine theoretical contribution and methodological honesty (theorem-compliant partitioning, candid CLIP discussion) lift it above those papers but not enough to reach borderline accept territory, especially given that the core KL+L0 complementarity narrative is contradicted by the CLIP results.

**Final score: 4.0**

This paper presents a genuinely novel theoretical idea — the complementarity of KL and L0 stability bands — with a well-structured formal guarantee. However, the experimental evaluation has two critical gaps that prevent acceptance: the complete absence of comparison to any existing adversarial detector, and the lack of adaptive attack evaluation. These are not minor additions; they are foundational requirements for an adversarial detection paper. Additionally, the CLIP results partially undermine the paper's central narrative about KL+L0 complementarity. The paper needs substantial additional experimentation before it can be properly evaluated for acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>