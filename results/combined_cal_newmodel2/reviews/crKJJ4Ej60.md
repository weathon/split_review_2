Now I have strong calibration. Let me produce the final review.

**Round 1 bracket:** I compared the paper against anchors spanning all score bands. The paper is clearly well above the reject-range papers (1.0-3.4) — it has a real method, real experiments, and real results. It is comparable to but somewhat weaker in evaluation completeness than papers in the 6.25–7.33 range (Sufficient Context, Retrieval is Accurate Generation, ReDeEP, Situated Faithfulness). It is clearly below the 8.0-range papers (Trustworthy RAG, Retrieval Head) in evaluation thoroughness.

**Round 2 narrowing:** I focused on the 5.5–7.5 band. The most directly comparable anchor is "Enhancing LLMs' Situated Faithfulness to External Contexts" (avg 7.25), which addresses the same problem with a more complete evaluation. Our paper's idea is arguably cleaner, but the evaluation gap (missing non-counterfactual baseline comparisons) is a real weakness that Situated Faithfulness does not share. The second closest anchor, "Is Factuality Enhancement a Free Lunch?" (avg 6.67), has a different contribution type (analysis vs. method) but similar evaluation thoroughness.

**Final score placement:** The paper's strengths (clean idea, well-designed pipeline, striking data efficiency, interesting mechanistic analysis) are genuine and well-supported. The main weakness — missing baseline comparisons in non-counterfactual settings — is significant but not fatal. The paper shows improvements over base models in non-counterfactual settings (Table 3) and strong results in counterfactual settings against strong baselines (Table 1). The evaluation gap prevents it from reaching the 7+ range but does not invalidate the core contribution. I place it at **6.5**, matching the lower-to-middle of the accept-range anchors.

## Summary

This paper proposes Copy-Paste, a generation paradigm that directly embeds contextual fragments into LLM responses to mitigate contextual faithfulness hallucinations in RAG. The approach is instantiated through a two-stage pipeline: (1) Copy-Paste-Prompting generates high-copying responses via three methods spanning hard extractive constraints (CP-Order) to soft iterative refinement (CP-Refine), and (2) CopyPasteLLM internalizes a preference for high-copying responses via DPO training on automatically constructed preference pairs. On FaithEval, CopyPasteLLM achieves 12.2%–24.5% accuracy improvements over the best baselines using only 365 training samples (50× less data). The paper also introduces the Context-Parameter Copying Capturing algorithm for mechanistic analysis, revealing that CopyPasteLLM recalibrates confidence in parametric knowledge rather than enhancing contextual representations.

## Strengths

- **Clean, intuitive core insight:** The observation that copying degree inversely correlates with contextual faithfulness (Section 2.2) is practically motivated, and the solution of directly embedding context fragments sidesteps a genuine failure mode of current RAG systems. [favorability=11.47]
- **Well-conceived two-stage pipeline:** Decoupling high-copying response construction (Stage 1) from preference internalization via DPO (Stage 2) is methodologically elegant. The three prompting methods (CP-Order, CP-Link, CP-Refine) form a clear spectrum from hard extractive constraint to soft iterative refinement. [favorability=15.58]
- **Striking data efficiency:** Using only 365 training samples to outperform methods trained on 10,000–32,580 samples (Table 1) is the paper's most impressive result, suggesting the preference data construction pipeline is highly effective at distilling the desired behavior. [favorability=12.62]
- **Mechanistic analysis adds useful depth:** The Context-Parameter Copying Capturing algorithm (Section 3.3) and the finding that CopyPasteLLM reduces confidence in parametric knowledge rather than enhancing contextual representations (Figure 4) is a genuinely interesting and non-obvious observation. [favorability=14.77]
- **Copy-Paste simultaneously addresses faithfulness and attribution:** The paper correctly notes that copied content serves as its own evidence of faithfulness (Section 1), a genuine advantage over citation-based methods which must separately verify content-source consistency. [favorability=11.64]

## Weaknesses

### Major

