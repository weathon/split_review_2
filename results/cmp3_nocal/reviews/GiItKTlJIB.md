## Summary

This paper introduces a deletion-based probing methodology to evaluate how much LLMs genuinely depend on their chain-of-thought (CoT) traces when solving physics problems. By intercepting CoT mid-generation, deleting tokens under three strategies (end, random, physics-aware), and measuring downstream effects on accuracy, answer length, and content overlap, the authors show that models remain accurate under moderate deletions (40–60%) and compensate by "cramming" reconstructed steps into final answers. The work is tested on three open-source models (Phi-4, Qwen-A3B, Magistral) and three physics benchmarks.

---

## Strengths

- **Well-motivated question with clear grounding.** The paper correctly identifies that accuracy-only evaluation is insufficient for scientific reasoning (§1, lines 9–10) and connects to the existing CoT faithfulness literature (Turpin et al., Lanham et al., Lyu et al.) appropriately. The gap between "CoT improves accuracy" and "models genuinely depend on CoT" is real and important for AI-for-Science.

- **Three deletion strategies provide complementary views.** End deletion tests reliance on recency/ordering, random deletion tests robustness to scattered removal, and physics-aware deletion tests whether domain-specific content is differentially important (§3.2, lines 127–148). This variety is the paper's strongest methodological contribution.

- **"Cramming" is a useful descriptive term** for the compensatory lengthening of final answers under deletion (§4.1, lines 158–160). Whether or not the mechanistic interpretation holds, the observation itself—answer length increases systematically when CoT is removed—is a clear and reproducible pattern worth reporting.

- **Physics domain is well-justified.** The paper argues that physics provides structured, testable reasoning with equations, units, and terminology that make faithfulness analysis more tractable than in open-ended domains (§1, lines 15–16). This is a sensible design choice.

---

## Weaknesses

### Fatal
None. No single issue invalidates the paper's core findings. The qualitative patterns (accuracy robust to moderate deletion, answers lengthen to compensate) are reproducible observations that do not depend on precise numerical calibration.

### Major

1. **Unvalidated LLM judge as the sole evaluation metric.** The paper evaluates every output using Claude-4 Sonnet as a judge, scoring 0–1 on "correctness, derivation accuracy, logic, formatting, and clarity" (§2.4, line 82). This is the only quantitative evidence for every result in Sections 3 and 4. The paper reports **no correlation with human expert judgment, no inter-rater agreement, and no calibration analysis** of the judge. This is structurally problematic because the paper's own thesis is that accuracy-based evaluation is insufficient for scientific reasoning, yet its own evidence rests entirely on an unvalidated LLM-based accuracy surrogate. While the relative trends (accuracy drops after X% deletion) are likely less sensitive to judge calibration than absolute scores, the absence of any validation means the quantitative findings are not independently verifiable. **This affects every result in the paper and must be addressed for the claims to be evaluable.**

2. **Conflation of deletion robustness with faithfulness.** The paper defines faithfulness as "the extent to which the scratchpad explicitly reflects the internal computations that lead to the model's final prediction" (§4.3, line 196), but the experiments measure something different: *how much of the CoT can be deleted before accuracy drops*. A model could be perfectly faithful yet robust to deletion (computation distributed across the scratchpad), or deeply unfaithful yet collapse under deletion (deletion disrupts generation). The title, abstract, and conclusion present findings about "faithfulness," "shallow and opportunistic reliance," and "reasoning-dependence gap" (Abstract, line 9) that the experimental design—which observes only external outputs, not internal mechanisms—cannot directly support. The paper acknowledges this partly ("we do not probe internal mechanisms directly," line 158) but the framing throughout overstates what deletion experiments alone can establish.

### Minor

3. **Bag-of-words overlap metrics are limited for structured physics content.** The information overlap analysis uses Jaccard similarity and Manhattan distance on bag-of-words representations (§4.2, Equations 1–2). These are lexical-level measures that cannot distinguish equivalent equations expressed differently (e.g., F=ma vs a=F/m), cannot distinguish genuine content reconstruction from coincidental reuse of domain terminology ("force," "mass," "acceleration" appear in any mechanics answer regardless of whether reasoning is reconstructed), and treat the very structured content the paper selected physics for (equations, units) as undifferentiated tokens. The paper's specific conclusions from these metrics are appropriately cautious ("surface-level similarity rather than genuine fidelity," line 192), but the claim that the domain structure "enables precise quantification" (line 35) overstates what BoW can deliver.

