Summary of the Paper:

This paper addresses the issue of out-of-distribution (OOD) detection and selective generation for conditional language models (CLMs).

CLMs, trained to predict the next token in a sequence, can suffer significant performance degradation and produce low-quality outputs when faced with OOD inputs.

The paper proposes lightweight and accurate OOD detection scores based on the model's input and output embeddings.

It further demonstrates how these scores, combined with perplexity, can be used for selective generation, enabling safer deployment of CLMs by abstaining from generating low-quality outputs on OOD examples.

The authors evaluate their methods on abstractive summarization and translation tasks, showing significant improvements over baseline approaches.

Strengths and Weaknesses:

Strengths:

Novelty: The proposed OOD detection scores based on input and output embeddings are novel and effective for CLMs.

Lightweight and Accurate: The methods require minimal additional computation and achieve high accuracy in OOD detection.

Selective Generation: Combining OOD scores with perplexity enables selective generation, allowing models to abstain from generating low-quality outputs on OOD examples.

Evaluation Framework: The paper proposes a comprehensive evaluation framework for OOD detection and selective generation in CLMs, including human evaluation for summarization quality.

Weaknesses:

Limited Task Modalities: While the methods are potentially applicable to other sequence-to-sequence tasks, the experiments are limited to summarization and translation. Model Architectures: The analysis focuses on encoder-decoder Transformers, and it is unclear how well the methods generalize to decoder-only architectures used by some large language models.

Clarity: Some aspects of the methodology, particularly the feature-based and deep ULF methods, could benefit from further elaboration and details.

Clarity, Quality, Novelty, and Reproducibility:

The paper is generally well-written and easy to follow.

The research is of high quality, with thorough experiments and analysis.

The proposed OOD detection scores and selective generation framework are novel and significant contributions.

The authors mention that code will be released, which will enhance reproducibility.

Summary of the Review:

This paper presents novel and effective methods for OOD detection and selective generation in CLMs.

The proposed OOD scores are lightweight, accurate, and enable safer deployment of CLMs by selectively generating high-quality outputs.

The research is well-conducted and the paper is well-written.

I recommend accepting this paper for publication.