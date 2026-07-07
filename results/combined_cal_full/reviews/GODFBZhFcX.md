## Summary

This paper proposes PCE (Planner-Composer-Evaluator), a framework that extracts the implicit assumptions latent in LLM reasoning traces, structures them into a decision tree, and scores each path by likelihood, gain, and cost for uncertainty-aware action selection in embodied multi-agent settings. The key insight is that rather than relying on communication-heavy coordination to resolve uncertainty, one can surface and systematize the assumptions LLMs already make internally. Experiments on C-WAH and TDW-MAT benchmarks with three LLM backbones (GPT-4o mini, GPT-OSS:20B, Gemma3:4B) show consistent improvements over communication-centric baselines, and a user study evaluates human perception of the resulting communication patterns.

## Strengths

- **A genuinely novel idea with strong motivation.** The core insight — that LLM planners already generate implicit assumptions about uncertainty in their reasoning traces, and that these can be extracted and structured rather than relying on communication-heavy coordination — is creative and well-grounded. The paper identifies a real weakness in current communication-centric approaches (Section 1, paragraphs 2–3) and the proposed solution directly addresses it. This conceptual contribution goes beyond prompt-engineering improvements to existing frameworks.

- **Clean, modular method design.** The Planner-Composer-Evaluator pipeline (Sections 4.2–4.4) is clearly described with well-defined roles for each component. The Planner surfaces initial action-assumption links, the Composer structures them into a decision tree, and the Evaluator scores paths by scenario likelihood, conditional gain, and execution cost. The utility function $U(\mathcal{S}, a) = \mathbb{E}[\text{gain}] - \lambda C(a)$ (Section 4.4) is sound and appropriately simple for the setting.

- **Broad backbone evaluation strengthens generality claims.** Running the method on three diverse LLMs (GPT-4o mini, GPT-OSS:20B, Gemma3:4B) — a good mix of commercial, open-source, and reasoning-specialized models — is well-motivated. The scaling ablation (Figure 3) showing that PCE's benefits persist across model sizes (Gemma3: 4B→12B→27B) and reasoning depths (Low→Medium→High) where the Planner-only baseline plateaus is a particularly informative addition.

- **User study goes beyond typical evaluation.** The human evaluation in Section 5.3, though limited in scope, tests a claim that automated metrics cannot: that selective communication (as produced by PCE) is perceived by human partners as more appropriate, efficient, and trustworthy than no-communication or always-communication baselines. This is a genuine strength — most papers in this area do not include any human evaluation.

## Weaknesses

### Major

- **No variance, error bars, or statistical significance reported.** The main evaluation sets are small (C-WAH: 10 episodes; TDW-MAT: 24 episodes), and all results are reported as single point estimates without standard deviations, confidence intervals, or multiple-seed runs. We cannot assess whether PCE's advantages (e.g., 42.76 vs. 46.80 steps on C-WAH with GPT-4o mini; 87.50% vs. 81.25% on TDW-MAT with GPT-4o mini) are robust or could be within the noise of LLM stochasticity. Figure 3 similarly plots clean lines without error bars. The paper uses "consistently outperforms" throughout, but the evidence as presented does not support claims about consistency without any quantification of variance. This is the most significant gap between the strength of the claims and the strength of the evidence.

### Minor

- **User study limitations.** The study (N=12) reports mean scores on 7-point Likert scales without any statistical tests — with 12 participants, the visible differences in Figure 4 could be non-significant. Additionally, participants observed and evaluated agent behavior rather than actually collaborating with the agent, so the study measures perceived trustworthiness of observed behavior rather than genuine collaborative performance.

- **Token usage framing is selectively optimistic.** The abstract and conclusion state PCE achieves "comparable token usage" to baselines. On C-WAH this is reasonably accurate (PCE is competitive with or better than most baselines). However, on TDW-MAT, PCE uses 42–88% more tokens than CoELA, the most token-efficient baseline (Table 2: e.g., PCE 197,807 vs. CoELA 113,059 with GPT-4o mini). While PCE outperforms CaPo and CoTS on tokens, the framing elides the CoELA comparison. A more precise characterization would be that PCE trades higher per-step inference cost for shorter episodes, achieving competitive aggregate token consumption with substantially better task performance.

- **Hyperparameters listed without justification.** The default settings $\alpha=\beta=\lambda=1$, $D=3$ (Section 5) are presented without sensitivity analysis or discussion of whether they were tuned on the benchmarks. This raises a question about whether baselines, whose own hyperparameters may not have been similarly tuned, are at a disadvantage. (The paper notes hyperparameter sensitivity analyses in Appendix A.5, which cannot be verified here but partially addresses this concern.)

- **No discussion of failure cases or limitations.** The paper presents uniformly positive results without acknowledging scenarios where PCE might predictably fail — e.g., if the Planner's reasoning trace contains incorrect assumptions, the Composer will faithfully structure them and the Evaluator may confidently select a wrong action. A limitations paragraph would strengthen credibility.

- **Several method details deferred to appendix.** The Composer's "local ranking policy" (Section 4.3) is described as using "LLMs' commonsense reasoning" to approximate POMDP criteria, but the exact criterion and how it is operationalized are not specified in the main text. The paper notes that prompting strategies are in Appendix A.12, but a reader relying on the main text cannot assess how reliably these operations work.

### Trivial

None.

## Nice-to-Haves

