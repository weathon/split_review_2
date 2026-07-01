## Summary

This paper introduces SPS and SPS+, differentially private dataset distillation algorithms that generate private synthetic datasets by matching privatized activation statistics from a public pretrained model. The core idea — adapting D3S-style activation-statistic-matching to the DP setting via a single-shot noise-addition step — is well-motivated, technically sound, and supported by competitive results. SPS+ achieves 95.1%/71.0% (single WRN28-10) at ε=1 on CIFAR-10/100, exceeding the DP-SGD baseline of 94.8%/70.3%, and demonstrates flexibility advantages (ensembling, federated learning, continual learning without additional privacy cost) that follow naturally from the data-based approach.

## Strengths

1. **Genuinely novel combination of dataset distillation with DP.** The paper correctly identifies that activation-statistic-matching methods (D3S) are particularly suited to DP because the statistic-collection phase can be privatized with a single noise-addition step, avoiding the iterative composition costs that would plague bilevel or trajectory-matching distillation approaches (Section 2.3, Section 3.2.2).

2. **Strong quantitative results from the single-model baseline.** SPS+ (single WRN28-10) achieves 95.1%/71.0% on CIFAR-10/100 at ε=1, outperforming the DP-SGD baseline of De et al. (2022) (94.8%/70.3%). On CIFAR-100 at low ε, the improvement is meaningful (0.7% at ε=1) — a regime where per-class noise scaling is most punishing (Table 1).

3. **Well-demonstrated flexibility advantages.** Sections 5.4–5.6 convincingly show downstream benefits that DP-SGD cannot easily provide: ensembling without additional privacy cost (Table 1), oversized synthetic datasets (Table 3), asynchronous federated learning (Section 5.5), and continual learning without catastrophic forgetting or privacy budget exhaustion (Section 5.6). These follow directly from the data-based approach and are accompanied by actual experiments.

4. **Well-engineered technical contributions.** Individual components — removing reliance on a privately trained model via random projections (Section 3.2.1), noise redistribution between global and per-class statistics (Section 3.2.4), multistage clipping (Section 4.1), and grouped pseudo-classes (Section 4.2) — are each motivated by specific failure modes in the DP setting.

## Weaknesses

### Fatal
None.

### Major

1. **The headline comparison conflates the data-generation method with post-processing advantages that are orthogonal to the algorithm itself.** The abstract (line 9) presents SPS+ as achieving **96.2%/76.6%** on CIFAR-10/100 vs. the DP-SGD baseline of 94.8%/70.3%. However, these headline numbers come from SPS+ with an **ensemble of 5 WRN34-10 models** after non-private fine-tuning. The DP-SGD baseline is a **single WRN28-10 model**. The single-model comparison (SPS+ WRN28-10: 95.1%/71.0% vs. DP-SGD WRN28-10: 94.8%/70.3%) shows real but much smaller gains of 0.3% and 0.7% respectively — gaps within or near one standard deviation of the baseline. The paper does present the breakdown in Table 1, but the abstract gives only the ensemble-asymmetric comparison without qualification. Since the other contributions of SPS+ (grouped pseudo-classes, multistage clipping) are evaluated on single models, conflating ensemble/larger-model gains with distillation-algorithm gains exaggerates the method's advantage over DP-SGD.

2. **The privacy accounting for multistage clipping does not report the number of stages (M) per entry in Table 1.** Theorem 4.1 states that M releases compose to ε = Mα/(2σ²) in RDP terms, so ε scales linearly with M. Table 1 reports accuracy at ε values {1, 2, 4, 8} but does not state which M was used to achieve each ε for the SPS+ results. Figure 2 shows that larger M improves accuracy at a given ε (by lowering per-stage noise), but without knowing M per entry, the reader cannot verify whether the apparent advantage over DP-SGD reflects a more favorable decomposition of the privacy budget. The paper states that M is varied and that details are in Section D.2 (stripped appendix), but the main comparison table should specify M.

### Minor

1. **The grouped pseudo-classes mechanism is described too briefly in the main text for independent evaluation.** Section 4.2 states that P > C pseudo-classes are formed, each class belongs to PN_{c/p}/C pseudo-classes (implying overlap), and that the technique works "only due to dynamics of optimizing the loss function, specifically the Σ inversion in the KL-divergence, and the eigenvalue clipping of Σ." The mechanism by which overlapping mixed-class statistics yield discriminative synthetic images is not explained at a level that can be evaluated from the main text alone, yet the paper's strongest CIFAR-100 results depend on it. The paper defers to Section A.5 (stripped appendix) for details.

2. **CAMELYON17 comparisons use different ε values across methods.** Table 2 reports SPS at ε=8, DP-Diffusion at ε=10, Private Evolution at ε=7.56, and DP-SGD at ε=10. The ε=8 versus ε=10 difference makes the comparison less precise, especially since SPS's advantage over DP-Diffusion (92.6% vs. 91.1%) is modest.

3. **The BatchNorm incompatibility framing in the introduction is somewhat misleading in context.** The paper states that DP-SGD has "incompatibilities with... BatchNorm" (line 13). SPS itself uses BatchNorm (post-BatchNorm activations) from a public pretrained model — it offloads the BatchNorm problem to the public pretraining phase rather than solving it within the DP pipeline. This distinction should be clearer.

4. **No ablation for the dimensionality choices D_G and D_C in the main text.** These hyperparameters directly control the signal-to-noise ratio of the privatized statistics and are a claimed advantage over DP-SGD (line 120). Their impact on accuracy is not explored in the main text.

5. **The margins over the sole DP-SGD baseline are small on single-model comparisons (0.3–0.7%).** While the paper also demonstrates flexibility advantages, the core accuracy comparison rests on a single 2022 baseline. A broader set of gradient-based comparisons or discussion of whether the baseline remains current would strengthen the evidence.

### Trivial

1. **Table 3 column header reads "Distilled Dataset size" but values (1×, 2×, etc.) are multipliers of the original dataset size, not absolute sizes.**

## Nice-to-Haves

- An ablation study showing how the dimensionality choices D_G and D_C affect accuracy across privacy budgets.
- Discussion of whether privacy amplification by subsampling (e.g., Poisson subsampling) could be applied to further reduce effective ε.
- A computational cost comparison (GPU-hours) between SPS+ generation and DP-SGD training, as the paper acknowledges generation cost is high (Section 6) but does not quantify it.

## Removed Points

These points were raised in the input review but are removed or downgraded per the filtering rules:

- **Typo/parser artifact in Theorem 4.1 (δ vs. σ) and the norm bound expression in Section 3.2.4:** Removed under the hard rule about formatting artifacts from PDF extraction.
- **Speculation about more recent DP-SGD baselines:** The critic questioned whether De et al. (2022) remains SOTA and whether newer results would change the comparison. Removed because we cannot verify the existence of such works; this would constitute speculation about missing related works. (The reframed Minor weakness #5 above retains only the measurable observation about small margins.)
- **Criticism that synthetic datasets are same size as original (50k images), at odds with "distillation" framing:** Removed because the paper also demonstrates compression results (Figure 5 shows performance at 10% size) and the primary contribution is private data generation, not compression.
- **Request for alternatives/ablations for random projection choices:** The critic noted the paper doesn't discuss alternatives. This is a generic "could-do-more" observation that does not identify a specific flaw; folded into Minor weakness #4.
- **Section-by-section observations about missing confidence intervals, BN vs. SPS framing, etc.:** Where these duplicated already-listed weaknesses, they were merged. Where they were purely generic observations (e.g., "the choice of sigmoid nonlinearity... the paper does not discuss alternatives"), they were removed as speculation without identified concrete harm.

## Novel Insights

The input review's most notable observation is that the paper's headline numbers (96.2%/76.6%) reflect a compound of three distinct advantages — the distillation algorithm, ensembling, and larger model capacity — while the single-model improvement over DP-SGD is 0.3–0.7%. This is not a contradiction of the paper's claims (the single-model improvements are real) but an important contextualization. The review's second key insight is the transparency gap in M-stage accounting: because the privacy budget scales linearly with M, and M is not reported per Table 1 entry, the reader cannot verify whether the reported ε values are directly comparable to DP-SGD's composition structure. Both insights are about presentation and verification, not methodological validity.

## Suggestions

1. Disaggregate the sources of performance in the abstract and introduction: state both the ensemble/larger-model result and the single-model WRN28-10 result when comparing to DP-SGD.
2. Report the M value used for each entry in Table 1, or add a footnote explaining the relationship between M and reported ε for each condition.
3. Expand the grouped pseudo-classes explanation in the main text to a level that does not require the appendix for basic understanding — at minimum, clarify the privacy implications (or lack thereof) of overlapping pseudo-class statistics.
4. Add an ablation study for D_G and D_C dimensionality choices in the main text or supplement.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>