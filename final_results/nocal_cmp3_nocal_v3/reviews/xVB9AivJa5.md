## Summary

Blueprint-Bench introduces a benchmark for evaluating spatial reasoning in AI models by tasking them with converting apartment photographs into 2D floor plans. The benchmark is model-agnostic, supporting LLMs (via SVG), image generation models, and agent scaffolds under a shared scoring framework based on connectivity graphs and size rankings. The paper evaluates 12 models and finds that all remain far below human performance, highlighting a spatial reasoning blind spot in current AI systems.

## Strengths

- **Clever and well-motivated task design.** Unlike abstract reasoning benchmarks (e.g., ARC) that use alien grid patterns, Blueprint-Bench uses photographs as input — well within the training distribution of multimodal models — while the floor-plan reconstruction task itself is *not* something models were explicitly trained for. This creates a principled test of whether models can perform genuine spatial reasoning using familiar inputs, a thoughtful design choice that avoids trivializing the benchmark.

- **Model-agnostic evaluation framework.** The same task accepts LLMs (through SVG generation), image generation models (direct image output), and agent scaffolds (Docker environments). This enables direct architectural comparisons that are rare in the literature, and the authors' claim to provide "the first numerical framework for comparing spatial intelligence across different model architectures" is credible.

- **Transparent about limitations.** Section 2.4 openly discusses three specific limitations: rooms are not labeled by type, room shape is not accounted for, and the scoring algorithm conflates instruction-following with spatial intelligence. This honesty helps readers calibrate their interpretation of the results and distinguishes the paper from benchmarks that overclaim.

## Weaknesses

### Major

1. **The abstract's headline quantitative claim contradicts the paper's own data.** The abstract states: *"most models perform at or below a random baseline."* Figure 5 shows the random baseline at 0.279; of the 12 models tested, **10 have mean scores above 0.279** (ranging from 0.32 to 0.42). Only two models (GPT-4o at 0.15, NanoBanana at 0.18) fall below. The body text (Section 3) qualifies this by claiming only four models "statistically perform better" than random, but no statistical test is named, no p-values or confidence intervals are reported, and the error bars (described only as "standard deviation") leave the statistical claim unverifiable. A reader of the abstract walks away with a materially false impression.

2. **The random baseline is inconsistently reported without explanation.** Figure 5 (all 50 apartments) shows the random baseline at **0.279**, while Figure 7 (12-apartment subset with human baseline) shows it at **0.322** — a ~15% relative difference. Since the random baseline is defined (Section 2.2) as "generating typical floor plans...without any image input," it should not depend on which ground-truth apartments it is compared against, except through sampling variation across subsets. A shift of this magnitude without explanation undermines confidence in the baseline's stability. Additionally, Figure 7's caption states "Error bars show 2.5 standard deviation" (line 171) while the body text for the same figure says "Error bars represent standard deviation" (line 173), adding confusion about what is actually plotted.

3. **The "statistically better than random" claim is unsupported.** The paper asserts (Section 3, line 112) that four models "statistically perform better than the random baseline" but provides no test name, p-values, confidence intervals, or multiple-comparison correction. With 12 models and 50 apartments, this is a non-trivial gap. The reader cannot evaluate whether the claim holds or whether the four highlighted models were selected post hoc. The "blind spot" narrative of the paper rests in part on this statistical claim; without evidence, the claim is unsubstantiated.

### Minor

4. **The scoring algorithm conflates spatial intelligence with instruction-following, and the paper acknowledges this but does not resolve it.** Section 2.4 states: *"Blueprint-Bench should test spatial intelligence, not instruction following."* Yet Section 3 attributes the lowest scores (GPT-4o, NanoBanana) to "poor instruction following, leading to outputs that do not adhere to the rules and therefore cannot be scored by our algorithm." This means the benchmark is measuring at least two entangled capabilities for the lowest-performing models, and the scores for those models are uninterpretable as spatial intelligence measures. The paper's defense — that this is "the right tradeoff at current model capabilities" — is contestable, and the benchmark would be strengthened by a mechanism to separately report rule compliance and spatial accuracy.

