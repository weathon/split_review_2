Now let me finalize my review with the calibration anchors clearly listed.

## Summary

This paper develops a theoretical framework analyzing data curation (pruning) in high-dimensional ridge regression for binary classification. It derives exact asymptotic test error formulas under label-agnostic and label-aware pruning rules, proving that the optimal strategy—keep hard vs. keep easy examples—depends on the generator's quality (ρ). When the generator is strong (ρ→1), keeping hard examples is optimal; when it is weak (ρ<1), keeping easy examples wins. The theory is verified on synthetic data matching the model, validated on ImageNet (showing the predicted crossover and model collapse mitigation), and connected interpretively to recent LLM reasoning results (LIMO, s1).

## Strengths

1. **Clean, actionable theoretical insight (Theorem 2).** The paper distills a non-trivial RMT analysis into a crisp condition: optimal pruning flips from "keep hard" to "keep easy" as generator quality degrades. This sharpens intuition beyond prior work (Sorscher et al., 2022) and gives practitioners a clear decision rule.

2. **Technically substantial derivation (Theorem 1).** Deriving exact asymptotic test error under *data-dependent* pruning—where the pruning operator deforms the spectral distribution of the design matrix—is a genuine technical achievement. The Stieltjes-transform deformation approach is non-trivial and represents real progress in high-dimensional learning theory.

3. **Model collapse mitigation result (Figure 3).** The demonstration that "keep hard" pruning stabilizes iterative pseudo-labeling across multiple rounds, while training on all data degrades, is empirically striking and practically consequential. This goes beyond existing work (which mostly studies detection/correction of collapse) by proposing a theoretically grounded prevention mechanism.

4. **Honest limitations section.** The paper explicitly acknowledges the gap between its Gaussian-linear model and real-world structured data, notes the absence of non-linear predictors and multi-epoch training, and identifies three concrete future directions.

## Weaknesses

### Major

**1. Overclaiming on the LLM connection.** The paper frames its LLM discussion (Section 4.2) as providing "a rigorous justification" (abstract, contribution bullet 3) and "explanation" (conclusion: "are not coincidences but follow from fundamental properties") for LIMO/s1. In reality, Section 4.2 contains zero experiments by the authors—it reproduces tables from prior papers and offers post-hoc interpretation. The phrase "Our theory resolves this cleanly" (line 204) treats narrative consistency as evidence. While a theoretical framework *can* suggest plausible explanations, calling this "rigorous justification" and claiming to have "empirically confirm[ed]" the theory on this setting conflates interpretation with evidence. This is the paper's most significant weakness and should be addressed by reframing the LLM discussion as a suggestive connection that requires controlled experimental testing.

**2. Theorem 2 assumes an excellent pruner without discussing practical implications.** Both parts of Theorem 2 condition on ρ_* → 1 (the pruning oracle is excellent). This is stated in the theorem, but the paper never discusses what happens when the pruner is imperfect (ρ_* < 1), which is arguably the more common real-world scenario. The central actionable claim ("when the generator is strong, keep hard; when it is weak, keep easy") therefore applies only when the oracle is near-perfect. The practical scope of the main theoretical result is narrower than the paper's narrative suggests, and this limitation should be prominently discussed rather than buried in the theorem precondition.

### Minor

**3. ImageNet experiments under-specified in the main text.** Section 4.3 does not specify the architecture used, how difficulty/hardness was operationalized (margin? loss? softmax confidence?), how pseudo-labels were generated, or what the error bars represent. The paper references Appendix B for details, but the main text's sparseness makes it difficult to assess whether the results genuinely validate the theory or are artifacts of a particular implementation. Adding at least the architecture, difficulty metric definition, and error bar explanation to the main text would substantively strengthen the paper.

**4. The unified oracle model conflates separate operations.** The label-aware pruning rule (Eqn 6) uses a single oracle vector w_o that simultaneously determines both correctness verification and difficulty scoring. In actual LIMO/s1 pipelines, these are decoupled (e.g., a final-answer checker for correctness, a separate difficulty metric). The paper does not discuss how faithfully this abstraction captures the actual pipeline, leaving a gap between the mathematical model and the systems it claims to explain.

**5. Theorem 2 optimizes over q for a fixed pruning fraction p.** The optimality result assumes p is fixed first; the paper does not discuss whether the optimal fraction p itself depends on the strategy. In practice, one needs to know both *which* examples to keep and *how many*, and these decisions may interact.

### Trivial

**6.** The Marchenko-Pastur "deformation" referenced in Theorem 1 is not explained in the main text. A one-sentence description of what m, \tilde{m}, and r represent (e.g., "m is the Stieltjes transform of the limiting spectral distribution of the pruned sample covariance matrix") would help non-specialist readers.

