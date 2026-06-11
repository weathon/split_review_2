## Summary
**External literature verification disclaimer:** This review was conducted under Retrieval-Disabled Mode (external paper search unavailable due to API token configuration). All novelty/comparison conclusions are explicitly deferred for manual verification. The analysis below is grounded entirely in manuscript evidence.

**Manuscript type:** Theoretical (optimization complexity) + Empirical (one experimental validation).

## Summary

This paper studies stochastic bilevel optimization in the nonconvex-strongly-convex setting and proposes F²SA-p, a class of fully first-order methods that improve the stochastic first-order oracle (SFO) complexity from the previous best Õ(ε^{-6}) for F²SA to Õ(p ε^{-4-2/p}) for p-th-order smooth problems. The key insight is to reinterpret the hyper-gradient approximation in F²SA as a first-order forward difference and generalize it to higher-order finite differences (central difference for p=2, and general p-th-order schemes). The paper also proves an Ω(ε^{-4}) lower bound via a separable construction that extends the single-level lower bound (Arjevani et al., 2023), showing near-optimality of F²SA-p in the highly-smooth regime (p = Ω(log(1/ε)/log log(1/ε))). One experiment on learn-to-regularize logistic regression (20 Newsgroup) validates the practical behavior.

Strengths include: (i) a genuine theoretical advance—closing part of the gap between Õ(ε^{-6}) and Ω(ε^{-4}); (ii) clean finite-difference interpretation that connects bilevel optimization to classical numerical analysis; (iii) honest open-problem discussion. Weaknesses center on: (i) experimental section lacking statistical rigor (no error bars, no runtime comparison); (ii) reliance on high-order smoothness in y only, whose practical scope is not fully discussed; (iii) the use of normalized gradient steps without analysis of the standard case; (iv) a separable lower-bound construction that sidesteps the coupled difficulty. The paper is likely to be of interest to the optimization theory community, but the empirical verification would need significant strengthening for broader impact.

## Strengths
**S1. Genuine theoretical advancement.** The paper makes a non-trivial contribution to the complexity theory of bilevel optimization. It improves the SFO upper bound from Õ(ε^{-6}) to Õ(p ε^{-4-2/p}) by identifying a finite-difference interpretation of the existing F²SA method and extending it to higher-order schemes. The asymptotic improvement is meaningful: for the highly-smooth regime where p = Ω(log(1/ε)/log log(1/ε)), the complexity approaches Õ(ε^{-4}), matching the single-level lower bound. This is a solid theoretical step toward resolving the open gap between upper and lower bounds in bilevel optimization.

**S2. Clean methodological connection.** The core insight—reinterpreting the penalty formulation of F²SA as a forward-difference hyper-gradient approximation and generalizing it via p-th-order finite differences—is elegant and well-executed. The connection to classical numerical analysis (Atkinson & Han, 2005) makes the paper's logic transparent and the extension natural. The central difference symmetric penalty problem (4) flows directly from this perspective and is clearly explained. The use of Lemma 3.1 (finite difference error bounds) and Lemma 3.2 (Lipschitz continuity of ∂^{p+1}ℓ_ν/∂ν^p∂x) provides a clean theoretical scaffold.

**S3. Honest positioning and open-problem discussion.** The paper openly acknowledges the gaps that remain: the Ω(κ^9) condition number gap, the suboptimality for small p, and the open question of whether tighter lower bounds exist under standard oracles. This transparency strengthens credibility. The comparison to related assumptions (stochastic Hessian, mean-squared smoothness, joint high-order smoothness) is thorough and helps readers understand the paper's position in the literature.

**S4. Clean lower bound construction.** The separable construction f(x,y) ≡ f_U(x), g(x,y) = μy^2/2 elegantly reduces bilevel optimization to single-level optimization, avoiding technical issues that plagued prior constructions. While it sidesteps coupling difficulty, it is a valid lower bound that cleanly extends Arjevani et al. (2023) to the bilevel setting.

**S5. Well-structured presentation for a theory paper.** Despite the density of the technical content, the paper is logically organized: introduction establishes the gap, preliminaries clearly state assumptions, method section provides the finite-difference intuition before the algorithm, and complexity analysis is self-contained. The notation is generally consistent and well-defined.

## Weaknesses
### W1. Experimental evaluation is insufficiently rigorous (MAJOR)

The single experimental section (Page 9 - Experiments) provides only qualitative line plots without variance information, statistical tests, or runtime comparisons.

**Evidence:** The experiments section (lines 159-160) reports test loss/accuracy curves over 1000 outer iterations but does not report error bars, confidence intervals, or multiple-seed statistics. The hyperparameter search is described as "in a logarithmic scale with base 10" without specifying ranges, number of trials, or selection criteria.

**Impact:** Without variance reporting, readers cannot assess whether the observed improvements of F²SA-p over F²SA and HVP-based methods are statistically significant. The claim that F²SA-p is more practical than HVP methods is not supported by wall-clock time or memory usage comparisons. Reproducibility is reduced by underspecified hyperparameter search.

