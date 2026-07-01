## Summary

This paper introduces MGA (Massive Genre-Audience Reformulation), a two-stage framework that augments pretraining corpora by adaptively generating diverse genre-audience pairs from source documents and then reformulating the text accordingly using lightweight fine-tuned tool SLMs. The authors produce the 770B-token MGACorpus and demonstrate via extensive experiments (134M–13B parameters, up to 800B tokens) that training on MGA-augmented data consistently outperforms data repetition and upsampling, shows widening gains with model scale and data budget, and complements other synthetic data strategies. The paper also provides analysis of synthetic data collapse and the nuanced role of validation loss, arguing that higher loss on original data need not indicate collapse but may reflect a beneficial shift in learning strategy.

## Strengths

- **Timely and impactful problem.** Data scarcity and repetition-induced degradation are critical bottlenecks for LLM scaling, and this paper offers a principled, reproducible solution that directly targets this challenge.
- **Thorough and convincing experiments.** The scaling experiments across multiple model sizes (134M–13B), data budgets, and comparison with repetition/upsampling/Nemotron-Syn are comprehensive and consistently show MGA’s advantage. The widening performance gap with model scale (superior N-scaling) is particularly compelling.
- **Principled framework design.** The two-stage pipeline (maximize variance via adaptive GA-pair generation, then enforce invariance via filtered SFT) is well-motivated. The “Limited Consistency” principle is empirically validated through the SLM-Base vs. Strict vs. Relaxed ablation.
- **Insightful analysis of validation loss and model collapse.** Section 4.3.3 provides a nuanced, fine-grained loss pattern analysis demonstrating that increased validation loss on real data does not necessarily signify collapse, but may reflect different learning strategies; this is a valuable caution for the community.
- **Strong reproducibility commitment.** The authors promise to release the full MGACorpus, prompts, tool-model finetuning data, and cleaning scripts, which is essential for community adoption and verification.

## Weaknesses

### Fatal

None.

### Major

1. **Computational cost of data generation is not discussed.** The paper does not report the GPU-hours or total cost required to generate the 770B-token MGACorpus using the 3.3B MoE tool SLM. Without this, it is difficult for practitioners to assess the practical trade-off between the performance gains and the upfront generation cost.

2. **Evidence for “shifted learning strategy” is indirect.** The claim in Section 4.3.3 that the model “may prioritize learning generalizable patterns from context over memorizing specific sequence dependencies” is based solely on positional loss patterns. Direct evidence (e.g., probing tasks, representation similarity analysis, or counterfactual examples) would substantially strengthen this conclusion.

3. **The “Limited Consistency” principle is operationalized as prompt engineering only.** While the empirical comparison (SLM-Base vs. Strict vs. Relaxed) is useful, the principle itself is not formalized into a quantitative objective or measure, limiting its generalizability beyond the specific prompts used here.

### Minor

1. **The comparison with “collect more hq data” in Figure 3 may not be fully controlled.** The additional 195B of real FineWeb-Edu data might be of lower quality at the margin than the original 50B seed. MGA’s advantage over this baseline is impressive, but the experiment does not isolate whether the improvement comes from higher average quality or from the reformulation mechanism itself.

2. **The role of data quantity vs. diversity is not fully disentangled.** In the main experiments (Table 2), MGA-Expansion uses the same total token count as the baseline (600B for 134M), but replaces a portion of the training data with reformulated versions. The gains could partly stem from the introduction of new tokens rather than stylistic diversity per se. The SLM-Base vs. SLM-Strict comparison partially addresses this, but a controlled experiment where total unique tokens are held constant would be cleaner.

3. **Some terminology is imprecise.** For example, “one-pass-for-many strategy” (Section 3.2) is used without formal definition, and “SLM-Relaxed makes only 2× tokens” (Section 4.3.2) conflates the expansion factor with the prompt relaxation.

## Nice-to-Haves

- Provide an estimate of the GPU-hours required for generating the MGACorpus, broken down by stage (GA-pair generation, reformulation, cleaning).
- Include probing experiments (e.g., factual recall vs. pattern completion tasks) to directly test whether MGA-trained models rely less on memorization.
- Investigate whether the reformulated data introduces systematic factual errors or domain-specific biases, and report a human-evaluation sample.

## Novel Insights

Beyond the paper’s own contributions, a noteworthy insight is that **validation loss on the original data distribution can be a misleading metric for synthetic data quality**. The paper shows that model performance on downstream benchmarks can improve substantially even while in-distribution perplexity degrades, and that fine-grained positional loss analysis can distinguish between genuine collapse and a beneficial shift toward more context-general learning. This has important implications for how the community evaluates synthetic pretraining data going forward.

## Suggestions

1. Include a cost-benefit table or paragraph in the main text (or an appendix that will be visible) showing the generation cost in GPU-hours or token-equivalent compute, so that readers can weigh the overhead against the performance gains.
2. Conduct a small probe-based study (e.g., using masked token prediction or one-shot factual recall) to provide more direct evidence for the claimed shift from memorization to generalizable learning.
3. In the scaling experiments, add a control where the same total number of unique tokens is used (e.g., upsample real data to match the token count of MGA but without synthetic diversity) to more clearly separate the effects of volume and diversity.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>