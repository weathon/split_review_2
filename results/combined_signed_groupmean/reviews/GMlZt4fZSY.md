## Summary

This paper presents a full-stack, open-source training recipe for sub-billion-parameter reasoning language models (MobileLLM-R1 series). The core proposal is a data-centric framework combining (1) cross-capability influence-based data mixing for pre-training, and (2) data-model co-evolution for mid-training compression. The resulting 950M model achieves a striking AIME score of 15.5 (vs. 0.6 for OLMo-2-1.48B and 0.3 for SmolLM-2-1.7B), and under controlled reasoning SFT (Table 2) consistently outperforms similarly sized fully-open models on MATH, GSM8K, and LiveCodeBench.

---

## Strengths

- **Strong, well-validated empirical results.** MobileLLM-R1-950M delivers a large and consistent margin over comparable fully-open baselines on AIME (15.5 vs. 0.6/0.3), MATH, GSM8K, and LiveCodeBench. These are not incremental gains; they are decisive. [impact=+9.99]

- **Credible controlled comparison (Table 2).** By fine-tuning all models on the identical reasoning SFT data (OpenMathReasoning + OpenScienceReasoning-2 + OpenCodeReasoning-2), the paper isolates the contribution of pre-training/mid-training from post-training quality. MobileLLM-R1-950M* achieves 57.8% MATH vs. 53.0% (OLMo-2-1.48B) and 41.4% (SmolLM2-1.7B), providing strong evidence that the data curation pipeline builds better latent reasoning potential. [impact=+9.99]

- **Fully open, reproducible release.** The commitment to releasing models, datasets (all open-source), code, and training recipes at this scale is a genuine contribution to reproducibility. [impact=+3.01]

---

## Weaknesses

### Major

- **Missing end-to-end ablation of the influence-based data mixing method.** The paper's central methodological claim is that cross-capability influence-based data mixing (Section 2.2) drives the final performance. However, no experiment replaces this mixing with uniform sampling (or a baseline strategy) at the full 4.2T-token scale and compares final benchmark scores. The evidence for the method (Figure 4) shows perplexity improvements on probing datasets at 500K steps — a positive signal, but not proof that the mixing algorithm (rather than the overall curated dataset quality or other pipeline elements) causes the AIME/MATH/GSM8K results. Without this ablation, the paper cannot causally attribute its results to the proposed method. [impact=-10.00]

- **Proxy experiments operate at a scale that may not transfer.** The LOO analysis (Figure 3) and data mixing validation (Figure 4) are conducted at ~500K steps with an unspecified model size, while full pre-training uses 4.2T tokens at up to 950M parameters. The paper provides no evidence that the relative importance of datasets observed at small scale holds at the full training scale. Data dynamics can shift dramatically with scale, making this a non-trivial gap. [impact=-1.89]

### Minor

- **Evidence for data-model co-evolution (Section 3) is limited to MMLU.** Figure 6 shows improvements from subsampling only on MMLU, not on reasoning benchmarks (MATH, GSM8K, HumanEval). Since the paper's thesis is about reasoning capabilities, this evidence is incomplete. The "original" data curve also shows an anomalous dip around 30K steps that could reflect training instability rather than a data quality effect. [impact=-2.76]

- **The headline Qwen3 token-efficiency claim oversimplifies the comparison.** The paper states (Abstract, Introduction) that MobileLLM-R1-950M "matches or surpasses Qwen3-0.6B" using "only 11.7% of the tokens" (4.2T vs. 36T pre-training tokens). However, at the base model level, Qwen3-0.6B-base massively outperforms MobileLLM-R1-950M-base (61.6% vs. 5.0% GSM8K, 52.4% vs. 26.5% MMLU). The final parity is achieved primarily through the post-training pipeline, not just pre-training efficiency. The paper should clearly distinguish pre-training efficiency from overall pipeline efficiency. [impact=-0.04]

- **The "benchmark-free" framing is overstated.** The capability-probing datasets used for influence computation (Section 2.1.1) are constructed via hierarchical rejection sampling using FineWeb-Edu classifier filtering and Ask-LLM scoring with domain-specific prompts targeting code, math, and knowledge. These are essentially curated proxy evaluation sets, making the "benchmark-free" claim more terminological than substantive. [impact=-0.18]

### Trivial

- The model size used for the ~500K-step proxy experiments (LOO and data mixing) is not specified in the paper. [impact=-0.00]

---

## Nice-to-Haves

- An end-to-end ablation comparing influence-based data mixing vs. uniform sampling at the full 4.2T-token scale would validate (or reframe) the central methodological claim.
- For the data-model co-evolution, evaluating on reasoning benchmarks (MATH, HumanEval) in addition to MMLU would strengthen the evidence.
- A discussion of the computational cost of the influence score computation (training domain-specialized models, Hessian-vector products at 10 checkpoints) relative to simpler heuristics would be informative.

---

## Removed Points

These points were flagged by the input review but are removed from the main review:

- **"No statistical significance/variance reported"** — Generic criticism; single-run evaluation at this training scale is standard practice in large-scale LLM research. Removed.
- **"Baseline comparison not perfectly matched (instruct vs Tulu-SFT)"** — The paper explicitly discloses this difference in the Table 2 caption. The comparison is transparent and informative. Removed.
- **"Computational cost not discussed"** — A reasonable nice-to-have but not a weakness; the paper focuses on data efficiency, not training efficiency. Demoted to Nice-to-Haves.
- **"No comparison against OLMo/SmolLM data mixing strategy"** — Partially addressed; the paper uses Dolmino (OLMo 2's mid-training corpus) and compares against their final results. Removed.
- **"Data mixing improvement is modest"** — Subjective; the perplexity improvements (Figure 4) are consistent across all three domains. Removed.

---

## Novel Insights

The most revealing observation from the reviews is that the paper's strength (strong open-source small reasoning model) and its weakness (unvalidated causal link between the mixing algorithm and results) are two sides of the same coin. The paper positions itself as a methods contribution ("we propose influence-based mixing that achieves SOTA"), but the evidence better supports an empirical recipe contribution ("we present a fully open training pipeline for a strong sub-billion reasoning model"). This tension — between method novelty claims and recipe-style evidence — is the central axis for evaluating the paper. The most honest path forward is to reframe the contribution around the comprehensive open recipe and treat the influence-based mixing as one explored design choice, not the primary validated innovation.

---

## Suggestions

1. **Add one end-to-end ablation:** Train the 950M model with uniform data mixing (same datasets, same token budget, same post-training) and compare final benchmark scores. This is the single highest-leverage addition.
2. **For the data-model co-evolution,** evaluate on MATH/HumanEval in addition to MMLU.
3. **Qualify the Qwen3 comparison** to explicitly distinguish pre-training token efficiency from overall pipeline efficiency.
4. **Specify the model size** used in the proxy (500K-step) experiments.
5. **Reframe the contributions** to center the open empirical recipe and analyses, rather than claiming the influence-based method as a validated innovation.

---

## Calibration Report

**Round 1 bracket:** 5.0–6.5 (from comparison against anchors at 5.25–6.75)

**Anchors considered:**

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|-------------------------|
| `Fq8tKtjACC.md` (phi-1) | 6.00 | 1 | Yes | Similar empirical contribution (small model + curated data) but phi-1 had data-withholding issues this paper doesn't; however, phi-1's method was simpler and better communicated |
| `79ZkWgY2FI.md` (Small-to-Large) | 5.25 | 1 | Yes | Less directly comparable (studies proxy model transfer), but occupies the same score band |
| `aP3OBwf8dk.md` (Need Small SLM) | 6.00 | 1 | Yes | Similar topic (data curation for small models) but different methodology; both face validation concerns |
| `3OyaXFQuDl.md` (Smaller Weaker Yet Better) | 7.00 | 1 | Yes | Stronger empirical methodology and more comprehensive ablations, setting a higher bar |
| `f4gF6AIHRy.md` (Combatting Dimensional Collapse) | 8.00 | 1 | Yes | Thoroughly validated data selection method with strong ablations; our paper lacks comparable validation |
| `sZGZJhaNSe.md` (Aioli) | 6.25 | 2 | Yes | Directly comparable (data mixing paper); shared the "small-scale validation" concern but was accepted |
| `1hQKHHUsMx.md` (What Kind of Pretraining Data) | 6.75 | 2 | Yes | Uses influence functions to study reasoning data; accepted despite narrow scope |
| `eENHKMTOfW.md` (Training Mice) | 6.00 | 3 | Yes | Most similar in genre — an open empirical recipe paper accepted at 6.00 despite low-novelty concerns |

**Narrowing logic:** The paper shares the two strongest impact items with the phi-1 anchor (strong empirical results at +9.99 and significant missing-validation weakness at -10.00), but is cleaner in its openness and has a more informative controlled comparison (Table 2). It does not reach the 7+ band because of the missing ablation that fully validated anchors like "Combatting Dimensional Collapse" and "Smaller, Weaker, Yet Better" provide. It is above the 4–5 band because the empirical results are genuinely strong and the controlled comparison convincingly demonstrates that the pre-training pipeline matters. The closest anchor is "Training Mice to Compete with Elephants" (6.00), but this paper's missing-ablation weakness is more central to its claimed contribution, placing it slightly lower at **5.5**.

---

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>