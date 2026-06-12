## Summary

This paper develops an automated pipeline for extracting "persona vectors"—linear directions in a language model's activation space corresponding to personality traits (e.g., evil, sycophancy, hallucination)—from natural-language descriptions alone. The authors demonstrate that these vectors enable monitoring of persona shifts during deployment and finetuning, introduce a novel "preventative steering" method that mitigates finetuning-induced drift by steering toward the undesired direction during training, and show that pre-finetuning projections of training data onto persona vectors can predict and flag problematic datasets and samples before any training occurs.

## Strengths

- **Comprehensive multi-application framework from a single extraction method.** The paper demonstrates four distinct applications—deployment monitoring, inference-time mitigation, preventative steering during training, and pre-training data screening—all from one automated extraction pipeline. This breadth is impressive and each application is supported by strong empirical correlations (e.g., r = 0.76–0.97 in Figure 4 for finetuning shift vs. trait expression).

- **Novel preventative steering method with practical advantages.** The counterintuitive idea of steering *toward* an undesired direction during finetuning to prevent drift is genuinely novel. The fact-acquisition case study (Section 5.2) convincingly demonstrates that preventative steering preserves both newly learned facts and general capabilities (MMLU), while inference-time steering degrades both—a compelling practical advantage.

- **Strong cross-model validation.** Experiments are conducted on two architecturally distinct models (Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct), and the key results—finetuning shift correlations (Figure 4) and data projection correlations (Figure 7)—replicate consistently, increasing confidence that the findings are not model-specific artifacts.

- **Practical data screening application with fine-grained resolution.** The ability to detect problematic samples at the individual level (Figure 8), including from "EM-like" datasets where traits are not explicitly present in the data, is practically valuable. The complementary strengths with LLM-based filtering (Appendix M) suggest a realistic deployment strategy.

- **Automated and accessible pipeline.** Requiring only a natural-language trait description makes the approach broadly applicable without expert intervention for each new trait of interest.

## Weaknesses

### Fatal

None.

### Major

- **Heavy reliance on LLM-based trait evaluation as the primary metric.** The trait expression score (0–100 from GPT-4.1-mini) underpins nearly every quantitative claim in the paper. While the authors note validation against human evaluators (Appendix D), the sensitivity of results to the choice of judge model, prompt design, and scoring granularity is not systematically explored. A single flawed evaluation criterion could inflate or deflate multiple correlations simultaneously.

- **Limited model scale diversity.** All experiments use ~8B parameter models. It is unclear whether persona vectors remain linear and interpretable at much larger scales, or whether the strength of correlations (e.g., the remarkably high r values in Figure 7) hold for frontier-scale models where representations may be more distributed or polysemantic.

- **Thin theoretical grounding for preventative steering.** The intuition that adding the persona vector during training "counteracts the finetuning objective's tendency to push the model along that direction" is plausible but underspecified. Why does external perturbation during training prevent internal representation learning of the same direction? A mechanistic account—perhaps connecting to gradient dynamics or loss landscape geometry—would substantially strengthen the contribution.

### Minor

- **Inter-trait correlation is noted but underexplored.** Footnote 6 observes that negative traits and humor shift together, and opposite to optimism, suggesting persona vectors are not independent. This raises questions about whether the vectors capture a general "alignment direction" rather than trait-specific factors, which would complicate the data screening application (a sample flagged for "evil" might really be flagged for general negativity).

- **The "EM-like" datasets are somewhat contrived.** While inspired by Betley et al. (2025), the constructed datasets (flawed math, insecure code, etc.) are synthetic. The brief mention of real-world dataset results in Appendix N is promising but cannot be fully evaluated from the main text.

- **Preventative steering effectiveness varies by trait and dataset.** Single-layer preventative steering does not fully suppress trait acquisition for intentionally trait-eliciting datasets (acknowledged by the authors), requiring multi-layer steering (Appendix L.3). This limits the plug-and-play simplicity of the approach.

### Trivial

None.

## Nice-to-Haves

- A comparison with mechanistic interpretability approaches (e.g., sparse autoencoders) for extracting trait-relevant features, to contextualize the linear assumption.
- Analysis of whether persona vectors transfer across model families or scales, which would broaden the practical utility.
- Ablation on the number of contrastive prompt pairs and evaluation questions needed for reliable vector extraction.

## Novel Insights

The paper's most genuinely novel observation is that steering *toward* an undesirable direction during finetuning (preventative steering) more effectively prevents persona drift than steering *against* it at inference time, while better preserving model capabilities. This is counterintuitive—one would naively expect that amplifying the bad direction during training would make things worse. The practical demonstration that this works for fact acquisition while preserving MMLU accuracy (Section 5.2) is a strong result. Additionally, the finding that training data projections onto persona vectors can predict post-finetuning trait expression *before any training occurs* (with r > 0.9 for several trait-model combinations) is a noteworthy empirical discovery with practical implications for data curation pipelines.

## Suggestions

- Investigate the mechanism behind preventative steering more deeply—consider measuring gradients along persona vectors during finetuning with and without the intervention, to build a mechanistic understanding.
- Add at least one larger-scale model (e.g., 70B) to the main experiments to test whether the linear persona vector framework scales.
- Provide a sensitivity analysis of the LLM judge evaluation: how do results change under different judge models, different score thresholds, or different evaluation prompt framings?

## Score and Decision

The paper presents a well-executed empirical study with multiple practically relevant contributions. The automated pipeline, preventative steering method, and data screening application each address real needs in the alignment and safety community. The experimental design is thorough with cross-model replication and strong correlations. The main weaknesses—reliance on LLM evaluation, limited model scale, and insufficient theoretical grounding for preventative steering—are significant but do not invalidate the core contributions.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept