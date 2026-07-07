Now let me write the final consolidated review.

## Summary

This paper proposes L-TTA, the first method for test-time adaptation (TTA) of vision-language models (VLMs) under long-tailed test distributions. The method has three co-designed components: Synergistic Prototypes (SyPs) that maintain two types of prototypes (DPs and EPs) to enrich tail-class representations, Rebalancing Shortcuts (RSs) with a class re-allocation loss to improve feature clustering, and Balanced Entropy Minimization (BEM) that modifies standard entropy minimization with a penalty term weighted by prediction confidence. The paper evaluates on 15 datasets across 3 benchmarks (OOD, Cross-Domain, Corruption), 3 imbalance ratios, 12 baselines, and multiple backbones, showing consistent improvements in both accuracy and macro-F1 with competitive efficiency.

## Strengths

- **Novel and well-motivated problem.** The paper correctly identifies that existing TTA for VLMs assumes balanced test distributions, while real-world test streams are often long-tailed. It identifies specific failure modes (text-induced tail erosion, modality-bias amplification) unique to the VMA LT-TTA setting. This problem framing is practically relevant and underexplored.

- **Extensive and rigorous evaluation.** The evaluation covers 15 datasets across 3 benchmarks (OOD, Cross-Domain, Corruption), 3 imbalance ratios (10, 20, 50), 12 baselines spanning diverse approaches (prompt tuning, training-free, visual-adaptation, prototype-based, RL-based), and 5 backbones (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG). L-TTA shows consistent improvements, particularly in macro-F1 which directly measures class balancing. The efficiency results (1.45h on ImageNet vs. 18.3h for RLCF and 27.7h for WATT) are a concrete strength.

## Weaknesses

### Major

- **No error bars or standard deviations despite 5 runs.** The paper states each experiment is run 5 times (line 208, line 212 caption) but the main tables (Tables 1-3) report single numbers without variance estimates. On many datasets L-TTA's lead over the second-best method is 1–2% (e.g., OOD average at imb=10: 65.97 vs 64.50 for DPE). Without standard deviations, the reader cannot assess statistical significance. This is a basic expectation for experimental papers and the most impactful fixable weakness.

### Minor

- **Missing ablation condition.** Table 6 reports DP alone, EP alone, DP+RS, EP+RS, SyP(DP+EP)+RS, and the full method, but does not include SyP(DP+EP) without RS. This would help isolate RS's marginal contribution beyond the combined prototypes. (Note: the claim that SyP+RS without BEM is missing is incorrect — row 5 "SyP(DP+EP)+RS" is exactly that condition.)

- **Internal inconsistency in hyperparameter K.** The implementation (line 208) sets K=0.3 for main results, but the ablation (line 334, Figure 4c) finds K=0.2 yields the best performance, with K values ranging from 0.1 to 1.0. The paper does not explain why 0.3 was chosen over 0.2, nor does it clarify whether K is an integer count or a ratio relative to C (the fractional values suggest the latter, but this is never stated).

- **Propositional framing without rigorous assumptions.** Propositions 1 and 2 are presented in theorem-like form with proofs deferred to the appendix, but the main text's assumptions are vague ("split C into C_head and C_tail with certain measurements"). Proposition 2 only shows the gradient gap between head and tail shrinks under BEM, not that this leads to better optimization (a smaller gap could in principle mean both are poorly optimized). These are better framed as motivating intuitions rather than formal results.

- **BEM's self-limiting property.** The penalty term (1−P̃)^β suppresses the prior adjustment for confident predictions. The paper states this "favors classes that are both rare and uncertain," but a tail-class sample predicted confidently (correctly or incorrectly) would also have its adjustment suppressed. BEM's effectiveness therefore depends on the empirically plausible but unverified assumption that tail-class predictions remain systematically uncertain. The paper does not discuss this self-limiting behavior.

### Trivial

- The claim that EPs store "the most improbable features of each class" (line 98) is imprecise: the update mechanism (Eq. 5) uses prediction-probability-weighted EMA across all classes' features, not an explicit selection of improbable features. The naming itself is reasonable (the φ weighting gives features from non-predicted classes slightly more relative influence, which is consistent with the "exclusionary" concept).

## Nice-to-Haves

