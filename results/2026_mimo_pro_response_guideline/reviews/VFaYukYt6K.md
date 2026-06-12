## Summary
This paper proposes a framework for motion planning by performing greedy discrete search over the latent tokens of a highly compressed, causally-ordered, environment-conditioned trajectory autoencoder. The autoencoder uses adaptive soft quantization (noise injection at the bottleneck) and nested dropout to learn a discrete latent space small enough (e.g., N=3 tokens, D=3 dimensions) that greedy tree search over quantized token values is tractable. The framework is demonstrated on WOMD for motion prediction (variance minimization), planning with user-specified objectives (left turns, speed reduction), multi-agent joint trajectory generation, and interaction understanding via LLM.

## Strengths
- **Greedy token search outperforms the learned encoder for reconstruction (Table 1).** With 2 tokens and N_levels=2, greedy search achieves ADE 0.485 vs. the autoencoder's 0.519; with 1 token and N_levels=3, greedy search achieves 0.524 vs. 0.617. This is the strongest validation that the causal + noise-resilient structure enables effective discrete search.
- **Arbitrary test-time objectives can be optimized without retraining (Table 3).** The same pre-trained autoencoder achieves 75.5% success for a left-turn maneuver and 63.2% for speed reduction, with near-zero edge contact rates (0% and 0.13%), demonstrating flexible planning with learned priors.
- **Adaptive soft quantization is theoretically motivated and empirically justified (Eq. 1-2, Figure 2).** The noise injection is connected to the capacity-achieving input distribution of an amplitude-limited Gaussian channel (Smith, 1971), and Figure 2 shows it achieves lower validation ADE and more stable training than fixed noise.
- **The causally-ordered, variable-length latent structure enables principled coarse-to-fine greedy search (Section 2.2, Figure 3).** Nested dropout forces later tokens to capture progressively finer details, making token-by-token greedy selection viable.
- **Computational efficiency at test time.** With N=3, D=3, N_levels=2, greedy search requires only 24 decoder evaluations (vs. 512 for exhaustive search), generating ~115 trajectories/second on a single GPU (Section 3.4).
- **Multi-agent extension naturally produces coherent joint behavior from single-agent goal specifications (Figure 6).** When a terminal goal is imposed on one pedestrian, the joint decoder automatically adjusts vehicle behavior accordingly.

## Weaknesses

### Fatal
None.

### Major
- **No comparison to trajectory optimization baselines for planning tasks.** The introduction explicitly positions trajectory optimization as the competing paradigm ("motion planning has traditionally relied heavily on a classical toolbox including, for example, trajectory optimization"), and the core claim is that the deep prior combined with search offers advantages over classical methods. Yet the planning experiments (Section 3.4) compare only against the "no search" baseline (original scenario). Even a simple trajectory optimizer (e.g., CEM or MPPI operating directly in trajectory space) on the same objectives would validate whether the learned decoder prior contributes beyond what the objective function alone provides. The zero edge contact rate suggests the prior matters, but this is not conclusive without a direct comparison.

- **Multi-agent and LLM experiments lack sufficient quantitative rigor.** Table 4 reports only generic language generation metrics (ROUGE-L, BLEU, METEOR, CIDEr, SPICE) on WOMD-Reasoning rather than challenge-specific metrics (e.g., grounding accuracy, planning accuracy) the benchmark is designed for. Additionally, Motion-LLaVA is based on LLaVA-v1.5-7B while the proposed method uses Qwen3-4B — a different model family and size — making the comparison less informative. The interaction generation experiment (Figure 6) is qualitative only with no quantitative metrics (e.g., collision rate, feasibility rate, diversity).

### Minor
- **Variance minimization as a prediction proxy is empirically effective but weakly motivated.** Section 3.3 minimizes the variance of the final predicted point; Table 2 shows this works (minADE₆ 0.6793), but limited analysis of when this proxy succeeds or fails is provided. A mode-seeking decoder could assign low variance to a single wrong mode. The random-objective ablation (last row of Table 2) validates that variance-based selection matters, but failure case analysis would help readers understand appropriate use cases.

- **Limited ablation on compression hyperparameters.** The paper uses N=3, D=3, N_levels=2 for planning and N=1, D=3 for prediction. Table 1 only ablates reconstruction performance. Understanding how planning success rate and prediction quality scale with these parameters would strengthen practitioner guidance.

### Trivial
None.

## Nice-to-Haves
- Report standard errors or confidence intervals for success rates in Table 3 (aggregated over ~300-800 scenarios).
- Discuss planning failure cases: is it because the decoder cannot represent the desired behavior, or because greedy search gets stuck in local optima?
- Ablation on how planning success rate varies with N, D, and N_levels.

## Removed Points
These points are flagged to be removed, treat them with caution.
- No points removed from the harsh critic — all major concerns verified against the paper and found valid.
- All eight strengths from the strength finder are grounded in specific evidence (tables, figures, equations) from the paper; none removed.

