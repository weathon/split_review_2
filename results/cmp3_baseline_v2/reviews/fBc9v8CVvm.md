## Summary

The paper proposes TWINFLOW, a training framework for one-step generation in large-scale generative models. The key idea is to extend the time interval of flow matching from [0,1] to [-1,1], creating "twin trajectories"—a positive branch mapping noise to real data and a negative branch mapping noise to model-generated "fake" data. By minimizing the velocity field discrepancy between these two trajectories, TWINFLOW achieves a self-adversarial signal without requiring any auxiliary networks (discriminators, frozen teachers). Experiments on SANA models (0.6B/1.6B) and Qwen-Image-20B show strong GenEval scores (0.83 on 0.6B, 0.86 on Qwen-Image LoRA, 0.89 on full-parameter 20B) at 1-NFE, matching or surpassing multi-step baselines while reducing inference cost by two orders of magnitude.

## Strengths

- **Novel and clean conceptual framework**: The idea of extending time to [-1,1] and creating twin trajectories to obtain a self-contained training signal is original. It avoids the complexity of GAN discriminators, frozen teacher models, or multiple network copies, making the pipeline much simpler than existing few-step methods like DMD2 or SANA-Sprint.
- **Compelling empirical results at scale**: TWINFLOW demonstrates strong 1-NFE and 2-NFE generation quality across multiple architectures, including full-parameter training on a 20B model. The results are competitive with (and often better than) both few-step baselines (RCGM, SANA-Sprint, FLUX-Schnell) and the original multi-step models, which is a practically significant achievement.
- **Clear memory and simplicity advantages over adversarial competitors**: The GPU memory comparison (Figure 2b) and Table 3 convincingly show that DMD2/VSD/SiD cannot even be trained at 20B scale without OOM or mode collapse, while TWINFLOW fits with batch size 24 on 76GB. This is a strong practical argument for the method.
- **Ablation studies are informative**: The study on λ (Figure 4a), the impact of ℒ_TwinFlow (Figure 4b), and the training dynamics (Figure 4c) provide useful insight into how the method works and where improvements come from.

## Weaknesses

### Major

- **The theoretical derivation connecting KL divergence to the rectification loss is not rigorous.** The paper claims that minimizing ℒ_rectify (Eq. 9) minimizes the KL divergence between fake and real distributions (Eq. 3). However, the gradient of Eq. 9 under L2 metric is ∇_θ ‖F_θ(z,0) − sg(Δ_v + F_θ(z,0))‖² = 2 (F_θ − (Δ_v+F_θ))^T (∂F_θ/∂θ) = −2 Δ_v^T (∂F_θ/∂θ). In contrast, the KL gradient in Eq. 6 contains an additional factor −(1−t)/t and involves an expectation over different random variables (x_t', z^fake, etc.) than those in Eq. 9. The paper does not show that these gradient expressions are equivalent, nor does it discuss the discrepancy. The stop-gradient trick is a heuristic—without a proper justification, the claim that the method is derived from distribution matching is overstated. This weakens the theoretical grounding of the core contribution.

- **The self-adversarial loss (Eq. 2) requires generating fake samples from the model during training**, which introduces a dependency between the loss and the current model parameters. This could lead to training instability, error accumulation, or computational overhead (e.g., requiring two forward passes). The paper does not discuss these potential issues, nor does it provide analysis of training stability (e.g., loss curves, sensitivity to the quality of fake samples).

- **Insufficient differentiation from RCGM and consistency models.** TWINFLOW builds directly on the RCGM any-step framework and uses a very similar loss structure (N=2 formulation, base loss + additional terms). The key addition is the twin trajectory with an extra self-adversarial term. However, the paper does not clearly explain why RCGM fails (GenEval 0.52 on Qwen-Image 20B) while TWINFLOW succeeds (0.86), beyond the presence of ℒ_TwinFlow. A deeper analysis of what exactly the twin trajectory provides that RCGM lacks would strengthen the paper.

- **The evaluation on DPG-Bench is weaker than SANA-Sprint** (Table 4: TWINFLOW 0.6B 1-NFE 78.9 vs SANA-Sprint 0.6B 1-NFE 78.6, comparable; but at 2-NFE TWINFLOW 0.6B achieves 79.7 vs SANA-Sprint 79.5 [reported as 81.5 in the "with auxiliary models" section but 78.6 and 80.1 in the "without auxiliary models" section—this discrepancy is confusing]. The paper attributes this to data quantity, which is plausible but not tested. A controlled experiment with identical training data would be more convincing.

### Minor

- The term "self-adversarial" is somewhat misleading: the method does not involve adversarial training (minimax game) but rather a self-consistency loss between two trajectory branches. A less flashy but more accurate term (e.g., "twin-consistency loss") might be preferable.
- Figure 2 and Table 1 formatting (embedded in figures) makes it hard to read. The GPU memory comparison is important but presented as an image rather than a clean table.
- The paper claims "no auxiliary trained model or frozen teacher" but still relies on the RCGM framework's base loss, which itself was trained on a teacher. The initialization of the network (from a pre-trained flow matching model) is still required. This should be stated more clearly.

## Nice-to-Haves

- Include a simple pseudocode algorithm for the training loop to improve reproducibility.
- Provide an analysis of the computational overhead of generating fake samples during training (wall-clock time, memory).
- Add a comparison between TWINFLOW and a consistency model trained from scratch on the same data to isolate the benefit of the twin trajectory.
- Show failure cases or diversity metrics (FID, CLIP score) alongside GenEval and DPG-Bench.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Provide a more rigorous derivation showing that the rectification loss (Eq. 9) indeed minimizes the KL divergence between fake and real distributions, or explicitly state that it is an approximation/heuristic and explain why it works empirically.
- Discuss potential training instability issues and how to mitigate them (e.g., using EMA, gradient clipping).
- Include a comparison of training time and memory for TWINFLOW vs RCGM on the same model to highlight the incremental cost of the twin trajectory.
- Clarify the data regime: are the results on DPG-Bench likely to improve with more data? Provide evidence, even if limited.

## Score and Decision

The paper presents a practically useful and novel method for one-step generation at scale, with strong empirical results and a clean overall design. The main weakness is the lack of rigorous theoretical justification for the rectification loss, but the empirical evidence is substantial enough to support the claims. I recommend acceptance with the expectation that the authors address the theoretical concerns in the final version.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>