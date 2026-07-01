## Summary

LPFQA is a benchmark of 502-505 questions sourced from professional technical forums (Project Euler, CONTROL.com, MATH, CHEMISTRY) across 20 academic/industrial fields, designed to evaluate LLMs on long-tail, real-world professional knowledge. The paper describes an 8-step construction pipeline (crawl → MLLM generate QA → LLM clean → expert verify → difficulty calibrate) and reports scores for 12 LLMs. The core idea—sourcing practitioner-level questions from real forums—addresses a genuine gap in the benchmark landscape. However, the paper as submitted has several significant problems that prevent its contribution from being properly assessed.

## Strengths

1. **Well-motivated gap.** The paper correctly identifies that existing long-tail knowledge benchmarks (iNaturalist, ImageNet-LT) use simplistic classification tasks, while user-centric benchmarks (Arena-Hard) lack domain depth, and extreme benchmarks (HLE) are unrepresentative of everyday use. A benchmark of complex, real-user professional questions is a genuinely useful target (Lines 15, 36-50).

2. **Scalable construction pipeline.** The three-phase pipeline (data collection → automated question generation with quality control → expert verification and difficulty adjustment) is clearly described and could be applied to other forum sources. Using screenshots to preserve visual/contextual information before MLLM processing is a practical design choice (Lines 108-136).

3. **Expert verification.** The inclusion of human expert verification (Step 7) and empirical difficulty calibration (Step 8) adds confidence beyond a purely automated pipeline (Lines 130-134).

## Weaknesses

### Major

1. **The scoring metric is never defined, making the experimental results uninterpretable.** Tables 1-4 report "Scores" ranging from ~28 to ~54, but the paper never states what these numbers represent. Are they percentage accuracy? A weighted combination? Accuracy on multiple-choice plus partial credit on short-answer? What is the denominator or maximum possible score? The paper describes that questions come in multiple-choice and short-answer formats and that "key knowledge points" are used as criteria for short-answer correctness (Line 128), but it never defines how these are aggregated into the reported Score. Without this definition, the entire empirical contribution—model rankings, field-level comparisons, ablation differences—cannot be interpreted, reproduced, or trusted. This is the most critical omission in the paper.

2. **The analysis of the main results directly contradicts the reported data.** Line 265 states: "Among all evaluated systems, DeepSeek-V3 demonstrates the most balanced and consistent performance across disciplines, with no apparent weaknesses, and can thus be regarded as the overall best-performing model." Yet Table 1 shows DeepSeek-V3 at 32.60—the second-lowest score among 12 models, just above GPT-4o (32.40) and far below GPT-5 (47.28), Gemini-2.5-Pro (44.42), and o3-high (43.03). Calling a near-bottom-scoring model "the overall best-performing model" without any explanation of why aggregate score is overridden by "balanced performance" is a clear analytical error that undermines confidence in the entire results section.

3. **Three of the four claimed innovations are asserted but never demonstrated in the evaluation.** The abstract and introduction highlight four contributions (Lines 25-28): (i) fine-grained evaluation dimensions (knowledge depth, reasoning, terminology, contextual analysis), (ii) hierarchical difficulty, (iii) user personas, (iv) interdisciplinary integration. However:
   - **(i) Evaluation dimensions:** No results are reported broken down by knowledge depth, reasoning, terminology, or contextual analysis. The paper never shows whether models differ more on one dimension than another, or whether these dimensions are even measurable.
   - **(ii) Difficulty hierarchy:** The paper mentions difficulty levels but never reports results stratified by difficulty. There is no analysis showing that harder questions separate models more than easier ones.
   - **(iii) User personas:** The term "user personas" appears only in the contribution list (Lines 9, 27). No example persona is given, no construction method is described, and no analysis examines whether personas affect performance.
   
   Claims asserted but not demonstrated should not be counted as contributions.

4. **No comparison against existing benchmarks.** For a benchmark paper, the absence of any comparative analysis is a significant gap. The paper argues that MMLU, HLE, and Arena-Hard have limitations (Lines 15, 36-50) but never shows that LPFQA empirically addresses them. Does LPFQA produce different model rankings? Is it more discriminative? Do scores correlate with human expert judgments? Without any comparative evidence, the claim that LPFQA fills a gap remains an assertion rather than a demonstrated result.

### Minor

