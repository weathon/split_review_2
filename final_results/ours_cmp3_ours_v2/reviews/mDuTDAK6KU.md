Now let me compose the final review.

## Summary

This paper proposes KOALA, an adversarial detection method that flags attacks when class predictions from two complementary nearest-prototype classifiers — one using KL-divergence (sensitive to dense, low-amplitude perturbations) and one using an L0-based similarity (sensitive to sparse, high-impact changes) — disagree. The paper provides a formal proof (Theorem 1) establishing conditions under which detection is guaranteed, and evaluates on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet under PGD, CW, and AutoAttack. The only training required is fine-tuning the backbone encoder on clean images.

## Strengths

1. **Well-motivated complementary-metrics intuition.** The observation that energy-bounded adversarial perturbations naturally fall into two regimes — dense low-amplitude vs. sparse high-impact — is clearly explained (Section 1, lines 23–27; Figure 1), and the choice of KL divergence and L0-based similarity to target these two regimes is principled and original.

2. **Formal correctness guarantee is a genuine novelty.** Providing explicit conditions under which detection is provably guaranteed (Theorem 1, Section 3.2) is rare in the adversarial detection literature and goes beyond purely empirical approaches. The proof sketch is clearly communicated even though the full proof is in the appendix.

3. **The ablation study (Table 2) is informative and honestly discussed.** The finding that KL+L0 outperforms other metric pairings on ResNet/CIFAR-10 supports the complementarity claim. The honest acknowledgment that the three-metric combination on CLIP/Tiny-ImageNet achieves high detection "by breaking the underlying classification" (lines 216–218) shows good scientific judgment.

4. **Impressive adversarial accuracy on ResNet/CIFAR-10.** The KL+L0 fine-tuned model achieves substantially better adversarial accuracy (57.32% on PGD ε=2/255, 54.60% on ε=4/255) than the baseline (45.5%, 33.11%) or any single-metric alternative (Table 3), showing that the joint optimization genuinely improves robustness on this setup.

## Weaknesses

### Major

1. **Non-standard confusion matrix conflates detection and classification, making headline metrics uninterpretable as detection performance.** The paper defines (Section 4.2, line 188):
   - TP includes cases where the detector *misses the attack* (â=0) but the nearest-prototype classifier happens to predict the correct class (ŷ=y*).
   - FP includes clean inputs where the detector correctly says benign (â=0) but the classifier misclassifies (ŷ≠y*).
   
   Under standard detection definitions, TP means the detector correctly flags an attack; this paper counts missed attacks with correct classification as TPs (inflating recall), and clean misclassifications as FPs (conflating classification error with false alarm). The headline numbers from the abstract — Precision 0.94, Recall 0.81 — are computed under these non-standard definitions and cannot be meaningfully compared with any prior detection method. While the definitions are explicitly stated, calling them "standard metrics: Accuracy, Precision, Recall, and F1-score" (line 190) for "detector metrics" (line 183) is misleading. This issue is structural: the experimental section would need to be re-run with standard detection metrics (TP = detector says attack on attacked input, etc.) for the results to be interpretable in the standard detection sense.

2. **No evaluation against adaptive attacks.** For an adversarial detector, it is standard practice to evaluate against attacks that are aware of the detection mechanism (see Carlini et al., 2019; Tramer et al., 2020). The paper evaluates only against PGD, CW, and AutoAttack generated against the underlying classifier, but does not test an adversary who optimizes a joint objective accounting for both the KL-based and L0-based detection signals. Given the paper's central claim that a single perturbation "cannot simultaneously" satisfy both conditions (Theorem 1), the most direct test of this claim is an adaptive attack that explicitly tries to do so. Its absence significantly limits the empirical validation.

