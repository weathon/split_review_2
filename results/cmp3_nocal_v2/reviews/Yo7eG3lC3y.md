## Summary

This paper introduces LEGO-EVAL, a tool-augmented VLM pipeline for evaluating text-to-3D scene synthesis, and LEGO-BENCH, a benchmark of 130 fine-grained scene instructions with 1,250 constraints. The four-stage framework (constraint identification → tool planning → argument selection → validation) uses 21 tools across three categories (environment interaction, textual reasoning, multimodal reasoning) to ground scene components. Experiments show LEGO-EVAL achieves 0.81 holistic F1 vs. 0.40 for VLM-as-a-judge, and benchmarking of four existing generation methods reveals ≤10% holistic success rates — a useful result for the community.

## Strengths

1. **Well-motivated problem (Section 1).** The paper provides concrete, convincing examples of VLMs hallucinating (e.g., "finding" a flashlight that does not exist, misidentifying a painting as a laptop) and clearly explains why CLIPScore and VLM-as-a-judge fail at multi-hop grounding for fine-grained 3D scene evaluation.

2. **Sensible, principled pipeline (Section 3.1).** Decomposing evaluation into constraint identification → tool planning → argument selection → validation is a clear architecture. The design choice to leverage prior constraint evaluations to avoid redundant tool calls is pragmatic and well-integrated.

3. **Ablation study demonstrates all three tool types contribute (Table 2).** The 24.9% holistic F1 drop when disabling Environment Interaction + Multimodal Reasoning is dramatic and informative, providing credible evidence for the design choices.

4. **Impactful benchmarking result (Table 3).** The finding that all evaluated generation methods achieve at most 10% holistic success rate quantifies a real gap and gives the community a concrete target. The breakdown by constraint type (e.g., Object Selection at 11–50%) usefully identifies where specific methods fail.

5. **Refinement experiment demonstrates practical utility (Figure 7).** Using LEGO-EVAL's feedback to iteratively improve Holodeck scenes (~8.5% → ~18.5% holistic SR, vs. VLM feedback ~8.5% → ~14.5%) shows the framework works beyond just scoring.

## Weaknesses

### Fatal
None.

### Major

1. **The human annotation protocol for ground-truth judgments is undocumented in the main paper.** The paper reports F1=0.81 and Cohen's κ=0.63 for agreement with "human judgments" on 260 instruction-scene pairs, but provides no information about who produced these judgments, how many annotators were used, what instructions they followed, whether inter-rater reliability was assessed, or whether annotators viewed only rendered images or had interactive access. While Appendix B.2 is referenced for dataset collection procedures, the provenance of the evaluation ground truth — upon which every quantitative result in Table 1 depends — is not described. If the "human judgments" were produced without documented protocols or by the authors themselves, the headline numbers become difficult to assess. This is the single most important issue to address for the paper's claims to be verifiable.

2. **No analysis of LEGO-EVAL's failure modes.** With F1=0.81, LEGO-EVAL disagrees with human judgments on ~19% of cases. The paper provides no analysis of where these disagreements occur — whether they cluster on specific constraint types, spatial relations, object categories, or scene complexities. Understanding failure modes is necessary for the community to improve upon the framework and would substantially increase the paper's impact.

### Minor

1. **Figure 8 contains an apparent contradiction.** LEGO-EVAL outputs "Valid ✓" alongside the reasoning "Since neither object is present, there is no way to assess whether the flashlight and the laptop are facing the same way. This means the constraint cannot be satisfied." If the constraint cannot be satisfied, the scene should be Invalid. The paper's text claims "all methods achieve accurate judgments," which would be consistent if the output were ✗ instead of ✓. This is very likely a typographical error (✓ should be ✗), but as the paper's main illustrative case study, this needs correction.

2. **The comparison against baselines is structurally asymmetric in a way that is acknowledged but not controlled for.** LEGO-EVAL's tool set includes `get_object_list`, `get_object_info`, `get_spatial_relation` — tools that directly query the Unity engine's internal state (exact coordinates, full object inventories including occluded objects). Baselines only see rendered images. An ablation restricting LEGO-EVAL to only what a VLM looking at images could access (no oracle scene queries) would isolate the value of the pipeline design from the value of privileged information access and provide a fairer comparison point.

