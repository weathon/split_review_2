## Summary
# Final Review Report

## Summary

This paper proposes IRIS (Intrinsic Reward Image Synthesis), a reinforcement learning framework that fine-tunes autoregressive text-to-image (T2I) models using only an intrinsic reward signal — specifically, negative self-certainty (NSC), defined as the negative KL divergence between the model's output distribution and a uniform distribution. The central idea is that minimizing the model's self-certainty (i.e., maximizing uncertainty) on both text and image tokens, as opposed to maximizing it (as done in prior LLM reasoning work), leads to more diverse and visually appealing image generation.

The key empirical observation is that during RL training with external reward models, self-certainty on image tokens *decreases* while T2I performance improves, whereas for LLMs on reasoning tasks it increases. Based on this, the authors apply GRPO with NSC as the sole reward signal to fine-tune Janus-Pro (1B and 7B) models. They report improvements over the base model on GenEval (+9.1% relative), T2I-CompBench (+13.3%), and WISE (+28.8%) for the 1B model, achieving performance within 0.01–0.03 absolute points of a strong external-reward baseline (T2I-R1).

The paper addresses a meaningful problem — reducing reliance on expensive human annotation and domain-specific reward models for T2I alignment. The observation that self-certainty behaves differently across modalities is interesting and could stimulate further research on modality-specific RL training strategies. However, the paper contains several overclaims, relies on correlational evidence for its core causal claim, and has limited training scope (800 steps) that weakens convergence guarantees.

## Strengths
1. **Novel Problem Framing:** The paper identifies an interesting and under-explored direction — using purely intrinsic reward signals for RL-based fine-tuning of autoregressive T2I models. The observation that self-certainty behaves differently across text reasoning (where higher is better) and image generation (where lower may be beneficial) is a non-trivial empirical finding that could inform future research on modality-aware RL training strategies.

2. **Clean and Focused Method:** IRIS is conceptually simple — replacing external reward models with negative self-certainty (NSC) as the optimization target within an existing GRPO framework. This simplicity is a strength: the method is architecture-agnostic, requires no external models or human annotation, and the objective is differentiable and easy to implement. The ablation study systematically investigates the design choices (CoT vs. no CoT, text vs. image SC direction, forward vs. backward KL, RL vs. direct optimization), providing useful empirical guidance.

3. **Competitive Empirical Results Under a Challenging Setting:** Despite using no external supervision, IRIS achieves scores within 0.01–0.03 absolute points of a strong external-reward baseline (T2I-R1) across three diverse benchmarks and two model scales. This is noteworthy because T2I-R1 was explicitly optimized on the same external reward models used for evaluation, creating an inherent advantage for the baseline. That IRIS remains competitive suggests the intrinsic reward signal carries meaningful training signal.

4. **Transparency About Implementation Corrections:** The paper honestly identifies a chat-template inconsistency in the T2I-R1 baseline implementation and corrects it. This level of transparency about baseline reproduction issues is commendable and improves the reliability of the empirical comparison.

## Weaknesses
### W1. Overclaiming "competitive with or superior to" (Severity: Major)

The manuscript repeatedly claims that IRIS achieves performance "competitive with or superior to external rewards" (abstract, conclusion). However, the paper's own results (Table 1) show IRIS scores are **consistently lower** than T2I-R1 across all three benchmarks for both model scales:
- GenEval Overall: IRIS 0.72 vs T2I-R1 0.75 (1B); IRIS 0.77 vs T2I-R1 0.78 (7B)
- T2I-CompBench Complex: IRIS 0.3793 vs T2I-R1 0.3820 (1B); IRIS 0.3916 vs T2I-R1 0.3992 (7B)
- WISE Overall: IRIS 0.37 vs T2I-R1 0.38 (1B); IRIS 0.48 vs T2I-R1 0.50 (7B)

