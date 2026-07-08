Now let me write the final consolidated review.

## Summary

This paper proves a first-order equivalence between activation steering and influence functions, showing that any steering vector can be mapped to a signed influence measure over training data and vice versa. The key contributions include: (i) a closed-form Influence-Aligned Steering (IAS) vector that maps parameter-space influence updates to activation-space edits; (ii) a geometric diagnostic $\gamma(x)$ (the cosine of the smallest principal angle between two Jacobian subspaces) that characterizes when steering can faithfully replace influence; (iii) a no-free-lunch bound showing steering is provably insufficient when $\gamma$ is small; (iv) spectral optimality for choosing steering directions under an $\ell_2$ budget; and (v) generalization bounds for low-rank steering interventions.

## Strengths

- **Novel theoretical connection between two previously disconnected research strands.** The primal-dual formulation (Section 3) elegantly frames activation steering and influence functions as projections of the same sensitivity tensor. This is a genuinely new contribution — the paper is the first to give a closed-form map between the two ideas and quantify when one subsumes the other. [weight=10.73]

- **The $\gamma(x)$ diagnostic and no-free-lunch bound (Theorem 6.2).** The result that when $\gamma(x)$ is small, *no* activation-space edit can achieve more than a $\gamma(x)$-fraction of the desired logit displacement gives a principled, theoretically grounded stopping rule for steering versus weight editing. This emerges naturally from the analysis rather than being ad hoc. [weight=9.05]

- **Closed-form constructive formulas.** The IAS vector $\Delta h^* = \mathbf{J}_{h \rightarrow y}^\dagger \mathbf{J}_{\theta \rightarrow y} \Delta \theta$ (Theorem 5.2) is a concrete, computable quantity that gives practitioners an explicit mapping from a parameter perturbation to a steering vector. The paper does not just assert an equivalence — it provides the computation. [weight=9.49]

- **Spectral optimality result (Theorem 5.3).** Showing that the top eigenvector of $\Sigma$ is the optimal steering direction under an $\ell_2$ budget provides a principled alternative to hand-crafted steering vectors, and the power-iteration recipe makes it implementable in practice. [weight=9.40]

## Weaknesses

### Fatal
None.

### Major

- **The linearity experiment's slope of 1.5 is a 50% unexplained magnitude discrepancy that the paper glosses over.** Section 7.2 reports that predicted vs. actual logit shifts have cosine 0.978 but slope 1.50, meaning the actual logit shift is **50% larger** than the first-order prediction. The paper describes this as "consistent with the expected linear regime" without explanation. If the first-order theory were quantitatively accurate at the tested magnitudes, the slope should be close to 1.0. The paper offers no analysis of whether this is due to the damping parameter $\lambda$, the Gauss-Newton approximation, or higher-order nonlinearities. While the directional alignment is strong (cosine 0.978), the systematic magnitude error undermines the quantitative claim of first-order equivalence and needs to be addressed — either by showing the slope approaches 1.0 as $\alpha \to 0$, or by identifying and controlling for the systematic factor, or by honestly reframing the claims as directional equivalence only. [weight=1.99]

- **The detoxification experiment (Section 7.1) shows IAS underperforming CAA without explanation, and the construction of the IAS vector is underspecified.** Table 1 reports that CAA achieves toxicity 0.0150 and perplexity 13291, while IAS achieves toxicity 0.0164 and perplexity 13701 — IAS is worse on *both* metrics. The paper reports this neutrally without any discussion. More critically, the setup says "Steering vectors are built from 50 toxic vs. 50 neutral Jigsaw prompts" but never describes *how* IAS uses these prompts differently from CAA. IAS maps from a *parameter perturbation* $\Delta\theta$ to an *activation perturbation*, so the source of $\Delta\theta$ must be specified — is it derived from influence-weighted parameter updates from the toxic vs. neutral prompts? This is a methodological gap that prevents reproducibility. [weight=1.52]

- **The spectral optimality experiment (Section 7.4) does not validate the claimed optimality.** Theorem 5.3 claims the top eigenvector of $\Sigma$ is the *optimal* steering direction under an $\ell_2$ budget, but the experiment only shows that this spectral direction has a significantly different spectral radius from random directions (p=0.00498). This demonstrates non-randomness, not optimality. The experiment does not show: (a) that steering with this direction actually increases the target logit, (b) that it outperforms any baseline steering method (random direction, mean activation difference, CAA analog), or (c) that the "optimality" guarantee holds in practice. [weight=0.87]