3. **No confidence intervals or statistical significance tests.** The main results in Tables 1 and 3 lack confidence intervals. For a benchmark paper, this limits the reader's ability to assess the reliability of reported gaps. Given the modest scale (130 instructions, 260 pairs), bootstrapped or exact binomial confidence intervals would be informative.

4. **The distinction between CLIP and VLM usage in Step 4 (Constraint Validation) is not explained.** Figure 2 shows "text → CLIP" and "text & image → VLM," but the prose does not describe when each is used or what the decision boundary is. The tool descriptions are deferred to Appendix C.3 (stripped), but a brief explanation in the main text would help.

### Trivial
None.

## Nice-to-Haves

- A dedicated limitations section discussing the dependence on Unity as the rendering/retrieval backend, the manually engineered tool set (21 tools), and the benchmark's focus on indoor scenes.
- A computational cost comparison (LEGO-EVAL calls an LLM/VLM multiple times per constraint plus tool executions vs. a single VLM call per scene).
- Clarify whether the 130 "valid" LEGO-BENCH scenes were manually constructed from scratch or generated by a baseline and then annotated.

## Removed Points

- **Figure 7 y-axis criticism (harsh critic claimed y-axis values appear to be absolute counts, not percentages).** This is factually incorrect. Table 3 shows Holodeck at 8.4% holistic SR and Figure 7 shows Holodeck's baseline at ~8.5 — consistent as percentages. The critic's alternative interpretation (absolute counts: 8.5 out of 130 ≈ 6.5%) does not match either value. This criticism is removed.
- **"All methods achieve accurate judgments" in Figure 8 (the critic implied the paper's claim is wrong).** The paper's text says all methods are accurate. If the ✓ in Figure 8 is a typo (should be ✗), then the paper's text is correct and this is purely a presentation error (captured in Minor weakness #1 above as needing correction). The critic's framing as a contradiction undermining the framework is inflated.
- **Missing limitations section (the critic listed this as a weakness).** Demoted to nice-to-have — many papers at top venues do not have explicit limitations sections.
- **Small benchmark size (the critic argued 130 instructions limits statistical power).** The benchmark is modest but the paper's main results (≤10% SR) are clear and impactful. The critic's concern about "distributional artifacts" is speculative.
- **The critic's speculation about the 130 valid scenes' origin ("If they were manually designed by the authors, the human judgments may encode bias").** The paper states the scenes are "manually annotated" — the critic is speculating about bias without evidence.
- **The critic's question about the F1 positive class definition.** Precision and recall are reported separately for all methods, making F1 interpretable regardless of which class is "positive."
- **The critic's concern about the "no limitations section" as a weakness.** This is standard formatting advice, not a substantive weakness.

## Novel Insights

The most valuable insight from these reviews is that the paper's central quantitative claim (F1=0.81) rests on ground-truth human judgments whose provenance is not described in the main text. This is a documentation gap — not a methodological flaw — but it is the critical issue the authors must address. The reviews also surface that the Figure 8 case study, meant to showcase the method's reliability, instead creates confusion through an apparent output contradiction. Beyond these points, the reviews confirm the paper's core contributions are solid and well-supported.

## Suggestions

1. **Document the human annotation protocol in full.** Describe: number of annotators and their qualifications, annotation instructions, whether annotators saw only rendered images or had interactive access, and inter-rater agreement statistics. This is the single most important addition for the paper's claims to be verifiable.
2. **Fix Figure 8.** Resolve the contradiction between "Valid ✓" and the reasoning that the constraint cannot be satisfied. If ✓ is a typo, correct it to ✗.
3. **Add an ablation controlling for information access.** Run LEGO-EVAL with tools restricted to only what a VLM looking at images could access (no `get_object_list`, no coordinate queries) to isolate the pipeline contribution from the oracle-access advantage.
4. **Add a failure analysis.** Analyze where LEGO-EVAL disagrees with human judgments — by constraint type, spatial relation type, or object category — to help the community understand limitations and improve the framework.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>