Now I have all the calibration data I need. Let me finalize the review.

## Summary

This paper introduces HES (High-Entropy Sum), a metric that sums the entropy of only the top ~0.5% highest-entropy tokens in a reasoning trajectory, rather than averaging across all tokens. The insight is that critical decision points ("forking tokens") are drowned out by trivial tokens under global averaging. HES is applied to data selection across SFT, RFT, and RL training paradigms. The SFT results are the strongest contribution: training on the top 80% of data ranked by HES consistently outperforms training on the full dataset (35.36% vs 32.61% average accuracy on math/STEM benchmarks), across two model families, two datasets, and two non-math domains.

## Strengths

- **Simple, well-motivated idea with strong empirical payoff.** The insight that averaging entropy over long reasoning chains drowns out signal from critical decision points is clearly articulated and backed by strong evidence. The SFT results (Table 1) are the strongest evidence: Highest-HES-80% achieves 35.36% average accuracy vs. Full-Dataset at 32.61% — a meaningful gain that holds across two model architectures (Qwen3-8B, DeepSeek-R1-Distilled-7B), two training datasets, and two non-math domains (Code, STEM).

- **Unified framework across three training paradigms (SFT, RFT, RL).** Most data selection methods target a single paradigm. Demonstrating that the same cheap-to-compute metric works for data pruning, response selection, and asymmetric RL sampling is a genuine contribution. The RL asymmetric strategy (Pos-High, Neg-Rand) properly separates the role of positive and negative sampling.

- **Small-to-large model transfer is cost-effective and convincingly demonstrated.** Using Qwen3-0.6B to score data for training Qwen3-8B yields performance (32.12%) comparable to the 8B's self-selection (31.14%), while reducing inference costs by over an order of magnitude. This is a practical contribution that makes the method more useful.

- **Thorough baseline coverage.** The SFT experiments compare against 11 baselines including length, difficulty, multiple entropy variants (AvgE, AvgHE, ES), absolute vs. relative threshold, forking-only gradient updates, and both random and lowest-HES controls. This coverage makes the main result more convincing.

## Weaknesses

### Fatal
None.

### Major

1. **Framing inconsistency between theoretical claims and empirical evidence.** The paper claims (Section 3.1) that "A higher HES_relative score indicates the successful navigation of more numerous and intense forks, which represents higher quality." However, Figure 1 shows that incorrect samples have substantially higher normalized HES (0.68) than correct samples (0.29). If HES directly measured reasoning quality, the opposite would be expected. The metric actually measures reasoning complexity/uncertainty — and *within correct-answer subsets*, higher complexity correlates with better training signal. The paper never reconciles this tension, overstating what HES measures. The practical application (always applying HES within correct-answer subsets) is sound, but the theoretical framing needs correction.

2. **No statistical significance or variance reporting anywhere.** Every result in Tables 1–6 is a single point estimate with no error bars, standard deviations, or significance testing. Several head-to-head comparisons are close enough that sampling noise could reverse conclusions: e.g., Highest-HES-20% (31.14) vs. Highest-ES-20% (30.92) in Table 1 (0.22 point gap); Full-Batch (20.63) vs. Pos-High-Neg-Rand (21.30) in Table 6 (0.67 point gap). Pass@1 over 16 samples per problem enables straightforward bootstrapped confidence intervals. Their absence makes it impossible to assess which comparisons reflect genuine signal vs. noise, especially for the RFT and RL results where gains are more modest.

### Minor

