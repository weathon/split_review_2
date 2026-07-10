Now I have sufficient calibration data. Let me synthesize everything and write the final review.

## Summary of Anchor Comparisons

**Calibration Anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| On the Hardness of Faithful CoT | .../1OyE9IK0kx.md | 5.00 | R1 | Yes | Most topically similar. Both study CoT faithfulness in LLMs. That paper had more extreme polarization (strengths up to 12.69, weaknesses down to -7.06). My paper has a stronger novel methodology but slightly less extreme strengths. |
| Understanding CoT Through Info Theory | .../ouRX6A8RQJ.md | 6.40 | R1 | Yes | Similar analytical framing but more theoretical. Strengths 7-13, weaknesses mostly positive. |
| To CoT or not to CoT? | .../w6nlcS8Kkn.md | 6.67 | R1 | Yes | Broader meta-analysis, accepted. No weaknesses below -1.28. My paper's -0.68 weakness puts it clearly below this. |
| Mind Your Step | .../rpbzBXdo4x.md | 5.00 | R2 | Yes | CoT performance analysis. Weaknesses down to -6.77. Similar score bracket. |
| Can LLMs Reason? 3-SAT | .../FP77VtEuaT.md | 5.25 | R2 | Yes | Empirical analysis of LLM reasoning limits. Weaknesses down to -6.92. Similar bracket. |

**Round 1 bracket**: Score between 4.5 and 6.0, based on the gap between "On the Hardness of Faithful CoT" (5.00) and "To CoT or not to CoT" (6.67).

**Narrowing**: My paper shares with the 5.00 anchors the pattern of a genuinely interesting core question backed by a solid methodology, but with a few significant methodological gaps that prevent the conclusions from being fully supported. My paper's most negative weakness (LLM judge unvalidated, fav=-0.68) is less extreme than the worst weaknesses in the 5.00 anchors (-7.06, -6.77, -6.92), and the paper's novel deletion methodology is a genuine strength. However, it lacks the very high-favorability strengths (>10) seen in some 5.00 anchors. Balancing these, the paper sits near the top of the borderline-reject range.

**Final score: 5.0** — The paper has a genuine methodological contribution and interesting empirical findings, but the three major issues (faithfulness/dependence mismatch, mechanical confound in overlap metrics, unvalidated LLM judge) prevent acceptance in the current form.

---

## Final Review

## Summary

This paper introduces a deletion-based probing framework to study how open-source reasoning LLMs (Phi-4, Qwen-A3B, Magistral) use chain-of-thought scratchpads in physics problem solving. By intercepting CoT mid-generation, deleting tokens via three strategies (end, random, physics-aware), and measuring downstream effects on accuracy, answer length, and information overlap, the paper documents a "cramming" phenomenon: models maintain accuracy under heavy deletion (40–60%) by regenerating missing reasoning steps in final answers. The authors interpret these findings as evidence that CoT usage is "shallow and opportunistic."

## Strengths

- **The deletion framework is a clean, novel experimental design.** Intercepting the scratchpad mid-generation, deleting tokens, and observing downstream effects is a natural and principled way to probe dependence on CoT content. The three deletion strategies (end, random, physics-aware) provide complementary views of how models respond to different types of content removal (Section 3.2). This is the paper's strongest methodological contribution.
- **The "cramming" observation is genuinely interesting and well-documented.** The finding that final answer length increases under deletion (Figures 5, 6, 11) and that information overlap rises (Figure 7) documents a real behavioral phenomenon. The term "cramming" usefully labels this compensatory behavior.
- **Strong empirical breadth.** The paper compares three distinct open-source reasoning models (Phi-4, Qwen-A3B, Magistral) across three physics benchmarks of varying difficulty, providing a reasonably broad empirical basis (Sections 2.1, 2.2).
- **Reasonable statistical calibration.** The calibration study with bootstrapped confidence intervals (Section 3.1) demonstrates attention to statistical rigor in determining sample sizes, and the paper reports standard error bands in its overlap figures (Figure 7).

## Weaknesses

### Major

**1. The paper frames its contribution as being about CoT faithfulness but the experiments primarily measure CoT dependence.** The paper defines faithfulness as "the extent to which the scratchpad explicitly reflects the internal computations that lead to the model's final prediction" (Section 4.3). However, the deletion experiments test whether models *need* their CoT tokens to produce correct answers — i.e., *dependence*. These are different concepts: a model could faithfully use its CoT while being robust to deletion of up to 40–60% of tokens, because the remaining tokens contain the essential structure, or because it can reconstruct from partial information using internalized knowledge. The conclusion that CoT traces are "shallow and opportunistic" (Abstract) is an inference about faithfulness drawn from dependence evidence. This mismatch between what is measured and what is claimed weakens the central argument. The paper would be significantly stronger if reframed as a study of CoT dependence and robustness to deletion, with faithfulness implications treated as suggestive rather than conclusive.