5. **Data contamination from publicly sourced real estate listings is unaddressed.** The dataset is sourced from publicly available real estate listings. Many tested models (GPT-5, Claude Opus 4.1, Gemini 2.5 Pro, etc.) were trained on web-scale data that likely includes such listings. A model could produce a plausible floor plan by retrieving a memorized listing rather than by reasoning spatially from the photographs. The paper acknowledges overfitting risk (keeping most data private) but does not discuss the contamination threat, nor does it provide any analysis (e.g., partitioning results by listing date relative to model training cutoffs). Given the small dataset size (50 apartments), this is a validity concern worth addressing.

6. **The human baseline is underdocumented.** Human performance covers only 12 of 50 apartments, with no details on the number of subjects, their expertise, or how instructions were standardized. The paper states that humans "always got connectivity correct" but struggled with size rankings, leading to a "harsh penalty" from the scoring algorithm. It then speculates that a different scoring model "would make the human's lead over the AI models much larger" — an appeal to intuition rather than evidence. The human baseline is the paper's key anchor for the "blind spot" claim, yet its construction is opaque.

7. **The claim that agents show "no meaningful improvement" is not well supported by the data.** Claude Code (agent, score 0.38) vs. Claude Opus 4.1 (non-agent, score 0.32) represents roughly a 19% relative improvement. Meanwhile, CodeX (GPT-6) at 0.40 vs. GPT-5 at 0.42 involves *different underlying models*, confounding the agent vs. non-agent comparison. The paper's narrative that iteration does not help is contradicted by at least one clean comparison (Claude Code vs. Claude Opus 4.1) that shows a non-trivial gain.

### Trivial

8. The scoring weight choices (50% edge overlap, 20% degree correlation, 10% density, 10% room count, 5% door count, 5% door orientation) are presented without justification. While any set of weights is ultimately a design choice, the absence of any sensitivity analysis or rationale leaves the reader unsure how much the reported rankings depend on these arbitrary-seeming proportions.

## Nice-to-Haves

- Decouple instruction-following from spatial intelligence scoring, e.g., by reporting separate "rule compliance" and "spatial accuracy" scores.
- Add per-apartment difficulty analysis to deepen the benchmark's diagnostic value.
- Include qualitative analysis of successful generations (e.g., what does a score of 0.42 mean visually?).
- Clarify what "epochs" refers to in the averaging (multiple runs? different random seeds?) and explain the discrepancy in error bar descriptions (SD vs. 2.5 SD) across Figure 5 and Figure 7.

## Removed Points

These points from the input review are flagged for removal; treat them with caution:

- **"Random baseline may already be too high because it uses LLM-prior floor plans"** — The paper defines this as a "worst-case baseline" (Section 2.2), making its directionality intentional. If the baseline is conservative (inflated), that works against the paper's narrative, which is a *different* criticism from what was raised. The reviewer's framing is not quite accurate to the paper's stated intent. Demoted because the paper is transparent about what the baseline is.
- **"Introduction discussion of image generation models is speculative"** — This is a judgment about framing, not a weakness with evidence. The paper itself says "this is an empirical observation" and does not claim general intelligence.
- **"The paper should discuss missing related works"** — Removed per hard rule: as an external reviewer, I cannot confirm what related works exist or do not exist beyond the paper's own citations.
- **"Statistical testing is absent"** — Already captured in Major weakness #3 above (merged).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the abstract.** Replace "most models perform at or below a random baseline" with an accurate summary, e.g., "all models score far below human performance, and only a minority statistically exceed a non-informative baseline." Ensure the abstract's numerical claims match the data in Figure 5.
2. **Explain the random baseline discrepancy** between Figure 5 (0.279) and Figure 7 (0.322). If the difference is sampling variation on the 12-apartment subset, state this explicitly and quantify the expected variability.
3. **Provide statistical detail** for the four models claimed to be "statistically better" than random: name the test, report p-values, and note whether multiple-comparison corrections were applied.
4. **Address data contamination** with at minimum a brief discussion and, if possible, an analysis partitioning apartments by listing recency relative to model training cutoffs.
5. **Document the human baseline** (number of subjects, instructions, whether the same 12 apartments were used for all subjects, etc.).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>