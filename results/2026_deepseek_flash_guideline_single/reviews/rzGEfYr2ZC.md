## Summary

This paper proposes SparseFW, a layerwise LLM pruning method that relaxes the binary mask selection problem to a convex program (over the convex hull of binary masks with an L₁ budget) and solves it via the Frank-Wolfe (FW) algorithm. The paper derives Wanda and RIA as single-step greedy approximations, demonstrates substantial per-layer reconstruction error reductions (20–40% average, up to 80%), and reports perplexity/accuracy gains across several modern GPT architectures (Qwen 2.5, LLaMA 3, Yi 1.5, Gemma 2). Theoretical approximation guarantees are also provided.

## Strengths

1. **Clean formalization of existing methods.** The derivation showing Wanda's salience score is equivalent to a single-step greedy pruning of the local quadratic objective (Equations 3–5) and the similar treatment of RIA as Wanda on a rescaled weight matrix are precise and insightful contributions.

2. **Principled convex relaxation with well-motivated solver.** Replacing the combinatorial constraint $\|M\|_0 \leq k$ with the convex hull $\{M \in [0,1]^{d_{\text{out}}\times d_{\text{in}}}, \|M\|_1 \leq k\}$ is natural, and the choice of Frank-Wolfe (with its efficient LMO that yields sparse vertex updates) is well-justified. The precomputation of $G=XX^\top$ and $H=WG$ to decouple per-iteration cost from sequence length is a practical insight.

3. **Substantial local pruning error reduction.** Figure 2 shows up to 80% reduction in per-layer reconstruction error relative to Wanda, with average reductions of 20–40% across models and sparsity regimes. This is a genuine empirical finding about the optimization quality of FW on the relaxed objective.

4. **Evaluation on modern architectures.** Unlike many pruning papers that test only on LLaMA-1/OPT, this paper evaluates on Qwen 2.5, LLaMA 3.1, Yi 1.5, Gemma 2, and DeepSeek — reflecting current model landscape.

## Weaknesses

### Major

1. **Warmstart dependency (α=0.9) fundamentally changes what the method contributes.** The paper reports (lines 157, 283) that pure SparseFW (α=0.0) — FW on the convex relaxation without any fixed weights — *"consistently yields worse results than the baselines."* To obtain improvements, 90% of weights are locked to Wanda's decisions and only the remaining 10% are optimized via FW. This means the method that outperforms baselines in Table 1 is not "solving the relaxed problem with FW yields better masks" but rather "FW can marginally refine a small fraction of Wanda's decisions." The abstract, contributions list, and Algorithm 1 do not convey this dependency. While Section 2.3 and the Conclusion mention it candidly, the high-level framing substantially overstates what the pure relaxation approach achieves. This is the most significant limitation of the paper.

2. **SparseGPT is excluded from comparisons.** The paper justifies this by saying SparseGPT "involves a reconstruction step" while the paper focuses on methods that "aim to find a better pruning mask by solving (MASK SELECTION)" (lines 192–193). This distinction is artificial — SparseGPT is fundamentally a mask selection method that also reconstructs remaining weights, and it is the dominant SOTA baseline that substantially outperforms Wanda at high sparsities. Without this comparison, it is impossible to assess whether SparseFW's improvements over Wanda constitute a meaningful practical advance. Given that the paper's own Section 2.1 discusses SparseGPT's mask selection procedure in detail, the exclusion is a clear gap.

3. **RIA accuracy at 60% sparsity duplicates Wanda's values exactly.** In Table 1, the 60% sparsity accuracy row for RIA (63.19, 53.7, 50.51, 59.44, 63.58, 48.08) is identical to the Wanda row above it, which is almost certainly a data-entry error. This undermines confidence in the reporting.

### Minor

4. **Perplexity improvements are inconsistent, especially at lower sparsity.** At 50% sparsity, SparseFW(Wanda) is *worse* than Wanda on DeepSeek-7 (7.89 vs 7.79) and LLaMA-3 (10.21 vs 10.09). SparseFW(RIA) is worse than RIA on DeepSeek-7 (7.93 vs 7.90). At 60%, SparseFW(Wanda) is worse than Wanda on DeepSeek-7 (11.99 vs 11.44). No standard deviations or confidence intervals are reported for Table 1, so the statistical significance of the often modest gains cannot be assessed.

