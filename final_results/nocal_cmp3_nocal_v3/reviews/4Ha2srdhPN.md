## Summary

GRAID proposes a framework for generating high-fidelity spatial reasoning VQA data using only 2D bounding boxes, avoiding the cascading errors of monocular 3D reconstruction and hallucinations from caption-based generation. It operationalizes this through SPARQ (a predicate-based early-rejection system) and produces over 8.5M VQA pairs across three driving datasets (BDD100k, NuImages, Waymo). Human evaluation finds ~91% validity for GRAID data, and fine-tuning experiments show cross-dataset generalization (e.g., +29.1% on NuImages after training on 10% of BDD) and transfer to held-out question types and external benchmarks.

## Strengths

- **Well-motivated and clean core insight.** The observation that qualitative spatial relationships can be reliably determined from 2D bounding boxes alone (Section 3.1, Table 1), sidestepping the cascading errors of monocular depth estimation and 3D reconstruction, is both sound and practically valuable. The paper articulates this clearly and contrasts it with prior approaches that require 3D estimates or caption-based generation.

- **SPARQ is a genuinely useful engineering contribution.** The predicate-based early-rejection design (Section 3.2) is elegant, and the reported timing breakdown (predicate: 5.17ms vs. realize: 46.95ms for the `RightOf` template; up to 1407× speedup for `LargestAppearance`) makes the efficiency argument concrete. The insight that simple geometric predicates are often sufficient conditions for question feasibility is non-trivial.

- **RQ1 and RQ2 provide the paper's strongest evidence.** Training on 10% of GRAID-BDD and seeing +29.1% on GRAID-NuImages (completely different city/visual domain) is compelling evidence of transferable learning. Even more striking: training on only 6 of 22 question types and improving on over 10 held-out types including an entire fifth category (Size & Aspect) not seen in training (Figure 3) — this directly supports the claim that the data teaches *spatial primitives* rather than template-specific patterns.

- **Human evaluation establishes a meaningful quality baseline despite limitations.** Evaluating 317 GRAID pairs and 250 SpatialVLM pairs across four human judges with a structured protocol is a reasonable effort. The resulting ~91% validity rate for GRAID is a nontrivial achievement for an automated pipeline, and the gap with the SpatialVLM comparison set is large enough to be informative even accounting for the metric issues discussed below.

## Weaknesses

### Major

- **The headline comparison (91.16% vs. 57.6%) compares different quantities across sections, and the Introduction contradicts the body.**  
  Three issues here, all anchored to the paper's text:
  1. **Abstract vs. body metric mismatch.** The abstract (line 9) reports "57.6% human validation rate" for SpatialVLM and "91.16% human-validated accuracy" for GRAID, implying a direct like-for-like comparison. However, the body (line 182) reports **two distinct numbers** for SpatialVLM: 41.6% of questions were invalid (→ 58.4% valid), and separately 57.6% of answers were incorrect (→ 42.4% correct). The 57.6% figure refers to **answer incorrectness**, not overall validity. For GRAID, the 91.16% is the combined rate of VQA pairs with neither question nor answer issues. These are different composite metrics, and the abstract does not define them uniformly.
  2. **Introduction directly contradicts the body.** Line 51 states "our human evaluation reveals that only **57.6% of questions are valid**." But the body (line 182) reports 104/250 = 41.6% were not valid questions, i.e., **58.4% of questions were valid** — not 57.6%. The 57.6% in the body refers to answer incorrectness, not question validity. The Introduction has used the wrong number for the wrong quantity.
  3. **"Over 91.16%" is a precision artifact.** 28/317 = 8.83% problematic → 91.17% valid. The "over 91.16%" phrasing (lines 53, 60, 293) treats a fixed sample proportion as if it had sub-percentile precision.

  **Why this matters:** The paper's central comparative claim — that GRAID data is dramatically higher quality than prior work — appears directionally correct (even re-computing like-with-like leaves a large gap), but the numbers as currently presented in the abstract and introduction are imprecise or factually wrong as written. This must be corrected.

- **RQ3 comparison between GRAID and OpenSpaces (SpatialVLM) is underspecified.**  
  The paper reports fine-tuning the same four VLMs on GRAID-BDD and on OpenSpaces, evaluated on five benchmarks (Section 5, line 202; Tables 4-6 in appendix). However, two confounds are not discussed:
  - **Dataset size.** GRAID-BDD (without depth) contains 3.34M training QA pairs. The paper does not report the size of OpenSpaces (number of QA pairs or images). If OpenSpaces is substantially smaller, training for the same number of steps gives GRAID an advantage that has nothing to do with data quality.
  - **Question type distribution.** OpenSpaces contains metric (distance/area) questions with 3D-estimated measurements, while GRAID contains qualitative (comparative) questions. Different question types test different capabilities, and the benchmarks used may favor one type over the other. The paper does not discuss this.

  The scale of the reported improvements (e.g., 32.5% on A-OKVQA for Llama 3.2) suggests meaningful gains beyond these confounds, but transparency about dataset sizes and a discussion of how the question-type mismatch affects interpretation would significantly strengthen the claim.

### Minor

- **The "overfitting" explanation for the `LessThanThresholdHowMany` regression is speculative.**  
  The paper (line 200) observes regression on `LessThanThresholdHowMany` / `MoreThanThresholdHowMany` and attributes it to "overfitting." However, the model trained for only 200 steps on ~18K examples, completing less than a full epoch. Classical overfitting at this stage is unlikely. A more plausible alternative is that counting-with-threshold requires compositional skills not covered by the 6 training question types (which include plain counting but not threshold-based counting). The paper should discuss this more carefully.

- **RQ1/RQ2 results are reported as single-run point estimates without variance.**  
  The paper reports before/after accuracies (e.g., "31% to 80.7%," lines 198-199) without confidence intervals or multiple seeds. For 1,000 held-out examples, a single run could be noisy. Reporting results over 3 runs with standard deviations would strengthen the quantitative claims.

### Trivial

- **SPARQ timing statistics are reported as point estimates without variance.**  
  Line 136 reports "5.17ms" and "46.95ms" averages, and the 1407× speedup for `LargestAppearance`, without any indication of variance or distribution. A brief note on variability would help.

## Nice-to-Haves

- Define "valid question" vs. "correct answer" unambiguously at the start of Section 4, and ensure every use of the 57.6% and 91.16% figures throughout the paper references the same metric for both datasets.
- Report OpenSpaces dataset size (number of QA pairs, images) alongside GRAID-BDD in the RQ3 section, and discuss whether the benchmarks might favor qualitative over metric reasoning questions.
- The depth-question extension (Section 4) is presented as optional but its existence slightly dilutes the "no 3D errors" narrative. A sentence clarifying that all main results use the without-depth variant would help.

## Removed Points

These points are flagged to be removed from the harsh critic's review; treat them with caution:

- **Concern about missing appendix tables (4, 5, 6).** The parser strips appendix content from all papers; these tables exist in the original submission. Removed per hard rule.
- **"The use of depth with configurable thresholds somewhat undercuts the paper's core thesis."** The paper explicitly states depth questions are an extension/demonstration of extensibility (line 157), and the main results rely on the without-depth variant. Removing speculative framing that the depth extension "dilutes" the core thesis.
- **Criticism that Waymo variant is "practically useless."** The paper acknowledges the size difference transparently and uses it for demonstration, not training. Not a substantive weakness.
- **"Over 91.16%" phrasing nitpick.** This is a trivial rounding observation, not a weakness that merits space. Removed to Trivial.
- **Generic strengths about problem importance.** The harsh critic's strengths are grounded in specific evidence; none removed.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one useful observation: the metric inconsistency between the abstract/introduction and the body is not just a presentation issue — it reveals that the paper's flagship comparative claim ("91.16% vs 57.6%") is built on different operational definitions for the two datasets. The direction of the result is robust, but the precision of the headline is misleading. This is a concrete, verifiable flaw that the paper should acknowledge and fix.

## Suggestions

1. **Fix the headline numbers.** In the abstract and introduction: (a) use the same metric for both GRAID and SpatialVLM (e.g., overall VQA-pair validity, or separate question-validity and answer-correctness rates); (b) correct the Introduction's "57.6% of questions are valid" to "57.6% of answers were incorrect" (consistent with line 82 and line 182) or replace with the correct 58.4% question-validity figure.
2. **Add dataset-size and training-budget transparency to RQ3.** Report the number of QA pairs in OpenSpaces and, if sizes differ, run an ablation matching by number of unique training examples rather than steps.
3. **Replace the "overfitting" speculation** for the threshold-counting regression with a discussion of why these particular question types might require compositional skills not covered by the 6 training types.
4. **Add confidence intervals or multiple-seed results** for RQ1 and RQ2 to give readers a sense of variability.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>