## Summary

This paper proposes HiSo, a federated zeroth-order optimization method that uses a learned diagonal preconditioner (built from squared ZO gradient estimates communicated as scalars) to accelerate convergence while preserving the dimension-free (scalar-only) communication property of ZO-FL methods. The paper presents a generalized scalar-only communication framework, theoretical convergence analysis showing rate improvements under a "well-approximated" Hessian condition, and LLM fine-tuning experiments (OPT-125M to OPT-2.7B) demonstrating 1.4–5.4× speedup in communication rounds over the DeComFL baseline.

## Strengths

- **Generalized scalar-only communication framework (Section 3.3).** The insight that scalar-only communication follows from the representation of updates (scalar + seed) rather than from ZO-SGD specifically is cleanly articulated and decouples a design constraint that was implicit in prior work (DeComFL). This enables a broader class of algorithms within the dimension-free regime.

- **Zero-extra-communication Hessian-like preconditioner.** The mechanism of building a diagonal preconditioner (Eq. 12) from already-communicated Δx values — which must be stored for model reconstruction anyway — is elegant and well-motivated. No additional function evaluations or communication are required.

- **Theoretical extension to τ > 1 local updates (Corollary 3).** The paper correctly identifies that DeComFL's convergence analysis does not cover multiple local steps, and shows that HiSo can maintain dimension-independent rates in this setting under the well-approximated condition. This is a genuine theoretical advance over the state of the art.

- **Communication cost reductions are striking.** Tables 2 and 3 show KB-level total communication for HiSo versus TB-level for first-order methods and GB-level for FedZO. Even accounting for accuracy gaps on some tasks, the savings are practically significant for bandwidth-constrained federated LLM fine-tuning.

- **Empirical evaluation across multiple model scales and tasks.** Results span OPT-125M, OPT-350M, OPT-1.3B, and OPT-2.7B on SST-2, QQP, and SQuAD, with consistent convergence speedups over DeComFL.

## Weaknesses

### Fatal

None.

### Major

- **The core theoretical claim of dimension-free convergence depends on an unverified condition (the "well-approximated condition," Definition 17).** Corollary 1's rate of O(√ζ/mR) — the key dimension-free result — is conditional on H satisfying Tr(H^{-1/2}ΣH^{-1/2}) ≤ ζ (a quantity independent of d). The paper acknowledges (Section 5.2 Remarks) that *"it is hard to determine if this approximation holds in the context of LLMs."* The only supporting evidence is a synthetic simulation (Fig. 4, left) with 200 log-normal eigenvalues — not actual LLM Hessians, and not using the actual HiSo H update rule. More critically, the paper does not provide a mechanism or argument for why squared ZO gradient estimates (Eq. 12) would approximate the true Hessian in the sense of Eq. 17. The empirical speedups could plausibly come from adaptive scaling (RMSProp-style) rather than curvature correction, and the theory does not distinguish these mechanisms. The paper's own fallback — that *"at worst case, [HiSo] degenerates into DeComFL"* — is a safe bound but does not validate the stronger claim.

