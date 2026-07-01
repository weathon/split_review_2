Now let me write the final review.

## Summary

PLAGUE proposes a modular three-phase framework (Planner → Primer → Finisher) for generating multi-turn LLM jailbreaks, augmented with a lifelong learning memory component that stores and retrieves successful strategies. The key idea is to decompose multi-turn attacks into separate phases for planning the attack strategy, priming the conversation context through seemingly benign questions, and delivering the final harmful request. The framework is "plug-and-play," allowing existing attacks like GOAT, Crescendo, and ActorBreaker to be substituted as modules. Evaluations on HarmBench across five models (o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3-70B) show SOTA SRE of 81.4% on o3 (+32.1% over best baseline), 93.1% on o1 (+16.7%), and 67.3% on Claude Opus 4.1 (+40.2% with a Crescendo-based Finisher).

## Strengths

1. **Well-motivated and conceptually novel framework design.** The three-phase decomposition (Planner → Primer → Finisher) is a genuine conceptual advance over treating multi-turn jailbreaking as a monolithic prompt optimization loop. The paper convincingly motivates this design by analyzing specific failure modes of prior work — semantic drift in Crescendo, over-reliance on fixed strategy sets in GOAT. The plug-and-play modularity is a useful engineering contribution that lets future work swap components rather than reimplementing entire attacks.

2. **Disciplined, monotonic ablation study (Table 3).** Adding components one at a time — Backtracking (+4.3% SRE on o3), Reflection (+14.9%), Planner (+1.2%), Memory Retrieval (+4.1%) — produces clear cumulative improvements. This goes beyond what most jailbreaking papers provide and gives strong evidence that each component contributes. The model-specific sensitivity (Reflection helps o3 most, Backtracking helps Claude Opus 4.1 most) is an interesting and well-documented finding.

3. **Genuinely strong results on the hardest models.** The SRE of 81.4% on o3 (vs. 61.6% best baseline, +32.1% relative) and 93.1% on o1 (vs. 79.8%, +16.7% relative) are substantial margins on widely recognized safety-hardened models. The improvement on o3 is large enough that it cannot be explained by noise.

4. **Thorough efficiency analysis (Table 5).** Reporting Target, Evaluator, and Planner call counts separately for every model and every baseline is more detailed than typical and demonstrates the performance gains are not achieved simply by burning more budget.

## Weaknesses

### Major

1. **Abstract substantially overclaims the scope of improvement.** The abstract states PLAGUE achieves "improving attack success rates (ASR) by more than 30% across leading models." Per Table 2 (the main results table using GOAT as Finisher), the SRE improvements over the best baseline per model are: o3 +32.1%, o1 +16.7%, Deepseek-R1 0.0%, Claude Opus 4.1 −3.1%, Llama 3.3-70B +0.8%. Only one model (o3) exceeds 30% in the main results. The 40.2% improvement on Claude Opus 4.1 requires replacing the GOAT Finisher with a Crescendo Finisher (Table 4). The phrase "across leading models" implies broadly consistent improvement that the evidence does not support. The body of the paper (Introduction, Section 5.1) correctly qualifies specific numbers to specific models, but the abstract — the most widely read part — is misleading. This is the paper's most serious flaw and needs correction before publication.

2. **Baseline modifications may disadvantage competitors without sufficient evidence of neutrality.** Three modifications are made without adequate validation:
   - **ActorBreaker**: Limited to K=2 actors per objective (original uses 5). The paper justifies this as "similar to evaluating ASR@K," but independent parallel sampling and sequential budget-constrained attempts are not equivalent. No analysis is provided of how performance changes with K.
   - **GOAT**: Run "without history enabled" and with early stopping. The paper claims the impact is "negligible" based on "extensive ablation" but provides no data to support this.
   - **Crescendo**: "Remove any explicit backtracking counts" without justification.
   
   The paper should report what each baseline achieves in its original configuration alongside the modified version, even if only in a summary table.

### Minor

3. **Fragmented best results across configurations.** No single PLAGUE configuration outperforms all baselines on all models. For most models PLAGUE uses a GOAT Finisher; for Claude Opus 4.1 the best result (0.673 SRE) requires replacing the Finisher with Crescendo — the GOAT-based configuration (0.465 SRE) actually underperforms the Crescendo baseline (0.48 SRE). The paper is transparent about this in-text and with a footnote on Table 2, but the abstract presents the Claude result (67.3%) alongside the o3 result (81.4%) without noting they come from different configurations, creating a misleading impression of monolithic superiority.

4. **"Lesser or comparable query budget" claim imprecise.** Per Table 5, PLAGUE's total LLM calls exceed GOAT's on every model tested (e.g., o3: 6.53 vs 3.08, o1: 5.61 vs 3.00). The claim is accurate vs Crescendo (comparable) and ActorBreaker (lesser), but not vs GOAT. The paper should be precise about which comparison holds.

5. **No statistical variance reported.** Results are averaged over three runs (line 155) but no standard deviations, confidence intervals, or significance tests are provided. For comparisons where margins are small (e.g., Llama 3.3: PLAGUE 0.958 vs GOAT 0.950, a 0.8% difference), the reader cannot assess whether the difference is meaningful.

