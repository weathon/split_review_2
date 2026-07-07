Now I have the calibration data. Let me finalize my analysis and write the review.

**Bracket analysis:** The most directly comparable anchor is the MINDE paper (0kWd8SJq8d.md, avg 6.50), which proposes a diffusion-based MI estimator for continuous data. INFO-SEDD is its discrete-data counterpart. The MINDE paper had severe weaknesses (-9.34 for unclear organization, -5.12 for missing error bars) that INFO-SEDD does not share. INFO-SEDD's weaknesses are uniformly minor. The discrete diffusion convergence paper (pq1WUegkza.md, avg 7.00) is a theoretical paper with stronger theoretical contributions but no empirical validation. INFO-SEDD sits between these two — stronger empirically than the theory paper, stronger organizationally than MINDE.

**Initial bracket: 5.5 – 7.5.**

Now let me finalize the review. I need to keep the filter discipline in mind:

1. The backbone asymmetry weakness had weight +1.80 (positive), meaning the scoring model doesn't see it as a real weakness. Let me check if I should keep it. Per the instructions: "If a weakness reads like an area-of-concern sweep... REMOVE it." And: "For every retained weakness, you must be able to point to a specific sentence, equation, figure, or table in the paper that the weakness applies to." The backbone concern does apply to specific text (Section 4.2 about using MDLM-SMALL backbone with embedding layers for competitors). But the model gave it +1.80, which is positive. Let me re-examine: The model might think this criticism is actually not valid or even helps the paper. Given that the synthetic experiments (the strongest evidence) train the backbone from scratch, and for text experiments using the same backbone for all methods is standard practice, I think this criticism is weak. I'll move it to removed points.

2. The variance not reported weakness had weight +0.21 (barely positive). The model slightly disagrees it's a weakness. This is a common request but not standard. I'll keep it as trivial.

3. The motif discovery weakness had weight -4.94. This is valid - the experiment is qualitative without baselines.

Let me also reconsider which strengths to keep. The strength "genomics consistency test uses a classifier-based reference" had weight +2.62 - moderate but lower than others. I'll keep it as it's specific and evidence-backed.

Let me now write the final review.Now let me write the final consolidated review.

## Summary

INFO-SEDD introduces a method for estimating KL divergences and mutual information (MI) for high-dimensional discrete data using score functions from Continuous Time Markov Chains (CTMCs) — the same score functions used by discrete diffusion models. The core theoretical contribution derives a tractable KL estimator via Dynkin's formula (Equations 2–5), and an absorbing-state construction (Equation 6) that allows a single trained model to produce both joint and marginal scores. Synthetic experiments (Table 1) show INFO-SEDD remains accurate (bias ~2 nats at MI=50, D=50) where all variational competitors collapse. Real-world applications in text summarization and genomics demonstrate practical utility, including a novel motif-discovery task. An error bound (Equation 7) decomposes estimation error into a score-approximation term and an exponentially decaying truncation bias.

## Strengths

- **[Theoretical contribution]** The derivation from CTMCs through Dynkin's formula to a tractable KL estimator (Equations 2–5) is coherent and non-trivial. Deriving a KL divergence estimator via two CTMCs with shared generators but different initial conditions and applying Dynkin's lemma to obtain a Monte Carlo-tractable expression represents a genuine technical contribution over the existing SEDD framework. (Section 2)

- **[Theoretical contribution]** The absorbing-state trick (Equation 6) that allows a single score model to produce both joint and marginal scores is clean and well-justified (proof in Appendix A.3). This is practically important because it avoids training separate models for the joint and marginal distributions. (Section 3)

- **[Theoretical contribution]** The error bound (Equation 7) decomposing the error into a score-approximation term (scaling with D|χ| and score errors) and a truncation bias (decaying exponentially in T) provides useful structural insight into the method's behavior, even if the constants are not fully quantified. (Section 3)

- **[Strong empirical evidence]** The synthetic benchmark (Table 1) systematically varies both MI (10–50) and dimensionality (10–50), and INFO-SEDD's estimates are consistently accurate (bias under ~2 nats even at MI=50, D=50) while competitors degrade severely. GAN-DIME, the best competitor, collapses after D=30. Standard deviations over 10 seeds are reported, demonstrating robustness. (Section 4.1, Table 1)

- **[Empirical evidence]** The applications are diverse and demonstrate practical utility beyond reporting MI numbers. The motif discovery experiment (Figure 5) is compelling as a qualitative demonstration — the MI peak aligns with a known biological location (TATA-box at positions -39 to -26) without any supervised training for that task. (Section 4.3)

- **[Empirical evidence]** The genomics consistency test (Figure 4) uses a classifier-based reference that is more principled than the text reference, directly estimating H(Y|X) from classification accuracy. INFO-SEDD-C closely matches this reference, adding credibility to the method's real-world accuracy. (Section 4.3)

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The text consistency test reference lines are approximate and may overestimate true MI.** The reference lines (256·ρ nats and 303·ρ nats) multiply character-level entropy rates of *general English text* by the average summary length. The paper calls them an "order-of-magnitude estimate," which is appropriate, but summaries are shorter, more structured, and drawn from a narrower distribution than general text, so the reference lines likely overestimate the true MI. The paper's conclusion that INFO-SEDD's agreement with these references validates its accuracy is somewhat circular — it shows INFO-SEDD agrees with the paper's *own reference construction*, not that INFO-SEDD is objectively correct. Competitors' low estimates are indeed explained by known limitations (McAllester and Stratos, 2020), but the paper overstates the validation this test provides. (Section 4.2, Figure 1)

2. **Overstatements in positioning and no limitations section.** The abstract and conclusion describe INFO-SEDD as providing "seamless integration with pretrained models" and being "unique." However, Section 4.2 notes the training strategy was "slightly modified" from Sahoo et al. (2024) and the CADUCEUS model is fine-tuned — these are reasonable steps but "seamless" overstates the required effort. Calling the method "unique" (Conclusion) — even hedged with "to the best of our knowledge" — is an overstatement given that MINDE (Franzese et al., 2023a) is a closely related continuous-space diffusion-based MI estimator. The paper also lacks a Limitations section, where it could discuss reliance on pretrained discrete diffusion models (which may not exist for every domain), sensitivity to the choice of T and the absorbing-state schedule, and settings where INFO-SEDD might underperform due to poor score approximation. (Abstract, Section 5)

3. **No computational cost comparison.** The abstract claims the method is "lightweight and scalable," but the paper does not compare runtime, GPU hours, or FLOPs between INFO-SEDD and competitors. For the synthetic experiments, training was done for 10^5 steps at batch size 1024 for all methods, but actual wall-clock time is not reported. For text and genomics experiments, INFO-SEDD uses full discrete diffusion models (MDLM-SMALL, CADUCEUS) as backbones — these are expensive to train. A practitioner needs to know whether INFO-SEDD trades compute for accuracy, and if so, how much. (Section 4.1)

4. **Model selection correlation analysis uses small sample size without uncertainty quantification.** Table 2 reports Pearson correlations based on only 15 data points (summarization models with human judgments). With N=15, the gap between INFO-SEDD-C's Pearson r=0.740 and Kendall's τ=0.505 suggests the correlation may be driven by a small number of high-leverage points. The paper does not report p-values, confidence intervals, or show individual data distributions beyond GP regression plots. (Section 4.2, Table 2)

5. **The motif discovery experiment is qualitative and lacks baseline comparison.** Showing that MI peaks near the known TATA-box (Figure 5) is a reasonable sanity check but not a demonstration of superiority over alternative approaches. The paper claims other MI estimators would need different training runs for each window while INFO-SEDD natively supports this — a genuine advantage — but this claim is stated without experimental support showing that other methods actually fail or are impractical. (Section 4.3)

6. **Variance of the estimator is not reported for real-world experiments.** For synthetic experiments, standard deviations over 10 seeds are reported (Table 1). But for the text consistency test (Figure 1) and genomics experiments (Figures 4–5), only point estimates are shown. Given that the estimator involves Monte Carlo sampling over time steps and forward processes, its variance is nontrivial and should be characterized to understand estimator reliability. (Section 4.2, Section 4.3)

### Trivial
- No limitations section — easy to add in camera-ready.

## Nice-to-Have
- Provide a controlled experiment isolating whether the performance advantage in text experiments comes from avoiding the "embedding trick" specifically or from using a discrete diffusion backbone whose pretraining objective (DWDSE) natively serves INFO-SEDD's score needs. This could be addressed by comparing against competitors that use the same backbone but with a different output head.
- Quantify the motif discovery result with a baseline comparison (e.g., a logistic regression coefficient profile or a simple mutual information baseline) to demonstrate a practical advantage.
- Add p-values or confidence intervals to the model selection correlation analysis (Table 2).

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Backbone asymmetry as a critical issue:** The harsh critic claimed the text comparison is fundamentally unfair because INFO-SEDD's backbone (MDLM-SMALL) was pretrained with DWDSE while competitors must add embedding layers. However, (a) for synthetic experiments — the strongest evidence — the backbone is trained from scratch, eliminating any pretraining asymmetry, and (b) for text experiments, using the same pretrained backbone architecture for all methods is the standard and fairest feasible approach. The paper explicitly notes competitors add "an embedding look-up table" to project tokens, which is a thin adaptation. The remaining asymmetry concern is minor at most and applies only to the text experiments, not the paper's core claims.
- **Presentation nitpicks** about Equation (4)'s implicit assumption and Equation (5)'s notation: these are stylistic preferences that do not affect the paper's correctness or clarity.
- **"No analysis of failure modes":** a generic expectation not standard for every paper; removed.
- **Missing appendix content, formatting artifacts, and related work gaps:** removed per hard rules.

## Novel Insights

None beyond the paper's own contributions. The reviews identify specific areas where the paper's claims modestly outpace the evidence (consistency test reference lines, "unique" in the conclusion) and where additional analysis would strengthen the contribution (computational cost, variance reporting), but these are standard critical observations.

## Suggestions

1. Add a Limitations section discussing: reliance on pretrained discrete diffusion models (which may not exist for every domain), computational cost of discrete diffusion training, sensitivity to T and the absorbing-state schedule, and conditions where score approximation error (εₚ, ε_q from Eq. 7) could cause inaccurate estimates.
2. Provide a runtime/GPU-hours comparison table for the synthetic experiments to ground or qualify the "lightweight" claim in the abstract.
3. For the text consistency test, either add a more principled reference (e.g., a classifier-based lower bound, similar to the genomics experiment) or explicitly state the limitations of the entropy-rate-based reference lines.
4. Add confidence intervals or bootstrap-based uncertainty estimates to the 15-point model selection correlations.
5. Tone down "unique" and "seamless" — they are not needed to convey the contributions, which stand on their own merits.

## Score and Decision

**Calibration anchors:**
| Paper | Avg Score | Round | Itemized? | Comparison |
|-------|-----------|-------|-----------|------------|
| 0kWd8SJq8d.md (MINDE) | 6.50 | R1 | Yes | Continuous-space diffusion MI estimator; structurally similar but INFO-SEDD addresses discrete data — a genuine gap. INFO-SEDD has fewer severe weaknesses (no -9.34 organization issues, no -5.12 missing error bars) but similar missing runtime analysis. |
| pq1WUegkza.md (Discrete Diff. Conv.) | 7.00 | R1 | Yes | Pure theory paper with no experiments; stronger theoretical contributions but no empirical validation. INFO-SEDD has weaker theory but stronger empirical support. |
| WR9M6AA4LT.md (Fit Like You Sample) | 6.00 | R1 | Yes | Theoretical score matching paper; less directly comparable. INFO-SEDD has stronger empirical evidence. |

The weighted-item comparison with MINDE (the closest anchor) shows INFO-SEDD shares MINDE's strongest positive items (important problem, strong synthetic results, clear theoretical derivation) but also shares some of its negative items (missing runtime comparison). INFO-SEDD avoids MINDE's most severe weaknesses (unclear organization, missing error bars on benchmarks) while having its own set of minor weaknesses (overstated claims, approximate consistency references, small-sample correlation analysis). Overall, INFO-SEDD is comparable to or slightly above MINDE in quality due to cleaner organization and addressing a genuine gap, but below the pure theory paper (7.00) which had no empirical validation concerns. **Final score: 6.5.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>