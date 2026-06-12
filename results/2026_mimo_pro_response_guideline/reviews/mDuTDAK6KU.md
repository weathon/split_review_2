Now I have enough calibration data. Let me write the final review.

**Calibration Analysis:**

**Round 1 Bracket: 4.5 – 6.0**

**Key anchors retrieved:**
- **KAWlH5pfQu** (Detecting Adversarial Examples, avg 3.0, Reject) — Similar topic: adversarial detection with theoretical justification. Has weak baselines, no adaptive attacks. KOALA has a significantly stronger formal proof and better ablation design, so should score higher.
- **kfYM5lBzB6** (Randomized Feature Squeezing, avg 4.75, Reject) — Clean-only training without adversarial training. Rejected at 4.75. KOALA has a more rigorous theoretical foundation.
- **r5d8zkYizS** (Adversarial Attacks as Near-Zero Eigenvalues, avg 5.33, Reject) — Mathematical framework for adversarial examples. Has theoretical depth but practical limitations. Comparable to KOALA's profile.
- **RzdtpxL0H5** (DDAD, avg 6.2, Reject) — Distributional-discrepancy defense with theoretical proofs and external baselines on CIFAR-10/ImageNet-1K. Stronger evaluation than KOALA. KOALA has a cleaner formal proof but weaker empirical evaluation.
- **5bNYf0CqxY** (Certified Adversarial Robustness for SNNs, avg 6.75, Accept) — Novel theoretical contribution with comprehensive empirical results. Stronger overall package than KOALA.
- **GNNCert** (avg 8.0, Accept) — Deterministic certification, much stronger contribution.

**Round 2 narrowed to 4.5 – 5.5, settling on 5.0.**

Rationale: KOALA's theoretical contribution (Theorem 1 with formal proof) is genuinely novel and non-trivial, placing it well above the score-3 adversarial detection papers. However, the empirical evaluation has significant issues: a factual error in Table 4's caption, no external baselines, a non-standard TP definition that inflates metrics, and the core KL+L₀ complementarity claim failing on CLIP. Compared to DDAD (6.2, which had external baselines and more comprehensive evaluation but was still rejected), KOALA has a stronger formal guarantee but weaker empirical validation. This places it at 5.0 — below the acceptance threshold.

---

## Summary

The paper introduces KOALA, an adversarial detector based on the disagreement between KL-divergence and L₀-based nearest-prototype classifiers. Its central contribution is a formal proof (Theorem 1) that under norm-bounded perturbations and mild assumptions, the two metrics' prediction stability bands are mutually exclusive, guaranteeing detection. The method requires only clean-image fine-tuning and no adversarial training.

## Strengths

- **Formal theoretical guarantee with strong empirical validation on compliant samples**: Theorem 1 proves mutual exclusivity of KL and L₀ stability bands. Table 1 shows perfect 1.0 precision/recall/accuracy/F1 on all theorem-compliant samples across all four settings (ResNet/CIFAR-10 at ε=2/255 and 4/255: 3345/2967 samples; CLIP/Tiny-ImageNet: 510/556 samples), directly confirming the theory.

- **Best detection and adversarial robustness on ResNet/CIFAR-10**: Table 2 shows KL+L₀ achieves F1=0.87 (ε=2/255) on ResNet, outperforming all other metric combinations. Table 3 shows KL+L₀ fine-tuning achieves 57.32% adversarial accuracy (PGD ε=2/255) vs. 45.5% baseline — a meaningful improvement using only clean images.

- **Honest and insightful analysis of failure modes**: The paper transparently discusses why KL+L₀+Cosine's high detection rate on CLIP stems from classification collapse (adversarial accuracy 14.93%, lines 216-218), and why L₀ alone suffices for CLIP due to its cosine-contrastive pre-training (lines 274-276). This self-awareness strengthens credibility.

- **Systematic experimental design**: Three complementary experiments (theorem verification, metric ablation, adversarial resilience) across two architectures (ResNet-18 from scratch, CLIP ViT-B/32), two datasets, three attack methods (PGD, CW, AutoAttack), and two perturbation budgets.

## Weaknesses

### Fatal
None

### Major