3. **The RFT results show only modest gains.** In Table 5 (per-query setting), average gains over Random are +1.01 (k=2), +1.69 (k=4), and +0.97 (k=8) percentage points. Length-based selection often comes within 0.5–1.0 points of Highest-HES (e.g., k=2: Length 30.27 vs. Highest-HES 31.38). The paper uses "significantly" in the colloquial rather than statistical sense, which is misleading given the absence of variance estimates (Major Weakness #2).

4. **The computational cost of HES is understated.** The paper repeatedly calls HES "training-free" and contrasts it against "costly external reward models," but computing HES requires: (a) a forward pass of the scoring model on every token of every candidate response, and (b) the full softmax distribution over the vocabulary at each position to obtain per-token entropies. This is essentially the same cost as generating the response itself. The paper should acknowledge and quantify this overhead.

5. **Sensitivity analysis for the key hyperparameter (high-entropy token ratio p) tests only four values:** 0.005, 0.05, 0.5, and 1.0. This sparse grid makes the optimal value's sharpness unclear — values like 0.001 or 0.01 could potentially perform better. The claim that 0.005 is optimal should be qualified as "best among the tested values."

6. **The Forking-Only baseline (token-level reweighting) achieves 32.51 vs. Full-Dataset at 32.61** (Table 1), nearly matching the benefit of HES-based pruning. This deserves more discussion — it suggests an alternative interpretation that the signal is at the token level rather than the sample level, which is consistent with but not uniquely supportive of the paper's sample-level selection framework.

7. **No discussion of data contamination.** The training datasets (Open-Math-Reasoning, Open-R1-220k) include large web-scraped math collections that may contain AIME/HMMT/Olympiad problems used as evaluation benchmarks. Given that the paper's main claim is that HES selects better data, if evaluation problems appear in training data, the metric could inadvertently select memorization-friendly samples. The paper should at minimum acknowledge this and discuss deduplication steps taken.

### Trivial
None.

## Nice-to-Haves

- A qualitative analysis showing examples of high-HES vs. low-HES correct responses, illustrating what kind of reasoning trajectories HES preferentially selects.
- Expanding the sensitivity analysis for the high-entropy token ratio to finer granularity near p=0.005.

## Removed Points

*These points were raised by reviewers but are excluded from the main weaknesses for the following reasons:*

- **Distinction between productive vs. unproductive forking**: Too speculative to count as a concrete weakness — there is no evidence that differentiating these would change the method's design or results.
- **Testing HES in answer-verification-free RL**: Outside the paper's stated scope (the paper focuses on settings with verifiable answers).
- **Request for qualitative analysis of selected data**: A nice-to-have, not a required element for the paper's contribution.
- **Claim that "the RFT results partially undermine the paper's core claims"**: The SFT results are the paper's strongest claim and are not undermined by modest RFT results; this overstates the issue.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's strengths (simple, effective, broadly applicable metric) and identify correctable framing and reporting gaps, but do not surface a fundamentally novel perspective that the paper itself misses.

## Suggestions

1. **Reframe HES as a measure of reasoning complexity/exploration among correct solutions**, not an absolute quality metric. This resolves the contradiction with Figure 1 and makes the theoretical framing consistent with the empirical design.
2. **Add bootstrapped confidence intervals or variance estimates** across random seeds to all main tables, especially for the RFT and RL results where gaps are small.
3. **Acknowledge and roughly quantify the computational overhead** of computing per-token entropies relative to the baselines.
4. **Add a brief discussion of potential training/evaluation data overlap** and any deduplication measures taken.
5. **Qualify the high-entropy token ratio optimal value** as "best among tested values" and consider finer-grained evaluation.
6. **Discuss the Forking-Only result** more explicitly, clarifying whether HES-guided pruning and token-level reweighting capture the same underlying signal.

## Score and Decision

### Calibration Anchors

| Path | Avg Human Score | Round | Itemized | Comparison |
|------|----------------|-------|----------|------------|
| 5kMwiMnUip.md (jailbreaking) | 1.40 | R1 | No | Completely different topic; far weaker contribution |
| 8QTpYC4smR.md (survey) | 1.00 | R1 | No | Survey paper, not comparable |
| mfTM4UdYnC.md (logic games) | 2.50 | R1 | No | Tangentially related; far weaker |
| EOPLy80bBm.md (data pruning study) | 3.00 | R1, R2 | Yes | Systematic study of existing methods; lower novelty than HES |
| t15cWqydys.md (logit-based selection) | 3.00 | R2 | No | Related but more narrow focus |
| qUJsX3XMBH.md (random selection) | 4.40 | R1, R2 | Yes | Negative result paper; HES has stronger positive results |
| cijO0f8u35.md (scaling analysis) | 5.25 | R3 | Yes | SFT/RFT scaling; HES has broader experiments |
| SpTzsQjgxF.md (rule-based selection) | 5.75 | R1, R2 | Yes | Rule-based data selection; HES metric simpler and more elegant |
| Fty0wTcemV.md (DELIFT) | 6.00 | R2, R3 | Yes | Data selection across fine-tuning stages; comparable scope and quality |
| GtpubstM1D.md (math reasoning) | 5.71 | R2 | No | Training recipe paper; HES has more focused contribution |
| 1hQKHHUsMx.md (pretraining data) | 6.75 | R2, R3 | Yes | Analysis paper about reasoning data; deeper questions but narrower experiments |

### Score Determination

**Round 1 bracket:** The paper is clearly above the 3.0–4.4 range (descriptive studies/negative results) and sits in the 5.5–7.5 band. Compared to the strongest anchor in the middle band — DELIFT (avg 6.00) — the HES paper offers a simpler metric and stronger SFT evidence (beats full dataset), but has a more significant framing coherence problem and lacks any variance reporting.

**Round 2 narrowing:** Comparing itemized favorability against DELIFT (6.00) and the pretraining data paper (6.75): the HES paper's strengths (favorability 11.2–12.0) are comparable to DELIFT's (10.5–11.8) and the pretraining paper's (11.4–13.2). However, the HES paper's most negative weakness (framing inconsistency, favorability -0.77) is more severe than DELIFT's weakest items (lowest at -0.29). The framing issue and complete absence of variance estimates prevent this paper from reaching the level of the 6.75 anchor, but the strong SFT contribution and unified paradigm treatment place it above the 5.75 anchor.

**Final score: 6.0.** The paper makes a genuine contribution with a simple, effective metric validated primarily through strong SFT results. The framing incoherence and missing variance estimates are significant but fixable. With a corrected framing and added variance reporting, this would be a clean accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>