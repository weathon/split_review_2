## Summary
# Final Review Report

## Summary

This paper studies the phenomenon of *training loss curve (TLC) collapse* — where normalized loss curves from different model sizes align onto a universal trajectory — in the context of large language model (LLM) families trained with practical scaling recipes. The authors identify three key controls that govern TLC shape under maximal update parameterization (μP): the AdamW timescale τ, the tokens-per-parameter ratio (TPP), and the learning-rate schedule. They demonstrate that when τ is set optimally for a given TPP and held fixed across model sizes, normalized TLCs collapse across scales ranging from 100M to 3.9B parameters. The paper introduces the Celerity LLM family, trained with fixed TPP bands (20, 80, 234) and optimal τ, showing competitive accuracy on the compute-efficiency frontier. Two practical applications are presented: (1) deviation-from-collapse as an early diagnostic of training pathologies (detecting a numerical kernel issue ~30% earlier than raw loss inspection), and (2) a parametric surrogate model for normalized TLCs that enables early stopping in hyperparameter tuning (selecting optimal hyperparameters after 10–30% of training). The paper is clearly written, the experimental methodology is rigorous, and the findings have practical significance for LLM pre-training at scale.

**Research value:** The paper provides a principled understanding of what controls TLC shape during LLM training and offers practical tools (diagnostics via collapse residuals, early stopping via surrogate models) that can reduce the cost of large-scale training. The Celerity family serves as a useful benchmark for compute-efficient pre-training. The main limitations are: (1) the diagnostic application is demonstrated for only one specific numerical issue, (2) the TPP trade-off analysis relies on power law exponents from prior work without empirical validation in this setting, (3) the \$1B-run extrapolation in the conclusion is unsupported, and (4) novelty relative to prior work (Qiu et al. 2025) could be sharpened with explicit discussion of normalization differences.

## Strengths
**1. Clear identification of TLC shape controls.** The paper identifies three specific, testable factors (τ, TPP, LR schedule) that govern normalized TLC shape under μP. This is a useful conceptual advance beyond prior work, which either treated TLCs as monolithic or focused only on final loss prediction. The experiments in Section 3 cleanly isolate each factor by sweeping one hyperparameter (η, λ, or B) while keeping τ matched.

**2. Practical demonstration of collapse at LLM scale.** While Qiu et al. (2025) showed collapse only for small-scale autoregressive tasks with vanilla Adam, this paper extends the finding to LLM families (100M–3.9B parameters) trained with AdamW and weight decay under practical scaling recipes. The Celerity family provides a concrete instantiation with documented hyperparameters, enhancing reproducibility.

**3. Novel diagnostic application.** The use of collapse residuals for early detection of training issues is a practical innovation with clear operational value. The case study (1.8B run with numerical kernel bug) convincingly shows that residuals can flag problems ~30% earlier than raw loss inspection, potentially saving substantial compute time in large runs.

**4. Principled early stopping framework.** The proposed procedure for hyperparameter selection from partial training runs (exploiting collapse) is well-motivated and supported by experiments showing that the "predicted best" method achieves negligible loss gaps after only 10–30% of training. The use of a parametric surrogate (Eq. 4-5) to avoid re-training small models for each HP setting is a practical contribution.

**5. Clear writing and exposition.** The paper is well-structured, the notation is consistent (Table 1 is useful), and the key findings are summarized in "Key takeaway" boxes that help readers navigate the contributions. Figures are informative and support the narrative.

## Weaknesses
### W1. Normalization discrepancy with prior work not adequately explained [Major]
The paper uses a simpler normalization than Qiu et al. (2025) — dividing by final training loss ($\hat{L}=0$) instead of affine rescaling with an irreducible loss offset — but does not adequately justify this choice. The text states this was found empirically to give "optimal alignment across scales" (Sec. 3, experimental setup), but provides no theoretical or empirical analysis of *why* this works or when it might fail. Since language modeling has non-zero irreducible loss (entropy of natural language), setting $\hat{L}=0$ is technically incorrect; the paper should discuss why this approximation is valid for their setting. This gap weakens the claimed connection to prior supercollapse theory. *(See Annotation 6)*

**Fix:** Add an analysis of how the choice of $\hat{L}$ affects collapse quality. Show that at the TPP and compute scales studied, $L(T) \gg \hat{L}$ or $\hat{L} \propto L(T)$, making the offset approximately cancel. Discuss conditions under which this approximation could break down (e.g., very high TPP or small models where final loss approaches irreducible loss).

### W2. Scale-invariance assumption lacks empirical validation [Major]
The scale-invariance claim (Sec. 3) relies on the assumption that "residual bias at end-of-training is negligible relative to the variance floor." This assumption is critical for collapse to hold across model sizes, but the paper provides no empirical check. If small models retain higher residual bias (because they converge less fully relative to their variance floor), collapse could degrade at smaller scales. The 20 TPP results (Fig. 6, left) already show "small early deviations" attributed to LR warmup differences, suggesting the assumption may not hold universally. *(See Annotation 8)*

**Fix:** Add empirical verification: (a) compute the bias-to-variance ratio at convergence for each model size (e.g., by comparing final loss to fitted irreducible loss), (b) demonstrate that this ratio is small and approximately constant across sizes, (c) identify settings (TPP, τ combinations) where the assumption is violated.

### W3. TPP trade-off analysis uses unvalidated power law exponents [Major]
The choice of TPP = 234 (62% parameter reduction for 67% extra FLOPs) is based on power law exponents from prior work (Hoffmann et al., 2022; Besiroglu et al., 2024). The paper does not validate that these exponents transfer to the Celerity setting (GPT2-like architecture, μP, SlimPajama data, specific τ choices). An error of ±10% in the exponent could change the compute cost estimate by approximately ±15%, potentially shifting the optimal TPP. *(See Annotation 9)*

**Fix:** Either (a) empirically validate the iso-loss trade-off by training models at 20 TPP and 234 TPP and comparing actual loss vs. FLOPs, or (b) add sensitivity analysis showing how recommended TPP varies with plausible ranges of power law exponents, and add a caveat that estimates rely on prior work.

### W4. "Pareto frontier" claim is overstated [Major]
Fig. 2 and the text claim Celerity models are on the "compute-efficiency frontier." This claim depends on: (a) which baselines are included/excluded, (b) how FLOPs are computed (the paper counts student FLOPs only for distilled models), and (c) the specific 7-task average. No error bars or confidence intervals are provided for the frontier position, and the fit line ("100 - 5 / (tau * 154e38)^-0.097") is a three-parameter curve fit to heterogeneous data without goodness-of-fit reporting. *(See Annotation 10)*

**Fix:** Provide bootstrap confidence intervals for the frontier, report task-wise variance, and clarify that the frontier refers to the set of open models evaluated (not all published LLMs). Add a caveat that different FLOPs accounting conventions (e.g., including data processing or inference cost) could shift relative positions.

### W5. Conclusion contains unsupported extrapolation and lacks limitations [Major]
The conclusion states "For \$1B runs, collapse provides a valuable reference trajectory" — but the largest model trained is 3.9B parameters (far below \$1B training cost), and no experiments at that scale are presented. This is an unsupported extrapolation. Additionally, the conclusion does not discuss any limitations or failure modes of the approach. *(See Annotation 13)*

**Fix:** Remove the \$1B claim or explicitly qualify it as speculation. Add a limitations paragraph covering: (a) diagnostic validated for one numerical issue only, (b) TPP trade-off depends on unvalidated power laws, (c) collapse assumes fixed LR schedule across sizes (many LLM families vary this), (d) experiments span up to 3.9B — scaling to >100B may reveal new challenges.

