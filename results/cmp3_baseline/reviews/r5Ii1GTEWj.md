## Summary

This paper proposes Motion-R1, a framework for text-to-motion generation that aims to handle multi-turn dialogue inputs and enforce physical consistency. The authors introduce a Motion2Motion dataset with ERA-CoT annotations, an enhanced GRPO algorithm using JS-divergence, and a low-level RL-based kinematic optimization. The work claims to bridge the gap between semantic understanding of complex contexts and physically plausible motion synthesis.

## Strengths

- The paper identifies a genuine limitation in current text-to-motion methods: most cannot handle multi-turn dialogue or implicit user intentions, and they often lack physical consistency. The motivation to address both issues simultaneously is well-founded.
- The three-component pipeline (dataset → GRPO training → low-level optimization) is logically structured and attempts to create a closed-loop system from high-level intent to physically executable motion.
- The inclusion of a low-level kinematic optimization component that enforces physical constraints (joint limits, collision avoidance) is a practical addition that many prior text-to-motion works neglect.

## Weaknesses

### Fatal

- **The experimental evaluation is fundamentally insufficient and does not support the paper's core claims.** The paper claims to generate "physically consistent" motions from "multi-turn dialogue" inputs, yet the experiments only evaluate text generation metrics (semantic similarity, keyword matching, Jaccard similarity) on action/skill descriptions, not on actual motion sequences. There are no quantitative metrics for motion quality (e.g., FID, R-precision, diversity), no physical plausibility metrics (e.g., foot skating, penetration rates), and no comparison to standard text-to-motion baselines (MDM, MLD, T2M-GPT, etc.). The only visual result (Figure 3) shows a robot performing a "kick the door" action, but this is a qualitative comparison against "Anyskill" with no quantitative motion evaluation.

- **The paper's claims about "multi-turn dialogue" understanding are unsubstantiated.** The Motion2Motion dataset is described as containing "multi-turn dialogic interactions," but the experiments only evaluate single-turn action/skill generation. There is no experiment demonstrating multi-turn dialogue comprehension, no comparison on multi-turn inputs, and no metric for contextual continuity across turns. The core claimed contribution—handling multi-turn dialogue—is never tested.

- **The evaluation metrics are inappropriate for the claimed task.** The paper evaluates action and skill generation using text-based metrics (semantic similarity, keyword matching, Jaccard similarity) on the output of a language model, not on generated motion sequences. This evaluates whether the LLM can produce text descriptions of actions, not whether the system can generate actual motions. The "low-level kinematic optimization" component (Section 3.3) is described but never quantitatively evaluated—there are no results showing that it improves physical plausibility over baselines.

### Major

- **The paper lacks comparisons to standard text-to-motion baselines.** The baselines used (Qwen2.5, Llama3.2) are general-purpose LLMs, not text-to-motion models. There is no comparison to MDM, MLD, MotionDiffuse, T2M-GPT, or any other established motion generation method. This makes it impossible to assess whether Motion-R1 advances the state of the art.

- **The Motion2Motion dataset is small (7,132 samples) and its construction methodology raises concerns.** The dataset is generated using GPT-4 with human-in-the-loop validation, but there is no analysis of dataset quality, no inter-annotator agreement, and no comparison to existing motion datasets (HumanML3D, KIT-ML, etc.). The ERA-CoT annotation framework is described in detail but its effectiveness is never empirically validated.

- **The GRPO formulation appears to contain errors.** Equation (3) shows `min(π_θ/π_θ_old, 1-ε, 1+ε)` which is not the standard PPO/GRPO clipping. The standard clipping is `clip(ratio, 1-ε, 1+ε)`, not a min over three arguments. This suggests a misunderstanding of the core algorithm.

- **The paper claims JS-divergence is superior to KL-divergence but provides no theoretical or empirical justification specific to motion generation.** The advantages listed (symmetric penalty, gradient stabilization, constrained update dynamics) are generic properties of JS-divergence, not specific insights about why it benefits motion generation. The experimental results show marginal improvements (e.g., SS 0.2178 vs 0.2111) that may not be statistically significant.

### Minor

- The paper's structure is unusual: the "Related Work" section includes a subsection on "Large Language Models" that reads like a general survey rather than a focused discussion of relevant prior work.
- Figure 4's evaluation uses "GPT-4 as the judge" with model names (Formal3.0, Formal3.0B, etc.) that are never defined in the paper, making the results uninterpretable.
- The paper claims to be "inspired by DeepSeek-R1" but does not actually implement any reasoning chain or test-time reasoning—the connection to R1 is superficial.

### Trivial

- The word cloud and frequency chart in Figure 2 are not informative for evaluating the method.
- Some equations (e.g., Equation 1) are presented with notation that is not clearly explained.

## Nice-to-Haves

- A proper evaluation on standard text-to-motion benchmarks (HumanML3D, KIT-ML) with standard metrics (FID, R-precision, diversity, multi-modality) would be necessary to establish the method's validity.
- An ablation study isolating the contribution of each component (dataset, GRPO, low-level optimization) would help understand what drives performance.
- User studies or perceptual evaluations would strengthen claims about "lifelike" and "contextually appropriate" motions.

## Novel Insights

None beyond the paper's own contributions. The idea of using RL to improve motion generation from text is not new, and the specific technical contributions (JS-divergence in GRPO, ERA-CoT annotation) are not convincingly shown to be effective.

## Suggestions

- The authors should either reframe the paper as a text-based action description generation method (and remove claims about actual motion generation) or conduct proper motion generation experiments with standard benchmarks and metrics.
- The multi-turn dialogue claim should either be demonstrated with concrete experiments or removed from the contributions.
- The GRPO formulation should be corrected to match standard PPO clipping, or the authors should explain the deviation.
- The low-level optimization component should be evaluated quantitatively, showing improvements in physical plausibility metrics.

## Score and Decision

The paper's core claims—physically consistent motion generation from multi-turn dialogue—are not supported by the experimental evidence. The evaluation only tests text generation capabilities, not motion generation, and lacks comparisons to standard baselines. The technical contributions (JS-divergence GRPO, ERA-CoT) are not convincingly validated. The paper does not meet the standards for acceptance at ICLR.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>