4. **Missing zero-CoT baseline.** The paper varies "Full Reasoning," "Medium Reasoning," and "Low Reasoning" prompts (§2.3, lines 66–74), but the model still generates CoT in all conditions. No condition tests direct answering without any CoT generation. The "40–60% stability" finding is relative to full CoT, but without a true zero-CoT baseline one cannot distinguish whether CoT is partially redundant or whether even heavily deleted CoT provides useful residual context. This limits the interpretation of the paper's central quantitative claim.

5. **Cramming interpretation is underdetermined.** The paper interprets the answer-length increase as compensatory reconstruction (§4.1, lines 158–160). The paper acknowledges it does not probe internal mechanisms, but several alternative explanations are not ruled out: total response-length budget shifts toward the answer when less CoT is produced; longer answers may contain generic physics exposition that happens to overlap lexically with deleted CoT; the length increase could reflect model confusion rather than targeted recovery.

6. **Potential confound in physics-aware deletion.** Claude-4 Sonnet both identifies physics tokens for deletion (§3.2, line 128) and scores the resulting answers (§2.4, line 82). If the judge model is more forgiving of outputs that resemble its own annotation patterns, this creates a confound. At minimum this should be discussed.

7. **Calibration was conducted only on the easiest dataset.** The convergence analysis (§3.1, line 112) uses "50 UG-Physics questions with 5 re-runs" (the easiest dataset) to establish that approximately 5 prompts suffice. There is no validation that this sample size is adequate for harder datasets (PhyBench, PhysReason) or under heavy deletion where variance may increase.

8. **Composite score conflates multiple dimensions.** The single 0–1 score combines correctness, derivation accuracy, logic, formatting, and clarity (§2.4, line 82), making it impossible to tell why scores change under deletion (e.g., are final answers numerically correct with sloppy derivations? or conceptually wrong with plausible-sounding text?).

9. **No statistical significance testing.** Trends are described qualitatively without significance tests, effect sizes, or confidence intervals on the key comparisons (accuracy at different deletion thresholds).

### Trivial
None.

---

## Nice-to-Haves

- An error analysis breaking down what types of errors occur under deletion (arithmetic, conceptual, unit conversion) would be directly relevant to the AI-for-Science framing.
- Reporting the Score metric broken into sub-components (e.g., final-answer numerical correctness separately from derivation quality) would substantially strengthen the analysis.
- A zero-CoT baseline (direct answer without CoT generation) to anchor the deletion sweep results.

---

## Removed Points

- **"Magistral" spelling inconsistency** (line 59 vs. abstract): Removed per rule — typographical/formatting issues are parser artifacts, not author errors.
- **"UG Physics has no size or source citation"**: The paper does cite Xu et al., 2025 (line 17). Dataset size is not given in the main text, which is a minor presentation choice, not an evidential gap.
- **"No exact numbers in tables"**: The reviewer's request for tables with specific accuracy values at each threshold is a presentation preference; figures with error bars are standard for sweep experiments and the main trends are visually clear.
- **"Limitations section doesn't flag X"**: The limitations section (§4.4) is reasonably honest about scope; the fact that it doesn't enumerate every possible limitation is not itself a weakness.
- Any criticism rooted in speculation about what the appendix might contain (the parser stripped appendix sections from all papers; they exist in the original submission).

---

## Novel Insights

None beyond the paper's own contributions. The harsh review does not surface any genuinely novel observation about the paper that the paper itself does not already articulate or imply.

---

## Suggestions

1. **Validate the LLM judge** against human expert evaluation on a representative sample of outputs (e.g., 100–200 answers scored by physics experts). Report correlation, agreement rates, and error patterns. If the judge is reliable, the paper's quantitative findings become credible; if not, the scores need recalibration or replacement.
2. **Adjust the framing** to make clear the paper measures *deletion robustness and compensatory behavior*, not faithfulness of internal reasoning. Replace or qualify "faithfulness" claims throughout the title, abstract, and conclusion to match what the experimental design actually establishes.
3. **Add a true zero-CoT baseline** (direct answer without CoT generation) to allow interpretation of the 40–60% deletion thresholds.
4. **Replace or supplement bag-of-words overlap** with structure-aware metrics that capture equation equivalence, unit consistency, and reasoning-step correspondence.
5. **Break down the composite Score** into sub-scores (e.g., final-answer numerical correctness, derivation quality) to enable finer-grained analysis of how deletion affects different aspects of output quality.

---

## Score and Decision

**MY FINAL SCORE:** <score>6.0</score>

**MY FINAL DECISION:** <decision>Accept</decision>