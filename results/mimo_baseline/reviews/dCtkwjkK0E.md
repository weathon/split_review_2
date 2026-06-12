## Summary

This paper proposes an active learning framework specifically for flow matching generative models, addressing the underexplored problem of data-efficient training for generative (rather than discriminative) models. Using a piecewise-linear neural network analysis of closed-form flow matching, the authors derive two query strategies—one targeting diversity (Q_D) by selecting label-similar data, and one targeting accuracy (Q_A) by selecting label-distant data—and demonstrate their inherent conflict, which they interpret as a diversity-accuracy trade-off in dataset composition.

## Strengths

- **Novel problem framing.** The paper correctly identifies that most prior work on "active learning + generative models" uses generative models to assist active learning for discriminative tasks, rather than performing active learning for the generative model itself. This is a genuinely underexplored and practically relevant direction, especially in domains like shape design and numerical simulation where labeling is expensive.

- **Interesting theoretical insight.** The observation that same-label data enhances diversity while different-label data enhances accuracy (derived from the piecewise-linear framework) provides a clean, interpretable explanation for the diversity-accuracy trade-off from a dataset composition perspective. This is a useful conceptual contribution.

- **Computationally efficient query strategies.** The proposed Q_D and Q_A operate directly on the dataset using RBF networks for label prediction, avoiding repeated training of the flow matching model. This is practically valuable in the active learning setting where annotation budgets are limited.

- **Application-driven evaluation.** Experiments on real engineering shape design tasks (airfoils, flying wings, starships) with labels obtained from numerical simulation demonstrate practical relevance beyond toy problems.

## Weaknesses

### Fatal
None.

### Major

- **Gap between theoretical analysis and practical implementation.** The theoretical framework (Eqs. 1–3) is derived for *closed-form* flow matching models under the assumption of piecewise-linear neural network interpolation. However, the experiments use standard trained neural networks with AdamW optimization over 4M steps. The paper does not establish why the closed-form analysis transfers to trained networks, which fundamentally undermines the theoretical motivation for Q_D and Q_A. The condensation phenomenon is cited as justification, but the conditions for condensation (small initialization, dropout, etc.) are not verified or controlled in the experimental setup.

- **Strong assumptions in the diversity analysis.** The combinatorial argument in Section 2.3 (e.g., that a condition c* between c_0 and c_1 generates mn sample types) assumes exact interpolation and that all combinations are equally likely. In practice, with neural network training and stochastic sampling, the actual diversity may deviate substantially from these combinatorial upper bounds. The paper acknowledges these are upper bounds but uses them directly to motivate Q_D without empirical verification of the tightness.

- **Limited experimental depth.** Only 5 active learning iterations with 6% data per iteration are shown, which provides limited evidence of long-term behavior. The paper also does not compare against modern active learning baselines like BADGE or other gradient-embedding-based methods. The committee baseline uses only traditional regression models (SVR, Random Forest, XGBoost), which may not represent the state of the art for active learning with continuous labels.

- **Q_D outperforming full dataset in diversity.** The paper notes that Q_D achieves higher diversity than training on the full dataset (Section 3.2), which is counterintuitive and warrants deeper investigation. This could indicate that the model overfits to certain data regions when trained on all data, but the paper does not analyze whether the extra diversity from Q_D is meaningful or corresponds to artifacts (e.g., mode collapse in the full-data model).

### Minor

- **Hyperparameter sensitivity of Q_D.** The strategy involves three weighting coefficients (α, β, γ) in Eq. 4, yet the paper provides no systematic analysis of their sensitivity. The ablation study (Fig. 9) removes entire terms but does not explore how α, β, γ interact or how to set them in practice.

- **Simplicity of diversity metric.** The diversity score (Eq. 8) is essentially average pairwise Euclidean distance of generated samples, which does not capture structural diversity (e.g., whether generated samples span the full mode space or cluster in a few modes). The Vendi score is mentioned in passing but not actually used.

- **1D analysis generalization.** The core diversity analysis in Section 2.3 is presented for the 1D case (d=1), and the paper does not rigorously extend this to higher-dimensional label spaces (the datasets have labels up to d=4). The combinatorial arguments become considerably more complex in higher dimensions.

### Trivial
None.

## Nice-to-Haves

- Empirical verification that the piecewise-linear interpolation assumption holds for the trained networks in the experiments (e.g., measuring interpolation consistency between conditions).
- Comparison with modern active learning methods such as BADGE or batchBALD adapted for the continuous-label regression setting.
- Analysis of the diversity-accuracy Pareto frontier (ω sweep) compared against a random sampling baseline to verify that the hybrid strategy actually dominates.

## Novel Insights

The paper's central insight—that data selection for generative models involves a fundamental tension between diversity and accuracy that can be understood through the lens of label-space interpolation—is genuinely novel and provides a clean conceptual framework. However, this insight is derived under strong assumptions (closed-form flow matching, piecewise-linear interpolation) whose applicability to practical trained models remains largely unsubstantiated.

## Suggestions

- Provide empirical evidence that the piecewise-linear interpolation assumption holds for the trained models, e.g., by measuring whether model outputs for interpolated conditions approximate interpolations of outputs at dataset conditions.
- Extend the combinatorial diversity analysis to higher-dimensional label spaces or provide bounds that hold more generally.
- Include modern active learning baselines and extend the number of active learning iterations to demonstrate sustained benefit.

## Score and Decision

The paper addresses an interesting and practically relevant problem with a novel theoretical perspective. However, the theoretical framework relies on strong assumptions that bridge poorly to the experimental setting, and the experimental validation, while showing the intended trends, lacks depth in terms of iteration count, baseline diversity, and hyperparameter analysis. As a pilot study, it is a reasonable starting point, but the gap between the theoretical claims and empirical evidence is too significant for acceptance at ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>