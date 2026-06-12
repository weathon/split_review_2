## Summary
This paper proposes integrating n-gram induction heads (from Akyürek et al., 2024) into transformers for in-context reinforcement learning (ICRL), building on Algorithm Distillation. The core claims are that these n-gram layers reduce data requirements (up to 27×), decrease hyperparameter sensitivity, and can be extended to image observations via vector quantization. Experiments are conducted on Dark Room, Key-to-Door, and Miniworld environments using an Expected Maximum Performance (EMP) evaluation protocol.

## Strengths
- **Well-motivated method with clear connection to theory**: The approach is grounded in established findings on induction heads and simplicity bias in transformers (Olsson et al., Edelman et al., Akyürek et al.), providing a principled motivation for why n-gram layers should help in the ICRL setting.
- **Honest evaluation protocol**: Using EMP with random hyperparameter search rather than cherry-picked best runs is commendable and provides a realistic picture of each method's practical usability. This is a more informative evaluation than what many papers use.
- **Good ablation design**: The permuted n-gram mask experiment (Table 1c) is a thoughtful sanity check demonstrating that the improvement comes from meaningful n-gram matching rather than architectural changes alone. The ablations on n-gram length and position (Tables 1a, 1b) show the method is robust to its own hyperparameters.
- **Extension to visual observations**: The use of vector quantization to adapt n-gram matching to image-based environments is a reasonable engineering contribution that broadens applicability.

## Weaknesses
### Fatal
None.

### Major
- **Experiments limited to toy environments**: Dark Room is a 9×9 grid with a single goal cell; Key-to-Door adds a key and door on a similar grid; Miniworld variants are slightly more complex but still very simple 3D rooms. None of these approach the complexity of standard ICRL benchmarks like XLand-Minigrid or even basic Atari-like tasks. The paper acknowledges this limitation but does not address it. Given that the core claim is broad efficiency improvements, the experimental scope is insufficient to support it convincingly.
- **Shallow mechanistic analysis**: The paper hypothesizes that n-gram heads help because they circumvent simplicity bias and the transient nature of in-context learning, but provides no evidence for this mechanism in the RL setting. Are the n-gram patterns that emerge meaningful for RL (e.g., matching goal-approach subsequences)? How do the attention patterns differ between baseline and n-gram models? Without this analysis, the paper remains a "plug in existing NLP technique to RL and observe improvement" work without explaining *why* it helps, which limits the transferability of insights.
- **Data efficiency claims need qualification**: The "27× less data" claim compares against AD's reported setting of 2048 goals with full learning histories, but the authors' own method still requires 100 goals with 500–1000 learning histories in Key-to-Door. The comparison conflates task diversity with data volume. Moreover, the additional compute for VQ pretraining and the overhead of n-gram matching at inference are not accounted for in the efficiency comparison.

### Minor
- **VQ model details and sensitivity**: The VQ encoder-decoder architecture, training procedure, and codebook size are not described. The quality of n-gram matching for images depends entirely on how well VQ clusters correspond to true state equivalence classes, and no analysis is provided on this critical component.
- **Incomplete environment specification**: The number of environment steps per episode, reset behavior, and goal sampling distributions are only partially described, making reproduction difficult.
- **Figure 5 compares different goal counts**: In Miniworld-Dark, NGH uses 50 goals while baseline uses 60, which is a minor but unnecessary confound in an otherwise careful evaluation.

### Trivial
None.

## Nice-to-Haves
- An analysis of what n-gram patterns the model learns in RL sequences (e.g., visualizing attention patterns to understand which subsequences are matched)
- Experiments on at least one more complex environment to demonstrate broader applicability
- Comparison against other ICRL baselines beyond Algorithm Distillation (e.g., Decision Transformer variants or other in-context approaches)

## Novel Insights
The paper's genuinely novel contribution is the demonstration that structural inductive biases from the NLP induction head literature can meaningfully transfer to the in-context RL setting, and that vector quantization can bridge the gap between discrete n-gram matching and continuous observation spaces. The finding that n-gram layers introduce negligible hyperparameter overhead (Table 1a,b) while significantly reducing sensitivity to the base transformer's hyperparameters is a useful practical insight. However, beyond the paper's own framing, no deeper novel insight emerges about why sequential pattern matching is particularly beneficial for RL versus other domains.

## Suggestions
- Expand experiments to at least one complex benchmark (e.g., XLand-Minigrid, a subset of Meta-World, or an Atari-style environment) to substantiate the generality of claims.
- Add mechanistic analysis: visualize what n-grams the model matches in RL trajectories and how this relates to task-relevant structure (e.g., do matched subsequences correspond to goal-reaching behaviors?).
- Provide a fairer compute-equivalent comparison: account for VQ pretraining cost and n-gram computation overhead when claiming efficiency gains.
- Describe VQ architecture and training in detail so the image-based results are reproducible.

## Score and Decision

MY FINAL SCORE: 4.0
MY FINAL DECISION: Reject