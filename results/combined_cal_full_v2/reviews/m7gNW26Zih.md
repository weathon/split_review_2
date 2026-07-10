Now let me write the final review.

## Summary

This paper addresses language-based audio retrieval using a dual-encoder framework enhanced with three techniques: (i) soft-label distillation from an ensemble of pretrained retrieval teachers, (ii) LLM-driven caption augmentation (back-translation and caption mixing), and (iii) cluster-guided auxiliary classification. On the CLOTHO dataset, the best single model achieves 46.6 mAP@16 and a weighted ensemble reaches 48.83 mAP@16. The paper provides a reproducible description of the system components and a clear motivation for softening binary correspondence assumptions in audio-text retrieval.

## Strengths

- **Clean motivation for softening binary correspondence assumptions (Section 2.2).** The paper correctly identifies that CLOTHO's audio-caption pairs do not reflect a strict one-to-one mapping, and using soft targets from an ensemble of pretrained models to address this is a well-motivated idea with clear formulation (Eqs. 5–8).

- **Reproducible description of LLM augmentation pipeline (Section 2.4).** The paper specifies two concrete augmentation strategies (back-translation and LLM mix for mixed audio) with enough detail to reproduce. Creating 50k synthetic audio-text pairs is a non-trivial engineering contribution.

- **Consistent improvements from distillation across all three audio backbones.** The gain from SID 1 (no distillation) to SID 2 (distillation only) is +4.54 to +5.77 mAP@16 across PaSST, EAT, and BEATs, demonstrating robust effectiveness of the soft-label distillation approach.

- **Cluster-guided auxiliary task is conceptually interesting (Section 2.3).** The idea of clustering captions into semantic topics and training the audio encoder to predict these cluster labels as an auxiliary task is a creative approach to strengthening audio-text alignment, even if the empirical results are mixed.

## Weaknesses

### Fatal

None.

### Major

- **The two claimed novel contributions (LLM augmentation and cluster-guided classification) do not reliably improve over the distillation-only baseline — and in several cases they hurt.** Verified against Table 2:
  - *Augmentation (SID 2 → SID 3):* Helps EAT (+0.70) and BEATs (+0.77) but hurts PaSST (−0.21), the best-performing backbone.
  - *Clustering (SID 3 → SIDs 4/5):* Hurts EAT (−0.71 on both SID 4 and 5) and BEATs (−0.08 to −0.78), and yields only noise-level changes on PaSST (−0.02 to +0.09).
  - *Full system with all three techniques (SID 5) vs. distillation alone (SID 2):* PaSST 46.50 < 46.62, EAT 45.34 ≈ 45.35, BEATs 43.88 ≈ 43.89. The full system does not outperform distillation alone on any backbone.
  
  The abstract claims these techniques "jointly improve robustness," and the introduction lists them as contributions, but the data directly contradicts this claim. The paper does acknowledge "mixed single-model gains" in the conclusion (line 206), but the core framing of the paper is at odds with its own results.

- **No comparison to prior work.** The paper reports mAP@16 on CLOTHO but provides no external baselines, no prior published results, and no SOTA context. Without this, a reader cannot assess whether the reported numbers (single-model 46.6, ensemble 48.83) represent a meaningful advance. This is a fundamental omission for a system paper at a research conference.

- **No statistical significance or variance reporting.** All results in Table 2 appear to be from single runs. Several comparisons involve differences of 0.02–0.21 mAP@16 — margins that could easily fall within run-to-run variance. Without multiple seeds or confidence intervals, the reader cannot distinguish genuine improvements from random variation. This is especially problematic given that the paper's central claim about the novel components relies on extremely small differences.

- **Acknowledged reliance on adopted technique.** The distillation loss is the single clearly effective component (gains of +4.5–5.8 mAP@16), but it is explicitly adopted from prior work (Primus et al., 2024, top-ranked DCASE 2024 Task 8 system). The two components presented as contributions (augmentation and clustering) show mixed-to-negative additive value. This leaves the paper in an awkward position: the technique that works is not novel, and the techniques presented as novel do not reliably improve results.

### Minor

- **Key details about the clustering procedure are missing.** The paper does not report the number of clusters produced, the dimensionality of embeddings before clustering, or the specifics of the outlier reassignment process. The number of clusters is a critical hyperparameter for the auxiliary classification head's output dimension (line 94: "projecting the output to a vector with dimensions equal to the number of clusters").

- **No qualitative analysis.** The paper provides no examples of augmented captions, no cluster topic visualizations, no analysis of retrieval successes or failures, and no discussion of why different backbones respond differently to the same techniques. This makes the paper feel abstract and prevents the reader from building intuition about the methods.

- **The evaluation set performance drop is not discussed.** The paper reports mAP@16 of 0.421 on the evaluation set (line 198), which is substantially lower than the dev test results (0.46–0.49). This drop is stated without any analysis or explanation.

- **"Multiple annotation" vs. "Single annotation" protocol is undefined.** Table 2 uses these column headings without explanation. Given that CLOTHO has five captions per audio, the reader needs to know what these settings mean and how mAP is computed in each case.

- **Abstract claims unsupported in main text.** The abstract states "ablations indicate consistent improvements under high correspondence ambiguity," but no analysis of correspondence ambiguity or any ablation organized by ambiguity level appears in the main paper body.

- **Batch sizes differ across models.** PaSST uses batch size 64, EAT uses 24, and BEATs uses 16 (line 184). Since contrastive loss depends on batch size, cross-model comparisons are less clean.

### Trivial

None.

## Nice-to-Haves

- Reporting results with multiple random seeds (3–5) would establish whether the small differences for the novel components are significant.
- Adding a comparison to prior published SOTA on CLOTHO would contextualize the results.
- Qualitative examples of augmented captions and cluster assignments would ground the methods.

## Removed Points

The following points from the input review were removed with justification:

- **"The paper's structure and depth are thin for ICLR" / general thinness criticism.** The appendix is stripped by the parser, so missing content (ablations, analysis, examples) may exist in the original submission. Removed per rule about missing appendix content.
- **Criticism that "no analysis is provided for why different backbones respond differently."** This is partly covered in Minor weaknesses (#2, no qualitative analysis) but the broader framing as a "thin paper" was removed as overlapping with appendix-stripping concerns.
- **"AudioCaps test split usage is unusual."** This is a methodological note but does not undermine results since CLOTHO is a separate dataset. Retained only as implicit context in the batch-size note.
- **"Choice of mAP@16 not motivated."** While the paper mentions mAP@16, it also reports mAP@10 and R@k. The choice of primary metric is inherited from DCASE evaluation norms and is a presentation preference, not a technical flaw.

## Novel Insights

None beyond the paper's own contributions. The core finding — that soft-label distillation from pretrained retrieval teachers yields substantial gains (+4.5–5.8 mAP@16) while the additive contributions of LLM augmentation and cluster-guided classification are marginal to negative on top of distillation — is valuable but is not presented as a finding in the paper; it emerges from reading against the paper's own framing.

## Suggestions

The paper would be substantially stronger if it were reframed to honestly present the results: (1) acknowledge that the distillation component drives all gains and is adopted from prior work; (2) treat the LLM augmentation and clustering as attempted extensions that require further investigation to produce reliable improvements; and (3) add external comparisons to prior published results on CLOTHO. If the paper wants to keep all three techniques as contributions, multiple-seed experiments demonstrating statistically significant additive gains are essential.

## Score and Decision

**Final Score: 3.5**

**Calibration process:**

**Round 1 bracket (3.0 – 4.5):** I compared my draft's weighted item scores against anchors from the calibration corpus. The strongest negative weights in my draft are "no external comparison to prior work" (−3.34) and "novel contributions do not improve over distillation baseline" (−2.55). These are similar in severity to the "limited novelty" (−3.70, −5.21) and "results underwhelming" (−4.81) weights in the "Don't Pre-train, Teach" paper (avg 3.00, Reject), but my draft also has substantially higher positive weights for its strengths (9.52–9.70) than that anchor's best positive weights (8.65–9.15). The "Multi-label Cluster Discrimination" anchor (5.00, Reject) had more thorough experiments but similar novelty concerns; the "Leveraging LLM Embeddings for Music Emotion" anchor (4.00, Reject) had similar missing-detail issues and weak baselines.

**Round 2 narrowing (3.0 → 3.5):** Compared against the "Don't Pre-train" (3.00) and "AVCaps" (4.00) anchors itemized in round 2. Our paper matches the "Don't Pre-train" paper in the severity of the novelty-evidence mismatch (both have a key technique adopted from prior work that drives results, with limited additive value from claimed novel components). However, our paper's motivation is sharper, the engineering contributions (50k augmented pairs, reproducible pipeline) are more concrete, and the distillation results are clearly positive even if adopted. These factors push it slightly above 3.00. But the paper falls below 4.00 because the core claim about "joint improvement" is contradicted by the paper's own Table 2, unlike the AVCaps paper whose contribution (a dataset) at least delivers what it promises. The absence of external SOTA comparisons and variance reporting further limits the paper's evidentiary strength.

**Final calibration:** The paper's weighted items place it between the 3.00 "Don't Pre-train" anchor (which shares similar novelty-evidence mismatch) and the 4.00 "AVCaps" anchor (which at least delivers on its primary contribution). Score 3.5 — borderline reject.

**All anchors consulted:**
- `gwZ90hFSL2.md` (1.00, R1) — not topically relevant
- `5lUdTogEL3.md` (1.00, R1) — not topically relevant
- `P49gSPmrvN.md` (1.00, R1) — not topically relevant
- `nh5tSrqTpe.md` (3.00, R1, itemized) — distillation paper with similar novelty-evidence gap
- `Wv9Gl1bFbc.md` (3.00, R1) — self-distillation for SLMs, moderate relevance
- `rwdeKOdAwY.md` (3.00, R1) — multimodal retrieval with limited novelty
- `qqExiDNsa7.md` (5.00, R1, itemized) — speech separation pre-training study, moderate relevance
- `Gi3SwL98nL.md` (4.00, R1, itemized) — LLM+clustering for music emotion, similar missing-detail issues
- `OPpqmSp0wK.md` (5.00, R1, itemized) — cluster discrimination, more thorough experiments
- `U42TkrEDzb.md` (6.75, R1) — audio LLM, not directly relevant
- `Tn6lrFbiP4.md` (6.33, R1, itemized) — text-video retrieval with LLM augmentation, stronger paper overall
- `14rn7HpKVk.md` (6.67, R1) — SALMONN audio LLM, not directly relevant
- `3i13Gev2hV.md` (8.00, R1) — hyperbolic VLMs, not directly relevant
- `9Cu8MRmhq2.md` (8.00, R1) — video correspondence learning, moderate relevance
- `uAFHCZRmXk.md` (8.00, R1) — modality gap analysis, moderate relevance
- `UhcXE3o1R3.md` (4.33, R2) — Apollo multi-modal reasoning, moderate relevance
- `ufi0WPTgWp.md` (4.25, R2) — video captioning, moderate relevance
- `FFUmPQM8c5.md` (4.00, R2, itemized) — AVCaps dataset, similar weak-experiment issues
- `hgayrNSbri.md` (3.40, R2, itemized) — lightweight captioning, similar limited-novelty issues
- `a8dQutiF9E.md` (3.40, R2) — audio editing, not relevant
- `nhgTmx1TZJ.md` (3.00, R2) — UniAudio, not directly relevant
- `cLws58ZojF.md` (3.00, R2) — speech-conditioned LLMs, not relevant

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>