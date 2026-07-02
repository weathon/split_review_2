Now I'll produce the final consolidated review.

## Summary

This paper proposes PLAGUE, a plug-and-play framework for generating multi-turn jailbreak attacks against LLMs. The framework decomposes attack generation into three modular phases (Planner, Primer, Finisher) with a lifelong learning component that retrieves successful strategies from memory. Evaluated on HarmBench across five frontier models (o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3-70B), PLAGUE achieves strong headline results including 81.4% SRE on o3 and 67.3% on Claude Opus 4.1 with its best configuration.

## Strengths

1. **Well-motivated and timely problem.** Multi-turn jailbreaking is genuinely under-explored relative to single-turn attacks. The paper correctly identifies that real-world LLM interaction is increasingly multi-turn and agentic, making this a relevant contribution to red-teaming methodology.

2. **Clean architectural decomposition.** The three-phase design (Planner → Primer → Finisher) with a separate lifelong learning mechanism is conceptually clear. The plug-and-play framing—where existing attacks (GOAT, Crescendo, ActorBreaker) can serve as Planner or Finisher modules—is a genuine organizational contribution that allows component-level ablation.

3. **Strong headline results.** The reported 81.4% SRE on o3 and 67.3% on Claude Opus 4.1 (best configuration) are impressive against models considered highly resistant. The 97.8% on Deepseek-R1 is notable. Results span five frontier models, which is among the most comprehensive evaluations in the multi-turn jailbreak literature.

4. **Budget-aware evaluation.** Tracking Target, Evaluator, and Planner LLM calls separately (Table 5) is a legitimate methodological improvement over prior work that often ignores computational costs. The analysis shows PLAGUE achieves its gains with comparable or lower query budgets.

## Weaknesses

### Major

1. **Baseline modifications undermine comparison fairness.** The paper documents modifications to all three multi-turn baselines (GOAT without attack history and with early stopping; ActorBreaker capped at K=2; Crescendo with backtracking removed) but provides no validation that these modifications do not significantly degrade performance (lines 157–161). The paper claims "Through extensive ablation, we also observe that the impact on GOAT's performance with and without an attack history is negligible" but does not present this ablation. Without such evidence, the reader cannot distinguish whether PLAGUE's reported improvements reflect genuine superiority or asymmetrically constrained competitors. This is the most serious concern and cuts across all headline comparison claims.

2. **Factual error in headline numerical claim.** The paper states: "With OpenAI's o3 model, we outperform the previous best - GOAT by a factor of 32.14%" (line 200). However, Table 2 shows that on the SRE metric (which the paper uses interchangeably with ASR, line 155), **ActorBreaker achieves 0.616 SRE while GOAT achieves 0.587**. ActorBreaker is the stronger baseline on SRE. The 32.14% figure itself (0.814 vs 0.616 ≈ +32.14%) uses ActorBreaker's SRE as the denominator, not GOAT's. Either way—whether the text misidentifies the comparator or the calculation uses the wrong baseline—this is a factual error in a headline result that erodes confidence in the paper's quantitative handling.

### Minor

3. **No variance reporting despite acknowledged stochasticity.** The paper states results are "averaged over three runs for robustness" and acknowledges "increased variance observed due to a multitude of possible paths in multi-turn conversations" (line 155). Yet no table or figure reports error bars, standard deviations, confidence intervals, or per-run results. With only three runs and the acknowledged high variance, the reader cannot assess whether reported improvements are statistically meaningful.

4. **Diversity claims are unsubstantiated.** The paper claims "PLAGUE's planning module largely drives improvements in diversity" and "diversity improves by 15% (Figure 3)" (line 40), but no diversity metric is defined or quantified anywhere in the paper. Figure 3 is referenced but its content is not visible in the parsed output. These claims are central to the lifelong learning framing but rest on an undefined evaluation criterion.

5. **Imprecise and potentially misleading presentation of Claude Opus 4.1 results.** Table 2 shows PLAGUE achieves 0.465 SRE on Claude Opus 4.1, which is *lower* than Crescendo's 0.480. The asterisk points to Table 4, where a different configuration (Crescendo Finisher + PLAGUE components) achieves 0.673. The paper is transparent about this (lines 43–44, 230), but presenting a 40.2% improvement in the abstract and introduction while the main comparison table shows underperformance is structurally misleading. Additionally, the abstract bundles GPT-4o with Deepseek-R1's 97.8% result ("up to 97.8% on state-of-the-art models such as Deepseek-R1, GPT-4o and Meta's Llama 3.3-70B"), but GPT-4o does not appear in any evaluation table.

6. **Ablation pattern contradicts "gradual improvements" narrative.** The paper describes "noticeable, gradual improvements in ASR as we add components one at a time" (lines 202–203). However, Table 3 shows that adding the Planner component to GOAT+BT+R *decreases* Bin-ASR on o3 from 0.59 to 0.582. The improvement only materializes with RSS (retrieval). This non-monotonic pattern is not discussed.

### Trivial

None.

## Nice-to-Haves

