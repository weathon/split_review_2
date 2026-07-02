Summary of the Paper:

This paper proposes a novel recitation-augmented generation (RECITE) paradigm to improve language models' performance on closed-book question answering (CBQA) tasks.

RECITE first recites relevant passages from the language model's own memory via sampling before producing the final answers.

The authors show that utilizing recitation as an intermediate step in a recite-and-answer scheme can achieve state-of-the-art performance on various CBQA tasks.

They verify the effectiveness of RECITE on three pre-trained models (In-house LM, UL2, and OPT) and three CBQA datasets (Natural Questions, TriviaQA, and HotpotQA).

Fine-tuning the pre-trained LMs on synthetic question-passage pairs can further improve recitation and downstream QA accuracy.

Strengths and Weaknesses:

Strengths:

- Novel recitation-augmented generation paradigm for closed-book QA that improves performance by reciting relevant passages from the LM's memory before answering.

- Experiments on multiple LMs and CBQA datasets demonstrate broad effectiveness of the approach.

- Additional fine-tuning on synthetic data further improves recitation and QA performance.

- Analysis of number of recitations, robustness to few-shot exemplars, and comparison to retrieval provides useful insights.

Weaknesses:

- Lacks comparisons to very recent state-of-the-art CBQA methods to contextualize the results.

- Evaluation is limited to CBQA datasets; broader applicability to other knowledge-intensive NLP tasks is not explored.

- Updating the LM's knowledge requires costly re-training/fine-tuning, limiting flexibility compared to retrieval-augmented methods.

- Some key implementation details are missing, such as specifics of the synthetic data generation process.

Clarity, Quality, Novelty and Reproducibility:

The paper is generally well-written and easy to follow.

The proposed recitation-augmented generation approach is novel and the extensive experiments demonstrate the effectiveness and robustness of the method.

Key details are provided to understand the methodology.

However, some specifics are lacking that would be needed to fully reproduce the results, such as details on the synthetic data generation process for fine-tuning.

The overall quality of the research appears high, though comparisons to very recent state-of-the-art CBQA methods are missing to fully contextualize the significance of the results.

Summary of the Review:

This paper presents a novel and effective recitation-augmented generation approach for closed-book question answering with large language models.

Experiments on multiple models and datasets provide convincing evidence of the benefits of the recite-and-answer paradigm.

The analysis of various aspects of the method offers useful insights.

Some weaknesses include the lack of comparisons to recent SOTA methods and full reproducibility details.

Overall, this work makes a valuable contribution to improving CBQA with language models, though further work is needed to explore broader applicability and knowledge updating.