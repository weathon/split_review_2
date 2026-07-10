Now I have all the information I need. Let me compose the final consolidated review.

## Summary

This paper introduces CALM, a framework for automatic heuristic design (AHD) that integrates RL-based fine-tuning (GRPO) of an LLM into the evolutionary search loop, breaking from prior work that keeps the LLM frozen. The LLM co-evolves with the search by using prompt-response-performance triplets produced during evolution as training data. Combined with improved prompt-engineering operators (fine-granularity injection/replacement, diversity-aware crossover), CALM using a quantized 7B model on a single 24GB GPU consistently outperforms API-based baselines using GPT-4o-mini across OBP, TSP, CVRP, and OP tasks.

## Strengths

- **Genuinely novel direction for LLM-based AHD.** The core idea — treating the prompt-response-performance triplets produced by evolutionary search as training data for RL-based fine-tuning of the LLM itself — is well-motivated and represents a clear departure from prior frozen-LLM approaches. The paper correctly identifies this as a missing dimension in existing work (Liu et al., 2024a; Ye et al., 2024; Zheng et al., 2025).

- **Strong empirical results despite using a substantially weaker base model.** CALM uses a quantized 7B model (Qwen2.5-7B-Instruct-INT4) yet consistently achieves lower optimality gaps than API-based baselines using GPT-4o-mini across four optimization tasks (Tables 1–3). The CVRP results (Table 3: 3.83%/5.44%/3.95% vs MCTS-AHD's 5.44%/6.98%/4.70%) and OBP results (Table 1: 0.71% average gap, including zero gap on the 1k_500 test set) are particularly clean.

- **Systematic ablation study** (Table 4) decomposing contributions. The finding that disabling GRPO causes the largest drop in performance, and that removing the simplification operator has the most impact among the prompt operators, provides genuine insight into how the method works. The ablation of collapse mechanism hyperparameters and reward variants is thorough.

- **Practical resource efficiency** is demonstrated convincingly. Running entirely on a single 24GB GPU with a quantized 7B model (fine-tuning only 1.15% of weights) and outperforming methods that depend on GPT-4o-mini API access is a genuine practical contribution.

## Weaknesses

### Major

- **Evaluation budget comparison is underspecified.** The paper states "comparable evaluation budgets — specifically, 1,000 heuristic evaluations for baselines and a fixed budget of 2,000 LLM queries for CALM" (Section 5), but never specifies the value of *G* (the number of responses sampled per prompt) for the main CALM experiments. *G* = 1 is only stated for the API-based ablation (Section 5.2). Since GRPO requires *G* > 1, the total number of heuristic evaluations performed by CALM could be 2,000 (if "LLM queries" means total responses) or 2,000 × *G* (if "LLM queries" means prompts). This ambiguity makes it impossible for the reader to assess whether the comparison is fair. The paper must clarify: (a) the value of *G* for main experiments, (b) total heuristic evaluations (T × G), and (c) what "LLM query" means as a unit.

- **The "local, w/o GRPO" ablation is only reported for two of four tasks.** This ablation — the cleanest test of whether RL fine-tuning drives performance — appears only for OBP and OP in Table 4. The paper claims "disabling the GRPO module causes the largest drop in performance across near all ablations" (Section 5.2), but this claim is directly supported on only two of four tasks. Without this control on TSP and CVRP, the reader cannot assess whether the RL fine-tuning is responsible for CALM's advantage on those tasks, or whether the advantage comes primarily from the improved prompt engineering operators that CALM also introduces.

### Minor

- **No variance reported for main results (Tables 1–3).** All tables report averages over 3 runs without standard deviations, confidence intervals, or p-values. With only 3 runs, variance could be substantial, and finer-grained comparisons (e.g., TSP N=50: CALM at 10.04% vs EvoTune at 10.43%) could easily be within noise. Figure 2 provides standard deviation bands for CVRP and OP training curves but not for final test performance, and bands are absent for OBP and TSP.

- **TSP results are notably weaker than the paper's overall framing suggests.** On TSP N=50 (in-domain), CALM's gap (10.04%) is worse than MCTS-AHD's (9.69%). On N=100, CALM (11.58%) is essentially tied with MCTS-AHD (11.79%). The strong result is only at N=200 (13.41% vs 13.71%). Without variance estimates, these thin margins do not clearly support an unqualified claim of outperforming all LLM-based baselines.

- **The comparison with EvoTune confounds multiple differences simultaneously.** CALM differs from EvoTune in the RL algorithm (GRPO vs DPO), the reward function, the prompt operators, and the overall evolutionary framework. The paper does not isolate which differences drive the performance gap. The "local, w/o GRPO" ablation partially addresses whether RL helps (on OBP and OP), but a controlled comparison controlling for prompt operators and reward design would strengthen the claim that GRPO specifically is beneficial.

### Trivial

None.

## Nice-to-Haves

- A wall-clock time comparison (including fine-tuning overhead) versus API-based methods would make the practical efficiency case more concrete.
- An ablation replacing GRPO with DPO within CALM's framework would help isolate the effect of the RL algorithm choice vs. EvoTune's DPO-based approach.

## Removed Points

These points from the input review were removed, treat with caution:

1. **Reward function edge cases (duplicate penalty, clipping degeneracy).** The reviewer speculated about potential edge cases in Eq. (3)-(4) without demonstrating they cause actual problems in experiments. Removed as unsubstantiated speculation.
2. **Claim that introduction oversells novelty.** The paper explicitly acknowledges concurrent work (Surina et al., 2025; Liu et al., 2025) in Section 2 and appropriately scopes its claim as "one of the first." Removed as factually inaccurate criticism.
3. **Small G making GRPO noisy.** Speculative; no evidence provided. Removed.
4. **Analytical approximation (Eq. 2) being of questionable utility.** Subjective opinion about standard practice. Removed.
5. **HSEvo outperforming CALM on OP N=50.** The paper's claim is factually correct (it restricts the comparison to EoH, MCTS-AHD, and EvoTune), and HSEvo's margin is tiny (23.98% vs 24.22%). Removed.
6. **Missing wall-clock time.** Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Specify the value of *G* for the main CALM experiments and report total heuristic evaluations (T × G) alongside the baseline budgets. Clarify what unit "LLM query" refers to.
2. Report the "local, w/o GRPO" ablation for TSP and CVRP, either in the main tables or as an extended ablation table.
3. Add standard deviations or confidence intervals to all main results tables (Tables 1–3).
4. Consider an ablation replacing GRPO with DPO in CALM's framework to isolate the effect of the RL algorithm choice vs. EvoTune's DPO-based approach.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>