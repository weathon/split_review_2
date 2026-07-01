## Summary
This paper presents a pilot study on active learning for flow matching generative models in the context of continuous conditional datasets. The authors propose a theoretical analysis framework based on piecewise-linear neural networks and closed-form flow matching to derive how individual data points influence model diversity and accuracy. Based on this analysis, they propose two query strategies—one for enhancing diversity and one for improving accuracy—and a weighted hybrid strategy to trade off between these objectives, with experiments on shape design tasks showing improvements over classical active learning methods.

## Strengths
- **Novel problem formulation**: The paper addresses the under-explored area of active learning specifically designed for generative models (flow matching), rather than using generative models to assist discriminative model training, which is a genuine gap in the literature.
- **Theoretical grounding with closed-form analysis**: The use of piecewise-linear neural network analysis and closed-form flow matching to derive explicit relationships between dataset composition and generation properties (diversity vs. accuracy) provides a principled foundation for query strategy design, which is rare in active learning for generative models.
- **Practical decoupling from model retraining**: The proposed query strategies operate directly on the dataset level using RBF networks for label prediction, avoiding repeated training of expensive flow matching models during the active learning loop, which is a significant practical advantage for the intended applications (medical imaging, numerical simulation).

## Weaknesses

### Fatal
None.

### Major
- **Limited experimental validation**: The experiments compare Q_D and Q_A mainly against random, coreset, committee, and anchor methods, but not against the most directly relevant baseline: random sampling followed by full-dataset training at each budget step. Given that the method involves training auxiliary RBF networks and selecting data based on predicted labels, the natural baseline of "just train on everything labeled so far" should be included. Additionally, only one specific flow matching architecture and training setup is tested; results may not generalize.
- **Missing quantitative comparisons with standard active learning budgets**: The paper does not report standard active learning metrics such as labeling efficiency (accuracy/diversity per annotation cost), convergence speed, or comparisons at fixed annotation budgets. The visual comparisons (Fig 5, 6, 8) are qualitative and lack statistical significance testing.
- **Weak justification for CPWL assumption for flow matching**: The paper claims that neural networks in flow matching exhibit piecewise-linear interpolation behavior, citing condensation phenomena. However, the connection between condensation (studied mainly in simple feedforward classifiers with specific initialization) and the learned vector field of flow matching models (which are usually trained on noisy trajectories) is not rigorously established or empirically verified in the paper. The entire theoretical framework rests on this unverified assumption.

### Minor
- **Diversity-accuracy trade-off is not new**: The fundamental trade-off between diversity and accuracy in generative models is well known in the literature (e.g., precision-recall, coverage-fidelity trade-offs). The paper presents this as a novel finding from a dataset perspective, but the insight that "data with same label → diversity, data with different labels → accuracy" is stated without sufficient nuance about what "same label" means in continuous label spaces.
- **The query strategies rely on predicted labels from RBF networks**: The practical implementation requires label prediction for unlabeled data, and the quality of this prediction directly affects query quality. The paper does not analyze or report the accuracy of these predictions, nor the sensitivity of results to prediction errors.
- **Ablation study limited**: The ablation (Fig 9) only tests removal of individual terms from Q_D on diversity, but does not ablate Q_A or the hybrid strategy, nor does it test sensitivity to the weighting hyperparameters α, β, γ in Eq 4.

### Trivial
- The paper states "we propose to increase the number of such individual samples as a query strategy" (Sec 2.3) but the actual Q_D formulation (Eq 4) does not directly optimize for number of individual samples, making the logical connection between the diversity analysis and the final strategy somewhat indirect.

## Nice-to-Haves
- Include standard active learning baselines like uncertainty sampling and Bayesian active learning by disagreement, and compare at multiple budget fractions.
- Provide empirical validation of the CPWL assumption for flow matching models (e.g., by analyzing linear regions or condensation indicators in trained models).
- Analyze the computational overhead of the proposed method compared to alternatives, especially the RBF network training component.

## Novel Insights
The key insight—that data points sharing similar labels increase the number of possible interpolated outputs (diversity) while data points with distinct labels tighten the interpolation error bound (accuracy)—is a clean and potentially useful formalization for understanding how training data composition affects generative model behavior in continuous conditional settings. However, this insight is essentially a restatement of the known fact that more training data in a region reduces interpolation error (accuracy), while more diverse data in a region increases coverage (diversity). The linear interpolation analysis under CPWL assumption provides a mathematical vocabulary for this intuition but does not yield fundamentally new understanding beyond what is already known about nearest-neighbor-like behavior of overparameterized models.

## Suggestions
- Add a direct comparison with "train on all labeled data" (batch retraining) to demonstrate that the proposed selection strategy is genuinely better than random acquisition at the same budget, which is the most critical baseline for any active learning method.
- Provide quantitative results (with error bars over multiple seeds) for diversity and accuracy at each budget step, including for the hybrid strategy.
- Include an analysis of how the accuracy of the RBF label predictions affects the query selection quality and overall performance.

## Score and Decision
The paper tackles a relevant and underexplored problem with a reasonable theoretical motivation and practical query strategies. However, the experimental validation is insufficient to fully support the claimed superiority over standard methods: key baselines are missing, the CPWL assumption is not verified, and results lack statistical rigor. The contributions are interesting but the evidence base is not strong enough for acceptance at a top venue.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>