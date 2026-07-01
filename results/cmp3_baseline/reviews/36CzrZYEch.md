## Summary

This paper proposes IRIS, a reinforcement learning framework that uses **negative self-certainty (NSC)** as an intrinsic reward to fine-tune autoregressive text-to-image (T2I) models without any human labels or external verifiers. The key insight is that, contrary to text-based reasoning tasks where maximizing self-certainty is beneficial, minimizing self-certainty (i.e., maximizing uncertainty) improves T2I generation by encouraging visually rich and diverse outputs. Empirical results on Janus-Pro models show that IRIS achieves performance competitive with external reward methods across GenEval, T2I-CompBench, and WISE benchmarks, while requiring no domain-specific supervision.

## Strengths

- **Novel and principled approach**: The paper is the first to successfully train autoregressive T2I models using only an intrinsic reward derived from the model’s own output distribution. The idea of using negative self-certainty is clean, well-motivated, and contrasts interestingly with prior work in LLM reasoning.
- **Clear and surprising finding**: The observation that minimizing, rather than maximizing, self-certainty improves image generation is well supported by quantitative evidence (Figure 2 shows a clear decreasing trend in image self-certainty during RL training with external rewards) and qualitative examples (Figure 1). This task-dependent behavior of self-certainty is a genuine contribution.
- **Thorough evaluation**: The paper evaluates on three diverse benchmarks covering object-level, compositional, and knowledge-based generation, for both 1B and 7B model sizes. Ablation studies systematically examine the effect of Chain-of-Thought, the direction of self-certainty on text vs. image tokens, forward vs. backward KL divergence, and the necessity of RL-based optimization over direct maximization.
- **Competitive empirical results**: IRIS achieves performance comparable to external reward methods (T2I-R1) on most metrics, and even surpasses them on all three benchmarks for the 1B model at early training steps. The paper honestly discusses where external rewards maintain an advantage (e.g., counting, spatial relations) and attributes this to the specific external signals used.
- **Well-written and structured**: The paper clearly motivates the problem, presents the hypothesis and counter-intuitive finding, describes the method, and supports claims with extensive experiments.

## Weaknesses

### Fatal
None.

### Major
- **Limited architectural scope**: The method is only demonstrated on one family of autoregressive T2I models (Janus-Pro). While the paper acknowledges that T2I architectures are diverse (diffusion, masked modeling, etc.), the generalizability of the “minimize self-certainty” principle to other architectures remains untested. This significantly tempers the strength of the claimed “first framework” and the broader applicability statement.

- **Inconsistency in baseline reproduction**: The paper notes that the official T2I-R1 implementation uses the wrong chat template for Janus-Pro, leading to different numerical results. While the authors use the correct template for both IRIS and their T2I-R1 baseline, the exact conditions of the original T2I-R1 results are not reproduced. This makes strict comparisons with published numbers (e.g., in Table 1) difficult, though the relative comparison within the paper’s own experiments is still valid.

### Minor
- **Evaluation metrics in ablation**: The four external reward models used for evaluation (HPSv2, DINO, GIT, ORM) are the same ones used to train the T2I-R1 baseline. While the authors correctly argue that these are unbiased for IRIS since they are not used in training, the metrics are nonetheless proxies for human preference and may not fully capture image quality. A human evaluation or a broader set of metrics would strengthen the results.
- **Interpretation of text self-certainty**: The paper speculates that minimizing text self-certainty encourages diverse semantic CoTs, but does not provide direct analysis (e.g., measuring CoT diversity or informativeness). The argument is plausible but relies on indirect evidence.

### Trivial
- The paper uses “RLIF” but the intrinsic reward is differentiable and optimized via GRPO; this differs from some prior definitions of RLIF that are not differentiable. This is a minor terminology point.
- The claim that IRIS “enhances reasoning capabilities” of T2I models is a stretch; the improvements are in generation quality rather than logical reasoning per se.

## Nice-to-Haves

- Extending experiments to at least one other autoregressive T2I model (e.g., SEED-X, or a diffusion-based model by converting the reward to a likelihood-based signal) would greatly strengthen the paper’s core claim.
- A human evaluation study (e.g., pairwise preference judgments) comparing IRIS, T2I-R1, and the base model would provide stronger evidence that the improvements correspond to real perceptual quality.
- Analysis of the generated semantic CoTs (e.g., length, novelty, diversity) to directly support the claim that minimizing text self-certainty leads to more diverse and useful reasoning.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Address the architectural generalizability concern by either (a) testing on another autoregressive T2I model, or (b) providing a clear roadmap for how IRIS could be adapted to non-autoregressive models (e.g., by using the model’s output distribution over discrete latent codes or diffusion steps).

## Score and Decision

The paper presents a novel, well-motivated, and empirically sound method for aligning T2I models using only intrinsic signals. The observation that self-certainty behaves oppositely for image generation compared to text reasoning is a clear and valuable insight. The experimental evaluation is thorough, with careful ablation studies and competitive results against external reward methods. The main limitation is the single-model-family validation, which prevents full acceptance of the claimed generality. However, the strength of the core idea and the quality of the experiments justify acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>