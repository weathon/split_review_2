## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT) for multimodal learning, addressing "modality imbalance" where dominant modalities bias the classifier and suppress weaker ones. The key innovation is a two-stage framework: (1) pretrain a shared classifier with contribution-aware regularization, then (2) freeze it during alternating training while modality-specific LoRA modules enable adaptation. The paper reports consistent improvements over SOTA on CREMA-D (+2.27%), Kinetic-Sound (+6.76%), and MVSA (+1.92%). The core idea — that encoder-level fixes (alternating training) leave classifier bias untouched — is a genuine and well-motivated insight.

## Strengths

- **Novel and well-motivated core idea.** The observation that alternating training (MLA) solves encoder interference but leaves classifier bias unaddressed is a genuine gap, supported by Figure 1 showing persistent contribution disparity (0.90/0.10 at epoch 100). Freezing a pretrained classifier while allowing modality-specific LoRA adaptation is internally consistent with the diagnosed problem. [weight=10.05]

- **Consistent positive results across three diverse benchmarks.** CCAT outperforms all baselines on CREMA-D (85.89 vs. LFM 83.62), Kinetic-Sound (79.29 vs. LFM 72.53), and MVSA (80.73 vs. MMPareto 78.81) in Table 1, spanning audio-visual and text-image modality pairs. [weight=10.45]

- **Systematic ablation study.** Table 2 removes each of the four components (classifier freezing, alternating training, secondary updates, LoRA) individually, allowing readers to trace the source of gains. [weight=9.66]

## Weaknesses

### Major

- **Overclaimed theoretical contributions.** The paper claims to "establish a unified theoretical framework and provide a proof" (Sec. 3.1) of a "profound theoretical isomorphism" between class and modality imbalance. What is actually presented is a heuristic gradient analogy (Eqs. 2–3) showing that both settings produce gradient dynamics dominated by a single term. There are no theorems, bounds, or formal statements. This is listed as contribution (i), and the rhetoric substantially overstates what is a useful but modest insight. The method design remains plausible without this framing, but the mismatch between claims and substance undermines credibility. [weight=-0.88]

- **No statistical significance reporting.** Results are reported as average accuracy over 3 random seeds with no standard deviations, confidence intervals, or any variance measure (Table 1). Key comparisons — e.g., the LoRA contribution is only 0.38% on MVSA (80.73 vs. 80.35, Table 2) — cannot be assessed for statistical significance. For a method paper whose central claim is SOTA improvement, this is a significant evidential gap. [weight=1.04]

### Minor

- **Unexplained large gain on Kinetic-Sound.** The +6.76% gain on KS is ~3x larger than gains on other datasets. CCAT's audio-only accuracy (61.65%) is +5.25% above the best baseline (56.40%), yet video-only accuracy (53.75%) is below LFM (55.62%) — so the entire multimodal gain comes from the audio branch. The paper does not discuss this disparity or explore what properties of KS drive this result. [weight=3.30]

- **Missing comparison with closely related baselines.** Reconboost (Hua et al., 2024) and SMLV (Zhou et al., 2025b) are discussed in Related Work as directly relevant alternating training and sample-level valuation methods, but neither appears in Table 1. Including them would clarify whether CCAT's gains come from the frozen-classifier insight specifically or from having more parameters / a more elaborate procedure. [weight=4.05]

- **Inconsistency in Figure 1.** The caption states MLA "reduces initial contribution disparity (1.00 → 0.92)" but the table shows MLA Modality A at 0.90 and B at 0.10 at epoch 100. The value 0.92 does not match any reported entry. [weight=3.72]

- **β sensitivity shows non-monotonic behavior.** On CREMA-D, accuracy goes 85.89 (β=0.15) → 84.14 (β=0.20) → 84.54 (β=0.25) — a zigzag pattern not discussed, which may indicate high variance or complex interactions. [weight=5.39]

- **Suspicious identical values in Table 1.** OGM-GE and QMF both report Video=32.19 on Kinetic-Sound, an unexplained identical value. [weight=2.86]

- **LFM missing on MVSA.** LFM has "—" entries for MVSA in Table 1 without justification. [weight=3.36]

### Trivial

None.

## Nice-to-Haves

- An analysis of what the LoRA modules actually learn (e.g., do they shift unimodal feature distributions toward what the frozen classifier expects?) would strengthen the method section.
- Reporting individual per-seed results would help readers assess variance even without formal statistical tests.
- The β sensitivity zigzag on CREMA-D warrants a brief discussion.

## Removed Points

- Criticism that the gradient analogy is "fundamentally imprecise" because class imbalance is about sample frequency while modality imbalance is about feature dominance: The paper explicitly compares the *resulting gradient dynamics* (the recursive cycle of early dominance → entrenched bias), which is structurally similar. The analogy is about the dynamics, not the causes, which the paper's framing acknowledges.
- Speculation about confounds on the KS result (hyperparameter tuning, dataset size): Speculative — the paper discloses tuning grids and there is no evidence baselines were disadvantaged.
- Concern about the MI estimator "cheating" (same data for regularization and MI estimation): Speculative without evidence.
- Demand for analysis of what LoRA learns: Nice-to-have, not a core weakness.
- Criticism of MLA's high video-only performance on CREMA-D as "not discussed": This is an observation about a baseline's behavior, not a weakness in the paper's own method.
- Multiple presentation-level observations from the "Section-by-Section Notes" that amount to formatting or minor notational preferences.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add standard deviations** (or per-seed results) to all tables. This single change would transform the evaluation from suggestive to convincing.
2. **Recalibrate the theoretical claims** in Sec. 3.1: replace "unified theoretical framework" and "proof" with an accurate characterization (e.g., "motivating gradient analogy").
3. **Include Reconboost and SMLV** in the experimental comparison, or justify their exclusion.
4. **Add a brief analysis** discussing the KS result — per-class breakdowns or feature analysis to explain why audio benefits disproportionately.
5. **Clarify the 0.92 value** in Figure 1, the "—" entries for LFM on MVSA, and the identical Video=32.19 for OGM-GE/QMF on KS.

## Score and Decision

### Calibration Report

**Round 1 — Bracketing.** I queried the calibration corpus with "multimodal learning modality imbalance alternating training" across all score bands. Relevant anchors retrieved:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `ul1cjLB98Y.md` (Theory of Unimodal Bias) | 5.25 | R1 | Yes | Directly comparable: analyzes the same modality imbalance phenomenon. That paper has formal theoretical analysis but only toy simulations; this paper has real empirical results but overclaims its theory. |
| `5BXWhVbHAK.md` (Can One Modality Synergize) | 6.33 | R1 | Yes | Both propose novel multimodal methods with theoretical framing and empirical validation. The anchor paper has stronger theoretical backing (actual proofs) and more modality pairs tested. |
| `uAFHCZRmXk.md` (Two Effects, One Trigger) | 8.00 | R1 | Yes | Analysis paper — stronger writing, more thorough experiments, no significant weaknesses. Well above this paper's quality. |
| `TPZRq4FALB.md` (Test-time Adaptation, Reliability Bias) | 8.00 | R1 | Yes | Strong method paper with clear problem framing, benchmarks, and comprehensive evaluation. Significantly stronger than this paper. |
| `XTwwtlEfTF.md` (Robust Multimodal Learning, Missing Modalities) | 4.50 | R2 | Yes | Also uses parameter-efficient adaptation. Weaker strengths and more severely negative-weighted weaknesses than this paper. |
| `0yTf37PXcH.md` (Improving MLLM, MM-LoRA) | 5.40 | R2 | Yes | Also uses modality-specific LoRA. Similar tier — has negative-weight weaknesses (-3.24, -0.61) that this paper lacks, but more experiments. |
| `CagdoUkvvl.md` (Relaxing Representation Alignment) | 4.50 | R2 | Yes | Multi-modal continual learning. Has more severe negative-weight criticisms (-4.68, -4.74). This paper is stronger. |

**Round 1 bracket**: Between 4.5 and 6.5.

**Round 2 — Narrowing.** I itemized the most relevant anchors. Comparing weighted items:

- My paper's most damaging weakness (theory overclaim, weight=-0.88) is far less severe than the most damaging items in the 4.50–5.40 anchors (e.g., -2.66, -4.53, -3.24, -4.68). This pushes my paper above these anchors.
- However, my paper lacks the theoretical rigor of the 6.33 anchor (actual proofs with non-negative-weight weaknesses) and has more accumulated minor issues.
- The 6.33 anchor was accepted (6, 8, 5); my paper has a similar strength profile but weaker theory and missing std devs.

**Final placement**: 5.5 — above the 5.25 "Theory of Unimodal Bias" anchor (which had -4.53 weight items and only toy experiments) but below the 6.33 anchor (which had actual proofs and broader validation). The paper has a genuine method contribution but the theoretical overclaim and missing variance reporting prevent confident acceptance.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>