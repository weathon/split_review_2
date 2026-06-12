Good. Now I have strong calibration anchors in the 6.0-6.5 range. Let me finalize.

**Reporting:**
- **Round 1 bracket**: 5.5–7.0
- Round 2 anchors narrowed to 6.0–6.5:
  - DELIFT (6.0, Accept): Data efficient fine-tuning across 3 stages. HES paper is more comprehensive across paradigms but comparable in impact.
  - GraphFilter (6.0, Reject): Quality-diversity data selection for SFT. HES has broader validation.
  - STAFF (6.5, Accept): Coreset selection for task-specific fine-tuning. HES is more broadly applicable.
  - CoE self-evaluation (6.0, Accept): Training-free metric for LLM self-evaluation. Similar simplicity.

The HES paper sits at the boundary: its experimental breadth (SFT + RFT + RL + cross-domain + proxy transfer) is unusually strong for data selection papers. However, the conceptual framing issue, lack of statistical testing, and modest RL/RFT margins pull it down. The SFT results are genuinely strong and practical. Final score: **6.5**.

## Summary
This paper proposes High-Entropy Sum (HES), a training-free metric that sums the entropy of the top 0.5% highest-entropy tokens in each reasoning sample to quantify reasoning complexity. HES is applied as a data selection criterion across SFT, RFT, and RL training paradigms, with the central finding that training on HES-curated subsets (e.g., top-80%) outperforms full-dataset training and alternative selection heuristics across multiple benchmarks, models, and domains including math, code, and STEM.

## Strengths
- **Strong SFT results demonstrating "pruning harmful data"**: Table 1 shows Highest-HES-80% (35.36%) surpasses Full-Dataset (32.61%) by +2.75 points on Qwen3-8B-Base. This finding is replicated across model/dataset combinations (Table 2: DeepSeek-R1-Distilled-Qwen-7B; Tables 3-4: code and STEM domains). The Lowest-HES-20% achieving only 14.90% (vs Random-20% at 25.89%) provides strong evidence that HES identifies actively harmful training samples, not merely less useful ones.
- **Discriminative power demonstrated empirically**: Figure 1's table shows HES separates correct (normalized mean 0.29) from incorrect (0.68) samples far better than average entropy of all tokens (0.52 vs 0.53) or average entropy of high-entropy tokens (0.82 vs 0.82), establishing that cumulative entropy at high-entropy tokens captures information that averaging-based metrics miss.
- **Cross-domain generalization**: Tables 3-4 show HES extends beyond math to code (codeforces-cots) and STEM (Llama-Nemotron), with Highest-HES-20% surpassing Full-Dataset by over 3% and 5% respectively.
- **Cost-effective proxy model transferability**: Table 1 shows Qwen3-0.6B proxy HES selection achieves 32.12% AVG when training Qwen3-8B, comparable to 8B self-selection (31.14%), with an order-of-magnitude inference cost reduction—a practical and cost-effective finding.
- **Comprehensive experimental design across three paradigms**: 12+ selection strategies compared in SFT (Table 1), multiple RFT and RL strategies (Tables 5-6), sensitivity analysis across high-entropy token ratios (Figures 3-4), and validation across SFT, RFT, and RL.
- **Insightful RL finding on negative sample diversity**: Table 6 shows curating negative samples hurts (Pos-Rand-Neg-Low: 19.76%, Pos-High-Neg-Low: 19.50%) vs random negatives, while curating positives helps (Pos-High-Neg-Rand: 21.30%), providing a useful mechanistic insight for RL practitioners.

## Weaknesses

### Fatal
None

### Major
- **Conceptual framing conflates reasoning complexity with reasoning quality**: The paper consistently frames HES as measuring "reasoning quality" (abstract, Section 3 heading "Quantifying Reasoning Quality," line 42), but Figure 1 shows incorrect samples have *much higher* normalized HES (0.68) than correct samples (0.29). HES measures reasoning *complexity*, not quality. The actual experimental protocol requires pre-filtering for correctness first, then ranking among correct solutions by HES. The paper never formally states this correctness-precondition as a requirement of the method. While the experiments are sound, this framing is misleading and could cause practitioners to misapply the metric as a standalone quality signal. The paper should reframe as measuring complexity-within-correctness.

- **No statistical significance testing for key claims**: No results include variance, confidence intervals, or multiple-seed runs. Several claims rest on marginal gains: the RL result (Table 6) shows Pos-High-Neg-Rand at 21.30% vs Full-Batch 20.63% (+0.67 points), but individual benchmarks are inconsistent—Full-Batch wins on HMMT25 (15.21 vs 11.88) and GPQA (36.71 vs 35.54). RFT per-query gains at k=2 (31.38 vs 30.37, +1.01 points) are similarly modest. Without error bars from multiple independent runs, it is impossible to determine whether these average improvements represent real effects or run-to-run noise.

