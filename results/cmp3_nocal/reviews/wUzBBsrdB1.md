## Summary

This paper studies the effect of the L0 hyperparameter (average number of active latents per token) in sparse autoencoders (SAEs) for LLM interpretability. Using toy models with ground-truth features, it demonstrates that when L0 is set too low, SAEs mix correlated features together to improve reconstruction, producing polysemantic latents despite looking better on sparsity-reconstruction tradeoff plots. The paper introduces a decoder pairwise cosine similarity metric (c_dec) that detects when L0 is too low, and validates on Gemma-2-2b and Llama-3.2-1b that the L0 suggested by c_dec coincides with peak sparse probing performance.

## Strengths

- **Clean toy-model causal demonstration (Section 3.1–3.2).** The controlled setup with known ground-truth features isolates the effect of L0 from incidental optimization difficulties. The experimental control of initializing a low-L0 SAE to the ground-truth solution and showing gradient pressure pushes it away (Section 3.1) is particularly strong — it proves the problem is structural, not just a local minimum issue.

- **The sparsity-reconstruction tradeoff is shown to be actively misleading (Section 3.3, Figure 4).** The paper demonstrates that at low L0, a ground-truth SAE (correct decoder) achieves *worse* reconstruction (MSE 4.88) than a trained SAE that mixes correlated features (MSE 2.73). This is a non-obvious and impactful result: it shows that if a training method produced perfect SAEs, the standard evaluation plot would incorrectly reject them. This finding holds when comparing different methods at the same L0 (Figure 4 directly compares a trained SAE vs a ground-truth SAE across matched L0 values).

- **Validation on real LLMs with downstream sparse probing (Section 4, Figure 8).** The paper shows that the "elbow" in the c_dec curve (L0 ≈ 200) coincides with peak sparse-probing F1 on both Gemma-2-2b and Llama-3.2-1b. This connects the toy-model findings to practical SAE utility, using a well-established evaluation benchmark (Kantamneni et al., 2025). The inclusion of JumpReLU experiments (Section 4.1, Figure 9) further validates that the pattern generalizes beyond BatchTopK SAEs.

## Weaknesses

### Major

- **The claim that "most commonly used SAEs have an L0 that is too low" is under-evidenced.** This claim appears in the abstract (line 9), the introduction (line 37), and the discussion (line 240). The only support offered is "a cursory search of open source SAEs on Neuronpedia shows L0 less than 100 is very common" (line 240), referenced to Appendix A.13. The paper itself describes the evidence as a "cursory search," which is insufficient for such a sweeping claim about the state of the field. Even if Appendix A.13 contains additional systematic analysis, the main text characterizes it as cursory. This claim would require knowing the correct L0 for each model/layer — which the paper does not establish — and should be substantially weakened or removed to avoid misleading readers.

### Minor

- **Tension between "correct L0" framing and real-LLM complications.** The paper's headline claims ("L0 must be set correctly," abstract line 9) imply a single correct L0 value, but Section 4.2 (line 226) suggests that different latents may need different sparsity levels simultaneously — "the L0 is too high for some latents while simultaneously being too low for other latents." The paper acknowledges this complication but does not reconcile it with the framing in the abstract and introduction. The key results (c_dec elbow matching probing performance) are about identifying a *range* of L0 that avoids the deep low-L0 pathology; the stronger framing about a single "correct" L0 is not fully supported.

- **No sensitivity analysis on the feature orthogonality assumption.** The toy model uses perfectly orthogonal features (line 65: "All are orthogonal"), while the paper acknowledges real LLM features are only "nearly orthogonal" (line 13). The paper does not test how the results degrade as features deviate from perfect orthogonality. Since real features are only approximately orthogonal, understanding this sensitivity would significantly strengthen the claims about real-world applicability.

- **The c_dec metric requires flexible interpretation.** For Llama-3.2-1b, the c_dec curve has a clear global minimum matching optimal probing. For Gemma-2-2b, the global minimum falls in a shallow region, and the authors use the "elbow" instead. The paper handles this honestly, but the need for ad hoc judgment about curve shape (sometimes minimum, sometimes elbow) reduces the metric's precision as a standalone diagnostic.