6. **Evaluator model substitution not validated.** The paper uses Qwen3-235B-A22B-fp8 as the StrongReject Evaluator with a "slightly modified" prompt. The original StrongReject metric (Souly et al., 2024) was validated using GPT-4 as the judge. Using a different judge model means the absolute ASR values are not directly comparable to previously reported numbers. A correlation analysis between the Qwen-based and GPT-4-based StrongReject on a shared set of outputs would strengthen confidence in the reported numbers.

### Trivial

7. Table 2 in the parsed version shows a duplicate ActorBreaker row. Should be corrected.

## Nice-to-Haves

- Include summary statistics for the diversity analysis (Figure 3 is referenced but the data lives in the appendix, which is stripped by the parser).
- Report X-Teaming and FITD results (Table 6, referenced in appendix) with summary in the main text.
- Provide clearer isolation of the lifelong learning component's benefit beyond the two human-crafted initialization strategies — as the paper itself notes about AutoDAN-Turbo, this is a known challenge.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Missing diversity analysis in main text"** — The paper references Figure 3 for diversity analysis. This data may be in the appendix (stripped by the parser). Removed because the parser strips appendices.
- **"Missing X-Teaming/FITD results"** — These are reported in Table 6 (appendix). Removed because the parser strips appendices.
- **"Speculative evaluator overfitting"** — The critic suggested Qwen being used for both the Rubric Scorer and Evaluator "creates a subtle evaluator overfitting concern." This is speculative and unsupported by evidence. Removed.
- **"Missing pseudocode in main text"** — The algorithm is described in sufficient detail in Sections 3.3–3.5. Removed as a presentation nitpick.
- **"Duplicate ActorBreaker row in Table 2 is a typesetting error"** — This is likely a parser artifact in the extracted version, not present in the original submission. Removed as a parser issue.
- **GOAT history modification "extensive ablation" unsubstantiated** — The critic says "no data is shown to support this claim" but acknowledged the data could be in the appendix. The broader concern about baseline modifications is kept in Major; this specific framing is removed.

## Novel Insights

The review surfaces one observation not fully articulated by the paper itself: the model-specific sensitivity of individual PLAGUE components (Backtracking adds +17.4% SRE on Claude Opus 4.1 but only +4.3% on o3, while Reflection adds +14.9% on o3 but only +0.6% on Claude) suggests that different safety alignment strategies create different vulnerability profiles. This asymmetry could motivate a more targeted understanding of model safety — where specific training interventions make models asymmetrically vulnerable to certain attack mechanisms. The PLAGUE framework, precisely because of its modularity, is well-positioned to enable this kind of analysis systematically.

## Suggestions

1. **Rewrite the abstract** to precisely state: "PLAGUE achieves SOTA on several leading models, with particularly large gains on o3 (+32.1%) and, using a Crescendo-based Finisher, on Claude Opus 4.1 (+40.2%). Results are comparable to or better than baselines on other models." This is honest and still impressive.
2. **Run and report baselines in their original configurations** alongside the modified versions, even if only in a summary table or appendix, to demonstrate modifications are neutral.
3. **Report standard deviations** for all main results, particularly where margins between methods are small.
4. **Calibrate the evaluator** — report agreement (e.g., Cohen's κ) between Qwen-based and GPT-4-based StrongReject on a held-out set of jailbreak outputs.
5. **Consolidate results** into one primary table showing each model's best PLAGUE configuration side-by-side with all baselines, with explicit notation of which Finisher module was used.

## Score and Decision

**Round 1 bracket:** 5.5–6.5

**Anchor papers used:**
- `kvvvUPDAPt.md` (ActorAttack, 5.33) — Multi-turn jailbreak; similar topic but weaker evaluation (50 samples, 2 models). PLAGUE is stronger.
- `ov678VcvlO.md` (Jigsaw Puzzles, 4.25) — Simpler multi-turn split approach; missing baselines. PLAGUE is stronger.
- `fFtmpqLFvw.md` (Uncovering Model Vulnerabilities, 5.75) — Human red-teaming on 1 model only. Different approach, comparable quality.
- `H6UMc5VS70.md` (FlipAttack, 5.75) — Single-turn attack with evaluation concerns (system prompt inflation). PLAGUE's framework contribution is stronger.
- `e9yfCY7Q3U.md` (Improved GCG, 6.25, Accept) — Optimization-based improvements with strong results. Different approach; both are solid contributions at similar quality levels.
- `KyKTjRtyNG.md` (MRCJ, 3.00) — Multi-turn jailbreak with limited novelty. PLAGUE is substantially stronger.

The PLAGUE paper makes a genuine and novel framework contribution, with strong evaluation and a clean ablation study. Its main weaknesses are presentational (abstract overclaiming) and methodological (baseline modification justification). These are addressable without changing the core method. The paper is comparable to accepted work in the 6.0–6.25 range and stronger than rejected work in the 4.25–5.75 range. Score 6.0 reflects a solid contribution held back by presentation and justification issues that should be corrected through revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>