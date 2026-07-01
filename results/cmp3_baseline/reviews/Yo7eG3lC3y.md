## Summary

This paper introduces LEGO-EVAL, a framework for evaluating text-guided 3D scene synthesis that augments VLMs with a diverse set of 21 tools enabling multi-hop grounding of scene components. The authors also contribute LEGO-BENCH, a benchmark of 130 fine-grained instructions with 1,250 constraints spanning objects and architectural components. Experiments show LEGO-EVAL achieves 0.81 F1 (vs. 0.40 for VLM-as-a-judge) and reveals that current scene generation methods satisfy at most 10% of instructions holistically.

## Strengths

- The problem is well-motivated and practically important: evaluating whether generated 3D scenes satisfy fine-grained constraints is critical for embodied agent training, and the paper convincingly demonstrates that existing methods (CLIPScore, VLM-as-a-judge) fail at multi-hop grounding.
- The tool-augmented approach is novel and principled: decomposing evaluation into constraint identification, tool execution planning, argument selection, and validation with 21 heterogeneous tools is a clean design that addresses the limitations of monolithic VLM evaluation.
- Empirical results are strong and comprehensive: LEGO-EVAL achieves 0.81 F1 and 0.63 Cohen's kappa vs. 0.40 and 0.05 for VLM baselines, and the paper provides careful ablation studies (disabling tool types), component analysis (tool planning vs. argument selection), and end-to-end validation (automatic vs. human-annotated constraints).
- The refinement experiment (Figure 7) provides compelling evidence that LEGO-EVAL's interpretable evaluations serve as useful feedback signals, outperforming prompted VLMs as a refinement mechanism.

## Weaknesses

### Fatal
None.

### Major

1. **Benchmark size limits statistical power.** LEGO-BENCH contains only 130 instructions, which is modest for a benchmark intended to evaluate generation methods. While the authors add 130 negative scenes for evaluation experiments, the core benchmark remains small, raising questions about coverage of diverse room types, object categories, and spatial configurations.

2. **Limited generalizability assessment.** The framework relies on Unity rendering infrastructure and a specific tool set tightly coupled to the simulator. The paper does not discuss how LEGO-EVAL would generalize to other 3D scene representations (e.g., NeRF, mesh-based, or different simulators), which limits its applicability for the broader community.

3. **The comparison with SceneEval is not fully equitable.** SceneEval cannot evaluate 41% of LEGO-BENCH constraints, and treating unevaluable constraints as incorrect (Full Dataset) arguably penalizes it unfairly for limitations of the benchmark rather than its own evaluation capability. The Measurable Dataset comparison (F1 0.47 vs. 0.81) is more appropriate, but the gap is still partly attributable to SceneEval's restricted constraint taxonomy rather than poor grounding.

4. **Computational cost is unaddressed.** LEGO-EVAL uses 21 tools requiring multiple VLM/LLM calls, Unity rendering, and tool execution planning per constraint. The paper provides no analysis of runtime or cost relative to baselines, which is a practical concern for adoption as an evaluation standard.

### Minor

1. The constraint categories (Floor Layout, Material Selection, Object Selection, Object Placement) have potential overlap. For example, "a sliding window on an orange wall" involves both Object Selection (window) and Material Selection (wall color), and the paper does not clarify how such cross-cutting constraints are assigned.

2. The paper does not analyze failure cases of LEGO-EVAL itself. Understanding which constraint types are hardest to evaluate (e.g., spatial reasoning vs. attribute verification) would strengthen the contribution.

3. The claim "more than doubles the F1 score" is numerically correct but slightly overstated since the baseline F1 is very low (0.40), making the relative gain less surprising.

### Trivial
None.

## Nice-to-Haves

- A breakdown of LEGO-EVAL's performance by constraint type (Floor Layout, Material Selection, etc.) would help identify which aspects of evaluation benefit most from tool augmentation.
- Discussion of whether the framework could be adapted to use open-source 3D engines (e.g., Blender, Three.js) rather than Unity would improve reproducibility.
- An analysis of how many tool executions are typically needed per constraint and the corresponding token cost would help practitioners assess trade-offs.

## Novel Insights

Beyond the paper's own contributions, there is an interesting observation about the relationship between evaluation and generation: the sharp gap between partial and holistic success rates (methods achieve ~60% partial SR but ≤10% holistic SR) suggests that current generation methods treat constraints independently and fail to compose them. This mirrors similar findings in compositional generation tasks and suggests that 3D scene synthesis may benefit from approaches that model constraint interactions explicitly, rather than treating generation as independent constraint satisfaction.

## Suggestions

- Release LEGO-EVAL as an open-source evaluation harness that can be adapted to new simulators, with documentation on how to add custom tools or swap the underlying rendering engine.
- Conduct a human study comparing the interpretability and informativeness of LEGO-EVAL's evaluation explanations against those from VLM-as-a-judge, to further substantiate the qualitative case study in Figure 8.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>