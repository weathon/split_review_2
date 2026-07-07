Now I have all the calibration data I need. Let me compile the final review.

## Final Review

**Round 1 Bracket: 4.5–5.5**

The weighted-item comparison against anchors places this paper below **Davidsonian Scene Graph** (avg 6.00), whose strengths include very strong motivation weights (+6.94, +6.87, +4.74) and only mild weaknesses (~−3.20 max). Our paper's strongest positive weights (+4.99 for end-to-end validation, +4.34 for quantitative results) are solid but lower, and our weaknesses include a concrete labeling error (Figure 8) and a scope concern about ground-truth access that the DSG paper does not face. However, our paper is clearly above **Scene Language** (4.75) and **EvalAlign** (4.75), both of which had severe weakness weights (−7.86, −8.55, −10.63) that our paper lacks. The paper sits between these anchors, closer to the DSG paper in quality of contribution but held back by unaddressed scope issues and a presentation error.

---

## Summary

This paper introduces LEGO-EVAL, a tool-augmented evaluation framework for text-guided 3D scene synthesis that decomposes evaluation into constraint identification, tool planning, argument selection, and constraint validation using 21 tools across three categories (Environment Interaction, Textual Reasoning, Multimodal Reasoning). It also presents LEGO-BENCH, a benchmark of 130 fine-grained instructions with 1,250 annotated constraints. The experiments show that LEGO-EVAL (GPT-4.1) achieves 0.81 F1 and 0.63 Cohen's kappa, substantially outperforming VLM-as-a-judge baselines (best: 0.40 F1, 0.05 kappa), and that existing scene generation methods achieve at most 10% holistic success rate on LEGO-BENCH.

## Strengths

- **Tool-augmented decomposition is structurally sound.** Breaking evaluation into constraint identification → tool planning → argument selection → validation (Section 3.1) is a principled response to the multi-hop grounding challenge. Rather than asking a single model to handle everything, the method matches each subtask to the most appropriate tool modality. (weight: +3.35)

- **Quantitative results are strong and consistent.** LEGO-EVAL (GPT-4.1) achieves 0.81 F1 and 0.63 Cohen's kappa vs. the best VLM-as-a-judge at 0.40 F1 and 0.05 kappa (Table 1), with gains across both holistic and partial metrics. The ablation study (Table 2) confirms that all three tool types contribute, and the component analysis (Table 5) separately validates tool planning and argument selection. (weight: +4.34)

- **End-to-end validation is well-designed.** Showing that automatic constraint identification produces nearly identical results to using human-annotated constraints (+0.00–0.03 difference in SR across four methods, Table 4) convincingly demonstrates that the framework works as a fully automated pipeline. (weight: +4.99)

- **The LEGO-BENCH benchmark is a useful resource.** The finding that all four evaluated scene generation methods achieve <10% holistic success rate (Table 3) reveals significant limitations in current approaches and provides a clear baseline for future work. (weight: +1.32)

## Weaknesses

### Major

- **The Textual Reasoning tools access ground-truth simulator data, creating an asymmetric comparison.** As stated in Section 3.2 (lines 172–173), the Textual Reasoning tools "retrieve textual descriptions from structured scene representations such as exact coordinates or occluded object attributes, that image cannot reliably provide." Tools like `get_object_list`, `get_object_info`, `get_spatial_relation` return exact coordinates, object identities, and attributes directly from the simulator's scene graph. The baselines (VLM-as-a-judge, CLIPScore, SceneEval) operate only on rendered images. The comparison in Table 1 therefore shows that *evaluation with access to ground-truth scene graphs* outperforms perception-only evaluation — which is a narrower claim than "LEGO-EVAL is a better general-purpose evaluator." The paper should explicitly delineate this limitation and adjust its framing. The ablation study partially mitigates this (removing Textual Reasoning drops holistic F1 by only 5.05%), but the paper would be strengthened by a perception-only ablation that runs LEGO-EVAL with only image-based tools. (weight: −0.81)

