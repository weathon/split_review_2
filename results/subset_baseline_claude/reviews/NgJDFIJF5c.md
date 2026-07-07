## Summary

Strata-Sword is a hierarchical, bilingual (Chinese-English) jailbreak safety benchmark for LLMs organized by "Reasoning Complexity." The authors decompose reasoning complexity into three dimensions—Logical Depth, Linguistic Ambiguity, and Task Overhead—and use these to classify 15 jailbreak attack methods into three levels. A key contribution is the introduction of novel Chinese-specific attacks (Character Disassembly, Lantern Riddle, Acrostic Poem). The benchmark is applied to evaluate 23 LLMs and LRMs, revealing that ASR generally increases with complexity level and that models have distinct safety profiles across languages.

## Strengths

- **Novel Chinese-specific attacks**: The Character Disassembly, Lantern Riddle, and Acrostic Poem attacks are genuinely novel, linguistically motivated, and fill a real gap. The paper offers concrete reasoning for why pictographic language properties create unique attack surfaces not covered by English-only benchmarks.
- **Broad evaluation scope**: Evaluating 23 models including recent frontier systems (GPT-5, Claude-3.7, Gemini-2.5-Pro, Qwen3, Oyster, RealSafe, STAIR) makes the benchmark immediately relevant and the results table is the most informative part of the paper.
- **Bilingual framing reveals genuine disparities**: The observation that safety fine-tuning is language-imbalanced (e.g., DS-Distill-Qwen3 improves significantly in English but barely in Chinese) is a concrete, practically important finding supported by quantitative results.

## Weaknesses

### Fatal
None.

### Major

1. **Ambiguous and partially circular level classification criteria.** The criteria for assigning attacks to levels are defined in terms of "one or two reasoning steps" (Level 2) vs. "more than three" (Level 3), but no methodology is provided to count reasoning steps for arbitrary attacks. The claim that an attack belongs to Level 3 if it "meets any above factors or satisfies two different factors defined for Level 2" is ad hoc. For example, "Long Text" is placed at Level 2 under "Simple Logical Depth," yet many-shot jailbreaking (Anil et al., 2024) is widely recognized as a distinct, non-trivial phenomenon. The classification criteria seem post-hoc and could assign a new attack to an arbitrary level without a principled protocol.

2. **Figure 3 (closed-source per-model ASR pie charts) is uninformative and potentially misleading.** The associated table shows identical 10% values for nearly all attack types across all five closed-source models, which corresponds to uniform benchmark composition (10 attack types × 10% = 100%), not model-specific ASR distributions. The text states "The ASR ratio for different jailbreak attacks in three levels for closed-source LLMs" and discusses model-specific weaknesses (e.g., "Gemini-2.5-Pro demonstrates obvious weaknesses against Chinese Character Split"), but the data in the table does not support differentiated claims. This is a significant inconsistency between the visualization and the narrative.

3. **No validation of the QwQ-32B judge.** The entire benchmark's validity rests on QwQ-32B correctly classifying responses as "safe" or "unsafe." No human annotation agreement study, comparison against other judges, or analysis of false-positive/negative rates is provided. Given that evaluating jailbreak success is itself a nuanced judgment task, this is a major methodological gap.

### Minor

1. **Small dataset size per attack type.** The benchmark contains 700 total instructions across 15 attack methods and 2 languages. Some Level 3 attacks (e.g., Lantern Riddle, Acrostic Poem) have only ~100 samples in a single language, making model-specific comparisons statistically fragile.

2. **The multi-turn attack implementation is known to be flawed.** The paper acknowledges that multi-turn contexts are concatenated into a single input, which may not replicate the interactive dynamics. This design choice artificially weakens that attack, making the Level 3 cross-attack comparisons inconsistent.

3. **Insights 1, 3 are expected.** The observations that ASR increases with reasoning complexity and that safety follows a scaling law are predictable and broadly known. Framing these as major "Insights" overstates their novelty.

### Trivial
- The description of Level 2 mentions "12 reasoning steps" which appears to be a formatting artifact for "1–2 reasoning steps."

## Nice-to-Haves

- An inter-annotator agreement study or human evaluation to validate the QwQ-32B judge would significantly strengthen the paper.
- A protocol for assigning future attacks to levels (e.g., a rubric or annotation template) would make the taxonomy extensible.
- Correct and informative per-model ASR distributions in Figure 3, ideally as bar charts with actual percentages per attack per model.

## Novel Insights

The paper's most genuinely novel insight is that Chinese linguistic structures (logographic characters, acrostic conventions, lantern riddle formats) create an attack surface qualitatively different from phonetic English, and that current safety fine-tuning is systematically under-resourced for Chinese. The quantitative demonstration—specifically the DeepSeek-distilled Qwen3 showing 2× improvement in English but near-zero improvement in Chinese after fine-tuning—concretely substantiates this claim and has direct implications for multilingual safety alignment practice.

## Suggestions

- Conduct a human evaluation of ≥200 QwQ-32B judgments across attack types to report judge accuracy and establish ground truth.
- Replace Figure 3 pie charts with per-model heatmaps showing actual attack-specific ASR so the claimed model-specific vulnerabilities are legible in the data.
- Provide an explicit operationalization protocol (e.g., step-counting annotation guide) so future attacks can be reproducibly assigned to complexity levels.
- Increase dataset size per attack or report confidence intervals to make cross-attack comparisons more credible.

## Score and Decision

The benchmark addresses a real need, and the Chinese-specific attacks are genuinely novel. However, the classification framework lacks rigor, the primary evaluation figure (Figure 3) is inconsistent with its described purpose, and the LLM judge is unvalidated. These are substantive issues in a benchmark paper where the reliability of the evaluation instrument is paramount. The paper is borderline: the idea is solid, the execution needs hardening.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>