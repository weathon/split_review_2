## Summary

AutoNFS proposes a neural feature selection method that uses Gumbel-Sigmoid relaxation to learn a binary mask over input features, trained end-to-end with a sparsity penalty that automatically determines how many features to retain. The method is evaluated on 11 OpenML benchmark datasets (with three corruption scenarios following Cherepanova et al., 2023) and 24 real-world metagenomic datasets, showing competitive or superior performance relative to 10 baseline methods while selecting far fewer features and exhibiting near-constant wall-clock time as dimensionality grows.

## Strengths

1. **Clean, practical architecture with automatic cardinality.** The masking-network + task-network design (Section 3) is clearly specified, and the automatic determination of feature count — removing a common user pain point — is a genuine practical advantage over most filter/wrapper/embedded methods that require the user to pre-specify the number of features.

2. **Striking empirical complexity result.** Figure 4 shows AutoNFS maintaining roughly constant wall-clock time (~10 seconds) as features grow from 10² to 10⁵, while filter methods (ANOVA, Mutual Information) increase by 1–2 orders of magnitude. The estimated complexity exponent α≈0.08 is well below linear. If this holds under scrutiny, it is the paper's strongest empirical contribution.

3. **Strong benchmark performance.** Following the Cherepanova et al. (2023) framework across 11 datasets and three corruption scenarios, AutoNFS achieves the best average rank in all scenarios (Figure 2). The metagenomic analysis (Table 2) shows that reducing features to 7.7% of original dimensionality *improves* average accuracy for both MLP (+0.7 pp) and Random Forest (+1.2 pp) downstream classifiers.

4. **Informative diagnostic analyses.** The misselection-error analysis (Figure 3a) and average-predictive-power analysis (Figure 3b) go beyond simple accuracy reporting, providing insight into what kinds of features the method selects and whether the selected set is minimal.

## Weaknesses

### Fatal
None.

### Major

1. **The most directly comparable differentiable FS methods (STG, HardConcrete) are absent from the experiments.** The paper situates itself in the "differentiable line" of FS (Section 2, line 36), citing Louizos et al. (2017) — HardConcrete gates for L₀ regularization — and Yamada et al. (2020b) — Stochastic Gates (STG). Both methods use the *same paradigm* as AutoNFS: a continuous relaxation of a binary selection variable, trained end-to-end with a sparsity penalty that automatically determines the number of features. Neither appears among the 10 baselines (Section 4.1). The closest differentiable competitor included is LassoNet, which uses a fundamentally different mechanism (hierarchical coupling of linear skip and deep features). Without STG and HardConcrete, the reader cannot tell whether the Gumbel-Sigmoid choice is the reason for the reported improvement, or whether any differentiable relaxation with a sparsity penalty would achieve similar results. This is an evidential gap that weakens the core contribution claim.

2. **The "nearly constant computational overhead" claim is not adequately explained.** The paper asserts this property repeatedly (abstract, Section 1, Section 4.3) and shows empirical evidence (Figure 4, α≈0.08), but the mechanism is not explained. The masking network f : ℝ^{D_e} → ℝ^D outputs D logits, costing at least O(D) flops; the task network receives a D-dimensional masked input, so its first layer also scales with D. The paper does not specify: (a) the architecture of the masking network (layer count, hidden dimensions), (b) whether the task network's first-layer size grows with D or uses a fixed-size projection, (c) what exactly is being timed in Figure 4a (total training time? per-epoch? inference?), or (d) whether the task network architecture is held constant across all D values or scales with D. Without this information, the near-constant result may be an artifact of a specific experimental configuration rather than a genuine property of the method.

### Minor

3. **Asymmetric comparison confounds selection quality with selection quantity.** The benchmark adds 50% corrupted features; baselines are configured to select exactly D features (the original dimensionality before corruption), while AutoNFS freely selects a much smaller subset (Table 1, RHS: often 40–60% of original D). The paper acknowledges this (line 204: "It is important to note that all baseline methods select the same number of features as were in the initial representation [before corruption], whereas our method automatically chooses a much smaller subset"). This asymmetry means baselines are *forced* to keep potentially irrelevant features to meet the D-feature budget, while AutoNFS can discard them. The performance gap could partly reflect the difference in selected-set size rather than selection quality. A controlled comparison — either letting baselines select their optimal cardinality or restricting AutoNFS to select exactly D features — would strengthen the attribution.

