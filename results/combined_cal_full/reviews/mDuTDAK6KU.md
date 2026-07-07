Now let me compose the final consolidated review.

## Summary
2-3 sentence summary of the paper's contribution.

The paper introduces KOALA, an adversarial detector that flags attacks when two complementary nearest-prototype classifiers—one using KL divergence (sensitive to dense perturbations) and one using an L0-based metric (sensitive to sparse perturbations)—produce disagreeing class predictions. The method requires no adversarial training or architectural changes, only lightweight fine-tuning on clean images. A theoretical guarantee (Theorem 1) establishes conditions under which detection is provably forced by the mutual exclusivity of the two metrics' prediction-stability bands.

## Strengths

1. **Clean, well-motivated geometric intuition** (Section 3.1, Figures 1–2). The idea that KL divergence and an L0-based metric are sensitive to complementary perturbation types (dense low-amplitude vs. sparse high-impact), and that their disagreement signals an attack, is clearly explained and visually illustrated. This gives the work a strong conceptual anchor.

2. **Lightweight training recipe** (Section 3.3). Fine-tuning only on clean images with no adversarial training, no access to attack generators, and no architectural changes is a genuine practical advantage. The composite loss (Eq. 5–6) is sensible and the approach works across two different architectures (ResNet, CLIP).

3. **Direct empirical validation of the theoretical claim** (Experiment 1, Table 1). Splitting the test set into theorem-compliant and non-compliant samples and showing perfect detection (Accuracy = Precision = Recall = F1 = 1.0) on the compliant subset is the right way to verify a conditional guarantee. This demonstrates internal consistency between theory and practice.

4. **Formal theoretical guarantee** (Theorem 1). Providing explicit conditions under which detection is guaranteed is rare among intrinsic-statistics adversarial detectors and distinguishes KOALA from purely empirical approaches such as feature squeezing, LID, and MagNet.

## Weaknesses

### Fatal
None.

### Major
1. **Non-standard evaluation metrics conflate detection with classification** (Section 4.2, lines 186–191). The paper defines True Positives for attacked inputs as cases where either (a) the detector flags the attack and abstains, OR (b) the detector does NOT flag the attack but the final classification happens to be correct. This means an input is counted as a "detected positive" even when the detector entirely fails to flag it, as long as the model's classification survives the attack. Symmetrically, False Positives include clean inputs that the detector correctly accepts (â=0) but then misclassifies. These definitions conflate two distinct capabilities—detecting that an attack is present and classifying correctly despite an attack—and make the reported precision and recall incomparable to standard detection metrics used by every prior method in this space. Standard detection metrics (TP = attacked ∧ flagged, FP = clean ∧ flagged) should be reported alongside or instead of the current definitions.

2. **No empirical comparison against any existing detection method.** Despite surveying feature squeezing, LID, MagNet, Mahalanobis detection, NIC, CADet, and Bayesian uncertainty methods in Section 2 (Related Work), the experimental section contains zero comparisons against any of these. Headline claims such as "precision of 0.94 and recall of 0.81 on ResNet/CIFAR-10" are unanchored without context against prior work. Without baselines, the reader cannot judge whether KOALA advances the state of the art.

3. **No evaluation against adaptive attacks.** All evaluated attacks (PGD, CW, AutoAttack) target the classifier's output. An informed adversary who knows that KOALA flags disagreement between KL and L0 predictions can directly craft a perturbation that maintains agreement between both metric-based classifiers while flipping the true class. This is a well-documented failure mode for detection-based defenses (Carlini & Wagner, 2017; Athalye et al., 2018). Evaluating against adaptive attacks is especially important given that the paper's own Theorem 1 makes a claim about conditions under which no such adversary can succeed—testing this empirically would be the strongest possible validation.

### Minor

4. **Theorem compliance covers only a minority of samples on CLIP/Tiny-ImageNet** (Table 1). Only ~10% of samples satisfy the theorem conditions on CLIP/Tiny-ImageNet (510/5000 at ε=2/255). On the remaining 90%, performance is modest (e.g., Precision 0.63 at ε=2/255). The paper acknowledges this but does not provide runtime criteria to determine whether a given input falls within the compliant regime, limiting the practical applicability of the guarantee.

5. **The L0 metric's relative threshold needs more rigorous justification** (Eq. 2). The threshold τ·μ depends on μ(c,p), the mean absolute difference across all coordinates. This means the same coordinate-wise difference may or may not be counted depending on the overall perturbation magnitude, making the claimed clean separation between "dense" and "sparse" sensitivity less straightforward than presented. The paper should either justify why this relative-threshold design is preferable to an absolute threshold, or formally characterize its behavior under different perturbation structures.

6. **Theorem presentation in the main text is incomplete.** The threshold Γ_i(ε) in Theorem 1 (line 120) is referenced but not defined in the body. The proof sketch (lines 124–129) is qualitative prose without the key inequality. This makes it impossible for a reader to assess the theorem's content from the main text alone; the appendix is needed to evaluate the theoretical contribution.

7. **Fine-tuning epochs not specified** (Section 4.1). The number of fine-tuning iterations is not reported, which affects reproducibility and makes the "lightweight" claim harder to assess quantitatively.

8. **KL divergence direction not justified** (Eq. 1). The paper uses KL(c||p) without discussing why this asymmetric direction is chosen over KL(p||c). Since the two directions have different sensitivities, this choice warrants a brief justification.

### Trivial
None.

## Nice-to-Haves
- Report standard detection metrics (TP = attacked ∧ flagged, FP = clean ∧ flagged) alongside the paper's system-level definitions.
- Add 2–3 baseline comparisons from intrinsic-statistics detectors (e.g., feature squeezing, Mahalanobis detection) under the same evaluation setup.
- Design and evaluate adaptive attacks that directly optimize for agreement between KL and L0 predictions while causing misclassification. This is the natural adversary for this defense and would be the strongest test of Theorem 1.
- Define Γ_i(ε) in the main text to make Theorem 1 self-contained.
- Provide detection performance variance across multiple random seeds.
- Specify the number of fine-tuning epochs.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **Critic's claim that L0 behaves "opposite" to what the paper claims**: Concrete analysis shows L0's behavior is consistent with the paper's intended design (sparse attacks produce discriminable distances, dense attacks make both prototypes equidistant, which is precisely why KL is needed). This was an overstatement. Kept as Minor with corrected framing (#5 above).
- **Critic's concern about Section 4.3 undercutting the KL+L0 claim**: The paper honestly explains the three-metric artifact (random predictions inflating detection rates) and frames it as a failure mode. This is an honest discussion, not a weakness.
- **KL divergence on normalized embeddings**: The paper explicitly specifies softmax normalization in Assumption A1. This is a legitimate design choice, not a flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Prioritize adding baseline comparisons and adaptive attack evaluation; these are the most significant gaps that prevent the paper from making a compelling case for its empirical claims.
- Report standard detection metrics (or both standard and system-level) so readers can separate pure detection performance from classification-under-attack.
- Provide a practical criterion for determining whether a given input falls within the theorem-compliant regime at runtime, or characterize the feature-space separation that governs compliance.

## Score and Decision

Let me compile the calibration anchor table first.

**Calibration Anchors Retrieved:**

