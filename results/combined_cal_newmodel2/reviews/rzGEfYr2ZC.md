## Summary

This paper proposes SparseFW, a method for pruning LLMs that replaces greedy heuristics (Wanda, RIA) with convex relaxation over the convex hull of binary masks, solved via the Frank-Wolfe algorithm. The approach accounts for weight interactions that greedy methods ignore, provides theoretical guarantees on mask suboptimality, and achieves substantial per-layer local error reductions (20–40% on average, up to 80%). Evaluation spans six model families across unstructured and semi-structured sparsity regimes.

## Strengths

- **Novel problem framing.** Formulating mask selection as a convex relaxation over the convex hull of binary masks and solving with Frank-Wolfe is genuinely different from greedy heuristics (SparseGPT, Wanda, RIA). The LMO reduces to top-k selection on the negative gradient (Eq. 12), which is both efficient and principled. Section 2 develops this cleanly.

- **Theoretical guarantees for mask suboptimality.** Lemma 1 provides a data-dependent bound decomposing error into optimization error (vanishing with more FW iterations) and thresholding error. This is a genuine advantage over Wanda and RIA, which lack such guarantees. Figure 4 empirically confirms the predicted behavior.

- **Substantial local pruning error reduction.** Figure 2 reports per-layer reductions of up to 80% in the local objective relative to Wanda, with average reductions of 20–40% across models and sparsity regimes. This demonstrates that FW genuinely finds better solutions to the relaxed problem.

- **Broad model coverage.** Evaluation spans six model families (LLaMA-3.1-8B, Gemma-2-9B, Yi-1.5-9B, DeepSeek-7B, Qwen2.5-7B, Qwen2.5-14B), broader than many pruning papers.

- **Honest discussion of limitations.** Section 5 explicitly acknowledges the local-global objective mismatch and that vanilla FW without weight fixing tends to prune crucial weights. This self-awareness is commendable, though it undercuts the paper's own framing.

## Weaknesses

### Fatal
None.

### Major

- **The method's best version freezes 90% of Wanda's decisions (α=0.9), and pure FW without Wanda guidance (α=0.0) performs worse than baselines.** This is stated in Section 2.3 (lines 157–158: "setting α = 0.0 (full FW without any fixed weights) consistently yields worse results than the baselines"), but the abstract and introduction present SparseFW as a standalone method without this qualification. The paper's framing as a replacement for greedy heuristics is at odds with its own evidence that the method depends critically on the heuristic it claims to supersede. A hybrid method (Wanda initialization + convex refinement on 10% of weights) is still a useful contribution, but the paper should present it as such from the abstract onward.

- **The most important baseline, SparseGPT, is excluded from comparison** (line 192–193) with the justification that it involves a reconstruction step. However, SparseGPT is the de facto standard for LLM pruning, and Wanda was designed as a cheaper approximation to it. Without this comparison, readers cannot assess whether SparseFW improves upon the actual state of the art in final model quality. If SparseFW is only a mask selection method, it should be compared against SparseGPT using the same reconstruction protocol.

- **Perplexity results at 50% sparsity are mixed, not consistently superior.** At 50%: Wanda beats SparseFW(Wanda) on DeepSeek-7B (7.79 vs. 7.89); RIA beats both SparseFW variants on LLaMA-3.1-8B (9.88 vs. 10.21/9.95). The abstract and contributions claim "consistent gains" and "outperforms strong baselines," which overstates the evidence. Results are stronger at higher sparsity (60%, 2:4) and on zero-shot accuracy, but the blanket claim needs tempering.

- **The local-global objective mismatch runs deeper than the paper acknowledges.** The paper motivates the convex relaxation approach by arguing that greedy heuristics produce suboptimal masks for the local objective. But optimizing the local objective better (vanilla FW, α=0.0) produces worse perplexity than baselines, and the fix (freezing 90% of Wanda's mask) essentially concedes that the greedy heuristic captures something the convex optimizer misses. This does not invalidate the paper — refinement on 10% of weights is still useful — but it means the narrative is at odds with the evidence and needs significant reframing.

### Minor

- **Standard deviations are omitted from results tables** (line 208: "We omit standard deviations for legibility"). Given that several perplexity comparisons are within 0.1–0.2 points (e.g., Wanda 7.79 vs. SparseFW(Wanda) 7.89 on DeepSeek-7B at 50%), variance information is essential to distinguish meaningful improvements from noise.

- **Algorithm 1 does not include the α weight-fixing step** that is critical to the method's performance. This step only appears in the prose (lines 157–158). A reader skimming the algorithm could easily miss this essential detail.

- **No wall-clock runtime comparison is provided.** The paper acknowledges SparseFW is "clearly more compute-intensive" (line 240) and uses 2000 FW iterations per layer, but does not quantify the cost. Readers need this to evaluate the cost-benefit trade-off.

### Trivial

- **Numerical inconsistency between abstract and contributions:** line 39 claims "up to 80%" per-layer pruning error reduction, while line 44 claims "up to 70%" for the same claim.

## Nice-to-Haves

- Include magnitude pruning as a sanity-check baseline (the paper explains it doesn't work for LLMs, but including it is standard practice).
- Analyze the thresholding gap empirically (the τ₁ distance between continuous and thresholded masks) and its variation with sparsity/model size.
- Provide an ablation study of the α parameter across multiple models in the main text (currently deferred to the appendix, Table 2).

## Removed Points

These points are flagged to be removed, treat them with caution:

- *"No comparison to magnitude pruning"* — Removed. The paper explicitly discusses that magnitude pruning performs no better than random pruning for LLMs (lines 15–16). This is adequately addressed; including it would be a nice addition but not a weakness.
- *"No analysis of the thresholding gap"* — Moved to Nice-to-Haves. The paper provides an upper bound via Lemma 1; an empirical analysis would strengthen but is not a required weakness.
- *"No discussion of warmstart for semi-structured sparsity"* — Removed. The paper references Appendix D for LMO adaptation to n:m patterns, which is standard practice for main-text conciseness.
- *"The paper's title and abstract claim without qualification"* — Already subsumed by the strength-of-claims weaknesses above.
- *"Missing related works"* — Removed as per policy (cannot confirm from external knowledge).
- Various formatting nitpicks and grammar issues — Removed as parser artifacts.

## Novel Insights

The most striking finding across the reviews and the paper itself is the α=0.0 failure: the pure convex optimization approach (without any Wanda warmstart) *underperforms* the greedy heuristics it was designed to replace. This is not just a practical quirk but reveals a structural mismatch between the local layerwise objective and global model performance. The paper's own limitation paragraph admits this, but the implication is that the mask selection problem, as formulated, may not be the right objective to optimize. The success of the α=0.9 hybrid suggests that the value of the convex relaxation lies not in replacing greedy selection but in arbitrating *edge cases* — the ~10% of weights where the greedy heuristic is uncertain. This reframed understanding (hybrid refinement rather than replacement) would strengthen the paper considerably.

## Suggestions

1. **Reframe the contribution honestly** as a principled refinement of Wanda (hybrid: greedy initialization + convex refinement on uncertain weights) rather than a replacement for greedy methods.
2. **Add SparseGPT** to the comparison — either by comparing final perplexity using the same reconstruction protocol, or by clearly delineating the class of methods SparseFW belongs to.
3. **Report standard deviations or confidence intervals** for all results.
4. **Include a wall-clock runtime comparison** table.
5. **Add the α weight-fixing parameter to Algorithm 1** so that a reader can see it without reading the prose.
6. **Resolve the 80% vs. 70% numerical inconsistency.**
7. **Temper the language** in abstract and contributions: use "competitive with, and often better than, especially at higher sparsities" rather than "consistently outperforms."

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>