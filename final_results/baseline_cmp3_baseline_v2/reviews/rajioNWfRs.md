## Summary

The paper introduces TNT, a two-stage training framework for deep memory modules (e.g., Titans, TTT) that decouples training efficiency from inference performance. Stage 1 uses a hierarchical memory architecture—a global module processing large chunks for long-range context and multiple parallel local modules with periodic state resets to enable massive context parallelism. A Q-K projection mechanism mitigates the domain mismatch between memory compression and retrieval. Stage 2 is a lightweight fine-tuning phase that adapts local memories to smaller chunk sizes for optimal inference. Experiments on 150M-parameter Titans models show up to 17× training speedup over the most accurate baseline and improved perplexity and commonsense reasoning accuracy.

## Strengths

- **Clear identification of fundamental challenges:** The paper systematically articulates three concrete problems (training inefficiency, compression-retrieval mismatch, and chunk-size sensitivity) that have limited the practicality of deep memory modules.
- **Novel combination of mechanisms:** The periodic reset of local memory states to enable context parallelism for non-linear recurrences, combined with hierarchical memory and Q-K projection, is a practical and effective solution that goes beyond simple chunking.
- **Strong empirical validation:** The experiments demonstrate significant wall-clock speedups (up to 17×) and consistent perplexity improvements over strong baselines (Titans, TTT, DeltaNet) at the 150M scale, with comprehensive ablations confirming each design choice.

## Weaknesses

### Fatal

None.

### Major

- **Limited generality claim:** The paper asserts that TNT is “a general training paradigm applicable to any deep memory module,” yet all experiments are conducted only on the Titans architecture. Without validation on TTT, Atlas, or other deep memory models, the claim of model-agnostic generality is unsupported.
- **Baseline selection inflates speedup claims:** The headline “17× faster” compares TNT (C_L=64) to Titans with chunk size 8, which is an intentionally slow configuration. Against the more practical Titans C=256, the speedup would be far smaller. The choice of the “most accurate baseline” (C=8) for the speedup ratio is fair but should be contextualized with other comparisons.

### Minor

- **Fine-tuning Stage 2 details are sparse:** The paper states fine-tuning requires “only an additional 5% of the original pre-training compute” with a “brief” schedule, but does not report the exact number of steps, learning rate, or whether the full dataset is reused. Replication would be difficult without these details.
- **No comparison to linear memory modules:** While the paper is about deep memory modules, including a baseline like Mamba or Gated DeltaNet in the efficiency comparison would help position TNT relative to the broader efficient sequence modeling landscape.
- **Q-K projection overhead not quantified:** The projection matrix involves a d×d running sum. The paper should report the additional FLOPs or memory relative to the base memory module, especially for large d (e.g., 768 for 150M models).

### Trivial

- The acronym “TNT” is overloaded (also refers to a popular explosive and a computer graphics library), but this is not a substantive issue.

## Nice-to-Haves

- A comparison of TNT with TTT (the other major deep memory module) to substantiate the generality claim.
- An analysis of how the number of local modules N affects the trade-off between speedup and quality, beyond the four tested configurations.
- A discussion of whether the reset interval S_L (local window length) could be tuned automatically or learned.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Validate TNT on at least one additional deep memory architecture (e.g., TTT or Atlas) to support the claim of generality.
- Provide the exact number of fine-tuning steps, learning rate schedule, and dataset fraction used in Stage 2.
- Report the compute overhead (FLOPs and memory) of the Q-K projection mechanism relative to the base memory module.
- Include a speedup comparison against a more natural “fast” Titans baseline (e.g., C=128 or C=256) to give a balanced view.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>