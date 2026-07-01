Now let me produce the final review.

## Summary

This paper introduces Ambig-SWE, an underspecified variant of SWE-Bench Verified, and evaluates how well LLM-based coding agents handle missing information through interaction with a simulated user. The authors decompose underspecification handling into three capacities (detection, question-asking, and integration) and evaluate six models across three settings: Full (fully specified), Hidden (underspecified, no interaction), and Interaction (underspecified, with interaction). Key findings include that interaction significantly improves performance for most models, but models default to non-interactive behavior, struggle to detect underspecificity, and vary widely in question quality. Notable findings: Qwen 3 Coder completely refuses to interact under any prompt, and interaction improves effectiveness but not efficiency.

## Strengths

- **Well-motivated problem framing.** The paper clearly distinguishes underspecificity (missing information) from the narrower concept of ambiguity (single-detail unclearness) studied in prior work (lines 31–35), and motivates why complex agentic tasks create qualitatively harder challenges with multiple interdependent gaps. The running example (Figure 1) cleanly illustrates the failure mode.

- **Clean three-stage decomposition.** By separating resolution into detection (RQ2), question-asking (RQ3), and integrated problem-solving (RQ1), the framework avoids treating task success as a monolithic metric and enables targeted diagnosis of where models fail. The three experimental settings (Full, Hidden, Interaction) allow clean attribution of the effect of interaction.

- **Rigorous dataset construction with honest limitations.** The authors conduct a distributional difference analysis comparing their GPT-4o-generated underspecified issues against naturally-occurring ones (lines 64–66), explicitly acknowledge where their data differs (more aggressive information removal), and explain why natural underspecified examples cannot be used (lack of paired ground truth, line 68). This methodological transparency is above the norm for benchmark papers.

- **Several non-obvious and practically relevant findings.** (a) Qwen 3 Coder's complete refusal to interact under any prompt (100% FNR in RQ2, line 190) despite being a strong SWE-Bench performer — a real and surprising failure mode. (b) Qwen 3 Coder's performance actually *worsens* when given navigational information (Table 1), revealing rigid protocol-following. (c) Interaction improves effectiveness but not efficiency across all models (line 127). (d) Claude Haiku matches Sonnet 3.5's gap-recovery rate despite much worse raw coding ability, suggesting interaction skill is partially independent of coding skill.

## Weaknesses

### Fatal
None.

### Major

- **Asymmetric evaluation of Claude Sonnet 4 in the Hidden setting.** Sonnet 4 is evaluated on only 100 of the 500 instances in the Hidden setting, while all other models and all other settings (Interaction, Full) use the full 500 instances (footnote at line 131). This means the headline comparison — Sonnet 4's improvement from Hidden (40.0%) to Interaction (61.4%) — compares results from different test sets. The Hidden baseline (100 instances) may not be representative, and the "gap recovery" percentage mixes different instance sets. The main text provides no way to assess how the 100-instance subset was selected (random? stratified? first 100?) or whether it is representative. This directly affects the validity of the paper's strongest quantitative claims about the best-performing model.

- **Unequal interaction turn limits across models.** Sonnet 4 and Qwen 3 Coder receive up to 100 interaction turns while all other models are limited to 30 (line 106). The stated justification — "greater reasoning and planning capacity" — introduces a confound: higher Interaction-setting performance for these models may partly reflect more opportunity to explore, edit, and test, rather than better underspecification handling. The paper partially mitigates this by reporting average steps (65–75, below the cap), but the asymmetric cap means outlier cases are gated differently across models, making clean comparison of interaction effectiveness impossible.

### Minor

- **User proxy (GPT-4o) shares lineage with evaluated models and is maximally cooperative.** The simulated user is GPT-4o (line 84), which shares training data and interaction norms with several evaluated models. The proxy is instructed to always provide correct information, never get frustrated, and never provide misleading information. This creates an idealized setting where interaction results may be specific to the GPT-4o-as-user configuration — different models' questions might receive less useful responses from a different proxy or from a real human. The paper acknowledges this at line 281 but does not explore sensitivity to proxy choice, making it unclear whether findings generalize beyond this specific setup.

- **Synthetic underspecification differs from natural underspecification in known, unanalyzed ways.** The underspecified issues are generated by GPT-4o. The distributional analysis (lines 64–66) shows generated issues have more aggressive information removal (fewer code snippets, error messages) and fewer conversational fragments than natural underspecified issues. The paper correctly explains why natural examples cannot be used (no paired ground truth), but does not discuss the likely direction of bias — would real underspecified issues (with partial code/error snippets but less complete context) benefit more or less from interaction than these synthetic ones?

- **No human validation of generated underspecified variants.** The paper validates through aggregate distributional analysis and LLM-based annotations, but reports no human evaluation (e.g., inter-annotator agreement on whether individual generated variants are genuinely underspecified). A small-scale human check would strengthen confidence that the generated issues are realistic and that the removed details are indeed the critical ones.

- **Data leakage acknowledged but unquantified.** The paper notes Qwen 3 Coder's Hidden performance "potentially inflates due to reliance on internal knowledge" (line 127), implying training data contamination on SWE-Bench tasks, but provides no analysis of magnitude or impact.

