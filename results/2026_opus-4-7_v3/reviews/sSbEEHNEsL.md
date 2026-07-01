Now let me verify a few more specific claims by re-reading key sections:Now I have a thorough understanding of the paper. Let me draft the review.Now let me run calibration Round 1 — bracketing:Let me read a few of the most relevant anchors for calibration:Now I have sufficient calibration information. Let me form my initial bracket.

**Round 1 Bracket:**
- Strong reject (1.0): Fundamentally broken papers — not applicable to USR 2.0.
- Reject (3.0): Limited novelty, major methodological issues — not applicable.
- Borderline reject (3.5–5.5): Cross-lingual pseudo-labeling (5.25) has limited novelty and narrow scope — USR 2.0 is clearly stronger.
- Borderline accept to accept (5.5–7.5): CR-CTC (6.75) and AWP (7.00) are most relevant comparisons — both are CTC-related improvements in ASR with clean ideas and good evaluations. USR 2.0 has comparable or stronger contributions with larger OOD improvements and practical speedup.
- Strong accept (8.0+): These are outstanding papers — USR 2.0 is strong but incremental over USR.

**Initial bracket: 6.5 – 7.5**

Now let me write the final consolidated review:

---

## Summary
USR 2.0 proposes CTC-driven teacher forcing for pseudo-labelling in unified speech recognition (ASR/VSR/AVSR), replacing slow autoregressive decoding with parallel generation of attention-based pseudo-labels conditioned on collapsed CTC outputs. Combined with a mixed sampling strategy to mitigate exposure bias, the method halves training time, substantially improves out-of-distribution robustness across long utterances, noise, and unseen datasets, and achieves state-of-the-art in-distribution results on LRS3, LRS2, and WildVSR using a single unified model.

## Strengths

- **Clean, non-obvious core idea with rigorous motivation.** CTC-driven teacher forcing—feeding collapsed CTC greedy outputs into the decoder to generate attention pseudo-labels in a single forward pass—simultaneously addresses two distinct USR limitations (speed and robustness). The key insight that global coherence of teacher-forced attention PLs is unnecessary in a pseudo-labelling setting, because teacher and student share the same CTC prefix conditioning (Section 4.1, "Global coherence"), is genuinely non-trivial. The paper explains this clearly with precise equations (Eq. 3–4).

- **Thorough and convincing OOD robustness evaluation.** Section 5 evaluates along three distinct axes of distribution shift: input length (Figure 3, VoxCeleb2), noise (Table 1, babble noise at 10dB to −5dB), and unseen datasets (Table 3, LibriSpeech/WildVSR/AVSpeech). Improvements are large and consistent—e.g., 25.3%→15.4% on LibriSpeech, and stable WER beyond 155 frames where USR degrades catastrophically. The beam-size analysis (Figure 3c) adds practical insight by showing USR 2.0's robustness is intrinsic, not recoverable by expensive inference.

- **Well-designed ablations that cleanly validate the mechanism.** Table 4 isolates contributions of each PL type per branch: removing CTC supervision from the decoder in CTC-driven mode causes 24.2%→35.1% OOD degradation with minimal ID change (3.2%→3.3%), directly validating the coupled-supervision hypothesis. Figure 4 reveals an interpretable trade-off curve between ID accuracy, OOD robustness, and training cost.

- **Substantial practical training speedup (~2×).** Per Figure 5, the speedup comes from both faster per-step computation (removing AR decoding) and faster convergence (50 vs. 75 epochs), making semi-supervised training at scale significantly more practical (demonstrated with the Huge model).

## Weaknesses

### Fatal
None.

### Major
- **Huge model results lack a USR baseline at the same scale.** The Huge model (Table 2, bottom row) achieves impressive WERs (17.6%/0.9%/0.8%) but uses different training data (LRS2+LRS3 labelled, VoxCeleb2+AVSpeech unlabelled) with no USR comparison at this scale. Without this comparison, it is impossible to disentangle gains from the USR 2.0 method versus additional data and model capacity. This leaves the scaling claim only partially supported.

