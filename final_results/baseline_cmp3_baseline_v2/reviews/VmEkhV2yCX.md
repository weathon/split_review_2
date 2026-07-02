## Summary

This paper presents a systematic study of how reasoning data—varying in scale, diversity, and quality—affects LLM performance when introduced at different stages of training (pretraining vs. SFT). The authors pretrain 8B models from scratch with different reasoning data configurations and evaluate downstream performance after SFT and RL. Their key findings are that front-loading reasoning data into pretraining creates a durable advantage (+19% after RL), that pretraining benefits most from diversity while SFT benefits most from quality (an asymmetric allocation principle), and that high-quality pretraining data can have latent effects only unlocked after SFT.

## Strengths

- **First systematic study of reasoning data placement across the full training pipeline.** The paper addresses an important and timely question—whether reasoning data should be introduced during pretraining or only during post-training—with a clean experimental design that controls for token budgets and data characteristics. This fills a clear gap in the literature where most work focuses on post-training only.

- **Strong empirical evidence for the "front-loading" advantage.** The results convincingly show that models pretrained with reasoning data maintain and amplify their advantage through SFT and RL, and that even doubling SFT epochs for the baseline cannot close the gap. The 19% average gain after RL on expert-level benchmarks is a striking result.

- **Actionable asymmetric allocation principle.** The finding that diversity matters most in pretraining while quality matters most in SFT provides a clear, practical heuristic for data strategy. The ablation showing that naive scaling of SFT data with mixed quality is actively harmful (-5% on math) is a valuable cautionary result.

## Weaknesses

### Major

- **The "catch-up" experiment is not a fair test of the hypothesis.** The authors test whether doubling SFT epochs for the baseline can match reasoning-pretrained models, but this is a weak test. A proper test of the catch-up hypothesis would involve using more SFT data (not just more epochs), higher-quality SFT data, or different SFT recipes. The claim that "SFT cannot compensate for a weak foundation" is too strong given that only one SFT scaling strategy was tested.

- **The reasoning data ratio during pretraining is confounded with data type.** The authors fix the token ratio at 20% reasoning data for 400B tokens, but this means that different reasoning datasets (e.g., D_SHQ with 1.2M samples vs. D_LDQ with 268M samples) are repeated very different numbers of times. This repetition could introduce confounding effects—the model sees the same narrow set of examples many times with D_SHQ, which could explain its weaker performance compared to the more diverse D_LDQ. The paper does not adequately address this confound.

- **Limited evaluation of generalization beyond reasoning tasks.** The paper focuses heavily on reasoning benchmarks (math, science, code) but does not systematically evaluate whether reasoning-rich pretraining harms performance on other capabilities (e.g., language understanding, factual knowledge, creative generation). The instruction-following metric (IFEval) shows some degradation with higher reasoning ratios (Table 7), but this is not explored in depth. Without broader evaluation, it's unclear whether the proposed strategy is a net positive or involves meaningful trade-offs.

### Minor

- **The "latent effect" claim is based on a single comparison.** The finding that M_LMQ outperforms M_LDQ after SFT despite similar pretraining performance is interesting, but it relies on a single data point. The effect size (+4.25%) is modest, and it's unclear whether this is statistically significant or reproducible.

- **The RL experiments are limited to one configuration.** Only two models are compared after RL (M_base + SFT_SHQ vs. M_LMQ + SFT_SHQ), which limits the generality of the RL-stage conclusions. It would be informative to see whether the asymmetric allocation principle holds through RL as well.

### Trivial

- The paper uses proprietary data (Nemotron-Pretraining-SFT-v1, NVIDIA base corpus) which limits reproducibility, though this is acknowledged and common in large-scale pretraining studies.

## Nice-to-Haves

- A more thorough test of the catch-up hypothesis using different SFT data mixtures, learning rates, or training durations would strengthen the central claim.
- Evaluation on non-reasoning benchmarks (e.g., MMLU general knowledge, HellaSwag commonsense, or open-ended generation quality) would help characterize trade-offs.
- Analysis of whether the benefits of reasoning-rich pretraining are driven by specific domains (e.g., math vs. code vs. science) or are broadly distributed.

## Novel Insights

Beyond the paper's own contributions, the most novel insight is the asymmetric allocation principle: the same data characteristics (diversity vs. quality) have opposite importance depending on the training phase. This suggests that the role of data in pretraining is to build broad, generalizable representations (where diversity helps), while SFT is about targeted refinement (where quality dominates). This is a useful conceptual framework that could inform data strategy beyond reasoning tasks. The finding that high-quality pretraining data can have "latent" effects only activated after SFT is also interesting, though less well-supported.

## Suggestions

- For the catch-up experiment, test whether a baseline model trained with 2x or 4x more SFT data (not just epochs) can match reasoning-pretrained models. Alternatively, use a stronger SFT recipe (e.g., longer training, different learning rate schedule) to give the baseline a fairer chance.
- Add evaluation on a broader set of benchmarks to characterize potential trade-offs, including language understanding (e.g., MMLU), commonsense reasoning (e.g., HellaSwag), and open-ended generation (e.g., MT-Bench).
- Clarify how data repetition is handled for small datasets (D_SHQ) and discuss whether this could confound the diversity vs. quality comparison.

## Score and Decision

The paper addresses an important and under-explored question with a well-designed experimental framework and produces several actionable findings. The main weaknesses are the limited test of the catch-up hypothesis and the potential confound from data repetition, but these do not invalidate the core contributions. The asymmetric allocation principle and the demonstration that front-loading reasoning data yields durable gains are valuable contributions to the community.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>