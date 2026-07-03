## Summary

This paper addresses the problem of unsafe intermediate reasoning (CoT) in Large Reasoning Models (LRMs), where harmful content persists even when final responses appear safe. The authors propose Intervened Preference Optimization (IPO), which: (1) empirically analyzes safety dynamics during generation, identifying "safety triggers" and "compliance cues" as critical junctures; (2) constructs preference pairs by replacing compliance cues with safety triggers at critical steps; and (3) applies DPO on the diverging segments only. Experiments across three model families (DS-8B, DS-7B, Qwen3-8B) and three safety benchmarks show consistent improvements in reasoning safety, achieving a relative reduction of over 30% in overall harmfulness while preserving reasoning capability.

## Strengths

- **Quantitative, automated procedure for identifying safety triggers**: Rather than relying on qualitative observation, the paper defines the Continuation Safety Ratio (CSR, Eq. 1) and a precise turning-point detection rule (Eq. 2 with μ=0.9, K=15). Section 3.1 reports that over 90% of sampled safe trajectories contain such turning points, enabling automatic construction of a trigger pool rather than manual curation.

- **Causal evidence that compliance-cue replacement steers reasoning toward safety**: Section 3.3 (Figure 6) directly tests the paper's core mechanism — substituting a compliance cue with a safety trigger progressively reduces the harmful ratio from ~100% to ~15% over five iterative interventions. This is causal evidence for the corrective claim, not just correlational.

- **Ablation isolating the benefit of divergence-point DPO over full-trajectory DPO**: Table 3 shows that partial DPO (applied only to the divergent segment) achieves 10.9% average harmfulness on StrongReject, substantially better than full-trajectory DPO (19.0%) and SFT (42.3%). This directly validates the design choice to focus supervision at safety-critical steps rather than treating all tokens equally.

- **Quantitative diagnosis and explicit remedy for the rollout-diversity bottleneck in RL-based safety alignment**: Section 2.3 (Figure 4) shows that ~36% of prompts yield zero safe reasoning paths in GRPO rollouts and ~50% yield few or none, concretely explaining why GRPO struggles. IPO circumvents this by creating safe trajectories through intervention, requiring ~14 generations and ~40 minutes vs. GRPO's ~40 generations and >2 hours (Section 4.3).

- **KL divergence analysis provides mechanistic evidence for targeted supervision**: Figure 7 shows IPO produces a sharp KL divergence peak (~1.75 at token index ~50) concentrated where compliance cues appear, while STAR and RealSafe show flat, low divergence (<0.5). This confirms that IPO's training signal lands at the intended critical steps, whereas prior methods lack such token-level behavioral verification.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Evaluation judge confounded with training pipeline components**: GPT-4o serves three roles: (a) safety evaluator for all experimental results (Section 2.1), (b) compliance cue detector for training data construction (Section 3.4), and (c) compliance cue labeler for the correlation analysis (Section 3.2). While Table 3 ablates the training detector (showing robustness when using DeepSeek-R1 or DS-8B instead of GPT-4o), the *evaluation* judge remains GPT-4o throughout. This means the evaluation partially measures how well models produce outputs that GPT-4o considers safe, rather than measuring genuine safety. The improvements are large and consistent across three models and three benchmarks — so this does not invalidate the results — but the paper would benefit from either a human evaluation sample or an evaluation using a different judge model that was not involved in any part of the pipeline.

- **No variance or statistical significance reported**: All safety results in Tables 2 and 3 are single-point estimates. Safety evaluations on 100–250 prompts using a stochastic judge (GPT-4o) will have non-trivial variance. Without confidence intervals, error bars, or significance tests, it is difficult to assess whether differences between IPO and the best baselines (e.g., IPO 15.3% vs. GRPO 18.5% reasoning harmfulness on DS-8B) are reliable or within noise. While the overall trends are consistent, this reporting gap weakens the quantitative rigor.