### Trivial

- **Ambiguous "up to 74%" phrasing in the abstract (lines 9, 37).** The claim reads as a relative improvement over the Hidden setting, but the actual numbers (e.g., Sonnet 4: 40→61.4 is a 53.5% relative increase; Haiku: 13.4→26.8 is 100%) indicate the figure refers to gap recovery (Sonnet 4 recovers ~76% of the Hidden-to-Full gap). Clarifying this would prevent misinterpretation.

## Nice-to-Haves

- **Human evaluation of question quality.** A small-scale developer study on whether generated questions are helpful or burdensome would ground the LLM-as-judge metric.
- **Ablation with a different user proxy.** Running a subset of experiments with a non-GPT-4o proxy (e.g., Llama-based or rule-based) would test whether findings generalize beyond this configuration.
- **GPT-4o as an agent baseline.** Since GPT-4o serves as the user proxy, evaluating it as an agent under all three settings would provide a useful calibration point.
- **Quantified data leakage analysis.** Testing on a held-out set of recent GitHub issues not present in SWE-Bench would directly assess the contamination concern.

## Removed Points

These points are flagged to be removed based on meta-review filtering rules. Treat them with caution.

1. **Criticism that Table 4 / p-values are only in the appendix.** The rule about missing appendix content applies: the parser strips appendix sections from all papers; these exist in the original submission. The core concern about asymmetric evaluation (Sonnet 4 on 100/500 instances) is verifiable from the main text (footnote 4 at line 131) and is retained as a Major weakness.

2. **Criticism that "cannot be verified from the main text" regarding statistical significance.** Same reason as above — the appendix content exists in the original submission.

3. **Criticism about missing qualitative examples in the appendix.** Same reasoning.

4. **Several generic "Strengthening the Paper on Its Own Terms" suggestions about "fix the asymmetric evaluation" and "report on consistent instance set."** These are valid but are already captured in the Major weakness about asymmetric evaluation and in Suggestions below, so the duplicated framing is removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Fix the asymmetric evaluation.** Run Sonnet 4 on the full 500 instances in the Hidden setting, or alternatively report all Sonnet 4 results (Hidden, Interaction, Full) on a consistent 100-instance subset so that at least one internally consistent comparison is available.
- **Clarify "up to 74%."** Add a sentence in the abstract specifying whether this refers to relative improvement or gap recovery, with the specific model and calculation.
- **Discuss direction of bias from synthetic data.** A paragraph analyzing whether real underspecified issues would likely show larger or smaller interaction benefits would help readers calibrate.
- **Report human validation** on a random sample of generated underspecified variants.
- **Analyze data leakage sensitivity.** Show how conclusions change when removing or flagging Qwen 3 Coder and Sonnet 4, the two models most susceptible to contamination concerns.

## Calibration

**Round 1 (Bracketing).** Queries across score bands retrieved the following anchor papers:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| SWE-bench (VTF8yNQM66) | 6.25 | R1 | Foundational benchmark using real GitHub issues; stronger methodological consistency but simpler framing. Ambig-SWE has more novel problem framing and broader evaluation, but uses synthetic data and has evaluation inconsistencies. |
| RefactorBench (NiNIthntx7) | 6.50 | R1 | 100 handcrafted refactoring tasks; stronger methodology but narrower evaluation (1-2 models). Ambig-SWE is more comprehensive in model coverage but has more significant methodological concerns. |
| τ-bench (roNSXZpUDN) | 6.50 | R1 | Tool-agent-user interaction benchmark; very similar user-simulation methodology. Ambig-SWE shares the same user-proxy limitation but has an additional asymmetric evaluation issue not present in τ-bench. |
| SWE-bench Multimodal (riTiq3i21b) | 5.00 | R1 | SWE-Bench variant for JavaScript+images; some reviewers called it incremental. Ambig-SWE has a stronger, more novel problem framing and more thorough evaluation. |
| ML-Bench (sf1u3vTRjm) | 5.75 | R1 | ML repository benchmark; rejected despite 5.75 avg due to mixed reviews (8,6,3,6). Ambig-SWE has clearer contribution framing and more transparent methodology. |
| Commit0 (MMwaQEVsAg) | 6.67 | R1 | Library generation benchmark; accepted. Stronger methodology but less model coverage. |
| DataSciBench (BltaWJZMeR) | 3.20 | R1 | LLM-generated data benchmark; rejected due to quality concerns. Ambig-SWE is substantially stronger in framing, transparency, and analysis. |

**Round 1 bracket:** 5.0–6.5 (Ambig-SWE is stronger than SWE-bench Multimodal at 5.0 but has methodological concerns that make it weaker than τ-bench at 6.5).

**Round 2 (Narrowing).** Retrieved SWE-bench Multimodal (5.00, Accept) and τ-bench (6.50, Accept) as closest topical analogs. Ambig-SWE is more novel than SWE-bench Multimodal but has an evaluation asymmetry that τ-bench does not. Final score anchored between these two.

**Final score:** 6.0 — borderline accept. The paper's framework and qualitative findings are valuable, but the asymmetric evaluation of Sonnet 4 and unequal turn limits weaken confidence in the headline quantitative comparisons. These issues are fixable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>