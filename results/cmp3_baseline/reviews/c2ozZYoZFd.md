## Summary

This paper presents a detailed case study of "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024), an ICLR 2025 Oral paper, and argues that the original paper's four lines of evidence (human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims) do not support its central claims about min-p sampling's superiority. Through re-analysis of the original data and extensive new experiments, the authors demonstrate that min-p does not consistently outperform existing sampling methods when proper statistical methods are applied and hyperparameter tuning is controlled for. The paper derives general lessons for more rigorous empirical ML research from this case study.

## Strengths

- **Important and timely contribution to research integrity**: The paper addresses a genuine crisis of rigor in empirical ML research, and the case study approach makes the abstract problem concrete and actionable. The detailed documentation of specific errors (omitted data, incorrect statistical tests, selective reporting, unsubstantiated claims) provides a valuable teaching resource for the community.

- **Methodological contribution for fair comparison**: The "Best-of-N" analysis controlling for hyperparameter volume is a novel and practical methodology that addresses a widespread but under-discussed source of unfair comparisons in ML research. This is a genuine methodological contribution that could be adopted by other researchers.

- **Thorough and reproducible re-analysis**: The paper conducts extensive re-analyses (6000 A100-hours of compute) across multiple models, temperatures, and hyperparameters, and makes all data and code publicly available. The level of detail in documenting the original paper's errors is commendable.

- **Clear and actionable general lessons**: The six lessons distilled from the case study (controlling for hyperparameter volume, proper statistical testing, data transparency, scrutinizing qualitative claims, methodological clarity, avoiding selective reporting) are concrete, well-motivated, and directly applicable to improving research practices across the field.

## Weaknesses

### Fatal
None.

### Major
- **The paper's central contribution is a critique of another paper, not a novel scientific contribution to ML.** While the case study is thorough and the general lessons are valuable, the paper is fundamentally a negative result about someone else's work. The "blueprint" lessons are not novel in themselves—they are well-known best practices that have been articulated many times before (e.g., the need for multiple comparison correction, data transparency, controlling for hyperparameter tuning). The paper's primary novelty is the detailed documentation of errors in a specific high-profile paper, which is more of a commentary or meta-scientific contribution than a research contribution to machine learning. The paper would be more appropriate for a venue focused on reproducibility or meta-science.

- **The paper's own analyses have limitations that are not fully acknowledged.** The "Best-of-N" analysis for controlling hyperparameter volume is clever, but it has its own biases: it assumes that all hyperparameter values are equally likely to be tried in practice, and it does not account for the fact that some hyperparameters are more "natural" or commonly used than others. The paper also only evaluates on GSM8K CoT, which is a single benchmark with a specific format; the claim that min-p does not outperform other samplers is based on limited evidence. The authors acknowledge this as a limitation but do not discuss how it might affect the generalizability of their conclusions.

- **The paper's tone and framing may be perceived as overly adversarial.** While the detailed critique is warranted given the severity of the errors, the paper reads more like a rebuttal or exposé than a constructive scientific contribution. Phrases like "the paper's own evidence invalidates its central claim" and the extensive documentation of errors could be seen as attacking the original authors rather than focusing on the scientific lessons. This tone may reduce the paper's persuasiveness and impact within the community.

### Minor
- **The paper does not fully explore the possibility that min-p might be useful in specific settings or for specific use cases.** The conclusion that "min-p offers no apparent advantage" is based on aggregate analyses; it is possible that min-p has advantages for certain model sizes, certain temperatures, or certain types of prompts that are not captured by the aggregate statistics. The paper could have explored this more carefully.

- **The "Best-of-N" analysis, while clever, has its own limitations that are not fully discussed.** The analysis assumes that the maximum performance over a random subset of hyperparameters is a fair measure of a method's potential. However, in practice, researchers do not select hyperparameters uniformly at random; they use prior knowledge, heuristics, or grid search. The analysis also does not account for the fact that some hyperparameters are more "natural" or commonly used than others (e.g., top-p=0.9 is more standard than top-p=0.7).

### Trivial
None.

## Nice-to-Haves
- The paper could have included a more systematic analysis of the original paper's review process, e.g., by analyzing the reviewer comments and the AC decision in light of the identified errors. This would strengthen the argument about systemic issues in peer review.
- The paper could have proposed concrete guidelines or a checklist for reviewers to use when evaluating papers that make similar claims, which would increase the practical utility of the "blueprint."

## Novel Insights

The paper's most novel insight is the "Best-of-N" methodology for controlling for hyperparameter volume when comparing methods that require different amounts of tuning. This is a practical and principled approach to detecting potential cherry-picking or unfair comparisons, and it could be widely adopted. The paper also provides a compelling demonstration of how multiple small methodological errors (omitted data, incorrect statistical tests, selective reporting, unsubstantiated claims) can compound to produce a paper that appears convincing but is actually unsupported by its own evidence. This serves as a powerful cautionary tale for the community.

## Suggestions
- Consider reframing the paper as a meta-scientific contribution about improving research practices, with the min-p case study as a detailed example, rather than as a critique of a specific paper. This would make the contribution more constructive and less adversarial.
- Add a section discussing the limitations of the "Best-of-N" analysis more thoroughly, including potential biases and when it might not be appropriate.
- Consider adding a practical checklist or set of guidelines for reviewers and researchers based on the six lessons, to increase the paper's practical utility.

## Score and Decision

**Score: 6** — This is a borderline accept. The paper is thorough, well-executed, and addresses an important topic (research rigor). The "Best-of-N" methodology for controlling hyperparameter volume is a genuine methodological contribution. However, the paper's primary contribution is a critique of another paper, and the general lessons, while well-articulated, are not novel. The paper would be a strong contribution to a meta-science or reproducibility venue, but its value to ICLR as a core ML venue is more limited. The paper is well-written and the analyses are sound, but the contribution is more about improving research practices than advancing ML methods or theory.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>