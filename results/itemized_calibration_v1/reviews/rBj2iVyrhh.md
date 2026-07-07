## Summary

This paper proposes CCAT (Classifier-Constrained Alternating Training), a two-stage framework for multimodal learning that addresses modality imbalance. The key idea is: (1) pretrain a shared classifier with bidirectional cross-attention and a regularization term that balances modality contributions; (2) freeze this classifier during alternating training to prevent it from developing bias toward faster-converging modalities, using modality-specific LoRA adapters to handle the distribution mismatch between fused and unimodal inputs; (3) apply sample-level secondary updates for severely imbalanced samples. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements over existing methods.

## Strengths

1. **Clear problem diagnosis.** The paper identifies a genuine and non-obvious limitation of existing alternating training methods (MLA et al.): they reduce encoder-level gradient interference but fail to prevent the shared classifier from developing structural preference toward faster-converging modalities. This diagnosis is well-articulated (Section 1) and supported by the empirical contribution plot in Figure 1.

2. **Consistent SOTA across three datasets.** The method outperforms all baselines on all three benchmarks (Table 1). The gains on Kinetic-Sound (+6.76% vs LFM, the previous best) are substantial, and unimodal accuracy for the weaker modality also improves in most cases (e.g., CREMA-D Video: 68.01% for MLA → 73.79% for CCAT).

3. **Clean ablation design.** Table 2 systematically isolates each component (classifier freezing, alternating training, secondary updates, LoRA), and every component contributes positively to the final result. The ablation is conducted on the same dataset and with the same encoder backbone, increasing confidence that the individual design choices matter.

4. **Useful architectural insight.** The idea of modality-specific LoRA modules to bridge the distribution mismatch between the classifier (pretrained on fused features) and the unimodal inputs during alternating training (Section 3.3) is a practical and lightweight solution to a real design tension.

## Weaknesses

### Fatal
None.

### Major

1. **Baseline comparison fairness is not established.** The paper states it uses "ResNet18 encoders for both audio and visual modalities across all datasets" (line 232) but does not specify whether *all baselines* were re-implemented with these same encoder backbones, or whether numbers for some baselines were taken from their original papers (which likely use different backbones, e.g., VGGish for audio). The fact that LFM's MVSA results are listed as "–" (not reported) while CCAT was run on MVSA suggests inconsistent experimental setups across baselines. This is the most structurally significant weakness: if baselines were not re-implemented under identical conditions, the comparison could favor the proposed method. The authors must clarify exactly which baselines were re-implemented and which numbers were adopted from prior work, and ideally provide a controlled re-implementation of all baselines under the same encoder backbone.

### Minor

2. **Numerical discrepancy in the abstract.** The abstract and introduction claim "accuracy gains of +1.35% on CREMA-D." From Table 1, the best baseline (LFM) achieves 83.62% and CCAT achieves 85.89%, which is an absolute gain of +2.27 percentage points, not +1.35%. The +1.35% does not match any baseline comparison in the table. This needs correction; notably the actual gain is larger, so the error understates the result.

3. **Overclaimed "theoretical framework."** Contribution (i) claims "a new theoretical framework for understanding multimodal imbalance" and the paper describes "a profound theoretical isomorphism" (line 87) between class and modality imbalance. What Section 3.1 actually provides is a heuristic analogy supported by two gradient equations (Eq. 2 and 3) describing known phenomena. No theorem, bound, or formal derivation is provided. The paper should substantially temper this claim — it is a conceptual connection, not a theoretical framework.

