## Summary

This paper proposes the PRO-DYN nomenclature, a framework for categorizing components of time-series forecasting (TSF) models as either PRO (processing, operating within the input time interval) or DYN (dynamics, mapping from the input to the future time interval). Using Allen's interval algebra as a foundation, the authors analyze 15+ existing TSF models and identify two performance-driving features: (1) having a complete, learnable DYN function, and (2) placing that DYN function at the model's end (PRE-DYN configuration). These observations are validated empirically by adding linear DYN layers to under-performing models and converting well-performing models to DYN-first (post-processing) configurations, across 25 datasets with statistical significance testing.

---

## Strengths

- **Principled taxonomic framework:** The PRO-DYN nomenclature grounded in Allen's interval algebra provides a rigorous and systematic way to categorize model components. The derivation showing that LSTF-Linear models implement learnable linear dynamics (Eq. 2, Section 3.2) is crisp and illuminating.
- **Thorough empirical validation:** Experiments cover 25 datasets × 4 horizons = 100 configurations per model, with both MSE and MAE, Wilcoxon statistical significance testing, and careful ablations to isolate dynamics from confounds (parameter count, input length differences). The paper goes beyond correlation in Table 1 by actually perturbing models and measuring causal effects.
- **Performance driver analysis is careful:** Section 4.3 explicitly controls for the two main confounders (parameter count via PRO-added counterparts; input length via H>L/H=L/H<L conditioning), and the results generally hold even under adverse conditions for DYN models, which strengthens the main claims.
- **Broad model coverage:** RQ1 covers Transformer, CNN, and SSM backbones; RQ2 covers encoder-only, patch-based, and encoder-decoder variants. The diversity of evidence prevents the conclusions from being architecture-specific.

---

## Weaknesses

### Fatal
None.

### Major

- **"Dynamics" is loosely defined relative to its claim.** The paper equates learning a linear mapping W∈ℝ^{H×L} from past observations to future ones with "learning dynamics." In dynamical systems theory, dynamics refers to an evolution operator Φ, which for a proper dynamical system satisfies the semi-group property and is defined on state space—not on concatenated observation windows. The learned linear map is more accurately a direct multi-step regression. Calling this "dynamics" and concluding "dynamics is what you need" overstates the physical interpretation. The paper would be stronger if it either (a) justified why this linear map approximates a true evolution operator, or (b) softened the claims to "learnable temporal projection at the model end."

- **The Triformer anomaly is not adequately resolved.** Triformer is noted to have all "green" PRO-DYN features (checkmark in Complete learnable dynamics, PRE-DYN config, Linear DYN, Transformer PRO) yet falls in the underperforming group. The paper dismisses this with a single sentence in the conclusion ("results against NLinear and Triformer position suggest performance depends not only on dynamics but also on the choice of PRO functions"), which effectively concedes that the framework is insufficient to explain all observed variance. A more detailed analysis of what Triformer does differently would be valuable.

- **RQ2 experiment design is confounded.** Moving the linear DYN layer to the beginning and relabeling the original output linear as a PRO layer simultaneously changes: (a) where dynamics occurs, (b) the input to the main transformer block (now a predicted future sequence rather than a historical sequence), and (c) the interpretation of all intermediate computations. The paper correctly notes that vanilla models still outperform post-processing versions, but attributing this cleanly to "DYN position" vs. "main block receiving semantically different input" is not fully disentangled.

### Minor

- **MICN and FEDformer DYN remain below NLinear** (normalized scores: −0.164 and −0.360 vs. NLinear = 0). The improvement over vanilla is real but the models are still far from simple baselines, which weakens the practical takeaway.
- **FiLM DYN result is ambiguous.** Section 4.3 acknowledges that FiLM's DYN gain likely comes from parameter addition rather than dynamics, since the SSM itself already learns temporal evolution. This complicates the claim that "learnable dynamics is the key driver" for all four RQ1 models.

### Trivial
- The term "foundation models" is used for iTransformer, PatchTST, and Crossformer, which are not foundation models in the conventional sense (pre-trained on large diverse corpora).

---

## Nice-to-Haves
- It would strengthen the paper to test a non-linear DYN function (e.g., a small MLP mapping L→H) to verify whether linearity is essential or whether any learnable temporal projection suffices.
- Providing a dataset-level breakdown of when DYN additions help vs. hurt would illuminate the role of dataset domain in the underlying dynamics.

---

## Novel Insights

The paper's most genuinely novel contribution is formalizing, through Allen's interval algebra, the implicit architectural distinction that has been overlooked in the TSF literature: whether a model's learnable final prediction step is a temporal projection (DYN) or a within-window transformation (PRO). The insight that LSTF-Linear models succeed precisely because their single linear layer is, by construction, a DYN function—whereas Informer-style decoders initialized with zero-padding are not—is clean and retrospectively obvious but previously unstated. This reframing provides a useful design principle: deep backbone modules should serve as pre-processors for a learnable final temporal projection, not as post-processors refining a naive initial prediction.

---

## Suggestions

- Empirically test whether replacing the linear DYN function with a small autoregressive or MLP DYN function yields further improvements, to test the claim that dynamics expressiveness matters beyond mere learnability.
- Add a section analyzing why iTransformer is less sensitive to DYN position than PatchTST/Crossformer, as the temporal-dimension inversion in iTransformer provides a natural explanation worth making explicit.
- Clarify the distinction between "learning a dynamics" and "direct multi-step regression" to avoid overclaiming the physical interpretation.

---

## Score and Decision

The paper addresses a genuine and important question in TSF with a systematic, original framework and solid empirical evidence. The PRO-DYN nomenclature is a useful conceptual contribution, the experiments are thorough and statistically rigorous, and the conclusions are largely supported. The main concerns—loose use of "dynamics," the unresolved Triformer anomaly, and confounds in RQ2—are significant but not fatal; they reduce confidence but do not invalidate the core message. Given the quality of the analysis relative to typical papers at this venue, this paper sits at borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>