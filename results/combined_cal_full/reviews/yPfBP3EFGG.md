## Summary

This paper proposes STNAdam, a stochastic optimizer that combines Nesterov acceleration with Adam-style adaptive learning rates through a novel "two-track" iteration framework: one track performs a regular update while the other performs an extrapolation update, with parameters dynamically scheduled. The authors provide a convergence analysis under the Kurdyka-Łojasiewicz (KL) property that accepts any variance-reduced gradient estimator (SGD, SAGA, SARAH, etc.), and evaluate on low-light image enhancement (LIE). The core algorithmic idea is genuinely different from single-track Nesterov or Adam variants.

## Strengths

- **Conceptual novelty of the two-track framework** (Section 2, Algorithm 1, Figure 1). Maintaining two coupled iteration trajectories — one extrapolation track and one regular update track, governed by Nesterov momentum and Adam-style adaptive conditioning — is a genuinely different architectural idea from standard single-track Nesterov or Adam variants. This two-track mechanism is the paper's primary algorithmic contribution.

- **Generality of the convergence analysis** (Section 3, Lemmas 1–5, Theorems 1–2). The proof framework accepts any variance-reduced gradient estimator (SGD, SAGA, SARAH, SVRG, SPIDER) under a unified set of conditions (Lemma 1). The convergence rates in Theorem 2 are explicit in terms of the KL exponent, and the Lyapunov/energy function construction is mathematically elaborate. The analysis meaningfully advances theory for the "nonconvex + weakly-convex" problem class.

- **Clear and structured presentation.** The paper provides a helpful paired notation table (Table 1) distinguishing full-gradient and stochastic-gradient quantities, a visual trajectory comparison (Figure 1), and a step-by-step convergence analysis organized into lemmas. The algorithmic framework is laid out transparently.

## Weaknesses

### Fatal

None.

### Major

- **Abstract overclaims convergence mode.** The abstract states the sequence "almost surely converges" to a stationary point, and the contributions section (line 44) also claims "almost-sure global convergence." However, the central Theorem 1(ii) proves convergence "in expectation." Lemma 4 does establish some almost-sure properties (sum of squared differences converges a.s., distance to accumulation set goes to 0 a.s.), but the main convergence claim about reaching a stationary point is proven in expectation, not almost surely. The abstract and contributions section should match what is rigorously proven.

- **Experimental evaluation is limited to one specialized application.** The paper proposes a general-purpose stochastic optimizer but evaluates it exclusively on low-light image enhancement (LIE). Standard deep learning benchmarks that are routine for optimizer papers (e.g., image classification, language modeling) are absent. The paper's motivation mentions "the complexities of modern deep learning tasks" (line 17) and "massive network parameters and data sets" (line 15), but the single-task evaluation does not support the claim that STNAdam handles these complexities. The LIE task itself is valid, but the evaluation scope is too narrow for the claimed generality.

- **Uncontrolled comparison against task-specific algorithms.** The LIE-specific baselines (NPE, DeHz, LIME, Retinex-Net, LR3M) are separate methods with their own models and architectures, not instances solving the same optimization problem (14). Comparing STNAdam-SARAH against these methods conflates model architecture effects with optimizer performance. The controlled comparison against SGD, SAdam, and SNAdam (all applied to the same model) is valid, but the paper draws most of its superiority claims from comparing against the task-specific methods. The 5+ dB PSNR gap over the best optimizer baseline (SNAdam at 17.14 vs. STNAdam-SARAH at 22.26) may partly reflect different models or preprocessing rather than optimizer quality.

- **No error bars or variance reporting.** All results in Tables 2 and 3 are single point estimates with no standard deviation, confidence intervals, or replication information. For stochastic optimization, single-run results are not statistically informative.

### Minor

- **Parameter update intervals reference constants not readily computable from problem data.** The intervals (6)–(8) for γ_{k+1}, λ_{k+1}, α_{k+1} involve constants M, H, Z, D, s, V₁, V_T, ρ. The paper describes M, H, Z, D as "parameters within some certain intervals" (line 204) and references Lemma A.1 in the Appendix, but does not specify in the main text how a practitioner would determine these values. Remark 3's justification ("appropriately increasing L and τ if necessary") is vague. This makes the claimed "dynamic scheduling, removing hand-tuning" (line 48) difficult to realize as described without consulting the appendix or solving an auxiliary system.

