Now I have sufficient information for calibration. Let me write the final review.

## Final Review

## Summary
This paper proposes HES (High-Entropy Sum), a training-free metric for scoring the quality of reasoning traces. The key insight is that instead of averaging token-level entropy (which washes out signal from long sequences), HES sums entropy only from the top 0.5% highest-entropy tokens, focusing on critical "forking points" (Wang et al., 2025). HES is validated across three training paradigms (SFT, RFT, RL), multiple model families (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B), three domains (math, code, STEM), and seven evaluation benchmarks.

## Strengths
1. **Clean, well-motivated idea.** The paper correctly identifies that averaging entropy over all tokens dilutes signal from the few critical decision points in long-CoT reasoning. Using the *sum* of top-percentile entropy tokens is a simple, interpretable fix (Section 3, Figure 1). The motivation directly addresses a real limitation of existing metrics like average entropy.

2. **Impressive empirical breadth.** Validation across SFT, RFT, and RL — with multiple model families, three domains (math, code, STEM), and seven benchmarks — is a genuine strength. Tables 1–6 consistently show that HES-based selection matches or beats full-dataset training. Few data-selection papers provide this scope, making the "unified" claim substantially more credible.

3. **Cross-model transfer (Section 4.1.2, Table 1).** Using a 0.6B proxy model to screen data for an 8B model achieves comparable (even slightly higher: 32.12% vs 31.14%) performance than the 8B model's own selection. This is practically valuable and cleanly demonstrated.

4. **Pruning low-HES data is clearly beneficial.** The finding that pruning the 20% lowest-HES data (Highest-HES 80%) reliably outperforms the full dataset (Tables 1, 2, 3, 4) is strongly evidenced. The Lowest-HES-20% score (14.90%) being far below Random-20% (25.89%) in Table 1 convincingly shows low-HES data is actively harmful, not merely uninformative.

## Weaknesses

### Fatal
None.

### Major

1. **No statistical uncertainty quantification for any result.** Every reported number is a point estimate (average@16) with no confidence intervals, standard errors, or significance tests. Several comparisons presented as decisive involve small margins:
   - Table 1: Highest-HES (31.14) vs. Highest-ES (30.92) — a 0.22-point gap across 8 benchmarks.
   - Table 6: Pos-High, Neg-Rand (21.30%) vs. Pos-Difficulty, Neg-Rand (20.27%) — ~1 point on a ~20-point baseline.
   - Table 5 (RFT Per-Query k=2): Highest-HES (31.38) vs. Random (30.37) — +1.01 points.
   
   Given the evaluation protocol (pass@16, temperature 0.6), these gaps could fall within sampling noise. The paper uses "significantly" in prose (lines 159, 206, 307) without any statistical test. This is the single most impactful weakness — it prevents the reader from distinguishing stable effects from noise, especially for the more nuanced comparative claims.

2. **Narrow comparison against existing training-free selection methods.** The paper compares HES against: random, length, difficulty, average entropy, average entropy of high-entropy tokens, total entropy sum, and Forking-Only. These are reasonable, but the paper's framing ("significantly surpassing existing training-free selection methods," abstract; "overcoming the limitations of traditional metrics," line 42) implies broader coverage. The Related Work (Section 5) cites DSIR (Xie et al., 2023) and perplexity-based filtering (Wettig et al., 2024; Marion et al., 2023) — methods that are also training-free and computationally lightweight — but none are benchmarked. Including at least one established training-free baseline would substantially strengthen the paper's central claim.

### Minor

3. **Motivation-to-application gap for reference data.** The paper's motivation (Section 3) is that high-entropy "forking tokens" in *self-generated* responses are key drivers of reasoning improvement. However, in SFT, HES is computed on reference training data written by *other models* using the base model's token-level probabilities. High HES on a reference solution could also reflect unfamiliar notation or reasoning patterns the base model hasn't seen, rather than genuine "forks." The empirical results do vindicate the approach across settings (and cross-model transfer experiments help), but the conceptual chain from "forking tokens are critical" to "HES on reference data measures reasoning quality" is not directly bridged.

4. **RL experiment design detail.** Line 301 states "we train the baseline to its officially reported accuracy" without specifying which benchmark this accuracy refers to or what the value is. Since HES-based downsampling uses 16 of 32 trajectories while Full-Batch uses all 32, the comparison involves different per-upstep sample sizes that could introduce different optimization dynamics. The paper should clarify the baseline accuracy target and acknowledge the sample-size asymmetry.

5. **RFT global pool setting comparison.** In the global pool setting (Table 5), the Random baseline drops substantially (e.g., AVG=27.83 for k=2) compared to per-query Random (AVG=30.37). The paper's explanation (loss of query diversity, line 232) is reasonable, but this means the HES advantage in the global pool setting is partly relative to a degraded baseline rather than pure selection strength. The per-query advantage of HES over Random is modest (+1.01 points for k=2).

### Trivial

6. The paper does not report the computational cost of computing HES, which requires a forward pass through the model for each token position. For long reasoning traces (8K–32K tokens), this is not negligible; a brief wall-time or FLOP analysis would strengthen the practical contribution.
7. The 0.5% high-entropy token threshold is empirically motivated (sensitivity analysis, Figures 3–4) but lacks a theoretical rationale. Minor since the analysis shows robustness to this choice.
8. Potential data contamination between training sources (Open-Math-Reasoning, Open-R1-220k) and evaluation benchmarks (AIME, HMMT, OlyMATH) is not discussed. For competition math problems, this is worth acknowledging.

## Nice-to-Haves
- An ablation that disentangles whether the benefit comes from HES scoring per se vs. the specific selection protocol (particularly in RL, where the asymmetric sampling design combines HES-positive selection with random-negative selection).
- A check of whether the Full-Batch RL baseline benefits from tuned hyperparameters (since 32 vs. 16 trajectories may warrant different learning rates).

## Removed Points
- **Claim that "every downsampling strategy that uses random negatives roughly matches or exceeds Full-Batch" in RL (harsh critic issue 2):** Factually inaccurate. Table 6 shows Pos-Difficulty (20.27%) and Pos-Longest (20.23%) are both *below* Full-Batch (20.63%), and Pos-Rand,Neg-Rand (19.88%) is substantially worse. Only Pos-High, Neg-Rand (21.30%) exceeds Full-Batch. This criticism is removed.
- **Observation that Forking-Only baseline (32.51) is tied with Full-Dataset (32.61):** This is an observation about the results, not a weakness — the paper does not claim Forking-Only would outperform full-dataset. Removed.
- **Claim about the sensitivity analysis in STEM/Code showing no variation:** The paper explicitly frames this as a robustness property ("HES is robust to the specific high-entropy token ratio used," line 316–317). This is accurately described, not a weakness. Removed.
- **Claim that the RFT non-monotonic pattern is a weakness:** The paper already explicitly describes this as "non-monotonic but consistently positive" (line 278). Removed.
- **"0.5% threshold lacking theoretical rationale" as a major weakness:** Softened to trivial since the paper provides empirical justification via sensitivity analysis. Removed as standalone weakness, folded into trivial.

## Novel Insights
The harsh critic's decomposition of the RL experimental design is genuinely insightful: noting that all downsampling strategies with random negatives produce different patterns, and that the Full-Batch baseline may have subtler issues than the paper acknowledges. However, the critic's specific claim about "any reasonable downsampling helps" is contradicted by the data in Table 6. The more accurate insight — that HES is the *only* positive-selection strategy that exceeds Full-Batch, but the margin over difficulty/length baselines is small — is worth the authors' attention but is not a flaw in the paper's reasoning.

## Suggestions
1. **Add uncertainty quantification.** Bootstrapped confidence intervals (or at minimum reporting variance across multiple training seeds) for the main results in Tables 1, 2, 5, and 6 would substantially strengthen all comparative claims.
2. **Add at least one established training-free baseline** (e.g., perplexity-based filtering or DSIR) to the SFT comparison to support the claim of "surpassing existing training-free selection methods."
3. **Clarify the RL baseline accuracy target** referenced on line 301 and acknowledge the sample-size asymmetry (16 vs. 32 trajectories per update) in the Full-Batch comparison.
4. **Briefly discuss potential data contamination** between training and evaluation sets for competition math problems.

## Score and Decision

**Calibration Anchors (all from the deepreview_13k_calibration corpus):**
| Paper | Avg. Human Score | Round | Comparison |
|-------|-----------------|-------|------------|
| NEMESIS (5kMwiMnUip) | 1.40 | R1 | Unrelated jailbreaking paper; far weaker |
| Language Models for Textual Data Valuation (OdoS6cH8MP) | 2.00 | R1 | Data quality assessment with limited validation; weaker |
| Disentangling Roles in Data Pruning (EOPLy80bBm) | 3.00 | R1 | Data pruning study with conceptual confusion; weaker on scope |
| Pre-Memorization Train Accuracy (OegBJMucyM) | 4.25 | R1 | Interesting finding but narrow scope; weaker on breadth |
| FEEDER (diKRhKs5yl) | 5.25 | R1 | ICL demonstration selection; comparable quality but narrower scope |
| 3DS Medical (I5p1Gm8GFS) | 5.75 | R1 | Data selection for medical domain; comparable but narrower domain |
| Rule-Based Rating (SpTzsQjgxF) | 5.75 | R1 | Data rating with DPP; comparable quality, similar baseline concerns |
| **DELIFT (Fty0wTcemV)** | **6.00** | **R1** | **Most comparable: data selection for LLM fine-tuning. Accepted. Our paper has broader paradigm coverage (SFT+RFT+RL vs. fine-tuning stages) but weaker statistical rigor.** |
| Understanding CoT via Info Theory (ouRX6A8RQJ) | 6.40 | R2 | Information-theoretic CoT analysis; rejected due to applicability concerns. Our paper has stronger empirical grounding. |
| Combatting Dimensional Collapse (f4gF6AIHRy) | 8.00 | R1 | Pre-training data selection with strong theory; better than our paper |

**Round 1 Bracket:** 5.5 – 7.5. The paper is clearly stronger than papers in the 1.0–5.5 range (which have fundamental flaws, narrow scope, or conceptual issues), but does not reach the 8.0 level (which requires exceptional theoretical depth or transformative empirical findings).

**Narrowing:** Compared to DELIFT (6.0, accepted) — the most directly comparable anchor — this paper has broader paradigm coverage (SFT+RFT+RL vs. fine-tuning stages) and a cleaner metric, but lacks the statistical rigor that DELIFT's reviewers did not flag as a major issue. Compared to 3DS (5.75, rejected) and Rule-Based Rating (5.75, rejected), this paper's empirical validation is stronger and more comprehensive. The paper sits above these anchors but below the 8.0 papers.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>