## Summary

This paper analyzes how attention-based transformers acquire word associations during training by deriving closed-form approximations of the learned weights via a gradient leading-term expansion. The key theoretical result is that the output, value, and query-key matrices converge at different rates (O(η), O(η²), O(η⁴)) and can be expressed as compositions of three corpus-statistic basis functions: bigram mapping, interchangeability mapping, and context mapping. Experiments on a 3-layer attention-only model (TinyStories) and on Pythia-1.4B show that the theoretical characterizations correlate with actual learned representations.

## Strengths

- **Gradient leading-term analysis reveals non-trivial convergent structure.** The different convergence rates of W_O (O(η)), V (O(η²)), and W/P (O(η⁴)) are a genuinely interesting and non-obvious theoretical finding. It provides a formal explanation for why simple bigram statistics dominate early outputs, with attention-based refinement arriving later — a clear advance over prior theoretical work on transformer training dynamics.

- **The three-basis-function decomposition (bigram, interchangeability, context) is conceptually clean and well-connected to linguistic constructs.** The paper walks through how these basis functions compose across weight matrices (Section 4.2) and illustrates the resulting structure (Figure 2, Section 4.2.3), making the abstraction concrete and interpretable.

- **Per-head analysis (Figure 7) reveals layer-dependent specialization rates.** The finding that layer 2 learns the leading-term features more slowly, layer 13 exhibits faster head specialization, and layer 24 retains leading-term features longer is an empirically grounded discovery that emerges naturally from the theoretical framework.

## Weaknesses

### Fatal
None.

### Major

1. **The theoretical guarantee covers ~5–6 gradient steps; experiments run for 100 epochs.** With the experimental parameters (η=0.005, T=200, L=3), Theorem 4.1's bound gives s ≤ 5.6 steps. The experiments use SGD (not full-batch GD) with batch size 2048 and run for 100 epochs — likely tens of thousands of parameter updates. The paper notes that the characterization "remains informative well beyond" the guaranteed regime, but offers no mechanism or separate analysis for why the alignment persists. This means the experiments do not actually verify the theorem within its validity window, and the observed agreement beyond it is unexplained rather than confirmed. Running a controlled experiment within the guarantee window (full-batch, ≤5–6 steps) and separately documenting the persistence behavior would honestly separate what is proven from what is empirically observed but unexplained.

2. **Full-batch GD theory tested with mini-batch SGD.** Section 3.3 explicitly assumes full-batch gradient descent. The experiments (Section 5.1) train with SGD using batch size 2048. The paper does not address whether the leading-term approximation holds under stochastic gradients or discuss batch-size effects. This is a clear mismatch between the theoretical conditions and the experimental protocol used to validate them.

3. **The architecture analyzed differs materially from practice in ways the paper downplays.** The theoretical model (Definition 3.1) uses (i) no layer normalization, (ii) no MLP layers, (iii) a shared query-key matrix W^(l) (rather than separate Q/K projections), and (iv) one-hot inputs with |V|×|V| weight matrices operating directly in vocabulary space. The paper claims to "substantially reduce the gap between formal analysis and practical use" (Section 2) and describe this as a "realistic architecture," but these are still toy-model simplifications. Pythia-1.4B, used for validation, differs on all four counts. The paper does not acknowledge these gaps as limitations or assess which simplifications are most consequential.

4. **Pythia-1.4B validation methodology is several steps removed from the theorem.** Because Pythia uses different dimensions and architecture, the paper cannot compare weights directly. Instead it: passes single tokens individually through the model → collects embedding covariances → normalizes rows of theoretical matrices to unit norm (discarding scale) → compares cosines of covariance matrices. The connection between this procedure and Theorem 4.1 (which characterizes weight matrices directly) is weak. Covariance of single-token embedding vectors is not the same as the weight matrices the theorem characterizes. The paper acknowledges the need for indirect methodology but the conclusions drawn ("the token representations strongly match our theoretical analysis across all layers") outrun what the methodology can support.

### Minor

1. **No variance or statistical significance reported.** Table 1 reports single "Min. Cosine" values with no indication of run-to-run variation across random seeds or different dataset splits. Figure 4 shows traces but without confidence intervals.

2. **Semantic vs. distributional framing is imprecise.** The paper's title and motivating question (Section 1) foreground *semantic* associations, but what is actually characterized are generic distributional statistics (bigram probabilities, co-occurrence frequencies, previous-token distribution similarities). The paper defines "semantic" broadly as distributional relationships, and Figure 5's caption notes the features capture "both grammatical and semantic structures." However, the consistent "semantic" framing throughout the abstract and introduction — without consistently acknowledging the syntactic/grammatical component — gives an inflated impression of what is being explained.

3. **No ablation of the leading-term approximation itself.** The paper does not characterize how the approximation quality degrades with larger initialization scales, with learning rates outside the η ≥ 1/T regime, or with deeper models approaching the L ≤ √T/4 bound.

### Trivial
None.

## Nice-to-Haves

- A comparison to simple count-based baselines (e.g., directly computing bigram/co-occurrence matrices from the corpus without any training) would clarify what the gradient analysis adds beyond "the model learns corpus statistics."
- Quantitative evaluation of the semantic structure claims (Figure 5) using established word-similarity benchmarks (WordSim-353, SimLex-999) or a downstream probing task would strengthen the evidence that the three basis functions capture semantics specifically, not just co-occurrence.

## Removed Points
- **"The bound for W_O is quite loose":** The relative error within the guarantee window (sη ≤ 0.028) is small (≤ ~2.8%). This criticism does not hold up against the numbers.
- **"Zero initialization not used in practice":** The main Theorem 4.1 uses small Gaussian initialization; zero initialization is a secondary result in the appendix.
- **"Semantic overclaiming — paper doesn't distinguish syntactic from semantic":** The paper's Figure 5 caption explicitly acknowledges "both grammatical and semantic structures," and the paper defines "semantic associations" in distributional terms (Section 1). The criticism overstated the omission.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

1. Run a controlled experiment within the theory's guarantee window (full-batch GD, ≤5–6 steps) with the same model and report cosine similarities there. Then separately document the persistence behavior beyond this window as an empirical observation that the theory does not yet explain.
2. Address the full-batch / mini-batch mismatch explicitly — either extend the theory to SGD, or run the within-guarantee experiment with full-batch GD.
3. Add a limitations paragraph that candidly discusses the architectural simplifications (no LayerNorm, shared QK, one-hot inputs, no MLP) and assesses which are likely to affect the generality of the three-basis-function characterization.
4. Report variance across random seeds for the TinyStories experiments.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>