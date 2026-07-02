### Summary

The authors proposed a novel method to simplify the generation diffusion space by splitting the molecules into rigid fragments. The experimental results show the effectiveness of this approach.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed method is well-motivated and reasonable.
2. The experimental results are good.

### Weaknesses

#### Some Related Works


#### comment

1. The presentation of the paper needs to be improved. The introduction part should include more related work rather than just a few references. The authors should comprehensively discuss the existing methods and highlight the limitations of existing methods, which are solved in this work. Specifically, the introduction should delve into the details of current diffusion-based molecular docking methods, explaining their shortcomings in terms of computational cost, generalizability, and the quality of generated poses. A more thorough discussion of the specific challenges in the field would better contextualize the authors' contribution.
2. The proposed method is well-motivated. However, some parts are not clearly explained. For example, in the Fragmentation Scheme section, the authors introduce the irreducible fragments and the reduced DoFs. The authors should provide more explanations on the reduced DoFs. It is unclear how the merging of fragments leads to a reduction in degrees of freedom and how this impacts the overall diffusion process. A more detailed explanation of the mathematical formulation of the reduced DoFs and their relation to the fragment graph is needed.
3. The proposed method is quite complex. The proposed method includes many modules, such as the fragmentation scheme, soft triangulation constraints, and SO(3)-equivariant architecture. The authors should provide more details and deep analyses of the proposed method. For instance, the interaction between these modules and their individual contributions to the final performance should be analyzed. The paper lacks a detailed ablation study that would clarify the necessity of each component.
4. The authors should also include more ablation studies to validate the effectiveness of the proposed modules. For example, the effectiveness of the SO(3)-equivariant architecture. The authors should provide more quantitative and qualitative analyses. The ablation study should include a comparison of different architectures, not just the presence or absence of the SO(3)-equivariant one. Furthermore, the qualitative analysis should include visualizations of the generated poses and their comparison to the ground truth.

### Suggestions

The introduction should be significantly expanded to include a more detailed discussion of existing molecular docking methods, particularly those using diffusion models. The authors should not only cite these methods but also provide a critical analysis of their limitations. For example, they should discuss the computational challenges associated with high-dimensional diffusion spaces, the difficulties in generalizing to new molecules or protein targets, and the tendency of some methods to generate physically implausible poses. This discussion should explicitly highlight the specific problems that the proposed method aims to solve, thereby providing a clear motivation for the work. The introduction should also include a more detailed explanation of the conformational manifold and its importance in molecular docking, as well as the limitations of existing methods in capturing this manifold accurately.

To address the lack of clarity in the fragmentation scheme, the authors should provide a more detailed explanation of how the reduction in degrees of freedom (DoFs) is achieved. This should include a mathematical formulation of the DoFs before and after the merging of fragments, and a clear explanation of how the merging process affects the connectivity of the fragment graph. The authors should also explain how the soft triangulation constraints are implemented and how they help to preserve bond lengths and angles across fragments. A visual representation of the fragmentation process, showing how the fragments are merged and how the DoFs are reduced, would be beneficial. Furthermore, the authors should provide a more detailed explanation of the SO(3)-equivariant architecture, including the specific mathematical operations that ensure equivariance and how this property is beneficial for the task of molecular docking. The authors should also discuss the limitations of their fragmentation scheme, such as the potential for information loss during the merging process.

Finally, the authors should include a more comprehensive ablation study to validate the effectiveness of the proposed modules. This study should include a comparison of different architectures, not just the presence or absence of the SO(3)-equivariant one. The ablation study should also analyze the impact of different fragmentation strategies and the effect of the soft triangulation constraints. The authors should provide both quantitative and qualitative analyses of the ablation study results. For example, they should show how the performance of the model changes when different modules are removed or modified, and they should provide visualizations of the generated poses to illustrate the impact of these changes. The qualitative analysis should include a comparison of the generated poses with the ground truth poses, highlighting the strengths and weaknesses of the proposed method. The authors should also discuss the computational cost of each module and how it affects the overall efficiency of the method.

### Questions

Please refer to the weaknesses.

### Rating

6

### Confidence

3

**********