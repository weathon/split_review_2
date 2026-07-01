Now I have sufficient calibration context. Let me compose the final authoritative review.

## Summary

This paper proposes IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with a noising-denoising transition kernel to iteratively refine intermediate states toward higher reward. The key idea is to apply MCMC-style refinement *in situ* at chosen timesteps, rather than relying on single-pass trajectory sampling. The method is evaluated across two language diffusion models (MDLM, LLaDA-8B) and one image diffusion model (MaskGIT) with multiple reward functions.

## Strengths

1. **Principled MTM framing tailored to discrete diffusion.** The paper correctly identifies that discrete diffusion poses two specific challenges for test-time scaling: no gradient signal from reward models due to token discretization, and irreversibility of tokens once generated. The predictor-corrector framing (noise to explore, denoise to restore consistency) is a well-motivated design that follows naturally from these constraints. Casting iterative refinement as Multiple-Try Metropolis with a noising-denoising kernel is technically sound (Section 3.1).

2. **Elegant simplification of the acceptance computation.** The use of the balancing function to reduce the acceptance ratio to β = min(1, exp((r(x′)−r(x))/α)) (Equation 3) turns a potentially expensive MCMC acceptance computation into something nearly free. This is a genuine algorithmic contribution.

3. **Consistent empirical advantage across diverse settings.** The method outperforms baselines across two language diffusion models (MDLM, LLaDA-8B) and one image diffusion model (MaskGIT), with four different language reward functions and CLIPScore for images. The range of settings is substantial enough to suggest the method is not narrowly tuned to one task.

4. **Informative iteration-vs-particles analysis.** The finding that increasing iterations (k) consistently outperforms increasing parallel proposals (N) at the same total compute (Table 3, Figure 4) is a non-obvious result that supports the paper's central claim that iterative refinement is the right mechanism. This strengthens the paper beyond what a simple performance comparison would provide.

## Weaknesses

### Major

1. **NFE-based comparison mixes fundamentally different computational profiles, directly affecting the headline efficiency claims (Section 3.3, Section 4.2, Figure 2).** IterRef's computational profile (many short partial noising-denoising calls per refinement step) is structurally different from parallel-sampling baselines like BoN (many full denoising trajectories + reward calls). The paper acknowledges this concern explicitly — *"aggregating these into a single NFE value may obscure meaningful differences, and it is preferable to report generative-model calls and reward-model calls separately"* (Line 174) — but then proceeds to use aggregated NFE in every main figure and bases the "8× faster" claim on it. The claim that IterRef at 4T NFE matches FK at 32T NFE (Section 4.2) is a statement about NFE-efficiency, not necessarily wall-clock speed or practical cost, because the ratio of diffusion-model calls to reward-model calls differs across methods. Without separate reporting of these components in the main results, or a wall-clock analysis in the main paper, the headline efficiency comparisons are not fully interpretable. The paper states Appendix C.4 provides wall-clock analysis, but this belongs in the main text for the central claim.

2. **No statistical uncertainty reported for any language result (Section 4.2).** All language experiments report only mean scores with no error bars, standard deviations, or confidence intervals across the 3 seeds × 15 prompts setting. Given that between-prompt variance on metrics like CoLA, Toxicity, and Perplexity is typically substantial, the absence of variance information makes it impossible to assess whether observed gaps (e.g., the 4-point CoLA difference between "Evenly" at 83.0 and "0.1T" at 87.0 in Table 2) are meaningful or within noise. The non-monotonic behavior in Table 3 (k=8,N=4 outperforming k=16,N=2 by 6 points on Toxicity) further underscores this concern.

3. **PG-DLM (Dang et al., 2025) is discussed in Related Work but entirely absent from the experimental comparison (Section 4.1).** PG-DLM applies Particle Gibbs sampling, repeatedly resampling entire trajectories — it is the most conceptually relevant MCMC-based baseline for IterRef. The paper compares against FK Steering (SMC-based trajectory search), SVDD (importance sampling), SoP (continuous-diffusion search adapted to discrete), and BoN, none of which are MCMC-based trajectory refinement methods. While the paper already compares against four reasonable baselines, the omission of the one method that shares IterRef's MCMC-refinement philosophy is a notable gap that weakens the empirical comparison, regardless of whether PG-DLM is stronger or weaker.

### Minor

4. **The convergence guarantee (Proposition 1) assumes a condition unlikely to hold in practice and lacks caveats.** Proposition 1 requires that q and p_θ "form a reversible Markov kernel." In practice, p_θ is a learned approximation of the true reverse process, and there is no reason to expect the pair (q, p_θ) to satisfy detailed balance except in the limit of perfect training. This does not invalidate the method — many MCMC methods work well with approximate kernels — but the paper presents the convergence result as a clean theoretical guarantee without discussing how severely the assumption is violated in practice and what effect that might have.

5. **The s parameter (how far to noise forward in the transition kernel) is never specified.** The transition kernel K(x_t, x_t') = Σ_{x_s} q(x_s|x_t) p_θ(x_t'|x_s) (Equation 2) leaves s as a free parameter with only "t < s" specified. How s is chosen directly determines the cost of each proposal (s−t diffusion-model calls, as noted in Section 3.3) and affects the exploration behavior. This is a meaningful reproducibility gap.

