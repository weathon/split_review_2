## Summary
KOALA proposes a novel adversarial detection method that flags an input as attacked when the class predictions from two complementary nearest-prototype classifiers—one using KL divergence (sensitive to dense perturbations) and one using an \(L_0\)-based similarity (sensitive to sparse perturbations)—disagree. The method is semantics-free, requires only fine-tuning the backbone encoder on clean images (no adversarial training), and is accompanied by a formal theorem claiming that when class prototypes are sufficiently separated, any norm-bounded perturbation must cause this disagreement, guaranteeing detection. Experiments on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet show perfect detection on a “theorem-compliant” subset and moderate performance on the full test set.

## Strengths
- **Novel detection principle** – The idea of using the disagreement between a dense-sensitive metric (KL) and a sparse-sensitive metric (\(L_0\)) as an adversarial detector is original and well-motivated.  
- **Lightweight and plug-and-play** – The method does not require adversarial training, architectural changes, or external semantic information, making it practical for many existing models.  
- **Theoretical ambition** – Providing a formal guarantee under explicit assumptions is a desirable direction, and the proof sketch conveys a clear geometric intuition.

## Weaknesses

### Fatal
**Non-standard and incorrect detection metrics.**  
The paper defines true positives (TP) for the detection task as:  
\(TP := [a=1] \land [(\hat{a},\hat{y})=(1,\perp) \lor (\hat{a},\hat{y})=(0,y^*)]\).  
This means that an *undetected* attack (the system does not flag it) is counted as a TP as long as the classification happens to be correct. In standard detection evaluation, an attack that is not flagged is a false negative regardless of classification outcome. Similarly, false negatives are defined only when the attack is not flagged **and** the classification is wrong. This formulation conflates detection with classification accuracy and **severely inflates** reported precision and recall. Consequently, all detection numbers (Tables 1 and 2) are not interpretable as standard detection performance and the empirical claims of the paper are unsupported. This is a fatal flaw that invalidates the core experimental contribution.

### Major
1. **Unspecified criterion for “theorem-compliant” samples.**  
   Experiment 1 partitions the test set based on whether Theorem 1’s condition (\(|c_i^* - \hat{c}_i| > \Gamma_i(\epsilon)\)) is satisfied. The paper never defines \(\Gamma_i(\epsilon)\) nor describes how this condition is evaluated in practice (e.g., which adversarial class prototype is considered, how the bound is computed). Without this, the central experiment is not reproducible and the claim “perfect detection when conditions are met” becomes a tautology (the subset is defined by the very condition that guarantees detection).

2. **Insufficiently rigorous proof in the main text.**  
   While the appendix is missing (and cannot be penalized), the proof sketch in Section 3.2 lacks crucial details: the derivation of the threshold \(\tau\), the exact form of the “coordinate gap” condition, the handling of multiple adversarial classes, and the role of the Lipschitz constant of the backbone. A reader cannot assess whether the theorem is indeed correct. Given that the theoretical guarantee is the paper’s headline contribution, the main text should provide at least a self-contained high-level argument with quantifiable constants; instead it only gives qualitative propositions.

### Minor
- **Sensitivity of hyperparameters** – The fine-tuning loss uses weights \(\omega_{L_0}=0.9, \omega_{KL}=0.1\) and \(\tau=0.75, \phi=0.5\) with no ablation study or sensitivity analysis.  
- **CLIP prototype definition** – For CLIP, class prototypes are obtained from the text encoder (“a photo of [CLASS]”), which introduces a form of semantic prior, weakening the “semantics-free” claim.  
- **Ambiguity in perturbation scope** – Assumption A2 refers to a perturbation \(\delta\) in feature space, but attacks are applied in input space. The transfer requires Lipschitz continuity, which is mentioned but not quantified or verified for the models used.

### Trivial
- Some notation inconsistencies (e.g., \(\hat{y}\) used for both KL and \(L_0\) predictions and for final decision; softmax normalization on features is assumed but not empirically checked).

## Nice-to-Haves
- A standard ROC or AUROC analysis for detection would be more informative than the bespoke confusion matrix.
- A comparison with existing detection methods (e.g., LID, Mahalanobis, feature squeezing) in the same setting would help position the work.
- An analysis of the false positive rate on clean data (beyond the theorem-compliant subset) is needed.

## Novel Insights
The geometric intuition that a norm-bounded perturbation cannot simultaneously push an embedding out of both a KL-based stability band and an \(L_0\)-based stability band is genuinely insightful. If the theoretical conditions can be made practically checkable, this principle could lead to certifiable detection without requiring fully certified classifiers.

## Suggestions
1. **Revise the detection evaluation** to use standard definitions: TP = attacked input flagged as attack; FN = attacked input not flagged; FP = clean input flagged; TN = clean input not flagged. Report detection rate (recall), false positive rate, and AUROC.  
2. **Operationalize the theorem condition** – specify how \(\Gamma_i(\epsilon)\) is computed and how the “theorem-compliant” subset is selected. Provide a reproducible algorithm.  
3. **Strengthen the theoretical exposition** in the main paper by providing at least a few key inequalities that bring the threshold \(\tau\) and the class-gap condition into concrete terms.

## Score and Decision
*Score*: 3  
*Decision*: Reject  

The paper presents a novel and interesting idea, but a fatal flaw in the evaluation metrics invalidates the reported detection performance, and a major lack of reproducibility for the core theorem verification undermines the empirical support. The theoretical contribution remains promising but is not yet convincingly demonstrated or connected to practical evaluation.  

MY FINAL SCORE: 3</score>  
MY FINAL DECISION: Reject</decision>