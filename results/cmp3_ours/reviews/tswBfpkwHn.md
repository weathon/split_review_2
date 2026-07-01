Here is my final consolidated review:

---

## Summary

This paper provides the first theoretical analysis of SGD training dynamics for a one-layer Mamba model (simplified to linear attention + nonlinear gating) trained for in-context learning on binary classification tasks with outliers. It proves convergence and generalization bounds, showing that Mamba's gating mechanism enables robustness to high outlier fractions at the cost of harder training (larger batches, more iterations). A comparison with one-layer linear Transformers is provided, along with a mechanistic decomposition: attention selects same-pattern examples, gating suppresses outliers and induces exponential local bias. Synthetic experiments verify the key predictions and extend to 3-layer models.

## Strengths

1. **First training-dynamics analysis of Mamba for ICL.** The paper correctly identifies that existing theoretical ICL work focuses on Transformers, while Mamba theory has been limited to loss-landscape global minima (Li et al., 2024b, 2025b). Theorems 1-2 genuinely extend the frontier to Mamba's SGD training trajectory with convergence and sample-complexity guarantees. This gap is real and filling it is a concrete contribution.

2. **Clean mechanistic decomposition.** Corollary 1 (attention selects same-pattern examples) and Corollary 2 (gating suppresses outliers and induces exponential local bias) provide a testable, component-level account of how Mamba implements robust ICL. Experiments in Section 4.2 (Figures 3 and 4) directly verify this decomposition, including for a 3-layer model that goes beyond the paper's theoretical scope, increasing confidence that the mechanism is not an artifact of the one-layer simplification.

3. **Principled comparison framework.** By setting the Transformer's gating to 1 (making gating the only architectural difference between the two compared models), the paper provides an apples-to-apples theoretical comparison that isolates the effect of the gating mechanism. The finding — Mamba is harder to train (larger batches, more iterations) but more robust at test time (α up to p_a l_tr/l_ts vs. α < 1/2) — is non-trivial and conceptually informative.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Underspecified polynomial bounds reduce informativeness.** Several key bounds involve "poly(M_1^{κ_a})" (Theorems 1 and 2, lines 149, 175) without specifying the degree or functional form. Since κ_a (outlier magnitude) appears in the exponent, this effectively means "some very large constant." While not uncommon in theoretical work, this weakens the paper's stated goal of providing "quantitative guarantees" (Section 3.1) — the reader cannot determine how the bounds scale with problem parameters.

2. **Unexplained gap between theoretical sufficient condition and experimental results.** Theorem 2 condition (c) guarantees generalization when α < min(1, p_a l_tr/l_ts). With the paper's experimental setup (p_a = 0.6, l_tr = l_ts = 20), this gives α < 0.6. Yet Figure 2 shows Mamba maintaining error < 0.01 at α = 0.8, well beyond 0.6. Sufficient conditions being loose is expected, but the paper does not acknowledge or discuss this gap. Without discussion, the reader cannot calibrate whether the theoretical comparison is tight for Transformers and loose for Mamba, potentially exaggerating the apparent gap between architectures.

3. **The test-time outlier condition is significantly constrained and its boundaries are not tested.** Theorem 2 condition (a) (equation 11) requires test outliers to lie in the cone spanned by training outliers with total coefficient mass ≥ L > 0. Outliers orthogonal to the training-outlier subspace are not covered. The experiments (v'_3 with coefficients summing to 0.3 at the boundary L=0.3) satisfy the constraint but do not probe the regime where it is violated. The paper could strengthen the analysis by discussing how restrictive this condition is and testing an orthogonal outlier regime.

4. **Trade-off revealed by the CQ experiment (Table 1) is under-discussed.** When outliers are placed closest to the query (CQ setting), Mamba's accuracy drops to 82.73% vs. 93.96% for the linear Transformer. This is a direct consequence of the local bias characterized in Corollary 2 (exponential decay with index distance) and therefore a predicted trade-off of the same gating mechanism that provides robustness in other settings. The paper acknowledges this briefly but could frame it more prominently as an inherent architectural trade-off rather than an incidental weakness. Doing so would turn a vulnerability into supporting evidence for the theory.

5. **The framing overreaches slightly on what "Mamba" means.** The paper reduces one-layer Mamba to equation (3) by setting A = -I, collapsing the selective state-space dynamics to a simple element-wise product. While the paper states this derivation, the framing (title "Can Mamba Learn in Context with Outliers?", abstract's "first theoretical analysis of a one-layer Mamba model") could more prominently and consistently caveat that what is analyzed is a simplified gated linear attention model derived from Mamba under specific assumptions. The gap between the analyzed model and the full Mamba architecture should be more explicitly and prominently stated.

### Trivial
None.

## Nice-to-Haves

- Specifying the degree or form of the polynomial in "poly(M_1^{κ_a})" would significantly strengthen the quantitative claims.
- Discussing the gap between the theoretical α < 0.6 bound and experimental α ≈ 0.8 demonstration would improve the theory's credibility.
- Testing a regime where test outliers violate Theorem 2 condition (a) (e.g., orthogonal to the training outlier subspace) would clarify how restrictive the condition is.

## Removed Points

These points were considered and removed for the reasons given:

- **"The Transformer baseline is a linear attention model, not a standard Transformer"** (Harsh Critic Issue 2): The paper consistently and accurately uses the term "linear Transformer" throughout (Abstract, Sections 1.1, 2, 3.4, Remark 6). The abstract explicitly states "a linear Transformer." Any concern about readers overlooking the modifier is a reader behavior issue, not a paper flaw.
- **"Strong orthogonality assumption"**: The paper follows well-established conventions in theoretical ICL analysis (Huang et al., 2023; Zhang et al., 2023; Li et al., 2024a). This is a generic limitation of nearly all theoretical work in this area, not specific to this paper.
- **"Remark 6 placement"**: A presentation nitpick about ordering within a section.
- **""Unseen tasks" vs "unseen outliers" distinction"**: A minor clarity point that does not affect technical correctness.
- **"No error bars"**: Standard practice for theoretical papers with synthetic verification experiments.
- **"Could discuss violations of orthogonality"**: Same as the orthogonality point above — follows established conventions.

## Novel Insights

The review's most valuable observation is the identification of the CQ (closest-to-query) vulnerability as a predicted trade-off of the gating mechanism (Corollary 2) rather than an incidental failure — and the suggestion that the paper could strengthen itself by deliberately framing this as supporting evidence. This turns the Table 1 result from a limitation into a feature of the theory, which is an insightful reframing the authors should adopt.

## Suggestions

1. Frame the CQ vulnerability (Table 1) as a direct prediction of Corollary 2's local bias characterization, rather than an incidental weakness.
2. Discuss the gap between the sufficient condition (α < 0.6) and the experimental result (α ≈ 0.8), explaining why the bound is loose.
3. Add an explicit list of what architectural features of full Mamba are simplified away (selective SSM dynamics, SiLU activations, convolution kernel, hardware-efficient scan) and a brief justification for why the remaining structure preserves the phenomena of interest.
4. Test a regime where test outliers violate Theorem 2 condition (a) to probe the boundaries of the theory.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>