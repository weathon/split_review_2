Now I have all the information I need. Let me compile the final review.

## Summary

This paper proposes CALM, a framework for automatic heuristic design (AHD) that simultaneously evolves prompts (verbal guidance) and fine-tunes the underlying LLM via GRPO (numerical guidance). CALM integrates fine-granularity mutation operators (injection, replacement), a diversity-aware crossover, a collapse mechanism for escaping local optima, and a reward function that credits heuristic improvements over base heuristics. Experiments on OBP, TSP, CVRP, and OP show that CALM using a 7B INT4-quantized model on a single 24GB GPU matches or exceeds SOTA API-based methods, with the RL component providing the largest single contribution per ablation analysis.

## Strengths

- **Genuinely novel combination in the AHD literature.** CALM is the first framework to jointly optimize prompt evolution (verbal guidance) and the LLM itself via RL fine-tuning (numerical guidance), directly addressing the limitation of frozen-LLM approaches. The paper honestly acknowledges concurrent but methodologically distinct work (Surina et al., 2025; Liu et al., 2025), placing the contribution as genuinely novel among published work.

- **The verbal-only (API, w/o GRPO) variant establishes a strong baseline within the paper's own design.** This variant matches or exceeds prior SOTA methods using GPT-4o-mini across Tables 1–3 at matched budgets. This separates the prompt-engineering gains from the RL gains, demonstrating that the operator design (injection, replacement, diversity-aware crossover, collapse) is independently competitive even without fine-tuning.

- **Resource efficiency is demonstrated concretely.** A 7B INT4-quantized model on a single 24GB GPU outperforms methods relying on GPT-4o-mini API calls, with the paper honestly acknowledging GPT-4o-mini's accuracy advantage. This is a practically significant result.

- **Thorough ablation study (Table 4).** The paper systematically ablates the RL component, the collapse mechanism (4 hyperparameter configurations), and each operator individually. The finding that removing GRPO causes the largest performance drop supports the paper's central claim, and the operator-level ablations are informative — especially the result that removing simplification causes the largest performance drop among operators.

- **Evaluation spans four diverse optimization tasks** (OBP, TSP, CVRP, OP) with both in-domain and out-of-domain test sets, following established protocols from prior work. This breadth strengthens the evidence for the method's generality.

## Weaknesses

### Fatal
None.

### Major

- **Budget asymmetry on non-OBP tasks weakens the "outperforms SOTA" claim for the local GRPO variant.** The paper states (line 140): "1,000 heuristic evaluations for baselines and a fixed budget of 2,000 LLM queries for CALM across all tasks except OBP." Each query produces one heuristic, so CALM evaluates 2,000 heuristics while baselines evaluate only 1,000 on TSP, CVRP, and OP — a 2× budget advantage. On OBP, where budgets are matched (2,000 evaluations each), CALM's improvement over MCTS-AHD is 0.71% vs 0.89% — real but modest. Several non-OBP margins are small (e.g., TSP N=100: 11.58% vs MCTS-AHD's 11.79% = 0.21pp; OP N=50: 24.22% vs HSEvo's 23.98%). The paper does not run CALM at matched budgets on non-OBP tasks or demonstrate that performance saturates well before the budget is exhausted. **However, this does not invalidate the core contribution** because: (a) the verbal-only API variant matches/exceeds SOTA at matched budgets, separating operator gains from RL gains; (b) the ablation study (Table 4) shows removing GRPO causes the largest performance drop; and (c) training curves (Figure 2) show CALM's advantage persists over the full training trajectory.

### Minor

- **Value of G for the main GRPO variant is not reported in the main text.** G=1 is stated only for the API variant (line 221). For the primary local GRPO variant, G is never given. This parameter determines the number of responses per prompt, affecting both the number of evolutionary rounds within the 2,000-query budget and the quality of GRPO's group-mean baseline. Without it, the reader cannot fully assess search dynamics or the claimed memory savings. (It may be in the stripped appendix, but it should appear in the main text.)

