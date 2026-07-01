## Summary

This paper introduces a new perspective on machine unlearning by decoupling the class label from the target concept, identifying four distinct forgetting scenarios (all matched, target mismatch, model mismatch, data mismatch) that better reflect practical unlearning requests. The authors systematically analyze the forgetting dynamics at the representation level, introduce the notion of representation gravity, and propose TARF – a general framework combining annealed gradient ascent on the forgetting data with target-aware gradient descent on selected retaining data to approximate retraining. Extensive experiments on CIFAR-10/100, ImageNet-1k, and real-world applications (stable diffusion, LLM unlearning) demonstrate that TARF consistently outperforms existing unlearning methods in mismatched scenarios while remaining competitive on conventional all-matched forgetting.

## Strengths

- **Novel problem formulation**: The paper is the first to systematically study mismatched label domains in class-wise unlearning (target mismatch, model mismatch, data mismatch). This is a practically relevant and under-explored direction that opens up new research questions beyond the standard all-matched setting.

- **Principled analysis of forgetting dynamics**: Theorem 3.2 and the accompanying empirical analysis (Figure 3) provide a clear theoretical grounding for how representation similarity governs the co-movement of different data subsets during gradient-based unlearning. The "representation gravity" concept is well-motivated and directly informs the algorithm design.

- **Effective and general framework**: TARF unifies three phases (target identification, target separation, retraining approximation) into a single objective. It works across all four mismatch scenarios without requiring task-specific modifications, as demonstrated by the comprehensive results in Table 3 and Table 4.

- **Thorough empirical evaluation**: The paper conducts experiments on multiple benchmarks (CIFAR-10/100, Tiny-ImageNet, ImageNet-1k) with several architectures, includes ablation studies on key hyperparameters (k, annealing strategy, operation on selected data), and extends to real-world applications (stable diffusion concept removal, TOFU LLM unlearning). The results are consistently strong.

## Weaknesses

### Fatal

None.

### Major

- **Limited theoretical novelty**: Theorem 3.2 is essentially a Lipschitz-based bound that quantifies how representation distance affects gradient ascent dynamics. While the interpretation is useful, the core inequality is a straightforward consequence of smoothness assumptions and does not offer fundamentally new theoretical insights beyond what is already well understood in the optimization literature. The paper would benefit from a deeper theoretical characterization of when the gravity effect is strong enough to guarantee identification.

- **Hyperparameter sensitivity is underexplored**: The method introduces several hyperparameters (initial strength k, transition times t0, t1, threshold β) whose interplay is not fully analyzed. The ablation on k is helpful, but the sensitivity to t0, t1, and the threshold estimation method (e.g., top-10% rule) is not systematically studied across datasets and scenarios. This raises concerns about the need for additional tuning in new applications.

### Minor

- **Evaluation metrics in model mismatch need more nuance**: In the model mismatch scenario, the retrained model's UA is not zero (e.g., 87.76% on CIFAR-10), which is correctly handled by the Gap metric. However, the interpretation of MIA in this setting is less clear because the retrained model still predicts the superclass label for forgetting-class data. The paper would benefit from a brief clarification of how MIA should be interpreted when label spaces differ.

- **Real-world application results are limited**: The stable diffusion and TOFU experiments are presented only briefly (Figure 6 and Table 5). The TOFU table in particular appears to have formatting issues (repeated rows) and lacks a clear comparison to the retrained reference in the LLM setting. The paper would be stronger with a more detailed case study and quantitative comparison in at least one real-world scenario.

### Trivial

None.

## Nice-to-Haves

- A visualization of the learned representations after each phase of TARF (similar to Figure 3 but for the final unlearned model) would help readers intuitively understand how the method disentangles the target concept.
- A discussion of how the representation gravity signal can be used in a weakly supervised setting where no class labels are available for identification (as hinted in Appendix B) would broaden the applicability.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that *forgetting dynamics themselves contain rich information about latent concept structure* – the co-movement of losses/accuracies during gradient ascent can be exploited to identify data that belong to the same semantic concept as the forgetting set, even when labels are mismatched. This "gravity" perspective transforms unlearning from a one-step scrubbing operation into an iterative discovery process. The paper also highlights a fundamental tension: removing a target concept while preserving model utility requires both *decomposition* (when representations are entangled) and *completion* (when the forgetting set is a subset of the target concept), which most existing methods fail to balance.

## Suggestions

- Provide a systematic study of how the threshold β (based on loss/accuracy change ranking) performs under different noise levels or when the number of false retaining classes is unknown. A simple sensitivity analysis would increase confidence in the method's robustness.
- Clarify the evaluation of MIA and UA in the model mismatch scenario – specifically, how the superclass-level prediction affects the interpretation of membership inference attacks.
- Include the full results with standard deviations for all main experiments (Table 3) in the main text rather than only in the appendix, as the variability is important for assessing reliability.

## Score and Decision

**Score**: 7.0  
**Decision**: Accept  

MY FINAL SCORE: <score>7.0</score>  
MY FINAL DECISION: <decision>Accept</decision>