Based on the calibration, I have a clear picture. Let me write the final review.

**Round 1 Bracket: 3.0 – 4.5.** KOALA is more developed than the score-3.0 anchor ("Detecting Adversarial Examples," KAWlH5pfQu), which also lacks adaptive attacks and baseline comparisons but has less theoretical grounding and fewer ablations. It falls substantially short of the score-6.2 anchor ("DDAD," RzdtpxL0H5), which includes adaptive attack evaluation and SOTA comparisons. The bracket is 3–4.5 and no further narrowing pass is needed — the paper sits at approximately **4.0**.

---

## Summary
KOALA is a plug-in adversarial detector that flags inputs when two complementary nearest-prototype classifiers—one using KL divergence (sensitive to dense, low-amplitude perturbations) and one using an L0-based distance (sensitive to sparse, high-impact changes)—disagree on the predicted class. The method requires only lightweight fine-tuning on clean images and provides Theorem 1, a formal guarantee that detection is certain when class prototypes are sufficiently separated. Experiments are run on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet under PGD, CW, and AutoAttack.

## Strengths
- **Principled metric pairing (Section 3.1, Figure 1).** The observation that energy-bounded perturbations must be either dense-low-amplitude or sparse-high-impact, and that KL divergence and L0 distance are geometrically complementary along this axis, is clean and well-motivated—crisper than typical ad-hoc statistical detectors.
- **Lightweight training recipe.** No adversarial training, no architectural changes, only a brief clean-data fine-tuning step. The plug-in design is consistent with this motivation and represents a genuine practical advantage.
- **Systematic ablation (Tables 2 and 3).** All single and pairwise metric combinations are evaluated, giving the reader real information about what each metric contributes rather than just presenting the winning configuration.

## Weaknesses

### Fatal
None that are unambiguously verifiable from the paper as written.

### Major

- **No adaptive attack against the detector.** All experiments (Section 4) evaluate PGD, CW, and AutoAttack, which are optimized to fool the *classifier*, not KOALA's detection mechanism. An adversary who knows KOALA flags inputs when ŷ_KL ≠ ŷ_L0 can craft an attack that maintains agreement between the two predictors while still causing misclassification—treating the disagreement condition (Eq. 4) as a differentiable penalty. Theorem 1 does not preclude this: its geometric separation conditions (A1–A4, inter-class coordinate gap) are not guaranteed to hold under an adversary specifically optimizing to violate them. In adversarial ML, this gap is not minor—detection methods that fail under adaptive attack have been systematically shown to provide false security, which is precisely why the paper cites Carlini & Wagner (2017). The absence of adaptive attack evaluation leaves the paper's central empirical claim unvalidated under any realistic threat model.

- **Circular empirical validation of Theorem 1.** Experiment 1 (Table 1) partitions the test set into "Theorem-Compliant" and "Non-Compliant" samples, then reports perfect detection (Acc=Prec=Rec=F1=1.0) on the compliant subset and calls this "strong empirical support for our theoretical guarantee" (Section 4.2). By construction, theorem-compliant samples are those satisfying Theorem 1's sufficient conditions, which *guarantee* detection—observing perfect detection is mathematically trivial; it is the theorem restated, not an independent verification. The operationally meaningful question—what fraction of real adversarial examples satisfy the conditions?—is answered implicitly by the sample sizes in Table 1: for CLIP/Tiny-ImageNet at ε=2/255, only 510/5000 (~10%) are theorem-compliant. On the majority non-compliant subset, precision drops to 0.63 and recall to 0.84. Experiment 1 does not advance beyond circular self-validation.

- **No comparison to prior detectors.** Section 2 carefully reviews LID, Feature Squeezing, Mahalanobis, MagNet, CADet, NIC, and several others, but none appear as quantitative baselines in the experiments. The paper positions KOALA as superior because of its formal guarantee, but never demonstrates empirically that it achieves better detection than these methods. Without such comparisons, the precision/recall numbers in the abstract (0.94/0.81 on ResNet/CIFAR-10, 0.66/0.85 on CLIP/Tiny-ImageNet) are uninterpretable in context.

- **Non-standard TP definition inflates detection metrics.** Section 4.2 defines `TP := [a=1] ∧ [(â,ŷ)=(1,⊥) ∨ (â,ŷ)=(0,y*)]`. The second disjunct counts adversarial attacks as true positives even when the detector does **not** flag them, as long as the model classifies correctly despite the attack. A standard detection TP should be: attacked input that is *flagged* by the detector. This non-standard definition inflates recall by crediting the detector for adversarial examples it did not catch but that failed to fool the model anyway. The headline precision/recall numbers are therefore unreliable without knowing how many TPs fall into each category.

### Minor

- **Misleading Table 4 caption vs. CLIP results.** The caption for Table 4 reads "The KL+L0 objective demonstrates superior adversarial accuracy," but the table shows L0-alone achieves 25.43% vs. KL+L0's 16.18% under AutoAttack at ε=2/255, and 37.49% vs. 11.91% under CW at ε=2/255. The text body does acknowledge and explain the inconsistency (Section 4.4), but the caption directly contradicts the data.

- **CLIP results reveal limits of the theoretical framework.** For CLIP, the best detection combination is KL+L0+Cosine (Table 2), but the authors explain this works "by breaking the underlying classification rather than preserving it" (Section 4.3). Combined with L0-alone outperforming KL+L0 for adversarial accuracy (Table 4), these results show the theoretical framework does not reliably predict which metric combination will work best in practice—the method is more empirically contingent than the formal framing suggests.

