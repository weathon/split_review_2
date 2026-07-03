Now let me proceed to finalize the review.

The calibration search tool is unavailable, so I will calibrate against my knowledge of the review standards. Let me produce the final consolidated review.

---

## Summary

This paper introduces *Ambig-SWE*, a benchmark derived from SWE-Bench Verified that creates synthetic underspecified variants of GitHub issues and evaluates LLM-based agents across three capabilities: detecting underspecification, asking clarification questions, and leveraging interaction to improve task completion. Six models (Claude Sonnet 3.5/4, Claude Haiku 3.5, Qwen 3 Coder, Deepseek-v2, Llama 3.1 70B) are evaluated, with findings showing that interaction can substantially improve performance but that models default to non-interactive behavior and struggle to detect when information is missing.

## Strengths

1. **Three-stage decomposition of underspecification handling.** Rather than treating underspecification as a single failure mode, the paper structures evaluation around three distinct capacities (detection in §4, questioning in §5, integration in §3). This modular design enables targeted analysis and improvement of individual capabilities, a clear advance over prior work that measures only end-to-end resolve rates.

2. **Paired synthetic-underspecified dataset enabling causal measurement.** By generating underspecified variants from fully-specified SWE-Bench Verified issues while preserving complete ground-truth specifications (§2.1 lines 59–68), the design allows measuring whether performance improvements come from resolving genuine underspecification versus other confounding factors. This is a methodological improvement over evaluating on naturally-occurring underspecified issues that lack verified correct specifications.

3. **Navigational vs. informational detail analysis (Table 1).** The finding that Qwen 3 Coder's resolve rate *worsens* after receiving file-location information (52.38% with info vs. 55.43% without) reveals a specific rigidity failure pattern — the model follows a fixed protocol rather than adaptively integrating user input — that is not observable from aggregate resolve rates alone.

4. **Exploration-first questioning strategy insight (§5.3).** The observation that Claude Sonnet models achieve comparable information gain to Qwen 3 Coder (0.171 vs. 0.179 cosine distance) with ~50% fewer questions (4.03 vs. 6.02) by exploring the codebase before asking provides concrete, actionable design guidance for agent development.

5. **Prompt-engineering ablation across three encouragement levels (Table 2).** Testing Neutral, Moderate, and Strong interaction prompts reveals that Qwen 3 Coder maintains 100% FNR across all conditions, providing clear evidence that prompt engineering alone is insufficient — a result that would be missed in a single-prompt study.

## Weaknesses

### Major

1. **Unequal turn allocation confounds cross-model Interaction comparisons.** Claude Sonnet 4 and Qwen 3 Coder receive up to **100 turns** while all other models are capped at **30 turns** (line 106). The paper justifies this by citing "greater reasoning and planning capacity," but this means cross-model comparisons in the Interaction setting conflate interaction capability with resource budget. For example, the finding that "Claude Sonnet 4 attains the highest relative performance (89%)" (line 127) could be driven partly by the 3.3× larger action budget. Within-model Hidden→Interaction comparisons (e.g., "Sonnet 3.5 recovers 80% of the performance gap") are not affected, but claims about cross-model rankings of interaction effectiveness are undermined.

2. **Claude Sonnet 4's Hidden baseline is computed on only 100 of 500 instances.** Footnote 4 (line 131) states Sonnet 4 was evaluated on a 100-instance subset for the Hidden setting, while its Interaction and Full scores use the full 500. This means: (a) the Hidden→Interaction improvement (40.00% → 61.40%) is computed on different instance sets and its magnitude is not directly comparable to other models'; (b) cross-model Hidden-setting comparisons (e.g., "Qwen 3 Coder achieves 45.6% vs. Sonnet 4's 40.0%") may reflect instance selection rather than capability differences. The paper acknowledges this in a footnote but does not discuss how it affects comparability.

3. **The "up to 74%" headline claim is unsupported by the presented data.** The abstract and introduction state that interactivity boosts performance "up to 74% over the non-interactive settings" (lines 9, 37). Computing (Interaction−Hidden)/Hidden from Figure 3 yields: Llama 50%, Deepseek 32.1%, Haiku 100%, Sonnet 3.5 63.6%, Qwen 18%, Sonnet 4 53.5%. **None equals 74%.** If the intended computation is gap-closing — (Interaction−Hidden)/(Full−Hidden) — the maximum is ~76% for Sonnet 4, but this is not what "over the non-interactive settings" means. Since this is the paper's most prominent quantitative headline, it requires correction or clarification.

4. **GPT-4o circularity in RQ3 evaluation.** GPT-4o is used as both the user proxy that generates responses and as the LLM-as-judge that scores those same responses (lines 84, 227). The LLM-as-judge scores (Figure 6) therefore measure GPT-4o's internal consistency rather than the actual informativeness of responses to a human. The cosine distance metric (using text-embedding-3-small) is more robust to this concern, but the qualitative analysis in §5.3 is more informative than either quantitative metric. An ablation using a different model as evaluator would strengthen confidence.