4. **Individual dataset failures are masked by averaging in the metagenomic analysis.** Table 2 shows that on several datasets, AutoNFS substantially degrades MLP performance (KeohaneDM_2020: 0.469→0.344; YuJ_2015: 0.653→0.417; ThomasAM_2018a: 0.733→0.567). The paper's claim that AutoNFS "maintains predictive performance" (line 216) is true on average (0.588→0.596) but does not reflect the variance or worst-case behavior. A discussion of failure cases would give users a more complete picture.

5. **"Deep Lasso" — a strong baseline — is not defined or cited in the main text.** Deep Lasso achieves the second-best average rank (3.8 in the Corrupted scenario, Figure 2) and is the closest competitor to AutoNFS. Yet the method is never defined, cited, or discussed in the related work or experimental setup sections. The paper references Appendix C for experimental details, and parts of the references are truncated in the version available for review, so the definition and citation may exist in the complete submission.

### Trivial

6. **Naming inconsistency.** The method is called "AutoNFS" throughout the paper, but Figure 4's captions and alt text refer to it as "GFS-NetWork," which is confusing and suggests an earlier naming convention was not fully updated.

## Nice-to-Haves

- An ablation replacing Gumbel-Sigmoid with a standard sigmoid (no Gumbel noise) would isolate whether the noise injection drives the improvement.
- A sensitivity analysis for λ (beyond the reference to Appendix F) would help readers understand the sparsity-accuracy trade-off.
- Adding confidence intervals or significance tests (e.g., Friedman test, Wilcoxon signed-rank) for the ranking analysis in Figure 2 would strengthen the statistical grounding.

## Removed Points

- *"The paper does not specify total epochs E or hyperparameter values"* — These details likely reside in the stripped appendix (Appendix C for experimental setup, which the paper references). Removed per hard rule on missing appendix content.
- *"Missing architecture details of masking network f"* — Overlaps with Major Issue 2 above; retained there in the context of explaining the complexity claim, but removed as a standalone reproducibility complaint.
- *Criticisms framed as generic concerns without concrete paper anchor* (e.g., "could the metric be measuring a proxy?") — Removed as speculative noise.
- *"The appendix may specify X but…" framing* — Removed as speculation about stripped content.
- *Generic strength about "addressing an important problem"* — Removed as not specific to this paper's contribution.

## Novel Insights

The reviews surface that the paper's central tension is between its clear practical contribution (automatic cardinality determination + favorable scaling) and the absence of the most directly comparable differentiable baselines. The Gumbel-Sigmoid mechanism is well-motivated and the empirical results on the Cherepanova benchmark are strong, but without STG/HardConcrete comparisons the paper cannot demonstrate that the *specific relaxation* (as opposed to the general differentiable-relaxation+sparsity-penalty paradigm) is responsible for the improvements. The complexity result, if properly explained, could be the paper's most distinctive contribution — a genuinely sub-linear scaling method in FS is notable — but the current lack of mechanistic explanation is a significant gap.

## Suggestions

1. Add STG (Yamada et al., 2020b) and HardConcrete (Louizos et al., 2017) as baselines in the main experiments. If computational budget is a concern, prioritize the benchmark datasets and at minimum add them to the metagenomic analysis.
2. Provide a theoretical or architectural explanation for the near-constant complexity result. Specify the masking network architecture used in the timing experiments and clarify what is being measured (total training time? per-epoch?).
3. Run a controlled experiment where baselines are given the same feature budget that AutoNFS selects, to disentangle selection quality from selection quantity.
4. Include a brief discussion of variance and worst-case behavior for the metagenomic results.
5. Replace "GFS-NetWork" with "AutoNFS" in all figures for consistency, and either cite or define "Deep Lasso" in the main text.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>