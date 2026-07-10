Now I'll write the final consolidated review.

## Summary

This paper formalizes critical KV cache entry selection in LLMs from an output perturbation perspective. It derives an upper bound on attention output perturbation (Theorem 3.3), revealing that both attention weights *and* projected value-state norms ‖VW^O‖₁ matter — an overlooked factor in prior heuristic methods. The authors propose a two-stage perturbation-constrained selection algorithm and show it serves as a universal plug-in enhancement. Across 29 datasets (Ruler + LongBench), three LLMs (8B–32B), and three base methods (SnapKV, AdaKV, HeadKV), the algorithm consistently and substantially reduces compression loss with negligible computational overhead (~1.7% TTFT increase).

## Strengths

- **Principled problem formalization (Section 3.2–3.3):** The paper defines critical cache identification as minimizing output perturbation (Definition 3.1), a clean, measurable objective beyond prior heuristic reliance on accumulated attention weights.
- **Theoretical derivation revealing an overlooked factor (Theorem 3.3):** The upper bound θ shows that optimal selection depends not only on attention weights Aᵢ but also on projected value states ‖VᵢW^O‖₁ — a non-obvious insight that directly motivates the algorithm and is the paper's clearest differentiator.
- **Consistent and substantial empirical gains (Tables 1–3, Figure 1):** Across three LLMs (8B–32B), three base methods (SnapKV, AdaKV, HeadKV), and 29 datasets, the algorithm improves results in nearly every configuration, frequently halving or more the loss relative to full cache (e.g., AdaKV on Qwen2.5-32B at 40% cache on Ruler drops from 24.3% loss to 0.69% loss).
- **Minimal computational overhead (Section 4.6):** The added cost is ~0.06s TTFT at batch size 1 (32K context) — a 1.7% increase — and essentially zero decoding overhead, making the method practically attractive.
- **Multi-turn QA validation (Section 4.4):** SCBench results (Table 3) add a realistic deployment scenario beyond single-turn benchmarks, and the gains are largest at the tightest budgets where the method matters most.

## Weaknesses

### Fatal
None.

### Major
- **Algorithm 1 pseudocode is inconsistent with the text and with Assumption 3.4.** The text (line 126) states Stage 1 "prioritize[s] KV cache entries with high attention weights," and Assumption 3.4 (line 170) formalizes this using Topₖ of raw attention weights A. However, Algorithm 1 line 5 selects by Topₖ(𝒜, b′) where 𝒜 is the *combined score* (A × value norm), not raw attention. If Stage 1 actually uses the combined score, the two stages use identical criteria and the two-stage design collapses into a single-stage combined-score selector. This ambiguity must be resolved for reproducibility.

### Minor
- **Incomplete ablation of the source of improvement.** The paper does not compare against a single-stage combined-score selector (α=0) across all base methods and models. The α sensitivity analysis (Table 4) is limited to AdaKV on LongBench, yet on Llama-3.1-8B, α=0 achieves 44.35 vs. α=0.5's 43.77 — meaning the simpler one-stage selector *outperforms* the two-stage design on this model. Without broader ablation, it is unclear whether the gains come from incorporating value norms (the theoretical insight) or from the two-stage perturbation-constrained design (the algorithmic contribution). The paper notes this effect but does not explore why the two models differ.
- **Gap between theory and algorithm.** The paper derives an upper bound θ (Theorem 3.3) and states the algorithm "constrains worst-case perturbation," but the algorithm does not solve the optimization implied by θ. The paper acknowledges this (line 124: "directly minimizing the upper bound θ remains non-trivial"), but the phrasing throughout overstates the connection. The algorithm is *inspired by* the bound, not derived from it.
- **No error bars or confidence intervals.** The main results (Tables 1–3) report point estimates without standard deviations or confidence intervals. While the improvements are large and consistent enough that significance is plausible, this is an omission.

### Trivial
- The term "4srs" / "1srs" in the Figure 3 caption is undefined in the paper body.

## Nice-to-Haves
- Report perturbation upper bound values (θ or its components) for Algorithm 1 vs. attention-only selection on a sample of heads, to directly validate whether the algorithm lowers the bound it was designed to constrain.
- A brief discussion of why the two models (Llama vs. Mistral) differ in their sensitivity to α=0 would be informative.

## Removed Points
*These points appeared in the input review but were excluded after verification.*

- **H2O simulation caveat:** The paper transparently discloses the limitation of using only the last 256 tokens' attention weights and cites prior work for the approach. This is a stated practical compromise, not an oversight.
- **Code domain degradation:** The paper explains the code domain is "naturally insensitive to cache eviction," and the few marginal degradations are within the context of a known phenomenon from prior work.
- **Questioning the "more than half" claim:** The claim is "on average across 29 datasets," not per-case. The averaged data in Figure 1 supports it.
- **Theorem 3.2 intuition concern:** Deferring intuition and proof to the appendix is standard practice for conference papers.
- **α=0 outperforming α=0.5 on Llama without commentary:** The paper does comment on this, attributing it to Assumption 3.4 being satisfied by Llama but violated by Mistral at α=0. This is acknowledged in the existing sensitivity analysis.

## Novel Insights
None beyond the paper's own contributions. The reviews confirm the paper's core finding — that incorporating projected value-state norms into KV cache selection yields consistent gains — without surfacing any unrecognized limitation beyond what the ablation analysis already surfaces.

## Suggestions

1. **Fix Algorithm 1:** Stage 1 should select by Topₖ(A, b′) (raw attention weights) to match the text and Assumption 3.4.
2. **Add a one-stage ablation (α=0)** across all three base methods and three models on both Ruler and LongBench, to isolate whether the improvement comes from incorporating value norms or from the two-stage design.
3. **Define "srs"** in the Figure 3 caption or body text.
4. **Add error bars** for main results where sampling variance exists.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>