| File | Score | Round | Itemized | Comparison |
|------|-------|-------|----------|------------|
| 5kMwiMnUip.md | 1.40 | R1 | No | Jailbreaking paper, unrelated topic |
| Uj0h13lVrR.md | 1.00 | R1 | No | KL divergence for GFlowNets, different domain |
| 5lUdTogEL3.md | 1.00 | R1 | No | Person Re-ID, unrelated |
| P49gSPmrvN.md | 1.00 | R1 | No | Scientific discourse visualization, unrelated |
| **KAWlH5pfQu.md** | **3.00** | **R1** | **Yes** | Adversarial detection via layer outputs. Similar weaknesses (no adaptive attacks, weak baselines), but that paper had a demonstrably wrong theorem. KOALA is stronger. |
| **kz78RIVL7G.md** | **2.60** | **R1** | **Yes** | Statistical detection via compressive sensing. Worse presentation and weaker experiments than KOALA. |
| dIK7GpOwNY.md | 3.00 | R1 | No | Effective dimensionality for robustness, different approach |
| uw5U7FfTRf.md | 3.00 | R1 | No | Backdoor detection, different problem |
| **RzdtpxL0H5.md** | **6.20** | **R1** | **Yes** | DDAD — adversarial detection with theoretical guarantees. Has baseline comparisons and standard metrics; KOALA does not. KOALA is weaker in evaluation rigor. |
| 8CJDYx8GwF.md | 6.25 | R1 | No | Provably robust classifier via gradient flow, different approach |
| **9528xxcT7h.md** | **6.50** | **R1** | **Yes** | Transduction+rejection for provable robustness. Stronger theoretical framing and clearer empirical strategy than KOALA. |
| F5dhGCdyYh.md | 7.33 | R1 | Yes | Illusory attacks (attack generation, not detection), different problem |
| IGzaH538fz.md | 8.00 | R1 | No | GNN certification, different domain |
| I5lcjmFmlc.md | 8.00 | R1 | No | Diffusion-based classifier robustness, different approach |
| 4BYzyGKIcb.md | 4.00 | R2 | No | OOD detection with adversarial robustness, only tangentially related |
| **adhxppqQAn.md** | **3.75** | **R2** | **Yes** | **Multi-task consistency detection. Most comparable paper: same approach family (detection via inconsistency), same core weaknesses (no adaptive attacks: weight -2.82; no baselines: weight -7.60). KOALA has a stronger theoretical contribution but similar evaluation gaps. This anchor anchors the lower bound.** |
| xdnoULh5Sv.md | 4.00 | R2 | No | Adversarial training + purification, different approach |
| EWP9BVRRbA.md | 4.00 | R2 | No | VLM detection, different domain |
| r5d8zkYizS.md | 5.33 | R2 | No | Eigenvalue framework, theory-heavy, different mechanism |
| G3OCarOfxx.md | 4.80 | R2 | No | Adversarial training theory, different problem |
| **R1crLHQ4kf.md** | **5.00** | **R2** | **Yes** | **Distributional detection for ASR. Has adaptive attacks and some baseline comparison (which KOALA lacks). Stronger evaluation completeness. Anchors the upper bound.** |
| Oi6BhzIu7R.md | 4.67 | R2 | No | Test-time defense, different mechanism |
| LVFoynuAQn.md | 4.33 | R2 | No | Dataset similarity metric, unrelated |
| Nx8lVqyKeZ.md | 4.25 | R2 | No | Membership inference, different problem |

**Bracket and calibration reasoning:**

**Round 1 bracket**: 3.0 – 6.2. The most comparable anchor papers are KAWlH5pfQu (3.00, adversarial detection with similar evaluation gaps) and RzdtpxL0H5 (6.20, adversarial detection with theory). KOALA's approach and writing quality exceed the 3.00 paper, but its evaluation completeness falls short of the 6.20 paper.

**Round 2 narrowing**: 3.5 – 5.0. The adhxppqQAn paper (3.75) uses the same detection-by-inconsistency paradigm and has the same core evaluation gaps (missing baselines: weight -7.60; missing adaptive attacks: weight -2.82). KOALA's theoretical contribution and cleaner experiments elevate it slightly above this anchor. Conversely, R1crLHQ4kf (5.00) demonstrates the evaluation rigor expected for acceptance (adaptive attacks, baseline comparisons) that KOALA lacks, setting a clear upper bound.

**Final score**: **4.0**. KOALA has a genuinely interesting idea and a formal theoretical guarantee, which distinguish it from the 3.0–3.75 range. However, the three major weaknesses—non-standard metrics that preclude comparison, zero baseline comparisons, and no adaptive attack evaluation—prevent the empirical claims from being properly assessed. These gaps are directly comparable to those that led the adhxppqQAn paper (3.75) and KAWlH5pfQu paper (3.00) to rejection. KOALA's theoretical contribution and cleaner execution justify a slightly higher score than those papers, but the evaluation deficiencies are too central to warrant acceptance (which would require ~6+).


MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>