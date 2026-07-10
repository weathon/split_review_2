## Summary

This paper introduces CALM, a framework that combines prompt evolution with on-the-fly RL fine-tuning of an LLM (via GRPO) for automatic heuristic design (AHD). The key insight is that the evolutionary loop naturally produces prompt-response-performance triplets that can serve as training data for RL, allowing the LLM to co-evolve with the search process — a genuine departure from prior frozen-LLM approaches. Experiments on OBP, TSP, CVRP, and OP show strong results, with the quantized 7B model running on a single 24GB GPU outperforming API-based methods from larger models.

## Strengths

- **Genuinely novel core idea.** The central insight — treating the evolutionary loop as a source of RL training data to adapt the LLM itself — is clearly articulated (Section 4, Section 1) and represents a clear departure from prior frozen-LLM approaches that only use prompt engineering ("verbal gradients"). This is not an incremental improvement.

- **API-based ablation cleanly isolates the verbal guidance contribution.** Section 5.2 shows that with G=1, GPT-4o-mini backend, and matched query budgets, CALM matches or exceeds MCTS-AHD on CVRP, OP, and OBP. This separates the prompt-engineering innovations (fine-granularity operators, collapse mechanism, diversity-aware crossover) from the RL component and demonstrates that the verbal guidance alone is already at the frontier.

- **Thorough and informative ablation study (Table 4).** Each component is systematically ablated. The finding that GRPO contributes the largest single performance gain, and that the simplification operator is surprisingly critical, provides useful scientific insight into what drives performance.

- **Practical engineering achievement.** Running a competitive AHD system on a single 24GB GPU with an INT4-quantized 7B model and outperforming API-based methods from larger models (GPT-4o-mini) is a nontrivial contribution (Section 5).

## Weaknesses

### Fatal
None.

