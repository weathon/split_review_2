## Summary

This paper proposes Copy-Paste, a generation paradigm that directly embeds contextual fragments into responses to mitigate hallucinations in RAG systems. The authors observe an inverse correlation between copying degree and hallucination density on RAGTruth, then instantiate this through a two-stage pipeline: Copy-Paste-Prompting methods (CP-Order, CP-Link, CP-Refine) that generate high-copying responses, and CopyPasteLLM trained via DPO on automatically constructed preference pairs. On FaithEval, CopyPasteLLM achieves 92.8% accuracy (12.2–24.5% over baselines) using only 365 training samples—1/50th of Context-DPO's 18,000. The paper also introduces Context-Parameter Copying Capturing to analyze the model's internal behavior, finding it recalibrates parametric knowledge confidence rather than enhancing contextual representations.

## Strengths

- **Strong empirical results with 50× data efficiency.** Table 1 shows CopyPasteLLM achieving 92.8% on FaithEval (Llama-3-8B) vs. 80.2% for Context-DPO (the strongest fine-tuning baseline, using 18,000 samples). The improvement holds across all three backbones (12.6, 12.2, and 24.5 percentage points for Llama-3-8B, Mistral-7B-v0.2, and Llama-3.1-8B respectively). In non-counterfactual settings (Table 3), CopyPasteLLM also improves over base models by up to 20.67% on the challenging ConFiQA subsets.

- **Mechanistic discovery about parametric knowledge suppression.** The UMAP analysis (Figure 4) and logit analysis (Figure 3) reveal that CopyPasteLLM maintains nearly identical contextual knowledge representations to the base model while substantially shifting parametric knowledge distributions. This non-obvious finding—that the model works by *suppressing parametric overconfidence* rather than *enhancing contextual encoding*—provides genuine insight into how the method operates.

- **Three-prompting-paradigm design with systematic evaluation across model scales.** CP-Order (hard extractive), CP-Link (extractive+discourse glue), and CP-Refine (soft-constraint writer-reviewer loop) are evaluated across four model scales from 7B to 671B (Table 2), showing that CP-Refine best balances the faithfulness-fluency-relevance trade-off. This systematic analysis strengthens confidence in the approach.

- **Context-Parameter Copying Capturing extends prior methodology.** The paper explicitly distinguishes its algorithm from Knowledge Token Capturing (Bi et al., 2024), which analyzes only short final answers, by extending to full Chain-of-Thought response trajectories. The positional analysis in Figure 3 reveals that CopyPasteLLM achieves peak contextual knowledge utilization earlier in generation—a temporal pattern the prior method could not capture.

## Weaknesses

### Major

- **The Twist and Causal hallucination metrics in Table 2 are not defined in the main text.** The paper reports Elo-style scores from an LLM-as-Judge tournament that "diagnoses two major hallucination modes—Twist and Causal" (Section 3.2), but never states what these modes are, how the scores are computed, or what the scoring range implies. A reader cannot assess whether the reported improvements (e.g., CP-Refine's 1533.8 vs. Attributed's 1506.9 on RAGTruth-Twist) are meaningful. This undermines a significant portion of the Stage 1 experimental evidence.

- **The evaluation partially favors the behavior CopyPasteLLM was explicitly optimized for.** The primary evaluation (Table 1, FaithEval/ConFiQA counterfactual subsets) tests models on scenarios where the correct behavior is to repeat the context even when it conflicts with parametric knowledge. CopyPasteLLM was trained via DPO specifically to maximize copying degree in these scenarios. Baselines like Context-DPO were trained for contextual faithfulness more generally, not to maximize lexical overlap. While the comparison is not circular (all methods aim at contextual faithfulness), the 12–24% gap is less surprising given this asymmetry. The paper also selectively frames the ConFiQA-MR result: for Llama-3-8B, Context-DPO achieves 88.4 vs. CopyPasteLLM's 80.9, yet the paper's discussion focuses on Mistral-7B where the gap favors CopyPasteLLM.

### Minor

- **Answer-stamping confound in DPO training.** Section 3.2 describes appending the gold answer to the top Copy-Paste candidate (chosen) and wrong answers to other candidates (rejected). This means the chosen and rejected sequences differ not only in generated text but also in a post-hoc appended suffix. The DPO model could learn to exploit this structural signal rather than the faithfulness properties of the generated text. An ablation without answer stamping is needed to validate the learning mechanism.

- **The core causal assumption underlying the pipeline is supported only by correlation.** The paper motivates the entire approach with an observed inverse correlation between copying degree and hallucination density (Section 2.2, Figure 1). While the subsequent experiments validate the method empirically, the correlational evidence alone (without error bars, quantitative coefficients, or a controlled causal experiment) does not establish that *forcing* higher copying *causes* reduced hallucination. The paper would be stronger with a controlled experiment that artificially varies copying degree (e.g., through constrained decoding) and measures the effect on hallucination rates.

- **Context-Parameter Copying Capturing has methodological confounds.** Token classification depends on span overlap with the context; tokens appearing in both the context and parametric knowledge are classified as contextual, potentially inflating contextual knowledge counts. The "logits power" metric is referenced but not formally defined in the main text. The UMAP analysis (Figure 4) is interpreted through visual inspection of 2D projections without quantitative separation measures (e.g., centroid distance, silhouette score).

### Trivial

- The composite copy score threshold for CP-Refine's iterative refinement is referenced but not specified (Section 3.1).
- The title of the GPT-4o comparison (47.5%) referenced in the main text for FaithEval should ideally include the prompting details rather than deferring entirely to the appendix.

## Nice-to-Haves

