Summary of the Paper:

The paper presents a method for out-of-distribution (OOD) detection and selective generation for conditional language models (CLMs), focusing on improving the safety and reliability of CLMs in practical applications like abstractive summarization and translation.

By identifying and abstaining from low-quality, OOD examples, the method enables CLMs to produce higher-quality outputs.

The approach uses embeddings from CLMs to accurately detect OOD examples and combines perplexity scores with a newly introduced OOD score for selective generation.

This combination allows for the adjustment of output quality based on the distributional shift of the input,  demonstrating significant improvement over baseline methods in both summarization and translation tasks.

Strengths and Weaknesses:

Strengths:

The methodology introduces a practical and effective solution for OOD detection in CLMs without requiring a separate detection model.

The paper provides a comprehensive evaluation framework that includes human quality ratings, addressing a critical need in the community.

The combined use of perplexity and the novel OOD score for selective generation is innovative and demonstrates a significant improvement over existing methods.

Weaknesses:

The approach's dependency on specific embeddings and the potential for its performance to vary across different models or tasks is not extensively discussed.

While the method shows improvements, the real-world applicability and scalability of the proposed solution could be further explored, particularly in more diverse or adversarial settings.

Clarity, Quality, Novelity, and Reproducibility:

The paper is well-written, presenting a clear and logical progression of ideas.

The research is of high quality, leveraging both theoretical insights and empirical evaluations.

The novelty of the approach lies in its effective combination of perplexity scores and OOD detection for improving CLM outputs.

The provided details and evaluation framework contribute to the paper's reproducibility, although additional information on the implementation and potential limitations would further enhance it.

Summary of the Review:

This paper introduces an innovative method for enhancing the safety and reliability of conditional language models through OOD detection and selective generation.

It addresses a critical gap in the field, providing both theoretical contributions and practical improvements.

Despite some areas for further exploration, the paper's strengths in novelty, methodological clarity, and potential impact make a compelling case for its acceptance.