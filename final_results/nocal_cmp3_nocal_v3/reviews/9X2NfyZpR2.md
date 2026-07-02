Good — the CTC inconsistency is confirmed. Now let me produce the final review.

## Summary

This paper introduces TbLTA, the first weakly-supervised framework for dense Long-Term Action Anticipation (LTA) that uses only video transcripts (ordered action lists without timestamps or durations) during training — no frame-level annotations. The architecture combines a transformer encoder, an ATBA-style temporal alignment module (to generate pseudo-labels), a cross-modal attention layer that contextually grounds video features using transcript embeddings, and an anticipation decoder with CRF-based sequence refinement. Evaluated on Breakfast, 50Salads, and EGTEA, the deterministic variant achieves strong results on Breakfast (beating all supervised baselines at 30% observation) while showing more modest performance on 50Salads and EGTEA. A stochastic variant that samples multiple futures is also reported.

## Strengths

1. **First weakly-supervised dense LTA method.** The paper correctly identifies that existing dense LTA methods rely on expensive frame-level annotations, and it proposes the first approach trained exclusively from transcripts. This is a novel and timely direction for reducing annotation cost while retaining the semantic signal most relevant to procedural understanding.

2. **Deterministic results on Breakfast are genuinely strong.** At Obs 30%, the deterministic TbLTA achieves 29.03 average MoC, outperforming all supervised baselines (ActFusion: 28.45, FUTR: 26.59, Cycle Cons: 25.13). This is notable: a weakly-supervised method surpassing fully-supervised counterparts on a standard benchmark.

3. **Clean architectural design.** The modular architecture — ATBA-style alignment → pseudo-labels → cross-modal enrichment → anticipation decoder with CRF — is a reasonable and well-motivated instantiation of the transcript-supervision idea for LTA.

## Weaknesses

### Fatal
None.

### Major

1. **Cross-attention module has an unresolved train-test mismatch.** The cross-attention layer (Section 3.1) uses transcript embeddings and pseudo-labels to enrich video features: "The enriched features X̂, contextually grounded by the actions and objects described in the transcript, are then used for both TAS and LTA" (line 138). However, at inference, the paper states "only [E || X_obs] is provided" (line 116) and the inference path in Figure 2 does not include the cross-attention module — no transcript is available at test time. The paper never specifies whether cross-attention is simply dropped at inference, whether the transcript is somehow reconstructed, or how the downstream heads (trained on enriched features) cope with non-enriched features at inference. This is a genuine architectural gap in the description: the model as described does not have a well-specified inference-time behavior for a core component. The authors should clarify how they bridge this mismatch and ideally quantify its impact (e.g., by comparing against a variant that removes cross-attention from both training and inference).

### Minor

1. **Ablation study uses the stochastic-oracle Top1 metric rather than the deterministic metric.** The ablations (Section 4.3, Table 4) report "Top-1 MoC" which corresponds to the stochastic protocol — selecting the best among multiple generated futures. The paper justifies this as providing "a stable reference point" (line 231), but this metric is an oracle evaluation not achievable by a deterministic system. A component that adds diversity could improve stochastic-oracle Top1 while degrading the deterministic output that would be used in deployment. Ablations should also be reported for the deterministic setting.

2. **No variance or error bars reported.** Results are averaged over 4 splits (Breakfast) or 5 splits (50Salads), yet no standard deviations or per-split ranges are provided. Given the small dataset sizes (50Salads has only 50 videos), it is impossible to assess whether reported differences (e.g., the ~0.6–0.8 point drops in the CTC ablation) are statistically reliable.

3. **WS-DA comparison is limited and uses a different supervision budget.** The only weakly-supervised baseline, WS-DA (Zhang et al., 2021), uses frame-level labels on the observed portion — more supervision than TbLTA. While beating a method with more supervision is genuinely interesting, only a single configuration (Obs 30%, horizon 10%) is reported, making the comparison incomplete across the evaluation grid.

4. **CTC loss notation inconsistency.** The segmentation head predictions π are defined as having length αT (observed frames only, line 160), but Equation 4 sums the product over t=1..T (all frames). The paper should clarify whether the CTC operates over the full video (using features from both observed and future portions during training) or only over the observed portion.

### Trivial
None.

## Nice-to-Haves
- The duration loss relies on pseudo-label quality through its momentum buffer, but the paper does not analyze how sensitive this loss is to alignment noise or how the buffer is initialized and updated.
- On EGTEA, only two baselines (Timeception, Anticipatr) are compared. Including more recent supervised LTA methods would strengthen the benchmark comparison.
- The qualitative analysis offers only two examples and acknowledges that duration prediction is challenging, but does not analyze systematic failure patterns (e.g., overpredicting short actions, confusing adjacent procedural steps).

## Removed Points
These points are flagged to be removed; treat them with caution.

- **"Central claim of 'competitive with, occasionally superior to' rests on stochastic protocol"** — Removed because the paper's deterministic results on Breakfast Obs 30% genuinely beat all supervised baselines (29.03 vs 28.45 ActFusion). The paper separates deterministic and stochastic results clearly in the table (bold vs gray, with * marking stochastic), and the text explicitly states "in certain settings" (lines 227, 291). The evidence supports the claim in the deterministic setting for Breakfast.
- **"Abstract overclaims"** — The abstract says "robust and less costly alternative," not "superior." This is accurate framing given the results.
- **"Duration loss sensitivity to pseudo-label quality"** — Moved to Nice-to-Haves. The momentum buffer mechanism is described; further analysis would strengthen but is not a core flaw.
- **"Qualitative results only two examples"** — Too minor; most papers show a comparable number of qualitative examples.
- **"EGTEA baselines are old"** — Moved to Nice-to-Haves. The paper's main evaluation is on Breakfast/50Salads; EGTEA is an additional benchmark.

## Novel Insights
None beyond the paper's own contributions. The reviews surfaced the cross-attention train-test mismatch and the ablation-metric concern as issues the paper itself does not discuss, but these are design/description gaps rather than novel analytical insights about the problem domain.

## Suggestions
1. **Clarify the cross-attention inference behavior.** State explicitly whether the cross-attention module is used at inference, and if not, explain how the downstream heads handle the feature mismatch. Add an ablation that removes cross-attention from training entirely to quantify the impact of the enrichment.
2. **Report ablations using the deterministic metric** in addition to the stochastic Top1 metric, so the practical value of each component is interpretable.
3. **Add variance estimates** (standard deviations over splits) for all main results.
4. **Fix the CTC notation** in Equation 4 to match the domain of π.
5. **Expand or de-emphasize the WS-DA comparison** — either report results for more configurations or clarify that the comparison is illustrative rather than a direct head-to-head.

## Score and Decision
**Score:** 6  
**Decision:** Accept

The paper's core contribution — demonstrating that transcript-only supervision can drive dense LTA, with strong deterministic results on Breakfast — is novel and significant. The main concern is the cross-attention train-test mismatch, which is a description gap rather than a fatal design flaw (the reported results still demonstrate the approach works, but the inference-time behavior of a core component needs clarification). The other weaknesses (ablation metric, missing variance, limited WS-DA comparison) are addressable. Overall, the paper opens a promising new direction for annotation-efficient LTA, and the evidence, while imperfect, supports its central thesis.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>