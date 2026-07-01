Now let me finalize the review.

## Summary

This paper proposes Copy-Paste, a generation paradigm for RAG where models are trained to directly copy context fragments into responses as an operational proxy for contextual faithfulness. The work is instantiated through a two-stage pipeline: (1) Copy-Paste-Prompting methods (CP-Order, CP-Link, CP-Refine) that generate high-copying responses via hard and soft constraints, and (2) CopyPasteLLM, trained via DPO on only 365 samples to internalize a preference for context-copying behavior. The paper also contributes the Context-Parameter Copying Capturing (CPCC) algorithm for token-level mechanistic analysis of knowledge source usage during generation. Experiments on FaithEval, ConFiQA, and PubMedQA show strong performance, particularly in counterfactual settings, and the CPCC analysis reveals that CopyPasteLLM's effectiveness stems from recalibrating confidence in parametric knowledge rather than enhancing contextual representations.

## Strengths

1. **Well-motivated by a clear observation.** The inverse correlation between copying degree and hallucination density on RAGTruth (Figure 1, Section 2.2) provides concrete, easily verifiable empirical grounding for the paper's central hypothesis. This motivates the approach cleanly and gives the reader immediate intuition.

2. **The Copy-Paste-Prompting Stage 1 results (Table 2) are convincing and well-supported.** Across four model families (Mistral-7B, Llama-3.1-8B, Qwen2.5-72B, DeepSeek-V3) and three datasets (RAGTruth, FaithEval, PubMedQA), the three prompting methods consistently outperform baselines (Attributed, Citations) on faithfulness metrics. CP-Order and CP-Refine dominate on most settings, providing solid evidence that explicit copy-paste prompting improves contextual faithfulness. This is the cleanest comparison in the paper.

3. **The Context-Parameter Copying Capturing analysis (Sections 3.3, 4.2) provides genuine mechanistic insight.** Extending KTC (Bi et al., 2024) to full Chain-of-Thought trajectories rather than just final answers is methodologically sound. The finding that CopyPasteLLM suppresses parametric confidence rather than enhancing contextual representations (Figure 4 shows parametric distributions shift substantially while contextual distributions remain nearly co-distributed with base) is non-obvious and offers a specific, testable mechanism for how the DPO training works.

4. **Data efficiency is noteworthy.** The claim of 365 training samples versus 18,000 for Context-DPO and 32,580 for ParamMute is a practically meaningful advantage, even accounting for the confound discussed below.

## Weaknesses

### Major

1. **The FaithEval comparison is confounded by training-data distribution overlap, undermining the headline accuracy claims.** CopyPasteLLM is trained on 365 samples, of which 241 are explicitly drawn from FaithEval (Table 1 caption: "We removed 241 samples used for training CopyPasteLLM from FaithEval, with the remaining samples used for testing"). The test set is the remaining held-out FaithEval samples. Meanwhile, the strongest baseline (Context-DPO, 18K samples) was trained on a completely different corpus (Wikipedia-based adversarial contexts). This means CopyPasteLLM has been fine-tuned on data from the same distribution as the test set, while Context-DPO has seen no FaithEval data. The paper presents the FaithEval results as a head-to-head comparison (claiming "12.2%-24.5% improvement over the best baseline"), but this pattern is exactly what one would expect from a training-set-overlap advantage. On ConFiQA—where CopyPasteLLM has not seen training data—it performs competitively but does not dominate in the same way. This asymmetry weakens the central empirical claim. A proper control would train CopyPasteLLM on data entirely disjoint from FaithEval (e.g., only RAGTruth samples) and re-evaluate.

2. **The non-counterfactual evaluation (Table 3) compares only against the base model, not against published fine-tuned baselines.** In original/non-counterfactual settings, CopyPasteLLM is compared only against the base model (no DPO training). Context-DPO, Canoe, ParamMute, Attributed, Citations, and CoCoLex are all absent from this table. The abstract claims "best performance in both counterfactual and original contexts," but the evidence for "original contexts" is a comparison against only the base model—not against competing fine-tuned methods. A method trained to copy verbatim should trivially beat an untrained base model on non-counterfactual in-context QA. The meaningful question is how it compares against other fine-tuned methods in this setting, and that comparison is missing.

### Minor

3. **The GPT-4o comparison (92.8% vs. 47.5%) is presented without sufficient analysis of what drives the gap.** The paper states that CopyPasteLLM achieves 92.8% on FaithEval, "remarkably outperforming GPT-4o's reported 47.5%" (Section 4.1.2). This is an extraordinary claim, but it receives little scrutiny. If FaithEval accuracy is primarily determined by whether the model reproduces the counterfactual context verbatim, then a model explicitly trained to copy will mechanically score near-perfect, while GPT-4o's lower score may reflect a more nuanced balance between context and parametric knowledge. The paper would benefit from analyzing what fraction of CopyPasteLLM's correct answers are near-exact copies of the provided context, and discussing whether the gap is meaningful or partly an artifact of the task design incentivizing verbatim copying.

4. **The composition of the 365 training samples is underspecified in the main text.** The paper states that 241 of the 365 samples are from FaithEval (removed for testing) but does not clearly state where the remaining ~124 samples come from (referenced to Appendix Table 4, which is stripped). The main text should be self-contained enough for readers to understand the training data composition without consulting the appendix.

### Trivial

5. **The "Hit Rate" metric in Table 1 is not defined in the main paper.** The paper mentions that "exact matching is difficult due to lengthy gold answers" but does not formally specify what Hit Rate measures.

## Nice-to-Haves

- **Statistical significance or confidence intervals** would strengthen the claims, especially given the modest held-out test set sizes on FaithEval.
- **An ablation of the "stamping" procedure** (appending gold/wrong answers to chosen/rejected candidates in preference construction) would clarify how much of the 365-sample data efficiency comes from this oracle-augmented labeling versus the Copy-Paste methodology itself.
- **An evaluation on tasks where verbatim copying is inappropriate** (e.g., multi-document synthesis, summarization where the answer must integrate information not present verbatim in any single passage) would clarify the method's scope boundaries.

## Removed Points

- The harsh critic's "Issue 4" (conflating copying with faithfulness as a methodological gap) is removed. The paper explicitly defines the Copy-Paste task as maximizing lexical reuse (Section 2.1), acknowledges limitations in the ethics statement ("over-reliance on copied content may lead to verbatim reproduction of potentially biased or incorrect source material"), and scopes itself to tasks where contextual faithfulness is paramount. Criticizing a paper for not addressing tasks it explicitly scoped out is not a valid weakness.
- The harsh critic's comment about Context-DPO's ConFiQA numbers marked `<sup>T</sup>` being a "serious reporting concern" is removed. The paper transparently marks them with `<sup>T</sup>` for "seen data" and correctly restricts the comparison on those subsets. This is appropriate reporting, not a flaw.
- Several generic formatting/presentation nitpicks from the harsh critic are removed per the filtering rules.

## Novel Insights

The reviews converge on a key point the paper itself underplays: the CPCC mechanistic analysis (Section 4.2) may be the paper's strongest and most durable contribution. The finding that CopyPasteLLM works by *suppressing parametric confidence* rather than *enhancing contextual representations* is a clean, non-obvious mechanism that could inform future work on contextual faithfulness independently of the specific copy-paste methodology. This insight is more valuable than the headline accuracy numbers, which are confounded by the evaluation design.

## Suggestions

1. **Add a cross-dataset transfer experiment**: train CopyPasteLLM on 365 samples from RAGTruth (or another source entirely disjoint from FaithEval) and test on FaithEval, to demonstrate that the method generalizes beyond the training distribution. This is the single most important fix.
2. **Add fine-tuned baselines to Table 3**: include Context-DPO, Canoe, and ParamMute in the non-counterfactual comparison, or at minimum acknowledge the absence and explain why these comparisons are not feasible.
3. **Analyze the GPT-4o gap**: report what fraction of CopyPasteLLM's FaithEval answers are near-exact copies of the context, and what fraction of GPT-4o's errors are cases where it did not copy.
4. **Clarify the 365-sample composition** in the main text and formally define "Hit Rate."

## Score and Decision

**Calibration anchors:**

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| BALCONI | hPk92D2GJV | 5.25 | R2 | Same topic (context vs. parametric knowledge), less novel methodology, cleaner evaluation → Reject |
| SCOPE | dTkqaCKLPp | 5.80 | R2 | Same methodology (synthetic preference data for faithfulness), similar contribution level → Accept |
| Fine-Tuning for Factuality | WPZ2yPag4K | 5.75 | R1 | Simpler method with cleaner eval on factuality → Accept |
| Mask-DPO | d2H1oTNITn | 6.40 | R1 | DPO for factuality with cleaner evaluation → Accept |
| TRUST-ALIGN (RAG Trustworthiness) | Iyrtb9EJBp | 8.00 | R1 | Strong RAG trustworthiness paper with comprehensive eval → Accept |

**Round 1 bracket:** 5.0–6.5

**Narrowing:** The paper has more methodological novelty than BALCONI (5.25, Reject) and Fine-Tuning for Factuality (5.75, Accept), but its central empirical claims are weakened by a training-data confound that neither of those papers has. The Stage 1 prompting results and CPCC analysis are genuine strengths that lift the paper above BALCONI. The incomplete non-counterfactual comparison and underanalyzed GPT-4o comparison hold it back relative to Mask-DPO (6.40). It is closest to SCOPE (5.80) in contribution level, but with a more serious evaluation gap.

**Final score:** 5.5 — The paper has a genuinely novel paradigm and an insightful mechanistic analysis, but the headline empirical claims are undermined by a training-data confound (FaithEval) and an incomplete comparison (non-counterfactual settings). These are fixable weaknesses, but in the current form they prevent a clean acceptance.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>