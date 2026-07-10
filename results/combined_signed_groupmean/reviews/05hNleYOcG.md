Now I'll produce the final review.

---

## Summary

This paper proposes PLAGUE, a modular three-phase framework (Planner → Primer → Finisher) for generating multi-turn jailbreak attacks against LLMs. The framework disentangles planning, adversarial context-building, and iterative refinement into plug-and-play components, and incorporates a strategy retrieval memory. Evaluated across five leading models (o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3 70B) under a strict six-turn budget, PLAGUE achieves strong Attack Success Rates including 81.4% on o3 and 67.3% on Claude Opus 4.1.

## Strengths

- **The three-phase design is a thoughtful synthesis of prior work.** The paper correctly identifies that ActorBreaker excels at planning while GOAT and Crescendo excel at iterative query optimization, and constructs a framework that combines both. The Primer phase — building adversarial context gradually from plan steps before the final attack — is the most novel component and is clearly motivated (Sections 3.3–3.5). [impact=+9.99]

- **Plug-and-play modularity is a genuine practical contribution.** Ablations in Tables 3 and 4 demonstrate that different victim models benefit from different component configurations (e.g., Crescendo Finisher outperforms GOAT Finisher on Claude Opus 4.1). This enables model-specific customization for real red-teaming. [impact=+9.98]

- **Budget-controlled evaluation is a strength.** Capping all methods at six target-LLM calls and explicitly reporting the call breakdown (Table 5) avoids the common pitfall of letting one method use arbitrarily many calls while comparing to budget-limited baselines. [impact=+8.09]

- **Strong across-model results with concrete numbers:** 81.4% SRE on o3 and 67.3% on Claude Opus 4.1 — two models widely regarded as having the strongest safety alignment (Table 2). [impact=+9.97]

## Weaknesses

### Fatal
None.

### Major

- **The lifelong learning claim is not validated by any experiment that isolates its effect.** The title, abstract, and Table 1 all highlight lifelong learning as a key contribution, yet the only relevant evidence is the RSS (Retrieving Successful Strategy) ablation in Table 3, which shows ASR improving from 0.773 to 0.814 on o3. However, the strategy library is initialized with two human-written seed strategies (Section 3.3: "We initialize the strategy library with two strategies adapted from examples in Crescendo"), and the ablation does not distinguish between (a) the benefit of having those seed strategies plus a retrieval mechanism and (b) the benefit of actually accumulating new strategies across goals during evaluation. The paper provides no experiment comparing an empty vs. populated memory bank, no measurement of whether ASR improves as the library grows across a sequence of goals, and no evidence that strategies discovered during evaluation are productively retrieved. Without such evidence, the "lifelong learning" framing is unsupported — what is demonstrated is a static retrieval mechanism, not a system that learns from experience. [impact=-10.00]

### Minor

- **The headline "32.14% improvement on o3" is inconsistent with Table 2.** The paper (Section 5.1, line 200) states the baseline is GOAT (SRE 0.587), but 32.14% matches the improvement over ActorBreaker (SRE 0.616): (0.814−0.616)/0.616 = 32.1%. Over GOAT, the actual improvements are (0.814−0.587)/0.587 = 38.7% for SRE and 48.8% for Bin-ASR. The text claims one baseline while the arithmetic fits another. This numerical inconsistency in a headline figure erodes confidence in quantitative precision. [impact=-3.77]

- **Baseline modifications are acknowledged but their impact on comparability is unanalyzed.** GOAT is modified to receive per-round rubric feedback (Section 4, line 157), Crescendo has backtracking removed (line 160), and ActorBreaker is capped at K=2 actors (line 159). The paper provides no sensitivity analysis comparing modified vs. original implementations for at least one model, so the reader cannot assess whether PLAGUE's advantages are architectural or driven by evaluation changes. [impact=-0.81]

- **The paper claims diversity improves by 15%** (Section 1, line 40, referencing Figure 3) and that ActorBreaker has "higher overall diversity," but no diversity metric is ever defined. Without a definition, these quantitative claims are unverifiable. [impact=-10.00]

- **All attacks use Deepseek-R1 as the fixed attacker LLM** (Section 4). Results may not generalize to other attacker models — a limitation the paper does not discuss. [impact=-0.02]

