## Summary
This paper proposes integrating n-gram induction heads into transformer-based in-context reinforcement learning (ICRL) models, specifically building on Algorithm Distillation (AD). The authors argue that n-gram attention patterns reduce the data required for generalization, make training less sensitive to hyperparameters, and can be adapted to pixel-based environments via vector quantization. Experiments on Dark Room, Key-to-Door, and Miniworld environments show that the proposed method matches or outperforms AD, particularly in low-data regimes.

## Strengths
- **Addresses a practical problem**: The paper tackles the real challenges of data inefficiency and training instability in ICRL, which are well-documented issues in the literature.
- **Novel application of n-gram heads to RL**: While n-gram induction heads have been studied in language modeling, applying them to in-context reinforcement learning is a new and sensible direction.
- **Clear experimental protocol**: The use of Expected Maximum Performance (EMP) with random hyperparameter search is a rigorous way to compare methods without cherry-picking, and the fixed gradient steps ensure fair data usage.
- **Demonstrates adaptation to visual observations**: The use of vector quantization to enable n-gram matching in pixel-based environments (Miniworld) is a non-trivial extension and shows the method's broader applicability.

## Weaknesses
### Fatal
None.

### Major
- **Limited scope of environments**: The experiments are confined to simple grid-world and Miniworld environments. The paper does not test on more challenging or standard RL benchmarks (e.g., Meta-World, XLand-Minigrid, or continuous control tasks), which limits the strength of the claims about general applicability.
- **Insufficient comparison to other ICRL methods**: The baseline is only Algorithm Distillation. Other ICRL approaches (e.g., Lee et al. 2023, or methods using data augmentation/filtering) are mentioned in related work but not compared against. This makes it unclear whether the gains are specific to AD or would transfer to other ICRL frameworks.
- **The 27x data reduction claim is not fully substantiated**: The claim in Section 4.2 and Appendix B (not visible) is based on a specific comparison to AD's reported requirements (2048 goals and 2048 histories). However, the paper does not show that AD with 27x less data fails completely; it only shows that AD plateaus at suboptimal performance. The "27x" figure may be an overstatement without a direct ablation showing the exact data threshold where AD fails.

### Minor
- **Hyperparameter sensitivity analysis is limited**: The ablation in Section 4.4 only tests n-gram length and layer position on Miniworld-Dark. It does not explore other hyperparameters (e.g., learning rate, number of layers, embedding size) that might interact with the n-gram layer.
- **The VQ-based n-gram matching for images is not deeply analyzed**: The paper does not report how often the VQ model produces correct matches, nor does it ablate the quality of the VQ encoder. The "permuted mask" experiment (Section 4.5) is a good sanity check, but it does not quantify how often the VQ model actually fails.
- **No analysis of computational overhead**: The paper does not discuss the additional computational cost of the n-gram attention layer (e.g., FLOPs, memory, training time) compared to the baseline. This is important for practitioners considering adoption.

### Trivial
- The paper uses "transitivity" instead of "transience" when discussing the nature of in-context learning (Section 6), but this is a minor wording issue.

## Nice-to-Haves
- Testing on a more diverse set of environments (e.g., continuous control, Meta-World) would significantly strengthen the claims.
- A direct comparison to other data-efficient ICRL methods (e.g., noise curriculum, data augmentation) would help position the work.
- An analysis of the learned n-gram patterns (e.g., what kind of state transitions are being matched) could provide deeper insight into why the method works.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Add experiments on at least one additional ICRL baseline (e.g., Lee et al. 2023) to show that the n-gram heads benefit more than just AD.
- Provide a more precise characterization of the data reduction: run AD with varying data amounts to find the exact point where it fails, rather than relying on a single reported number from the original AD paper.
- Include a brief analysis of the VQ model's matching accuracy and its impact on n-gram layer effectiveness.

## Score and Decision
The paper presents a clear, well-motivated idea with solid experimental evidence on simple environments. However, the limited scope of environments and the lack of comparison to other ICRL methods prevent it from being a strong contribution at this stage. The work is promising and addresses a real problem, but the evidence is not yet sufficient to support broad claims about data efficiency and hyperparameter robustness.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>