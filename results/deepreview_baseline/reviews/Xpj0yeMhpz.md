## Summary

This paper expands the scope of machine unlearning by decoupling the class label from the target concept, introducing three new unlearning scenarios beyond conventional all-matched forgetting: target mismatch, model mismatch, and data mismatch. The authors identify key challenges such as insufficient representation and decomposition lacking that arise from label domain mismatch, and propose TARF (TARget-aware Forgetting), a framework combining annealed gradient ascent on forgetting data with target-aware gradient descent on selected retaining data. Experiments across multiple benchmarks and real-world applications demonstrate that TARF consistently outperforms existing methods under these newly defined mismatch settings while maintaining competitive performance on conventional all-matched forgetting.

## Strengths

- **Conceptually novel problem formulation**: The paper identifies and formalizes a genuinely important gap in existing unlearning research—the implicit assumption that class labels and target concepts always align. By introducing three concrete mismatch scenarios (target, model, data), the work provides a structured taxonomy that substantially broadens the practical relevance of machine unlearning to realistic deployment scenarios where user requests may not align with pre-training taxonomies.

- **Theoretical grounding of observed phenomena**: Theorem 3.2 establishing the "gravity effects" on forgetting dynamics is a valuable contribution. The connection between representation distance and the degree of forgetting spillover provides a principled explanation for why existing methods fail under mismatch scenarios, and the formalization guides the algorithmic design of TARF.

- **Strong empirical validation**: The experimental evaluation is comprehensive and convincing. Table 3 shows that TARF achieves dramatically lower Gap scores compared to all baselines on the challenging mismatch scenarios (e.g., Gap of 0.21 vs. 8.86 for GA on CIFAR-100 target mismatch; Gap of 1.17 vs. 2.43 for GA on CIFAR-100 data mismatch). The fine-grained evaluation in Table 2 demonstrates that TARF successfully achieves the intended separation between forgetting and affected retaining data within the same superclass. Large-scale experiments on ImageNet-1k confirm scalability.

- **Well-motivated algorithm design**: The three-phase interpretation (target identification, target separation, retaining approximation) of the unified TARF framework is logically connected to the identified challenges. The ablation studies (Figure 7) systematically validate each design choice, including the annealing strategy for gradient ascent and the identification mechanism for false retaining data.

## Weaknesses

### Major

1. **The target identification mechanism (Phase I) relies on class-level accuracy drops, which presupposes access to class labels during unlearning.** The paper states this is available "as it is also available for unlearning" (Section 3.3), but this is a strong assumption that limits applicability. In many practical unlearning scenarios, the forgetting request may involve examples without ground-truth class labels, and the mechanism for identifying false retaining data from accuracy drops across labeled classes may not transfer to other modalities (e.g., language models, generative models) where the notion of "class accuracy" is not well-defined. The paper's own case studies on stable diffusion and TOFU (Table 5) sidestep this issue, and the claimed "general framework" requires this identification step to work without explicit class structures.

2. **The proposed framework introduces additional hyperparameters (k, t₀, t₁, β) with limited guidance for practical tuning.** While the paper provides some discussion in Appendix E, the sensitivity of TARF to these parameters (especially the initialization strength k shown in Figure 7, where performance degrades significantly beyond the optimal value) raises concerns about practical usability. The paper does not provide a systematic procedure for setting these hyperparameters that would generalize across different datasets, models, and forgetting requests.

3. **The reliance on representation gravity for identification is not evaluated under distribution shift or noisy representation regimes.** The paper briefly mentions in the "Open challenge" section that this mechanism becomes weaker when concepts are "inherently ambiguous, weakly clustered, or attribute-entangled," but does not provide concrete experiments or robustness evaluations showing the degradation pattern. This is particularly relevant given that many realistic forgetting requests may involve precisely such ambiguous concepts (e.g., erasing "harmful content" or "bias" that spans multiple high-level categories).

### Minor

1. **The computational advantage of TARF over baselines varies significantly by task.** While TARF achieves the best Gap scores across mismatch scenarios, its runtime (4.21-4.85s on CIFAR-100) is substantially higher than GA (0.05-0.06s) and BS (0.78-0.97s). For resource-constrained deployment scenarios, this computational overhead may be a practical concern, and the paper does not adequately discuss the runtime-effectiveness tradeoff.

2. **The case study on stable diffusion (Figure 6) is presented as a demonstration of "data mismatch concept removal" but lacks quantitative evaluation.** Unlike the classification experiments with clear metrics (UA, RA, TA, MIA), the generative removal results are shown qualitatively without any automated metric for concept retention/forgetting, making it difficult to compare against baselines or assess the degree of successful removal.

3. **The application on TOFU (Table 5) shows that TARF's performance is sometimes worse than simple GA on retaining data** (e.g., QA Prob on R. for All-matched: 0.0824 vs 0.1624 for GA). While the paper frames TARF as better overall, the mixed results in the LLM domain suggest the framework may need adaptation for language modality, which is not discussed.

## Novel Insights

The key novel insight is the identification of "representation gravity" in forgetting dynamics—the phenomenon that gradient-based unlearning propagates non-uniformly through representation space proportional to the distance between data points in the latent space. This insight, formalized in Theorem 3.2, bridges the gap between the geometry of learned representations and the effectiveness of forgetting, and provides a principled mechanism for detecting "false retaining data" (data that belongs to the target concept but was not explicitly identified for forgetting). This repurposing of the forgetting process itself as a diagnostic tool is conceptually elegant and practically useful.

## Suggestions

1. **Provide more explicit guidance or an automated procedure for setting the key hyperparameters (k, t₀, t₁, β)** , perhaps based on properties of the training data (e.g., number of classes, loss statistics from initial gradient ascent). A sensitivity analysis with recommendations for different dataset scales would significantly improve practical usability.

2. **Evaluate TARF under more challenging conditions where class labels are not available for target identification**, such as using only feature-space proximity (e.g., k-NN in representation space) instead of class accuracy drops, to demonstrate the generality of the framework beyond classification tasks.

3. **Quantitatively evaluate the stable diffusion case study** using established metrics for concept erasure (e.g., CLIP score on generated images, success rate of concept classifiers, or FID on concept-free generation) to provide a more rigorous comparison with existing concept removal baselines.

## Score and Decision

The paper makes a genuinely novel and important contribution to the machine unlearning literature by identifying and formalizing a previously overlooked assumption (alignment of class labels and target concepts) and providing both theoretical analysis and algorithmic solutions. The empirical evidence is strong across multiple benchmarks and tasks. The weaknesses—primarily around the reliance on class labels for identification and limited hyperparameter guidance—are significant but not fatal to the core contribution.

The paper is well above the acceptance threshold. It provides new problem formulations that will likely influence future work in the field, sound theoretical intuition, and a practical framework that demonstrably outperforms existing methods.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>