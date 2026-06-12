## Summary

This paper presents PromptArmor, a defense against prompt injection attacks that leverages an off-the-shelf LLM as a guardrail to detect and remove injected prompts from untrusted data samples before they reach the backend LLM. The authors demonstrate that while prior work dismissed this prompting-based approach as ineffective (evaluated on older LLMs), modern LLMs with strong reasoning capabilities (e.g., GPT-4o, GPT-4.1) achieve sub-1% false positive and false negative rates on AgentDojo and below 5% on Open Prompt Injection and TensorTrust. The paper argues this approach should be reconsidered as a standard baseline for evaluating prompt injection defenses.

## Strengths

- **Comprehensive and convincing experimental evaluation.** The paper evaluates PromptArmor across three established benchmarks (AgentDojo, Open Prompt Injection, TensorTrust), multiple guardrail LLMs (GPT-3.5, GPT-4o, GPT-4.1, Qwen3 family from 0.6B to 32B), multiple prompting strategies, and against adaptive attacks via AgentVigil. This breadth of evaluation substantially strengthens the empirical claims.

- **Informative ablation studies.** The investigation of model size and reasoning (Section 4.4) reveals that model capacity is the primary driver of detection performance, with Qwen3-32B matching GPT-4.1 regardless of reasoning mode, while reasoning particularly helps mid-sized models (8B). The prompting strategy ablation (Section 4.3) shows that naïve prompting fails and that providing a definition of "prompt injection" is necessary for weaker models. These findings provide genuinely useful guidance for practitioners.

- **Practical contribution with clear deployment value.** PromptArmor requires no model fine-tuning, no architectural changes, and can be deployed as a drop-in guardrail. The comparison in Table 2 shows it substantially outperforms existing defenses including fine-tuned detectors (Deberta, DataSentinel, Llama Prompt Guard 2) and system-level defenses (MELON) on the AgentDojo benchmark, achieving 0.00% ASR with GPT-4.1.

- **Responsible evaluation practices.** The memorization test (Section 4.5) addresses the important concern that detection performance could stem from benchmark data contamination rather than genuine detection capability. The adaptive attack evaluation using AgentVigil (Section 4.6) provides evidence of robustness against adversarial evasion.

## Weaknesses

### Fatal

None.

### Major

- **Limited novelty in the core approach.** The paper explicitly acknowledges that prompting-based detection has been proposed before (Stuart Armstrong, 2023; Nakajima, 2022; Liu et al., 2024). The primary contribution is demonstrating that it works better with modern, stronger LLMs. While this is a valid and useful empirical finding, the technical novelty is modest—the core method is a straightforward system prompt with fuzzy matching for removal. The paper would benefit from deeper analysis of *why* modern LLMs succeed where older ones failed beyond simply "stronger reasoning."

- **Adaptive attack evaluation is limited in scope.** The adaptive attacks use AgentVigil, which is a fuzzing-based template optimization method. A more concerning class of adaptive attacks—where the attacker specifically targets LLM-based detection by using obfuscation, encoding, role-playing, or other techniques designed to fool the guardrail LLM—is not explored. The claim of robustness would be substantially strengthened by including such targeted evasion attempts, particularly given that the attacker model can be assumed to know the defense mechanism.

- **Dataset-specific prompt tuning raises generalization concerns.** The paper states that "we adjusted the detection prompt for each dataset" (Section 4.1). While the core prompt structure appears consistent (Figure 2), this tuning per benchmark weakens the claim of easy deployment and strong out-of-the-box generalization. The paper should clarify exactly what was adjusted and whether a single universal prompt achieves comparable performance across all benchmarks.

### Minor

- **Computational cost and latency are not discussed.** Running an additional LLM inference for every untrusted data sample has non-trivial cost implications, especially for agent workflows with many tool calls. The paper discusses "computational efficiency" qualitatively in Section 3.2 but provides no quantitative analysis of latency or cost overhead.

- **Comparison fairness with DataSentinel.** The paper notes that DataSentinel uses Mistral-7B and wasn't adapted to agent settings, but still includes it as a primary comparison. A fairer comparison would either retrain DataSentinel with a stronger backbone or note this caveat more prominently in the main results table rather than in a paragraph of discussion.

- **The GPT-3.5 definition workaround (Section 4.3) has mixed implications.** On one hand, it shows that prompting strategy matters; on the other, it suggests the detection capability may partially depend on the model having been trained on security-related literature about prompt injection. This raises questions about generalization to entirely novel attack paradigms that aren't well-represented in training data.

### Trivial

None.

## Nice-to-Haves

- A failure analysis section examining specific examples where PromptArmor fails (both false positives and false negatives) would provide deeper insight into the method's limitations and help guide future work.
- Quantitative latency and cost measurements (e.g., tokens processed per second, additional API cost per agent step) would strengthen the practical deployment argument.
- Evaluation on more diverse and recent prompt injection benchmarks beyond the three used would further support the generalization claims.

## Novel Insights

The paper's most novel insight is methodological: it demonstrates that the performance gap between prompting-based and fine-tuned detection has essentially closed for modern LLMs, effectively inverting the community's prior understanding. The finding that a 32B parameter model matches frontier model performance (Qwen3-32B matching GPT-4.1) suggests that this capability is accessible at reasonable computational cost. The systematic demonstration that reasoning capability helps mid-sized models more than frontier models (where capacity alone suffices) is a useful contribution to understanding LLM security capabilities.

## Suggestions

- Add a targeted adaptive attack evaluation where the attacker specifically crafts injections designed to evade LLM-based detection (e.g., indirect instructions, encoded content, or benign-appearing language that misdirects the guardrail).
- Report results with a single fixed prompt across all benchmarks to disentangle the contribution of prompt engineering from model capability.
- Provide quantitative cost/latency analysis to support the practical deployment argument.
- Include a failure case analysis to characterize the types of attacks that PromptArmor still misses.

## Score and Decision

The paper makes a solid practical contribution by rigorously demonstrating that a previously dismissed defense approach is now highly effective with modern LLMs. The experimental evaluation is thorough and the results are compelling. However, the core technical novelty is limited—the method is straightforward prompting with fuzzy matching—and the adaptive attack evaluation could be stronger. As a baseline paper, it serves the community well, but its contributions are primarily empirical validation rather than new methods or deep theoretical insights.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <score>Accept</score>