**2. The information overlap metrics have a mechanical confound not addressed by the analysis.** Information overlap is defined as the intersection between deleted CoT content and new content in the final answer, measured via Jaccard similarity and Manhattan distance on bag-of-words (Section 4.2). As the deletion fraction increases, the set of deleted CoT tokens grows larger, which mechanically increases the ceiling on possible token overlap regardless of whether the model is genuinely reconstructing reasoning. The rising overlap trends in Figure 7 may partly reflect this statistical artifact. The paper does not control for this base-rate effect (e.g., by normalizing by deleted set size or comparing against a random-token baseline).

**3. The accuracy evaluation relies entirely on an unvalidated LLM judge.** All accuracy scores are computed using Claude-4 Sonnet as a judge (Sections 2.4, 3.1), scoring 0–1 based on correctness, derivation accuracy, logic, formatting, and clarity. There is no human evaluation, no comparison against expert grading, no inter-rater reliability metric, and no validation that the LLM judge's physics grading is accurate. This is a significant evidential weakness — especially since the paper itself argues that LLM reasoning can be unreliable. Even a small-scale human verification (e.g., 50 answers scored by a physics tutor) would substantially strengthen the results.

### Minor

**4. The deletion methodology lacks a control condition to distinguish CoT-specific effects from general LM robustness to corrupted inputs.** When tokens are removed from an autoregressively generated scratchpad mid-generation, the remaining prefix is truncated/corrupted in ways the model was never trained on, creating discontinuities. The observed "cramming" could be a general text completion mechanism triggered by any unnatural input structure rather than something specific to CoT reasoning deletion. The paper does not include a non-reasoning control (e.g., deleting the same fraction of tokens from a filler scratchpad). The comparison across three deletion strategies partially addresses this concern but does not substitute for a proper baseline.

**5. Model naming is inconsistent.** The model is referred to as "Magistral" (Abstract), "Magistrall" (Section 2.2), and "Magistral-Small" (Related Works), creating confusion about the exact model evaluated.

**6. The claimed deletion thresholds are presented as clean breakpoints but the underlying data appear more graded.** The paper states accuracy "remains stable until approximately 40% deletion" for end deletion and "approximately 60%" for random deletion, but Figure 4 suggests that for some model-dataset combinations accuracy declines gradually well before these thresholds. The claims would benefit from more precise quantification.

### Trivial

None.

## Nice-to-Haves

- Adding a non-reasoning control condition for the deletion experiments (e.g., deleting the same fraction of tokens from a non-reasoning scratchpad) would strengthen the claim that cramming is CoT-specific.
- Analyzing error types under deletion (algebraic vs. conceptual vs. unit conversion errors) would enrich the connection to the physics-specific motivation.
- Reporting error bars or statistical tests for the main deletion sweep accuracy results (not just the calibration study) would improve precision.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Information overlap metrics are surface-level token reuse"** — The paper itself acknowledges this limitation (Section 4.2, line 192: "surface-level similarity rather than genuine fidelity"). This is not a hidden flaw but a stated caveat. The mechanical confound (kept as Major #2) is a separate, unaddressed issue.
- **"UG Physics dataset description is vague"** — The paper provides a standard description with citation. Standard practice.
- **"No CoT baseline"** — The paper directly compares direct answer generation vs. CoT prompting (Figure 2), contradicting this claim.
- **"Needs larger datasets / more models / more domains"** — Scope-expansion demands; the paper explicitly scopes to physics.
- **"Missing appendix details / formatting artifacts"** — Parser-stripped content and parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the paper's central claims** from CoT "faithfulness" to CoT "dependence" and "robustness to deletion." The deletion experiments cleanly measure dependence; the faithfulness implications can be discussed but should not be presented as primary findings.
2. **Control for the mechanical confound in the overlap metric** by normalizing by deleted set size or comparing against a random-token baseline.
3. **Validate the LLM judge** with at least a small-scale human evaluation (e.g., 50–100 responses graded by a physics domain expert).
4. **Add a non-reasoning control condition** for deletion experiments to establish that cramming is CoT-specific rather than a general robustness phenomenon.
5. **Report error bars or confidence intervals** for the main deletion sweep accuracy results.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>