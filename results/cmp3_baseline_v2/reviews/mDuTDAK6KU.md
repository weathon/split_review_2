## Summary

The paper proposes KOALA, an adversarial detection method that flags an input as attacked when two complementary similarity metrics—KL divergence and a custom L₀-based metric—disagree on the predicted class. The method requires only fine-tuning a backbone encoder on clean images, avoids adversarial training, and is accompanied by a formal theorem claiming that under certain conditions detection is guaranteed. Experiments on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet are presented.

## Strengths

- The core idea of using two complementary metrics (KL for dense, low-amplitude perturbations; L₀ for sparse, high-impact perturbations) is intuitive and well-motivated.
- The paper attempts to provide a theoretical guarantee for detection, which is rare in the adversarial detection literature.
- The method does not require adversarial training or architectural changes, making it potentially practical as a plug-in module.

## Weaknesses

### Fatal

**Non-standard and misleading evaluation metrics.** The paper defines True Positive (TP) as:  
`[a = 1] ∧ [ (â, ŷ) = (1, ⟂) ∨ (â, ŷ) = (0, y*) ]`.  
This means that an attacked input is counted as a true positive even when the detector *does not flag it* (â=0) as long as the model still predicts the correct class. This conflates successful classification under attack with attack detection. Standard detection evaluation should treat an undetected attack as a false negative. Similarly, False Positive includes cases where a clean input is misclassified (â=0, ŷ≠y*), which is a classification error, not a false alarm.  

Because of this non-standard definition, all reported precision, recall, and F1 scores are inflated and do not reflect the detector’s actual ability to distinguish clean from adversarial inputs. The paper’s central experimental claims are therefore unsupported. This flaw alone invalidates the empirical contribution.

### Major

- **No comparison to any existing detection method.** The paper does not benchmark against any prior adversarial detector (e.g., LID, Mahalanobis, feature squeezing, NIC, CADet, etc.). Without such comparisons, it is impossible to assess whether KOALA offers any practical advantage over the state of the art. The paper’s claim of being a “novel” detector is unsubstantiated.

- **The theoretical guarantee is not operationalized.** Theorem 1 states that detection is guaranteed when “there exists a coordinate i where the gap between the true class prototype and the predicted adversarial class prototype is sufficiently large.” The paper does not specify how to compute the threshold Γᵢ(ε), how to check this condition in practice, or what fraction of test examples satisfy it. The experimental “Theorem-Compliant” subset is defined without explaining the criterion used to partition the data. The guarantee therefore has no actionable value.

- **The proof sketch is too vague to be assessed.** The main paper only sketches three propositions without stating them formally. The full proof is relegated to the appendix (not provided). The assumptions (A1–A4) are strong and not clearly justified (e.g., A1 requires normalized positive embeddings summing to 1, which is not typical for encoder outputs; A2 assumes a feature-space perturbation bound that is not directly related to the input-space ε used in attacks). The proof does not convincingly establish the claimed mutual exclusivity.

- **The method’s performance on the full test set is modest.** On ResNet/CIFAR-10, precision is 0.94 but recall is only 0.81; on CLIP/Tiny-ImageNet, precision drops to 0.66. Even ignoring the metric flaw, these numbers are not competitive with existing detectors that often achieve >0.95 on both precision and recall. The paper does not discuss this.

- **The ablation study reveals a problematic behavior on CLIP.** The KL+L₀+Cosine combination yields the highest detection metrics, but the paper explains this is because the model’s classification breaks down (adversarial accuracy is very low), so disagreement is essentially random. This undermines the claim that KOALA is a principled detector—it can achieve high detection simply by making the model unreliable.

### Minor

- The L₀ metric defined in Eq. (2) is a custom thresholded count, not the standard L₀ norm. Its sensitivity to the hyperparameter τ (set to 0.75 without sensitivity analysis) is not explored.
- The paper does not evaluate against adaptive attacks where an adversary is aware of the detector.
- The training recipe is described as “lightweight” but no training time or computational cost is reported.

### Trivial

- The title “KL-L0 Adversarial detection via Label Agreement” is slightly misleading because the method detects attacks via *disagreement*, not agreement.

## Nice-to-Haves

- A comparison to at least 2–3 standard detection baselines (e.g., Mahalanobis, LID, feature squeezing) would be essential to demonstrate the method’s value.
- The evaluation should be redone with standard detection metrics (TP = attacked and flagged, FP = clean and flagged, etc.) and reported separately from classification accuracy.
- A sensitivity analysis of the L₀ threshold τ and the loss weights ω would strengthen the empirical study.

## Novel Insights

None beyond the paper’s own contributions. The idea of using two complementary metrics is interesting, but the paper does not provide a clean empirical validation or a practically useful theoretical condition.

## Suggestions

1. Redefine the detection confusion matrix using standard definitions: TP = attacked input that is flagged (â=1), FP = clean input that is flagged, TN = clean input not flagged, FN = attacked input not flagged. Report detection metrics separately from classification accuracy.
2. Compare KOALA against at least three existing detection methods on the same datasets and attacks.
3. Clarify how the “Theorem-Compliant” subset is determined and report the fraction of test examples that satisfy the condition. Provide a practical way to check the condition for a given input.
4. Provide the full proof in the main paper or a more detailed sketch that states the propositions and shows the key inequalities.
5. Evaluate against adaptive attacks (e.g., an adversary that optimizes to make KL and L₀ predictions agree on a wrong class).

## Score and Decision

**Score:** 3  
**Decision:** Reject  

The paper has a novel conceptual direction and attempts a theoretical analysis, but the evaluation is fatally flawed due to non-standard metrics that conflate detection with classification. Without a corrected evaluation and comparison to baselines, the empirical claims are not credible. The theoretical guarantee, while interesting, is not operationalized and the proof is insufficiently detailed. The paper in its current form does not provide reliable evidence that KOALA is an effective adversarial detector.

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>