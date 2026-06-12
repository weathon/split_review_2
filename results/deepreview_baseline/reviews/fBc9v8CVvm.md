## Summary

This paper proposes TWINFLOW, a framework for training one-step generative models that eliminates the need for auxiliary networks (e.g., GAN discriminators) or frozen teacher models. The key idea is extending the time interval to [-1, 1] to create "twin trajectories" — a positive branch mapping noise to real data and a negative branch mapping noise to fake data — and minimizing the discrepancy between their velocity fields. The method achieves strong text-to-image results, including a GenEval score of 0.83 at 1-NFE on SANA-0.6B and successfully scales to full-parameter training on Qwen-Image-20B, matching the original 100-NFE model's performance with 1-2 NFEs.

## Strengths

- **Novel and elegant framework design:** The twin-trajectory concept with extended time interval [-1, 1] is a creative and principled way to create a self-adversarial signal without requiring external discriminators or teacher models. The derivation connecting velocity matching to distribution matching via KL divergence (Eq. 3-6) is theoretically sound and well-motivated.

- **Impressive scalability demonstration:** The paper demonstrates full-parameter training on a 20B-parameter model (Qwen-Image-20B), which is a significant achievement. Table 3 shows that competing methods (VSD, DMD, SiD) suffer from OOM in the raw setting, while TWINFLOW achieves strong results (GenEval 0.89, DPG-Bench 87.54 with longer training) with a unified single-model design.

- **Strong empirical results:** The method achieves state-of-the-art or competitive results across multiple benchmarks. At 1-NFE on SANA-0.6B, TWINFLOW achieves GenEval 0.83, outperforming SANA-Sprint (0.76) and RCGM (0.80). The Qwen-Image-20B results (GenEval 0.86 at 1-NFE) closely match the original 100-NFE model (0.87).

- **Clean and practical contribution:** The simplicity of the framework (no auxiliary networks, no frozen teachers, no GAN training instability) is a genuine practical advantage. Table 1 clearly positions TWINFLOW against existing methods, and the GPU memory comparison in Figure 2b convincingly demonstrates the practical benefits.

## Weaknesses

### Major

- **Insufficient clarity and rigor in the method derivation:** The transition from the KL divergence gradient (Eq. 6) to the rectification loss (Eq. 9) is not fully justified. The paper states that the gradient takes the form of an inner product and then "constructs a tractable loss that produces this gradient structure" using stop-gradient, but the connection is hand-wavy. The derivation of Eq. 8 (Jacobian simplification) is also unclear — it jumps from the definition of x^{fake}_{t'} to a claim about proportionality to the gradient of F_theta without showing the full chain rule or explaining how the stop-gradient operator is applied. This lack of rigor weakens the theoretical foundation.

- **Limited evaluation on DPG-Bench for dedicated text-to-image models:** While TWINFLOW achieves strong GenEval scores, its DPG-Bench performance on SANA-0.6B/1.6B (78.9-79.7) lags behind SANA-Sprint (78.6-82.1) and multi-step models like SANA-1.5 (84.7). The paper attributes this to "data-driven" differences, but this is speculative without controlled experiments. Given that DPG-Bench measures compositional understanding, this gap suggests potential limitations in the method's ability to handle complex multi-object prompts.

- **Missing details on training data and compute:** The paper does not specify the training datasets used for the SANA experiments or the Qwen-Image experiments. Given that data quality is a known factor in few-step generation quality, this omission makes it difficult to assess whether the reported results are due to the method itself or favorable training data. The compute budget (GPU hours, number of training steps for each experiment) is also not reported, which is important for reproducibility and for assessing the practical cost of the method.

### Minor

- **Ablation study scope is limited:** The ablation in Figure 4 focuses primarily on the lambda hyperparameter and the presence/absence of L_TwinFlow. There is no ablation on the choice of N=2 in the any-step framework, the impact of the stop-gradient operator, or the sensitivity to the choice of metric function d(·,·). These would strengthen the understanding of which design choices are critical.

- **The "self-adversarial" terminology is somewhat misleading:** While the method creates a self-contained objective, it does not involve adversarial training in the traditional GAN sense (minimax game). The paper acknowledges this indirectly but the term "self-adversarial" may overstate the connection to adversarial methods.

### Trivial

- The paper states "Our method achieves a GenEval score of 0.83 in 1-NFE" in the abstract, but Table 4 shows this is for SANA-0.6B, while the Qwen-Image-20B result is 0.86. The abstract could be clearer about which model achieves which score.

## Nice-to-Haves

- A comparison of training stability (e.g., loss curves, variance across runs) between TWINFLOW and GAN-based methods like DMD2 would strengthen the claim of improved training stability.
- Analysis of the learned velocity fields (visualization of the twin trajectories) would provide intuitive understanding of what the model learns.
- Evaluation on additional modalities (video, audio) as mentioned in the limitations would significantly broaden the impact.

## Novel Insights

The key insight is that extending the time interval to [-1, 1] and creating twin trajectories allows the model to learn a self-consistent mapping where the "fake" trajectory (negative time) and "real" trajectory (positive time) are forced to agree. This elegantly bypasses the need for an external discriminator by making the model itself the arbiter of distribution matching through velocity field consistency. The connection between velocity matching and distribution matching via the score-velocity relationship (Eq. 5) is a nice theoretical contribution that justifies the practical loss design. The demonstration that this simple framework scales to 20B parameters without the memory overhead of competing methods is a significant practical insight.

## Suggestions

- Provide a clearer, step-by-step derivation of the rectification loss (Eq. 9) from the KL gradient (Eq. 6), explicitly showing where the stop-gradient operator is applied and why the resulting loss produces the desired gradient structure.
- Report the training datasets, data sizes, and compute budgets (GPU hours) for all experiments to improve reproducibility and allow fair comparison.
- Conduct controlled experiments on DPG-Bench using identical training data to isolate the method's contribution from data effects.
- Add an ablation on the choice of N in the any-step framework (e.g., N=1 vs N=2 vs N=3) to justify the N=2 choice.

## Score and Decision

The paper presents a genuinely novel and elegant framework for one-step generation that addresses a real practical need (simplicity, scalability, no auxiliary networks). The theoretical derivation, while needing some clarification, is principled. The empirical results are strong, particularly the demonstration on 20B-scale models which is a significant achievement. The weaknesses (derivation clarity, DPG-Bench gap on SANA, missing training details) are addressable and do not invalidate the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>