3. **Norm mismatch between theoretical analysis and experimental evaluation.** The theoretical analysis (Assumption A2, line 114) states "‖δ‖ ≤ ε" without specifying the norm and uses "energy budget" language suggesting ℓ₂ (Figure 1 caption, line 40, explicitly writes "‖δ‖₂ ≤ ε"). However, all experiments use ℓ∞-bounded attacks (line 178). If the theory assumes ℓ₂ but the evaluation uses ℓ∞, the empirical validation does not directly test the theoretical conditions. This mismatch needs clarification — at minimum, the paper should specify which norm(s) the theory applies to and justify why ℓ∞ experiments are appropriate.

4. **Theoretical guarantee covers a limited fraction of test data.** The conditions of Theorem 1 are satisfied by only 59–67% of CIFAR-10 samples and ~10–11% of CLIP/Tiny-ImageNet samples (Table 1). While the paper reports this transparently, the abstract and introduction present the formal guarantee as a central contribution without adequately qualifying its limited coverage. A reader could reasonably assume the guarantee applies broadly.

5. **"No architectural changes" claim is contradicted.** The abstract and introduction state the method "requires no architectural changes" (lines 9, 25, 33), but Section 3.1 explicitly says it "replaces this conventional classifier head with a novel component" (line 58). Replacing the classifier head with a nearest-prototype classifier is an architectural modification. The claim should be refined to specify that only the backbone encoder is unchanged.

### Minor

1. **The L0 threshold τ is fixed with no sensitivity analysis.** The value τ=0.75 is used throughout (line 173) with no analysis of how detection performance varies with τ, despite the proof sketch stating "we can always find a threshold τ" (line 128). A sensitivity study is needed to justify this choice.

2. **No variance or confidence intervals.** No table reports standard deviations or confidence intervals. This is especially important given the small compliant subset on CLIP (510 samples).

3. **Forward KL direction (KL(c||p) instead of KL(p||c)) is not justified.** Equation 1 uses KL(c||p) = Σ c_i log(c_i / p_i), measuring divergence from prototype to embedding. This is the reverse of the more typical direction and its suitability for a nearest-prototype classifier is not discussed.

4. **The claimed complementarity does not hold on CLIP.** On CLIP/Tiny-ImageNet, KL+L0 adversarial accuracy (26.50% on PGD ε=2/255) is substantially worse than KL-only (60.02%) or L0-only (53.31%) (Table 4). The paper's explanation (CLIP's pre-training favors sparsity) is reasonable, but it means the core complementarity claim is architecture/dataset dependent and does not generalize as stated.

### Trivial

- The L0 "distance" (Equation 2) is not a metric (fails symmetry and triangle inequality), though the paper consistently calls it one. Minor terminology issue.

## Nice-to-Haves

- Construct and evaluate adaptive attacks that jointly optimize against the KL-based and L0-based objectives. This is the most direct test of whether the claimed guarantee holds against an informed adversary.
- Report standardized detection metrics (TP = detector says attack on attacked input, etc.) as a separate column, so results are comparable with prior work.
- Characterize the non-compliant samples geometrically (e.g., proximity to decision boundaries).
- Evaluate sensitivity of detection performance to the L0 threshold τ.

## Removed Points

These points were raised by reviewers but are removed (with justification):

- **"Semantics-free" claim overreach.** The harsh critic claimed the method is not semantics-free because CLIP uses text prompts. However, the method's core principle does not require semantics (ResNet-CIFAR-10 prototypes are mean embeddings, not text). Using text prompts for CLIP prototypes is a reasonable adaptation to the pre-trained architecture, not a flaw in the method's claim of being "semantics-free" in principle.

- **L0 metric "pathology" with adaptive threshold.** The critic claimed the τ·μ threshold is "self-referential" and pathological. This misunderstands the design: the threshold is intentionally proportional to the average per-coordinate difference, making it a relative measure. This is a deliberate design choice, not a bug. The absence of a τ sensitivity study is a valid separate concern (kept above).

