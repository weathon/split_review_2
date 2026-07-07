## Summary
The paper introduces Factorization Memory, a recurrent neural network architecture that maintains *m* separate memory states and selectively routes input tokens to a subset of them via affinity scores. A sparse variant activates only top-*k* states per timestep, delivering real compute savings proportional to *k/m*. The model is trained with parallel prefix scan and evaluated against Transformer and Mamba-2 baselines, showing comparable short-context performance and notably better long-context extrapolation, alongside a measured 35–40% inference speedup over Mamba-2.

---

## Strengths
- **Compelling long-context extrapolation result.** Figure 4 is striking: when trained only on 1024-token windows and tested up to 128K tokens, Factorization Memory's loss remains nearly flat while Transformer and Mamba-2 diverge sharply. This holds for both English and Japanese, and the paper validates it both through the 2048-token scaling frontier (Figure 3b) and the full long-context benchmark, providing three independently consistent lines of evidence.
- **Sparse mechanism is elegant and practically motivated.** Reusing the same affinity distribution α_t for both write and read is non-trivial: it makes sparse top-*k* routing genuinely apply to both the update and the merge, enabling provable compute and memory reduction. Figure 5 empirically shows that 25%-proportional activation matches dense performance at sufficiently large *m*, a result that would not hold if the two operations used independent routing.
- **System-level contribution with real measured speedup.** Releasing optimized CUDA/Triton kernels and measuring wall-clock inference on an H100 with 16K-token prompts gives concrete evidence that the theoretical savings translate to practice (35–40% faster than Mamba-2).
- **Systematic scaling study.** The paper trains 5 model sizes (62M–1679M) for each of three architectures, computes Pareto loss frontiers, and fits power laws. This is considerably more thorough than many RNN architecture papers.

---

## Weaknesses

### Fatal
None.

### Major
1. **No explanation for the extrapolation advantage.** The paper observes that Factorization Memory extrapolates far beyond its training context length while Transformer and Mamba-2 do not, but never offers a mechanistic explanation. Why should distributing input across *m* independent states with a learned router produce better extrapolation than a single structured state (Mamba-2)? The lack of even an informal argument leaves this as an unexplained empirical observation rather than an understood property, making it hard to judge whether it will hold at larger scales or with different data distributions.

2. **Insufficient differentiation from Gated Linear Attention (GLA).** The architecture shares substantial structure with GLA: it has learned, input-dependent gating and uses softmax-based routing. The paper describes GLA in the background as having "finer control over long-range dependencies" but never provides a precise architectural comparison. The key claimed difference—sparse routing with the *same* distribution for read/write—should be contrasted directly with GLA's formulation, and the long-context extrapolation gap should be shown to stem from this difference rather than from training details.

3. **Short-context benchmark margins are small and lack significance testing.** The English average scores (30.98 vs. 29.53 vs. 29.06) differ by ≤1.5 points absolute, and individual tasks vary by similar amounts. At these low absolute levels (many tasks near chance), such differences could reflect training-run variance. No variance estimates, confidence intervals, or multiple-seed results are reported for Table 1.

### Minor
1. **Top-k routing may require auxiliary regularization.** The paper never discusses whether the router collapses (all tokens routing to the same *k* states) or requires auxiliary losses analogous to those in Mixture-of-Experts models. Figure 5 shows diminishing returns for fixed *k=4* activation at large *m*, which is consistent with collapse, but this is not analyzed.
2. **Temperature τ is a tunable hyperparameter requiring grid search.** Its optimal value changes with *m*, adding tuning complexity not needed by Mamba-2 or Transformer baselines. The paper does not discuss how sensitive results are to suboptimal τ.
3. **Inference speed benchmark caveat.** Figure 6 shows ~2000 seconds to process 12K tokens for Transformer, which is orders of magnitude slower than typical H100 numbers with KV-cache. It appears the benchmark is run sequentially (batch size 1, token by token), a regime favorable to RNNs. Batch-inference comparisons, where Transformer KV-cache costs are amortized across requests, are absent.

### Trivial
None worth noting.

---

## Nice-to-Haves
- An ablation isolating which aspect (multi-state structure vs. sparse routing vs. reused affinity distribution) is responsible for the long-context extrapolation advantage would substantially strengthen the paper.
- Reporting perplexity on standard public benchmarks (e.g., The Pile, SlimPajama) would allow direct comparison with published Mamba-2 and GLA results.

---

## Novel Insights
The most genuinely novel insight is that tying the write and read routing distribution in a multi-state RNN (using the same α_t for both the memory update gate θ_t and the output merge weight φ_t) is not merely a design convenience—it is what makes sparse activation feasible without independently sparse read and write heads. This coupling implies that a memory slot unused at write time carries no information relevant to the current token at read time, making the top-k sparsity semantically consistent rather than merely approximate. The observed empirical property that proportional sparse activation matches dense performance as *m* grows (Figure 5) suggests the router learns nearly non-overlapping specializations across slots, a form of emergent disentanglement that could be of independent interest for memory-augmented models.

---

## Suggestions
- Provide at least one controlled ablation showing that replacing the tied α_t with independent write and read distributions degrades either performance or the ability to exploit sparse computation, to validate the design choice.
- Report results for at least two independent training seeds for Table 1 and the DCLM experiments.
- Add a section analyzing router behavior (entropy of α_t distributions, slot utilization statistics) to support or refute the claim that slots encode distinct semantic "topics."

---

## Score and Decision

The paper makes a real architectural contribution with a clean formulation, releases hardware-efficient kernels, and produces a surprising and consistently validated long-context extrapolation result. The main gaps—lack of mechanistic explanation for the extrapolation advantage and insufficient differentiation from GLA—are significant but addressable. The work provides enough new knowledge to be useful to the ICLR community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>