- **Overcompleteness confound for c_dec not discussed in the main text.** With overcomplete SAEs (h >> d, standard practice), decoder vectors are necessarily non-orthogonal simply because there are more vectors than dimensions in the embedding space. The paper references theoretical justification in Appendix A.6, but the main text does not address this geometric confound, and c_dec's reliability across different dictionary sizes (h values) is not investigated.

- **Single SAE width (h=32768) in all LLM experiments.** The paper does not vary dictionary size. Feature hedging is known to interact with SAE width (Chanin et al., 2025), so whether L0 sensitivity and c_dec's shape change with width is an open question. The practical recommendations would be stronger with evidence across multiple widths.

- **Early toy model results lack variance reporting.** Figures 2–5 show single-run results without error bars or seed variance. Only Figure 6 (c_dec) reports variance across 5 seeds. This makes it unclear whether the striking patterns in the early toy model sections (e.g., "every latent is affected") are consistent or reflect a single run.

### Trivial

None.

## Nice-to-Haves

- The paper could explore whether c_dec can be optimized without a full sweep (the paper mentions this as future work, line 248).
- A more detailed protocol for reading c_dec curves (when to use elbow vs. minimum) would help practitioners.
- The JumpReLU "sticking" phenomenon (Figure 7) is presented as a strength, but it also means JumpReLU SAEs may be harder to tune to a desired L0 — this tradeoff could be discussed.
- Varying the degree of non-orthogonality in toy models would strengthen the claims.

## Removed Points

These points were identified in the input review but removed for the reasons stated:

1. *Criticism that the sparsity-reconstruction tradeoff claim doesn't apply to comparing architectures at the same L0.* **Removed because:** Figure 4 directly compares a trained SAE vs a ground-truth SAE at matched L0 values — this IS a comparison of different methods at the same L0. The reviewer misread the paper.

2. *Section 4.2 decoder projection analysis being "speculative."* **Removed because:** The paper uses appropriately cautious language ("We suspect," "This likely means") and presents it as a hypothesis. This is honest science, not a weakness.

3. *Missing reproducibility details (GPUs, seeds).* **Removed per hard rules:** nitpicks about trivial implementation details.

4. *The c_dec sweep requirement being a "methodological gap."* **Removed because:** The paper already acknowledges this limitation (line 248: "currently requires training a sweep"). It's listed as future work — not a hidden flaw.

## Novel Insights

The most insightful observation to emerge across both the paper and the review is the asymmetry in how too-low vs. too-high L0 corrupts features. The paper shows that low L0 corrupts *every* latent (line 107: "when L0 is too low, every latent in the SAE is affected"), while high L0 still preserves many correct latents. The reviewer rightly pushes on whether a single "correct" L0 is well-defined for real LLMs, and the paper's own Section 4.2 begins to address this by showing that different latents may need different sparsity levels. The most productive direction for future work would be to characterize this per-latent sparsity distribution — perhaps JumpReLU's per-latent thresholds are already learning it.

## Suggestions

1. **Weaken or remove the unsupported claim about "most SAEs."** The paper's core contributions stand without this claim. Replace it with a more precise statement like: "Our results suggest that commonly used L0 values (below ~100) may be in a regime where feature mixing occurs; practitioners should verify their L0 choices using the c_dec metric or sparse probing."

2. **Reframe the central contribution around avoiding the low-L0 pathological regime** rather than finding a single "correct" L0. The data supports the former; the latter is an overreach from toy models.

3. **Add a sensitivity analysis in the toy model** varying the degree of feature non-orthogonality. This would directly address the gap between the toy model's perfect orthogonality and real LLMs' near-orthogonality.

4. **Report seed variance for all toy model figures**, not just Figure 6.

5. **Add experiments with at least one additional SAE width** (e.g., h=16384 or h=65536) to test whether c_dec behavior and optimal L0 shift with dictionary size.

## Score and Decision

**Score:** 6

**Decision:** Borderline Accept

The core empirical findings are sound and valuable: the toy-model demonstration that low L0 causes feature mixing is clean and well-controlled, and the validation on real LLMs (c_dec elbow matching probing performance) provides practically useful guidance. However, the paper significantly overclaims in the abstract, introduction, and discussion — particularly the unsupported assertion that "most commonly used SAEs have an L0 that is too low" — and the framing of a single "correct" L0 is at odds with the paper's own evidence that different latents may need different sparsity levels in real LLMs. The paper would be stronger (score ~8) with these claims corrected.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>