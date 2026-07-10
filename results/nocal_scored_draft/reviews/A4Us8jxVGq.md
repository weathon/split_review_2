## Summary

This paper develops a theoretical analysis of how attention-based transformers learn semantic associations during training. Using a leading-term approximation of the gradient updates, the authors derive closed-form expressions for transformer weight matrices (output, value, query-key, positional) in terms of three interpretable corpus statistics: a bigram mapping (next-token dependencies), an interchangeability mapping (functional similarity between tokens), and a context mapping (longer-range co-occurrence). Theorem 4.1 provides error bounds showing the learned weights are close to these leading-term expressions for O(1/η) steps. The framework is empirically validated on a 3-layer attention-only transformer trained on TinyStories (achieving >0.998 cosine similarity), with additional experiments on Pythia-1.4B.

## Strengths

- **The three basis functions (bigram, interchangeability, context mappings) provide a clean, linguistically grounded decomposition of the features learned by transformers.** The definitions in Eqs. (9–11) are explicit, and Figure 5 confirms they capture interpretable semantic relationships (e.g., 'red' → 'balloon, truck, dress'; 'fish' → 'pond, lake, water').

- **The theoretical predictions are structurally non-trivial:** Theorem 4.1 predicts different weights scale with different powers of steps and learning rate (W_O ∝ sη, V^(l) ∝ s²η², W^(l) ∝ s⁴η⁴), which is a specific dynamical claim about the order in which different weight matrices acquire their leading-term signals.

- **The 3-layer transformer experiments on TinyStories provide remarkably clean quantitative validation:** minimum cosine similarities >0.998 between predicted and learned weights (Table 1), with the agreement persisting (cosine >0.9 at 30 epochs, >0.7 at 100 epochs) well beyond the rigorous theoretical guarantee.

- **The qualitative semantic analysis (Figure 5) validates that each basis function captures distinct and interpretable linguistic relationships** — bigram (next-token), interchangeability (functional roles, synonyms), and context (longer-range co-occurrence) — connecting the theory to concrete linguistic phenomena.

## Weaknesses

### Fatal
None.

### Major

- **Theory-experiment step-count gap:** Theorem 4.1 guarantees the leading-term approximation holds for s ≤ η⁻¹·min(5/(8√T), 1/(12L)) steps. With the experimental parameters (T=200, L=3, η=0.005), this evaluates to s ≤ 5.56 steps. The main experiments validate over 100 epochs, which (with batch size 2048) corresponds to orders of magnitude more gradient steps. The paper acknowledges this ('remain informative well beyond [the early stage]') but provides no argument for why the approximation should persist when the O(s²η²), O(s³η³), O(s⁵η⁵T) error bounds would, at hundreds of steps, dominate the leading-term main effect. The theory does not explain its own central empirical observation.

### Minor

- **Pythia-1.4B validation is indirect:** The methodology replaces direct weight comparison with covariance-matrix comparisons, which is a weaker test — different mechanisms can produce similar covariance structures. The results are reported only as heatmaps without numerical summary statistics (means, confidence intervals), making it difficult to assess the strength of the match. The claim of 'very strong agreement' (line 263) is not clearly supported by the visual evidence, particularly for attention correlations at early training steps.

- **No comparison to simpler baselines:** Table 1 reports cosine similarities >0.998 between learned weights and the theoretical compositional forms. The paper does not compare against simpler alternatives (e.g., the bigram matrix B̄ alone, a pointwise mutual information matrix, or a raw co-occurrence count matrix) to establish that the specific composition of basis functions is necessary rather than any plausible corpus statistic showing similar similarity.

### Trivial

- **The leading-term expansion is not formally defined in the main text.** The paper invokes 'leading-order approximation' and 'gradient leading terms' (lines 29, 88) but does not explicitly state what is being expanded (e.g., a power series in η or a Taylor expansion around initialization). Although the error-bound structure in Theorem 4.1 makes the expansion type implicitly clear, an explicit statement would improve readability.

- **The conclusion slightly overclaims:** 'theoretical foundations of representation learning in transformers' (line 277) is a stronger characterization than warranted for a theory validated on a simplified architecture (shared QK, one-hot inputs, |V|×|V| weights, no MLP, no embeddings) in a limited training regime (~6 provable steps).

## Nice-to-Haves

- Provide numerical summaries (mean ± std) for the Pythia heatmaps in Figure 6, and include confidence intervals or statistical significance tests for the cosine similarity values.
- Compare against simpler baselines (bigram-only, PMI, co-occurrence) in the small transformer experiment to quantify the value added by the compositional form.
- Derive (or numerically demonstrate) why the leading-term approximation tracks the true weights well beyond the proven bound, e.g., by simulating the theoretical leading-term trajectory alongside the actual gradient trajectory for the first several hundred steps.
- Report approximate gradient steps per epoch for the TinyStories experiments so readers can directly compare to the theorem's step-count bound.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *Strength about "Pythia-1.4B validation is ambitious"* — removed because it conflicts with the verified weakness that the Pythia validation is indirect and results are reported only qualitatively.
- *Weakness about "architectural simplifications understated"* — removed because the paper clearly states its architecture (Def. 3.1) and frames its contribution relative to prior work with more restrictive assumptions. The claims about "minimizing the gap" are reasonable in context.
- *Weakness about "leading-term expansion not defined"* — demoted to Trivial since the error-bound structure in Theorem 4.1 implicitly defines the expansion type.
- *Weakness about the MLP hypothesis* — the paper presents this as "one possible hypothesis" (line 265), not a claimed result.
- *Claim that the paper does not explain the process by which weights reach their configuration* — the gradient leading-term analysis is precisely about the training dynamics, i.e., the process.
- *Weakness about the paper claiming self-attention-only models match MLP performance* — this is a single cited remark (cite Wang et al., 2025), not a central claim.
- *Weakness about the "Implication" paragraph being speculation* — the paper's language ("we expect such relationships to be a useful anchor") is appropriately hedged.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's main strengths (clean basis-function decomposition, non-trivial polynomial weight predictions, strong small-scale empirical validation) and its primary limitation (the theory's proven regime covers ~6 gradient steps while validation spans orders of magnitude more steps, without an explanation for the persistence). The conceptual framework is genuinely interesting; the step-count gap is the key unresolved issue.

## Suggestions

- In the main text, explicitly state the form of the gradient expansion (e.g., "we expand ∇L as a power series in η") to clarify the approximation.
- For the Pythia experiments, report quantitative cosine similarity values (mean and range) alongside the heatmaps.
- Add a simple baseline comparison: show cosine(weight, B̄) and cosine(weight, Φ̄^T B̄^T) alongside cosine(weight, theory) to demonstrate that the specific compositional form matters.
- Acknowledge the step-count gap more prominently and either (a) attempt to extend the bound or (b) provide a numerical simulation showing the leading-term trajectory tracks the true gradient descent trajectory.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>