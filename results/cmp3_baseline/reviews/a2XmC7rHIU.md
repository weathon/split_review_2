## Summary

The paper introduces the Open Proof Corpus (OPC), a dataset of over 5,000 human-evaluated LLM-generated proofs on competition mathematics problems, covering problems from the IMO, USAMO, Putnam, and other sources. Using this dataset, the authors empirically address three open questions: the gap between natural-language and formal proof generation, the misalignment between final-answer accuracy and full proof correctness, and the effectiveness of best-of-n selection strategies. They further fine-tune an 8B parameter model on the OPC to achieve strong proof-judging accuracy (88.1%), close to the best proprietary models.

## Strengths

- **Large-scale, human-validated dataset for proof evaluation.** The OPC with 5,062 proofs across 1,010 problems fills a clear gap in the community. The annotation pipeline (double grading, pilot phase, uncertainty flags, coordinator oversight) is rigorous, and the inter-judge agreement of 90.4% indicates reliable labels.
- **Empirical resolution of important open questions.** The paper provides concrete numbers for the gap between formal and informal proof generation (informal solves ~4x more problems on PutnamBench), the drop from final-answer accuracy to proof correctness (up to 30% for o3), and the benefit of best-of-n strategies (ranking methods improve accuracy by 17% over pass@1). These findings are well-motivated and quantitatively supported.
- **Demonstrated utility through fine-tuning.** Training R1-QWEN3-8B on the OPC yields a model that matches Gemini-2.5-PRO and approaches GPT-5 on proof judging, showcasing the dataset's direct value for building better proof evaluators.
- **Open-source release and clear documentation.** The dataset is open-sourced, and the paper provides detailed methodology, problem sourcing, and split definitions, enabling reproducibility and downstream use.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Best-of-n analysis is limited in scope.** The experiments use only one model (O4-MINI) and a relatively small set of problems (60 fully judged, 134 total). The strong conclusions about ranking strategies would be more convincing with additional models and larger problem samples.
- **Comparison between formal and informal proof generation is not fully controlled.** The best formal model used for comparison (Goedel-Prover-V2) is not the state-of-the-art; the paper notes a private agentic system (Seed-Prover) achieves 50% on PutnamBench, which would reduce the claimed gap. While the conclusion that informal currently dominates is still valid, the "4x more" framing may overstate the advantage.
- **Fine-tuned judge evaluation may be inflated by distribution overlap.** The test set for the judge model is drawn from the same distribution as the training set. The paper addresses this with an out-of-distribution experiment in the appendix, but the main text's accuracy claims without caveat could give a slightly misleading impression of generalization.

### Trivial

None.

## Nice-to-Haves

- Extend best-of-n experiments to other models (e.g., Gemini, o3) and larger n values to confirm the pattern.
- Provide an out-of-distribution benchmark for the fine-tuned judge in the main results.
- Release the trained OPC-R1-8B model weights to maximize community impact.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- In the informal vs formal comparison, report the Seed-Prover result alongside the Goedel-Prover-V2 baseline and adjust the claim accordingly.
- For the best-of-n section, clearly state the small problem count and discuss the implications for statistical significance.
- When reporting judge accuracy, include a short statement about the in-distribution test set limitation and refer to the appendix for out-of-distribution results.

## Score and Decision

The OPC is a significant and well-curated resource that directly supports progress in LLM proof generation and evaluation. The three empirical studies are sound and provide valuable quantitative insights. Minor limitations do not undermine the core contributions. The paper is clearly written and will be useful to the community.

MY FINAL SCORE: <score>7.5</score>  
MY FINAL DECISION: Accept