### Major
- **The value of G (number of GRPO responses per prompt) is not reported for the main local experiments with GRPO.** The paper states "comparable evaluation budgets—specifically, 1,000 heuristic evaluations for baselines and a fixed budget of 2,000 LLM queries for CALM" (Section 5), but these are measured in different units. If G > 1 (as is typical for GRPO's group normalization), CALM evaluates 2,000 × G heuristics vs. the baselines' 1,000 — a potentially large discrepancy. The API-based ablation (G=1, matched budgets) partially addresses this for the verbal guidance component, but the main CALM (w/ GRPO) vs. baseline comparison is hard to evaluate fairly without G disclosed. The "local, w/o GRPO" baseline in Table 4 helps only if G is held constant between the two conditions, which is also unreported.

### Minor
- **Mixed results on TSP.** On the in-domain set (N=50), CALM (local) achieves 10.04% gap, which is *worse* than MCTS-AHD (GPT-4o-mini) at 9.69%. On out-of-domain sets, margins are thin (N=100: 11.58% vs 11.79%; N=200: 13.41% vs 13.71%) — sub-1 percentage point differences. The paper's broad "outperforms SOTA" framing is better supported on CVRP, OBP, and OP than on TSP, where the result is better described as competitive.

- **No confidence intervals or variance estimates in the main results tables (Tables 1-3).** With only three runs reported and margins below 1pp on TSP, readers cannot assess whether these differences are meaningful. Statistical significance tests are relegated to the appendix.

- **A subtle edge case in the reward function (Equation 4).** The condition checks performance ties with ANY base heuristic in H (∃h∈H s.t. g(h)=g(h_new)). A genuinely novel heuristic that happens to match the performance of an existing base heuristic would receive a negative reward (α₁·r_invalid). This is a minor issue — the paper's design intention is to discourage trivial reproduction — but it could penalize legitimate novel heuristics.

### Trivial
None.

## Nice-to-Haves
- State G explicitly for all experimental conditions and report the total number of heuristic evaluations performed by CALM alongside LLM query counts.
- Add confidence intervals or error bars to the main results tables.
- Include wall-clock time and GPU-hour costs in the main text (currently only in the appendix).

## Removed Points

These points are flagged to be removed; treat them with caution:
- **"Evaluation budget comparison is misleading"** (original Critical Issue 1): The core concern about G unreported is kept in Major Weaknesses above. The framing as a "structural/fatal" issue is removed because the API-based ablation (G=1, matched budgets) and the local w/o GRPO baseline (Table 4) provide sufficient controls to evaluate the GRPO contribution independently.
- **"G not reported undermines reproducibility"** (original Critical Issue 3): Merged into the Major Weakness above.
- Missing hyperparameter values (α₁, α₂, r_invalid) and computational cost details: Removed per the rule that these likely exist in Appendix I (stripped by parser); cannot penalize for appendix content.
- **"Improvement margins thin/negative on TSP inconsistent with paper's framing"**: Weakened from the critic's framing as a core issue to Minor. The paper's claim about out-of-domain performance is technically correct and the mixed results are partially acknowledged in the text.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Report G explicitly for all experimental conditions (both with and without GRPO) and reframe the budget comparison. Clarify the total number of heuristic evaluations performed by CALM relative to baselines.
2. Add confidence intervals or error bars to the main results tables, especially for TSP where margins are thin.
3. Qualify the TSP results more precisely in the main text: CALM is competitive with SOTA on TSP (with a negative result on the in-domain set) and clearly superior on CVRP, OBP, and OP.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `/home/.../8QTpYC4smR.md` | 1.00 | 1 | No | Tangentially related LLM survey; strong reject |
| `/home/.../5kMwiMnUip.md` | 1.40 | 1 | No | LLM jailbreak paper; not comparable |
| `/home/.../XTxdDEFR6D.md` | 3.40 | 1 | No | LLM4Solver: LLM for CO solver design; lower novelty |
| `/home/.../sUywd7UhFT.md` | 2.50 | 1 | No | LLM hyper-heuristics for multi-objective optimization |
| `/home/.../iTrd5xyHLP.md` | 3.40 | 1 | No | LLMatic: NAS via LLMs + QD; related approach |
| `/home/.../0fwJMANq9P.md` | 5.25 | 1,2 | Yes | Hercules: LLM-based heuristic generation; closest direct competitor. CALM has higher strength favorability (15.52 vs 11.94) and milder weaknesses (2.13+ vs -1.88). **CALM clearly stronger.** |
| `/home/.../Usk4KzBxLW.md` | 5.25 | 1 | No | LLM-LNS: LLM-driven large neighborhood search |
| `/home/.../xxSK3ZNAhh.md` | 3.80 | 1,2 | Yes | HeurAgenix: multi-agent LLM heuristic framework. CALM's ablations are much more thorough and the core idea is more novel. |
| `/home/.../rh54qNvxKO.md` | 4.17 | 1 | No | LLM+EA for critical node identification |
| `/home/.../cJPUpL8mOw.md` | 6.00 | 1,2 | Yes | REvolve: LLM-based reward evolution with human feedback. Lower strength favorability (max 11.32 vs CALM's 15.52) and more severe weaknesses (-2.27). |
| `/home/.../ZG3RaNIsO8.md` | 6.50 | 1,2 | Yes | EvoPrompt: LLMs + EAs for prompt optimization. CALM's strengths are higher (12.97-15.52 vs 7.54-12.63) and weaknesses milder (2.13-4.45 vs -5.12). |
| `/home/.../kWtP5ZOErR.md` | 6.25 | 1 | No | EvoPress: evolutionary model compression |
| `/home/.../LCrm1FSl26.md` | 5.60 | 1 | No | Evolutionary LLM pruning |
| `/home/.../awWiNvQwf3.md` | 7.00 | 2 | Yes | MOLLEO: LLMs + EAs for molecular discovery. Strength favorability max 11.33 (vs CALM's 15.52); worst weakness -4.07 (vs CALM's 2.13). |
| `/home/.../aVfDrl7xDV.md` | 6.25 | 2 | Yes | BOPRO: Bayesian optimization with LLMs. Lower strengths, more severe weaknesses (down to -4.44). |
| `/home/.../m2nmp8P5in.md` | 8.00 | 2 | Yes | LLM-SR: LLM-based symbolic regression. Peak strength 14.67 (slightly below CALM's 15.52); has a -1.26 weakness about overclaiming. CALM's profile is comparable but the unresolved G-value gap prevents reaching this tier. |
| `/home/.../UyhRtB4hjN.md` | 6.25 | 2 | No | LLEGO: LLM-enhanced decision tree evolution |

**Bracket (Round 1):** [6.0, 8.0] — clearly above the ~5.0-5.5 papers (Hercules, HeurAgenix) and below the 8.0 level (LLM-SR).

**Narrowing (Round 2):** CALM's itemized favorability profile dominates every anchor in the 6.0-7.0 range. Its worst weakness (favorability 2.13, missing confidence intervals) is less damaging than the worst weaknesses of MOLLEO (-4.07, limited novelty), EvoPrompt (-5.12, lack of novelty), or BOPRO (-4.44, insufficient innovation). Its strengths (12.97-15.52) exceed the best strengths of all these anchors. Compared to LLM-SR (8.00), CALM's strength profile is comparable or slightly higher, but the unresolved G-value issue (favorability 3.90) prevents reaching the 8.00 level where papers have near-flawless reviews. Final score: **7.5**.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>