## Summary

The paper introduces XBIC, a score for causal discovery in discrete Bayesian networks that augments the Bayesian Information Criterion (BIC) with edge-specific directional evidence derived from Shapley values. For each variable, an XGBoost classifier is trained to predict it from all other variables; TreeExplainer aggregates Shapley attributions across confidently predicted instances. These attributions are used to softly reduce BIC’s complexity penalty on edges with strong directional support, thereby helping hill-climbing search resolve within Markov‑equivalence classes. Experiments on ten benchmark networks (six to 76 nodes) across seven sample‑size regimes (700 total runs) show consistent improvements in oriented‑edge F₁ (5.6% relative over BIC, 20.9% over PC, 9.6% over GES) at the cost of a front‑loaded computational overhead from classifier training and SHAP aggregation.

## Strengths

* **Novel and principled combination.** Using local feature attributions to modulate a score‑based objective for discrete data is a creative bridge between explainability and structure learning. The idea is well‑motivated: BIC struggles with edge orientation, while Shapley values provide asymmetric, sample‑level signals that can break ties in Markov‑equivalence classes.  
* **Thorough empirical evaluation.** The paper evaluates on ten diverse networks with seven sample‑size regimes, comparing against three strong baselines (BIC‑HC, PC, GES). The aggregated results over 700 runs provide convincing evidence that the proposed soft‑weighting consistently improves directed‑edge recovery, especially at moderate‑to‑large sample sizes.  
* **Clear and reproducible methodology.** The three‑stage pipeline (train classifiers, compute Shapley values, hill‑climb with XBIC) is described with explicit algorithms, hyperparameter search spaces, and a released codebase. The method is a drop‑in replacement for BIC when directional evidence is weak, preserving standard BIC behavior by default.  
* **Theoretically grounded behavior.** The score retains BIC’s penalty order O(log N) when SHAP(G) is bounded, and exactly reduces to BIC when no attribution signal passes the confidence threshold. This ensures large‑sample consistency under standard regularity conditions.

## Weaknesses

### Fatal  
None.

### Major  

1. **Modest practical gains vs. high computational cost.** The headline F₁ improvement over BIC is 5.6% (absolute 0.04). While statistically significant, this is small in absolute terms. Meanwhile, Table 5 shows XBIC is often 50–200× slower than BIC (e.g., Asia: 0.39 s vs. 74.78 s; Win95pts: 75 s vs. 2139 s). For a “drop‑in upgrade,” this overhead is a serious barrier to adoption, especially in exploratory or large‑scale settings.  
2. **No principled way to choose the weight** ***w***. The paper sweeps w ∈ {1,2,3} and selects w = 2 based on aggregate results. In practice, without ground‑truth graph, a practitioner has no guidance on how to set this hyperparameter, and the optimal value likely depends on network structure and sample size. The method’s sensitivity to w (Figure 2) makes this a non‑trivial practical issue.  
3. **Limited theoretical justification for Shapley values as directional evidence.** The paper uses Shapley values computed from predictive classifiers as a proxy for causal directionality. There is no proof or formal argument that these attributions correspond to causal strength or that they are robust to confounding. The experimental results are encouraging, but the conceptual link between predictive importance and causal orientation remains heuristic.

### Minor  

* The confidence threshold τ used in the main experiments is not explicitly stated; only a range (0.7–0.95) is mentioned.  
* The definition of “relative improvement” in Table 4 is absent (presumably (XBIC – baseline)/baseline).  
* The comparison with GES is weakened by the fact that GES often failed to finish, forcing evaluation on only a subset of runs where it completed. While this is noted, it introduces a selection bias that is not fully addressed.  
* Runtime in Table 5 for Hailfinder shows PC at 15923 s, which seems anomalously high and may indicate a suboptimal implementation; this warrants a brief comment.

### Trivial  
None.

## Nice-to-Haves  

* A practical heuristic for choosing *w* (e.g., via cross‑validation of the XBIC score itself or stability across runs).  
* A comparison with an alternative attribution method (e.g., LIME or permutation importance) to isolate whether the specific properties of Shapley values are key.  
* An ablation study that ablates the confidence filter to show its effect on accuracy versus SHAP evaluations.

## Novel Insights  

The paper demonstrates that local feature attributions from black‑box predictive models can be repurposed as a directional signal to improve score‑based causal discovery. This establishes a two‑way bridge between explainable AI and structure learning: instead of using causal knowledge to constrain explanations, explanations are used to inform causal search. The empirical results on discrete data suggest that even imperfect, sample‑level attribution signals can break Markov‑equivalence ties in a score‑based framework, providing a new perspective on how to handle the orientation problem.

## Suggestions  

1. Provide explicit guidance on selecting the weight *w* in practice—for example, by tracking the penalized log‑likelihood on a held‑out validation set or by using a small grid with stability selection.  
2. Report the default confidence threshold τ used in the main experiments and clarify whether it was fixed across all networks or tuned per network.  
3. Include a brief discussion of the computational cost in the context of offline vs. online use: for many medical or insurance analyses where sample collection is far more expensive than computation, the overhead may be acceptable.  
4. For the GES comparison, consider reporting results on the subset where GES completed and also provide a runtime–quality trade‑off analysis.

## Score and Decision  

The paper presents a novel, well‑evaluated integration of Shapley values into the BIC score for discrete causal discovery. The contributions are sound, the empirical evidence is substantial, and the methodology is clearly described. The main concerns—modest absolute gains, high computational cost, and lack of a principled way to choose *w*—are not fatal but temper the impact. On balance, the work represents a valuable step forward in discrete structure learning and merits acceptance.

MY FINAL SCORE: <score>7</score>  
MY FINAL DECISION: <decision>Accept</decision>