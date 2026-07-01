## Summary

This paper investigates how three compression methods—quantization, distillation, and pruning—affect the reasoning capabilities of large reasoning models (LRMs). The authors benchmark compressed variants of DeepSeek-R1 on four reasoning datasets and apply mechanistic interpretability techniques (difference of means and attribution patching) to locate which weights are most important for reasoning. Key findings: (1) weight count impacts knowledge memorization more than reasoning, making pruning and distillation risky for knowledge-intensive tasks; (2) the MLP up\_proj in the final layer of distilled LRMs is one of the most critical components; (3) current quantization methods overly compress final-layer modules and MLP gate projections, and protecting only ~2% of weights can boost accuracy by 6.57%.

## Strengths

- **Comprehensive scope**: The paper systematically studies three major compression paradigms (quantization, distillation, pruning) on LRMs, which is underexplored in existing literature.
- **Mechanistic interpretability**: The adaptation of steering vectors and attribution patching to quantify fine-grained weight importance in compressed models is a novel and principled approach that goes beyond layer-level analyses.
- **Actionable findings**: The identification of the final-layer up\_proj as critical and the demonstration that a simple selective protection scheme improves 3-bit quantization by up to 23.17% provide clear guidance for future compression research.
- **Empirical validation**: The validation experiments (selective quantization of single components in Table 3 and selective protection in Table 4) directly support the conclusions about weight importance and quantization bottlenecks.

## Weaknesses

### Fatal
None.

### Major
1. **Reliance on GPT-4o behavior annotation**: The entire interpretability pipeline hinges on GPT-4o labeling token sequences for reasoning behaviors (backtracking, uncertainty estimation, example testing, adding knowledge). Validation of this annotation is deferred to Appendix G. Without robust evidence that these automatic annotations are accurate, the computed steering vectors and importance scores may reflect spurious patterns rather than genuine reasoning behaviors.
2. **Unvalidated attribution patching approximation**: The importance scores are computed as the absolute dot product of the steering vector with gradients of the cross-entropy loss on behavior token sequences. The paper does not assess the numerical stability, sensitivity to input selection, or convergence of this approximation, nor does it compare against alternative attribution methods (e.g., activation patching, integrated gradients) to confirm reliability.
3. **Asymmetric treatment of importance shifts**: The analysis only visualizes decreases in relative importance (setting increases to zero) based on the assumption that decreases are more informative. This discards information about cases where compression actually enhances a weight’s relative importance, and the justification (deferred to Appendix H) may not fully justify this asymmetric approach given that relative importance is zero-sum.
4. **Inconsistency in validation of importance scores**: In Table 3, the lowest-ranked component (1\_up) causes the largest accuracy drop on AIME 2024 (6.7%), which contradicts the ranking predicted by importance scores. This indicates that the importance scores may not reliably capture cross-layer differences, weakening the claim that the final-layer up\_proj is uniquely critical.
5. **Limitations of selective protection experiment**: The protection mechanism in Table 4 only retains 2% of weights in full precision—a trivial approach that is not a practical compression solution. The claim of “surpassing the state-of-the-art” is overstated because a complete quantization pipeline would need to handle those weights differently. Moreover, the experiment is only run on a single 8B model, leaving scalability to larger LRMs unverified.
6. **Causal inference for finding 1**: The claim that parameter count affects knowledge more than reasoning is based on correlational observations (e.g., Qwen 32B lower MuSiQue than Llama 70B despite better reasoning). Confounding factors such as architecture differences, training data, and distillation setup are not controlled, so the causal conclusion is not rigorously established.

### Minor
- Some notation is inconsistent (e.g., RI^c_mle in Figure 3 caption vs. RI^c_ml elsewhere).
- Experimental details such as calibration data choices for quantization methods and exact implementation of AlphaPruning on LRMs are omitted from the main text.
- The analysis focuses predominantly on R1-distilled models; generalization to non-R1 families is claimed but only discussed in an appendix.

### Trivial
None.

## Nice-to-Haves
- Provide a summary of the GPT-4o annotation validation (e.g., agreement with human raters or performance on held-out examples) in the main paper.
- Include ablation studies that compare the proposed attribution-based importance scores with simpler baselines (e.g., weight magnitude, activation range) to demonstrate added value.
- Test the selective protection strategy on larger distilled models (32B, 70B) to show that the findings scale.

## Novel Insights
The paper offers a fine-grained causal analysis of which weights matter most for reasoning in compressed LRMs. The identification of the final-layer MLP up\_proj as disproportionately critical, and the discovery that current quantization methods systematically over-compress gate projections and final-layer modules, are concrete and actionable insights that can directly guide future compression research. The combination of performance benchmarking with mechanistic interpretability provides a template for understanding compression effects beyond simple accuracy metrics.

## Suggestions
- Clearly report the results of GPT-4o annotation validation in the main paper or, if space is limited, present a concise summary of inter-rater reliability or accuracy against human-labeled data.
- Perform stability tests for the importance scores (e.g., repeat with different random seeds for gradient computation, or compare against a null distribution from shuffled steering vectors).
- Run selective protection on at least one larger model (32B or 70B) to confirm that the 6.57% improvement generalizes.

## Score and Decision

**Score**: 6.0

**Decision**: Accept

The paper addresses an important and timely research question with a well-structured combination of benchmarking and interpretability. Its findings are novel and have clear practical implications for improving LRM compression. However, the validity of the interpretability pipeline is hampered by reliance on unvalidated GPT-4o annotations and an untested attribution approximation, and some experimental choices (asymmetric shift visualization, limited scale of validation) prevent full confidence in the conclusions. These concerns are addressable, and the core contribution is strong enough to warrant acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>