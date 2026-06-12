## Summary

This paper proposes FourierFlow, a frequency-aware flow matching framework for generative turbulence modeling that addresses two identified problems: spectral bias (generative models underrepresent high-frequency turbulent structures) and common-mode noise (attention mechanisms averaging out dynamically critical local features). The method combines a Salient Flow Attention branch, a Frequency-guided Fourier Mixing branch with adaptive fusion, and MAE-based surrogate feature alignment, demonstrating state-of-the-art performance across three turbulent flow scenarios with strong generalization under OOD, long-horizon, and noisy settings.

## Strengths

- **Well-motivated problem identification with empirical and theoretical grounding.** The paper clearly identifies spectral bias and common-mode noise as fundamental limitations of generative models for turbulence, supported by spectral analysis (Figure 1) and a formal theorem (Theorem 4.1) showing that high-frequency components are corrupted earlier during forward diffusion due to power-law spectral decay. This is a genuine and practically important problem for the PDE-solving community.

- **Comprehensive experimental evaluation across multiple dimensions.** The paper evaluates on three turbulence scenarios (compressible N-S at Mach 0.1 and 1.0, shear flow), tests generalization under five OOD configurations, performs long-horizon rollouts up to 16+ steps, and conducts systematic ablations on each component. FourierFlow achieves ~20% improvement over the second-best method on average across MSE, nRMSE, and Max_ERR metrics. The ablation studies (Figures 4-6) cleanly isolate the contribution of each component.

- **Principled dual-branch architecture with adaptive fusion.** The combination of SFA (targeting spatial saliency and common-mode suppression) with the FM branch (targeting spectral coverage) is well-motivated and the data-driven gating mechanism (Eq. 9-10) allows dynamic balance between spatial and frequency-aware features rather than fixed weighting.

## Weaknesses

### Fatal
None.

### Major

- **Individual components lack novelty; contribution is primarily combinatorial.** The Salient Flow Attention is adapted directly from Differential Attention (Ye et al., 2025), the Fourier Mixing branch uses AFNO (Guibas et al., 2021) with a frequency-dependent weighting term, and the surrogate alignment follows REPA (Yu et al., 2024) with MAE replacing DINO. While the application to turbulence is appropriate, each component is a relatively modest modification of an existing technique. The paper does not provide sufficient analysis of why this specific combination is uniquely effective for turbulence versus other possible combinations of frequency-aware and attention mechanisms.

- **Figure 7 is effectively unreadable.** The OOD generalization figure has a critical labeling error where three of the four legend entries are identically labeled "Surrogate-MSE" in different colors (blue, orange, yellow), making it impossible to determine which baseline corresponds to which curve. Since this figure supports the paper's claim about OOD generalization (Q5), a core result is undermined.

- **Marginal gains on several metrics.** On Compressible N-S (M=1.0), FourierFlow's improvements over STDiT are narrow: Max_ERR is 3.2551 vs 3.2506 (STDiT is actually better), MSE improvement is only ~15%. For Shear Flow, the improvements are similarly modest (e.g., 0.5811 vs 0.5908 MSE). The claim of "approximately 20% improvement on average" appears cherry-picked from the M=0.1 scenario where gains are much larger (~55% MSE reduction).

### Minor

- **The common-mode noise framework for turbulence is not well-grounded.** The paper borrows the concept from differential amplifiers and differential attention, defining common-mode noise as the shared component across channels. However, the connection to turbulence physics is asserted rather than demonstrated: the paper states that "attention mechanisms can be affected by noise, often attending to irrelevant contextual background" but does not provide quantitative evidence of this failure mode (e.g., attention map visualizations showing the problem) beyond the ablation showing SFA helps.

- **Theoretical analysis (Theorem 4.1) is straightforward.** The result that high-frequency components have lower SNR and are corrupted earlier follows directly from the assumption that the initial signal has power-law spectral decay and that noise is spectrally flat—both well-known properties. The contribution is primarily a formalization of known behavior rather than new insight.

- **Limited comparison to recent physics-informed methods.** The baselines are primarily from the video generation and neural operator communities. There is no comparison with physics-informed loss variants, energy-conserving architectures, or spectral regularization methods that have been proposed for related problems.

### Trivial
- The notation is occasionally inconsistent (e.g., η vs n in Eq. 8).

## Nice-to-Haves
- Visualization of attention maps from SFA versus standard self-attention on turbulent flow fields, showing how SFA suppresses common-mode patterns and highlights vortices/shear layers.
- Analysis of computational overhead introduced by the dual-branch architecture relative to single-branch baselines.
- Sensitivity analysis of the MAE masking ratio (currently fixed at 75%) on alignment quality.

## Novel Insights

The paper's genuinely novel contribution is the identification and formalization of the connection between diffusion model dynamics and spectral bias specifically in the context of turbulence modeling. While Theorem 4.1 follows from known properties, framing it as a concrete barrier for turbulence generation—and then designing both explicit (FM branch) and implicit (MAE alignment) remedies—provides a useful conceptual framework. The observation that MAE pretraining captures high-frequency features (citing Park et al., 2023) and can therefore serve as a frequency-aware teacher for generative models in fluid dynamics is an insightful design choice that connects representation learning theory to physics-informed generation.

## Suggestions

1. **Fix Figure 7 immediately.** The three "Surrogate-MSE" labels must be corrected to distinguish the different baselines; this is essential for readers to evaluate the OOD generalization claim.

2. **Add attention map visualizations.** Show qualitative examples of SFA attention distributions versus standard self-attention on turbulent fields with vortices and shear layers to concretely demonstrate common-mode noise suppression.

3. **Report wall-clock training and inference times.** The dual-branch architecture with MAE alignment and 161M parameters likely introduces significant overhead. For the turbulence modeling community where computational cost is critical, this information is important for practical adoption.

4. **Provide a more honest presentation of per-scenario results.** The "20% average improvement" claim should be disaggregated so readers can see that gains are heterogeneous across scenarios and metrics.

## Score and Decision

The paper presents a solid empirical contribution combining well-known techniques for an important application domain. The experimental evaluation is thorough and the results are generally positive, though gains are heterogeneous across scenarios. The main weakness is the combinatorial nature of the contribution—each component is a modest adaptation of existing work—and the problematic Figure 7. The theoretical contribution provides useful formalization but limited new insight. Overall, this is a competent applied paper that advances the state of the art in generative turbulence modeling, but the individual novelty and depth of contribution are below what I would expect for a strong accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>