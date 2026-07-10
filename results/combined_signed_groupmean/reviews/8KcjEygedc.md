Now let me write the final consolidated review.

## Summary

This paper develops an exact asymptotic theory for oracle-based data pruning in high-dimensional Gaussian binary classification with ridge regression. The authors derive closed-form test-error formulas (Theorem 1) for arbitrary symmetric pruning functions under label-agnostic and label-aware curation rules, characterized by four scalar constants. Theorem 2 identifies when "keep hard" vs. "keep easy" pruning is optimal, depending on generator quality (ρ) and oracle quality (ρ_*). The theory is validated on synthetic data (matching theoretical curves to simulations) and qualitatively on ImageNet (showing the predicted crossover), and the paper draws connections to recent LLM reasoning results (LIMO, s1).

## Strengths

- **Clean, principled theoretical setup.** The generative model (Section 2) is precisely specified: the quality of the data generator (ρ), the pruning oracle (ρ_*), and their alignment (ρ_g) are defined via cosine similarities, giving a clear geometric picture. The distinction between label-agnostic curation (pruning by features only) and label-aware curation (pruning by label correctness + difficulty) captures a meaningful axis of variation in real curation pipelines.

- **Theorems 1-3 deliver exact asymptotic expressions.** Deriving closed-form limiting test error for an arbitrary symmetric pruning function under both curation rules—and showing that the impact of pruning is fully captured by four scalar constants (p, γ, β, β̃)—is a genuine technical contribution. Theorem 2's crisp characterization of when "keep hard" vs. "keep easy" is optimal, though limited to a specific asymptotic regime, is interpretable and connects cleanly to the paper's central question.

- **Qualitative predictions confirmed in synthetic experiments.** Figure 1 shows that the theoretical curves (solid lines) match empirical simulations (dashed lines with error bars) across four regimes (small/large n × strong/weak generator), and the predicted crossover—optimal p < 1 only when data is abundant and the generator is strong—is cleanly reproduced.

## Weaknesses

### Major

- **The paper overclaims in asserting it "explains" LIMO/s1 results.** The abstract, contributions list, and Section 4.2 state that the framework "provides a principled explanation" and "rigorous justification" for LIMO and s1. However, the mapping between the theory's setting (binary classification with Gaussian features, linear ridge regression) and these LLM methods (autoregressive transformers trained with next-token prediction on natural language) is entirely analogical. The theory makes rich quantitative predictions—exact error rates, phase transitions at specific threshold values—that are not tested on LLMs. Only a qualitative pattern (strong generator → keep hard, weak generator → need more data) is compared, and any theory yielding that basic conclusion would be consistent with these observations. The paper should reframe the LLM discussion as a qualitative parallel or speculative connection, not as validation of the theory.

### Minor

- **Theorem 2's optimality result is proven only in a narrow asymptotic regime.** The formal optimality claim holds in the limit φ→0 (data-rich, d/n→0) and λ→0 (unregularized), i.e., the interpolating regime. While synthetic experiments at finite n suggest the result extends more broadly, the formal guarantee does not cover the finite-φ, nonzero-λ settings where methods like LIMO and s1 operate.

- **The ImageNet experiments validate only the qualitative shape, not quantitative predictions.** The theory's parameters (ρ, ρ_*, ρ_g) are not measured or estimated on ImageNet; the experiments simply observe that "keep easy works for small n" and "keep hard works for large n." This is an important qualitative check, but it does not constitute a quantitative test of the theory, and alternative explanations (e.g., pseudo-label accuracy varying with n) are not ruled out.

- **The synthetic experiments conflate pruning rule with pruner informativeness.** In Figure 1, the "keep hard" strategy uses an informative pruner (ρ_g=0.5, ρ_* = ρ) while the "random" baseline uses an uninformative pruner (ρ_* = ρ_g = 0). The observed difference conflates the effect of the pruning rule (hard vs. random) with the informativeness of the pruner (aligned vs. orthogonal). A cleaner comparison would fix pruner quality and vary only the rule.

### Trivial

