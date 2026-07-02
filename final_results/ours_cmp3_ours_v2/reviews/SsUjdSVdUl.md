## Summary

This paper proposes Critique-RL, a two-stage reinforcement learning approach for training critique language models without stronger supervision. Stage I optimizes the critic's discriminability (correctly judging response correctness) using direct rule-based reward signals; Stage II optimizes helpfulness (providing constructive feedback) while maintaining discriminability through regularization. The paper first diagnoses that training with only indirect reward signals (based on actor refinement) leads to critics with degraded discriminability, then proposes the two-stage solution. Experiments on math reasoning tasks show consistent improvements over SFT, STaR, Retroformer (PPO), and CTRL (GRPO) baselines across two model scales.

## Strengths

- **Clear diagnosis of a genuine problem.** Section 4.1 and Figure 3 convincingly demonstrate that RL with only indirect reward signals (r_refine, r_Δ, r_correction) leads to critics whose discriminability degrades during training, producing either overly conservative or overly aggressive behavior. The training dynamics plots show discriminability for originally-correct and originally-incorrect responses moving in opposite directions under these rewards. This finding is well-articulated and independently valuable to the community.

- **Ablation design cleanly isolates the contribution of each component.** Table 3 is the strongest evidence in the paper. Removing Stage I ("w/o Stage I"), removing Stage II ("w/o Stage II"), or removing the discrimination-preserving regularization in Stage II ("Stage II w/o discrimination") all produce clear degradations in both Acc@Refine and Acc@Dis. Crucially, these ablations stay within the same RL algorithm (RLOO), so the component-level comparison is fair. The degradation is consistent across MATH and AQuA.

- **Substantial and consistent empirical gains.** Improvements over the strongest baseline (CTRL) are large and hold across three in-domain datasets, two OOD datasets, and two model scales. For example: +2.46 accuracy and +13.51% Acc@Dis on MATH for 3B; +4.54 and +13.78 for 7B. These are not marginal.

- **Coherent narrative from diagnosis to solution.** The paper leads the reader from the failure analysis (Section 4.1) to the proposed solution in a logical sequence. Stage I directly addresses the discriminability failure identified in the diagnosis; Stage II adds helpfulness optimization with explicit safeguards against re-degrading discriminability.

## Weaknesses

### Fatal
None.

### Major

- **RL algorithm confound in main comparisons.** Critique-RL uses RLOO, while the RL baselines Retroformer uses PPO and CTRL uses GRPO (lines 250, 274). The main results table (Table 1) conflates the two-stage design with the choice of RL optimizer. The ablation in Table 3 partially mitigates this by showing that the two-stage design produces gains within RLOO — e.g., full Critique-RL (48.6 Acc@Refine) vs. "Stage II w/o discrimination" (47.3) on MATH-3B. However, the headline comparisons against Retroformer/CTRL cannot be cleanly decomposed into gains from the two-stage design vs. gains from the RL algorithm choice. The paper presents these comparisons without acknowledging this confound (Section 5.2). Adding a single-stage RLOO baseline to Table 1 would substantially strengthen the evidence.

### Minor

- **No variance or statistical significance reported.** No confidence intervals, standard deviations, or significance tests are reported for any result (Tables 1–4). Given that RL training is inherently noisy, this prevents the reader from calibrating confidence in the quantitative claims. The magnitude of the main gains is large enough that this is unlikely to change qualitative conclusions, but it is a notable omission.

- **Scope is narrower than the title suggests.** Stage I depends on a rule-based oracle verifier for correctness checking. The experiments focus primarily on math reasoning tasks where such verifiers exist. The paper references summarization experiments (CNN/DailyMail) in Appendix G (line 361), but the main body is confined to tasks with verifiable answers. The title "Training Language Models for Critiquing" implies broader generality. This limitation should be acknowledged more prominently.

### Trivial

- **Inference compute scaling figure has unclear labels.** In Figure 1's right panel, "w/o Critique-RL (3B)" appears twice in the column headers, making the legend difficult to parse. The caption mentions "@2k and @3k" but the table does not label columns accordingly.

## Nice-to-Haves

- Reporting hyperparameter sensitivity for β₁ (the Stage II discrimination reward weight, set to 0.2) would strengthen the paper, as the balance between r_refine and r_dis is central to the method.
- Including a qualitative comparison (Critique-RL critique vs. baseline critique) in the main text beyond Figure 2 would help readers understand what "better discriminability" looks like in practice.

## Removed Points

The following criticisms from the input review were removed:

1. **"SFT initialization restricts baseline performance, inflating RL gains"** — Removed because the paper's explicit goal is to avoid stronger supervision. The SFT data comes from the same weak model for all methods, making comparisons fair. The paper's claims (e.g., "RL-based methods outperform fine-tuning-based ones" at line 280) are stated in the context of its own experiments, not as universal claims. This criticism misreads the paper's scope.

2. **Section-by-section presentation nitpicks** (e.g., "formatting makes it slightly hard to parse") — Removed as formatting/style nitpicks.

3. **"Hyperparameter sensitivity" and "Actor model quality analysis"** — Removed from weaknesses; these are speculative suggestions beyond the paper's scope. They are moved to Nice-to-Haves where appropriate.

4. **Criticism about missing qualitative analysis in main text** — Moved to Nice-to-Haves; the paper does include one example (Figure 2) in the main text.

## Novel Insights

The key insight is that discriminability must be *explicitly* optimized — it does not emerge as a side-effect of optimizing refinement-based rewards. This is a crisp finding that explains why prior RL-based critique training (Retroformer, CTRL) hits a ceiling. The paper further shows that once discriminability is established in Stage I, it must be *actively preserved* during helpfulness optimization in Stage II, not merely assumed to persist. The observation that discriminability for correct and incorrect responses diverges in opposite directions under indirect rewards (Figure 3, bottom row) is particularly useful and can inform future work on critique model training.

## Suggestions

1. **Add a single-stage RLOO baseline to Table 1.** The ablation in Table 3 has something close ("Stage II w/o discrimination"), but including it as a named row in the main comparison table would allow readers to cleanly decompose how much of the gain comes from RLOO vs. the two-stage design. Also add a brief discussion acknowledging the RL algorithm difference vs. baselines.

2. **Report results with at least 3 random seeds** (or a statement about observed variance) for the main experiments. Even a brief sentence like "we observed std < 1.0 across seeds for all main results" would be informative.

3. **Move or summarize the CNN/DailyMail results into the main body** to substantiate the claim of generalization to open-ended tasks. If the appendix results are compelling, even a brief summary paragraph would strengthen the paper's scope claims. Alternatively, add a clearer scope statement to the title or introduction.

---

**Calibration Anchors.** The following human-reviewed papers were used for score calibration:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `8QTpYC4smR.md` | 1.00 | R1 | Survey paper; far weaker than Critique-RL |
| `5kMwiMnUip.md` | 1.40 | R1 | Jailbreaking paper; substantially weaker |
| `uMxiGoczX1.md` | 2.50 | R1 | Creative-writing RLHF; less rigorous experiments |
| `9LAqIWi3QG.md` | 3.00 | R1 | Reward redistribution for RLHF; limited evidence |
| `ZK1NnjpjEs.md` | 3.00 | R1 | LLM understanding via RL; weaker results |
| `50P9TDPEsh.md` | 4.67 | R1 | Critique ability benchmark; different contribution type |
| `ToWKyjwDqO.md` | 5.00 | R1 | Preference optimization for judges; comparable novelty but weaker ablation |
| `e3odKmatZr.md` | 5.25 | R1 | Critique-out-Loud reward models; interesting but lacked RLHF validation |
| `YW79lAHBUF.md` | 3.75 | R1 | In-context RL; less direct relevance |
| `JEehcb48Vp.md` | 5.75 | R1 | Critic-CoT; similar topic, smaller gains, limited novelty concerns |
| `38E4yUbrgr.md` | 6.00 | R1 | RL Contemplation; accepted, similar self-improvement approach, comparable rigor |
| `4KqkizXgXU.md` | 8.00 | R1 | Curiosity-driven red-teaming; excellent execution — stronger than Critique-RL |
| `QEHrmQPBdd.md` | 8.00 | R1 | Reward model benchmark; comprehensive, well-executed |
| `rfdblE10qm.md` | 8.00 | R1 | Reward modeling theory; deep theoretical contribution |
| `WJaUkwci9o.md` | 8.00 | R1 | Self-improvement theory; rigorous theoretical analysis |

**Bracketing rationale.** Round 1 bracketing placed the paper between 5.5 and 7.5. It is clearly stronger than Critic-CoT (5.75) and Critique-out-Loud (5.25) due to cleaner ablations and larger gains. It is comparable to RL Contemplation (6.00, accepted) but has an additional confound (RL algorithm mismatch) that prevents it from reaching the 7+ tier occupied by the 8.00 anchors (which have no such confounds and demonstrate broader validation). The final score of 6.5 reflects a solid paper with a genuine contribution and strong evidence, tempered by the RL algorithm confound in the headline comparisons.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>