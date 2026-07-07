## Summary

The paper proposes detecting instruction fine-tuning attacks on LLMs using influence functions combined with a "semantic transformation" diagnostic. The core idea is that poisoned examples (those associating a trigger phrase with wrong labels) will retain high, same-sign influence scores before and after a sentiment inversion, while clean examples will flip sign. Experiments are conducted on a sentiment classification task (T5-small) and a math reasoning task (deepseek-coder-1.3b), showing that removing the detected "critical poisons" (~1% of data) recovers model performance.

## Strengths

- **Practical motivation with a knowledge-free framing:** The paper addresses a realistic threat model where the defender has no prior knowledge of triggers or attack strategy. The observation that influence scores under semantic transformation can discriminate poisons from clean data is a genuinely interesting diagnostic idea.
- **Demonstrated performance recovery:** In Figure 5 and the GSM8K results (Table 3, target output rate drops to 0 after removal), the paper shows tangible evidence that removing the flagged examples restores model behavior, which is the practical outcome that matters.
- **Computational feasibility:** Leveraging EK-FAC (Kronfluence) to make influence computation tractable on 50k examples within 2 hours on a single A100 is a useful engineering detail.

## Weaknesses

### Fatal

- **Critically low true positive rate contradicts the core claim of reliable detection.** Out of 653 flagged "critical poisons" in the sentiment classification experiment, only 23 are actual poisons—a true positive rate of 3.5%. This means ~96.5% of removed examples are clean data. Removing ~630 innocent training examples is not a principled defense; it is an indiscriminate cull that happens to also remove a handful of the 1,000 real poisons. The paper never discusses the false positive rate, which fundamentally undermines the claimed contribution.

- **The attack effectiveness itself is marginal.** In Table 1, the overall positive classification ratio is 62.12% (clean) vs. 64.36% (poisoned), a difference of ~2.2 percentage points. On most individual tasks the poisoned and clean numbers are identical or differ by less than 1%. A defense against an attack that barely works is difficult to interpret as meaningful validation.

### Major

- **No ablation of the transformation component's contribution.** The paper never compares against simply removing the top-K highest-influence examples without the transformation. Without this baseline, it is impossible to determine whether the sentiment transformation is adding anything over plain influence-based removal.
- **The method's scope is narrowly tied to sentiment.** For GSM8K, the "semantic inversion" is "What is the opposite of [question]?"—a heuristic that the paper itself notes "does not invert the influence score distribution" and causes only a "small, random shift." This casts doubt on whether the method generalizes beyond tasks with clear polarity.
- **Experimental scale is insufficient for an ICLR paper.** T5-small (60M parameters) and deepseek-coder-1.3b are not representative modern LLMs. The paper's contribution claims generalization to "recent LLMs" but neither model qualifies as such; both are orders of magnitude smaller than deployed LLMs.
- **Section 3.6 ablation is incomplete and inconclusive.** The paper acknowledges that certain prefix choices ("Do NOT calculate") do not invert the distribution, only shift it randomly. This suggests the method is brittle to the choice of transformation with no principled criterion for selecting a good one.

### Minor

- The math reasoning experiment's TPR degrades quickly: 60% for top-10, dropping to 15% for top-100. Since 100 examples must be removed to neutralize the attack, the actual true positives retrieved are only ~15. No analysis justifies why 100 examples is the right removal threshold.
- Table 2 reports identical accuracy (56.52%) for pretrained, clean, poisoned, and post-removal—all four conditions—which means there is no measurable performance degradation in the first place on the tracked accuracy metric. This undermines the narrative around sentiment classification.

### Trivial

- The paper uses "future work" as a primary section rather than integrating it, suggesting the work is incomplete.

## Nice-to-Haves

- A precision-recall curve or F1 score as the primary evaluation metric instead of reporting only the true positive ratio.
- Experiments on a stronger attack with higher poison ratio or more capable trigger phrases to stress-test the method.
- Comparison with leave-one-out retrain or direct high-influence-score removal as an ablation baseline.

## Novel Insights

The core insight—that poisoned examples with trigger-label associations should be semantically invariant under polarity inversion while clean examples should flip—is a conceptually interesting diagnostic. However, the experimental evidence does not convincingly validate this intuition: the 3.5% TPR suggests the criterion does not cleanly separate poisons from clean data in practice, and the math reasoning case shows the inversion does not work as expected outside sentiment domains.

## Suggestions

- Report precision and recall jointly; acknowledge the high false positive rate and discuss its implications for usability.
- Include a baseline of plain influence-based removal (top-K by raw influence score without transformation) to isolate the value of the transformation step.
- Conduct experiments on a more substantial LLM (e.g., 7B-scale) and a more clearly effective attack (higher ASR) before claiming generalization.

## Score and Decision

The paper addresses a real and important problem and contains a creative central idea. However, the core experimental results undermine the claimed contribution: the detection precision is very low (3.5%), the attack success being defended against is marginal, the models are not representative of modern LLMs, and the method's generality beyond sentiment tasks is unsupported. The work appears to be early-stage and not yet ready for publication at ICLR.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>