- **Table 4 caption is factually incorrect**: The caption at line 272 states "The KL+L₀ objective demonstrates superior adversarial accuracy, highlighting the complementary nature of these two metrics" for CLIP/Tiny-ImageNet. The actual numbers in the table show KL+L₀ achieves only 26.50% adversarial accuracy (PGD ε=2/255), while KL alone achieves 60.02% and L₀ alone achieves 53.31% — making KL+L₀ the worst among the three individual objectives. This appears to be a copy-paste error from Table 3 (where the caption is correct for ResNet). The prose at line 274 honestly acknowledges "the L₀-only fine-tuning objective yields the highest adversarial robustness," directly contradicting the table caption. This factual error in a key results table undermines reader trust.

- **Detection metrics conflate detection with incidental classification robustness**: The TP definition (line 188) counts an attacked input as a true positive if it is *either* detected by the system (â=1, abstain) *or* correctly classified despite the attack not being detected (â=0, y=y*). In a standard detection task, any attacked input that is not flagged should be a false negative regardless of whether the attack happened to be ineffective. This systematically inflates recall and F1 across all reported results. The paper should report a standard detection confusion matrix (detected vs. not detected, independent of classification outcome) alongside the current formulation.

- **No comparison to any external adversarial detector**: The Related Work section discusses numerous prior detectors (MagNet, Mahalanobis, NIC, feature squeezing, LID, CADet, Bayesian uncertainty), but all experiments compare only against internal metric combinations (KL, L₀, Cosine). Without at least one external baseline on the same experimental setup, there is no way to assess whether KOALA's empirical detection performance is competitive with prior work.

### Minor

- **Theorem 1 compliance covers only ~10% of CLIP samples**: Table 1 shows only 510/5000 (10.2%) CLIP samples satisfy Theorem 1 at ε=2/255, compared to 3345/5000 (66.9%) for ResNet. While valid as theory validation, this limits the practical relevance of the formal guarantee for CLIP-like models.

- **"Plug-and-play" / "no architectural changes" framing is misleading**: The abstract and introduction claim "requires no architectural changes" and is a "plug-and-play solution," but Section 3.1 (line 58) states "KOALA replaces this conventional classifier head with a novel component." Replacing the classifier head is an architectural modification, even if the backbone encoder is preserved.

- **Theorem 1 compliance determination is unexplained**: The paper partitions test samples into compliant/non-compliant (Table 1) but does not describe how compliance is evaluated. If it requires knowledge of the adversarial target class (to evaluate the coordinate gap), this cannot be done at deployment time, making the perfect scores on compliant subsets a retrospective artifact. The paper should clarify whether compliance can be computed from clean inputs and prototypes alone.

### Trivial
None

## Nice-to-Haves
- An adaptive attack evaluation (e.g., PGD targeting the combined KL+L₀ disagreement loss) would strengthen the practical security claims, especially for the ~90% non-compliant CLIP samples.
- Joint reporting of detection metrics and adversarial accuracy in the same table would clarify the detection-vs-robustness trade-off more clearly than the current split across Tables 2 and 3/4.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Theorem 1 circularity concern**: The paper frames Table 1 as theoretical validation (line 185: "The primary goal is to show that when the conditions are met, attack detection is guaranteed"), not as a deployment-time check. The harsh critic's concern about needing adversarial target class knowledge at deployment is valid but overstated — it is a limitation, not an invalidation.
- **A1/A3 softmax-space concerns**: These are refinements about the proof's scope, not invalidations. The paper explicitly assumes softmax normalization (Assumption A1), and the proof operates within that setting.
- **Missing adaptive attack evaluation**: Valid concern but the formal guarantee addresses compliant samples; the paper's claims for non-compliant samples are more modest. Treated as a nice-to-have.

## Novel Insights
The paper's genuinely novel contribution is Theorem 1: a formal proof that KL divergence and L₀-based metric stability bands are mutually exclusive under norm-bounded perturbations (given sufficient coordinate gap between true and adversarial class prototypes). This places adversarial detection on firmer foundations than purely empirical approaches and is a meaningful contribution to the field, even though the empirical evaluation does not fully support the paper's broader claims.

## Suggestions
1. Correct the Table 4 caption to honestly reflect that L₀ alone achieves the best adversarial robustness on CLIP.
2. Report a standard detection confusion matrix (detected/not-detected, independent of classification outcome) alongside the current one.
3. Add at least one comparison to an external adversarial detector (e.g., Mahalanobis or feature squeezing).
4. Clarify how Theorem 1 compliance is evaluated and whether it can be done at deployment time.

## Reporting