### Minor

5. **Detection measured indirectly through interaction behavior in RQ2.** The experiment measures detection by whether models *choose to interact* (line 168), not through explicit classification. A model might detect underspecification but decide not to ask questions for other reasons (overconfidence, task protocol, etc.). The paper interprets non-interaction as failure to detect, which conflates detection capability with willingness to act. This is noted but not adequately discussed as a limitation of the RQ2 design.

6. **No error bars or variance estimates on resolve rates.** All resolve rates (Figure 3, Table 1) are reported as point estimates. For models with low base rates (e.g., Llama 3.1 at 3.2% — ~16 successes out of 500), uncertainty is substantial. Confidence intervals would substantially strengthen confidence in the reported rankings.

### Trivial

7. **Synthetic underspecification may not capture real-world patterns.** The authors' own distributional analysis (lines 64–66) shows natural underspecified issues contain more code snippets, error messages, and conversational fragments. This means Ambig-SWE primarily measures a specific kind of vague-task-summary underspecification. The authors acknowledge this limitation.

## Nice-to-Haves

- Run the Interaction setting for all models at a uniform turn budget (e.g., 30 turns for everyone) to verify that cross-model rankings hold with equal resources.
- Compute Claude Sonnet 4's Hidden score on all 500 instances, or report which 100 were sampled and justify representativeness.
- Test an alternative user proxy (e.g., a different LLM) to verify that the RQ3 results are not artifacts of GPT-4o-to-GPT-4o communication.

## Removed Points

The following points from the reviewer inputs were removed with justification:

- **"Circularity in underspecification generation and user proxy"** (Harsh Critic point 3): The claim that using GPT-4o for both generating underspecified variants and serving as the user proxy creates methodological circularity is overstated. The user proxy is designed to respond only with information explicitly present in the *full* specification — it does not interpret or reason about the underspecified variant. It functions as a controlled information channel, not an interpretative oracle. The circularity concern mainly applies to the LLM-as-judge role (already captured in Major weakness 4 above).

- **"User proxy more predictable than real users"** : The paper explicitly acknowledges this in its conclusion/limitations section (line 281). This is a properly disclosed limitation of a controlled study, not an unaddressed flaw.

- **"Interaction is forced/compulsory"** : The paper also explains this (footnote 3) — models default to non-interactive behavior without compulsory prompting. For the purpose of measuring interaction *capability* rather than *proactivity*, forced interaction is a necessary and appropriate design choice.

- **Generic strengths from Strength Finder** : The Strength Finder labeled "three-stage decomposition" and "paired dataset" as strengths, which are already included above. A generic statement about "the problem being important" was dropped as it is a generic claim that applies to the broad area rather than a specific strength of this paper.

- **"The three capabilities are evaluated on different settings"** (Harsh Critic): This is presented as a weakness, but it is by design — the paper deliberately decomposes evaluation across settings. This is a feature, not a bug, and is consistent with the paper's stated goal of enabling targeted analysis of individual capabilities.

## Novel Insights

None beyond the paper's own contributions. The review process confirms that the paper's three-part decomposition framework is genuinely useful, and that the qualitative findings (exploration-first strategies, navigational information rigidity in Qwen, prompt-engineering insufficiency) are the most robust contributions. No reviewer synthesized a genuinely novel observation that the paper itself does not already articulate.

## Suggestions

1. **Correct or clarify the "74%" claim.** Provide the exact computation and the model it applies to. If it refers to gap-closing relative to the Full setting rather than direct percentage improvement, say so explicitly and use different phrasing ("recovers up to 76% of the performance gap" rather than "74% over the non-interactive settings").

2. **Equalize turn budgets for cross-model Interaction comparisons.** Run all models at 30 turns and (optionally) at 100 turns for capable models. Report both so readers can disentangle capability from resource effects.

3. **Compute Claude Sonnet 4's Hidden score on all 500 instances.** If cost is prohibitive, report the exact composition of the 100-instance subset and provide evidence that it is representative.

4. **Report confidence intervals or bootstrap estimates for resolve rates.** This is particularly important for low-performing models where the number of successes is small.

5. **Add an ablation for RQ3 using a different model as evaluator** (e.g., Claude Sonnet 4) to verify that the LLM-as-judge scores are not artifacts of GPT-4o evaluating its own outputs.

## Score and Decision

After careful consideration of the paper's genuine contributions against the verifiable methodological issues:

**Score rationale:** The paper introduces a useful benchmark and analytical framework, and its qualitative findings about exploration strategies, navigational vs. informational information, and detection failures are valuable. However, three verifiable issues undermine the quantitative precision of its central claims: (1) the unequal turn budget confounds cross-model Interaction comparisons, (2) the "up to 74%" headline number is inconsistent with the reported data, and (3) Claude Sonnet 4's Hidden baseline is computed on a different (smaller) instance set. These are fixable with additional experiments but are present in the current submission. The qualitative contributions are publishable, but the quantitative claims as presented are not sufficiently reliable.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>