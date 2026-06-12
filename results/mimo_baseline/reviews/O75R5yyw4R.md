## Summary
This paper introduces IterRef, a test-time scaling method for discrete diffusion models that applies iterative noising-denoising refinement within a Multiple-Try Metropolis (MTM) framework to progressively align intermediate states with a reward function. The method is evaluated across text generation (MDLM, LLaDA-8B) and image generation (MaskGIT) with multiple reward functions, demonstrating consistent improvements over existing reward-guided diffusion baselines, particularly under low compute budgets.

## Strengths
- **Well-motivated and timely problem.** Test-time scaling for discrete diffusion is genuinely underexplored compared to autoregressive and continuous diffusion settings. The paper clearly identifies the unique challenges (token discretization preventing gradient use, irreversibility of generated tokens) and provides a principled response.
- **Clean theoretical framing.** The adoption of MTM with a specifically designed noising-denoising transition kernel and balancing function is well-motivated. The derivation yields elegant closed-form expressions for importance weights (uniform) and acceptance rate (reward-difference-based), and Proposition 1 provides a convergence guarantee. The theoretical contribution is substantive rather than decorative.
- **Comprehensive empirical evaluation.** Experiments span two language model backbones (MDLM, LLaDA-8B) and one image model (MaskGIT), with four language reward functions (Toxicity, Sentiment, CoLA, Perplexity) and CLIPScore for images. The consistent improvements across all settings, especially the strong performance at low NFE budgets (e.g., matching FK at 32T NFEs with only 4T NFEs on Toxicity with MDLM), are compelling.
- **Insightful analysis.** The ablation studies on effective timesteps (Table 2) and the k-vs-N tradeoff (Table 3) provide genuinely useful insights. The finding that later denoising stages are more important for discrete diffusion guidance—contrasting with continuous diffusion where early steps dominate—is a valuable empirical observation. The result that increasing iterations k is more effective than increasing particles N further validates the iterative refinement philosophy.

## Weaknesses
### Fatal
None.

### Major
- **Missing recent baselines.** The related work section discusses several recent methods—DSearch (Li et al., 2025), DTS (Jain et al., 2025), and PG-DLM (Dang et al., 2025)—that are not included in the experimental comparison. Given that these methods address the same problem (reward-guided generation for discrete diffusion) and some use sophisticated search-based approaches, their absence weakens the empirical claims about IterRef's superiority. The paper should either include these baselines or provide a clear justification for their omission.
- **NFE comparison methodology.** The paper acknowledges in Section 3.3 that treating reward model and generative model calls equally in NFE counting "may obscure meaningful differences," especially since for LLaDA-8B the generative model dominates while for MDLM they are comparable. Yet the main results (Figure 2) still use a single NFE axis. This makes cross-method comparisons potentially misleading, as different methods may have different ratios of reward-to-generative model calls. A breakdown of these costs would strengthen the evaluation.

### Minor
- **Reversibility assumption in Proposition 1.** The convergence guarantee assumes that "q and p_θ form a reversible Markov kernel," which is a strong assumption. In practice, the learned denoiser p_θ is unlikely to satisfy exact reversibility with the forward noising process q. The paper does not discuss the practical implications of this assumption or how violations might affect convergence behavior.
- **Inconsistency in effective timestep results.** Table 2 shows that evenly distributed refinement is best for Toxic, Sentiment, and Perplexity, but 0.1T (late stage only) is best for CoLA. This inconsistency is noted but not explained. A brief discussion of why CoLA behaves differently would improve the analysis.
- **Limited diversity of image experiments.** The image generation evaluation uses only CLIPScore on MaskGIT with ImageNet. Including additional image reward functions or qualitative human evaluation would strengthen the cross-modality claims.

### Trivial
None.

## Nice-to-Haves
- A wall-clock time comparison (mentioned as being in Appendix C.4) presented in the main text would help practitioners assess practical utility.
- Analysis of how IterRef interacts with different reward model qualities or calibration levels.
- Discussion of failure cases or conditions under which IterRef might not help (e.g., when the base model is already well-aligned, as hinted by the CoLA/LLaDA result).

## Novel Insights
The paper's most novel insight is that iterative refinement at intermediate denoising states—rather than trajectory-level search or single-pass guidance—can be highly effective for discrete diffusion. The finding that later denoising stages are more critical for discrete diffusion guidance (contrasting with continuous diffusion) is empirically well-supported and practically useful. Additionally, the observation that increasing iteration count k is more effective than increasing particle count N reveals that the marginal value of additional proposals diminishes quickly, while iterative refinement progressively shifts the distribution—this has implications for how practitioners should allocate compute budgets.

## Suggestions
- Include DSearch, DTS, and PG-DLM as baselines, or at minimum provide a clear statement about why they were excluded (e.g., incompatible assumptions, different problem formulation).
- Decompose NFE into generative model calls and reward model calls in the main results, or provide a supplementary figure showing this breakdown.
- Add a brief discussion of the reversibility assumption's practical validity and any empirical evidence for or against it.

## Score and Decision
The paper presents a well-motivated method with solid theoretical grounding, comprehensive experiments, and strong empirical results. The core idea of applying MTM with noising-denoising transitions for iterative refinement is clean and effective. The main weaknesses are the missing recent baselines and the NFE comparison methodology, both of which are addressable. The paper makes a clear contribution to an underexplored area and provides useful insights about discrete diffusion dynamics.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>