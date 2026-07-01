## Summary

Blueprint-Bench introduces a benchmark that evaluates spatial reasoning in AI models by asking them to convert apartment photographs into 2D floor plans. The dataset comprises 50 apartments (~20 images each) with ground-truth floor plans, and models are scored on a composite metric of connectivity graph similarity and room size ranking. The paper evaluates 12 systems across LLMs, image generation models, and agents, reporting a large gap between all models and human performance.

## Strengths

1. **Well-motivated, clever task design.** Using photographs (in-distribution for multimodal models) as input for a spatial reconstruction task (out-of-distribution) is a cleaner probe of emergent spatial reasoning than benchmarks like ARC, which use entirely alien inputs. This is explicitly and convincingly argued in Section 1 (lines 15–21).

2. **Model-agnostic evaluation framework.** The benchmark accepts any system that can produce an image from image inputs — LLMs (via SVG code), image generation models (direct output), and agent systems (via Docker environments). This cross-architecture comparability is a genuine design strength and distinguishes Blueprint-Bench from task-specific benchmarks.

3. **Addresses a real evaluation gap for image generation models.** The paper correctly observes (line 39) that models like GPT-Image and NanoBanana have been released without numerical benchmarks. Blueprint-Bench provides a framework for quantitative comparison, which is a timely contribution.

4. **Open-source with private test set.** Releasing code and a data sample while keeping most data private (line 71) is the correct approach for a benchmark intended to track progress over time and prevent overfitting.

## Weaknesses

### Fatal
None.

### Major

1. **The abstract's headline claim contradicts the paper's own data.** The abstract states *"most models perform at or below a random baseline"* (line 9), and the results section echoes *"most do not outperform the random baseline"* (line 112). However, the data in Figure 5 shows that **10 out of 12 models have raw mean scores above the random baseline of 0.279** — only GPT-4o (0.15) and NanoBanana (0.18) are below. The results section hedges by saying only 4 models *"statistically perform better"* (line 112), but no statistical tests, p-values, or confidence intervals are reported to support this distinction. The central advertised finding is misleading as written. The benchmark itself remains valuable, but the paper's framing needs substantial correction — the story should be about the large gap from human performance, not that models are at chance.

2. **The random baseline is vaguely defined and inconsistently reported.** The baseline is introduced only as *"generating typical floor plans using LLMs and image generation models without any image input"* (line 69). This is not a reproducible definition — what does "typical" mean, how many samples were generated per apartment, and what generation procedure was used? Furthermore, two different random baseline values appear without explanation: **0.279** in Figure 5 (all 50 apartments) and **0.322** in Figure 7 (12-apartment subset). If the baseline is a fixed property of the scoring algorithm applied to random outputs, it should be consistent across subsets; if it varies, the methodology must be explained. Without a clear baseline, the central interpretive frame of the benchmark is undermined.

3. **Model categorization in the results is confused, making cross-architecture comparisons uninterpretable.** The abstract (line 9) defines three groups — *"language models (GPT-5, Claude 4 Opus, Gemini 2.5 Pro, Grok-4), image generation models (GPT-Image, NanoBanana), and agent systems (Codex CLI, Claude Code)."* However, the results table in Figure 5 (lines 119–132) labels GPT-5, Claude Opus 4.1, Claude Sonnet 4, Gemini 2.5 Pro, GPT-5-mini, Grok 4, and even the Claude Code agent all as **"Image model"** — only CodeX is listed as "Agent." The figure legend shows only two categories (striped bars for "Image models," dotted bars for "Agents"), so the reader cannot distinguish LLMs from image generation models in the main results. The abstract's claims about image generation models struggling with instruction following and about comparing LLMs and image generation models cannot be verified from the presented data.

### Minor

4. **Size-ranking dependency of the metric is acknowledged but not quantified.** The paper admits (line 100) that the room-size ranking causes cascading penalties in connectivity scoring — a model that correctly infers connectivity but misorders similarly sized rooms is penalized twice. Humans also made size-ranking errors (line 149), and the paper concedes this may understate human performance. However, no sensitivity analysis is provided (e.g., reporting scores under optimal matching of rooms) to establish how much the metric measures spatial reasoning vs. size-ordering ability.

5. **Statistical significance is claimed without supporting evidence.** The paper states that certain models *"statistically perform better than the random baseline"* (line 112) and that one agent's results were *"not statistically better"* (line 179), but reports no test statistics, p-values, or confidence intervals. For a benchmark comparing 12 systems across multiple models, this is a notable gap.

6. **The SVG pipeline is a potential confound for LLM evaluation.** LLMs generate SVG code that is then rendered into images (line 61). SVG syntax errors or rendering artifacts unrelated to spatial reasoning could degrade scores. The paper does not report SVG success rates or whether failed SVG generations were excluded or penalized.

7. **Human evaluation on a different subset with a different procedure.** Human performance (0.547) is measured on only 12 apartments, while model results in Figure 5 use all 50. Models re-scored on the same 12 apartments (Figure 7) show shifting scores. The human evaluation also allowed iterative refinement (viewing images, drawing, checking), whereas most models were single-pass. While this asymmetry is acknowledged (line 175), its effect on the human-model gap is not quantified.

8. **Scoring weights are presented without justification.** The six-component scoring function uses weights of 50% edge overlap, 20% degree correlation, 10% density, 10% room count, 5% door count, and 5% door orientation (line 96). No rationale, calibration, or sensitivity analysis is provided for these specific weights.

### Trivial

- The "first benchmark" claim (line 39) would benefit from more precise scoping ("first" in what sense?), though it is appropriately hedged with "To our knowledge."

## Nice-to-Haves

- A per-apartment breakdown of results for all 50 apartments (the appendix includes apartments 1–20 but could be expanded).
- Clarifying how many epochs/trials were used per model and whether "epochs" refers to multiple independent generations.
- An error analysis categorizing the types of mistakes models make (e.g., wrong room count vs. correct room count but wrong connectivity).

## Removed Points

These points are flagged to be removed; treat them with caution:
- **"No per-apartment results or error analysis"** — The paper explicitly states "Detailed graphs with results per data point can be found in Appendix" (line 112) and the appendix contains per-apartment charts. This criticism is factually incorrect.
- **Overstated novelty relative to VCR/NLVR/CLEVR** — Cannot verify these external benchmarks; per review guidelines, criticisms based on unverifiable prior work are removed.
- **Formatting, typo, and parser-artifact criticisms** — Removed per guidelines; these issues stem from the extraction process, not the original submission.
- **Missing appendix content, proofs, or references** — Removed per guidelines; the parser strips these sections from all submissions.
- **Speculative "could be a proxy" concerns without concrete anchor in the paper** — Removed per filtering discipline; generic methodological speculation without a specific identified problem is not retained.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the headline claims.** Rewrite the abstract and introduction to accurately state that most models score above the random baseline (albeit far from human performance), and reframe the central finding around the persistent human-model gap.
2. **Define and justify the random baseline.** Provide a clear, reproducible procedure and explain why the baseline value differs between the 50-apartment and 12-apartment subsets.
3. **Fix model categorization.** The results table and figure should use the same categories as the text (LLM / image generation model / agent) so that cross-architecture comparisons are interpretable.
4. **Report statistical tests.** Provide p-values or confidence intervals for all claims about models performing "statistically" better than the random baseline.
5. **Quantify the size-ranking dependency.** Add a sensitivity analysis showing scores under alternative room-matching schemes.
6. **Report SVG generation success rates** for LLM-based evaluations to rule out this confound.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>