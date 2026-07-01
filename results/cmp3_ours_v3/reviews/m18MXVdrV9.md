## Summary

This paper introduces INFO-SEDD, a method for estimating mutual information (MI) and entropy on high-dimensional discrete data using discrete diffusion models (Continuous Time Markov Chains). The core theoretical contribution links KL divergence to CTMC score functions via Dynkin's formula, enabling MI estimation without embedding discrete data into a continuous space. An absorbing-state trick allows computing marginal scores from a single joint model. Experiments on synthetic benchmarks, text summarization, and genomics show strong performance compared to embedding-based competitors.

## Strengths

1. **Novel theoretical derivation linking CTMCs to KL estimation.** The derivation (Section 2) connecting KL divergence to CTMC score functions via Dynkin's formula (Equation 4) is mathematically sound and non-trivial. This is a genuinely new connection that prior work on discrete diffusion (Lou et al., 2024) did not draw, and it cleanly bridges generative modeling and information-theoretic estimation.

2. **Practical absorbing-state trick for marginal scores.** Equation (6) shows that with absorbing-state CTMCs, marginal score ratios can be read off from a *single* joint model by clamping irrelevant variables to the absorbing state. This reduces the training cost from separate models for the joint and each marginal to one training run — a practically valuable insight that distinguishes INFO-SEDD from a naive implementation.

3. **Strong synthetic results demonstrating clear advantage.** Table 1 is convincing: across MI values from 10 to 50 (with D proportionally increasing), INFO-SEDD produces estimates within ~2% of true MI for MI ≤ 40 and within ~4.5% at MI=50, with small standard deviations (0.12–1.18). Competitors degrade dramatically — GAN-DIME collapses from 30.74 (MI=30) to 17.27 (MI=50) — directly demonstrating the method's advertised advantage in high-dimensional, high-MI settings.

4. **Clean genomics consistency test.** Figure 4 shows INFO-SEDD-C closely tracking the classifier-based reference in the HUMAN vs. WORM experiment, starting near 0 at ρ=0 and increasing linearly — a much cleaner result than the text consistency test, suggesting the method can be well-calibrated in lower-dimensional settings.

## Weaknesses

### Major

1. **Unaddressed systematic bias in the text consistency test undermines the "closely matching" claim.** At ρ=0 in Figure 1, where pairings are random and true MI should be ~0 by construction, INFO-SEDD estimates ~100 nats. The paper's own empirical reference (256ρ to 303ρ nats) passes through 0 at ρ=0, so INFO-SEDD's ~100-nat floor represents a substantial systematic bias — comparable in magnitude to the signal being measured (the increase from ρ=0 to ρ=1 is roughly 100–200 nats). The paper acknowledges the bias only in passing ("INFO-SEDD-C obtains MI estimates closer to zero than the joint variant, when ρ = 0.0") without analyzing its causes (inherent estimator bias vs. imperfect score model training) or discussing implications for absolute MI accuracy. The conclusion that INFO-SEDD "closely matches the empirical derivation" is overstated given this offset. The method may still be useful for relative comparisons, but the paper should qualify its claims about absolute accuracy.

### Minor

2. **No computational cost comparison despite higher per-step cost.** The abstract calls INFO-SEDD "lightweight and scalable," but the paper provides no wall-clock training time, GPU hours, or per-step cost comparison. INFO-SEDD trains a diffusion model with score matching across multiple timesteps per sample, while competitors (MINE, NWJ, SMILE, F-DIME) train a single critic — a substantial difference in training cost. The paper states all methods use the same backbone architecture with similar parameter counts and notes faster convergence in epochs (Appendix C.1.3), which partially addresses this, but the per-step cost remains a significant gap for practitioners needing to calibrate the accuracy-vs-cost trade-off.

3. **Model selection correlations lack statistical quantification.** Table 2 reports Pearson r and Kendall's τ for 15 models without p-values or confidence intervals. With N=15, the 95% CI for r=0.74 spans roughly 0.36 to 0.91, and weaker correlations (e.g., INFO-SEDD-C vs. coherence: r=0.209) may not be significant. The paper also does not test whether differences between estimators' correlations are significant. The qualitative patterns (MI correlates most with consistency) are sensible, but stronger statistical substantiation would substantially strengthen this analysis.

4. **No classical discrete MI estimators as baselines.** The paper motivates its approach by arguing that classical discrete estimators (plug-in, Miller-Madow, NSB) degrade with dimensionality, but never includes any of them as baselines — not even in synthetic experiments at moderate D where they would be applicable. While this omission does not undermine the core comparison against embedding-trick methods (which INFO-SEDD clearly outperforms), it limits the paper's ability to characterize where INFO-SEDD sits in the broader MI estimation landscape.

### Trivial

5. **"Empirical MI estimate" in Figure 1 is not explicitly defined.** The figure legend shows both "Empirical MI estimate (grey)" and "256-ρ nats to 303-ρ nats (black)" as separate entries, but the paper only describes the latter's derivation. The grey line's provenance is unclear from the main text.

6. **No sensitivity analysis for the time horizon T.** Equation (7) shows truncation bias depends on T through p_T(∅^D), but the paper does not report what T was used or study sensitivity to this hyperparameter.

## Nice-to-Haves

- Add p-values or bootstrapped confidence intervals to Table 2 correlations.
- Include at least one classical discrete MI estimator (e.g., Miller-Madow) as a baseline in synthetic experiments at moderate dimensionality.
- Report wall-clock training time or GPU-hours for all methods.
- Study sensitivity to time horizon T.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The Ising model entropy experiment is only in Appendix D"** — removed because the appendix exists in the original submission and the main text references it (Section 4: "In Appendix D, we provide additional results").
- **"No comparison against prior diffusion-based MI work"** — removed because the paper extensively cites MINDE (Franzese et al., 2023a) and the relevant continuous-domain diffusion MI literature; the paper's contribution is specifically about the *discrete* setting which is a different technical challenge.
- **"Missing proofs in appendix"** — removed per instructions (appendix exists in original).
- **"The method is not novel because score-MI connections exist"** — removed because the specific connection via Dynkin's formula for discrete CTMCs is genuinely new; prior continuous-domain connections (Girsanov theorem) apply to a different technical setting.
- Generic speculation about confounders or evaluation rigor without specific anchors — removed.
- Formatting and style nitpicks — removed.

## Novel Insights

The harsh critic observation about the ρ=0 bias being structural rather than anecdotal is important: the ~100-nat floor in the text consistency test is approximately consistent across the two INFO-SEDD variants and appears only in the high-dimensional text experiment, not in the lower-dimensional genomics experiment (Figure 4). This suggests the bias may scale with data dimensionality or sequence length rather than being inherent to the estimator — but the paper does not investigate this. If the bias is proportional to some property of the data (e.g., sequence length × log |χ|), a baseline correction might be feasible, which would strengthen the method's practical utility.

## Suggestions

1. **Directly investigate and explain the ρ=0 bias in the text consistency test.** Is it inherent to the estimator (perhaps related to the omitted 𝔼[log(p₀/q₀)(X₀)] term in Equation 4) or an artifact of imperfect score model training? If inherent, can it be corrected via baseline subtraction or does it affect only the constant offset (leaving MI comparisons valid)? This single issue most undermines the claim of absolute MI accuracy.

2. **Add a computational cost analysis** (wall-clock time or GPU-hours) comparing INFO-SEDD to competitors to support the "lightweight" claim in the abstract.

3. **Add confidence intervals or p-values** to the correlations in Table 2.

4. **Clarify what the "Empirical MI estimate"** in Figure 1 represents.

## Score and Decision

**Calibration anchors (all retrieved across rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 0kWd8SJq8d (MINDE, diffusion-based MI) | 6.50 | R1 | Directly comparable diffusion-based MI estimator for continuous data. Accepted [6,6,6,8] despite similar missing cost analysis. Current paper tackles harder discrete setting but has ρ=0 bias. |
| vgQmK5HHfz (Normalizing Flows DoE) | 4.83 | R1 | MI estimation via flows. Rejected due to limited novelty. Current paper is substantially stronger theoretically and experimentally. |
| spDUv05cEq (Flow-based Var. MI) | 6.00 | R1 | MI estimation with flows. Accepted [5,6,5,8]. Similar profile: strong theory, synthetic experiments, but limited real-world validation. |
| peNgxpbdxB (Scalable Discrete Diffusion) | 6.00 | R2 | Discrete diffusion paper. Accepted [6,6,6]. Similar discrete-domain contribution with comparable weakness (insufficient challenging experiments). |
| tQyh0gnfqW (DDSBM, discrete diffusion bridges) | 5.67 | R2 | Discrete diffusion + CTMCs. Accepted [8,3,6]. Similar theoretical contribution in discrete domain with some experimental gaps. |
| KC2MViQASx (f-Divergence MI) | 5.60 | R1 | MI estimation via data derangements. Rejected. Less novel than current paper. |

**Round 1 bracket:** 5.5 – 6.5  
**Round 2 narrowing:** The paper's theoretical contribution, strong synthetic results, and real-world applications place it alongside the 6.0 anchors (peNgxpbdxB, spDUv05cEq). The ρ=0 bias is a real concern but does not invalidate the core contribution, as the synthetic results (Table 1) are clean and the genomics consistency test (Figure 4) is well-behaved. The weaknesses are addressable and comparable in severity to those in accepted papers in this range.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>