- **The promised "practical workflow" (Contribution 4) is not demonstrated.** The paper claims an integrated workflow — "steer first, trace provenance, edit weights only when the geometry demands it" — but no experiment demonstrates this end-to-end. The experiments are piecemeal: detoxification (steering only, with IAS worse than CAA), linear equivalence, $\gamma$ diagnostic (alignment by layer depth), and spectral directions (significance only). There is no case study showing: a practitioner identifies an undesired behavior, computes IAS to connect it to specific training examples, uses $\gamma$ to decide whether steering suffices, and acts on that decision. The paper mentions "see Section 7" for the practical payoff of Corollary 1, but Section 7 does not actually trace any steering vector back to causal training documents. [weight=0.27]

### Minor

- **The cost model is misleading.** The paper states "all results rely on... two Jacobian–vector or vector–Jacobian products per input," but this is accurate only for the IAS *mapping* itself. Computing the influence-derived parameter perturbation $\Delta \theta = -\epsilon \mathbf{H}_\theta^{-1} \nabla_\theta \ell$ requires either an explicit Hessian inverse (infeasible at scale) or an iterative solver (many backward passes). The paper should separate the cost of computing influence functions from the cost of the IAS mapping. [weight=4.53]

- **The experiments are thin relative to the scope of claims.** Three of four experiments (Sections 7.1, 7.2, 7.3) use GPT-2 Medium at layer 8 — a single model, layer, and task configuration. There are no ablation studies varying the damping parameter $\lambda$, no experiments with different model scales, and no comparison to weight-space editing baselines. The detoxification results (Table 1) are reported as point estimates without confidence intervals or significance tests. [weight=-0.98]

- **The detoxification results lack statistical characterization.** Results in Table 1 are point estimates without confidence intervals or significance tests. The difference between CAA (0.0150) and IAS (0.0164) may not be statistically significant, which would change how the comparison is interpreted. [weight=4.02]

### Trivial

- **The proof sketch for Corollary 1 ($\ell_1$-minimality) is not logically sound as written.** The argument claims: "if another measure $\nu$ achieved the same shift with smaller $\ell_1$ norm, one could scale $\rho_s$ down and still match the shift, contradicting the definition of $\alpha$." Scaling $\rho_s$ down would change the shift magnitude, not match a different measure. While the claim may be true under the affine-independence assumption, the provided proof sketch is insufficient. [weight=3.45]

## Nice-to-Haves

- A sensitivity analysis of the spectral direction with respect to the choice of training set, layer, and damping parameter $\lambda$.
- A concrete demonstration of the data-attribution pipeline (Corollary 1) — e.g., take a steering vector, compute $\rho_s$, and show the top-weighted training examples are causally related to the targeted behavior.
- Varying the steering magnitude $\alpha$ to show that the slope in Figure 1 approaches 1.0 as $\alpha \to 0$, confirming the first-order regime.

## Removed Points

- **Criticism about Eq. (2) sign inconsistency**: The sign of $\lambda^*$ depends on how the Lagrangian constraint is written (convention choice). While the formula in Eq. (2) appears to drop the $(JJ^\top)^\dagger$ term compared to Theorem 5.2, Theorem 5.2 itself gives the correct pseudoinverse expression. This is a minor presentation inconsistency, not a substantive error.
- **Criticism about abstract overclaiming on feasibility condition**: Abstracts are summaries; the paper's Section 2 explicitly states the feasibility assumptions.
- **Criticism about Theorem 6.1 being "standard"**: The Rademacher bound is a standard form, but its derivation for low-rank IAS corrections is specific to this paper's setting.
- **"Missing related works"**: Removed per policy — external sources cannot be verified.
- **"Missing appendix content"**: Removed per policy — the parser strips appendix content from all papers.
- **Weakness about the paper not checking feasibility condition $\text{Im}(\mathbf{J}_{\theta \rightarrow y}) \subseteq \text{Im}(\mathbf{J}_{h \rightarrow y})$ empirically**: The paper does check this via the $\gamma$ diagnostic (which bounds the residual when feasibility fails via Theorem 5.1). The subset containment is a sufficient condition for exact matching; the $\gamma$ bound accounts for violations.

