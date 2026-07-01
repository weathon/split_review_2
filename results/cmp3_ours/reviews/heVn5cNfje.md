Now I'll write the final consolidated review.

## Summary

This paper proposes High-Entropy Sum (HES), a token-level entropy metric that sums the entropy of only the top 0.5% highest-entropy tokens in a reasoning sequence, to serve as a lightweight quality signal for data selection in LLM reasoning. HES is validated across SFT, RFT, and RL on multiple model families (Qwen3-8B, DeepSeek-R1-Distilled-7B, Qwen3-0.6B) across 9 benchmarks spanning math, code, and STEM. Key results include: (1) in SFT, training on the top 20% HES-ranked data matches full-dataset performance, and pruning the bottom 20% (using top 80%) surpasses it; (2) cross-model transfer where a 0.6B proxy model achieves comparable selection quality to the 8B target; (3) in RL, selecting highest-HES successful trajectories improves over full-batch GRPO.

## Strengths

1. **Well-motivated core idea.** The paper correctly identifies that in long-CoT sequences, global averaging metrics (AvgE, perplexity) dilute signal from the few genuinely uncertain "forking points." HES directly addresses this by focusing on the tail of the token entropy distribution. The intuition is clearly articulated in Sections 1–2 and supported by Figure 1's discriminative analysis.

2. **Broad empirical coverage across paradigms and domains.** HES is tested across three training paradigms (SFT, RFT, RL), on two model families (Qwen3-8B, DeepSeek-R1-Distilled-7B, plus Qwen3-0.6B), across 9 benchmarks in math, code, and STEM. This breadth is a genuine strength that most data-selection papers do not match.

3. **Cross-model transfer result is practically useful.** Table 1 (line 216) shows that HES computed using a 0.6B proxy model achieves comparable selection quality (32.12 avg) to using the 8B target model (31.14 avg), while reducing inference cost by an order of magnitude. This is the paper's most concrete practical contribution.

4. **Sensitivity analysis is responsibly done.** Figures 3–4 (Section 4.4) show HES is not brittle to the high-entropy token ratio, with 0.005 being a reasonable default. The data selection ratio analysis supports the "prune the worst, keep the rest" conclusion consistently.

## Weaknesses

### Major

1. **No variance estimates (error bars, confidence intervals, or significance tests) anywhere in the paper.** Every reported result is a single point estimate (average@16). Several critical comparisons have modest margins that could be within run-to-run noise of a single training run:
   - Table 1: Highest-HES-20% (31.14) vs. Highest-ES-20% (30.92) — a 0.22-point gap.
   - Table 2: Random-20% (30.38) already exceeds Full-Dataset (30.22), suggesting either high variance or dataset quality issues that cannot be diagnosed without repeated runs.
   - Table 6: Pos-High/Neg-Rand (21.30) vs. Full-Batch (20.63) — a 0.67-point gap on a single run.
   
   The paper repeatedly uses "significantly outperforms" (lines 38, 159, 232, 307) without statistical support. Because the paper's central claim is that HES is a **robust metric**, robustness claims require demonstration across runs, not just a single unperturbed execution. This is the most consequential weakness.

### Minor

2. **Missing comparison against lightweight established data-selection methods.** The related work (Section 5) discusses DSIR (Xie et al., 2023), perplexity-based filtering (Wettig et al., 2024; Marion et al., 2023), and other methods. The paper justifies omitting gradient-based methods due to cost (line 389), but DSIR uses n-gram features and is computationally lightweight. Including at least one such baseline would strengthen the claim of being a "unified data selection framework" (line 42) rather than a better heuristic. (Forking-Only [Wang et al., 2025] is included and is the most directly relevant baseline; the gap is the absence of a broader set.)

3. **Framing overclaim: HES does not replace reward signals in RL.** The paper claims HES "obviates the need for costly external reward models" (line 44). In the RL setup (Section 4.3.1), responses are first separated into positive/correct and negative/incorrect pools — this separation *requires* a reward signal (answer verification). HES then ranks within the positive pool only. HES supplements reward signals rather than replacing them. This framing should be calibrated.

4. **Dual role of HES not explicitly clarified.** Figure 1 shows that in mixed correct/incorrect data, incorrect samples have *higher* HES (0.68) than correct samples (0.29) — HES detects *confusion*. Yet in SFT, the paper selects *highest*-HES samples from a pool of *known-correct* demonstrations, where higher HES indicates *complexity*. The paper never explicitly states this distinction: HES operates as a confusion detector across mixed-quality data but as a complexity detector within known-correct data. This can be resolved in revision.

### Trivial

5. **Minor overclaim about "diverse failure modes."** The abstract states that pairing highest-HES positives with random negatives "enables the model to learn both strong reasoning patterns and diverse failure modes." This is inferred indirectly from ablations (Table 6, where curated negatives hurt performance) but never directly measured. A precision issue.

## Nice-to-Haves

- Add a case study showing token-level entropy patterns for a high-HES vs. low-HES correct solution, making the "forking point" mechanism concrete.
- Discuss limitations/settings where HES might fail (e.g., problems where high entropy arises from irrelevant digressions rather than genuine reasoning forks).
- The RFT experiments compare HES against Random, Length, and Difficulty but not against AvgE or ES (as was done in SFT). Including those would make the RFT ablation more complete.

## Removed Points

- **"Medium Difficulty bolding in Table 1"** — This is a formatting artifact from PDF extraction. Removed per Hard Rules.
- **"Training-free label is overclaimed"** — The paper uses "training-free" to mean "no additional model training required," which is standard usage. Removed.
- **"No discussion of failure cases / limitations"** — Moved to Nice-to-Haves since this is a suggestion for improvement, not a weakness.
- **"Related work is thin"** — This is a generic criticism without identifying specific concrete gaps beyond what is already addressed in Weakness #2.
- **"The RL experiment does not show that HES replaces reward signals"** — Retained as Weakness #3 but framed more precisely (it supplements rather than replaces).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add variance estimates:** Run at least 3 seeds for key SFT comparisons (Full-Dataset, Random-20%, Highest-HES-20%, Lowest-HES-20%) on at least one model/dataset pair. This single addition would transform the empirical credibility of the paper.

2. **Include one lightweight established baseline** such as DSIR in the main SFT comparison to show that HES is competitive beyond simple heuristics.

3. **Calibrate claims:** Replace "obviates reward models" with "provides finer-grained ranking within the positive pool after correctness-based filtering." Clarify the dual role of HES (confusion detector vs. complexity detector) in Section 3.1.

## Score and Decision

**Calibration Anchors (all query rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `qUJsX3XMBH` — "Rethinking Data Selection at Scale" | 4.40 | R1 | Weaker: negative result (random is competitive); narrower scope (SFT only) |
| `EOPLy80bBm` — "Disentangling Roles in Data Pruning" | 3.00 | R1 | Weaker: conceptual issues, small-scale experiments |
| `diKRhKs5yl` — "FEEDER" | 5.25 | R1 | Similar: data selection framework, but limited to ICL demonstrations |
| `SpTzsQjgxF` — "Rule-Based Rating and Selection" | 5.75 | R1 | Similar: data selection with missing baselines noted as weakness |
| `I5p1Gm8GFS` — "3DS" | 5.75 | R2 | Similar: data selection for domain adaptation, similar methodology concerns |
| `Fty0wTcemV` — "DELIFT" | 6.00 | R1 | Stronger: submodular optimization, better methodological rigor |
| `ouRX6A8RQJ` — "CoT Through Information Theory" | 6.40 | R2 | Stronger: novel information-theoretic framing, cleaner experiments |

**Round 1 Bracket:** 3.5–6.5, narrowed by comparison to "Rethinking Data Selection" (4.40) and "3DS" (5.75).

**Final Score Determination:** The paper's core idea is stronger than "Rethinking Data Selection at Scale" (a negative-result paper), and its empirical breadth exceeds "3DS" and "Rule-Based Rating." However, the total absence of variance estimates is a deeper evidential gap than what those papers had — they were asked to add error bars/standard deviations, not flagged as fatally missing. This gap, combined with the missing established baselines, places the paper at the lower end of the 4.5–6.0 bracket.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>