Now I will produce the final consolidated review.

## Summary

This paper introduces IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transitions to iteratively refine intermediate states during reward-guided generation. The method is formalized within an MTM framework, and the authors provide a convergence proposition (under an explicit reversibility assumption), practical computational optimizations, and empirical evaluations across text (MDLM, LLaDA-8B) and image (MaskGIT) domains with multiple reward functions. The key finding is that iterative refinement at later denoising steps is especially effective for discrete diffusion, in contrast to continuous diffusion where early steps dominate.

## Strengths

1. **Well-motivated problem.** The paper clearly articulates why test-time scaling for discrete diffusion faces distinct challenges from continuous diffusion — no gradient-based guidance, irreversible token assignments, and no natural error-correction mechanism — making a strong case for the need for new methods (Section 1).

2. **Principled theoretical framing.** Casting iterative refinement as a Multiple-Try Metropolis chain is a natural choice for discrete state spaces. The specific noising-denoising kernel K(x_t, x_t') = Σ_{x_s} q(x_s|x_t) p_θ(x_t'|x_s) connects the approach to the predictor-corrector paradigm, and Equations (2)-(3) derive a clean acceptance rule (Section 3.1).

3. **Practical computational optimizations.** The balancing function eliminates the need for auxiliary backward proposals, and the pool-reuse trick on rejection halves the per-iteration cost. These engineering details make the method practically usable (Section 3.3).

4. **Comprehensive empirical evaluation.** The evaluation spans two modalities (text, image), three backbones (MDLM, LLaDA-8B, MaskGIT), and multiple reward functions (CoLA, Toxicity, Sentiment, Perplexity, CLIPScore), which is meaningfully broader than many related papers (Sections 4.2, 4.3).

5. **Informative analytical finding.** The effective-timestep analysis (Table 2) reveals that later denoising steps matter more for discrete diffusion — opposite to the established trend in continuous diffusion — which is a nontrivial insight that could inform future work (Section 4.4).

## Weaknesses

### Fatal
None.

### Major

1. **The convergence guarantee depends on an unexamined reversibility assumption.** Proposition 1 states that IterRef converges to p^*(x_t) as k → ∞ under the assumption that "q and p_θ form a reversible Markov kernel." The paper never discusses whether this assumption holds for actual discrete diffusion models, offers no heuristic argument for why it might approximately hold, and does not discuss what behaviors arise when it is violated. The abstract further claims "proving convergence to the reward-aligned distribution" without the qualification that appears in Proposition 1. This does not invalidate the empirical results (the method may still work well even if the assumption fails), but it means the theoretical framing is weaker than the paper's language implies. The paper is transparent about the assumption in Proposition 1 itself, but the lack of any discussion about its plausibility is a significant gap.

2. **No error bars or measures of variability.** All results (Figure 2, Table 1) are reported as point estimates. Given the evaluation scale (15 prompts × 20 samples = 300 generations per condition for language), variance is a concern that affects the reader's ability to assess whether the reported advantages are statistically reliable.

### Minor

3. **The primary cost metric conflates costs of different magnitudes.** The paper measures compute in NFEs, treating generative-model calls and reward-model calls equally. For LLaDA-8B, a single diffusion forward pass costs vastly more than a toxicity or sentiment classifier. The paper explicitly acknowledges this limitation (Section 3.3, lines 174–175: "aggregating these into a single NFE value may obscure meaningful differences") and refers to Appendix C.4 for wall-clock analysis, but the main results and the "8× faster" claim are presented in NFE, making it hard to assess actual efficiency from the main paper alone.

4. **No diversity or distributional quality metrics.** The stated goal is to "preserve the naturalness of the samples while maximizing reward," but the evaluation measures only reward. Metrics such as self-BLEU, embedding diversity, or KL divergence between sample distributions and the base model's outputs are not reported, so the reader cannot verify whether the method maintains sample quality rather than simply optimizing reward.

5. **The KL temperature α is not reported or ablated.** The parameter α controls the reward-strength tradeoff and appears in the acceptance rule (β = min(1, exp((r(x_t') − r(x_t))/α))) and in the definition of the target distribution. Its value is never stated in the main text, and no sensitivity analysis is provided. This is a consequential hyperparameter, and the omission weakens the evaluation.

6. **No discussion of limitations.** The conclusion (Section 6) summarizes contributions without acknowledging any limitations of the method, which is a notable omission for a new-method paper.

### Trivial
None.

## Nice-to-Haves

- Adding distributional diagnostics (e.g., empirical KL or a similar distance between IterRef outputs and base-model unconditional outputs) would verify whether IterRef actually samples from the intended distribution p^*(x_t) rather than performing uncontrolled reward optimization.
- A sensitivity analysis for the baselines (e.g., showing FK with tuned hyperparameters under this protocol) would strengthen the comparison.
- Increasing evaluation scale or reporting standard errors would improve reliability assessment.

## Removed Points

- **"The magnitude of improvement is suspicious / unfair comparison"** — Removed because it is speculative. The paper states baselines are "favorably configured by following the original papers" (Section 4.1), and the reviewer does not point to concrete evidence of an uneven playing field.
- **Notation mismatches in Equations (line 96, line 113)** — Removed as parser artifacts that do not appear in the original PDF.
- **"Nearly zero cost" claim about noising** — Removed as a reasonable engineering characterization; random remasking is indeed cheap.
- **Wall-clock analysis should be in main paper** — Removed because the appendix exists in the original submission; the paper already references it (Section 3.3, Appendix C.4).
- **Generic speculation about baseline hyperparameters** — Removed; the paper follows standard practice of configuring baselines per their original publications.

## Novel Insights

None beyond the paper's own contributions. The harsh review's key insight — that the reversibility assumption is undiscussed — is valid but does not reveal a dimension of the paper that the authors themselves omitted from their analysis (the assumption is explicitly stated but not justified). The effective-timestep analysis remains the paper's own most novel finding.

## Suggestions

1. Add a brief discussion of the reversibility assumption in Section 3.1: explain what it entails, why it might approximately hold (or not) for absorbing-state discrete diffusion, and what the practical consequences would be if it is violated.
2. Report error bars or confidence intervals for the main results (Figure 2, Table 1).
3. State the value of α used in experiments and, ideally, provide a sensitivity analysis.
4. Include diversity or distributional-quality metrics alongside reward scores.
5. Qualify the abstract's "proving convergence" claim to reflect the conditional nature of Proposition 1.

## Score and Decision

**MY FINAL SCORE:** <score>6</score>
**MY FINAL DECISION:** <decision>Borderline Accept</decision>