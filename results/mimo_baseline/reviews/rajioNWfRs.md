## Summary

This paper introduces TNT, a two-stage training paradigm for deep memory modules (e.g., Titans) that decouples training efficiency from inference performance. Stage 1 uses a hierarchical memory architecture—global memory on large chunks plus multiple parallel local memory modules with periodic state resets—enabling context parallelism for non-linear RNNs. Stage 2 fine-tunes the local modules with smaller chunk sizes to optimize inference resolution. The framework achieves up to 17× training speedup over baseline Titans while improving language modeling perplexity and common-sense reasoning accuracy at 150M scale.

## Strengths

- **Well-identified and well-structured problem formulation.** The paper clearly articulates three concrete challenges (Section 3): training inefficiency from small chunks, compression-retrieval domain mismatch, and chunksize sensitivity. Each challenge is mapped to a specific solution (hierarchical memory + resets, Q-K Projection, fine-tuning stage), giving the paper a clean narrative structure.

- **Substantial empirical speedup with quality gains.** Table 1 demonstrates that TNT (C_L={64}) reaches the target loss 17.37× faster than the best-performing Titans baseline (C=8). Crucially, this speedup comes alongside quality improvements (Table 2: TNT Stage 1 with {4,8,16,32} achieves 23.13 avg PPL vs. 25.07 for the best Titans baseline and 23.58 for vanilla Transformer). This simultaneous improvement in both speed and quality is a strong result that directly validates the core claim.

- **Clean ablation study.** Table 3 provides clear evidence for each component: removing global memory degrades PPL from 21.04→25.60, removing Q-K Projection degrades PPL from 21.04→22.01, and adding Stage 2 fine-tuning improves PPL from 21.04→20.86. The incremental benefit of adding local memory modules (23.53→20.15) is also well demonstrated.

- **Principled mechanism for breaking sequential dependencies.** The periodic state reset of local memories (Eq. 6) is an elegant solution to enable context parallelism for non-linear recurrences, which the paper correctly identifies as a long-standing challenge. This is a genuinely useful insight for the broader community working on efficient RNN training.

## Weaknesses

### Fatal
None.

### Major

- **Limited scale of evaluation undermines scalability claims.** All experiments use 150M parameter models. The paper claims TNT "removes a critical scalability barrier" and "establishes a practical foundation for developing expressive RNNs," but provides no evidence that these gains persist at 350M, 1B, or larger scales. Training dynamics, the relative benefit of hierarchical memory, and optimal chunk configurations could all change substantially at larger scales. Given that the central motivation is enabling pre-training of deep memory modules, demonstrating at least one larger-scale experiment is essential.

- **Incomplete evaluation against claimed generality.** The paper states TNT is "model-agnostic" and mentions both Titans and TTT as target architectures, but TTT results are entirely absent from the experiments. Only Titans is evaluated, which limits the ability to assess whether the hierarchical memory with resets and Q-K Projection generalize to other deep memory module designs.

- **No long-context evaluation.** Despite the paper's focus on enabling long-sequence training, there are no experiments on long-context benchmarks (e.g., RULER, BABILong, SCROLLS, or even PG-19 at very long context). The experiments use context lengths of 16k, which does not demonstrate the practical advantages for the long-sequence regime that motivates the work.

### Minor

- **Speedup claims are context-dependent.** The headline 17× speedup compares against the slowest, most accurate baseline (Titans C=8). Against the practical alternative of a Gated Transformer with FlashAttention (0.96 hrs in Table 1), TNT (1.12 hrs) is actually slower. The paper acknowledges this but frames it as a kernel engineering gap; the degree to which TNT can close this gap with a custom kernel is speculative.

- **Sensitivity to S_L (reset frequency) is not analyzed.** The segment length S_L is a critical hyperparameter that controls the tradeoff between context parallelism and information retention for local memories. The paper uses fixed values (2048, 4096) without any sensitivity analysis. Understanding how S_L affects quality vs. speed is important for practitioners.

- **Q-K Projection adds state and computation.** The projection matrix is maintained as a d×d running sum per local memory module. For large d and many local modules, this could become non-trivial. The paper does not quantify the overhead of Q-K Projection in terms of memory or FLOPs.

### Trivial
None.

## Nice-to-Haves

- An evaluation on at least one model at 350M+ parameters to demonstrate scaling behavior.
- Results with TTT as the base deep memory module to support the model-agnostic claim.
- An analysis of how S_L and the number of local modules N affect the quality-efficiency Pareto frontier.
- Wall-clock comparison showing TNT + hypothetical custom kernel vs. FlashAttention Transformers.

## Novel Insights

The observation that periodic resetting of local memory states can break sequential dependencies in non-linear recurrences, thereby enabling context parallelism without requiring specialized kernels (as in linear RNNs), is a genuinely useful insight. The combination with a global memory that retains long-range context through the reset boundaries creates a clean hierarchical decomposition. Additionally, the finding that brief fine-tuning with smaller chunks (Stage 2) can recover and even surpass the quality of models trained from scratch with those smaller chunks, at only ~5% additional compute, provides a practical recipe that could be widely adopted.

## Suggestions

- Add experiments at 350M or 1B scale, even if only on a subset of benchmarks, to substantiate scalability claims. This is the single most impactful improvement the authors can make.
- Include TTT as a base model in the evaluation to demonstrate generality.
- Add a sensitivity analysis over S_L and N to guide practitioners on hyperparameter selection.
- Quantify the memory and compute overhead of Q-K Projection explicitly.

## Score and Decision

The paper addresses a real and important problem with a well-motivated, technically sound solution. The core ideas—hierarchical memory with periodic resets and two-stage training—are clean and effective. The ablation study is thorough. However, the evaluation is limited to 150M parameters, only one base architecture (Titans), and no long-context benchmarks. These limitations prevent the paper from fully substantiating its stronger claims about scalability and generality. Within its current scope, the results are solid, but broader evaluation is needed for the claims to carry weight in advancing the field.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject