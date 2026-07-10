Now I have all the information needed. Let me compose the final review.

## Summary

This paper proposes High-Entropy Sum (HES), a metric that sums the entropy of only the top 0.5% highest-entropy tokens in each reasoning sample, motivated by the observation that global entropy metrics dilute signal from the critical "forking" tokens in long-CoT reasoning. HES is validated across three training paradigms (SFT, RFT, and RL) on math, code, and STEM benchmarks, consistently outperforming heuristic baselines (random, length, difficulty, average entropy). The small-to-large model transfer experiment (0.6B proxy scoring data for an 8B model) is a practically useful contribution.

## Strengths

- **Well-motivated, targeted metric design (Sections 2.2, 3.1).** The paper correctly identifies why global metrics fail for long-CoT data — signal from critical forking tokens is diluted by the many predictable tokens. Focusing on the top-0.5% highest-entropy tokens is a crisp operationalization of the forking-token concept (Wang et al., 2025), and Figure 1 provides clear visual evidence that HES separates correct from incorrect samples better than AvgE or Entropy Sum.

- **Broad evaluation across three training paradigms (Sections 4.1–4.3).** Most data selection papers focus on a single paradigm. Validating HES on SFT, RFT, and RL is genuinely comprehensive and shows thoughtful adaptation of the metric to each setting (e.g., the asymmetric Pos-High/Neg-Rand design in RL).

- **Small-to-large model transfer is a practical contribution (Table 1, rows with 0.6B and 1.7B proxy models).** Using a 0.6B model to score data for an 8B model achieves comparable results (32.12% vs 31.14% AVG), reducing inference costs by over an order of magnitude. This goes beyond what most data selection papers demonstrate.

- **Consistency across models, datasets, and domains.** Core trends hold for Qwen3-8B and DeepSeek-R1-Distilled-7B, on Open-Math-Reasoning and Open-R1-220k, and on math, code, and STEM benchmarks (Tables 1–4). This breadth strengthens the argument that HES captures intrinsic data structure rather than model-specific artifacts.

## Weaknesses

### Fatal
None.

### Major

**1. No comparison against learned or reward-model-based selection methods, despite claiming to obviate their need.** The paper's abstract (line 9), contributions (line 44), and conclusion (line 393) state that HES "obviates the need for costly external reward models." Yet every baseline tested (random, length, difficulty, average entropy, entropy sum, AvgHE, Lowest-HES) is a zero-cost heuristic. No experiment compares HES against DSIR, LESS, D4, MoDS, or any verification/PRM-based method. The current experiments can only show HES beats simple heuristics — they do not support the advertised claim that HES replaces reward models. Since the paper frames its contribution partly as an alternative to costly methods, this gap is significant. (This is the most consequential weakness because the paper's strongest framing depends on it.)

**2. No statistical significance or variance reporting in any experiment.** Every result table reports a single number per benchmark (average@16). There are no error bars, standard deviations, confidence intervals, or statistical tests anywhere. This matters because many claimed advantages are small in magnitude: e.g., HES-20% AVG 31.14 vs. Highest-ES-20% 30.92 (Δ=0.22, Table 1); RL Pos-High,Neg-Rand 21.30% vs Full-Batch 20.63% (Δ=0.67, Table 6). The paper repeatedly states that HES "significantly outperforms" baselines (Sections 4.1.2, 4.2.2, 4.3.2) without any statistical warrant. For a purely empirical paper, this undermines the reader's ability to assess reliability.

### Minor

**3. RL experiments on a small model with modest absolute gains.** The best RL result (Pos-High, Neg-Rand, 21.30%) improves over Full-Batch (20.63%) by 0.67 percentage points on a 1.5B model (Section 4.3). While the trend is consistent with the paper's thesis, the small model scale and small gain limit confidence that the strategy carries over to the 7B+ scale where RL for reasoning is most impactful. The paper acknowledges this implicitly but does not discuss the limitation.

### Trivial
None.

## Nice-to-Haves

- Add at least one comparison against a learned/reward-model-based selection method to directly support the claim that HES avoids the cost of such methods.
- Provide variance estimates (e.g., bootstrap over the 16 sampling paths used for evaluation) for the main result tables.
- Include a brief qualitative analysis of what HES-selected data looks like (e.g., examples of high-HES vs. low-HES correct solutions).
- The paper would benefit from a limitations paragraph acknowledging that HES requires inference passes (not "training-free" in the strictest sense) and that it measures reasoning complexity, not correctness per se.

