## Summary

The paper introduces Insertion Language Models (ILMs), which generate sequences by inserting one token at a time at arbitrary positions, learning jointly the position and vocabulary element. ILMs address two key limitations of existing approaches: the fixed left-to-right order of autoregressive models (ARMs) and the fixed-length constraint of masked diffusion models (MDMs) (which cannot handle unknown infill lengths). The authors propose a biased denoising training objective that avoids high-variance marginalization, along with a transformer parameterization and a dedicated stop classifier. Empirical evaluation on planning tasks (star graphs, zebra puzzles) shows ILMs outperform both ARMs and MDMs, and on text generation/infilling tasks ILMs are competitive with ARMs and better than MDMs while offering greater flexibility for arbitrary-length infilling.

## Strengths

- **Novel and principled formulation of insertion-based generation.** The paper revisits the idea of generation by insertion and develops a practical training framework that overcomes the high variance of naive marginalization. The target insertion distribution derived from counting is a clever way to amortize the denoising signal.
- **Clear demonstration of failure modes on planning tasks.** The star graph experiments (easy/medium/hard) convincingly show where ARMs (fixed order) and MDMs (fixed length, absolute positions) fail, and where ILMs succeed due to out-of-order generation and relative position modeling. The zebra puzzle results further support this.
- **The model naturally handles arbitrary-length infilling without special training.** The ILM's ability to insert tokens anywhere and to decide when to stop directly addresses a known limitation of MDMs, which require a fixed number of mask tokens. The infilling results on LM1B and TinyStories confirm this advantage.
- **Well-designed evaluation with appropriate metrics.** The use of Llama-3.2-3B NLL and Prometheus LLM judge for text quality, plus percentage-change metrics for infilling, provides a solid assessment beyond simple perplexity.

## Weaknesses

### Major

1. **The training objective is a biased approximation without theoretical analysis.** The paper acknowledges that the naive denoising objective has high variance and replaces it with a counting-based target distribution, but it does not analyze the bias-variance tradeoff or provide guarantees about the quality of the approximation. This leaves open the question of whether the objective could fail on more complex data distributions.
2. **Language modeling results are not strongly superior to ARMs.** While ILMs perform better than MDMs, ARMs still achieve lower NLL on both datasets. The main claimed advantage is flexibility (infilling), but the paper does not compare with alternative flexible approaches such as fill-in-the-middle ARMs (Bavarian et al., 2022) or other insertion-based models trained with different objectives (e.g., a more standard Insertion Transformer). This weakens the case for ILM as a general language model.
3. **The MDM baseline uses only the vanilla sampler.** Recent MDM variants (greedy unmasking, flow-based sampling, token-wise reweighting) could potentially reduce the simultaneous-unmasking problem and improve infilling. By not including these baselines, the paper understates the potential of MDMs and makes the comparison less informative.

### Minor

4. **Limited ablation studies.** The paper does not ablate key design choices: the effect of the stop loss, the impact of the number of dropped tokens \(n\), or the choice of two-step sampling vs. joint sampling. Such ablations would strengthen the empirical understanding of ILMs.
5. **The stop classifier is somewhat ad-hoc.** The model uses a learned binary stop predictor trained on the full sequence (all zeros bit vector). It is unclear whether this generalizes well to sequences longer than those seen during training, or whether an EOS-token approach would work as well (the Insertion Transformer baseline uses EOS and performs poorly—why?).
6. **The paper does not analyze inference efficiency in depth.** Figure 6 shows per-token time vs. NLL for MDM and ILM, but the ARM comparison uses a model without KV-cache. ARM with KV-cache would be much faster. The paper acknowledges this limitation but does not quantify the practical cost.

## Nice-to-Haves

- Ablation on the number of dropped tokens \(n\) and how it affects training stability and generation quality.
- Comparison with the greedy MDM sampler (unmasking one token at a time) to isolate the effect of the training objective from the inference procedure.
- Theoretical analysis or empirical study of the bias introduced by the counting-based objective (e.g., on a small controlled setting).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide a theoretical or empirical analysis of the bias-variance tradeoff in the proposed training objective. This would add confidence in the method's foundations.
2. Include a stronger MDM baseline that uses a sequential unmasking strategy (e.g., unmasking the most confident token at each step) to show whether the advantage of ILMs persists against a more competitive MDM.
3. Add ablation studies on the loss components (stop loss, insertion loss) and on the effect of the noise distribution (uniform over \(n\)).

## Score and Decision

**Score:** 6.5 (between borderline accept and accept; the paper makes a solid contribution but has notable weaknesses in scope and theoretical depth)

**Decision:** Accept

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>