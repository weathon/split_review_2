Now I have all the data needed. Here is my final review.

## Summary

This paper introduces L-TTA, the first method designed specifically for long-tailed test-time adaptation of Vision-Language Models. It identifies two failure modes unique to this setting (Text-induced Tail Erosion and Modality-bias Amplification) and proposes three co-designed components: Synergistic Prototypes (SyPs) with exclusionary prototypes for contrastive signal, Rebalancing Shortcuts (RSs) for learnable adaptation, and Balanced Entropy Minimization (BEM) with theoretical grounding. The method is evaluated on 15 datasets across three benchmarks (OOD, Cross-Domain, Corruption) at three imbalance ratios, with consistent improvements.

## Strengths

- **Problem identification is novel and well-motivated.** The paper identifies two concrete failure modes unique to VLM-based LT-TTA — Text-induced Tail Erosion (pretraining biases in text embeddings compounding long-tailed effects) and Modality-bias Amplification (unimodal TTA methods worsening cross-modal misalignment). Figure 1 and Figure 2 provide clear visual and empirical evidence. This problem framing (TTA × VLMs × long-tailed distributions) has genuinely not been studied before.

- **Extensive and well-designed evaluation.** The paper evaluates on 15 datasets across three distinct benchmarks (OOD, Cross-Domain, Corruption) at three imbalance ratios (10/20/50), plus multiple backbone architectures (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG). Macro-F1 is reported alongside accuracy throughout — the correct metric for long-tailed evaluation. Ablation studies (Table 6) cleanly isolate each component's contribution.

- **Consistent improvement across nearly all settings.** L-TTA wins on 10/11 datasets in Cross-Domain (Table 2), all datasets in Corruption (Table 3), and most OOD datasets (Table 1). Macro-F1 gains over the best baselines are +2.20% (CDB), +2.64% (CB), +1.70% (OODB). The efficiency analysis (Table 4) shows these gains come with reasonable overhead (1.45h vs. 0.91h for TDA on ImageNet).

- **The BEM formulation is theoretically grounded.** Proposition 1 formalizes why standard EM amplifies head-class bias under long-tailed distributions, and the penalty term in Eq. 9 — weighting the log-amplified prior by $(1-\tilde{\mathbb{P}})^\beta$ — directly addresses this by reducing the contribution of already-confident classes. The ablation on $\beta$ (Fig. 4d) supports the design choice.

## Weaknesses

### Major

- **Inconsistency in the hyperparameter K.** The paper defines K as an integer count of hyper-class vectors (line 112: "assume there are K hyper-class vectors"), but the implementation details (line 208) state K=0.3 and the ablation (line 334) sweeps K from 0.1 to 1.0, concluding K=0.2 is optimal. The paper never clarifies whether K is an integer count, a ratio of the number of classes, or something else. This is a factual error: the main experiments use K=0.3 while the ablation identifies K=0.2 as optimal. The authors must (i) clarify what K physically represents, (ii) resolve the 0.3 vs. 0.2 discrepancy, and (iii) confirm whether main results change at the optimal value.

### Minor

- **The Exclusionary Prototypes (EPs) mechanism lacks direct analysis.** The paper frames EPs as "enriching tail class representations" (lines 40, 98, 110), but the mechanism in Eq. 8 subtracts EP similarity from predictions — making it an exclusionary/contrastive signal rather than a positive enrichment. While the ablation (Table 6) confirms EPs contribute (+3.22% macro-F1), the paper provides no visualization, nearest-neighbor analysis, or toy experiment showing what EPs actually learn or how their accumulated features behave. This does not invalidate the method but would significantly strengthen the paper's most novel claim.

- **Baseline hyperparameters were not tuned for the long-tailed setting.** The paper states methods are "reproduced with their provided hyperparameters" (line 208), which were designed for balanced TTA. Temperature parameters, in particular, can strongly affect entropy-based methods under imbalance. This is partially fair — the paper's argument is that existing methods *as designed* fail under LT — but the margin of improvement may partly reflect suboptimal baseline configuration. A sensitivity analysis for the strongest baselines' temperature would strengthen the comparison.

- **No error bars or confidence intervals.** The paper states 5 runs per experiment (e.g., Table 1 caption) but reports only averages without any measure of variance. This makes it difficult to assess statistical significance, especially on datasets where margins are small (e.g., ImageNet-A at Imb=50: L-TTA 60.07 vs. DPE 60.21 in accuracy).

### Trivial

- **Class prior feedback loop in BEM (Eq. 9).** The class prior is "continually updated based on the current predicted pseudo-labels" (line 138), creating a potential feedback loop where incorrect tail-class predictions lead to incorrect priors. The paper does not discuss or ablate this. A comparison of ground-truth priors vs. estimated priors would be straightforward to add.

- **Dataset construction edge case.** Line 206 notes "if the calculated cardinality is less than the class cardinality itself, we simply keep that class unchanged," meaning some classes in the constructed long-tailed sets may not actually exhibit imbalance. The paper should report what fraction of classes are affected.

## Nice-to-Haves

