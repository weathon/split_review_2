## Summary

This paper proposes LoLoRA, a fine-tuning method for LLMs that combines local unsupervised updates (HPCA) of the LoRA adapter matrix A during the forward pass with gradient-based updates of matrix B via backpropagation. The goal is to avoid storing activations for A's backward pass — matching the memory profile of LoRA-FA (frozen A) — while matching the performance of standard LoRA through online adaptation. The paper also provides theoretical analysis (Theorem 4.4, 4.5) characterizing the optimal initialization of adapter A under a random regression model, showing it should span the top-r eigenvectors of the input covariance.

## Strengths

- **Theoretical analysis (Section 4) is the paper's strongest asset.** Theorem 4.4 provides a clean characterization of the optimal LoRA adapter A under a random regression model: any nonsingular linear transformation of the top-r eigenvectors of the input covariance. Theorem 4.5 confirms the asymmetry between A and B (any full-rank B is equally optimal). These results are genuinely informative for the LoRA literature and provide the theoretical justification for PCA-based initialization that prior work (EVA) lacked, independent of whether LoLoRA itself succeeds as a method. **[weight=9.03]**

- **Thorough ablation study (Section 5.4).** The paper systematically compares five local update rules (HPCA variants, AE, SoftHebb) and four initialization strategies (uniform, orthogonal, PiSSA, EVA) across three ranks (r=2,4,8). This provides useful empirical ground truth for the community. **[weight=9.46]**

