## Summary
The paper proposes LS-Merge, a framework for model merging that operates in a learned latent space rather than raw weight space. It trains a Transformer-based VAE to encode LLM weights into compact latent representations, enables interpolation and merging in this space, and uses Optimal Transport for aligning latent distributions when merging models of different architectures or sizes. The approach addresses the fundamental limitation that existing merging methods require architecturally homogeneous models.

## Strengths
- **Genuinely novel and well-motivated approach**: Moving model merging from weight space to a learned latent space with OT-based alignment is a compelling idea that addresses a real limitation. No prior work enables principled cross-architecture merging between models of different depths/widths, so the research question itself is important.
- **Strong ablation studies**: Section 5.3 is particularly convincing—PCA collapses functional performance even at mild compression (r=1.6) while the VAE preserves near-original accuracy, demonstrating that the weight manifold is fundamentally non-linear and requires expressive encoders. The component-level ablation (Table 6) showing MLP and attention parameters encode complementary knowledge is also insightful.
- **Thorough weight statistics analysis**: Tables 1 and Figure 2 provide detailed empirical characterization of LLM weight distributions (heavy tails, high kurtosis, low-rank structure) that motivates design choices and has independent value for the community.
- **Consistent expert merging improvements**: Table 3 shows LS-Merge soup outperforms all weight-space baselines across 6 of 8 benchmarks, with gains of +3-6 MMLU points over the strongest baseline (Greedy Soup). These results are the paper's strongest empirical contribution.

## Weaknesses
### Fatal
None.

### Major
- **No training cost analysis**: The paper does not report how much compute is required to train the VAE, how many weight snapshots are needed, or how the total cost compares to alternatives (e.g., fine-tuning). This is a significant omission for a method that introduces substantial additional infrastructure before merging can even occur. Without this, it is impossible to assess practical viability.
- **Self-merging claims need stronger justification**: Table 2 shows that sampling and merging latent codes from a single model's posterior yields ~4% MMLU gains over the base model for Gemma-3-1B-it (35.13 vs 32.20). This is an extraordinary claim that could be explained by smoothing/regularization effects rather than genuine knowledge augmentation. The near-zero standard deviations (e.g., 54.20 ± 0.00) also raise questions about the experimental procedure. No comparison to compute-equivalent fine-tuning is provided.
- **Evaluation protocol inconsistency**: The paper switches between a custom evaluation subset (Tables 2, 3) and lm-eval (Tables 4, 5, 6, 7, 8) without clear justification. This makes cross-experiment comparison difficult and raises concerns about reproducibility.

### Minor
- **Limited model scale**: All experiments use models up to 13B parameters. Given that the paper claims scalability as a contribution, demonstrating on larger models (e.g., 70B) would significantly strengthen the case. The VAE itself presumably scales with model size, creating a chicken-and-egg scalability concern.
- **Mixed results against AIM**: In Table 4, LS-Merge beats AIM on MMLU and IFEval but loses on HumanEval and GSM8k. The paper claims "highly competitive" but the picture is mixed—AIM retains advantages on math and code tasks.
- **Cross-family merging gains are modest**: Table 5 shows improvements of ~1% over baseline (Winogrande 57.75 vs 56.83), and only at λ=0.1. The practical significance of cross-family merging thus remains somewhat unclear.
- **Proportional mapping formula is under-justified**: The depth/width scaling (r = n_t·N / n_s·M) is presented without theoretical or empirical justification for why proportional alignment is the right choice over alternatives.

### Trivial
- Table 1 is difficult to parse due to formatting (likely parser artifact but worth noting the presentation could be improved with clearer layer labeling).

## Nice-to-Haves
- A wall-clock compute comparison table showing VAE training cost, encoding cost, and total pipeline cost versus weight-space baselines.
- Experiments on larger models (30B+) to validate scalability claims.
- Sensitivity analysis of β in the β-VAE objective and chunk size c.
- Comparison to simply applying LoRA-style adapters to the target model as an alternative approach to cross-architecture knowledge transfer.

## Novel Insights
The demonstration that LLM weights lie on a non-linear manifold (not a linear subspace) is genuinely informative—the PCA vs. VAE ablation (Section 5.3) provides clean evidence that linear compression methods collapse functionally while non-linear encoding preserves downstream performance even at 4x compression. The finding that heavy-tailed weight distributions (kurtosis up to ~15) require encoders that preserve tail events rather than over-regularize toward Gaussians is also a useful design principle for future weight-space learning work.

## Suggestions
- Add a table reporting VAE training FLOPs, number of training snapshots, encoding time per model, and total end-to-end pipeline cost to make the method's practical value assessable.
- For self-merging, compare against (a) multiple VAE reconstructions averaged, (b) random perturbations in weight space, and (c) noise-augmented inference, to disentangle whether gains come from latent-space smoothing or genuine manifold exploration.
- Use a single consistent evaluation protocol (lm-eval) throughout all experiments for reproducibility and fair comparison.

## Score and Decision
The paper presents a genuinely novel framework for latent-space model merging with principled OT-based alignment, supported by informative ablations and consistent expert-merging improvements. However, the absence of training cost analysis, questionable self-merging claims, evaluation inconsistencies, and limited scale prevent a stronger recommendation. The core idea is strong but the evidence has meaningful gaps.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>