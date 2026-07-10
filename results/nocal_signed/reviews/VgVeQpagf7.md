Now I have a clear picture. Let me compose the final review.

## Summary

This paper presents SPS (Summarize-Privatize-Synthesize), a differentially private dataset distillation method that adapts D3S-style activation-statistic matching to produce synthetic data with formal DP guarantees. The key innovation is privatizing only the statistic-collection phase (a single Gaussian mechanism step per stage) rather than each optimization iteration, which enables high-quality synthetic data that can be post-processed freely. On CIFAR-10/100, SPS+ becomes the first generation-based method to match or exceed DP-SGD accuracy across multiple privacy budgets ($\varepsilon \in \{1,2,4,8\}$), while demonstrably supporting model ensembling, federated learning, and continual learning without additional privacy cost.

## Strengths

- **First generation-based method to match or exceed DP-SGD accuracy on standard image benchmarks.** Table 1 shows SPS+ (WRN34-10 Ensemble) at $\varepsilon=1$ achieving 96.2% on CIFAR-10 and 76.6% on CIFAR-100, versus DP-SGD (WRN28-10) at 94.8% and 70.3% respectively — a gap of roughly 1.4 points on CIFAR-10 and 6.3 points on CIFAR-100 that holds consistently across $\varepsilon \in \{1,2,4,8\}$. Prior generation-based methods (Private Evolution at 89.13% at $\varepsilon=10$, DP-KIP at 58.7%) were far behind DP-SGD; this paper closes that gap decisively.

- **The core technical idea is well-motivated and the engineering choices are concretely justified.** Adapting D3S-style activation-statistic matching to DP is a natural fit because it privatizes only the statistic-collection phase rather than each optimization iteration. The use of projected low-dimensional statistics to control the sensitivity dimension, replacement of the privately-trained $\theta_T$ with a public pretrained model, and the noise-redistribution trick (scaling per-class statistics by $\sqrt{S}$ without changing the privacy cost) are all thoughtfully explained and technically sound.

- **The SPS+ enhancements produce measurable improvements.** Table 1 shows SPS+ adds roughly 2–20 points on CIFAR-100 depending on $\varepsilon$, and 1–2 points on CIFAR-10 compared to SPS. This is the difference between being below DP-SGD (SPS on CIFAR-100) and above it (SPS+ on CIFAR-100).

- **The downstream flexibility experiments genuinely demonstrate advantages that DP-SGD cannot match.** The federated learning, continual learning, and oversized-dataset experiments directly illustrate the paper's central thesis: data-based privacy enables reuse patterns — asynchronous FL, unlimited reuse for continual learning, unrestricted use of GSAM and ensembling — that gradient-based privacy cannot support without additional composition cost.

## Weaknesses

### Fatal
None.

### Major

- **Ambiguous notation in Theorem 4.1 (privacy guarantee).** The theorem reads $\varepsilon = M\alpha/(2\delta^2)$, but $\delta$ already denotes the DP failure probability throughout the paper (e.g., $\delta = 10^{-5}$ on line 204). The noise scale in eq. (4) is $\sigma = b_0\|v\|_{\max}$, so the intended formula should be $\varepsilon = M\alpha/(2b_0^2)$. The reuse of $\delta$ in a conflicting role makes the core privacy claim unverifiable as stated. This is a fixable notational collision — the paper correctly invokes the standard RDP composition of Gaussian mechanisms — but it must be corrected for the paper to be self-consistent. (Line 196.)

### Minor

- **Grouped pseudo-classes (GPC) — a core component of SPS+ — lacks a clear theoretical account.** The paper states it "only works due to dynamics of optimizing the loss function, specifically the $\Sigma$ inversion in the KL-divergence, and the eigenvalue clipping of $\Sigma$" (lines 164–190) without explaining what those dynamics are or why they prevent GPC from working with simpler estimators. While the empirical improvements are clear, this hand-wavy justification is insufficient for a mechanism that is central to SPS+'s advantage. Whether the random grouping is public/data-independent should also be stated explicitly.

- **The headline comparison conflates multiple structural differences.** The abstract cites 96.2% (SPS+ WRN34-10 Ensemble with post-processing freedom) vs. 94.8% (DP-SGD WRN28-10 single model) without specifying these configurations. The more direct architectural match — SPS+ WRN28-10 (single) vs. DP-SGD WRN28-10 — shows a narrower 95.1% vs. 94.8% on CIFAR-10 at $\varepsilon=1$. The paper does not ablate how much of the gap is attributable to post-processing advantages (GSAM, ensembling, larger models) vs. the quality of the synthetic data itself. Reporting a non-private upper bound (fine-tuning original data with GSAM + ensembling) would help readers calibrate the privacy-accuracy trade-off.

- **The method is only validated on small-scale, low-resolution benchmarks.** The largest dataset is CIFAR-100 (50k images, 32×32); CAMELYON17 is binary classification at 64×64. The method involves $O(N)$ forward passes through a pretrained model and iterative optimization of synthetic images, so its scaling behavior to ImageNet-scale or higher-resolution tasks is an open question. The paper acknowledges computational cost as a limitation but defers details to the appendix.

- **Federated/continual learning results (Figure 5) lack error bars,** unlike the main CIFAR results in Table 1. This makes it difficult to assess whether the reported improvements over baselines are statistically significant.

- **The downstream fine-tuning protocol (learning rate, schedule, number of epochs, data augmentation) is underspecified in the main text,** which hinders reproducibility.

### Trivial

- The actual $d_{\text{tot}}$ values used in experiments are not reported (the paper gives the formula on line 120 but not the numeric instantiation), making it harder to gauge the SNR.

## Nice-to-Haves

- Reporting FID as a function of $M$ (number of clipping stages) would strengthen the link between visual quality and downstream accuracy.
- A DP-SGD baseline for the federated learning setting would make that comparison more complete.

## Removed Points

These points are flagged to be removed; treat them with caution:
- "Comparison with DP-SGD conflates post-processing freedom as a confound" — This IS the inherent advantage of data-based privacy. The paper is explicit about this distinction. Post-processing flexibility is a feature of SPS, not a weakness of the comparison.
- "CAMELYON17 uses different $\varepsilon$ values across baselines" — SPS at $\varepsilon=8$ outperforms baselines at $\varepsilon=10$, making the comparison conservative in SPS's favor.
- "Labels assumed non-private not explicitly stated" — Standard practice in DP literature; the reviewer acknowledges this.
- "Missing DP-SGD federated learning baseline" — The paper compares against FedLAP-DP and FedDM, which are the relevant baselines for that setting.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix Theorem 4.1** to use the noise multiplier $b_0$ (or $\sigma$) instead of $\delta$, and verify consistency between the formula, the definition of $b_0$ in eq. (4), and the standard RDP guarantee for the Gaussian mechanism.
2. **Provide a clearer explanation of GPC**: state whether the grouping is public/random and data-independent, and explain more concretely why pseudo-class matching works despite the lack of benefit for direct mean estimation.
3. **Add a non-private upper bound**: report accuracy after fine-tuning the original CIFAR-10/100 data with GSAM + ensembling under the same protocol, so readers can calibrate the full privacy cost.
4. **Report actual $d_{\text{tot}}$ values** used in the experiments.
5. **Add error bars** to federated and continual learning plots.
6. **Specify the downstream fine-tuning protocol** in detail in the main text or appendix.

## Score and Decision

The paper makes a genuine and well-supported contribution. The core idea is clever, the empirical results are strong, and the downstream experiments convincingly demonstrate the practical advantages of data-based privacy. The weaknesses are real but fixable: the most significant (GPC hand-waving) concerns explanation quality rather than method validity, and the notation issue in Theorem 4.1 is a straightforward correction. The strengths decisively outweigh the weaknesses.

**Score: 8 (Accept)** — a clearly positive paper with a meaningful advance over the state of the art and fixable presentation gaps.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>