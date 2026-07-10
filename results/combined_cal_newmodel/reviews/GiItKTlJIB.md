## Summary

This paper investigates whether LLMs genuinely depend on their chain-of-thought (CoT) traces for physics problem solving, or merely use them as scaffolding. The authors introduce a deletion framework: they intercept CoT mid-generation, delete tokens via three strategies (end, random, physics-aware), and measure downstream effects on accuracy, answer length, and information overlap. Applied to three open-source models (Magistral, Phi-4, Qwen-A3B) on three physics benchmarks, they find that accuracy remains stable under 40–60% deletion, and that models produce longer final answers that partially reconstruct deleted content ("cramming"). The core idea—probing reasoning dependence via deletion—is novel and well-motivated, but the evaluation has a significant structural weakness that undermines the quantitative claims.

## Strengths

- **Novel and well-motivated research question (Section 1).** The paper cleanly distinguishes faithfulness from accuracy and asks whether LLMs genuinely depend on their CoT scratchpads. This is a timely and important question for AI-for-Science, where reasoning reliability is critical. The framing against prior work (Turpin et al., 2023; Lanham et al., 2023; Lyu et al., 2023) is appropriate.

- **The deletion probing methodology is intuitive and clean (Section 3.2).** The core experimental design — intercept CoT mid-generation, delete tokens, measure downstream effects — is simple, transparent, and easy to understand. The three deletion strategies (end, random, physics-aware) cover complementary dimensions of the problem. This is a genuinely novel evaluation paradigm for probing reasoning dependence.

- **Physics is a well-justified testbed (Sections 1, 2.1).** Physics problem solving demands precise manipulation of equations, units, and numerical calculations, making reasoning faithfulness both operationally important and empirically measurable. The choice of three benchmarks spanning difficulty (UG Physics, PhysReason, PhyBench) is appropriate.

- **The cramming observation is a genuinely interesting empirical finding (Section 4.1).** The observation that models produce systematically longer final answers when CoT is deleted — partially reconstructing missing content — is a real and non-obvious pattern worth reporting, even if its interpretation requires additional controls.

## Weaknesses

### Major

- **Unvalidated LLM judge as the sole evaluation metric (Section 2.4).** The paper scores answers on a 0–1 scale using Claude-4 Sonnet as judge, based on "correctness, derivation accuracy, logic, formatting, and clarity." This is the only measure of "accuracy" throughout the paper — including for the headline claims about accuracy remaining stable under 40–60% deletion. There is no human evaluation, no agreement study, no calibration against ground-truth answers, and no evidence that Claude-4 Sonnet can reliably evaluate physics solutions. For a paper whose central thesis is that LLM reasoning may be unreliable in physics, using another LLM as the sole evaluator without any validation creates a serious circularity concern: the instrument's own reliability on physics evaluation is unexamined. Physics benchmarks typically have ground-truth final answers (numerical values, equations) — the paper does not use exact-match or numerical tolerance as a complementary or validating metric. Until the judge's reliability is demonstrated, every quantitative claim in the paper is on uncertain footing.

- **Cramming interpretation confounded by a plausible boundary artifact (Section 4.1).** The paper observes that when CoT tokens are deleted (especially from the end), the final answer becomes longer, interpreting this as "cramming" — models actively reconstructing missing reasoning. A simpler alternative explanation is a boundary artifact: the model was trained to generate CoT followed by a final answer; when the end of CoT is deleted, it may simply continue generating CoT-like content in the region the experimenter labels as "final answer." The paper does not describe how it segments CoT from the final answer, nor does it control for this alternative (e.g., comparing end deletion against beginning-of-CoT deletion of equal length, or against deletion from the middle of the answer). The random and physics-aware deletion conditions partially mitigate this concern for those strategies, but the boundary artifact remains uncontrolled for the key end-deletion experiments.

### Minor

- **Information-overlap metrics are too coarse for faithfulness claims (Section 4.2).** The paper uses Jaccard similarity and Manhattan distance on bag-of-words token sets to measure whether deleted CoT content reappears in final answers. These metrics ignore word order, equation structure, algebraic transformations, and logical dependencies — exactly the features that distinguish faithful from unfaithful physics reasoning (e.g., `v = u + at` vs `u = v − at` share most tokens but express different equations). The paper acknowledges these are "surface-level" measures, but still uses them to draw conclusions about faithfulness. Equation-aware metrics (symbolic matching, n-gram overlap with n≥2, or dependency graphs) would be needed to support the faithfulness claims.

- **Sample size transparency (Section 3.1).** The calibration study reports that "approximately 5 prompts are sufficient" based on bootstrapping 50 UG-Physics questions with 5 re-runs. However, the paper does not clearly state how many total problems and independent runs were used in the deletion sweeps. With temperature 0.6–0.7 and nucleus sampling, generation is stochastic, and without clear N reporting, it is difficult to assess whether the observed patterns (e.g., "accuracy remains stable until 40% deletion") are reliable or reflect small-sample noise.

