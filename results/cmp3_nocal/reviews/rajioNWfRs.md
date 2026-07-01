## Summary

The paper introduces TNT (Two-stage Non-linear Training), a training framework for deep memory modules (e.g., Titans and TTT). TNT's core technical contributions are: (1) a hierarchical memory architecture where a global module processes large chunks for long-range context while multiple parallel local modules handle fine-grained details; (2) a periodic state reset mechanism for local memories that breaks sequential dependencies, enabling context parallelism for non-linear RNNs; and (3) a Q-K Projection mechanism that resolves a domain mismatch between memory compression (key→value) and retrieval (query→value). A two-stage procedure decouples training efficiency (large chunks, Stage 1) from inference quality (small chunks via brief fine-tuning, Stage 2). Experiments on Titans show up to 17× training speedup and modest perplexity improvements over baseline Titans.

## Strengths

- **Clear problem diagnosis (Section 3).** The paper isolates three concrete challenges: poor hardware utilization from small chunk sizes, a domain mismatch between compression and retrieval, and inference sensitivity to pre-training chunk size. Challenge 3 is well-supported by Figure 2, which shows a 550M Titans model pre-trained at C=64 degrading from 13.78 to 24.23 PPL when evaluated at mismatched chunk sizes. This is a clean, non-obvious empirical finding.

- **Periodic state reset for non-linear recurrence parallelization (Eq. 6, Section 4.1.1).** Resetting local memory states to a learned initialization at segment boundaries is a genuinely novel and simple mechanism. Parallelizing non-linear RNNs across the sequence length is a long-standing problem; most prior work requires linear state transitions or custom kernel tricks. This reset mechanism is architecture-agnostic and directly addresses the sequential dependency bottleneck.

- **Q-K Projection (Eq. 7, Section 4.1.2).** The domain mismatch insight — that memory compression trains on keys but retrieval queries with queries — is subtle but real. The proposed projection of queries onto the key subspace via a running outer-product sum is elegant and computationally cheap. The ablation (Table 3) shows a clear penalty for removing it: PPL increases from 21.04 to 22.01.

- **Clean ablation design (Table 3).** The ablation isolates the contribution of each component: hierarchical memory (adding local modules progressively), global memory (removing it hurts: 21.04→25.60 PPL), Q-K Projection (21.04→22.01), and Stage 2 fine-tuning (21.04→20.86). This is well-organized and informative.

## Weaknesses

### Major

- **Abstract claims evaluation on TTT that does not match the paper's experiments.** The abstract states: *"Evaluated on Titans and TTT models, TNT achieves a substantial acceleration in training speed."* In Section 5, the paper says *"While TNT is model-agnostic, we instantiate it with a strong deep memory model, Titans."* TTT appears only as a baseline in Table 2 (single fixed C=256, PPL 27.62). There are zero experiments applying TNT (hierarchical memory, periodic resets, Q-K projection, two-stage training) to TTT models. This discrepancy between what the abstract advertises and what the experiments deliver undermines the paper's framing of TNT as a "general training paradigm applicable to any deep memory module." If the paper intends to claim generality, demonstrating the framework on at least one additional architecture is needed; otherwise the abstract and framing should be corrected.

### Minor

- **Parameter capacity is not accounted for in comparisons.** The paper states "150M parameter models" for both TNT and baselines (Table 2). This count likely refers to slow weights (θ) only. However, TNT with N local modules uses N+1 memory sub-networks (global V + N local W's), each with its own fast-weight parameters, compared to Titans' single memory sub-network. The perplexity improvements (e.g., 25.07→23.13) may partly reflect additional capacity from more memory modules rather than the training method alone. The ablation (Table 3) partially addresses this by progressively adding modules, but the paper should explicitly state what is and isn't counted in the "150M" figure for both TNT and baselines.

- **Stage 2 fine-tuning gains are marginal.** The best Stage 2 perplexity (23.09) improves only 0.04 over the best Stage 1 (23.13). For the single-module case, the improvement is 0.18 (21.04→20.86). While consistent across configurations, this is a modest gain for a mechanism presented as solving "Challenge 3" (inference chunk-size sensitivity). The paper should calibrate its claims about Stage 2's impact, especially since Stage 2 models use *different* chunk configurations from Stage 1 models ({2,4,8,16} vs. {4,8,16,32}), making it not a clean before/after comparison of fine-tuning on the same base model.

- **No analysis of segment length (S_L) tradeoffs.** The periodic reset uses S_L=2048 for efficiency benchmarks and S_L=4096 for performance benchmarks, with no ablation or discussion of how S_L affects the tradeoff between parallelization and information retention. This is a meaningful design parameter that merits analysis.

- **Q-K Projection applied only locally is asserted without evidence.** The paper states *"We apply projection only locally as its fine-grained nature makes it more sensitive to the mismatch"* but provides no ablation comparing "projection on both," "projection on global only," or "projection on local only." This claim needs experimental support.

- **Overstated positioning against Transformers.** The paper describes TNT as *"stand[ing] as a strong alternative to standard Transformers"* but the best TNT model (23.09 PPL) is worse than the Gated Transformer (22.39 PPL), and the accuracy edge (40.9% vs. 39.7%) is small and within plausible noise for 150M models. This framing overstates the result.

### Trivial

None.

## Nice-to-Haves

- A demonstration of TNT on a second deep-memory architecture (e.g., TTT) would validate the generality claim. If this is impractical, the paper should be reframed as architecture-specific.
- An ablation varying S_L (e.g., 1024, 2048, 4096, 8192) to show the parallelization-vs.-retention tradeoff would strengthen the analysis.
- A cleaner Stage 2 evaluation: take a specific Stage 1 model (e.g., {4,8,16,32}), fine-tune it with {1} directly, and report the before/after delta.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **17× speedup framing concern** (Critical Issue 4 from original review): The paper states "up to 17× faster than the most accurate baseline configuration." Table 1 fully discloses all configurations and timings. The language is accurate — "most accurate baseline" refers to Titans C=8 (PPL 25.07), and the data for TNT C_L={64} vs. Titans C=8 gives 17.37×. This is transparent reporting, not a weakness. The paper also reports apples-to-apples comparisons (7.68× at C_L=C=8). Removed.
- **Figure 4 flat runtime observation**: Not a weakness. The paper's fixed-token-count experimental design explains the flat profile. Removed.
- **"TNT blends architectural innovation with training innovation" characterization**: The paper explicitly calls it a "training framework" and acknowledges architectural components ("hierarchical memory architecture"). The categorization is not a flaw. Removed as a duplication of the parameter-count concern, which is kept separately.

## Novel Insights

The reviews do not surface any genuinely novel observational insight beyond the paper's own contributions. The key insight that the periodic reset mechanism enables context parallelism for non-linear RNNs is already the paper's central technical contribution.

## Suggestions

- Correct the abstract to reflect that TNT was evaluated on Titans (and compare against TTT as a baseline), not applied to TTT.
- Explicitly report and compare fast-weight parameter counts across TNT and baseline models, clarifying what "150M parameters" includes.
- Add an ablation for S_L and clarify the tradeoffs in choosing segment length.
- Add an ablation comparing Q-K projection on local vs. global vs. both.
- Either strengthen the Stage 2 evaluation (clean before/after on the same base model) or moderate the claims about its impact.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>