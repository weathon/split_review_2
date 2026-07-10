## Summary

This paper argues that diffusion models do not learn the statistical quantities (posterior, score, velocity field) they are assumed to learn in high-dimensional settings. The argument is built on two observations: (1) in high dimensions, the posterior p(x₀|xₜ) concentrates on a single training point, causing the fitting target of the objective to "degrade" from a weighted sum to a single sample; (2) existing inference methods can be unified within a "Natural Inference" framework that involves no statistical concepts. The paper provides no experiments with actual trained models to support its claims.

## Strengths

- **The frequency-domain interpretation in Section 3.3 (diffusion as progressive frequency completion) is clearly explained and visually illustrated**, tying training objectives to a spectral view of SNR-dependent frequency prediction. This provides an accessible narrative for how models behave across noise levels.

- **The attempted unification of sampling methods under a single "Natural Inference" framework in Section 4 is a useful organizational exercise** — it shows that DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, and DEIS can all be expressed as linear combinations of predicted x₀ values with signal and noise coefficient matrices satisfying magnitude constraints. As a descriptive taxonomy this is coherent.

## Weaknesses

### Fatal

- **The paper contains no experiments with actual trained diffusion models.** It claims that diffusion models "cannot effectively learn" statistical quantities and "operate via a different mechanism" (line 17), yet provides zero evidence about model behavior — no FID scores, no probing of learned representations, no training ablations, no comparison of predictions to ground-truth posterior means, no causal test linking the observed "degradation" to impaired generation quality. The only quantitative results (Tables 1, 2) characterize properties of the *training data* (the empirical posterior under a Dirac-delta approximation of p(x₀)), not the *model*. For a paper that claims to fundamentally overturn the standard understanding of how diffusion models work, this absence is decisive. Papers making comparable theoretical claims (e.g., the memorization-to-generalization transition paper avg 3.40, the "deficit of new information" paper avg 3.00) at minimum include controlled experiments; this paper does not.

### Major

- **The core "degradation" argument does not establish the claimed conclusion.** The reasoning (Section 3.2) is: posterior concentrates on one training point → fitting target degrades to a single sample → model cannot learn statistical quantities. This conflates two distinct things. First, the training objective min E[||f_θ(xₜ) − x₀||²] uses a Monte Carlo estimator that is unbiased regardless of how concentrated the posterior is at any given xₜ. Second, and more critically, if the posterior p(x₀|xₜ) *is* highly concentrated, the conditional variance is *low*, so using a single sample as an estimate of the mean produces *small* error — the opposite of what the paper claims when it says "using a single sample as an estimator of the mean, which typically have large error" (line 167). If anything, low-variance targets make learning *easier*, not harder. The paper provides no evidence that the learned function f_θ systematically deviates from the true posterior mean E[x₀|xₜ].

- **The analysis in Tables 1 and 2 is statistically weak and its implications are overstated.** The p > 0.9 threshold is arbitrary and unjustified. The near-1.0 rates at low t (t = 200, 300) are a trivial consequence of low noise (when Xₜ ≈ X₀, the closest point is necessarily the original). The claim that "the actual degradation ratio should be higher than the statistics show" (line 165) is unexplained and appears to misunderstand that the statistics already reflect the full empirical posterior. Most critically, the paper never tests whether this "degradation" metric actually correlates with any measurable impairment in model performance or generation quality.

- **The Natural Inference framework is an algebraic reformulation, not a demonstrated contribution.** Showing that existing samplers can be expressed as linear combinations of predicted x₀ values (Section 4.3) is a coherent exercise, but the paper presents no evidence that this perspective enables new methods, predictions, or insights. The "Self Guidance" concept (Section 4.1) relabels linear combinations of model outputs as guidance operations without proposing new mechanisms or showing improved performance. The paper acknowledges that optimal configurations "could be a direction for future work" (line 302), underscoring that the framework has not yielded practical advances. The repeated claim that this is "an entirely new and intuitive perspective" (line 27) is unsubstantiated.

### Minor

- **The frequency-domain interpretation (Section 3.3) characterizes the model as an "information enhancement operator" / frequency filter, but this description is not empirically tested.** No experiments show that model behavior aligns with this spectral view — it remains a plausible but untested narrative. Given that this interpretation is presented as the "different mechanism" through which diffusion models actually operate (Section 1), the lack of empirical grounding is a significant gap.

### Trivial

None.

## Nice-to-Haves

- A controlled experiment on synthetic data (varying dimensionality, known ground-truth posterior) directly testing whether "degradation" affects denoising accuracy or score estimation quality.
- Training a diffusion model and measuring whether its predictions f_θ(xₜ) systematically deviate from E[x₀|xₜ] (estimated via many Monte Carlo samples at each xₜ) in ways that correlate with the degradation metric.
- Using the Natural Inference framework to derive a genuinely new sampler that outperforms existing methods, rather than retrofitting existing ones.
- Probing learned representations to test whether they encode distributional information beyond nearest-neighbor lookups.
- Justifying or testing sensitivity to the arbitrary p > 0.9 threshold.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **"The paper asks a genuinely provocative question"** — Removed: generic strength about problem importance, not about the paper's concrete contribution.
- **"Tables 1 and 2 provide concrete statistics demonstrating that..."** — Removed: conflicts with verified weakness (the tables are substantively criticized); per rules, when a strength and weakness disagree, the weakness wins.
- **"Section 2 derivation is standard and not new"** — Removed: this criticizes the background section for containing standard material, which is expected; not a valid weakness.
- **"Section 3.1–3.2 posterior under empirical distribution"** — Removed: the paper explicitly acknowledges this (line 121: "the selection process can be considered as sampling from the following mixed Dirac delta distribution"); the critic's claim that the paper "treats this as a discovery about the true posterior" misreads the paper.
- **"No discussion of how diffusion models *do* work"** — Removed: the paper does offer the frequency-domain interpretation (Section 3.3) as an alternative mechanism; the critic is correct that it is untested, but not that it is absent.
- **"No comparison to existing theoretical work"** — Removed per hard rule: DO NOT mention missing related works.
- **Comments about missing appendix content** — Removed: appendix is stripped by parser; the original submission contains it.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a fundamental disconnect between the paper's strong claims and its purely data-side evidence, but this is a critique of the paper's framing, not a novel synthesis.

## Suggestions

The paper could be restructured as a short position paper or hypothesis piece, explicitly tempering the claims. To support the central thesis, the authors would need to (a) train diffusion models and show that their predictions deviate from ground-truth posterior means in ways that correlate with the degradation metric, (b) demonstrate that this deviation impairs generation quality, and (c) show that the Natural Inference framework enables new sampling methods or improves existing ones. Without such evidence, the current claims outrun the support.

## Score and Decision

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>