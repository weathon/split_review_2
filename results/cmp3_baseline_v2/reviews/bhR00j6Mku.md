## Summary

This paper presents the first systematic study of benchmark contamination detection in Large Reasoning Models (LRMs). It investigates two practical contamination scenarios: (Stage I) contamination introduced during supervised fine-tuning (SFT) on a base model and subsequently concealed through reinforcement learning (e.g., GRPO), and (Stage II) contamination with chain-of-thought (CoT) applied directly to an advanced LRM as a final SFT step. Through extensive evaluation of ten existing detection methods across multiple LRMs and reasoning benchmarks, the authors demonstrate that existing detection approaches are fragile—RL training shrinks the member/non-member log-probability gap (driven by PPO-style importance sampling and clipping), while CoT contamination on LRMs barely leaves detectable evidence because the models generalize to unseen samples. Theoretical analysis and ablation studies support the empirical findings, revealing a critical vulnerability in LRM evaluation integrity.

## Strengths

- Timely and important problem: The paper addresses a pressing issue in the evaluation of LRMs, where leaderboard-driven competition creates strong incentives for benchmark contamination, and existing detection methods are shown to be easily evaded.
- Comprehensive evaluation: The study tests 10 representative detection methods (generation-based, perturbation-based, reference-based, reference-free) across six reasoning benchmarks, using two different base models and four advanced LRMs, providing strong empirical evidence.
- Theoretical insight: The authors provide a formal analysis linking PPO-style clipping and importance sampling to the contraction of the NLL gap between members and non-members, and empirically validate the predictions through well-designed ablation studies (e.g., removing clipping restores detectability).
- Clear two-stage framing: The paper structures contamination around realistic development workflows (pre-LRM via SFT+RL, and post-LRM via final SFT), making the findings directly relevant to model development pipelines.
- Reproducibility orientation: Detailed contamination and detection setups are described, and the use of open-source models and benchmarks supports reproducibility.

## Weaknesses

### Fatal
None.

### Major
- Limited RL training steps: The maximum GRPO/RL training is 156 steps (one epoch of 10K questions), which is far fewer than typical LRM training. While the paper acknowledges this and shows monotonic concealment trends, it remains unclear whether the concealment effect fully saturates or whether detection methods might recover after very long RL training. The claim that "extensive GRPO training would render all existing detection methods to near-random performance eventually" is a conjecture not fully demonstrated.
- The theoretical analysis (Theorem 3.1) relies on several restrictive assumptions: tabular setting, small gradient steps, and simplified reward structure. While the analysis provides useful intuition, its generality to practical deep RL settings (e.g., function approximation, large batch sizes, adaptive optimizers) is not rigorously established.
- The Stage II contamination scenario only considers SFT with CoT data. In practice, developers might also apply RL on contaminated benchmarks in the post-LRM stage, which could interact differently with detection methods. The paper does not explore this combined threat model.

### Minor
- Some detection methods (e.g., LiRA) still achieve AUROC around 60–65% in the post-LRM scenario, which is above random but far from reliable detection. The paper sometimes characterizes this as "near random guesses," which slightly understates the residual signal.
- The paper does not discuss the feasibility of obtaining non-member data for reference-based methods like LiRA in realistic adversarial settings, where an attacker might control the training process and limit exposure of non-member data.

### Trivial
- The notation in Section 3.2 is dense and could benefit from a more intuitive walkthrough of the key covariance arguments.
- Some figures (e.g., Figure 2) are referenced with placeholder captions in the extracted text, but this is likely a parser artifact.

## Nice-to-Haves

- An exploration of whether detection methods based on output diversity (e.g., n-gram overlap, response variance) are also affected by RL concealment, beyond the log-probability-based methods studied.
- A discussion of potential adaptive countermeasures that could be built to resist such evasion, moving beyond the high-level directions in Section 5.
- A sensitivity analysis of the concealment effect under different RL hyperparameters (learning rate, clipping range, number of rollouts).

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the very mechanism that stabilizes RL training—importance sampling and clipping—has the side effect of erasing differential signals between memorized and non-memorized examples. This suggests that contamination detection cannot rely solely on statistical signatures that RL training naturally erodes, and that any training algorithm with similar per-example adaptive weighting may exhibit analogous concealment. Additionally, the finding that LRMs generalize to unseen samples after CoT contamination challenges the core assumption of membership inference in LLMs (that contamination is primarily about memorization), pointing to a fundamental shift needed in detection methodology.

## Suggestions

- To strengthen the claim about eventual near-random performance, consider running longer RL training (e.g., 500–1000 steps) on a subset of benchmarks to show that the monotonic trend continues.
- Provide a more explicit comparison of the computational cost of RL training versus the performance inflation achieved, to contextualize the practical threat level.
- Discuss whether contamination detection could be improved by analyzing the *reasoning traces* (if developers release them) rather than just the final answers, and why this may or may not be practical.

## Score and Decision

The paper presents a timely, well-executed study with strong empirical evidence and theoretical grounding. While the RL training duration is limited and the theoretical model is simplified, the core findings are convincingly demonstrated across multiple settings. The paper reveals a serious vulnerability in LRM evaluation and is likely to stimulate important follow-up work. I recommend acceptance.

**Score**: 8  
**Decision**: Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>