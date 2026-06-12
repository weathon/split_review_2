## Summary

The paper proposes QUOKA, a training-free, hardware-agnostic sparse attention method for accelerating LLM inference during chunked prefill. The key insight is that queries with low cosine similarity to the mean query attend broadly across keys and contribute most to attention logits; by prioritizing these queries, QUOKA selects a small representative query subset, scores keys via cosine similarity, and aggregates scores to subselect the KV cache. Experiments across NIAH, RULER, LongBench, and Math500 on multiple model families and hardware platforms demonstrate near-baseline accuracy with up to 5× attention speedup on GPUs and 7× on CPUs.

## Strengths

- **Well-motivated geometric observation with empirical support.** The paper identifies that queries with low cosine similarity to the mean query interact with the majority of keys (Figure 2c shows 0.737 correlation between S_q and max attention scores). PCA visualizations (Figure 2b) confirm that high-S_q queries lie closer to the key cluster. This provides a principled criterion for query subselection in the multi-query prefill setting where naive averaging of existing single-query methods fails.

- **Comprehensive and convincing evaluation.** The paper evaluates across 6 model families (Llama3, Qwen2.5, Qwen3, SmolLM, Qwen3-30B MoE, GPT-OSS), 4 benchmarks, and 3 hardware platforms (A100, RTX 2080, Intel Xeon CPU). Results are consistently strong: on RULER (Table 1), QUOKA outperforms the next-best method by 10–25 points at 32k context; on LongBench (Table 3), it maintains 94–103% of dense accuracy at B_SA=512 while baselines drop to 38–86%.

- **Practical deployment advantages.** The method requires no training, uses only standard linear algebra operations (no custom CUDA kernels), and is compatible with FlashAttention. The pre-aggregation trick for GQA (Section 3.3) reduces computation by a factor of the number of KV groups. Latency measurements on diverse hardware (Figure 5) demonstrate real-world applicability beyond datacenter GPUs.

- **Elegant algorithmic design.** The three-stage pipeline (query subselection, cosine similarity scoring, group-aware aggregation) is clean, well-motivated, and each component is individually justified. The use of cosine similarity over dot products is validated by >10% improvement on RULER (Table 9 reference), and max-aggregation over mean-aggregation across queries is supported by the heavy-tailed distribution in Figure 3.

## Weaknesses

### Fatal
None.

### Major

- **The connection between Theorem 1 and the actual subselection strategy is loose.** Theorem 1 bounds CosSim(M_Q, q*) in terms of CosSim(k, q_0) and CosSim(M_Q, k), but the paper doesn't formally establish why minimizing cosine similarity to the mean query is optimal for approximating the full post-softmax attention matrix. The empirical evidence is compelling, but the theoretical claim that this "preserves queries that contribute most to the attention distribution" (Section 3.1) is not rigorously derived from the theorem. A tighter connection—perhaps bounding the approximation error of the full attention output as a function of the query selection—would significantly strengthen the contribution.

- **Incomplete latency analysis.** The paper reports speedups relative to dense attention but does not decompose the overhead of QUOKA's scoring and selection steps versus the savings from reduced attention computation. For small B_SA or short sequences, the overhead of computing cosine similarities, top-k operations, and gather operations could dominate. A breakdown of time spent in each stage (query subselection, scoring, aggregation, gather, attention) would make the efficiency claims more transparent and help practitioners understand the crossover point where QUOKA becomes beneficial.

- **The NIAH "Full" baseline behavior needs clarification.** The figure description for Figure 4 states that the Full attention baseline shows "lower accuracy, especially at higher document lengths and needle depths," which is counterintuitive since chunked prefill is mathematically equivalent to standard prefill. If the full baseline is indeed degrading, this warrants explanation; if this is a parser artifact, the actual figure should be examined carefully. This ambiguity undermines confidence in the NIAH comparison.

### Minor

- **Math500 results are referenced but relegated to the appendix.** The claim that QUOKA "surpasses the accuracy of dense attention" on a generation-intensive reasoning task is a notable result that supports the paper's versatility claim. Presenting Table 8 in the main text would strengthen this argument.

- **GPT-OSS-20B results in Table 1 appear incomplete.** The QUOKA row for GPT-OSS-20B seems to be missing the 32k value, making it impossible to fully assess performance on the largest model at the longest context.

- **No analysis of per-layer behavior.** Attention patterns vary significantly across layers (early layers tend to be more local, later layers more global). Understanding where QUOKA is most and least effective would provide useful deployment guidance and could inform layer-specific budget allocation.

- **Limited guidance on hyperparameter selection.** While the ablation (Section 4.5) shows gradual degradation, the paper doesn't provide concrete recommendations for setting B_SA, B_CP, and N_Q given hardware constraints. A Pareto frontier analysis or decision procedure would be valuable for practitioners.

### Trivial
None.

## Nice-to-Haves
- A comparison showing how QUOKA interacts with KV cache eviction methods, which the paper acknowledges as complementary.
- Analysis of QUOKA's behavior on attention sink tokens, which are known to be critical for generation quality.
- Wall-clock comparison on additional consumer hardware (e.g., Apple Silicon, Qualcomm NPUs) to fully support the hardware-agnosticism claim.

## Novel Insights
The paper's most novel contribution is the geometric characterization of queries in the prefill setting: queries with low cosine similarity to the mean query are the dominant contributors to the attention distribution, and this property can be exploited for efficient multi-query KV selection. This insight addresses a genuine gap—existing sparse attention methods designed for single-query generation degrade significantly when naively extended to multi-query prefill. The paper also demonstrates that cosine similarity provides a more stable scoring proxy than dot products for this task, and that max-aggregation across queries (rather than mean) better preserves rare but important interactions, as evidenced by the heavy-tailed deviation distribution in Figure 3.

## Suggestions
- Provide a latency breakdown table showing time spent in each stage of Algorithm 1 versus the attention computation, across different sequence lengths and B_SA values.
- Clarify or correct the NIAH full-attention baseline results in Figure 4.
- Include Math500 results (Table 8) in the main paper.
- Add a brief analysis of per-layer QUOKA effectiveness to guide potential layer-specific tuning.

## Score and Decision
This is a well-executed paper that makes a genuine practical contribution to an important problem. The geometric observation about queries is novel and well-supported empirically, the algorithm is clean and hardware-agnostic, and the evaluation is comprehensive across models, benchmarks, and hardware. The main weakness is the gap between the theoretical justification (Theorem 1) and the actual algorithmic design, along with incomplete latency decomposition. However, the consistently strong empirical results and practical deployment advantages outweigh these concerns.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: Accept