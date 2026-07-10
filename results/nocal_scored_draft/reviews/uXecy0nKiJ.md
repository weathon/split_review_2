Now let me produce the final review.

## Summary

This paper investigates whether activation steering — a technique for controlling LLM behavior by adding vectors to hidden states during inference — can inadvertently compromise safety mechanisms even when the steering vectors are benign (random directions or interpretable SAE features). Through experiments across multiple model families (Llama-3, Qwen2.5, Falcon-3) using the JailbreakBench dataset, the paper shows that random steering produces non-zero compliance rates (up to 17% overall) and that SAE feature steering shows comparable effects. The paper also constructs a universal attack by averaging random vectors that jailbreak a single prompt, achieving up to a 4× average increase in compliance rate on unseen prompts.

## Strengths

- **Well-motivated and timely research question:** The paper identifies a genuine gap — whether benign steering vectors (used for legitimate, interpretable model control) can inadvertently compromise safety, which was underexplored relative to adversarial jailbreak vectors. [favorability: 1.00]
- **The random steering baseline is a clean methodological choice:** Using random directions as a control (Sec 3.2, line 75) cleanly separates the effect of "any perturbation" from "semantically meaningful perturbation," allowing the paper to quantify how much extra risk comes from interpretable steering vs. noise. [favorability: 1.00]
- **The universal attack construction (Sec 4.4) is genuinely novel:** Averaging random jailbreak vectors that succeed on a single prompt to produce a generalizable attack that requires no model weights or gradients is a non-obvious finding with practical security implications. [favorability: 1.00]
- **The Goodfire API case study (Sec 4.3) grounds the findings in practice:** Demonstrating that a public API deployed for safe, interpretable tuning can be used to jailbreak a production model via a semantically benign "brand identity" feature makes the paper's concerns concrete. [favorability: 0.96]

## Weaknesses

### Fatal
None.

### Major

- **The SAE vs. random comparison in the full-dataset evaluation (Fig 3) is confounded and uninterpretable.** SAE features are evaluated on Llama3.1-8B at the 2/3 depth layer, while random vectors are evaluated on Llama3-8B and Qwen2.5-7B at the 1/3 depth layer. The paper itself shows (Fig 2b) that steering effectiveness varies substantially by layer. The observed differences (e.g., SAE at 11% overall vs. random at 17%) could reflect layer choice, model differences (Llama3.1 vs. Llama3), or steering type — these factors cannot be disentangled. The single-prompt comparison (Fig 2c) is cleaner because it holds model and layer fixed, but the full-dataset version that drives Fig 3 and its discussion is not interpretable. [favorability: 0.06]

### Minor

- **The headline "2–27%" range in the abstract and introduction uses category-specific extremes** (the 27% is the maximum for two specific categories in one model) rather than overall rates (17% for Llama3-8B, 11% for Qwen2.5-7B). This could mislead readers about the expected magnitude of the effect. [favorability: 0.38]

- **The universal attack framing overstates what is achieved.** Describing it as "zero-shot" (line 239) understates the requirements: a specific harmful prompt, an automated judge, and 100–500 steering trials per model. Moreover, the "4× increase" headline masks that for several models the improvement is negligible (Qwen2.5-32B: 9%→9%; Falcon-H1-34B: 11%→18%). The paper acknowledges this variability but the headline framing does not reflect it. [favorability: 0.02–0.46]

- **No variance, confidence intervals, or error bars are reported for any experiment**, despite using 1,000 samples per condition. This makes it difficult to assess whether observed differences between models, layers, or steering types are meaningful relative to noise. [favorability: 0.17]

- **The LLM-as-judge protocol has a potential confound:** Incoherent, repetitive, or nonsensical responses are always classified as SAFE (Sec 3.4, line 96). Since strong steering can produce incoherent outputs, this could systematically deflate compliance rates at high coefficients — potentially contributing to the non-monotonic relationship noted in Sec 4.1. The paper references human annotation validation in the appendix but does not present this evidence in the main paper. [favorability: 0.26]

- **The claim that "SAE-based steering proves even more dangerous" (conclusion, line 249) is weakly supported.** It rests primarily on a 2–4% absolute increase over random in the single-prompt experiment (Fig 2c) on one model at one layer, with no reported variance. The full-dataset comparison (Fig 3) actually shows SAE at 11% overall vs. random at 17% on Llama3-8B. The evidence for this claim is thinner than the confident framing suggests. [favorability: 0.00]

- **The "poor generalization" framing of the cross-category analysis (Fig 4b) understates the generalization that the data actually shows:** conditioning on a feature jailbreaking one category, the conditional probability of it jailbreaking another is often 20–40%, which is meaningfully above baseline. This suggests some features do partially generalize, which the paper's narrative downplays. [favorability: 0.58]

### Trivial
None.

## Nice-to-Haves

- Adding random steering baselines on Llama3.1-8B at the same layer (2/3 depth) where SAE features are tested would enable a clean SAE-vs-random comparison at scale.
- Presenting the judge validation against human annotations in the main paper (not just the appendix) would increase confidence in the evaluation metric.
- A second prompt in the single-prompt probe (Sec 4.1) would help assess how much the results depend on the specific bomb-making prompt.

## Removed Points

These points were raised in the input review but are removed with justification:

- *"SAE analysis confined to one model/SAE"*: The paper explicitly acknowledges this limitation (Sec 3.3, line 82) and justifies it. Scope limitation, not a flaw.
- *"Fixed seed (42) means results are seed-dependent"*: Standard reproducibility practice; applies to all empirical ML research.
- *"Case study is anecdotal"*: It is explicitly labeled a "case study" intended to illustrate the mechanism, not to provide statistical evidence.
- *"Steering applied to prompt vs. generation tokens is consequential but not discussed"*: The paper follows prior work (Durmus et al., 2024) and is transparent about the choice; the reviewer's alternative-failure-mode concern is speculative.
- *Various section-by-section observations* that are stylistic opinions or suggestions rather than verifiable weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Unconfound the Fig 3 comparison:** Test random steering vectors on Llama3.1-8B at the 2/3 depth layer — the same model and layer used for SAE features — to enable a clean SAE-vs-random comparison at full-dataset scale.
2. **Add variance reporting:** Report standard deviations, percentiles, or confidence intervals for all averaged results (Figs 2, 3, 6). With 1,000 samples per condition this is straightforward.
3. **Recalibrate headline claims:** Use overall compliance rates in the abstract (e.g., "up to 17%") rather than category-specific extremes. Describe the universal attack's practical requirements transparently.
4. **Support or soften the "even more dangerous" claim:** Either provide matched random baselines at the same layer and with variance to support this claim, or reframe it as "comparable" rather than "more dangerous."
5. **Present judge validation in the main paper:** Show the agreement rate with human annotations and address the confound between coherence and safety judgments.

## Score and Decision

The paper addresses a genuinely important and underexplored question, and its core empirical finding — that even random steering vectors systematically produce non-zero jailbreak rates — is well-supported across multiple models. The universal attack construction is a novel contribution with security implications. However, the paper's strongest quantitative comparison (SAE vs. random at full-dataset scale) is confounded by different models and layers, several headline claims are overstated relative to the evidence, and the lack of variance reporting limits confidence in observed differences. These are fixable issues, but they are substantive enough that the paper's contribution cannot be fully assessed in its current form.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>