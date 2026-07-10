Now I'll produce the final consolidated review.

## Summary

This paper proposes the Fast and Slow Effect (FSE) framework to evaluate whether LLM/VLM-generated concept annotations for XAI are sufficient for accurate concept-class mapping. The framework collects concepts incrementally across five stages (from fast pixel-based classification to slow text-based concept reasoning) and measures the Class Representation Index (CRI). Across six models and five datasets, the paper finds that slow (concept-based) mode consistently underperforms fast (visual) mode on fine-grained datasets, and — most importantly — that fused (fast+slow) mode achieves high performance even when concept-only performance is poor, directly challenging the common "utility-as-proxy" evaluation practice.

## Strengths

- **Utility-as-proxy critique (Table 4) is the paper's strongest and most robust contribution.** The paper demonstrates that fused (fast+slow) mode achieves ~83–96% CRI while slow mode alone achieves only ~42–68% under identical conditions. This cleanly shows that strong downstream performance can coexist with poor concept annotations, directly challenging a frequently used evaluation shortcut in concept-based XAI. The finding is robust across models and datasets and is not compromised by the evaluation design's confounds.

- **The core evaluation problem is well-motivated.** The motivating example (Figure 1) — where an annotator correctly identifies an image but misclassifies when forced to reason from its own concepts — is intuitively compelling and clearly grounds the paper's central concern.

- **The experimental scope is substantive.** Six models from three families (GPT-4o, Qwen2-VL, Llama3.2) at two scales each, across five datasets spanning fine-grained (CUB, Cars, Flowers) and general (CIFAR-100, Caltech-101) categories, with both post-hoc and visual-grounded annotation scenarios, plus a carefully designed preliminary experiment on distractor selection.

## Weaknesses

### Fatal
None.

### Major

- **The CRI metric conflates concept quality with the model's text-reasoning ability (structural confound).** The paper measures whether the *same model that generated the concepts* can classify correctly from those concepts as text. Low CRI could indicate either (a) genuinely insufficient concepts, or (b) the model being poor at text-based reasoning from concept descriptions. The paper consistently interprets low CRI as (a), but the design cannot rule out (b). This is not a missing ablation — it is a structural limitation of the evaluation construct. A human baseline (can humans classify from the same concepts?) or cross-model transfer experiment (concepts from Model A, classified by Model B) would be needed to disentangle these explanations. The paper's strongest finding (utility-as-proxy critique) does not depend on this confound, but the paper's broader claims about "annotation insufficiency" are overstated relative to the evidence.

- **The headline fast vs. slow mode comparison confounds annotation quality with modality.** Fast mode (t=0) uses pixel-based visual classification, while slow mode (t>0) uses text-based classification from concept descriptions. That pixel-based inference outperforms text-based reasoning is expected — vision-language models are trained primarily on aligned image-text pairs, not text-only reasoning from concept lists. The paper frames the negative CRI gap as evidence that "annotations are insufficient," but an equally parsimonious interpretation is that text is a lossy representation of visual information and models are worse at reasoning from text than from pixels. This is partially mitigated by the reversal on common datasets (Table 3, where slow mode outperforms fast mode on CIFAR-100 and Caltech-101), but this reversal is reported without any analysis of *why* it occurs, which is a missed opportunity.

### Minor

- **Equation (2) contains an indexing error.** The CRI formula writes 1/t · Σ_{i=1}^{t} 1[y_i^t = y_i], using the annotation step index t as both the summation bound and denominator. Given the test set definition D_test = {(c_i^t, y_i^t) | i=1,...,l}, the formula should use l (the total number of test cases). This is likely a typo (reported values are plausible) but should be corrected as the paper's central equation.

- **The sample size l for main experiments is defined but never instantiated.** For the preliminary experiment the paper states "randomly sampling 100 images," but for the main CRI results (Figure 3, Tables 2–4) no sample size is given. Without knowing l, readers cannot independently assess reliability or plan replications.

- **The "Slow Mode Superiority" framing appeals to dual-process theory** (Kahneman, 2011), a theory of human cognition, without justifying its applicability to LLMs. This creates a theoretical expectation that the paper then "refutes." The empirical finding is interesting on its own; the framing inflates apparent novelty at the cost of rigor.

- **The five-stage concept refinement process is not validated.** The paper describes stages (Background, Superclass, Salient Features, Detailed Features, Auxiliary Features) but provides no evidence that stages produce genuinely distinct content. Without an inter-stage distinctiveness analysis, it is unclear whether stages 3–5 contribute substantially new information or produce overlapping concepts.

- **The reversal on common datasets (Table 3) is underexplained.** Slow mode outperforms fast mode on CIFAR-100 and Caltech-101, directly contradicting the fine-grained results. This is the paper's best internal control for the modality confound, but it is discussed in only one paragraph with no analysis of why the pattern flips (e.g., concept verbalization difficulty, distractor confusability, class count effects).

### Trivial
None.

## Nice-to-Haves

- Add a human baseline where humans classify from the LLM-generated concepts to resolve whether low CRI reflects insufficient concepts or poor text-reasoning.
- Add a cross-model transfer experiment (concepts from Model A classified by Model B) to disentangle concept quality from self-referential reasoning limitations.
- Analyze why the slow mode outperforms fast mode on common datasets — this would deepen the paper's contribution.
- Report the test set size l for all main experiments and fix the indexing typo in Equation (2).
- Temper categorical claims about "annotation insufficiency" in the abstract and introduction to reflect the CRI confound.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Definition 3.1 is circular"** — REMOVED. The reviewer claims the definition merely restates what CRI measures, but a conceptual definition followed by an operational metric is standard practice. This criticism is incorrect.
- **"Abstract wording 'dropping by over 25%' is misleading"** — REMOVED. This is standard ML reporting convention and the reported values are consistent with the description.
- **"Preliminary experiment measures similar quantity to CRI"** — REMOVED. The contradiction test serves a specific design purpose (distractor selection) and is explicitly preliminary; this is not a weakness.
- **"Generic conclusion"** — REMOVED. Minor presentation preference, not a substantive weakness.

## Novel Insights

None beyond the paper's own contributions. The utility-as-proxy critique (Table 4) is the paper's most novel and least-compromised insight and is already presented as such.

## Suggestions

- To resolve the central confound, add a human baseline where humans classify from the LLM-generated concepts. If humans succeed where the model fails, the issue is text-reasoning ability, not concept quality.
- Alternatively, add a cross-model transfer experiment (concepts from Model A classified by Model B) to disentangle concept quality from self-referential reasoning.
- Analyze why the slow mode outperforms fast mode on common datasets (CIFAR-100, Caltech-101) — this is the paper's best internal control for the modality confound.
- Report the test set size l for all main experiments and fix the indexing typo in Equation (2).
- Tone down categorical claims about "annotation insufficiency" to reflect that CRI conflates concept quality with text-reasoning ability.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>