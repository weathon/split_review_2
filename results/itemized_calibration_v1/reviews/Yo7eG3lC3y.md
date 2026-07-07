## Summary

This paper presents LEGO-EVAL, a tool-augmented VLM evaluation framework for assessing alignment between fine-grained 3D scene synthesis instructions and generated scenes, along with LEGO-BENCH, a benchmark of 130 instructions with ~1,250 annotated constraints spanning objects, architecture, and spatial relations. LEGO-EVAL decomposes instructions into constraints and uses 21 tools across three categories (Environment Interaction, Textual Reasoning, Multimodal Reasoning) to perform multi-hop grounding. Experiments show LEGO-EVAL with GPT-4.1 achieves F1=0.81 and Cohen's κ=0.63, substantially outperforming VLM-as-a-judge baselines (κ≈0.05). Benchmarking with LEGO-BENCH reveals existing generation methods achieve at most 10% holistic success rate.

## Strengths

1. **Large and well-characterized improvement over baselines.** Table 1 shows LEGO-EVAL (GPT-4.1) achieves F1=0.81 and Cohen's κ=0.63 vs. κ=0.05 across all VLM-as-a-judge baselines. Cohen's kappa near zero for baselines means they barely agree with human judgments beyond chance, while κ=0.63 qualitatively changes what evaluation quality is achievable with automated methods. The gap is large enough (~2× F1 improvement, ~12× κ improvement) that the main directional finding is robust.

2. **The benchmark fills a genuine gap.** LEGO-BENCH's 130 instructions with 9.6 constraints on average — spanning objects (55%), architectural components (39%), and four constraint types — addresses the lack of fine-grained benchmarks for 3D scene evaluation. Table 4's end-to-end validation (auto-extracted vs. human-annotated constraints produce nearly identical results, max ±0.03 difference) usefully addresses the concern that constraint identification is a weak link.

3. **Diagnostic benchmarking reveals a substantive field limitation.** Table 3 shows all four scene-generation methods achieve at most 10% holistic success rate (3.8%–10.0%). The breakdown by constraint type (Object Placement as the hardest at 4–46% partial SR) provides a useful diagnostic signal for future work on 3D scene generation.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Figure 8 contains an apparent internal contradiction.** LEGO-EVAL marks the constraint "The flashlight and the laptop are facing the same direction" as **Valid ✓**, while the explanation states "Since neither object is present, there is no way to assess whether the flashlight and the laptop are facing the same way. This means the constraint cannot be satisfied" (lines 338–340). Per the framework's definition (line 138: "A scene is deemed valid only if it fulfills all constraints"), a constraint that "cannot be satisfied" should yield an Invalid judgment, not Valid. The paper's text also claims "all methods achieve accurate judgments" (line 350), which conflicts with this output. This is a concrete inconsistency in the paper as presented. The most charitable interpretation is a figure labeling error, but it needs resolution — if the logic actually treats absent-object constraints as vacuously satisfied, the explanation is misleading, and if it's a bug, the reported F1 may be affected.

2. **Overclaim about multimodal reasoning tools.** The paper states "all three tools are indispensable for comprehensive and reliable evaluation" (line 249), but Table 2 shows removing Multimodal Reasoning tools drops holistic F1 by only −0.04% (from 0.81 to essentially unchanged). Removing Environment Interaction + Multimodal Reasoning causes a −24.90% drop, clearly showing the Environment Interaction tools are the primary drivers. The "indispensable" claim is not supported for the Multimodal Reasoning tools specifically; the ablation only supports indispensability of the overall toolset including Environment Interaction.

3. **Construction of the 130 negative scenes is not described.** The paper states "we also manually curate 130 additional scenes that intentionally do not fully satisfy the instructions" (line 217) but provides no information about who created them, under what instructions, or how violations were selected to avoid being trivially obvious. This makes it difficult to assess whether the evaluation task appropriately reflects the difficulty of real-world deployment, where violations are not hand-crafted. This does not invalidate the results but is a gap in the evaluation design documentation.

