## Summary

INFO-SEDD introduces a method for estimating KL divergences, mutual information, and entropy for high-dimensional discrete data using Continuous Time Markov Chains (CTMCs) and discrete diffusion models. The core insight connects CTMC theory to information estimation via Dynkin's formula, and a key practical result (Equation 6) shows that a single score model trained on the joint distribution suffices to compute marginal scores when using an absorbing-state rate matrix. The method is validated on synthetic benchmarks, text summarization, and genomics data.

## Strengths

- **Addresses a genuine gap**: MI estimation for high-dimensional discrete data without relying on the problematic "embedding trick" workaround that embeds discrete tokens into continuous space — an approach known to be fragile.

- **Elegant theoretical core**: The derivation connecting CTMCs to KL divergence via Dynkin's formula (Equations 2–5) is original and cogent. The exposition is at an appropriate technical level for the ICLR audience.

- **Single-model property (Equation 6)**: Using an absorbing-state rate matrix to compute marginal scores from a joint model is a practically important insight that avoids training separate score models for the joint and marginal distributions — which would dominate computational cost.

- **Strong synthetic benchmark results (Table 1)**: INFO-SEDD accurately estimates MI at high values (e.g., 47.77±1.18 at MI=50, D=50) where every competitor degrades severely or becomes uninformative. MINE gives 7.21±1.14 at the same setting. Standard deviations are substantially lower across the board. This is clean, convincing evidence.

- **Theoretical error bound (Equation 7)**: The decomposition into estimation error (linear in score approximation error) and truncation bias (exponentially decaying in T) provides structural grounding. While the constants are unspecified, the bound's form is informative and consistent with empirical behavior.

- **Practical applicability via pretrained models**: Fine-tuning existing discrete diffusion models (MDLM-SMALL for text, CADUCEUS for genomics) rather than training from scratch is a genuine practical advantage.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed precision in the text consistency test (Section 4.2, Figure 1)**. The reference MI range (256ρ–303ρ nats) is derived from character-level entropy rate estimates for general English text multiplied by average summary length — a rough order-of-magnitude estimate that the paper itself describes as such (line 130). Claiming INFO-SEDD "closely matches" this reference (line 144) implies a quantitative accuracy the estimate cannot support. The linear trend with ρ is a meaningful sanity check that INFO-SEDD passes, but the framing overstates the evidence. The paper should either reframe this as a consistency check (which it already is) and remove the "closely matches" language, or replace the reference with a principled lower/upper bound.

- **Motif discovery experiment (Section 4.3, Figure 5) is purely qualitative with no quantitative metric**. The TATA-box identification shows a plausible MI peak at the known location (-39 to -26 relative to TSS), but there is no AUC, precision-recall, or comparison to alternative motif-finding methods (e.g., MEME, convolutional classifiers from Umarov and Solovyev, 2017, which are cited but not compared against). The paper's claims are appropriately modest ("INFO-SEDD can effectively locate the TATA-BOX"), but the experiment remains a feasibility demonstration rather than a comparative evaluation. This limits the contribution of this particular experiment.

### Minor

- **No runtime or computational cost comparison with any competitor**. The paper provides no training time, memory usage, or inference speed comparisons. For a new-method paper where INFO-SEDD requires training a discrete diffusion model (simulating CTMCs, computing scores at multiple time steps), this makes it difficult for practitioners to assess the accuracy-compute tradeoff against simpler alternatives. This is addressable in a rebuttal.

- **Architectural asymmetry in comparisons** (line 134). INFO-SEDD uses a discrete diffusion backbone (MDLM-SMALL, CADUCEUS) native to the data modality, while competitors must project tokens through learned embedding layers into continuous space. The paper acknowledges this and claims "similar number of parameters," but the comparison is informative about real-world applicability rather than fundamental algorithmic superiority. Not a flaw in the method, but worth noting when interpreting the results.

- **The theoretical error bound (Equation 7) is structural rather than quantitative**: the constants (C₁, C₂, ε_p, ε_q) are left unspecified, and the linear relationship between score error and KL estimation error is not empirically validated. This is standard for the field but limits the bound's practical informativeness.

### Trivial

- The claim that the method is "unique" (line 210) is slightly overstated given prior work on diffusion-based MI estimation for continuous data (Franzese et al., 2023a; Kong et al., 2022), though the discrete-data focus is genuinely novel.

## Nice-to-Haves

- Provide wall-clock training time and model size comparison with at least one competitor (e.g., GAN-DIME or HD-DIME) on the synthetic benchmark.
- Add quantitative evaluation (AUC or precision-recall) for the TATA-box motif discovery task with a baseline comparison.
- Include a comparison to a simple plug-in discrete estimator at small D (e.g., D=10) to calibrate what INFO-SEDD gains over classical alternatives.
- Provide more explicit practitioner guidance on choosing between INFO-SEDD-J and INFO-SEDD-C (the paper discusses tradeoffs implicitly at lines 184 and 202 but does not distill a clear recommendation).

## Removed Points

These points were raised in the harsh review but are removed or downgraded upon verification:

- **Criticism about missing appendix details for architecture configurations**: Removed because the appendix is stripped by the parser; the paper's claim of "similar number of parameters" stands as stated.
- **Concern about Equation (2) deferring to Lou et al. (2024) for technical conditions**: Removed as standard practice; deferring to prior work for convergence conditions is expected.
- **Speculation about error propagation through the nonlinear function K(a)**: Moved to nice-to-have; a reasonable observation but not a core flaw.
- **Generic "strengthening" suggestions** (reframe text consistency test, add quantitative motif eval, report runtime): Absorbed into the weaknesses above or moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews surface standard evaluation concerns (qualitative experiments, missing compute benchmarks, overclaimed reference estimates) that are typical for new-method papers with real-world demonstrations. No reviewer identified a hidden flaw in the core theoretical derivation or a misinterpretation of the synthetic results, which remain the strongest evidence in the paper.

## Suggestions

1. Reframe the text consistency test (Section 4.2) to honestly acknowledge the crudeness of the entropy-rate-derived reference and remove the "closely matches" language — characterize it as a consistency sanity check rather than quantitative validation.
2. Add a runtime/compute comparison table for INFO-SEDD vs. at least one competitor (GAN-DIME or HD-DIME) on the synthetic benchmark.
3. Add quantitative evaluation (AUC) for the motif discovery experiment or reframe it as a purely illustrative demonstration.
4. Tone down the "unique" claim in the conclusion (line 210) to avoid overstatement.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>