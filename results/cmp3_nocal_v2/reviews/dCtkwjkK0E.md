Now I'll produce the final consolidated review.

## Summary

This paper proposes active learning query strategies for conditional flow matching generative models applied to shape design. Using a piecewise-linear neural network analysis framework on closed-form flow matching, the authors derive the insight that adding data with similar labels improves generative diversity while data with distinct labels improves accuracy. Based on this, they propose two query strategies (Q_D for diversity, Q_A for accuracy) and a hybrid strategy, evaluated on synthetic and three real-world aerodynamic shape datasets.

## Strengths

1. **Novel problem framing.** Applying active learning *to* generative models (rather than using generative models *for* active learning) is a genuinely underexplored direction. The paper correctly identifies this gap (Section 1, paragraph 2), and the application to conditional flow matching for shape design is well-motivated by the high cost of numerical simulation labels.

2. **Clean conceptual insight from theoretical analysis.** The derivation that same-label data contributes to diversity while different-label data contributes to accuracy (Sections 2.3–2.4) is internally coherent for the closed-form piecewise-linear flow matching model and provides an intuitive guiding principle. The formalization through Eq3 (convex combinations of training data) and Eq5 (error bound via max label distance in a subregion) is clearly presented.

3. **Ablation study of Q_D (Section 3.3, Fig9).** The three-term decomposition is tested, and the finding that the data-space coresets term dominates is informative for understanding what drives Q_D's performance.

## Weaknesses

### Fatal
None.

### Major

1. **Theory-experiment disconnect.** The theoretical analysis (Sections 2.2–2.4) is built entirely on *closed-form* piecewise-linear flow matching models (Eq1–Eq3), where the vector field is an explicit weighted sum of noise vectors from training data. The paper states this as a "hypothesis" about trained networks (Section 2.2: "we hypothesize that neural networks employed in flow matching also exhibit the property of piecewise-linear interpolation") but provides no empirical verification that the trained 8-layer LeakyReLU network actually behaves like the closed-form interpolation model. The condensation phenomenon cited (Luo et al., 2021; Xu et al., 2025) applies under specific conditions (dropout or small initialization) that are not reported as being used. Without verification that the trained network's outputs satisfy the key properties (Eq2–Eq3), the theoretical derivation does not directly support the experimental claims — the paper analyzes one object (closed-form CFM) and deploys a different object (trained neural CFM).

2. **No statistical grounding for experimental results.** The experiments run "5 iterations" (Fig4 caption) — these are rounds of data selection, not independent random seeds. No error bars, standard deviations, or confidence intervals are reported anywhere in the paper. Given that the learning curves (Fig4, Fig9) show visible variation between iterations, it is impossible to assess whether the observed differences between methods are statistically meaningful. This is a standard methodological requirement for papers making comparative claims.

3. **Unsupported claim about outperforming the full dataset.** Section 3.2 states that Q_D "even outperforms the model trained on the full dataset" on diversity. No "full dataset" baseline line is shown or described in the figures. If true, this would imply selective subsampling beats having all data — an extraordinary claim that would require careful analysis (e.g., does the diversity metric have a degeneracy where adding more data reduces it? Is the full model undertrained?). The paper offers no discussion.

4. **Q_A accuracy results not shown alongside baselines.** The paper claims "Q_A yields the highest accuracy" (Section 3.2), yet the main quantitative comparison (Fig4) shows curves only for "Random, Coreset, Committe, Anchor, and Q_D methods" in its accuracy panel. Q_A accuracy numbers appear only in qualitative sample figures (Fig5, Fig6, Fig8) without baseline comparisons. The reader cannot verify Q_A's claimed accuracy advantage against standard baselines from the presented evidence.

### Minor

5. **Query strategies are model-agnostic, weakening the claimed flow-matching specificity.** Q_D (Eq4) and Q_A (Eq6) operate entirely on the dataset without incorporating the trained flow matching model. The paper acknowledges this decoupling (Section 4), but this also means the strategies are applicable to any conditional generative model. The core insight about selection direction is derived from the theory, but the actual selection mechanisms (label-space distance, label entropy across clusters, data-space coresets) are generic heuristics. The paper does not demonstrate why these strategies are particularly effective for flow matching versus other conditional generative model classes.