5. **Theoretical bound is loose.** The thresholding error term $2(k + \sqrt{2 d_{\text{in}} d_{\text{out}} k})$ is constant in $T$ and large at LLM scale; $\lambda_{\max}(Q)$ is not estimated for any practical model. The guarantee is therefore not practically informative, as the paper acknowledges indirectly via Figure 4 (right panel, plateauing threshold residual). This does not invalidate the work but means the theory adds little beyond standard FW convergence.

### Trivial

None.

## Nice-to-Haves

- The ablation of warmstart fraction α (currently in the appendix) should appear in the main paper, as α=0.9 is the method's critical design choice.
- Wall-clock time comparison with baselines would help calibrate the cost-benefit tradeoff (the paper notes SparseFW is more compute-intensive but does not quantify this).

## Removed Points

The following points from the input review were removed (with justification):

1. *"RIA 60% perplexity for Yi-1.5 (14.37) seems anomalously high compared to Wanda's 11.38"* — This is speculation; it may be a real phenomenon.
2. *"The central framing is invalidated"* / *"fatal"* characterization — The paper does describe the warmstart; the issue is under-prominence, not absence. Demoted from fatal to major.
3. *"Missing standard deviations"* as a standalone complaint — Already covered in weakness #4 above with specific examples.
4. *Claims about the algorithm pseudocode not mentioning warmstart* — While technically true that Algorithm 1 describes pure FW, the adjacent paragraph in Section 2.3 explains the warmstart. This is a presentation issue, not a hidden omission.
5. *"No standard deviations are reported, so we cannot assess whether these small differences are statistically significant"* — Merged into weakness #4.

## Novel Insights

The paper's clearest empirical finding is the disconnect between local pruning error and downstream perplexity: FW optimizes the local quadratic objective far better than Wanda (up to 80% error reduction), but this only translates to perplexity gains when the greedy baseline's decisions are mostly locked in. This negative result — that better optimization of the per-layer reconstruction objective does not straightforwardly yield better downstream performance — is acknowledged in the conclusion and may be the paper's most interesting contribution, suggesting that the local objective has systematic blind spots that greedy heuristics implicitly correct for.

## Suggestions

1. Reframe the contribution to honestly center on the hybrid warmstart approach — the paper is essentially a refinement method that starts from a baseline mask.
2. Add SparseGPT as a baseline. If SparseFW(Wanda) does not approach SparseGPT's perplexity, the practical significance is limited regardless of improvements over Wanda.
3. Report standard deviations or confidence intervals for Table 1.
4. Move the α ablation to the main paper and analyze which of the 10% of optimized weights actually change.
5. Investigate and correct the RIA 60% accuracy entries.

## Score and Decision

**Round 1 bracket (from calibration):** 3.5–5.0

**Anchors consulted:**
- **FISTAPruner** (5.25, scores 6/6/6/3, Reject) — Most similar paper; also uses convex optimization for layerwise LLM pruning, compares against SparseGPT, shows consistent improvements. Our paper is weaker because of the warmstart dependency and missing SparseGPT comparison.
- **PGZ** (4.50, scores 3/5/5/5, Reject) — LLM pruning paper with mixed reviews; limited evaluations noted as weakness. Our paper has similar scope but additional issues (warmstart dependency, RIA data duplication).
- **CVXQ** (3.00, scores 3/3/3/3, Reject) — Convex optimization for LLM compression (quantization); uniformly scored 3 due to missing comparisons and practical caveats. Our paper has stronger empirical work but similar pattern of overclaimed framing relative to caveats.
- **OWL** (6.00, avg of 5/3/8/6/8, Reject) — LLM pruning with non-uniform sparsity; stronger results but also rejected on balance. Not directly comparable in methodology.
- **Probe Pruning** (7.00, scores 6/6/8/8, Accept) — Dynamic LLM pruning; accepted with clearly demonstrated improvements.
- **Reassessing Layer Pruning** (4.50, Reject) — LLM pruning analysis paper.
- **RotPruner** (5.33, Reject) — LLM pruning in rotated space.

**Final narrowing:** The paper is not as strong as FISTAPruner (5.25) — the prime comparable — because the warmstart dependency and missing SparseGPT comparison are concrete weaknesses that FISTAPruner does not share. It is stronger than CVXQ (3.00) because it has actual empirical validation across multiple modern architectures. The RIA data duplication pushes the score down further.

**Final score: 4.0** — Borderline reject. The core idea (convex relaxation + FW) and clean formalization of greedy methods have genuine merit, but the paper's claims outrun the evidence. The warmstart dependency is not adequately surfaced in the paper's framing, SparseGPT is missing from comparisons, and the data integrity concern (RIA accuracy duplication) requires clarification.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>