### W6. Unverifiable "first LLM family" claim [Minor]
The introduction claims Celerity is "the first LLM family trained with both optimal τ scaling and demonstrable TLC collapse." This priority claim is unverifiable without a comprehensive literature search; many families may have trained with fixed TPP without documenting it. The claim is not essential to the paper's contributions. *(See Annotation 5)*

**Fix:** Remove "first" or qualify as "to our knowledge, the first LLM family with documented TLC collapse and deliberate τ scaling."

### W7. Disconnect between early stopping procedure and surrogate model [Minor]
The 6-step early stopping procedure (Sec. 5) requires training a 100M model for each HP setting, which could be expensive for large sweeps. The surrogate model (Eq. 4-5) is then introduced as an alternative, but the procedure description does not mention it. This creates a structural disconnect. *(See Annotation 11)*

**Fix:** Restructure Section 5 to present the surrogate model as an integral part of the procedure (replacing steps 2-3), and quantify the cost savings.

### W8. Related work lacks differentiation from loss-prediction baselines [Minor]
The related work groups recent loss-prediction methods (Tissue et al., Luo et al., Schaipp et al., Hong & Wang) but does not explain how the proposed τ-centric surrogate differs mechanistically from or outperforms these approaches. *(See Annotation 12)*

**Fix:** Add one sentence per key baseline explaining the difference (e.g., "Unlike Tissue et al., we collapse LR and steps into the composite τ, reducing degrees of freedom from 3 to 1.") and, if available, comparative performance.

### W9. No discussion of when collapse might fail [Minor]
The paper presents collapse as a robust property of compute-efficient training, but never discusses conditions under which it might break down (e.g., highly suboptimal τ, non-fixed LR schedules, different optimizers, non-μP parameterizations). This limits the paper's scientific completeness. *(See Annotation 13)*

**Fix:** Add a paragraph (in Conclusion or as a new subsection in Section 3) discussing hypothesized failure modes and design experiments to test them.

### **External Literature Verification Note**
Due to the Retrieval-Disabled Mode (paper_search unavailable), all novelty/comparison conclusions in this review are based on manuscript-internal evidence only. External verification of claims relative to related work (especially the "first LLM family" claim, τ scaling novelty, and comparison with recent loss-prediction methods) requires manual follow-up by the authors or future reviews.

## Score
**Final Score: 7/10**

**Rationale:** The paper makes a genuine empirical contribution by extending training loss curve collapse from small-scale idealized settings to practical LLM families, and by identifying the specific controls (τ, TPP, LR schedule) that govern this phenomenon. The diagnostic and early-stopping applications are practical and well-demonstrated. The writing is clear and the experimental methodology is generally sound.

The score is reduced from a higher threshold due to several addressable weaknesses:

1. **Normalization discrepancy with prior work (W1):** The paper's simpler normalization is not adequately justified, weakening the connection to prior supercollapse theory. This is a missing piece of scientific argumentation rather than a fatal flaw.
2. **Unvalidated assumptions (W2, W3):** The scale-invariance assumption and the TPP trade-off analysis both rely on unverified premises that, if incorrect, could affect core claims.
3. **Overclaiming (W4, W5, W6):** The Pareto frontier claim, \$1B extrapolation, and "first LLM family" claim all need tighter bounding.
4. **Missing limitations (W5, W9):** The paper does not discuss failure modes or boundary conditions for collapse.

All identified weaknesses are fixable with additional analysis, caveats, and minor rewriting. The core contributions (identification of TLC controls, demonstration of collapse at LLM scale, diagnostic application, early stopping framework) are solid and represent a useful advance for the LLM pre-training community.

**Novelty assessment (deferred — external literature verification unavailable):** Due to Retrieval-Disabled Mode, novelty claims relative to external literature (particularly the "first LLM family" claim and comparison with recent loss-prediction methods) could not be independently verified. Authors should strengthen related-work positioning with explicit comparisons to nearest-neighbor approaches. The open-literature verification status does not affect the paper's manuscript-internal evidence quality.