## Summary

This paper presents GRAID, a framework that generates high-quality spatial reasoning VQA data using only 2D bounding boxes from standard object detectors, explicitly avoiding the 3D reconstruction errors and generative hallucinations that plague prior methods. The authors apply GRAID to three autonomous driving datasets (BDD, NuImages, Waymo), producing 8.5M+ VQA pairs across 22 templates spanning spatial relations, counting, ranking, and size comparisons. They further introduce SPARQ, a predicate-based early-rejection system that accelerates generation by up to 1400×. Human evaluation shows 91.16% pair validity, and fine-tuning on GRAID data produces models that generalize across datasets, question types, and established VQA benchmarks.

## Strengths

- **Clean, principled methodology.** The insight that qualitative spatial relationships (left/right, above/below, closer/farther, larger/smaller, counting) can be reliably determined from 2D bounding boxes alone is clearly articulated and directly addresses a genuine weakness in prior work. The method is simple, reproducible, and requires no architectural changes to VLMs. (Section 3)

- **Large-scale, high-quality dataset generation.** Generating 8.5M VQA pairs across three AV datasets with 91.16% human-validated pair validity is a substantial undertaking. The hierarchical breakdown (Fig. 2) shows broad coverage across five cognitive categories. If released post-review, this would be one of the largest high-quality spatial VQA resources available. (Section 4, Table 2)

- **SPARQ's predicate-based early rejection is well-designed and documented.** The measured speedups are concrete — predicates complete in 5.17ms vs. 46.95ms for full realization (9×) on RightOf, and over 1407× on LargestAppearance (0.02ms predicate time with 78.8% predicate success implying realization success). (Section 3.2, Algorithm 1)

- **Cross-dataset and cross-question-type generalization is convincingly demonstrated.** RQ1 shows 31%→80.7% on held-out GRAID-BDD and 38%→67.1% on unseen GRAID-NuImages. RQ2 shows training on only 6 question types improving performance on 10+ held-out types (overall +47.5pp on BDD, +38.0pp on NuImages). These results provide genuine evidence that models learn transferable spatial concepts rather than memorizing dataset patterns. (Section 5, Figure 3)

## Weaknesses

### Major

- **The headline claim compares against a community re-implementation, not the original method, with mismatched metrics.** The paper's most prominent numerical claim — "91.16% human-validated accuracy compared to 57.6%" (abstract) — compares GRAID's *unique-pair validity* (question AND answer correct) against OpenSpaces' *answer error rate* from the community implementation of SpatialVLM. These are different metrics presented as directly comparable. The paper reports the sub-metrics needed to reconstruct cleaner comparisons (question validity: 95.58% GRAID vs. 58.4% OpenSpaces; answer validity: 93.69% GRAID vs. 42.4% OpenSpaces, derived from lines 182–184) but uses the mismatched framing in the abstract. Additionally, OpenSpaces is a community re-implementation of SpatialVLM of uncharacterized fidelity; the paper does not describe how it differs from the original pipeline, so the comparison's relevance to the stated prior-art baseline is unclear.

