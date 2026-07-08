## Summary

This paper proposes DGNet, a self-supervised learning architecture for EEG-based dementia classification. The key idea is to decompose EEG signals into five frequency bands (delta through gamma), process each band with an independent CNN encoder and projection head in a multi-head SimCLR framework, then evaluate on binary AD vs. CN classification. The paper reports 92.90% accuracy, a claimed 31.5% relative improvement over training from scratch.

## Strengths

- **The multi-band design is neurophysiologically grounded.** The paper correctly identifies that dementia is associated with spectral slowing (increased delta/theta power, decreased alpha/beta/gamma power) and decouples bands for representation learning. This is a sensible inductive bias for EEG-based dementia classification.

- **The ablation study (Table 3) is comprehensive for this class of paper.** It separately evaluates SSL pretraining vs. training from scratch, multi-head vs. single-head, data augmentation, adaptive temperature, and regularization. Each component's contribution is documented, giving insight into which design decisions matter.

- **LOSO (Leave-One-Subject-Out) cross-validation** is the correct evaluation protocol for EEG subject-level generalization and is properly used.

- **The multi-band approach adds measurable value beyond a monolithic encoder.** The ablation shows multi-head (5 heads) at 79.55% vs. single-head at 73.52%, confirming that frequency-band-specific processing contributes positively even before adding adaptive temperature and regularization.

## Weaknesses

### Major

**1. Baseline evaluation is not credible.** In Table 1, several well-established EEG models score at or below chance on a binary AD/CN task: EEGInception 39%, TIDNet 44%, EEGNet 46%, FBCNet 48%, Deep4Net 49%, S-JEPA 50%. On a dataset where prior published work (Table 2) achieves 60–91%, the fact that 6 of 12 baselines are at or near chance strongly suggests improper adaptation, training, or hyperparameter tuning rather than genuine task difficulty. The paper's central claim of 92.90% state-of-the-art performance rests on a comparison where the baselines may not have been fairly trained or tuned for this dataset. The paper mentions "for the SSL models, fine-tuning was performed when pretrained weights were available," which implies some models used off-the-shelf weights from different EEG tasks — but does not describe any comparable training-from-scratch protocol for the supervised baselines.

**2. Loss function is presented inconsistently.** Equation 1 describes an additive objective combining (negated) positive similarity with the single hardest negative similarity plus separate regularization terms — this is structurally different from the standard NT-Xent loss (Equation 2) that uses a softmax over all negatives. The paper refers to both as NT-Xent without explaining the relationship between the two formulations or stating which was actually implemented. The reader cannot determine whether Equation 1 is the true loss (in which case calling it NT-Xent is incorrect) or Equation 2 is the true loss (in which case Equation 1 and its apparatus of learnable positive/negative temperatures is a decoy). This ambiguity affects the paper's core technical contribution.

**3. FTD subjects are unaccounted for.** The dataset contains three groups — AD (36), FTD (23), and CN (29) — but every experiment reports only binary AD vs. CN classification. The 23 FTD subjects (26% of the data) are never mentioned again after the dataset description, with no explanation for their exclusion. This raises concerns about selective reporting and leaves the method's ability to distinguish dementia subtypes or perform multi-class classification completely unexamined.

### Minor

- **The term "linear evaluation" is misused.** Section 2.1 describes fine-tuning all parameters as "linear evaluation," whereas in the SSL literature this term standardly means training only a classifier on frozen features. The actual protocol in Section 3 correctly freezes the encoder, so this is a presentation error rather than a methodological flaw.

- **The ablation table (Table 3) does not clearly specify what differs between the "Multi-head (5 heads)" row (79.55%) and the "constant temperature (τ=0.1)" row (86.53%).** The text explains the constant-temperature variant but leaves the configuration of the "Multi-head (5 heads)" row ambiguous.

- **It is not explicitly stated whether SSL pretraining uses the same 88 subjects' data or a separate unlabeled corpus.** If pretraining uses the same small cohort, the benefit of SSL over training from scratch warrants more discussion given the limited data size.

### Trivial

- Several baselines in Table 2 do not report precision or recall values (indicated by dashes), making some comparisons less complete.

## Nice-to-Haves

- A comparison with conventional bandpass filtering (e.g., FIR filters) would help justify the learned depthwise-convolution frequency extractor.
- Variance reporting (standard deviation or confidence intervals) for all main results would strengthen reproducibility.

## Removed Points

- "Introduction is overwritten": Style preference, not a substantive weakness.
- "Reference to Wang et al. 2024 raises novelty questions": The paper properly cites AMCL as the source of the adaptive temperature strategy.
- "Pure formatting/style nitpicks": Parser artifacts, not author errors.
- "Should compare to conventional bandpass filtering": Nice-to-have beyond stated scope.
- "Baseline evaluation 'fatal' — cannot be fixed": Demoted from fatal to major. While serious, the concern is about the comparison setup, not an inherent flaw in the method; proper baseline tuning could resolve it.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the baseline evaluation.** Train all baselines from scratch on the same training data with hyperparameter tuning, or apply the same SSL pretraining protocol to them. Demonstrate that baselines achieve reasonable (>60%) accuracy before claiming superiority.
2. **Resolve the loss-function ambiguity.** Either commit to standard NT-Xent per band (Equation 2) and explain how the adaptive temperature mechanism modifies it, or commit to the additive formulation (Equation 1) and clarify why this departure from NT-Xent is beneficial for EEG.
3. **Report results including the FTD group.** At minimum, perform 3-class (AD/FTD/CN) classification and AD-vs-FTD pairwise classification, or state the exclusion rationale explicitly.
4. **Clarify what dataset is used for SSL pretraining** (same 88 subjects or separate unlabeled corpus).
5. **Add error bars** (standard deviation or confidence intervals) to all main results.

## Score and Decision

**Bracketing (Round 1):** Retrieved anchors in the EEG self-supervised learning space ranged from strong reject (UniEEG, avg 2.00) to borderline accept (CBraMod, avg 6.75). Relevant anchors near the plausible score band: EEG-Pretraining Graph Contrastive MAE (avg 5.00), Cognition-Supervised Learning (avg 4.50), EEGPT (avg 4.00).

**Narrowing (Round 2):** Comparing item-weighted profiles:
- *EEGPT (4.00)*: Strongest negative weights -4.71 (evaluation methodology), -3.86 (tokenization), -3.55 (innovation). Positive weights ~10. Our paper's strongest negative is -2.32 (baseline eval), weaker than EEGPT's evaluation concern, but we have three major weaknesses rather than one concentrated one.
- *Cognition-Supervised Learning (4.50)*: Strongest negative -4.04 (overclaimed contribution). Positive weights ~10. Similar profile to this paper.
- *Graph Contrastive MAE (5.00)*: Negative weights -2.91, -2.47, -2.37. Positive weights 11.02, 8.71.

Our paper's strongest negative (-2.32) is comparable to papers scoring 4.0–5.0, but the presence of *three* independently problematical major issues (baseline credibility, loss-function incoherence, FTD exclusion) rather than one concentrated severe weakness pulls the score below the 5.0 anchor.

**Final Score: 4.0 / 10 — Borderline Reject.**

The paper has a conceptually interesting multi-band SSL architecture for EEG dementia classification and provides a thorough ablation. However, three major weaknesses — an evaluation comparison that is not credible because half the baselines perform at chance, an internally inconsistent loss-function description that makes the core technical contribution ambiguous, and the unexplained exclusion of 26% of the dataset — collectively prevent the paper from meeting the acceptance bar in its current form. The idea has merit, but the evidence presented does not support the claimed state-of-the-art performance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>