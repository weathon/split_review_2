## Summary

This paper introduces LEGO-EVAL, a tool-augmented evaluation framework for text-guided 3D scene synthesis that decomposes fine-grained instructions into constraints and uses a diverse set of 21 tools (environment interaction, textual reasoning, multimodal reasoning) to perform multi-hop grounding of scene components. It also presents LEGO-BENCH, a benchmark of 130 manually curated instructions with 1,250 constraints reflecting real-world complexity. Experiments show LEGO-EVAL achieves 0.81 F1 (Cohen's kappa 0.63) vs 0.40 (kappa 0.05) for VLM-as-a-judge, and reveals that current generation methods achieve at most 10% holistic success rate on fine-grained instructions.

## Strengths

- **Well-motivated problem**: The paper convincingly argues that evaluating fine-grained 3D scene synthesis is important for embodied AI, and that existing methods (CLIPScore, VLM-as-a-judge, SceneEval) are inadequate due to their inability to perform multi-hop grounding in 3D scenes. This is a genuine gap.

- **Novel and practical approach**: The four-stage pipeline (constraint identification → tool execution planning → argument selection & execution → constraint validation) is well-designed. The decomposition into 21 specialized tools across three types is thoughtful and covers the diverse aspects of scene understanding that end-to-end VLMs miss.

- **Strong empirical validation**: LEGO-EVAL achieves 0.81 F1 (holistic) and 0.63 Cohen's kappa vs 0.40 and 0.05 for the best VLM baseline — an improvement of more than 2× in F1. The ablation study (Table 2) convincingly shows that all three tool types are necessary, with environment interaction being the most critical (-24.9% when disabled).

- **Useful benchmarking result**: Showing that current methods achieve at most 10% holistic success rate on fine-grained instructions is an important finding for the community. The analysis in Figure 6 showing sharp decline with instruction complexity is particularly informative.

- **End-to-end automation works**: Table 4 shows that automatically identified constraints yield evaluation results nearly identical to human-annotated constraints, supporting practical usability.

## Weaknesses

### Major

- **Modest benchmark size and limited significance reporting**: LEGO-BENCH contains only 130 instructions (260 instruction-scene pairs after augmentation). The paper does not report confidence intervals or statistical significance tests for the F1/kappa comparisons. Given the small dataset, the impressive gap between methods might have wider variance than reported.

- **Simulator coupling and generalizability**: The 21 tools are tightly coupled to the Unity engine environment (e.g., `get_topdown_scene`, `get_object_info`). The paper does not discuss how LEGO-EVAL would transfer to other popular simulators (Habitat, Matterport3D, iGibson). The framework's design is principled, but the concrete implementation is not portable without substantial re-engineering.

- **No downstream validation**: The paper evaluates evaluation quality against human judgments, but does not validate whether scenes scoring higher on LEGO-EVAL actually lead to better embodied agent performance. This leaves a gap in the chain: we know LEGO-EVAL agrees with humans, but we don't know if scenes that pass LEGO-EVAL actually enable better policy learning or deployment.

### Minor

- **VLM-as-a-judge baselines are relatively weak**: The VLM baselines use a simple setup (4 images, self-consistency over 3 samples). Stronger prompt engineering (e.g., chain-of-thought, structured output format, more views) might narrow the gap. The comparison is fair but not maximally informative about what VLMs could achieve.

- **Refinement experiment (Figure 7) uses only Holodeck**: The demonstration that LEGO-EVAL serves as effective feedback for refinement is shown only with Holodeck. Results with other generation methods would strengthen the claim.

- **The 10% holistic SR finding could be overinterpreted**: All four generation methods (I-Design, LayoutGPT, Holodeck, LayoutVLM) were originally designed to work with coarser instructions. The low success rate on LEGO-BENCH's fine-grained instructions is revealing, but not necessarily a criticism of the methods' core design.

### Trivial

- Table 1 prints "GPT-o4-mini" which should be "GPT-4o-mini".

## Nice-to-Haves

- Release the code and LEGO-BENCH dataset publicly to facilitate community adoption and reproducibility.
- Evaluate on a downstream task (e.g., agent navigation success rate in high-scoring vs. low-scoring scenes) to close the validation loop.
- Analyze failure cases of LEGO-EVAL — what kinds of constraints does it still struggle with?
- Report inter-annotator agreement for the human ground-truth judgments used in Table 1.

## Novel Insights

The key insight is that *evaluating* 3D scene synthesis is itself a harder multi-hop grounding problem than often assumed — it requires (1) identifying scene components, (2) verifying their attributes, and (3) checking spatial relationships, all of which standard VLMs perform poorly on 3D data. The paper demonstrates that the solution is not better end-to-end VLMs but rather explicit decomposition into tool-mediated sub-tasks, where each tool retrieves a specific type of information (visual, textual, or text-from-visual) that compensates for VLMs' weaknesses in 3D spatial reasoning and fine-grained attribute verification. This suggests a broader principle: for structured evaluation tasks in 3D, tool augmentation may be more effective than scaling up monolithic models.

## Suggestions

- Add confidence intervals or bootstrapped error bars to the main evaluation results (Table 1) to strengthen statistical support.
- Include a discussion of how the tool set could be adapted to other 3D simulators, or provide an abstraction layer that would make porting easier.
- Add a small experiment connecting LEGO-EVAL scores to downstream agent performance (e.g., task success rate for agents trained in scenes with high vs. low evaluation scores).
- Release the benchmark and evaluation code to maximize community impact.

## Score and Decision

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>