## Summary
# Final Review Report

## Summary

This paper investigates active learning for flow matching models in continuous-conditional shape design tasks. The authors propose a theoretical framework based on piecewise-linear neural network analysis of closed-form flow matching models, from which they derive two competing query strategies: Q_D (for maximizing generation diversity) and Q_A (for maximizing generation accuracy). A weighted hybrid strategy Q_hybrid is introduced to navigate the diversity-accuracy trade-off. The approach is evaluated on synthetic and three real-world aerodynamic shape design datasets (airfoil, flying wing, starship).

**Core strengths:** The paper addresses a relevant and underexplored problem — active learning for generative models with continuous conditions. The idea of decoupling the query strategy from the trained generative model (operating at dataset level) is practically appealing for expensive simulation-based labeling scenarios. The diversity-accuracy trade-off analysis from a dataset composition perspective provides an intuitive conceptual framework.

**Core weaknesses:** (1) The piecewise-linear assumption underlying the theoretical framework is stated without adequate justification for flow matching models specifically. (2) The error bound Eq(5) is presented without derivation in the main text, and the relationship between the bound and Q_A's design is logically inconsistent — Q_A selects points to maximize label distance, which would increase rather than decrease the bound. (3) The Q_D formula has unspecified hyperparameters (α,β,γ), and the hybrid combination is scale-sensitive without normalization. (4) Experimental evaluation lacks statistical significance measures, dataset size specifications, and contains potential overclaims. (5) Novelty cannot be verified without external literature comparison in this run.

**Novelty assessment:** Deferred — external literature verification was not available in this run. The key claims — piecewise-linear analysis of flow matching for active learning, and the specific query strategies — appear plausible as a pilot study, but their novelty relative to prior work on CPWL analysis of generative models and AL for generative models requires manual verification.

## Strengths
1. **Relevant and timely problem formulation.** Active learning for generative models, especially flow matching models in engineering design, is an underexplored area. The paper correctly identifies that standard AL strategies designed for discriminative models do not naturally transfer to generative models with continuous condition spaces. The focus on shape design (aerodynamic optimization) is practically motivated, as obtaining high-fidelity simulation labels is genuinely expensive in these domains.

2. **Model-agnostic dataset-level querying.** The proposed query strategies Q_D and Q_A operate directly on the dataset without requiring repeated training or inference of the flow matching model. This is a practical advantage over model-based AL methods (e.g., uncertainty sampling, committee-based methods), which require model forward passes for each candidate. The paper's approach trains only an RBF network for label prediction, which is computationally lighter.

3. **Clear conceptual framework for the diversity-accuracy trade-off.** The paper identifies and formalizes a tension between two competing objectives in dataset composition for conditional generation: adding label-consistent points (same condition) increases interpolation diversity, while adding label-distinct points (new conditions) improves accuracy by reducing the interpolation region size. This conceptual lens — viewing the trade-off from a dataset perspective rather than a model-capacity perspective — is intuitive and could be useful for practitioners designing data collection strategies.

4. **Multi-dataset evaluation across realistic engineering tasks.** The experiments span one synthetic dataset and three real aerodynamic shape design datasets (airfoil, flying wing, starship) with label dimensions ranging from R^1 to R^4. The consistent pattern across datasets — Q_D improves diversity at the cost of accuracy, Q_A improves accuracy at the cost of diversity — suggests the identified trade-off is robust across different continuous-condition spaces.

5. **Transparent limitation acknowledgment.** The conclusion explicitly notes the key limitation: because the framework operates at the dataset level (decoupled from the model), it cannot directly address or correct behavioral biases of the trained flow matching model. This honest acknowledgment of the method's scope boundary is commendable and should be retained.

## Weaknesses
**W1. The piecewise-linear assumption is not adequately justified for flow matching models. [Major]**

The entire theoretical framework rests on the hypothesis that flow matching neural networks exhibit piecewise-linear interpolation behavior. The paper cites the condensation phenomenon (Luo et al. 2021; Xu et al. 2025) as justification, but condensation has been primarily studied in *classification* networks with ReLU activations under specific training conditions (dropout, small initialization). No empirical evidence or theoretical argument is provided that flow matching models — trained with continuous regression targets and flow-matching objectives — undergo the same phenomenon. Furthermore, Eq(2) claims a very specific form of *convex interpolation* in the condition space that goes beyond standard CPWL theory (which only guarantees the existence of a piecewise-affine partition, not that the affine functions are convex combinations of vertex outputs). This gap weakens the theoretical foundation significantly.

