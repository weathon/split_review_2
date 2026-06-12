Now I have enough calibration data. Let me finalize my review.

**Calibration analysis:**

**Key anchors retrieved:**
- MINDE (score 6.50, Accept) — direct predecessor using continuous diffusion for MI estimation
- SEDD (score 6.60, Reject) — direct predecessor of the CTMC score entropy framework
- Data Derangement DIME (score 5.60, Reject) — variational MI estimator improvement
- Convergence of Score-Based Discrete Diffusion (score 7.00, Accept) — theoretical discrete diffusion analysis
- How Much is Unseen (score 7.33, Accept) — information-theoretic estimator
- NetInfoF (score 7.33, Accept) — network usable information framework
- Faster Approximation of Probabilistic Values (score 7.50, Accept) — efficient estimation method
- InfoNet (score 5.75, Reject) — feed-forward neural MI estimator
- Normalizing Flows MI Estimator (score 4.83, Reject) — normalizing flow MI estimation
- Sparsistency for Inverse OT (score 6.75, Accept) — theoretical information/optimization
- Data Usage Inference (score 7.60, Accept) — dataset information inference

**Round 1 bracket: 6.5–7.5**

This paper is clearly stronger than MINDE (6.50) because it targets the harder problem of discrete data, achieves dramatically better synthetic results, and has stronger theoretical grounding (formal error bound). It is comparable to the Convergence of Discrete Diffusion paper (7.00) but with more practical breadth. The unexplained discrepancy between INFO-SEDD-C and INFO-SEDD-J (~800 vs ~400 nats) and the derivation clarity issue are real but fixable weaknesses. The paper has genuinely novel ideas (absorbing-state trick for single-model MI) and exceptionally strong synthetic evidence.

**Final score: 7.0**

---

## Summary
INFO-SEDD proposes a discrete diffusion-based method for estimating information-theoretic quantities (KL divergence, MI, entropy) directly on high-dimensional discrete data, using CTMC score functions and Dynkin's formula. A key practical innovation is the absorbing-state trick, which enables single-model MI computation by recovering marginal scores from a model trained only on the joint distribution. Experiments on synthetic benchmarks, text summarization, and genomics demonstrate strong accuracy, with INFO-SEDD dramatically outperforming all competitors at high MI and dimensionality.

## Strengths
- **Formal error bound with explicit consistency guarantee (Equation 7)**: The estimator error decomposes into a score approximation term and a truncation bias that vanishes exponentially with the absorbing-state probability, giving concrete conditions under which INFO-SEDD is reliable — a significant advantage over variational estimators that suffer exponential variance at high MI.
- **Dramatically superior accuracy on synthetic benchmarks (Table 1)**: At MI=50, D=50, INFO-SEDD estimates 47.77±1.18 while all competitors collapse (best: GAN-DIME at 17.27±1.46). Results are consistent across all five settings with uniformly low variance, using the same backbone and training budget for all methods.
- **Absorbing-state CTMC design enables single-model MI computation (Equation 6)**: By absorbing Y into ∅, marginal scores can be recovered from a model trained only on the joint distribution, halving model count relative to a naive KL[joint ‖ marginal] approach.
- **Compelling real-world applications**: (a) Motif discovery in *Arabidopsis thaliana* promoters (Figure 5) correctly identifies the TATA-BOX at the expected position (~-35 bp from TSS), with the single-window masking approach being robust to correlated motifs. (b) Text summarization model selection (Table 2) shows INFO-SEDD-C achieves Pearson r=0.740 with the consistency metric, far exceeding competitors (next best: KL-DIME at 0.214). (c) Genomics consistency test (Figure 4) closely tracks the classifier-based reference MI.
- **Well-designed consistency tests with principled empirical references (Figures 1, 4)**: The controllable mixing of matched/random pairs at rate ρ provides a principled test of estimator reliability, and INFO-SEDD variants track expected linear trends while competitors plateau or underestimate.

## Weaknesses

### Fatal
None.

### Major
- **Overloaded notation in core derivation (Equations 2–5)**: The subscripts $\vec{p}_0$, $\vec{q}_0$ are used for both the forward-time data distributions and the reverse-time terminal distributions. The transition from E[log p₀/q₀(X_T)] to E[log p_T/q_T(X_T)] in Equation (2) is not made explicit, and the statement "both p₀ and q₀ converge to π" (below Equation 4) is confusing — the data distributions are fixed; it is the forward-evolved distributions that converge to π. The paper cites Appendix E for proofs, and the final estimator (Equation 5) is mathematically sensible, but the main-text derivation is not self-contained enough for readers to independently verify the core argument. This weakens accessibility and is the type of issue that, if fixed, would substantially strengthen the paper.

### Minor
- **Unexplained ~2× discrepancy between INFO-SEDD-C and INFO-SEDD-J on text data**: From Figure 1, INFO-SEDD-C gives ~800 nats while INFO-SEDD-J gives ~400 nats at ρ=1. These should estimate the same quantity. The genomics section (Section 4.3) provides an explanation for the genomics case (different dimensionality making optimization easier for C variant), but no analogous discussion is provided for the text summarization experiment. This matters for practitioners choosing between variants and raises a question about whether one variant has a systematic bias.
- **No computational cost comparisons**: The paper claims efficiency and seamless integration with pretrained models but never reports wall-clock training times, memory usage, or inference cost relative to competitors. Since discrete diffusion model training has its own overhead, this comparison is important for assessing practical scalability.
- **Approximate real-world references**: The text summarization reference (256–303 nats) derives from entropy-rate estimates multiplied by summary length — acknowledged as an order-of-magnitude estimate with ~18% uncertainty band. The genomics reference uses H(Y|X) ≈ H_b(Acc.), assuming uniform classification error. The paper acknowledges these as approximations, and for the text experiment the claim is about consistency rather than absolute accuracy, but the strength of real-world evidence is weaker than the synthetic experiments suggest.

