Now I have all the verification I need. Let me write the final consolidated review.

## Summary

This paper proposes QubitCache, a KV-cache compression method that keeps 15% of tokens in classical storage while encoding attention patterns of the remaining 85% of tokens into quantum-inspired amplitude-encoded states (9-qubit circuits). During inference, these quantum states are measured to produce probabilistic attention weights for reconstructed (interpolated) value vectors, enabling "soft" rather than binary attention. The paper evaluates across five models and seven benchmarks, reporting 7× compression with 92–97% of uncompressed performance.

## Strengths

1. **Broad evaluation across models and benchmarks.** Table 1 tests five models (Mistral-7B, Qwen2-7B, Phi-4-mini, DeepSeek-Coder-7B, Llama-8B) on seven benchmarks spanning short-context, long-context, and multi-hop reasoning — broader coverage than many KV cache compression papers.

2. **Conceptual framing is genuinely interesting.** The observation that attention patterns (relational structure between tokens) may carry more information than the tokens themselves is well-motivated (p. 1–2) and offers a credible departure from the token-eviction framing dominant in the literature.

3. **The ablation study (Table 4) is informative and honestly reported.** It cleanly separates the contribution of attention-based token selection from quantum encoding, showing that attention-based selection drives most of the gain. The paper includes this comparison and reports the 3.9% quantum contribution explicitly rather than obscuring it.

## Weaknesses

### Major

1. **The "logarithmic compression beyond classical information-theoretic limits" claim is not realized in the implemented system.** The abstract (p. 1, line 9) advertises logarithmic compression, but §3.2.2 (p. 4) states: "the current implementation operates as a classical simulation." A classical simulation of a 9-qubit amplitude-encoded state stores all 2⁹ = 512 amplitudes — no memory savings over storing the 512 attention weights directly. The actual 7× compression in Table 3 comes from retaining only 15% of tokens (a token-eviction strategy), not from the quantum encoding. The O(log N) memory advantage is a theoretical claim for future quantum hardware, not a property of the present system.

2. **The quantum encoding provides only a negligible fraction of the method's performance, undermining the paper's core contribution.** The ablation (Table 4) shows:

   | Configuration | F1 | Drop from Full |
   |---|---|---|
   | Full QubitCache | 0.491 | — |
   | No Quantum | 0.472 | −3.9% |
   | Random + Quantum | 0.335 | −31.8% |
   | Random No Quantum | 0.334 | −32.0% |

   The quantum encoding contributes **3.9% relative improvement** with attention-based selection and **essentially zero** (0.3%, within noise) with random selection. In contrast, attention-based selection alone (Random No Quantum → No Quantum) provides ~41% relative improvement. The paper's central claimed novelty — quantum-inspired encoding — drives a negligible fraction of the overall results. This substantially undercuts the "paradigm shift" framing.

3. **The "relational preservation" claim overstates what the encoding captures.** The method averages attention scores across all layers and heads (Eq. 3–4) to produce a single probability distribution per 512-token segment. This loses head-specific attention patterns and directional asymmetries. The actual mechanism (Eq. 6–7) is: (a) select 15% of tokens via attention scores, (b) interpolate value vectors for the remaining tokens via inverse distance weighting, (c) weight these interpolated values by quantum-derived probabilities. This is value interpolation on top of token eviction, not truly preserving the "relational structure" between tokens as the paper claims.

### Minor

4. **Table 4 (the key ablation) does not specify which model, dataset, or task the F1 scores are measured on.** The values (0.491, 0.472, etc.) do not clearly match any single column in Table 1, and the surrounding text (§4.5.1) provides no identification. Without this context, the ablation results cannot be independently interpreted or reproduced.

5. **No variance or statistical significance is reported for any experiment.** Tables 1–4 and Figure 3 all present single-point estimates without standard deviations, confidence intervals, or multiple-run results. This is especially problematic given that the quantum encoding's claimed contribution is only 3.9% — an effect that could plausibly fall within run-to-run variance.

6. **The "103% of baseline performance" claim in Figure 3(b) is ambiguous.** The term "baseline" is not defined in this context. The F1 scale (0.7–0.85) differs substantially from the main results (max ~0.65), suggesting a different experimental setting, but the paper does not clarify. If this refers to uncompressed Full KV, a compression method exceeding uncompressed performance would require separate investigation that is not provided.

### Trivial

- None.

## Nice-to-Haves

- **Test on longer sequences.** The evaluation uses 2K–8K tokens (§4.1.2). KV cache pressure is most acute at 32K–128K+, and the method's interpolation assumption (positional locality of semantic content, Eq. 6) may degrade at longer ranges.
- **Report computational overhead.** The paper mentions Qiskit-based circuit simulation but does not report the latency or FLOP overhead per token, layer, and head. Since the O(2^n) gate cost of arbitrary state preparation is acknowledged in §2, a runtime analysis would help assess practical deployability.
- **Compare at matched retention ratios.** The paper compares QubitCache (15% retention) against baselines at 50% retention. Showing what baselines achieve at 15% retention would isolate the method's advantage from the retention-rate confound, though this asymmetry actually disadvantages the author's method.

## Removed Points

- **Missing baselines (SnapKV, KIVI):** Removed — the paper covers H2O, ScissorHand, StreamingLLM, and GEAR, which constitute a reasonable baseline set for this genre.
- **λ = √(|I_p|/N) choice without justification:** Removed — this is a minor design hyperparameter; extensive formal justification is not standard practice.
- **Theoretical proof absent from main text:** Removed — the appendix (stripped by the parser) is the natural location for proofs, and the main text (lines 9, 25) refers to the proof.
- **Computational cost through Qiskit not fully disclosed:** Removed — the paper (§4.1.1) mentions optimizations and refers to Appendix A.1, which the parser stripped.
- **PIQA as a short-context benchmark:** Removed — it is one of seven benchmarks; its inclusion does not materially affect the paper's claims.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a tension that the paper partially acknowledges but does not resolve: the quantum encoding provides the conceptual hook but delivers minimal empirical benefit, while the effective mechanism (attention-weighted selection + value interpolation) is a synthesis of known ideas whose independent contribution is hard to evaluate due to the conflated framing.

## Suggestions

1. **State the model, dataset, and task for Table 4's ablation.** This is necessary for the results to be interpretable.
2. **Report variance** (standard deviations or confidence intervals) for all main experiments, given the small effect size attributable to the quantum encoding.
3. **Clarify what "baseline" refers to in Figure 3(b)**, and if it refers to Full KV, explain how a compressed method can exceed uncompressed performance.
4. **Tone down the framing.** The paper would be better served by presenting the method as "attention-weighted token selection with probabilistic value interpolation" rather than as a quantum-inspired paradigm shift, given that the quantum component contributes 3.9%.

## Score and Decision

The paper presents an interesting conceptual framing and broad evaluation, but the central claimed contribution — quantum-inspired logarithmic compression — is not realized in the implemented system, and the ablation data show the quantum encoding provides negligible benefit (3.9%). The effective mechanism is a combination of attention-based token selection and value interpolation, whose novelty over existing methods is incremental. Given the gap between the paper's advertised contributions and what the implementation actually delivers, the paper does not meet the bar for acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>