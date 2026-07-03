The calibration database has a persistent I/O error. I will proceed without calibration, using my best judgment against the ICLR scoring scale.

Let me now write the final review.

**Score reasoning**: This paper has genuine contributions — a generalized scalar-only communication framework that cleanly decouples from ZO-SGD, a preconditioned ZO-FL method that learns a diagonal preconditioner at zero extra communication cost, and convergence theory extending DeComFL to τ > 1. The empirical results show improvement over the primary ZO baseline. However, there are non-trivial weaknesses: (1) the headline speedup claim in Table 2 uses an asymmetric metric (different standards for the two compared methods), which systematically inflates the reported numbers, (2) missing comparisons against ZO versions of adaptive FL methods (ZO-FedAdam, ZO-FedYogi) make it unclear whether the benefit is from the specific Hessian-informed design or from generic per-coordinate adaptivity, and (3) the "Hessian-informed" framing overstates what is actually demonstrated — the H-learning rule is RMSProp-like and its connection to the Hessian is not empirically validated. The theoretical conditions are honestly caveated but unverified. These issues are addressable but in the current form weaken the paper's core claims. The paper falls between borderline reject and borderline accept — solid contributions but with evaluation and framing issues that need resolution.

Score: 5.0, Decision: Reject (borderline, with potential after major revisions).

Wait, let me reconsider. Actually the contributions are quite solid. Let me think about this more carefully.

The main issues:
1. Asymmetric metric - This is significant but not fatal. The paper could recompute and the speedup might still be positive, just smaller.
2. Missing ZO adaptive baselines - A real gap, but the comparison against DeComFL (the original scalar-only ZO-FL method) is the primary comparison.
3. Overclaiming "Hessian-informed" - The paper is transparent in footnotes, and the method does derive from Hessian-informed principles (Eqs. 5-10). This is a presentational issue more than a methodological flaw.

If I think about it, the paper's core contributions are:
- A generalized framework (Algorithm 1) that's a clear advance over DeComFL
- Integrating preconditioning into scalar-only ZO-FL
- Convergence theory for τ > 1
- Empirical improvements

These are meaningful contributions. The evaluation issues are real but fixable. I think this is closer to a 5-6 than a 4-5. Let me go with 5.5 — borderline accept territory, with the caveat that major revisions are needed to address the evaluation concerns.

Actually, I'll stick with 5.0. The asymmetric metric issue is significant for the paper's central empirical claim, and the missing baselines weaken the evidence. The paper needs real work to address these concerns.

Decision: Reject (with potential for acceptance after addressing the issues).Now I will produce the final consolidated review.

## Summary

This paper proposes HiSo, a Hessian-informed zeroth-order federated optimization method that uses a global diagonal preconditioning matrix to accelerate convergence while preserving scalar-only (dimension-free) communication. The paper contributes: (i) a generalized scalar-only communication framework (Algorithm 1) decoupled from vanilla ZO-SGD, (ii) a preconditioned ZO gradient estimator using H_r^{-1/2} with the preconditioner learned from squared scalar updates at zero extra communication cost, (iii) convergence analysis under a "low whitening rank" condition that extends beyond DeComFL to τ > 1 local updates, and (iv) LLM fine-tuning experiments showing 1.4×–5.4× round reduction over DeComFL.

## Strengths

- **Generalized scalar-only communication framework (Algorithm 1, Section 3.3)**: Prior work DeComFL tightly coupled dimension-free communication with vanilla ZO-SGD. The paper identifies that the crucial element is the scalar representation property, not the specific ZO algorithm, and provides a clean decoupled framework (Algorithm 1) that admits arbitrary scalar-representable update directions. This is a genuine structural advance over DeComFL and enables the integration of Hessian-informed methods.

- **Preconditioner learned at zero extra communication cost (Section 4.2, Eq. 12)**: The diagonal preconditioner H is updated using Diag([Δx]²) from Δx values that are already communicated for model reconstruction. The paper correctly notes that "the server and clients can reconstruct this global Hessian without any extra communication" (line 178). This is a clever practical insight.

- **First ZO-FL convergence analysis with τ > 1 local updates under low-effective rank (Corollary 3)**: The paper proves a convergence rate O(√(ζ/τmR)) + O(√(τκ/mR)) that remains dimension-independent when the well-approximate and low-whitening-rank conditions hold. Corollary 3 explicitly notes resolving "the previous open question that DeComFL cannot provide the convergence rate with a low-effective rank assumption when τ > 1."

- **Consistent empirical improvement over ZO baselines across LLM tasks**: Table 3 shows HiSo achieves higher test accuracy than all ZO baselines (FedZO, DeComFL) across SST-2, QQP, and SQuAD with OPT-125M/350M/1.3B/2.7B, while maintaining the lowest communication cost on most settings.

## Weaknesses

### Fatal
None.

### Major

- **Asymmetric evaluation metric in Table 2 inflates the reported speedup**: The table measures rounds under different standards: DeComFL's round count is "the total number of communication rounds required to fully converge," while HiSo's is "the number of rounds needed to match DeComFL's best test accuracy." If HiSo converges to a higher accuracy (as Table 3 shows it does on most tasks), it will cross DeComFL's lower accuracy bar earlier than HiSo itself converges. This asymmetric comparison systematically inflates the reported speedup numbers (1.4×–5.4×). Since this is the paper's headline empirical claim ("HiSo delivers a 1~5× speedup in communication rounds"), the metric needs to be recomputed on a common standard — e.g., rounds for both methods to reach a shared accuracy target, or best accuracy at a fixed round budget for both.

- **Missing comparison against ZO versions of adaptive FL methods**: Since HiSo's H-learning rule is explicitly acknowledged as RMSProp-like (footnote 2: "our method resembles RMSProp"), the natural baselines to isolate the benefit of the specific design are ZO-FedAdam, ZO-FedYogi, and a simpler RMSProp-style variant (replacing H with E[g²] of the ZO gradient scalar). Without these, it is unclear whether HiSo's advantage over DeComFL comes from the Hessian-informed derivation of the update rule (Eqs. 5–10) or simply from per-coordinate adaptivity that any adaptive optimizer would provide. These baselines are implementable within the same scalar-only framework.

### Minor

- **"Hessian-informed" framing modestly overstates what is established**: The title, abstract, and introduction consistently invoke "Hessian-informed" / "curvature information" language, but the actual H-learning rule (Eq. 12) accumulates squared ZO updates — an RMSProp-like mechanism whose connection to the Hessian diagonal is not analytically justified. The paper is transparent in footnotes (footnote 2: "our method resembles RMSProp") and the update direction derivation (Eqs. 5–10) is genuinely motivated by Hessian-informed principles, but the main narrative does not clearly demarcate the principled derivation from the practical approximation. Readers may infer stronger Hessian guarantees than are demonstrated.

- **Dimension-independence claim rests on unverified conditions**: The rate O(√(ζ/mR)) depends on ζ = Tr(H^{-1/2}ΣH^{-1/2}) being independent of d, which requires both the "well-approximate" and "low whitening rank" conditions. The paper honestly notes "it is hard to determine if this approximation holds in the context of LLMs" (line 285) and provides only a synthetic log-normal eigenvalue experiment (Fig. 4) as illustration. No empirical measurement of ζ (or even a proxy) is provided for any LLM. The theory remains valid as a conditional result, but the empirical support for the key condition driving the headline theoretical claim is absent.

- **Limited FL scale and no heterogeneity analysis**: The LLM experiments use 6 clients with 2 sampled per round. The MNIST experiment uses Dirichlet(α=1), which is relatively mild non-IID. There is no investigation of performance under higher heterogeneity, client dropout, or larger client populations — the very system challenges that motivate FL.

- **No analysis of the OPT-1.3B+QQP outlier**: On this setting, HiSo uses 96.67 KB compared to DeComFL's 43.95 KB (~2.2× more communication). While the paper notes this (line 319: "only a little higher"), no analysis of why this configuration behaves differently is provided, making it unclear under what conditions HiSo's communication advantage breaks down.