The phrase "superior to" is factually unsupported in every reported comparison. The paper should replace this with precise, bounded language such as "within 0.01—0.03 absolute points of" the external-reward baseline. *(See annotation #1 on Abstract)*

### W2. Causal claim about self-uncertainty is correlational (Severity: Major)

The paper's core motivation — that "lower self-certainty causes better image generation" — is supported by a correlation shown in Figure 2 (during RL training with external rewards, image self-certainty decreases while image quality improves). This is purely correlational and confounded by the training process: the decrease in self-certainty could be a side effect of other training dynamics (e.g., increased output diversity, VQ codebook modal changes) rather than a causal mechanism. The paper interprets this correlation as causal (e.g., "This indicates that less self-confident multimodal LLMs will generate images with higher rewards") without interventional evidence. An ablation where self-certainty is independently perturbed (e.g., via temperature scaling, LoRA modulation) while holding other factors fixed would be needed to establish causality. *(See annotation #4 on Fig. 2)*

### W3. Inflated "reasoning capabilities" claim (Severity: Major)

The paper states that IRIS "can significantly enhance the reasoning capabilities of T2I models." This overstates what the evidence supports. GenEval, T2I-CompBench, and WISE benchmark improvements measure object-centric generation, compositional understanding, and knowledge alignment — not reasoning in the traditional sense (multi-step inference, logical deduction, planning). Moreover, the semantic CoT mechanism that might support reasoning is adopted from prior work (Jiang et al., 2025), not a novel contribution of IRIS. The paper should replace "reasoning capabilities" with precise descriptions of what the benchmarks measure. *(See annotation #6 on Introduction)*

### W4. Limited training budget — only 800 steps (Severity: Major)

All reported experiments use only 800 training steps (with effective batch size 8, i.e., 6,400 total samples). The training curves in Figure 3 show upward trends for IRIS at step 800, suggesting that performance has not converged. The external-reward baseline curves appear to plateau or drop, making the comparison at 800 steps potentially incomplete. The paper does not provide a rationale for stopping at 800 steps, and the "best checkpoint" selection from a narrow 100–800 window risks optimism bias. Without convergence evidence, the main results are preliminary. *(See annotation #8 on Experiment Configuration)*

### W5. Speculative explanation for text-token uncertainty (Severity: Major)

The paper acknowledges that maximizing text-token uncertainty appears to contradict the Fig. 2 observation (where training on reasoning tasks decreased uncertainty). The offered explanation — "math reasoning requires precise thought generation, while our T2I setting generates descriptive and explorative text" — is speculative and unsupported. The single reference to Team et al. (2025) on information-seeking agents is from a different domain and does not directly justify the claim. No direct measurement of CoT diversity (e.g., n-gram diversity, semantic variation) is provided. *(See annotation #7 on Section 3.2)*

### W6. Evaluation metric bias in ablation studies (Severity: Major)

The ablation studies use the same four external reward models (HPSv2, DINO, GIT, ORM) as evaluation metrics, while the T2I-R1 baseline was explicitly trained to optimize these exact metrics. This creates an inherent evaluation bias favoring T2I-R1 — it is directly optimized for HPSv2, DINO, etc., while IRIS is not. The paper calls these "simple and unbiased metrics," which is misleading: the metrics are unbiased for IRIS (not trained on them) but the *comparison* is biased in favor of T2I-R1. This should be acknowledged explicitly, and ideally supplemented with evaluation metrics that neither method was trained on. *(See annotation #11 on Ablation Study)*

### W7. Missing semantic CoT prompt template (Severity: Minor)

The paper mentions generating "semantic Chains of Thought (CoTs)" before image synthesis but does not specify the exact prompt template or the decoding strategy used (e.g., is the CoT generated zero-shot? Few-shot? Is there a system prompt?). Without this detail, the CoT procedure cannot be reproduced. This is critical because the ablation study shows CoT significantly affects performance.

### W8. Limited comparison to prior intrinsic-reward methods (Severity: Minor, deferred)

The paper compares IRIS against an external-reward baseline (T2I-R1) but does not compare against prior intrinsic-reward methods from the text domain (e.g., entropy maximization, self-certainty maximization from Zhao et al., Zhang et al.) applied to the T2I setting. A direct comparison would clarify whether NSC is uniquely beneficial or if any intrinsic signal would work. Due to the Retrieval-Disabled Mode in this review, a comprehensive novelty comparison could not be performed and is deferred for manual verification.

### W9. Graphics-only evidence for visual claims (Severity: Minor)

Figure 4 shows a single qualitative example (bicycle) to demonstrate that training with semantic CoTs improves image generation. A single example is insufficient to establish a general improvement pattern, especially given the inherent randomness in T2I generation. Quantitative evaluation of generated image quality with vs. without CoT across a diverse prompt set would strengthen this claim.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses an interesting and timely problem (reducing reliance on external reward models for T2I alignment) and makes a non-trivial empirical observation about modality-dependent self-certainty behavior. The IRIS method is clean, architecture-agnostic, and requires no human annotation. However, the score is constrained by several factors that limit confidence in the current presentation:

- **Research value (primary dimension):** Moderate. The core idea — using negative self-certainty as an intrinsic reward for T2I — is novel and potentially impactful, but the causal mechanism is not established, and several claims are overstated relative to the evidence. The observation about task-dependent self-certainty behavior is interesting but preliminary.

- **Novelty (primary dimension):** Moderate-to-uncertain. Applying negative self-certainty (originally proposed for text generation by Zhao et al. 2025b) to the T2I setting is a meaningful extension. However, a comprehensive novelty assessment requires literature verification that could not be performed in this review run (Retrieval-Disabled Mode). The "first" claim is plausible if tightly scoped but needs manual verification.

- **Validity/Soundness:** The empirical results are systematically reported with variance, but overclaiming ("superior to," "enhance reasoning capabilities," causal interpretation of correlational data) reduces trust in the conclusions. The 800-step training limit and evaluation metric bias in ablations are additional concerns.

- **Reproducibility:** Partially adequate. Hyperparameters and training procedures are reported, but the semantic CoT generation prompt template is missing. The corrected chat template for Janus-Pro is a positive transparency step.

The paper has a solid core that could be strengthened with: (1) more careful claim bounding, (2) longer training runs to demonstrate convergence, (3) a direct causal test of the self-uncertainty mechanism, and (4) acknowledgment of evaluation biases. With these revisions, the paper could potentially reach 7–8/10.