## Novel Insights
The paper's genuinely novel insight is that extreme compression of trajectory representations (N=3 tokens, D=3 dimensions) combined with causal ordering and noise-resilient training creates a latent space where simple greedy search can both replace the learned encoder and optimize arbitrary test-time objectives. This draws a creative connection between recent image tokenization work (Lao Beyer et al., 2025) and robotics planning, and is validated by Table 1 (greedy search outperforming the learned encoder) and Table 3 (successful planning with user-specified objectives without retraining).

## Suggestions
- Add comparison to at least one classical trajectory optimizer (CEM, MPPI) on the same planning objectives to directly validate the value of the learned prior.
- Report WOMD-Reasoning challenge-specific metrics in Table 4, or explain why only language generation metrics are appropriate.
- Add quantitative evaluation for multi-agent interaction generation (collision rate, feasibility rate).
- Analyze planning failure cases to understand when and why token search fails.

---

## Calibration Report

### Anchors Retrieved

**Round 1 (bracketing):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR (KL GFlowNets) | 1.00 | 1 | Much weaker; fundamental issues |
| gwZ90hFSL2 (Humanoid cross-lingual) | 1.00 | 1 | Much weaker; irrelevant |
| P49gSPmrvN (UMAP discourse) | 1.00 | 1 | Much weaker; rejected |
| 5lUdTogEL3 (Lifelong ReID) | 1.00 | 1 | Much weaker; rejected |
| k1qVBh5fnb (Latent Diffusion Planning) | 3.40 | 1 | Similar ideas but poor experimental support |
| OZ3NXrF3gQ (Reward-free PO) | 2.50 | 1 | Overly ambitious claims |
| 58KF6ne6d4 (KIRL trajectory) | 3.00 | 1 | Narrow CNC domain |
| q1Cv7Hp52y (Skills to Plans) | 3.00 | 1 | Limited environments |
| NlBuWEJCug (PcLast) | 4.50 | 1 | Limited to simple 2D/3D environments |
| XLCqhdaMpy (Latent Weight Diffusion) | 4.50 | 1 | Similar idea, rejected for limited scope |
| 1uHTIjXjkk (Potential-Based Diffusion) | 4.00 | 1 | Fails to justify core claims |
| MtCcVO8Oux (Agile Flight) | 4.50 | 1 | Limited to quadrotor domain |
| LYG6tBlEX0 (H-GAP) | 7.33 | 1 | Stronger; VQ-VAE + MPC with actual MPC baselines |
| pQsllTesiE (L-MAP) | 7.33 | 1 | Stronger; MCTS over VQ-VAE with comprehensive baselines |
| TOiageVNru (Physics-informed motion) | 6.00 | 1 | Comparable; solid but incremental |
| MxALfOAnXv (CpAE) | 6.50 | 1 | Comparable; clean autoencoder contribution |
| DzGe40glxs (Interpreting Planning) | 8.00 | 1 | Stronger; more rigorous analysis |
| 7BLXhmWvwF (Geometry-aware RL) | 8.00 | 1 | Stronger; comprehensive benchmark |
| 9pW2J49flQ (DeepLTL) | 8.00 | 1 | Stronger; comprehensive |
| KsUh8MMFKQ (Thin-Shell) | 8.00 | 1 | Stronger; comprehensive |

**Round 2 (narrowing):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 8ROIRnKloJ (ε-VAE) | 5.67 | 2 | Weaker; mixed scores, rejected |
| mb2ryuZ3wz (How many tokens) | 5.75 | 2 | Comparable variable-length tokenization |
| 8ishA3LxN8 (FSQ) | 6.50 | 2 | Comparable; clean VQ alternative with broader experiments |
| ZlQRiFmq7Y (VDR) | 6.67 | 2 | Comparable; NLP-supervised representations |
| mDIXfHvoqH (ITPNet) | 6.75 | 2 | Comparable trajectory prediction paper |
| UapxTvxB3N (Trajectory-LLM) | 5.75 | 2 | Weaker contribution |
| Bmzv2Gch9v (SmartPretrain) | 6.75 | 2 | Comparable; representation learning for prediction |
| DydCqKa6AH (PedGen) | 6.75 | 2 | Comparable; pedestrian generation |

### Bracket and Narrowing
- **Round 1 bracket:** 6.0–7.0. The paper is clearly above the 4.0–4.5 rejected robotics/planning papers (weaker validation, less novel cores). Comparable to FSQ (6.50) and trajectory prediction papers (6.75). Below H-GAP/L-MAP (7.33) which have stronger baseline comparisons and more comprehensive experiments.
- **Round 2 narrowing:** 6.5. The core idea is more novel than most 5.5–6.0 anchors (extreme compression + greedy search for planning is genuinely new) but experiments are shallower than 6.75+ anchors (no trajectory optimization comparison, simple objectives, underdeveloped multi-agent experiments).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>