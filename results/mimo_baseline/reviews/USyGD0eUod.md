## Summary

This paper systematically evaluates whether standard SAE quality metrics and auto-interpretability scoring pipelines can distinguish sparse autoencoders trained on trained versus randomly initialized Pythia transformers (70M–6.9B parameters). The central finding is that aggregate auto-interpretability scores (fuzzing and detection AUROC) are surprisingly similar between trained and randomized model variants, with only the noise-embedding control falling to chance—implying that these commonly used metrics are insufficient proof that SAEs have recovered genuinely learned, computationally relevant features.

## Strengths

- **Important and timely methodological critique.** The mechanistic interpretability community heavily relies on aggregate auto-interpretability scores to validate SAEs, yet this paper demonstrates convincingly—with multiple randomization schemes (Step-0, re-randomized with/without embeddings) and a proper control—that these metrics fail a basic sanity check. This finding has direct implications for how SAE quality is assessed across the field (Figures 1 and 2).

- **Thorough and systematic experimental design.** The paper covers five model sizes, multiple randomization variants, per-layer SAEs, and demonstrates robustness to SAE hyperparameters (expansion factor, sparsity). The inclusion of a Gaussian-embedding control that correctly drops to chance AUROC validates the experimental pipeline and strengthens the core negative result.

- **Proposes a constructive direction forward.** Rather than simply identifying a failure mode, the paper introduces token distribution entropy as a simple probe for feature "abstractness" and shows that it does differentiate trained from randomized models (last row of Figure 2). The toy model analysis in Section 4 offers plausible mechanistic hypotheses (preservation vs. amplification of superposition) that motivate future investigation.

- **Honest framing and careful scoping.** The authors are clear that they are not claiming SAEs fail to learn meaningful features—only that aggregate metrics cannot prove it. This distinction is important and well-communicated.

## Weaknesses

### Fatal

None.

### Major

- **Limited scope of models and datasets.** All experiments use the Pythia family and RedPajama. While the authors acknowledge this (Section 5), it limits generalizability claims. For instance, different architectures (e.g., Llama, Mistral) or data domains could exhibit different behavior. The core claim—that metrics fail to distinguish—needs replication across at least one or two additional model families to be fully convincing.

- **The entropy result is preliminary and not directly validated as a metric.** Token distribution entropy is introduced as a proof-of-concept for "abstractness," but it is never formally evaluated as a replacement or complement to existing metrics. Without showing that entropy-based filtering of latents leads to qualitatively better mechanistic explanations, its practical value remains speculative. The scatter plots in Appendix H are mentioned but not discussed in the main text in sufficient detail.

- **The causal mechanism remains unresolved.** The toy models in Section 4 provide two hypotheses (preservation vs. amplification of superposition) but explicitly defer determining which predominates in real transformers to future work. While this is understandable, the paper would be considerably stronger with even a simple empirical test (e.g., comparing the sparsity statistics of random transformer activations at different layers against the input data).

### Minor

- **Only 100 features sampled per SAE for auto-interpretability evaluation.** While this is computationally reasonable, it introduces sampling variance in AUROC estimates. The paper mentions multiple random seeds in Appendix E but does not quantify confidence intervals on the main figures, making it harder to assess the reliability of the closeness between trained and randomized AUROCs.

- **The $L^1$ norm behavior for Step-0 versus re-randomized variants is noted but not fully explained.** The authors speculate that parameter norm differences between initialization and trained states drive this gap, but this speculation could be partially tested by ablating individual weight matrix norms.

### Trivial

None.

## Nice-to-Haves

- A comparison on at least one non-Pythia architecture (even a small one like GPT-2) to strengthen generalizability.
- Statistical tests (e.g., permutation tests) quantifying whether the AUROC difference between trained and randomized variants is statistically significant, to add rigor to the "surprisingly similar" claim.
- A brief analysis of whether the high-AUROC random-variant latents correspond to qualitatively interpretable features or merely statistically detectable patterns.

## Novel Insights

The paper's most novel and potentially impactful observation is that the inductive biases of transformer architectures and the statistical structure of language data are sufficient to produce apparently interpretable SAE latents without any learning. This challenges the implicit assumption that high auto-interpretability scores reflect recovered learned computations. The proposed explanation—that neural networks preserve or amplify the superposed structure already present in natural data—offers a concrete mechanistic hypothesis that could reshape how the community thinks about feature attribution in SAEs. The finding that token distribution entropy tracks "abstractness" across layers for trained but not randomized models is a useful preliminary signal that aggregate auto-interpretability misses.

## Suggestions

- Add confidence intervals or error bars across multiple random seeds for all main AUROC results to strengthen the statistical basis of the central claim.
- Provide a concrete, practical recommendation: for practitioners using auto-interpretability scores, what threshold or filtering strategy (e.g., minimum token distribution entropy) should be applied alongside aggregate AUROC to increase confidence that discovered features reflect learned computation?
- Consider a brief analysis of whether the high-scoring random-variant latents are systematically different in character from high-scoring trained-model latents (e.g., do random-model latents tend to be token-identity features?).

## Score and Decision

This paper makes a clear, well-executed, and important methodological contribution to the mechanistic interpretability literature. The experimental design is sound, the central negative result is significant and well-supported, and the constructive proposals (entropy-based analysis, toy models) move the conversation forward. The main limitations—single model family and unresolved causal mechanism—are acknowledged and do not invalidate the core contribution. The result is the kind of benchmark finding that can redirect evaluation practices in the field.

MY FINAL SCORE: 7.0
MY FINAL DECISION: Accept