Summary of the Paper:

This paper proposes a lightweight and effective out-of-distribution (OOD) detection method for conditional language models (CLMs) such as those used in abstractive summarization and translation.

The authors show that model perplexity is not well-suited for OOD detection and instead propose using the input and output embeddings of the CLM itself to compute OOD scores, without requiring a separate detection model.

The OOD score is based on the Mahalanobis distance (MD) to Gaussians fit on the training embeddings, and an extension called Relative Mahalanobis Distance (RMD) which incorporates a background Gaussian.

A binary classifier using the embeddings as features is also evaluated.

Experiments demonstrate the proposed OOD scores significantly outperform perplexity and other baselines for detecting OOD examples.

Furthermore, the authors show that while perplexity is a reasonable quality predictor for in-distribution examples, combining it with the proposed OOD scores enables much better selective generation when the input distribution is shifted, abstaining on low-quality outputs while generating the rest.

Strengths and Weaknesses:

Strengths:

The proposed OOD scores are simple, lightweight and do not require training a separate detection model, making them very practical.

Extensive experiments on both summarization and translation tasks demonstrate the effectiveness of the proposed approach, significantly outperforming baselines.

Analysis showing perplexity has reduced correlation with output quality on OOD data is insightful and highlights the need for better selective generation under distributional shift.

Combining perplexity with OOD scores to enable selective generation on shifted data is a key contribution with high practical value for safer deployment of language models.

Weaknesses:

The Gaussian fitting and Mahalanobis distance computations could become expensive for very high-dimensional embeddings.

Computational cost and scalability could be discussed.

Analysis of selective generation focuses on abstention rate, but it would be interesting to see the coverage vs quality trade-off, i.e.

what % of examples can be generated while maintaining a specified quality bar.

Experiments cover a good range of domains but are limited to summarization and translation.

Generalization to other language tasks could be discussed.

Clarity, Quality, Novelty, and Reproducibility:

The paper is clearly written and easy to follow.

The methodology is explained in detail, including algorithms for fitting the Gaussians and computing OOD scores.

Assumptions made are stated upfront.

The experimental setup is comprehensive, covering multiple datasets of varying shift from the training data.

Results are extensive and include both automatic and human evaluation.

Key strengths and weaknesses of the method are analyzed.

The approach of using the CLM's own embeddings for OOD detection without a separate model is quite novel, as is the extension of selective prediction to language generation under distribution shift.

The authors plan to release code which would aid reproducibility.

Hyperparameters are provided to reproduce the binary classifiers.

Details on hardware requirements and runtimes could further improve reproducibility.

Summary of the Review:

This paper makes valuable contributions to OOD detection and selective generation for conditional language models under distributional shift.

The proposed OOD scores are highly effective while being simple and lightweight.

Experiments are extensive and results are promising.

The key weakness is the lack of discussion on computational efficiency.

But overall, this is a strong paper that would be of interest to the NLP community and spur further work in this important direction.