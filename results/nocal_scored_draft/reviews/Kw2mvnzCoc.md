Now let me assemble the final review.

## Summary

TSPulse proposes a family of ultra-light (1M parameter) pre-trained time-series models with three embedding types (temporal, spectral, semantic) learned via multi-objective masked reconstruction, plus lightweight task-specific fusers (MHT for anomaly detection, TSLens for classification). The model is evaluated on classification, anomaly detection, imputation, and similarity search across 75+ datasets, showing strong efficiency-accuracy tradeoffs.

## Strengths

- **Well-motivated multi-view architectural design (Section 2, Figure 2).** The paper correctly identifies that existing time-series pre-trained models entangle temporal, spectral, and semantic information into a single embedding, and designs separate reconstruction objectives across these modalities via different segments of the decoder output (time tokens → temporal, FFT tokens → spectral, register tokens → semantic).

- **Sensitivity analysis provides concrete evidence for embedding specialization (Section 6, Table 2).** Controlled perturbation experiments on synthetic signals show clear differential responses: temporal embeddings are highly sensitive to phase shifts (130% distortion), FFT embeddings are less so (21%), and semantic embeddings are the most robust (12%). This directly tests whether the three embedding types encode different signal properties.

- **Efficiency is demonstrated concretely with side-by-side comparison (Figure 7).** CPU inference time (0.387ms vs 5.51ms for MOMENT, 46.71ms for Chronos), GPU time, embedding dimension, and model size are reported together, allowing direct evaluation of the efficiency-accuracy tradeoff. At 1M parameters with sub-0.4ms CPU inference, the model is genuinely deployment-friendly.

- **Ablations cover all four tasks and provide informative diagnostics (Table 1a–d).** The most informative finding is the 79% imputation MSE degradation when pre-training uses only block masking instead of hybrid masking (Table 1c), which honestly quantifies the contribution of the masking strategy. Additional ablations confirm the value of dual-space learning, TSLens, and identity initialization for channel mixing.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed disentanglement framing (Section 2, Figure 2).** The paper uses "disentangled" ~20 times across abstract, introduction, architecture, experiments, and conclusion, but the architecture does not enforce strict disentanglement at the representation level. All three token types (time, FFT, register) are concatenated into `Input_E ∈ ℝ^{C×(2N+R)×D}` and processed together through a shared TSMixer backbone that "effectively fuses these views" (line 69). Only the output heads apply different loss objectives to different embedding segments. The sensitivity analysis (Table 2) shows that the three embedding types respond *differently* to perturbations — evidence for specialization, not disentanglement in the strict sense. The paper should acknowledge this distinction and frame the contribution as "specialized multi-view embeddings" rather than "disentangled representations."

- **Imputation evaluation protocol inflates headline gains (Section 4.3, Figure 6, Table 1c).** TSPulse is evaluated under irregular hybrid masking for imputation, which matches its hybrid masking pre-training distribution. The paper's own ablation shows that using block masking instead of hybrid masking during pre-training causes a **79% degradation** in imputation MSE (Table 1c). While the paper claims TSPulse "continues to outperform all baselines by a significant margin" under block masking (lines 225–226, citing Appendix Figure 13), no numerical values are provided in the main paper, and the headline "50%+" gains come entirely from the hybrid masking evaluation. The abstract and introduction present these gains without qualification about evaluation-protocol alignment.

### Minor

- **Similarity search comparison against Chronos is not informative (Section 4.4, Figure 7).** Chronos (Ansari et al., 2024) is a forecasting foundation model, not designed for representation learning or similarity search. Reporting "100% improvement" over Chronos (line 295) adds noise rather than evidence. The comparison against MOMENT (25–40% gains) is meaningful; the Chronos comparison should either be dropped or clearly qualified.

- **The term "zero-shot" for anomaly detection is imprecise (Section 4.1, lines 119, 166–167).** The reported TSPulse-ZS results use the Head_triang. approach, which selects the best head using a small labeled tuning set. The paper is transparent that this tuning set is "consistently used across all leaderboard methods" (line 166), but "zero-shot" conventionally implies no labeled data is used. Table 1(a) shows the gap between the true label-free Head_ensemble (0.44 VUS-PR) and the tuning-set-calibrated Head_triang. (0.48 VUS-PR) is 9%, which is non-trivial.

- **No statistical significance or variance reporting in any result.** Every reported metric — VUS-PR scores, classification accuracy, MSE, similarity search metrics — is a single point estimate without confidence intervals, standard deviations, or significance tests. This is especially concerning for classification (Figure 5) where the 5–16% improvements over strong baselines like VQShape and TRIP could be within noise.

- **Sensitivity analysis dimensions are unequal (Table 2, line 315).** Time and FFT embeddings have dimension d=1536 while semantic embeddings have d=256 — 6× smaller. Lower-dimensional embeddings can naturally exhibit lower distortion under perturbation, so the robustness comparison is partially confounded by dimensionality. A normalized comparison (e.g., measuring distortion per dimension) would strengthen the analysis.

### Trivial
None.

## Nice-to-Haves
- Report imputation results under block masking evaluation prominently in the main paper with numerical values alongside the hybrid masking results.
- Clearly separate AD zero-shot results into Head_ensemble (truly label-free) and Head_triang. (tuning-set-calibrated) as distinct variants.

## Removed Points
*These points are flagged to be removed; treat them with caution.*
- **Criticism about missing appendix details** (architectural hyperparameters, pre-training data description, proofs): The parser strips appendix sections from all papers; these exist in the original submission.
- **Formatting nitpicks** (garbled figure caption text, e.g., "5-16% size reduction"): Parser artifacts, not author errors.
- **Criticism about open-source code release**: The reproducibility statement commits to disclosing model parameters (Appendix A.9); code release expectations go beyond standard ICLR requirements.
- **Generic "no comparison to X related work"**: Cannot verify existence of omitted references.
- **Criticism about "variable masking ratios" being vague**: Addressed by the paper's definition of hybrid masking (line 63) and its description of masking both full and partial patches.
- **Abstract numerical claims being imprecise**: The numbers are presented as relative improvements with specific task context; the paper consistently references the relevant figures.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Reframe the central contribution** as "specialized multi-view embeddings" or "multi-objective representation learning" rather than "disentangled representations," and acknowledge that the shared backbone fuses information across token types.
2. **Report imputation under block masking** with numerical values in the main paper alongside the hybrid masking results.
3. **Remove or heavily qualify the Chronos similarity search comparison.**
4. **Separate AD zero-shot variants**: report Head_ensemble (label-free) and Head_triang. (tuning-set-calibrated) distinctly.
5. **Add confidence intervals or standard deviations** for at least the main benchmark results.
6. **Normalize the sensitivity analysis** distortion metric by embedding dimension.

## Score and Decision

MY FINAL SCORE: 5.0  
MY FINAL DECISION: Reject