## Removed Points

*These points were raised in the input review but removed after cross-checking against the paper. Treat them with caution.*

- **HES as "quality" vs. "complexity" ambiguity.** The paper defines HES as measuring "diversity and complexity of reasoning patterns, indicating a higher learning value" (line 36), and applies it only to correct samples in SFT/RFT, which resolves the tension. The framing could be sharper but is not misleading.
- **Forking-Only comparison is apples-to-oranges.** Both Forking-Only and HES leverage the high-entropy token insight in different but complementary ways. The comparison is informative and not misleading.
- **Medium-Difficulty baseline performance unexplained.** The poor performance of Medium-Difficulty is indeed puzzling, but the baseline is a minor control condition, not central to the paper's claims.
- **RFT Difficulty baseline asymmetrically reported.** Difficulty is only shown for Global Pool (Table 5), not Per-Query. This is a minor presentational inconsistency rather than a selective reporting concern.
- **No discussion of limitations.** The paper discusses limitations of prior methods; the lack of a dedicated limitations section is common at this venue and does not constitute a weakness.
- **Abstract overclaims "matches full-dataset performance."** In Table 2 (DeepSeek model), HES-20% actually *surpasses* Full-Dataset (34.61 vs 30.22). The claim is a reasonable summary.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Narrow the paper's central claim from "obviates costly external reward models" to "outperforms zero-cost heuristic baselines across three training paradigms." This is what the experiments actually support and is itself a respectable contribution.
- Add a limitations paragraph acknowledging that HES requires inference passes for scoring, and that it measures reasoning complexity (not correctness), which is why it is applied only to correct solutions in SFT/RFT.
- Provide bootstrapped confidence intervals or at minimum report variance across evaluation seeds for the main comparisons, especially the small-margin ones.

## Score and Decision

**Calibration summary:**

| Anchor Paper | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| Disentangling Roles of Repr. & Selection in Data Pruning | 3.00 | R1 | Yes | Lower: survey-style, no novel metric; our paper has stronger contribution |
| Rethinking Data Selection at Scale | 4.40 | R1, R2 | Yes | Similar: both about data selection heuristics; ours has novel metric, broader eval |
| Disentangling Reasoning Tokens & Boilerplate Tokens | 4.67 | R2 | Yes | Similar: token-level analysis for fine-tuning; ours broader (3 paradigms vs 1) |
| LLMs are Demonstration Pre-Selectors (FEEDER) | 5.25 | R1 | No | Similar strength, different domain (ICL vs SFT/RFT/RL) |
| 3DS: Medical Domain Data Selection | 5.75 | R1, R2 | Yes | Both propose training-free selection metrics; 3DS had stronger baselines comparison |
| DELIFT: Data Efficient Fine-Tuning | 6.00 | R1, R2 | Yes | Stronger: more rigorous comparison, error bars, clearer scope |
| Combatting Dimensional Collapse via Submodular Selection | 8.00 | R1 | Yes | Much stronger: rigorous theory, extensive experiments, error analysis |

**Bracket (Round 1):** 4.5–5.5. The paper is clearly stronger than survey/analysis papers (3.00) and single-paradigm token papers (4.67), but lacks the experimental rigor of accepted papers like DELIFT (6.00). Its closest peers in contribution type and evaluation breadth are the 4.40–5.75 data selection papers.

**Narrowing (Round 2):** The most damaging weakness (-2.58 favorability for missing learned baselines) pulls the paper down relative to the 5.75 anchor (3DS), which had more complete baselines. However, the paper's strongest strength (13.06 favorability for small-to-large transfer) and broad evaluation across 3 paradigms push it above the 4.40 and 4.67 papers. The lack of variance reporting (-0.96) is an additional gap that the 5.75+ papers typically address.

**Final score:** 5.0. The paper has genuine contributions — a well-motivated metric, broad validation, and a practically useful transfer experiment — but two significant gaps prevent it from being a clear accept: (1) the central framing about replacing reward models is unsupported because no such comparison is run, and (2) the absence of any variance reporting leaves the reader unable to assess whether the (often small-margin) improvements are reliable.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>