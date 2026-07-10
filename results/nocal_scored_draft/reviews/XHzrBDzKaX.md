## Summary

VisFACTOR is a benchmark that digitizes 20 vision-centric subtests from the Factor-Referenced Cognitive Test (FRCT) battery — a well-established cognitive psychology assessment — into an automated multimodal evaluation for MLLMs. The paper evaluates 23 frontier models and finds that the best model achieves only 30.17% accuracy, with systematic failures on mental rotation, spatial relation inference, and figure-ground discrimination. A parametric generator produces unlimited difficulty-controlled test cases for future-proofing.

## Strengths

- **Principled construct validity from cognitive psychology.** The benchmark is grounded in the FRCT battery with 20 subtests covering 10 established cognitive factors (Closure Flexibility, Spatial Orientation, Induction, etc.), giving it a theoretical backbone that most MLLM evaluation benchmarks lack. (§2.1)

- **Rigorous control over chance-level accuracy.** The paper reduces the average random-guessing baseline to 2.89% with no single subtest exceeding 6.25% through decomposed multiple-choice, grouped-consistency items, symmetry variants, and specialized rewrites — a genuine methodological improvement over benchmarks with 25% or 50% chance floors. (§2.3)

- **Comprehensive and current model coverage.** 23 frontier models across 7 model families (GPT, Gemini, Claude, LLaMA, Qwen, Seed, Moonshot) with temperature ablations, CoT ablations, and both reasoning and non-reasoning variants. (§3.1, Table 1)

- **Meaningful human baseline.** 31 participants completing 1,540 questions under the same digital protocol provides a credible calibration point; the gap between 78.8% (human) and 30.17% (best model) is stark and well-documented. (§3.4)

- **Diagnostic failure analysis with concrete findings.** Section 4 delivers specific, testable diagnoses: the diagonal-angle bias (zero correct on non-45° vectors), start-point marker size sensitivity (92% → 68% as size decreases), concept-recognition vs. visual-processing dissociation in MA1, and the text-as-crutch finding in CF3 (100% with text, 6.2% with vision). (§4)

- **Parametric generator for future-proofing.** The synthetic generation pipeline for 12 subtests produces unlimited test cases with controllable difficulty levels, addressing benchmark saturation concerns. (§2.4)

## Weaknesses

### Major

- **The central "castles in the air" claim — that high scores on existing benchmarks do not reflect genuine visual cognition — is asserted rather than evidenced.** The paper provides no correlation analysis (e.g., Spearman's ρ) between VisFACTOR scores and any existing benchmark (MMBench, MMMU, Blink, etc.) across the 23 evaluated models. Without this, the paper cannot substantiate that VisFACTOR measures something qualitatively different from existing benchmarks. The benchmark itself remains valuable, but the headline claim is weaker than presented.

### Minor

- **The "Middle Score Anomaly" framing (§3.2) over-interprets intermediate scores.** The paper claims intermediate (30-50%) performance on P3 is "evidence that current models lack genuine reasoning capabilities." Intermediate scores are equally consistent with genuine-but-brittle visual processing (noisy attention, inconsistent perception). The paper's own failure analysis (§4.2, marker-size smooth degradation from 92% to 68%) actually supports the brittle-capability interpretation. The claim should be softened.

- **The generated-test results (Table 3) contain an unexplained non-monotonic pattern.** On MA1, the Easy subset yields 50% while Hard yields 70.8% (Normal=90.5%). The paper states performance "increases progressively across the easy, normal, and hard subsets," but the overall total scores actually decrease (Easy=28.9, Normal=23.2, Hard=22.0) and the per-subtest MA1 pattern is non-monotonic. This inconsistency is not discussed.

- **The human evaluation (§3.4) samples only 20 items per subtest (vs. full item sets for models) and reports only point estimates without confidence intervals or variance across raters.** Some per-subtest human scores (CS1=35%, RL2=51.7%) are close enough to model performance that the "humans outperform on nearly all subtests" framing should be qualified with uncertainty.

- **The MA1 diffusion-model experiment (§4.1) is described qualitatively ("the model maintains high accuracy") without reporting any quantitative results.** This weakens the otherwise strong failure analysis.

- **The parametric generator (§3.3) is evaluated on only a single model (GPT-4.1).** Testing 2-3 additional models on the generated subsets would substantially strengthen claims about difficulty control and benchmark scalability.

- **The paper lacks any discussion of construct validity threats from digitization** — format change (paper-and-pencil to digital), instruction summarization by LLMs, altered response modality, and removed time pressure — which would strengthen the paper's credibility by preempting skeptical questions.

### Trivial

None.

## Nice-to-Haves

- A correlation analysis between VisFACTOR and existing benchmarks (MMBench, MMMU, Blink) would substantiate the "castles in the air" framing.
- Statistical significance testing (bootstrap confidence intervals or permutation tests) on key comparative claims.
- A brief limitations paragraph discussing construct validity threats from digitization.
- Evaluating 2-3 more models on the parametric generated subsets.

## Removed Points

These points from the input review were removed with justification:
- Characterization of prior-benchmark claims as "somewhat misleading" — this is a judgment call about a reasonable characterization, not a weakness.
- Note about CoreCognition overlap — removed per rules against missing-related-work citations.
- Reference to Table 6 being in the appendix — removed per rules about missing appendix content.
- "No statistical testing" as a standalone weakness — moved to Nice-to-Haves (standard practice in ML evaluation papers).
- Practical-implications claim in conclusion — standard for conclusion sections.
- Various minor presentation observations from section-by-section notes.

## Novel Insights

Beyond the paper's own contributions, the key insight emerging from synthesis is that the strongest evidence for the "castles in the air" thesis comes not from aggregate scores but from the specific, concrete failure modes identified in §4. The diagonal-angle bias (consistent default to nearest 45° approximation) is particularly novel and diagnostic, suggesting models have categorical rather than continuous spatial orientation representations. The CF3 text-vs-vision disparity (100% vs 6.2%) cleanly dissociates textual reasoning from visual perception in a way few prior benchmarks have achieved. In contrast, the "middle score anomaly" argument about P3 is more ambiguous and should not carry the rhetorical weight the paper places on it.

## Suggestions

1. Add a correlation analysis (Spearman's ρ) between VisFACTOR scores and existing benchmarks (MMBench, MMMU, Blink) across the 23 models, or explicitly temper the "castles in the air" framing.
2. Report confidence intervals for human evaluation scores.
3. Address the non-monotonic MA1 generated-test results (Easy=50%, Hard=70.8%).
4. Quantify the MA1 diffusion-model experiment results.
5. Add a brief limitations paragraph discussing digitization-related construct validity threats.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>