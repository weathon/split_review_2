The paper hedges properly — line 9: "To our knowledge, FEDSGM is the first framework…" and line 54: "To the best of our knowledge, FEDSGM is the first unified framework…" The reviewer's contrary claim is factually wrong and was already removed.

Here is the final consolidated review:

---

## Summary

FEDSGM presents a unified theoretical framework for federated constrained optimization that simultaneously handles functional constraints, bidirectional compression with error feedback, multiple local updates (E > 1), and partial client participation. It extends the Switching Gradient Method (SGM) to the federated setting, provides convergence guarantees with O(1/√T) rates and high-probability bounds, and introduces a soft-switching variant to mitigate boundary oscillations. Experiments on NP classification and CMDP (Cartpole) validate the theoretical predictions.

## Strengths

- **Genuinely unified theoretical treatment.** The paper subsumes several existing results (SGM with E=1, EF-SGD/EF14, FedSGM without compression, bi-directional compression without local steps) as special cases of its framework (lines 104–108, 161–163), demonstrating consistency with prior work and a principled generalization.
- **Clean decoupling of optimization and estimation error under partial participation.** Theorem 1's high-probability bounds separate the optimization error (scaling as 1/√T) from the statistical estimation error (scaling as σ√(log(T/δ)/m)) in a structurally interpretable way (lines 44–48).
- **Geometric motivation for soft switching via skew-symmetric matrices.** The analysis of rotational dynamics through K_glob and K_loc (lines 179–185) provides an intuitive explanation for boundary oscillations and why soft switching with finite β can mitigate them, even though the theory only fully covers the β → ∞ limit.

## Weaknesses

### Fatal

None.

### Major

- **No comparisons to existing methods in experiments.** The experimental section (Section 4) exclusively compares variants of FEDSGM against itself (hard vs. soft switching, different E, different m/n, different K/d values). There are no comparisons to any existing constrained FL method (e.g., constrained FedAvg from He et al. 2024, AL/ADMM-type methods), to unconstrained FedAvg (to show the value of constraint awareness), or even to a centralized SGM baseline for the NP task. Table 1's "Centralized" entry is a non-federated version of the same algorithm — not an independent baseline from prior work. The experiments validate that the algorithm converges and that parameter effects match theory, but they do not demonstrate that the unified framework provides practical benefits over simpler alternatives that handle only subsets of challenges. For a venue like ICLR that values both theory and experiments, this is a significant gap.

- **Soft switching convergence guarantee (Theorem 2) requires β ≥ 2/ε, asymptotically forcing hard switching.** Since ε → 0 as T → ∞, β must diverge to infinity for the guarantee to hold. As the paper itself acknowledges (line 215), this choice "may be overly conservative when ε is very small, effectively approximating a hard switch." The proved convergence of soft switching therefore covers only the regime where it is indistinguishable from hard switching. The practical benefits (stability, reduced oscillations) come from finite, moderate β, but this regime lacks theoretical backing. The experiments (Figure 1) partially compensate by showing soft switching with β=100 works well, but the mismatch between the theorem's condition and the practically useful β regime remains a substantive methodological gap that substantially weakens the theoretical contribution of the soft switching variant.

### Minor

- **Partial participation analysis is restricted to deterministic compressors (line 98).** The high-probability bounds for the m < n case apply only to deterministic compressors like Top‑K, excluding randomized compressors (Rand‑K, stochastic quantization) that are widely used in practice. The paper does not explain why this restriction is needed or whether it is an artifact of the proof technique.

- **CMDP/RL experiment operates entirely outside the convexity assumptions.** The theory (Assumption 1) assumes convex and G-Lipschitz f_j and g_j, yet the CMDP experiment uses TRPO with policy gradients — acknowledged as "highly non-convex" (line 269). The paper transparently flags this limitation, but the consequence is that the RL experiment cannot be interpreted through the theoretical lens; we do not know whether the algorithm's success is due to the properties the theory identifies or to unrelated factors. The experiment is better viewed as an empirical illustration of generality rather than as support for the theoretical claims.