- **Assumption A1 constrains embedding representational capacity.** Requiring all embeddings to be non-negative and sum to 1 (a probability simplex constraint, enforced by softmax normalization) is a significant constraint compared to standard cosine or Euclidean feature spaces. The paper asserts this is "mild and practical" (Section 3.2) without quantifying the practical cost to classification capacity.

### Trivial
- None.

## Nice-to-Haves
- An adaptive attack that adds a disagreement penalty `λ·𝟙[ŷ_KL ≠ ŷ_L0]` to the standard attack objective would either validate KOALA's real-world utility or honestly bound its scope to non-adaptive adversaries.
- A coverage analysis of Theorem 1's conditions as a function of ε, dataset, and attack type (i.e., what fraction of adversarial examples satisfy the geometric separation condition) would convert Experiment 1 from circular self-validation into a useful characterization of when the guarantee applies.
- Reporting what fraction of TPs are detector-flagged vs. model-correct-despite-attack would clarify the meaning of the current detection metrics.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Assumption A3 violated by adaptive adversary (standalone):** The harsh critic flagged that adaptive adversaries might specifically violate A3's coordinate-wise bound. This is real but fully subsumed by the broader adaptive attack weakness already retained as Major. Keeping it separately adds no new content.
- **Representational cost of simplex constraint (as Major):** Downgraded to Minor. While the softmax normalization of feature embeddings is unusual, the paper still demonstrates reasonable clean accuracy (94.78% for ResNet, 55.88% for CLIP), so the constraint is not fatally limiting in practice.

## Novel Insights
The core observation that KL and L0 stability bands can be formally shown to be mutually exclusive for sufficiently separated prototype classes—exploiting the geometry of energy-bounded perturbations—is a clean contribution. The systematic ablation showing that Cosine similarity degrades performance when combined with KL+L0 (Tables 2, 3) is an interesting negative finding that clarifies why the specific metric combination matters. However, the formal guarantee's narrow operational coverage (~10% of CLIP test samples) and the absence of adaptive attack evaluation substantially limit the impact of these insights.

## Suggestions
1. Evaluate an adaptive adversary that minimizes `L_attack + λ·soft(ŷ_KL ≠ ŷ_L0)` using a differentiable relaxation of the disagreement condition; report detection rate before and after.
2. Reframe Experiment 1 as a coverage analysis: for each attack type and ε, report what fraction of generated adversarial examples satisfy Theorem 1's geometric conditions.
3. Replace the current TP definition with the standard one (attacked input flagged by detector) and separately report attack-failure rate (adversarial examples that failed to fool the model).
4. Add at least one prior detector baseline (Feature Squeezing or Mahalanobis) using the same evaluation protocol to contextualize the precision/recall numbers.
5. Fix the Table 4 caption to accurately reflect that L0-alone dominates for CLIP under strong attacks.

---

## Score and Decision

**Anchor papers:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| KAWlH5pfQu | 3.00 | R1 | Lightweight adversarial detector with theoretical justification; also lacks adaptive attacks and SOTA baselines — similar structural gaps to KOALA but less systematic ablation |
| kz78RIVL7G | 2.60 | R1 | Statistical detector, no adaptive attacks, no SOTA comparison; weaker theoretical grounding than KOALA |
| lEsNGN1SjG | 2.00 | R1 | Information-theoretic classifier; strong reject |
| dIK7GpOwNY | 3.00 | R1 | Robustness metric paper; different scope |
| Oi6BhzIu7R | 4.67 | R1 | Test-time adversarial defense; borderline reject, more empirically grounded than KOALA but no formal theorem |
| R1crLHQ4kf | 5.00 | R1 | Output distribution detector for audio; compares to some baselines, no formal guarantee |
| nKSkM5h2VN | 5.33 | R1 | Test-time defense via diffusion; similar detection tier but no adaptive attacks addressed |
| RzdtpxL0H5 | 6.20 | R1 | DDAD with distributional discrepancy; includes adaptive white-box attacks and SOTA comparison — clearly above KOALA |
| hXA8wqRdyV | 6.14 | R1 | Adaptive jailbreaking paper; different topic |
| DFTHW0MyiW | 7.00 | R1 | RL robustness; different scope |
| F5dhGCdyYh | 7.33 | R1 | Information-theoretically detectable attacks; different scope |

**Bracketing:** Round 1 anchors place KOALA between 3.0 (KAWlH5pfQu — similar adversarial detection paper with same critical gaps) and 6.2 (RzdtpxL0H5 — detection paper that includes adaptive attacks and baselines). KOALA is meaningfully stronger than KAWlH5pfQu (formal theorem, two architectures, systematic ablation), but the three major gaps (no adaptive attack, no baselines, non-standard TP definition) prevent it from reaching the 6+ tier. Initial bracket: 3.5–5.

**Narrowing:** The missing adaptive attack evaluation is the single most important gap for a detection paper at ICLR — it is the standard evaluation requirement and the paper cites the paper (Carlini & Wagner) that established this norm. The circular Experiment 1, the non-standard TP definition, and the absence of prior detector comparisons further weaken the empirical claims. The formal theorem, while mathematically valid, covers only ~10% of CLIP test cases. Compared to score-5.0 anchor R1crLHQ4kf (which at least provides some baseline comparisons), KOALA's gaps are more fundamental. Final score: **4.0**.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>