- Validate that baseline modifications (removing GOAT history, capping ActorBreaker at K=2, removing Crescendo backtracking) do not significantly degrade performance on the same evaluation setup.
- Report per-run results, ranges, or standard deviations to support the three-run averaging.
- Define and quantify the diversity metric used for the lifelong learning diversity claims.
- Correct the o3 baseline identification (ActorBreaker, not GOAT, is the previous best on SRE).
- Add a limitations section discussing failure cases and scenarios where PLAGUE might underperform.
- Include GPT-4o results in evaluation tables if it is named in the abstract's headline results.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Rubric Scorer feedback loop concern** (harsh critic #4 in section-by-section): The critic argues that using the Rubric Scorer for both internal feedback and final evaluation creates a problematic feedback loop. However, the paper explicitly states (line 98) that the Rubric Scorer and final Evaluator prompts differ and use "varied sampling parameters." This concern is speculative and not verified as a concrete flaw.
- **Missing GPT-4o results** (harsh critic section-by-section): The critic flags that GPT-4o is named in the introduction but absent from evaluation tables. This is imprecise language in the abstract rather than a core experimental gap, and the paper does not claim specific results for GPT-4o.
- **Reproducibility concerns about prompts in appendix**: These are parser-removed sections that exist in the original submission. Not a valid criticism of the paper.
- **Missing related works**: Cannot be verified without external sources; the paper's related work section (lines 46–76) is actually well-organized and cites the relevant baselines.
- **Formatting/style nitpicks**: Parser artifacts, not author errors.
- **Criticism about "no discussion of limitations"**: While the paper's conclusion is brief, this is a minor presentation issue rather than a substantive weakness. The paper does acknowledge specific limitations in context (e.g., the Claude Opus 4.1 underperformance with GOAT Finisher).

## Novel Insights

The reviews surface one genuinely novel observation beyond the paper's own contributions: the non-monotonic ablation pattern (Planner addition slightly decreasing ASR before RSS recovers it) is a subtle but interesting finding that the paper itself under-discusses. This suggests that planning without retrieval can actually be harmful, which has implications for how modular attack frameworks should be assembled. The paper would benefit from explicitly addressing this pattern rather than glossing over it with a "gradual improvements" framing.

## Suggestions

1. **Run baselines in their original configurations.** For a subset of goals, compare each modified baseline against its original implementation and report whether modifications significantly change ASR. If they do not, include the results in an appendix. If they do, report both modified and unmodified numbers.

2. **Correct the factual error about the o3 baseline.** Acknowledge that ActorBreaker achieves the highest SRE (0.616) on o3 among baselines, and report improvements relative to both GOAT and ActorBreaker transparently.

3. **Add variance information.** Report standard deviations or per-run results for the three runs, or at minimum acknowledge the limitation and interpret results in light of observed variance.

4. **Define the diversity metric.** If diversity is measured (as Figure 3 suggests), describe the methodology. If it is not measured, remove or downgrade the diversity claims.

5. **Restructure Claude Opus 4.1 presentation.** Either move the best configuration to the main table or add an explicit callout in the main comparison explaining the configuration difference, rather than burying it behind an asterisk.

## Score and Decision

**Bracket determination (Round 1):** Initial bracketing placed this paper in the 5.0–6.5 range. Strong reject anchors (scores 1.0–1.4) are papers with fundamental errors or no meaningful contribution—PLAGUE does not belong in that band. Lower-band papers (3.0–3.67, e.g., "Incremental Exploits" at 3.00, "Quack" at 3.67) either have minimal evaluation, outdated models, or trivial methodology; PLAGUE's comprehensive evaluation and well-structured framework are clearly stronger. Mid-band papers (5.33–5.75, e.g., "Derail Yourself" at 5.33, "DAG-Jailbreak" at 5.50, "Uncovering Model Vulnerabilities" at 5.75) share similar scope but vary in execution quality. The upper anchor "I-GCG" (6.25, Accept) is a cleaner, more methodologically sound paper but makes a narrower contribution.

**Narrowing (Round 2):** Reading "Derail Yourself" (5.33, Reject) in full: it evaluates on only 2 models and 50 samples, lacks multi-turn baselines, and has limited novelty. PLAGUE is strictly stronger in evaluation breadth, methodological clarity, and baseline coverage. Reading "DAG-Jailbreak" (5.50, Reject): it has reproducibility gaps similar in severity to PLAGUE's baseline validation gap. PLAGUE's fact-checkable error in a headline claim is more concrete than DAG-Jailbreak's methodological opaqueness, but PLAGUE also has clearer strengths.

**Final calibration:** PLAGUE's genuine contributions (architectural decomposition, budget-aware evaluation, strong results, comprehensive model coverage) are offset by (a) unvalidated baseline modifications that threaten the core comparison claims, (b) a factual error in a headline result, (c) absent variance reporting, and (d) unsubstantiated diversity claims. These issues are fixable but, in the current form, prevent full confidence in the empirical claims. The paper is stronger than "Derail Yourself" (5.33) and comparable to "DAG-Jailbreak" (5.50), with more concrete weaknesses but also more concrete strengths. It falls short of "I-GCG" (6.25) where the methodology is cleaner and the claims are reliable as stated.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>