### Summary

The paper presents MolMiner, a novel fragment-based, geometry-aware, and order-agnostic autoregressive model for molecular design. The model supports conditional generation of molecules over twelve properties, including logP, QED, SAS, FractionCSP3, molecular weight, TPSA, molar refractivity, hydrogen bond donors and acceptors, ring count, rotatable bonds, and chiral centers. MolMiner uses symmetry-aware fragment attachments and dynamically updates 3D geometry during generation using force fields. The authors propose improved benchmarking methods for both unconditional and conditional generation, including distributional comparisons via Wasserstein distance and calibration plots for property control.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

- The paper introduces a novel fragment-based, geometry-aware, and order-agnostic autoregressive model for molecular design that supports conditional generation of molecules over twelve properties. 
- MolMiner uses symmetry-aware fragment attachments and dynamically updates 3D geometry during generation using force fields. 
- The authors propose improved benchmarking methods for both unconditional and conditional generation, including distributional comparisons via Wasserstein distance and calibration plots for property control.

### Weaknesses

#### Some Related Works


#### comment

 - The model is compared to a limited number of baselines, and the comparisons are not always comprehensive. For example, the authors only compare to HierVAE for unconditional generation and do not provide a direct comparison to other state-of-the-art models such as MoLeR.
- The model's performance in unconditional generation is not as strong as HierVAE, and the authors acknowledge that it underperforms in some properties, particularly molecular weight, MR, and TPSA. The lack of a clear advantage in unconditional generation raises questions about the model's overall effectiveness, especially given the complexity introduced by the fragment-based approach and dynamic geometry updates.
- The model's performance on QED during conditional generation is not as good as other models, and the authors note that the control accuracy degrades for this property. This suggests that the model may have limitations in its ability to accurately control certain molecular properties, particularly those that are highly sensitive to subtle structural changes.

### Suggestions

The paper would benefit from a more thorough comparison to state-of-the-art models, particularly in the context of unconditional generation. While the authors justify their choice of HierVAE as a baseline, a comparison to other relevant models like MoLeR, even if it requires adapting the evaluation protocol, would provide a more complete picture of the model's strengths and weaknesses. Specifically, the authors could explore methods to evaluate MoLeR's ability to generate molecules with specific properties, even if it requires a more indirect approach than the direct conditioning used in MolMiner. This would help to contextualize the performance of MolMiner relative to the broader landscape of molecular generation models. Furthermore, the authors should investigate the reasons behind the underperformance in unconditional generation, particularly in molecular weight, MR, and TPSA. A more detailed analysis of the training data and the model's learning dynamics could reveal potential biases or limitations in the current approach. It would also be beneficial to explore alternative training strategies or model architectures that could improve the unconditional generation performance, potentially by incorporating techniques from other generative models that have shown success in this area. 

To address the limitations in conditional generation, particularly for QED, the authors should investigate the specific factors that contribute to the degradation in control accuracy. This could involve a more detailed analysis of the model's predictions and the relationship between the input conditions and the generated molecules. It would be helpful to explore whether the model is struggling with specific types of structural changes that are necessary to achieve the desired QED values. Furthermore, the authors could consider incorporating additional constraints or regularization terms into the training objective to improve the model's ability to accurately control molecular properties. This could involve techniques such as adversarial training or reinforcement learning, which have been shown to be effective in improving the control accuracy of generative models. The authors should also consider the impact of the fragment-based approach on the model's ability to generate molecules with specific properties. While the fragment-based approach offers several advantages, it may also introduce limitations in terms of the model's ability to explore the full space of possible molecular structures. A more detailed analysis of the fragment vocabulary and the model's fragment selection process could reveal potential bottlenecks or areas for improvement.

Finally, the authors should provide a more detailed discussion of the limitations of the current approach and potential avenues for future research. This could include a discussion of the challenges associated with generating molecules with specific 3D structures or properties that are not well-represented in the training data. It would also be helpful to explore the potential for incorporating additional types of information into the model, such as experimental data or quantum mechanical calculations. The authors should also consider the computational cost of the current approach and explore potential methods for improving the efficiency of the model. This could involve techniques such as model compression or parallelization. By addressing these limitations and exploring potential avenues for future research, the authors can provide a more complete and nuanced picture of the model's capabilities and limitations.

### Questions

- The paper mentions that the model is optimized for conditional generation, but it would be useful to understand how the model performs in unconditional generation scenarios and whether it can be adapted for such tasks.
- The authors note that the model underperforms HierVAE in unconditional generation for some properties. It would be helpful to understand the reasons behind this underperformance and whether there are any potential solutions to address this issue.
- The paper mentions that the model's performance on QED during conditional generation is not as good as other models. It would be useful to understand why this is the case and whether there are any potential improvements that could be made to address this limitation.

### Rating

3

### Confidence

4

**********