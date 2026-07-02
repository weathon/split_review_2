Summary of the Paper:

This paper proposes Knowledge-in-Context (KiC), a novel semi-parametric language model architecture that combines a parametric text-to-text model (e.g., T5) with a knowledge-rich external memory.

The external memory encompasses six knowledge categories: entity, dictionary, commonsense, event, script, and causality.

KiC employs a knowledge selector to dynamically choose the most relevant knowledge type for each input instance, augmenting the input with retrieved knowledge pieces before feeding it to the text-to-text model for answer generation.

The paper argues that KiC can be viewed as a special mixture-of-experts (MoE) model, enabling the development of a novel differentiable learning algorithm for training the knowledge selector.

Experiments demonstrate that KiC outperforms much larger fully-parametric models on a variety of tasks, exhibiting emergent abilities at a smaller scale.

Strengths and Weaknesses:

Strengths:

Novel architecture: KiC introduces a unique approach to integrating diverse knowledge sources into a semi-parametric language model framework.

Adaptive knowledge selection: The instance-dependent knowledge selection mechanism allows KiC to utilize the most relevant knowledge for each specific input.

Strong empirical results: KiC outperforms significantly larger fully-parametric models on a wide range of tasks, demonstrating its effectiveness and efficiency.

Emergent abilities: KiC exhibits emergent abilities at a smaller model scale compared to fully-parametric models, suggesting superior knowledge utilization.

Clear and well-written paper: The paper presents the KiC architecture and learning algorithm in a clear and well-organized manner.

Weaknesses:

Limited analysis of knowledge quality: The paper lacks quantitative and qualitative analysis to assess the quality of the retrieved knowledge pieces.

Missing baselines: The paper does not compare KiC with a baseline that uses few-shot examples to generate augmentation data, making it difficult to fully gauge the performance gains attributable to the proposed approach.

Applicability to large PLMs: The current implementation of KiC may not be readily scalable to large PLMs due to computational constraints.

Limited task types: The experiments primarily focus on classification tasks, leaving the performance of KiC on other NLP tasks (e.g., question answering) unexplored.

Clarity, Quality, Novelty, and Reproducibility:

Clarity: The paper is well-written and easy to follow.

Quality: The research is well-designed and executed, with comprehensive experiments and detailed analysis.

Novelty: KiC presents a novel approach to semi-parametric language modeling with its adaptive knowledge selection and diverse knowledge sources.

Reproducibility: The paper provides code in the supplementary materials, facilitating reproducibility.

Additional Questions for Authors:

Can you provide more details on the quantitative and qualitative analysis of the retrieved knowledge pieces?

Have you considered comparing KiC with a baseline that uses few-shot examples for data augmentation?

How can KiC be scaled to larger PLMs, addressing the computational constraints?

Do you plan to explore the performance of KiC on other NLP tasks beyond classification?

Overall, this paper presents a valuable contribution to the field of NLP, and KiC is a promising approach to semi-parametric language modeling with its adaptive knowledge selection and diverse knowledge sources.

Addressing the weaknesses and exploring the additional questions will further strengthen the work and broaden its impact.

Summary of the Review:

KiC is a promising semi-parametric language model architecture that effectively leverages diverse knowledge sources to achieve strong performance on a variety of tasks.

However, further analysis is needed to assess the quality of the retrieved knowledge and the scalability of the approach to larger PLMs.

Additionally, exploring the performance of KiC on a wider range of NLP tasks would provide a more comprehensive understanding of its capabilities.