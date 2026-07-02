## Summary

The paper introduces a *noise-to-process (N2P)* paradigm for stochastic process modeling from a single trajectory. The core idea is to learn a single measurable generator that maps a shared base-noise process to an entire trajectory, ensuring projective consistency by design. The paradigm is instantiated with a deconvolution-based architecture (DBPT) that captures inter-temporal dependencies. Empirical evaluations on synthetic data, time series, image completion, and black-box optimization show competitive performance against several prior-driven and data-driven baselines.

## Strengths

- **Conceptually novel paradigm**: The N2P framework—using a shared base-noise process and a single generator to produce the full trajectory—is a clean and principled way to internalize projective consistency without strong structural priors. This addresses an important gap in single-trajectory stochastic process modeling.
- **Relevant problem setting**: Many real-world applications (e.g., expensive simulations, financial time series) yield only a single noisy trajectory. The paper targets this regime and demonstrates that DBPT can be effective where prior-driven methods suffer from misspecification and data-driven methods require multi-trajectory supervision.
- **Competitive empirical results**: DBPT achieves strong performance across diverse tasks, particularly in image completion (PSNR/SSIM) and black-box optimization (convergence speed), often outperforming baselines like GP, WGP, Markov, DKL, and CNP.

## Weaknesses

### Fatal
None.

### Major

1. **Unclear and potentially flawed NLL computation**: The NLL values in Table 1 (e.g., 602 for WGP on BIA) are orders of magnitude larger than typical values for normalized data. The paper does not specify how the likelihood is computed (e.g., whether data is normalized, what noise model is assumed, or how predictive variance is obtained). This casts serious doubt on the reliability of the time-series results and the conclusions drawn from them.

2. **Limited and uncompetitive baselines**: For time series, the paper omits modern methods such as deep state-space models, Transformers, or recurrent neural networks that can be adapted to single-trajectory settings. For image completion, specialized inpainting methods (e.g., partial convolutions, diffusion models) are not compared. The claim that DBPT is a general stochastic process model is weakened by the absence of strong, task-specific baselines.

3. **Overstated theoretical novelty**: The projective consistency result (Proposition 3) is a trivial consequence of the pushforward construction and holds for any stochastic process by definition. The Kolmogorov extension compatibility (Corollary 13) is also straightforward. The paper presents these as core contributions, but they do not provide deep theoretical insight beyond the basic definition.

4. **Insufficient ablation and analysis**: The only ablation varies the output-space grid resolution. There is no study of the noise encoder architecture, number of deconvolution layers, training loss variants, or sensitivity to the number of observed points. This makes it difficult to understand which components are critical to DBPT’s performance.

5. **No discussion of computational cost or scalability**: The paper does not report training time, inference time, or how DBPT scales with trajectory length. Given that deconvolution layers are used, this is an important practical consideration, especially for long sequences.

### Minor

- The term “weak-prior” is not clearly defined. DBPT still imposes inductive biases through its convolutional architecture and upsampling design. The paper should clarify what “weak” means in this context.
- The synthetic experiments use only two observations (positions 10 and 20). The paper does not systematically study how DBPT performs with varying numbers of observed points, which is central to the single-trajectory claim.
- The paper does not discuss failure cases or limitations of DBPT (e.g., when the trajectory is very short, highly non-stationary, or has irregular sampling).
- The writing could be clearer: the definition of projective consistency in the main text is somewhat confusing, and the phrase “once-for-all and index-agnostic” is not fully explained.

### Trivial

- Figure 1 caption is repeated in the text.
- Some references are incomplete due to parser artifacts (ignored per instructions).

## Nice-to-Haves

- Include a comparison with a simple baseline like a Gaussian process with a learned kernel (e.g., DKL) on all tasks for consistency.
- Provide uncertainty calibration metrics (e.g., reliability diagrams, coverage of confidence intervals) to support the claim of “calibrated uncertainty.”
- Discuss the relationship to deep generative models for sequences (e.g., WaveNet, time-series GANs) more thoroughly, as they also learn to generate trajectories from noise.

## Novel Insights

None beyond the paper’s own contributions. The core insight—that a shared noise process and a single generator can enforce projective consistency—is a useful conceptual framing, but it is not developed into a deeper theoretical or algorithmic principle beyond the basic construction.

## Suggestions

1. **Clarify and validate the NLL computation**: Normalize the data, specify the likelihood model (e.g., Gaussian with learned variance), and report NLL on a held-out test set. Provide a sanity check (e.g., compare to a simple baseline like a constant-variance Gaussian).
2. **Add stronger baselines**: For time series, include a simple LSTM or a linear state-space model. For image completion, include a modern inpainting method (e.g., partial convolutions or a lightweight diffusion model). This would strengthen the claim that DBPT is competitive in these domains.
3. **Expand ablation studies**: Vary the noise encoder architecture, number of deconvolution layers, and training loss (e.g., add a KL divergence term). Study sensitivity to the number of observed points and the length of the trajectory.
4. **Report computational cost**: Provide training time, inference time, and parameter counts. Discuss scalability to long sequences.
5. **Define “weak-prior” explicitly**: State what assumptions are made (e.g., only that the process is a pushforward of i.i.d. noise through a smooth generator) and what assumptions are avoided (e.g., stationarity, Markov property, specific kernel families).
6. **Include uncertainty calibration analysis**: Show coverage of 95% confidence intervals or probability integral transform (PIT) histograms to support the claim of reliable uncertainty quantification.

## Score and Decision

**Score**: 4.0  
**Decision**: Reject

The paper presents a conceptually interesting paradigm and shows promising results on several tasks. However, the major weaknesses—particularly the unclear NLL computation, limited baselines, insufficient ablation, and overstated theoretical novelty—prevent it from meeting the bar for acceptance at ICLR. With substantial revisions and additional experiments, the work could become a stronger contribution.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>