**Required repair:** (a) Report at least mean±std over 3-5 random seeds in Figure 1. (b) Specify hyperparameter search ranges and selection protocol. (c) Include wall-clock time or SFO counts to support efficiency claims. (d) Add a properly tuned L2-regularized SGD baseline.

### W2. Practical scope of Assumption 2.5 (high-order smoothness in y) is under-discussed (MAJOR)

**Evidence:** Assumption 2.5 (lines 68-72) requires p-th-order smoothness in the lower-level variable y only. Examples 2.1-2.2 (lines 73-79) are both linear-model problems where this holds. The paper does not discuss how many real-world bilevel problems satisfy this for p > 2.

**Impact:** The practical relevance of the improved rates (especially for large p) depends on the proportion of bilevel problems that satisfy smoothness of the required order. If most problems of interest (e.g., neural-network-based lower-level problems with ReLU activations) only satisfy low-order smoothness, the main theoretical contribution applies to a narrow class. The LLM training example mentioned in the introduction (Pan et al., 2024) likely involves non-smooth activations, creating a tension with the theory.

**Required repair:** Add a dedicated paragraph discussing the class of functions that satisfy Assumption 2.5 and those that do not. Explicitly state whether neural-network lower-level problems with common activation functions (ReLU, GELU, etc.) meet the p-th-order smoothness condition and for which p.

### W3. Normalized gradient step is unvalidated (MODERATE)

**Evidence:** Algorithm 1 (line 14) uses $x_{t+1} = x_t - \eta_x \Phi_t / \|\Phi_t\|$, which differs from the standard gradient update in prior F²SA work. Remark 3.1 (line 133) states without proof that "all our theoretical guarantees also hold for the standard gradient step."

**Impact:** Normalization introduces a practical concern: the algorithm commits to a fixed step length in parameter space even when $\Phi_t$ is a poor approximation of $\nabla\varphi(x_t)$, which can happen when the inner loop K is insufficient. If the standard gradient step is equivalent in theory, the paper should provide that analysis or at minimum compare both variants experimentally.

**Required repair:** Either provide the alternative convergence analysis for standard gradient steps, or add an ablation experiment comparing normalized vs. unnormalized updates.

### W4. Lower bound construction decouples the bilevel structure (MODERATE)

**Evidence:** The lower bound construction (lines 155-158) uses $f(x,y) \equiv f_U(x)$ and $g(x,y) = \mu y^2/2$ where g does not depend on x.

**Impact:** This separable construction reduces bilevel optimization to single-level optimization by design, so the $\Omega(\epsilon^{-4})$ lower bound directly inherits from single-level nonconvex optimization. It does not reflect the additional difficulty introduced by the coupling between x and y. While this is a valid lower bound for the class $\mathcal{F}^{nc-sc}$, it may be loose for the practically interesting subclass where g depends non-trivially on x.

**Required repair:** Explicitly note that the lower bound may not capture bilevel-specific hardness and that tighter bounds for non-separable instances remain open. (Partially addressed in the "open problems" section but could be more prominent.)

### W5. Condition number dependency is severe (MODERATE)

**Evidence:** The final complexity bound in Theorem 3.1 (line 144) scales as $\kappa^{9+2/p}$, which is a large polynomial dependence. The lower bound has only $\Omega(\epsilon^{-4})$ dependence (no $\kappa$ factor). As the paper acknowledges (line 33), "the current upper and lower bounds have a gap of $\Omega(\kappa^9)$."

**Impact:** For ill-conditioned problems where $\kappa$ is large (e.g., $\kappa=10^3$), the $\kappa^9$ factor makes the bound astronomically large, potentially larger than naive single-level methods. This limits the practical applicability of the theoretical guarantees even if the ε-dependence is optimal.

**Required repair:** While the paper honestly acknowledges this gap, adding a discussion of when $\kappa$ is expected to be small in practice (e.g., logistic regression with well-scaled data) would help readers assess applicability.

### W6. Writing quality issues (MINOR)

- Abstract (line 13) is dense and mixes four distinct contribution elements without clear separation. A more structured 5-sentence arc would improve readability.
- Introduction paragraph 1 (lines 15-20) packages motivation, problem definition, and hyper-gradient formula in one block; splitting would improve flow.
- Conclusion (line 162) contains a typo: "extended our theory" should be "extend our theory" or "can be extended."
- The "References" section (lines 169-182) is only partially present in the extracted text; some inline citations in the introduction (e.g., Shen et al., 2025a; Xiao & Chen, 2025) do not appear in the reference list, which may be an extraction artifact but should be verified.
- The notation $\mathcal{F}^{ncse}$ in Theorem 4.1 uses "ncse" while Definition 2.2 uses "nc-sc" — this inconsistency should be resolved.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper presents a genuine theoretical contribution—improving the SFO complexity of fully first-order bilevel optimization from Õ(ε^{-6}) to Õ(p ε^{-4-2/p})—with a clean finite-difference interpretation and a valid lower bound extension. The theoretical argument is well-structured and the open-problem discussion is honest. However, the score is constrained by: (1) the experimental evaluation lacks statistical rigor (no error bars, no runtime comparisons, underspecified hyperparameter search), which reduces the credibility of claimed practical advantages; (2) the high-order smoothness assumption (Assumption 2.5) that drives the improvement is not fully contextualized in terms of practical problem coverage; (3) the normalized gradient step modification is unvalidated against standard gradient steps; and (4) the severe κ^9 condition number dependency limits practical applicability. The novelty verification is deferred (external paper search unavailable in this run). The paper is publishable in a theory-oriented venue but would need substantially strengthened empirical validation for broader venues.

