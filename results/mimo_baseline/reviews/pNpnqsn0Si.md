## Summary

This paper introduces Thoughtbubbles, a transformer architecture variant that learns to dynamically fork or delete residual streams during pretraining using only standard language modeling loss. Tokens requiring more computation form "bubbles" of cloned latent residuals controlled by learned cumulative scores, enabling unsupervised parallel adaptive computation without any additional supervision signal. The approach consistently outperforms both parameter-matched standard transformers and computation-matched copy-based baselines in perplexity and most zero-shot evaluations across 150M–772M parameter scales.

## Strengths

- **Genuinely novel architectural contribution.** The forking mechanism—where cumulative scores drive top-k decisions to create or delete residual streams—is a creative approach to latent adaptive computation that requires no extra supervision, supervision labels, or manually placed thinking tokens. This is a meaningful advance over pause token approaches that require predetermined insertion positions.

- **Consistent, meaningful improvements across scales and datasets.** Perplexity improvements are consistent: at 772M on OpenWebText, Thoughtbubbles (κ=4L) achieves 19.74 vs. 21.22 baseline, and the 319M Thoughtbubbles model outperforms the 772M baseline (20.23 vs. 21.22), suggesting favorable scaling properties. LAMBADA improvements are substantial (23.9→29.4 at 772M on OpenWebText).

- **Rigorous baseline design with both parameter-matched and computation-matched comparisons.** The paper includes a standard GPT-2 baseline (parameter-matched) and copy-3/copy-5 baselines (computation-matched). This is important because the forking mechanism increases the effective sequence length and thus FLOPs, so demonstrating gains over computation-matched baselines isolates the value of *adaptive* vs. *naive* additional computation.

- **Interpretable computation allocation analysis.** Figures 4 and 5 provide compelling evidence that the model learns meaningful forking behavior: forked tokens attend heavily to their parents, and more computation is allocated to tokens with moderate-to-high entropy. The concave relationship between entropy and fork allocation (less forking at the very highest entropy) is an interesting empirical finding that invites further investigation.

## Weaknesses

### Fatal
None.

### Major

- **Limited experimental scale undermines generalizability claims.** All experiments are at 150M–772M parameters with only 2.5B training tokens. The paper acknowledges the model cannot be meaningfully evaluated on harder reasoning benchmarks (e.g., GSM8k) at this scale. Given that the primary motivation is enabling adaptive computation for complex multi-step problems, demonstrating value only on relatively easy zero-shot benchmarks weakens the central argument. The paper's claim that this approach "paves the way to unify train-time and test-time scaling behaviors" is aspirational without evidence at meaningful scale.

- **Mixed results on some benchmarks reduce confidence.** On BLiMP (syntax understanding), Thoughtbubbles sometimes underperforms computation-matched baselines, and PIQA results are inconsistent. The paper explains BLiMP by suggesting "pruned dynamic parallel computation may not be as helpful for syntax matches," but this is a post-hoc rationalization rather than an explanation supported by evidence. The PIQA weakness is attributed to short training, but this applies to all methods equally.

- **Incomplete FLOPs analysis.** The paper states κ=4L is "roughly FLOPs-matched against copy-5 baseline," but doesn't provide detailed FLOPs counting. The dynamic nature of forking (variable sequence lengths per layer, top-k operations, score computation) makes precise comparison non-trivial. A rigorous FLOPs-per-token accounting would strengthen the computation-matched comparison significantly.

### Minor

- **Top-k gradient bottleneck limits scalability.** The paper acknowledges that hard top-k decisions create zero-gradient regions for dropped tokens. This could become more problematic at larger scales with more forking layers. The suggestion of training-time randomization is mentioned but not explored.

- **Fixed forking layer placement.** Forking layers are placed at positions 3, 7, 11 for all model sizes, meaning larger models with more layers have forking concentrated in early-mid layers. The paper doesn't explore whether this is optimal or whether forking in deeper layers would help.

- **Wall-clock efficiency.** The raw PyTorch implementation is acknowledged to be slow. While this is an engineering rather than scientific concern, practical deployability would benefit from at least rough timing comparisons showing the efficiency characteristics of the approach.

## Nice-to-Haves

- Experiments at 1B+ parameter scale to evaluate whether improvements hold and compound
- Analysis of what linguistic patterns receive more forks (e.g., do ambiguous words, complex clauses, or rare tokens get forked more?)
- Ablation on the number and placement of forking layers
- Comparison against more adaptive baselines (e.g., Universal Transformers, mixture-of-depths approaches)

## Novel Insights

The concave relationship between token entropy and fork allocation (Figure 5) is a genuinely interesting finding: the model allocates the most additional computation to tokens with *moderate* uncertainty rather than the highest-entropy tokens. The authors' hypothesis—that highest-entropy tokens often arise at clause boundaries or coreferences where extra compute is less helpful, while moderate-entropy tokens represent genuine disambiguation points—connects to recent work on the informativeness of high-entropy tokens (Wang et al., 2025) and suggests a nuanced view of where adaptive computation is most valuable.

## Suggestions

- Add a table with detailed FLOPs counts per forward pass for each method at each scale
- Include an ablation on forking layer placement (e.g., evenly distributed vs. concentrated early vs. concentrated late)
- Show a qualitative example of fork allocation on a specific passage to illustrate the model's behavior intuitively
- Consider a 1B+ scale experiment if compute permits, even with fewer evaluations

## Score and Decision

The paper presents a genuinely novel architectural idea—unsupervised latent adaptive computation via learned residual stream forking—that addresses an important research question. The experiments are well-designed with appropriate baselines and the results are consistently positive. However, the limited scale of experiments (150M–772M, 2.5B tokens), mixed results on some benchmarks, and incomplete FLOPs accounting prevent full confidence in the approach's broader impact. This is a solid contribution with a promising direction that would benefit from scaling up.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept