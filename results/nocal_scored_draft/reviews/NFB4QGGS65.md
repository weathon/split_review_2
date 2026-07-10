Now let me compile the final review.

## Summary

This paper establishes a theoretical connection between GPTQ, a widely-used LLM post-training quantization method, and Babai's nearest plane algorithm from lattice theory. The authors prove that GPTQ executed back-to-front is mathematically identical to Babai's algorithm (without LLL reduction) applied to the lattice defined by the layer's factorized Hessian. This equivalence yields a tight worst-case error bound for the no-clipping setting (Theorem 5) and motivates two practical no-clipping quantization schemes (SSQR, HPTQ) with associated CUDA inference kernels.

## Strengths

- **A genuine theoretical connection.** The paper proves that GPTQ (back-to-front) = Babai's nearest plane algorithm on the Hessian-defined lattice (Theorem 4). This bridges LLM quantization and lattice-based CVP approximation — a non-obvious insight that provides a principled answer to why a local greedy rule works well globally. The equivalence is crisply stated, and the "ineffectiveness of composing algorithms" check (lines 201–202) confirms it is tight.

- **A concrete error bound (Theorem 5).** The bound is expressed in terms of the LDL decomposition of the permuted Hessian and the quantization scales, giving a testable prediction about worst-case layer-wise error in the no-clipping regime. This is more specific than the heuristic understanding that previously existed.

- **Honest, well-calibrated writing.** The paper explicitly acknowledges that the min-pivot order yields only "modest" accuracy gains, that the error bound only holds in the no-clipping setting, and includes a footnote about concurrent work (Birnick, 2025). This candor about limitations is commendable.

## Weaknesses

### Fatal
None.

### Major

- **Insufficient differentiation from QuIP/LDLQ.** The paper mentions QuIP (Chee et al., 2023) in a single sentence (line 27): "QuIP … proves an error guarantee for GPTQ and proposes the LDLQ method as an equivalent variant of GPTQ." QuIP's LDLQ is itself a lattice-based quantization scheme equivalent to GPTQ with an error guarantee. The paper claims to be "the first to provide a geometric interpretation for GPTQ" but does not explain what QuIP's existing guarantee was, whether it already implies the Babai connection, or what specific new insight the Babai framing adds (a tighter bound? a different geometric picture? a connection to the broader lattice literature?). A reader familiar with QuIP cannot determine what is genuinely novel here. This ambiguity about the primary contribution is a structural concern that should be resolved in the rebuttal.

- **Thin main-paper experimental validation.** (a) The method comparison (Figure 4a) shows only WikiText-2 perplexity on a single model (Qwen3-8B) in the main text. Zero-shot benchmarks (MMLU, ARC, HellaSwag) and results on other model families (e.g., Llama) are deferred entirely to the appendix. (b) The comparison set in the main paper is limited to RTN, GPTQ, HRTN, and SSQR variants — no recent SOTA PTQ methods appear in the main figures. The paper references an appendix section (Section E.5) comparing other methods, but the main text alone does not demonstrate that the practical methods are competitive with the current state of the field. For a paper claiming practical advances, this is insufficient.

- **The error bound (Theorem 5) is not empirically validated.** The paper presents Theorem 5 as a key theoretical contribution, but never measures the gap between the bound and the actual quantization error across layers or settings. The reader cannot assess whether the bound is informative, loose, or vacuous in practice. Even a simple plot of predicted vs. actual error per layer would address this gap.

### Minor

- **The practical methods (SSQR and HPTQ) are incremental combinations of existing ideas.** SSQR = SpQR + binary-search scale adjustment to meet an outlier-density target; HPTQ = GPTQ + Huffman encoding (previously explored for network compression by Choi et al., 2017, as the paper notes). The paper does not demonstrate that the Babai-theoretic framing *uniquely* motivates these designs or drives the improvement. The theoretical connection is elegant, but the practical methods do not serve as strong evidence that the theory yields non-obvious practical benefits.

- **The error bound only applies in the no-clipping setting.** The paper is transparent about this, but it means the main analytical result does not directly address the motivating question (why standard GPTQ, which clips, works well globally). The bound's relevance to standard GPTQ practice is indirect.

### Trivial
None.

## Nice-to-Haves

- Compare the CUDA kernel against an optimized INT4 GEMM baseline (e.g., GPTQ's own CUDA kernel or bitsandbytes), not just PyTorch BF16.
- Move at least one standard zero-shot benchmark (e.g., MMLU, ARC) into the main paper body to support the practical claims.
- Provide per-layer empirical validation of the error bound.

## Removed Points

*These points were flagged by the reviewer input but are removed per filtering rules; treat with caution.*

- **Proof deferred to appendix.** REMOVED: The parser strips appendix sections from all papers. The proof exists in the original submission and cannot be penalized.
- **"GPTQ is a weak bar."** The paper itself cites evidence that GPTQ still yields SOTA results in some regimes (Kurtic et al., 2025), making this a matter of perspective, not a verifiable flaw.
- **"Only one model shown."** Figure 4b shows HPTQ scaling across Qwen3-0.6B/1.7B/4B/8B/14B, so multiple model sizes are in the main text.
- **No SOTA comparisons at all.** The paper states that Section E.5 contains comparisons with other methods. Since the appendix exists in the original submission, we assume this is addressed.

## Novel Insights

Beyond the paper's own contributions, the key novel insight from the review process is that the paper's primary weakness is *not* an error in the theory but a presentation gap: the novelty relative to QuIP is insufficiently delineated, and the experimental evidence in the main paper is too thin to independently support the practical claims. Neither issue invalidates the core theoretical result, but together they lower confidence in the paper's full set of claimed contributions.

## Suggestions

1. In the rebuttal, clearly state what QuIP proved, whether its guarantee is equivalent to the Babai-bound derived here, and what the Babai framing adds — ideally in a dedicated paragraph comparing the two analyses.
2. Add at least one figure showing the gap between the error bound and actual quantization errors across layers to demonstrate the bound is informative.
3. Bring at least one zero-shot benchmark (MMLU, ARC) into the main paper and add at least one recent SOTA comparison to the main figures.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>