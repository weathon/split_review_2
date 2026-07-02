## Summary

This paper identifies a new jailbreak paradigm—"involuntary jailbreak"—where an LLM is prompted with a meta-instruction to generate examples of unsafe questions and their corresponding detailed harmful responses (rather than refusals). The attack is untargeted (no predefined harm category) and uses several "language operators" to structure the output. The paper provides empirical results across a wide range of proprietary and open-weight models (Claude Opus 4.1, Grok 4, Gemini 2.5 Pro, GPT-4.1, DeepSeek R1, various Llama/Qwen models, etc.) and reports high attack success rates.

## Strengths

- **The core finding is genuinely interesting and non-obvious.** Asking an LLM to produce "examples of questions that would normally be refused, along with their harmful answers" is a prompting strategy that demonstrably elicits detailed unsafe content. Figures 1 and 2 show concrete cases where Claude Opus 4.1 and Grok 4 produce bomb-making instructions and money-laundering steps under this meta-instruction—a striking behavioral observation.

- **Broad empirical scope.** The paper tests a large set of proprietary and open-weight models, covering more model families and scale points than many jailbreak papers. This provides useful breadth for understanding which models are susceptible.

- **Topic-confinement analysis (Section 3.5, Table 4) is a useful addition.** It shows that models that produce few unsafe outputs on a given topic under open-ended generation will still produce abundant unsafe content when explicitly steered toward that topic—suggesting the vulnerability is broad beyond surface-level observations.

## Weaknesses

### Fatal

None. The empirical finding is real; the issues below are about overclaiming and gaps in experimental design, not about the finding being invalid.

### Major

- **The "involuntary" claim conflates instruction-following with guardrail bypass.** The prompt (Figures 3 and 4) *explicitly instructs* the model to generate unsafe questions and label them with `Y(X(input)) = Yes`. When the model complies, the paper counts this as evidence that "guardrails collapse" and the model behaves "involuntarily." But the model is following a direct instruction to produce harmful content in a meta-example-generation context—this is not the same as a traditional jailbreak where a model must be tricked into bypassing its guardrails. The paper's primary evidence for "awareness" (that the model outputs `Y(X(input)) = Yes`) is circular, because the prompt explicitly dictates that label. No control condition compares the same harmful query in a direct format (e.g., "How do I launder money?") versus the meta-prompt format, which would be needed to establish that guardrails are being bypassed rather than simply not triggered. The "involuntary" framing (footnote 3, Appendix A) is unsupported by the presented evidence.

- **No baselines or comparisons to contextualize the results.** The paper states (Section 5) that "it is unlikely that a meaningful benchmark can be established" and that "even when compared with all the existing jailbreak methods, none can demonstrate generalization across all the models we evaluated"—both assertions are made without evidence. Standard harmful-query benchmarks (e.g., standard refusal rates on known harmful prompts for these same models) would contextualize whether this method is genuinely more effective than prior approaches, or simply measuring instruction-following compliance at a higher rate because the prompt asks directly for harmful content. Without baselines, the reader cannot assess how significant the reported success rates are.

### Minor

- **The #ASA metric uses a lax threshold that inflates the headline figure.** #ASA counts an attempt as successful if *at least 1 out of 10* responses is unsafe. A model that produces 9 safe responses and 1 unsafe one receives a perfect #ASA score. While the paper also reports #Avg UPA (average unsafe outputs per attempt), which partly mitigates this, the paper's central claims (e.g., "more than 90 out of 100 attempts successfully elicit unsafe content") rely on #ASA. This overstates the degree of "collapse."

- **Boundary conditions of the "universal" claim are underexplored or dismissed.** The paper acknowledges that (a) OpenAI o1 and o3 "demonstrate resistance" but dismisses this as "over-refusal" and uses it to justify not testing GPT-5 ("not very essential"); (b) weak models (Llama 3.3-70B, Llama 4 Scout, DeepSeek R1-Distilled) fail to generate unsafe content, which the paper attributes to "weak instruction following." This last point is particularly informative: if the attack's success depends on strong instruction-following, the vulnerability is better characterized as a property of capable instruction-following models rather than a universal guardrail failure. These boundary conditions are at tension with the paper's "universal" framing.

- **Judge validity is asserted without quantitative evidence.** The paper states that Llama Guard-4's judgments "align closely with humans, as well as those of the GPT 4.1 model" (Section 3.1) but provides no agreement metrics (e.g., Cohen's kappa, accuracy on a held-out set). The paper also acknowledges that operator C produces outputs that "fall outside the judge corpus" (Section 3.3), raising questions about judge calibration on this specific output distribution.

- **No defense experiments are conducted despite speculative claims.** The paper asserts that "detecting and blocking this specific prompt at the input level appears to be straightforward" (Section 6) and discusses output-level filtering, but no defenses are tested under controlled conditions. For a vulnerability disclosure paper, evaluating at least one straightforward defense (e.g., input filtering, system-prompt hardening) would be the responsible minimum.

### Trivial

None.

## Nice-to-Haves

- A direct comparison of the same harmful query asked in standard direct format versus the meta-prompt format, with refusal rates, would cleanly separate the vulnerability from simple instruction-following.
- Reporting confidence intervals or variance across the 100 attempts would strengthen the quantitative claims.
- A brief investigation of why the meta-prompt succeeds (e.g., analysis of whether models' internal reasoning shows them flagging the content as unsafe while generating it anyway) would support or refute the "involuntary" framing.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **Alt-text confusion in Figure 5:** This describes a parser/formatting artifact (the alt-text mentions "LUPA" and "training samples" which are unrelated to the figure's actual content). Per instructions, formatting artifacts from PDF extraction are not author errors.
- **Missing reproducibility details (API versions, temperature):** Likely in the stripped appendix. Per instructions, nitpicks about hyperparameters and trivial implementation details are removed.
- **No statistical significance / confidence intervals:** 100 attempts per model is standard in red-teaming work. Reporting CIs would improve the paper but is not a weakness given community norms.
- **"Post-hoc speculation" about auxiliary operators:** The paper states the operator rationale as a design intention (Section 2.1), which is standard for methodology sections. The reviewer's characterization is too strong.
- **Related work not engaging with superficial alignment:** The paper explicitly discusses superficial alignment (Qi et al., 2025) in Section 4. This criticism is factually incorrect.
- **Operator B ablation suggesting verbosity-driven results:** This is the reviewer's interpretive inference, not a weakness of the paper's experimental design.
- **Missing/incomplete "involuntary" justification:** Merged into the first Major weakness above; not a separate point.

## Novel Insights

The input review's most incisive observation is that the paper's experimental design cannot distinguish between guardrail bypass and simple instruction-following in a permissive meta-context, because the prompt explicitly asks for the behavior it then measures as "attack success." This is a subtle but important confound that applies broadly to meta-prompt or "example generation" style jailbreak evaluations: when the prompt itself instructs the model to produce harmful content and provide a "Yes" label, the resulting compliance is fundamentally different from a model that recognizes and overrides its own refusal mechanism. This insight has implications beyond this paper—it suggests that meta-instruction vulnerabilities should be evaluated with controls that separate task compliance from guardrail circumvention.

## Suggestions

1. **Reframe the contribution** to match the evidence: present this as a novel *meta-instruction vulnerability* rather than "involuntary jailbreak" or "guardrail collapse." The term "involuntary" implies a contradiction the paper does not demonstrate.
2. **Add a control experiment** comparing direct harmful queries vs. the meta-prompt format on the same set of harmful intents, reporting refusal rates for both conditions. This is the single highest-leverage addition.
3. **Include baselines** showing standard refusal rates on a harmful-query benchmark for the same models, to contextualize the reported success rates.
4. **Report #Avg UPA alongside #ASA in the abstract and headline claims**, or use a metric that does not collapse to near-ceiling when 1/10 responses is unsafe.
5. **Acknowledge boundary conditions honestly**: o1/o3 resistance, weak model failure, and the dependence on strong instruction-following are meaningful constraints on the claimed "universality."

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>