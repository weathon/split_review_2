## Summary

This paper introduces LEGO-EVAL, a tool-augmented evaluation framework for assessing fine-grained text-to-3D scene alignment, along with LEGO-BENCH, a benchmark of 130 detailed instructions with 1,250 constraints spanning objects, architecture, layout, and materials. The framework decomposes instructions into constraints, plans and executes 21 tools (environment interaction, textual reasoning, multimodal reasoning) to ground scene components, and produces binary judgments with interpretable explanations. Experiments show LEGO-EVAL achieves F1=0.81 and Cohen's κ=0.63, more than doubling the best VLM-as-a-judge baseline (0.40/0.05). Benchmarking reveals that all existing generation methods achieve ≤10% holistic success rate on LEGO-BENCH.

## Strengths

- **Large and consistent quantitative gap over baselines.** LEGO-EVAL achieves F1=0.81 and Cohen's κ=0.63 at the holistic level vs. the best VLM-as-a-judge at 0.40/0.05 (Table 1). This is more than doubling the F1 and moving from near-zero to substantial agreement — the gap is large enough that it cannot be explained by minor evaluation artifacts.

- **Well-designed ablation study (Table 2)** demonstrating the necessity of different tool types. Removing Environment Interaction tools causes a 24.9% drop in holistic F1; the asymmetric degradation across tool removals provides informative signal about which tools are backbone vs. supplementary.

- **End-to-end evaluation validation (Table 4):** automatically extracted constraints vs. human-annotated ones produce nearly identical outcomes (±0.03 SR) across four generation methods, showing that the framework is practically usable without manual constraint annotation.

- **Honest and impactful benchmark finding:** all evaluated generation methods achieve ≤10% holistic success rate on LEGO-BENCH. This is a sobering, clearly stated result that provides concrete direction for the community.

- **Concrete, compelling motivation.** The paper identifies a genuine gap: existing metrics cannot perform multi-hop grounding in 3D scenes. The "pencils one meter apart" example (Figure 1) is a clear, memorable illustration of the failure mode.

## Weaknesses

### Major

- **Figure 8 contains an internal contradiction.** LEGO-EVAL outputs "Valid ✓" alongside reasoning that "the constraint cannot be satisfied" because neither object (flashlight, laptop) is present in the scene. Per the paper's own Step 4 definition (Section 3.1: "A scene is deemed valid only if it fulfills all constraints C specified in the instruction I"), this scene should be judged Invalid. The paper then claims "all methods achieve accurate judgments" for this example (line 350), but the figure's output contradicts that claim. This must be clarified: either the figure has a labeling error (the checkmark should be an X), or the framework sometimes returns incorrect polarity despite reasonable reasoning. The paper needs to acknowledge and address this.

### Minor

- **The refinement experiment (Section 5, Figure 7) lacks critical detail.** The paper states that LEGO-EVAL output is used to "refine invalid scenes" but does not specify whether the conversion of feedback into scene modifications is automated or human-in-the-loop. If human-in-the-loop, the comparison against VLM-as-a-judge feedback is confounded by human effort and interpretability differences. This detail is essential for interpreting the reported improvement from ~8.5% to ~18.5% holistic SR.

- **The claim that all three tool types are "indispensable" is overstated.** Removing Multimodal Reasoning tools (w/o M) causes only a 0.04% drop in holistic F1 (Table 2), which is at noise level. The textual and environment tools clearly drive the gains; multimodal tools contribute marginally at best. The paper's framing should be tempered accordingly.

- **The correlation analysis (Table 5) confounds model capability with the planning-vs-argument dimension.** Comparing tool execution planning vs. argument selection across different LLMs (Gemma3-27B, Qwen2.5VL-32B, Qwen3-32B) means the observed correlation between planning and evaluation performance could be driven by differences in model capability rather than the inherent importance of planning over argument selection. A cleaner test would hold the LLM constant while varying plan/argument quality.

### Trivial

None.

## Nice-to-Haves

- Include a brief summary of the human annotation procedure (number of annotators, inter-annotator reliability) in the main text rather than deferring entirely to the appendix.
- Clarify how `get_spatial_relation` handles diverse natural-language spatial expressions, to make the claimed advantage over SceneEval more explicit.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Human annotation procedure underspecified:** The paper states that further details are in Appendix B.2 (which exists in the original submission). The main text provides reasonable summary information (130 instructions, 1,250 constraints, 260 total instruction-scene pairs). REMOVED per hard rule about missing appendix content.
- **Abstract phrasing ambiguity about "often leads to improperly grounded":** a wording nitpick. REMOVED.
- **SceneEval spatial relations comparison:** The paper explicitly states LEGO-EVAL "supports spatial reasoning across all scene components and can handle a broad range of relationships expressed in natural language." The concern is based on speculation about how `get_spatial_relation` works. REMOVED.
- **GPT-4.1 dependence:** The paper already addresses this through the end-to-end evaluation analysis (Table 4). REMOVED as already addressed.
- **Partial SR >50% claim:** The paper provides full data in Table 3 and acknowledges variation across constraint types. The statement is factually correct. REMOVED.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the Figure 8 contradiction.** Either correct "Valid ✓" to "Invalid ✗" (and update the claim about "all methods achieve accurate judgments" since LEGO-EVAL's judgment would then be correct), or explicitly explain the evaluation logic that produces "Valid" when a constraint cannot be satisfied despite the Step 4 definition.
2. **Specify the refinement mechanism** (automated or human-in-the-loop) in the main text.
3. **Temper the "indispensable" claim** about multimodal tools given the 0.04% drop at the holistic level.
4. **Add a caveat to the correlation analysis** acknowledging the model-capability confound, or re-run with a single LLM backbone.

## Score and Decision

This paper makes a solid contribution. The core idea — tool-augmented VLMs with decomposed constraints for 3D scene-instruction alignment — is sound, the ablation is well-designed, and the quantitative results are dramatically better than existing methods. The LEGO-BENCH dataset fills a genuine gap, and the finding that all existing methods cap at ≤10% holistic success rate is a valuable community result. The Figure 8 contradiction is the most significant issue; it needs to be resolved (it is likely a figure error rather than a fundamental flaw in the framework), and it does not undermine the paper's main experimental claims which are supported by full evaluations in Tables 1–4. The remaining weaknesses are minor and easily addressable.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>