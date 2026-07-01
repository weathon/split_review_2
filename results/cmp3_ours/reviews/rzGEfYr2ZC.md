Now I have enough calibration context. Let me compile the final review.

## Summary

This paper proposes SparseFW, a method for LLM pruning that relaxes the binary mask selection problem to a convex program over the convex hull of binary masks (with an L1 budget) and solves it using the Frank-Wolfe (FW) algorithm. The method accounts for weight interactions that greedy heuristics (Wanda, RIA) ignore. A critical practical detail is that SparseFW preserves 90% of the highest-saliency weights from a greedy warmstart and only optimizes the remaining 10% with FW. The paper provides theoretical guarantees bounding the gap between the rounded relaxed solution and the optimal combinatorial mask, and demonstrates improvements in perplexity and zero-shot accuracy over Wanda and RIA across several modern LLM architectures.

## Strengths

1. **Genuinely novel formulation for mask selection.** The convex relaxation of the combinatorial mask problem over the convex hull of binary masks with an L1 budget (Section 2.2) is structurally distinct from greedy heuristics. The connection to Frank-Wolfe is clean: the LMO reduces to selecting top-k most negative gradient entries (Eq. 12), which is efficient and yields naturally sparse updates. This is a substantive algorithmic contribution.

2. **Theoretical guarantee for the relaxed problem.** Lemma 1 provides a formal error bound decomposing into optimization error (k λ_max(Q)/T from FW convergence) and thresholding error. Greedy heuristics offer no such guarantees. While the bound may be loose at LLM scale, the formal connection is a strength over prior art.

3. **Consistent local-objective improvement.** Figure 2 shows per-layer pruning error reductions of up to 80% relative to Wanda across all layers of LLaMA-3.1-8B, directly validating that the method captures weight interactions that greedy methods miss.

4. **Broad empirical evaluation.** Experiments span 6 model families (LLaMA-3.1, Gemma-2, Yi-1.5, DeepSeek, Qwen2.5, LLaMA-3) at multiple sparsity levels (50%, 60%, 2:4), demonstrating generalizability across modern architectures.

## Weaknesses

### Fatal
None.

### Major

1. **Framing overstates independence from greedy methods; the working algorithm depends critically on preserving the greedy warmstart.** The title ("Don't Be Greedy, Just Relax!"), abstract, and contributions list present SparseFW as an alternative to greedy heuristics. However, the successful configuration (Section 2.3, lines 157–158) fixes 90% of the greedy warmstart's decisions and only optimizes the remaining 10% with FW. Pure FW (α=0.0) *consistently yields worse results than the baselines*. This dependence on the greedy prior is not reflected in the paper's high-level claims. The pseudocode (Algorithm 1) does not include the weight-fixing step, and the selection mechanism for the 90% fixed weights is not fully specified ("high-saliency weights (e.g., those with highest Wanda scores)" — per-row or global? which exact criterion?). The α sensitivity analysis is relegated to the (stripped) appendix despite being central to understanding the method.

2. **No reporting of variance or statistical significance.** Table 1 omits standard deviations, yet many gains are modest (e.g., at 50% sparsity, SparseFW often ties or barely exceeds baselines). Without variance information, it is impossible to assess whether improvements are statistically reliable. Figure 3 reports min-max ranges across seeds for one setting, but the main results table has no such information.

3. **No wall-clock time or FLOPs comparison.** The paper acknowledges SparseFW is "clearly more compute-intensive" than Wanda/RIA but provides no quantitative runtime. For 2000 FW iterations per layer, this cost difference is material and should be quantified to help practitioners evaluate the trade-off.

### Minor

1. **Mismatch between the theoretical guarantee and the practical success driver.** Lemma 1 bounds error on the local per-layer reconstruction objective (MASK SELECTION). However, the paper shows that optimizing this local objective does not reliably translate to better perplexity: pure FW (α=0.0) reduces local error more than the α=0.9 variant (Figure 4 vs. Table 1) but produces *worse* perplexity. The paper acknowledges this ("local–global objective mismatch persists") in the conclusion, but the theoretical contribution is thus disconnected from what makes the method work in practice.

2. **No comparison to SparseGPT on end-task metrics.** The paper excludes SparseGPT (line 192) because it "involve[s] a reconstruction step." While the scope choice is defensible, SparseGPT is the most widely-used LLM pruning method and consistently achieves stronger perplexity than Wanda in published work. The paper's practical positioning is weakened by this omission.

3. **Inconsistency in reported error reduction.** The abstract claims "up to 80%" reduction in per-layer pruning error, while the introduction (Contributions point 2) claims "up to 70%."

### Trivial
None.

## Nice-to-Haves
- A comparison to SparseGPT (even as a secondary table) would strengthen the empirical positioning, or the paper should more carefully qualify its claims relative to reconstruction-based methods.
- Further analysis of *why* local error reduction does not align with perplexity improvement (across layer types, attention vs. MLP) would deepen the contribution beyond the observed empirical phenomenon.
- Explicit specification of how the 90% fixed weights are selected (per-row or globally, based on which saliency criterion) would improve reproducibility.

## Removed Points
- **"The method works only because it preserves 90% of a greedy baseline's decisions"** — Kept as Major (1) with refined framing. The paper does disclose the caveat (Section 2.3), just not prominently in the title/abstract.
- **"Pure FW makes things worse"** — Kept as part of Major (1); this is factually correct per lines 157-158.
- **"The theory is about the wrong objective"** — Demoted to Minor (1). The theory correctly addresses what it claims (local error), and the paper acknowledges the local-global mismatch in the conclusion. The critic's framing as a "fundamental coherence problem" overstates the issue.
- **"No SparseGPT comparison"** — Demoted to Minor (2). The paper's explicit scope choice (mask selection methods only) is legitimate, but the omission limits practical significance.
- **Criticisms about α ablation in appendix, M0 specification** — Merged into Major (1) where applicable. The appendix points cannot be fully verified since the appendix is stripped.
- **"The algorithm box does not include weight-fixing"** — Kept as part of Major (1) since it contributes to the framing gap.

## Novel Insights
The structural finding that emerges from the reviews — and is arguably more interesting than the paper's own framing — is the sharp empirical demonstration of the local-global objective mismatch: Frank-Wolfe can reduce the per-layer reconstruction error substantially (up to 80%) while simultaneously hurting perplexity. This is a concrete illustration that the layerwise pruning objective and the end-task objective are substantially misaligned. The paper's workaround (fixing 90% of greedy decisions) is pragmatic, but the underlying phenomenon deserves deeper investigation as a separate contribution.

## Suggestions
- Reframe the paper honestly as a **two-stage method**: a greedy warmstart provides a strong prior, and FW optimizes the marginal decisions on the remaining search space. Remove the "Don't Be Greedy" framing.
- Include variance/standard deviation information in Table 1, at least for representative settings.
- Add a quantitative runtime comparison (wall-clock time) between SparseFW and baselines.
- Reconcile the 70%/80% inconsistency.
- Add a comparison to SparseGPT, even as a secondary table or in an appendix, to clarify where the method sits relative to the strongest available approach.

## Score and Decision

**Round 1 bracket:** Based on the calibration search, comparable papers in the LLM pruning space using convex optimization (FISTAPruner at 5.25, MoreauPruner at 4.80, Bypass Back-propagation at 5.00) all received scores in the 4.5–5.5 range and were rejected. Papers scoring below 4.0 tended to have poor writing or trivial contributions (SLiM at 3.67). Papers scoring above 6.0 (SNOWS at 6.60, MAST at 7.00) had stronger empirical results, cleaner narratives, or compared against the full set of relevant baselines.

**Anchor papers used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| BINwUtUGuq (FISTAPruner) | 5.25 | 1+2 | Most similar: convex optimization for LLM pruning. SparseFW has more novel formulation but worse framing honesty and missing SparseGPT comparison. |
| IU4L7wiwxw (PGZ) | 4.50 | 1 | Another LLM pruning paper with marginal improvements; SparseFW has stronger theoretical grounding and broader evaluation. |
| EjHtQlKEzV (Reassessing Layer Pruning) | 4.50 | 1 | Empirical study of layer pruning; SparseFW has more algorithmic novelty. |
| Y0qmwm6tgy (MoreauPruner) | 4.80 | 2 | LLM structured pruning with robustness claims; comparable quality. |
| D9GoWJJxS5 (Bypass Back-propagation) | 5.00 | 2 | Optimization-based structural pruning; similar score band. |
| 8QTpYC4smR (LLM Survey) | 1.00 | 1 | Poor-quality survey; not comparable. |
| eNQp79A5Oz (SNOWS) | 6.60 | 1 | Stronger vision pruning paper with cleaner narrative and full baselines. SparseFW is weaker by comparison. |
| qG1S5eXMzx (Heterogeneous Sublayers) | 3.50 | 2 | Lower-quality LLM pruning work; SparseFW is stronger. |

The paper has a genuinely novel formulation (convex relaxation + FW) and theoretical guarantees, which set it apart from purely empirical LLM pruning papers. However, the significant gap between the paper's framing (implying FW replaces greedy methods) and what actually works (FW as a marginal optimizer on 90% of a greedy mask), together with missing SparseGPT comparison and variance reporting, places it below the threshold for acceptance. The paper is comparable to FISTAPruner (5.25) in overall quality but has a more significant framing issue, balanced by stronger novelty.

**Final score: 5.0 — borderline reject. The core ideas are worthwhile but the presentation overstates the contribution, and the empirical case needs strengthening.**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>