- **Missing baseline comparisons in non-counterfactual evaluation (Table 3):** Table 3 compares CopyPasteLLM only against untuned base models on non-counterfactual (original context) settings. The strongest baselines from Table 1—Context-DPO (18,000 samples), Canoe (10,000), ParamMute (32,580)—are absent. The reader cannot assess whether CopyPasteLLM's gains on non-counterfactual data are actually competitive with these methods, or whether there is a trade-off where counterfactual gains come at a cost to factual performance. This asymmetry is the most significant weakness in the experimental evaluation. [favorability=-1.70]

- **Evaluation primarily on counterfactual benchmarks where the method's trained behavior is perfectly aligned with the evaluation objective:** Table 1 evaluates exclusively on counterfactual scenarios where the model must override parametric knowledge to follow provided context. CopyPasteLLM is explicitly trained (via DPO) to prefer copying from context, which is exactly the correct behavior on counterfactual data. Baselines like Context-DPO are designed for a more balanced policy (deciding when to trust context vs. parametric knowledge). While the method's strong performance on counterfactual data is a useful capability, the evaluation design makes it difficult to assess whether there is a meaningful trade-off. [favorability=0.29]

### Minor

- **The correlation observation in Section 2.2 lacks quantitative rigor:** Only a qualitative statement about a "clear pattern" based on kernel density visualization is provided for the claimed inverse correlation between copying degree and hallucination density. No correlation coefficient (Spearman or Pearson) or confidence interval is reported. For a claim that motivates the entire approach, the evidence is thinner than it should be. [favorability=1.82]

- **No human evaluation of response quality:** The automated metrics (MiniCheck, AlignScore, hallucination metrics) all measure faithfulness to context, which naturally favors copy-heavy responses. The paper acknowledges that CP-Order and CP-Link "sacrifice fluency" (Table 2 shows consistently lower perplexity for baselines) but does not evaluate whether responses with κ=0.93 (overwhelmingly copied text) are genuinely useful to end users along dimensions like informativeness, coherence, and naturalness. [favorability=4.63]

- **Preference data construction pipeline is not ablated:** The multi-criteria filtering (AlignScore, MiniCheck, κ, δ, embedding similarity, perplexity) and Elo tournament ranking are described but their individual contributions are not measured. It is unclear how many candidates survive each filtering stage and how sensitive the downstream results are to threshold choices. [favorability=5.50]

- **GPT-4o comparison (92.8% vs. 47.5%) is not apples-to-apples:** GPT-4o is evaluated zero-shot, while CopyPasteLLM is fine-tuned on data drawn from the same distribution it is tested on. This comparison inflates the apparent superiority and should be contextualized more carefully. [favorability=3.23]

- **Training data composition is underspecified in the main text:** Table 1 mentions "241 samples used for training CopyPasteLLM" removed from FaithEval, but the total training set is 365 samples. The source of the remaining ~124 samples and whether the selection from FaithEval is random or biased is not clearly described in the main paper body (deferred to the appendix). [favorability=4.83]

### Trivial

- **No confidence intervals or statistical significance tests** are reported for the main results (Tables 1, 2, 3), despite the small training set (365 samples) where variance could be nontrivial. [favorability=-1.40]

## Nice-to-Haves

- Report compute costs for generating the 365 preference pairs (multiple LLM calls per sample for CP-Refine, Elo tournament judging).
- Include failure case analysis: characterize question types where copying is insufficient (e.g., multi-hop reasoning, comparison questions).
- Add sensitivity analysis for DPO hyperparameters and filtering thresholds.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The inverse correlation is near-tautological" (Harsh Critic Issue 2):** Removed because this overstates the case. The correlation is between copying degree and hallucination density across different models' responses. A model could copy some parts and hallucinate in non-copied parts, so the relationship is empirical, not definitional. However, the related concern about missing a correlation coefficient is retained as a minor weakness above.

- **"394 unaccounted samples in FaithEval" (part of Harsh Critic Issue 5):** Removed because it stems from a misreading. The paper states 365 TOTAL training samples (not "365 from FaithEval"), and 241 of these are from FaithEval. FaithEval has 1000 samples total, so 1000 - 241 = 759 for testing. All samples are accounted for. The concern about selection bias in how the 365 are chosen is retained.

