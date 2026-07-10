Now let me write the final consolidated review.

## Summary

This paper introduces ChaosNexus, a foundation model for zero-shot forecasting of chaotic dynamical systems. The core architectural contribution is ScaleFormer, a U-Net-inspired encoder-decoder Transformer with hierarchical patch merging/expansion, MoE layers, and a wavelet-based frequency fingerprint. The model is pretrained on 20K synthetic chaotic ODE systems and evaluated on a 9.3K-system held-out test set and on real-world weather forecasting (WEATHER-5K). The paper also contributes a scaling analysis showing that increasing the diversity of training systems improves generalization far more than increasing per-system trajectory count.

## Strengths

**1. Valuable scaling analysis (Section 4.3, Figure 4).** The paper's cleanest result. The finding that increasing system diversity (number of distinct ODE systems) improves zero-shot generalization far more than increasing per-system trajectory count is a practically useful design principle for scientific foundation models. Figure 4(b) shows a nearly flat curve for per-system data scaling while Figure 4(c) shows clear improvements from adding more systems, documented with error bars and not confounded by architecture comparisons.

**2. Strong domain-specific framing (Figure 2).** The paper convincingly demonstrates that general-purpose time-series foundation models (Chronos, TimesFM, etc.) perform poorly on chaotic system forecasting, and that fine-tuning on the chaotic corpus helps (Chronos-S-SFT). This establishes that chaotic dynamics are a distinct domain warranting specialized models — a finding useful independent of whether the specific ScaleFormer architecture is optimal.

**3. Well-motivated architectural design (Section 3.2).** The observation that chaotic systems exhibit dynamics at multiple time scales, and that single-resolution architectures may struggle to capture this structure, is sound. The U-Net-inspired encoder-decoder with hierarchical patch merging and expansion is a reasonable architectural response, backed by clear equations and Figure 1.

## Weaknesses

### Major

**1. Weather evaluation confounded — does not isolate the multi-scale architecture's contribution (Section 4.2).** In the weather task, ChaosNexus is pretrained on 20K synthetic systems and then evaluated zero-shot or fine-tuned on WEATHER-5K, while baselines (CrossFormer, FEDFormer, Koopa, PatchTST, Transformer) are trained *from scratch* on 85K or 473K weather samples. As the paper itself acknowledges, "foundation models designed for chaotic system forecasting...including ChaosNexus, Panda, and Chronos-S-SFT, perform significantly better" (line 217), confirming the advantage comes from pretraining on the chaotic corpus, not from the multi-scale architecture. The dramatic gap in Figure 3 (ChaosNexus ~0.8°C MAE vs. baselines ~3–4.5°C) is primarily a pretraining advantage, not evidence for ScaleFormer. The paper claims "ChaosNexus also outperforms Panda on many variable forecasting tasks" (line 217) but defers these to the appendix; the main paper therefore provides no controlled comparison that isolates the architecture's contribution on real-world data.

**2. Overclaimed abstract and mixed evidence against the principal baseline (Section 4.1, Figure 2).** The abstract claims "notable improvements in the fidelity of long-term attractor statistics," but the evidence against Panda — the most relevant baseline (same training corpus, same patch embedding, same axial attention, same pretraining strategy) — is mixed. On D_frac (correlation dimension error), ChaosNexus has mean ~0.225 vs. Panda ~0.200 — Panda is better (Figure 2 caption, line 175). On D_step (KL divergence of attractors), both are ~1.2 — essentially identical (line 176). On sMAPE@128/512, ChaosNexus achieves ~69 vs. Panda ~75 — a modest ~8% relative improvement. So on two of the four main metrics shown in Figure 2, ChaosNexus is tied with or worse than Panda. The paper's text says "reduces the average correlation dimension error to 0.203" (line 164) without noting that Panda's mean is 0.200, and describes D_step as demonstrating "superior fidelity" when both models achieve ~1.2. The framing of "state-of-the-art zero-shot performance" is overstated given that the closest baseline matches or beats it on half the evaluation dimensions presented in the main paper.

### Minor

**3. Internal framing inconsistency.** The paper argues multi-scale modeling is crucial because chaotic systems have dynamics at multiple time scales, predicting the largest benefits on attractor metrics (D_frac, D_step, D_lyap, ME_LRW). However, the available improvements against Panda are on point-wise sMAPE, while D_frac is worse and D_step is tied. This is the reverse of what the paper's motivation would predict. The paper should explain why a multi-scale architecture improves short-term point-wise accuracy but not long-term attractor statistics, or acknowledge that the evidence does not cleanly support the claimed mechanism.

