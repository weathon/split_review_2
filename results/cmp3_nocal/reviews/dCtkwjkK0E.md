## Summary

This paper proposes active learning query strategies for flow matching models in continuous-condition shape design tasks. The authors develop a theoretical framework based on piecewise-linear neural network analysis to understand how data affects diversity and accuracy in generation, from which they derive two query strategies (Q_D for diversity, Q_A for accuracy) and a weighted hybrid. Experiments on one synthetic and three real-world shape design datasets show that Q_D improves diversity over standard active learning baselines, while the diversity-accuracy trade-off is demonstrated through the hybrid strategy.

## Strengths

1. **Novel problem framing.** Applying active learning *to* generative models (rather than using generative models *for* active learning) is an underexplored direction. The paper's focus on continuous-condition flow matching in shape design is well-motivated, as labeling costs via numerical simulation are genuinely high in this setting.

2. **Principled attempt to derive query strategies from generative mechanism.** Rather than borrowing methods designed for discriminative models, the paper tries to ground query design in an explicit model of how data points affect flow matching outputs (Eq1–Eq3, Eq5). This conceptual direction is valuable even if the theoretical assumptions are idealized.

3. **Honest characterization of the diversity-accuracy trade-off.** The paper explicitly identifies the conflict between Q_D and Q_A (Section 2.4) and provides a weighted hybrid strategy (Eq7) to navigate it, rather than claiming simultaneous improvement on both axes.

4. **Dataset-level decoupling of query strategy from model training.** The proposed strategies operate on the dataset (via an RBF label predictor) without requiring repeated training of the flow matching model, which is a practical advantage acknowledged in the paper.

## Weaknesses

### Major

1. **Q_A's accuracy results are claimed but absent from the main comparative figure, creating a central evidential gap.**

   The paper states (line 163): "In contrast, Q_A yields the highest accuracy." However, Figure 4 — the main comparative figure showing diversity and accuracy across four datasets — plots only "Random, Coreset, Committe, Anchor, and Q_D methods" for both panels (line 155 caption). Q_A is not included. The reader cannot verify the magnitude of Q_A's accuracy advantage relative to baselines, nor assess whether the advantage is consistent across datasets. Figures 5, 6, and 8 provide qualitative comparisons with per-condition accuracy numbers, and Figure 7 shows the hybrid trade-off, but a direct quantitative comparison of Q_A against all baselines is missing. For a paper whose headline contribution includes an accuracy-oriented strategy, this is a serious evidential gap.

2. **The core theoretical assumption (piecewise-linear interpolation behavior of the flow matching network) is unverified, creating a theory–experiment gap.**

   The entire theoretical analysis (Eq1–Eq3, Lemma 1, Lemma 2) depends on the assumption that the flow matching model's neural network exhibits piecewise-linear interpolation behavior. The paper acknowledges this as a hypothesis (line 45: "we hypothesize that neural networks employed in flow matching also exhibit the property of piecewise-linear interpolation") and cites condensation literature for motivation. However, the experiments use standard 8-layer LeakyReLU networks trained with AdamW — networks that are known to be *piecewise-linear* in the activation sense but may not satisfy the stronger *condensation/interpolation* property required by the analysis. No empirical verification is provided (e.g., checking whether the learned vector field at unseen conditions matches linear interpolation of training data). If the experimental model does not satisfy the theoretical assumptions, the connection between the derived strategies and their empirical performance is unexplained, and the theory may not generalize.

### Minor

3. **No statistical rigor.** No error bars, standard deviations, or multiple-seed experiments are reported for any result. All plots show single trajectories over 5 iterations. Active learning results are notoriously variable depending on the initial labeled set and random seed; single trajectories make it impossible to assess whether observed differences are significant or idiosyncratic.

4. **Weighting parameters (α, β, γ) in Q_D are unspecified.** The Q_D objective (Eq4) has three tunable weights whose values meaningfully affect the strategy's behavior. These are not specified anywhere in the paper, nor is a procedure for setting them described.

5. **Inconsistency between the ablation study and the formalism.** The ablation study (Figure 9 caption) includes a "no density" condition, but "density" is not a term in the Q_D formulation (Eq4), which uses *distance*(y,𝒴), Δ*entropy*, and *distance*(x,𝒳). The mismatch between the figure and the paper's formalism is confusing.

6. **Several experimental details are missing.** The pool size per dataset is not stated (only "6% of the data is selected" per iteration is given). The number of generated samples per condition used in the diversity evaluation (Eq8) is not specified, making the metric's scale ambiguous.

7. **The extension from 1D to higher-dimensional label spaces is asserted without derivation.** The diversity analysis is conducted for d=1, and the extension to higher dimensions (used in Eq4) is presented without formal justification of how the subregion decomposition and counting argument generalize.

### Trivial

8. Reference typo: "Scardelis et al. (2023)" on line 45 should be "Scarvelis et al. (2023)".

## Nice-to-Haves

- Verify the piecewise-linear interpolation assumption empirically on a small 1D/2D problem, which would substantially strengthen the connection between theory and experiments.
- Specify how the weights α, β, γ in Q_D are set (e.g., grid search on the first dataset and held fixed, or a heuristic).
- Report computational cost comparisons (RBF training vs. training four committee predictors per iteration).
- Clarify how many labeled points are needed for the RBF label predictor to be reliable in early iterations.

## Removed Points

- **"GAAL characterization is inaccurate"**: I cannot independently verify the GAAL paper's mechanism; this criticism is removed as unverifiable.
- **"Anchor method is a straw-man version of GALISP"**: I cannot independently verify the GALISP implementation; this criticism is removed as unverifiable.
- **"Baselines are set up to be disadvantaged"**: The paper acknowledges the limitation (line 19–20) and includes a random baseline. The comparison is informative as-is; this criticism overstates the issue.
- **"Accuracy evaluation irony (needs labels)"**: The evaluation uses labeled hold-out test data, which is standard practice. This is not a meaningful weakness.
- **"Committee computational cost"**: This point was raised as a "missing discussion" but is actually a practical advantage of the proposed method; moved here for context.
- Various grammar, formatting, and style nitpicks: removed per instructions as parser artifacts or non-substantive.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any genuinely novel observation about the paper's results, methodology, or positioning that is not already present in the paper itself.

## Suggestions

1. **Add Q_A to Figure 4.** This is the single highest-leverage fix: include Q_A's accuracy trajectory alongside the baselines so the reader can directly assess the claimed improvement.
2. **Report error bars or multiple-seed runs.** Active learning results are seed-dependent; even 3 seeds with standard deviations would substantially increase confidence in the findings.
3. **Acknowledge and ideally verify the theoretical assumption.** Either provide empirical evidence that the trained networks exhibit the condensation/interpolation property, or explicitly discuss the limitations this imposes on the theory-experiment connection.
4. **Specify α, β, γ values** and the procedure used to set them (e.g., grid search, heuristic, or held constant).
5. **Fix the "no density" / formalism mismatch** in the ablation study caption.
6. **State pool sizes** and the number of generated samples used for evaluation.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>