### Trivial
None.

## Nice-to-Haves
- Sensitivity analysis for the time horizon T and noise schedule σ(t), which control truncation bias and diffusion dynamics. Guidance on how these should be set in practice would help practitioners.
- Discussion of the practical training cost implications of INFO-SEDD-C's two-pass requirement (estimating both p_{Y|X} and p_Y).
- Ablation on the support size |χ| in the main text (the paper mentions Appendix C.1.6 but the main tables fix |χ|).

## Removed Points
These points are flagged to be removed, treat them with caution.
- Harsh critic's general concern about "real-world evaluations lack ground truth" — weakened rather than removed because the paper does acknowledge approximate references and the text experiment tests consistency rather than absolute accuracy. Still a valid point about evidential strength.
- Strength finder's "seamless integration with pretrained models" — generic and not distinguishing; many methods can be adapted to use pretrained backbones.
- Strength finder's "scalability via sparse rate matrices" — standard for the discrete diffusion literature (cited in footnote 1) and not novel to this paper.
- Strength finder's "Generality of framework — entropy estimation extension" — this is a straightforward consequence of the KL estimator and not a major distinguishing contribution.

## Novel Insights
The absorbing-state CTMC design (Equation 6) is a genuinely novel insight: by choosing the absorbing transition matrix, marginal scores can be recovered from a model trained only on the joint distribution. This is both theoretically elegant (proof in Appendix A.3) and practically important (halves model count). The application of Dynkin's formula to express KL divergences through CTMC score functions is a novel connection bridging information theory and discrete generative modeling, and the resulting estimator avoids the exponential variance issue that plagues variational approaches.

## Suggestions
- Clarify the notation in Equations (2)–(5): explicitly define what subscripts mean in each expression, show how Dynkin's formula is applied to f = log(p_t/q_t), and explain the omitted term with more precision.
- Add a paragraph discussing why INFO-SEDD-C and INFO-SEDD-J diverge substantially on the text summarization experiment.
- Include wall-clock training time and memory comparisons against competitors.
- Provide guidance on hyperparameter selection for T and σ(t).

## Score and Decision

**Reporting calibration anchors:**

| Round | Path | Avg Human Score | Comparison |
|-------|------|----------------|------------|
| 1 | kKXIYUi8ff (DynamicsDiffusion) | 3.00 | Weak diffusion paper, rejected; unrelated topic |
| 1 | 5sPgOyyjG5 (FKEE) | 3.00 | Weak estimator paper, rejected; much less complete |
| 1 | vgQmK5HHfz (Normalizing Flows MI) | 4.83 | MI estimator using normalizing flows, rejected; less novel |
| 1 | KC2MViQASx (Data Derangement DIME) | 5.60 | Variational MI estimator, rejected; incremental improvement |
| 1 | PyHRUMxKbT (InfoNet) | 5.75 | Feed-forward MI estimator, rejected; less principled |
| 1 | 0kWd8SJq8d (MINDE) | 6.50 | Diffusion-based MI estimation (continuous), accepted; directly comparable, weaker |
| 1 | 71mqtQdKB9 (SEDD) | 6.60 | Score entropy for discrete diffusion, rejected; predecessor of framework used here |
| 1 | pq1WUegkza (Convergence Discrete Diffusion) | 7.00 | Theoretical convergence analysis, accepted; comparable quality, less practical |
| 1 | tQyh0gnfqW (DDSBM) | 5.67 | Discrete diffusion Schrödinger bridge, accepted; different focus |
| 1 | XsgHl54yO7 (Guidance Discrete Diffusion) | 6.50 | Guidance for discrete diffusion, accepted; different focus |
| 1 | uqWM9hBDAE (How Much Unseen) | 7.33 | Information-theoretic estimator, accepted; different domain |
| 2 | lvSMIsztka (Faster Probabilistic Values) | 7.50 | Efficient estimation method, accepted; different domain |
| 2 | EUSkm2sVJ6 (Data Usage Inference) | 7.60 | Dataset information inference, accepted; different domain |
| 2 | wpXGPCBOTX (Sparsistency iOT) | 6.75 | Inverse OT theory, accepted; different domain |

**Round 1 bracket: 6.5–7.5**

The paper is clearly stronger than MINDE (6.50) — it addresses the harder problem of discrete data directly, achieves dramatically better synthetic results, has a formal error bound, and has more diverse applications. It is comparable to the Convergence of Discrete Diffusion paper (7.00) but with broader practical impact. The key weaknesses (derivation clarity, unexplained variant discrepancy, missing computational cost) are genuine but do not undermine the core contribution.

**Round 2 refinement:** The paper sits between MINDE (6.50) and the 7.0–7.5 range of strong accepted papers. The core contribution is novel and well-supported; the synthetic evidence is exceptionally strong. The weaknesses are fixable and do not threaten validity. Final score: **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>