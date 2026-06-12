## Summary

This paper introduces RSThinker, a Vision-Language Model for remote sensing that produces verifiable, step-by-step reasoning traces (Perceptually-Grounded Geospatial Chain-of-Thought, Geo-CoT) instead of opaque end-to-end outputs. The authors construct Geo-CoT380k, the first large-scale dataset of structured Geo-CoT rationales (384k samples), and train RSThinker via a two-stage alignment strategy—supervised fine-tuning to instill the reasoning architecture, followed by GRPO to refine factual correctness. RSThinker achieves state-of-the-art performance across grounding, detection, counting, classification, captioning, and VQA benchmarks.

## Strengths

- **Well-formalized reasoning framework**: The Geo-CoT paradigm (Planning → Grounding → Synthesis) is thoughtfully designed for the unique challenges of remote sensing—vast scenes, dense tiny objects, topologically-grounded queries—and the requirement that every analytical claim be linked to a verifiable spatial reference is a genuine conceptual advance over generic grounded CoT methods.
- **Comprehensive evaluation with strong ablations**: The paper evaluates across six task categories with both in-domain and zero-shot benchmarks, compares against 15+ baselines spanning commercial, open-source, reasoning, and domain-specific VLMs, and provides clean ablations (Table 8) isolating the contribution of CoT-based SFT, GRPO, and KL regularization. The ablation clearly shows CoT-supervised SFT unlocks a fundamentally higher performance tier than plain SFT.
- **Honest and instructive failure analysis**: The authors present a concrete failure case (Figure 7) where the model misidentifies a dock extension as a ship, and correctly argue that the explicit grounding mechanism turns silent failures into auditable errors. This demonstrates intellectual honesty and strengthens the practical case for the framework.
- **Scalable dataset construction pipeline**: Conditioning GPT-4V on verified ground-truth annotations (bounding boxes, captions, exemplars) rather than open-ended generation is a practical and defensible strategy for minimizing hallucinated rationales.

## Weaknesses

### Fatal
None.

### Major

- **Heavy reliance on GPT-4V for rationale generation**: The quality ceiling of Geo-CoT380k is bounded by GPT-4V's capabilities, and the rationale generation process is not validated beyond qualitative spot-checks. The paper acknowledges this limitation in passing but does not quantify the error rate of generated rationales or assess how errors in the training data propagate through SFT into the final model. A human evaluation of a sample of generated CoTs would substantially strengthen the claim that the dataset is "high-fidelity."

- **Potentially unfair baseline comparisons**: Several commercial models (Claude-sonnet-4, ChatGPT-5) achieve surprisingly low scores on tasks like visual grounding (11.1 and 14.4 mIoU@0.5 on VRSBench-VG). These scores are an order of magnitude below even simple open-source models, which raises questions about whether prompting strategies, output format constraints, or evaluation parsing differ systematically across baselines. The paper does not describe how commercial models were prompted or how their outputs were parsed to extract bounding boxes/counts, making it difficult to verify the fairness of these comparisons.

- **Missing comparison against recent remote sensing reasoning baselines**: The related work discusses SegEarth-R1 and RemoteReasoner in detail as prior work on reasoning in remote sensing, yet these do not appear in any of the main results tables. Omitting direct comparison against the most relevant prior approaches weakens the claim of state-of-the-art performance.

### Minor

- **Training data overlap with evaluation**: RSThinker is trained on DOTAv2-train, HRRSD-train, VRSBench-train, etc., and evaluated on the corresponding val/test splits. While this is standard practice, the paper does not discuss whether the Geo-CoT rationales could inadvertently leak information about the evaluation data through GPT-4V's parametric knowledge of these widely-used benchmarks.

- **Limited exploration of reward design**: The task-specific reward functions (Table 3) are reasonable but somewhat simplistic. For instance, the captioning reward is a weighted sum of standard metrics with unspecified weights. The paper could benefit from at least one experiment examining sensitivity to reward design choices.

- **The "first" claim is stated without thorough verification**: The paper repeatedly claims Geo-CoT380k is the "first large-scale dataset" for remote sensing CoT. While it may well be the largest, related datasets in the geographic domain (GeoChain, GAEA) exist and a more nuanced comparison would be appropriate.

## Nice-to-Haves

- A human evaluation of a random sample of generated CoT rationales to quantify quality and hallucination rate
- Sensitivity analysis on the number of GRPO samples (k) and the KL coefficient β
- A comparison of inference cost (latency, token count) versus end-to-end baselines, since the explicit reasoning trace substantially increases output length

## Novel Insights

The paper's central novel insight is that remote sensing reasoning requires a fundamentally different grounding paradigm than general computer vision. While general grounded CoT methods reason over discrete, salient objects, remote sensing demands iterative evidence gathering across vast, non-uniform scenes with dense, tiny objects. The Geo-CoT framework's Planning-Grounding-Synthesis architecture, with its mandatory spatial references, is a well-motivated response to this domain-specific challenge. Additionally, the empirical finding that SFT on structured rationales is a necessary prerequisite for GRPO (rather than GRPO alone being sufficient) provides useful guidance for the broader community on instilling complex reasoning capabilities in VLMs.

## Suggestions

- Add a detailed description of how commercial model baselines were prompted and how their outputs were parsed, to address concerns about fairness of comparison.
- Include a human evaluation study on a sample of Geo-CoT380k rationales to establish data quality.
- Add SegEarth-R1 and RemoteReasoner to the main comparison tables as the most directly relevant prior work.
- Report inference latency and average output token count to quantify the cost of explicit reasoning.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: Accept