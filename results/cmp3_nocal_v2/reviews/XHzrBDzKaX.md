## Summary

This paper introduces **VisFACTOR**, a benchmark that digitizes 20 vision-centric subtests from the Factor-Referenced Cognitive Test (FRCT) battery — a well-established psychometric instrument — into a format suitable for multimodal LLM evaluation. The authors evaluate 23 frontier models (GPT, Gemini, Claude, Qwen, LLaMA, etc.) plus a human baseline (31 participants), finding that the best model achieves only 30.17% accuracy versus 78.8% for humans. The paper includes careful chance-level reduction (2.89% on average), a synthetic generation component for future-proofing, and detailed failure analysis (e.g., showing models solve memory tasks via concept-level shortcuts rather than genuine visual memory).

## Strengths

1. **Grounding in established cognitive science.** Adapting the FRCT battery — a validated psychometric instrument with known factor structure — to MLLM evaluation is genuinely novel. The 20 subtests covering 10 FRCT factors (Closure Flexibility, Spatial Orientation, Visualization, etc.) provide a far more diagnostic profile than aggregate benchmarks. This is the first benchmark to systematically bridge psychometric factor analysis with MLLM evaluation.

2. **Careful chance-level reduction (Section 2.3).** The authors reduce random-guess success from 22.47% to 2.89% through decomposed multiple-choice, grouped-consistency items, symmetry variants, and specialized rewrites. No single subtest exceeds 6.25% chance accuracy. This is a concrete methodological advance over prior work (Blink, CoreCognition) where 1/n chance levels can inflate apparent capability.

3. **Thorough model coverage and human baseline (Sections 3.1–3.4).** Evaluating 23 models across all major families (GPT, Gemini, Claude, Qwen, LLaMA, Seed, o-series) with systematic variation of temperature, CoT, and reasoning budget is commendable. The human evaluation (31 participants, 1,540 questions, same digital protocol) provides a credible anchor. The gap between the best model (30.17%) and humans (78.8%) is stark and clearly documented.

4. **Insightful failure analysis (Sections 4.1–4.2).** The MA1 concept-recognition experiment (Table 5) is a highlight: by swapping semantically rich images with abstract line patterns and showing that accuracy collapses, the paper provides concrete evidence that models rely on verbalizable concept-level shortcuts rather than genuine visual processing. The 45-degree angular bias finding (Section 4.2) and the marker-size sensitivity experiment (Figure 4) are specific, reproducible diagnostics.

## Weaknesses

### Fatal

None.

### Major

1. **Construct validity gap: the benchmark may not measure what the paper claims.** The paper repeatedly claims VisFACTOR measures "foundational visual cognition," "gestalt-like perceptual capabilities," and "the precise visual capacities an MLLM truly possesses" (abstract, Section 1, conclusion). This leaps from *performance on digitized FRCT subtests* to *the latent cognitive factors that FRCT was designed to measure in humans* — but the two are not automatically the same. When FRCT was designed, its construct validity rested on factor-analytic work showing that human performance on these paper-and-pencil tasks correlates with specific cognitive factors. Porting these tasks to a digital format shown to MLLMs (which process images through patch-based ViT encoders and reason through text) may fundamentally alter what is being measured. For example, a model's failure on the CF3 Copying Test (6.2% accuracy) could reflect ViT resolution limits rather than a lack of "visual cognition" — especially since the same model achieves 100% when given textual coordinates (Section 4.2). The paper asserts the link between VisFACTOR scores and human-like visual cognition but does not demonstrate it. **This does not undermine the benchmark's value** — VisFACTOR is useful even as a measure of "performance on cognitive-psychology-inspired visual tasks" — but the strongest claims about "genuine" vs. "superficial" visual cognition need to be tempered or supported with additional validation (e.g., verifying that the FRCT factor structure is preserved in model performance patterns).

2. **Synthetic generation validated on only one model (Section 3.3, Table 3).** The "controllable difficulty" claim — a key contribution for future-proofing — is evaluated on GPT-4.1 only. The easy/hard distinction has been verified for exactly one model. Without confirming that multiple models across different families show the same difficulty gradient, or that human performance on synthetic items tracks similarly, the generality of the synthetic generation claims is unsubstantiated. Given that the paper describes this as enabling "unlimited test cases with controllable difficulty" (line 23) and "evaluating increasingly capable models" (line 221), validation on at least 3–5 models from different families is needed.

### Minor

3. **MA1 finding exposes a blind spot but is not extended to other subtests.** The paper elegantly shows that the MA1 memory subtest is solved via concept-level shortcuts rather than visual memory (Section 4.1). But if one subtest is vulnerable to non-visual strategies, others may be too. The P3 Identical Pictures Test (where models score 30–50%) could also be solved via concept-level matching rather than perceptual comparison, but this is not tested. The paper's diagnostic claims about *which specific visual faculties* models lack would be stronger if it checked how many subtests are similarly shortcut-able.

4. **"Middle Score Anomaly" interpretation is conceptually overstated (line 188).** The paper argues that intermediate scores (30–50% on P3) suggest models "lack genuine reasoning capabilities" because "humans can either solve this task almost perfectly or fail entirely." A model could genuinely possess *partial* perceptual capability — detecting some types of image differences (e.g., color) but not others (e.g., subtle geometry). The intermediate score would then reflect the fraction of items within its actual (incomplete) capabilities, which is consistent with genuine but bounded visual perception. The bimodal all-or-nothing structure the paper assumes for humans does not necessarily apply to models.

5. **Some human subtest scores are surprisingly low, raising digitization-fidelity questions (Table 4).** CS1 (Gestalt Completion) at 35.0%, SS2 (Choosing a Path) at 55.0%, RL2 (Diagramming Relationships) at 51.7%, and VZ2 (Paper Folding) at 58.3% are well below what one might expect for "foundational" visual tasks administered to university students. Without comparison to published FRCT norms from the original paper-and-pencil format, it is unclear whether the digital protocol introduced artifacts (e.g., image resolution, cropping, digital administration format affecting performance). The 35% on CS1 — a Gestalt Completion task — is particularly concerning for a benchmark claiming to measure basic perceptual ability.

6. **No confidence intervals, standard errors, or significance tests reported anywhere.** For the human baseline (31 participants, ~20 items per subtest), reporting variance is important — a few participants could substantially shift the mean on low-item-count subtests. For temperature experiments (Table 2), the claim that "performance fluctuates only marginally" should be backed by quantitative evidence beyond visual inspection. For the marker-size experiment (92% → 80% → 68%, Figure 4), error bars are needed.

7. **Per-subtest item counts not reported; subtest-level reliability not assessed.** The paper does not state how many items each subtest contains in the digitized VisFACTOR version. This matters because subtests with very few items yield noisier estimates. Internal consistency measures (e.g., Cronbach's alpha) for the human data would strengthen claims that the subtests measure something coherent.

8. **Human evaluation protocol lacks key details.** "31 university students" — were they screened for normal/corrected vision? Were they native speakers of the test language? What were the time limits per item? Were they compensated? These details matter for assessing the human baseline's credibility.

### Trivial

9. **The claim that "MLLMs' text-based reasoning forces step-by-step traversal" (line 272) attributes a processing mechanism not directly tested.** CoT was not required for most models in the main evaluation; the paper's own analysis shows CoT sometimes hurts. The mechanistic attribution ("forces step-by-step traversal") is speculative.

10. **RL2 inclusion rationale is somewhat circular.** RL2 is included because it "demands visual reasoning" (Section 2.1), but the paper later explains human-model parity by noting RL2 "relies more on textual object knowledge, a known strength of MLLMs rather than visual reasoning" (Section 3.4). If RL2 does not actually require visual reasoning, its role in a benchmark measuring visual cognition should be clarified.

## Nice-to-Haves

- Validate construct validity by checking whether the FRCT factor structure (correlations among subtests loading on the same factor) is preserved in model performance patterns. If subtests within the same factor show correlated performance across models, this would suggest the factor structure partially transfers.
- Verify the synthetic difficulty gradient across multiple model families (at least 3–5 models from different families).
- Report per-subtest item counts and add confidence intervals or bootstrapped standard errors.
- Compare human digital scores against published FRCT norms (if available) to quantify digitization fidelity.

## Removed Points

These points from the input review were removed; treat them with caution:

1. **"45 of the 65 vision-relevant subtests were excluded because they accept text answers"** — Factually incorrect. The paper states 45 subtests *can* accept text answers, and those demanding visual reasoning were *included* (20 selected from 45). The reviewer misread the selection criteria.
2. **"Single-digit scores" on human subtest performance** — Factually incorrect. CS1=35.0%, SS2=55.0%, RL2=51.7%, VZ2=58.3% — none are single-digit. The underlying concern about digitization fidelity is retained as Minor #5.
3. **Table 1 formatting / garbled column headers** — Parser artifact; not present in the original submission.
4. **Section 2.2 instruction-summarization confound** — The paper already mitigates this with human reconciliation. The concern is acknowledged but insufficient to retain as a standalone weakness.
5. **"Benchmark covers only ~28% of the FRCT battery"** — The paper never claims comprehensive coverage of FRCT; selection criteria are clearly documented. Scope creep.
6. **Demanding evidence that improving VisFACTOR scores transfers to downstream applications** — The paper does not claim to demonstrate transfer. Scope creep.
7. **Abstract framing commentary ("MMBench vs. VisFACTOR overstates failure")** — Commentary on rhetorical choices rather than a substantive weakness.

## Novel Insights

The most novel insight from the review process is the tension between the paper's strongest asset (its psychometric grounding) and its weakest point (construct validity for models): the same FRCT factor structure that makes the benchmark principled for humans is asserted but not verified for models. The MA1 concept-recognition experiment (Table 5) is both a strength (revealing how models "cheat" on visual tasks) and a vulnerability (showing that subtest → factor mapping is not tight for models). This double-edged nature — where the paper's own diagnostic tools partially undermine its diagnostic claims — is a genuinely interesting meta-insight that the authors could productively address in a limitations section.

## Suggestions

1. **Temper the strongest construct-validity claims.** Replace "human-like visual cognition" / "gestalt-like perceptual capabilities" with more precise phrasing like "performance on cognitive-psychology-inspired visual tasks." The benchmark is valuable either way.
2. **Validate synthetic generation on at least 3–5 models from different families** (not just GPT-4.1) to substantiate the "controllable difficulty" claim.
3. **Add variance reporting** — confidence intervals or bootstrapped standard errors for all main results, especially the human baseline.
4. **Report per-subtest item counts** and, if possible, inter-subtest correlations or internal consistency for the human data.
5. **Add a limitations paragraph** explicitly discussing construct validity, the MA1 shortcut issue for other subtests, and the digitization-fidelity gap (no comparison to original FRCT norms).
6. **Clarify the human evaluation protocol** — include vision screening, language background, time limits, and compensation details.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>