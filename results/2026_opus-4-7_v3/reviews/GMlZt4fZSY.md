Now let me draft the review based on my reading of the paper and verification of the critic's claims.Now let me start calibration. Round 1 — Bracketing:Let me read a few key anchors to calibrate:Now let me read one more anchor to finalize my calibration — the "Programming Every Example" paper at 6.0:Now I have enough calibration data. Let me finalize the review.

## Summary

MobileLLM-R1 presents a data-centric training pipeline for sub-billion-parameter reasoning language models. The paper combines principled data curation techniques—leave-one-out (LOO) analysis to identify per-corpus contributions (Section 2.1), influence-function-based data mixing via AutoMixer (Section 2.2), and iterative mid-training data compression (Section 3)—with a multi-stage pipeline (pre-training → mid-training → post-training). The resulting MobileLLM-R1-950M model achieves competitive reasoning benchmarks (57.8 MATH, 15.5 AIME) while using only 4.2T pre-training tokens from ~2T unique open-source data.

## Strengths

- **Controlled comparison isolating pre/mid-training quality (Table 2):** The paper finetunes all baselines (OLMo-2-1.48B, SmolLM2-1.7B) on *identical* reasoning SFT data (OpenMathReasoning + OpenScienceReasoning-2 + OpenCodeReasoning-2, one epoch). MobileLLM-R1-950M (949M params) outperforms both OLMo-2-1.48B (57.8 vs 53.0 MATH, 68.5 vs 58.8 GSM8K) and SmolLM2-1.7B (57.8 vs 41.4 MATH) despite being substantially smaller. This is the paper's strongest piece of evidence that pre-training/mid-training curation matters beyond post-training quality.

- **Methodologically sound LOO analysis (Figure 3, Section 2.1.2):** Equal-probability token sampling ensures fairness; systematic removal of individual datasets tracks NLL on three capability-probing datasets. The finding that FineWeb-Edu serves as cross-domain "glue" (largest degradation across all three capabilities when removed) while domain-specific datasets primarily strengthen their own domains is specific and actionable. The unexpected finding that StarCoder benefits math more than OpenWebMath benefits code (line 139) challenges conventional wisdom.

- **Iterative mid-training compression with convergence signal (Section 3, Figures 5-6):** The observation that influence score distributions compress toward zero across stages provides both a stopping criterion and an intuitive explanation for information exhaustion. Figure 6 concretely shows that subsampled mid-training data avoids the performance dip that the original data causes around 30K steps on MMLU (original drops to ~29 at 30K steps while subsampled reaches ~40.5 by 40K).

- **Full reproducibility commitment:** All datasets are publicly available open-source corpora (Table 5), models and code are released, and detailed training configurations are provided (Section A referenced). For a recipe paper, this is essential and adds significant community value.

## Weaknesses

### Fatal
None

### Major

- **Missing end-to-end ablation of influence-based mixing on downstream accuracy.** The effect of the data mixing contribution (Section 2.2, the paper's first listed contribution) is demonstrated only through perplexity curves (Figure 4). The paper never shows how much final reasoning benchmark accuracy (MATH, GSM8K, AIME, LiveCodeBench) changes when using the influence-derived mixture vs. uniform sampling through the full pipeline. Figure 4's caption acknowledges the comparison is "Original (uniform sampling) with our derived Datamix" but only on perplexity. Perplexity does not always translate to downstream task accuracy, especially at sub-1B scale where calibration can be poor. Without this end-to-end ablation, the reader cannot assess whether the influence-based mixing—presented as a core contribution—is marginal or substantial in the metrics the paper actually reports. This is the most significant evidential gap.

- **Headline comparisons overstate pre-training curation's contribution by conflating it with post-training differences.** The abstract claims "5× higher MATH accuracy than OLMo" and "AIME score of 15.5, compared to just 0.6 for OLMo-2-1.48B." However, the 5× comparison (contribution bullet 3, line 52) is between *final* models that use different post-training pipelines. Table 2's controlled comparison—where all models receive identical SFT—shows a real but more modest gap: 57.8 vs 53.0 MATH (a ~9% relative gain, not 5×). Similarly, the AIME headline (15.5 vs 0.6) compares fully post-trained MobileLLM-R1 against OLMo-2's instruct checkpoint rather than OLMo-2 fine-tuned on the same reasoning SFT. The paper's central thesis is about data curation, but its strongest headline numbers are driven by a combination of curation *and* state-of-the-art SFT data. The gap between the rhetorical claims and the controlled evidence undermines trust in the paper's framing.

### Minor

- **AIME variance not reported.** AIME 2024 has only 30 problems. At sub-1B scale, variance from decoding stochasticity can be substantial. The paper does not report sampling temperature, number of attempts averaged, or confidence intervals for any benchmark. The precise comparison of 15.5 vs 0.6 on such a small test set is hard to interpret reliably without variance information.

- **"Benchmark-free" framing is overstated.** The paper repeatedly calls its data optimization "benchmark-free" and "self-evolving" (abstract, Section 2.2, conclusion). However, the capability-probing datasets are constructed through a multi-stage filtering pipeline (Section 2.1.1) that explicitly uses domain-specific Ask-LLM prompts "with specific emphasis on code, math, general knowledge" (line 105). These probing sets define the optimization objective and functionally serve as benchmarks—the optimization is clearly *target-aware*. The paper's own Figure 4 caption notes the benchmarks are "not accessed during training or data selection," but the probing sets are designed to correlate with them. Calling this "benchmark-free" rather than "test-set-free" or "held-out-benchmark-free" overpromises on the novelty.

- **Qwen3 token-efficiency comparison lacks nuance.** The "11.7% of Qwen3's 36T tokens" framing (abstract, introduction, conclusion) conflates different training objectives. Qwen3 targets a broad capability profile (multilingual, long-context, instruction following, tool use) while MobileLLM-R1 is narrowly optimized for reasoning benchmarks. The extra tokens are not "wasted"—they support capabilities MobileLLM-R1 does not target. The paper does not sufficiently acknowledge this asymmetry, making the comparison catchy but potentially misleading.

### Trivial
None noted.

## Nice-to-Haves

- **Quantification of relative contributions:** Separately measuring the improvement from pre-training mixing vs. mid-training compression vs. SFT data quality would transform the paper from a recipe report into a deeper scientific contribution about which stage matters most.
- **Sensitivity analysis of hierarchical rejection sampling thresholds** (classifier score > 4, top 10% Ask-LLM) — the entire downstream pipeline depends on probing set quality.
- **Ablation of capability weighting** in Eq. 4: uniform weighting across capabilities (C, M, K) is stated without justification; if the goal is reasoning, weighting math/code more heavily is worth exploring.
- **Qualitative error analysis** of what kinds of reasoning the model fails at, grounding the quantitative results.
- **Computational cost accounting** for the full curation pipeline (training LOO models, computing influence scores at 10 checkpoints × 3 domains) to contextualize the "data-efficient" framing.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Architecture description missing from main text:** The reviewer notes the model architecture is entirely deferred to the appendix. Per rules, appendix-deferred content exists in the original submission; this is a presentation preference rather than a substantive flaw.
- **LOO scale transfer concern:** The reviewer worried LOO findings from small models might not transfer, but then acknowledged this is implicitly validated by the paper training all three model sizes (140M, 360M, 950M) with the same recipe and showing consistent gains.
- **OLMo/SmolLM as "straw-man" comparisons:** The reviewer suggested these models weren't designed for competition math. However, these are the closest fully open-source baselines, and the paper explicitly categorizes models by openness (fully vs. partially open-source). This is a valid comparison framework, not straw-manning.
- **Figures being garbled:** Parser artifacts, not paper issues.
- **Reproducibility details (hyperparameters, etc.):** The paper commits to releasing all code, models, and detailed configurations in the appendix (Section A).

## Novel Insights

The iterative mid-training data compression via influence score convergence is a genuinely novel observation: as training progresses, influence score distributions compress toward zero (Figure 5), indicating information exhaustion and providing a natural, principled stopping criterion for when continued training on a dataset yields diminishing returns. The cross-domain LOO finding that StarCoder benefits math more than OpenWebMath benefits code (Section 2.1.2, Figure 3) is a specific, counter-intuitive insight that reverses commonly held assumptions and could influence data curation decisions in other training pipelines.

## Suggestions

1. **Add an end-to-end ablation:** Train MobileLLM-R1-950M with uniform data mixing (no influence-based weighting) through the complete pipeline including SFT, and compare final reasoning accuracy against the curated version. This single experiment would directly quantify the data curation contribution.
2. **Report confidence intervals or multi-run statistics** for AIME and LiveCodeBench, and specify sampling temperature and number of attempts.
3. **Temper the "benchmark-free" framing** to acknowledge that capability-probing datasets are hand-designed optimization targets drawn from training distributions—call it "test-set-free" or "held-out-benchmark-free."
4. **Separate headline claims** about pre-training curation from claims about the full pipeline; present Table 2's controlled comparison as the primary evidence rather than burying it after the less controlled comparisons.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to MobileLLM-R1 |
|-------|------|-----------|-------|---------------------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Survey with no contribution; MobileLLM-R1 vastly stronger |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Off-topic, not a real research paper; incomparable |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Weak attack paper; MobileLLM-R1 vastly stronger |
| Financial Markets NN | nSDOkm0SKo | 1.00 | R1 | Not a research contribution; incomparable |
| Paramanu-Ganita | v3DwQlyGbv | 2.33 | R1 | Small math model with poor ablations, presentation issues; MobileLLM-R1 is much more rigorous |
| FreeLM | qgLyKwXVDs | 2.00 | R1 | Fine-tuning-free strategy with weak results; MobileLLM-R1 is significantly stronger |
| LogicJitter | mfTM4UdYnC | 2.50 | R1 | LLM reasoning for misinformation; limited methodology; MobileLLM-R1 stronger |
| Generalization from Starvation | f7aWmxgSN4 | 3.00 | R1 | KG learning with hints of universality; interesting but limited; MobileLLM-R1 has stronger empirical contributions |
| LokiLM | bppG9srkpR | 3.60 | R1 | Technical report with limited novelty; MobileLLM-R1 much stronger methodology |
| Lean-ing on Quality | Qdp7hlenr6 | 4.00 | R1 | Data curation for autoformalization; mixed reviews; MobileLLM-R1 has broader impact and better ablations |
| Pelican Soup Hypothesis | aaYBsuGRne | 5.20 | R1 | In-context learning analysis; interesting but more theoretical; MobileLLM-R1 has stronger practical results |
| Unearthing Large Scale Domain Knowledge | 8EM1A6qfX5 | 5.00 | R1 | Domain-specific data collection; MobileLLM-R1 has more principled methodology |
| Curated LLM | ynguffsGfa | 6.33 | R1 | LLM data curation for tabular augmentation; different domain; comparable quality |
| Programming Every Example (ProX) | UNxCphTxWp | 6.00 | R1 | Data quality improvement framework; comprehensive but has methodology concerns; MobileLLM-R1 has more novel insights |
| What Kind of Pretraining Data | 1hQKHHUsMx | 6.75 | R1 | Uses influence functions to study pretraining data for reasoning; accepted; comparable depth but more analytical vs. MobileLLM-R1's applied recipe |
| Textbooks Are All You Need (phi-1) | Fq8tKtjACC | 6.00 | R1 | Data quality for small code models; MobileLLM-R1 has more principled methodology, better ablations, full reproducibility |
| Synthetic continued pretraining | 07yvxWDSla | 8.00 | R1 | Clean method + theoretical analysis + comprehensive evaluation; stronger than MobileLLM-R1 in rigor |
| Self-Alignment Backtranslation | 1oijHJBRsT | 8.00 | R1 | Self-curation approach with clean experiments; stronger overall |
| Combatting Dimensional Collapse | f4gF6AIHRy | 8.00 | R1 | File selection for pretraining with clean methodology; stronger in experimental rigor |
| Training on the Test Task | jOmk0uS1hl | 8.00 | R1 | Evaluation methodology paper; different focus; cleaner experimental design |

### Bracket and Reasoning

**Round 1 bracket: 6.0–7.0.**

MobileLLM-R1 is clearly stronger than the reject-tier papers (1.0–4.0) in methodology, ablations, and results. It is stronger than phi-1 (6.0, Rejected) in principled methodology, controlled ablations (Table 2), and full reproducibility—phi-1 withheld key details and had less rigorous ablations. It is comparable to "What Kind of Pretraining Data" (6.75, Accepted), which uses influence functions for analytical insights about reasoning, whereas MobileLLM-R1 uses them for practical data optimization with strong applied results. However, MobileLLM-R1 falls below the 8.0 accept-tier papers (Synthetic continued pretraining, Combatting Dimensional Collapse) which have cleaner theoretical grounding and/or more complete ablations.

The missing end-to-end ablation of the influence-based mixing is a real gap—the paper's first listed contribution lacks direct downstream accuracy validation. The framing issues (benchmark-free, 5× OLMo, 11.7% Qwen3 tokens) are real but addressable. The contributions are genuine: the LOO analysis, influence-based mixing, and mid-training compression form a principled and reproducible pipeline with strong applied results. The full open-source release adds substantial community value.

**Final score: 6.5** — This paper makes genuine methodological contributions to data curation for small reasoning models, with strong controlled experiments (Table 2) and novel insights (mid-training compression convergence, cross-domain LOO findings). The missing end-to-end ablation of influence-based mixing and overstated framing prevent a higher score, but the paper's contributions are real, reproducible, and valuable to the community.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>