- **Missing appendix references / proof verification.** The appendix is stripped by the parser; this is not an author error. Per instructions, criticisms about missing appendix content are removed.

- **Formatting/style nitpicks.** Per instructions, all formatting, grammar, and presentation issues attributable to the parser are removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Re-run the evaluation with standard detection metrics** (TP = a=1 ∧ â=1, FP = a=0 ∧ â=1, etc.) so the reported precision and recall measure what readers in the adversarial detection community expect. The current system-level metrics (which count correct classification after missed detection as a "true positive") can be reported as a secondary, complementary view.

2. **Construct adaptive attacks** that explicitly optimize against the KL+L0 disagreement signal (e.g., minimizing cross-entropy to a target class while penalizing the KL-L0 prediction mismatch). Evaluate on both compliant and non-compliant subsets.

3. **Clarify the norm in the theoretical analysis** — specify whether the energy bound (Assumption A2) uses ℓ₂, ℓ∞, or another norm, and ensure the experimental attacks match. If the theory is specifically for ℓ₂, acknowledge that ℓ∞ attacks in experiments are a separate evaluation axis.

4. **Qualify the theoretical guarantee's coverage** in the abstract and introduction (e.g., "for a subset of samples satisfying inter-class separation conditions").

## Score and Decision

### Calibration

**Retrieved anchors across two rounds (bracketing + narrowing):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `5kMwiMnUip.md` | 1.40 | R1 (strong reject) | Unrelated LLM jailbreaking paper. Not comparable. |
| `KAWlH5pfQu.md` | 3.00 | R1 (reject) | Adversarial detection with flawed proof, no adaptive attacks. Weaker than KOALA — KOALA's proof sketch is more coherent and the core idea is more clearly motivated. |
| `kz78RIVL7G.md` | 2.60 | R1 (reject) | Attack-agnostic detection with no adaptive attacks, weak baselines. Weaker than KOALA — KOALA has a novel theoretical contribution this paper lacks. |
| `lEsNGN1SjG.md` | 2.00 | Narrowing | Bias classifier with fundamentally wrong claims. Weaker than KOALA. |
| `NI0RsRuFsW.md` | 4.00 | Narrowing | Trojan detection paper. Comparable evaluation depth but different topic. |
| `RzdtpxL0H5.md` | 6.20 | R1 (borderline accept) | SADD-based defense with theory, adaptive attacks, strong results. Stronger than KOALA — more thorough evaluation. |
| `4M0BRyGMnJ.md` | 6.50 | R1 (accept) | Democratic training defense. More rigorous empirical evaluation. Stronger than KOALA. |
| `8QTpYC4smR.md` | 1.00 | R1 (strong reject) | LLM survey paper. Not comparable. |
| `IGzaH538fz.md` | 8.00 | R1 (strong accept) | Graph neural network certification. Stronger theoretical guarantees and more rigorous evaluation. Stronger than KOALA. |

**Round 1 bracket: 3.5 – 6.5** (eliminated strong reject and strong accept bands as KOALA has a genuine novel contribution but significant evaluation issues)

**Narrowing:** Compared against `KAWlH5pfQu` (3.00, similar issues but more severe flaws), `NI0RsRuFsW` (4.00, similar evaluation depth), and `RzdtpxL0H5` (6.20, stronger evaluation). KOALA sits between the 3.00–4.00 (reject) and 6.20 (borderline accept) anchors — its novel theory and well-motivated approach are genuine strengths, but the non-standard confusion matrix and missing adaptive attacks prevent it from reaching the 6+ level.

**Final score: 5.0**

The paper presents a genuinely novel detection principle based on complementary metrics and provides a formal analysis — contributions that are rare in the adversarial detection literature. However, the evaluation has a structural issue (non-standard confusion matrix that makes headline detection metrics uninterpretable as standard detection performance) and a significant gap (no adaptive attacks). These weaknesses are addressable with revision but are too severe for acceptance in the current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>