Now I have all the information I need. Let me compile the final review.

## Summary

This paper introduces IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transition kernels to iteratively refine intermediate states during sampling. The method addresses a genuine limitation of existing reward-guided approaches for discrete diffusion — their inability to correct misaligned intermediate states once generated. The paper provides a theoretical convergence guarantee (Proposition 1) under the assumption of reversibility, and presents empirical results across two language diffusion models (MDLM, LLaDA-8B) and one image diffusion model (MaskGIT) with multiple reward functions, consistently showing improvements over baselines.

## Strengths

- **Principled integration of MCMC into discrete diffusion sampling.** The paper identifies a genuine limitation of existing reward-guided methods for discrete diffusion — they cannot correct misaligned intermediate states — and addresses it by framing iterative refinement within the Multiple-Try Metropolis (MTM) framework. The specific design of the transition kernel and balancing function (Eq. 2) that yields the simple acceptance probability in Eq. 3 is clever and non-obvious.

- **Consistent empirical advantage across diverse settings.** The experiments cover two discrete diffusion language models (MDLM, LLaDA-8B), one discrete image diffusion model (MaskGIT), and four reward functions for language plus CLIPScore for images. The results in Figure 2 and Table 1 are consistent: IterRef outperforms or matches all baselines at almost every NFE budget on nearly every task.

- **Computational flexibility.** Unlike particle-based methods (SMC, FK) that require maintaining multiple trajectories throughout the entire denoising process, IterRef can be applied selectively at chosen timesteps via the effective set U, and computational cost can be tuned through k (iterations), N (candidates), and the density of U.

## Weaknesses

### Fatal
None.

### Major

- **Theory-practice gap in the convergence guarantee.** Proposition 1 states that the MTM chain converges to the optimal distribution p^*(x_t), where p^*(x_t) depends on the intermediate reward r(x_t) = α log E_{x_0~p_θ(·|x_t)}[exp(r(x_0)/α)]. However, the practical algorithm (line 117) replaces this expectation with a single-sample approximation by evaluating the reward on the diffusion model's prediction of x_0. The paper offers no analysis of what this approximation does to the stationary distribution or the convergence guarantee. The theoretical claim in Proposition 1 therefore applies to an idealized version of the algorithm, not the one actually evaluated. This is a significant gap between the paper's theoretical framing and its practical instantiation.

- **No measures of variance or statistical significance.** Every quantitative result (Figure 2, Table 1, Table 2, Table 3, Figure 5a) is reported as a single number with no error bars, standard deviations, or confidence intervals. The language experiments use 15 prompts × 20 samples = 300 generations with 3 seed conditions. Without variance estimates, the reader cannot assess whether IterRef's advantage over baselines is large relative to the noise or whether it varies substantially across prompts. Given the paper's central claim of "striking gains" and "8× faster" scaling, the absence of any uncertainty quantification is a significant evidential gap.

### Minor

- **The critical assumption underlying Proposition 1 — that q and p_θ form a reversible Markov kernel — is stated without discussion.** For absorbing-state discrete diffusion, the forward process q is a fixed masking process and p_θ is learned. Exact reversibility is not guaranteed for a learned model. The paper should at minimum discuss when this assumption holds approximately and what happens when it does not.

- **The hyperparameter configuration (k, N, U) used for the main results in Figure 2 and Table 1 is not specified.** Algorithm 2 lists k, N, and U as key hyperparameters, and the analysis sections (Section 4.4, Tables 2-3) explore these, but the primary experimental results are presented without stating which values produced them. This makes it difficult to reproduce the main claims.

- **The detoxification qualitative examples (Figure 5b) show the method reducing toxicity by changing the semantic content entirely** (e.g., toxic prompt → song lyrics about Trinidad). The paper notes this behavior ("completing sentences as if they were quoted speech from someone else") but does not critically assess it as a limitation — this is topic drift rather than genuine detoxification of the intended content.

- **No dedicated limitations section.** The paper does not explicitly discuss its limitations despite several that are apparent (the theory-practice gap, the reversibility assumption, the topic drift in detoxification).

### Trivial
None.

