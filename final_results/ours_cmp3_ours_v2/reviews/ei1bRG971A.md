## Summary

DND proposes adding a lightweight linear router to standard transformer layers that identifies "critical" tokens (those with high prediction uncertainty) and reprocesses them through the same layer in a nested pass. Two training strategies — a router controlling loss (score dispersion + distribution preservation) and a threshold control scheme (buffer proportional control + EMA synchronization) — stabilize the token selection process. DND is applied as post-training SFT on existing pretrained models and is evaluated on dense (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and MoE (Qwen3-30B-A3B) models across 17 benchmarks.

## Strengths

1. **Well-motivated design with direct empirical validation.** The paper correctly notes that not all tokens demand equal computation (Gloeckle et al., 2024) and operationalizes this via a router and nested pass. The token selection analysis (Figs. 4a, 4b) provides direct evidence that the router preferentially selects higher-entropy (more uncertain) tokens and that the nested pass reduces their entropy — this is the strongest evidence in the paper that the method does what it claims.

2. **Practical post-training positioning.** DND can be applied to existing off-the-shelf models without pretraining from scratch, a genuine practical advantage over the most closely related method, MOR (Bae et al., 2025), which requires training from scratch on 200B tokens.

3. **Consistent empirical gains across multiple models.** The method shows solid and consistent improvements across all three 1B-scale dense models (+1.88 to +2.50 average), with especially notable gains on reasoning-heavy benchmarks like BBH and GPQA (~5 points). Gains extend to the larger Qwen3-30B-A3B MoE model (+0.87 average across 17 benchmarks).

4. **Thoughtful training strategy design with ablation support.** The router controlling loss and threshold control scheme are well-engineered. The ablation (Table 4) shows the combined strategies add meaningful value, and the training visualizations (Figs. 5, 6a, 6b) concretely demonstrate that the mechanisms work as intended.

## Weaknesses

### Major

1. **Attention mechanism in the nested pass is unspecified.** Section 3.1.2 describes packing selected tokens, assigning new positional embeddings, and processing them through the same transformer layer L_i, but never states whether the self-attention uses causal masking (as in the base autoregressive model) or full attention. The paper discusses information leakage for the *routing* stage (Section 3.1.1) but not for the nested pass itself. While the most natural interpretation (causal attention + ordered packing preserving original sequence order) would preserve causal structure — making the critic's "information leakage" concern less severe than presented — the specification gap is significant enough that the core architectural mechanism is not fully verifiable from the paper as written. The authors must clarify: (a) what attention mask is used in the nested pass, (b) whether the packed sequence preserves original token order, and (c) how new positional embeddings interact with causal structure.

2. **No comparison against uniform depth increase.** DND adds a second pass through the same transformer layer for ~20% of tokens, consuming ~6% extra FLOPs. The paper does not compare against simply adding a small number of additional transformer layers (or increasing hidden dimension) with a matched compute/parameter budget. Without this baseline, it is unclear whether the gains come from DND's *adaptive* allocation or simply from having more computation available. This baseline directly tests the paper's central claim that dynamic nested depth outperforms uniform capacity increase.

3. **Insufficient post-training baselines.** The only post-training method compared is ITT (Chen et al., 2025), and only on a single model (Qwen3-1.7B) without reported hyperparameter details for the re-implementation. Other lightweight post-training approaches (e.g., LoRA, adapters, additional layers trained post-hoc) are not compared, making it hard to assess what DND uniquely contributes beyond "add more capacity via post-training."

### Minor

4. **The MOR scaling comparison is misleading.** The paper states "MOR is limited to 1B-parameter, whereas our DND successfully scales to a 30B MoE model" (Section 2.2). However, Qwen3-30B-A3B has 30B total parameters but only ~3B *active* parameters per token — comparable to MOR's 1B dense model range. The total parameter count of an MoE model is not directly comparable to a dense model's parameter count. This framing inflates the apparent scaling achievement.

5. **Practical significance at MoE scale is modest relative to throughput cost.** For Qwen3-30B-A3B, the average gain is +0.87 points, concentrated in coding tasks (BFCL +2.05, LCB-v6 +1.42) with much smaller gains on general knowledge benchmarks (MMLU +0.50, BBH +0.13, MATH +0.15). Throughput drops to 91.6–93.1% of baseline (Table 3). The paper frames this uniformly as "minimal computing increase," but a more nuanced discussion of when the cost-benefit trade-off is favorable vs. marginal would strengthen the paper.

6. **Potential router degeneracy not addressed.** The Score Dispersion Loss (Eq. 6) normalizes scores to a probability distribution and maximizes entropy, which would be trivially satisfied by a router producing uniform random scores. The paper does not discuss how the router is prevented from converging to this degenerate solution, or how the interaction between the two loss terms reliably yields task-relevant routing rather than uniform scores.

### Trivial

7. **Layer range ablation is too coarse.** Only three configurations are tested for L_s:L_e (4:23, 5:22, 3:24) with small differences (61.41 vs 61.05 vs 60.36), insufficient to make a strong claim about optimal layer placement.

8. **β initialization and learned values not reported.** The learnable fusion parameter β (Eq. 4) is described but its initialization and final learned values are not specified.

## Nice-to-Haves

- A breakdown of where the 7–9% throughput overhead comes from (router, packing/unpacking, nested attention) would help practitioners understand deployment costs.
- Analyzing whether the router produces genuinely task-relevant scores or merely high-entropy outputs would address the degeneracy concern.

## Removed Points

These points from the input review were removed with justification:

- **Information leakage as a "fatal" flaw**: Removed because the critic's concern assumes random packing order, which is not supported by the paper's description. The most natural implementation (causal attention from the autoregressive layer + ordered packing preserving original sequence position order) would preserve causal structure without leakage. Retained as Major weakness #1 (specification gap, not fatal flaw).
- **Training strategies "overstated" as essential**: Removed. The ablation shows full strategies add +0.87 over z-loss baseline — an ~86% relative improvement — which reasonably supports the paper's framing. The critic's characterization does not match the evidence.
- **Abstract "minimal computing increase" overstatement**: Subsumed by Weakness #5 (cost-benefit discussion).
- **Section-by-section notes on β initialization and layer ablation coarseness**: Moved to Trivial weaknesses #7 and #8.
- **Various formatting/style nitpicks**: Removed as parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Explicitly specify the attention masking in the nested pass — state whether causal attention is used and whether the packed sequence preserves original token order.
2. Add a baseline comparing DND against a uniform depth increase (small number of additional layers with matched FLOPs) to directly test the adaptivity claim.
3. Extend the ITT comparison to all four models and include at least one additional post-training baseline (e.g., LoRA).
4. Discuss the cost-benefit trade-off more honestly, noting which task types benefit most and where the gains are marginal.
5. Address the router degeneracy concern by analyzing whether the router's score distribution is genuinely task-correlated or merely high-entropy.

## Score and Decision

**Calibration anchors** (all papers from the deepreview_13k_calibration set):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| FiRST (`ulGwcj1egv`) | 3.00 | R1 | Router-selective layer skipping; weaker evaluation than DND |
| Stutter (`UvYrFbKj8j`) | 4.50 | R2 | Extremely similar concept (selective additional compute for challenging tokens); tested on smaller models with limited benchmarks, rejected. DND is clearly stronger. |
| CITER (`J2FyEVg8HR`) | 4.75 | R1 | Token-level routing between SLM/LLM; rejected, weaker evaluation |
| OrthoRank (`SYv9b4juom`) | 5.25 | R3 | Token selection for efficiency; rejected for insufficient theoretical justification |
| CoTFormer (`7igPXQFupX`) | 5.75 | R2 | Adaptive computation via token-level CoT-like re-application; accepted. DND has comparable quality but more structural gaps. |
| DOTS (`tn2mjzjSyR`) | 6.25 | R1 | Dynamic reasoning trajectory search; accepted with stronger evaluation |
| Learning How Hard to Think (`6qUUgw9bAZ`) | 6.50 | R3 | Input-adaptive compute allocation at decoding time; accepted with thorough evaluation |
| MoE++ (`t7P5BUKcYv`) | 8.00 | R1 | MoE with zero-computation experts; clean, well-evaluated, clear impact |

**Round 1 bracket**: 4.5–5.5. **Final reasoning**: DND is a meaningfully stronger paper than Stutter (4.50) — it tests larger models, more benchmarks, has better analysis — but falls short of CoTFormer (5.75) and Learning How Hard to Think (6.50) due to the unresolved attention specification gap (Major #1) and missing key baseline comparisons (Major #2–3). The core idea is solid and the empirical evidence is decent, but the paper needs structural revisions before acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>