- **Missing a ZO-adaptive baseline (ZO-RMSProp/Adam within the same scalar-only framework) prevents isolating the source of improvement.** The paper compares against DeComFL (unadapted ZO-SGD), FedZO, and first-order methods. Since HiSo's H update (Eq. 12) is structurally identical to RMSProp's running average of squared gradients (as the paper's own Footnote 2 acknowledges), a ZO-RMSProp baseline implemented within the same scalar-only framework would directly test whether the benefit is due to curvature-aware preconditioning or simply adaptive scaling. This experiment goes to the core of what the paper claims. Without it, the empirical results underdetermine the mechanism.

- **The convergence metric in Theorem 1 is the weighted gradient norm ‖∇F(·)‖_{H^{-1}}², not the unweighted norm.** This is a non-standard metric: a small value of ‖∇F‖_{H^{-1}} could arise from large entries in H (small preconditioner inverse) even if the actual gradient ‖∇F‖ is large. DeComFL's theory targets the unweighted gradient norm. The paper should discuss what this metric choice implies for the strength of the convergence guarantee.

### Minor

- **The "Hessian-informed" framing overstates the relationship to second-order information.** The paper consistently uses "Hessian-informed" in the title, abstract, and introduction, but Footnote 2 acknowledges the method *"resembles RMSProp as it currently is without a momentum term."* The diagonal preconditioner H is constructed from squared ZO gradient estimates (Eq. 12), not from actual second-derivative information. While the paper provides footnotes clarifying this, the overall narrative creates an expectation of curvature exploitation that the algorithm does not fully deliver. The framing should be brought into alignment with what the method actually does.

- **The speedup metric in Table 2 is non-standard and potentially favorable to HiSo.** The metric is: rounds for DeComFL to fully converge ÷ rounds for HiSo to *match DeComFL's best test accuracy*. This does not capture whether HiSo itself continues improving beyond DeComFL's plateau. A more neutral comparison would report rounds to reach a fixed target accuracy (within reach of both methods) or area under the accuracy-vs-rounds curve.

- **The number of local steps τ used in LLM experiments is not clearly specified.** The paper states *"We set P = 5 for all ZO methods"* in the LLM setup (line 301), but does not define P in relation to τ, which is the symbol used in the theoretical analysis (Corollary 3's key result concerns τ > 1). The experimental section should state τ explicitly for each experiment.

- **The large accuracy gap between HiSo and DeComFL on MNIST (Fig. 5, left: ~85% vs ~75%) warrants explanation.** On a simple dataset, such a gap suggests either DeComFL is not well-tuned or the Hessian-like preconditioning provides a qualitatively different optimization path. The paper states both methods were tuned with optimal learning rates but provides no learning rate grid or sensitivity analysis.

- **No analysis of computational overhead.** While computing H^{-1/2} for a diagonal H is O(d) and cheap, the paper never states this or compares the per-round computation cost of HiSo versus DeComFL. The additional operations (elementwise squaring, EMA update, preconditioned direction generation) should be quantified.

- **Interaction between model reset and Hessian state is under-specified.** Algorithm 1, line 13 says *"reset the model and other necessary states"* — if H is global state reconstructed from global scalars, this should be made explicit. If clients maintain local H estimates that are reset, the mechanism differs.

### Trivial

- Equation 12 appears twice (lines 140 and 174) with different subscript notation: first as |Δx_{r,τ}^{(i)}|² and later as [Δx_{r,0}]². This inconsistency should be cleaned up.

## Nice-to-Haves

- Empirical validation of the well-approximated condition on a small actual model (e.g., the MNIST CNN from Fig. 5, or OPT-125M on a subset of parameters) by estimating Tr(H^{-1/2}ΣH^{-1/2}) would significantly strengthen the core theoretical claim. The current synthetic eigenvalue simulation (Fig. 4) does not involve the actual algorithm and provides weak support.
- A ZO-RMSProp or ZO-Adam baseline within the same scalar-only framework, as noted in Major weaknesses.
- Reporting convergence to a fixed accuracy target (in addition to the current speedup metric) for Table 2.

## Removed Points

These points were removed from the input review as either factually incorrect, misunderstandings of the paper, or trivial formatting/style complaints:

1. **"Absorbing (u^T H^{-1} u)^{-1} into the learning rate changes the update direction"** — Factually incorrect. This term is a scalar; absorbing a scalar into the learning rate scales the step but does not change the direction, which remains H^{-1/2}u.
2. **"Random seed communication means it's technically more than scalar-only"** — The seeds are distributed by the server (downlink) and are integers, which are scalars. This is not a meaningful deviation from the claimed scalar-only property.
3. **"Missing appendix content and proofs"** — Appendices are stripped by the parser; they exist in the original submission.
4. **Generic related-work concerns and formatting nitpicks** — Removed per filtering guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a ZO-RMSProp baseline within the scalar-only framework to isolate whether gains come from adaptive scaling or curvature-aware preconditioning.
2. Validate the well-approximated condition empirically on a small model where the true Hessian can be estimated (e.g., the MNIST CNN).
3. Clarify the τ value used in LLM experiments and ablate over different τ values.
4. Discuss the convergence metric choice (weighted gradient norm) and its implications relative to the unweighted norm used in DeComFL's theory.
5. Recalibrate the framing to more accurately reflect that H is a diagonal preconditioner built from gradient information (RMSProp-style) rather than second-order curvature.

## Score and Decision

This paper addresses an important problem and makes several concrete contributions: the generalized scalar-only framework, the zero-extra-cost preconditioner construction, and the theoretical extension to multiple local updates. The empirical results consistently show improvements over the primary ZO baseline.

However, the paper's central theoretical claim — dimension-free convergence acceleration via Hessian information — rests on a condition (the "well-approximated condition") that is acknowledged as unverified for LLMs and for which only synthetic simulation evidence is provided. The missing ZO-adaptive baseline means the empirical acceleration cannot be attributed to curvature-aware optimization as opposed to simpler adaptive scaling. These two issues together create a meaningful gap between what is claimed and what is demonstrated.

The contributions are real and worthwhile, but the paper would benefit from either (a) validating the condition empirically, (b) adding the ablative baseline, or (c) reframing the claims more modestly as an adaptive ZO-FL method. In its current form, the gap between the Hessian-informed narrative and the evidence is too large for acceptance at a top venue, though the underlying algorithmic contribution is promising.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>