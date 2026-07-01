## Summary

The paper introduces LEGO-EVAL, a tool-augmented evaluation framework for fine-grained 3D scene synthesis, and LEGO-BENCH, a benchmark of 130 detailed instructions (1,250 constraints). LEGO-EVAL decomposes evaluation into four steps — constraint identification, tool execution planning, argument selection & execution, and constraint validation — using 21 tools across three categories (Environment Interaction, Textual Reasoning, Multimodal Reasoning). Experiments show LEGO-EVAL achieves 0.81 holistic F1 and 0.63 Cohen's kappa vs. human judgments, substantially outperforming VLM-as-a-judge baselines (0.40 F1, 0.05 kappa). Benchmarking reveals that generation methods satisfy at most 10% of instructions holistically.

## Strengths

1. **Concrete problem demonstration.** The paper grounds its motivation in a specific failure of existing methods — their inability to perform multi-hop grounding (e.g., locating a "blue chair next to the black desk" requires identifying objects, verifying attributes, and checking spatial relations). The case study in Figure 8 (VLM hallucinating a non-existent flashlight and laptop) makes the problem tangible rather than abstract.

2. **Large and consistent quantitative improvement.** Table 1 shows LEGO-EVAL (GPT-4.1) at 0.81 holistic F1 and 0.63 Cohen's kappa vs. the best VLM-as-a-judge at 0.40 F1 and 0.05 kappa. The gap is roughly a doubling of F1 and a twelve-fold increase in kappa, and this pattern holds across Holistic and Partial settings and multiple backbone LLMs.

3. **End-to-end validation (Table 4) directly validates practical use.** Showing that automatic constraint extraction yields nearly identical results to human-annotated constraints (max ±0.03 SR difference across four methods) demonstrates the method works as an automated tool, not just with oracle constraints. This goes beyond what most evaluation papers provide.

4. **Ablation study (Table 2) isolates each tool type's contribution.** The 24.9% holistic F1 drop when removing both Environment Interaction and Multimodal Reasoning tools confirms the tool augmentation is functional, not decorative. The finding that Textual Reasoning alone accounts for a 5.05% drop justifies the multi-type tool design.

## Weaknesses

### Fatal

None.

### Major

1. **No analysis of LEGO-EVAL's own failure modes.** The method achieves 0.81 holistic F1, meaning roughly 19% of its judgments disagree with the human reference — yet the paper provides no breakdown of these errors. Are failures concentrated on certain constraint types (spatial relations vs. material attributes)? Do they stem from constraint identification errors, tool planning mistakes, argument selection failures, or validation errors? For an evaluation paper whose purpose is improving assessment quality, understanding the evaluator's own blind spots is essential. Without this, the community cannot determine where the method's limitations lie or how to improve it.

2. **Human ground-truth documentation is insufficient for a benchmark paper.** All quantitative claims — F1, precision, recall, and especially Cohen's kappa — are measured against "human judgments," yet the main text provides almost no information about how these judgments were produced: number of annotators, their qualifications, independence from the authors, annotation instructions/guidelines, whether inter-annotator agreement was computed and its value, or how disagreements were resolved. The paper states "Further details on our dataset collection procedure can be found in Appendix B.2" (line 182), and the appendix was stripped by the parser, so some details may exist in the full submission. However, the main body should at minimum state the number of annotators and inter-annotator agreement for the benchmark to be credible as a community resource. The Cohen's kappa values (0.63 vs. 0.05) lose interpretive force if the reliability of the reference standard is unknown.

### Minor

3. **No confidence intervals or statistical significance on any quantitative result.** The headline result (0.81 vs. 0.40 F1) is a single point estimate from 260 instruction-scene pairs. Without variance estimates (confidence intervals, bootstrapped error bars, or significance tests), the reader cannot assess whether the improvement is stable across different samples. This is readily fixable.

4. **The 130 "negative" scenes are not described.** The evaluation uses 130 positive and 130 negative instruction-scene pairs. The paper states negative scenes are "manually curated" (line 217) but does not explain how — whether they are random perturbations of valid scenes, outputs from existing generation methods, or manually constructed counterexamples. The difficulty distribution of the negative examples directly affects the evaluation task's interpretability.

5. **The refinement experiment (Figure 7) has a weak control.** Both LEGO-EVAL and VLM-as-a-judge improve success rates when used as feedback (8.5%→18.5% vs. 8.5%→14.5%), suggesting even noisy feedback has value. The additional improvement from LEGO-EVAL could reflect superior evaluation quality, but it could also reflect differences in how actionable the textual feedback is, or regression to the mean. This experiment is suggestive but not conclusive.

6. **No discussion of computational or API cost.** LEGO-EVAL executes multiple tool calls per constraint (Figure 5 shows all three tool types are actively used). The total cost in API calls, tokens, or runtime per evaluation is never mentioned, which matters for a method positioned as a practical evaluation framework.

### Trivial

None.

## Nice-to-Haves

- Adding bootstrapped confidence intervals or standard errors to Tables 1, 2, and 3.
- A stronger VLM-as-a-judge baseline that provides structured scene data (object lists, coordinates) as text alongside images, to better isolate the contribution of tool-based execution vs. privileged information access.
- Discussing approximate API/runtime cost per LEGO-EVAL evaluation.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"Tool descriptions not in main text (Appendix C.3)."** → REMOVED: The parser strips appendix sections from all papers; they exist in the original submission. The main text already summarizes the three tool types.
2. **"Four views may be insufficient for VLM-as-a-judge."** → REMOVED: Speculative concern without evidence that more views would change results.
3. **"Augmenting methods with Holodeck introduces confounds."** → REMOVED: The paper transparently acknowledges this and explains the bridging strategy. This is a necessary experimental design choice, not a flaw.
4. **"Abstract overclaims the comparison."** → REMOVED: Comparing VLM+tool augmentation vs. VLM alone is the correct experimental design for the paper's thesis. The information asymmetry is the point, not a confound.
5. **"LLM dependency bounds performance."** → REMOVED: Generic concern applicable to any LLM-based method. The paper already tests multiple backbones.
6. **"CLIPScore baseline is weak."** → REMOVED: Observation, not a weakness; CLIPScore is treated as a lower bound.

## Novel Insights

None beyond the paper's own contributions. The reviews surface documentation gaps and missing analyses (failure mode breakdown, confidence intervals, negative scene description) rather than conceptual flaws in the method. The point that the refinement experiment's control is weak and the improvement could partly reflect factors beyond evaluation quality is the most useful critical observation.

## Suggestions

1. Add a failure analysis section breaking down LEGO-EVAL's errors by constraint type and failure source (constraint identification, tool planning, argument selection, validation).
2. Report inter-annotator agreement for the human ground-truth labels in the main text (or clearly reference the appendix section containing this information).
3. Add bootstrapped confidence intervals or error bars to all main quantitative results.
4. Describe how the 130 negative scenes were generated/curated.
5. Report approximate computational cost (API calls or runtime per evaluation).

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>