6. **Q_D formulation includes components not derived from the theory.** The theoretical analysis (Section 2.3) motivates selecting data with *identical* labels to increase diversity. The first term relaxes this to label similarity, which is reasonable. However, the second term (Δentropy — encouraging uniform label distribution across clusters) and third term (data-space coresets) are introduced without derivation from the theory. The ablation study (Fig9) further shows that the data-space coresets term dominates, raising the question of how much Q_D's performance is just standard coresets with a label-conditioned soft constraint. Additionally, the clustering method for Δentropy is underspecified: "partition the dataset labels into clusters... A cluster is defined as a set of data points whose inter-point distances fall below a given threshold" (Section 2.3) with no clustering algorithm or threshold selection method described.

7. **RBF label prediction accuracy unreported.** Both Q_D and Q_A require predicting labels for unlabeled data using RBF neural networks. The entire active learning pipeline depends on these predictions, yet the paper reports no accuracy metrics (e.g., RMSE on held-out labeled data) for the RBF predictor, how it degrades with extrapolation, or how prediction errors affect query selection quality.

8. **Q_hybrid evaluation is thin.** Fig7 shows ω ∈ {0.1, 0.2, 0.3, 0.4} but does not show the ω=0 (pure Q_A) and ω=1 (pure Q_D) endpoints, and there is no comparison against simply mixing the datasets independently selected by Q_D and Q_A.

### Trivial

9. The diversity metric is a "custom variant of the Vendi score... calculated as the average pairwise Euclidean distance" (Section 3.1). This could conflate "many distinct samples" with "a few extreme outliers," a known limitation of pairwise-distance metrics.

## Nice-to-Haves

- Compare against a simple "label-aware random" baseline: randomly select data with labels close to existing labels (for diversity) or far from existing labels (for accuracy) to test whether the complex Q_D/Q_A formulations add value beyond the directional insight alone.
- Report the computational cost of the active learning pipeline to quantify annotation savings.
- Compare Q_D/Q_A applied to a different conditional generative model class (e.g., conditional GAN or diffusion model) to isolate what is flow-matching-specific about the strategies.

## Removed Points

- **"Entropy term contradicts the first term of Q_D":** The critic claimed the entropy term (balancing label distribution across clusters) directly contradicts the similarity term. Upon inspection, these are addressing different aspects — within a cluster, labels are similar by construction; balancing across clusters does not inherently conflict with selecting label-similar data. Removed as overstatement.
- **"Q_A not shown in Fig4":** The figure caption (extracted by parser, may be incomplete) lists only certain methods. Without seeing the actual rendered figure, this cannot be confirmed as a paper error versus a parser artifact. Removed as unverifiable from text alone.
- **"Proofs deferred to appendix":** The appendix is stripped by the parser; the original submission likely contains them. Removed per hard rule.
- **"No comparison against a trivial label-aware random baseline":** Moved to Nice-to-Haves, as this is a constructive suggestion rather than a core flaw.
- **"No analysis of computational cost":** Moved to Nice-to-Haves.

## Novel Insights

Beyond the paper's own contributions, the review surfaces a structural tension: the paper frames its contribution as "active learning for flow matching models," yet the resulting strategies are dataset-level and model-agnostic. The decoupling is presented as a feature (computational efficiency from avoiding repeated model training), but it also means the paper's most specific theoretical contribution is the *directional insight* (same-label → diversity, different-label → accuracy) rather than the algorithmic formulations themselves. This tension suggests that future work in this direction may need to either build selection mechanisms that engage with the flow matching model's internal state (e.g., the learned vector field or probability paths) or explicitly reframe the contribution as theory-informed data selection for conditional generative models broadly.

## Suggestions

1. **Bridge theory and experiments.** Add empirical verification that the trained network approximately satisfies the piecewise-linear interpolation property (Eq2–Eq3), e.g., by testing whether interpolating between two conditions in the network's output produces convex combinations of the corresponding outputs.
2. **Add statistical rigor.** Report all results with multiple random seeds (at least 3–5) and include error bars.
3. **Address or remove the full-dataset claim.** Either show the full-dataset baseline in figures and explain how selective subsampling can yield higher diversity, or remove the unsubstantiated claim.
4. **Show Q_A against baselines.** Include Q_A in the main quantitative comparison alongside the other methods.
5. **Report RBF prediction accuracy.** Provide held-out accuracy of the label predictor and analyze how prediction errors affect query quality.
6. **Tighten Q_D's derivation or scope.** Either derive each term more directly from the theory, or acknowledge Q_D as a heuristic interpretation. Report the clustering details for the Δentropy term.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>