- Adding simple post-hoc LT-adapted baselines (e.g., TPT/DPE with test-time logit adjustment using estimated class frequencies) would help contextualize whether the full three-component L-TTA design is necessary or whether simpler fixes are sufficient.
- An empirical analysis of actual gradient statistics (head vs. tail) during adaptation, showing how standard EM degrades tail classes and how BEM corrects this, would strengthen the paper's mechanistic claims beyond the current informal propositional framing.
- The paper mentions "rich classes" (text-pretraining bias causing certain classes to have high accuracy regardless of head/tail status) as a key failure mode, but provides no quantitative evidence for this phenomenon.

## Removed Points

- "EP update mechanism is conceptually confused / name contradicts the update equation": REMOVED because the reviewer's mathematical claim is incorrect. For the predicted class (φ=0), EMA update is standard. For other classes (φ≈1), the new feature has slightly *more* relative influence (old prototype weighted by N-1 rather than N), meaning non-class features contribute more to each class's EP — supporting rather than contradicting the "exclusionary" concept.
- "Figure 1b is schematic, not empirical — claims about text-induced tail erosion are unsupported": REMOVED. Schematic figures illustrating conceptual failure modes are standard practice; the paper does not claim Figure 1b is a quantitative result.
- "Missing ablation: SyP+RS without BEM": REMOVED because this condition IS present in Table 6 (row 5: SyP(DP+EP)+RS is SyP+RS without BEM).
- Generic criticisms about missing t-SNE/visualization analysis: MOVED to Nice-to-Have.

## Novel Insights

None beyond the paper's own contributions. The main novel observation from the review process is that the BEM penalty term is self-limiting by design: as tail-class predictions become more confident (which is the goal), the prior adjustment weakens. This is a subtle behavior the paper does not discuss.

## Suggestions

1. Add standard deviations to all main result tables (Tables 1-3) since 5 runs are performed.
2. Clarify whether K is an integer count or a ratio relative to C, and explain why K=0.3 (not the ablation-optimal 0.2) is used for main results, or update to the optimal value.
3. Add the SyP(DP+EP) without RS condition to the ablation table.
4. Consider re-framing Propositions 1-2 as empirical intuitions rather than theorem-like statements, or provide clear assumptions in the main text.
5. Add a discussion of BEM's self-limiting behavior: what happens when tail-class predictions become confident.

## Score and Decision

**Calibration anchors used:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lF9QXpfNHm.md` (avg 4.67, Round 1, itemized): ROSITA — TTA for VLMs but weaker evaluation, some technical limitations. Our paper is clearly stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6yJuDK1DsK.md` (avg 4.50, Round 1, itemized): FEATHER — lifelong TTA but CNNs-only, limited evaluation. Our paper is stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BUDxvMRkc4.md` (avg 4.67, Round 1, itemized): BLG — long-tailed + VLM but no TTA component. Different setting.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yD2JMeKumt.md` (avg 6.00, Round 1 & 2, itemized): DOTA — closest anchor, same TTA-for-VLMs setting. Our paper has more extensive evaluation (15 datasets vs ~11) and clearer problem novelty, but DOTA has a cleaner/simpler method and doesn't face the same error-bar criticism. Our paper's weighted comparison shows heavier negative items (missing error bars at -3.58) but also heavier positives (efficiency at +4.59, extensive evaluation at +3.05). Net: comparable to DOTA's 6.00.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kIP0duasBb.md` (avg 6.67, Round 2, itemized): RLCF — TTA for VLMs with CLIP reward. Simpler cleaner method, evaluation across 3 tasks. Our paper is weaker on method cleanliness and polish.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/75PhjtbBdr.md` (avg 6.25, Round 2, itemized): Multi-Label BEM — introduces BEM for multi-label TTA. Strong theoretical analysis. Our paper has comparable evaluation scope and problem novelty.

**Round 1 bracket**: [5.5, 7.5] — clearly above reject-range papers (4.5-4.67) and below the strongest accepts (6.67+).

**Narrowing**: The weighted-item comparison shows this paper shares strong evaluation extent with DOTA (6.00) but carries a heavier negative weight (-3.58 for missing error bars) that DOTA largely avoids. The paper does not reach the method cleanliness and polish of RLCF (6.67).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>