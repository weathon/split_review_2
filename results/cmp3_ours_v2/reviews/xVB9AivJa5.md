Now I have sufficient calibration data. Let me produce the final review.

## Summary

Blueprint-Bench introduces a benchmark for evaluating spatial reasoning in AI models through the task of converting apartment photographs into accurate 2D floor plans. The dataset contains 50 apartments (~20 photos each) with ground-truth floor plans. The paper evaluates leading LLMs (GPT-5, Claude 4 Opus, Gemini 2.5 Pro, Grok-4), image generation models (GPT-Image, NanoBanana), and agent systems (Codex CLI, Claude Code), finding that most models perform near or below a no-image-input baseline while humans remain substantially superior.

## Strengths

- **Clever and well-motivated task design.** The core idea—testing spatial reasoning by asking models to convert apartment photos to floor plans—is genuinely creative. The argument that this tests a form of intelligence distinct from in-distribution pattern matching (Section 1) is compelling and well-articulated. The input modality is in-distribution while the generation task is not.

- **Model-agnostic evaluation framework.** Using SVG for LLMs, direct image generation for image models, and a Docker environment for agents (Section 2.2) enables cross-architecture comparisons that are non-trivial to implement. This is a practical contribution—the community can use this framework to compare models across fundamentally different architectures.

- **Explicit limitations section (Section 2.4).** The paper candidly acknowledges that the scoring algorithm does not handle room types, that size-ranking errors cascade into connectivity penalties, and that strict formatting rules conflate instruction-following with spatial reasoning. Many benchmarks lack this level of self-critique.

## Weaknesses

### Major

1. **"Random baseline" is misnamed and overstates the findings.** The paper calls its baseline "random" in the abstract, Figure 5, and Figure 7, but Section 2.2 describes it as "generating typical floor plans using LLMs and image generation models without any image input." This is an LLM-prior baseline, not a random process—an LLM already has strong priors about what floor plans look like. The headline claim that "most models perform at or below a random baseline" (Abstract) frames this as a much stronger negative result than "most models are not much better than an LLM guessing without seeing the photos." Renaming the baseline changes the paper's central rhetoric.

2. **No statistical evidence for claimed comparisons.** The paper asserts that GPT-5, Gemini 2.5 Pro, GPT-5-mini, and Grok-4 "statistically perform better than the random baseline" (Section 3) but reports no statistical tests, p-values, confidence intervals, or effect sizes. With 50 apartments, the data is sufficient for paired tests or bootstrap CIs, but none are provided. Error bars in Figures 5 and 7 are described only as "standard deviation" without specifying whether this is per-apartment variance, across epochs, or something else. A benchmark paper making comparative claims needs this rigor.

3. **Experimental design is critically underspecified.** The term "epochs" (lines 112, 117, 152) is never defined. The paper does not report: the number of trials per model per apartment, temperature/hyperparameter settings for any model, whether all models received the same set of photos, or total API/compute budget. These details are essential for reproducibility and for interpreting the reported error bars.

4. **Scoring conflates instruction-following with spatial reasoning, partly contradicting the paper's own stated goal.** The paper notes in Section 2.4 that "Blueprint-Bench should test spatial intelligence, not instruction following" but the scoring algorithm heavily penalizes instruction-following failures. Models like NanoBanana (0.18) and GPT-4o (0.15) score low primarily because they violate formatting rules (Figure 6), not because they lack spatial reasoning. While the paper acknowledges this tension, it still uses these scores to make blanket claims about "spatial intelligence" in the abstract and conclusion without disentangling the two factors.

### Minor

5. **Human baseline is thin.** The human comparison (Figure 7) uses only one participant on 12 of 50 apartments. The paper observes that "all human floor plans were drawn such that the connectivity between the rooms was correct" but this is an anecdotal observation, not a statistically supported finding. A single human on a subset does not establish a reliable human performance ceiling.

6. **Scoring weight justification is absent.** The 50%/20%/10%/10%/5%/5% weighting of the six similarity components (Section 2.3) is stated without justification or ablation. No sensitivity analysis is provided to show that rankings are stable under reasonable weight perturbations.

### Trivial

7. **Minor baseline inconsistency.** The no-image baseline is 0.279 on all 50 apartments (Figure 5) but 0.322 on the 12-apartment subset (Figure 7). If the baseline is generated per-apartment this could be sampling variation, but the paper does not comment on this.

## Nice-to-Haves

- Adding statistical tests (paired t-tests or bootstrap confidence intervals) would substantially strengthen the paper's comparative claims.
- A sensitivity analysis on the scoring weights would increase confidence in ranking stability.
- Expanding the human baseline to multiple participants would provide a more reliable upper bound.

## Removed Points

These points from the input review are flagged for removal with justification:

- *"The random baseline inconsistency reveals a structural problem"* → Removed. If the baseline is generated per-apartment (consistent with Section 2.2 description), subset variation is expected. This is underspecified but not structurally problematic.
- *"Claims about being the first numerical framework are overstated without a survey"* → Removed. The claim is specific to cross-architecture spatial intelligence comparisons; the reviewer offered no concrete counterexample.
- *"Missing comparison to specialized floor plan generators"* → Removed as scope creep. The paper explicitly states (Section 1) that its purpose is "not to find the best possible system."
- *"Per-apartment variance should be discussed more in main text"* → Removed. The appendix provides per-apartment breakdowns; discussing all in main text goes beyond reasonable scope.
- *"Temperature settings and exact prompts not provided"* → Merged into Weakness 3 (experimental underspecification).

## Novel Insights

None beyond the paper's own contributions. The reviewer insight about the baseline mislabeling being the single most impactful fix follows directly from reading the paper's method description against its own framing.

## Suggestions

1. Relabel the baseline from "random" to "no-image baseline" or "LLM-prior baseline" throughout the paper. This changes the framing from "models are worse than random" (overclaimed) to "models are not much better than guessing without visual input" (still meaningful but more honest).
2. Add statistical tests (paired comparisons with confidence intervals) for all model-vs-baseline and model-vs-model claims.
3. Define "epochs" and document all experimental parameters (number of trials, temperatures, sampling strategy) in the main text or appendix.
4. Add a sensitivity analysis on the scoring weights (e.g., vary each weight by ±10% and check ranking stability).
5. Expand the human baseline with more participants to establish a reliable human performance ceiling.

## Score and Decision

**Calibration details.** This paper was compared against the following anchor papers retrieved from the review corpus:

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| SPACE Benchmark (WK6K1FMEQ1) | 6.75 | R1 | Significantly more rigorous methodology, extensive human baselines, comprehensive evaluation. Blueprint-Bench is weaker. |
| ET-Plan-Bench (UiLtbLsiPU) | 4.50 | R1 | Similar level of methodological concerns (task generation pipeline, insufficient evaluation detail). Comparable quality. |
| 3D Reasoning of VLMs (uBhqll8pw1) | 4.00 | R1 | Similar: interesting spatial reasoning evaluation but limited dataset and methodological concerns. Comparable quality. |
| FoREST (9Y6QWwQhF3) | 4.25 | R1 | Spatial reasoning benchmark with similar scope and comparable weaknesses. |
| SynBuild-3D (TCSaLeANpN) | 3.00 | R1 | Dataset paper with no baseline evaluations; Blueprint-Bench has a stronger empirical component. |
| MCTBench (BVACdtrPsh) | 3.00 | R1 | Multimodal cognition benchmark with similar methodology concerns but weaker task novelty. |

**Round-1 bracket:** 3.5–5.5, narrowed to 3.5–5.0 based on comparison with the 3.5–5.5 band anchors.

**Final score:** 4.0. The paper's task design and cross-architecture framework are genuine contributions that distinguish it from weaker benchmark papers (~3.0). However, the evaluation methodology has several significant gaps—misleading "random" baseline terminology that overstates the headline result, absence of statistical tests, critically underspecified experimental parameters, and conflation of instruction-following with spatial reasoning—that prevent it from reaching the rigor expected at the borderline-accept level (~5.5+). A revised version addressing these gaps could be a stronger submission.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>