### Minor
- **Whisper-generated ground truth for some OOD evaluations.** VoxCeleb2 (Section 5.1) and AVSpeech (Section 5.3) evaluations use Whisper transcriptions as ground truth. The paper acknowledges Whisper as an "oracle" but does not discuss its own error rate on these challenging conditions—particularly for long utterances and noisy audio, which are the exact settings being tested. This is a bounded concern: LibriSpeech and LRS3 evaluations use human transcriptions and are unaffected, and the directional findings are large enough to be robust, but absolute WER numbers on Whisper-transcribed sets should be interpreted cautiously.

- **Loss weighting between PL types (0.5) in Equations 5 and 6 is not ablated.** While the mixed sampling probability between CTC-driven and AR modes is thoroughly ablated in Figure 4, the fixed 0.5 weighting between CTC and attention PL targets within each loss term is a separate design choice that is not justified or varied.

- **Coherence argument is supported only indirectly.** The theoretical linchpin—that globally incoherent CTC-driven attention PLs enable effective knowledge transfer because of matched conditioning (Section 4.1)—is argued conceptually and validated by end-task performance. Direct empirical analysis (e.g., token-level agreement rates between CTC-driven and AR attention PLs, or characterizing the nature of the "incoherence") would transform this from a plausible argument to a grounded one. The paper references Appendix C.4 for further discussion.

### Trivial
None.

## Nice-to-Haves
- Variance estimates from 2–3 runs on the Base/LRS3 configuration would confirm that small in-distribution gains (e.g., 3.0% vs. 3.2% in Table 2) are reliable. Single-run evaluation is standard in this field, so this is not a weakness, but the smallest ID improvements are on the order of noise margins.
- The AR-mode-optimal probability for ID performance appears to be ~0.6–0.8 (Figure 4 data points: 2.8% at both 0.6 and 0.8), while the default is 0.5. More explicit discussion of the Pareto trade-off and guidance on tuning would be helpful.
- Discussion of failure cases: when does CTC-driven teacher forcing produce worse pseudo-labels than AR decoding, and how does the mixed sampling strategy handle these?

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"No variance estimates across all results" as a weakness** — Downgraded to nice-to-have. Single-run evaluation is standard practice for large-scale speech recognition training. The OOD improvements are large enough (e.g., 25.3%→15.4%) to be unambiguous; the in-distribution gains, while sometimes small, are consistently directional across multiple model sizes and data settings. Demanding multi-seed runs is not standard in this community.

- **Criticism about absence of Appendix C.4 discussion** — Removed per rule on stripped appendices. The appendix exists in the original submission and may contain the detailed coherence analysis the reviewer seeks.

- **"Training time halved" claim lacks qualification** — Removed. The reviewer flagged the abstract's "halves training time" as unqualified, but Figure 5 demonstrates ~2× speedup across three different settings (Base/LRS3, Base/LRS3+Vox2, Large/LRS3+Vox2), and the paper says "nearly 2× faster training," which is a reasonable summary.

## Novel Insights
The paper's central insight—that global coherence of pseudo-labels is unnecessary when teacher and student share the same conditioning prefix—is a genuinely useful observation for the broader self-training community. This decouples generation-time sequence coherence from training-time knowledge-transfer effectiveness, an observation that extends beyond speech to any sequence-to-sequence self-training setting with a non-autoregressive alignment module. The complementary finding that CTC and attention pseudo-labels can be jointly predicted in a single decoder pass to couple two otherwise-independent branches is a practical contribution to hybrid CTC-attention architectures.

## Suggestions
- Train USR at Huge scale for direct comparison, even if only on one modality, to validate that USR 2.0's gains persist at scale.
- Provide direct analysis of CTC-driven attention PLs: token-level agreement with AR-generated PLs, how disagreement correlates with input difficulty (length, noise, modality), and concrete examples of globally incoherent but locally useful PLs.
- Ablate the 0.5 loss weighting between PL types in Equations 5 and 6 separately from the mixed sampling probability.

## Score and Decision

### Calibration Anchors

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| gwZ90hFSL2 (Humanoid Robots Chinese NLP) | 1.00 | 1 | Fundamentally flawed; not comparable. |
| 8QTpYC4smR (LLM Survey) | 1.00 | 1 | Pure survey, no contribution; not comparable. |
| Uj0h13lVrR (KL Divergence GFlowNets) | 1.00 | 1 | Flawed methodology; not comparable. |
| 5lUdTogEL3 (Lifelong Person ReID) | 1.00 | 1 | Fundamental issues; not comparable. |
| UFwefiypla (DM-Codec) | 3.00 | 1 | Speech tokenization; limited novelty; USR 2.0 is substantially stronger. |
| xRi8sKo4XI (Unsupervised Prompt Learning) | 3.00 | 1 | Semi-supervised classification; weak evaluation; USR 2.0 is much stronger. |
| aXSxSu3fvg (Semi-supervised Early Stopping) | 3.00 | 1 | Limited contribution; USR 2.0 is far stronger. |
| gW4bdLwypB (Objective Soups ASR) | 3.40 | 1 | Multilingual ASR with conflicts; USR 2.0 has cleaner contribution and stronger results. |
| 4lOWCkhr4g (Cross-Lingual Pseudo-Labeling) | 5.25 | 1 | Pseudo-labeling for ASR but limited novelty; USR 2.0 has a cleaner insight and stronger evaluation. |
| eSO9quCgmz (Rethinking Pseudo-labeling) | 5.00 | 1 | General pseudo-labeling framework; rejected for limited novelty; USR 2.0 is stronger. |
| 7NlGsjrEd8 (CTC Alignment Methods) | 4.50 | 1 | CTC alignment modeling; narrow scope; USR 2.0 has broader impact. |
| MazxSMs6Hs (African-Accented ASR) | 3.67 | 1 | Active learning for ASR; limited methodology; USR 2.0 is substantially stronger. |
| CIs9x2ZRgh (CR-CTC) | 6.75 | 1 | Most relevant anchor: CTC improvement for ASR with consistency regularization. Simple method, good results but smaller improvements. USR 2.0 has a cleaner insight, larger practical impact (2× speedup + OOD robustness), and more thorough evaluation. USR 2.0 is comparable or slightly stronger. |
| fUGhVYPVRM (Align With Purpose CTC) | 7.00 | 1 | CTC framework with plug-and-play alignment optimization. General but with modest improvements. USR 2.0 has larger practical gains and more convincing evaluation. Comparable. |
| 4N97bz1sP6 (Bi-modal Audio Separation) | 6.67 | 1 | Different domain (audio separation); accepted with moderate scores. |
| FyMjfDQ9RO (Sylber) | 6.75 | 1 | Speech representation with syllabic structure; accepted. USR 2.0 has comparable contribution quality. |
| PdaPky8MUn (Never Train from Scratch) | 8.00 | 1 | Strong methodological contribution with broad impact; USR 2.0 is more specialized but with strong practical value. |
| tyEyYT267x (SAR Diffusion LMs) | 8.00 | 1 | Novel interpolation between AR and diffusion; broader methodological contribution. USR 2.0 is more application-focused with comparable execution quality. |

**Round 1 bracket:** 6.5–7.5

**Narrowing:** USR 2.0 is at least as strong as CR-CTC (6.75) and AWP (7.00): it has a cleaner core insight, larger practical improvements (2× training speedup, substantial OOD gains), and more thorough multi-axis evaluation. Its main weakness (no Huge-scale USR baseline) is a bounded gap, not a fundamental flaw. The paper does not quite reach the 8.0 tier (which requires broader methodological novelty or exceptional rigor), but it is a clear accept-quality paper with strong practical significance.

**Final score: 7.0**

This paper presents a clean, well-motivated method that addresses real limitations of USR with substantial empirical backing. The OOD improvements are large and convincing, the training speedup is practically significant, and the ablations are well-designed. The main gap (missing Huge-scale baseline) is notable but does not undermine the core contribution. The paper merits acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>