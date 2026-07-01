## Summary

MoEP proposes a decoder-only architecture that combines layer-level parallel Transformer blocks with top-k token routing and MoE-style shrink/grow projections. The key idea is to add sparsity (selective token activation across parallel blocks) while keeping the total parameter count fixed by operating the parallel stack at reduced dimensionality. The method is evaluated on BabyLM strict-small (~10M words) against GPT-2 and GPT-BERT baselines.

## Strengths

1. **Novel architectural idea.** Combining parallel blocks (PaPaformer-style) with top-k routing and dimensionality reduction to maintain fixed parameter count while adding sparsity is a genuinely different approach from standard FFN-level MoE. Section 3 and Figure 2 clearly communicate the design.

2. **Reproducible setup.** The paper uses the BabyLM strict-small track with a well-defined evaluation pipeline, releases code and models, and describes training procedures in adequate detail. This is a reasonable low-resource prototyping choice.

3. **Acknowledged limitations.** Section 6 notes that small-scale results may not transfer to larger settings and that reduced-dimensionality parallel layers may not suffice on complex data. The paper is appropriately cautious about scope.

---

## Weaknesses

### Fatal

None.

### Major

1. **Overclaim of outperforming all baselines.** The introduction (line 31) claims MoEP "outperformed all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models as well." Table 1 shows this is misleading: on the macro average excluding AoA, GPT-BERT variants score 52.40–54.10 while MoEP scores 49.00. The claim only holds when the AoA task is included in the aggregate—and GPT-BERT scores poorly on AoA because the task is architecturally inapplicable (see line 197: "Our GPT-2 and MoEP-SwiGLU results do not include AoA scores"). The abstract (line 9) more cautiously claims only "outperform the GPT-2 baseline," but the introduction's broader claim is unsupported by the evidence in the paper's own Table 1. This is a significant framing mismatch that misrepresents the results.

2. **Marginal improvement over the paper's own GPT-2 with no variance reporting.** MoEP scores 49.00 vs. the paper's own GPT-2 at 48.10 on macro avg excluding AoA—a 0.9-point gap (Table 1). No multiple seeds, confidence intervals, or significance tests are reported. The paper itself acknowledges its GPT-2 "reached performance near comparable to MoEP" (line 168). With such a small gap and no variance estimates, it is impossible to determine whether the improvement is reliable or due to noise in a single-run evaluation.

3. **No efficiency or sparsity measurements despite the title's emphasis on "efficiency" and "sparsity."** The paper's title reads "Compact and Efficient Sparsity with Modular Expert Paths," and the abstract claims sparsity "accelerates model learning." Yet the paper reports zero FLOP counts, throughput (tokens/sec), inference latency, memory footprint, or any quantitative sparsity metric (e.g., fraction of activated parameters per token). Without these, the "efficiency" claim is unevidenced. The computational profile of MoEP (10 parallel layers at d=192 with top-2 routing among 4 blocks) vs. GPT-2 (12 dense layers at d=384) is structurally different and should be measured to support the paper's central framing.

4. **No ablation studies.** MoEP combines multiple design choices: (a) parallel blocks vs. sequential layers, (b) top-k routing across parallel blocks, (c) MoE shrink/grow projection layers, (d) reduced dimensionality in the parallel stack, (e) load-balancing auxiliary loss, and (f) an optional SwiGLU variant. There are zero ablations isolating any component. A critical missing baseline is a parallel-block version *without* routing (e.g., averaging the outputs of all P blocks) at the same total parameter count. This would isolate whether routing-driven sparsity drives the result, or whether the parallel structure and reduced dimensionality alone explain the performance.

### Minor

5. **MoEP-SwiGLU violates the fixed-parameter-count premise.** Table 2 shows MoEP-SwiGLU at 38M parameters vs. GPT-2's 28M—a 36% increase. The paper's core selling point ("add sparsity while keeping the total parameter count fixed") does not hold for this variant. While the base MoEP (28M) maintains parity, the SwiGLU variant's parameter increase should be explicitly acknowledged as a departure from the premise, and the comparison discussed more carefully. (MoEP-SwiGLU also performs worse than base MoEP at 47.70 vs. 49.00, further undermining the rationale for this variant.)

6. **Single-run evaluation with limited statistical rigor.** Training for 10 epochs on ~10M words using a single seed (Table 3), with substantial overlap between training examples (stride of 128, line 150), makes it difficult to assess the reliability of the results. No per-task variance is reported.

7. **Non-standard load-balancing loss without justification.** Equation (2) defines the balancing term as the entropy of routing probabilities (−Σ p_i log p_i). The paper calls this "the standard load-balancing regularizer" (line 126), but this differs from the squared coefficient-of-variation or importance-based losses standard in the MoE literature (Switch Transformer, DeepSeek). Entropy maximization encourages uniform routing, which is reasonable, but the choice is unmotivated and not compared to alternatives. Additionally, p_i is not fully defined (are these softmax probabilities before top-k discretization, or actual assignment frequencies over a batch?).

---

## Nice-to-Haves

- FLOPs or throughput comparison between MoEP and GPT-2 to support the efficiency/sparsity claims.
- Ablation: parallel blocks without routing at same parameter count.
- Multiple training seeds with variance reporting to assess the 0.9-point gap.
- Analysis of the actual sparsity ratio (activated params per token vs. total params).
- Comparison with a more recent small model architecture (e.g., a TinyLlama-style model at comparable size) rather than only GPT-2 (2019).

---

## Removed Points

These points were flagged for removal from the harsh critic's input. Treat them with caution if referenced.

- **Claim that the headline overclaim is "fatal" / structural.** While the introduction overclaims (claiming to beat all baselines when GPT-BERT variants clearly outperform MoEP on the primary metric excluding AoA), this is a significant framing issue (Major) but not fatal. The paper's core contribution—parallel blocks + routing at fixed parameter count—does not depend on beating GPT-BERT. The abstract correctly limits the claim to GPT-2.
- **Formatting/duplication nitpick** (repeated paragraph in introduction, lines 15–16). Removed per formatting-rule instructions. Parser artifacts, not author errors.
- **"Missing appendix content" references.** Removed per parser-artifact rule. Appendices are stripped by the parsing pipeline but exist in the original submission.
- **"MoEP converges faster but both peak at 30M checkpoint undermines sample efficiency claim."** This overreads the evidence. MoEP reaching near-optimal scores earlier in training (Appendix A.3, lines 307–311: "MoEP exhibits more comprehensive early learning, reaching peak performance at the 30M checkpoint") can still indicate better sample efficiency even if both models ultimately peak at the same checkpoint.
- **Criticism about "unfair comparison favoring the author's method."** GPT-BERT variants are presented as baselines from the BabyLM leaderboard, not selected by the authors. The asymmetry (GPT-BERT beats MoEP) actually works against the authors, not for them.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Correct the overclaim in the introduction.** MoEP does not outperform GPT-BERT variants on macro avg excluding AoA. Frame the contribution accurately: competitive with GPT-2 at fixed parameter count with an alternative form of sparsity and better sample efficiency.
2. **Add at least one critical ablation:** a version with parallel blocks but no routing (e.g., average all P blocks) at the same total parameter count.
3. **Report FLOPs, activated parameter ratio, or wall-clock throughput** to support the efficiency/sparsity claims.
4. **Run 3+ seeds** and report variance so readers can judge whether the 0.9-point gap is reliable.
5. **Address the MoEP-SwiGLU parameter discrepancy** explicitly, or redesign it to match the 28M count.

---

## Calibration Report

**Round 1 bracket:** 4.0–4.5 (based on similarity to papers in the 3.5–5.5 range).

**Anchor papers retrieved (all rounds):**

| Anchor | Avg Human Score | Round | Comparison |
|--------|----------------|-------|------------|
| NanoMoE (04RLVxDvig) | 3.00 | R1 (1.5–3.5) | MoEP has a more substantial evaluation (BabyLM vs. toy problems) but both lack efficiency metrics and ablations. MoEP is stronger. |
| MOEfication by Masks (762u1p9dgg) | 3.40 | R1 (1.5–3.5) | MoEP has a clearer architectural contribution and a more realistic evaluation setting. |
| MoIN (L0PciKdHsP) | 4.50 | R1 (3.5–5.5) | Similar weaknesses: marginal improvement over baselines, unclear efficiency benefits. MoEP's evaluation is more standardized (BabyLM pipeline). |
| Efficient Expert Pruning (TTUtPIpaol) | 5.25 | R1 (3.5–5.5) | More thorough experimental design (multiple model sizes, many datasets). MoEP's evaluation is weaker. |
| MoLEx (rWui9vLhOc) | 6.33 | R1 (5.5–7.5) | Stronger paper with comprehensive experiments and clear methodology. MoEP does not reach this quality bar. |
| Dynamic Layer Tying (d4uL2MSe0z) | 4.50 | R2 (3.5–5.5) | Similar scope (parameter-efficient Transformers). MoEP has a more novel architecture but weaker evidence (no efficiency metrics vs. measured memory reduction). |
| Learning Param Sharing (tGsumqfOUk) | 4.75 | R2 (3.5–5.5) | More thorough ablation study. MoEP has zero ablations. |
| SeerAttention (HmwneoGoy9) | 5.25 | R2 (3.5–5.5) | Stronger evaluation with clear efficiency claims backed by measurements. |

**Narrowing rationale:** MoEP sits below Efficient Expert Pruning (5.25, Reject) and MoIN (4.50, Reject) because it provides no efficiency measurements despite "efficiency" being in the title. It sits above NanoMoE (3.00) because the architectural idea is clearer and the evaluation is more realistic. The strongest points of comparison are MoIN (4.50) and Dynamic Layer Tying (4.50). MoEP's combination of overclaiming, absent efficiency metrics, zero ablations, and marginal 0.9-point improvement places it at the lower end of the 4–5 range.

**Final score: 4.0.**

---

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>