*Required action:* Either (a) provide empirical evidence of linear interpolation regions in a trained flow matching model (e.g., visualization of the vector field as a function of condition input), or (b) explicitly frame the analysis as a *toy model* that provides intuition rather than a rigorous theory, and soften claims accordingly.

---

**W2. Logical inconsistency between the error bound (Eq5) and Q_A's design. [Major]**

Eq(5) states |f(x*) - c*| ≤ K·max||c_i - c_j||^2, implying that to minimize error, one should *reduce* the maximum distance between training conditions in each region. A natural strategy would be to add points that *fill gaps* in the condition space. However, Q_A (Eq6) selects points with distance(y, 𝒴) *maximized* — i.e., it selects points whose labels are farthest from existing ones, which would push the convex hull outward and potentially *increase* max||c_i - c_j||. The paper claims Q_A "performs the coresets algorithm in the label space," but coresets select points to cover the space uniformly, not to maximize distance. The logical chain from the error bound to Q_A's design is therefore broken.

*Required action:* Explain the mechanism by which adding far-away label points improves accuracy. Is it because the RBF label predictor benefits from a wider coverage? Or does the bound in Eq(5) only apply within each *existing* region, and Q_A targets different regions? Provide a clear reconciliation between the bound and the query strategy, or revise Q_A's definition to be consistent with the bound.

---

**W3. Q_D's hyperparameters (α, β, γ) are unspecified, making the method irreproducible. [Major]**

Eq(4) introduces three weighting coefficients, but their values used in experiments are not reported. The clustering-based Δentropy term also requires a distance threshold that is not specified. Without these values, the method cannot be reproduced or compared fairly. Furthermore, the ablation study shows that the data-space distance term (γ·distance(x, 𝒳)) dominates, while the Δentropy term (β) has minor effect — this raises the question of whether the two theory-derived terms (label similarity and entropy) actually contribute beyond standard coresets.

*Required action:* Report all coefficient values used in experiments, describe the selection procedure (e.g., grid search, cross-validation), and include a sensitivity analysis for each coefficient.

---

**W4. Q_hybrid = ω·Q_D + (1-ω)·Q_A is scale-dependent without normalization. [Major]**

Q_D and Q_A have different numerical ranges (Q_D sums three terms while Q_A is a single distance), so the weight ω does not control the trade-off as intended unless the scores are normalized. The paper reports results for ω ∈ {0.1, 0.2, 0.3, 0.4} but does not describe any normalization. If Q_A values are much larger than Q_D values, the actual trade-off is not what ω suggests.

*Required action:* Either (a) normalize Q_D and Q_A to comparable scales (min-max, z-score, or rank-based) before combining, or (b) define the hybrid strategy at the decision level rather than at the score level. Report the normalization procedure explicitly.

---

**W5. Experimental evaluation lacks statistical rigor and key details. [Major]**

Several critical experimental details are missing: (a) Dataset sizes for all four datasets are not reported. (b) The number of initial labeled samples and total number of selection rounds are not specified. (c) Results are presented without error bars, confidence intervals, or statistical significance tests — only line plots with single trajectories. Given the stochasticity in data selection and model training, readers cannot assess whether observed differences are meaningful. (d) The evaluation metrics defined as integrals over the condition space (Eq8-9) are impractical as written; the actual discretization procedure (number of test conditions, number of generated samples per condition) is not described. (e) The claim that Q_D "even outperforms the model trained on the full dataset" in diversity is surprising but not explained — why would training on less data produce more diversity?

*Required action:* Report dataset statistics, initial label counts, number of rounds, and evaluation details (test condition count, samples per condition). Add variance estimates (standard deviations over 3+ seeds) to all main results. Explain why training on less data can yield higher diversity than the full dataset.

---

**W6. The diversity metric conflates coverage with variance. [Minor]**

The paper uses average pairwise Euclidean distance of generated samples as the "diversity score." This metric primarily measures the variance/spread of the generated distribution, not the number of distinct modes or the coverage of the true data distribution. Using a generative model, one could produce uniformly random points with high pairwise distance but zero utility. The Vendi score, which the paper references, addresses this through eigenvalue-based entropy — but the paper's actual metric is a simpler heuristic. A more meaningful diversity evaluation would combine coverage of ground-truth modes with intra-mode variance.

