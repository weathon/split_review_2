Now I have a comprehensive calibration picture. Let me produce the final review.

**Round 1 bracket:** Based on calibration anchors, the paper sits between the 4.40-5.25 range (negative/empirical data selection papers) and the 5.75-6.00 range (method papers with broader validation). The paper's novel metric and three-paradigm validation push it above 4.4-5.25, but the missing model specification and no error bars prevent it from reaching the 6.0+ level. Narrowest plausible range: **5.0–6.0**.

**Final anchor comparisons:**

| Paper | Score | Comparison |
|-------|-------|------------|
| Rethinking Data Selection at Scale (qUJsX3XMBH) | 4.40 | Negative result paper; current paper has a positive method contribution and is clearly stronger |
| Scaling Relationship on Math Reasoning (cijO0f8u35) | 5.25 | Empirical study of scaling laws; current paper has a novel metric which is a stronger contribution |
| 3DS Medical Domain (I5p1Gm8GFS) | 5.75 | Domain-specific; current paper is broader (3 paradigms, multiple domains) but 3DS is more rigorous |
| DELIFT (Fty0wTcemV) | 6.00 | Comparable breadth (3 stages vs 3 paradigms); DELIFT accepted, but current paper's idea is arguably more novel |
| Understanding CoT via Information Theory (ouRX6A8RQJ) | 6.40 | Novel theory but very limited experiments (toy + GSM8K); current paper has much broader validation |

The paper's genuine contribution and broad validation place it in the 5.5-6.0 range, but the missing model specification and lack of variance estimates prevent acceptance in current form.

---

## Summary

This paper proposes High-Entropy Sum (HES), a training-free metric for data selection in LLM reasoning training. The key insight is that standard averaging metrics dilute the signal from critical decision-point tokens in long-CoT responses. HES sums the entropy of only the top 0.5% highest-entropy tokens. The paper validates HES across SFT, RFT, and RL on multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B) and domains (math, code, STEM), showing that training on high-HES subsets matches or exceeds full-dataset performance.

## Strengths

1. **Well-motivated and genuinely novel core idea.** The observation that averaging metrics dilute signal from critical "forking tokens" in long-CoT reasoning (Section 2.2, Section 3.1) is clearly articulated. The shift from global statistics to a sparse top-percentile sum of token entropies is a simple but non-obvious insight that builds sensibly on prior work (Wang et al., 2025). This is the paper's genuine contribution.

2. **Validation across three training paradigms (SFT, RFT, RL).** Most data selection papers focus on one paradigm. Demonstrating consistent HES-based improvements across SFT (Tables 1–4), RFT (Table 5), and RL (Table 6) is the paper's strongest claim to generality. The consistent pattern—highest-HES data helps, lowest-HES data hurts—is convincing evidence that the metric captures something real.

3. **Small-to-large model transfer (Section 4.1.2).** Qwen3-0.6B screening data for training Qwen3-8B achieves 32.12% vs 31.14% for self-selection. This is a practical, well-designed demonstration that HES captures dataset-intrinsic properties rather than model-specific artifacts, with clear engineering value (cheap proxy model curates data for a much larger one).

4. **Clean ablation of metric design choices (Table 1).** The comparison of HES against AvgE, AvgHE, and ES cleanly isolates what matters: the *sum* over *only the top high-entropy tokens* produces the best discrimination, not averaging or summing everything.

## Weaknesses

### Major

1. **Missing specification of the entropy-computation model.** The paper defines token entropy as H_t = −∑ P_t(j) log P_t(j) but never states which model's probability distribution is used for computing HES on the pre-existing SFT datasets (Open-Math-Reasoning, Open-R1-220k). For RFT and RL, the training model generates its own responses, so the entropy model is the training model. But for SFT on pre-existing datasets, it is ambiguous whether HES is computed using the training model's base checkpoint, a smaller proxy model, or some other reference model. The "(0.6B)" and "(1.7B)" rows in Table 1 are explicitly marked with the proxy model name, making the ambiguity of the unadorned "Highest-HES" rows salient. This must be specified for reproducibility.

2. **No statistical significance or variance reported.** Every result in Tables 1–6 is a single point estimate with no error bars, confidence intervals, or multiple-seed experiments. Many claimed advantages are 1–3 percentage points (e.g., RFT Per-Query k=8: Highest-HES 31.13% vs Random 30.16%; RL Pos-High, Neg-Rand 21.30% vs Full-Batch 20.63%). Without variance estimates, it is unclear whether these differences are meaningful or within noise. This is standard to expect in empirical LLM papers.

3. **RL results are modest, and the language overclaims them.** The best HES strategy (Pos-High, Neg-Rand) achieves 21.30% vs Full-Batch 20.63% — a 0.67pp aggregate gain. On individual benchmarks, HES underperforms Full-Batch on HMMT25 (11.88% vs 15.21%) and GPQA (35.54% vs 36.71%). The abstract claims HES "significantly surpasses existing training-free selection methods," but the comparison baselines are only two simple heuristics (Pos-Difficulty at 20.27%, Pos-Longest at 20.23%) with similarly small margins. The language should be tempered to match the evidence.

### Minor

4. **Full-dataset baseline inconsistency in Table 2.** The Full-Dataset baseline for DeepSeek-R1-Distilled on Open-R1-220k achieves 30.22% — *worse* than Random-20% (30.38%). This unusual result suggests either dataset noise that random downsampling mitigates, or a training procedure suboptimal for the full dataset (e.g., 3 epochs on the full set means more training steps, potentially leading to overfitting or undertuning). The paper does not discuss this, making the "Highest-HES-20% surpasses full dataset" claim (34.61% vs 30.22%) less clean: some of the gap may come from the full-dataset baseline not being properly tuned.

5. **The dual role of HES w.r.t. correctness could be clarified.** Figure 1 shows HES distinguishes correct from incorrect responses in a mixed pool (higher HES → more likely incorrect). But in SFT/RFT/RL, HES is applied *within* already-correct responses to rank reasoning complexity (higher HES → more complex → better learning). The abstract and introduction frame HES as a general "quality" metric without explicitly noting this conditioning. Adding an explicit paragraph explaining this duality would strengthen the paper.

6. **Coarse sensitivity analysis.** The hyperparameter sweep for the high-entropy token ratio (Figures 3–4) tests only four values: 0.005, 0.05, 0.5, 1.0. The claim that 0.5% is optimal is only "best among these four." A finer sweep would be more informative, though the observed trend (smaller ratios consistently better) partially mitigates this concern.

### Trivial

7. The RFT finding that per-query selection outperforms global pool selection is attributed to "preserving query diversity" but this is not directly verified (e.g., by measuring diversity of the selected sets). The hypothesis is reasonable but unsupported.

8. The "Forking-Only" baseline (gradient updates only on high-entropy tokens) achieves 32.51% vs HES-20% at 31.14%. This interesting comparison is noted but not analyzed further.

## Nice-to-Haves

- Including DSIR (Xie et al., 2023) as a lightweight training-free baseline would broaden the comparison.
- Adding qualitative examples comparing high-HES and low-HES correct solutions to the same problem would illustrate what HES captures.

## Removed Points

- **"The paper never specifies which model computes HES" framed as a fatal/structural issue** — Demoted to Major. The natural reading for RFT/RL is the training model (it generates the responses). For SFT, the training model base checkpoint is the natural choice, as evidenced by the "(0.6B)" rows being specially marked. Still a real omission, but not fatal.
- **"No comparison against DSIR or D4"** — The paper does not claim exhaustive baseline coverage, and DSIR's computational profile is not obviously cheaper than a single forward pass for HES. Moved to Nice-to-Haves.
- **"Per-query vs global pool finding undermines the claim that HES is a general quality metric"** — Overstated. The paper itself notes this finding and offers a reasonable hypothesis about diversity. It does not undermine HES's quality signal; it merely shows selection strategy matters too.
- **"Inconsistent across benchmarks for RFT"** — The pattern across 28 RFT conditions in Table 5 is actually very consistent: Highest-HES outperforms Random in the large majority of individual benchmarks. Removed as overly negative.
- **"Framing of negative diversity results"** — The reviewer's alternative explanation is speculative. The paper's explanation (diversity matters for negatives) is reasonable and supported by the data. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the entropy-computation model explicitly** for each experiment. State: "We compute token-level entropies using [model name]'s base checkpoint on the responses."
2. **Add variance estimates** — re-run with 3 seeds, or compute bootstrap confidence intervals from the 16 sampling paths already collected.
3. **Add an explicit paragraph** clarifying that HES ranks reasoning complexity *within* already-correct responses; its use on mixed pools (Figure 1) distinguishes correctness, which is a different regime.
4. **Temper the RL claims** — replace "significantly surpasses" with language matching the 0.67pp aggregate gain and mixed per-benchmark results.
5. **Discuss the Table 2 full-dataset baseline anomaly** (worse than random-20%).

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>