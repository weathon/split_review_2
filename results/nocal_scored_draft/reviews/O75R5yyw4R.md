Now let me produce the final consolidated review.

## Summary

This paper proposes IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transitions to iteratively refine intermediate states toward reward alignment. The key innovation is a tailored balancing function that makes proposal weights uniform and acceptance depend only on the reward difference, avoiding costly reward-weighted proposal selection. Experiments across text (MDLM, LLaDA-8B) and image (MaskGIT) domains show consistent improvements over baselines like BoN, FK, SVDD, and SoP.

## Strengths

- **Well-motivated problem and method design.** The paper correctly identifies two genuine obstacles to test-time scaling in discrete diffusion — no gradient access from reward models and the irreversibility of generated tokens — and designs the noising-denoising kernel to address both. The predictor-corrector inspiration (Song et al., 2020) is conceptually clean and naturally suited to the setting.

- **Principled theoretical framing via Multiple-Try Metropolis.** The choice of MTM is not decorative: the paper tailors the transition kernel K and balancing function λ so that importance weights become uniform (w_n = N⁻¹) and the acceptance probability reduces to min(1, exp((r(x_t') − r(x_t))/α)). This means the selection step requires no reward model calls — reward evaluation enters only in the acceptance step, which is a genuine efficiency advantage over particle-based alternatives like SMC that must weight every particle at each step.

- **Consistent empirical gains across modalities and backbones.** Results in Figure 2 (MDLM and LLaDA-8B across four language rewards) and Table 1 (MaskGIT with CLIPScore) show IterRef outperforming baselines at nearly every compute budget. The advantage holds across absorbing-state diffusion (MDLM, LLaDA) and masked image modeling (MaskGIT), and across diverse reward functions (classifier-based, embedding-based, perplexity).

- **Timestep analysis yields a non-trivial insight.** Table 2 shows that later denoising stages (closer to t=0) matter more for discrete diffusion, which contrasts with continuous diffusion where early steps dominate. This is a genuinely interesting finding about the dynamics of discrete diffusion models that goes beyond evaluating the proposed method.

- **Iterations vs. particles analysis (Table 3).** The controlled comparison at roughly constant compute (k×N ≈ 32) shows that increasing iterations k is more effective than increasing particle count N. This directly supports the paper's core thesis — that iterative refinement of a single state is more valuable than parallel exploration of many states.

## Weaknesses

### Fatal
None.

### Major

- **Convergence guarantee depends on an unverified reversibility assumption.** Proposition 1 assumes "q and p_θ form a reversible Markov kernel," a strong condition requiring p_θ to be the exact reversal of q over multiple steps. In practice, p_θ is a learned approximation of the *single-step* reverse process; the integrated kernel K(x_t, x_t') = Σ_{x_s} q(x_s|x_t) p_θ(x_t'|x_s) involves two steps (noise then denoise), and there is no reason to expect exact reversibility. The paper acknowledges this only as an assumption and provides no empirical diagnostics (e.g., measuring how close p(x_t)K(x_t,x_t') and p(x_t')K(x_t',x_t) actually are for trained models) nor analysis of robustness when reversibility is violated. This does not invalidate the paper's empirical contribution — the theory is a supporting guarantee, not the primary result — but it leaves the theoretical claim weaker than it appears at first glance.

### Minor

- **No uncertainty quantification in experimental results.** All results are reported as point estimates with no standard deviations, confidence intervals, or error bars. The language experiments use 15 prompts with 20 samples each (300 generations per condition). Variance across prompts could be substantial, and without error bars the reader cannot assess whether IterRef's advantages are statistically reliable, especially when multiple methods have similar scores at the high end of the compute axis in Figure 2.

- **The "8× faster" claim is presented ambiguously.** The specific 8× comparison in Section 4.2 is clearly for MDLM + Toxicity reward (4T NFEs matching FK at 32T NFEs). However, the label "8× faster" appears in Figure 1(b) which displays LLaDA-8B safety results. The figure caption references Section 4.5 for details, but Section 4.5 does not explicitly articulate an 8× comparison for LLaDA-8B. This creates a mismatch between a visual claim and the text's explicit justification, which could mislead readers.

- **Small-scale language evaluation limits confidence in generalizability.** The main language experiments use 15 prompts (Han et al., 2022) with 20 samples each. This is far fewer than typical evaluations in the controllable generation literature (often 100+ prompts). With only 15 prompts, a few outlier responses could disproportionately affect the averages. The image experiments (50k conditional generations) are much more thorough, but the language evaluation — where most headline claims are made — is undersampled.

- **The "pool reuse" strategy lacks theoretical justification.** When a proposal is rejected, the paper reuses the previously generated sampling pool. The paper states the pool remains "valid" because candidates were drawn i.i.d. from the same kernel, but it does not discuss how reusing proposals (which were already tested in the previous iteration's acceptance step) affects the Markov property or the convergence guarantee of Proposition 1.

- **Limited analysis of failure modes.** The paper mentions one case (LLaDA + CoLA, where BoN outperforms), but otherwise presents uniformly positive results. A discussion of when and why the advantage diminishes — specific reward functions, compute regimes, or model architectures where IterRef does not help — would strengthen credibility.

### Trivial
None.

## Nice-to-Haves

- Include wall-clock time results in the main text (the paper notes they exist in Appendix C.4) rather than deferring them, since NFE-based cost conflates generative and reward model calls in a way the paper itself acknowledges.
- Expand the language evaluation prompt set from 15 to at least 50–100 prompts for stronger generalizability claims.

## Removed Points

- **NFE cost measure concern (originally "Critical Issue 4").** The paper explicitly acknowledges this concern (line 174: "aggregating these into a single NFE value may obscure meaningful differences") and states Appendix C.4 provides wall-clock time analysis. The paper already addresses this concern; further critique is unwarranted.
- **Test-time scaling framing as tenuous.** This is a scope-creep / framing preference criticism. The paper clearly defines test-time scaling in the discrete diffusion context, and the method genuinely involves scaling compute at inference. Not a substantive weakness.
- **Notation issue in Algorithm 1.** A formatting nitpick common in MTM literature.
- **Section-by-section notes that were neutral or positive** (Preliminaries: "no issues," Related Works: "accurate," Ethics: "adequate").

## Novel Insights

The review contributes one genuinely novel observation beyond the paper's own contributions: the reversibility assumption's practical validity is the primary gap between the paper's theory and its empirical claims. While the paper is transparent about stating the assumption, the practical distance between the idealized reversibility condition and the behavior of learned denoisers is unexamined. All other review insights either restate what the paper already says or are standard evaluation desiderata (error bars, larger prompt sets).

## Suggestions

1. Add empirical diagnostics for the reversibility assumption: measure how close the forward-backward transition distributions are for the trained models used in experiments.
2. Include error bars or variance estimates (e.g., standard deviations across prompts) in the main experimental figures.
3. Clarify the "8× faster" claims: spell out the specific comparison for each setting (MDLM/Toxicity and LLaDA/safety) directly in the main text rather than relying on figure labels alone.
4. Discuss the theoretical implications of pool reuse or provide empirical evidence that it does not harm convergence.

## Score and Decision

The paper presents a well-motivated, theoretically-grounded method for test-time scaling in discrete diffusion. The MTM-based formulation is clever and yields a genuine computational advantage. Empirical results are consistently positive across two modalities and multiple backbones, with insightful ablations (timestep analysis, iterations vs. particles) that go beyond simple benchmark reporting. The single major weakness is that the theoretical convergence guarantee depends on an unverified reversibility assumption — but the paper is transparent about this assumption, and the contribution is primarily empirical and methodological rather than theoretical. The minor weaknesses (no error bars, small prompt set, ambiguous 8× framing, pool reuse justification) are addressable and do not undermine the core findings. This is a strong, solid paper with a clear contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>