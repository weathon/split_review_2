## Summary
# Final Review Report

## Summary

This paper introduces MoEP (Modular Expert Paths), a sparse decoder-only Transformer architecture that combines layer-level top-k routing across parallel blocks with MoE-style projections. The key idea is to achieve sparsity while keeping the total parameter count fixed relative to a dense baseline (28M parameters for the linear-expert variant, matching GPT-2). The model is evaluated on the BabyLM strict-small benchmark (~10M words) and compared against GPT-2 and GPT-BERT baselines.

**Core strengths:** The fixed-parameter sparsity idea is timely and practically motivated — standard MoE models substantially increase total parameters, creating deployment/storage challenges. The architecture design (dimension-reduced parallel blocks with top-k routing) is a clean instantiation of this idea. The BabyLM evaluation is thorough, covering 14 tasks and providing training dynamics analysis.

**Core weaknesses:** (1) The load-balancing loss formulation uses entropy (−Σ p_i log p_i) rather than the standard importance-based MoE auxiliary loss, which may not effectively prevent expert collapse. (2) Performance claims are overstated — the paper claims to "outperform all BabyLM strict-small baseline models" while the data shows GPT-BERT variants achieve higher macro averages on most tasks. (3) No variance or statistical significance is reported, making it impossible to assess reliability. (4) The introduction contains grammatical errors and fragmented sentences that undermine readability and argument clarity. (5) The related-work section reads as a list rather than an analytical comparison, weakening the novelty positioning. (6) Several key architectural hyperparameters (N, P, E, k, λ values) are not specified in the main text.

**Novelty note:** External literature verification is unavailable in this run (Retrieval-Disabled Mode); novelty/comparison conclusions are intentionally deferred for manual verification. The paper's core idea — fixed-parameter sparsity via layer-level routing with dimension reduction — appears to have merit, but its novelty relative to PaPaformer, MoLE, and standard MoE variants cannot be fully assessed without targeted literature retrieval.

## Strengths
1. **Timely and practical motivation.** The paper addresses a genuine limitation of standard MoE: the substantial increase in total parameter count. While MoE reduces active parameters, it typically increases total parameters 2-8x (e.g., Mixtral 8x7B: 47B total vs ~13B active). MoEP's approach of keeping total parameters fixed at the dense-equivalent level is practically valuable for deployment scenarios where storage and memory are constrained.

2. **Clean architectural design.** The interleaving of full-size layers with dimension-reduced parallel layers connected by MoE shrink/grow blocks is conceptually elegant. The use of linear experts in the baseline variant keeps the design lightweight and interpretable. The architecture is well-illustrated in Figure 2, making it accessible to readers.

3. **Thorough BabyLM compliance.** The paper follows the BabyLM strict-small evaluation pipeline faithfully, including training a matching tokenizer, using the same data and checkpoint selection procedure. This ensures that comparisons against the provided baselines are reasonably controlled. The training dynamics analysis (Appendix A.3) provides useful insight into learning behavior beyond final scores.

4. **Honest limitation discussion.** The conclusion openly acknowledges the small-scale setting and the uncertainty about scaling behavior. This level of scientific candor is commendable and should be preserved in revision.

5. **Reproducibility effort.** The authors commit to releasing code and model weights on GitHub and Hugging Face, and specify the hardware environment (single A100) and training duration (1-2 hours per model). These details facilitate reproduction.

## Weaknesses
### W1. [Major] Incorrect load-balancing loss formulation
**Page 4 - Section 3.4: Routing Objective and Training Loss**

The paper defines the load-balancing regularizer as L_balance = -Σ p_i log p_i (entropy of the routing distribution, Equation 2). This entropy formulation encourages the routing probabilities p_i to be uniform, but it does NOT directly penalize token-assignment imbalance — a standard requirement for MoE training. The standard auxiliary loss (Switch Transformers, Fedus et al. 2022; DeepSeek-V2) is L_aux = E · Σ_i f_i · P_i, where f_i is the fraction of tokens assigned to expert i and P_i is the average routing probability. The entropy formulation could allow a gate to be uniformly uncertain (all p_i ≈ 1/E) while still routing most tokens to the same expert, defeating the purpose of load balancing.

**Required fix:** Replace Eq. (2) with the standard importance-based load-balancing loss and specify λ_block and λ_expert values. Without this correction, the training stability of MoEP cannot be guaranteed.

**Priority:** Must

### W2. [Major] Overstated performance claims
**Page 1 - Introduction (line 17) and Page 6 - Section 5.1 (line 86)**

The paper claims MoEP "was able to outperform all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models as well." However, Table 1 shows GPT-BERT (causal) achieves a macro average of 54.10 (excluding AoA) versus MoEP's 49.00 — GPT-BERT is substantially higher. MoEP only achieves the best macro average when AoA is included (44.50), a task where GPT-BERT variants score near zero or negative. The claim of universal superiority is not supported by the reported data.

**Required fix:** Replace with precise, evidence-grounded wording: "MoEP achieved a macro average of 44.50 (including AoA), outperforming the GPT-2 baseline (37.40), while GPT-BERT variants achieved higher macro averages on most tasks (up to 54.10)."

**Priority:** Must

### W3. [Major] Missing statistical significance and variance
**Page 6 - Section 5.1 and Table 1**

All results are reported as single-point estimates without standard deviations, confidence intervals, or significance tests. The margin between MoEP (44.50) and GPT-2 baseline (37.40) on the AoA-included macro average is 7.1 points, but without multi-seed variance, the reader cannot assess whether this gap is statistically reliable. On individual tasks, MoEP underperforms on BLiMP (59.15 vs 59.70), EWOK (50.20 vs 57.85), and WUG (33.00 vs 36.00) compared to the authors' own GPT-2 — suggesting the overall advantage may be driven by a few tasks rather than consistent improvement.

**Required fix:** Run all experiments with at least 3 random seeds and report mean ± std. Add statistical significance tests (e.g., paired bootstrap) for the primary comparison. Discuss task-level patterns of improvement and regression.

**Priority:** Must

### W4. [Major] Poor introduction writing quality limits scientific communication
**Page 1 - Introduction (lines 9-11)**

The introduction contains multiple grammatical errors and fragmented sentences that undermine scientific credibility:
- "Recent and previous work have examined **sparse and routing-based models** ... and" — incomplete sentence ending with "and."
- "enhance efficiency and re-thinking sparsity **novel way**" — grammatically broken.
- "different tokens communicates with different depth stack" — subject-verb agreement error.
- "ourEx layer-level MoEP" (Figure 1 caption) — probable typo for "our".

These errors extend beyond the introduction into other sections ("textbfAdamW" in Section 4, "a dense models" in Conclusion). While the technical content is understandable, the writing quality falls below conference publication standards.

**Required fix:** Thorough proofread and copy-edit of the entire manuscript. The introduction paragraphs should be restructured to follow a clear argument flow: problem → gap → solution → evidence → contributions. See annotation on lines 9-11 for a concrete rewrite.

**Priority:** Must

### W5. [Major] Related-work section lacks analytical depth
**Page 1-3 - Section 2.2: Mixture-of-Experts**

Section 2.2 reads as a paper-by-paper list organized by expert placement (FFN-level, Attention-level, etc.) without critical comparison. The most important comparison for MoEP's novelty — against MoLE (layer-level MoE for fine-tuning) and PaPaformer (parallel paths with independent pre-training) — is not sufficiently developed. The paper would benefit from a comparative table or explicit analysis of how MoEP differs from each related approach across dimensions such as: training regime (scratch vs fine-tuning), parameter efficiency, routing mechanism, and sparsity granularity.

**Required fix:** Add a comparative analysis paragraph contrasting MoEP with MoLE and PaPaformer along concrete axes. Alternatively, replace the list-style subsections with a structured comparison table.

**Priority:** Must

### W6. [Major] Missing key architectural parameters in main text
**Page 4 - Section 3.1-3.3**

The method section introduces parameters N (number of parallel layers), P (number of parallel blocks), E (number of experts), k (top-k), d_L, and d_P without providing their values. Readers must consult the appendix (Table 2) to learn that N=10, P=4, E=4, k=2, d_L=384, d_P=192. The shrinkage from d_L=384 to d_P=192 is a central design choice — it determines the parameter savings — yet the text does not discuss why 2x reduction was chosen or whether other ratios were tested.

**Required fix:** State all architectural hyperparameter values in Section 3 and include a brief rationale for the dimension reduction factor. Add a sensitivity analysis on d_P or at minimum acknowledge the design choice.

**Priority:** Should

### W7. [Minor] Training data stride and checkpoint description need clarification
**Page 5 - Section 4: Training Procedure**

The use of "stride of 128" for pre-tokenization is ambiguous without explanation of how stride interacts with the 512-token sequence length. The checkpoint description ("every 1M words up to 9M words, and subsequently every 10M words up to 100M words") is confusing because the training data is only ~10M words — the 100M figure refers to cumulative tokens seen across 10 epochs but this distinction is not made explicit.

**Required fix:** Clarify the stride-sequential length relationship and explicitly distinguish cumulative tokens from unique data size.

