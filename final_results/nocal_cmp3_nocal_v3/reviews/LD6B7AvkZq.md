## Summary

This paper introduces a framework for studying how language models learn context-free grammars through the lens of "subgrammars" — decompositions of a PCFG into its constituent substructures (inner subgrammars from derivation subtrees, outer subgrammars from simplified rule subsets). It proves decomposition theorems showing that the KL divergence of an autoregressive language model from a PCFG can be expressed as a sum over subgrammar contributions, and presents empirical observations including that small transformers learn subgrammars in parallel (rather than sequentially), that subgrammar pretraining improves alignment in attention layers, and that models struggle with recursive depth more than string length.

---

## Strengths

1. **The subgrammar definitions are conceptually novel and well-motivated.** The distinction between inner subgrammars (derivation subtrees) and outer subgrammars (simplified rule subsets) is clean, linguistically plausible, and provides a concrete mathematical vocabulary for studying compositional learning. The connection to Gruska's (1971) grammatical levels is properly acknowledged (line 114).

2. **The parallel-learning observation (Figures 1–2) is genuinely interesting and non-obvious.** The finding that small transformers do not master simpler subgrammars first but instead reduce all subgrammar KL divergences simultaneously is a concrete empirical result that contrasts with a plausible developmental hypothesis. This opens a worthwhile research direction.

3. **The depth-vs-length generalization experiment (Figure 3) is clean and informative.** The contrast between $(a)^i$ (low error) and $(^i$ (increasing error) clearly isolates recursive depth as the primary difficulty, separate from sequence length. The fact this is then checked anecdotally against GPT-5.1 adds texture (with appropriate caveats, line 303).

4. **The paper is clearly written and well-structured.** The theoretical development (definitions → decomposition → recursive case) follows a logical progression, and the paper is transparent about the strength of its assumptions (e.g., calling context-insensitivity a "strong assumption" at line 168).

---

## Weaknesses

### Fatal
None.

### Major

1. **The CKA analysis uses a "top quantile of seeds" without justification (line 250).** The paper selects the best-performing seeds for the cosine-similarity analysis that supports a central empirical claim (that pretraining causes internal representations to reflect subgrammar structure). Without reporting what the other quantiles show, or why this selection is necessary, the reported results could reflect cherry-picking. This undermines the "definitively" language in the abstract. The authors should report the full distribution of results across all 30 seeds, or justify why only a subset is informative.

2. **The empirical evaluation lacks critical details needed for reproducibility.** The paper states it trains "small transformers" and "two-layer transformers" but provides no information about: embedding dimension, number of heads, hidden dimension, parameter count, optimizer, learning rate or schedule, training data generation (how many strings, maximum derivation depth, EOS handling), or how KL divergence is estimated from samples. Grammar definitions are relegated to a stripped appendix. While the paper is primarily theoretical, the empirical component is presented as a central pillar and must be reproducible.

### Minor

3. **Theorem 4.3 is overclaimed relative to its depth.** The paper calls it "the most important contribution of our work" and "a fundamental theorem" (lines 26, abstract), but the result is essentially the chain rule of KL divergence for autoregressive models with terms grouped by subgrammar origin. The grouping is a useful notational contribution that could enable future analysis, but describing it as a "fundamental theorem" about CFGs inflates what is an application of a standard identity. The framing should be calibrated.

4. **The parallel-learning claim lacks a quantitative operationalization.** The paper states "they learn all subgrammars in parallel" (lines 208–210) based on visual inspection of Figure 1. No metric of "parallelness" is defined, no statistical test is applied, and no baseline for what sequential learning would look like is established. Corollary 4.7 gives a sufficient condition that essentially restates the desired property. This weakens what is otherwise an intriguing observation.

5. **CKA results are reported without variance estimates.** Table 1 reports CKA similarities averaged across 30 seeds but gives no standard deviations or confidence intervals. Differences of +8.9% to +21.7% in attention layers cannot be evaluated for significance. Additionally, the MLP-layer changes are small (−0.2% to −4.7%), which the paper does not discuss — this asymmetry between attention and MLP layers may itself be informative.

6. **The "child language" framing (abstract, line 13) is rhetorical rather than operationalized.** The abstract states the finding is "unlike children — who first master simple substructures" — but the paper never defines what a child-like sequential pattern would look like in measurable terms, cites no developmental linguistics evidence for the specific sequential-learning claim, and tests no controlled comparison. This framing adds rhetorical weight without analytical substance. The paper would be stronger without it, or with it explicitly caveated as motivational speculation.

### Trivial
None.

---

## Nice-to-Haves

- **Define a quantitative metric for "parallel learning"** — e.g., variance of per-subgrammar KL convergence times, or a cross-subgrammar interference measure — and validate it on a synthetic setting where sequential learning is forced.
- **Report full distributions** (not just top-quantile) for all seed-dependent analyses, including standard errors or confidence bands for the CKA values in Table 1.

---

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"Theorem 4.6 is not mathematically well-founded"** — The critic argued this is a structural error. However, under the explicitly stated context-insensitivity assumption (Corollary 4.5), the ground-truth distribution over recursive S-occurrences equals P_G by definition of the PCFG, and the model's conditional distribution equals its unconditional distribution by the context-insensitivity assumption. The autoregressive factorization of KL divergence allows additive decomposition, making the linear recurrence and denominator (1−𝔼[R]) mathematically well-founded. The derivation for the running example (S → x / S → (S and S)) is consistent with this reasoning. The critic's objection misunderstands how KL divergence decomposes under recursion in autoregressive models. This is not a valid weakness.

2. **"Tables/figures referenced but missing"** — The critic noted Figure 5, Figure 6, and Table 3 as missing. These are parser-stripping artifacts (likely in the original appendix); they are not author errors.

3. **"Child language comparison not operationalized" (as a separate weakness)** — This is a motivational framing device, not a central claim being tested. Criticizing it as a missing experiment is scope creep. The observation about parallel learning stands on its own empirical merits regardless of the child comparison.

---

## Novel Insights

The most interesting critical insight is that the parallel-learning observation, while visually striking, lacks a proper quantitative definition. Without a metric for "parallelness" and a baseline for what sequential learning would look like, the claim rests on visual inspection alone. This is a concrete gap the authors could address by defining convergence-based metrics (e.g., measuring whether one subgrammar's KL stabilizes significantly before another's). The CKA "top quantile" issue is likewise a concrete methodological concern that a rebuttal could plausibly clarify or fix by reporting full distributions. No deeper structural flaw emerges from the review.

---

## Suggestions

1. Report full CKA distributions (all 30 seeds) for Table 1 with standard deviations, and either justify or remove the "top quantile" selection in the cosine-similarity analysis.
2. Add a quantitative metric for parallel learning (e.g., per-subgrammar convergence times or cross-subgrammar KL variance) to support the visual claim.
3. Temper the language around "fundamental theorems" and "definitively" to better match the scope of what is shown.
4. Provide basic experimental details in the main paper (even a short paragraph on architecture and training setup) for reproducibility.
5. Either remove the child-language comparison or ground it with a clear, testable prediction.

---

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>