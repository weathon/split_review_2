## Summary

The paper introduces the *Open Proof Corpus* (OPC), a large-scale, human-validated dataset of over 5,000 LLM-generated mathematical proofs across more than 1,000 problems from prestigious competitions. Using this dataset, the authors address three open questions: (1) the gap between natural language and formal proof generation, (2) the relationship between final-answer accuracy and full proof correctness, and (3) the effectiveness of best-of-*n* selection strategies. They also fine-tune an 8B-parameter model on the OPC to achieve 88.1% accuracy in judging proof correctness, matching GEMINI-2.5-PRO and approaching GPT-5.

## Strengths

- **Large-scale, high-quality human annotation**: The dataset contains 5,062 proofs with binary human judgments, 10% double-graded with 90.4% inter-judge agreement, and includes detailed grading guidelines and quality control. This is a significant resource for the community.
- **Addresses important open questions**: The paper provides clear, empirical answers to three under-explored questions: (a) informal proofs dramatically outperform formal ones (4× on PutnamBench), (b) final-answer accuracy is a poor proxy for proof correctness (o3 drops 30% when requiring proof), and (c) ranking-based best-of-*n* selection substantially outperforms discrete/continuous methods.
- **Demonstrates practical utility**: Fine-tuning an 8B model on the OPC yields a proof judge that matches GEMINI-2.5-PRO (88.1% accuracy), showing the dataset’s value for training and suggesting that open-source models can compete with frontier closed models on proof evaluation.
- **Rigorous methodology**: The pipeline includes problem and judge preparation, pilot phase, monitoring, double-grading, and LLM-issue summaries (verified not to bias judges). The design is thoughtful and reproducible.

## Weaknesses

### Major

None.

### Minor

- **Limited scope of mathematical domains**: The dataset is dominated by high-school level competition problems (≈84%), with only a small fraction from undergraduate-level competitions. This limits the generality of conclusions about LLM proof-generation capabilities, particularly for research-level mathematics. The authors acknowledge this limitation.
- **Formal vs. informal comparison uses a potentially weak formal baseline**: The best formal model reported (Goedel-Prover-V2) achieves <19% on PutnamBench, but a private agentic system (Seed-Prover) reportedly achieves 50%. The paper notes this but does not fully address whether the gap is as large as claimed when using state-of-the-art formal systems. The conclusion that informal solves “4× more” may be overstated.
- **Best-of-*n* experiments are on a small sample**: The full evaluation with all eight human-judged proofs is only on 60 problems, and the larger subset is 134 problems. While the relative comparisons are valid, the absolute performance numbers have wide confidence intervals, and the findings would benefit from larger-scale validation.
- **Fine-tuning evaluation distribution overlap**: The test set for OPC-R1-8B shares the same distribution as the training set. The authors address this with an out-of-distribution experiment in the appendix, but the main paper does not fully discuss the potential inflation of performance, and the appendix is not included in the review.
- **Human baseline comparison is slightly mismatched**: The human inter-judge agreement (90.4%) is measured on all double-graded proofs, while the LLM judging accuracy is measured on a specific test subset. The authors argue this is not significant, but a direct comparison on the same subset would be cleaner.

### Trivial

- Inconsistent naming: The model is referred to as “GEMINI-PRO” in Table 1 and “GEMINI-2.5-PRO” in the text and figures. This is a minor inconsistency.

## Nice-to-Haves

- **Release the dataset and code**: The paper states the dataset is open-sourced, but no link or repository is provided. Making the dataset and fine-tuned model publicly available would greatly increase the impact.
- **Extend to more advanced domains**: Including problems from research-level mathematics or more diverse topics would strengthen the generality of the conclusions.
- **Include more recent models**: The dataset was constructed before GROK-4 and GPT-5, so these models are only evaluated as judges. Including them as provers in future iterations would be valuable.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Provide a clear public release plan for the dataset, including a link to the repository and the fine-tuned model weights.
- In the formal vs. informal comparison, include a more detailed discussion of the state-of-the-art in formal proof generation and acknowledge that the “4×” claim may be sensitive to the choice of formal benchmark and system.
- Increase the size of the best-of-*n* subset with human judgments for all *n* to reduce confidence intervals and strengthen the conclusions about ranking methods.
- Report the out-of-distribution evaluation results for the fine-tuned judge model in the main paper to give readers a more complete picture of its generalization.

## Score and Decision

Score: 8  
Decision: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>