- A brief sketch of the proof logic for Proposition 1 in the main text (the full proof resides in the appendix, which is standard practice, but a 2–3 line intuition would help readability).
- Reporting what fraction of classes are affected by the dataset construction edge case (line 206).

## Removed Points

These points from the harsh critic input are removed per review policy:
- **Proofs deferred to appendix**: Removed — the parser strips appendices; deferring proofs is standard and the full proofs exist in the original submission.
- **"First" claims should be softened**: Removed — this is a presentation preference, not a substantive weakness. The paper's contributions stand on their own.
- **General speculative concerns about EPs not being robust** (signal-to-noise, OOD rejection): Removed — these are speculative without evidence that the mechanism actually fails, and the ablation confirms EPs contribute positively.
- **Strong criticism that EPs "do not enrich" tail classes**: The framing as "enriching" while the mechanism is subtractive is captured in the Minor weakness above. However, many contrastive methods use negatives to effectively enrich representations, so the framing is not fundamentally wrong — the ablation confirms the mechanism works.
- **Missing statistical significance analysis was reported in the Minor weaknesses section above, not removed.**

## Novel Insights

None beyond the paper's own contributions. The main insight from cross-referencing the reviews is that the K hyperparameter inconsistency (0.3 in implementation vs. 0.2 in ablation) is a concrete factual error that the authors should correct, and it interacts with the broader question of whether the main results are optimal.

## Suggestions

1. **Resolve the K inconsistency.** Clarify whether K is an integer count or a ratio. If 0.2 is truly optimal (per ablation), regenerate main results at K=0.2 or justify why 0.3 was used.
2. **Add a brief analysis of EP contents.** A simple nearest-neighbor visualization or synthetic 2D experiment showing what EPs learn would substantially strengthen the paper's central methodological claim.
3. **Add error bars to main results.** With 5 runs available, reporting standard deviations (or at least min/max ranges) would help assess statistical significance.
4. **Include a simple analysis of the class-prior feedback loop.** Compare using ground-truth class priors vs. estimated priors in BEM to show whether the feedback loop is a practical concern.
5. **Tune temperature for the strongest baselines** (at least TDA, DPE, SCAP) for the long-tailed setting to confirm the reported margins.

## Score and Decision

**Calibration anchor summary:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/.../5lUdTogEL3.md | 1.00 | R1 | No | Irrelevant (person re-ID); far below this paper |
| /home/.../gwZ90hFSL2.md | 1.00 | R1 | No | Irrelevant (robot NLP); far below |
| /home/.../pdzHpQbGrn.md | 2.50 | R1 | No | Active TTA prompting; weaker evaluation |
| /home/.../JIlIYIHMuv.md | 2.50 | R1 | No | VLM continual learning; weaker evaluation |
| /home/.../ZaudLwn0Hm.md | 2.50 | R1 | No | Few-shot VLM adaptation; different setting |
| /home/.../gNoqEdT2wO.md | 2.33 | R1 | No | Multimodal continual learning benchmark |
| /home/.../BUDxvMRkc4.md | 4.67 | R1 | Yes | Long-tailed CLIP; incremental innovation concerns, weaker eval |
| /home/.../lF9QXpfNHm.md | 4.67 | R1 | Yes | Open-world VLM TTA; missing baselines, incomplete eval |
| /home/.../9RnTw9YiXV.md | 4.40 | R1 | No | LT in LVLMs; analysis paper, different scope |
| /home/.../Rc3RP9OoEJ.md | 5.00 | R1 | No | In-context prompt learning; less extensive eval |
| /home/.../b20VK2GnSs.md | 7.00 | R1/R2 | Yes | Concept drift in MLLMs; cleaner theory but experimental concerns |
| /home/.../yD2JMeKumt.md | 6.00 | R1/R2 | Yes | DOTA; rejected for unclear methodology; below this paper |
| /home/.../kIP0duasBb.md | 6.67 | R1/R2 | Yes | RLCF; accepted with comparable innovation, weaker eval breadth |
| /home/.../k9NYnsC4Mq.md | 5.67 | R2 | Yes | PROOF; rejected, weaker evaluation, methodological concerns |
| /home/.../sb7qHFYwBc.md | 6.50 | R2 | Yes | C-CLIP; accepted despite typos and presentation issues |
| /home/.../eE2PXlNydB.md | 6.00 | R2 | Yes | ClusPro; CZSL, different task, weaker evaluation breadth |

**Final score determination:** The paper sits between DOTA (6.00, Reject) and RLCF (6.67, Accept) / C-CLIP (6.50, Accept). Its evaluation is decisively stronger than all three (impact +9.59 for eval, +10.00 for results), and its problem framing is genuinely novel. The two main weaknesses — the K inconsistency (-9.59 impact) and the EPs analysis gap (-9.95 impact) — are fixable reporting/analysis gaps rather than fundamental methodological flaws. Unlike DOTA (rejected for unclear methodology), this paper's method is well-specified. The paper's strong evaluation (+9.59, +10.00) and clear motivation (+6.17) outweigh its fixable weaknesses. Placing it within the 6.0–7.0 bracket, at **6.5**: borderline accept with clear acceptance rationale, conditional on the authors resolving the K inconsistency.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>