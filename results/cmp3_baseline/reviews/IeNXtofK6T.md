## Summary

The paper proposes PromptArmor, a defense against prompt injection attacks that uses an off-the-shelf LLM (the “guardrail LLM”) to detect and remove injected prompts from data samples before they reach the backend LLM. The key finding is that, contrary to earlier results showing this approach was ineffective, modern LLMs with strong reasoning capabilities (e.g., GPT-4o, GPT-4.1) achieve extremely low false positive and false negative rates (below 1% on AgentDojo, below 5% on two other benchmarks), and that the defense is robust against adaptive attacks. The authors argue that prompting a strong, off-the-shelf LLM should now be regarded as a standard baseline for evaluating prompt injection defenses.

## Strengths

- **Strong empirical evidence:** PromptArmor is evaluated on three diverse benchmarks (AgentDojo, Open Prompt Injection, TensorTrust) with multiple models, showing convincing results. The detection FPR/FNR < 1% on AgentDojo and ASR drops from 54.53% to 0.00% using GPT-4.1.
- **Thorough ablation studies:** The paper systematically investigates the impact of model size, reasoning mode (Qwen3 with/without reasoning), prompting strategies, and data contamination (memorization test). These analyses strengthen the claim that reasoning capability is critical.
- **Practical and modular design:** The defense is a drop-in guardrail that requires no modifications to the backend LLM or agent architecture, and it includes a removal step (not just rejection) that preserves utility.
- **Adaptive attack evaluation:** The paper tests robustness against an automated red-teaming method (AgentVigil) and shows that PromptArmor remains effective even when the attacker tailors prompts to the defense.
- **Clear and well-structured writing:** The paper is easy to follow, with good illustrations (Figure 1 & 2) that clarify the workflow.

## Weaknesses

### Fatal

None.

### Major

- **Limited novelty:** The core idea—using a prompted LLM to detect prompt injection—has been explored before (e.g., Nakajima 2022, Liu et al. 2024). The paper’s main contribution is an empirical demonstration that stronger LLMs make it work well. This is a valuable finding, but it is conceptually straightforward and does not introduce a new technical principle or algorithm.
- **Incomplete baseline comparisons:** Several strong or recent defenses are omitted or only partially compared. For example, DataSentinel is tested with Mistral-7B (an older small model) rather than with a modern reasoning LLM. SecAlign and StruQ are mentioned but not run because they degrade utility; however, the paper does not quantitatively show that PromptArmor matches or exceeds them on utility under attack. The comparison would be stronger if the authors had adapted DataSentinel to use GPT-4o or compared against other prompt-injection-specific guardrail models.
- **No analysis of cost or latency:** The defense requires an additional LLM call for every data sample (and potentially per tool-call result in agents). For high-throughput systems, this overhead could be prohibitive. The paper does not discuss the practical deployment trade-offs.

### Minor

- **Limited adaptive attack threat model:** The adaptive attack evaluation uses only a single automated red-teaming framework (AgentVigil). It is plausible that more sophisticated human-crafted adaptive attacks or query-based attacks could evade PromptArmor, especially if the attacker knows the detection prompt. The paper could discuss this limitation.
- **Detection prompts differ per dataset:** The authors acknowledge adjusting the prompt for each benchmark (e.g., providing “prompt injection” definitions for GPT-3.5). This tuning might inflate performance; a single unified prompt across all datasets would be a stronger indicator of generalization.

### Trivial

- The paper states “We report the average FPR, and FNR, and UA of the four attacks mentioned above, and report the combined ASR” (Section 4.2) – small grammatical issue.
- “AgentVigil-NoDefense can achieve a high ASR” – the phrasing is slightly informal.

## Nice-to-Haves

- A cost/speed analysis comparing PromptArmor to other defenses (e.g., Tool Filter, which is also a call per tool use).
- An evaluation with a single fixed detection prompt across all three benchmarks to test robustness to prompt variation.
- A study of what types of injected prompts are most commonly misdetected (e.g., highly obfuscated instructions, context-dependent attacks).
- Comparison with more open-source guardrail models that have been released after the paper’s submission (e.g., NVIDIA NeMo Guardrails, Guardrails AI) to see if they also benefit from stronger base LLMs.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Expand the baseline comparison by re-implementing DataSentinel’s approach (known-answer detection) with GPT-4o or GPT-4.1 as the guardrail to isolate whether the improvement comes from the method or the model.
- Add a brief section discussing the practical deployment considerations (latency, cost, trade-offs between using the same vs. a smaller guardrail model) to help practitioners assess when PromptArmor is appropriate.

## Score and Decision

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>