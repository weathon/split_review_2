Now I have all the information I need. Let me compile the final review.

## Summary

This paper proposes STNAdam, a stochastic two-track Nesterov-accelerated adaptive momentum optimizer for solving "nonconvex + weakly-convex" composite optimization problems. The key algorithmic novelty is maintaining two intertwined iteration trajectories — an extrapolation track and a regular update track — governed by Nesterov momentum and Adam-style adaptive conditioning. The paper provides a KL-based convergence theory accommodating arbitrary variance-reduced gradient estimators (SGD, SAGA, SARAH, SPIDER) and evaluates the method on low-light image enhancement (LIE) using the LOL dataset.

## Strengths

- **A genuinely novel algorithmic template.** The two-track framework (Algorithm 1) — maintaining separate extrapolation (x̃^{k+1}) and regular update (x^{k+1}) trajectories governed by Nesterov momentum and Adam-style adaptive conditioning interactively — is structurally distinct from single-track methods like NAdam, SNAdam, or Adam itself. This is not a trivial coefficient modification; it is a real algorithmic design choice worth investigating.

- **General convergence theory that accommodates arbitrary variance-reduced gradient estimators.** Lemma 1 characterizes a broad class of estimators (SGD, SAGA, SARAH, SPIDER) under a unified set of conditions (MSE bound, geometric decay, convergence of estimator), and the theory is built on this abstraction. The KL-based convergence (Theorem 2) with explicit rates parameterized by the KL exponent is a nontrivial theoretical contribution.

- **Substantial empirical margins on the LOL dataset.** STNAdam-SARAH achieves PSNR 22.26 versus SNAdam 17.14 and Retinex-Net 18.44 (Table 2). The joint denoising results (Table 3, PSNR 20.91 vs. 17.14 for Retinex-Net on Wardrobe) show consistent multi-dB improvements that are unusual in low-light image enhancement.

## Weaknesses

### Major

1. **The LIE model likely violates the paper's own weakly-convex assumption.** The paper's convergence theory assumes g is weakly-convex with modulus τ > 0 (line 25). The experimental model (14) uses the term h‖∇L‖_{1/2}^{1/2} — the ℓ_{1/2} quasi-norm raised to the 1/2 power, which equals ∑|(∇L)_i|^{1/2}. The function φ(t) = |t|^{1/2} is not weakly convex in the standard sense: its second derivative diverges to -∞ as t → 0, which no finite quadratic regularization (adding (τ/2)‖·‖²) can compensate. The paper asserts at line 25 that the ℓ_{1/2}-norm is an example of a weakly-convex regularizer, but this claim is itself questionable, and the term actually used in experiments (‖·‖_{1/2}^{1/2}) is even further from satisfying the assumption. This creates a fundamental disconnect between the theory and the experiments: the empirical success may not validate the convergence guarantees, and the theory's assumptions may not hold in the tested setting.

2. **No ablation isolates the claimed contribution of the two-track mechanism.** The paper attributes STNAdam's performance to its two-track framework (Contribution i), but the comparisons against SGD, SAdam, and SNAdam conflate multiple differences simultaneously: two-track vs. single-track structure, variance-reduced vs. plain gradient estimators, and dynamic hyperparameter scheduling vs. fixed parameters. STNAdam-SGD vs. SGD compares two-track+Adam+dynamic-scheduling against plain SGD; STNAdam-SGD vs. SNAdam compares two-track+SGD-gradients against single-track+Adam-gradients. Without an ablation that turns off only the extrapolation track while keeping all other components identical, there is no evidence that the two-track mechanism specifically drives the reported gains.

3. **Citation and baseline identification errors undermine comparison credibility.** (a) "SAdam" is cited as (Kingma & Ba, 2014) in both the contribution list (line 50) and the experiment section (line 281), but Kingma & Ba proposed Adam, not SAdam — the paper's own related work (line 33) correctly attributes SAdam to Le-Duc et al. (2024). (b) "SNAdam" is cited as (Xie et al., 2024) in the experiments (line 281) and contributions (line 50), but the related work (line 33) attributes SNAdam to Reddi et al. (2019) and SAdan to Xie et al. (2024). A reader cannot determine which algorithm was actually implemented as the baseline.

4. **Evaluation is too narrow to support the claimed generality.** The paper's title frames STNAdam as a general optimizer for "nonconvex + weakly-convex composite optimizations," but the empirical evaluation is limited to a single application (LIE) using a single dataset (LOL). There are no results on standard deep learning benchmarks (e.g., CIFAR-10/100 classification with ResNet, language modeling, or any neural network training task). The comparisons against LIE-customized algorithms (NPE, DeHz, LIME, Retinex-Net, LR3M) further conflate model quality with optimizer quality, as these methods optimize different objective functions. For an optimizer paper claiming broad applicability, this evaluation scope is insufficient.

### Minor

5. **Abstract overstates the convergence guarantee proven in the main text.** The abstract (line 9) states that STNAdam "almost surely converges to a stationary point," but Theorem 1(ii) proves convergence "in expectation" (line 263). The conclusion (line 336) also states convergence "in expectation." These are different modes of convergence — "in expectation" is strictly weaker than "almost sure." While Lemma 4 establishes some almost-sure properties for auxiliary quantities (e.g., ‖x̄^k - x̄^{k-1}‖ → 0 a.s.), the paper's central convergence theorem for the iterate sequence is stated in expectation, not almost surely.

