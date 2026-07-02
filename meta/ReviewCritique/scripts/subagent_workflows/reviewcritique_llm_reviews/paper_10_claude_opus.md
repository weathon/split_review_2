Summary of the Paper:

This paper proposes a novel semi-parametric language model architecture called Knowledge-in-Context (KiC) that augments a parametric text-to-text language model with an external memory containing six different types of knowledge: entity, dictionary, commonsense, event, script, and causality knowledge.

For each input instance, the KiC model adaptively selects the most helpful knowledge type and retrieves the most relevant knowledge pieces.

The knowledge-augmented input is then fed into a text-to-text model like T5 to generate the output.

The authors find that KiC can be formulated as a special mixture-of-experts (MoE) model, where the knowledge selector acts as the router to determine the input-to-expert assignment, inspiring a novel end-to-end learning algorithm.

Experiments on over 40 tasks show that KiC Large with 770M parameters outperforms much larger language models by a large margin in zero-shot settings.

KiC also exhibits emergent abilities at a much smaller scale compared to fully-parametric models.

Strengths and Weaknesses:

Strengths:

- The KiC architecture that augments a parametric LM with a knowledge-rich external memory containing multiple knowledge types is novel and well-motivated.

- Formulating KiC as a special MoE model is an interesting observation that enables fully differentiable end-to-end learning of the model.

- The comprehensive experiments on over 40 tasks demonstrate the effectiveness of KiC in achieving superior zero-shot performance with much fewer parameters compared to large language models.

- Analysis on the usefulness of different knowledge types for different tasks provides good insights.

Weaknesses:

- More details can be provided on the prompting and knowledge selection/retrieval process with concrete examples to improve clarity.

- Ablation studies on the impact of different knowledge types and the knowledge selector would strengthen the paper.

- Some more discussion on the limitations and potential negative impacts of the model is recommended.

Clarity, Quality, Novelty and Reproducibility:

The paper is overall clearly written with good organization.

The proposed KiC model is novel and the comprehensive experiments demonstrate the high quality of the work.

Key implementation details are provided, though some more specifics on the prompting and knowledge selection would further aid reproducibility.

The authors state that code will be released.

Summary of the Review:

This paper presents Knowledge-in-Context (KiC), a novel semi-parametric language model architecture that effectively incorporates multiple types of knowledge from an external memory to achieve impressive zero-shot performance across many tasks with a relatively small number of parameters.

The MoE-based formulation of KiC that enables end-to-end learning is innovative.

The extensive experiments and analyses provide strong support for the proposed approach.

Some added details on the methodology and discussion on limitations would further strengthen the paper.

Overall, this is a high-quality paper that makes valuable contributions to the field.