- **Human evaluation lacks inter-annotator agreement and small sample sizes.** The OpenSpaces evaluation uses 250 questions (50 images × 5 questions) and the GRAID evaluation uses 317 questions, both with 4 evaluators. No inter-annotator agreement metric (e.g., Cohen's κ) is reported for either evaluation. Without this, the numerical gap cannot be fully distinguished from evaluator variability. For SpatialVLM's metric (distance/size) questions, the paper does not explain whether human evaluators systematically applied the [50%, 200%] tolerance or relied on their own visual judgment of distance — a distinction that matters when determining answer correctness without 3D ground truth (lines 82, 182).

### Minor

- **The IoU=0 requirement in Algorithm 1 excludes overlapping objects from left/right questions.** Objects that partially overlap in 2D (e.g., a person partly occluded by a car) will never generate left/right questions even when the spatial relationship is meaningful. This is a design choice that limits question coverage for real-world scenes with occlusion (Algorithm 1, line 127).

- **RQ2 regression on threshold-based counting questions warrants deeper analysis.** The paper attributes regression on `LessThanThresholdHowMany` and `MoreThanThresholdHowMany` to "overfitting" (line 200). However, these questions require a different type of spatial primitive (threshold-based quantity estimation) than the six training question types, and the regression may instead indicate that learned primitives do not transfer to all unseen types. A more precise diagnostic would strengthen the claims about generalization.

### Trivial

- None beyond what can be addressed through revisions to the presentation and analysis above.

## Nice-to-Haves

- **Benchmark against the original SpatialVLM dataset** (or at minimum characterize how OpenSpaces differs and explicitly acknowledge this limitation). This would eliminate the fidelity ambiguity in the headline comparison.

- **Report human evaluation using a balanced design**: same evaluators, same metric, same image sources for both GRAID and OpenSpaces, with inter-annotator agreement.

- **Error analysis of GRAID's 28 problematic VQA pairs.** The paper aggregates errors but does not categorize them (detector failures? ambiguous spatial configurations? template logic errors?). Understanding failure modes would help users of the framework.

- **Ablation showing how object detector accuracy affects GRAID output quality.** The paper uses ground-truth AV annotations to evaluate GRAID "in isolation" (line 155), but real users would rely on imperfect detectors. An experiment with varying detector quality would clarify practical robustness.

## Removed Points

These points from the input review were removed after cross-checking against the paper; they are listed here for transparency but should be disregarded in evaluation:

- **"Open-source implementation by authors" checked in Table 1 but dataset/code will be released after review period** — Removed per hard rule: criticisms about release status of cited artifacts are not permitted.
- **Typo "Llama 3.2B 11B" and Figure 3 caption garbling** — Removed per hard rule: these are parser-induced formatting artifacts, not author errors.
- **Missing Tables 4/5/6 in main text** — Removed per hard rule: appendix content is stripped by the parser; the tables exist in the original submission.
- **RQ3 hyperparameter parity unconfirmed** — Removed per hard rule: details are in the appendix (stripped by parser); the main text states "the same SFT experiment" was performed (line 202).
- **Interpretability methods listed in Section 3.1 are tangential** — Removed: the paper uses them to illustrate the maturity of 2D detection tooling, not as a core part of the method. This is a stylistic observation, not a substantive weakness.
- **Post-correction asymmetry (91.16% claimed as post-correction)** — Removed: re-reading shows 91.16% is calculated from the raw 28/317 problematic instances (line 184), and corrections are a separate step yielding "even higher validity." The reviewer misread this.
- **All experiments are in the driving domain** — Removed: the paper explicitly scopes this as an instantiation choice (line 53), not a domain limitation, and RQ3 tests on non-driving benchmarks (A-OKVQA, BLINK, NaturalBench, etc.) partially address this.

## Novel Insights

None beyond the paper's own contributions. The core findings — that 2D-only qualitative geometry suffices for high-quality spatial VQA data generation, and that models trained on such data generalize across datasets, question types, and benchmarks — are well-supported by the experiments presented.

## Suggestions

1. **Reconcile the headline comparison.** Restructure the abstract and Section 4's introduction to compare like-with-like: report GRAID's answer-validity rate (93.69%) and question-validity rate (95.58%) alongside OpenSpaces' corresponding figures (42.4% and 58.4%), then use the unique-pair validity (91.16%) as a conservative aggregate. Acknowledge that the comparison is against the community re-implementation OpenSpaces, not the original SpatialVLM, and characterize any known differences.
2. **Report inter-annotator agreement** for all three human evaluations (SpatialRGPT, OpenSpaces, GRAID).
3. **Add an error analysis** breaking down the 28 problematic GRAID instances by error type (detection, annotation, template, ambiguity).
4. **Consider relaxing the IoU=0 constraint** for left/right questions to handle partial occlusion, or explicitly justify and document this design limitation.
5. **Clarify the RQ2 regression analysis** on threshold-based counting — is it overfitting, or a genuine limitation of the learned primitives?

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>