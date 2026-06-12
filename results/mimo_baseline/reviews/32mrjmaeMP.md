## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a dataless regularizer for weight disentanglement in Task Arithmetic that exploits the connection between representation drift and the Generalized Gauss-Newton (GGN) matrix under linearization. By using Kronecker-Factored Approximate Curvature (KFAC) to approximate the intractable Jacobian Gram matrix and introducing a Kronecker accumulation heuristic that merges per-task curvature factors into a single surrogate, the method achieves constant complexity in the number of tasks while eliminating the need for external task data. TAK achieves state-of-the-art results in task addition and negation across vision (CLIP ViTs) and language (T5-base) benchmarks.

## Strengths

- **Elegant theoretical connection with practical payoff:** The paper convincingly shows that the representation drift regularizer under linearization simplifies to a quadratic form of the Jacobian Gram matrix, which is exactly the GGN under squared loss (Eq. 3→5). This connection to the well-studied second-order optimization literature is clean and immediately enables leveraging KFAC. This is a genuine insight that transforms a data-dependent regularizer into a dataless one.

- **Strong empirical results, especially on task negation:** On task negation (Table 2), TAK achieves the lowest target-task accuracy (best forgetting) while best preserving the control task across all three ViT variants, surpassing even τJp which uses external task data. On task addition, TAK matches or exceeds τJp on ViT-B/32 (85.8 vs 85.0 abs. acc. at α=1) and ViT-L/14 (91.6 vs 90.9), demonstrating that dataless regularization can rival data-dependent approaches.

- **Demonstrated robustness to α eliminates held-out tuning:** The α-sweep analysis (Fig. 4a) shows that TAK maintains stable high accuracy across a wide range of scaling coefficients, unlike unregularized linear FT which peaks sharply at α≈0.5. This is a practically significant result that removes the need for cross-task validation data, further reinforcing the dataless nature of the method.

- **Constant complexity aggregation scheme:** The Kronecker accumulation heuristic (Eq. 8) reduces storage from O(T) to O(1) in the number of tasks. Table 3 shows this introduces only marginal performance gaps compared to the idealized naïve multi-task formulation, with the accumulated regularizer even slightly outperforming on ViT-B/16 and T5-base.

- **Comprehensive ablation studies:** The paper systematically examines KFAC estimation quality (Fig. 7a), compression strategies (Fig. 7b), scheduling frequency (Fig. 8), memory overhead (Fig. 6), and task localization behavior (Fig. 5), providing practitioners with actionable guidance for deployment.

## Weaknesses

### Fatal
None.

### Major

- **Kronecker accumulation heuristic lacks theoretical justification:** The merging step in Eq. 8, $(\sum_t B_t) \otimes (\sum_t \lambda_t A_t)$, is introduced without formal analysis of its approximation quality. While empirically validated, this is the core technical contribution that enables constant complexity, and the paper does not provide bounds, conditions under which it fails, or theoretical reasoning for why it works. The ViT-B/32 results in Table 3 show a measurable gap (86.5→85.8, ~0.7 points) suggesting the approximation is not lossless, yet no analysis explains when or why the gap widens.

- **Non-linear regime extension relies on a non-principled workaround:** Applying TAK in the non-linear regime requires pairing with Attention-Only Fine-Tuning (Jin et al., 2025), justified by the empirical claim that it "induces approximately linear fine-tuning dynamics." This makes the non-linear results dependent on a separate finding rather than the paper's own framework, and limits applicability to architectures where attention-only fine-tuning is viable.

### Minor

- **Limited diversity of architectures and tasks:** All experiments use ViT-based CLIP models for vision and T5-base for language. The paper does not evaluate on larger foundation models (e.g., LLMs for generative tasks), other modalities, or more complex downstream tasks (e.g., VQA, captioning). Given the paper's emphasis on foundation model adaptation and mentions of conversational models in the conclusion, broader evaluation would strengthen the claims.

- **Inconsistency in best results between methods:** TAK achieves the best absolute accuracy with best α on ViT-B/32 and ViT-L/14, but on ViT-B/16 its best normalized accuracy (98.1) is lower than τJp's (98.7). This is not discussed or analyzed.

### Trivial
None.

## Nice-to-Haves

- A theoretical analysis or bound on the quality of the Kronecker accumulation approximation, even under simplifying assumptions (e.g., when task KFAC factors have particular structure).
- Evaluation on larger-scale models (e.g., 7B+ LLMs) where the practical benefits of dataless regularization are most relevant.
- Analysis of how TAK interacts with parameter-efficient fine-tuning methods (LoRA, adapters) which are more commonly used in practice than full fine-tuning.

## Novel Insights

The core novel insight is that the representation drift regularizer under linearization can be reinterpreted as a GGN quadratic form (Eq. 3→5), which is a well-studied object in second-order optimization. This reframing is non-trivial: it transforms a regularizer that conceptually requires computing pairwise Jacobian products over external datasets into a curvature matrix that can be approximated once and shared. The additional insight that per-task KFAC factors can be approximately aggregated via a simple outer-product-of-sums heuristic (Eq. 8) to achieve constant complexity in T is practically valuable. The paper also demonstrates that curvature regularization enables a clean operational definition of "task localization" (Fig. 5), providing interpretable evidence that the regularizer indeed promotes weight disentanglement.

## Suggestions

- Add a formal analysis of the Kronecker merging approximation quality. Even a simple perturbation analysis showing how the error depends on the correlation structure across tasks' KFAC factors would strengthen the theoretical contribution.
- Discuss the limitations of the non-linear extension more explicitly, including when attention-only fine-tuning may not induce approximately linear dynamics (e.g., with very deep networks or non-Transformer architectures).
- Provide a clearer comparison of when τJp's use of external data is beneficial versus when TAK's dataless approach is sufficient, helping practitioners choose between the two approaches.

## Score and Decision

The paper makes a solid contribution by connecting representation drift regularization to well-established curvature approximation techniques, achieving a practical and theoretically motivated dataless regularizer. The empirical results are strong, particularly on task negation and robustness to scaling coefficients, and the comprehensive ablation studies provide useful practical guidance. The main weaknesses—lack of theoretical justification for the Kronecker accumulation heuristic and the non-principled extension to non-linear fine-tuning—are meaningful but do not invalidate the core contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept