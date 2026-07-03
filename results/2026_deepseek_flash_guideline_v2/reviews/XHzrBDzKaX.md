## Summary

VisFACTOR is a benchmark that digitizes 20 vision-centric subtests from the FRCT cognitive psychology battery (a well-established assessment of human visual cognition factors) for evaluating MLLMs. The paper evaluates 23 frontier models (GPT, Gemini, Claude, Qwen, LLaMA, etc.), finding the best model (GPT-5.1) achieves only 30.17% while humans score 78.8%. It includes a parametric test-case generator for 12 subtests with controllable difficulty, and a failure analysis demonstrating that models rely on concept-level recognition rather than genuine low-level visual perception — most clearly shown by the MA1 ablation where accuracy drops from ~90% to 2–33% when semantically rich images are replaced with abstract line figures.

## Strengths

1. **Psychometric grounding via FRCT battery**: The benchmark adapts 20 subtests from an established cognitive psychology assessment (FRCT) that decomposes vision into latent factors (Closure Flexibility, Spatial Orientation, Visualization, etc.). This factor-analytic grounding is a principled departure from prior multimodal benchmarks that lack such decomposition. The 20 subtests cover 10 distinct FRCT factors across four cognitive domains.

2. **Carefully engineered low chance-level accuracy (§2.3)**: Four strategies — decomposed multiple choice (one yes/no per option), grouped-consistency items, symmetry variants (balancing yes/no distribution), and specialized rewrites — reduce the average random-guess baseline from 22.47% to 2.89%, with no single subtest exceeding 6.25%. This is a measurable improvement over prior benchmarks using standard multiple-choice or True/False formats.

3. **Controlled MA1 ablation isolating concept recognition from visual perception (§4.1, Table 5)**: The paper ablates the MA1 memory test by replacing semantically rich images with abstract CF2/MV1 line figures while keeping the task structure identical. With semantically rich images, all three models maintain ~90% accuracy at 80 pairs; with abstract CF2 figures, accuracy drops to 33.3% (GPT-4.1), 9.5% (Claude-3.7), and 7.1% (Qwen-VL-Max). This directly supports the paper's core thesis that models rely on concept-level recognition rather than low-level visual processing.

4. **Parametric generation with validated difficulty modulation (§2.4, Table 3)**: Automated generation for 12 subtests with controllable parameters (grid size, noise severity, number of folds/pairs). GPT-4.1 performance tracks the difficulty tiers: Easy (28.9%) > Normal (23.2%) > Hard (22.0%), validating the generator for future-proofing the benchmark against saturation.

5. **Specific, falsifiable discovery of diagonal-orientation bias (§4.2)**: On a controlled test of 20 non-45-degree vectors (e.g., vector (2,1)), models achieve zero correct angular identification, consistently defaulting to the nearest 45-degree approximation. This is a concrete, reproducible finding about MLLM visual limitations that goes beyond aggregate accuracy scores.

6. **Human baseline using the identical digital protocol (§3.4, Table 4)**: 31 university students were evaluated with the same instructions and scoring rules, yielding 78.8% average accuracy. This confirms the human–model gap (best model 30.17%) is not an artifact of benchmark design or digitization.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Human-model comparison over different item sets**: Humans were tested on 20 items per subtest (1,540 total questions, line 231), while models were evaluated on the full benchmark whose total item count is not stated in the main text. The headline comparison (78.8% human vs 30.17% model) is therefore computed over different item sets. The gap is large enough that the conclusions likely hold, but the paper should report model scores on the exact same 20-items-per-subset for a clean comparison and state the full benchmark size.

2. **Subtest selection transparency**: Section 2.1 states that 45 of 65 text-compatible subtests are text-answerable, and "those demanding visual reasoning but accept text answers form our benchmark" — but the 25 excluded subtests are never named or listed with exclusion rationales. Since the benchmark claims to broadly sample "human visual cognition," the reader cannot assess whether the selection is representative or biased. A supplementary table of all 45 text-answerable subtests with per-item exclusion rationale would address this.

3. **"Model size and recency do not guarantee" claim is anecdotal**: The evidence (lines 146–147) is limited to several cherry-picked counterexamples (Qwen-2.5-32B > 72B, Claude-3.7 > Claude-4, Seed-1.5 > Seed-1.6). The claim is modest ("do not guarantee"), but the same paragraph acknowledges counterexamples (GPT-4o > GPT-4o-Mini, o3 > o1). A systematic analysis — even a simple rank correlation between score and parameter count or release date across all 23 models — would be more informative than isolated anecdotes.

4. **"Middle Score Anomaly" lacks empirical support for the human behavior claim**: The paper invokes the Middle Score Anomaly (cited to Babaie et al., 2025) and claims about P3 that "it would be highly unusual for a human to achieve, say, 70% accuracy on this task" (line 188). No evidence or citation is provided for this specific claim about human performance on P3. While the human data in Table 4 (91.7% on P3) is consistent with near-perfect performance, the assertion about intermediate scores being anomalous is unsupported. The overall observation is interesting but its framing in terms of "genuine reasoning" (line 188) exceeds the evidence.

5. **No confidence intervals or uncertainty quantification**: The paper reports fine-grained model scores differing by fractions of a percent and reports CoT correlation coefficients (−0.18, −0.28, −0.35) without confidence intervals. While absolute statistical rigor is not the norm for benchmark papers, the reader cannot assess whether small differences (e.g., GPT-4.1 at 21.3% vs GPT-4o at 21.4%) are meaningful or whether the negative CoT correlations are reliably non-zero.

6. **No explicit differentiation from CoreCognition (Li et al., 2025b)**: Section 5 mentions CoreCognition as prior work using synthetic images and cognitive tasks but does not clearly articulate what VisFACTOR adds beyond it. Given the similarity of scope, the paper should explicitly distinguish its FRCT factor-grounded approach.

### Trivial

1. **Prompt confound not acknowledged**: GPT-4o and Gemini-2.5-Flash were used to summarize task instructions (line 39), which could subtly advantage these model families. The paper should acknowledge this.

2. **LLaMA-3.2 near-chance performance**: LLaMA-3.2-13B (2.4%) and 90B (4.1%) score close to the 2.89% random baseline (Table 1). The paper should briefly discuss whether this reflects genuine inability or a possible evaluation-format mismatch.

## Nice-to-Haves

- Compute model scores on the same 20-items-per-subset used for human evaluation.
- Add a rank correlation or regression analysis of score vs. model parameter count / release date.
- Add confidence intervals for total scores and CoT correlation coefficients.
- Provide a table of all 45 text-answerable FRCT subtests with exclusion rationales.
- Explicitly differentiate VisFACTOR from CoreCognition in the related work.

## Removed Points

These points were flagged by reviewers but removed after verification against the paper:

1. **"Table 1 formatting is garbled/column-count mismatch"** — Removed because the harsh critic acknowledges this is "likely a PDF extraction artifact." Pure formatting issue, not a paper problem.

2. **"CF3 validity: text description vs. drawing limits comparability"** — Removed because the paper's entire experimental design in §4.2 is to make exactly this comparison (text provision → 100% accuracy, visual input → 6.2%). This is a feature of the controlled experiment, not a weakness.

3. **"Middle Score Anomaly contradicted by other subtest scores in Table 4"** — Removed because the critic conflates different subtests. The paper's claim is about P3 specifically (human score 91.7%, consistent with near-perfect). Intermediate scores on CF2 (56.7%), VZ1 (58.3%), etc. are from different, harder tasks and do not contradict the claim about P3.

4. **"Section 2.4 too brief to evaluate"** — Removed because the algorithms are referenced to §C of the appendix, which was stripped by the PDF parser. The harsh critic acknowledges this limitation.

5. **"Abstract/Introduction overstates weakness of prior work"** — Removed as a minor framing nitpick that does not affect the paper's contributions.

6. **"Synthetic augmentation does not faithfully reproduce original difficulty profile"** — The critic points to per-subtest differences (e.g., S2: 0% generated vs 28.6% original). This is a valid observation but the paper acknowledges that some generated subtests differ in difficulty (attributed to using commonly encountered objects, line 221) and this is a limitation worth noting but not a core weakness. Kept here for completeness.

## Novel Insights

The reviews collectively highlight that VisFACTOR's most compelling evidence is the MA1 ablation (Section 4.1), which cleanly demonstrates that MLLMs rely on concept-level recognition rather than genuine low-level visual perception. An underappreciated finding that emerges from combining the failure analysis with the controlled generator is that the "visual gap" is specifically a gap in *continuous spatial perception* (line length, angle, proportion) that cannot be bridged by textual mediation. The diagonal-orientation bias (§4.2) — zero correct identification on 20 non-45-degree vectors — and the CF3 text-vs-visual comparison (100% vs 6.2%) together suggest that MLLM visual systems may learn categorical approximations of spatial properties rather than continuous representations, a limitation that aggregate benchmark scores obscure.

## Suggestions

1. Report model performance on the exact same 20-items-per-subset used for human evaluation, and state the full benchmark item count in the main text.
2. List all 45 text-answerable FRCT subtests with per-item exclusion rationales.
3. Replace the anecdotal scale/recency discussion with a systematic analysis (e.g., Spearman rank correlation between score and parameter count).
4. Add confidence intervals for total scores and CoT correlation coefficients.
5. Explicitly differentiate VisFACTOR from CoreCognition in the related work section.
6. Either provide evidence for the claim that intermediate scores on P3 would be "highly unusual" for humans, or soften the Middle Score Anomaly framing.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>