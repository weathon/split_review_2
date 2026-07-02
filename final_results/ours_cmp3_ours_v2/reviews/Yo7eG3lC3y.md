## Summary

This paper presents LEGO-EVAL, a tool-augmented evaluation framework for assessing fine-grained alignment between text instructions and generated 3D scenes. The framework decomposes evaluation into four stages (constraint identification, tool execution planning, argument selection, validation) and uses 21 tools across three types (Environment Interaction, Textual Reasoning, Multimodal Reasoning) to perform multi-hop grounding. The paper also introduces LEGO-BENCH, a benchmark of 130 fine-grained instructions with 1,250 constraints. Experiments show LEGO-EVAL achieves F1=0.81 and Cohen's κ=0.63 at the holistic level versus at most F1=0.49 and κ=0.05 for baselines (Table 1). Benchmarking generation methods reveals they achieve at most 10% holistic success rate (Table 3).

## Strengths

- **Well-motivated and cleanly designed framework.** The paper identifies a genuine limitation of CLIPScore and VLM-as-a-judge for 3D scene evaluation — their inability to perform multi-hop grounding (locating components, verifying attributes, checking spatial relations). The four-stage decomposition (constraint identification → tool planning → argument selection → validation) directly addresses this failure mode, and exploiting available structured scene metadata alongside rendered images is sensible.

- **Large and consistent performance gains.** LEGO-EVAL achieves F1=0.81 and Cohen's κ=0.63 at holistic level versus at most F1=0.49 and κ=0.05 for alternatives (Table 1). The gap is consistent across both holistic and partial settings and across multiple base LLM backbones (GPT-4.1, GPT-4.1-mini, Qwen2.5VL-32B). The ablation study (Table 2) confirms all three tool types contribute substantially, with Environment Interaction being particularly critical (removing it plus Multimodal Reasoning drops holistic F1 by 24.9%).

- **Striking benchmark finding.** The result that existing generation methods achieve at most 10% holistic success rate (Table 3), with performance collapsing on instructions with 13+ constraints (Figure 6), is a genuinely useful finding that establishes a clear gap for the field.

- **Informative component analysis.** The correlation analysis (Table 5) showing tool planning is more predictive of overall evaluation performance than argument selection goes beyond "our method works" to explain why. The finding that evaluation with automatically extracted constraints closely matches human-annotated ones (Table 4) supports practical end-to-end usage.

## Weaknesses

### Fatal
None.

### Major

- **Human-judgment ground truth is under-specified.** All central claims about LEGO-EVAL's superiority (F1, precision, recall, Cohen's κ) are computed against human judgments on 260 instruction-scene pairs. Yet the paper provides no information about how these judgments were obtained: who the annotators were, how many there were, what instructions they received, what inter-annotator agreement was reached, or how disagreements were resolved. The paper references Appendix B.2 for dataset collection (stripped by parser), but the core evaluation protocol motivating Table 1 requires explicit description. For a paper whose central claim is alignment *with human judgment*, this omission is significant.

- **Figure 8 case study contains a clear internal contradiction.** The case study is meant to demonstrate LEGO-EVAL's superior reasoning. The instruction specifies "The flashlight and the laptop are facing the same direction." LEGO-EVAL's judgment reads **"Valid ✓"** but its own reasoning text says "Since neither object is present, there is no way to assess whether the flashlight and the laptop are facing the same way. This means **the constraint cannot be satisfied.**" The judgment ("Valid ✓") directly contradicts the reasoning ("cannot be satisfied"). The paper's accompanying text claims "all methods achieve accurate judgments" — but if the ground truth is that the constraint is not satisfied (as VLM-as-a-Judge and SceneEval correctly indicate with Invalid ✗), then LEGO-EVAL's checkmark is wrong. This is not a formatting issue; it is an error in the paper's own flagship demonstration. It does not invalidate the quantitative results in Table 1, but it does erode confidence in presentation quality.

### Minor

- **No confidence intervals or measures of variance.** All metrics are reported as point estimates on 260 instruction-scene pairs without confidence intervals or statistical significance tests. On a dataset of this size, the reader cannot assess the reliability of the reported gaps without some variance estimate.

- **Conflated informational and reasoning advantages.** LEGO-EVAL accesses structured scene metadata (exact coordinates, object IDs, property values from the Unity engine) through its tool set, while VLM-as-a-judge receives only four rendered images. The paper does not attempt to separate how much of the 0.41 F1 gap comes from having access to ground-truth scene data versus from the multi-step reasoning pipeline. While tool augmentation is the point of the framework, a complementary experiment giving VLM-as-a-judge the same structured inputs would clarify the source of gains.

- **Internal VLM error propagation not discussed.** Several tools in the tool set rely on VLMs internally (e.g., `get_property_verification`, `get_object_match`). The paper treats tools as reliable oracles and does not discuss how internal VLM errors might propagate through the pipeline. This is partially mitigated by the ablation study showing all tool types matter, but the concern is not explicitly addressed.

- **The refinement experiment (Figure 7) is somewhat circular.** Showing LEGO-EVAL provides better feedback than VLM-as-a-judge for scene refinement is expected given that Table 1 already establishes VLM-as-a-judge as a poor evaluator. This experiment is interesting but predictable from the main results.

### Trivial
None.

## Nice-to-Haves

- Disentangle informational advantage from reasoning advantage by providing VLM-as-a-judge with structured scene metadata alongside images.
- Include error analysis: examples where LEGO-EVAL disagrees with human ground truth, with characterization of why.
- Report computational cost: average number of API calls per evaluation and approximate cost.
- Discuss generalizability to other simulators beyond the Unity-based pipeline used.

## Removed Points

These points were flagged for removal and should be treated with caution:

- **"LEGO-BENCH is too small"** — Removed. 130 instructions with 1,250 constraints is reasonable for a specialized benchmark. Many accepted benchmarks at top venues start at similar or smaller scales. The reviewer's concern about confidence intervals is already kept as a minor weakness.
- **"Implausibly high refinement values"** — Removed. The reviewer's skepticism about 18.5% SR is unsupported speculation; these values are physically plausible for iterative refinement with a strong evaluator.
- **"Missing baselines from related work"** — Removed per rules (cannot confirm existence of unmentioned works).
- **"Formatting/style nitpicks"** — Removed per rules (parser artifacts).
- **Various generic doubts expressed as "could this be measuring a proxy?"** — Removed. These are speculative and not anchored to specific paper content.
- **"No discussion of generalizability"** — Demoted from weakness to nice-to-have. The paper scopes itself to the presented simulator; this is not a core flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Provide full annotation protocol details** (in main paper or appendix): annotator qualifications, number of annotators, inter-annotator agreement (e.g., Fleiss' κ or pairwise agreement), instructions given, and disagreement resolution procedure.
2. **Correct the Figure 8 case study:** either the judgment should be "Invalid ✗" or the reasoning text should be revised to match the judgment. Verify that the reasoning text correctly reflects the scene content (the scene description states a laptop is present but LEGO-EVAL's reasoning claims "neither object is present").
3. **Add confidence intervals** (bootstrap estimates) for all main metrics in Tables 1 and 3.
4. **Include a VLM-as-judge+structured-inputs ablation** to isolate the reasoning advantage from the informational advantage.
5. **Add a brief failure analysis section** discussing cases where LEGO-EVAL disagrees with human ground truth.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>