6. **The "8× faster" headline claim conflates NFE efficiency with practical speed.** The claim "IterRef with only 4T NFEs matches FK with 32T NFEs, resulting in nearly an 8× faster inference-time scaling" (Section 4.2) is framed in terms of NFE, but the paper's own Section 3.3 acknowledges that NFE conflates different types of model calls. Without wall-clock validation in the main text, this claim is misleading in isolation.

### Trivial

None.

## Nice-to-Haves

- Separate reporting of diffusion-model calls and reward-model calls in the main figures (or moving the wall-clock analysis from the appendix to the main paper).
- Error bars or confidence intervals on all main results.
- Including PG-DLM as a baseline, even in the appendix.
- Clarifying how s is chosen in the transition kernel.
- Softening the "8× faster" claim or qualifying it alongside the NFE caveat.
- Discussing the practical implications of the reversibility assumption in Proposition 1.

## Removed Points

- **p(x_t) computation in Equation (2) concern**: The critic questions how the marginal p(x_t) is computed in the balancing function. However, the paper shows that the specific choice of λ leads to tractable simplified formulas (w_n = N^{-1}, β = min(1, exp(…))) in Equation (3), with derivations deferred to the appendix. Since the main text already demonstrates that the computation reduces to a tractable form, this is a standard practice of deferring algebraic derivations.
- **Figure 5(a) label inconsistency**: The alt text mentions methods "SLP, SR, SVTOD" not defined in the main text. This is a parser artifact from the figure's embedded text; the actual paper caption correctly describes the figure as comparing against "baselines."
- **Scope creep criticisms about SoP adaptation to discrete diffusion**: The critic questions whether SoP is fairly adapted to the discrete setting. The paper states that baseline hyperparameters are "favorably configured by following the original papers" (Line 186). The reviewer has no evidence that the adaptation was unfair, and the asymmetry of comparison (favoring baselines) makes this speculation rather than a concrete weakness.
- **Criticism that 15 prompts is too narrow**: The 15-prompt evaluation is standard in the controllable generation literature (Han et al., 2022, as cited). The paper also validates on image domains with 50k generations, providing cross-modal support.
- **"Evenly vs. specific timesteps" confound concern**: The critic notes that applying IterRef evenly means each application gets fewer iterations. However, the paper explicitly states it fixed the total NFE budget (Line 260), making this a controlled comparison by design.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Separate the compute accounting.** Present all main results with broken-down counts of diffusion-model calls and reward-model calls, or move the wall-clock analysis into the main paper. Without this, the central efficiency claim is not fully interpretable.

2. **Add variance information.** Standard errors across seeds, or per-prompt box/violin plots, would substantially increase confidence in the reported improvements.

3. **Include PG-DLM as a baseline.** Even a single configuration in the appendix would address the most salient comparison gap.

4. **Clarify the s parameter and the reversibility assumption caveat.** Both are small changes that would improve reproducibility and scientific honesty.

## Score and Decision

**Round 1 bracket:** 4.5–6.5

**Calibration anchors used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/.../u1cQYxRI1H.md` | 0.50 | R1 | Unrelated paper (illumination harmonization); not comparable |
| `/home/.../Uj0h13lVrR.md` | 1.00 | R1 | GFlowNets paper with fundamental flaws; the current paper is substantially stronger |
| `/home/.../2fgzf8u5fP.md` | 3.80 | R1 | Derivative-Free Guidance paper — similar topic but weaker empirical results and questionable theoretical grounding; current paper is stronger |
| `/home/.../4hFT4rfG40.md` | 3.75 | R1 | Plug-and-Play Controllable Generation paper — weak theoretical contribution and limited experiments; current paper is stronger |
| `/home/.../MBDH5zyxHM.md` | 4.60 | R1 | Controlled Denoising paper — simpler method, unclear scope; current paper has more principled framework |
| `/home/.../Ombm8S40zN.md` | 6.25 | R2 | Steering MDMs via DDPP — similar topic but training-based approach, stronger empirical validation (wet-lab); current paper has more novel methodology |
| `/home/.../i5MrJ6g5G1.md` | 5.25 | R2 | Simple Uniform Discrete Diffusion — simpler guidance mechanisms, smaller vocabulary scope; current paper has broader empirical scope |
| `/home/.../0FbzC7B9xI.md` | 6.60 | R1 | Truncation for physics diffusion — clear contribution but weak theoretical novelty; comparable to current paper |
| `/home/.../kIPEyMSdFV.md` | 7.00 | R1 | Reverse Diffusion Monte Carlo — strong theoretical contribution; current paper has more empirical breadth |
| `/home/.../QyNN5n37nK.md` | 5.75 | R2 | Unified Multimodal Discrete Diffusion — mixed results led to rejection despite decent scores; current paper has cleaner results |

**Final score determination:** The paper's novel MTM-based method and consistent cross-modal empirical results place it above the 3.8–4.6 papers that had weaker methods or inconclusive results. However, the three Major weaknesses — particularly the NFE accounting issue that directly affects the central claim, and the missing error bars — prevent the paper from reaching the 6.0+ tier where the empirical evidence more cleanly supports the claimed advantages. The method is genuinely interesting and likely useful, but the current presentation overstates the evidence. Score 5.5 reflects a borderline accept with substantial revisions needed.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>