- **Statistical significance / error bars are absent from the main tables for several close comparisons.** On TSP N=50 (Table 2), CALM (local) at 10.04% gap is *worse* than MCTS-AHD (GPT-4o-mini) at 9.69%. On TSP N=100, 11.58% vs 11.79% is a 0.21pp difference from 3 runs. On OP N=50 (Table 3), CALM at 24.22% is comparable to HSEvo at 23.98%. The paper mentions p-values are in Appendix I, but without error bars or confidence intervals visible in the main paper, the reader cannot assess whether these small differences reflect genuine improvements or run-to-run variance.

- **The most controlled comparison (CALM vs EvoTune) is under-analyzed.** EvoTune uses the same base model (Qwen2.5-7B-Instruct-INT4 with GRPO), and CALM clearly outperforms it. This is the strongest evidence for CALM's operator and reward design, yet the paper does not discuss *why* — whether the advantage comes from the reward formulation, the fine-granularity operators, the diversity-aware crossover, or a combination. The ablation data provides clues but is not connected explicitly to this comparison.

- **The reward function's denominator in Equation (3) can be zero.** The term `min(|g(h_new)|, |g(h_t_base)|)` in the denominator is zero if either heuristic achieves zero cost (perfect solutions), making the reward undefined. The paper does not discuss this edge case or how it is handled.

- **Ambiguity in the injection operator's "component" definition.** The injection operator (Section 4.1) requires the LLM to introduce "components distinct from those previously saved," but the paper does not define what constitutes a "component" or how the LLM is prevented from repackaging identical ideas under different names — a known failure mode of LLM-based novelty filtering.

- **The "original seed algorithm" retained during collapse (line 100) is not clearly specified** as human-designed or LLM-generated. Since the seed heuristics are "directly adopted from Zheng et al. (2025)" (line 140), if this is a known hand-crafted heuristic (e.g., Best-Fit for OBP), the collapse mechanism periodically injects human expert knowledge, giving CALM an advantage over methods that do not do this. This should be clarified.

### Trivial
None.

## Nice-to-Haves

- Run CALM at matched heuristic evaluation budgets (1,000 evaluations on non-OBP tasks) to isolate the benefit of RL fine-tuning from the benefit of additional search.
- Add a brief analysis of why CALM outperforms EvoTune (the most controlled comparison), connecting the ablation data to this comparison.
- Clarify the edge-case handling for Equation (3) when `min(|g(h_new)|, |g(h_t_base)|)` = 0.
- Clarify what constitutes a "component" in the injection operator and how novelty is enforced.
- Clarify whether the "original seed algorithm" in the collapse mechanism is a human-designed heuristic or an LLM-generated one.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **GRPO preliminaries are too verbose (from Section-by-Section notes)** — This is a stylistic preference, not a substantive weakness. The GRPO exposition provides necessary context.
2. **Collapse mechanism is "standard" / "not novel"** — The paper presents this as "simple yet effective" and does not claim it as a major novelty. The overall contribution is the framework, not this individual component.
3. **Pure formatting/style nitpicks** — These are parser artifacts, not author errors.
4. **Missing related work** — Cannot be verified; all cited works are assumed to exist per guidelines.
5. **Reproducibility concerns about missing appendix content** — Appendix content is stripped by the parser, not omitted by authors.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis confirms the paper's framing: the key insight is that RL fine-tuning of the LLM within an evolutionary AHD loop provides gains beyond what prompt engineering alone can achieve, and the ablation study cleanly validates this. No reviewer surfaced an insight that contradicts or substantially reframes this.

## Suggestions

1. **Address the budget asymmetry directly**: Run CALM at 1,000 queries (matching baseline heuristic evaluations) on non-OBP tasks, or show that performance saturates before 2,000 queries. Report the results — even if they degrade — to honestly bound the contribution.
2. **Report G and the resulting number of evolutionary rounds** for the GRPO variant in the main text.
3. **Add error bars or confidence intervals** to the main tables, especially for TSP and OP where margins are small.
4. **Add a brief discussion** connecting the ablation results to the CALM-vs-EvoTune comparison.

## Score and Decision

### Calibration