- **Practical recommendation exceeds evidence (Section 4.3).** The paper suggests that "early stopping of CoT generation may provide a cost-effective way to save tokens," but the experiments involve deleting tokens from a pre-generated CoT, not stopping generation early. These are different operations, and this recommendation should be caveated accordingly.

### Trivial

- **Model name inconsistency.** The abstract and most of the paper refer to "Magistral," but Section 2.2 (line 59) spells it "Magistrall."
- **"Excess Reasoning" in Figure 1.** This term appears in the figure caption but is never defined or discussed in the body text.

## Nice-to-Haves

- Add a ground-truth answer verification metric (exact match or numerical tolerance) to complement or replace the LLM judge, or validate the LLM judge against human annotations on a representative sample.
- Add a control for cramming: compare end deletion against beginning-of-CoT deletion of equal length, or against deletion from the middle of the answer.
- Adopt equation-aware overlap metrics (symbolic matching with variable substitution tolerance, or at minimum n-gram overlap with n≥2) to meaningfully measure faithful recovery of physics reasoning.
- Clearly report the number of problems and independent runs per deletion condition.
- Provide per-problem or case-study analysis to show whether the deletion robustness pattern is consistent across problems or driven by a subset.

## Removed Points

These points were flagged by the harsh critic but are removed per the filtering rules:

- **Criticism that the "AI-for-Science" framing is overblown and the contribution is incremental** — removed as a subjective opinion about scope rather than a verifiable weakness.
- **Missing implementation details about CoT/answer segmentation and from-the-end deletion mechanics** — the paper states "intercepting CoT mid-generation" and "truncating the last k% of tokens," which are reasonably clear given space constraints. The physics-aware annotation protocol gap is minor enough to be subsumed under other points.
- **Criticism about missing appendix content** — the parser strips appendix sections from all papers; they exist in the original submission.
- **Low absolute scores (0.2–0.5) not discussed** — this is a contextual observation, not a methodological weakness; the paper's claims are about relative changes under deletion, not absolute performance.
- **"No analysis of what 'accurate' means under deletion" and "No discussion of variance across problems"** — these are suggestions for additional analyses, not concrete flaws.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Replace (or at minimum validate) the LLM-as-judge with ground-truth answer verification (exact match or numerical tolerance) for the core accuracy metric. This one change would most improve the paper's evidential foundation.
2. Add a control condition for the cramming analysis: delete the same number of tokens from the beginning of the CoT or from the middle of the answer, to distinguish genuine reconstruction from a boundary artifact.
3. Move from bag-of-words overlap to equation-aware metrics (symbolic matching or at least n-gram overlap with n≥2) to support the faithfulness claims.
4. Report the number of problems and independent runs used in each deletion sweep, and clarify whether error bars are standard deviations or standard errors.

## Score and Decision

**Calibration anchors used:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| On the Hardness of Faithful CoT Reasoning | `1OyE9IK0kx.md` | 5.00 | R1, R2 | Yes | More conventional methodology (applying existing techniques), similar evaluation challenges; my paper has a more novel methodology but a more central evaluation weakness |
| Mind Your Step (by Step): CoT can Reduce Performance | `rpbzBXdo4x.md` | 5.00 | R2 | Yes | Similar probing methodology; my paper has a cleaner experimental design but a more significant evaluation gap |
| Stochastic Parrot on LLM's Shoulder | `LSB2mRJdgZ.md` | 3.75 | R1, R2 | Yes | Physics-focused but more fundamental scope/contribution issues; my paper is clearly above this |
| How Much Can RAG Help the Reasoning of LLM? | `Q6M7bZIo9t.md` | 4.67 | R2 | Yes | Similar probing/analysis study; my paper has a more novel methodology but a more central evaluation weakness |
| To CoT or not to CoT? | `w6nlcS8Kkn.md` | 6.67 | R1, R2 | Yes | Much broader, more comprehensive evaluation; my paper is clearly below this tier |

**Round 1 bracket:** 3.5–5.5. **Round 2 narrowing:** the paper sits above 3.75 (Stochastic Parrot) due to a cleaner methodology and more interesting empirical findings, but below the 5.0 anchors due to a more central evaluation weakness (unvalidated single-metric LLM judge). The favorability comparison confirms: the -1.10 favorability on the LLM judge weakness is the most consequential item, dragging the score below the 5.0-level papers which had less central weaknesses.

**Final score:** 4.5. The paper asks a good question and introduces a genuinely novel methodology, but the reliance on an unvalidated LLM judge as the sole accuracy metric undermines confidence in all quantitative claims. The cramming interpretation also needs a proper control. These are fixable in revision but constitute significant weaknesses in the current submission.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>