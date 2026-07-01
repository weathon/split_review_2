## Summary

This paper proposes integrating n-gram induction heads into transformer-based in-context reinforcement learning (ICRL) models, specifically building on Algorithm Distillation. The authors argue that n-gram attention patterns can reduce the data required for generalization and make training less sensitive to hyperparameters. They provide experimental evidence on grid-world (Dark Room, Key-to-Door) and pixel-based (Miniworld) environments, showing that their method matches or surpasses Algorithm Distillation in performance, particularly in low-data regimes, and claim up to 27x data reduction.

## Strengths

- **Timely and relevant problem**: The paper addresses real challenges in ICRL—data inefficiency, training instability, and hyperparameter sensitivity—which are important practical barriers for deploying these methods.
- **Clean integration of existing ideas**: Building n-gram induction heads (from Akyürek et al.) into Algorithm Distillation is a sensible and well-motivated combination. The authors correctly identify that transformers naturally learn such patterns slowly, so hardcoding them provides a useful inductive bias.
- **Thoughtful adaptation to RL and pixel observations**: The use of Vector Quantization to enable n-gram matching in image-based environments is a creative solution that extends n-gram methods beyond discrete text-like domains. The ablation with permuted attention masks (Table 1c) convincingly shows that when the n-gram mechanism is broken, performance reverts to baseline, confirming the mechanism's value.

## Weaknesses

### Major
1. **Insufficient experimental rigor and missing key details**: The evaluation is limited to very simple environments (Dark Room, Key-to-Door, Miniworld). While these serve as proof-of-concept, the paper claims "generalization to novel tasks" and "data efficiency" without testing on standard ICRL benchmarks used in the community (e.g., XLand-Minigrid, Meta-World tasks mentioned in the conclusion). The 27x data reduction claim relies on a comparison in Appendix B, but the underlying calculations are not clearly justified—specifically, the baseline's required data point (2048 goals and 2048 histories) is cited from Laskin et al., but the paper does not reproduce this baseline under the same conditions to ensure a fair comparison.

2. **Inconsistent and potentially misleading reporting**: The paper uses "Expected Maximum Performance" (EMP) which aggregates across random hyperparameter searches. While this is a valid metric for demonstrating ease of training, the results are presented in a way that conflates "better hyperparameter search efficiency" with "better algorithm performance." In many plots (Figures 2, 4, 5), the n-gram method achieves higher final EMP, but it remains unclear whether this is because the method simply finds good hyperparameters faster or because it genuinely achieves higher peak performance. The paper does not show the *best single run* performance or a direct comparison at equivalent optimal hyperparameters. Additionally, some figures use different numbers of training goals for compared methods (e.g., Figure 6 left: N-Gram on 50 goals vs baseline on 60 goals), which undermines the fairness of the comparison.

3. **Limited analysis of computational overhead**: The paper introduces additional components (n-gram attention layers and, for pixel environments, a VQ model). There is no discussion of the computational cost—training time, inference overhead, memory usage—of these additions. The core claim is improved efficiency, but without quantifying the extra cost, it is impossible to assess the practical trade-off. For example, the VQ model requires pretraining and a forward pass at each inference step; this may negate some data-efficiency gains in wall-clock time.

4. **N-gram matching in RL context is conceptually less clean than claimed**: The paper matches n-grams over *(s, a, r)* tuples or states. However, in RL, repeated states do not necessarily indicate the same decision-relevant context (e.g., the same state reached via different trajectories may have different value). The theoretical grounding from language modeling (where repeated n-grams correspond to syntactic patterns) does not directly transfer. The paper does not discuss this mismatch or provide intuition for why state-level n-grams are beneficial for ICRL beyond "capturing sequential patterns."

### Minor
- The hyperparameter ablation (Table 1a-b) is performed on only one environment (Miniworld-Dark) with relatively few trials, making the conclusion that n-gram length and position do not matter tentative.
- The related work section is well-structured but does not position the paper clearly against alternative approaches to ICRL data efficiency (e.g., data augmentation [14], retrieval-augmented methods [26]).

### Trivial
- The title "FORMATTING INSTRUCTIONS FOR ICLR 2026 CONFERENCE SUBMISSIONS" is clearly a placeholder and should be corrected.
- There is a typo in the caption of Figure 3: "the agent does not see their location" should be "its location."

## Nice-to-Haves
- Test on at least one larger-scale, more complex ICRL benchmark to demonstrate that the benefits hold beyond toy domains.
- Include a wall-clock time comparison or parameter count analysis to contextualize the efficiency claims.
- Provide an open-source implementation of the full pipeline to facilitate reproducibility and adoption.

## Novel Insights

None beyond the paper's own contributions. The core insight—that n-gram induction heads can improve ICRL—is a direct application of existing language model findings to the RL setting. While this is a useful engineering insight, it is not a conceptually novel finding.

## Suggestions

- **Strengthen the baseline comparison**: Replicate the Algorithm Distillation baseline in the exact same setting (same number of training goals/histories) and report both EMP and best single-run performance. This would clarify whether the advantage is in hyperparameter search efficiency or peak performance.
- **Provide computational cost analysis**: Report the additional training time per step, inference time, and memory usage for the n-gram models. This is essential for evaluating the practical efficiency claim.
- **Expand evaluation to a more complex domain**: At minimum, include experiments on a standard benchmark like XLand-Minigrid or Procgen to show the method scales beyond simple grid-worlds and small visual environments.
- **Clarify the theoretical motivation**: Discuss why state-based n-gram matching is expected to help in RL beyond the "simplicity bias" argument. Provide examples or intuition for what patterns the n-gram heads should capture (e.g., "the agent repeats a successful exploration action").
- **Fix the figure inconsistencies**: Ensure all comparisons use the same number of training goals/histories for both methods, or explicitly state and justify any differences.

## Score and Decision

**Summary**: The paper addresses a practical problem in ICRL and proposes a reasonable modification. However, the experimental evaluation is too narrow and lacks the rigor needed to support the central claims about data efficiency and reduced hyperparameter sensitivity. The lack of baseline reproduction, inconsistent comparisons, missing computational cost analysis, and absence of evaluation on standard ICRL benchmarks all weaken the contribution. While the idea is promising, the current evidence is insufficient for acceptance at ICLR.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>