**All anchors retrieved:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `5kMwiMnUip.md` (jailbreaking LLMs) | 1.40 | R1 | No | Unrelated topic, far lower quality |
| `8QTpYC4smR.md` (systematic review) | 1.00 | R1 | No | Unrelated, not a research paper |
| `Uj0h13lVrR.md` (GFlowNets) | 1.00 | R1 | No | Unrelated topic |
| `gwZ90hFSL2.md` (robots/Chinese NLP) | 1.00 | R1 | No | Unrelated topic |
| `ZK1NnjpjEs.md` (LLM NLU via RL) | 3.00 | R1 | No | Different focus (NLU, not AHD) |
| `z4Ho599uOL.md` (JSSP dataset) | 3.00 | R1 | No | Dataset paper, different methodology |
| `XTxdDEFR6D.md` (LLM4Solver) | 3.40 | R1 | Yes | LLM for algorithm design but limited novelty vs prior work; CALM has stronger originality |
| `aYYZBPoSHb.md` (Multi-objective alignment) | 3.40 | R1 | No | Different focus (alignment, not AHD) |
| `0fwJMANq9P.md` (Hercules) | 5.25 | R1 | Yes | Most related AHD paper; fatal weaknesses (incremental over Ye et al. 2024, missing baselines) not present in CALM |
| `Usk4KzBxLW.md` (LLM-driven LNS) | 5.25 | R1 | No | Different method (LNS, not heuristic generation) |
| `xxSK3ZNAhh.md` (HeurAgenix) | 3.80 | R1 | Yes | Multi-agent AHD but insufficient detail/reproducibility; CALM's ablations and clarity are much stronger |
| `rh54qNvxKO.md` (critical nodes) | 4.17 | R1 | No | Different problem domain |
| `EKCubxFdOs.md` (LLaMoCo) | 5.75 | R1 | No | Instruction tuning for optimization, not online RL fine-tuning |
| `aVfDrl7xDV.md` (BOPRO) | 6.25 | R1 | Yes | LLM+BO for search; negative results on key tasks, limited evaluation; CALM has stronger empirical results |
| `OSmjkkF6Uy.md` (FunBO) | 5.80 | R1 | No | Focused on acquisition functions for BO |
| `UyhRtB4hjN.md` (LLEGO) | 6.25 | R1 | Yes | LLM+EA for decision trees; accepted — CALM has similarly strong experiments but broader scope |
| `mMPMHWOdOy.md` (WizardMath) | 8.00 | R1 | No | Math reasoning, different domain |
| `JDud6zbpFv.md` (CCQD) | 8.00 | R1 | No | Quality-diversity, different domain |
| `WJaUkwci9o.md` (Self-Improvement) | 8.00 | R1 | No | Language model self-improvement, different domain |
| `4KqkizXgXU.md` (Red-teaming) | 8.00 | R1 | No | Red-teaming, different domain |
| `jKhNBulNMh.md` (Symb4CO) | 6.67 | R2 | Yes | Symbolic branching policies; accepted — comparable score band |
| `8QkpCRio53.md` (Preference Optimization) | 5.75 | R2 | Yes | Preference optimization for CO; rejected due to limited experiments and missing comparisons |
| `CFLEIeX7iK.md` (Neural Solver Selection) | 5.75 | R2 | No | Solver selection, different paradigm |
| `yEox25xAED.md` (Grammar RL) | 6.60 | R2 | No | Graph counting, different domain |

**Round 1 bracket:** [5.5, 7.5]. The most directly comparable papers (Hercules at 5.25, LLEGO at 6.25, BOPRO at 6.25) span this range.

**Round 2 narrowing:** Compared against itemized anchors, CALM shares the high-magnitude strengths of accepted papers (novel method, thorough experiments, strong empirical results) while lacking the fatal weaknesses that pulled rejected papers down (e.g., Hercules: -9.97 incremental over prior work; Preference Optimization: -9.55 limited experiments, -9.99 empirical results don't match claims). CALM's primary weakness (-2.73 budget asymmetry) is moderate in impact and does not threaten the core contribution, which is supported by multiple independent lines of evidence (verbal-only baseline at matched budgets, ablation study, OBP results at matched budgets, training curves). The accepted papers LLEGO (6.25) and Symb4CO (6.67) have comparably strong strengths with similar or smaller weakness magnitudes.

**Final score:** 6.5. CALM sits above LLEGO (6.25) due to its broader evaluation scope and genuinely novel combination of prompt evolution + RL fine-tuning, but below Symb4CO (6.67) due to the budget asymmetry concern and several minor clarity gaps that the stronger paper did not have.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>