- **Safety trigger pool construction is underspecified**: The paper identifies triggers from "30 prompts from JailbreakBench" (Section 3.1) and uses "six representative safety triggers" (Section 4.1). The total pool size, the criteria for selecting the six as "representative," and whether performance degrades with fewer or different triggers are not reported. With only six trigger templates, there is a risk that the model learns to pattern-match to those specific phrases rather than developing a generalized capability for safe reasoning. The strong generalization across diverse benchmarks (including WildJailbreak) partially mitigates this concern, but an ablation over trigger pool size and selection would strengthen the method characterization.

### Trivial

- **"Over 30% relative reduction" claim could be more precisely qualified**: The abstract states "a relative reduction of over 30% in harmfulness" without specifying the reference baseline or metric. The claim holds for overall harmfulness (averaging reasoning and response) against the best per-model baselines, but the precise value varies depending on which baseline and metric are used. A qualification would improve precision without weakening the result.

- **GRPO baseline details are thin**: The paper says GRPO is trained "until reward convergence with at least twice the sampled trajectories of IPO" but does not report training steps, learning rates, or whether reward collapse was observed. Given GRPO is a key comparison point, slightly more detail (e.g., in the appendix) would aid reproducibility.

- **SafeKey baseline citation**: SafeKey is listed as a baseline in Table 2 but is not explicitly named in the related work section (Section 5 refers to "Zhou et al. (2025b) further enhances STAR" without the SafeKey name). Minor inconsistency.

## Nice-to-Haves

- A human evaluation on a subset (50–100 outputs per model) comparing IPO vs. best baseline would directly address the GPT-4o confound concern.
- Ablation of trigger pool size (1, 3, 6 triggers) would clarify sensitivity to this design choice.
- Evaluating with at least one non-GPT-4o safety judge would decouple the training–evaluation confound.

## Removed Points

These points were flagged by the reviewer inputs but are removed with justification:

- **Figure 6 data appearing identical across trigger types**: The harsh critic noted that the extracted table shows all three trigger types with the same harmfulness percentages at each intervention step. This is a parser artifact (the original figure is garbled in extraction), not a problem in the submitted paper. Removed per the rule against formatting/parser artifacts.
- **GRPO baseline description being insufficient**: While the critic asked for more training hyperparameters, the paper's statement "trained until reward convergence with at least twice the sampled trajectories of IPO" is a reasonable level of detail for a conference paper; the criticism was demoted from the critic's original framing to trivial above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add bootstrapped confidence intervals or standard errors to the main results in Tables 2 and 3 to support statistical comparisons.
2. Evaluate with at least one non-GPT-4o judge (e.g., an open-source safety classifier) or provide a human evaluation sample of 50-100 outputs to decouple the training–evaluation confound.
3. Report the total size of the identified safety trigger pool and the criteria used to select the six "representative" triggers used in training.
4. Qualify the "over 30% relative reduction" claim in the abstract with the specific reference baseline (e.g., "over 30% relative reduction in overall harmfulness compared to the best prior method").
5. Include GRPO training hyperparameters (learning rate, number of steps, reward curves) in the appendix for reproducibility.

## Score and Decision

**Calibration note**: The calibration_search tool encountered a persistent file-system error and was unable to retrieve anchor papers. Score is based on direct analysis of the paper's content and reviewer inputs against the ICLR scoring rubric.

**Reasoning**: This paper makes three concrete contributions: (1) it quantifies the gap between reasoning-level safety and response-level safety across multiple aligned LRMs; (2) it provides an empirical analysis of safety dynamics during generation, identifying safety triggers and compliance cues as critical junctures; and (3) it proposes IPO, a well-motivated method that leverages these insights, with strong and consistent results across three model families and multiple benchmarks. The weaknesses (GPT-4o confound partially addressed by ablation, missing variance estimates, underspecified trigger pool) are real but do not threaten the core claims. The improvements are large and consistent enough that the qualitative conclusion — IPO substantially improves reasoning safety — is robust. The paper is well-written, the method is clearly motivated from empirical observations, and the problem is timely and important. This is a clear accept.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>