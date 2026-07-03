Now let me produce the final consolidated review.

## Summary
This paper proposes CALM, a framework for Automatic Heuristic Design (AHD) that co-evolves both the prompts fed to an LLM and the LLM's own weights via GRPO-based reinforcement learning. The joint optimization allows an INT4-quantized 7B model running on a single 24GB GPU to outperform prior SOTA methods that rely on more powerful API-based models with frozen weights. The paper introduces fine-granularity mutation operators (injection, replacement), a diversity-aware crossover, a collapse mechanism for escaping local optima, and a progressive reward function designed for the RL fine-tuning loop.

## Strengths

1. **RL fine-tuning delivers a clear, measurable improvement over verbal-only guidance.** The ablation in Table 4 shows that disabling GRPO causes the largest single performance drop among all ablations (OBP gap rises from 0.71% to 1.78%, a 60% relative degradation). The training curves in Figure 2 visualize the convergence benefit from GRPO with standard deviation shading. This directly substantiates the paper's central claim that RL-based "numerical gradients" add value beyond verbal prompt manipulation. This is the strongest piece of evidence in the paper.

2. **A weaker local quantized model + RL outperforms stronger API-based models without RL.** Tables 1–3 consistently show CALM's INT4-quantized Qwen2.5-7B-Instruct (with GRPO) beating GPT-4o-mini-based SOTA methods across all four tasks: e.g., 0.71% vs 0.89% (MCTS-AHD) on OBP average gap, 3.83% vs 5.44% on CVRP N=50, 12.58% vs 15.10% on OP N=200. Section 5 explicitly acknowledges the accuracy hierarchy (GPT-4o-mini > Qwen2.5-14B > Qwen2.5-7B > Qwen2.5-7B-INT4), making this a conservative comparison.

3. **Comprehensive ablation study with 15 distinct conditions.** Table 4 systematically covers removal of RL fine-tuning, two alternative reward designs, five collapse-mechanism configurations, and removal of each of the five evolutionary operators. The ablation uncovers non-obvious findings: diversity-unaware crossover is worse than no crossover at all; removing simplification causes the largest drop in both tasks, suggesting redundancy control is critical.

4. **Even without RL, CALM's verbal guidance matches or exceeds prior SOTA.** Section 5.2 tests an API-based variant of CALM (GPT-4o-mini, no GRPO, matching baseline budgets exactly) and shows it achieves the lowest gaps on OBP 5k_100 and 10k_100, matches MCTS-AHD on CVRP, and surpasses it on OP. This cleanly separates the contribution of the evolutionary operators from the RL component.

5. **Evaluation covers four diverse optimization tasks with explicit out-of-distribution generalization.** The paper tests on OBP (6 scales, 2 OOD), TSP (N=50/100/200), CVRP (N=50/100/200), and OP (N=50/100/200), with training on small scales and testing on larger unseen scales. CALM consistently outperforms baselines on OOD scales.

## Weaknesses

### Major

1. **Main results tables lack variance information for small-margin comparisons.** Tables 1–3 report averages over 3 runs without standard deviations, confidence intervals, or error bars. Several key comparisons hinge on small absolute differences: on OBP the average gap difference between CALM (0.71%) and MCTS-AHD (0.89%) is 0.18 percentage points; on TSP N=50, MCTS-AHD (9.69%) actually leads CALM (10.04%); on OP N=50, HSEvo (23.98%) leads CALM (24.22%). With only 3 runs and no variance reported, the reader cannot determine whether any of these differences are meaningful or within the noise of the experimental setup. The paper states that p-values are in Appendix I (stripped from this text), but basic uncertainty quantification belongs in the main results exposition where the paper makes its comparative case. The training curves in Figure 2 do include standard deviation shading and provide supporting evidence, but the final aggregate tables upon which the headline comparisons rest do not.

2. **Fine-tuning method is critically underspecified in the main text.** The paper states it fine-tunes "just 1.15% of its weights" on an INT4-quantized model using "Unsloto" (presumably Unsloth), but never specifies the parameter-efficient fine-tuning approach. Are these LoRA adapters? DoRA? Selective layer fine-tuning? Which layers/modules are trained? What rank? What learning rate? How are training steps interleaved with heuristic evaluation rounds? Since the paper's central contribution is RL-based fine-tuning of the LLM, the fine-tuning mechanism itself must be precisely specified. The reference to Appendix H (stripped) does not substitute for stating the PEFT method in the main paper.

### Minor

3. **The budget comparison between CALM and baselines is not perfectly apples-to-apples.** The paper states "1,000 heuristic evaluations for baselines and a fixed budget of 2,000 LLM queries for CALM" on non-OBP tasks. Since CALM generates G>1 responses per prompt, 2,000 LLM queries produce ~2,000 heuristic evaluations — approximately 2× the baseline count. The paper calls these "comparable evaluation budgets," which is imprecise. On OBP the asymmetry runs the other direction (baselines get 2,000 evaluations while CALM gets 2,000 queries). The API-based variant in Section 5.2 (G=1, matching baseline budgets) partially addresses this concern, but the main CALM comparison should either match total heuristic evaluations or explicitly acknowledge and justify the asymmetry.