## Nice-to-Haves

- Run a controlled small-scale LLM experiment (e.g., on GSM8K or MATH) testing whether the predicted crossover between keep-hard and keep-easy holds as generator quality varies. This would transform the LLM section from interpretive commentary into genuine validation.
- Include a simulation sweep over ρ_* < 1 to characterize the sub-excellent-pruner regime, which is the more practically relevant setting.
- Add a "keep easy" curve to the bottom-left panel of Figure 1 (strong generator, large n) to directly test whether keep-hard outperforms keep-easy as Theorem 2 predicts, rather than only comparing keep-hard vs. random.

## Removed Points

The following points from the harsh review were removed with justification:
- **"Issue 4 — synthetic experiments do not validate practical relevance"**: Removed as scope creep. Synthetic experiments are explicitly for mathematical verification of asymptotic formulas; external validation is on ImageNet. This is standard practice for theory papers.
- **"Section 5 — paper does not articulate clear difference from Sorscher et al."**: Removed because the paper states it provides "theoretical justification for the improved scaling behavior," which is a clear articulation of the difference.
- **"Section 4.2 — base model achieves 16.5% on AIME and 1.0% on hard AIME, not a strong generator"**: Removed because this misreads the argument: the paper's point is that the same model can be a strong generator for average questions (ρ high) and a weak generator for hard questions (ρ low), which is internally consistent.
- **Criticisms about missing appendix content or deferred proofs**: Removed per the hard rule that the parser strips appendix sections.
- **Formatting, grammar, or typo nitpicks**: Removed as parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the LLM discussion (Section 4.2) from "rigorous justification" / "explanation" to "suggestive connection that future work should test via controlled experiments." Remove "empirically confirm" from contribution bullet 3 with respect to the LLM connection.
2. Add a prominent discussion of the ρ_* → 1 assumption's practical implications, ideally with a figure from simulations sweeping ρ_* < 1.
3. Add the architecture, difficulty metric definition, and error bar interpretation for the ImageNet experiments to the main text.
4. Add a one-sentence explanation of the Stieltjes-transform deformation in the main text to help non-RMT-specialist readers.

## Calibration Anchors

All anchors retrieved from the human-reviewed corpus at `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`.

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| nSDOkm0SKo.md (unrelated financial NN) | 1.00 | R1, <1.5 | Far weaker — no theoretical contribution, flawed methodology |
| bEgDEyy2Yk.md (minimax path impl.) | 1.00 | R1, <1.5 | Far weaker — implementation paper, no learning theory |
| EOPLy80bBm.md (disentangling representations) | 3.00 | R1, 1.5–3.5 | Weaker — empirical comparison study without novel theory |
| e2F0mJJeN0.md (GM matching for pruning) | 3.00 | R1, 1.5–3.5 | Weaker — heuristics without exact theoretical characterization |
| Bk13Qfu8Ru.md (severing spurious correlations) | 3.80→7.00 | R1, 3.5–5.5 | Mixed scores; accepted paper with empirical rather than theoretical contribution |
| 9ccZzuix2D.md (distilling knowledge in pruning) | 5.33 | R1, 3.5–5.5 | Weaker — empirical study with limited theory |
| FT4gAPFsQd.md (how sparse can we prune) | 6.00 | R1, 5.5–7.5 | Comparable theoretical depth (phase transitions in pruning) but less actionable result |
| nxnbPPVvOG.md (flat minima / Gauss-Markov) | 5.67 | R2, 5.5–7.5 | Comparable style (RMT analysis of ridge regression) but narrower scope |
| Jc0FssXh2R.md (feature learning criterion) | 6.25 | R2, 5.5–7.5 | Comparable theoretical contribution in high-dimensional learning theory |
| VoI4d6uhdr.md (bias amplification theory) | 7.00 | R2, 5.5–7.5 | Comparable methodology (RMT for ridge regression); better empirical validation but less crisp actionable theorem; slightly stronger overall |
| et5l9qPUhm.md (strong model collapse) | 8.00 | R1, 7.5–8.5 | Stronger — similar theoretical style (RMT + model collapse) with more thorough real-data validation and no overclaiming issue |

**Initial bracket (Round 1):** 4.0–7.0, narrowed to 5.5–7.5 after inspecting mid-range anchors.

**Narrowing (Round 2):** Compared against anchor papers at 5.67–7.00. The paper's theoretical depth is comparable to the 6.0–7.0 range. The overclaiming on LLM connection and unaddressed excellent-pruner assumption prevent it from reaching the 7.0 level of "Bias Amplification," while the genuine theoretical novelty places it clearly above the 5.33–5.67 range.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>