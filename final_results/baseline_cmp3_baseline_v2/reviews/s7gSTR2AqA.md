## Summary

This paper investigates whether LLMs can develop human-aligned semantic categories that follow the Information Bottleneck (IB) principle, focusing on color categorization. The authors conduct two main experiments: (1) an English color naming task across 39 models, finding that larger instruction-tuned models achieve the best alignment and IB efficiency, and (2) an iterated in-context language learning (IICLL) paradigm simulating cultural evolution, which reveals that LLMs restructure random category systems toward greater IB efficiency and human-alignment over generations. Only Gemini 2.0 recapitulates the full range of near-optimal IB tradeoffs observed in human languages, while other state-of-the-art models converge to low-complexity solutions.

## Strengths

- **Novel synthesis of theoretical frameworks** – The paper productively combines the Information Bottleneck principle and iterated language learning, both well-established in cognitive science, to study semantic categorization in LLMs. This theory-driven approach is a valuable methodological contribution.
- **Comprehensive empirical scope** – The evaluation of 39 models across 6 families (varying size, instruction-tuning, modality) provides a rich and informative picture of how model properties affect color naming behavior, revealing non-trivial failures even in strong models.
- **IICLL as a methodological innovation** – The adaptation of iterated in-context learning to replicate human iterated language learning experiments is elegant and opens a new avenue for probing inductive biases in LLMs in a controlled way.
- **Clear and compelling results** – The key finding that LLMs evolve IB-efficient systems without being trained for that objective, and that only the most capable model matches the human range, is robustly supported and well-visualized (Figures 2-4).

## Weaknesses

### Major

- **Overclaimed "inductive bias" interpretation** – The paper argues that LLMs exhibit a "human-like inductive bias toward IB-efficiency." However, IICLL relies on in-context learning from a small set of examples; the resulting convergence could reflect statistical patterns implicitly encoded during training (e.g., human language data already favors IB-efficient splits) rather than an independent bias. The term "inductive bias" is stronger than what the evidence supports, and the text sometimes conflates emergent behavior with innate preference.
- **Generality limited by reliance on a single model** – Only Gemini 2.0 reproduces the full human range of IB tradeoffs. The other three strong models converge to low-complexity solutions, and the paper acknowledges smaller models fail. This raises questions about whether the claimed capacity to evolve human-like categories is a general LLM property or a feature of frontier models with exceptional in-context learning. The title and abstract understate this limitation.
- **Shepard circles analysis is preliminary and not tied to IB** – The brief experiment on a non-color domain lacks quantitative IB evaluation, making the claim that results "may generalize beyond color" unsupported. This section feels like a sketch rather than a contribution.

### Minor

- **Inconsistent presentation of human IL data** – Figure 3 shows only final-generation human IL points, while LLM trajectories show intermediate generations. The human data are not directly comparable in dynamics, which slightly weakens the visual comparison.
- **Lack of formal statistical testing** – The improvement over IICLL generations (Figure 4) is shown with confidence intervals but no formal hypothesis tests (e.g., permutation tests against null models) to confirm that convergence is significant relative to random drift or rotation baselines.

### Trivial

None.

## Nice-to-Haves

- Add formal statistical comparisons (e.g., Bayesian mixed-effects models or permutation tests) for the IICLL convergence trajectories.
- Extend the Shepard circles analysis with IB evaluation, even if only for a few conditions, to strengthen the domain-generality claim.
- Discuss more explicitly how instruction-tuning might instill an efficiency bias (e.g., via RLHF pressure for concise/accurate responses).

## Novel Insights

The paper demonstrates that a drive toward optimal compression (IB-efficiency) can emerge in LLMs purely through iterated in-context language learning, without explicit optimization of that objective. This suggests that IB-efficiency may be a deep structural property of intelligent systems that process structured data, rather than a learned consequence of training objectives. The finding that many LLMs fail at simple color naming—despite massive English training data—is also surprising and underscores that distributional statistics alone do not guarantee human-like grounding.

## Suggestions

- Reframe "inductive bias" to "emergent tendency" or "behavioral bias revealed through IICLL" to more accurately reflect what the experiments show.
- Include a statistical comparison of IICLL convergence against a baseline that simply replicates the initial random system or a rotation-perturbed system, to quantify the strength of the bias.
- Clarify in the abstract that only the strongest model examined (Gemini 2.0) fully replicates human IB tradeoffs, and note the others converge to low-complexity solutions.

## Score and Decision

Score: 8

Decision: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>