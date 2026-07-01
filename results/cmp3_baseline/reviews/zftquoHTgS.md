## Summary

This paper identifies and characterizes the "underthinking" problem in Long Chain-of-Thought (LongCoT) reasoning LLMs, where models prematurely abandon promising reasoning paths by switching thoughts too frequently without sufficient exploration. To address this, the authors propose SmartSwitch, a training-free, plug-and-play inference framework that uses a Process Reward Model (PRM) to detect prematurely abandoned high-potential thoughts and intervenes by backtracking and injecting a "deepen prompt" to encourage further exploration. Experiments on five mathematical reasoning benchmarks across multiple model scales (1.5B to 32B) show consistent accuracy improvements (e.g., +16.7% on AIME25 for 1.5B, +10.0% on AIME25 for QwQ-32B) while also reducing response length and inference time.

## Strengths

- **Clear problem identification and characterization**: The paper provides both qualitative and quantitative evidence for the underthinking phenomenon, introducing a well-defined metric (Underthinking Frequency) and demonstrating its correlation with problem difficulty and incorrect answers across multiple models. This establishes a solid motivation for the proposed method.
- **Practical and effective framework**: SmartSwitch is training-free, model-agnostic, and plug-and-play, making it immediately applicable to existing LongCoT models without additional training. The results show substantial and consistent gains across model sizes (1.5B to 32B) and benchmarks, with particularly impressive improvements on smaller models (e.g., +23.3% on AIME25 for 7B).
- **Efficiency improvements alongside accuracy gains**: Counterintuitively, the method reduces both response length and wall-clock inference time while improving accuracy, demonstrating that it prunes wasteful reasoning rather than simply adding more computation. This is a strong practical advantage.
- **Thorough ablation studies**: The paper systematically ablates key design choices including the PRM model, process division strategy, score mapping strategy, and score threshold, providing clear evidence for each design decision and showing the importance of selective, PRM-guided intervention over naive approaches.

## Weaknesses

### Fatal
None.

### Major
- **Reliance on a single PRM with limited analysis of PRM quality**: The framework's performance is fundamentally bounded by the PRM's ability to assess reasoning path potential. While the paper shows Universal-PRM-7B outperforms other PRMs, there is no analysis of PRM accuracy on this specific task (e.g., what percentage of "high-potential" thoughts flagged by the PRM actually lead to correct answers when deepened?). The "Always Intervene" baseline (18.9%) shows that naive intervention hurts, but the paper does not report false positive/negative rates of the PRM's assessments, which is critical for understanding the framework's reliability.
- **Limited evaluation scope**: The method is only evaluated on mathematical reasoning benchmarks. While the paper acknowledges this as a limitation, the claim that SmartSwitch is a general reasoning enhancement framework would be significantly strengthened by evaluation on at least one additional domain (e.g., programming, scientific QA, or logical reasoning). The current evaluation, while thorough for math, does not demonstrate generality.
- **Thought-switch detection via linguistic cues is fragile**: The detection mechanism relies on a predefined list of linguistic cues (e.g., "Alternatively"). The paper acknowledges this limitation but does not analyze its recall (what fraction of actual thought switches are captured?) or precision (how many detected "switches" are false positives?). A model that switches thoughts without explicit textual markers would be missed entirely, potentially limiting real-world applicability.

### Minor
- **The "deepen prompt" is fixed and relatively simple**: The intervention uses a single, generic prompt ("Wait, this seems like a promising idea..."). While effective, the paper does not explore whether more context-aware or dynamically generated prompts could yield further improvements. The fixed prompt may not be optimal for all reasoning contexts.
- **Hyperparameter sensitivity**: The ablation on the score threshold (Table 8) shows that performance is highly sensitive to this value—a change from 0.70 to 0.71 drops accuracy from 40.0% to 30.0% for the 1.5B model. The paper does not provide guidance on how to select this threshold for new models or domains without extensive tuning.

### Trivial
None.

## Nice-to-Haves

- An analysis of the PRM's false positive/negative rates on the thought evaluation task would strengthen confidence in the framework's reliability.
- Evaluation on at least one non-mathematical reasoning benchmark (e.g., GPQA, LiveCodeBench) would significantly strengthen claims of generality.
- A study of the recall/precision of the linguistic cue-based switch detection mechanism would help understand its limitations.

## Novel Insights

The key insight is that the "underthinking" problem in LongCoT models can be effectively mitigated through a lightweight, inference-time intervention that selectively encourages deeper exploration of promising but prematurely abandoned reasoning paths. The finding that this intervention simultaneously improves accuracy and reduces token usage is particularly noteworthy—it suggests that the model's default exploration-exploitation balance is suboptimal, and that targeted redirection toward high-potential paths can prune wasteful exploration while improving outcomes. This contrasts with prior work (TIP) that applies uniform penalties to all thought-switching, which the paper shows is less effective because it cannot distinguish between productive and unproductive switches.

## Suggestions

- Add an analysis of PRM evaluation quality on the thought-scoring task, reporting metrics such as the percentage of high-scoring thoughts that, when deepened, lead to correct answers versus those that remain unproductive.
- Include at least one non-mathematical reasoning benchmark (e.g., a programming or science QA dataset) to demonstrate the generality of the approach beyond math.
- Provide a more detailed analysis of the linguistic cue detection mechanism, including recall and precision estimates, and discuss potential failure cases where thought switches occur without explicit cues.

## Score and Decision

The paper makes a clear, well-motivated contribution with a practical, effective, and thoroughly evaluated method. The problem is well-characterized, the approach is sound, and the results are strong and consistent across model scales. The main limitations are the reliance on a single PRM without deep analysis of its evaluation quality, and the narrow evaluation domain (math only). These are significant but not fatal, and the paper's practical value and clear presentation warrant acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>