- **Figure 8 contains an internal contradiction that undermines reader confidence.** LEGO-EVAL's output in Figure 8 is shown as "Valid ✓" (line 338), but the accompanying explanation reads: "Since neither object is present, there is no way to assess whether the flashlight and the laptop are facing the same way. This means the constraint cannot be satisfied" (lines 340–341). If the constraint cannot be satisfied because required objects are absent, the judgment should be "Invalid," not "Valid." The paper's own text confirms LEGO-EVAL "determines the constraint cannot be satisfied" (line 350) and claims all methods reach "accurate judgments" — yet the figure shows a checkmark. Even if this is a labeling error in the figure rather than a system bug, it must be resolved to establish trust in the framework's outputs. (weight: −1.09)

- **The refinement experiment creates a potential evaluation-circularity concern.** Section 5 (lines 346–348) uses LEGO-EVAL's feedback to refine Holodeck scenes and then evaluates the refined scenes with the same LEGO-EVAL. If the feedback includes ground-truth coordinates and specifics of what failed, the generator could overfit to LEGO-EVAL's particular evaluation criteria rather than producing genuinely better scenes. The paper does not address whether a held-out evaluation protocol or a different evaluator was used for the final assessment. (weight: −2.06)

### Minor

- **The tool set is tied to a Unity-based simulator infrastructure.** The tools (Figure 3) interact with a Unity environment (line 172: "These tools interact with the Unity environment") and assume structured scene data is accessible through specific APIs. Portability to other scene representations (NeRF-based, mesh-based, different simulators) is not discussed, making the contribution narrower than the paper's general framing of "text-guided 3D scene synthesis evaluation." (weight: −2.73)

- **The main results lack confidence intervals or significance tests.** Table 1 reports F1, precision, recall, and kappa over 260 instruction-scene pairs without any measure of variance. Readers cannot assess whether the large gaps between methods are robust to the particular test split. Bootstrapped confidence intervals would substantially strengthen the claims. (weight: −1.72)

## Nice-to-Haves

- A perception-only ablation running LEGO-EVAL with only Environment Interaction + Multimodal Reasoning tools (no Textual Reasoning / ground-truth querying) would directly quantify how much performance relies on privileged data.
- A discussion of LEGO-BENCH's diversity (number of distinct room types, architectural styles, environment sources) would help assess the benchmark's coverage.
- Since the ablation (Table 2) suggests Environment Interaction contributes most to performance (~25% drop when removed along with Multimodal), the paper could more clearly characterize what these tools provide that the baselines' rendered images do not.

## Removed Points

These points are flagged to be removed; treat them with caution:

- "Figure 2 is hard to parse" — subjective formatting/style nitpick, not a substantive weakness.
- "Code release / reproducibility of tool set" — hard rule: remove nitpicks about undisclosed implementation details and code release plans.
- "Appendix C.3 details not available in extract" — parser-stripped appendix; the original submission contains it.
- "Generic problem importance reframing" — not specific to this paper's contribution; the paper's own description suffices.
- "SceneEval comparison is unfair because it's general-purpose vs. purpose-built" — the model's own weight (+0.84) indicates this is not actually a weakness; SceneEval is designed for the same task and the paper handles the coverage disparity transparently.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a table categorizing each tool as "ground-truth access" or "perception-based" and run a perception-only ablation (only image-based tools) to quantify how much performance relies on privileged scene-graph data.
2. Fix the Figure 8 contradiction: if the constraint is unsatisfied, the output label should be "Invalid ✗."
3. Add bootstrapped confidence intervals or statistical significance tests to Table 1.
4. In the refinement experiment, clarify whether a held-out evaluation set or a different evaluator was used to assess the final refined scenes.
5. Discuss portability of the tool framework to other simulator backends (e.g., Isaac Sim, MuJoCo) or scene representations.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Accept</decision>