## Summary

This paper introduces a systematic deletion framework to probe whether LLMs genuinely depend on their chain-of-thought (CoT) reasoning traces in physics problem solving. By intercepting CoT mid-generation, deleting tokens under various strategies (end, random, physics-aware), and measuring downstream effects on accuracy, answer length, and information overlap, the authors find that models remain accurate under heavy deletions (40-60%) by "cramming" reconstructed steps into final answers. The work reveals that current accuracy-based evaluations are insufficient for scientific domains and argues for evaluation methods that assess reasoning faithfulness.

## Strengths

- **Novel methodological contribution**: The deletion-based probing framework is a creative and principled approach to studying CoT dependence. Intercepting the scratchpad mid-generation and systematically removing tokens provides a controlled experimental paradigm that goes beyond standard accuracy comparisons.

- **Well-motivated domain choice**: Physics is an excellent testbed for studying CoT faithfulness because it requires precise manipulation of equations, units, and structured terminology, making both the reasoning traces and their potential reconstruction quantifiable. The connection to AI-for-Science is timely and important.

- **Comprehensive experimental design**: The paper evaluates three different deletion strategies (end, random, physics-aware) across three models and three datasets, providing a thorough characterization of the phenomenon. The use of multiple metrics (accuracy, answer length, Jaccard similarity, Manhattan distance) captures different aspects of the behavior.

- **Clear identification of "cramming" behavior**: The observation that models produce longer final answers when CoT is deleted, attempting to reconstruct missing reasoning, is a genuine empirical finding that is well-documented across multiple conditions.

## Weaknesses

### Fatal
None.

### Major

- **The core claim about "faithfulness" is not directly tested**: The paper argues that CoT traces are not "faithful" because models can reconstruct missing information, but this conflates two distinct concepts: (1) whether the CoT is necessary for the final answer, and (2) whether the CoT accurately reflects the model's internal computations. The deletion experiments primarily test (1), not (2). A model could genuinely use CoT for most computations but still be able to reconstruct some steps from internal knowledge when CoT is deleted—this doesn't demonstrate unfaithfulness. The paper's title and framing imply a stronger claim about necessity than the experiments actually support.

- **The "cramming" interpretation is speculative without mechanistic analysis**: The paper attributes increased answer length to "cramming" (reconstructing missing reasoning), but this is an inference from output length alone. Without analyzing the content of the longer answers (e.g., whether they actually contain correct physics reasoning or just verbose filler), the claim remains weakly supported. The information overlap analysis partially addresses this, but the metrics used (bag-of-words Jaccard and Manhattan distance) are too coarse to distinguish genuine physics reasoning reconstruction from superficial token reuse.

- **Limited model and dataset scope relative to claims**: The paper evaluates only three models (all open-source, all relatively recent) and three physics datasets. The claims about "LLMs" broadly and implications for "AI-for-Science" are much broader than what the evidence supports. The paper acknowledges this as a limitation but then proceeds to make sweeping claims in the abstract and conclusion that go beyond what the data can justify.

- **The evaluation metric (Claude-4 Sonnet as judge) is itself an LLM-based evaluation**: Using one LLM to judge another LLM's physics solutions introduces potential confounders. The paper does not validate this judge against human expert evaluation or provide evidence of its reliability for physics-specific scoring. Given that the paper's core argument is about the unreliability of LLM reasoning, using an LLM as the primary evaluator is methodologically circular.

### Minor

- **The "calibration study" is underspecified**: The paper states that 5 prompts are sufficient based on a convergence analysis over 50 questions with 5 re-runs, but the details are vague. What confidence interval width was targeted? How was the "relative error bar" computed? The figure reference (Figure 8) is not in the provided content.

- **The prompting manipulation is coarse**: The distinction between "Full Reasoning," "Medium Reasoning," and "Low Reasoning" is based on prompt wording, but there is no verification that models actually follow these instructions differently. The observed differences could reflect prompt sensitivity rather than genuine changes in reasoning depth.

- **Information overlap metrics are surface-level**: Jaccard similarity and Manhattan distance on bag-of-words representations cannot capture semantic equivalence in physics reasoning. Two different but equally valid derivations of the same result would have low overlap by these metrics, while verbatim repetition of incorrect equations would have high overlap.

### Trivial
None.

## Nice-to-Haves

- A human evaluation study validating the Claude-4 Sonnet judge for physics scoring would significantly strengthen the paper.
- Content analysis of the "crammed" answers (e.g., do they contain correct equations? Are they logically coherent?) would make the cramming claim more concrete.
- Testing on non-physics structured reasoning domains (e.g., math, chemistry) would strengthen the generalizability claims.

## Novel Insights

The paper's most genuinely novel insight is the observation that LLMs exhibit a systematic compensatory behavior—"cramming"—when their CoT traces are disrupted, and that this behavior allows accuracy to remain stable under surprisingly high deletion rates (40-60%). This finding challenges the assumption that CoT traces are necessary for correct answers and suggests that models may have internalized solution templates that can be deployed independently of the explicit reasoning trace. However, the paper does not fully establish whether this is a feature (robustness) or a bug (unfaithfulness), and the mechanistic basis remains unclear.

## Suggestions

1. **Strengthen the faithfulness claim**: Either provide mechanistic evidence (e.g., probing internal representations, analyzing attention patterns) that CoT traces are not used, or reframe the paper's claims around "necessity" rather than "faithfulness." The current framing overclaims relative to the evidence.

2. **Validate the evaluation metric**: Conduct a human expert evaluation on a subset of the data to establish that Claude-4 Sonnet's scoring correlates with human judgment for physics solutions. Report inter-rater reliability.

3. **Analyze the content of crammed answers**: Instead of just measuring length, categorize the content of longer answers (e.g., correct physics vs. verbose filler vs. incorrect reasoning). This would distinguish genuine reconstruction from superficial verbosity.

4. **Test on additional domains**: Even a small experiment on math or chemistry problems would significantly strengthen the claim that the findings generalize beyond physics.

5. **Consider alternative interpretations**: The paper should discuss the possibility that models are genuinely using CoT but can also draw on internal knowledge when CoT is disrupted—this would be a sign of robustness, not unfaithfulness.

## Score and Decision

The paper presents a novel methodological contribution and documents an interesting empirical phenomenon (cramming under CoT deletion). However, the core claim about "faithfulness" is not adequately supported by the experimental design, which primarily tests necessity rather than faithfulness. The evaluation relies on an LLM judge without validation, and the information overlap metrics are too coarse to support the strong conclusions drawn. The paper would benefit from a more measured framing and additional mechanistic or content-based analysis.

**Score**: 5.0

**Decision**: Reject

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>