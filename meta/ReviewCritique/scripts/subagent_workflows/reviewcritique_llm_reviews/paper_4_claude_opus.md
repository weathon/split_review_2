Summary of the Paper:

This paper compares various methods for efficiently approximating human similarity judgments at scale.

The authors evaluate over 600 pre-trained deep neural network (DNN) models across images, audio, and video modalities to assess their alignment with human judgments.

They find a significant performance gap between these DNN methods and collecting exhaustive pairwise human judgments.

To address this, they propose novel methods for approximating similarity using natural language, either via large language models (LLMs) applied to stimulus descriptions or classical word frequency analysis (WFA) on tags/captions.

They also introduce a new adaptive tag collection pipeline called STEP-Tag.

The language-based methods significantly improve over the DNN methods while requiring only O(N) human judgments compared to O(N^2).

Combining the best DNN and language embeddings via "stacking" provides the closest approximations to human judgments overall.

Based on their results, the authors provide a best practices guide for collecting similarity data under different constraints.

Strengths and Weaknesses:

Strengths:

- Conducts the first large-scale, systematic evaluation of how well various DNN models approximate human similarity judgments across multiple modalities

- Introduces an adaptive tag collection paradigm (STEP-Tag) to obtain informative tags

- Compares unimodal, multimodal, and hybrid "stacked" approaches to integrating DNN and language information

- Synthesizes findings into a practical flowchart to guide researchers in collecting similarity data

Weaknesses:

- Evaluation is limited to three modalities (images, audio, video); extending to other domains like text or graphs would further demonstrate the generality of the language-based methods

- Additional analysis of what factors enable certain DNN architectures to better capture human similarity could provide further insights

- Discussion of potential risks (e.g.

encoding human biases) is quite brief

Clarity, Quality, Novelty, and Reproducibility:

The paper is clearly written and easy to follow.

The experiments are rigorous and comprehensive, evaluating a very large number of models and ablating key components of the proposed methods.

The language-based similarity approximation methods, especially the stacking approach, represent a novel contribution that significantly improves efficiency over prior work.

By open-sourcing their code and data, the authors have made their results fully reproducible.

Summary of the Review:

This paper makes valuable contributions to the important problem of efficiently collecting human similarity judgments at scale.

The systematic evaluation of DNN methods reveals their limitations, while the proposed language-based approaches, combined with the useful best practices guide, provide an effective and practical way forward.

Some additional evaluation, analysis and discussion of risks could further strengthen the work, but overall this is a significant and well-executed study.