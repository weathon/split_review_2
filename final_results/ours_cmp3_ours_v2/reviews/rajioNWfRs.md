Now let me produce the final consolidated review.

## Summary

This paper introduces TNT, a two-stage training framework for deep memory modules (such as Titans). The key idea is a hierarchical memory architecture: a global memory module processes large chunks for long-range context, while multiple local memory modules with periodic state resets process fine-grained details in parallel. The periodic reset mechanism breaks sequential dependencies, enabling context parallelism for models that otherwise have non-linear recurrences. Stage 2 fine-tunes with smaller chunk sizes at minimal cost. Experiments on 150M-parameter models show up to 17× training speedup over baselines while maintaining or improving perplexity.

## Strengths

- **The core idea — periodic resets of local memory states to enable context parallelism — is novel and well-motivated.** The paper correctly identifies that sequential state dependencies in deep memory modules prevent parallel training across sequence shards. The periodic reset (Eq. 6) directly breaks this dependency, and the speedup results (Table 1, Figure 4) are substantial and convincingly demonstrated. At matching chunk sizes (C=8), TNT is already 7.68× faster than the Titans baseline.

- **The Q-K Projection (Section 4.1.2, Eq. 7) is a principled fix for the compression-retrieval domain mismatch.** The insight that compression trains the memory on keys but retrieval queries it with queries is genuine. The ablation (Table 3) confirms its importance (PPL increases from 21.04 to 22.01 without it).

- **The three challenges articulated in Section 3 clearly motivate the design.** Challenge 2 (compression-retrieval mismatch) and Challenge 3 (chunk-size sensitivity at inference) are non-trivial observations that prior work has not systematically addressed.

- **The paper is clearly written and well-structured.** The method is presented logically, figures are informative, and the distinction between the two training stages is easy to follow.

## Weaknesses

### Major

- **The claim about "quadratic growth of Titans" is contradicted by the paper's own data (Section 5.2).** The paper states: "TNT's runtime grows linearly with sequence length, in contrast to the quadratic growth of Titans and standard attention." However, Figure 4's data for Titans (C=16) shows: 2048→~400ms, 4096→~600ms (1.5×), 8192→~1000ms (1.67×), 16384→~2000ms (2×), 32768→~4000ms (2×). This is approximately *linear* scaling (doubling sequence length roughly doubles runtime), not quadratic. The paper later contradicts itself by saying "Although models like Titans are also theoretically linear." This mischaracterization should be corrected.

- **No statistical variance is reported anywhere in the paper.** No standard deviations, confidence intervals, or multiple-seed runs are provided. This is particularly problematic because: (a) the Stage 2 fine-tuning improvement is only 0.04 PPL (23.13 → 23.09), which could easily fall within noise; (b) the paper itself acknowledges downstream task accuracy "can be subject to higher variance" (Section 5.3) but provides no variance estimates for those metrics; (c) several accuracy differences in Table 2 are small (e.g., TNT 41.0% vs. Gated Transformer 39.7%).

- **The abstract over-claims evaluation on "Titans and TTT models."** TNT is only applied to the Titans architecture in the experiments. TTT (Sun et al., 2024) is used as a *baseline* (Table 2), not as a model that TNT is applied to. This factual over-claim should be corrected. The paper also describes TNT as a "general training paradigm applicable to any deep memory module" but only evaluates on one architecture.

### Minor

- **Model capacity is not perfectly controlled across comparisons.** The paper states all models have 150M parameters, but TNT allocates parameters differently (global memory + N parallel local memories) compared to Titans (single memory). The perplexity improvements in Table 2 could partly reflect more efficient parameter allocation rather than the training paradigm alone. A controlled experiment matching parameter counts specifically in the memory system (versus feedforward layers) would strengthen the analysis.

- **The ablation baseline in Table 3 uses a weaker Titans configuration.** The "Base Model (Titans)" shows PPL 23.53, which corresponds to Titans with C=256 in Table 2. However, the best Titans model in Table 2 uses C=8 and achieves PPL 22.25. The improvement from 23.53 to 21.04 (TNT +1 local) partly reflects starting from a suboptimal baseline. A comparison against the best Titans configuration (C=8) would show a smaller gap.

- **The Q-K Projection's computational and memory overhead is not analyzed.** The paper mentions the projection matrix is "constant-size" and updated efficiently but provides no analysis of its FLOPs or memory cost relative to the base memory module. Since the projection involves maintaining a d×d matrix per chunk, this overhead should be quantified.

### Trivial

- Several minor presentation issues such as the paper claiming "quadratic growth" when the data shows linear scaling for Titans (noted above under Major).

## Nice-to-Haves

- A comparison against the concurrent work cited (Zhang et al., 2025), which the paper notes as addressing similar parallelization challenges, would strengthen the positioning.
- The Stage 2 fine-tuning procedure would benefit from more detail: number of steps, learning rate schedule, and whether the chunk size is annealed or switched abruptly.
- The shared learned state W_init (Eq. 6) is introduced but never ablated — what happens if it is fixed to zeros or randomly initialized?

## Removed Points

- **"TNT is an architectural modification, not a training paradigm"** — This criticism is partially semantic and overstates the problem. Many ML innovations combine architectural and training changes. The paper does introduce architectural modifications, but the core novelty (periodic resets for parallelism) is a training-enabling mechanism. The critic's claim that the speedup comparison is "not controlled" because TNT adds architectural components is noted but weakened by the fact that Table 1 does compare matched chunk sizes (C_L={8} vs. Titans C=8 gives 7.68×), and the paper is clear about the architectural differences.

- **"The fine-tuning improvement is presented as a contribution but is negligible"** — While the 0.04 PPL improvement is small, it is consistent across all four local-memory configurations in Table 2. The paper is transparent about the magnitude and presents it as "consistent improvement." This is kept as a minor weakness (lack of variance estimates) rather than a major one.

- **Section-by-section nitpicks about Eq. 5 sequential dependency, W_init ablation, and denominator simplification** — These are detail-level questions appropriate for a discussion but do not rise to the level of weaknesses that affect the paper's overall assessment.

- **"No comparison to Zhang et al. (2025)"** — This is a reasonable suggestion but the paper acknowledges this as concurrent work and notes it combines large chunks with local attention (a different approach). Not a weakness of the presented work.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the "quadratic growth" characterization of Titans in Section 5.2 to match the data (which shows linear scaling).
2. Add variance estimates (at least 2–3 seeds) for the key comparisons in Tables 2 and 3.
3. Clarify in the abstract and conclusion that TNT is evaluated on Titans specifically, and note that application to other deep memory modules (e.g., TTT) is future work.
4. Add a brief analysis of the Q-K Projection's computational cost (FLOPs and memory) to Section 4.1.2.
5. Include the Stage 2 fine-tuning hyperparameters (number of steps, learning rate) for reproducibility.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>