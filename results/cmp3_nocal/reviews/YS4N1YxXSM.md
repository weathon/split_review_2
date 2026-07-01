## Summary

QUOKA presents a training-free, hardware-agnostic sparse attention method designed specifically for the chunked prefill setting. The key insight is that queries with low cosine similarity to the mean query are the most informative for KV selection. The method subselects representative queries via this dissimilarity measure, scores keys by cosine similarity to those queries, and aggregates via max-pooling across queries. Experiments across RULER, LongBench, NIAH, and Math500 on five model families show substantial accuracy improvements over prior sparse attention methods (often 10–20+ points) while delivering 3–7× speedups.

## Strengths

- **Novel, well-motivated method that fills a real gap.** Existing query-dependent sparse attention methods are designed for single-query generation and degrade under chunked prefill. QUOKA's three-component design (query subselection by cosine dissimilarity → cosine-similarity scoring → max-aggregation) directly addresses the multi-query setting. The paper correctly identifies the problem and constructs a principled solution.

- **Strong empirical results across diverse conditions.** The main accuracy results (Table 1 for RULER, Table 3 for LongBench) show QUOKA outperforming competing sparse attention methods by large margins across 5 model families (Llama3.2, Qwen2.5, Qwen3, SmollM3, GPT-OSS), including MoE and NoPE variants, across selective budgets from 512 to 2048. The ablation study demonstrates gradual degradation under increasing sparsity, which is desirable for deployment tuning.

- **Hardware-agnostic by design.** QUOKA uses only standard linear algebra operations and feeds the reduced KV set into dense attention kernels, avoiding custom-CUDA-kernel dependencies. The latency results (Figure 5) across A100, RTX 2080, and Intel Xeon CPU credibly demonstrate this portability advantage.

- **Comprehensive evaluation scope.** The paper evaluates on multiple benchmarks (synthetic retrieval, multi-task long-context, mathematical reasoning), measures both accuracy and latency (attention-level and end-to-end TTFT), and ablates key hyperparameters (B_SA, B_CP, N_Q).

## Weaknesses

### Major

- **Theorem 1 is incomplete as stated.** The theorem on page 4 (lines 143–149) states a bound involving q\* but never defines what q\* is. It appears in the conclusion (Eq. 5) and in the definition of S_q (line 149) without introduction. The surrounding prose ("if a query q attends strongly to k…") uses q and q\* interchangeably. This is a structural flaw in the presentation of the paper's theoretical motivation. The method's empirical results stand independently, but a paper that presents a theorem should state it correctly. The proof is deferred to Appendix D (which the parser strips), but the theorem should be self-contained in the main text.

- **The core geometric observation is supported by evidence from a single layer and head.** The entire method is motivated by the claim that "queries with low cosine similarity to the mean query interact more strongly with more keys and have the greatest contribution to final attention logits." The evidence for this claim comes entirely from Figure 2, which is explicitly from "Llama 3.2-3B-Instruct, layer 0 head 11" — one layer and one head of one model. The paper does not show that this property holds across layers (where attention patterns differ substantially), across heads, or across other models. Given that different layers in transformers exhibit very different attention behavior (early layers attend broadly, later layers focus on specific tokens), this is an evidential gap. The strong downstream accuracy results serve as indirect validation, but the paper overclaims the strength of its empirical motivation.

### Minor

- **Sparse attention beating dense attention is not discussed.** In Table 3, QUOKA achieves normalized accuracy > 1.0 for SmollM3 at B_SA=1024 and B_SA=2048 (1.03 and 1.028, meaning it exceeds the full-attention baseline). Section 4.4 similarly notes that QUOKA "in some cases surpasses the accuracy of dense attention" on Math500. A sparse approximation outperforming exact computation warrants at least a brief comment — e.g., whether this reflects a regularizing effect of sparsity, evaluation noise, or some property of the chunked prefill baseline. Without discussion, this observation undermines the paper's framing as an *approximation* method and raises mild questions about the evaluation protocol.

- **Baseline fairness concerns.** The paper acknowledges that competing methods (SparQ, Loki, LessIsMore) were designed for generation, not prefill (Section 2.4), but applies them with default settings without quantifying how much tuning they received. The reported accuracy gaps are unusually large — e.g., on RULER at 32k for Llama3.2-3B, QUOKA scores 57.01 vs. the next-best at 31.14. While the direction of improvement is believable, the magnitude may be inflated by untuned baselines. A sentence describing whether each baseline received any prefill-specific tuning would address this concern.

- **No limitations or failure-mode discussion.** The paper has no limitations section. Every method has failure modes — e.g., what happens when most queries are near the mean (short prompts, or layers with homogeneous attention)? What if the outlier queries are themselves uninformative? Acknowledging boundaries would strengthen the paper.

### Trivial

- Accuracy results lack error bars or statistical significance estimates (latency results are properly averaged over 100 trials).

## Nice-to-Haves

- Fix or downgrade Theorem 1: define q\* explicitly, or if the proof requires the appendix, restructure the presentation so the main text does not rely on an incomplete theorem statement.
- Add a simple quantitative analysis of the core geometric claim across multiple layers and heads for at least 2–3 models — e.g., report the correlation between S_q and attention entropy or max attention weight across layers.
- Briefly explain the sparse-beats-dense phenomenon (SmollM3 >1.0, Math500).
- Add a limitations paragraph acknowledging settings where QUOKA may struggle.

## Removed Points

- **"The 70% runtime claim should be cited more precisely"** — The paper *does* cite it (Agrawal et al., 2024; Kamath et al., 2025; Xu et al., 2025a) on line 13. The criticism is factually incorrect.
- **"The claim about averaging over queries misleadingly references Table 3"** — This is a minor phrasing observation, not a substantive weakness.
- **"Code not released weakens reproducibility"** — The paper acknowledges this. Algorithm 1 is detailed and uses standard operations; reproduction is feasible.
- **"Section-by-section notes"** that are observations without actionable criticism (e.g., PCA projection limitations, normalized accuracy format) are subsumed by the weaknesses above or are too speculative to stand alone.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix Theorem 1 by defining q\* explicitly, or remove the theorem and keep the geometric argument as an empirical observation supported by data.
2. Add a small supplementary analysis showing the S_q–attention correlation across layers and heads for at least one additional model.
3. Add one paragraph in Section 4 discussing the >1.0 normalized accuracy results.
4. Add a sentence in the experimental setup describing baseline tuning efforts (or acknowledging the absence thereof).

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>