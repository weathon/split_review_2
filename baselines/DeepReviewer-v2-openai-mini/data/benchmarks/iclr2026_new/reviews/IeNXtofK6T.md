## Summary
# Final Review Report

## Summary

This paper revisits a simple yet previously dismissed idea: using an off-the-shelf LLM to detect and remove prompt injection attacks. The proposed method, PromptArmor, operates as a guardrail layer that prompts a modern LLM (GPT-4o, GPT-4.1, or Qwen3-32B) to identify injected instructions within data samples and then removes them via fuzzy matching before the backend LLM processes the data. The authors argue that prior work considered this approach ineffective because it relied on older LLMs (e.g., GPT-3.5) with weaker reasoning capabilities, and that the strong reasoning abilities of current LLMs change this conclusion.

The evaluation covers three benchmarks (AgentDojo, Open Prompt Injection, TensorTrust) and demonstrates that PromptArmor with GPT-4o/GPT-4.1 achieves very low false positive and false negative rates (below 1% on AgentDojo, below 5% on the other two). The attack success rate drops from 54.53% (undefended) to 0.00% with GPT-4.1. Additional ablations examine the impact of model size and reasoning capability (using Qwen3 models), alternative prompting strategies, adaptive attacks (AgentVigil), and data memorization.

**Core contributions claimed by the authors:**
- **C1:** Revisiting and re-establishing off-the-shelf LLM prompting as an effective prompt injection defense, leveraging modern LLMs with strong reasoning.
- **C2:** Adding prompt removal (not just detection) so that sanitized inputs can still be processed by the backend LLM, preserving task continuity.
- **C3:** Comprehensive empirical characterization of how reasoning capability and model size affect detection performance.

**Novelty note:** Due to Retrieval-Disabled Mode in this review run, external literature verification was not possible. The novelty and positioning claims (C1-C3) are assessed from the manuscript-internal evidence only and should be verified against the broader literature by the authors and readers.

## Strengths
**1. Timely and practical research question.** Prompt injection is a critical security concern for LLM agents, and a simple, deployable defense baseline is of high practical value. The paper addresses a real gap: the assumption that prompting-based detection does not work, which was based on older, weaker models.

**2. Clean, modular architecture.** PromptArmor's design as a drop-in guardrail layer that does not modify the backend LLM or agent architecture is a practical strength. This modularity reduces adoption barriers and is clearly motivated.

**3. Broad and transparent evaluation.** The evaluation spans three benchmarks (AgentDojo, Open Prompt Injection, TensorTrust) covering both agent and non-agent scenarios. The use of multiple guardrail LLMs (GPT-3.5, GPT-4o, GPT-4.1, Qwen3 family) provides a systematic view of how model capability affects defense performance.

**4. Informative ablation on model size vs. reasoning.** The Qwen3 ablation (Section 4.4) is a highlight of the paper: it disentangles the effects of model capacity and reasoning mode on detection accuracy. The finding that 32B models approach GPT-4.1 performance is practically useful and helps readers understand when prompting-based defense is viable.

**5. Proactive contamination check.** The memorization test (Section 4.5) addresses a key concern in closed-source LLM evaluation. While not definitive, the effort to rule out data leakage strengthens confidence in the results.

**6. Adaptive attack robustness testing.** The inclusion of AgentVigil-based adaptive attacks (Section 4.6) goes beyond standard benchmark evaluation and provides preliminary evidence that the defense is not trivially circumvented by automatically generated attack variants.

## Weaknesses
**W1 — Absence of formal threat model (Major).** The paper does not define a formal threat model specifying attacker knowledge, capabilities, and goals. The evaluation only covers four specific attack templates on AgentDojo, leaving unclear what broader class of attacks the defense is expected to handle. Without a threat model, it is difficult to assess the completeness of the evaluation or to generalize the results. The defense problem description (Page 1 - Section 2: Defense problem) is stated in prose without formalizing assumptions about whether the attacker knows the guardrail prompt or can adapt to the defense.

**W2 — Overly strong claims of generality (Major).** The Abstract and Conclusion state that prompting an off-the-shelf LLM "should be regarded as a standard baseline" for evaluating defenses, but the evidence comes from only three benchmarks with a narrow set of attack types (four templates on AgentDojo, five on Open Prompt Injection, two on TensorTrust). The claim that PromptArmor is "robust against adaptive attacks" is based on a single automated red-teaming tool (AgentVigil) and may not hold under more diverse adaptive strategies, including human-crafted adversarial prompts or optimization-based attacks. See annotations on Abstract (Page 1 - Abstract) and Adaptive Attacks (Page 1 - Section 4.6).

**W3 — Exclusion of training-based defenses weakens comparison (Major).** The paper excludes training-based defenses (SecAlign, StruQ) from the main comparison table with the justification that they exhibit "poor utility on AgentDojo even in the absence of attacks." However, this assertion is not quantitatively supported in the paper. These methods represent a major family of prompt injection defenses, and their exclusion may inflate PromptArmor's relative performance. A fair comparison should either adapt these methods to the agent setting or provide concrete utility numbers justifying the exclusion. See annotation on Page 1 - Section 4.2 Results.

**W4 — Underspecified sanitization mechanism (Major).** The fuzzy matching removal algorithm (Page 1 - Section 3.1) is described only at a high level: "extract all words... construct a regular expression that allows arbitrary characters between these words." Key details are missing: word tokenization rules, handling of multiple overlapping injections, and safety guarantees against incomplete removal (which could leave residual malicious instructions). The claim that removal is better than rejection is not quantitatively supported — there is no experiment comparing user task success with removal vs. rejection under the same conditions.

**W5 — Conclusion lacks limitations and future work (Major).** The Conclusion (Page 1 - Section 6) is only two sentences that restate the abstract without discussing any limitations, failure conditions, or concrete next steps. This is a significant omission for a security paper. Readers need to understand when PromptArmor might fail (e.g., under strong adaptive attacks, with low-capacity models, or in non-English contexts) and what improvements are most needed. See annotation on Page 1 - Section 6.

**W6 — No statistical significance or variance reporting (Minor).** All evaluation results (FPR, FNR, UA, ASR) are reported as point estimates without confidence intervals, standard deviations, or significance tests. Given the very low error rates (e.g., 0.07% FPR), even a handful of misclassified samples could cause substantial relative shifts. Multiple runs with different random seeds or data splits are not reported.

**W7 — Combined ASR metric conflates attack types (Minor).** The combined ASR metric (Page 1 - Section 4.2) counts a defense as failed if any one of four attack types succeeds. This union-based metric makes it impossible to distinguish between a defense that completely blocks three attack types but fails on one (which may still be valuable) versus one that partially fails across all types. Per-attack ASR should be reported.

**W8 — Prompt engineering dependency chain (Minor).** In Section 4.3, the definition of "prompt injection" used to improve GPT-3.5's performance is generated by GPT-4.1 itself. This creates a dependency chain: the weaker model's performance depends on the stronger model's output quality. The paper does not analyze whether this introduces a systematic bias — e.g., if GPT-4.1's definition reflects the same detection patterns that make GPT-4.1 effective, which may not transfer to other models or settings.

**W9 — Memorization test limited scope (Minor).** The memorization test is only conducted on GPT-4.1, while GPT-4o is also a primary guardrail model. The 3.5% of samples exceeding the memorization threshold could still affect benchmark conclusions, especially if those cases are systematically easier. See annotation on Page 1 - Section 4.5.

**W10 — Cost analysis missing (Minor).** Section 3.2 claims "computational efficiency" as an advantage, but no cost comparison is provided between API-based (GPT-4o/GPT-4.1) and open-source (Qwen3) deployment options. A 32B open-source model requires substantial inference hardware, which may negate the cost advantage over API alternatives. See annotation on Page 1 - Section 4.4.

## Score
**Final Score: 6/10**

**Scoring rationale:** The paper addresses a practical problem with a clean evaluation, but the core idea (prompting an LLM to detect injections) is not conceptually new — the main contribution is demonstrating that modern LLM capabilities change the effectiveness regime. The empirical work is solid and the ablation on model size vs. reasoning is informative, but several major weaknesses (missing threat model, overclaimed generality, exclusion of key baselines, underspecified removal mechanism, and absent limitations discussion) prevent a higher score. The paper is publishable with major revisions addressing these issues.

**Key strengths supporting the score:** Practical relevance, systematic evaluation across multiple guardrail LLMs, informative Qwen3 ablation, proactive contamination check, adaptive attack testing.

**Key weaknesses constraining the score:** (W1) No formal threat model; (W2) Overclaimed generality beyond evaluated scenarios; (W3) Exclusion of training-based defenses without quantitative justification; (W4) Underspecified sanitization mechanism; (W5) Conclusion lacks limitations and future work; (W6-W10) Various methodological and reporting gaps.