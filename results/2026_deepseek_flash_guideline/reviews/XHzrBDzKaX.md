## Summary

This paper introduces VisFACTOR, a benchmark that digitizes 20 vision-centric subtests from the FRCT cognitive psychology battery (covering 10 factors across 4 domains) to evaluate MLLMs' foundational visual abilities. On 23 frontier MLLMs, the best model (GPT-5.1) achieves only 30.17% — compared to 78.8% from human participants. The benchmark uses principled design strategies (decomposed MC, grouped-consistency scoring, symmetry variants) to reduce chance-level accuracy to 2.89%, and includes parametric generation for 12 subtests to enable difficulty-controlled test cases. A failure analysis reveals that models rely on high-level concept recognition rather than genuine low-level visual processing, and identifies specific geometric and spatial biases (e.g., diagonal-orientation bias, marker-size sensitivity).

## Strengths

- **Psychometric grounding via a standardized cognitive assessment battery rather than ad-hoc tasks.** The paper selects 20 vision-centric subtests from the established 72-subtest FRCT battery (Ekstrom & Harman, 1976), covering 10 distinct cognitive factors across 4 domains (Section 2.1). This enables factor-level diagnosis of what visual capacities MLLMs truly possess, a structural improvement over benchmarks that test aggregate task accuracy on natural images.

- **Chance-level accuracy reduced from 22.47% to 2.89% through four principled design strategies.** The paper introduces decomposed multiple choice, grouped-consistency scoring, symmetry variants, and specialized rewrites (Section 2.3), with explicit per-subtest calculations (e.g., S1: (0.5)⁸ ≈ 0.39%). This ensures that measured performance reflects genuine visual reasoning rather than lucky guesses, a methodological step beyond standard multiple-choice benchmarks.

- **Controllable-difficulty parametric generation for 12 subtests.** Algorithmic generators (Section 2.4) produce unlimited valid question–answer pairs with adjustable parameters (rotation angle, noise severity, grid size, fold count). Table 3 demonstrates progressive performance changes across Easy/Normal/Hard subsets (e.g., CF3: 15.6% → 4.7% → 4.7%; MA1: 50.0% → 90.5% → 70.8%). This future-proofs the benchmark against overfitting.

- **Systematic failure analysis isolating concept-recognition from genuine visual processing.** The MA1 experiment (Section 4.1, Table 5) swaps semantically rich images with abstract CF2 line patterns, causing GPT-4.1 to drop from ~90% to 33.3% and Qwen-VL-Max to fall to 2.38% at 40 pairs. The diffusion-model control (e.g., "a horse on the moon") confirms the drop is not due to distribution shift. This controlled ablation directly supports the paper's central claim that MLLMs rely on high-level semantic concepts rather than low-level visual processing.

- **Discovery of specific, reproducible failure patterns.** The diagonal-orientation bias (Section 4.2, lines 270–271): all tested models misclassify non-45° vectors as the nearest 45° approximation, scoring 0/20. The marker-size degradation (92% → 80% → 68%) and the CF3 text-vs-vision comparison (100% textual accuracy vs. 6.2% visual accuracy) are precise, falsifiable findings that identify concrete visual bottlenecks.

## Weaknesses

### Major

- **The "castles in the air" narrative overstates what the evidence supports.** The paper's central framing — that high scores on general benchmarks (e.g., MMBench at ~90%) are "castles in the air" — implies these benchmarks are actively misleading about models' visual abilities. However, the evidence only shows that VisFACTOR measures something different from what MMBench measures, which is valuable but weaker. The paper never tests whether VisFACTOR performance predicts any downstream outcome (robustness, generalization, safety), nor shows a dissociation (e.g., models with high MMBench but low VisFACTOR are more brittle in deployment). The abstract and conclusion (lines 9, 294) assert practical ramifications ("rendering high-level downstream applications...infeasible"; "Hallucinated perception in safety-critical applications, brittle spatial reasoning in robotics") without supporting evidence. This overclaiming is the paper's most significant weakness — it does not invalidate the benchmark, but the paper would be stronger with more measured claims.

### Minor

- **Human evaluation lacks variance reporting.** The human evaluation (Section 3.4) uses 31 participants with 3 per question and reports 78.8% total accuracy with per-subtest scores (Table 4), but provides no measure of variance (standard deviation, confidence intervals, or inter-participant agreement). Without this, it is unclear whether the gap between the best model (30.17%) and humans (78.8%) is statistically reliable for individual subtests, or whether some subtests show overlapping ranges.

- **Construct validity of strict scoring rules is not acknowledged.** The stringent all-or-nothing scoring (decomposed MC, grouped-consistency items) is a deliberate design choice to reduce chance, but it changes what is measured relative to the original FRCT. A model that correctly identifies the right answer in a 5-option question but misclassifies one distractor gets zero credit — the same as a model that cannot see the stimulus at all. On S1 (Card Rotation), a model with 80% per-item accuracy gets all eight correct only ~16.8% of the time. The paper should acknowledge that scores are lower-bound estimates and discuss whether the scoring could systematically disadvantage models in ways unrelated to visual cognition.

- **Ambiguous phrasing in Section 3.3.** Line 221 states "The model's performance increases progressively across the easy, normal, and hard subsets," but Table 3 shows Easy (28.9) > Normal (23.2) > Hard (22.0). This is the expected pattern (easier → higher scores) but the phrasing is backwards or unclear.

### Trivial

- **Symmetry variants wording inconsistency (line 115).** The text says "We generate three variants per item" then computes chance as (0.5)⁴ = 6.25%, which implies 4 total questions (original + 3 variants). The text should say "all four correctly" rather than "all three correctly."
- **Item selection method for human evaluation not described.** "We sample 20 items per subset" (line 231) without explaining how items were selected (random? stratified?), which matters given the variant structure.
- **Participant population details omitted.** No information on whether participants were screened for visual impairments or prior familiarity with FRCT-style tests.

## Nice-to-Haves

- **Validation of the benchmark's relevance to downstream tasks.** The paper repeatedly invokes embodied AI and safety-critical applications. A correlational study — even limited — linking VisFACTOR scores to performance on downstream tasks (e.g., spatial reasoning benchmarks, visual grounding accuracy) would significantly strengthen the "castles in the air" thesis by turning it from interpretation into evidence.
- **Relaxed scoring for graded measurement.** Reporting results under both the strict scoring (all-or-nothing) and a relaxed scoring (partial credit per item) for a subset of models would reveal whether the qualitative pattern is robust to the scoring rule, and help readers gauge how much of the reported deficit is due to measurement compression.
- **Statistical significance testing for key comparisons**, particularly the temperature analysis (Table 2) and the MA1 ablation results (Table 5).

## Removed Points

These points were considered but removed with justification:

- **Criticism about unfair comparison favoring baselines:** The asymmetry always favors the baseline, not the author's method — removed per Hard Rules.
- **Criticism about missing related works:** Removed per instructions (no external sources to confirm existence).
- **Formatting/style nitpicks about Table 1 density:** Removed as likely parser artifacts.
- **Criticism about GPT-4o/Gemini authoring prompts:** The paper uses human reconciliation of summaries, making this a manageable design choice, not a fatal flaw.
- **Criticism about RL2 result "cutting against the narrative":** The paper already acknowledges this explicitly (line 235: "except RL2...where success relies more on textual object knowledge, a known strength of MLLMs rather than visual reasoning").
- **Criticism about "Middle Score Anomaly" being speculative:** This is interpretive but the paper explicitly frames it as an observation and interpretation (line 188), not a proven claim. Not a clear weakness.
- **Criticism that models' intermediate scores reflect partial competence rather than lack of reasoning:** This is an interpretation difference, not a verified weakness.
- **Criticism about practical recommendations (conclusion) being unsupported:** These are standard conclusion-level future directions, common practice in benchmark papers.
- **Strength: "the paper addressed an important problem":** Generic, removed per filtering guidance.
- **Strength: "The scale of evaluation (23 models) is appropriate":** Generic and superficial, removed.
- **Criticism about the item selection for 20 subtests being underspecified:** Valid but the paper states the selection criteria clearly (Section 2.1: exclude image-production and speech-dependent tasks from the remaining 65, select those demanding visual reasoning).

## Novel Insights

The harsh critic correctly identifies that the paper's most interesting finding is not the headline accuracy figure (30.17%) but the dissociation revealed in Section 4: models perform well on memory tasks with semantically rich images (~90% on MA1 with natural images) but collapse when the same task uses abstract line patterns (2.38–33.3%). Combined with the CF3 text-vs-vision comparison (100% textual vs. 6.2% visual) and the diagonal-orientation bias, this constitutes genuinely diagnostic evidence: MLLMs have a visual perception bottleneck that is masked when inputs can be mapped to familiar verbal concepts. The paper would benefit from centering this dissociation more prominently, as it is more specific and informative than the aggregate "castles in the air" framing.

## Suggestions

1. **Tone down the "castles in the air" framing.** The benchmark stands on its own merits — rigorous psychometric grounding, thorough evaluation, insightful failure analysis — without needing this rhetorical device. Either soften the claim or support it with downstream validation.
2. **Add confidence intervals or standard deviations to the human evaluation** (Table 4).
3. **Acknowledge the construct validity trade-off** introduced by the strict scoring rules. Ideally, report a subset of results under relaxed scoring to show robustness.
4. **Clarify the item selection procedure for human evaluation** (line 231).
5. **Fix the ambiguous phrasing in Section 3.3** ("performance increases progressively across the easy, normal, and hard subsets" — should be "decreases progressively").
6. **Consider restructuring the paper** to foreground the visual vs. verbal dissociation findings (Section 4) as the central empirical contribution, with the benchmark as the enabling tool.

## Score and Decision

**Calibration anchors.** All anchors from `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`:

| Anchor | Avg Score | Decision | Round | Comparison to this paper |
|--------|-----------|----------|-------|------------------------|
| SPACE (WK6K1FMEQ1) | 6.75 | Accept | 2 | Similar cognitive-science-grounded benchmark; fewer tasks but stronger cross-modality analysis |
| 3D-PC (UIFAJZ22ZF) | 6.67 | Accept | 1 | Similar approach (cognitive tasks, human vs. model); comparable quality |
| VL-ICL Bench (cpGPPLLYYx) | 6.50 | Accept | 1 | Benchmark paper of comparable scope and thoroughness |
| Labyrinth of Links (vJ0axKTh7t) | 6.25 | Accept | 2 | Association benchmark; similar depth of evaluation |
| Voila (q5MUMlHxpd) | 5.80 | Accept | 2 | Simpler analogical reasoning benchmark; accepted with similar score |
| MMMU-Pro (2jTdHYuguF) | 5.80 | Reject | 1 | Incremental benchmark extension; rejected despite reasonable methodology |
| Face-Human-Bench (x1Bk51SCL9) | 5.75 | Reject | 2 | Face understanding benchmark; rejected for limited novelty |
| CogDevelop2K (fDNBPqgr4K) | 4.75 | Reject | 2 | Similar cognitive-development framing; rejected for overclaiming and limited insights |
| VCog-Bench (QrhB9HcgnL) | 4.75 | Reject | 2 | Matrix reasoning benchmark; rejected for incremental contribution |
| MERLIM (UL95Epgrl8) | 5.00 | Reject | 1 | Multimodal evaluation benchmark; rejected for limited novelty |
| PhysBench (Q6a9W6kzv5) | 8.00 | Accept | 1 | Much larger scale benchmark with proposed solution; stronger overall |

**Bracket (Round 1):** 5.5–7.0, based on similarity to SPACE (6.75), 3D-PC (6.67), and VL-ICL (6.50) on the upper end, and Voila (5.80) on the lower end, with clear separation from CogDevelop2K (4.75) and VCog-Bench (4.75).

**Narrowing (Round 2):** The paper's psychometric grounding, parametric generation, and failure analysis place it above simple re-benchmarking efforts like MMMU-Pro (5.80) and VCog-Bench (4.75). The overclaiming ("castles in the air") is a real weakness that weighs against it compared to SPACE (6.75) and 3D-PC (6.67), which have stronger evidence for their central claims. The paper lands at 6.0 — borderline accept territory.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>