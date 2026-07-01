## Summary
This paper introduces Insertion Language Models (ILMs), which generate sequences by inserting tokens at arbitrary positions rather than left-to-right (ARMs) or via masking (MDMs). The authors propose a denoising training objective with a tailored transformer parameterization that avoids the high-variance problem of naive insertion training. Experiments on planning tasks (star graphs, zebra puzzles) show ILMs significantly outperform ARMs and MDMs, while on text generation/infilling they are competitive with ARMs and superior to MDMs in handling arbitrary-length infilling.

## Strengths
- **Clear motivation and well-articulated limitations**: The paper precisely identifies key failure modes of both ARMs (fixed left-to-right order, poor planning) and MDMs (simultaneous unmasking violating dependencies, fixed-length constraint for infilling). These are empirically demonstrated.
- **Effective solution to a challenging training problem**: The approximate denoising objective for insertion is a practical and clever way to avoid the intractable marginalization required for exact insertion training. The parameterization with a single transformer and a separate stop classifier is clean and works well.
- **Compelling results on planning tasks**: On star graphs with variable arm lengths, ILM achieves 100% and 99.1% accuracy (medium and hard) while MDM drops to 36.5% and 21%, and ARM struggles. On zebra puzzles ILM (90.0%) outperforms both ARM (81.2%) and MDM (82.6%) without requiring an oracle decomposition order.
- **Natural handling of arbitrary-length infilling**: Unlike MDMs which require fixed mask counts, ILMs can infill segments of any length without changing the input format. The infilling experiments across single- and multi-segment settings demonstrate this flexibility.

## Weaknesses
### Fatal
None.

### Major
- **The text generation results do not clearly demonstrate an advantage over ARMs**: On both Stories and LM1B, ILM's NLL (2.14, 4.67) is worse than ARM's (2.11, 3.94). While the paper frames ILM as "competitive," the main claimed advantages (planning, constraints) are not tested in text generation. The benefit of out-of-order generation for open-ended text is not empirically shown.
- **The approximate training objective's impact is not analyzed**: The paper acknowledges the objective is biased but provides no analysis of the bias-variance tradeoff, no comparison to an exact (Monte Carlo) estimator even on a small scale, and no ablation showing how the bias affects generation quality.
- **Efficiency is a practical concern**: Figure 6 shows ILM is slower than ARM (without KV cache) at the same NLL. Combined with the inability to cache (unlike ARMs with KV cache), this makes the inference cost substantially higher, which limits practical applicability.

### Minor
- **The comparison to MDMs is limited to a single sampling strategy (tau-leaping)**: The related work discusses greedy and top-k unmasking strategies (Gong et al., Campbell et al.) that address the simultaneous-unmasking problem. Including these in the comparison would strengthen the claim that ILM's advantage is intrinsic rather than just relative to a poorly-tuned baseline.
- **The infilling evaluation uses a non-standard metric**: Percentage change in NLL is difficult to interpret absolutely. The paper shows delta-NLL improvement over MDM (e.g., -3.57 vs -0.49 on LM1B single-segment) but does not report raw NLL values, making it hard to gauge absolute quality. Comparison to standard infilling methods (e.g., FIM-trained ARMs) is missing.
- **Scaling behavior is not explored**: All experiments use models with ~85M non-embedding parameters. Whether the advantages of ILM hold at larger scales (e.g., 1B+ parameters) is an open question, especially given the worse scaling laws reported for MDMs.

### Trivial
None.

## Nice-to-Haves
- An ablation of the noising schedule (uniform across length vs. data-dependent).
- A small-scale experiment with an exact Monte Carlo training objective to quantify the bias introduced by the approximation.
- Wall-clock inference time comparisons (including ARMs with KV caching) to better contextualize the speed-quality tradeoff.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add an analysis of the approximate objective's bias, e.g., by training a small ILM on a tiny dataset with exact (high-variance) Monte Carlo and comparing the learned insertion distributions.
2. Include MDM baselines with greedy/top-k unmasking in the star graph and zebra experiments to show ILM's advantage over those more sophisticated MDM sampling strategies.
3. Report raw NLL values alongside the percentage changes in the infilling tables, and add a comparison to a FIM-trained autoregressive model on the single-segment infilling task.

## Score and Decision
The paper presents a well-motivated and technically sound approach that demonstrably addresses real limitations of both ARMs and MDMs on planning tasks. The star graph and zebra puzzle results are strong and clearly attributed to the model's design. However, the text generation results are not clearly better than ARMs, the training objective bias is unexamined, and the efficiency is a practical concern. Overall, the contribution is solid but not transformative—the paper convincingly carves out a niche where insertion-based generation excels but does not broadly surpass the best existing methods in language modeling.

MY FINAL SCORE: 6.5<score>6.5</score>
MY FINAL DECISION: Accept<decision>Accept</decision>