*Required action:* Either justify why mean pairwise distance is appropriate for the shape design application (where the ground-truth distribution is continuous), or augment with a mode-coverage metric. Rename the metric to "Mean Pairwise Distance (MPD)" to avoid confusion with the Vendi score.

---

**W7. Introduction conflates classification labels with continuous conditions. [Minor]**

The abstract and introduction repeatedly use "labeled samples" terminology derived from classification active learning, but the paper's setting is continuous conditional generation where "labels" are continuous performance vectors (e.g., lift coefficient, drag coefficient). This framing is misleading — flow matching models do not "classify" shapes, and obtaining a condition label via simulation is fundamentally different from manual annotation in medical imaging (the paper's primary motivating example). The two settings have very different cost structures and failure modes.

*Required action:* Restructure the introduction to clearly separate: (a) the general AL motivation (expensive labeling), from (b) the specific setting of continuous-conditional generation for engineering design. Replace "labeled samples" with "paired (shape, condition) samples" where appropriate.

---

**W8. The ablation study is one-sided. [Minor]**

The ablation only tests Q_D's three components. Missing ablations include: (a) removing the label-similarity term (-α·distance(y, 𝒴)) to test whether the core theoretical insight drives diversity gains, (b) sensitivity of Q_A to RBF prediction quality (varying training set size for the RBF), (c) sensitivity of the hybrid strategy to ω at different budget levels. The ablation also uses confusing terminology ("no density" in the figure does not match any term in Eq4).

*Required action:* Add the missing ablations and clarify the figure labeling to match the equation terminology.

---

**W9. Novelty cannot be assessed without external literature comparison. [Deferred]**

This run operated in Retrieval-Disabled Mode, so external literature verification was not available. The paper claims a "novel analytical framework" and "pilot study of active learning for flow matching models." While the application domain appears novel, the core technical components (piecewise-linear analysis, coresets-based querying) are well-established individually. A manual literature verification is needed to assess whether the specific combination and the diversity-accuracy trade-off finding constitute sufficient novelty for publication.

*Required action:* The authors should ensure their related work section thoroughly covers (a) CPWL analysis of generative models, (b) active learning for generative models beyond the cited works, and (c) any prior work on dataset-level query strategies for conditional generation. This assessment is deferred for this review.

## Score
**Final Score: 5.5/10**

**Scoring rationale:**

The paper addresses a relevant and novel problem — active learning for flow matching models in continuous-conditional shape design — which contributes to an underexplored intersection of generative models and active learning. The dataset-level querying approach is practically attractive for expensive simulation-based labeling scenarios. However, the score is constrained by several major weaknesses that affect research value and methodological soundness:

- **Validity risk (W1, W2):** The theoretical foundation rests on an unsubstantiated piecewise-linear assumption for flow matching models, and the accuracy-maximizing strategy Q_A is not logically connected to the error bound that supposedly motivates it. These issues undermine confidence in the core theoretical claims.
- **Reproducibility concern (W3, W4):** Key hyperparameters (α, β, γ) are unreported, and the hybrid combination is scale-sensitive without specified normalization. The method cannot be reproduced as described.
- **Experimental rigor (W5):** Results lack variance estimates, dataset sizes, and key procedural details. The claim that Q_D outperforms the full-dataset model is unexplained.
- **Novelty assessment (W9, deferred):** External literature comparison was not available in this run, so the novelty of the analytical framework relative to prior CPWL and AL-for-generative-models work is conservatively marked as unclear.
- **Strengths (S1-S5):** The problem selection is relevant, the dataset-level approach is practical, and the conceptual diversity-accuracy trade-off framing is clear. The multi-dataset evaluation provides useful evidence of the trade-off's robustness.

**Recommended revision path to improve score:**

1. Provide empirical validation of the piecewise-linear interpolation assumption in flow matching models (addressing W1).
2. Reconcile the logical gap between Eq(5) and Q_A, or revise Q_A's formulation and theoretical justification (W2).
3. Report all hyperparameters, normalization procedures, and experimental details (W3, W4, W5).
4. Add statistical significance measures (error bars, multi-seed runs) to all experimental results (W5).
5. Expand the ablation study to test the theory-derived terms specifically (W8).
6. Restructure the introduction to accurately frame the continuous-conditional setting (W7).
7. Conduct a thorough related-work comparison to establish novelty (W9).