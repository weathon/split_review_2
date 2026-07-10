Now I have all the information needed to write the final consolidated review and assign the score.

## Summary

The paper proposes **Steady Thought (ST)**, a three-stage framework (thought segmentation via entropy, thought completion via suppressed-decoding, and thought-level preference optimization via STPO) to mitigate "under-thinking" in Large Reasoning Models — where models find correct reasoning thoughts early but abandon them through excessive switching. The method is evaluated on DeepSeek-R1-Distill-Qwen (1.5B, 14B) and Qwen3-8B across four math/code benchmarks, showing accuracy improvements of up to ~5.3% with output length reductions of 19–39%.

## Strengths

- **Well-motivated problem with empirical grounding.** Figures 1a/b concretely demonstrate that LRMs often find correct thoughts early (low rank of first correct thought) but still generate many additional thoughts, providing clear evidence that under-thinking is a real failure mode.
- **Clean adaptation of SimPO to the thought level.** The STPO loss (Eq. 7) conditions on (Q, T_i) rather than just Q and applies the preference signal at the exact reasoning divergence point. This is a principled way to avoid the noisy holistic rejection problem of whole-response DPO.
- **Consistent empirical trends across model scales (1.5B, 8B, 14B).** ST improves or maintains accuracy on most datasets while reducing token usage. Gains are clearest on Qwen3-8B (+3.12% accuracy, −25.5% tokens) and DeepSeek-R1-Distill-Qwen-14B (+2.52% accuracy, −17.3% tokens). OOD generalization to LiveCode is a genuine positive signal.
- **Informative ablation comparing training objectives (Table 4).** STPO outperforms both SFT (which also shortens outputs) and DPO on the same data pipeline, showing that the preference optimization component — not simply fine-tuning on shorter completions — drives the gains.

## Weaknesses

### Major

- **Training data generation confound.** The chosen completions in STPO preference pairs are generated under suppressed-decoding conditions (logits of trigger words like "wait" and "alternatively" driven close to zero, per Sec. 3.2). At inference, no such suppression is applied. The model is trained to prefer outputs from a distribution it cannot replicate at test time, making it difficult to tell whether accuracy gains come from genuine reasoning improvement or from learning surface-level properties of suppressed-decoding completions (e.g., shorter sentence structure, specific phrasing patterns). This is a real confound in the method design that should be isolated via an ablation where chosen completions are generated *without* logit suppression (e.g., by sampling multiple rollouts and selecting correct ones that naturally stay on track).

- **The central mechanistic claim is not fully supported.** The paper claims ST teaches the model to "recognize and commit to a promising intermediate thought" (Abstract, Sec. 3.3), but the observed effects (shorter outputs, fewer switches) are also consistent with a simpler global shortening bias. Some results actively conflict with the claimed mechanism: on DeepSeek-R1-Distill-Qwen-1.5B for AIME 2024, the number of thoughts *increases* (12.87 → 18.21) while the proportion of last thought *decreases* (18.96% → 15.66%, Figure 2a). The paper's explanation ("smaller models tackling high-difficulty problems tend to increase thought transitions") is ad-hoc and does not demonstrate selective commitment (i.e., committing to promising thoughts while still exploring unpromising ones).

### Minor

- **No variance or confidence intervals reported for main results (Table 1).** The paper states "average of eight test runs for AIME 2024" but provides no standard deviations or significance tests. Given modest accuracy improvements (1–5%), statistical significance is essential to establish that gains are not within the noise range.

- **SEAL outperforms ST on one metric without discussion.** On Qwen3-8B LiveCode, SEAL achieves 83.4% vs. ST's 77.1% (Table 1). The paper frames this as "ST still achieved positive results" without acknowledging where SEAL does better. While ST wins on overall average accuracy (83.35% vs 82.58%) and token efficiency (4558 vs 6940), the LiveCode gap deserves acknowledgment and discussion.

- **GSM8K accuracy decrease not mentioned.** DeepSeek-R1-Distill-Qwen-1.5B shows a GSM8K accuracy drop (81.9% Vanilla → 81.3% ST, Table 1) that is not noted in the main discussion.

- **Logit suppression mechanism is vaguely specified.** Section 3.2 states "sharply decrease the logits... driving their prediction probability close to zero" without quantitative detail (subtraction factor, temperature modification, or top-k filter), hindering reproduction.

- **Entropy threshold detection is underspecified.** Section 3.1 states "any of the initial tokens at the beginning of a candidate step" without specifying how many tokens are checked, making the segmentation procedure difficult to reproduce precisely.

### Trivial

None.

## Nice-to-Haves

- Generate chosen completions without logit suppression and verify the gains hold, to separate the preference optimization signal from the decoding confound.
- Add a controlled analysis comparing switching behavior when the first thought is correct vs. incorrect, to directly test selective commitment rather than global shortening bias.
- Compare against training-time alternatives (e.g., RL with switching penalties, or fine-tuning on curated switching-free trajectories) rather than only inference-time baselines.
- Provide quantitative specification of the logit suppression mechanism and the entropy threshold detection rule.

## Removed Points

These points were flagged by the harsh critic but are removed per the filtering rules. Treat them with caution:

- **"Method for labeling intermediate thoughts as correct should be in main paper"**: The paper does describe this — Section 3.2 states "By evaluating the correctness of that final answer, we can determine whether the thought was a valid one." The method is in the main text.
- **"Entropy threshold analysis is thin (only one model, three values)"**: The paper states threshold tuning on more models is in Appendix D, which was stripped by the parser. Per rules, missing appendix content is not a valid weakness.
- **"Computational cost should be stated explicitly in the main paper"**: The paper directs readers to Appendix E for this, which was stripped by the parser.
- **"NOWAIT catastrophic degradation on Qwen3-8B not discussed"**: This describes a baseline's behavior, not a weakness of the proposed method.
- **"Formatting: table header arrows reversed"**: Pure formatting artifact; parser issue, not author error.
- **"Missing related works"**: Per rules, cannot be verified without external sources.
- **"DPO is actually quite competitive on AIME (30.8% vs STPO 31.2%)"**: The paired comparison shows STPO achieves comparable accuracy with far fewer tokens (8608 vs 10701), supporting the paper's length-normalization argument.

## Novel Insights

None beyond the paper's own contributions. The reviews surfaced verification questions about experimental design and mechanistic attribution (training data confound, alternative explanations for observed effects) but did not produce a genuinely novel interpretation of the results that the paper itself does not already contain.

## Suggestions

1. **Fix the training data confound:** Generate the "chosen" completions *without* logit suppression — e.g., by sampling multiple rollouts and selecting correct ones that naturally avoid switching. Run this as an ablation to verify the gains hold. If they do, the confound is ruled out.
2. **Report standard deviations** for all main results, especially given the modest accuracy deltas (1–5%) and the claim of eight runs for AIME 2024.
3. **Test selective commitment directly:** Construct a controlled analysis comparing switching behavior when the first thought is correct vs. incorrect. If ST selectively commits to promising thoughts and explores unpromising ones, this would distinguish the method from a global shortening bias.
4. **Quantify the logit suppression** (e.g., subtraction factor, temperature, or top-k threshold) and the **entropy detection rule** (number of initial tokens checked) for reproducibility.

## Score and Decision

**Calibration anchors considered across all rounds:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| 5kMwiMnUip (Jailbreaking CoT) | 1.40 | R1 | No | Very weak, unrelated topic |
| Uj0h13lVrR (GFlowNets) | 1.00 | R1 | No | Very weak, unrelated |
| gwZ90hFSL2 (Cross-Lingual Robots) | 1.00 | R1 | No | Very weak, unrelated |
| pXIbcRPxWR (Supervised CoT) | 2.50 | R1 | No | Much weaker, less principled |
| jOuHjFw71C (Planning in Strawberry Fields) | 3.00 | R1 | No | LRM evaluation, different focus |
| sdpVfWOUQA (Planning with MCTS) | 3.00 | R1 | No | MCTS for LLM, different approach |
| CuwjD3cazX (LD-DPO) | 5.00 | R1 | Yes | Similar topic (DPO length). My paper has a more principled method and less severe weakness items (-0.92 vs -1.66 most negative) |
| FSlfoBIctk (LOGO) | 5.25 | R1 | No | Long-context alignment, less related |
| jRZ1ZeenZ6 (Rational Metareasoning) | 5.00 | R1 | No | Selective reasoning use, less related |
| 8QkpCRio53 (PrefOpt CO) | 5.75 | R1 | Yes | Different domain (CO). My paper's weaknesses are comparable but its method is more directly applicable |
| **O0sQ9CPzai (TPO)** | **6.33** | **R1/R2** | **Yes** | **Most similar: preference optimization for reasoning at step level. My paper's worst weakness (-0.92) is less severe than TPO's worst (-2.19). My strengths (11.6–12.7) comparable to TPO's (10.7–13.2).** |
| **VIUisLx8lQ (TypedThinker)** | **6.00** | **R1** | **Yes** | **Reasoning framework with typed thinking. My paper's weaknesses (-0.92 worst) substantially less severe than TypedThinker's (-4.10 worst).** |
| rfdblE10qm (Reward Modeling) | 8.00 | R1 | No | Too high-quality, not comparable |
| 3bq3jsvcQ1 (Take a Step Back) | 8.00 | R1 | No | Too high-quality, not comparable |
| mMPMHWOdOy (WizardMath) | 8.00 | R1 | No | Too high-quality, not comparable |
| HHKboqbkec (Multimodal ToM) | 5.75 | R2 | Yes | Different domain. My paper's weakness severity is lower. |
| CrGfGLC2Ad (Factor Level Prefs) | 5.33 | R2 | No | Preference optimization, different focus |
| ToWKyjwDqO (Direct Judgement PO) | 5.00 | R2 | No | Judge training, less related |
| TU5ApbbeDZ (Loss Landscapes PO) | 5.00 | R2 | No | Empirical study, not comparable |

**Round 1 bracket (initial):** 5.0–7.0. The paper clearly sits above the 1–3 reject tier (it has a principled method and consistent results) and below the 8+ strong-accept tier (it has unresolved methodological concerns). The closest topical anchors are TPO (6.33) and TypedThinker (6.00) in the 5.5–7.5 bracket.

**Round 2 narrowing:** The favorability comparison with TPO and TypedThinker shows that this paper's most negative weakness item (mechanism claim not supported, −0.92) is substantially less severe than TPO's worst (−2.19 for adaptive step reward lacking support) and TypedThinker's worst (−4.10 for lacking novelty). The paper's strengths (11.56–12.69) are comparable to both anchors. However, the training data confound (favorability 2.47 — recognized as real but not devastating by the scoring model) and the missing variance (−0.79) prevent the paper from reaching the 6.5–7.0 level. The paper is closer to TypedThinker (6.00) than TPO (6.33) in overall quality signal.

**Final score:** 6.0. The paper makes a genuine, well-motivated contribution (thought-level preference optimization for under-thinking) with a clean formulation and consistent results across model scales. The key concerns (training data confound, incomplete mechanistic evidence, missing variance) are real and should be addressed, but they do not invalidate the core contribution. The paper is a solid borderline accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>