**All anchors retrieved:**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| 5kMwiMnUip (Jailbreaking LLMs) | 1.40 | R1 | Unrelated topic; much weaker paper |
| nSDOkm0SKo (Financial Markets NN) | 1.00 | R1 | Unrelated; very weak paper |
| Uj0h13lVrR (KL Divergence GFlowNets) | 1.00 | R1 | Unrelated topic |
| 5lUdTogEL3 (Lifelong Person ReID) | 1.00 | R1 | Unrelated topic |
| KAWlH5pfQu (Detecting Adversarial Examples) | 3.00 | R1 | Most directly comparable; KOALA has much stronger formal proof and better ablation design |
| kz78RIVL7G (Statistical Adversarial Detection) | 2.60 | R1 | Similar topic; weaker theoretical contribution |
| lEsNGN1SjG (Bias Classifier) | 2.00 | R1 | Adversarial robustness; much weaker |
| puGvShnqeA (DLGN Adversarial Interpretability) | 3.00 | R1 | Adversarial robustness; weaker formal guarantees |
| r5d8zkYizS (Near-Zero Eigenvalues) | 5.33 | R1+R2 | Mathematical framework; comparable theoretical depth but weaker experiments |
| 2ErS9Bkc3O (Adversarial Fragility) | 4.50 | R1 | Theoretical adversarial analysis; comparable |
| G3OCarOfxx (CGRO in Adversarial Training) | 4.80 | R1 | Theory of adversarial training; different focus |
| Oi6BhzIu7R (REAL Test-Time Defense) | 4.67 | R1 | Adversarial defense; comparable contribution level |
| RzdtpxL0H5 (DDAD) | 6.20 | R1 | Best comparison: has external baselines, more comprehensive eval, still rejected |
| 8CJDYx8GwF (Robust Classifiers orthonormal) | 6.25 | R1 | Certified robustness; stronger empirical package |
| 5bNYf0CqxY (Certified SNN Robustness) | 6.75 | R1 | Accepted; stronger overall (novel theory + comprehensive eval) |
| ExUC9dQJhQ (Certified Poisoning Robustness) | 6.00 | R1 | Certified robustness; comparable theoretical depth |
| IGzaH538fz (GNNCert) | 8.00 | R1 | Much stronger paper across the board |
| P7KIGdgW8S (Hölder Stability GNN) | 8.00 | R1 | Much stronger theory |
| I5lcjmFmlc (Robust Diffusion Classifier) | 8.00 | R1 | Much stronger paper |
| cJs4oE4m9Q (Orthogonal Hypersphere) | 8.00 | R1 | Unrelated area |
| 7GCRhebJEr (Bregman Divergence Robustness) | 5.00 | R2 | Robustness via learned metric; comparable |
| 5HGPR6fg2S (Normalized Space Alignment) | 3.75 | R2 | Weaker |
| 4BYzyGKIcb (SaGD OOD Detection) | 4.00 | R2 | OOD/Adversarial detection; comparable topic |
| 8S7eGD15b6 (Subspace Grid-sweep) | 5.25 | R2 | Defense evaluation; comparable |
| 0w42S2Gp70 (LipSim) | 5.33 | R2 | Robust perceptual metric; comparable level |
| MZ324wU7Hj (Oracle for Errors) | 6.00 | R2 | Error prediction; comparable |
| qz3mcn99cu (Certifiable Robustness Recipe) | 6.33 | R2 | Accepted; stronger eval |
| pA8oI8a00l (CleanerCLIP) | 4.25 | R2 | CLIP defense; weaker |
| sBpYRQOrMn (Dummy Classes AT) | 5.75 | R2 | Adversarial training; different approach |
| Uqxf2YH9LZ (BDetCLIP) | 5.75 | R2 | CLIP backdoor detection; comparable |
| kfYM5lBzB6 (Randomized Feature Squeezing) | 4.75 | R2 | Clean-only training; comparable but KOALA has stronger theory |

**Round 1 bracket: 4.5–6.0**. KOALA is clearly better than the 3.0-scored adversarial detection paper (stronger proof, better ablation) but weaker than DDAD (6.2, which had external baselines and was still rejected).

**Round 2 narrowed to 4.5–5.5**. KOALA's theoretical contribution places it above the 4-4.5 range but its empirical weaknesses (caption error, no external baselines, TP inflation) prevent it from reaching 5.5+.

**Final score: 5.0**. The genuine theoretical contribution is the paper's saving grace, but the empirical evaluation has too many issues for acceptance. A score of 5.0 reflects a paper with real merit that needs significant revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>