- **The term "exact scaling laws" is somewhat imprecise.** Theorem 1's expressions require numerical evaluation of Stieltjes transforms and auxiliary functions, unlike traditional scaling laws (Kaplan et al., Hoffmann et al.) which provide closed-form power-law relationships (e.g., L(N) ∝ N^{-α}). The paper provides exact asymptotic formulas, not explicit scaling exponents.

## Nice-to-Haves

- Include a "keep easy" synthetic experiment for the weak-generator (ρ<1) regime to directly test Theorem 2(B)'s prediction that keep-easy is optimal.
- Add a brief intuitive discussion of the qualitative behavior of the functions m, m̃, r in Theorem 1 (e.g., monotonicity in p) to aid reader intuition.
- Provide more experimental detail for ImageNet (architecture, pre-training data, number of random seeds, error bar computation).

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- "Analytical model-collapse result is claimed but not presented": REMOVED. The paper references Appendix C (line 157) for the analytical result; the parser strips appendix content from all papers. The analytical result exists in the original submission and cannot be evaluated from the parsed version.
- "Missing keep-easy comparison in synthetic experiments": Moved to Nice-to-Haves. This would strengthen the paper but is not a core flaw.
- Strength "Timely, well-motivated question": REMOVED as generic/superficial per filtering rules.
- Various formatting/style nitpicks from input review: REMOVED per hard rules.

## Novel Insights

None beyond the paper's own contributions. The reviewers' analyses converge on the paper's own framing (exact asymptotics for pruning in linear classification) without adding fundamentally new observations about the paper's content.

## Suggestions

1. **Reframe the LLM discussion.** Change Section 4.2 from presenting the framework as "explaining" or "providing rigorous justification" for LIMO/s1 to offering a qualitative parallel or speculative connection. This would better align the claims with what the evidence supports.
2. **Add a keep-easy synthetic baseline** for the poor-generator regime to directly test Theorem 2(B).
3. **Clarify Theorem 2's scope** by explicitly noting that the formal optimality result is proven in the φ→0, λ→0 limit, with the synthetic experiments providing empirical evidence for broader applicability.

## Score and Decision

**Round 1 bracket (from calibration):** 5.5–7.5. The paper's closest topical anchors (RMT-based analysis of data pruning in classification, score 5.50; statistical theory of data selection under weak supervision, score 5.50) share the same theoretical paradigm (high-dimensional asymptotics, Gaussian covariates, regularized ERM) and similar weakness profiles: Gaussian assumptions limit practical applicability, and the gap between the toy model and the claimed practical implications is substantial. The paper under review has a *stronger* theoretical contribution than these anchors (Theorem 1 covers *any* symmetric pruning function, not just a specific selection rule) but also a *more severe* overclaiming problem (asserting explanation of LLM results).

**Anchor comparison:**

| Anchor | Score | Key shared high-magnitude items | Key differences |
|--------|-------|--------------------------------|-----------------|
| I9Dsq0cVo9 (RMT synthetic data) | 5.50 | +9.93 "complete analytic theory" / -9.99 "setup not used in practice" | Our paper has broader theory (general pruning functions) but stronger overclaiming |
| HhfcNgQn6p (data selection theory) | 5.50 | +9.99 "biased beats unbiased" / +9.99 "solid math guarantees" / -10.00 "surrogate = Bayes optimal" assumption | Our paper has explicit closed-form expressions vs. qualitative lessons |
| 4vzGQcVUG8 (weak-to-strong generalization) | 6.50 | +8.34 "exact characterization" / -9.93 "main body only one theorem" / -7.53 "details in appendix" | Our paper has more main-text results but looser connection to practice |

**Final score:** 6.0. The paper's theoretical contribution (exact asymptotic analysis of data pruning with general pruning functions) is genuine, technically substantial, and well-validated on synthetic data. However, the paper's central narrative overreaches by claiming to "explain" LLM reasoning results based on a qualitative analogy, and the empirical validation on ImageNet is qualitative rather than quantitative. After correcting the framing (toning down LLM claims), this would be a solid accept. The score reflects a borderline accept: strong theory weakened by overclaiming.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>