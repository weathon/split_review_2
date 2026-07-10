Here is my final consolidated review.

---

## Summary

This paper proposes DGNet, a self-supervised multi-band EEG representation learning framework for dementia classification. The architecture decomposes EEG signals into five standard frequency bands (delta through gamma), processes each band through independent CNN encoders, and uses an adaptive NT-Xent contrastive loss with per-band projection heads. The model is pre-trained on unlabeled EEG data and then evaluated via LOSO cross-validation on AD vs. CN classification using 65 subjects (36 AD, 29 CN). The paper reports 92.90% accuracy and 96.77% AUC, claiming significant improvements over baselines.

## Strengths

- **Neurophysiologically motivated architecture.** Processing each EEG frequency band (delta through gamma) through independent encoders is well-motivated by known spectral slowing biomarkers in dementia (increased delta/theta power, decreased alpha/beta/gamma power in AD). The paper correctly identifies and links these clinical findings to its architectural design.

- **Clean two-stage SSL pipeline.** The architecture (frequency band decomposition → independent CNN encoders → per-band projection heads → adaptive NT-Xent loss) is a coherent adaptation of SimCLR to multi-channel EEG, and the unlabeled pre-training → linear evaluation pipeline is appropriate for the low-label regime the paper targets.

## Weaknesses

### Major

