### Summary

This paper introduces a new benchmark designed to evaluate the compositional generalization capabilities of machine learning force fields (MLFFs). The benchmark consists of four tasks, each designed to assess a specific type of generalization: length extrapolation, functional group composition, functional group duplication, and functional group combination. The authors evaluate several state-of-the-art MLFFs on this benchmark and find that these models exhibit significant performance degradation when generalizing to out-of-distribution (OOD) data.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses an important and under-explored problem in the field of MLFFs, namely compositional generalization. This is a critical issue for the practical application of MLFFs in molecular discovery and materials science.

2. The benchmark is well-designed and systematically evaluates different aspects of compositional generalization. The four tasks cover a range of challenges, from length extrapolation to functional group composition and duplication.

3. The experimental results are comprehensive and provide valuable insights into the limitations of current MLFFs. The authors evaluate several popular models and show that they struggle to generalize to OOD data, highlighting the need for more robust models.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion of the limitations of the proposed benchmark. For example, the benchmark focuses on relatively simple molecules and functional groups. It is unclear how well the findings generalize to more complex systems, such as large biomolecules or materials with periodic structures. The benchmark's scope is limited to small organic molecules, and it does not address the challenges of applying MLFFs to systems with more complex bonding environments, such as those found in inorganic materials or large biomacromolecules with intricate secondary structures. The current benchmark does not explore the generalization capabilities of MLFFs on systems with varying charge states or protonation levels, which are crucial for modeling biological systems.

2. The paper does not provide a thorough analysis of the reasons behind the poor generalization performance of the evaluated models. While the results show that current models struggle with compositional generalization, the authors do not delve deeply into the underlying causes. For instance, it is unclear whether the poor performance is due to the models' inability to capture long-range interactions, their lack of physical inductive biases, or other factors. The analysis lacks a detailed investigation into the specific architectural limitations of the models, such as the receptive field of the neural networks or the ability of the models to capture the underlying physics of interatomic interactions. A more detailed analysis of the model's learned representations could provide insights into the failure modes.

### Suggestions

The authors should consider expanding the benchmark to include more complex molecular systems, such as proteins, nucleic acids, and inorganic materials. This would involve generating datasets with diverse chemical compositions, structural motifs, and bonding environments. For example, the benchmark could include proteins with varying secondary structure content, such as alpha-helices and beta-sheets, or inorganic materials with different crystal structures and bonding types. Furthermore, the benchmark should incorporate systems with varying charge states and protonation levels to assess the models' ability to handle different chemical environments. This would provide a more comprehensive evaluation of the generalization capabilities of MLFFs and better reflect the challenges of real-world applications. The inclusion of periodic systems, such as crystal structures, would also be valuable to assess the models' ability to handle long-range interactions and periodic boundary conditions.

To better understand the reasons behind the poor generalization performance, the authors should conduct a more detailed analysis of the model's learned representations. This could involve visualizing the feature maps of the neural networks or analyzing the sensitivity of the models to different types of structural variations. For example, the authors could investigate whether the models are overly sensitive to the presence of specific functional groups or whether they struggle to capture the long-range interactions between different parts of the molecule. Furthermore, the authors should explore the impact of different architectural choices on the generalization performance. This could involve comparing the performance of different types of neural networks, such as graph neural networks and transformers, or investigating the effect of different regularization techniques. A more detailed analysis of the model's failure modes would provide valuable insights into the limitations of current MLFFs and guide the development of more robust models.

Finally, the authors should consider incorporating more physically-informed architectures or training strategies to improve the generalization performance of MLFFs. This could involve incorporating symmetry constraints into the model architecture or using physics-based loss functions. For example, the authors could explore the use of equivariant neural networks, which are designed to respect the symmetries of the physical system, or incorporate a loss function that penalizes deviations from known physical laws. Furthermore, the authors could explore the use of transfer learning techniques to leverage knowledge from related tasks or datasets. By incorporating more physically-informed approaches, the authors could develop more robust and generalizable MLFFs that are better suited for real-world applications.

### Questions

1. How do the authors plan to address the limitations of the benchmark in future work? Are there plans to extend the benchmark to more complex molecular systems or different types of chemical tasks?

2. Can the authors provide more insights into the reasons behind the poor generalization performance of the evaluated models? Are there specific architectural limitations or training strategies that contribute to this issue?

3. How do the authors plan to encourage the development of more robust and generalizable MLFFs? Are there specific recommendations or guidelines for future research in this area?

### Rating

6

### Confidence

3

**********