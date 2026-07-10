Now I have all the information I need. Let me produce the final consolidated review.

---

## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight, plug-in intervention for mitigating language confusion (unintended language mixing) in multilingual LLMs. The method uses norm-adjusted self-distillation — training a small two-layer MLP on the frozen model's own debiased logits to predict which language families are permissible at each generation step, then masking inappropriate tokens. Across 5 base models and two generation paradigms, LCG reduces confusion by roughly an order of magnitude (e.g., CJ confusion from 4.5%→0.1% on Qwen3-8B) with negligible overhead (~0.4% wall-clock time), while attempting to preserve legitimate code-switching.

## Strengths

- **Norm-adjusted self-distillation is a novel, well-motivated training method grounded in a genuine mechanistic observation about token embedding norm bias.** The ablation (Table 3) directly validates its contribution, showing LCG-adjusted consistently outperforms LCG-unadjusted.
- **The method is practically attractive:** a two-layer MLP that intervenes on ~0.38% of tokens with 0.4% wall-clock overhead and no modification to the base model, making it deployable in production.
- **Evaluation is appropriately broad:** 5 base models (Qwen3-8B/30B, Llama3.1-8B, Gemma3-12B, GPT-OSS), two paradigms (standard generation and reasoning/thinking), and multiple datasets (FLORES+, INCLUDE, Humaneval-XL) with consistent confusion reductions across settings.
- **The paper devotes serious experimental effort to distinguishing harmful confusion from legitimate code-switching** (FLORES-WITH-LATIN analysis, token-level preservation experiment, human annotation), which is the hardest part of the problem and where rule-based approaches fail.

## Weaknesses

### Fatal
None.

### Major

1. **ORPO baseline comparison lacks sufficient methodological detail to assess fairness.** The paper reports that ORPO degrades INCLUDE accuracy (61.4→57.3 for Qwen3-8B; 46.1→43.2 for Llama3.1-8B) and concludes this is a limitation of training-based methods, but does not specify training data size, hyperparameters, number of epochs, learning rate, or whether hyperparameters were tuned. Without these details, the comparison cannot distinguish between ORPO inherently degrading performance and the ORPO baseline being undertuned, weakening the claim that LCG outperforms training-based methods.

2. **The code-switch preservation claim (86.7% preservation of human-validated code-switch points) is central to the paper's argument that LCG preserves legitimate multilingual behavior, but the human annotation methodology is underspecified.** The paper states that outputs were "judged by human annotators to be natural, appropriate code-switch" without reporting: number of annotators, annotation instructions, inter-annotator agreement, number of examples annotated, or how disagreements were resolved. This makes the 86.7% figure difficult to evaluate as evidence.

### Minor

1. **The FLORES-NO-LATIN Latin confusion metric may overcount confusion** by treating all Latin characters in model output as errors, even when legitimate preservation of proper nouns or technical terms (e.g., Python, iPhone, ReLU) could produce them. The paper acknowledges this challenge (Section 3.3) and uses the FLORES-WITH-LATIN/NO-LATIN split, but the NO-LATIN subset can still contain cases where Latin script is legitimate but absent from the reference. The CJ results (where the metric is clean) carry the paper, but the Latin-specific reductions are less interpretable than presented.

2. **Table 4's caption reads "Effectiveness of LCG Intervention on 'No-Think' Models measured on Humaneval-XL"** but the content (reasoning length, Pass@1, Pass@10) and surrounding text describe the thinking/reasoning model experiment. This is an editing error that should be corrected.

3. **The confusion point analysis (Section 3.1)** — the finding that language-consistent tokens appear within top-3 99.29% of the time — is performed only on Qwen3-8B. Replicating on at least one additional model would strengthen this foundational claim.

4. **Training hyperparameters for the gate** (learning rate, batch size, optimizer, number of epochs) are not reported, making the method harder to reproduce.

### Trivial
None.

## Nice-to-Haves

- Reporting confidence intervals (via bootstrap) for the very low confusion rates (0.1%, 0.0%) would strengthen the statistical claims.
- A more controlled evaluation of code-switch preservation (e.g., constructing test cases where legitimate code-switching is unambiguously required, such as sentences that must contain proper nouns from a different script) would complement the current human annotation experiment.

## Removed Points

These points from the input review were removed with justification:

- **Statistical significance / variance not reported** — removed because single-run evaluation on large benchmarks is standard practice in this field; requesting confidence intervals for very low rates is a nice-to-have, not a genuine weakness.
- **GPT-OSS-20B not described** — removed per hard rules: cited entities are assumed to exist and be identifiable as referenced. The paper attributes it to (OpenAI, 2025), which is sufficient.
- **"Not much lower" characterization (Section 5.3)** — the reviewer's comment that 25.90% vs 38.36% is a 32% relative reduction is valid but is an interpretation of existing data, not a new weakness; the paper already presents the raw numbers.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide full annotation methodology for the code-switch preservation experiment (annotator count, instructions, inter-annotator agreement, example count, disagreement resolution).
2. Report ORPO hyperparameters, training data size, and tuning procedure to establish a fair comparison.
3. Replicate the confusion point analysis (99.29% top-3 finding) on at least one additional model.
4. Disclose gate training hyperparameters (learning rate, batch size, optimizer, epochs) for reproducibility.
5. Correct the Table 4 caption to read "Thinking Models" instead of "No-Think Models."

---

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>