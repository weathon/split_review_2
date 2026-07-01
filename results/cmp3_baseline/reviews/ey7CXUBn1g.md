## Summary

The paper presents AdaSVD, an adaptive SVD-based compression method for LLMs. It introduces **adaComp**, which reduces SVD truncation error by alternately updating the truncated singular matrices \(U\) and \(V^\top\) using Moore-Penrose pseudoinverse updates (rather than naive gradient updates), together with a stack-of-batch strategy to efficiently use more calibration data under memory constraints. It also introduces **adaCR**, which assigns layer-specific compression ratios based on the cosine similarity between layer inputs and outputs. Experiments on LLaMA, OPT, Vicuna, Mistral, and LLaVA models across multiple compression ratios (40%–80%) show consistent perplexity improvements and higher zero-shot accuracy compared to existing SVD-based methods (SVD, FWSVD, ASVD, SVD-LLM).

## Strengths

- **Clear practical improvement at high compression ratios.** AdaSVD significantly reduces perplexity over SVD-LLM at 60%–80% compression on WikiText-2 (e.g., 50.33 vs. 89.90 at 60% on LLaMA2-7B), which is practically important for deployment on memory-constrained devices.
- **Simple and well-motivated components.** The use of Moore-Penrose pseudoinverse to stabilise the U/V update is a natural remedy for the instability of naive gradient-based compensation, and the layer-importance-based compression ratio assignment (adaCR) is intuitive and shown to be effective.
- **Thorough experimental evaluation.** The paper evaluates on multiple LLM families (LLaMA2, OPT, Mistral, Vicuna), multiple compression ratios (40%–80%), language modelling perplexity, zero-shot reasoning, a VLM task, and ablation studies for each component. The integration with weight quantization (GPTQ) further demonstrates orthogonality.
- **Reproducibility-oriented.** The pseudocode is provided, implementation details are given (calibration set size, hardware), and code/models will be released.

## Weaknesses

### Fatal
None.

### Major
1. **The alternating-update claim is not well supported by the ablation.** The ablation in Table 3(c) shows that across 40%, 50%, and 60% compression, a single iteration (\(k=1\)) of the pseudoinverse update gives the best perplexity; increasing iterations (3 or 15) consistently hurts performance. This contradicts the paper’s emphasis on “alternately updating until convergence” (Eq. 16). The method’s actual benefit appears to come from the single pseudoinverse step, not from the alternating scheme. The authors should either reframe the contribution or provide a clear explanation (and evidence) of when/why alternating helps.
2. **Lack of statistical significance.** All results are reported as single numbers without variance or multiple runs. Since the calibration data is randomly sampled (256 sentences from WikiText-2), results may vary across draws. This is especially important for the zero-shot accuracy metrics where differences of 1–2 percentage points could be within noise. The paper should report mean and standard deviation over several seeds, or at least clarify that the procedure is deterministic given the sampled data.

### Minor
- The stack-of-batch strategy averages mini-batches of calibration samples. This effectively reduces the number of distinct calibration samples. The paper claims it allows “utilizing more calibration data”, but it actually collapses \(N\) samples into \(M\) averaged samples. A clearer justification (e.g., variance reduction, or a comparison against simply using fewer samples) is needed.
- The importance metric for adaCR is cosine similarity between input and output activations. While simple, the paper does not discuss alternatives (e.g., loss perturbation, gradient norms) or provide evidence that cosine similarity is a good proxy for sensitivity to SVD compression. A brief justification would strengthen this component.
- The minimum retention ratio (mrr) is a hyperparameter with no principled selection heuristic; the ablation shows sensitivity at higher compression ratios. Practical guidance would be useful.
- Some figures/tables from the PDF extraction appear duplicated (e.g., Figure 1 and its caption) but this does not affect content evaluation.

### Trivial
- No trivial issues worth listing.

## Nice-to-Haves
- Run the main experiments with 3–5 different calibration seeds and report mean ± std for perplexity and zero-shot accuracy.
- Investigate and discuss why the alternating scheme overfits with limited calibration data, and whether a single pseudoinverse update is the core of the improvement.
- Compare adaCR with alternative importance metrics (e.g., Fisher information, loss-based sensitivity).

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Revise the narrative around adaComp to accurately reflect that one iteration of the pseudoinverse update is typically sufficient, and that alternating updates can be harmful unless carefully regularised or applied at very high compression ratios.
- Add a discussion of the computational overhead of the pseudoinverse SVD compared to the initial SVD compression step.
- Provide a simple guideline for choosing the minimum retention ratio (mrr) based on the observed range of layer importance.

## Score and Decision

**Score:** 6

**Decision:** Accept

**Rationale:** The paper presents a practically useful technique that improves SVD-based LLM compression, especially at high compression ratios. The adaptive compensation (adaComp) using a single pseudoinverse update is effective and the adaptive compression ratio (adaCR) further boosts performance. The experimental evaluation is comprehensive. The major weakness is the mismatch between the claimed alternating-update scheme and the ablation evidence, which requires revision but does not invalidate the core contributions. With a corrected narrative and the addition of variance estimates, the paper would be suitable for publication.

MY FINAL SCORE: 6<score>6</score>
MY FINAL DECISION: Accept