4. **Ablation has a constrained design.** Table 2 keeps "tools returning list of scene components... enabled" because they are "necessary for argument selection" (line 249). This means the ablation never tests a fully tool-free baseline — the "w/o E + M" condition still has Textual Reasoning tools. The paper's framing of "indispensability" should acknowledge this limitation more explicitly.

### Trivial
None.

## Nice-to-Haves

- **Report API cost / LLM call budget.** LEGO-EVAL likely uses many LLM calls per instruction (constraint identification, tool planning, argument selection, validation). Reporting approximate token usage would help practitioners assess the practical tradeoff against simpler baselines.
- **Discuss portability to other simulators.** LEGO-EVAL requires a Unity engine with 21 specific API tools. A brief discussion of what would be required to port to AI2THOR, Habitat, or ThreeDWorld would clarify the generalizability of the methodology.
- **The refinement experiment (Figure 7) stops at 3 iterations with no sign of plateauing** (Holistic SR reaches ~18.5%). Running more iterations would show the upper bound of improvement possible with LEGO-EVAL feedback.
- **Dataset balance.** The 50/50 positive/negative split (130 positive + 130 negative) means chance F1 ≈ 0.50, which several baselines fall below. Real-world evaluation distributions are more imbalanced. A minor note on how performance might change under realistic class priors would be helpful.

## Removed Points

- **"Human judgment ground truth is undocumented":** REMOVED per hard rule. The paper references Appendix B.2 for dataset collection and annotation details. The parser strips appendices from all papers; these details are assumed to exist in the original submission.
- **"SceneEval comparison complications due to Holodeck augmentation for baselines":** REMOVED. The paper transparently acknowledges that LayoutGPT, LayoutVLM, and I-Design are augmented with Holodeck to produce full scenes (line 264). This is an openly disclosed experimental design choice, not a flaw.
- **Strength about "well-motivated problem" dropped:** REMOVED per filtering rules. While true, the problem motivation is generic background context rather than a property distinguishing this paper. The remaining strengths are concrete and specific.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the Figure 8 contradiction: clarify whether "Valid ✓" is a labeling error, and if not, explain the logical treatment of absent-object constraints.
2. Soften the claim about Multimodal Reasoning tools being "indispensable" given the −0.04% ablation result, or provide analysis showing scenarios where they contribute meaningfully.
3. Describe the negative-scene curation process to help readers assess evaluation difficulty.
4. Add a brief note on API cost estimates to help practitioners evaluate the practical tradeoff.

## Calibration Anchors

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| ITq4ZRUT4a (DSG — text-to-image evaluation benchmark) | 6.00 | R1 | Yes | Both are evaluation benchmarks; LEGO-EVAL has stronger ablations and more baselines but a smaller benchmark. Comparable in quality. |
| s3sJenvY5H (Generative Robotic Simulations evaluation) | 4.75 | R1 | Yes | Had unclear contribution (−4) and no proposed benchmark; LEGO-EVAL is clearly stronger with a concrete benchmark and clearer methodology. |
| rDLgnYLM5b (ISG — interleaved text-image evaluation) | 7.20 | R2 | Yes | Has larger benchmark (1,150 samples) but uses MLLM-as-judge with cascading errors; LEGO-EVAL's tool-augmented methodology is more novel but has a smaller benchmark. |
| toqQYz2N2X (TAG-EQA — embodied QA benchmark) | 4.00 | R1 | Yes | Had significant readability issues (−5) and questionable rationale (−4); LEGO-EVAL is substantially stronger. |

**Bracket assessment (Round 1):** 5.5–7.0, based on comparing LEGO-EVAL's weighted items against the DSG (6.00) and Generative Robotic Simulations (4.75) anchors. LEGO-EVAL shares DSG's strong experimental rigor but lacks its readability issues, and is clearly stronger than the Robotics Simulations anchor. **Narrowing (Round 2):** The comparison with ISG (7.20) confirms LEGO-EVAL's methodology is more novel (tool-augmented vs. MLLM-as-judge), but its benchmark is smaller and has minor presentation issues, placing it below ISG.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>