### Trivial
None.

## Nice-to-Haves
- Add an empirical verification of the connection between the learned H and the actual Hessian diagonal, even on a small model (e.g., the CNN from the MNIST experiment) where the Hessian can be estimated via finite differences.
- Report an empirical estimate of ζ for at least one LLM configuration to ground the dimension-independence claim.
- Include per-round wall-clock time alongside communication cost.
- Study the interaction between the smoothing parameter μ and the preconditioned perturbation scale H_r^{-1/2}u.

## Removed Points
The following points from the reviewers were removed after verification against the paper:

1. **"No comparison against DeComFL with per-coordinate learning rates"** (Harsh Critic): Per-coordinate LR for ZO-SGD is not a standard baseline and is not part of the scalar-only framework. This would require transmitting per-coordinate information, contradicting the dimension-free setting. Removed as scope creep.

2. **"No analysis of computation cost / Cholesky decomposition"** (Harsh Critic): The critic acknowledges this is "cheap for a diagonal matrix." For a diagonal H_r^{-1/2}, computing square roots of diagonal entries is O(d) and negligible. Removed as a non-issue.

3. **"No discussion of smoothing parameter μ"** (Harsh Critic): The choice of μ is standard in ZO methods and not specific to HiSo. Removed as generic.

4. **"Strength: addressed an important problem"** (Strength Finder): Generic/superficial. Removed.

5. **"Strength: this paper targeted an interesting question"** (Strength Finder): Generic/superficial. Removed.

6. **Harsh critic point about "ζ = d when H perfectly approximates Σ" contradicting claims**: The paper itself acknowledges this (line 224: "If H is the perfect approximation of Σ, then ζ = d"). The critic's framing implied the paper was hiding this, but it is openly discussed. Removed as factually inaccurate about the paper's disclosure.

7. **Criticism that DeComFL round count asymmetry "partially measures the accuracy gap between the two methods rather than speed per se"**: This restatement of the asymmetric metric concern was merged into the single weakness entry above. Removed to avoid duplication.

## Novel Insights
None beyond the paper's own contributions. The reviewer inputs did not surface observations not already present in the paper.

## Suggestions

1. **Recompute Table 2 with consistent evaluation**: Report rounds for both HiSo and DeComFL to reach the same accuracy target (e.g., DeComFL's best accuracy), or report best accuracy at a fixed round budget for both. Without this, the headline speedup numbers are not on firm ground.

2. **Add ZO-FedAdam and ZO-FedYogi baselines**: Implement these within the scalar-only framework to isolate whether HiSo's benefit comes from its specific design or from generic per-coordinate adaptivity. An RMSProp-style variant (replacing H with running E[g²] of the ZO gradient scalar) would be especially informative.

3. **Empirically estimate ζ**: Even a rough proxy — e.g., via Hessian-vector products on a subset of parameters — would substantially strengthen the theoretical claim. Currently the dimension-independence result is entirely conditional.

4. **Analyze the OPT-1.3B+QQP outlier**: Explain why this configuration requires more communication, and characterize the conditions under which HiSo's advantage holds.

5. **Clarify the "Hessian-informed" framing in the main text**: Move the RMSProp acknowledgment from footnote 2 into the main body (Section 4.2), and clearly separate the principled Hessian-informed motivation for the update direction structure (Eqs. 5–10) from the practical RMSProp-like H-learning rule (Eq. 12).

6. **Scale up the FL setting**: Even adding one configuration with more clients (e.g., 20–50) or higher heterogeneity would strengthen the empirical claims.

## Score and Decision

The paper makes genuine contributions — a generalized scalar-only communication framework, a principled integration of preconditioning into ZO-FL, convergence theory that extends the state-of-the-art, and empirical improvements over the leading ZO-FL baseline. However, the headline empirical claim (speedup) is supported by an asymmetric evaluation metric that inflates the numbers, key baselines that would isolate the source of improvement are absent, and the theoretical conditions driving the central claim are unverified. These issues are addressable but in the current form weaken the paper's core evidentiary case.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>