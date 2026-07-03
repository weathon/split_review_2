## Summary

INFO-SEDD introduces a method for estimating mutual information (MI) and KL divergence on high-dimensional discrete data using Continuous Time Markov Chains (CTMCs). The core idea is to apply Dynkin's formula to express KL divergence in terms of score functions learned by a discrete diffusion model, and to use an absorbing-state transition matrix so that a single score model trained on the joint distribution suffices for computing marginal scores. The method is evaluated on synthetic benchmarks (accurate up to MI=50/D=50 where competitors fail), text summarization (consistency tests and model selection), and genomics (motif discovery).

## Strengths

- **Strong synthetic benchmark results (Table 1):** INFO-SEDD achieves estimates within ~4.5% of ground truth at MI=50/D=50 (47.77±1.18 vs. true 50), while the best competitor (MINDE) reports 32.60±3.93 (34.8% error) and MINE reports 7.21±1.14 (85.6% error). The gap widens at higher MI, directly supporting the claim that the method handles regimes where prior estimators fail. Standard deviations are reported over 10 seeds, demonstrating consistency.

- **Single-model marginal score computation via absorbing-state CTMC (Equation 6):** The paper demonstrates that by choosing an absorbing-state transition matrix, the ratio of joint probabilities with masked components equals the ratio of marginal probabilities. This means a single score model trained on the joint distribution computes marginal scores, avoiding separate models for each distribution — a non-obvious theoretical property and a concrete differentiator from prior approaches that require per-distribution models.

- **Rigorous error bound with consistency guarantee (Equation 7):** The error is formally decomposed into estimation error (linear in score approximation error, scaling with \(\bar{\sigma}(T) D |\chi|\)) and truncation bias (vanishes exponentially as the absorbing-state probability approaches 1). This provides a principled characterization that most variational MI estimators lack.

- **Native subset-MI demonstrated on TATA-box discovery (Figure 5):** INFO-SEDD computes MI between sliding windows of DNA sequences and promoter labels from a single trained model, correctly localizing the TATA-BOX motif at the biologically known position (-39 to -26 relative to TSS). As the paper notes, other MI estimators would need different training runs for each window — a concrete practical advantage.

- **Seamless integration with pretrained discrete diffusion backbones:** The method works with MDLM-SMALL (text) and CADUCEUS (genomics) with minimal architectural changes and no ad-hoc embedding look-up tables, unlike competitors that require learning projections into continuous embedding spaces.

## Weaknesses

### Fatal

None.

### Major

- **No discrete-native baseline included.** The paper cites Pinchas et al. (2024) as an existing discrete estimator and mentions non-parametric methods (Kraskov et al., 2004; Gao et al., 2015), but none are included as baselines. All eight competitors are continuous-data methods applied via the "embedding trick." This means the empirical comparison conflates two distinctions (discrete-native vs. embedding-based, and diffusion-based vs. variational) and cannot substantiate the claim of outperforming other discrete-native approaches. Adding even a simple plug-in estimator or the method of Pinchas et al. (2024) would strengthen the paper's central empirical claim. Without this, the contribution appears narrower than claimed — the paper primarily shows that a discrete diffusion method beats continuous methods applied to discrete data, not that it beats methods designed for discrete data.

### Minor

- **Equation (2) exposition is confusing and potentially misleading as presented.** The paper states \(\text{KL}[p_0\|q_0] = \mathbb{E}[\log(p_0/q_0)(X_T)] = \mathbb{E}[\log(p_T/q_T)(X_T)]\) without explaining the relationship between these quantities. A reader trained in information theory will notice that \(\mathbb{E}_{X_T\sim p_T}[\log(p_0/q_0)(X_T)] \neq \text{KL}[p_0\|q_0]\) generally, and that \(\text{KL}[p_T\|q_T]\) (which is what the third expression evaluates) is not equal to \(\text{KL}[p_0\|q_0]\) — in fact it decays to zero as \(T\to\infty\). The full derivation (appendix) likely resolves this via Dynkin's integral capturing the gap between \(\text{KL}[p_0\|q_0]\) and \(\text{KL}[p_T\|q_T]\), but the main text does not communicate this correctly. The remark "we omit the term \(\mathbb{E}[\log(p_0/q_0)(X_0)]\), as both \(p_0\) and \(q_0\) converge to \(\pi\)" (line 59) hints at awareness of the boundary issue but does not clarify the derivation. This needs rewriting to avoid readers concluding the math is simply wrong.

- **INFO-SEDD-J estimate at ρ=0 in the text experiment is not adequately explained.** At ρ=0 (randomly paired text and summary), true MI should be near 0. INFO-SEDD-J reports ~100 nats while INFO-SEDD-C reports ~1 nat. The paper notes this gap (line 144) but does not explain which variant is more trustworthy or why the joint variant's estimate is so far from the expected value. This raises questions about the joint variant's calibration in low-MI regimes.

- **Low Kendall's Tau values are not discussed despite high Pearson correlations.** Table 2 shows INFO-SEDD-C achieves Pearson=0.740 for consistency but Kendall's Tau=0.505, and Pearson=0.679 for fluency but Kendall's Tau=0.134. This large gap between linear and rank correlation is unaddressed, and suggests the linear relationship may be driven by outliers or a non-monotonic pattern. The paper extensively discusses Pearson correlations but ignores the rank-correlation discrepancy.

- **TATA-BOX experiment is qualitative only.** Figure 5 shows MI peaking in the biologically expected region, but no quantitative comparison against a baseline (e.g., consensus sequence scanning, position-weight matrix scanning) is provided. While this is a valid demonstration of a practical application, it does not rigorously validate the method's accuracy for motif discovery.

- **Computational cost not reported.** The paper claims INFO-SEDD is "lightweight" (abstract) but provides no training time, GPU-hour, or resource comparisons against baselines. This omission matters for practitioners considering adoption.

### Trivial

None.

## Nice-to-Haves

- Systematic comparison of INFO-SEDD-J vs. INFO-SEDD-C across all experimental settings to help practitioners choose between variants.
- Confidence intervals or significance tests for the correlation values in Table 2.

## Removed Points

- **"Ground truth reference in text consistency test is unreliable":** Removed because the paper explicitly calls it an "order-of-magnitude estimate" (line 130) and does not present it as precise ground truth. The reference is used as a rough sanity check.
- **"Synthetic data generation not described in main text":** Removed because this content is in Appendix C.1, which exists in the original submission (the parser strips appendices from all papers per system instructions).
- **"Sample complexity concern":** Removed because sample sizes are reported (10^5 for synthetic training, 10^5 for genomics consistency test); the claim about 10^3 samples is from a specific ablation study, not the main result.
- **"Missing related work citations":** Removed per policy; the reviewer cannot verify existence of missing references without external sources.

## Novel Insights

The Harsh Critic's observation about the Pearson/Kendall's Tau discrepancy in Table 2 is a genuinely useful diagnostic that the paper's own discussion overlooks. If Pearson is high but Kendall's Tau is low, the relationship may be driven by a few outliers — this is testable and worth investigating. The Critic also correctly notes that the two INFO-SEDD variants behave very differently at ρ=0 (~100 nats vs. ~1 nat), and the paper's explanation ("optimization is harder for the joint variant") is too vague to be satisfying.

The Strength Finder's insight that the absorbing-state trick (Equation 6) is a non-obvious theoretical property that cleanly bridges discrete diffusion and marginal score computation is well-taken. This is a genuinely clever design choice and deserves more emphasis as a core contribution.

## Suggestions

1. **Add at least one discrete-native baseline** (e.g., plug-in estimator, Pinchas et al. 2024) to Table 1. Even if it fails on high-dimensional settings, it would substantiate the claim that discrete-native methods struggle at high dimensions.
2. **Rewrite Equation (2) and surrounding text** to explicitly state the identity being used, including the boundary term that vanishes as \(T\to\infty\), and clearly explain how Dynkin's formula bridges the gap.
3. **Address the INFO-SEDD-J vs. INFO-SEDD-C discrepancy at ρ=0** — provide an explanation or ablation study showing the source of the ~100 nat estimate.
4. **Discuss the low Kendall's Tau values** in Section 4.2 and note whether the high Pearson correlations are robust to outlier removal.
5. **Report training time/compute cost** to validate the "lightweight" claim.

## Score and Decision

**Calibration:** The calibration tool was unavailable due to a path issue. Scores are therefore calibrated against my knowledge of the ICLR reviewing standards and the paper's own content.

**Score reasoning:** The paper introduces a genuinely novel method that bridges discrete diffusion models and information estimation — this is a timely and well-motivated contribution. Table 1 provides compelling evidence that the method works in controlled settings where all eight competitors fail badly. The error bound and absorbing-state trick are substantive theoretical contributions. However, the paper is weakened by (1) the absence of any discrete-native baseline, which narrows the empirical claim's scope, (2) confusing mathematical exposition in Equation (2) that undermines reader trust in the derivation, and (3) several unexplained empirical patterns (INFO-SEDD-J at ρ=0, low Kendall's Tau). These are addressable weaknesses, not fatal flaws. The paper sits in the borderline-accept range: the core contribution is solid and the synthetic evidence is strong, but the presentation and evaluation completeness need improvement.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>