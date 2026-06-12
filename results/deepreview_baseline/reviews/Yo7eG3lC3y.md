## Summary

This paper introduces LEGO-EVAL, a tool-augmented evaluation framework for assessing alignment between fine-grained textual instructions and generated 3D scenes, along with LEGO-BENCH, a benchmark of 130 complex instructions with 1,250 constraints. The framework decomposes instructions into constraints, plans and executes tool calls (environment interaction, textual reasoning, multimodal reasoning) to ground scene components, and validates each constraint individually. Experiments show LEGO-EVAL achieves 0.81 F1 and 0.63 Cohen's kappa for holistic evaluation, substantially outperforming VLM-as-a-judge baselines (0.40 F1, 0.05 kappa), and reveals that existing 3D scene generation methods satisfy at most 10% of instructions fully.

## Strengths

- **Novel and well-motivated approach to a real problem**: The paper correctly identifies that existing evaluation methods (CLIPScore, VLM-as-a-judge) fail at multi-hop grounding in 3D scenes—they cannot reliably locate objects, verify attributes, and check spatial relations. The tool-augmented framework is a principled solution that directly addresses this failure mode.

- **Strong empirical results with clear baselines**: LEGO-EVAL achieves 0.81 holistic F1 vs. 0.40 for the best VLM baseline, and 0.63 Cohen's kappa vs. 0.05. The ablation study (Table 2) convincingly shows all three tool types are necessary, with environment interaction being most critical (24.9% drop when removed).

- **Comprehensive benchmark and analysis**: LEGO-BENCH contains 1,250 constraints across 130 instructions with human annotations, covering diverse constraint types. The analysis of existing methods (Table 3, Figure 6) reveals that even the best method (LayoutVLM) achieves only 10% holistic success rate, and performance collapses on complex instructions (13+ constraints). This provides a clear signal to the community about where progress is needed.

- **End-to-end automation validated**: Table 4 shows that using automatically identified constraints yields nearly identical results to human-annotated constraints, demonstrating the framework can operate fully autonomously without manual constraint extraction.

## Weaknesses

### Major

- **Limited evaluation of the evaluation framework itself**: The human agreement study uses only 260 instruction-scene pairs (130 valid, 130 invalid). While this is reasonable, the paper does not report inter-annotator agreement among human judges, making it difficult to assess the upper bound of achievable agreement. If human judges themselves disagree on some cases, the reported 0.63 kappa might be closer to human-level performance than it appears.

- **No analysis of failure modes or error cases**: The paper reports aggregate metrics but does not analyze where LEGO-EVAL itself fails. Understanding whether errors come from tool planning, argument selection, or constraint validation would strengthen the contribution and guide future improvements. The case study in Figure 8 shows a success case but no failure cases.

- **Computational cost and latency not discussed**: The framework executes up to 21 tools per constraint, with multiple LLM calls for planning, argument selection, and validation. For a 10-constraint instruction, this could involve hundreds of tool executions and dozens of LLM calls. The paper does not report runtime, API costs, or discuss whether this is practical for large-scale evaluation.

### Minor

- **The tool set is tightly coupled to Unity/Holodeck**: The 21 tools (e.g., `get_topdown_scene`, `get_room_list`, `get_spatial_relation`) are designed for the Unity-based Holodeck environment. While this is a reasonable choice, it limits the framework's applicability to other 3D scene generation pipelines that use different representations (e.g., NeRF, Gaussian Splatting, or other simulators). The paper does not discuss how the tool set might generalize.

- **Constraint categorization is inherited from Holodeck**: The four constraint types (Floor Layout, Material Selection, Object Selection, Object Placement) are taken directly from Holodeck's module design. While functional, this categorization may not be optimal for all fine-grained instructions—for example, "the two pencils are about one meter apart" involves spatial relations between objects that don't fit neatly into "Object Placement" (which typically concerns object-to-architecture relations).

### Trivial

- The paper states "Since neither object is present, there is no way to assess whether the flashlight and the laptop are facing the same way. This means the constraint cannot be satisfied" in Figure 8, but the correct conclusion should be that the constraint is violated (objects are missing), not that it "cannot be satisfied." This is a minor logical inconsistency in the example.

## Nice-to-Haves

- A comparison with human-level agreement (inter-annotator reliability) would contextualize the 0.63 kappa score.
- An analysis of per-constraint-type performance (e.g., does LEGO-EVAL struggle more with spatial relations than attribute verification?) would be informative.
- A discussion of how the framework could be adapted to other 3D scene representations beyond Unity/Holodeck.

## Novel Insights

The key insight is that evaluating 3D scene-instruction alignment requires explicit multi-hop grounding that current VLMs cannot perform, and that this can be achieved by decomposing the task into constraint identification, tool planning, argument selection, and validation—each handled by specialized tools rather than relying on a single monolithic model. The finding that textual reasoning tools are more important than multimodal reasoning tools (5.05% vs. 0.04% F1 drop when removed) is non-obvious and suggests that structured scene representations (coordinates, object lists) are more reliable for evaluation than visual reasoning alone. The observation that existing methods achieve only 10% holistic success rate despite 60% partial success rate reveals that the bottleneck is not generating individual correct elements but satisfying all constraints simultaneously—a finding that reframes the challenge in 3D scene generation.

## Suggestions

- Report inter-annotator agreement among human judges to establish an upper bound for evaluation performance.
- Include an error analysis section that categorizes LEGO-EVAL's failures (e.g., tool planning errors vs. argument selection errors vs. validation errors) to guide future improvements.
- Discuss the computational cost (runtime, API calls) and whether the framework is practical for large-scale evaluation or refinement loops.

## Score and Decision

The paper makes a clear, well-supported contribution to an important problem. The evaluation framework is novel, the benchmark is valuable, and the empirical results convincingly demonstrate superiority over existing methods. The weaknesses are manageable and do not invalidate the core claims. The paper is a strong candidate for acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>