**Priority:** Should

### W8. [Minor] MoEP-SwiGLU parameter mismatch
**Page 9 - Table 2**

The "total parameter" row shows MoEP-SwiGLU has 38M parameters vs MoEP and GPT-2's 28M. This is a 36% increase. The Abstract claims MoEP "add[s] sparsity while keeping the total parameter count fixed" — this is only true for the linear-expert variant. The discrepancy should be transparently noted in the Abstract and Conclusion. If the SwiGLU variant is a contribution (C4), its different parameter count must be acknowledged.

**Required fix:** Add a note in the Abstract clarifying that the parameter-fixed claim applies to the linear-expert baseline, and that MoEP-SwiGLU uses 38M parameters.

**Priority:** Should

### W9. [Minor] No analysis of computational efficiency
**Page 5 - Section 4: Implementation Environment**

The paper provides training time (1-2 hours on a single A100) but does not report actual sparsity ratios, FLOPs per token, or inference speedup compared to the dense baseline. Since the paper's title emphasizes "Compact and Efficient Sparsity," quantitative efficiency metrics are expected. How many parameters are actually activated per token? What is the theoretical FLOP reduction? Is there a wall-clock speedup?

**Required fix:** Add a subsection reporting: (a) activated-to-total parameter ratio, (b) FLOPs per token for MoEP vs GPT-2, (c) wall-clock inference time.

**Priority:** Should

### W10. [Minor] Contribution 3 (routing behavior analysis) is underdeveloped
**Page 1 - Introduction (line 22)**

Contribution 3 states "We analyze expert networks routing behavior and show that layer level parallelism enable fast and stable training." However, the routing analysis in the main text (Section 5) is limited to comparing MoEP vs GPT-2 learning curves. There is no analysis of which experts/blocks are most frequently selected, whether different tokens specialize to different paths, or how routing patterns evolve during training. The training dynamics analysis in Appendix A.3 shows learning curves but does not examine routing behavior directly.

**Required fix:** Either add routing behavior analysis (expert utilization heatmaps, token-expert assignment entropy over time, routing stability across checkpoints) or rephrase the contribution to match what is actually shown (fast early learning).

**Priority:** Nice-to-have

### W11. [Minor] Writing quality issues (additional instances)
Throughout the manuscript

Beyond the introduction, several sentences contain grammatical or formatting errors:
- "textbfAdamW" (Section 4, should be "textbf{AdamW}" or "AdamW")
- "ourEx layer-level MoEP" (Figure 1 caption)
- "which prior work suggest as the major of the performance increase" (Introduction, unclear meaning)
- "a dense models" (Conclusion, subject-verb agreement)
- "Liner" (Table 2, should be "Linear")

These are individually minor but collectively signal insufficient proofreading.

**Required fix:** Thorough copy-edit pass.

**Priority:** Nice-to-have

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses a timely and practically motivated problem (fixed-parameter sparsity) with a clean architectural design. The BabyLM evaluation is thorough in terms of task coverage, and the authors commit to open-source release. However, several critical issues prevent a higher score:

1. **Novelty uncertainty (deferred):** External literature verification is unavailable in this run. The core idea — layer-level routing with dimension-reduced parallel blocks — has suggestive novelty versus PaPaformer and MoLE, but this cannot be confirmed without retrieval-based literature analysis. Score impact: -1 point.

2. **Methodological flaw in load-balancing loss (W1):** The entropy-based regularizer is not the standard MoE auxiliary loss and may not prevent expert collapse. This directly affects the validity of the training procedure. Score impact: -1.5 points.

3. **Overstated performance claims (W2, W3):** The paper claims to outperform all baselines while data shows GPT-BERT achieves higher macro averages. No variance or significance is reported. This undermines the central experimental claim. Score impact: -1.5 points.

4. **Writing quality (W4, W11):** Grammatical errors, fragmented sentences, and unclear argumentation reduce readability and professional quality below conference standards. Score impact: -1 point.

5. **Insufficient analytical depth in related work (W5):** The paper does not clearly differentiate itself from the most relevant prior methods, weakening its novelty positioning. Score impact: -0.5 point.

The paper has a solid core idea and honest limitation awareness, which are positive signals. With substantial revision addressing the load-balancing loss, statistical rigor, claim precision, writing quality, and related-work analysis, the paper could become a meaningful contribution to the sparse LLM architecture literature.

**Post-Revision Target:** [6, 7]/10 — Achievable if the load-balancing loss is corrected, claims are bounded to match evidence, multi-seed variance is reported, and writing quality is brought to publication standard.