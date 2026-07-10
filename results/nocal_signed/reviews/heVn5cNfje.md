Now I have all the evidence needed. Let me produce the final consolidated review.

## Summary

This paper proposes High-Entropy Sum (HES), a training-free metric for data selection in LLM reasoning training. HES sums the entropy values of only the top 0.5% highest-entropy tokens in a reasoning path, focusing on critical "forking points" rather than averaging over all tokens. The metric is validated across three training paradigms (SFT, RFT, RL) on multiple models and benchmarks spanning math, code, and STEM domains. The core finding is that training on HES-ranked data subsets (especially after correctness filtering) consistently outperforms random selection and heuristic baselines, with the notable practical result that small proxy models can select data for larger ones.

## Strengths

- **Well-motivated core idea.** Sections 1 and 2.2 clearly articulate a genuine limitation of average entropy in long-CoT settings: the fraction of truly decision-critical tokens is small, and averaging over the full sequence drowns out their signal. The connection to "forking tokens" (Wang et al., 2025) provides principled grounding. This is the paper's strongest intellectual contribution.

- **Broad experimental validation across three paradigms.** The paper validates HES in SFT (Tables 1–4, ~8 benchmarks each, two base models), RFT (Table 5, 3 selection sizes × 2 sampling modes), and RL (Table 6, 8 strategies). Seeing HES work across three very different training paradigms is genuinely more informative than a deep dive into one, and the consistent signal is compelling.

- **Small-to-large model transfer (Section 4.1.2).** Using Qwen3-0.6B as a proxy to select data for Qwen3-8B achieves 32.12% vs. self-selection at 31.14% (Table 1), reducing inference costs by over an order of magnitude. This is a practically useful, non-obvious result.

- **The RL asymmetric sampling design.** Selecting the highest-HES positive rollouts while pairing them with randomly sampled negative rollouts (Pos-High, Neg-Rand) achieves the best RL performance (21.30%) and surpasses Full-Batch (20.63%). The contrast with Pos-High, Neg-Low (19.50%) yields an insightful finding about the importance of diverse negative examples — constraining negatives to be "easy" harms learning.

- **Lowest-HES control consistently shows catastrophic degradation.** In every table, samples ranked lowest by HES produce near-random performance (SFT: 14.90%, RFT Global Pool: 13.39%). This asymmetry is strong evidence that HES captures meaningful signal, even if its interpretation requires care.

## Weaknesses

### Fatal
None.

### Major

- **No variance or uncertainty quantification.** Every result in Tables 1–6 is reported as a single point estimate with no indication of multiple seeds, confidence intervals, or standard deviations. For the RL experiment specifically, where the claimed gain over Full-Batch is only 0.67 points (21.30 vs 20.63) on a 1.5B model, the difference could plausibly fall within run-to-run variance. While the SFT and RFT gains are larger (e.g., +5.25 points for Highest-HES-20% over Random-20%), the absence of any uncertainty measure weakens confidence in all comparisons and prevents the reader from assessing reliability.

- **Framing issue: the paper's narrative conflates "quality" with "correctness" in a way that obscures what HES actually measures.** Figure 1 and its accompanying table show that HES for incorrect samples (0.68 normalized mean) is more than double that for correct samples (0.29). The paper acknowledges this gap in the figure caption but never reconciles it with the central framing that HES distinguishes "high-quality from low-quality data" (abstract, Section 1). As presented in the text, HES is *inversely correlated with correctness* — it does not directly distinguish correct from incorrect paths. The paper's actual usage (filtering for correctness first, then applying HES within the correct pool) is methodologically valid, but the narrative needs substantial revision. The paper should explicitly frame HES as measuring *reasoning-path complexity among correct solutions* and provide a principled argument for why complex correct solutions have higher training value. The current framing actively confuses a careful reader.

### Minor

- **The "robustness" claim for the high-entropy token ratio (Section 4.4) is overstated for the Math domain.** On AIME24, performance drops 27% (0.457 → 0.335) when moving from the default ratio 0.005 to 0.5. While STEM and Code domains show flat sensitivity (MMLU STEM and LiveCodeBench are invariant across all ratios), the Math domain — which is the paper's primary evaluation focus — shows meaningful sensitivity that happens to favor the extreme low end of tested values. The paper should acknowledge this rather than describing the metric as "robust" without qualification.

