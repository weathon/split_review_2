Now I have enough information to produce the final review. Let me put it all together.

## Summary

KOALA proposes an adversarial detection method based on disagreement between two complementary similarity metrics — KL divergence (sensitive to dense, low-amplitude perturbations) and an L₀-based score (sensitive to sparse, high-impact changes). The paper provides Theorem 1 establishing conditions under which this disagreement guarantees detection, and a lightweight fine-tuning procedure using only clean images. Experiments are conducted on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet under PGD, CW, and AutoAttack.

## Strengths

- **A principled, geometrically motivated detection criterion.** The central idea — detecting adversarial examples via disagreement between KL divergence and an L₀-based score — is clean, well-motivated, and grounded in a genuine observation about the geometry of norm-bounded attacks (Sections 3.1, Figure 1). Unlike many detection methods that rely on ad hoc feature statistics, KOALA's detection rule has a clear rationale.

- **A formal theorem with an explicit proof sketch.** Theorem 1 and its supporting propositions (Section 3.2) provide a mathematical framework connecting inter-class prototype separation to guaranteed detection. Having explicit, testable conditions that *provably* force metric disagreement is a genuine theoretical contribution that most detectors in the literature lack.

- **Lightweight training requirement.** The fine-tuning procedure (Section 3.3) uses only clean images — no adversarial examples, no architectural modifications, no adversarial training. This makes KOALA a practical plug-and-play solution for existing models.

## Weaknesses

### Fatal
None.

### Major

- **Non-standard evaluation metrics that conflate detection with classification.** The confusion matrix (lines 186–191) defines TP as any attacked input that is *either* flagged as attack *or* correctly classified, and FP as any clean input that is misclassified — even if the detector correctly did not flag it. This means the precision (0.94) and recall (0.81) reported in the abstract do not measure what a reader would assume. They evaluate a combined classification+detection system under a rubric that is not comparable to any prior detection work. This is a structural evaluation issue: the paper's central empirical claims rest on metrics that measure something other than what readers (and the paper's own abstract) claim to measure.

- **No comparison to any existing detection method.** The paper extensively discusses prior detectors (NIC, feature squeezing, LID, MagNet, Mahalanobis, CADet, etc.) in Section 2 but evaluates against none. Without baselines, it is impossible to assess whether KOALA improves upon, matches, or falls behind the state of the art. This gap substantially weakens the claim of contribution.

- **The theoretical guarantee covers a limited and varying fraction of test data — with minimal discussion of this limitation.** On ResNet/CIFAR-10 (ε=2/255), the theorem covers 3345/5000 = 67% of test samples; on CLIP/Tiny-ImageNet, only 510/5000 ≈ 10% (Table 1). On the non-compliant majority (90% for CLIP), precision drops to 0.62–0.78 and recall to 0.42–0.84. While the theorem's conditions are mathematically sound, the paper does not adequately frame or discuss this limited coverage as a limitation of the method's practical usefulness.

- **No evaluation against adaptive attacks.** The paper criticizes prior detectors for lacking "formal proof-of-correctness guarantees against adaptive adversaries" (line 48), yet KOALA itself is evaluated only against standard attacks (PGD, CW, AutoAttack) that do not attempt to bypass the detection rule. Since the KL-L₀ disagreement criterion is simple, differentiable, and fully known to a white-box adversary, an adaptive attack that directly optimizes against the agreement constraint is a natural stress test that is missing.

### Minor

- **No sensitivity analysis for key hyperparameters.** The L₀ threshold τ=0.75, sigmoid temperature φ=0.5, and loss weights ω_L₀=0.9, ω_KL=0.1 (justified only as "L̂₀ is harder to optimize") are set without any ablation or sensitivity study showing how detection performance varies with these choices.

- **Performance varies dramatically across architectures without deep analysis.** On ResNet/CIFAR-10, KL+L₀ achieves the best adversarial accuracy (57.32% PGD, Table 3). On CLIP/Tiny-ImageNet, the same KL+L₀ model achieves only 26.50% PGD accuracy, far below KL-only (60.02%) or L₀-only (53.31%) models (Table 4). The paper offers a plausible explanation (different pre-training objectives) but does not thoroughly analyze why the method's core strength is architecture-dependent.

### Trivial
None.

## Nice-to-Haves

- Report standard detection metrics (TPR, FPR, AUC) alongside the proposed combined metrics to enable direct comparison with prior work.
- Include confidence intervals or variance estimates across multiple fine-tuning seeds.
- Validate the sigmoid-based L₀ surrogate against the true discrete L₀ metric during inference.
- Show a curve of theorem coverage vs. prototype separation threshold (not just two data points).
- Evaluate against an adaptive attack that directly optimizes against the KL-L₀ disagreement criterion.

## Removed Points

These points appeared in the input review but were removed after paper verification:

- "L₀ metric has circular dependence that the proof may not account for" — The paper defines the metric transparently (Eq. 2). The claim that the proof does not handle this cannot be verified because the full proof is in the appendix (stripped by the parser). Not a verifiable weakness.
- "KL direction asymmetry (KL(c||p) vs KL(p||c)) not justified" — The paper clearly states the direction used. This is a standard design choice, not a flaw.
- "Three-metric model (KL+L₀+Cosine) outperforming two-metric (KL+L₀) on CLIP undermines the core argument" — The paper explicitly addresses this (lines 216–218), explaining it is an artifact of classification collapse and distinguishing it from the principled approach.
- "No limitations section" — This is a formatting preference, not a substantive weakness. The paper does discuss limitations implicitly (e.g., the CLIP coverage issue in the Table 1 discussion).
- "Section-by-Section Notes" items that are observations without being specific, verifiable weaknesses — removed per filtering rules.

## Novel Insights

The harsh critic's most valuable observation is that the evaluation metrics (lines 186–191) effectively define the detection task to include correct classification as part of a "successful" outcome, which is non-standard and makes the headline results (precision 0.94, recall 0.81) misleading when presented without caveat in the abstract. This is a genuine insight that the paper's authors should address, as it is the single largest barrier to comparability with prior work. None beyond the paper's own contributions and the above observation.

## Suggestions

1. **Fix the evaluation metrics.** Separate detection evaluation (binary â vs a, using standard precision/recall/AUC) from classification evaluation. Report both.
2. **Add at least 2–3 baseline comparisons** (e.g., Mahalanobis [Lee et al., 2018], LID [Ma et al., 2018], feature squeezing [Xu et al., 2018]) on the same models, datasets, and attacks.
3. **Add an adaptive attack** that directly optimizes against the KL-L₀ disagreement criterion.
4. **Honestly characterize the theorem's coverage** — add a figure showing coverage vs. prototype separation margin, and discuss the practical implications of limited coverage (especially the 10% coverage on CLIP).
5. **Run a hyperparameter sensitivity study** for τ, φ, and the loss weights.

---

## Calibration Report

All anchors retrieved across rounds (paths, avg score, round, itemized?):

| Path | Avg Score | Round | Itemized? | Comparison to KOALA |
|------|-----------|-------|-----------|---------------------|
| /home/.../Uj0h13lVrR.md (KL Divergence GFlowNets) | 1.00 | R1 (bracket) | No | Unrelated topic, much lower quality |
| /home/.../5lUdTogEL3.md (Person Re-ID) | 1.00 | R1 | No | Unrelated |
| /home/.../5kMwiMnUip.md (LLM Jailbreaking) | 1.40 | R1 | No | Unrelated |
| /home/.../u1cQYxRI1H.md (Diffusion) | 10.00* | R1 | No | Outlier (10.0 avg but topic mismatch) |
| /home/.../4Hf5pbk74h.md (Nearest Neighbors) | 2.33 | R1 | No | About improving decision boundaries, not detection |
| /home/.../kz78RIVL7G.md (Compressive Sensing Detection) | 2.60 | R1 | **Yes** | Detection paper with test set leakage, no novelty. KOALA is clearly stronger. |
| /home/.../fiTpna7fO5.md (Multi-attacks) | 3.25 | R1 | No | About generating multi-image attacks, not detection |
| /home/.../qx07JhIs8E.md (TRADES overestimation) | 2.33 | R1 | No | About adversarial training, not detection |
| /home/.../ywGSgEmOYb.md (Fine-tuning backdoors) | 4.40 | R1 | **Yes** | Backdoor defense, not adversarial detection. KOALA has stronger theory. |
| /home/.../r5d8zkYizS.md (Kernel eigenvalues) | 5.33 | R1 | **Yes** | Theory paper about adversarial examples. KOALA has more applied theory but weaker eval. |
| /home/.../qqZijHRcA5.md (Membership inference) | 4.25 | R1 | No | About privacy, not adversarial detection |
| /home/.../G3OCarOfxx.md (Clean gen/robust overfitting) | 4.80 | R1 | No | About adversarial training theory |
| /home/.../RzdtpxL0H5.md (DDAD) | 6.20 | R1 | **Yes** | Detection+defense with theory and SOTA comparisons. KOALA has cleaner theory but much weaker evaluation. |
| /home/.../I4Lq2RJ0eJ.md (Unlearnability) | 6.00 | R1 | No | About unlearnable examples, not detection |
| /home/.../xmQuUqSynb.md (Right to be forgotten) | 5.75 | R1 | No | About machine unlearning |
| /home/.../pE6gWrASQm.md (Adv training subset) | 6.50 | R1 | No | About adversarial training |
| /home/.../BXMoS69LLR.md (Blind MI baselines) | 4.50 | R2 (narrow) | No | About membership inference evaluation |
| /home/.../NI0RsRuFsW.md (Trojan detection) | 4.00 | R2 | No | About Trojan detection, different subfield |
| /home/.../R1crLHQ4kf.md (Audio detection) | 5.00 | R2 | **Yes** | Audio adversarial detection with extensive experiments and adaptive attacks. KOALA has stronger theory but much weaker evaluation. |
| /home/.../EWP9BVRRbA.md (VLM detection) | 4.00 | R2 | No | VLM adversarial detection, different modality |
| /home/.../KX5hd1RhYP.md (ACR metric) | 4.67 | R2 | No | About evaluation metrics for randomized smoothing |

**Round 1 bracket**: The paper sits between the 2.60 detection paper (strong-reject territory, major flaws) and the 5.00–5.33 papers (reject but with real contributions). The bracket was **[2.6, 5.0]**.

**Round 2 narrowing**: Comparing itemized anchors:
- vs "Compressive Sensing Detection" (2.60): That paper had test set leakage (-9.16), missing related work (-10.00), and poor presentation (-10.00). KOALA has a *stronger theoretical contribution (+10.00 vs +2.09/+0.40)* and a cleaner evaluation design. KOALA is clearly above 2.60.
- vs "Audio Detection" (5.00): That paper had *extensive experiments (+10.00), adaptive attacks (+0.78), and baseline comparisons (+6.23)*. KOALA has a *stronger theoretical contribution* but vastly weaker evaluation (no baselines, non-standard metrics, no adaptive attacks). KOALA is clearly below 5.00.
- vs "Kernel Eigenvalues" (5.33): That paper had a strong theory (+10.00, +9.98) but limited practical significance (-3.00, -9.98). KOALA has a more applied theory that directly leads to a detection method, but its evaluation gaps are more severe than that paper's experimental insufficiency.

**Final placement**: The four decisive-level weaknesses (non-standard metrics: -10.00, no baselines: -10.00, limited coverage: -9.98, no adaptive attacks: -9.46) heavily outweigh the three strong-to-decisive strengths (principled criterion: +7.02, formal theorem: +10.00, lightweight training: +9.10). The paper is meaningfully stronger than the 2.60 anchor but clearly weaker than the 5.00 and 5.33 anchors, placing it in the **3.0–4.0 range**.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>