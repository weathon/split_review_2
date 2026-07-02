## Summary
# Final Review Report

## Summary

This paper presents DGNet, a self-supervised multi-band EEG representation learning framework for dementia classification. The method extends SimCLR contrastive learning to EEG by decomposing signals into five frequency bands (delta, theta, alpha, beta, gamma) and applying independent 1D-CNN encoders with per-band projection heads. An adaptive temperature mechanism with regularization is introduced per band. The model is evaluated on a clinical dataset of 88 participants (36 AD, 23 FTD, 29 CN) using Leave-One-Subject-Out cross-validation, achieving 92.90% accuracy and 92.85% F1-score for AD vs. CN classification.

**Core strengths:** The multi-band architecture is neurophysiologically motivated (EEG spectral slowing in dementia is a well-known biomarker), and the SSL approach addresses the practical challenge of limited labeled medical data. The reported gains over from-scratch training (+29.6 absolute pp, +31.5% relative) are substantial.

**Core weaknesses:** The claims are undermined by several methodological issues: (1) The main loss function (Eq. 1) structurally differs from standard NT-Xent without explanation or justification; (2) Baseline comparisons are unfair — generic EEG decoding models are evaluated without task-specific training; (3) No confidence intervals or variance are reported for any method, making the reported improvements unverifiable; (4) The ablation study contains confounded conditions and a surprisingly large (+13pp) gain attributed to adaptive temperature/regularization that is not mechanistically explained; (5) FTD data is excluded from the main analysis without comment; (6) The SOTA claim in the abstract is unverifiable without external literature retrieval, which was unavailable in this review run. Given these concerns, the paper requires substantial revision before acceptance.

## Strengths
1. **Neurophysiologically motivated architecture.** The multi-band decomposition aligns with established EEG biomarkers of dementia (spectral slowing), giving the method a clear clinical rationale. Processing each frequency band independently rather than using aggregated band-power features is a reasonable design choice.

2. **Self-supervised learning for scarce medical data.** The application of SimCLR-style contrastive learning to EEG, where labeled data is expensive but unlabeled recordings are relatively abundant, addresses a genuine bottleneck in clinical machine learning.

3. **Strong reported empirical results.** The absolute improvements over from-scratch training (+29.6 percentage points) are large, and the 92.9% accuracy on the binary AD vs. CN task is competitive with prior published work on this dataset (Table 2).

4. **Detailed data augmentation strategy.** The paper provides precise parameters for five EEG-specific augmentations (Gaussian noise σ=0.03, scaling factor 0.8–1.2, 10% time/frequency masking, 10% channel dropout), which is valuable for reproducibility.

5. **Leave-One-Subject-Out evaluation.** LOSO cross-validation is the appropriate protocol for EEG subject-independent evaluation, preventing data leakage between training and testing. This strengthens the generalization claims relative to random train/test splits.

6. **Comprehensive ablation study direction.** While the ablation has confounds (detailed in Weaknesses), the attempt to isolate SSL, multi-head, augmentation, adaptive temperature, and regularization effects provides a useful framework for understanding the contribution of each component.

## Weaknesses
### W1. Critical: Loss function mismatch (Eq. 1 vs. standard NT-Xent) — Page 5

The adaptive multi-band loss in Eq. (1) is structurally different from the standard NT-Xent loss defined in Eq. (2). Eq. (1) is an additive combination of raw cosine similarities with a max-over-negatives operator, whereas standard NT-Xent uses a softmax-normalized log-probability over all negatives. The text describes the loss as "NT-Xent" but the equation does not implement it. Additionally, the notation $\tau_{(i,n)}^{(b)-}$ implies per-negative-instance learnable temperatures — with batch size 64 and 5 bands, this would mean 315 learnable temperatures per anchor, which is likely not what was implemented. This discrepancy must be resolved: either correct the equation to match the implementation, or rename the loss and justify the additive + max-over-negatives design with a dedicated ablation.

**Severity: Major | Fixability: Easy (clarify or correct)**

### W2. Critical: Unfair baseline comparison — Page 7 (Table 1)

Table 1 compares the proposed method against 12 generic EEG decoding models (designed for motor imagery/ERP) without task-specific training or pretraining on dementia data. The proposed model uses SSL pretraining on the target dataset, giving it a decisive advantage. A fair comparison requires: (a) supervised training of each baseline on the same AD/CN task, and (b) SSL-pretrained variants of equivalent backbone architectures. Without this, the reported "93% vs. next-best 74%" is misleading.

**Severity: Major | Fixability: Medium (add fair baselines)**

### W3. Critical: Missing variance and statistical significance — All tables

No standard deviations, confidence intervals, or significance tests are reported for any method in any table. With N=88 subjects and LOSO cross-validation, accuracy estimates have substantial binomial variance. The only baseline with reported variance (BI-MCGNN: 91.25 ± 0.38 in Table 2) overlaps with the proposed method's 92.90% within 2-3 standard errors. The claim of "significantly outperforming all comparison models" is not statistically supported.