6. **Inconsistent notation between the deterministic description and the algorithm.** The TNAdam description (Figure 1, line 81) defines the extrapolation point as x̄^{k+1} = λ_{k+1} x^k + (1 - λ_{k+1}) x̂^k, where x̂^k is never defined. Algorithm 1 (line 105) uses x̃^k instead of x̂^k. While Algorithm 1 is self-consistent, this discrepancy between the illustrative description and the actual pseudocode would confuse a reimplementer.

7. **Unclear runtime reporting.** The "Time(s)" column in Tables 2 and 3 reports values on the order of 10⁻⁵ seconds for all methods without specifying whether these are per-iteration times, per-image times, or total time to convergence. STNAdam-SARAH, which requires two proximal gradient operations per iteration plus variance-reduced gradient computation, reports a lower time (2.64e-05) than SGD (2.85e-05), which is counterintuitive if these are total wall-clock times.

### Nice-to-Haves

- Add standard deep learning benchmarks (CIFAR classification with ResNet, or a language modeling task) to support the claim of generality.
- Conduct an ablation that removes the extrapolation track (x̃) while keeping variance reduction and dynamic scheduling identical, to isolate the two-track mechanism's contribution.
- Verify the weakly-convex condition for the ‖·‖_{1/2}^{1/2} term or replace it with a provably weakly-convex regularizer.
- Correct the SAdam and SNAdam citations to match the literature.
- Report total wall-clock time to convergence rather than (or in addition to) per-iteration timing.

### Removed Points

The following points from the input review were removed with justification:

- **Appendix-dependent theoretical quantities**: The reviewer criticized key coefficients (A_i, M, H, Z, D) being deferred to the appendix. The PDF parser strips appendix sections from all papers; these details exist in the original submission. **Removed per hard rules.**
- **Missing comparisons against AdamW, Lion, AdaBelief, Schedule-Free**: Requesting additional baselines beyond the paper's stated comparison set is a nice-to-have, not a core weakness.
- **Missing hyperparameter details and tuning protocol**: The paper states implementation details are in the appendix (stripped by parser). **Removed per hard rules about appendix stripping.**
- **Notation presentation issues in the energy function**: The complexity of the energy function (9) is inherent to the analysis approach, not a flaw. The paper clearly states which quantities are defined in the appendix.

### Novel Insights

None beyond the paper's own contributions. The two-track framework is genuinely interesting but the current evaluation cannot substantiate whether the mechanism itself drives the empirical gains.

### Suggestions

1. Conduct a controlled ablation: STNAdam without the extrapolation track (x̃), keeping variance reduction and dynamic scheduling, compared against full STNAdam.
2. Either prove (or cite a proof) that the ℓ_{1/2}^{1/2} term satisfies weakly-convexity, or replace it with a regularizer that provably does.
3. Add results on at least one standard ML benchmark (e.g., CIFAR-10/100 with a ResNet, or a language modeling task) to support the claim that STNAdam is a general-purpose optimizer.
4. Correct baselines: cite SAdam as Le-Duc et al. (2024) and clarify whether SNAdam follows Reddi et al. (2019) or Xie et al. (2024).
5. Clarify whether "Time(s)" is per-iteration or total time, and report convergence plots or total wall-clock time.

### Score and Decision

**Calibration anchors used (all rounds):**

| Anchor Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| mEBSeSk49H.md (Adam under Non-uniform Smoothness) | 4.25 | R1 | Yes | Pure theory with proof errors; our paper has stronger algorithm novelty but similar theory-experiment gap |
| DIAaRdL2Ra.md (Convergence of Adafactor) | 5.00 | R1 | Yes | First Adafactor analysis; our paper has more novel algorithm but narrower eval |
| Fj6Yv5rPRe.md (Online learning meets Adam) | 4.25 | R1 | Yes | Theory with correctness concerns; comparable overall quality |
| rIJbFQ1zII.md (Adam for Bilevel Optimization) | 5.25 | R2 | Yes | Solid theory + multiple tasks; our paper's eval is substantially narrower |
| YwJkv2YqBq.md (Nesterov acceleration benignly non-convex) | 6.75 | R2 | Yes | Strong theory accepted paper; our paper has more significant experiment-theory gaps |
| BZrSCv2SBq.md (Adam with Adaptive Batch Selection) | 6.67 | R2 | Yes | Good theory + experiments, accepted; our paper has narrower eval and assumption issues |
| 2KWZjdFwmh.md (StEVE: Kronecker-Factored Eigenbasis) | 4.25 | R3 | No | Similar optimizer variant paper with mixed scores |
| CVldG5ohCy.md (Adam through a Second-Order Lens) | 4.00 | R3 | No | Adam variant with limited evaluation; similar tier |

**Bracketing:** Round 1 established a plausible range of 3.5–5.5. Round 2 narrowed to 3.5–5.0 by comparing against the bilevel Adam paper (5.25) — our paper has a more novel algorithm but narrower evaluation and a more fundamental assumption gap. Round 3 confirmed 4.0 as the appropriate anchor.

**Final placement:** The paper sits near the 4.0 anchor (CVldG5ohCy.md) because both share: (a) a genuinely novel algorithm idea paired with (b) limited evaluation that doesn't adequately support the claimed scope. Favored items (two-track novelty, general VR-estimator theory, strong LIE margins) are comparable to that anchor's strengths, while the most damaging item (narrow evaluation) and the assumption-experiment gap are comparable severity. The Adafactor paper (5.00) has better-supported theory despite restrictive assumptions, placing it slightly above our paper. Our paper is below the bilevel Adam paper (5.25) because that paper evaluated on multiple tasks while ours tests only one dataset.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>