- **Ambiguous pre-training data split raises data leakage concerns.** The paper describes a single pre-training stage (Section 3, line 124) without specifying any data split. Leave-One-Subject-Out (LOSO) cross-validation is described only for the linear evaluation stage (Section 3.4). The dataset contains exactly 88 subjects (Section 3.1), and there is no mention of per-fold pre-training (i.e., pre-training on 87 subjects' unlabeled data and holding out the test subject for each LOSO fold). If pre-training consumed all 88 subjects' data — including the eventual test subject — this constitutes label leakage that would inflate the reported 92.90% accuracy. The paper's silence on this critical methodological detail undermines confidence in all reported results.

- **Numerical inconsistency between abstract claims and ablation results.** The abstract reports "a 31.5% relative performance improvement over training from scratch, and a 25.4% improvement over the single-head approach." From Table 3: training from scratch = 63.35%, single-head = 73.52%, full model = 92.90%. No reasonable computation yields both stated numbers: (92.90−63.35)/63.35 = 46.6%; (92.90−63.35)/92.90 = 31.8% (close but not 31.5%); (92.90−73.52)/73.52 = 26.4%; (92.90−73.52)/92.90 = 20.9%. The paper does not define how "relative improvement" is computed, and the stated numbers cannot be reproduced from Table 3.

- **23 FTD subjects are unaccounted for.** The dataset (Section 3.1) contains three groups: AD (36), FTD (23), and CN (29). All experiments report only AD vs. CN classification. The paper never explains what was done with the 23 FTD subjects — whether they were excluded entirely, included only in pre-training, or used in some other way. This is a significant omission in experimental reporting that affects both data utilization and the composition of pre-training data.

### Minor

- **Several baselines in Table 1 perform implausibly poorly.** EEGInception (39%), TIDNet (44%), EEGNet (46%), and Deep4Net (49%) score at or below chance on a binary AD vs. CN task (majority-class baseline = 55.4%). While the proposed method may genuinely outperform these approaches, results this far below chance strongly suggest suboptimal tuning, mismatched evaluation protocols, or implementation issues. Without per-baseline evaluation details or code, these comparisons cannot be reliably interpreted.

- **Inconsistent definition of "linear evaluation."** Section 2 (line 80) states that linear evaluation involves updating "all parameters of the model including those of the encoder" — which describes fine-tuning, not linear evaluation. However, the experimental setup (Section 3, line 124) and Figure 1 caption both state that "the pre-trained encoder is frozen" during linear evaluation, which is the standard SSL definition. The paper contradicts itself on a basic experimental term.

- **Equation (1) departs from standard NT-Xent without justification.** The loss function uses a max-over-negatives formulation ($\max_{n=1,\dots,N} \text{sim}$) instead of the standard sum-over-negatives used in SimCLR's NT-Xent loss (Eq. 2). This is a substantive architectural choice that is never motivated or discussed in the paper.

- **No standard deviations reported despite LOSO producing per-fold metrics.** LOSO evaluation naturally yields 88 per-fold metrics, but no variance measures are reported for the proposed method in Tables 1 or 2 (one baseline in Table 2 reports "91.25 ± 0.38" while Ours reports only a point estimate).

### Trivial

- **Slightly inconsistent architecture language.** The text alternates between "the encoder consists of three convolutional blocks" (singular) and "five parallel 1D encoders" (Figure 2 caption), though the intended design (independent encoders per band) is eventually clear from the detailed description.

## Nice-to-Haves

- Pre-train the encoder separately for each LOSO fold, using only the 87 training subjects' unlabeled data, to properly evaluate subject-independent generalization.
- Report mean and standard deviation (or per-fold distributions) for all LOSO metrics.
- Explain the role of the 23 FTD subjects in the experimental pipeline.
- Provide justification for the max-over-negatives formulation in Eq. (1).
- Release code to support reproducibility and baseline verification.

## Removed Points

- **Data leakage described as a "fatal structural flaw":** Demoted from fatal to major. The paper is ambiguous about whether pre-training is done per fold or on all subjects — it does not explicitly state "all 88 subjects were used in pre-training." A rebuttal could clarify this. The concern is significant but is based on an ambiguity in the paper rather than an unambiguous statement, so it does not meet the threshold for a fatal claim.
- **"Unprecedented gap over baselines" as evidence of leakage:** Removed. Weak baselines could explain the gap regardless of leakage; this reasoning is circular.
- **SOTA claim is "circular":** Trivial framing issue; removed.
- **Abstract framing (dementia crisis paragraphs) is excessive:** Removed — scope creep, not a substantive technical weakness.
- **"No code release" criticism:** Moved to nice-to-have. Code is not required for ICLR.
- **"No discussion of limitations":** Moved to nice-to-have.
- **"Wang et al. 2024 not in visible reference section":** Removed — references are truncated by the parser; the paper likely includes this citation in the stripped appendix.
- **Specific criticism about spectrogram visualization quality:** Removed as subjective.

## Novel Insights

None beyond the paper's own contributions. The review surfaces a significant methodological ambiguity (pre-training data split), a concrete numerical error in the abstract, and an unexplained subset of the dataset (FTD subjects), but these are corrective observations rather than novel insights about the work.

## Suggestions

1. Clarify the pre-training data split. If pre-training was performed per LOSO fold, state this explicitly and describe the procedure. If it was performed on all 88 subjects, the evaluation must be redesigned with per-fold pre-training.
2. Correct the abstract's numerical claims to match Table 3, or explicitly define how "relative improvement" is computed.
3. Report mean and standard deviation across LOSO folds.
4. Explain how the 23 FTD subjects were used.
5. Justify the max-over-negatives formulation in Eq. (1) or replace it with the standard sum over negatives.
6. Re-evaluate baselines with proper tuning and identical evaluation protocols.

## Calibration

**Round 1 bracket: 2.0–4.0.** All retrieved topically similar papers fell in this range: UniEEG (2.00, avg scores 1/3/3/1), FSL-MIC (2.20, 1/3/1/3/3), Invariant Spatiotemporal (3.00, 5/1/3/3), HyperEEGNet (3.00, 1/5/3/3), EEG-DisGCMAE (5.00, 6/5/3/8/3/5), EEGPT (4.00, 5/3/3/5). Papers scoring above 5.0 (Cognition-Supervised at 4.50, Decoding Natural Images at 6.75) had substantially stronger contributions (novel paradigms, large-scale evaluation, or dataset releases).

**Round 2 narrowing: 2.0–3.0.** Comparing itemized impact scores: UniEEG (2.00) had pervasive writing and methodological issues with impact up to −10.00 and weak strengths. FSL-MIC (2.20) had lack-of-novelty and evaluation issues with −10.00 impact. Both match this paper's pattern of weak strengths (max +2.95) and strong negative signals (−10.00 for data leakage ambiguity, −10.00 for numerical inconsistency). Papers in the 3.0–5.0 range (Invariant Spatiotemporal, EEGPT) had larger-scale evaluations or stronger strengths despite their own flaws.

**Final placement: 2.5.** This paper is above UniEEG (2.00) because its core neurophysiological motivation is sounder. It is below Invariant Spatiotemporal (3.00) because that paper had at least a clean evaluation pipeline, while this one has both a concrete numerical error in its headline claim and an ambiguous pre-training setup that could invalidate all reported numbers. The gap between the stated and computable relative improvements is a verifiable error, and the data split ambiguity is a serious methodological concern that the paper does not address.

## Score and Decision

MY FINAL SCORE: <score>2.5</score>
MY FINAL DECISION: <decision>Reject</decision>