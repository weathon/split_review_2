Summary of the Paper:

This paper investigates the use of language as a proxy for human similarity judgments, which are valuable for various machine learning applications but expensive to collect at scale.

The authors compare several approaches, including using pre-trained deep neural networks (DNNs), large language models (LLMs) applied to textual descriptions, and hybrid "stacked" methods combining both.

They also introduce STEP-Tag, a novel adaptive pipeline for collecting high-quality word tags.

Evaluating these methods across image, audio, and video datasets, the authors find that stacked representations best approximate human similarity, followed by text-based methods and then DNNs.

They conclude by providing a guide for researchers to choose the most suitable method for their specific needs and resource constraints.

Strengths and Weaknesses:

Strengths:

Comprehensive comparison: The paper provides a valuable and extensive comparison of different methods for approximating human similarity judgments, encompassing DNNs, LLMs, and hybrid approaches.

Novel methods: The proposed language-based methods, particularly the use of LLMs and STEP-Tag, offer efficient and modality-agnostic alternatives for approximating similarity, especially when pre-trained DNNs are unavailable.

Open data and code: Sharing the collected data and code promotes transparency and facilitates further research in this area.

Weaknesses:

Limited interpretability analysis: While interpretability is claimed as a key advantage of the proposed methods, the paper lacks a dedicated analysis to support this claim. Further investigation is needed to assess how interpretable the generated prompts and representations actually are.

Focus on relatively simple tasks: The experiments primarily focus on tasks with easily defined prompts, such as emotion recognition and activity recognition. Evaluating the methods on more complex NLP tasks would provide stronger evidence for their ability to generate and understand complex prompts.

Lack of comparison with recent prompting methods: The paper does not compare with some recent methods for finding better discrete prompts, which would be helpful to gauge the relative performance of the proposed methods.

Clarity, Quality, Novelty, and Reproducibility:

Clarity: The paper is generally well-written and clear, although some details about the experimental setup could be further clarified.

Quality: The research is well-designed and executed, with a comprehensive evaluation across different modalities and methods.

Novelty: The proposed language-based methods and the STEP-Tag pipeline are novel and offer valuable contributions to the field.

Reproducibility: The authors provide code and data, which facilitates the reproduction of their results.

Summary of the Review:

This paper presents a valuable contribution to the field of human similarity approximation.

The proposed language-based methods and the STEP-Tag pipeline offer promising alternatives for efficiently collecting and approximating similarity judgments, particularly in situations where pre-trained DNNs are unavailable.

However, further investigation is needed to assess the interpretability of the generated representations and the performance on more complex NLP tasks.