- **"The comparison between train-set performance and test-set performance" (Context-DPO ConFiQA <sup>T</sup>):** Removed because Context-DPO's ConFiQA results are explicitly marked as <sup>T</sup> (trained on that data), and the paper does not claim otherwise. The comparison is still informative as a "strong upper bound" comparison, and the paper also evaluates Context-DPO on FaithEval (unseen) where CopyPasteLLM outperforms it.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add Context-DPO, Canoe, and ParamMute comparisons in the non-counterfactual setting (Table 3).** This is the single highest-leverage addition. It would directly address whether the method's counterfactual strength comes at a cost to factual performance, and it would complete the evaluation story.

2. **Report Spearman's ρ (or similar) with confidence intervals** for the correlation between copying degree and hallucination density in Section 2.2.

3. **Include a small-scale human evaluation** of response quality (fluency, informativeness, naturalness) to validate that high-copying responses are genuinely useful, not just mechanically high-scoring on automated metrics.

4. **Clarify the training data split** in the main text: how the 365 samples are selected, what fraction comes from each dataset, and whether the selection is random or stratified.

## Score and Decision

**Round 1 bracket (initial range):** After comparing against anchors spanning 1.0 to 8.0, I narrowed to the 5.5–7.5 range. The paper is clearly above reject-range papers (1.0–3.4) which lack substantive methods, and well below strong-accept papers (8.0) which have exceptionally thorough evaluations. The most directly comparable anchor is "Enhancing LLMs' Situated Faithfulness to External Contexts" (avg 7.25), which addresses the same problem with a more complete evaluation.

**Round 2 narrowing:** I compared itemized favorability ratings between the paper under review and the closest anchors. Compared to "Situated Faithfulness" (7.25), the paper under review has a cleaner idea and more striking data efficiency, but its evaluation has a significant gap that the anchor does not (missing non-counterfactual baseline comparisons). Compared to "Is Factuality Enhancement a Free Lunch?" (6.67), the paper under review has stronger novelty and a more impactful contribution but a less thorough evaluation. Compared to "Retrieval is Accurate Generation" (7.0), which has a similar extractive-generation approach, the paper under review has a more practical pipeline but a less complete evaluation.

**Final calibration:** The paper's core contribution is genuine — the copy-paste paradigm is clean, the pipeline is well-designed, and the data efficiency is impressive. The evaluation gap (missing baseline comparisons in non-counterfactual settings) is the main factor limiting the score, as it prevents full verification of the paper's broader claims. This places the paper below the 7+ anchors (which have more complete evaluations) but clearly above the 5–6 anchors (which have weaker contributions or less clean ideas).

All anchors retrieved:
| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 8QTpYC4smR.md | 1.0 | R1 | No | Survey paper, not comparable |
| 5kMwiMnUip.md | 1.4 | R1 | No | Jailbreaking LLMs, not comparable |
| a2rSx6t4EV.md | 2.33 | R1 | No | EDU-RAG benchmark, weaker contribution |
| IlleFmPNb6.md | 3.4 | R1 | No | Training-free RAG for VQA, less relevant |
| JnWJbrnaUE.md | 3.75 | R1 | No | Corrective RAG, less novel |
| mCnWT9OVvK.md | 5.25 | R1 | Yes | Understanding Retrieval Augmentation for LFQA, analysis paper |
| K2jOacHUlO.md | 7.25 | R2 | Yes | **Most comparable anchor**: Situated Faithfulness, more complete evaluation |
| asGQQc7gNo.md | 6.67 | R2 | Yes | Factuality vs. Faithfulness trade-off, analysis paper |
| WPZ2yPag4K.md | 5.75 | R2 | No | Fine-tuning for factuality, similar topic |
| d2H1oTNITn.md | 6.40 | R2 | No | Mask-DPO for factuality, similar technique |
| oXYZJXDdo7.md | 7.0 | R1 | Yes | "Retrieval is Accurate Generation", similar extractive approach |
| ztzZDzgfrh.md | 7.33 | R1 | Yes | ReDeEP, hallucination detection via mechanistic analysis |
| Iyrtb9EJBp.md | 8.0 | R1 | Yes | Trustworthy RAG, very thorough evaluation |
| Jjr2Odj8DJ.md | 6.25 | R2 | Yes | Sufficient Context, analysis paper |

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>