- **Proximal operator ambiguity with vector-valued step size.** Algorithm 1 calls P_g with α/(√π̂_{k+1}+ε) as the third argument. Remark 1 defines P_g(x, y, t) with scalar t (involving 1/(2t)‖u−x‖²). In Adam-style algorithms, √π̂_{k+1} is a per-coordinate vector. Whether a scalar step size or element-wise operation is intended is unclear, and the convergence analysis would need to account for this distinction.

- **SAdam misattributed in experiment section.** Line 281 attributes "SAdam (Kingma & Ba, 2014)" — but Kingma & Ba proposed Adam, not SAdam. The related work section correctly identifies SAdam as from Wang et al. (2019) and Le-Duc et al. (2024). This inconsistency raises questions about whether the SAdam baseline was correctly implemented.

- **"Randomly select" instruction underspecified.** Algorithm 1 Step 3 says to randomly select γ_{k+1}, α_{k+1}, λ_{k+1} within updated intervals. The paper does not specify the random distribution (uniform? some other distribution?), making this step underspecified for exact reproduction.

- **Timing data lacks clarity.** Per-iteration times of ~2–8×10⁻⁵ seconds are reported without specifying what is being timed (per-iteration? total elapsed? on what hardware? batch size?). Without this context, the timing numbers are difficult to interpret or compare across methods.

### Trivial

None.

## Nice-to-Haves

- Include convergence curves (loss vs. iterations) for the LIE experiments. For an optimizer paper, the learning trajectory is essential to assess convergence behavior and stability.
- Run a controlled ablation isolating the two-track mechanism: compare STNAdam against a single-track version with all other components identical, to directly attribute gains to the two-track innovation.
- Investigate sensitivity to the key parameters μ (which has a theoretical bound of 1/√2) and ν.
- Compare different gradient estimator variants (SGD, SAGA, SARAH) within STNAdam on a standard benchmark.

## Removed Points

These points from the input review were removed with justification:
- "Suspect 5 dB gap is implausible" — Removed as speculative; the reviewer asserts implausibility without evidence of different model capacity or preprocessing. The gap could be real; no factual error in the paper supports the claim.
- "No hyperparameter details" — Removed per rule about missing appendix sections; the paper states details are in the appendix.
- "Missing related works (Reddi et al., Adam divergence)" — Removed per rule about not mentioning missing related works.
- "No analysis of adaptive learning rate behavior / sensitivity analysis" — Removed as scope-creep nice-to-haves, not core flaws.
- "Pure formatting/style nitpicks" — Removed per formatting rules.
- "The paper does not engage with literature on Adam convergence" — Removed per rule about missing related works.
- Several other speculative or category-driven concerns from the sweep — Removed for lacking concrete anchor in the paper.

## Novel Insights

None beyond the paper's own contributions. The two-track framework and its general convergence analysis are the paper's stated novelty, and the reviews do not surface unrecognized implications that the paper itself does not discuss.

## Suggestions

1. **Correct the abstract** to state "converges in expectation" (matching Theorem 1) or provide the missing proof for almost-sure convergence.
2. **Provide concrete guidance** for setting the constants M, H, Z, D (or reformulate the parameter selection to depend only on known problem constants L, τ, etc.) so the algorithm is implementable as specified.
3. **Run controlled optimizer comparisons** on at least one standard deep learning benchmark (e.g., CIFAR image classification with a fixed ResNet architecture) to support the claim of general-purpose utility.
4. **Report error bars** from multiple random seeds.
5. **Clarify the timing measurement** (per-iteration? total? hardware? batch size?) and the SAdam baseline implementation details.
6. **Specify the random distribution** used for parameter selection in Algorithm 1.
7. **Clarify whether the proximal operator** is applied element-wise or with a scalar step size when √π̂_{k+1} is a vector.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>