4. **No statistical significance or variance reported.** The paper reports "average test accuracy (%) of three random seeds" but provides no standard deviations, confidence intervals, or any measure of variance (Table 1 caption). For a method where some gains are modest (e.g., +1.92% on MVSA relative to MMPareto's 78.81%), knowing whether the improvement is within or beyond the noise floor is essential. The t-SNE clustering metrics (CH, SH, DB) in Figure 5 are also reported as point estimates without uncertainty.

5. **Secondary update mechanism's overfitting risk not discussed.** The sample-level secondary update (Algorithm 1, lines 10–15) performs additional gradient steps on samples where c_i^m < β, using the same batch already used for the primary update (lines 6–8). Samples flagged as imbalanced receive effectively double the gradient updates per epoch. The paper does not discuss whether this increases effective learning rate on those samples, whether it leads to overfitting on hard or noisy samples, or how the threshold β trades off between addressing imbalance and overfitting. The threshold values vary substantially across datasets (β=0.15 for CREMA-D, 0.30 for KS, 0.05 for MVSA) without analysis of what drives these differences.

6. **t-SNE analysis is weakly informative.** The features visualized in Figure 5 are not clearly specified (encoder outputs? classifier inputs? fused features?), and the "Non-Fixed Classifier" setting achieves CH=200.01, barely different from MLA's CH=198.98, which is surprising given the ~3% accuracy difference between these two conditions. The quantitative clustering improvement from CCAT (CH=242.55) is more meaningful but would benefit from error bars and a clear statement of which features are being compared.

### Trivial

7. **Figure 1 contribution disparity metric unclear.** The text claims MLA "reduces initial contribution disparity (1.00 → 0.92)," but the table below Figure 1 shows MLA Modality A going from 1.00 to 0.90 and Modality B from 0.00 to 0.10. Neither the difference (0.80) nor the ratio (9) equals 0.92. The metric being reported should be clarified.

8. **Equation (5) notation not self-contained.** The mutual information estimation formula uses notation ( \bar{ \mathbf{f} }_i, \bar{ \mathbf{z} }_i^m ) and summation over l that are not defined in the main text.

## Nice-to-Haves

- Sensitivity analysis for the regularization coefficient λ (currently set to 0.001 with no ablation).
- A controlled comparison of frozen+LoRA vs. fine-tuned classifier (no freeze, no LoRA) starting from the same pretrained initialization, to directly test whether the freezing strategy itself outperforms allowing the classifier to adapt.
- A limitations section discussing: computational overhead of sequential modality processing and secondary updates; sensitivity to hyperparameters β and λ; the assumption of exactly two modalities.
- Reporting total training time relative to MLA and standard joint training.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Distribution mismatch not resolved — it is sidestepped (Critic's Point 4):** The paper acknowledges the distribution mismatch (line 133) and proposes LoRA modules as a solution; the ablation shows LoRA contributes positively (+1.21% on CREMA-D). Claiming the mismatch is "sidestepped" rather than addressed is too harsh — the paper identifies the problem and proposes a reasonable mitigation strategy. The suggestion to compare freeze+LoRA vs. fine-tuned classifier is a valid strengthening but is a nice-to-have, not a flaw in the current approach.
- **L1 vs L2 regularization choice:** The critic asks why L1 rather than L2 or KL divergence was chosen. This is a granular design decision; the L1 penalty is a simple and sensible default. Not a meaningful weakness.
- **Algorithm 1 missing details:** The critic notes the algorithm doesn't specify whether the classifier is updated during pretraining. This is clear from the paper: Algorithm 1 explicitly starts with "Freeze Cls" and handles only the alternating training stage; pretraining is described separately in Section 3.2. The secondary update operating on the same batch is also clearly shown in the algorithm.
- **LoRA rank variation across datasets (r=2 vs r=8):** The paper reports a full grid search (Table 3) and explains the choice was empirically determined via validation. The critic's question about why MVSA needs r=8 is reasonable but the paper does report the search results transparently.
- **Missing code release:** The paper does not mention code release, which is common for double-blind conference submissions and carries no weight in evaluation.
- **Missing limitations section:** A reasonable suggestion for improvement but not a weakness in the paper's technical contribution.

## Novel Insights

The strongest analytical contribution from the review process is identifying the structural tension at the heart of the paper's design: the classifier is pretrained on fused (cross-attended) features but must process unimodal features during alternating training and inference. While the paper acknowledges this distribution mismatch (line 133) and proposes LoRA adapters to bridge it, the ablation shows only a modest 1.21% gain from LoRA on CREMA-D (84.68% → 85.89%), which leaves open the question of whether the mismatch is genuinely resolved. A more controlled experiment — comparing frozen+LoRA against simply fine-tuning the classifier on unimodal features from the same pretrained initialization — would cleanly isolate whether the freeze strategy itself is what matters. This is a sharper experimental design question than the paper currently addresses.

## Suggestions

- Clarify whether all baselines were re-implemented with identical encoder backbones and experimental setups. If numbers from original papers were used, re-run all baselines under the same conditions or explicitly state the differences.
- Correct the CREMA-D accuracy gain in the abstract from +1.35% to the actual value (+2.27% over LFM).
- Temper the "theoretical framework" claim; describe Section 3.1 as a conceptual analogy.
- Report standard deviations over three random seeds for all main results.
- Add a discussion of the secondary update's overfitting risk and how β was chosen relative to dataset characteristics.
- Clarify which features are visualized in the t-SNE plots (Figure 5) and add error bars to the clustering metrics.

## Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| ul1cjLB98Y.md (A Theory of Unimodal Bias) | 5.25 | R1 | Yes | More theoretical, limited to linear networks; our paper has stronger empirical validation on real data |
| XTwwtlEfTF.md (Robust MML with Missing Modalities) | 4.50 | R1 | Yes | Uses parameter-efficient adaptation; our paper is clearer and more novel |
| 5BXWhVbHAK.md (Can One Modality Synergize Training) | 6.33 | R1 | Yes | Strong theory + comprehensive validation; our paper is weaker in theory but has comparable empirical breadth |
| Pa6SiS66p0.md (Beyond Unimodal Learning) | 4.33 | R2 | Yes | Weak baselines, insufficient experiments; our paper has stronger empirical methodology |
| BZWssJoYEv.md (Towards Holistic Multimodal Interaction) | 5.50 | R2 | Yes | Information-theoretic analysis with limited experiments (≤2% gains); our paper has larger and more consistent improvements |
| 19ufhreGTj.md (Understanding Dimensional Collapse) | 5.80 | R2 | No | Cross-modal distillation analysis; our paper proposes a new method rather than analysis |

**Bracket:** After Round 1, the initial bracket was [5.5, 6.5]. The Round 2 narrowing confirmed this range: our paper is clearly stronger than the 4.33–5.50 group (better experiments, cleaner ablations, larger gains) but has a notable baseline fairness concern and overclaimed theory that prevent it from reaching the 6.33 level of the synergy paper. The most directly comparable anchor (the 5.25 theory paper) was limited to linear networks; our paper avoids that limitation. The 5.50 interaction paper had marginal improvements (≤2%) and unclear methodology; our paper has larger improvements and clearer experimental design. The baseline fairness question (Major weakness) is the primary factor keeping the score below the 6.33 anchor.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>