## Summary

This paper introduces the Perceptually-Grounded Geospatial Chain-of-Thought (Geo-CoT) framework for Vision-Language Models in remote sensing. The authors construct Geo-CoT380k, the first large-scale dataset of structured CoT rationales for remote sensing, and train RSThinker via a two-stage alignment strategy combining supervised fine-tuning with Group Relative Policy Optimization (GRPO). The resulting model demonstrates strong performance across multiple remote sensing tasks including visual grounding, object counting, detection, classification, captioning, and VQA.

## Strengths

- **Comprehensive experimental evaluation**: The paper evaluates RSThinker across a wide range of remote sensing tasks (visual grounding, object counting, detection, classification, captioning, VQA) with extensive comparisons against both general-purpose and domain-specific VLMs, including proprietary models like Claude, Gemini, and ChatGPT. The results show substantial improvements, particularly in fine-grained perception tasks (e.g., +30+ mIoU over GLM-4.1V-Thinking on visual grounding benchmarks).

- **Novel dataset contribution**: Geo-CoT380k (384,591 samples) is presented as the first large-scale CoT dataset for remote sensing, spanning multiple tasks including VQA, captioning, classification, grounding, counting, and detection. The scalable pipeline using GPT-4V with strict conditioning on verified bounding boxes is a practical methodological contribution.

- **Well-motivated problem framing**: The paper convincingly argues that end-to-end VLMs in remote sensing suffer from unverifiable reasoning, and makes a strong case for why perceptual grounding is particularly important in Earth Observation (dense objects, scale variations, high-stakes applications).

- **Clean ablation study**: Table 8 clearly demonstrates the contribution of each component (SFT without CoT, SFT with CoT, and GRPO), showing that structured CoT rationales provide substantially more benefit than direct task fine-tuning, and that GRPO provides additional gains.

## Weaknesses

### Major

- **Limited novelty of the overall approach relative to existing work**: The two-stage pipeline of SFT followed by RL (GRPO) for CoT reasoning closely mirrors established methodologies from the LLM reasoning literature (e.g., DeepSeek-R1, reasoning-oriented LLMs). The "Planning–Grounding–Synthesis" cognitive architecture, while well-described, does not appear to be a fundamentally new design; it is essentially standard CoT with explicit spatial references. The paper's primary contribution is the domain adaptation of these existing techniques to remote sensing, which is valuable but may not rise to the standard of a top-tier methods paper at ICLR.

- **The claim of "perceptual grounding" is overstated**: The framework grounds reasoning through bounding box coordinates, but the paper does not provide rigorous evidence that the model is actually attending to the specified regions. The model could be learning to output plausible-looking coordinates as a stylistic pattern without genuine visual grounding. The failure case in Figure 7 explicitly shows this: the model outputs a coherent reasoning trace with a bounding box for a non-ship object, suggesting the "grounding" mechanism can act as a learned heuristic rather than true perceptual anchoring. The paper would benefit from visual attention analysis or human evaluation to verify grounding fidelity.

- **GRPO reward design details are problematic**: Table 3 shows task-specific reward functions, but several are poorly specified. For object counting, the reward uses "Abs" without definition. For image captioning, a weighted combination of BLEU-4, METEOR, CIDEr, and ROUGE-L is used as an RL reward signal—this is known to potentially optimize for surface form overlap rather than semantic quality. The reward for VQA uses a three-tier system (1.0, 0.6, 0.0) without explaining how "partially correct" (0.6) is operationalized across different question types.

- **GRPO training details are insufficient**: The paper mentions using "on-policy sampling" with "k outputs" per group, but does not specify the value of k, the number of training steps, batch sizes, or computational budget for RL training. The GRPO objective includes a KL penalty, but the paper does not report the β hyperparameter or how it was tuned.

## Minor

- **Fairness of baseline comparisons**: Some comparisons may be unfair due to training data overlap. For example, RSThinker is trained on DOTA-v2-train and HRRSD-train, then evaluated on DOTA-v2-val and HRRSD-test. While this is standard practice, several baselines (especially general-purpose VLMs) would not have been trained on these specific remote sensing datasets. The large gap on counting benchmarks (e.g., 85.26 vs. 61.48 Acc on HRRSD) may partially reflect task-specific training rather than general reasoning capability.

- **Missing error bars**: All main results are presented as point estimates without variance information. Given the stochastic nature of CoT generation and RL training, this omission makes it difficult to assess the statistical significance of reported improvements.

- **The paper claims "the first" too aggressively**: The paper claims "the first large-scale CoT dataset for remote sensing" and "the first VLM for geospatial reasoning." However, SegEarth-R1 (Li et al., 2025a), RemoteReasoner (Yao et al., 2025), and other works cited by the authors explicitly generate CoT rationales for remote sensing. The paper needs to more carefully distinguish what is novel about Geo-CoT380k compared to these existing efforts.

## Trivial

- Table 2 title reads "Additional Dataset for RL" but it appears to list evaluation or training datasets, not the RL dataset itself. The description in Section 3.3 says GRPO uses "the original, rationale-free instances from Geo-CoT380k, augmented with additional datasets," which conflicts slightly with the table labeling.

- Several typos in baseline model names appear throughout tables (e.g., "Claude-some4," "SkSenceGPT," "VHIM").

## Nice-to-Haves

- A human evaluation study assessing whether the generated rationales are actually faithful to the image, rather than just structurally plausible.
- Zero-shot/ablative analysis on a new, unseen RS benchmark to validate generalization beyond training datasets.

## Novel Insights

The paper's most interesting observation is that explicit grounding in reasoning traces (even when imperfect, as in the failure case) can serve as a safety mechanism: by externalizing the specific spatial reference ([413, 225]), the model makes its errors auditable and falsifiable, which is a unique property for high-stakes EO applications. This insight—that grounded reasoning provides a transparency guarantee even when accuracy fails—is worth further exploration.

## Suggestions

1. Include error bars or confidence intervals on all main results to establish statistical significance.
2. Provide a visual attention analysis (e.g., GradCAM) on a sample of outputs to demonstrate that the specified bounding boxes genuinely correspond to attended regions, rather than being syntactically plausible patterns.
3. Clarify whether the large improvements on counting and grounding tasks reflect genuine reasoning advances or primarily reflect task-specific training data not available to baselines.
4. Report GRPO hyperparameters (k, β, number of steps, compute budget) and more clearly separate the RL training set from evaluation sets.

## Score and Decision

The paper makes a solid empirical contribution by demonstrating that structured CoT with explicit grounding, combined with modern RL fine-tuning, can achieve strong results across diverse remote sensing tasks. The dataset is a valuable resource. However, the core technical approach is a direct application of existing LLM reasoning techniques (SFT + RL) to a new domain, without substantial methodological innovation. The claimed "perceptual grounding" is not rigorously validated beyond output format. The paper would be stronger with clearer novelty signals and stricter evaluation protocols.

MY FINAL SCORE: 6.0<score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>