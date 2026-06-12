## Summary

The paper proposes a framework for robotics motion planning that performs direct search over a highly compressed, discrete, causally-ordered latent token space learned by a conditional trajectory autoencoder. The key insight is that extreme compression (3 tokens × 3 dimensions) combined with soft quantization and causal ordering enables efficient greedy tree search to optimize arbitrary user-specified objective functions at test time without additional training. The method is demonstrated on the Waymo Open Motion Dataset for motion prediction, maneuver generation (turns, speed changes), and multi-agent interaction modeling.

## Strengths

- **Elegant conceptual framework.** The paper draws a compelling parallel between advances in image tokenization (where extreme compression enables training-free generation) and robotics, proposing that highly compressed trajectory representations can serve as a bridge between learned priors and classical objective-based planning. This is a genuinely novel and well-motivated idea.

- **Effective compression pipeline.** The combination of adaptive soft quantization (noise injection with a schedule tied to reconstruction quality), causal self-attention masking, and nested dropout is technically sound and well-motivated. The adaptive noise schedule in Figure 2 clearly outperforms fixed noise, and the nested dropout enables the coarse-to-fine token structure that makes greedy search viable.

- **Greedy search outperforms the learned encoder.** Table 1 is a striking result: greedy search with quantized tokens beats the encoder that produced those tokens. This validates the paper's central thesis that the latent space is structured enough for simple search strategies.

- **Flexible test-time objectives without retraining.** The maneuver generation experiments (Table 3) convincingly demonstrate the framework's core promise: the same autoencoder can be repurposed for left turns, speed reduction, or any other objective by simply changing the search criterion. The zero/near-zero edge contact rates show the decoder acts as a learned feasibility filter.

- **Multi-agent extension.** The extension to joint multi-agent tokenization (Section 3.5) is well-designed, reusing the single-agent components and demonstrating that joint tokens capture interaction semantics. Figure 6 is particularly compelling—optimizing only the pedestrian's goal position automatically produces coordinated vehicle behavior.

- **LLM-based understanding via tokens.** Table 4 shows that feeding the frozen autoencoder's tokens into a fine-tuned LLM matches Motion-LLaVA on language metrics, suggesting the tokens encode meaningful semantic information without end-to-end fine-tuning of the encoder.

## Weaknesses

### Fatal
None.

### Major

- **Prediction performance gap.** While the paper frames the method as useful for prediction (Table 2), the results show a substantial gap to SOTA methods (e.g., minADE₆ of 0.6793 vs. DriveGPT's 0.5240, a ~30% relative gap). The paper partially acknowledges this but could be more transparent about the limitations. The variance-minimization objective is clever but the paper does not analyze why it works, which feels important for a method paper.

- **Limited ablation of design choices.** The paper does not provide sufficient ablation for key hyperparameters. For instance: why N=3, D=3 specifically? How does the choice of N_levels affect planning success rate (beyond Table 1's reconstruction metrics)? What is the effect of ADE_target? The adaptive noise schedule has multiple hyperparameters (γ, Δσ) whose sensitivity is unexplored. This makes it difficult to assess how robust the approach is to different settings.

- **Single benchmark.** All experiments are on WOMD. While this is a standard benchmark, the paper makes broad claims about applicability to robotics (manipulation, autonomous driving) but only demonstrates on one driving prediction dataset. Even a simple simulation-based manipulation experiment would significantly strengthen the contribution.

### Minor

- **Narrow scope of planning objectives.** The paper demonstrates two specific objectives (turning and speed reduction). While these are reasonable proof-of-concept experiments, more diverse or adversarial objectives (e.g., maximizing distance from other agents, combining multiple competing objectives) would more convincingly demonstrate the "arbitrary objective" claim.

- **Token semantics analysis is somewhat informal.** Section 3.1 presents qualitative evidence for token semantics (Figure 5) but lacks a quantitative analysis. How many distinct behavior clusters exist in the token space? What fraction of the test set is well-captured by a small token library? A more rigorous clustering analysis would strengthen the interpretability claims.

- **Multi-agent search limited to qualitative results.** The multi-agent interaction generation (Figure 6) is presented with only a single example, and the multi-agent ADE results (Table 5, referenced but shown in-text) use different hyperparameters than the single-agent case. A more systematic evaluation of multi-agent planning objectives would be valuable.

### Trivial
- The paper references "Table 5" for multi-agent reconstruction results in Section 3.5 but the table content is not fully detailed in the visible text.

## Nice-to-Haves

- A comparison with continuous latent space optimization (e.g., gradient-based search in the same autoencoder's bottleneck) would help quantify the benefit of discrete/casual structure.
- Analysis of failure cases: when does greedy search fail to find a valid solution, and could beam search or more sophisticated search strategies help?
- Discussion of how the framework handles real-time constraints in actual robotics deployment.

## Novel Insights

The central observation that extreme trajectory compression creates a latent space where greedy token search suffices for both reconstruction and arbitrary objective optimization is genuinely novel, particularly the connection drawn to recent findings in image tokenization (Lao Beyer et al., 2025). The finding that learned encoder outputs can be surpassed by search in the same space (Table 1) suggests that the autoencoder's training procedure learns a latent structure that is richer than what the encoder alone can exploit—a surprising and interesting finding. The multi-agent extension showing that joint token search with a single-agent objective produces coordinated multi-agent behavior is also a novel and practically useful observation.

## Suggestions

- Add ablation studies on N, D, N_levels, and search depth to establish robustness of the approach and guide practitioners.
- Include at least one non-driving robotics domain (even a simple one) to support the general robotics framing.
- Provide a more systematic quantitative analysis of token semantics (e.g., clustering metrics, entropy of token distributions conditioned on maneuver type).
- Discuss computational tradeoffs more carefully: the 115 trajectories/second figure is helpful but analysis of how this scales with more agents, longer horizons, or finer quantization would be valuable.

## Score and Decision

This paper presents a clean, well-motivated framework with a compelling central idea and solid experimental validation. The conceptual contribution—bridging learned priors and model-based planning via latent token search—is novel and well-executed. The main weaknesses are the limited ablations, single benchmark, and the prediction performance gap to SOTA, which prevent it from being a strong accept. However, the paper is technically sound, clearly written, and offers a framework that could seed meaningful follow-up work in the robotics and planning communities.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>