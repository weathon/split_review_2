## Summary

This paper introduces CANON (Conditional advaNtage estimatiON), a novel advantage estimation method for Reinforcement Learning with Verifiable Rewards (RLVR) in LLMs. The core idea is to split sampled responses into two groups based on a training metric (entropy or response length), then compute inter-group and intra-group advantages that let the data determine which direction of the metric is beneficial, rather than imposing a hard-coded directional prior. The authors provide theoretical grounding (Theorems 1 and 2) showing CANON selectively amplifies the grouping metric's signal, and that DR.GRPO is a special case when μ=0.5. Empirical results across six math reasoning benchmarks and three logic reasoning tasks on three LLMs demonstrate consistent improvements, with particularly strong efficiency results establishing a clean Pareto frontier in the performance–token-cost trade-off.

## Strengths

- **Well-motivated and technically clean core idea (Section 4).** CANON's solution—splitting responses into two groups by metric value, then computing inter-group and intra-group advantages—lets the data determine which direction of the metric is beneficial while amplifying the metric's influence. The formulation is simple and the mechanism is transparent. **[impact=+9.45]**

- **Theoretical grounding showing selective amplification (Section 4.2, Theorems 1 and 2).** Theorem 1 establishes that with equal-sized groups, the inter-group advantage amplifies the signal of the grouping metric relative to DR.GRPO. Theorem 2 shows CANON does not amplify independent conditions—it is selective. The unifying observation that DR.GRPO is a special case of CANON when μ=0.5 (Eq. 7) is a nice theoretical contribution. **[impact=+9.99]**

- **Strong efficiency results with a genuine Pareto frontier (Section 5.3, Table 3, Figure 4).** CANON-Eff at α=0.96 achieves essentially the same accuracy as DR.GRPO (56.2 vs 56.6) with 26% fewer tokens (822 vs 1115). At α=0.88, it dominates the Length Reward baseline with lower tokens and better accuracy. The Pareto frontier analysis (Figure 4c) shows CANON-Eff dominating all baselines across the efficiency–accuracy trade-off space—a rare and clean result. **[impact=+10.00]**

- **Training dynamics analysis provides mechanistic insight (Section 6, Figures 2, 5, 6).** The analysis of how CANON-Inter reduces entropy (favoring exploitation) while CANON-Intra increases it (favoring exploration), and how CANON-Dynamic's scheduled μ achieves positive rethinking gains without sacrificing training reward, substantiates the claimed mechanism. **[impact=+9.97]**

## Weaknesses

### Fatal
None.

### Major

- **Figure 3 radar chart data is inconsistent with main experimental tables without explanation.** The table beneath Figure 3 reports values that do not match Tables 1 and 2. To cite specific discrepancies for Qwen2.5-Math-7B: DR.GRPO Math is shown as 57.6 in Figure 3 (Table 1 says 55.7), DR.GRPO Logic as 39.2 (Table 1 says 26.2), CANON-Inter Math as 45.0 (Table 1 says 57.6), and CANON-Intra Logic as 45.0 (Table 1 says 29.1). CANON-Dynamic shows suspiciously symmetric values (45.0/45.0 for Qwen-7B, 35.2/35.2 for Llama-8B) that do not match any tabular results. The paper states "Performance is measured on a scale from 0 to 100" but does not describe any normalization, rescaling, or transformation procedure. This is a presentation/transparency issue that must be resolved—either by explaining the transformation applied or correcting the table. It does not affect the integrity of the main tabular results (Tables 1, 2, 3) which are independently consistent.

### Minor

- **The Llama3.1-8B experiments use a different training dataset.** The paper states (Section 5.2, line 198) that for Llama3.1-8B, "we collect a simpler dataset with 35k samples from four open-source datasets" vs the 45k from OpenR1-Math-220k used for Qwen models. This confounds the model comparison: the Llama results may reflect the different training data rather than (or in addition to) the method's generality. The main Qwen experiments use consistent data and are not affected.

