Now let me synthesize the results and produce the final review.

## Summary

The paper studies language model pre-training in a data-constrained, compute-unconstrained regime. It proposes evaluating recipes by their loss asymptote (limit as parameters → ∞) rather than by fixed-budget performance. The main empirical findings are: (1) optimal weight decay should be ~30× larger than standard practice for over-parameterized data-constrained training, converting non-monotonic scaling into monotonic power-law improvement; (2) ensembling independently trained models achieves a lower loss asymptote than scaling a single model's parameter count; (3) these recipes compose, with a joint scaling recipe showing improved data efficiency; and (4) distillation can compress these gains into smaller models.

## Strengths

- **Well-motivated and cleanly framed problem (+10.0).** The paper identifies a genuine regime shift (compute grows ~4x/year while web text grows ~1.03x/year, Section 1) and formalizes the asymptote evaluation metric — evaluating recipes by $\lim_{N\to\infty} \mathcal{L}_D(N)$ rather than by fixed-budget performance — which is a natural and useful conceptual contribution for the data-constrained, compute-unconstrained regime.

- **Deliberate evaluation hygiene (+9.4).** The paper states it did not evaluate on any downstream benchmarks until after selecting the best recipes via validation loss (Section 7, line 233). This avoids benchmark-fitting and makes downstream results a genuine test of generalization.

- **Transparent multi-level scaling analysis (+8.9).** The nested approach — fitting scaling laws in $K$ (per $N$), then $N$ (per $D$), then $D$ — is methodologically reasonable for estimating asymptotic performance, and the paper is generally forthcoming about where it is extrapolating vs. reporting measured results.

- **Specific, actionable finding about weight decay (+7.2).** The paper shows optimal weight decay increases with over-parameterization, reaching 3.2 for a 1.4B model on 200M tokens — $30\times$ the standard default of 0.1 (Figure 3 table, lines 97-101). This demonstrably converts non-monotonic (overfitting) scaling into monotonic power-law improvement (Figure 3).

## Weaknesses

### Major

- **Fragile extrapolation from small-scale experiments.** The paper's main experiments use 200M tokens (up to 1.6B in Section 5), while the motivating regime involves trillions of tokens — a gap of roughly 4 orders of magnitude. The data scaling analyses (Section 5, Figures 6-7) are fit to only **four** token budgets (200M, 400M, 800M, 1.6B) using 3-parameter power laws ($A/D^\alpha + E$), yielding only 1 degree of freedom per fit. The central 5.17× figure results from a multi-level nested extrapolation (asymptote in $K$ → asymptote in $N$ → data scaling law in $D$) with no uncertainty propagation across levels. The paper acknowledges data scaling laws are "expected to be noisy" (line 195) but provides no confidence intervals on exponents or numerators — essential for evaluating whether the apparent similarity of exponents across recipes is meaningful rather than coincidental. The 3-parameter power law fits in parameter count ($A/N^\alpha + E$, Section 3) suffer from the same issue: 4 data points, 1 degree of freedom.

- **Self-distillation claim is unsupported.** The self-distillation result (Section 6.2) rests on a single data point (300M teacher → 300M student, 200M tokens). The paper claims this "avoids collapse" and "vastly outperforms" the teacher (line 219), contradicting recent work on model collapse (Shumailov et al., 2024; Dohmatob et al., 2024; Taori and Hashimoto, 2022). No analysis of the mixing ratio $D:D'$, number of self-distillation rounds, or conditions for success is provided. This is a minor sub-result but the claim strength exceeds the evidence.

### Minor

- **Headline number inflates the evidence.** The paper leads with the extrapolated 5.17× data efficiency figure in the abstract and throughout the introduction, while the directly measured result of 3.75× (from a 5-member ensemble of 1.4B models, requiring no asymptotic extrapolation) appears only in a single sentence in Section 5.2 (line 185). This framing presents the most speculative number as the headline contribution.

- **Missing control baseline.** The standard recipe tunes only learning rate and epoch count, with weight decay fixed at the GPT-3 default of 0.1. The regularized recipe additionally tunes weight decay. The improvement (Figure 3, red vs. purple) therefore conflates two changes: the choice of weight decay value and the fact that weight decay was tuned at all. A control that tunes weight decay within the standard recipe search would isolate whether the specific high weight decay values matter.

- **Joint scaling recipe uses heuristic, not tuned hyperparameters.** The joint scaling recipe (Section 4.3) uses a heuristic of "2× epochs and 0.5× weight decay" because the authors "cannot fully find locally optimal hyperparameters due to experimental constraints" (line 143). This adds another layer of approximation to an already nested chain of extrapolations.

- **Limited downstream evaluation.** Evaluation is restricted to three small-scale accuracy-based benchmarks (PIQA, SciQ, ARC Easy), all relatively saturated. The paper acknowledges these are "standard benchmarks for models at our scale" (line 42/229), but the 9% improvement claim should be understood in this limited context.

### Trivial

- The characterization that "existing data-constrained approaches of increasing epoch count and parameter count overfit" (line 17) is imprecise: Figure 2 (left) shows epoching improves loss from 1 to 8 epochs before degrading at 128. The statement should more carefully distinguish the regime where epoching helps from where it hurts.

## Nice-to-Haves

- Add a control baseline that tunes weight decay in the standard recipe's hyperparameter search.
- Report bootstrap estimates or confidence intervals on scaling law parameters (exponents, numerators, asymptotes).
- Provide a simple table reporting training FLOPs for each recipe to clarify compute trade-offs.
- Analyze what high weight decay values do to learned representations (e.g., effective rank, gradient norms) to strengthen the weight decay contribution.

## Removed Points

These points from the input review were removed, with justification:

- **Critical Issue 4 (internal inconsistency about data efficiency persisting):** The critic claimed that if asymptotes are equal the data efficiency ratio must approach 1 at large $D$. This is mathematically incorrect — two power laws $L(D) = A/D^\alpha + E$ with the same $E$ and $\alpha$ have a constant data efficiency ratio $(A_2/A_1)^{1/\alpha}$, independent of $D$. The paper's math on this point is correct. The underlying concern about fit uncertainty is already covered by the Major weakness above.
- **Section note on Figure 2 right non-monotonicity:** An observation about the data rather than a weakness of the paper.
- **Pure formatting or presentation nitpicks** that reflect parser artifacts rather than author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the headline.** Prioritize the measured 3.75× data efficiency (from the 5-member ensemble of 1.4B models) over the extrapolated 5.17×. Present the asymptotic extrapolations as speculative projections with appropriate caveats, not as the primary result.
2. **Add the missing control.** A baseline that tunes weight decay alongside LR and epochs in the standard recipe would cleanly isolate whether high weight decay specifically drives the improvement.
3. **Quantify uncertainty.** Add bootstrap confidence intervals or leave-one-out analyses on scaling law parameters to give readers a sense of stability.
4. **Strengthen the self-distillation result** with at least one additional setting (different model size, token budget, or mixing ratio) and analysis of when it works vs. triggers collapse.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>