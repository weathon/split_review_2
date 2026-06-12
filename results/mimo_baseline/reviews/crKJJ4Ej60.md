## Summary

This paper proposes Copy-Paste, a generation paradigm for RAG systems that directly embeds contextual fragments into responses to reduce faithfulness hallucinations. The authors observe an inverse correlation between response copying degree and hallucination density, then develop three Copy-Paste-Prompting methods (CP-Order, CP-Link, CP-Refine) and train CopyPasteLLM via DPO on automatically constructed high-copying preference data. CopyPasteLLM achieves 12.2%-24.5% accuracy improvements on FaithEval's counterfactual subset over the best baseline while using only 365 training samples (50× less data), and a novel Context-Parameter Copying Capturing algorithm reveals the mechanism operates by suppressing parametric knowledge reliance rather than enhancing contextual representations.

## Strengths

- **Novel and clean core idea.** The Copy-Paste paradigm is intuitively compelling: instead of having the model reinterpret retrieved content (risking paraphrasing hallucinations), directly copying contextual fragments both reduces hallucination risk and provides inherent attribution. The three prompting methods form a well-designed spectrum from hard extractive constraints (CP-Order) to soft iterative refinement (CP-Refine), enabling diverse preference data construction.

- **Remarkable empirical results with extreme data efficiency.** CopyPasteLLM trained on only 365 samples outperforms Context-DPO (18,000 samples), Canoe (10,000), and ParamMute (32,580) by 12.2%-24.5% on FaithEval's challenging counterfactual subset, reaching 92.8% accuracy on Llama-3-8B—surpassing GPT-4o's reported 47.5%. Performance generalizes across three backbone models (Mistral-7B, Llama-3-8B, Llama-3.1-8B) and maintains strong results on non-counterfactual benchmarks (Table 3), with dramatic improvements on ConFiQA's multi-conflict subsets (e.g., +20.67% on Mistral-7B-v0.2 MR).

- **Insightful mechanistic analysis.** The Context-Parameter Copying Capturing algorithm extends Knowledge Token Capturing to full CoT trajectories, enabling token-level, position-aware analysis of contextual vs. parametric reliance. The UMAP visualizations (Figure 4) reveal a striking pattern: CopyPasteLLM preserves contextual knowledge representations similar to the base model while substantially recalibrating parametric knowledge distributions, suggesting the mechanism operates through selective parametric suppression rather than contextual enhancement—a genuinely novel and non-obvious finding.

## Weaknesses

### Fatal

None.

### Major

- **Causality of the motivating observation remains partially unresolved.** The inverse correlation between copying degree and hallucination density (Section 2.2, Figure 1) is observational—when context clearly contains the answer, models may naturally both copy more and hallucinate less, without a causal link from copying to reduced hallucination. The DPO-trained CopyPasteLLM's strong performance on counterfactual contexts (where the context deliberately contradicts parametric knowledge) provides indirect causal evidence, but a more controlled ablation—e.g., training on high-copying data that is deliberately unfaithful—would strengthen the causal claim that copying behavior drives faithfulness rather than merely correlating with it.

- **Evaluation asymmetry with Context-DPO.** Context-DPO is trained on 18,000 samples from ConFiQA, which constitutes "seen" data for ConFiQA evaluation (marked with T in Table 1), while CopyPasteLLM uses only 365 samples from elsewhere. On FaithEval the comparison is fair (unseen for both), but on ConFiQA the comparison conflates data efficiency with data distribution mismatch. The paper would benefit from Context-DPO results on FaithEval or a clearer framing that ConFiQA comparisons only demonstrate generalization rather than direct superiority on that benchmark.

### Minor

- **Only 7-8B models are fine-tuned.** While prompting results span 7B to 671B models (Table 2), CopyPasteLLM is only trained and evaluated on 7-8B parameter models. Given that larger models already show strong copying behavior (DeepSeek-V3 CP-Order achieves 97.79% Twist faithfulness), it would be valuable to know whether the DPO training provides additional benefits at scale or whether prompting alone is sufficient for larger models.

- **Query relevance is underexplored in quantitative results.** The paper mentions query relevance as a key trade-off dimension (Section 2.1) and shows qualitative comparisons in Appendix Figure 6, but Table 2 omits explicit query relevance scores. Given that CP-Order's strict extraction could produce off-topic answers, systematic relevance metrics across all methods would strengthen the evaluation.

- **CP-Refine's iterative loop adds inference overhead.** The writer-reviewer loop introduces additional LLM calls per sample. While the paper discusses quality trade-offs, the computational cost relative to single-pass baselines is not quantified, making it hard to assess practical deployment costs.

## Nice-to-Haves

- A human evaluation comparing CopyPasteLLM responses against baselines on faithfulness, informativeness, and fluency would complement the automatic metrics.
- Analysis of failure cases—queries where high-copying produces overly literal or unhelpful answers—would provide a more complete picture of the approach's boundaries.
- Evaluation on domain-specific production RAG pipelines (beyond benchmark datasets) would demonstrate practical applicability.

## Novel Insights

The paper's most novel insight is the mechanistic finding that CopyPasteLLM achieves enhanced contextual faithfulness not by strengthening contextual knowledge representations, but by selectively suppressing the model's internal confidence in parametric knowledge. This is evidenced by the UMAP analysis showing that contextual knowledge distributions remain nearly co-distributed between base and CopyPasteLLM models, while parametric knowledge distributions diverge substantially. This finding—that faithfulness can be improved by "quieting" competing internal knowledge rather than "amplifying" external knowledge processing—has implications beyond this specific method and could inform future work on knowledge conflict resolution in LLMs.

## Suggestions

- Add a controlled experiment where high-copying data is constructed to be unfaithful (e.g., copying from an irrelevant context), to disentangle the effect of copying behavior from the effect of faithfulness in the training signal.
- Report query relevance scores (e.g., embedding similarity to the query) alongside faithfulness metrics in Table 2 to verify the faithfulness-relevance trade-off is well-managed.
- Include a brief cost analysis comparing the inference overhead of CP-Refine's iterative loop against the single-pass baselines.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>