- **Clear exposition of the method.** Algorithm 1 is clearly stated, the motivation (avoiding storing activations for A's backward pass) is straightforward, and Figure 1 correctly summarizes the memory-flow differences between LoRA, LoRA-FA, and LoLoRA. **[weight=9.51]**

## Weaknesses

### Fatal
None.

### Major

1. **The headline claim of "comparable performance to standard LoRA" is not supported by the experimental evidence.** The abstract states the method "maintains performance comparable to standard LoRA," but across the 10 task comparisons (8 GLUE tasks + LLaVA + MetaMathQA), LoLoRA is numerically worse than standard LoRA on 9 of them. Several gaps exceed typical GLUE variance (CoLA: 69.6 vs 66.3, −3.3; MRPC: 90.9 vs 89.9, −1.0; QQP: 91.7 vs 90.6, −1.1). Only on MetaMathQA does LoLoRA beat LoRA (0.829 vs 0.821). The paper should honestly frame this systematic degradation rather than calling it "comparable."

2. **LoLoRA does not outperform the simpler LoRA-FA with EVA initialization, which is the relevant baseline.** The paper's premise is that LoRA-FA (freezing A) degrades performance and LoLoRA's local updates fix this. However: (a) On GLUE, LoLoRA vs LoRA-FA (EVA) differences are within ±1.6 points with overlapping error bars; (b) On MetaMathQA, LoLoRA (0.829±0.004) and LoRA-FA (EVA) (0.829±0.005) are **identical**; (c) On LLaVA, LoLoRA perplexity (2.93) is *worse* than LoRA-FA (EVA) (2.92). The paper's own ablation summary states: *"all local update rules that converge to the optimal PCA subspace perform equally well. Similarly, LoRA-FA with EVA initialization achieves comparable performance."* This is an admission that the central mechanism — online local adaptation — provides no benefit over one-shot PCA initialization followed by freezing.

3. **LoLoRA provides no meaningful memory advantage over LoRA-FA.** Both methods avoid storing activations for A's backward pass. The paper's own memory numbers confirm this: on MetaMathQA both use 26 GB; on LLaVA, LoLoRA (24.1 GB) uses *more* memory than LoRA-FA (uniform) (23.9 GB). The paper frames memory savings against standard LoRA, but those savings are already achieved by the simpler LoRA-FA baseline. LoLoRA also requires extra optimizer state for the local updates (acknowledged in the conclusion).

### Minor

4. **The theoretical analysis relies on a strong i.i.d. Gaussian assumption for ΔW₀ (Assumption 4.1) that is not discussed or validated.** Each entry of the optimal weight change is modeled as i.i.d. Gaussian, but real LoRA fine-tuning produces structured weight updates. The paper acknowledges the stationarity limitation but not the Gaussian regression assumption itself. Whether the real optimization landscape of a transformer can be reasonably approximated by this model is not argued, and no experiment bridges this theory-practice gap.

5. **The ablation study shows consistent degradation vs full LoRA that is not discussed.** In Table 6, Full LoRA achieves 2.537 (r=2), 2.528 (r=4), 2.521 (r=8) on TinyLlama+Alpaca. The best LoLoRA variants achieve 2.557, 2.545, 2.535 — non-overlapping degradation at every rank. The paper reports these numbers but does not discuss this gap.

6. **The MetaMathQA evaluation reports the best result over multiple checkpoints (every 0.2 epoch) rather than the final result.** This inflates all methods equally, making comparisons between methods still fair, but the absolute numbers are less clean for reproducibility.

### Trivial
None.

## Nice-to-Haves

- **Test the adaptation-to-distribution-shift claim directly.** The paper's central mechanistic argument is that LoLoRA adapts A to distribution shifts during fine-tuning. An experiment with a known distribution shift (e.g., multi-domain or curriculum setup) comparing LoLoRA's A drift against LoRA-FA (EVA)'s fixed A would directly test this claim.
- **Quantify subspace alignment** between LoLoRA's learned A and the true PCA subspace of inputs during real fine-tuning, to validate whether the theoretical prediction (Theorem 4.4) holds empirically under transformer conditions.
- **Include a performance-memory Pareto plot** across LoRA, LoRA-FA (uniform), LoRA-FA (EVA), and LoLoRA to honestly characterize trade-offs.

## Removed Points

The following points from the harsh critic review were removed for the stated reasons:

1. **"No comparison of wall-clock time versus memory savings"** — Partially addressed: Table 4 includes run time for LLaVA. The availability of timing data makes this more of a nice-to-have than a missing analysis.

2. **"No analysis of rank as a hyperparameter"** — The paper provides ablation across ranks r=2,4,8 in Table 6, which is standard coverage for LoRA papers.

3. **"EVA initialization overhead should be quantified"** — The paper acknowledges this advantage. The criticism is a suggestion, not a gap.

4. **"No discussion of when LoLoRA might be harmful"** — This is a framing suggestion, not an empirical gap. The paper reports the data honestly.

5. **"The theory justifies initialization, not updating"** — The paper explicitly motivates HPCA updates as converging to the same subspace the theorem identifies as optimal. The theory validates the target subspace; the local update rules are a means of reaching it without a separate PCA pass. This reading is consistent with the paper's text.

6. **"Conclusion claim is misleading about 'outperforms standard LoRA-FA'"** — Against LoRA-FA (uniform initialization, the "standard" variant), LoLoRA beats LoRA-FA on MetaMathQA (0.829 vs 0.826) and LLaVA (2.93 vs 2.97 perplexity), and has mixed results on GLUE. The claim "two out of three experimental setups" is technically accurate per the paper's reported data.

7. **Figure caption formatting** — Parser artifact, removed per hard rules.

8. **Missing appendix content** — The parser strips appendix text from all papers. Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis confirms that the paper has a genuine theoretical contribution and a thorough ablation study, but the method claims are not supported — a conclusion that emerges directly from the reported data rather than from any external insight.

## Suggestions

1. **Reframe the paper around its theoretical contribution.** The strongest contribution is Section 4 (Theorem 4.4, 4.5), which provides a principled justification for PCA-based initialization of LoRA A. The current method-centric framing (LoLoRA) creates expectations that the experiments do not satisfy. A reframing as a theoretical analysis paper with LoLoRA as a practical instantiation would better match the evidence.

2. **Add the distribution-shift experiment** described in Nice-to-Haves — this is the single most impactful experiment that could validate (or refute) the paper's core mechanistic claim.

3. For the MetaMathQA experiment, report final checkpoint results alongside the best-of-checkpoint results.

## Score and Decision

**Bracket (Round 1):** 3.5–5.5, narrowed to 4.0–5.0.

**Calibration anchors:**
- **EVA** (4.75, Reject): Directly related. LoLoRA provides the theory EVA lacked, but its method claims are weaker. Comparable quality.
- **LoRA-FA** (5.33, Reject): Key baseline. Core claim empirically supported. LoLoRA is weaker here since it cannot improve on this baseline.
- **MoRA** (4.75, Reject): Method paper with mixed support. Similar in that improvements are not universal.
- **GLoRA** (4.75, Reject): Theory-experiment gap noted, similar to LoLoRA's gap.
- **RoCoFT** (5.00, Reject): Marginal gains, limited novelty.

**Weighted comparison:** LoLoRA's strength weights (9.03 theory, 9.46 ablation, 9.51 exposition) are comparable to the best anchor items. Its structural weakness weights (-1.66, -1.35 for not beating LoRA-FA EVA and no memory advantage) place it below LoRA-FA (5.33) whose core claim held up, but above pure incremental novelty cases because the theoretical analysis has standalone value. The paper sits closest to EVA (4.75) — both have a useful idea but the empirical evidence falls short of the claims.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>