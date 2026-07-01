## Summary
The paper presents a data-centric framework for training sub-billion parameter language models with strong reasoning capabilities. It introduces a benchmark-free influence-based data curation method for pre-training data mixture optimization and a data-model co-evolution strategy for mid-training knowledge compression. Using only 4.2T tokens (11.7% of Qwen3’s 36T), the resulting MobileLLM-R1 models match or surpass Qwen3-0.6B on multiple reasoning benchmarks, significantly outperforming other fully open-source small models. The authors release all models, data, and code.

## Strengths
- **Important and timely problem**: enabling strong reasoning in small models is critical for on-device deployment, and the paper directly addresses this with a practical, data-centric approach.
- **Principled influence-based data curation**: The benchmark-free, self-evolving data optimization using influence scores (extending AutoMixer) is a novel and well-motivated technique for data mixture tuning, especially for small models where data quality is paramount.
- **Extensive empirical validation**: The paper includes a leave-one-out analysis to identify dataset contributions, comparisons of mixture strategies, post-training stage ablations, and a fair comparison where all models are fine-tuned on the same reasoning SFT data (Table 2). These experiments rigorously support the claims.
- **Strong results**: MobileLLM-R1-950M achieves state-of-the-art among fully open-source sub-1B models, matching or surpassing Qwen3-0.6B on MATH, AIME’24, and LiveCodeBench while using far fewer training tokens.
- **Full reproducibility**: The authors commit to releasing all models, datasets, and code, and the training pipeline is described in sufficient detail.

## Weaknesses
### Fatal
None.

### Major
- **Computational cost of influence scoring is not quantified**: The method requires training separate domain-specialized models to convergence and computing influence at multiple checkpoints. The paper claims the approach is scalable but provides no analysis of the computational overhead (e.g., GPU hours) relative to standard training. This is a significant practical concern.
- **Leave-one-out analysis is performed at a small scale**: The LOO experiments (Figure 3) appear to be run for only 500k steps, far less than the full 4.2T token budget. The paper does not specify the total token count used in these experiments or discuss whether the conclusions about dataset importance (e.g., FineWeb-Edu being the most beneficial) generalize to the full training scale.
- **Comparison with simpler mixture baselines is missing**: The influence-based mixture (Figure 4) is only compared against uniform sampling. To demonstrate the added value of the influence scores, the paper should also compare against heuristic mixtures (e.g., upweighting FineWeb-Edu, equalizing curriculum-stage mixtures) or other simple filtering strategies.
- **“Benchmark-free” terminology is slightly misleading**: The method uses capability-probing datasets derived from the training data itself, which is a reasonable choice, but it is not entirely free of reference distributions. The term could be clarified.

### Minor
- **The fair comparison of reasoning SFT (Table 2) uses baseline instruct models** that may have already been fine-tuned on instruction data that overlaps with the reasoning corpus. This could give them an advantage, while MobileLLM-R1* is only at the Tulu3-SFT stage. The paper does not discuss this potential confound.
- **The post-training ablation (Table 1) shows non-monotonic behavior**: Adding code data to math+science lowers MATH (60.0 → 57.8). This trade-off is acknowledged but not deeply analyzed.
- **The influence computation relies heavily on the AutoMixer framework**, which is only referenced. While the paper extends it to multiple domains and iterative mid-training, the core approximation technique is not novel.

### Trivial
- Some figures (e.g., Figure 8, 9) have minor formatting issues (overlapping labels, truncated model names), likely due to PDF parsing.

## Nice-to-Haves
- Include a quantitative comparison of the total GPU hours required for the influence computation pipeline versus standard training.
- Ablate the number of influence checkpoints (T) and the blending factors (α) to show sensitivity.
- Compare the influence-based mixture against a simple baseline that filters training data using the FineWeb-Edu classifier alone.

## Novel Insights
The paper provides a concrete demonstration that reasoning capabilities in small models can be unlocked with far less data than previously assumed, provided the data is carefully curated and adapted to the model’s capacity. The key insight is that a “benchmark-free” influence-based data mixture optimization, combined with an iterative data-model co-evolution during mid-training, can effectively compress the information needed for reasoning into a compact model. The observation that influence scores converge to zero as training progresses (Figure 5) suggests a principled termination criterion for data selection, which is novel and practically useful.

## Suggestions
- Clarify the token budget of the leave-one-out experiments and discuss whether the conclusions hold at full scale.
- Include a quantitative analysis of the computational overhead of the influence score computation.
- Add a comparison with simple heuristic mixtures (e.g., uniform with FineWeb-Edu upweighted) to isolate the benefit of the influence-based method.
- Discuss the sensitivity of the results to the number of checkpoints and blending factors, or provide a default choice with justification.

## Score and Decision
MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>