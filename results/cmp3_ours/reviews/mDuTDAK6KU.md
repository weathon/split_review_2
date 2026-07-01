Now I have sufficient calibration context. Let me finalize the review.

## Summary

KOALA is an adversarial detector that flags attacks when two complementary similarity metrics — KL divergence and an L0-based distance — disagree on the predicted class when used as nearest-prototype classifiers. The paper provides a formal theorem claiming that under sufficient inter-class prototype separation, no norm-bounded perturbation can simultaneously fool both metrics, guaranteeing detection. A lightweight fine-tuning procedure on clean images only is used to align embeddings with both metrics. Experiments on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet evaluate detection performance.

## Strengths

1. **Formal theoretical framing is a genuine contribution.** Most adversarial detectors are purely empirical. The idea of proving that two complementary metrics cannot both be fooled by a single norm-bounded perturbation (Section 3.2, Theorem 1) is conceptually interesting and sets this paper apart. The proof sketch articulates a non-trivial claim about mutual exclusivity of stability bands.

2. **Experiment 1 directly validates the theorem's conditions** by partitioning test sets into Theorem-compliant and non-compliant samples (Table 1). The perfect scores (1.0 across all metrics) on the compliant subset are consistent with the theoretical claim. This kind of targeted validation of a formal condition is uncommon in the detection literature and is a genuine strength.

3. **The method requires no adversarial training or architectural changes** to the base classifier, making it lightweight and potentially practical as a plugin. The fine-tuning relies only on clean images (Section 3.3), which is a practical advantage.

## Weaknesses

### Fatal
None.

### Major

1. **Non-standard evaluation metrics inflate reported detection performance and make results non-comparable.** The TP/FN definitions in Section 4.2 (line 188) conflate detection success with classification success. For an attacked input (a=1):
   - TP = [detector flags attack, â=1] OR [detector misses attack but classifier still predicts the correct label, â=0, ŷ=y^*]
   - FN = [detector misses attack AND classifier predicts wrong label, â=0, ŷ=-y^*]
   
   Under standard detection evaluation, a TP should be an adversarial input the detector *flags* (â=1), regardless of whether the downstream classifier happens to guess correctly. The paper's definition counts an adversarial example that fully evades detection (â=0) as a TP as long as the base classifier still produces a correct prediction. A detector that never flags anything could achieve artificially high precision and recall under this definition if the base classifier has reasonable accuracy on attacked inputs. Since every quantitative claim in the paper (headline numbers: precision 0.94, recall 0.81 on ResNet/CIFAR-10) depends on these metrics, the reported numbers cannot be interpreted as standard detection metrics and are likely inflated. This is a structural problem affecting all empirical results.

2. **Gap between the theoretical guarantee and the fixed hyperparameter τ.** The proof sketch (Proposition 4, line 128) states: "For any given adversarial perturbation, *we can always find a threshold τ* for the L0 metric that forces a trade-off." The conclusion (line 129) states "such a threshold τ always exists." However, the implemented system uses a *fixed* τ=0.75 (Section 4.1, line 173) for all inputs and all experiments. A proof that shows existential quantification ("there exists some τ that would work") does not automatically establish that a specific τ=0.75 works for all inputs and all perturbations. The theorem statement itself (Theorem 1) does not mention τ, and without seeing the full proof (which is in the parser-stripped appendix), it is unclear whether the guarantee transfers to the system as configured with τ=0.75. This gap needs resolution.

3. **No adaptive attacks are evaluated.** The paper tests only standard attacks (PGD, CW, AutoAttack) designed to fool a single classifier, not to fool a dual-metric nearest-prototype detector. The related work section (line 48) criticizes prior detectors for lacking "formal proof-of-correctness guarantees against adaptive adversaries," yet the paper itself provides no evaluation against attacks designed to simultaneously manipulate both the KL and L0 nearest-prototype classifiers. For a detector claiming formal correctness guarantees, evaluation against adaptive adversaries — especially on the ~90% of non-compliant samples where the theory does not apply — is essential but absent.

### Minor

4. **Limited scope of the theoretical guarantee on CLIP/Tiny-ImageNet.** Only 10–11% of test samples (510/5000 at ε=2/255, 556/5000 at ε=4/255) satisfy Theorem 1 conditions on CLIP/Tiny-ImageNet (Table 1). On the remaining ~90% of non-compliant samples, precision is 0.62–0.63 and recall is 0.80–0.84 — modest numbers. The paper acknowledges the low compliant fraction (attributing it to CLIP's compact embedding space, lines 185–186) but does not deeply analyze *why* so few samples satisfy the conditions or what would need to change to increase coverage. This directly impacts the method's practical utility on one of the two evaluated setups.

5. **No comparison to prior detection methods and missing standard metrics.** The paper cites numerous detection methods in the related work (Ma et al., 2018; Xu et al., 2018; Lee et al., 2018; Feinman et al., 2017; etc.) but provides no quantitative comparison against any of them. The evaluation is limited to ablations of the paper's own metric combinations. Additionally, standard detection metrics (AUROC, AUPR, TPR at low FPR) are absent; only accuracy, precision, recall, and F1 are reported, which depend on the base rate of attacks in the test set and are not directly comparable to prior work.

### Trivial
None.

## Nice-to-Haves
- Perform a τ sensitivity analysis (e.g., τ ∈ {0.2, 0.4, 0.6, 0.8, 1.0}) to understand how detection rate depends on this critical hyperparameter.
- Present results under both the paper's current metric definitions and standard detection definitions so readers can assess the gap.
- Analyze the non-compliant samples more deeply: why do ~90% of CLIP/Tiny-ImageNet samples fail the theorem conditions, and what would increase coverage?
- Provide an ablation over loss weights (ω_L0=0.9, ω_KL=0.1) to justify the severe imbalance.

## Removed Points

These points were flagged by the harsh critic but are removed or demoted for the following reasons:

- **"KL+L0+Cosine outperforms KL+L0 on CLIP/Tiny-ImageNet"** — The paper already addresses this directly (lines 216–218), explaining that the three-metric setup breaks classification leading to chance-level disagreements that inflate detection rate. This is a reasonable explanation; the criticism is already addressed.
- **"KL direction not discussed"** — A minor design choice. Using KL(c||p) (prototype as reference) is a standard choice in nearest-prototype settings. Not a substantive weakness.
- **"Softmax normalization concern"** — The paper is transparent about Assumption A1; this is common practice when working with nearest-prototype classifiers and KL-based objectives.
- **"Loss weight imbalance"** — The paper provides a reasonable justification (L0 is harder to optimize). Demoted to Nice-to-Haves.
- **"L0 not a metric"** — The paper explicitly defines L0 and never claims it's a proper metric. This is a transparent design choice.
- **Various section-by-section notes** — Most are observations about design choices the paper is transparent about, not actual weaknesses.

## Novel Insights

The harsh critic usefully identifies that the paper's evaluation metrics are non-standard in a way that inflates numbers. This is an important meta-observation: the paper's TP/FN definitions effectively measure *system-level correctness* (classifier + detector combined) but present the results as *detection metrics*, which is misleading. Additionally, the critic correctly identifies a tension between the existential quantification of τ in the proof sketch and the fixed τ in the implementation — a theory-practice gap that the paper does not address.

## Suggestions

1. **Re-define the evaluation metrics** to conform to standard detection conventions (TP = detector flags an attacked input regardless of classification outcome) and report results under both the paper's and standard definitions.
2. **Clarify the τ issue** — Either show that the theorem guarantees detection for τ=0.75 specifically, or adjust the theorem statement to match what is actually proven.
3. **Evaluate against adaptive attacks** designed to fool the dual-metric detector, especially on the non-compliant subset.
4. **Include standard detection metrics** (AUROC, AUPR) and quantitative comparisons with at least one prior detection method.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 5kMwiMnUip (jailbreaking) | 1.40 | R1 | Not relevant; much weaker paper |
| 5lUdTogEL3 (person re-id) | 1.00 | R1 | Not relevant |
| kz78RIVL7G (attack-agnostic detection) | 2.60 | R1 | Similar topic but weaker method and no theory |
| KAWlH5pfQu (detecting adv examples/layer analysis) | 3.00 | R1 | Similar topic, also lacked adaptive attacks |
| adhxppqQAn (multi-task consistency detection) | 3.75 | R1, narrow | Closest analogy: consistency-based detection, no adaptive attacks, limited attack scope — very similar weaknesses. KOALA has stronger theory but worse metric definitions |
| NI0RsRuFsW (trojan detection) | 4.00 | narrow | Less related topic |
| 3iGponpukH (physical attack evaluation) | 4.75 | narrow | About evaluation practices; less directly comparable |
| R1crLHQ4kf (output distribution detection, audio) | 5.00 | R1, narrow | Solid evaluation incl. adaptive attacks, but limited novelty |
| NlEt8LYAxC (fast adversarial training sparse) | 6.00 | R1 | Thorough empirical paper with theory but limited novelty |
| KmQEsIfhr9 (detecting backdoors in CLIP) | 6.00 | R1 | Strong empirical evaluation on CLIP detection |
| GrDne4055L (OOD detection Lyapunov) | 6.25 | R1 | Strong theory + experiments, accepted paper |
| IGzaH538fz (GNNCert) | 8.00 | R1 | Deterministic certification; not directly comparable |
| pE6gWrASQm (adversarial training subset) | 6.50 | R1 | Thorough empirical study |

**Round 1 bracket:** 3.5 – 5.5 (the paper's novel theory pushes it above purely empirical detection papers, but the structural evaluation problems and τ gap prevent it from reaching the 5.5+ range)

**Narrowing:** Comparing against the closest anchor — "Multi-Task Consistency-based Detection" (avg 3.75) — KOALA has a stronger theoretical contribution but worse evaluation issues. The "output distribution detection" paper (avg 5.0) has better evaluation (including adaptive attacks) but less novelty. KOALA sits between these.

**Final score:** 4.5

**Decision:** Reject — The paper presents a genuinely interesting theoretical framework, but the evaluation methodology has a structural flaw (non-standard TP/FN definitions that inflate reported numbers) that undermines all quantitative claims. Combined with the theory-practice gap regarding τ, the lack of adaptive attack evaluation, and the limited scope of the guarantee on one of the two datasets, the paper in its current form does not support its central empirical claims. The core theoretical idea has merit and could be the basis for a strong paper after substantial revision to the evaluation.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>