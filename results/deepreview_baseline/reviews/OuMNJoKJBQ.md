## Summary

This paper investigates why current LLM alignment techniques remain vulnerable to jailbreak attacks. Through causal intervention experiments (deactivating reasoning-critical neurons), the authors provide empirical evidence that existing alignment relies on shallow refusal heuristics rather than deep reasoning. To address this, they construct and release a Chain-of-Thought (CoT) safety fine-tuning dataset, and propose Alignment-Weighted DPO (AW-DPO), which decomposes responses into reasoning and final-answer segments and assigns separate preference weights to each for more targeted optimization. Experiments across multiple models and jailbreak benchmarks show improved safety while maintaining utility.

## Strengths

- **Empirical causal analysis of alignment superficiality**: The causal intervention experiment (deactivating top reasoning-critical attention heads and showing alignment performance unaffected while reasoning degrades) provides a clean and compelling demonstration that current safety mechanisms are largely independent of deep reasoning. This is a valuable diagnostic contribution that goes beyond observational correlation studies.

- **Well-motivated and principled method**: AW-DPO is directly motivated by a concrete error analysis (15% of failures involve reasoning-response mismatch), and the decomposition into reasoning and response segments with separate weights is a natural, principled extension of DPO. The method addresses a genuine limitation of standard DPO, which treats the entire output uniformly.

- **Extensive and rigorous evaluation**: The paper evaluates across four model families (LLaMA-2, LLaMA-3.2, LLaMA-3.1, Mistral), 20 jailbreak attack types across five categories, and multiple strong baselines including SAFECHAIN, RR, and STAIR. The transferability experiments (Table 3) and ablation studies (Tables 4, 5) add thoroughness.

- **Release of a CoT safety dataset**: The paper constructs and plans to release a long-form CoT dataset combining safety-critical and utility-oriented prompts with reasoning traces. This is a practical contribution that will benefit the community.

## Weaknesses

### Fatal
None.

### Major

1. **The causal intervention experiment's interpretation may be overclaimed**: Deactivating the top 10% of attention heads with highest probing accuracy on a reasoning task does not necessarily isolate "reasoning-critical" neurons in a causal sense. Probing accuracy measures linear separability of representations, not causal necessity for reasoning. The observed result could also be explained by alignment being an easier task that requires fewer or different computational resources, rather than alignment being "superficial" in the sense of lacking reasoning. The paper would benefit from additional causal analyses (e.g., intervening on alignment-specific neurons and checking reasoning performance) to strengthen the claim.

2. **The 15% failure case quantification is not sufficiently rigorous**: The paper states that "approximately 15% of all failure cases" are due to reasoning-response mismatch (correct reasoning + unsafe answer, or incorrect reasoning + safe answer), but the methodology for determining "correct" vs "incorrect" reasoning is not described. How is reasoning correctness judged? Is it automated or human-annotated? Without a clear protocol, the reliability of this key motivating figure is unclear. This is important because AW-DPO is specifically designed to address these 15% of cases.

3. **Dependence on a judge model for harmfulness scoring is a practical concern**: AW-DPO requires an LLM judge to assign harmfulness scores to reasoning traces and response segments separately. The paper does not discuss the reliability, calibration, or potential biases of this judge model. If the judge model itself has alignment weaknesses, the preference pairs and weights could be noisy or misaligned. An analysis of judge model agreement or a comparison with human judgments would strengthen the method's credibility.

4. **Limited comparison with reasoning models**: The comparison with Phi-4-Reasoning and Phi-4-Reasoning-Plus (Figure 3) is used to argue that "merely improving general reasoning ability is insufficient." However, these models may not have undergone any safety alignment at all, making the comparison unfair. A more controlled experiment (e.g., taking a base model, fine-tuning it on general reasoning CoT data, and then evaluating safety) would better isolate the effect of reasoning on alignment.

### Minor

- The notation in Equation (3) defines \(w_{s_t} \in \{0,1\}\) as a mask, but the actual weights used in Equation (4) are continuous values derived from harmfulness score differences. This inconsistency in notation could confuse readers.
- The utility evaluation relies solely on MMLU accuracy, which measures factual knowledge rather than general instruction-following or helpfulness. Additional utility benchmarks (e.g., MT-Bench, AlpacaEval) would provide a more complete picture.
- The paper uses "respond" and "response" interchangeably in variable names (e.g., \(w_{\text{respond}}\) vs \(w_{\text{response}}\)), which is a minor clarity issue.

### Trivial
- Table 2 contains a typo: "SAFERACH" should be "SAFECHAIN".

## Nice-to-Haves

- An analysis of how often the judge model's harmfulness scores for reasoning traces agree with human judgments, or a calibration study.
- A more detailed breakdown of the 15% failure cases, including examples and inter-annotator agreement if human evaluation was used.
- Evaluation on additional utility benchmarks beyond MMLU to better assess the utility-safety trade-off.

## Novel Insights

Beyond the paper's own contributions, the key insight is that alignment and reasoning can be causally dissociated in current LLMs: models can maintain refusal behavior even when their reasoning capabilities are severely impaired. This suggests that safety alignment may be encoded in a separate, potentially more brittle, set of mechanisms than general reasoning. The AW-DPO method then provides a way to explicitly bridge this gap by training the model to produce reasoning that is consistent with safe outcomes, rather than treating reasoning and response as a monolithic output.

## Suggestions

- Provide a clear protocol for how reasoning correctness was judged in the error analysis (e.g., human annotation guidelines, automated criteria, or both) and report inter-annotator agreement if applicable.
- Include an analysis of the judge model's reliability for scoring reasoning traces, such as agreement with human raters or consistency across different judge models.
- Consider a more controlled experiment to test the effect of reasoning on alignment: take a base model, fine-tune it on general reasoning CoT data (without safety content), and evaluate safety performance. This would strengthen the claim that general reasoning alone is insufficient.
- Clarify the notation in Equation (3) to match the actual continuous weights used in practice.

## Score and Decision

The paper makes a solid contribution with a well-motivated method, extensive experiments, and a valuable dataset release. The causal intervention analysis, while not fully rigorous, provides an interesting diagnostic perspective. The weaknesses are not fatal but do temper the strength of some claims. Overall, the paper is above the ICLR acceptance threshold.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>