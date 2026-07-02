## Summary

This paper studies how a decision maker should act when given predictions that satisfy only partial (ℋ-)calibration guarantees, rather than the intractable full calibration. The authors characterize the minimax-optimal decision rule via a duality argument, showing that when the calibration class includes the decision-calibration indicators (a tractable condition), the optimal policy collapses to simply best-responding to the raw predictions—the same as under full calibration. For weaker guarantees, the optimal robust policy remains efficiently computable, and the paper provides empirical validation on regression tasks using a self-orthogonality condition that arises naturally from squared-error training.

## Strengths

- **Novel and well-motivated framing**: The paper addresses a genuine practical gap—full calibration is intractable in high dimensions, yet weaker calibration notions lack clear decision-theoretic semantics. The robust minimax lens is a principled way to bridge this gap, and the paper is the first to apply it to partially calibrated high-dimensional forecasts.

- **Sharp theoretical result**: Theorem 4.1 and Theorem 4.2 identify a precise threshold (decision calibration) at which the minimax-optimal policy becomes the simple plug-in best response. This "collapse" is surprising and practically significant—it means a tractable, low-dimensional calibration condition suffices for the same decision-theoretic trustworthiness as full calibration.

- **Clean characterization and efficient computation**: Theorem 3.1 provides a closed-form characterization of the optimal robust policy via dual variables, and the resulting optimization is low-dimensional and efficiently solvable for finite ℋ. The paper also derives simple closed-form policies for practically relevant special cases (self-orthogonality from squared loss, bin-wise calibration).

- **Empirical validation**: The experiments on two regression datasets confirm the theoretical predictions: the robust policy outperforms the plug-in rule under adversarial distributions consistent with the calibration constraints, and the cost of robustness under i.i.d. conditions is mild.

## Weaknesses

### Major

- **The "self-orthogonality" guarantee (Proposition 4.4) is approximate in practice, but the theory assumes exact ℋ-calibration.** The experiments use a two-layer MLP trained to approximate stationarity of squared loss, which will only approximately satisfy the moment conditions. The paper acknowledges this implicitly but does not analyze how approximate ℋ-calibration affects the minimax guarantees. The appendix mentions approximate calibration but the main text and experiments rely on exact guarantees. This gap between theory and practice is significant for the empirical claims.

- **The experimental evaluation is limited in scope.** Only two regression datasets are used, both with small action sets (3 actions). The utility functions are hand-specified and the adversarial distributions are constructed from the dual solution rather than representing realistic distribution shifts. The paper would benefit from experiments with larger action spaces, multiclass outcomes, and comparisons to baselines beyond the simple plug-in rule (e.g., other robust decision rules or post-hoc recalibration methods).

- **The paper does not compare against existing practical approaches.** For practitioners who cannot achieve decision calibration, the paper recommends using the robust policy derived from self-orthogonality or bin-wise calibration. However, there is no comparison against simple baselines like Platt scaling, temperature scaling, or isotonic regression followed by best response. It is unclear whether the robust policy offers meaningful gains over these simpler alternatives in practice.

### Minor

- The paper assumes the decision maker knows the exact ℋ-calibration class and that the forecaster satisfies it perfectly. In practice, the decision maker may need to estimate which ℋ holds from data, introducing statistical uncertainty that is not addressed.

- The "sharp transition" result (Theorems 4.1-4.2) is elegant but the practical implications are somewhat limited: if a forecaster is already decision-calibrated, the decision maker can simply best-respond; if not, the robust policy requires solving an optimization problem that depends on the specific ℋ. The paper does not provide guidance on how to choose ℋ when multiple candidate classes are available.

### Trivial

- Figure 1 and Figure 2 are described in the text but the captions are garbled (likely a parser issue). The content is still understandable.

## Nice-to-Haves

- An analysis of the sample complexity of estimating the dual variables λ* from finite calibration data would strengthen the practical applicability.
- Experiments with multiclass classification (where decision calibration is most relevant) would significantly broaden the impact.
- A discussion of how to handle the case where the decision maker has multiple candidate ℋ classes and must choose among them (e.g., via model selection on a validation set).

## Novel Insights

Beyond the paper's own contributions, the key insight is that the decision-theoretic value of calibration is not monotonic in the richness of the test class—there is a sharp threshold at decision calibration. This suggests that the "trustworthiness" of predictions is not a continuous spectrum but rather a discrete property that can be achieved with relatively weak guarantees. This has implications for how practitioners should think about calibration: rather than striving for full calibration (which is often impossible), they should target decision calibration for their specific decision problem, which is both tractable and sufficient for optimal decision-making in the minimax sense.

## Suggestions

- Add a theoretical analysis of approximate ℋ-calibration (e.g., with ε error in the moment conditions) and how it affects the minimax guarantees. This would directly address the gap between theory and practice.
- Include experiments with multiclass outcomes and larger action sets to demonstrate scalability and generality.
- Compare the robust policy against simple post-hoc recalibration baselines (e.g., histogram binning + best response) to quantify the practical value of the proposed approach.

## Score and Decision

The paper makes a novel and theoretically sound contribution to an important problem (decision-making with partially calibrated forecasts). The main theoretical results are clean and surprising, and the framework is well-motivated. However, the empirical evaluation is limited and does not fully bridge the gap between the exact theoretical guarantees and the approximate nature of real-world calibration. The paper would benefit from stronger empirical validation and analysis of approximate calibration before acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>