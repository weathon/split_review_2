I have all the information I need from the earlier full read. Let me now write the final consolidated review.

## Summary

This paper studies language model pre-training under a fixed data budget with no compute constraints — a regime motivated by the observation that web text grows ~1×/year while pre-training compute grows ~4×/year. The authors show that standard data-constrained practices (epoching and parameter scaling) overfit. They demonstrate that tuning weight decay to be ~30× higher than the standard 0.1 value enables monotone loss scaling in parameter count, and propose evaluating recipes by their **asymptote** (limit of loss as N→∞ or K→∞) rather than at fixed compute budgets. They find that ensembling independently trained models achieves a lower asymptote than scaling a single model, and that composing both yields further gains. Distillation can compress most of the ensemble benefit into smaller models. The core empirical findings are supported by directly measured non-extrapolated results, but the headline quantitative claim (5.17× data efficiency) depends on nested power-law extrapolations with limited uncertainty quantification.

## Strengths

1. **Timely, well-motivated problem.** The data-vs-compute growth asymmetry (Villalobos et al., 2024: 1.03× vs 4× per year) is concrete and makes the research question genuinely important. This is not a hypothetical scenario; it is a trajectory the field is on.

2. **Weight decay finding is non-obvious and practically useful.** The observation that optimal weight decay is ~30× larger (3.2 vs 0.1) for data-constrained, over-parameterized models is the cleanest actionable result. Figure 3's table shows optimal weight decays monotonically increasing with parameter count (0.8 → 1.6 → 3.2 → 3.2), a finding practitioners can immediately adopt.

3. **The asymptote metric is a genuinely useful conceptual reframing.** For the data-constrained regime where compute is not the bottleneck, comparing losses at fixed compute budgets (Chinchilla-style) is the wrong lens. The asymptote (limit of loss as N→∞ or K→∞) is well-motivated as the way to compare algorithmic approaches under infinite compute.

4. **Core patterns are supported without relying on extrapolation.** The paper reports non-extrapolated results: the best 1.4B model is 2.09× more data-efficient than baseline, and the best 5-member ensemble of 1.4B models is 3.75× more data-efficient (Sections 5.1, 5.2). The core empirical patterns — regularization helps, ensembles help more — are supported by raw data, not just fitted asymptotes.

5. **Good methodology on benchmark hygiene.** The authors state they did not evaluate on downstream benchmarks until the end of the project, after selecting recipes based on validation loss (Section 7). This makes the 9% downstream improvement a genuine test of generalization rather than an artifact of benchmark chasing.

6. **Distillation results are practical.** Showing that an 8-ensemble can be distilled into an 8× smaller model retaining 83% of the loss improvement (Figure 8) addresses the practical concern that ensembles require huge inference budgets. The self-distillation result (same-size teacher and student outperforms the teacher) is also interesting and non-obvious given the model collapse literature.

## Weaknesses

### Fatal
None.

### Major

1. **The headline "5.17× data efficiency" rests on nested power-law extrapolations from minimal data points without uncertainty quantification.** The 5.17× figure is the output of a three-level chain of fits: (a) for each N and D, fit A/K^α + E to K ∈ {1,2,3,4,5} (5 points, 3 parameters); (b) take the E estimates and fit A'/N^α' + E' across N ∈ {150M, 300M, 600M, 1.4B} (4 points, 3 parameters); (c) repeat across D ∈ {200M, 400M, 800M, 1.6B} and fit A''/D^α'' + E'' (4 points, 3 parameters). Each fit has only 1–2 degrees of freedom. The paper reports that asymptotes vary by at most 0.02 across 3 seeds (Appendix I.1), but this captures only variance from initialization and data ordering — it does not capture uncertainty from the parametric form itself, nor does it propagate through the nested fitting procedure. The paper states "the data scaling laws are expected to be noisy" (Section 5.3) but provides no confidence intervals, bootstrap estimates, or predictive intervals for the 5.17× figure. **The core qualitative patterns are supported by non-extrapolated results (2.09×, 3.75×), so the conclusion that regularization+ensembling helps is robust. But the specific 5.17× number and the claim that "this improvement persists at higher token budgets" (abstract) are presented more definitively than the evidence supports.**

### Minor

2. **The "standard recipe" baseline conflates regularization with broader hyperparameter tuning.** The standard recipe (Figure 2) tunes learning rate and epoch count but fixes weight decay at 0.1. The regularized recipe (Figure 3) tunes weight decay, learning rate, and epoch count jointly. The improvement between them reflects *both* the value of higher weight decay and the value of tuning more hyperparameters. The weight decay table (Figure 3) shows optimal values far from 0.1 (0.8–3.2), so the specific finding is robust. However, the quantitative 2.29× data efficiency improvement could partially reflect under-tuning of the baseline rather than the specific weight decay choice alone.