**Severity: Major | Fixability: Medium (report variance over LOSO folds or bootstrap)**

### W4. Major: Ablation study confounds — Page 8 (Table 3)

The jump from "Multi-head (5 heads)" at 79.55% to the full model at 92.90% (+13.35 pp) is attributed to adaptive temperature + regularization, yet no mechanistic explanation is given for such a large gain from a loss modification. Missing controls: (a) adaptive temperature without regularization, (b) standard NT-Xent (all negatives, fixed τ) as a proper baseline. The "w/o augmentation" row uses a fundamentally different pretraining objective (MSE reconstruction), making it an unfair comparison rather than a clean ablation.

**Severity: Major | Fixability: Medium (add missing controls + explanations)**

### W5. Major: Small sample and missing FTD results — Page 6 (Section 3.1)

The dataset has only 88 subjects. The FTD group (N=23) is excluded from Tables 1-2 without justification. Unequal recording durations (AD range: 5.1–21.3 min; CN range: 12.5–16.5 min) could introduce systematic bias. The paper should report 3-way (AD/FTD/CN) results, explain why FTD is excluded, and verify that per-subject data quantity does not correlate with classification outcomes.

**Severity: Major | Fixability: Medium (add analysis)**

### W6. Major: Unverifiable SOTA claim — Abstract

"To the best of our knowledge, our proposed method achieved state-of-the-art performance in multi-head approaches" is vague (what is a "multi-head approach"?) and unverifiable without external literature retrieval (unavailable in this review run). The in-text supporting claim "31.5% relative improvement over training from scratch and 25.4% over single-head" is correctly computed from Table 3 (63.35% to 92.90% is ~46.6% relative improvement, not 31.5% — verify arithmetic) but the relative improvement denominator needs explicit reporting.

**Severity: Major | Fixability: Easy (rewrite with bounded scope)**

### W7. Major: No limitations discussion — Conclusion (Page 8)

The paper lacks any limitations or future work section. Critical unaddressed limitations include: single dataset evaluation, no out-of-distribution testing, no deployment feasibility analysis, no interpretability of learned representations, and no discussion of clinical applicability constraints.

**Severity: Major | Fixability: Easy (add limitations paragraph)**

### W8. Moderate: Two downstream approaches described but only one evaluated — Page 4

Both frozen-encoder (linear evaluation) and full fine-tuning are described, but only frozen-encoder results are reported. The MLP classifier (2 hidden layers, 512+256 units) is also overengineered for standard linear evaluation, which typically uses a single linear layer. The classifier itself may be learning task-specific features beyond what the encoder provides.

**Severity: Minor | Fixability: Easy (report both or simplify)**

### W9. Moderate: Introduction writing quality — Page 1

The introduction is unusually long (~60% of the paper's pre-method text) and uses overly dramatic language ("tsunami," "shaking foundations," "perfectly aligns"). Two paragraphs make the same point about MRI/PET costs without progression. The spectral biomarkers paragraph (well-written but disconnected from the technical gap) does not explain why existing methods fail or how the proposed SSL approach addresses their shortcomings.

**Severity: Minor | Fixability: Easy (restructure and tighten)**

### W10. Moderate: New term AMCL in conclusion — Page 8

"Adaptive Multi-head Contrastive Learning (AMCL)" from Wang et al. (2024) is introduced only in the conclusion without prior definition in the Method section. It is unclear whether this is the authors' term for their method or an existing method they applied. This creates confusion about the paper's original contribution.

**Severity: Minor | Fixability: Easy (define earlier or remove)**

### W11. Moderate: Novelty assessment deferred

Due to Retrieval-Disabled Mode in this review run (external paper search unavailable), the novelty of the proposed multi-band SimCLR adaptation relative to existing EEG contrastive learning work (e.g., TS-TCC, CLOCS, EEG-SimCLR variants) cannot be independently verified. The paper does not cite or compare against these methods. This verification should be performed manually by the authors or a reviewer with literature access.

**Severity: Information | Fixability: Manual verification needed**

### W12. Minor: Data augmentation paragraph has a redundant sentence — Page 4

"It generates two views of the same original signal that are semantically identical but morphologically different by applying various transformations" repeats the idea from the preceding sentence almost verbatim.

**Severity: Minor | Fixability: Easy (delete duplicate)**

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses a relevant clinical problem (EEG-based dementia screening) with a neurophysiologically motivated multi-band self-supervised learning approach. The reported empirical results are competitive. However, multiple major methodological weaknesses prevent a higher score at this stage: (1) the loss function definition in Eq. (1) does not match the described NT-Xent formulation, creating a reproducibility risk; (2) baseline comparisons are unfair, undermining the claimed superiority; (3) variance and significance testing are entirely absent from all tables; (4) the ablation study has confounded conditions that prevent clean attribution of gains; and (5) the novelty of the approach relative to existing EEG contrastive learning work cannot be verified without external literature access. These issues are individually fixable — the paper's core idea has merit — but the current presentation overstates what has been rigorously demonstrated. A revised version addressing the major weaknesses (W1–W7) could raise the score to 6–7/10.