Now I have all the information needed to write a thorough review. Let me compose it.

## Summary

MoEP proposes a sparse decoder-only architecture that combines layer-level parallel blocks with top-k token routing and MoE-style linear projections. The key architectural distinction is that it introduces sparsity without increasing total parameter count (28M for both MoEP and its GPT-2 baseline). The paper evaluates on the BabyLM strict-small track and reports comparisons against dense GPT-2 and GPT-BERT baselines.

## Strengths

1. **Fixed parameter count despite sparsity is genuinely novel.** Standard MoE increases total parameters to accommodate expert weights, then relies on sparse activation to keep FLOPs manageable. MoEP instead keeps total parameters equal to the dense baseline (28M, Table 2) by operating parallel blocks at reduced hidden dimension (d_P=192 vs d_L=384). This is a well-documented architectural distinction that the paper clearly explains and quantifies.

2. **Outperforms the direct GPT-2 baseline under matched conditions.** MoEP achieves macro average 49.00 (excluding AoA) vs the official BabyLM GPT-2 baseline at 46.60 and the paper's own GPT-2 replication at 48.10 (Table 1). Since MoEP uses GPT-2's sublayer structure as its dense component, this comparison is relatively clean and isolates the benefit of the proposed sparsity mechanism.

3. **Training dynamics analysis provides useful insights.** The appendix (A.3) compares checkpoint-level trajectories, showing that MoEP peaks at 30M words while MoEP-SwiGLU does not peak until 80M words. The paper visualizes how different tasks converge differently across architectures, giving a more nuanced picture than a single aggregate score.

4. **Code and model weights are released**, improving reproducibility.

## Weaknesses

### Major

1. **The headline outperformance claim is misleading.** The Introduction (line 31) states MoEP "outperform[ed] all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models." This is only true under one specific averaging convention (the AoA-inclusive macro average). On the excluding-AoA macro average (listed first in Table 1), GPT-BERT (causal) achieves 54.10 vs MoEP's 49.00 — a gap of over 5 points. The paper does clarify this in Section 5.1 ("when the AoA task score was included"), but the unqualified claim in the Introduction is overstated and would mislead a casual reader. This matters because AoA is an outlier task where MoEP scores 53.70 but GPT-BERT (causal) scores −3.90; including it mechanically inflates MoEP's relative standing.

2. **No comparison against a standard MoE baseline.** The paper's motivation is that standard MoE increases total parameter count, which MoEP avoids. But the experiments contain no standard FFN-level MoE model matching the same 28M parameter budget. The baselines are entirely dense (GPT-2, GPT-BERT). Without a vanilla MoE control, it is impossible to tell whether MoEP's results come from its novel layer-level parallel architecture or simply from the well-known benefits of introducing any sparsity via routing. This is the most important missing control for the paper's thesis.

3. **MoEP-SwiGLU comparison is invalidated by parameter mismatch.** MoEP has 28M parameters and MoEP-SwiGLU has 38M — a 36% increase (Table 2). The paper compares both against the same 28M baseline models and draws conclusions about "lightweight linear experts being more effective at small scale." But the independent variable (expert type) is perfectly confounded with parameter count, making this comparison uninterpretable as an ablation. If the goal is to compare linear vs SwiGLU experts, the parameter counts must be matched.

4. **No efficiency measurements despite "efficient" in the title.** The paper's title promises "Compact and Efficient Sparsity," and the abstract frames MoEP as avoiding computational overload. Yet the paper reports no FLOPs per token, no throughput (tokens/sec), no latency, no training-time comparison, and no activated-to-total parameter ratio. The only runtime information is "1-2 hours per model" for all models collectively (Section 4). Since sparse routing has well-known costs — routing computation, memory bandwidth overhead — the paper provides no evidence that MoEP is efficient in any measurable sense. If efficiency claims are to be made, they must be measured.

5. **No ablations of any architectural choice.** MoEP has several tunable components: number of parallel blocks per layer (P=4), top-k selections (k=2), number of parallel layers (N=10), MoE expert count (E=4), linear vs learned routing, load-balancing loss coefficients (λ^block, λ^expert). None are ablated. We do not know whether routing is better than random selection, whether the MoE shrink/grow blocks matter, whether the parallel layer count is important, or whether the load-balancing loss has any effect. The paper cannot attribute its results to any specific design component.

### Minor

6. **Peak-checkpoint selection introduces subtle bias.** The paper selects the checkpoint with the best fast-evaluation performance for each model (Section 4). This compares *peak* values rather than *final* or *converged* values. Different models peak at different points (MoEP and GPT-2 at 30M, MoEP-SwiGLU at 80M), so the convention may favor models that peak early and then degrade. The paper acknowledges this partially but does not discuss whether it inflates MoEP's reported scores relative to a final-checkpoint comparison.

7. **The "faster convergence" claim is weakly supported.** The abstract claims MoEP "accelerates model learning," but both MoEP and GPT-2 peak at 30M words. The appendix analysis shows MoEP has different learning dynamics (more comprehensive early learning), but the claim of "acceleration" specifically is not clearly demonstrated relative to the dense GPT-2 baseline — only relative to MoEP-SwiGLU, which has a parameter mismatch confound.

8. **The load-balancing loss uses entropy regularization without justification.** Equation 2 uses an entropy penalty (-Σ p_i log p_i), which encourages uniform routing probabilities. Standard MoE practice (e.g., Switch Transformer) uses a differentiable auxiliary loss based on the squared coefficient of variation of expert assignment frequencies, which directly penalizes load imbalance. The paper does not justify the design choice or cite precedent for entropy-based balancing in this context.

### Trivial

9. Some minor formatting artifacts and imprecise wording (e.g., "Liner" instead of "Linear" in Table 2, "textbf" verbatim in Section 4). These do not affect the technical content.

## Nice-to-Haves

- Reporting variance (mean ± std over multiple seeds) would help assess whether the 0.9-point gap between MoEP (49.00) and GPT-2 (48.10) on the excluding-AoA macro average is significant or noise.
- A comparison between entropy-based balancing and the more standard load-imbalance auxiliary loss would strengthen the methodological contribution.
- Analyzing the activated-to-total parameter ratio per token would provide a basic efficiency sanity check even without wall-clock measurements.

## Removed Points

The following points from the Harsh Critic and Strength Finder are removed or demoted under the filtering rules:

- *Criticism about missing related works*: Removed — reviewer cannot verify existence of missing references.
- *Section-by-section catalog of which model wins which individual task (e.g., "GPT-2 beats MoEP on EWOK")*: Removed — these are descriptive observations, not structural weaknesses. The paper does not claim to win every task.
- *Strength about "lightweight linear experts outperforming SwiGLU" as a clean ablation*: Demoted — this strength conflicts with the verified weakness (28M vs 38M parameter mismatch), and per filtering rules, when a strength and weakness disagree, the weakness wins. The raw observation is still useful but must be interpreted with the confound in mind.
- *Strength about reproducibility provisions*: Kept but minimized — code release is standard practice and not a distinguishing strength.
- *"The paper cannot attribute its results to any specific component" framing*: Reframed as a specific weakness about missing ablations rather than a generic methodological complaint.

## Novel Insights

The Harsh Critic's most valuable observation is the unqualified "outperform all baselines" claim in the introduction (line 31) — this is not a minor phrasing issue but a systematic framing problem that extends to how the contribution should be understood. The paper has two stories available to it: (a) a modest and well-supported claim that MoEP achieves competitive results while keeping parameters fixed, and (b) an overreaching claim that it beats all baselines. The paper keeps sliding between (b) in the introduction and (a) in the results section, which creates an inconsistency that harms credibility. The Strength Finder is correct that the fixed-parameter-count achievement is genuine and worth highlighting; the paper would be stronger if it led with that as the central contribution rather than the fragile outperformance claim.

## Suggestions

1. **Add a standard FFN-level MoE baseline.** Create a 28M-parameter MoE model by replacing GPT-2's FFN layers with top-2-out-of-4 routed experts, with expert dimensions scaled to match the total parameter budget. This is the single most important missing experiment and would directly test whether MoEP's layer-level parallelism provides benefits beyond vanilla MoE sparsity.

2. **Report FLOPs per token and activated parameter ratio for each architecture.** This turns the "efficiency" claim from unsubstantiated to measurable. If MoEP achieves its results with, say, 30% fewer FLOPs than the dense GPT-2, that is a meaningful efficiency story even if the aggregate scores are similar.

3. **Ablate the routing mechanism.** Compare top-k routing against random block selection in the parallel layers. If routing is driving performance, the random variant should degrade. If it does not, the paper's explanation for its results needs revision.

4. **Match parameter counts for the SwiGLU variant**, or report per-parameter scaling trends so the comparison is interpretable.

5. **Use a consistent and qualified framing.** The introduction's claim (line 31) should be explicitly qualified to match the more careful statement in Section 5.1.

## Score and Decision

I cannot use the calibration tool as it was unavailable. Based on my assessment:

**Score: 4.0** — The paper has a genuinely interesting core architectural idea (fixed-parameter sparsity via layer-level parallel blocks with routing) and is clearly described. However, the experimental evaluation has multiple significant gaps: the central performance claim is misleadingly framed, a critical baseline (standard MoE) is absent, the SwiGLU comparison is confounded by parameter mismatch, efficiency is never measured despite being in the title, and no ablations support the architectural choices. The evidence as presented does not convincingly establish that MoEP works better than alternatives. A substantially strengthened version with proper baselines and measurements could be acceptable.

**Decision: Reject** (borderline — the core idea has merit but the evaluation is insufficient to support the claims).

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>