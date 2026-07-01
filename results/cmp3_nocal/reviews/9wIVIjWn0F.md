Now I have a thorough understanding of the paper and have verified the critic's claims against the source text. Let me write the final consolidated review.

## Summary

This paper proposes RTA (Regression-based Test-Time Adaptation), which trains a LightGBM decision tree on CLIP logits from a diverse image pool to predict pseudo cross-entropy loss, then uses the predicted loss at test time to select confident augmented views for ensemble prediction. The paper first presents a "ceiling TTA" analysis showing that selecting views based on ground-truth cross-entropy loss yields near-oracle performance, then attempts to approximate this mapping using only pseudo-labels.

## Strengths

1. **Ceiling-TTA analysis (Section 4.1, Tables 1–2) is genuinely informative.** Using ground-truth label CE loss (LCE) for view selection yields dramatic gains (e.g., 90.2% on ImageNet-A, 94.4% on ImageNet-R with ViT-B/16 and 64 views), vastly outperforming entropy-based selection. This cleanly demonstrates that view selection via true-label CE loss is a near-optimal oracle, and it establishes a clear motivation for learning such a mapping.

2. **The method is computationally lightweight.** Training a LightGBM once on 1,000 samples and then applying it without online updates is practically appealing. The paper correctly distinguishes itself from methods that require continuously maintained memory banks or per-instance optimization.

3. **Multi-label results show the largest and most consistent gains.** On MSCOCO (RN50: 53.25% vs ML-TTA's 51.58%; ViT-B/16: 58.95% vs 57.52%) and NUSWIDE (45.52% vs 42.53%), the margins are substantial and robust across backbones (Tables 5–6). This suggests the approach may be especially well-suited to multi-label settings.

## Weaknesses

### Fatal
None.

### Major

**The regression target is a deterministic function of the input logits, and the critical ablation needed to validate the claimed mechanism is missing.** The regression model is trained on pairs (logits $s^{\text{reg}}$, pseudo-CE loss $\mathcal{L}_{\text{CE}}(\mathbf{y}^{\text{reg}} \mid s^{\text{reg}})$). Since the pseudo-label $\mathbf{y}^{\text{reg}}$ is the argmax of the same logits' softmax, the target simplifies to $-\log(\max(\text{softmax}(s)))$ — a function that can be computed directly from the logits in closed form. The paper frames this as "establish[ing] a regression mapping between augmented views and their corresponding cross-entropy loss" (abstract) and as a "key finding" of a "strong regression mapping" (Section 1), consistently implying that the regression captures something about *true* label quality. What it actually learns is an approximation to a simple deterministic function of the logits.

The paper never includes the single most important ablation: comparing RTA's regression-based view selection against **directly computing $-\log(\max(\text{softmax}(s)))$ at test time** (i.e., using the negative log of the max-softmax probability as the selection criterion without any regression). If RTA outperforms this direct baseline, then the regression tree genuinely adds value beyond what is already in the logits and the paper would have a real finding. If it matches or underperforms the direct baseline, then the contribution reduces to an engineering approximation of a trivial function. Without this experiment, the claimed intellectual contribution — that the regression mapping is the source of RTA's effectiveness — is unsupported by evidence.

This does not invalidate RTA's empirical results (the method may still work well), but it means the paper's central framing and claimed "key finding" are overstated. The paper should either provide the missing ablation or reframe the contribution honestly as a practical engineering study.

### Minor

1. **Gains over strong baselines are modest in several settings, and no uncertainty quantification is reported.** On the most competitive benchmarks (Table 3, ViT-B/16), the margins over Zero (NeurIPS 2024) are: IN-1k +0.24, IN-V2 +0.32, IN-R +0.23. On cross-domain (Table 4, ViT-B/16), RTA's average is 68.70 vs BCA's 68.59 — a 0.11% difference — and RTA underperforms BCA on 4 of 10 individual datasets (Pets, Flowers, DTD, EuroSAT, SUN). No standard deviations, confidence intervals, or multi-seed runs are reported anywhere. With margins below 0.5% on several datasets, it is impossible to assess whether these differences are meaningful or within measurement noise.

2. **The claimed advantage over entropy-based selection is not empirically demonstrated.** The paper asserts that entropy "struggles to estimate reliable entropy for outliers" (abstract) and that RTA overcomes this by learning a "view-loss mapping relationship" on diverse data. However, since RTA's regression target ($-\log(\max(\text{softmax}(s)))$) is itself computed from the current instance's probability distribution, the paper provides no analysis showing *how* or *why* the regression tree's predictions differ from simpler confidence measures (e.g., max-softmax probability, entropy) for OOD samples. The t-SNE visualization (Figure 2) uses *true* label loss, not the pseudo-CE loss that RTA predicts; the Spearman's analysis (Figure 3) similarly correlates logits with *true* labels. These analyses motivate the general approach but do not explain RTA's mechanism over entropy-based alternatives.

3. **Potential data leakage between regression training and IN-1k evaluation.** The regression model is trained on 1,000 samples drawn from "ImageVal-12k" (line 332), which appears to be a subset of the ImageNet validation set. The IN-1k results in Table 3 are reported on the ImageNet validation set. The paper does not specify whether the 1,000 training samples are excluded from evaluation. This could inflate the IN-1k numbers, though OOD results (IN-A, IN-R, etc.) would be unaffected. The authors should clarify this.

4. **The gap between the ceiling-TTA oracle and RTA's actual performance is not discussed.** The ceiling analysis (Section 4.1) achieves 90.2% on IN-A (ViT-B/16), while RTA reaches 65.65%. This 24.55 percentage-point gap is the measure of how much information is lost by substituting pseudo-labels for true labels. The paper motivates RTA from the ceiling but never addresses this gap, leaving unclear whether the regression mapping as implemented actually approximates the oracle in any meaningful sense.

### Trivial
None.

## Nice-to-Haves

- An ablation comparing RTA against using max-softmax probability directly as the view-selection criterion, without any regression.
- A direct empirical comparison against Kim et al. (NeurIPS 2020), the most closely related loss-predictor approach, which is cited but not evaluated.
- An analysis of pseudo-label accuracy on the regression training data (what fraction of the high-confidence pseudo-labels are correct?).
- Sensitivity analysis for the number of augmented views ($N$) and the filtering ratio beyond the fixed default values (64, 0.1) inherited from Zero and ML-TTA.
- Justification for the choice of LightGBM over simpler alternatives (e.g., an MLP with few parameters, ridge regression on logits).

## Removed Points

These points are flagged for removal but are retained here in case they are useful:

1. *"The free lunch metaphor is misleading"* — Removed as subjective framing critique without technical substance.
2. *"No discussion of why LightGBM specifically"* — Removed; this is a nice-to-have implementation detail, not a weakness.
3. *"Figures 4 and 5 are informative but descriptive"* — Removed as too generic; the figures serve their stated purpose.
4. *"The critic's question about whether the regression tree is a differentiable approximator"* — Removed; the paper does not claim differentiability, and this is a non-issue.
5. *"Comparison against using max softmax probability directly"* — Already covered in the Missing Ablation (Major weakness); not a separate point.

## Novel Insights

The harsh critic's most valuable insight is that the regression target $\mathcal{L}_{\text{CE}}(\mathbf{y}^{\text{reg}} \mid s^{\text{reg}})$ is a deterministic function of the input logits — specifically $-\log(\max(\text{softmax}(s)))$. This reframing exposes a gap between the paper's claimed contribution (learning a mapping to cross-entropy loss, framed as approximating the ceiling oracle) and what it actually does (learning an approximation to a quantity computable from the logits alone). The critic correctly identifies that the missing ablation — comparing RTA against direct computation of this function — is the single experiment needed to determine whether the regression adds genuine value. Beyond this, the critic's observations about the modest margins on several benchmarks and the lack of uncertainty quantification are standard but well-articulated.

## Suggestions

1. **Add the critical missing ablation:** Compare RTA's regression-based view selection against directly computing $-\log(\max(\text{softmax}(s)))$ at test time. If RTA outperforms this baseline, report by how much and analyze why. If not, acknowledge this honestly and reframe the contribution accordingly.

2. **Add uncertainty quantification:** Report results over multiple random seeds with standard deviations, at least for the main tables (Tables 3–4). With margins below 0.5% on multiple datasets, this is essential for interpretation.

3. **Clarify the training/evaluation data split:** Explicitly state whether the 1,000 samples from ImageVal-12k are removed from the IN-1k evaluation set. If they are not removed, re-run the IN-1k evaluation excluding them.

4. **Add a mechanistic analysis:** Show how RTA's predicted loss differs from max-softmax probability or entropy for individual examples, particularly OOD examples where entropy is argued to be unreliable. A scatter plot or case study would help substantiate the claimed advantage.

5. **Discuss the ceiling-to-RTA gap:** Address why RTA's performance is far below the ceiling oracle. Is it because the pseudo-labels are noisy? Because the regression tree is a poor approximator? Or because the fundamental mapping from logits to true CE loss is not learnable without label supervision?

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>