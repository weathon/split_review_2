## Summary

This paper introduces Influence-Aware Time Series Forecasting (IATSF), arguing that the universal "self-stimulation" assumption—predicting future values from only historical observations—creates a mathematical performance ceiling. Through control-theoretic analysis, they formalize this limitation and show that incorporating external textual influences can break this barrier. They contribute a leak-free benchmark with temporally-synchronized textual influences, and FIATS, an LLM-free model featuring channel-aware mechanisms (CASM and CAPS) that learn channel-specific sensitivity to textual signals.

## Strengths

- **Clear and compelling motivation**: The paper frames a genuine and important problem—the marginal gains of sophisticated models over simple baselines in TSF—and offers a principled explanation rooted in dynamical systems theory. The control-theoretic framing, while elementary, provides useful vocabulary and formal structure for understanding why purely autoregressive models fundamentally cannot capture event-driven dynamics.

- **Principled benchmark design**: The emphasis on leak-free, temporally-synced textual influences is a valuable methodological contribution. The benchmark spans three tiers (toy systems, real-world physics/traffic, human-driven markets), enabling controlled validation of theoretical claims and testing on complex real-world problems. The explicit treatment of independence requirements (Section 4.1) and the discussion of influence prediction uncertainty (Appendix B.3 referenced) show careful design thought.

- **Strong empirical results across diverse domains**: FIATS achieves near-zero error on the FM toy (approaching the theoretical bound), 36% MSE reduction on Atmospheric Physics, 44% on NYC Traffic, and 12.6% average improvement on GAUD over PatchTST. These gains are consistent across synthetic, physics-based, and business datasets, suggesting genuine benefit from influence modeling rather than dataset-specific artifacts.

- **Interpretable architecture**: The CASM and CAPS mechanisms are well-motivated by the theoretical analysis (channel-specific sensitivity governed by $c^i B^j$). The attention map visualizations (Figures 3, 5) provide meaningful interpretability, showing how the model differentially attends to influences across channels.

- **Efficient LLM-free design**: By operating directly on text embeddings rather than prompting LLMs, FIATS demonstrates that principled influence modeling does not require billion-parameter language models, making the approach more practical and reproducible.

## Weaknesses

### Fatal
None.

### Major

- **Theoretical contributions are elementary restatements**: Proposition 2.1 (self-stimulation error bound) is essentially the well-known result that the conditional expectation minimizes MSE, and that $\text{Var}(X) = \text{Var}(\mathbb{E}[X|Y]) + \mathbb{E}[\text{Var}(X|Y)]$. Proposition 3.1 (partial influence efficacy) follows immediately from the additivity of variance for independent random variables. While the control-theoretic framing adds contextual value, presenting these as novel propositions (with proofs deferred to an appendix) overstates the theoretical contribution. The paper would be strengthened by acknowledging this connection to classical estimation theory while emphasizing the novel *application* and *systematic framework* aspects.

- **Largely unfair baseline comparisons**: The central experimental comparison pits FIATS (which uses textual influences) against self-stimulated models (DLinear, PatchTST, Chronos, MOIRAI, TimeMoE) that have no access to this information. Given the paper's core thesis that self-stimulation is fundamentally limited, demonstrating this against self-stimulated baselines is somewhat circular—the results validate the premise rather than the model. The only text-informed baseline, TimeLLM, is a single method designed for a different paradigm (prompting vs. structured influence modeling). A stronger evaluation would include more text-informed baselines, compare against simpler influence integration strategies (e.g., concatenating embeddings, FiLM conditioning), or show that FIATS outperforms alternatives *within* the IATSF paradigm.

- **Missing ablation on architectural design choices**: While ablations on embedding models and influence quality are provided, there is no ablation comparing CASM/CAPS against simpler alternatives for integrating textual influences. For instance, how much does the channel-aware cross-attention contribute versus simply concatenating a text embedding vector to the time series? This is important for understanding whether the gains stem from the *principled architectural design* or simply from *having access to textual information*.

### Minor

- **Practical deployment challenges underexplored**: The paper acknowledges that "ground-truth future influences are unavailable" in deployment but doesn't fully address this. For atmospheric physics, weather forecasts are readily available, but for GAUD (developer logs), the cold-start scenario assumes these logs exist before game launch. How general is this assumption? A discussion of the practical costs of obtaining and maintaining high-quality textual influences would strengthen the paper.

- **Limited comparison with existing exogenous variable methods**: The paper briefly mentions ARIMAX but doesn't compare against modern methods for incorporating exogenous variables (e.g., N-BEATS with exogenous inputs, or the Chronos-X paper cited in references). This would help situate IATSF relative to the broader landscape of influence-aware methods.

- **No confidence intervals or statistical significance**: All results are reported as single MSE values. Given the relatively small number of test samples in some datasets, error bars or multiple-run statistics would strengthen the empirical claims.

- **Channel descriptors as a practical requirement**: FIATS requires textual channel descriptions (e.g., "atmospheric pressure") for the CASM mechanism. While reasonable for physics systems, the paper doesn't discuss how this scales to systems with hundreds of channels or channels with non-obvious semantics.

### Trivial
None.

## Nice-to-Haves

- A comparison showing FIATS's performance when given noisy or imperfect influences (beyond the noise injection in Figure 6) versus having perfect influence information, to quantify the practical cost of influence uncertainty.
- Extension to standard benchmarks (ETT, Weather, etc.) to show whether IATSF can be applied even when no obvious textual influences exist (e.g., by constructing synthetic or LLM-generated influence descriptions).
- Analysis of computational overhead relative to baselines, since the paper claims FIATS is "lightweight."

## Novel Insights

The paper's central insight—that the field's stagnation may stem from the self-stimulation assumption rather than architectural limitations—is a genuinely important reframing. While the mathematical machinery is elementary, the systematic connection between control theory, the self-stimulation assumption, and the design of influence-aware models provides a coherent framework that could redirect research attention. The demonstration that even billion-parameter foundation models collapse on the FM toy when deprived of influence data is a powerful empirical statement about the limits of scale.

## Suggestions

- Strengthen the theoretical section by explicitly connecting to classical estimation theory (law of total variance, conditional expectation optimality) while emphasizing what is *new* in the framing—e.g., the system-theoretic interpretation, the implications for model design, and the formalization of partial influence efficacy for practical model building.
- Add ablations comparing CASM/CAPS against simpler influence integration strategies (concatenation, FiLM, additive bias) to isolate the contribution of the principled architecture.
- Include at least one additional text-informed baseline or a comparison showing how existing exogenous-variable methods perform when given the same textual (embedded) influences.
- Provide confidence intervals across multiple runs to strengthen empirical claims.

## Score and Decision

The paper presents a clear and compelling reframing of a core problem in time series forecasting, supported by a well-designed benchmark and strong experimental results. However, the theoretical contributions are overstated relative to their novelty, and the experimental methodology relies heavily on comparisons that are somewhat unfair by construction. The paradigm-level contribution is valuable, but the evidence would be more convincing with better-controlled comparisons within the IATSF paradigm and ablations isolating the architectural contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept