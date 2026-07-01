## Summary

AdaSVD proposes two improvements over prior SVD-based LLM compression: (1) **adaComp**, an alternating pseudoinverse-based update of the singular matrices U and V after truncation to compensate for compression error, and (2) **adaCR**, which assigns layer-specific compression ratios based on cosine similarity between layer inputs and outputs. Experiments on LLaMA2-7B, OPT-6.7B, Mistral-7B, and Vicuna-7B across language modeling and reasoning benchmarks show consistent improvements over SVD-LLM and other SVD baselines at 40–60% compression ratios.

---

## Strengths

1. **Clear problem identification and sound mathematical formulation (Section 3.1, Eq. 4–5, Eq. 8–13).** The paper correctly identifies two genuine limitations of prior SVD-based compression: insufficient post-truncation compensation of remaining singular vectors and uniform compression ratios across layers. Reformulating the compensation problem as a least-squares problem over calibration data and solving via the Moore-Penrose pseudoinverse (Eq. 10, 13) rather than direct matrix inversion is mathematically sound and avoids numerical instability (Figure 3a).

2. **Consistent empirical improvement across models and compression ratios (Table 1, Table 3).** AdaSVD consistently outperforms all prior SVD-based methods (SVD, FWSVD, ASVD, SVD-LLM) on LLaMA2-7B across 40–60% compression ratios on both language modeling perplexity and reasoning accuracy. The improvements over SVD-LLM are meaningful (e.g., WikiText-2 perplexity 14.76 vs 16.11 at 40%, 50.33 vs 89.90 at 60%). Results also generalize across four LLM families (LLaMA2, OPT, Mistral, Vicuna) as described in the text.

3. **Well-structured and informative ablation study (Table 3a–d).** The ablation cleanly separates the contributions of adaComp and adaCR. Table 3a shows adaComp alone improves over SVD-LLM; Table 3b shows adaCR adds further gains. The iteration count sweep (Table 3c) and minimum retention ratio sweep (Table 3d) are honestly reported, including the finding that more iterations can hurt performance.

4. **Orthogonality to quantization demonstrated (Table 4).** AdaSVD + GPTQ-INT4 consistently outperforms SVD-LLM + GPTQ-INT4 across all compression ratios, demonstrating the method's utility as a component in a broader compression pipeline.

---

## Weaknesses

### Major

1. **The alternating update procedure overfits to the small calibration set, and the paper's own ablation data shows that the iterative nature is counterproductive at practical compression ratios (Table 3c).** With only 256 samples from WikiText-2 used for calibration, increasing iterations monotonically *worsens* perplexity at 40% compression (1 iter: 14.76 → 3 iter: 15.47 → 15 iter: 15.84) and at 50% (25.58 → 27.11 → 27.45). At 60%, 1 iteration (50.33) also outperforms 3 iterations (64.12). The paper acknowledges "overfitting due to limited calibration data" (Section 4.3) but still frames iterative alternating updates as a core contribution. Since the method is evaluated only on standard benchmarks that overlap distributionally with WikiText-2, generalization to out-of-distribution settings is unverified. This is a structural tension: the method's signature feature (iterative alternating updates) is either unnecessary (1 iteration suffices) or actively harmful at 40–50% compression.

2. **No variance or statistical significance reported for any experiment.** None of the tables report standard deviations, standard errors, or confidence intervals. Given the small calibration set (256 samples) and the iterative optimization nature of adaComp, results could be sensitive to the random seed used for calibration sample selection. Single-run evaluation is insufficient to establish that observed improvements (e.g., 14.76 vs 16.11 at 40%) are statistically reliable rather than noise.

### Minor

1. **The GPU memory justification for stack-of-batch is questionable.** The paper states: *"during our experiments, we found that extending X to just 32 samples on an 80GB GPU is challenging"* (Section 3.1). A LLaMA2-7B model in FP16 occupies ~14 GB. Even with activations for 32 sequences stored, the total memory footprint should be well within 80 GB. While the stack-of-batch strategy may be beneficial for other reasons (e.g., reducing pseudoinverse computation cost), the stated rationale is not credible and undermines confidence in the experimental narrative.

2. **The absolute quality of compressed models is severely degraded, yet the paper's deployment framing overreaches.** At 40% compression, WikiText-2 perplexity is 14.76 vs the original 5.68 (2.6×). At 60%, perplexity is 50.33 (8.9×). Reasoning average accuracy drops from 68.85% to 42.63% at 40%. While AdaSVD is better than baselines, claiming these models are suitable for "smartphones and IoT devices" (Section 4.2) without evidence of practical viability overstates the case. The claims should be calibrated to relative improvement rather than deployment readiness.

3. **Results at higher compression ratios (70%, 80%) and the cross-LLM comparison table (Table 2) are relegated to the supplementary file** (per Section 4.2 and ablation references), yet the text makes broad claims about "all compression ratios" and "consistently outperforms." The reader cannot fully verify these claims from the main paper.

4. **The layer importance metric in adaCR (cosine similarity between input X and output Y, Eq. 17) lacks justification.** A layer with high input-output similarity could be identity-like and thus *more* compressible, not less. The paper does not provide theoretical or empirical evidence for why this particular metric captures "importance" for compression decisions, nor does it compare against alternatives.

### Trivial

None.

---

## Nice-to-Haves

- Report variance across multiple calibration sample seeds to establish statistical reliability.
- Include an ablation of adaComp *without* stack-of-batch but with equivalent data volume to test whether averaging samples helps beyond simply using more data.
- Provide computational cost (time/FLOPs) for the alternating update procedure.
- Compare the adaCR importance metric against alternatives (e.g., layer removal experiments from the pruning literature).

---

## Removed Points

- **Table 1 column-swap artifact (C4/Mmlu):** Parser rendering issue, not a paper flaw.
- **Missing related works:** Cannot be verified externally per review guidelines.
- **Missing Table 2 vagueness:** Appendix is stripped by the parser; cross-LLM results are described in text.
- **Missing comparison with non-SVD compression methods:** Paper explicitly scopes itself to SVD-based compression and states SVD is orthogonal to other methods.
- **"Implausible memory claim" elevated to fatal:** The memory claim is questionable but the method works regardless; computational efficiency is an alternative justification.

---

## Novel Insights

None beyond the paper's own contributions. The pseudoinverse-based alternating update for post-SVD-truncation compensation is a technically sound incremental contribution over SVD-LLM, but the overfitting pattern in the ablation data reveals that the iterative framing partially overclaims what the method actually delivers.

---

## Suggestions

1. Provide results with multiple calibration set random seeds and report variance.
2. Clarify or replace the memory justification for stack-of-batch (e.g., cite computational cost of pseudoinverse on large calibration matrices).
3. Move 70–80% compression results and Table 2 into the main paper.
4. Include a more detailed analysis of the adaCR importance metric, including correlation with other measures of layer importance.
5. Tone down claims about practical deployment viability given the absolute quality degradation of the compressed models.

---

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>