### Minor
- **Abstract overstates the primary 20%-SFT result**: The abstract claims "training on just the top 20% of data ranked by HES matches full-dataset performance." In Table 1 (primary setup: Qwen3-8B-Base on Open-Math-Reasoning), Highest-HES-20% achieves 31.14% vs Full-Dataset 32.61%, a 1.47-point gap. This only "matches" on a different model/dataset (Table 2). The abstract cherry-picks the favorable case.
- **RL contribution slightly overstated**: The improvement over Full-Batch is +0.67 points. Additionally, Pos-Difficulty-Neg-Rand (20.27%) and Pos-Longest-Neg-Rand (20.23%) also outperform or nearly match Full-Batch (20.63%), suggesting that simply downsampling positives with any reasonable heuristic helps. HES's edge over other heuristics is modest. The compute-efficiency angle is genuine but should be emphasized over the accuracy improvement.
- **RFT difficulty baseline comparison slightly asymmetric**: In Table 5, the Difficulty baseline uses "medium difficulty" while HES selects "highest complexity"—these are not directly analogous selection directions, making the comparison slightly favor HES.

### Trivial
- **"Forcing-Only" typo in Table 1**: The table labels it "Forcing-Only" which should be "Forking-Only" (as referenced in the experimental design on line 155).

## Nice-to-Haves
- Add correlation analysis between HES and other sample properties (length, difficulty, correctness rate) to clarify what HES uniquely captures beyond existing heuristics.
- Deepen SFT analysis to understand *why* lowest-HES samples are harmful—are they shorter, from easier problems, or template-like?
- Discuss why the 0.005 high-entropy token ratio works better than coarser ratios—the sensitivity analysis confirms it but doesn't explain the mechanism.
- In RL, explore different positive selection fractions (e.g., top-25% or top-75%) to understand the sensitivity of the asymmetric sampling strategy.
- Explicitly compare the Forking-Only baseline (Table 1: 32.51%) with HES-80% (35.36%) more prominently—this cleanly shows that sample-level selection outperforms token-level selection and is a strong result.

## Removed Points
These points are flagged to be removed, treat them with caution.
- "Unified framework" terminology is loose: The paper uses the same HES metric across paradigms with different selection logic. This is a reasonable use of "unified" and is a stylistic nitpick, not a substantive weakness.
- Missing related works: Cannot verify which related works are truly absent from the original submission.

## Novel Insights
The paper's most genuinely novel insight is that among correct reasoning solutions, cumulative entropy at high-entropy decision points (rather than average entropy across all tokens or across high-entropy tokens) is a strong predictor of training value—and critically, that lowest-complexity correct solutions are not merely uninformative but *actively harmful* to training. The evidence for this (Lowest-HES-20% at 14.90% vs Random-20% at 25.89% in Table 1, replicated in Tables 2-4) is strong and counterintuitive, suggesting that data curation for reasoning should focus on removing low-complexity correct solutions, not only filtering incorrect ones. This "harmful noise" finding has practical implications beyond the specific HES metric.

## Suggestions
- Add multi-seed variance (minimum 3 runs) to all headline results, particularly the RL and marginal RFT gains.
- Reframe the narrative: explicitly state that HES measures reasoning complexity among correct solutions, and that a correctness filter is a prerequisite for applying the metric. The current "reasoning quality" framing contradicts the paper's own Figure 1.
- Highlight the Forking-Only comparison (Table 1: 32.51% vs HES-80% at 35.36%) more prominently in the main text—it cleanly shows sample-level selection outperforms token-level selection.
- For RL, frame the main finding as "HES-guided positive trajectory selection achieves comparable or better accuracy with half the data (compute savings)" rather than "significantly surpasses existing methods."

**Score calibration:** Anchors retrieved:
1. KL Divergence GFlowNets (1.0, Strong Reject) — fundamentally different topic, weak paper
2. Systematic LLM Review (1.0, Strong Reject) — survey paper, not comparable
3. Entropy of LMs (3.0, Reject) — entropy metric paper, much weaker
4. Pre-Memorization (4.25, Reject) — reasoning analysis, interesting but limited scope
5. "Random Selection Almost All You Need" (4.4, Reject) — direct competitor, finds random works; weaker contributions than HES paper
6. Rule-Based Rating (5.75, Reject) — data selection framework, weaker primary results
7. 3DS (5.75, Reject) — medical domain data selection, limited domain
8. DELIFT (6.0, Accept) — data efficient fine-tuning across stages, comparable scope
9. GraphFilter (6.0, Reject) — quality-diversity SFT data selection, narrower
10. CoE Self-Evaluation (6.0, Accept) — training-free LLM metric
11. CoT Information Theory (6.4, Reject) — info-theoretic CoT analysis, limited experiments
12. STAFF (6.5, Accept) — coreset selection for fine-tuning, comparable rigor
13. Self-Consuming Training (6.25, Reject) — different topic
14. Putnam-AXIOM (5.8, Reject) — benchmark paper, different
15. DiSF (8.0, Accept) — strong data selection paper with theoretical grounding
16. Synthetic Continued Pretraining (8.0, Accept) — different setting

**Bracket**: Round 1: 5.5–7.0. Round 2: 6.0–6.5.

The HES paper has broader experimental validation than most 6.0 data selection papers (DELIFT, GraphFilter) but less theoretical novelty than STAFF (6.5, accept) or DiSF (8.0, accept). The SFT results are strong and practically valuable, but the conceptual framing issue and lack of statistical testing are meaningful weaknesses. The paper sits firmly in the 6.0-6.5 range, at the accept/reject boundary for ICLR.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <score>Accept</score>