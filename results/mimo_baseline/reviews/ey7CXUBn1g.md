## Summary
The paper proposes AdaSVD, an adaptive SVD-based compression method for LLMs with two components: (1) adaComp, which compensates for SVD truncation errors by alternately updating the singular matrices U and V^T using Moore-Penrose pseudoinverse solutions, and (2) adaCR, which assigns layer-specific compression ratios based on cosine similarity between layer inputs and outputs as an importance measure. Experiments on multiple LLM families and a VLM demonstrate consistent improvements over SVD-LLM and other SVD-based baselines.

## Strengths
- **Consistent empirical improvements**: AdaSVD outperforms SVD-LLM across all tested compression ratios (40%–80%) on LLaMA2-7B, with particularly notable gains at high compression ratios (e.g., WikiText-2 perplexity of 50.33 vs. 89.90 at 60% compression).
- **Thorough ablation studies**: Table 3 systematically isolates the contributions of adaComp, adaCR, iteration count, and minimum retention ratio, providing clear evidence that both components contribute meaningfully.
- **Generalizability**: The method is evaluated on four LLM families (LLaMA2, OPT, Mistral, Vicuna) and extended to a VLM (LLaVA-7B), demonstrating broad applicability. The integration with GPTQ quantization (Table 4) further shows orthogonality with other compression techniques.

## Weaknesses
### Fatal
None.

### Major
- **Limited novelty in core techniques**: adaComp is essentially alternating least squares (ALS) applied to the truncated SVD factors—a well-established technique in matrix factorization—yet the paper does not acknowledge this connection. The reformulation as a least-squares problem with pseudoinverse solutions is standard numerical linear algebra. This significantly limits the intellectual contribution.
- **Ad hoc importance metric for adaCR**: The layer importance is measured as cosine similarity between input X and output Y=WX. No theoretical justification is provided for why this particular metric captures "importance" for compression, and no alternative metrics are explored. The connection to prior work on layer importance (cited as inspiration from Men et al. and Dumitru et al.) is superficial.
- **Impractical absolute performance at moderate-to-high compression**: At 60% compression, AdaSVD achieves a WikiText-2 perplexity of 50.33 for LLaMA2-7B (original: 5.68). At 80%, perplexity reaches 206.51. The paper does not discuss whether these compressed models are usable in practice, nor does it provide any downstream task evaluation beyond zero-shot QA.
- **No wall-clock or memory measurements**: The paper claims "significantly reduced memory requirements" but provides no actual memory usage or inference latency measurements. Without these, it is impossible to assess the practical benefit of the compression.

### Minor
- **Iteration sensitivity**: Table 3c shows that 1 iteration is optimal at 40% and 60% compression, while more iterations can hurt performance (likely due to overfitting on limited calibration data). This fragility is acknowledged but not well addressed.
- **No comparison with non-SVD methods**: The paper only compares against other SVD-based methods. Comparing with quantization (GPTQ, AWQ) or pruning (SparseGPT) baselines would help contextualize where SVD-based compression stands.
- **VLM evaluation is qualitative only**: Figure 5 shows image captioning examples but provides no quantitative metrics (e.g., CIDEr, BLEU) for VLM performance.

### Trivial
- The stack-of-batch strategy is a minor engineering contribution that simply averages calibration samples to fit within GPU memory.

## Nice-to-Haves
- A discussion of convergence properties or at least empirical convergence plots for the alternating updates.
- Runtime analysis comparing AdaSVD's compensation overhead against the baseline methods.
- Quantitative VLM evaluation metrics.

## Novel Insights
The observation that alternating updates of U and V^T after SVD truncation can effectively reduce compression error is practically useful, even if the underlying technique (ALS) is well-known. The empirical finding that 1 iteration often suffices at lower compression ratios while more iterations help at higher ratios is a useful practical insight for practitioners applying SVD-based compression.

## Suggestions
- Explicitly connect adaComp to the alternating least squares literature and discuss how the contribution lies in the application context rather than algorithmic novelty.
- Provide wall-clock compression time and inference latency/memory measurements to substantiate practical claims.
- Explore alternative importance metrics for adaCR (e.g., based on Fisher information, gradient norms, or reconstruction error) and provide justification for the cosine similarity choice.
- Add quantitative VLM evaluation to complement the qualitative examples.

## Score and Decision
The paper presents a reasonably well-executed empirical study with consistent improvements over SVD-LLM baselines. However, the core techniques lack novelty (ALS is well-known; importance-based ratio allocation is standard in pruning), the absolute performance at practical compression ratios remains poor, and critical practical metrics (memory, latency) are absent. The contribution is incremental rather than transformative.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject