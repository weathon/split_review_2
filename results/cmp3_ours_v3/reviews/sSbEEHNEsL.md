Now let me write the final review.

**Calibration Analysis:**

**Round 1 bracket:** The paper sits between borderline-accept and accept papers (scores 5.5–7.5). Compared to:
- **Unsupervised ASR via Cross-Lingual Pseudo-Labeling** (5.25, Reject): Similar pseudo-labelling topic but our paper has a more novel core insight and stronger OOD evaluation. Our paper is clearly stronger.
- **CR-CTC** (6.75, Accept): Consistency regularization on CTC with modest WER gains. Our paper has a more substantial contribution (training efficiency + robustness) and more thorough evaluation across OOD dimensions. Our paper is stronger.
- **Align With Purpose** (7.00, Accept): Well-executed CTC plug-and-play framework with comparable rigor. Our paper has more practically compelling gains (2× speedup, large OOD improvements).
- **OTTC** (5.67, Reject with mixed 8/6/3): Novel perspective but trails baselines. Our paper outperforms baselines.
- **Rethinking pseudo-labeling** (5.00, Reject): Good idea but significant methodological gaps. Our paper is cleaner methodologically.

The paper's contributions (non-obvious CTC-driven teacher forcing insight, ~2× speedup, convincing OOD robustness gains, SOTA in-distribution) position it above the mid-range papers. The lack of variance reporting is the main weakness but doesn't invalidate the core claims given the large and consistent OOD improvements. Final score: **7.0**.

## Summary

This paper proposes USR 2.0, an improved semi-supervised framework for unified speech recognition (ASR, VSR, AVSR) that addresses two limitations of its predecessor USR: the computational cost of autoregressive pseudo-labelling and decoupled supervision that hurts out-of-distribution robustness. The core idea — CTC-driven teacher forcing — uses greedily-decoded CTC outputs to condition the decoder for generating attention-based pseudo-labels in a single forward pass, removing the AR bottleneck. A mixed sampling strategy (interleaving CTC-driven and AR modes) mitigates exposure bias. The method achieves ~2× faster training, improved OOD robustness on long utterances, noise, and cross-dataset evaluations, and state-of-the-art in-distribution results on LRS3/LRS2/WildVSR with a single unified model.

## Strengths

1. **A genuinely non-obvious insight about pseudo-labelling (Section 4.1, Equations 3–4).** CTC-driven teacher forcing replaces autoregressive decoding with conditioning on CTC outputs, which the paper acknowledges can be globally incoherent. The key argument — that global coherence of the teacher sequence is unnecessary in pseudo-labelling because teacher and student share the same conditioning context, making token-wise cross-entropy meaningful — is well-reasoned and distinguishes this design from naive teacher forcing.

2. **Strong, well-designed OOD evaluation (Section 5, Tables 1 and 3, Figures 3a–3c).** Robustness is evaluated across three distinct types of distribution shift: sequence length (VoxCeleb2, up to 600 frames vs. 155-frame training max), noise (NOISEX babble at 10dB to -5dB, zero-shot), and cross-dataset (LibriSpeech, WildVSR, AVSpeech). Results consistently favor USR 2.0, often by wide margins (e.g., Table 3: 15.4% vs. 25.3% WER on LibriSpeech under greedy decoding). The beam size ablation (Figure 3c) convincingly shows that the robustness gain reflects genuinely better decoder training, not just a CTC-scoring inference artifact.

3. **Training efficiency with no sacrifice of in-distribution quality (Section 6, Figure 5).** The ~2× training speedup is supported by concrete factors: faster per-step computation (CTC-driven steps avoid AR decoding) and faster convergence (50 vs. 75 epochs). In-distribution results (Table 2) show USR 2.0 matches or exceeds USR on LRS3 across all tasks and model sizes, with gaps widening at larger scales and with more pre-training data.

4. **Principled ablation design (Section 7, Table 4).** By isolating CTC-driven and AR modes and independently ablating which targets each branch predicts, the paper cleanly demonstrates that (a) both CTC and attention PL targets are necessary in CTC-driven mode, (b) OOD robustness comes specifically from CTC PL supervision, and (c) the CTC-driven mode is singularly responsible for OOD gains (24.2% vs. 40.1% OOD WER compared to AR-only mode).

## Weaknesses

### Fatal
None.

### Major

1. **No variance or statistical significance reported for any result.** Not a single number in Tables 1–4 comes with a standard deviation, confidence interval, or indication of multiple seeds. For in-distribution comparisons where improvements over USR are marginal (e.g., Table 2 Base LRS3: USR 2.0 VSR 36.2 vs. USR 36.0 — a regression; ASR 3.0 vs. 3.2 — a 0.2 gap), the absence of uncertainty quantification makes it impossible to assess whether these differences are meaningful or within run-to-run noise. While the OOD improvements are large enough to be convincing, the in-distribution claims would be significantly more credible with variance estimates. This is the paper's most significant methodological gap.

### Minor

1. **Training-time measurement is underspecified.** The paper's ~2× speedup claim (Figure 5) is central to the contribution, but the evidence lacks key details: the training hardware configuration is not stated, and it is unclear whether USR and USR 2.0 were run on identical hardware with identical batch sizes and data pipelines. The paper qualitatively attributes the speedup to "faster training steps" and "fewer epochs" (50 vs. 75) but does not quantify the per-component contribution. While the claim is plausible and consistent with the mechanism, the evidence is reported with insufficient detail for rigorous verification.

2. **The "global coherence" argument lacks direct empirical support in the main text.** The paper argues (Section 4.1) that CTC-driven attention PLs may lack global coherence but that this does not harm learning because teacher and student share the same conditioning context. While the theoretical justification is clearly stated, the main text offers no direct analysis — e.g., measuring the sequence-level WER of CTC-driven attention PLs vs. AR PLs against ground truth — to substantiate this core claim. The downstream results support the method's effectiveness but conflate multiple factors, leaving the coherence argument more asserted than verified.

### Trivial

1. **Confidence thresholding details are underspecified.** The paper mentions confidence-based filtering with a threshold of 0.8 and that sequence-level confidence is computed as the average log-probability over token predictions (Section 4.3). It is not stated whether the same threshold applies to both CTC and attention PLs independently, or what fraction of samples is filtered at this threshold.

## Nice-to-Haves

- A pseudocode block showing the training loop for one step would improve reproducibility.
- Quantifying the components of the 2× speedup (per-step time savings vs. epoch reduction) in a table would strengthen the efficiency claim.
- Analyzing whether certain types of samples benefit more from AR mode (rather than a fixed 0.5 random probability) could yield further insights.

## Removed Points

These points were raised in the input review but are removed or demoted with justification:

- **Sampling granularity not specified (per-sample vs. per-step).** The paper explicitly states "At each training step, we randomly sample a mode" (Section 4.2). This criticism is factually incorrect. **Removed.**
- **How decoder receives CTC tokens is underspecified.** The method description (Section 4.1, Equations 3–4) and Figure 2 provide sufficient detail — the collapsed CTC sequence is fed as input to the decoder via teacher forcing. **Removed** as a reproducibility nitpick about a point that is already clear.
- **Whisper oracle may inflate Figure 1 gap.** Speculative; the reviewer acknowledges relative comparisons are still meaningful. **Removed.**
- **Limited NAR baseline comparison.** Outside the paper's stated scope (CTC-driven teacher forcing, not NAR comparison). **Removed** as scope creep.
- **Huge model results not comparable to other rows.** The paper clearly marks the Huge model as a separate scaling experiment with a different training setup (* footnote). This is properly scoped and disclosed. **Removed.**
- **"Several methods do not report AVSR" as a weakness of this paper.** This is an issue with the baselines, not the paper. **Removed.**
- **Missing related works.** Cannot be verified without external sources. **Removed** per policy.
- **Pure formatting/style nitpicks.** **Removed** per policy.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run each experiment with at least 2–3 seeds and report mean ± std, especially for the in-distribution results (Table 2) where improvements over USR are small.
2. Decompose the 2× training speedup by reporting per-iteration time for USR vs. USR 2.0 (CTC-driven vs. mixed modes) alongside epoch counts.
3. Include a simple empirical analysis of the "global coherence" claim on a small labelled subset (e.g., WER of CTC-driven attention PLs vs. AR PLs against ground truth).
4. Clarify whether confidence thresholding is applied to attention PLs and what fraction of samples is filtered.

## Score and Decision

**Score:** 7.0

**Decision:** Accept

**Rationale:** The paper presents a well-motivated, non-obvious method (CTC-driven teacher forcing) with strong experimental support, particularly for OOD robustness where improvements are large and consistent. The evaluation is comprehensive (length, noise, cross-dataset), the ablations are clean, and the practical benefits (~2× training speedup, SOTA in-distribution) are clear. The primary weakness — absence of variance reporting — is real but does not invalidate the core contributions, which are well-supported by the scale and consistency of the observed improvements.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>