**4. No inference cost comparison despite added complexity.** The method adds significant architectural components (U-Net encoder-decoder with multiple levels, MoE with gating, wavelet scattering) beyond Panda's framework, but the paper does not report inference time, memory usage, or training cost relative to Panda. If the ~8% sMAPE improvement comes at substantially higher compute, practitioners may prefer the simpler baseline.

**5. Key architectural hyperparameters deferred to appendix.** The main paper's method section does not specify the number of encoder/decoder levels, the patch length D, the number of MoE experts M and top-K, or the loss weights λ₁, λ₂. (These exist in the appendix of the actual submission.)

### Trivial

None.

## Nice-to-Haves

- Report absolute sMAPE values alongside the 49.83% relative improvement claim for parameter scaling (Section 4.3), since percentage improvement alone is uninformative without base values.
- Include the ChaosNexus vs. Panda weather comparison in the main paper rather than the appendix; this is the most direct test of whether the multi-scale architecture helps on real-world data.
- Add a minimal ablation (full model, without MoE, without wavelet fingerprint, without U-Net) on the synthetic benchmark to show which components drive the sMAPE improvement over Panda.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"The paper lacks controlled ablation studies in the main text"** — REMOVED per instructions: the appendix (which exists in the actual submission) contains ablation studies; the parser strips appendix content from all papers.
2. **"Weather evaluation uses only MAE for temperature"** — REMOVED: the paper states detailed results of all weather variables are in Appendix A.6, which exists in the actual submission.
3. **"Complexity reduction from axial attention is not a contribution of this paper"** — This is a factual observation, not a weakness. The paper does not claim axial attention as novel.
4. **"No discussion of the random polynomial and Fourier features"** — REMOVED: these are explicitly described as adopted from Panda (line 74: "an approach adopted from recent work (Lai et al., 2025)").

## Novel Insights

None beyond the paper's own contributions. The key discrepancy highlighted by the reviews — that the paper claims multi-scale modeling improves long-term attractor statistics, but the available data shows improvements on point-wise accuracy while attractor metrics are tied or worse against Panda — is a useful observation that the authors should address but does not constitute a novel insight beyond what the paper itself needs to resolve.

## Suggestions

1. Add a controlled weather experiment where Panda (and ideally DynaMix) is also pretrained on the same corpus and fine-tuned on WEATHER-5K, so the comparison isolates architecture from pretraining advantage.
2. Report both sMAPE and attractor metrics for ChaosNexus vs. Panda in the same figure/table with honest discussion of where the model underperforms its baseline, and tone down the abstract to match what the data actually show.
3. Include an inference cost comparison (time, memory, parameters) against Panda.
4. Report absolute sMAPE values at each model size in Section 4.3, rather than only the relative percentage improvement.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| SvjFHucuDZ.md (FMint) | 4.50 | R1 | Yes | DE foundation model with overclaimed results and unfair comparisons — similar weaknesses, but ChaosNexus has better architecture clarity and a real scaling contribution |
| NPSZ7V1CCY.md (Zero-shot Imputation) | 6.25 | R1 | Yes | Stronger paper overall with cleaner evaluation — ChaosNexus doesn't reach this bar |
| 4NhMhElWqP.md (DAM) | 7.00 | R1 | Yes | Foundation model for forecasting with stronger execution — ChaosNexus is weaker |
| 9EBSEkFSje.md (GIFT-Eval) | 5.25 | R1 | Yes | Benchmark paper — less comparable |
| S8nFZ98pmU.md (Contrastive Meta Learning) | 4.75 | R1 | Yes | Dynamical systems zero-shot — similar topic but weaker methodology than ChaosNexus |
| f3NLRksLiZ.md (Reservoir Transformer) | 4.25 | R1 | Yes | Chaotic time series — similar level of overclaim |
| ntSP0bzr8Y.md (PowerGPT) | 3.00 | R1 | Yes | Much weaker foundation model paper |

**Round 1 bracket:** 4.0–5.5. The paper has genuine contributions (scaling analysis [+9.99], domain-specific framing [+8.13]) that push it above weak-reject territory, but the two major weaknesses (confounded weather evaluation [-9.95], overclaimed abstract/mixed evidence [-10.00]) prevent it from reaching borderline-accept. The central claim about multi-scale architectural improvements is not convincingly supported in the main paper, placing it closer to FMint (4.50, REJECT) than to Zero-shot Imputation (6.25, ACCEPT).

**Final score: 4.5**

**Final decision: Reject**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>