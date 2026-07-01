## Summary
This paper proposes a post-training fine-tuning framework for flow-matching generative models that enforces physical constraints (PDE residuals) and jointly infers latent physical parameters. The method leverages adjoint matching with weak-form PDE residuals as the reward, scales the memoryless noise schedule for stability, and introduces a joint evolution of state and parameter variables to enable inverse problem solving without paired parameter-solution training data. Experiments on four PDE families (Darcy, linear elasticity, Helmholtz, Stokes) and a natural-image color transformation demonstrate reduced residuals and plausible parameter recovery.

## Strengths
- **Clearly motivated and principled framework**: The paper tackles an important practical problem—enforcing parameter-dependent PDE constraints in generative models when only state observations are available. The use of adjoint matching to tilt the generative distribution is theoretically grounded, and the extension to joint parameter-state flows is a natural and effective solution.
- **Novel technical contributions with practical value**: The scaled memoryless noise schedule ($\sigma^2(t) = (1-\kappa)2\eta_t$) preserves theoretical consistency while providing a stability knob—a simple but useful improvement over the original formulation. The joint evolution of $\alpha$ with a surrogate base flow and the regularization term $f(\alpha)$ are well-designed to balance physical consistency and distributional fidelity.
- **Thorough empirical validation across diverse PDE problems**: Experiments cover four distinct PDE families (elliptic, elastic, wave, incompressible flow) with different types of misspecification (noise, boundary condition mismatch, model form error). The ablations systematically explore the $\lambda_x,\lambda_\alpha,\lambda_f$ trade-offs, giving practical insight.
- **Low computational overhead**: Fine-tuning requires only 20 gradient steps (<15 minutes for Darcy) and inference is at base-model cost—a strong practical advantage over pre-training or projection-based approaches.
- **Clearly written and well-structured**: The method is presented step by step, the loss functions are clearly specified, and the relationship to adjoint matching is well explained.

## Weaknesses

### Fatal
None.

### Major
- **Insufficient comparison to existing post-training/inference-time constraint enforcement methods**: The paper compares only to ablations of its own method and to PBFM (a pre-training approach). Established post-training alternatives such as projection-based methods (Christopher et al. 2024, Lu & Xu 2024), guidance-based methods (Huang et al. 2024, Xu et al. 2025), and distillation approaches are mentioned in related work but never used as baselines. Without such comparisons, it is difficult to assess whether the proposed framework offers meaningful advantages over existing approaches in terms of residual reduction, distributional fidelity, or computational cost.
- **Limited experimental scope**: The method is only tested on 2D steady-state PDEs with simple geometries. Time-dependent problems, 3D domains, non-linear PDEs, or coupled systems are not considered. The natural-image example uses a non-physical PickScore reward, weakening the paper’s core claim of “physics-constrained fine-tuning.” The paper’s title and main focus promise physical constraints, yet the image experiment is tangential and does not involve PDEs.
- **Potential feedback-loop issue with inverse predictor $\varphi$**: The inverse predictor $\varphi$ is pre-trained on base model samples, which may be noisy or inaccurate (e.g., Darcy case). The fine-tuning then relies on $\varphi$ to define the surrogate base flow for $\alpha$ and the regularization target. If $\varphi$ is biased, errors may propagate during fine-tuning. The paper does not analyze this coupling or evaluate sensitivity to $\varphi$ quality.
- **Ad-hoc elements with limited theoretical justification**: The surrogate base flow $v_{t,\alpha}^{\text{base}}(\alpha_t) = (\hat{\alpha}_1 - \alpha_t)/(1-t)$ and the regularization $f(\alpha) = \lambda_f \|v_{t,\alpha}^{\text{ft}} - v_{t,\alpha}^{\text{reg}}\|^2$ are plausible but presented without formal analysis. The justification for why this specific construction leads to a valid joint flow is missing, and the impact of the regularization on the final tilted distribution is not characterized theoretically.

### Minor
- **Evaluation metrics**: The relative residuals (scaled by mean residual of a reference set) could be sensitive to the choice of reference set. MMD values are reported without confidence intervals or statistical significance tests across multiple runs. The MMD values are small and close across methods, making it hard to determine practical significance.
- **Insufficient intuition for scaled memoryless schedule**: The paper states that the scaled schedule $\sigma^2(t) = (1-\kappa)2\eta_t$ remains memoryless (Lemma 1 in Appendix D.4), but the main text does not provide the intuition or proof sketch. Given its central role in the method, a brief justification would help readers.
- **Hyperparameter sensitivity**: While ablations demonstrate trade-offs, the optimal settings for $\lambda_x, \lambda_\alpha, \lambda_f$ appear problem-dependent. The paper does not offer guidelines on how practitioners should select these values in new applications.

### Trivial
- Some figure captions are overly repetitive (e.g., Figure 1 caption repeats the same information in three paragraphs). The paper would benefit from more concise figure captions.

## Nice-to-Haves
- Apply the method to a time-dependent PDE (e.g., Burgers equation, advection-diffusion) to demonstrate generalization.
- Analyze the computational cost and scaling of the adjoint computation for higher-resolution or 3D problems.
- Include a comparison to one inference-time projection method (e.g., Christopher et al. 2024 or Lu & Xu 2024) on at least one PDE example to strengthen the empirical case.

## Novel Insights
Beyond the paper’s own contributions, the key insight is that adjoint matching can be extended beyond state-only fine-tuning to jointly sample latent physical parameters without paired training data, by constructing a surrogate base flow for parameters via a pre-trained inverse predictor. The addition of a scaled memoryless schedule is a practical innovation that may be applicable to other adjoint-matching settings (e.g., preference fine-tuning of flow models) where noise-induced instability near $t=0$ is a concern.

## Suggestions
- Add at least one comparison to a representative post-training or inference-time constraint enforcement method (e.g., the projection approach of Christopher et al. 2024 or the guidance method of Huang et al. 2024) on one of the PDE tasks to contextualize the method’s performance.
- Include an analysis of how the quality of the pre-trained inverse predictor $\varphi$ affects fine-tuning results, e.g., by varying the amount of training data for $\varphi$ and measuring downstream residual and MMD metrics.
- Provide a brief proof sketch or intuitive explanation in the main text for why the scaled noise schedule $\sigma^2(t) = (1-\kappa)2\eta_t$ retains the memoryless property, so that readers can understand the theoretical guarantee without consulting the appendix.
- Report confidence intervals or statistical significance tests for the MMD comparisons across multiple random seeds to strengthen conclusions about distributional fidelity.

## Score and Decision
Score: 6
Decision: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>