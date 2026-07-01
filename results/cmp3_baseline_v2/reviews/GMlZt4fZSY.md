## Summary

This paper introduces MobileLLM-R1, a series of sub-billion-parameter reasoning models that challenge the assumption that strong reasoning capabilities require massive training datasets. The authors propose a data-centric framework with benchmark-free, self-evolving data optimization for pre-training data curation and a data-model co-evolution strategy for mid-training, demonstrating that with only 4.2T tokens (11.7% of Qwen3's 36T), their 950M model matches or surpasses Qwen3-0.6B across multiple reasoning benchmarks. The work provides a fully open-source recipe including datasets, models, and training code.

## Strengths

- **Strong empirical results with clear practical significance**: The paper demonstrates that MobileLLM-R1-950M achieves an AIME score of 15.5 compared to 0.6 for OLMo-2-1.48B and 0.3 for SmolLM-2-1.7B, while using only 4.2T tokens versus Qwen3's 36T. These results are compelling and directly challenge prevailing assumptions about data scaling requirements for reasoning.

- **Principled and well-motivated methodology**: The leave-one-out analysis (Figure 3) and influence-based data mixing (Section 2.2) provide a systematic, theoretically grounded approach to data curation that goes beyond heuristic or ad-hoc methods. The cross-capability self-influence framework is a novel contribution that enables benchmark-free optimization.

- **Comprehensive ablation studies**: The paper includes thorough ablations on post-training stages (Table 1), controlled comparisons with baselines under identical reasoning SFT (Table 2), and mid-training data compression analysis (Figure 6). These experiments effectively isolate the contribution of each component.

- **Full transparency and reproducibility commitment**: The authors commit to releasing all trained models, code, and complete dataset specifications, which is valuable for the community and aligns with ICLR's reproducibility standards.

## Weaknesses

### Fatal
None.

### Major

- **Insufficient evidence for the "self-evolving" claim in pre-training**: The influence-based data mixing (Section 2.2) is presented as "self-evolving" and "benchmark-free," but the method requires training separate domain-specialized models to convergence on full training sets of Code, Math, and Knowledge domains. This is computationally expensive and the paper does not provide a clear comparison of the computational cost of this approach versus simpler alternatives (e.g., uniform sampling, heuristic weighting). The claim that this is "self-evolving" is overstated when it requires pre-trained domain experts.

- **Limited novelty relative to existing influence-based methods**: The influence score computation (Eq. 2) and the AutoMixer framework are directly adopted from prior work (Chang et al., 2025). The extension to cross-capability influence is incremental, and the paper does not clearly articulate what new technical challenges were overcome beyond applying existing methods to a new setting. The "data-model co-evolution" in mid-training (Section 3) is essentially iterative influence-based filtering, which is a straightforward application of existing ideas.

- **Missing critical details about the mid-training compression**: The paper states that two stages of mid-training suffice (100B tokens each), but does not provide evidence that this is optimal or that the process converges reliably. Figure 5 shows influence scores concentrating near zero, but the paper does not quantify what fraction of data is retained after each stage, nor does it show that further stages would not improve performance. The claim that "the dataset's information has been largely exhausted" is not rigorously supported.

- **Potential confounding in the final comparison**: The final results (Figures 8 and 9) compare MobileLLM-R1 against baselines that may have been trained with different post-training procedures. While Table 2 provides a controlled comparison under identical reasoning SFT, the final model comparisons mix the effects of pre-training, mid-training, and post-training. The paper would benefit from a clearer decomposition of which stage contributes most to the gains.

### Minor

- **The paper's title and framing emphasize "exploring the limits" but the work is primarily a recipe paper**: The contribution is a specific training recipe that works well, but the paper does not systematically explore the limits of what is possible (e.g., how low can tokens go? What is the minimal data required?). The title sets an expectation that is not fully met.

- **The "benchmark-free" claim is somewhat misleading**: While the method does not use benchmark test sets during optimization, it does use capability-probing datasets that are curated using the Ask-LLM paradigm with prompts that explicitly ask about reasoning relevance. These probing datasets are constructed with domain-specific prompts emphasizing code, math, or general knowledge, which implicitly encodes benchmark-like objectives.

- **The paper does not discuss failure cases or limitations of the approach**: For example, are there reasoning tasks where MobileLLM-R1 performs poorly despite the curated data? How sensitive is the method to the choice of probing datasets? Acknowledging limitations would strengthen the paper.

### Trivial
None.

## Nice-to-Haves

- A comparison of the computational cost (FLOPs or GPU-hours) of the influence-based data curation versus simpler baselines would help practitioners assess the practical trade-offs.
- An analysis of how the data mixture ratios change across training phases would provide insight into the dynamics of the method.
- A discussion of whether the approach generalizes to other model architectures or scales beyond 1B parameters would increase the impact.

## Novel Insights

The paper's most interesting finding is that code data (StarCoder) benefits math performance more than math data (OpenWebMath) benefits code performance, which reverses the commonly held assumption that mathematical data disproportionately contributes to coding ability. This cross-domain transfer asymmetry is a genuinely novel observation that could inform future data curation strategies. Additionally, the observation that FineWeb-Edu acts as a "glue" connecting heterogeneous domains, with its removal causing the largest cross-domain degradation, provides empirical evidence for the importance of diverse web data even in specialized reasoning models.

## Suggestions

- Provide a clearer decomposition of the contribution of each training stage (pre-training data mixing, mid-training compression, post-training) to the final performance gains, perhaps through a cumulative ablation study.
- Include an analysis of the computational cost of the influence-based methods and compare it to simpler alternatives to help readers assess the practical utility.
- Discuss the limitations of the approach more explicitly, including potential failure cases and sensitivity to probing dataset construction.

## Score and Decision

The paper presents a well-executed empirical study with strong results that challenge important assumptions in the field. The methodology is principled and the ablation studies are thorough. However, the novelty is somewhat limited by the reliance on existing influence-based frameworks, and the "self-evolving" and "benchmark-free" claims are overstated. The practical significance of the results is high, and the commitment to full reproducibility is commendable. The paper is a solid contribution that advances our understanding of data-efficient training for small reasoning models, but it does not introduce fundamentally new techniques or insights beyond what is already known in the influence-based data curation literature.

MY FINAL SCORE: 6.0score</score>
MY FINAL DECISION: Accept</decision>