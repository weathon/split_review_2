Now I have strong calibration. Let me write the final calibrated review.

## Summary

This paper analyzes the role of pooled CLIP embeddings in diffusion transformers, finding them largely inactive as direct conditioning signals (partially in FLUX schnell, fully in HiDream-Fast). The authors then propose "modulation guidance"—a training-free technique that extrapolates between pooled embeddings of positive and negative prompts in modulation space (Equation 3). The method is evaluated across 5 T2I models, 2 T2V models, and 1 image editing model, with human evaluation and multiple automatic benchmarks, showing improvements in aesthetics, complexity, object counting (+9 points on GenEval), and hands correction (+18% win rate).

## Strengths

1. **Clean empirical analysis with practical significance.** Table 1 and Figure 1 provide a well-motivated, quantitative analysis showing that the pooled CLIP embedding contributes little in several contemporary diffusion transformers. This explains the design trajectory in recent models that drop pooled CLIP, and gives practitioners a principled basis for this choice.

2. **Simple, training-free method with broad applicability.** Modulation guidance (Equation 3) is straightforward, adds negligible compute, and is shown to improve generation across multiple model families (FLUX, SD3.5, HiDream, COSMOS, Hunyuan, CausVid), generation modes (multi-step and few-step), and tasks (T2I, T2V, image editing). The dynamic layer-wise variant (Figure 3b) improves the trade-off between aesthetic quality and prompt fidelity.

3. **Breadth of evaluation.** The paper evaluates on 5 T2I models + 2 T2V models + 1 image editing model, uses human side-by-side evaluation across four criteria, multiple automatic metrics (PickScore, CLIP Score, ImageReward, HPSv3), and specialized benchmarks (GenEval, VBench). Improvements on hard problems like object counting (+9 points) and hands correction (+18% win rate) are meaningful.

4. **Attention-based interpretability analysis.** Figure 4 provides a concrete explanation of why modulation guidance helps—it shifts attention toward task-relevant tokens (hands, hand-related tokens). This goes beyond reporting benchmark numbers and shows the mechanism of action.

## Weaknesses

### Fatal
None.

### Major

1. **The claim that modulation guidance provides an "additional degree of freedom beyond CFG" is not adequately supported.** The paper states (line 110) that modulation guidance "can be applied on top of CFG guidance" and "provides an additional degree of freedom," but never systematically compares against optimized CFG scaling. For multi-step models (FLUX dev, SD3.5) that use CFG, the baselines are the original models with *default* CFG settings, not with optimally-tuned CFG. Improvements could partially reflect suboptimal default CFG rather than a genuinely complementary mechanism. The strongest evidence would be a comparison of (a) default CFG, (b) optimally-tuned CFG (scale sweep), (c) modulation guidance alone, (d) modulation guidance + default CFG, and (e) modulation guidance + optimal CFG. Without this, the "additional degree of freedom" claim is unsupported. (Note: the paper does show gains on few-step models that do not use CFG, which is valid evidence for the method's standalone utility.)

2. **Baseline comparisons against prior guidance methods are deferred to the appendix.** The paper reports 34% improvement over Normalized Attention Guidance and 16% over Concept Sliders (line 223), citing Appendix E (Tables 8–9). For a methods paper, these comparisons against prior work are central evidence and should appear in the main paper with full detail (error bars, evaluation protocol, number of trials). Keeping them in the appendix undermines their evidentiary weight and makes the main paper's evaluation feel incomplete.

### Minor

3. **Framing imprecision between the two contributions.** The paper's narrative implies that "reactivating" (line 96) the pooled embedding via modulation guidance is directly motivated by the finding that the pooled embedding is "inactive" in its conventional role. In reality, the guidance method (Equation 3) uses the *difference* between two pooled embeddings y(p₊,t) − y(p₋,t) as a perturbation—which is structurally analogous to CFG or attention guidance methods applied in modulation space. The method would work with any two text embeddings differing along a semantic axis. The paper already uses language like "from a different perspective" (Abstract, line 15), which partly addresses this, but the "reactivate CLIP" framing (line 96) overstates the connection. The two contributions (inactivity analysis, guidance method) are independently valuable and need not be tightly coupled.

4. **Dynamic guidance strategy incompletely specified.** The step-function variant (Figure 3b) relies on two parameters (cutoff layer i and weight w) with no explanation of how they are chosen or whether they generalize across tasks. The evaluation of this variant uses only proxy metrics (PickScore, CLIP Score) on one task (aesthetics on MJHQ), with no human evaluation validating that the claimed better trade-off translates to user preference. The paper mentions (line 126) that "more complex strategies (Appendix C) can yield better results," but without seeing that appendix the reader cannot assess robustness.

5. **Human evaluation protocol is deferred to an inaccessible appendix.** The paper (line 174) states "details in Appendix J" for the side-by-side human evaluation. Key details—number of annotators, qualifications, inter-annotator agreement, specific statistical test used for significance markers (green/red in Table 2), and whether p-values were adjusted for multiple criteria—are not in the main text. While standard practice allows deferring full protocol details, the main text should at minimum report the number of annotators and the statistical test used.

6. **No comparison against simple prompt engineering.** The method requires selecting positive and negative prompts per dimension. A much simpler zero-cost baseline—prepending desired qualities to the prompt (e.g., "high quality, detailed, aesthetically pleasing")—is not compared against. Many practitioners use this approach, and it would contextualize the method's practical advantage.

### Trivial

7. **Some trade-offs are dismissed too quickly.** The paper characterizes drops in relevance/defects as "minor" (line 197), but FLUX dev Aesthetics shows a 12-point drop in relevance (56% original → 44% ours, Table 2), and COSMOS Complexity shows a 6-point drop in defects. These are meaningful degradations that warrant fuller discussion, especially for practitioners deciding when the trade-off is worth it.

## Nice-to-Haves

- A CFG-complementarity experiment (optimally-tuned CFG vs. modulation guidance + default CFG vs. modulation guidance + optimal CFG) would cleanly resolve the "additional degree of freedom" claim.
- Reporting how dynamic guidance parameters (cutoff i, weight w) are selected and whether a single setting transfers across tasks would strengthen the method's practical appeal.
- Moving baseline comparisons (vs. Normalized Attention Guidance, Concept Sliders) to the main paper with full statistical detail would strengthen the method's evidence.
- Adding a prompt engineering baseline would contextualize the method's practical advantage over a zero-cost alternative.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Harsh Critic Critical Issue #1 (structural/methodological gap):** The reviewer framed this as a fatal flaw—that the method doesn't "reactivate" CLIP but uses the difference between embeddings. However, the paper already qualifies its claims with "from a different perspective" (Abstract, line 15) and "reconsidering its role" (line 92). This is a narrative imprecision, not a structural gap. Demoted to Minor #3.
- **Harsh Critic Critical Issue #5 (CLIP-free fine-tuning confound):** The reviewer argued the distillation objective makes CLIP "inactive" by design, creating a confound. However, this is explicitly by design—the paper states "The model behaves identically to the original when the pooled embedding is set to 0" (line 134) and uses the setup to verify that CLIP alone doesn't change behavior. The concern about a training/inference T5 mismatch (unconditional prompt during training vs. unspecified prompt at inference) is a valid sub-concern and is retained in Minor #7, though without the "fundamental confound" framing.
- **Harsh Critic Critical Issue #3 (human evaluation opacity):** The reviewer's demand for full details in the main text is partly about an inaccessible appendix. The core concern (statistical test, annotator count) is valid and retained in Minor #5, but the framing as a major evidential issue is reduced since deferring protocol details to an appendix is standard practice and the appendix likely addresses these points.
- **Criticism about missing appendix content:** Removed per hard rules—the parser strips appendix sections from all papers; they exist in the original submission.
- **General speculative concerns** (e.g., "could the metric be measuring a proxy?") that lack specific anchors in the paper text: removed per filtering discipline.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run a CFG scale sweep** for multi-step models to compare (optimally-tuned CFG) vs. (modulation guidance + default CFG) vs. (modulation guidance + optimally-tuned CFG). This is the cleanest way to support or qualify the "additional degree of freedom" claim.
2. **Move baseline comparisons** against Normalized Attention Guidance and Concept Sliders into the main paper, with error bars and the evaluation protocol clearly stated.
3. **Specify the human evaluation protocol** (number of annotators, inter-annotator agreement, the statistical test used for significance markers) in the main text.
4. **Clarify the dynamic guidance parameter selection** (how cutoff i and weight w are chosen) and show whether a single setting generalizes across tasks or requires per-task tuning.
5. **Tighten the framing** to separate the two contributions more cleanly: (a) pooled CLIP is largely inactive as a conditioning signal, and (b) modulation guidance works by using the differential between pooled embeddings, which is a fundamentally different operation. The "reactivate" language should be replaced with precise mechanistic language.
6. **Add prompt engineering as a baseline** to demonstrate the practical advantage of the method over a zero-cost alternative.

## Score and Decision

**Calibration bracket:** Round 1 bracketing placed the paper between approximately 5.0 and 6.5. I examined several anchors in detail:

| Anchor | Score | Comparison |
|--------|-------|------------|
| Dreamguider (Hpu3KIX8Am) | 4.00 | Rejected; limited contributions over prior work, weak results. Our paper has stronger empirical grounding and broader evaluation. |
| Universal Guidance (pzpWBbnwiJ) | 5.25 | Accepted; simple training-free guidance, but less evaluation breadth than our paper. |
| CFG is a Predictor-Corrector (8K36RkrI7N) | 5.75 | Rejected; theoretical contribution with limited practical implications. Our paper has more immediate practical value. |
| Revamping Diffusion Guidance (b3CzCCCILJ) | 6.00 | Accepted; clean guidance method with solid experiments. Comparable contribution type and rigor to our paper. |
| Eliminating Oversaturation (e2ONKX6qzJ) | 6.00 | Accepted; well-balanced theory/practice, broad experiments. Similar in having a practical guidance improvement with real limitations. |
| Representative Guidance (gWgaypDBs8) | 7.33 | Accepted; more novel perspective and stronger quantitative results than our paper. |
| Superposition of Diffusion Models (2o58Mbqkd2) | 7.33 | Accepted; theoretical depth and diverse applications, but also had notable weaknesses in evaluation. Our paper is less theoretically ambitious but more empirically broad. |

Our paper combines a genuine empirical finding (CLIP inactivity analysis) with a practical, broadly-applicable method. The evaluation breadth is above average for this area. However, the "additional degree of freedom" claim is unsubstantiated, baseline comparisons are deferred to the appendix, and there are minor framing and specification issues. These are all addressable. The paper sits comfortably in the 5.5–6.5 band, closest in profile to the Revamping Diffusion Guidance and Eliminating Oversaturation papers (both 6.0, both accepted).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>