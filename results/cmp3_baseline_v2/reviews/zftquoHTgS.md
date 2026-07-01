## Summary

This paper identifies and characterizes the "underthinking" problem in Long Chain-of-Thought (LongCoT) LLMs, where models prematurely abandon promising reasoning paths by switching thoughts too frequently without sufficient exploration. To address this, the authors propose SmartSwitch, a training-free, plug-and-play inference framework that uses a Process Reward Model (PRM) to detect prematurely abandoned high-potential thoughts and intervenes by backtracking and injecting a "deepen prompt" to encourage further exploration. Experiments on challenging mathematical reasoning benchmarks (AIME24/25, AMC23, MATH-500, GaoKao2023en) show consistent accuracy improvements across multiple model families and sizes (1.5B to 32B), while also reducing response length and inference time.

## Strengths

- **Well-motivated problem identification**: The paper provides both qualitative and quantitative evidence for the underthinking phenomenon, including a new metric (Underthinking Frequency) and systematic analysis showing its correlation with problem difficulty and incorrect answers. This establishes a clear and practically relevant research problem.
- **Simple yet effective method**: SmartSwitch is training-free, model-agnostic, and operates purely at inference time, making it immediately applicable to existing LongCoT models without additional training cost. The design is clean and the two-module (Perception + Intervention) architecture is intuitive.
- **Strong empirical results**: The method achieves substantial and consistent accuracy gains across five benchmarks and five model variants (1.5B to 32B), with improvements as large as +23.3% on AIME25 for the 7B model. Notably, it also reduces both response length and wall-clock inference time, demonstrating that deeper exploration of promising paths can replace wasteful shallow switching.
- **Thorough ablation studies**: The paper systematically ablates key design choices including the PRM model, process division strategy, score mapping strategy, and score threshold, providing clear evidence for why each component is designed as it is.

## Weaknesses

### Major

- **Dependence on external PRM quality and availability**: The framework's effectiveness is fundamentally bounded by the PRM's ability to correctly assess reasoning path potential. The paper uses Universal-PRM-7B, which is a specific model with long-context support, but the general availability and reliability of such PRMs for diverse reasoning domains is not guaranteed. The ablation shows that a naive "Always Intervene" baseline degrades performance (18.9% vs 20.0% vanilla), confirming that poor PRM calibration can hurt rather than help.
- **Hyperparameter sensitivity**: The score threshold ablation (Table 8) reveals extreme sensitivity: for R1-Distill-Qwen-1.5B, accuracy jumps from 30.0% at threshold 0.69 to 40.0% at 0.70, then drops back to 30.0% at 0.71. This narrow effective range (0.70 ± 0.01) raises concerns about robustness and the need for careful per-model tuning. The paper does not provide guidance on how to select this threshold in practice without access to a validation set.
- **Limited evaluation scope**: The method is evaluated exclusively on mathematical reasoning benchmarks. While mathematics is a natural testbed for reasoning, the paper claims broader applicability (software engineering, scientific discovery, legal analysis) without any evidence. The thought-switch detection via linguistic cues (e.g., "Alternatively") may not generalize to domains with different discourse structures.

### Minor

- **Thought-switch detection is heuristic**: The reliance on a fixed set of linguistic cues (e.g., "Alternatively") may miss subtle or implicit thought transitions that lack explicit textual markers. The paper acknowledges this limitation but does not quantify how many switches are missed or how this affects performance.
- **The "deepen prompt" is fixed**: The intervention uses a single, hand-crafted prompt ("Wait, this seems like a promising idea..."). The paper does not explore whether different prompts or dynamically generated prompts could yield better results, nor does it ablate the prompt wording.
- **Comparison with TIP is limited**: The TIP baseline (Wang et al., 2025) is compared only on one model (1.5B) and one benchmark (AIME24). A broader comparison across models and benchmarks would strengthen the claim that SmartSwitch is superior to existing underthinking mitigation methods.

### Trivial

- The paper states "We report the pass@1 accuracy averaged on 32 responses for all benchmarks" but does not report standard deviations or confidence intervals, making it difficult to assess the statistical significance of the reported gains.

## Nice-to-Haves

- An analysis of how many interventions are actually triggered per problem and how often the PRM's assessment aligns with human judgment of "promising thought."
- A study of the method's behavior on problems where the model already answers correctly—does SmartSwitch ever degrade performance on these cases? (The paper briefly mentions it maintains 100% accuracy on previously correct answers for one model/benchmark, but a systematic analysis would be valuable.)
- Exploration of whether the PRM could be replaced by a simpler heuristic (e.g., thought length, self-consistency) to reduce external dependencies.

## Novel Insights

None beyond the paper's own contributions. The key insight—that premature thought-switching in LongCoT models can be detected and mitigated by evaluating abandoned thoughts with a PRM and intervening with a deepening prompt—is well-executed but not conceptually surprising given the existing literature on process reward models and the known "underthinking" phenomenon.

## Suggestions

- Provide guidance on how to select the score threshold in practice, e.g., using a small validation set or a calibration procedure, and report the sensitivity of results to this choice across multiple models.
- Evaluate the method on at least one non-mathematical reasoning domain (e.g., multi-hop QA, scientific reasoning) to support the claim of broader applicability.
- Report standard deviations or confidence intervals for the main results to allow assessment of statistical significance.
- Quantify the recall of the linguistic-cue-based switch detection (what fraction of actual thought switches are captured?) and discuss the impact of missed detections.

## Score and Decision

The paper addresses a well-motivated and practically important problem with a clean, training-free method that achieves strong and consistent empirical gains. The ablations are thorough and the efficiency improvements are a nice bonus. However, the extreme hyperparameter sensitivity (threshold 0.70 ± 0.01) and the dependence on a specific external PRM with limited availability are significant concerns that temper enthusiasm. The evaluation is also limited to mathematics. These issues are major but not fatal—the core contribution is solid and the method is likely to be useful to the community.

MY FINAL SCORE: 6.0score</score>
MY FINAL DECISION: Accept</decision>