- **The SFT "surpasses full dataset" claim is not uniform across benchmarks.** In Table 1, Highest-HES-80% underperforms Full-Dataset on HMMT24 (27.08 vs 28.13) and ties on Oly(H) (6.94 vs 6.94). The average improvement (35.36 vs 32.61) is real, but the text's language ("consistently and significantly outperforms Full-Dataset") slightly overstates the uniformity of the gains.

- **No limitations section.** Given the issues identified in the paper itself (single-run results, threshold sensitivity, the inverse correlation between HES and correctness, small RL model scale), the absence of a limitations paragraph in Section 6 is a notable gap.

- **No comparison with reward-model-based data selection methods.** The paper claims HES "obviates the need for costly external reward models" (Section 1) but compares only against training-free heuristics (length, difficulty, average entropy, random). A quantitative comparison of cost vs. performance against methods like PRM-based selection would strengthen this claim.

- **RL experiments limited to a 1.5B model.** It is unclear whether the asymmetric sampling findings hold at practical 7B+ scales where reasoning systems typically operate.

### Trivial
None.

## Nice-to-Haves

- A qualitative analysis validating that the top-0.5% tokens selected by HES actually correspond to "forking points" (Wang et al., 2025) would strengthen the connection between the metric and its claimed mechanism.
- An overlap analysis showing how much HES-selected samples overlap with length-selected or difficulty-selected samples would clarify whether HES captures genuinely new signal versus being conflated with simpler heuristics.
- An explicit explanation for why incorrect paths have higher HES (e.g., the model generates many high-entropy tokens when uncertain or flailing) would resolve the tension identified in the framing issue.

## Removed Points

These points from the input review were removed with brief justification:

- **"HES-80% surpasses on only 5/8 benchmarks":** Factually inaccurate — it surpasses on 6/8, ties on 1/8, and underperforms on 1/8. The broader point about non-uniform gains is retained in the Minor weaknesses above.
- **"Monotonic degradation in sensitivity analysis":** HMMT25 plateaus at 0.211 for both 0.5 and 1.0 ratios, and STEM/Code domains are flat. The retained weakness correctly notes Math-domain sensitivity without overstatement.
- **"Paper claims 'always surpasses'":** The paper actually says "consistently surpasses" in reference to the average. The retained weakness reflects what the text actually claims.
- **Generic strength claims (e.g., "addressed an important problem"):** Removed for being superficial.
- **"No analysis of what high-entropy tokens correspond to":** Moved to Nice-to-Haves as a qualitative suggestion, not a core weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the narrative.** Lead with HES as a measure of *reasoning-path complexity* that is applied *after* correctness filtering. Explicitly address the Figure 1 finding that incorrect samples have higher HES and explain why this does not undermine within-correct-pool selection.

2. **Add basic uncertainty quantification.** Report results from at least one additional seed per experiment (three total), especially for the RL experiment where the gain over Full-Batch is modest.

3. **Add a limitations paragraph** to Section 6 acknowledging single-run results, the threshold sensitivity in the Math domain, and the small RL model scale.

4. **Soften the "robustness" language** regarding the high-entropy token ratio threshold, or report a wider sweep (e.g., ratios between 0.001 and 0.05) to better characterize the sensitivity.

5. **Consider an RL experiment at 7B+ scale** to test whether the asymmetric sampling finding generalizes.

## Score and Decision

The paper introduces a simple, well-motivated metric and validates it with unusual breadth across SFT, RFT, and RL. The small-to-large transfer result is practically useful, and the RL asymmetric sampling design yields an insightful finding about negative sample diversity. The core weaknesses are (a) a framing problem that conflates what HES measures with correctness, (b) a complete absence of uncertainty quantification across all experiments, and (c) several overclaimed statements about robustness and uniform superiority. The framing issue is fixable through narrative revision, and the model-based comparison and uncertainty quantification are addressable additions. The empirical evidence, while lacking variance estimates, is broadly consistent across paradigms, models, and domains — the directional claims are well-supported even if their precision is unclear. I recommend acceptance with a clear expectation that the authors address the major concerns.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>