## Nice-to-Haves
- Adding error bars (at minimum over seeds) would greatly strengthen the empirical claims.
- An explicit analysis of how the single-sample approximation of r(x_t) affects the stationary distribution of the MTM chain would close the theory-practice gap.
- Wall-clock time comparisons (referenced as Appendix C.4) would help validate that NFE-based comparisons are meaningful.
- Discussing the reversibility assumption's practical validity and implications would strengthen the theoretical framing.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Parentheses typo in Eq. 3**: The critic noted unbalanced parentheses in β = min(1, exp((r(x_t') - r(x_t)/α))). This is a formatting artifact from PDF extraction; the original submission does not have this issue. Per hard rules, removed.
- **Algorithm 2 indentation ambiguity**: The critic questioned whether the denoising step (Line 10) is inside the refinement loop. The paper's text explicitly states "After completing the k refinements, we proceed with a one-step denoising update" — the indentation in the extracted text is a parser artifact. Removed.
- **Missing appendix content (wall-clock time analysis)**: The critic referenced Appendix C.4 being unavailable. Per hard rules, weaknesses about missing appendix content are removed.
- **Claim about "existing methods assume the current state is already aligned"**: The critic called this framing adversarial. This is an accurate characterization of how prior methods work (they advance without correcting current states), not a factual error. Removed.
- **Speculative concerns about NFE cost accounting**: The critic raised an unsupported question about whether NFE counts properly account for proposals vs. auxiliary samples. Removed as speculation without evidence of an actual error.
- **SoP adaptation concern**: The critic speculated about whether SoP was fairly adapted to the discrete setting without evidence of unfairness. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
1. Add a dedicated analysis or discussion of how the single-sample approximation of r(x_t) affects the stationary distribution of the MTM chain, or clearly separate the idealized theoretical claims from the practical algorithm with appropriate caveats.
2. Report error bars or standard deviations for the main experimental results (at minimum over the 3 seeds).
3. Specify the exact (k, N, U) configuration used for each main result in Figure 2 and Table 1.
4. Add a limitations section discussing the reversibility assumption, the reward approximation gap, and the observed topic-drift behavior in safety tasks.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| pq1WUegkza.md (Convergence of Score-Based Discrete Diffusion Models) | 7.00 | R1 | Yes | Stronger theoretical paper; purely analytical with no experiments. Our paper is stronger empirically but weaker theoretically. |
| kIPEyMSdFV.md (Reverse Diffusion Monte Carlo) | 7.00 | R1 | Yes | Theoretical MCMC+diffusion paper with only 2D experiments. Our paper has much stronger empirical validation but a less ambitious theoretical contribution. |
| fXkoROek1M.md (Avoiding mode collapse in diffusion models fine-tuned with RL) | 4.00 | R1 | Yes | Weaker paper seen as having trivial method extension. Our paper has a more novel core idea and broader experiments. |
| Ombm8S40zN.md (Steering Masked Discrete Diffusion Models via DDPP) | 6.25 | R2 | Yes | Most directly comparable: both steer discrete diffusion models. DDPP had stronger presentation/significance scores (+7.02) but also a very harsh -12.43 weakness. Our paper's weighted items are comparable in magnitude. |
| 1pTlvxIfuV.md (Reparameterized Discrete Diffusion for Text) | 5.50 | R2 | No | Discrete diffusion text generation paper; not directly about test-time scaling or guidance. |
| i5MrJ6g5G1.md (Simple Controllable Uniform Discrete Diffusion) | 5.25 | R2 | No | Focused on guidance mechanisms for discrete diffusion; lower score suggests weaker empirical results. |

**Bracket (Round 1):** The paper sits between 5.5 and 7.0, most comparable to the DDPP steering paper (6.25) and above the controllable discrete diffusion paper (5.25).

**Final Score Calibration:** Comparing weighted items: my draft's strongest positive (+6.05 for principled MCMC integration) is slightly below DDPP's strongest (+7.02), but my strongest negative (-5.70 for theory-practice gap) is less extreme than DDPP's -12.43. The key distinguishing factor is the theory-practice gap in Proposition 1: the paper claims a convergence guarantee that does not directly apply to the practical algorithm using an approximate reward. This gap prevents the paper from reaching the 6.5+ range despite its broad and consistent empirical results. The missing variance estimates further reduce confidence. However, the core methodological contribution is substantial, and the empirical wins are consistent across modalities. This places the paper at the lower end of borderline accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>