3. **The ensemble-vs-parameter-scaling comparison mixes training and inference cost frames.** The paper's framing emphasizes "no compute constraints at training" (Section 1), but the comparison between ensembles and single models uses total parameter count (inference cost) as the x-axis (Figure 4). Ensembles require K× more training compute at the same total parameter count. The paper explicitly states this comparison choice (Section 4.1: "we will consider an ensemble's total parameter count as NK"), so there is no concealment, but the framing oscillates between "unlimited training compute" and "total parameter count as a cost proxy" in a way that weakens the clarity of the comparison.

4. **The joint scaling recipe (Section 4.3) uses heuristic hyperparameters rather than careful tuning.** The paper acknowledges: "For the inner limit, we cannot fully find locally optimal hyperparameters due to experimental constraints. Instead, we use the heuristic of taking the optimal regularized hyperparameters with 2× epochs and 0.5× weight decay" (Section 4.3). This creates an asymmetry with the single-model results where hyperparameters were carefully tuned via coordinate descent. The heuristic could advantage or disadvantage the joint recipe relative to a properly tuned alternative.

5. **The quality of unconditionally generated synthetic data for distillation is not characterized in the main text.** The distillation procedure (Section 6.1) samples from the teacher "unconditionally (i.e. with no prompt)" to generate D' synthetic tokens. For autoregressive LMs, unconditional sampling can produce degenerate or repetitive outputs. The paper states that model collapse is avoided by mixing D and D' tokens, but the quality, diversity, or distribution of the synthetic data is not described.

6. **The parameter range for scaling laws is narrow.** The four model sizes (150M–1.4B) span less than one order of magnitude, and the ensemble sizes span only K ∈ {1,2,3,4,5}. The power law exponent of ≈ 1.02 for parameter scaling is unusually high relative to typical scaling law exponents (Chinchilla reports 0.34) and could reflect overfitting the parametric form to a limited range.

7. **Downstream evaluation is limited to 3 accuracy-based benchmarks (PIQA, SciQ, ARC Easy).** While appropriate for the model scale and the paper is transparent about this, the coverage of capabilities is narrow. Benchmarking on reasoning or knowledge tasks is deferred.

### Trivial
None.

## Nice-to-Haves

- **Uncertainty quantification for power-law extrapolations.** Bootstrapped confidence intervals or predictive intervals on the 5.17× figure would substantially strengthen the headline claim. If the uncertainty is large (e.g., 95% interval spanning 2×–15×), reporting it honestly would still leave the qualitative conclusion intact.
- **Compute-matched training budget comparison** between ensembles and single models, in addition to the total-parameter-count comparison.
- **Characterization of the unconditionally generated synthetic data** used for distillation (diversity metrics, overlap with training data, sample quality).
- **More data points** — additional parameter counts (e.g., 3B) and ensemble sizes (K > 5) would substantially increase confidence in the power law fits.
- **Tuning weight decay in the standard recipe baseline** to confirm that 0.1 is genuinely a poor choice rather than an artifact of not tuning it.

## Removed Points

- Issue about "Without seeing Appendix F, it is unclear how this data compares..." — The parser strips appendices from all papers; they exist in the original submission. The underlying concern (main text lacking characterization of synthetic data quality) is retained as Minor weakness #5.
- Issue about "The paper only tries up to 128 epochs for 300M models; it is not shown that the same U-shaped curve holds for other parameter counts" — A reasonable completeness observation but does not threaten any core claim; the epoching experiment at 300M is sufficient to demonstrate the overfitting pattern.
- Generic speculation about whether the same-asymptote claim holds if the parametric form is wrong — This is inherent in any scaling law analysis and not a specific weakness.
- Criticism about benchmark coverage being "limited to reasoning or knowledge tasks" — The paper scopes this to the model scale and cites Thrush et al. for standard benchmarks at this scale.

## Novel Insights

The input review's strongest insight is the observation about nested extrapolation fragility: the 5.17× figure is not a measured result but the product of a three-level fitting chain where each stage has minimal degrees of freedom (4 data points, 3 parameters at the outer levels). The paper provides seed-level variance but not parametric-form uncertainty or propagated error. This reframes the paper's main quantitative claim from a settled finding to a suggestive estimate. A second insight is that the ensemble-vs-parameter-scaling comparison would benefit from a clean separation between the training-compute frame (where the paper claims unlimited resources) and the inference-cost frame (where the comparison is made). None beyond the paper's own contributions.

## Suggestions

- Add confidence intervals or bootstrap uncertainty estimates for the power-law fits, particularly around the 5.17× figure, or reframe the headline claims around the non-extrapolated results (2.09×, 3.75×) and present the extrapolations as suggestive predictions.
- Clearly separate the two resource frames (training compute vs. inference cost) in the ensemble comparison, or add a compute-matched training comparison as a supplementary analysis.
- Tune weight decay for the standard recipe baseline to isolate the effect of regularization from the effect of more extensive tuning.
- Provide basic characterization of the unconditionally generated distillation data in the main text.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>