- **The sub-Gaussian assumption (Assumption 4, line 74) is strong and its implications under violation are not discussed.** The assumption rules out heavy-tailed constraint values, which can arise in practice (e.g., ratios with small denominators, highly heterogeneous client data). Since the switching decision depends on ĝ(w_t), a noisy estimate can trigger the wrong gradient direction. The union-bound analysis handles this probabilistically, but the paper does not discuss practical diagnostics for when this assumption might break.

### Trivial

- Only 3 random seeds for NP classification (line 221) and 5 seeds for CMDP (line 247) are used, which is modest for stochastic algorithms where larger seed counts and clearer variance interpretation are standard practice.

## Nice-to-Haves

- Adding two simple baselines to the NP experiment — constrained FedAvg (or the closest available prior method) and a centralized SGM — would substantially strengthen the empirical story by showing whether FEDSGM introduces degradation relative to simpler approaches that handle only subsets of the four challenges.
- Relaxing the β ≥ 2/ε condition in Theorem 2 (or proving a weaker rate for finite β) would close the gap between the theory and the practically useful regime of soft switching.
- Discussing whether the deterministic-compressor restriction in the partial participation case is fundamental or a proof artifact would help readers assess the scope of the theoretical results.

## Removed Points

Points flagged for removal (treat with caution — they are either factually incorrect, parser artifacts, misunderstandings, or noise that does not belong in a final review):

- **"First framework" claim not hedged:** The reviewer stated the claim is presented as fact without hedging. The paper actually uses "To our knowledge" (line 9) and "To the best of our knowledge" (lines 54, 267). This criticism is factually wrong and is removed.
- **T vs Γ parser artifact:** The reviewer noted a possible typo in the ε expression of Theorem 1 but acknowledged it could be a parser artifact. Removed as unverified.
- **Projection-free inconsistency:** The reviewer criticized the use of Π_𝒳 as contradicting "projection-free." Domain projection onto a compact convex set is standard; "projection-free" correctly refers to not projecting onto the constraint set g(w) ≤ 0. Removed as a misunderstanding.
- **Section-by-section observational notes** (e.g., "no discussion of dependency on T," "should cite and discuss EF mechanism," "no convergence plots for CMDP"): These are either observational notes without specific anchor points in the paper, speculative (appendix content), or inaccurate (Figures 3 and 4 do show results over rounds). Removed per noise-filtering rules.
- **"Three seeds" as standalone criticism:** Merged into Trivial section rather than presented as an independent weakness.
- **Generic concern about Assumption 4 (too strong, not discussed):** Retained in Minor section because it *is* a concrete criticism anchored to a specific assumption; the removed version of this referred to heavy-tailed distributions generically without connection to the paper's setup — the version in Minor is appropriately anchored.

## Novel Insights

The harsh critic's observation about the β ≥ 2/ε condition is the most pointed insight beyond the paper's own framing. The paper acknowledges this limitation (line 215), but the critic correctly identifies it as structurally more central than the paper's tone suggests — it is not a minor caveat but rather a gap where the theory for soft switching does not cover the regime in which soft switching provides practical value. This sharpens the paper's own limitation discussion and clarifies what would need to be addressed to fully substantiate the soft switching contribution.

## Suggestions

1. Add at least 2–3 baseline methods to the NP classification experiment (constrained FedAvg, unconstrained FedAvg, centralized SGM) and discuss how FEDSGM compares in terms of constraint satisfaction vs. communication efficiency and objective value.
2. Include an explicit discussion of why the partial participation theory requires deterministic compressors and whether this is a fundamental or proof-technique restriction.
3. Consider adding a small-scale convex constrained optimization experiment (e.g., a synthetic quadratic program) where all assumptions are provably satisfied, to provide a clean empirical validation of the theory that the CMDP experiment cannot offer.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>