**Note on novelty:** All novelty/comparison conclusions are explicitly deferred for manual verification due to Retrieval-Disabled Mode in this review run (external paper search unavailable).

---

### ASCII Diagram A — Paper Structure & Evidence Map

```text
[Core Claim: F²SA-p improves SFO complexity from Õ(ε^{-6}) to Õ(pε^{-4-2/p})]
    |
    ├── Theoretical Support (well-developed)
    │   ├── Lemma 3.1: Finite difference error guarantee (O(ν^p))
    │   ├── Lemma 3.2: Lipschitz continuity of ∂^{p+1}ℓ_ν/∂ν^p∂x (O(κ^{2p+1}L̄))
    │   ├── Theorem 3.1: Main complexity bound with hyperparameter schedule
    │   └── Theorem 4.1: Ω(ε^{-4}) lower bound via separable construction
    │
    ├── Empirical Support (weak)
    │   └── Figure 1: Single-run curves, no variance, no runtime, no statistical tests
    │
    └── Gap Analysis
        ├── ε-gap: partially closed (approach optimal when p is large)
        ├── κ-gap: Ω(κ^9) remains open
        └── Evidence gap: practical superiority not validated statistically
```

### ASCII Diagram B — Revision Strategy Roadmap

```text
Priority 0 (Must fix before resubmission):
  [W1: Weak experiments]
      → Add 5-seed variance bars, hyperparameter details, runtime table
      → Expected impact: statistical credibility, reproducibility
  [W2: Assumption 2.5 scope]
      → Add practical scope discussion paragraph
      → Expected impact: readers can assess applicability

Priority 1 (Should fix):
  [W3: Normalized gradient step]
      → Add ablation comparing normalized vs. standard update
      → Expected impact: validate methodological choice
  [W4: Lower bound limitation]
      → Acknowledge separability limits in main text
      → Expected impact: honest positioning

Priority 2 (Nice to have):
  [W5: Condition number discussion]
      → Add practical κ estimation for examples
  [W6: Writing fixes]
      → Fix typo, restructure abstract, unify notation
```

### ASCII Diagram C — Related-Work Taxonomy Tree (Layered)

```text
Note: Taxonomy is constructed from manuscript-cited works only, as external paper search was unavailable.
All novelty verdicts are deferred for manual verification.

Stochastic Bilevel Optimization Methods (Root)
├── Branch 1: Hessian-Vector-Product (HVP) Methods
│   ├── Leaf 1.1: BSA [Ghadimi & Wang, 2018]
│   ├── Leaf 1.2: stocBiO [Ji et al., 2021]
│   └── Leaf 1.3: FdeHBO [Yang et al., 2023b]
│   Assumption: Require stochastic Hessian oracle (stronger than SGD)
│
├── Branch 2: Variance-Reduced HVP Methods
│   ├── Leaf 2.1: MRBO / VRBO [Yang et al., 2021]
│   └── Leaf 2.2: Methods of [Khanduri et al., 2021]
│   Assumption: Mean-squared smoothness + stochastic Hessian
│   Complexity: Õ(ε^{-3})
│
├── Branch 3: Fully First-Order Methods (Gradient-only)
│   ├── Leaf 3.1: F²SA [Kwon et al., 2023] — forward-difference, Õ(ε^{-7})→Õ(ε^{-6})
│   ├── Leaf 3.2: F²SA-p [THIS PAPER] — p-th-order finite-difference, Õ(pε^{-4-2/p})
│   └── Leaf 3.3: Two-timescale F²SA [Chen et al., 2025b] — Õ(ε^{-2}) deterministic
│   Assumption: Standard SGD assumptions only (weaker than Branch 1/2)
│   Novelty risk: LOW (this paper is the main contributor to this branch)
│
└── Branch 4: Second-Order Stationary Methods
    └── Leaf 4.1: Jointly second-order smooth methods [Huang et al., 2025; Yang et al., 2023a]
    Assumption: Joint (x,y) high-order smoothness (stronger than Assumption 2.5)
    Goal: Second-order stationary points, not first-order

Contribution-level Novelty Conclusion (provisional, requires verification):
C1 (Finite-difference interpretation): Likely novel. The forward-difference reinterpretation of F²SA
    and extension to p-th-order finite differences appears to be a new perspective not explored
    in prior bilevel literature.
C2 (Improved complexity bound): Likely novel. The Õ(pε^{-4-2/p}) bound improves over prior
    Õ(ε^{-6}) for p ≥ 2 under the stated smoothness assumptions.
C3 (Ω(ε^{-4}) lower bound): Partially overlapping with [Arjevani et al., 2023; Dagru et al., 2024;
    Kwon et al., 2024a] but the separable construction is novel and clean.
```