- An ablation study removing the answer-stamping mechanism to isolate the effect of DPO on the generated text vs. structural cues.
- Quantitative separation measures (silhouette score, centroid distance) to support the visual UMAP interpretation.
- Controlled experiment that varies copying degree (e.g., through constrained decoding) to directly test the causal link.

## Removed Points

These points were flagged for removal; treat them with caution if reading the raw reviews:

- **"365 training samples claim is misleading."** The paper compares DPO training data size (365 query-context pairs) to baselines' training data size (18,000 for Context-DPO), which is an apples-to-apples comparison for the fine-tuning stage. The total pipeline cost is higher, but the claim is about *data efficiency* of the final training stage, not total compute.

- **"GPT-4o comparison is uninformative/incomplete."** The paper cites Appendix Table 6 for these details. The appendix was stripped by the parser; it exists in the original submission.

- **"No evaluation of overriding wrong context."** This asks for a different capability (context verification) beyond the paper's stated scope (RAG faithfulness). The paper explicitly tests counterfactual scenarios where the model should trust the provided context over parametric knowledge.

- **"No analysis of training sample composition/dataset overlap."** These details are in the stripped appendix (Appendix Table 4). Per policy, missing appendix content is a parser artifact.

- **Formatting/typo criticisms.** These are parser artifacts from PDF extraction, not author errors.

- **Various speculation-based criticisms** (e.g., "maybe the model learns X instead of Y" without specific evidence from the paper). These were removed per the filtering discipline.

## Novel Insights

None beyond the paper's own contributions. The mechanistic finding that CopyPasteLLM works by recalibrating parametric knowledge confidence rather than enhancing contextual representations is the most interesting novel insight, but it is presented clearly in the paper itself.

## Suggestions

1. **Define Twist and Causal hallucination modes in the main text.** Clarify what they mean, how the Elo tournament works, and what the score range implies so readers can interpret Table 2 without the appendix.
2. **Add an ablation removing answer stamping** to verify that the model learns from generated text content rather than the structural suffix difference.
3. **Address the ConFiQA-MR Llama-3-8B result explicitly.** Discuss why CopyPasteLLM underperforms Context-DPO here while outperforming on other metrics.
4. **Add quantitative separation metrics** (silhouette score, centroid distance, KL divergence) to support the visual UMAP interpretation in Figure 4.
5. **Report a quantitative correlation coefficient** (with significance) for the Figure 1 observation, and ideally include a controlled experiment that varies copying degree independently to test causality.

## Score and Decision

**Calibration anchors (all retrieved, across all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 5kMwiMnUip (Jailbreaking) | 1.40 | R1 strong-reject | Much weaker; not a serious technical paper |
| 8QTpYC4smR (Systematic Review) | 1.00 | R1 strong-reject | Not a technical contribution |
| gwZ90hFSL2 (Cross-lingual Robotics) | 1.00 | R1 strong-reject | Not comparable; low quality |
| nSDOkm0SKo (Financial Analysis) | 1.00 | R1 strong-reject | Not comparable |
| RuY1r1PDdQ (FAITHQA benchmark) | 3.00 | R1 reject | Benchmark paper; less novel methodology |
| a2rSx6t4EV (EDU-RAG) | 2.33 | R1 reject | Simple benchmark, less rigorous |
| fMaEbeJGpp (Multimodal RAG) | 2.50 | R1 reject | System paper, limited novelty |
| 56mg1JFd3n (Writing in Margins) | 3.00/6.00* | R1 reject | Inference method; mixed reviews |
| JnWJbrnaUE (CRAG) | 3.75 | R1 border-rej | RAG pipeline; limited technical novelty |
| hPk92D2GJV (BALCONI) | 5.25 | R1 border-rej | Most similar in topic; weaker empirical results, rejected due to one 3 |
| SR8LFpmVun (UncertaintyRAG) | 4.75 | R1 border-rej | Retrieval method; less novel paradigm |
| HUzDU7u5B4 (RLFH) | 4.33 | R1 border-rej | Hallucination mitigation; smaller scope |
| asGQQc7gNo (Factuality v. Faithfulness) | 6.67 | R1 borderline | Analysis paper; no new method. Current paper has stronger contribution (working method) |
| Jjr2Odj8DJ (Sufficient Context) | 6.25 | R1 borderline | Analysis of RAG failures; less novel methodologically |
| K2jOacHUlO (Situated Faithfulness) | 7.25 | R1 accept | Comprehensive; multiple methods + dataset. Current paper comparable in scope |
| ztzZDzgfrh (ReDeEP) | 7.33 | R1 accept | Strong mechanistic analysis for hallucination detection |
| Iyrtb9EJBp (Trustworthiness RAG) | 8.00 | R1 strong-accept | All 8s; more polished experimental design |
| GGlpykXDCa (MMQA) | 8.00 | R1 strong-accept | Different topic (tables) |
| WbWtOYIzIK (Knowledge Card) | 8.00 | R1 strong-accept | Different paradigm |

*The "Writing in the Margins" paper had avg 3.0 in the (1.5,3.5) filter but the abstract shows scores 10,3,5,6 = avg 6. The filter's averaging may be misleading; I treat this as a borderline paper.

**Round 1 bracket:** 5.5–7.5 (the paper is clearly above the 3.5–5.5 reject/borderline band and below the 7.5+ strong accept band).

**Final score:** 7.0. The paper proposes a novel, well-motivated paradigm with strong empirical support and interesting mechanistic analysis. The data efficiency claim is notable. However, the undefined hallucination metrics in the main text, the answer-stamping confound, and the evaluation framing that partially favors the method prevent this from being a clear strong accept. The paper sits comfortably at the accept level, between the analysis-only paper at 6.67 and the most comprehensive studies at 7.25–7.33.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>