- Add wall-clock time measurements. Given that PCE makes multiple LLM calls per step (Planner + Composer + Evaluator), real-time performance is a practical concern for embodied agents that the paper acknowledges but does not quantify.
- Run the component ablation (Table 3) on at least one additional backbone and on TDW-MAT to support the claim that each module contributes essentially across settings.
- Characterize the stability and calibration of the LLM-generated likelihood/gain/cost scores (the paper references human-expert correlation studies in Appendices A.10–A.11, which partially addresses this).

## Removed Points

The following points from the harsh critic input were removed after verification:

- **"Core mechanism relies on LLM-generated numerical scores with no reliability analysis"** — REMOVED because the paper explicitly states "reliability assessments of the Composer and Evaluator based on human-expert correlation studies" exist in Appendices A.10 and A.11. While the degree of coverage cannot be verified, the claim of "no analysis" is factually contradicted by the paper's own text.
- **"Composer's tree expansion is underspecified as a fatal/major issue"** — REMOVED in its strong form because the paper states "Detailed prompting strategies for Planner, Composer, and Evaluator are provided in Appendix A.12." The parser strips appendices; the original submission contains these details. Retained as a minor weakness about the main text's clarity.
- **"Framing is broader than actual contribution (multi-agent vs. single-agent belief)"** — REMOVED as scope creep. The paper operates in a multi-agent decentralized setting; the method handles each agent's own belief state, which is standard for decentralized POMDP formulations.
- **"Assumptions may not be independent (tree structure limitation)"** — REMOVED as speculative. The paper acknowledges it uses "commonsense reasoning" rather than true probabilities, and the concern is not demonstrated to materially affect results.
- **"No prior work claim about scaling is too strong"** — REMOVED as a phrasing nitpick.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add variance information.** Run evaluations multiple times (3–5 seeds with different LLM temperatures) and report means with standard deviations or confidence intervals for all main metrics. This is the single highest-leverage improvement. For deterministic benchmark episodes, report per-episode statistics (e.g., box plots or histograms) instead of just means.

2. **Reframe the token usage claim.** Replace "comparable token usage" with more precise language such as "competitive aggregate token consumption" or "higher per-step cost offset by shorter episodes," acknowledging the tradeoff with CoELA explicitly.

3. **Add a limitations paragraph.** Discuss failure modes: cases where the Planner generates misleading assumptions that the Composer then structures confidently, sensitivity to the quality of the initial reasoning trace, and the assumption that assumptions can be treated as conditionally independent in the tree structure.

4. **Strengthen the user study.** Add statistical significance tests (even paired t-tests or Wilcoxon signed-rank tests) to validate that the observed differences are not due to chance with N=12. If possible, increase sample size or add a between-subjects condition with actual collaborative interaction.

5. **Expand the component ablation.** Run Table 3 on at least one additional backbone (GPT-OSS:20B or Gemma3:4B) to confirm the "each module contributes essentially" claim across different model types.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| CoELA | EnXJfQqy0K.md | 6.50 | R1-Band4 | Yes | Same benchmarks, similar evaluation methodology. CoELA had weaker negatives (-2.22, -2.38) but our paper has more novel core idea. |
| CaPo | KRv9NubipP.md | 6.00 | R1-Band4 | Yes | Same benchmarks. CaPo was heavily penalized for limited novelty (-7.10 to -9.81), which is not our paper's problem. |
| ReAd | y5tkxH7kxQ.md | 5.00 | R1-Band4 | Yes | LLM multi-agent collaboration. Had novelty and unfair comparison concerns. Our paper has clearer novelty but weaker experimental reporting. |
| YOLO-MARL | SOXxa4pPGY.md | 4.00 | R1-Band4 | Yes | Had concerns about single-run results without error bars (-3.16) and novelty (-8.27). Our paper's novelty is stronger. |
| Tree-Planner | Glcsog6zOe.md | 5.25 | R2-Narrow | Yes | Similar tree-structured LLM planning concept. Penalized for single environment, limited tasks (-10.14 for originality). Our paper has broader evaluation but similar reporting gaps. |
| DeLLMa | Acvo2RGSCy.md | 7.33 | R2-Narrow | Yes | Decision-making under uncertainty with LLMs. Had similar human evaluation weakness (-3.95) and appendix reliance (-7.16), but stronger theoretical framing and ablation. |
| Gen. World Explorer | 8NlUL0Cv1L.md | 6.25 | R2-Narrow | Yes | Had strong negatives (-5.08 to -6.18) yet scored 6.25, suggesting even papers with significant weaknesses can reach borderline accept. |

### Bracket and Calibration

**Round 1 bracket:** 4.0 – 6.5. The paper is clearly above YOLO-MARL (4.0, which had both novelty and rigor issues) and likely below CoELA (6.50, which had very mild negatives and stronger positive weights).

**Narrowing comparison:** Against CoELA (6.50), our paper has a more novel core idea (extracting latent assumptions vs. communication-based coordination) but weaker reporting rigor (no variance vs. CoELA's mild negatives of -2.22, -2.38). Against Tree-Planner (5.25), our paper has broader evaluation (2 benchmarks, 3 backbones) and a more novel idea (Tree-Planner was criticized with -10.14 for limited originality). Against CaPo (6.00), our paper lacks the heavy novelty criticisms that pulled CaPo down.

**Final placement:** The paper's weighted items show strong positives (+5.25 for multi-backbone evaluation, +4.20 for user study) and two notable negatives (-3.89 for variance, -4.27 for user study quality). The variance weakness (-3.89) is the decisive factor pulling the score below CoELA (6.50) and CaPo (6.00). The paper lacks any of the -7 to -10 novelty criticisms that dragged down those anchors. This places it at 5.5 — above reject territory but below the stronger empirical standards set by the 6.0+ anchors.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>