## Novel Insights

The harsh critic's analysis surfaces a useful meta-observation: the paper's strongest theoretical contribution (the primal-dual equivalence) and its weakest experimental evidence (the slope=1.5 discrepancy) are linked. The core claim of first-order equivalence *necessarily* predicts a slope of 1.0 in the linearity experiment under the small-edit regime; the observed slope of 1.5 thus directly probes the validity regime of the theory itself, making this not merely an experimental sloppiness but a first-order check on the theory's practical domain of applicability. The harsh critic also correctly identifies that the spectral optimality experiment tests a necessary condition (non-randomness) but not a sufficient one (actual steering utility), which is a pattern that applies broadly to papers that claim empirical support for theoretically-derived quantities without running the actual downstream validation.

## Suggestions

1. **Resolve the slope=1.5 discrepancy.** This is the highest-leverage improvement. Vary the steering magnitude $\alpha$ and show the slope approaches 1.0 as $\alpha \to 0$, or identify the systematic factor (damping $\lambda$, nonlinearity of attention/MLP layers after the steering layer), or acknowledge the magnitude limitation and reframe claims to "directional equivalence."
2. **Specify the IAS construction in the detoxification experiment.** Describe what parameter perturbation $\Delta\theta$ is used and how the 50 toxic vs. 50 neutral prompts feed into it.
3. **Properly validate the spectral direction.** Show actual steering performance (logit changes) of the spectral direction against baselines (random direction, mean activation difference).
4. **Add a concrete data-attribution case study** — take a steering vector, compute $\rho_s$, and inspect the top-weighted examples.
5. **Provide confidence intervals for Table 1.**
6. **Clarify the cost model** by distinguishing the cost of computing influence functions from the cost of the IAS mapping.

## Score and Decision

### Calibration Report

**All anchors retrieved across rounds:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Hessian-Free Influence Functions | WT2bL7sCM1.md | 3.00 | R1 | Yes | Incremental contribution to influence functions, mostly rejected for lack of novelty. This paper has stronger theoretical novelty. |
| Steering → Conceptors | 9wjGUN65tY.md | 5.00 | R1 | Yes | Steering theory paper, rejected for limited experiments and clarity issues. Similar profile — strong theory, weak experiments. |
| ActAdd Activation Engineering | 2XBPdPIcFK.md | 5.00 | R1 | Yes | Mixed reviews (3,3,6,8). Simple effective method but novelty questions. This paper has deeper theory but worse empirical validation. |
| Effectively Steer LLM | ZPkNrs6aNO.md | 5.50 | R2 | Yes | Theory-driven steering paper rejected for limited baselines and weak empirical support. Closest structural match to this paper. |
| Temporal Data Influence | uHLgDEgiS5.md | 8.00 | R1 | Yes | Strong accept. Clean theory + thorough experiments. This paper's theory is comparably novel but experiments are much thinner. |

**Round 1 bracket:** After drafting the review and weighting all items (strengths 9.05–10.73, major weaknesses 0.27–1.99, minor weaknesses -0.98–4.53), the initial bracket was estimated at **3.5–5.5**.

**Round 2 narrowing:** Retrieved four additional anchors in the 4.0–7.0 range. The closest structural match is "Effectively Steer LLM" (score 5.5, rejected) — both have strong theoretical frameworks but significant gaps between claims and empirical evidence. Compared to that anchor:
- This paper has heavier theoretical strengths (weight 9–10.7 vs 7.75–10.6)
- This paper has more severe claim-evidence gaps (undemonstrated workflow, slope discrepancy, spectral non-validation)
- The weaknesses in this paper have lower (less negative) weights than in the 5.5 anchor, but this is likely because the model weights empirical gaps less severely than theoretical flaws

**Final score placement:** The paper sits at the boundary between the score-3.0 anchor (where weaknesses were primarily about flawed theory/novelty) and the score-5.5 anchor (where weaknesses were about empirical validation gaps). The theoretical contribution is genuinely stronger than either the 3.0 or the 5.0 anchors' contributions, but the empirical gaps are more numerous and more consequential for the practical claims. This places the paper at **5.0** — the theoretical core is worth engaging with and constitutes a real contribution, but the experiments do not adequately support the practical claims the paper makes, and several findings (slope=1.5, IAS < CAA) actively contradict what the theory would predict.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>