4. **Several baseline results are missing from certain tables without explanation.** ReEvo (Ye et al., 2024) is listed as a baseline in Section 5 and appears in Table 1 (OBP) but is absent from Tables 2 (TSP) and 3 (CVRP/OP). Additionally, Table 3 contains two HSEvo rows with different numerical values but no label explaining what distinguishes them (e.g., two configurations or two independent runs). The paper should clarify both absences.

5. **The reward function parameter r_invalid is ambiguously specified.** The paper states "r_invalid ∈ (-1, 0)" as a bound, but Eq. (4) uses r_invalid as a fixed scalar multiplied by α₁ or α₂. It is unclear whether r_invalid is a selected hyperparameter, a learnable parameter, or sampled from the stated range during training. The specific value or selection criterion should be stated explicitly.

### Trivial

6. **Minor inconsistency in novelty claim.** The introduction (line 32) describes CALM as "one of the first" frameworks to jointly optimize prompts and the LLM for AHD, while the conclusion (line 268) calls it "the first framework." These should be harmonized.

## Nice-to-Haves

- A controlled comparison between GRPO (used in CALM) and the DPO-based approach in EvoTune under identical base models, operators, and compute budgets would cleanly isolate the relative benefits of score-based RL vs. preference-based fine-tuning for AHD, and would sharpen the paper's contribution.
- An analysis showing what the LLM learns through fine-tuning (e.g., token-level attribution showing increased probability for code patterns from successful heuristics) would move beyond treating the model as a black box and strengthen the "co-evolution" narrative.
- Including standard deviations or confidence intervals directly in the main result tables would substantially improve the paper's empirical case.

## Removed Points

- **EvoTune anomalously weak (Harsh Critic, point 4):** The critic questions whether EvoTune was "run under conditions that disadvantage it." The paper explicitly states that all LLM-based AHD baselines were aligned with "consistent settings, including shared seed heuristics ... identical training datasets ... and comparable evaluation budgets." This is a speculative concern without evidence of unfairness. Removed as unsupported speculation.

- **"Verbal gradient" mechanism not validated (Harsh Critic):** The critic argues that the claimed connection between fine-granularity operators and GRPO credit assignment "doesn't validate the specific mechanism hypothesized." The paper states this as a design intuition ("GRPO is expected to more effectively identify") and the ablation confirms the operators are useful. The mechanism claim is stated as an expectation, not a proven result. This is reasonable engineering motivation, not an unsubstantiated claim. Demoted to nice-to-have.

- **Duplicate HSEvo row thought to be extraction artifact:** The two HSEvo rows in Table 3 have genuinely different numbers, so they may represent two configurations or runs. The issue is lack of labeling, which is captured in Minor point 4 above.

- **"First" vs "one of the first" (Style):** Minor inconsistency, merged into Trivial point 6.

- **Generic/scope-creep criticisms from the harsh critic:** Several concerns (e.g., demanding token-level attribution analysis, requesting more models) were removed as scope creep or nice-to-haves.

## Novel Insights

None beyond the paper's own contributions. The main insight — that a weaker quantized 7B model fine-tuned via GRPO during evolutionary search can outperform frozen stronger API-based models — is the paper's own central finding. The ablation's demonstration that diversity-unaware crossover is worse than no crossover is a specific, non-obvious takeaway.

## Suggestions

1. Add standard deviations or confidence intervals to all main result tables (Tables 1–3).
2. Specify the PEFT method (presumably LoRA through Unsloth), rank, learning rate, and training configuration directly in the main text.
3. Clarify the budget comparison: state that CALM evaluates ~2,000 heuristics vs ~1,000 for baselines, justify the asymmetry, or adjust budgets for stricter comparability.
4. Explicitly state the value or selection criterion for r_invalid in the reward function.
5. Add notes to Tables 2–3 explaining why ReEvo is absent and what the two HSEvo rows represent.
6. Harmonize "one of the first" (intro) with "the first" (conclusion).

## Score and Decision

Based on my assessment, the paper makes a real contribution — demonstrating that online RL fine-tuning of an LLM during evolutionary heuristic search delivers measurable improvements, including enabling a quantized 7B model to outperform stronger API-based methods. The experimental evaluation is broad (4 tasks, multiple scales, OOD testing), and the ablation study is thorough. The weaknesses are significant but addressable: the variance omission in main tables is the most serious, but the training curves (Figure 2) with std. dev. shading and the strong ablation (Table 4) partially compensate. The fine-tuning underspecification is a documentation gap rather than a methodological flaw.

This is a solid paper with a well-executed engineering contribution. The weaknesses do not invalidate the core claims but do require attention before publication. The paper is clearly above the reject threshold but has meaningful presentation gaps that prevent it from being a top-tier accept.

**Score: 6.5** — Borderline accept with needed improvements.

**Decision: Accept**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>