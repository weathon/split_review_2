Now I have enough information for calibration. Let me write the final review.

## Summary

This paper identifies a genuine limitation in time series forecasting — the "self-stimulation" assumption where models use only historical values and ignore external influences — and proposes Influence-Aware Time Series Forecasting (IATSF). It provides control-theoretic analysis proving an irreducible error bound under self-stimulation (Proposition 2.1) and showing that measurable influence information reduces this bound (Proposition 3.1). The paper contributes a leak-free, temporally-synced benchmark with textual influence data across toy, real-world, and human-driven systems, and presents FIATS, a model with Channel-Aware Adaptive Sensitivity Modeling (CASM) and Channel-Aware Parameter Sharing (CAPS) mechanisms. Experiments across synthetic and real-world datasets demonstrate FIATS outperforming baselines by incorporating textual influence descriptions.

## Strengths

- **Control-theoretic grounding that directly links to architecture design.** The paper formalizes a genuine limitation (Proposition 2.1's irreducible error bound under self-stimulation) and proves that incorporating influence data reduces this bound (Proposition 3.1). The CASM mechanism (Section 5) is a clean operationalization: query as channel sensitivity, key as influence filter, value as influence translator. This theory-to-architecture bridge is rare in time series work and the attention maps in Figure 5 indeed show interpretable sensitivity patterns (e.g., pressure channel attending to pressure-related sentences). This is the paper's strongest contribution.

- **Ablation study correctly isolates the role of influence information from the role of channel-wise sensitivity.** Table 3's design is well-structured: "Zero News" (removing all influence input) drops performance from 0.182→0.249 MSE, while "Zero Desc." (removing channel descriptions only) drops to 0.209. This cleanly separates the contribution of the influence signal itself from the contribution of the CASM mechanism's channel-specific modeling. The further degradation from 0.209 (Zero Desc.) to 0.249 (Zero News) confirms that even without CASM's channel-specific queries, the raw influence embedding still provides value.

- **Leak-free benchmark fills a genuine gap.** The temporal-sync requirement and independence principle for influence data are well-motivated. The GAUD dataset (developer logs for game activity) is particularly clean as a test of external influences, and the weather datasets are constructed from publicly available forecasts rather than ex-post observations.

## Weaknesses

### Major

- **FIITS column in Table 1 is completely undefined.** The main results table includes a "FIITS" column with results substantially worse than FIATS (e.g., FM Toy pred_len 14: 0.282 vs. 0.003), but the paper never explains what FIITS is — whether it is an ablation (FIATS without influences), a different model variant, or a typo. This omission undermines the interpretability of the central experimental result. The paper must define this and discuss what the comparison shows.

- **Uneven comparison between FIATS and baselines blurs what the experiments demonstrate about architecture vs. information availability.** FIATS receives textual influence data (weather forecasts, developer logs) that none of the baseline models (DLinear, PatchTST, Chronos-L, MOIRAI-L, Time-MoE-U) receive. The headline claims (36.0% MSE reduction on Atmospheric Physics, 44.3% on NYC Traffic) compare a model with strictly more input information against models with less. This validates the paradigm (influence information helps) but does not directly validate FIATS's specific architectural mechanisms (CASM/CAPS) as the best way to use that information. While the ablation (Zero News) controls for this internally, the paper would be substantially stronger with an influence-aware baseline that receives the same text data via a simpler integration method (e.g., concatenating text embeddings with patch embeddings in a standard transformer). Without this, the claim that performance gains "stem from principled influence modeling, not architectural complexity" (line 29) is only partially supported.

### Minor

- **"LLM-free" terminology overstates the case.** The paper calls FIATS "LLM-free" (lines 23, 131), but the text embeddings come from models derived from large language models (OpenAI text-embedding-ada-002, MiniLLM, mpnet). The paper correctly explains that FIATS uses frozen embeddings without generative LLM fine-tuning, but "LLM-free" invites justified criticism. "Does not fine-tune generative LLMs" or "uses frozen text embeddings" would be more precise.

- **The "independent influence" framing for weather datasets could be more precise.** The paper calls weather forecasts "independently evolving influences — external factors that influence the system but are not themselves outcomes of it" (Section 4.1). For Atmospheric Physics, the forecast text and the target variables describe the same physical system. A weather forecast is not independent in a causal sense — it is a correlated signal about the same underlying state, produced by a separate model (NWP). The paper's core claim (external information helps forecasting) is unaffected, but the framing overstates the conceptual separation. This matters because it opens the door to a form of information leakage if the forecast encodes signal about the target distribution that the time series history alone does not capture.

- **No uncertainty estimates on main results.** Table 1 reports point estimates without variance or confidence intervals. Many gaps are modest (e.g., Electricity Utility pred_len 96: FIATS 0.124 vs. PatchTST 0.130), and without uncertainty estimates it is unclear which differences are meaningful. This is standard practice to address in revision.

### Trivial

- **Noise robustness experiment (Figure 6).** The experiment shows noisier influence embeddings monotonically degrade performance, which is consistent with Proposition 3.1 but is also trivially true of any input feature in any model. This does not specifically test anything about the IATSF framework.

## Nice-to-Haves

- An influence-aware baseline that receives the same text data via a simpler integration method (e.g., concatenating text embeddings with patch embeddings, standard transformer decoder) would directly test whether FIATS's CASM/CAPS mechanisms outperform simpler alternatives.
- Clarifying what inputs TimeLLM was given for the textual datasets would help interpret the comparison (Table 1).
- The GAUD dataset provides the cleanest test of the paradigm (developer logs are genuinely external). Expanding this evaluation with tabular results alongside Figure 4 would strengthen the paradigm-level claim.
- Clarifying the temporal split of influence data in Atmospheric Physics (whether the weather forecasts used at training time are pre-forecast or would have been available at the time) would address reproducibility concerns.

## Removed Points

- **"CAPS under-specified"**: Removed. The paper specifies the cross-attention formulation (Q = U_f^c, K,V = Z̃) with causal masking (line 166). This is sufficient for a conference paper.
- **"Self-stimulation being a known finding"**: Removed. The paper uses this as motivation, not as a claimed contribution. This is a framing preference, not a weakness.
- **"Full-observability assumption is a limitation"**: Removed. The paper explicitly states this is "for analytical clarity" (line 43). The assumption is reasonable for the theoretical analysis.
- **"GAUD underplayed"**: Removed. The paper provides Figure 4 results and a full subsection (Section 6.3).
- **"Electricity Utility holiday influence is too weak"**: Removed. The paper frames this as a simple dataset, and the modest gap (0.124 vs. 0.130) is consistent with that framing. The reviewer's claim of 4.6% improvement is selective reading.
- **"TimeLLM not specified" framing as major weakness**: Demoted from a separate weakness to a Nice-to-Have. The paper provides results for TimeLLM but does not specify its input modality for the text datasets, which is a clarification issue, not a core flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Define FIITS in the paper (or, if it is an ablation — FIATS without influence input — rename and discuss it explicitly as the primary control).
2. Add an influence-aware baseline that receives the same text data via a simpler integration method, to directly test whether CASM/CAPS provide architectural benefits over naive text fusion.
3. Replace "LLM-free" with more precise terminology (e.g., "uses frozen text embeddings without generative LLM fine-tuning").
4. Clarify the temporal split design for the Atmospheric Physics influence data (are the weather forecasts from before the prediction time?).
5. Report variance or confidence intervals on main results (Table 1).
6. Add a sentence specifying what inputs TimeLLM received for the textual datasets.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mfc6FKgtQA.md (TGTSF) | 5.00 | R1 (3.5–5.5) | Topically very similar (text-guided TSF, cross-attention, benchmarks). Current paper has stronger theory and more principled architecture, but shares the same evaluation asymmetry gap. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QE1ClsZjOQ.md (Dual-Forecaster) | 4.50 | R1 (3.5–5.5) | Similar multimodal TSF with text. Current paper has better theoretical grounding and cleaner benchmark design. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uRXxnoqDHH.md (MoAT) | 5.00 | R1 (3.5–5.5) | Multimodal TSF with augmentation. Current paper has stronger theoretical contribution and interpretability. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oANkBaVci5.md (Simple Baseline) | 6.75 | R1 (5.5–7.5) | Stronger evaluation (8 datasets, 15 baselines). Current paper has comparable theoretical contribution but weaker evaluation rigor. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TYXtXLYHpR.md (Transparent TSF) | 5.75 | R1 (5.5–7.5) | Interpretability-focused. Current paper has stronger empirical results but less thorough evaluation framework. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2wwPG1wpsu.md (LST-Bench) | 2.50 | R1 (1.5–3.5) | Much weaker — benchmark-only without model or theory. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/nSDOkm0SKo.md | 1.00 | R1 (<1.5) | Not real research — far below current paper. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md | 1.00 | R1 (<1.5) | Not real research — far below current paper. |

**Initial bracket:** [5.0, 6.5] — above the rejected but similar TGTSF (5.0) and below the accepted Simple Baseline (6.75).

**Narrowing rationale:** The paper sits above TGTSF (5.0, rejected) because of its control-theoretic grounding and principled CASM/CAPS architecture, which TGTSF lacks. It sits below the Simple Baseline paper (6.75, accepted) because of two concrete evaluation gaps that Simple Baseline did not have: (1) the undefined FIITS column in the main result table, and (2) the uneven comparison against baselines without text data. Both issues are fixable but currently weaken the evidence. The score of 5.5 reflects a paper with genuine theoretical and architectural contributions that needs to strengthen its evaluation design.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>