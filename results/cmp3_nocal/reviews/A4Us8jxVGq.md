Now I have all the evidence I need. Let me write the final review.

## Summary
2-3 sentence summary of the paper's contribution.

This paper studies how semantic associations emerge in attention-based transformers trained on natural language data. It derives closed-form approximations for the weights (output, value, query-key) at early training, expressing them as compositions of three corpus-derived basis functions—bigram, interchangeability, and context mappings. The theory is validated with remarkably high cosine similarities (≥0.998) in a controlled 3-layer attention-only model, and suggestive evidence is provided via covariance analysis on Pythia-1.4B.

## Strengths

1. **Genuinely novel theoretical result.** The central claim — that weight matrices can be approximated by closed-form compositions of simple corpus statistics — is new and non-obvious. Prior theoretical work either studied synthetic languages (Li et al., 2023b; Yang et al., 2024) or stripped away components like positional encodings, causal masking, and residual streams (Bietti et al., 2023; Tian et al., 2023; Huang et al., 2025). The paper's setup (Definition 3.1) retains all of these, making its analysis meaningfully closer to practice than most prior literature. The specific forms — W_O ≈ B̄, V ≈ Φ̄ᵀB̄ᵀ, W ≈ Q̄ — are concrete and interpretable.

2. **Surprisingly strong empirical fit in the controlled setting.** Table 1 reports minimum cosine similarities of 0.998–0.999 between theoretical predictions and learned weights for the 3-layer attention-only model on TinyStories. These values persist above 0.7 even after 100 epochs (Figure 4). For a leading-term analysis, this level of numerical agreement is unusual and genuinely striking.

3. **The basis functions are interpretable and linguistically grounded.** The decomposition into bigram mapping B̄, interchangeability mapping Σ_{B̄}, and context mapping Φ̄ maps cleanly onto concepts from distributional semantics (Harris, 1954; Firth, 1957). Figure 5 provides concrete examples (e.g., "red" → "truck, balloon"; "fish" → "pond, lake") that make the abstractions tangible. The interpretation of Σ_{B̄} as capturing functional/grammatical similarity and Φ̄ as capturing topical associations is coherent and well-explained.

4. **Attempt to bridge to realistic LLMs.** Most theoretical papers stop at controlled settings. The Pythia-1.4B analysis (Section 5.2), while indirect, demonstrates a methodology for testing theoretical predictions in more complex architectures, and the heatmaps (Figure 6) show measurable agreement especially at early training.

## Weaknesses

### Fatal
None.

### Major

1. **Gap between provable regime and empirical validation.** Theorem 4.1 guarantees the leading-term approximation holds for at most s ≤ η⁻¹·min(5/(8√T), 1/(12L)) gradient steps. For the controlled experiment (η=0.005, T=200, L=3), this is s ≤ **≈5.6 steps** — less than a single epoch with batch size 2048. Yet the paper's key empirical claim is that cosine similarities remain above 0.99 for **30 epochs** (~30,000+ steps) and above 0.7 for **100 epochs** (~100,000+ steps). The paper acknowledges this (line 211: "remain informative well beyond it") but provides no explanation for *why* the approximation persists 3–4 orders of magnitude beyond its provable regime. This weakens the central claim — that the gradient leading-term expansion is the mechanism responsible for the observed structure — because the evidence for the mechanism comes from a timescale the mechanism is not proven to govern. Either the dynamics preserve the leading-term structure through an as-yet-unexplained attractor, or the cosine similarity metric is picking up a coarse stable property that happens to correlate with the leading-term direction without being driven by it. The paper does not distinguish these possibilities.

2. **Pythia-1.4B validation uses substantially weaker methodology than the controlled experiments, and the generalization claim is overstated.** The paper compares covariance matrices of token embeddings (from Pythia) with covariance matrices of the theoretical leading terms (Section 5.2). Covariance matrices can agree while the underlying representations differ by an arbitrary rotation or global scaling. The attention analysis averages over all 32 heads before comparing (line 242), which could wash out head-specific structure. The embedding analysis includes the MLP contribution (which the theory does not model), and the "no-MLP" ablation does not fully separate attention effects because the parallel architecture still mixes them. The paper states the results as though they show the theory "generalizes" to practical LLMs (line 264: "suggests that our analysis on attention-based models generalizes with the addition of multi-head attention or MLP"), but the methodology is too indirect to bear this weight. The agreement could reflect coarse corpus-statistic correlations in both the theory and the model without the specific compositional structure being responsible.

### Minor

3. **Theorem bounds Frobenius norm; empirical validation uses cosine similarity.** The error bounds in Theorem 4.1 are stated in Frobenius norm (Eqs. 5–8), but all empirical validation uses cosine similarity (Table 1, Figure 4). These metrics are not directly related: a small Frobenius-norm error does not guarantee high cosine similarity (if the leading term has small norm, a small additive error can produce a large angular deviation), and high cosine similarity does not imply a low Frobenius-norm error. The paper should discuss how the theoretical bounds connect to the empirical metric.

4. **Theorem proven for full-batch GD; experiments use mini-batch SGD.** Line 84 states the analysis assumes full-batch gradient descent. Line 210 describes training with "SGD using a batch size of 2048." The paper does not discuss how stochastic gradient noise might affect the leading-term approximation, despite the fact that mini-batch sampling introduces variance not captured by the deterministic theory.

5. **No error bars or variance estimates across seeds.** The controlled experiments (Section 5.1) report single cosine-similarity values. For a result that aims to demonstrate a universal theoretical prediction, reporting statistics across multiple random initializations would substantially strengthen the evidence.

6. **No ablation of the theory's components.** The paper shows that the full theoretical predictions match the learned weights, but never tests whether each basis function contributes significantly. For example, does dropping the interchangeability mapping from the Q̄ construction degrade the fit? Such ablations would isolate which aspects of the theory drive the alignment.

### Trivial
None.

## Nice-to-Haves

- The qualitative examples in Figure 5 could be quantified: measuring rank correlation or overlap between the nearest-neighbor lists predicted by theory and those observed in the learned weights.
- The Pythia analysis would be more informative if complemented by a cleaner architectural bridge — e.g., adding multi-head attention to the controlled architecture one component at a time and measuring when the fit degrades.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution.

1. **"Architecture departs substantially from practice" (Critical Issue 3).** The paper is transparent about its architectural choices in Definition 3.1. It explicitly states it follows Nichani et al. (2024) and acknowledges the simplifications. The claim to "minimize the gap" is a comparative statement relative to prior theoretical work, not a claim that the architecture matches deployed LLMs. The paper's scope is clearly stated; evaluating it against full practical architectures exceeds that scope.

2. **"Semantic association used loosely" (Critical Issue 4).** The paper explicitly defines semantic associations on line 15: "statistical and functional relationships between tokens that encode meaning" — and grounds this in distributional semantics (Harris, 1954; Firth, 1957). Under the distributional hypothesis that the paper explicitly adopts, statistical co-occurrence *is* the basis of semantics. The reviewer's objection that the paper should use "distributional association" instead misunderstands the paper's own theoretical framework.

3. **"Missing related works."** Cannot be fact-checked without external sources; removed per instructions.

4. **Formatting/style nitpicks.** Removed per hard rules (parser artifacts, not author errors).

## Novel Insights

The input review's most insight is the identification of a deeper structural issue: the paper claims that the gradient leading-term expansion *explains* the emergence of semantic associations, but the provable regime (~5 steps) is negligible compared to the empirical regime (~30,000+ steps). This creates a gap between the paper's mechanistic claim and the evidence it provides for that claim. The empirical correlation is genuine and striking, but the chain of causality from gradient expansion → learned weights is weaker than the paper suggests for the timescale over which the correlation is asserted. A secondary insight is that the Pythia analysis, while ambitious, uses covariance-based comparisons that are substantially less diagnostic than direct weight comparison and cannot independently validate the compositional structure the theory predicts.

## Suggestions

1. Most importantly, address the gap between the provable regime and empirical validation. Provide an empirical analysis of what happens to higher-order gradient terms over time — do they cancel out, accumulate, or preserve the leading-term direction? Alternatively, prove a weaker condition under which the *direction* (rather than the value) of the weights remains close to the leading term.
2. Connect the Frobenius-norm theoretical bounds to the cosine-similarity empirical metric, or reframe the empirical validation to use a metric more directly tied to the theory.
3. Discuss the implications of using mini-batch SGD rather than full-batch GD for the theoretical predictions.
4. Add variance estimates across multiple seeds for the controlled experiments.
5. Tone down the generalization claims about Pythia-1.4B to match the indirectness of the methodology.

## Score and Decision

This paper makes a genuine and novel theoretical contribution: closed-form, interpretable expressions for transformer weights as compositions of corpus statistics, validated with strikingly high cosine similarities in a controlled setting. The core idea is interesting and potentially influential. However, the central weakness is significant: the theorem's provable regime (~5 gradient steps) is 3–4 orders of magnitude smaller than the regime over which the empirical fit is claimed (30–100 epochs), and the paper provides no mechanistic explanation for this persistence. This does not invalidate the theoretical result itself or the empirical finding, but it weakens the claim that the gradient leading-term expansion is the *mechanism* responsible for the observed structure in the weights. The Pythia experiments, while ambitious, use an indirect methodology that provides suggestive but not decisive support. The paper should be given the opportunity to address this gap, but in its current form the central explanatory claim is not fully supported by the evidence.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>