5. **Ablation conclusions are not directly supported by the evidence.** 
   - **Code interpreter (CI) ablation (Lines 313-315):** The paper concludes that "LPFQA primarily reflects a model's mastery of domain knowledge rather than its reasoning ability" because adding a CI *reduces* scores. This is a non-sequitur. The CI could hurt for many reasons unrelated to the knowledge/reasoning distinction: poor CI integration, questions not amenable to code-based solution, overhead interfering with other capabilities. The observation is consistent with the claim but does not constitute evidence for it.
   - **Search tool ablation (Lines 317-319):** The paper attributes performance drops to the long-tail nature of the knowledge. While plausible, this is not proven—the drop could also stem from poor retrieval quality, prompt interference, or models not being trained to use search tools effectively.

6. **The filtered-benchmark analysis (LPFQA⁻, LPFQA⁼) is post-hoc and model-dependent.** Removing questions no model answered correctly, and questions all models answered correctly, conditions the benchmark on the particular set of 12 models evaluated (Lines 273-309). A different set of models would yield different filtered subsets. As an exploratory analysis of discriminative power this is reasonable, but the paper should acknowledge that the filtering criterion is specific to this model population.

7. **Uneven field distribution weakens per-field comparisons.** Physics (68), Math (61), and Biology (61) dominate, while Data Science (3), AI (8), Aerospace (8), ICE (7), and Energy (9) have very few questions (Figure 2). Per-field radar charts and conclusions (e.g., "En records the lowest overall average") are unreliable for fields with <10 questions, where a single correct/incorrect answer shifts scores by 10%+.

8. **No variance reported.** Results are "averaged over three trials" (Line 211) but no standard deviations or confidence intervals are given. Given the small dataset (505 questions), trial-to-trial variance could be substantial.

9. **502/505 inconsistency.** The abstract states "502 tasks" (Line 9), while the introduction and Section 3.1 state "505 questions" (Lines 21, 58). Figure 2's per-field counts sum to 502.

### Trivial

None.

## Nice-to-Haves

- Report results stratified by the claimed evaluation dimensions (knowledge depth, reasoning, terminology, contextual analysis) or remove the claim.
- Report results by difficulty level.
- Report scores of the same 12 models on one or more existing benchmarks (e.g., MMLU-Pro, GPQA) to demonstrate what LPFQA adds.
- Provide confidence intervals or Bayesian credible intervals for per-field scores, especially for fields with <15 questions.
- Clarify whether short-answer evaluation is performed by LLM-as-judge, string matching, or human review.

## Removed Points

These points were raised in the harsh review but are removed per filtering rules:

- **Missing specification of which MLLM/LLM was used in the pipeline:** The reviewer acknowledged this detail may be in the appendix (which was stripped by the parser). The paper's Reproducibility Statement (Line 333) explicitly promises to provide "all prompts used for question generation" in the appendix. Removed per rule about missing appendix content.
- **"CS 2121" formatting issue in Table 2:** This is a parser artifact (concatenation of "21" and "21"). Removed per rule about formatting artifacts.
- **"DeepSeep" typos in figure captions:** Parser artifacts. Removed per rule about formatting/typo issues.
- **Speculations about what the appendix may or may not contain:** Removed per rule about missing appendix content.

## Novel Insights

The key insight that emerges from this review is that the paper claims four innovations (evaluation dimensions, difficulty hierarchy, user personas, interdisciplinary integration) but only one (interdisciplinary integration via 20 fields) is actually evidenced in the evaluation. The other three are described at the design level but never operationalized in the results section. This creates a gap between the paper's self-presentation and what it actually delivers—a gap large enough that a reader relying only on the abstract would have a materially misleading picture of the paper's contributions.

## Suggestions

1. **Define the scoring metric explicitly.** State whether "Score" is accuracy (percentage correct), a weighted combination, or something else. Report raw correct/total counts alongside normalized scores.
2. **Correct the DeepSeek-V3 analysis.** Remove or reframe the erroneous claim, and offer a sober interpretation of the actual ranking.
3. **Operationalize the claimed evaluation dimensions** by labeling questions and reporting per-dimension results, or remove the claim if it cannot be realized.
4. **Add at least one comparative benchmark analysis** (e.g., same models on MMLU-Pro or GPQA) to demonstrate LPFQA's discriminative properties.
5. **Resolve the 502/505 inconsistency** and acknowledge the field-size limitation on per-field conclusions.

## Score and Decision

The paper identifies a legitimate gap and its construction pipeline has merit. However, the paper as submitted has several problems that prevent its contribution from being assessable: the scoring metric is never defined (making all empirical results uninterpretable), the main analysis contains a clear factual contradiction, and three of four claimed innovations are not demonstrated in the evaluation. These are fixable with substantial revision, but in its current form the paper cannot be accepted.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>