- **CANON-Dynamic results involve model-specific schedule selection, weakening the generality claim.** The paper tries four scheduling strategies and selects different ones for different models (Cosin-First-Inter-Later-Intra for Qwen-7B and Llama-8B, First-Inter-Later-Intra for Qwen-1.5B). The improvements over DR.GRPO (1–3 points) are modest enough that some gap could be attributed to the extra degrees of freedom in schedule selection. The paper acknowledges this, but a cleaner comparison would use a fixed schedule for all models and report that result alongside the per-model optima.

- **No variance or statistical significance reporting.** The paper reports single-run results without error bars or confidence intervals. Several claimed improvements are modest (1–3 points on aggregate metrics, 5 points on AIME24 but −1.6 on AIME25) and could fall within noise—especially on small benchmarks like AIME (~30 problems). While single-run reporting is common in large-scale LLM training due to cost, at minimum this limitation should be explicitly discussed.

### Trivial
None.

## Nice-to-Haves
- Response-level to token-level advantage conversion could be stated more explicitly (though it follows the standard GRPO convention).
- An ablation varying the group split ratio (e.g., 40:60, 30:70) would test whether the equal-size constraint is necessary or merely sufficient.
- A sensitivity experiment with G=32 or G=8 samples per prompt would assess robustness to group size.
- Reporting GPU hours or wall-clock time would help practitioners assess the computational overhead (which is claimed to be negligible).

## Removed Points
- **[Theorem 1's practical scope]** — The paper explicitly addresses this by sorting and splitting into equal-sized groups (line 96: "Based on Theorem 1, we divide the responses into two equally sized groups"), circumventing the concern. The reviewer's own text acknowledges the paper handles this.
- **[Response-to-token-level advantage conversion]** — The subscript t in Eqs. 3–4 with response-level R_o follows the standard GRPO/PPO convention where the same advantage is applied to every token. Not a genuine gap.
- **[CANON-Dynamic presupposes preference about when to schedule]** — The schedule governs task balance, not metric direction. The paper's claim is specifically about not presupposing metric direction.
- **[Token budget as confound in Table 1]** — Addressed in Section 5.3 through controlled budget experiments.
- **[Numerical Scaling factor of 2 is arbitrary]** — The comparison adequately demonstrates that naive scaling does not replicate CANON's effects; a sweep would strengthen but is not required.
- **[Missing ablation on group size, sensitivity to G, failure modes, compute budget]** — Reasonable suggestions but typical paper-length constraints rather than core weaknesses; moved to Nice-to-Haves.
- **[Missing related works]** — Not verifiable from information available to the reviewer.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Resolve the radar chart discrepancy** — Clearly explain what normalization or transformation was applied to produce the Figure 3 table values, or remove the inconsistent table and present the radar chart with actual performance values.
2. **Add multiple-seed runs or bootstrapped confidence intervals** — Even 2–3 seeds for the main comparisons (Tables 1 and 2) would give a sense of variance, especially for small-benchmark subsets (AIME, ZebraLogic).
3. **Use a fixed schedule for all models in the main comparison** — Report per-model optimization separately as supplementary, with the fixed-schedule result as the primary comparison.
4. **Ablate the Llama training dataset confound** — Run the Llama3.1-8B experiment on the same training data as the Qwen models, or add an explicit ablation controlling for dataset effects.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison to CANON |
|---|---|---|---|---|
| Uj0h13lVrR.md | 1.00 | 1 | No | Not relevant (GFlowNets) |
| 5kMwiMnUip.md | 1.40 | 1 | No | Not relevant (jailbreaking) |
| 8QTpYC4smR.md | 1.00 | 1 | No | Not relevant (survey) |
| gwZ90hFSL2.md | 1.00 | 1 | No | Not relevant (robotics) |
| u1cQYxRI1H.md | 0.50 | 1 | No | Outlier with 10/10/10/10 scores |
| ZK1NnjpjEs.md | 3.00 | 1 | No | Much weaker method, limited results |
| 28TLorTMnP.md | 2.50 | 1 | No | Weaker approach, limited evaluation |
| VRRuYBaq9u.md | 3.25 | 1 | No | Less relevant (POMDP) |
| 9LAqIWi3QG.md | 3.00 | 1 | No | Weaker empirical results |
| H8RgPl5OQX.md | 3.00 | 1 | No | Less relevant |
| **F0GNv13ojF.md** | **5.17** | **1** | **Yes** | Similar topic; CANON has far stronger novelty and cleaner evaluation; scored above |
| **gdzpnRBP4F.md** | **4.50** | **1** | **No** | Weaker method, modest gains |
| N2sN3LESoW.md | 4.75 | 1 | No | Less relevant (preference optimization) |
| **RtOTTdWbZd.md** | **5.25** | **1** | **Yes** | Similar (advantage estimation); CANON has stronger theory and evidence; scored above |
| MwU2SGLKpS.md | 4.50 | 1 | No | Less relevant (reward models) |
| **O0sQ9CPzai.md** | **6.33** | **1** | **Yes** | Comparable quality; both accepted; CANON has stronger strengths |
| **rlgplAuN2p.md** | **6.80** | **1** | **Yes** | Comparable quality; CANON similarly strong |
| N6o0ZtPzTg.md | 6.00 | 1 | No | Less relevant (prompt optimization) |
| DpFeMH4l8Q.md | 5.67 | 1 | No | Less relevant (few-shot alignment) |
| **mMPMHWOdOy.md** | **8.00** | **1** | **Yes** | Much stronger absolute results; CANON scored below |
| rfdblE10qm.md | 8.00 | 1 | No | Different focus (reward modeling theory) |
| OOxotBmGol.md | 8.00 | 1 | No | Different focus (Bayesian optimization) |
| 8BAkNCqpGW.md | 8.00 | 1 | No | Different focus (POMDP theory) |
| WJaUkwci9o.md | 8.00 | 1 | No | Different focus (self-improvement) |
| **HGCk5aaSvE.md** | **6.50** | **2** | **Yes** | Similar Pareto/efficiency framing; CANON has substantially stronger strength scores (+9.4 to +10.0 vs +1.6 to +7.8) |
| aVfDrl7xDV.md | 6.25 | 2 | No | Different focus (Bayesian optimization for search) |
| fWRBheSJth.md | 6.67 | 2 | No | Different focus (prompt optimization with gradients) |
| womU9cEwcO.md | 6.67 | 2 | No | Different focus (autonomous agents) |
| e2NRNQ0sZe.md | 6.25 | 2 | Yes | Different focus (LLM priors for RL); accepted |
| u6imHU4Ebu.md | 5.75 | 2 | No | Different focus (embodied tasks) |

**Round 1 bracket**: [5.5, 7.5]

**Narrowing rationale**: CANON sits clearly above the 5.17/5.25 papers (which had fundamental novelty and baseline concerns) and below the 8.00 WizardMath paper (which had dramatically stronger absolute gains). Compared directly with the closest anchor **HGCk5aaSvE** (ParetoPrompt, 6.50, accepted), CANON's strengths are uniformly higher-magnitude (+9.45 to +10.00 vs +1.66 to +7.75) and its main weakness (radar chart presentation) is less concerning than ParetoPrompt's weaknesses (missing baselines, limited experiment scope, counterintuitive objectives, all scoring -8.88 to -9.98). CANON's secondary weaknesses have very low impact scores (-0.01, -0.38, -4.93), indicating the scoring model considers them minor.

**Final score**: 6.5 — a solid paper with a genuinely novel method, sound theoretical grounding, and strong empirical results (particularly the efficiency Pareto frontier). The radar chart discrepancy is a real presentation concern that needs fixing, but it does not undermine the core methodological contribution or the independently consistent tabular results.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>