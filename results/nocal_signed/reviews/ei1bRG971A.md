Now I'll compose the final consolidated review.

## Summary
This paper introduces Dynamic Nested Depth (DND), a post-training method that identifies "critical" tokens via a lightweight linear router and reprocesses them through the same transformer layer in a compact nested pass. A dual-objective router loss (score dispersion + distribution preservation) and a two-level threshold controller (buffer proportional + EMA synchronization) ensure stable token selection. DND is evaluated on three dense models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and one MoE model (Qwen3-30B-A3B), showing average gains of +1.88 to +2.61 on small models and +0.87 on the 30B MoE, with minimal parameter overhead (~0.03M) and ~92% throughput retention.

## Strengths
- **Thoughtfully designed training strategy with strong ablation support.** The dual-objective router loss plus two-level threshold controller is a coherent engineering solution to a genuine problem in token-choice routing (lack of explicit ratio control). The ablation study (Table 4) convincingly shows that removing both components drops gains from +1.88 to +1.01, confirming they are not decorative.
- **Clean post-training integration with measured efficiency.** DND requires no pre-training from scratch and no architectural modification beyond lightweight routers and a learnable fusion parameter. It works on both dense and MoE architectures. Throughput measurements (Table 3) show 91.6–93.1% speed retention, and parameter overhead is negligible (<0.1M), making the method practically attractive.
- **Well-motivated and clearly scoped problem.** The paper builds on the established observation (Gloeckle et al., 2024) that token difficulty varies, and positions DND as a natural extension beyond token pruning: allocating *additional* computation to hard tokens rather than simply discarding easy ones. The motivation is clearly presented in Section 1 and Figure 1.
- **Token selection analysis provides internal validation.** Figures 4a and 4b show that tokens selected by the router have higher logit entropy (r=0.34) and that entropy decreases after reprocessing (r=-0.58), directionally supporting the claim that DND targets uncertain tokens and refines them.

## Weaknesses

### Fatal
None.

### Major
- **Insufficient baselines for proper isolation.** The only prior method compared is ITT (Chen et al., 2025), evaluated on just one of four models (Qwen3-1.7B, Table 1). Missing are: (a) simple heuristic baselines (e.g., selecting tokens by output entropy for a second forward pass — this would isolate whether the learned router is necessary), (b) overhead-matched baselines (e.g., adding an extra layer to the full model for comparable FLOPs — this would indicate whether the gains are specific to DND's selective mechanism or simply reflect more computation), and (c) any comparison to related test-time compute scaling methods. Without these, it is unclear whether the improvements come from the DND mechanism itself or from allocating extra computation to a subset of tokens in any manner.

- **No statistical significance or variance reporting.** Every result in Tables 1, 2, and 4 is reported as a single point without standard deviations, confidence intervals, or multiple seeds. For the 30B MoE model, where the average gain is +0.87 and many individual benchmark improvements are below 0.5 points (BBH +0.13, MATH +0.15, MATH-500 +0.20, DROP +0.27), these differences could plausibly fall within evaluation noise. The ablation study (Table 4) shows several configurations differing by as little as 0.04–0.17 points (columns 3 vs. 4), further underscoring the need for variance estimates to assess whether differences are systematic.

### Minor
- **The MOR capacity claim is imprecise.** The paper states "MOR is limited to 1B-parameter, whereas our DND successfully scales to a 30B MoE model" (line 58). MOR was *demonstrated* at 1B scale, but there is no evidence it *cannot* scale. The phrasing conflates "was only shown at 1B" with "is fundamentally limited to 1B."
- **Nested depth design does not address positional embedding effects.** When selected tokens are non-consecutive in the original sequence, compacting them (Eq. 3) assigns new positional embeddings that create adjacency relationships that did not exist. The paper does not discuss whether this causes representational distortions.
- **Push-pull dynamic between router losses is not analyzed.** The paper acknowledges that L_sd (pushes scores toward 0/1) and L_dp (pulls scores toward 0.5) create tension, but does not study the resulting equilibrium, potential conflicts, or sensitivity to the ratio λ_sd / λ_dp (whose numerical values are not reported in the main text).
- **Weak correlation overinterpreted.** The Pearson correlation of r=0.34 between selection frequency and logit entropy (Figure 4a) means most of the variance is *not* explained by entropy. The claim that DND "preferentially selects tokens with greater uncertainty" (Section 4.5) overstates what this modest correlation supports.
- **Training compute cost not reported.** No GPU hours are given for DND post-training relative to vanilla SFT, making it hard for practitioners to assess practical overhead.
- **Fusion parameter β is shared across all layers** (Eq. 4), which may be unnecessarily restrictive since different layers could have different optimal fusion ratios. This design choice is not discussed or ablated.

### Trivial
None.

## Nice-to-Haves
- Add a heuristic baseline (e.g., entropy-based token selection without a learned router) to isolate the value of the learned router.
- Add an overhead-matched baseline (e.g., one extra full layer for comparable FLOPs) to test whether DND's selective mechanism drives gains beyond simply having more computation.
- Report variance estimates (multiple seeds or confidence intervals), especially for ablation comparisons.
- Include key hyperparameter values (λ_sd, λ_dp, α, γ, N_b) in the main text.
- Add a brief discussion of limitations and potential failure modes.
- Report training GPU hours.

## Removed Points
These points were raised in the input review but are excluded here:

- **Request to reimplement ITT with DND's router/training regime**: This is speculative; the paper offers an explanation for ITT's weak performance (Top-P mismatch causing train/inference discrepancy). The core concern (too few baselines) is already captured as a Major weakness.
- **Request to approximate MOR within DND's framework**: The paper explains MOR requires pre-training from scratch on 200B tokens; asking the authors to approximate it post-hoc is scope-creep.
- **"Natural next step" framing as overreach**: This is a minor presentational claim that does not affect the technical validity of the work.
- **FLOPs analysis "relegated to the appendix"**: The appendix is stripped by the parser; the paper states the analysis exists.
- **Hyperparameter values not in main text**: The paper states they are in Appendix Sec. B; this is a presentation preference, not missing content.
- **No limitation section**: A useful addition but not a core weakness; captured under Nice-to-Haves.

## Novel Insights
None beyond the paper's own contributions. The review surfaces no observation about the method or results that the paper itself does not state or imply.

## Suggestions
- Run a simple heuristic baseline (entropy-based token selection + second forward pass) to directly test whether the learned router is necessary.
- Report standard deviations or confidence intervals for the main results, particularly for the 30B MoE model and the ablation study configurations.
- Acknowledge the weak correlation (r=0.34) more honestly and discuss what additional evidence would be needed to confirm the router's selection criterion.
- Discuss the positional embedding issue for compacted non-consecutive tokens, either as a potential limitation or with analysis showing it does not matter.

## Score and Decision

Given the paper's genuine contributions — a well-motivated method, a thoughtfully designed training strategy validated by ablation, and consistent positive results across four models from different families — I consider the paper to have solid technical merit. However, the evaluation is weakened by two meaningful gaps: (1) the baseline set is too narrow, with only ITT compared on one model and no heuristic or overhead-matched baselines to isolate the mechanism's value, and (2) the absence of variance estimates undermines confidence in the stated gains, especially on the 30B MoE model where many individual improvements are small (~0.2–0.5 points). These gaps prevent the paper from being a strong accept but do not invalidate its core contribution. I assess this as a borderline accept that would benefit substantially from a strengthened empirical evaluation.

**MY FINAL SCORE: <score>6</score>**
**MY FINAL DECISION: <decision>Accept</decision>**