- **No sensitivity analysis is provided for key parameters:** the cosine similarity threshold of 0.6 (Section 3.3.1) and the Rubric Scorer's scoring thresholds of 7/10 (Primer) and 3/10, 8/10 (Finisher) in Sections 3.4–3.5. These thresholds directly control attack behavior and the definition of success. [impact=-0.01]

### Trivial
None.

## Nice-to-Haves
- Report error bars or confidence intervals for the three-run averages, given the paper itself acknowledges "increased variance" in multi-turn settings.
- Include a failure-mode analysis by harm category to understand what kinds of goals PLAGUE struggles with.
- Run a human evaluation or agreement study to verify that the automated Evaluator (Qwen3-235B) correlates with human judgment for multi-turn scenarios.

## Removed Points
- "Timely and well-motivated problem" — removed as generic praise lacking specific anchoring to this paper's content.
- "Multi-turn jailbreaks lack formal investigation" slight overstatement — removed as subjective opinion, not a substantive weakness.
- "No clear winning attack within a fixed budget, excluding ours" overstated — the critic misreads this sentence; it refers to baselines having no clear winner among themselves.
- "On Deepseek-R1, GOAT ties PLAGUE" — factual but does not contradict the paper's overall claims; GOAT is competitive on one model but PLAGUE dominates across others.
- "SRE and ASR used interchangeably is confusing" — the paper explicitly states this convention on line 155; it is not an error.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Validate the lifelong learning claim directly:** Run PLAGUE on a sequence of HarmBench goals and measure whether ASR improves as the strategy library grows, or compare a version with only the two seed strategies against the version that accumulates strategies. If the improvement is negligible, drop the "lifelong" framing.
2. **Correct the 32.14% figure:** Either change it to reflect the actual GOAT comparison (~38.7% for SRE) or clarify which baseline is being used.
3. **Show unmodified-baseline results:** For at least one model, run unmodified GOAT, Crescendo, and ActorBreaker alongside the modified versions to quantify how evaluation changes affect relative performance.
4. **Define the diversity metric** used to support the 15% improvement claim.
5. **Report error bars** for the three-run averages.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `kvvvUPDAPt.md` ("Derail Yourself") | 5.33 | R1 | Yes | Weaker evaluation, missing baselines, similar scope — PLAGUE is stronger |
| `KyKTjRtyNG.md` ("Incremental Exploits") | 3.00 | R1 | Yes | Much weaker: limited novelty, weak models tested |
| `fFtmpqLFvw.md` ("Uncovering Model Vulnerabilities") | 5.75 | R1 | Yes | Single-model human study — PLAGUE is more comprehensive |
| `4KqkizXgXU.md` ("Curiosity-driven Red-teaming") | 8.00 | R1 | Yes | Exceptionally clean execution — PLAGUE has unvalidated claims that prevent reaching this level |
| `e9yfCY7Q3U.md` ("Improved Techniques") | 6.25 | R2 | Yes | Comparable profile: incremental method but clean execution; PLAGUE has more novel framework but unsupported central claim |
| `hXA8wqRdyV.md` ("Jailbreaking Leading Safety-Aligned LLMs") | 6.14 | R2 | Yes | Engineering-heavy approach — PLAGUE's framework is more novel but has similar weakness severity |
| `vESNKdEMGp.md` ("Multilingual Jailbreak Challenges") | 6.40 | R2 | No | Different focus (multilingual) |
| `sULAwlAWc1.md` ("One Model Transfer to All") | 7.00 | R2 | No | Cleaner method — PLAGUE is weaker |

**Round 1 bracket**: 5.5–7.5.

**Narrowing**: PLAGUE sits above the 5.33–5.75 papers (stronger evaluation, more novel framework) and roughly on par with the 6.14–6.25 papers (comparable contribution-to-weakness ratio). The lifelong learning gap (impact −10.00) and undefined diversity metric (impact −10.00) are the decisive factors keeping it from 7+, while the strong contributions (three-phase framework impact +9.99, modularity +9.98, results +9.97) place it clearly above 5.5.

**Final placement**: PLAGUE has real contributions — the three-phase architecture, the modularity demonstration, and the budget-controlled strong results on frontier models. However, the unsupported lifelong learning claim (in the title) is a significant gap that prevents a higher score. The paper is comparable to the ~6.1–6.25 accepted papers in this area.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>