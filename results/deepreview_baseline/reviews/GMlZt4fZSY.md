## Summary
This paper investigates how to efficiently endow sub-billion-parameter language models with strong reasoning capabilities through careful data curation. It proposes a multi-stage pipeline: (1) a benchmark-free, influence-based data mixture weighting for pre-training that leverages cross-domain self-influence scores, (2) a data-model co-evolution strategy for mid-training that iteratively prunes negative-influence samples, and (3) standard post-training. Trained on only ~4.2T tokens (11.7% of Qwen3’s 36T), the resulting MobileLLM-R1-950M matches or exceeds Qwen3-0.6B on multiple reasoning benchmarks, while substantially outperforming previous fully open-source models of similar or larger size.

## Strengths
- **Strong practical contribution.** The paper provides a complete open-source recipe (data, code, model weights) for training sub-billion reasoning models that achieve state-of-the-art results among fully open-source models. This fills an important gap for on-device deployment.
- **Clear and well-motivated problem.** The focus on data efficiency for small models is timely and tackles a real need. The claim that quality and curation matter more than raw token count for small capacities is convincingly supported by the experimental results.
- **Thoughtful empirical methodology.** The leave-one-out analysis (Figure 3) and the influence-based mixing (Sections 2.1.2, 2.2) are well-designed diagnostic tools. The mid-training data compression with convergence to zero influence (Figure 5) is a novel and insightful observation.
- **Comprehensive ablation studies.** The post-training ablation (Table 1) and the controlled reasoning SFT comparison (Table 2) cleanly isolate the contributions of different components, strengthening confidence in the proposed pipeline.

## Weaknesses
### Fatal
None.

### Major
- **The “benchmark-free” claim is overstated.** The method relies on carefully curated *capability-probing datasets* that are themselves derived from the training corpora via hierarchical rejection sampling. While not standard public benchmarks, these are not automatically generated and still encode human priors about what “reasoning” looks like. The novelty of this aspect is more incremental than suggested.
- **The contribution of the influence-based pre-training mixture (Datamix) to final model performance is not directly validated.** Figure 4 shows perplexity improvements on probing datasets, but there is no ablation that ties Datamix to the final downstream benchmark results of MobileLLM-R1. Given that the full pipeline is complex, it is unclear how much of the gain comes from this mixing versus other components (e.g., high-quality data selection, mid-training compression, post-training). A final-model comparison with and without Datamix would significantly strengthen the paper.
- **The leave-one-out analysis (Figure 3) uses equal sampling probability across datasets regardless of their size.** This is an unconventional normalization that may not reflect realistic training dynamics. The interpretation that FineWeb-Edu acts as a “glue” relies heavily on this choice; under standard scaling by dataset size, the relative importance of smaller datasets might change. The results therefore need careful contextualization.

### Minor
- **Figure 8 and 9 have garbled numerical labels** (likely a PDF parsing artifact), making it impossible to read exact values from the provided content. The main text refers to tables in the appendix for full comparisons, but the figures alone do not clearly convey the quantitative advantage.
- The paper uses “M, S, C” abbreviations for datasets in Table 1 without immediate expansion in the caption (though explained in a footnote-like note). This slows reading.
- The phrase “pre-training with 4.2T tokens on the dataset resampled from these ~2 T tokens” is ambiguous: it means training for ~2 epochs on ~2T unique tokens. Clarifying the effective epoch count would help.

### Trivial
- The claim that the work “challenges the conventional belief that small reasoning models require massive data” is somewhat overblown; previous small models (e.g., SmolLM, OLMo) already used modest data (2-4T). The novelty lies more in the *systematic* curation and the specific recipes.
- Some figures (e.g., Figure 6) have a table embedded that duplicates the plot data; this is redundant.

## Nice-to-Haves
- An ablation that directly compares final model performance (e.g., MATH, HumanEval) with and without the Datamix pre-training strategy.
- More extensive analysis of the mid-training convergence: at what point does the influence distribution collapse? The paper states two stages suffice, but a plot of retained sample fraction per stage would be informative.
- Evaluation on additional reasoning benchmarks (e.g., BBH, ARC, MMLU-Pro) to broaden the assessment.

## Novel Insights
The most interesting insight is the observed *compression* of influence scores during mid-training: as the model becomes more capable, most samples’ influence converges toward zero, providing a natural stopping criterion for data augmentation. This framing of mid-training as a “denoising” process that sharpens the signal from target capabilities is conceptually clean and practically useful. Additionally, the finding that FineWeb-Edu benefits all three reasoning domains (code, math, knowledge) suggests that broad web data acts as a critical substrate that connects specialized reasoning data—a result that is consistent with the idea of “glue” data but is empirically demonstrated here for small models. The negative transfer of code reasoning to MMLU (Table 1) is a concrete illustration of capacity trade-offs in compact models.

## Suggestions
- Rename “benchmark-free” to something more precise (e.g., “evaluation-set-free” or “without access to standard test sets”) to avoid overclaiming.
- Include an ablation comparing final model quality with and without the Datamix pre-training mixture to directly quantify its impact.
- Clarify the sampling normalization used in the leave-one-out experiments and discuss how the results might change under standard dataset-ratio sampling.

## Score and Decision
**Score:** 7

**Decision:** Accept

The paper makes a solid empirical contribution with clear practical value, strong reproducibility, and insightful analysis. The main weaknesses (overstated “benchmark-free” claim and lack of direct ablation for the pre-training mixture on final performance) hold it back from a higher score, but do not invalidate its core findings.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>