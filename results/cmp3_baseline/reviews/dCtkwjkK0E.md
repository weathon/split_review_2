## Summary

This paper studies active learning for flow matching generative models on datasets with continuous labels (conditions).  
It introduces an analytical framework using piecewise-linear neural networks and closed-form flow matching to derive how individual data points affect model diversity and accuracy, concluding that points with the same label as existing data increase diversity while points with different labels increase accuracy.  
Based on this insight, the authors propose two query strategies — one for diversity (Q_D) and one for accuracy (Q_A) — and a weighted hybrid strategy to trade off between the two, with experiments on synthetic and three real-world shape design datasets (airfoils, flying wings, starship-like).

## Strengths

- **Novel problem formulation**: Active learning specifically designed for generative models (flow matching) with continuous conditions is underexplored and practically relevant.
- **Theoretically motivated query design**: The paper derives insights from a piecewise-linear analysis of closed-form flow matching, leading to interpretable, data-centric query strategies that do not require iterative model retraining.
- **Clear conceptual contribution**: The identification of a data-driven trade-off between diversity and accuracy (same‑label points benefit diversity, different‑label points benefit accuracy) is intuitive and grounded in the analysis.
- **Practical evaluation on real engineering datasets**: Experiments on airfoil, flying wing, and starship-like shape design tasks demonstrate applicability in domains where labeling is expensive.

## Weaknesses

### Fatal
- None.

### Major
- **Critical inconsistency between text and figure caption**:  
  The text on page 7 states “Q_A yields the highest accuracy”, but the caption of Figure 4(b) says “Random achieves the highest accuracy”.  
  This is a contradictory claim about the main experimental result; it undermines the paper’s core message and must be clarified.

- **Strong theoretical assumptions not validated in practice**:  
  The analysis assumes the flow matching model behaves as a piecewise‑linear interpolant (closed‑form solution).  
  Real flow matching models use deep, nonlinear neural networks; the paper provides no evidence that the proposed strategies remain effective when this assumption is violated.  
  The theoretical derivations (Eqs. 1–3) are heuristic and rely on an absent appendix for key lemmas, making the “rigorous theoretical characterization” claimed in the contributions difficult to assess.

- **Limited baseline comparison**:  
  Only coresets, committee, anchor, and random are compared.  
  Standard active learning methods for regression (e.g., uncertainty sampling for continuous outputs, density‑weighted strategies) are omitted.  
  The claim of outperforming “methods designed for discriminative models” is not fully supported given the narrow set of baselines.

- **Unclear handling of label prediction for unlabeled data**:  
  Both Q_D and Q_A require label predictions for unlabeled points, obtained via an RBF neural network.  
  The paper does not analyze how errors in these predictions affect query quality, nor does it compare alternative label prediction methods.

- **Ablation study shows distance(x, X) term dominates**:  
  While the ablation is helpful, the most influential term in Q_D is essentially a standard coresets‑style diversity penalty, which somewhat weakens the novelty of the strategy.

### Minor
- The definition of “Δentropy” in Q_D is vague; it refers to clustering labels and computing classification entropy, but the clustering threshold is not specified.
- Weights α, β, γ in Q_D and ω in the hybrid strategy are not justified or systematically tuned.
- The diversity metric (average pairwise Euclidean distance) may not capture all aspects of diversity (e.g., coverage or mode coverage).

### Trivial
- Some notation inconsistencies (e.g., “Scardelis” vs “Scarvelis” in references).

## Nice-to-Haves

- Analyze the sensitivity of query performance to the accuracy of the RBF label predictor.
- Include a baseline that performs active learning for flow matching by simply retraining the model and using uncertainty over generated outputs.
- Provide a clearer justification for why the distance(x, X) term is so dominant and whether simpler heuristics could replace the other terms.

## Novel Insights

None beyond the paper’s own contributions. The identification of dataset composition effects on diversity/accuracy in flow matching (same‑label vs different‑label points) is the paper’s main unique insight, but it is derived under strong idealized assumptions and not rigorously validated.

## Suggestions

- Resolve the contradiction between the text and Figure 4(b) regarding which method achieves the highest accuracy.
- Weaken the theoretical claims or provide empirical evidence that the piecewise‑linear interpolation behavior holds approximately for the trained models used in experiments.
- Include additional active learning baselines for regression (e.g., uncertainty sampling based on variance of an ensemble regressor trained on labeled data).
- Report how accurately the RBF network predicts labels on the pool and how this affects the query outcome.
- Clarify the computation of Δentropy and the choice of clustering threshold.

## Score and Decision

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>