## Summary

This paper systematically ablates the components of GRPO (group-relative advantage estimation, PPO-style clipping/policy ratios, and KL regularization) to determine which are essential for training LLMs to reason on math tasks. It finds that (1) negative feedback is essential, (2) group-relative advantage estimation is crucial for stability, and (3) PPO-style clipping and policy ratios can be removed without harming performance. Based on these findings, the paper proposes RGR (REINFORCE with Group Relative Advantage), a simplified variant that retains only group-relative advantage estimation and KL regularization.

## Strengths

1. **Well-motivated and timely research question.** The paper correctly identifies that the growing ecosystem of GRPO variants (DAPO, CPPO, S-GRPO, GTPO) may be overengineering the algorithm without first establishing which components actually matter. This framing is grounded in the literature (citing Ahmadian et al. 2024) and is worth investigating.

2. **Clean conceptual ablation design.** The decomposition of GRPO into three components — group-relative advantage estimation, PPO-style clipping/policy ratios, and KL regularization — and the design of three variants that isolate each component (positive-only advantages, RGR, direct REINFORCE) is methodologically sound and maps cleanly onto the research question.

3. **RGR is genuinely simpler.** Removing policy ratios and clipping eliminates the clipping range hyperparameter ε and the min/clip machinery, yielding the gradient in Equation 2 — the simplest possible policy gradient with a group-normalized baseline. This simplification is meaningful if it holds at larger scales.

## Weaknesses

### Fatal
None.

### Major

1. **No statistical significance or variance reporting; all results are single-run point estimates.** Tables 1–3 report every accuracy as a bare number with no confidence intervals, standard deviations, or indication of multiple seeds. Many of the claimed wins for RGR over GRPO are very small (e.g., RGR vs GRPO on Llama3.2 GSM8K: 43.3 vs 43.0, a 0.3-point difference; on Qwen2.5-0.5-it Gaokao2023-Math-En, GRPO beats RGR by 30.4 vs 29.1, a 1.3-point difference). Without variance estimates, there is no way to know whether these differences are meaningful or simply noise. The claim that "RGR surpasses GRPO in 17 out of 27 individual comparisons" cannot be properly evaluated. This is the single most important evidential gap in the paper.

2. **The experimental regime (small models, LoRA, short training) is too narrow to support the broadest claims.** The paper trains 0.5B–1.5B parameter models with LoRA (rank 128, ~10% trainable parameters) on 1,800 GSM8K instances for only ~65–70 training steps. DeepSeek-R1's use of GRPO involves full fine-tuning of far larger models for thousands of steps. LoRA constrains the effective rank of weight updates, which may reduce the risk of destructive policy updates that clipping is designed to prevent, and short training runs may not experience the kind of policy collapse that clipping mitigates over longer horizons. The paper acknowledges this as a hardware limitation ("Future works will consider... larger models"), but the headline claims are stated without this caveat. The finding that "PPO-style clipping is unnecessary" needs verification at a scale closer to where GRPO is practically deployed, or at minimum a more precise scope statement.

### Minor

1. **The "reasoning emergence" analysis (Countdown, Figure 2) is anecdotal, not quantitative.** The paper claims that "RAFT and positive-only GRPO models fail to generate explicit reasoning steps" while "GRPO and RGRA models exhibit emergent reasoning," but supports this with only a single cherry-picked example from each category. No quantitative metric is provided (e.g., proportion of responses with reasoning traces across multiple prompts, reasoning quality scores). This section should either be replaced with systematic measurement or re-labeled as illustrative rather than evidential.

2. **RGR retains KL regularization, so the ablation of "PPO-style constraints" is narrower than it may appear.** The paper concludes that "PPO-style clipping is unnecessary" — which is precise — but the broader framing of "simplifying GRPO" and "complicated loss functions" (title) is somewhat misleading because RGR retains the KL penalty term β D_KL[π_θ || π_ref], which is itself a constraint mechanism. An ablation that also removes the KL term (a pure REINFORCE with group advantage, no constraints at all) would be needed to determine whether *any* constraint is necessary. Without this, the simplification is less dramatic than claimed — one constraint (clipping) is removed, but another (KL) remains.

3. **The REINFORCE-with-direct-rewards baseline is unnecessarily weak.** Comparing against raw REINFORCE with no baseline at all — which is known to be highly unstable — and concluding that "advantage estimation is essential" is unsurprising. A more informative baseline would be REINFORCE with a simple mean-reward baseline subtraction (the standard textbook variant), which would test whether a *simple* baseline suffices versus whether the *group-relative* structure is specifically necessary.

4. **The Countdown dataset is mentioned but never defined, cited, or described.** It appears once in the reasoning emergence analysis (Section 4) with no reference, no description of its contents or size, and no details on how the analysis was conducted.

5. **No discussion of hyperparameter sensitivity.** The paper does not report whether results are sensitive to the KL coefficient β, the group size G=8, the LoRA rank, or the learning rate — all choices that could affect the relative performance of GRPO vs. RGR.

### Trivial

1. **Inconsistent naming.** The method is referred to as "RGR," "RGR A," "RGRA," and "RGRa" at different points in the paper. This should be unified.

## Nice-to-Haves

- An ablation that removes the KL term (alongside clipping) would cleanly separate the question of whether *any* constraint is needed from whether *clipping specifically* is needed.
- RGR samples from π_θ rather than π_θ_old, meaning it cannot reuse old-policy samples. The paper should acknowledge this trade-off: RGR removes code complexity (no clipping/ratios) but may increase sample cost due to on-policy sampling.
- A comparison to at least one other GRPO variant (e.g., DAPO, which also modifies the clipping mechanism) would help position the work.

## Removed Points

These points from the harsh critic's review have been removed after cross-checking against the paper and applying filtering rules:

- **Missing code link** — removed per rule: missing link text ("The link to our code is ." with empty space) is treated as a parser artifact; the original submission presumably contains the link.
- **Missing appendix details / training hyperparameters** — removed per rule: appendix stripping is a parser artifact, not an author omission.
- **"No comparison to other GRPO variants (DAPO, CPPO, etc.)"** — removed per rule (scope creep): the paper's stated focus is on analyzing/simplifying GRPO, not on benchmarking against all variants. Listed as a nice-to-have instead.
- **"KL inside sum over tokens differs from literature"** — removed as a likely parser/formatting issue about equation presentation.

## Novel Insights

None beyond the paper's own contributions. The reviewers' main insight is that the paper's core evidential weakness is not its experimental design but its lack of statistical rigor — single-run point estimates with no variance reporting make many of the quantitative comparisons uninterpretable, especially when margins are small (~1–2 percentage points). This is a standard but important observation that applies broadly to empirical ML papers.

## Suggestions

1. **Run all experiments with at least 3 random seeds and report means ± standard deviations.** This is the single highest-priority improvement. Without it, numerical comparisons between RGR and GRPO are not interpretable.
2. **Replace the anecdotal reasoning emergence analysis with a proper quantitative metric** (e.g., percentage of responses containing multi-step reasoning traces across a held-out prompt set).
3. **Ablate the KL term** to cleanly distinguish whether *any* constraint is needed versus whether *clipping specifically* is needed.
4. **Add a REINFORCE-with-mean-baseline condition** to strengthen the claim that group-relative advantage estimation is specifically beneficial.
5. **Scope the claims more precisely** to the LoRA + small-model regime, and soften the title-level implication that "complicated loss functions" as a whole are unnecessary (RGR itself retains KL regularization).

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>