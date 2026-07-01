## Summary

This paper identifies an important limitation in time series forecasting: the "self-stimulation" assumption where models predict the future using only historical values, ignoring external influences that drive real-world systems. It formalizes this through a control-theoretic lens (Propositions 2.1, 3.1), introduces the Influence-Aware Time Series Forecasting (IATSF) paradigm, builds a leak-free temporally-synced benchmark with textual influences, and proposes FIATS—a lightweight, LLM-free model with novel channel-aware cross-attention mechanisms (CASM, CAPS). Experiments span synthetic, physics-based, traffic, and market datasets, showing FIATS outperforms self-stimulated baselines.

## Strengths

- **Well-motivated problem framing.** The paper correctly identifies the self-stimulation assumption as a fundamental limitation in current TSF practice, and the control-theoretic framing provides a clear vocabulary for discussing why ignoring external influences induces an error floor.
- **Leak-free benchmark design principles are a concrete methodological contribution.** The emphasis on temporal synchronization and the requirement that influences be genuinely independent of the target series (as opposed to summaries of it) addresses real flaws in existing multimodal TSF datasets.
- **FIATS is architecturally novel and genuinely LLM-free.** The CASM mechanism (channel descriptions as queries, textual influences as keys/values in cross-attention) and the CAPS decoder are principled designs that directly operationalize the paper's theoretical framework. In a space currently dominated by LLM-heavy approaches, having a model that processes text embeddings through purpose-designed numerical mechanisms is a practical contribution. The interpretability via attention maps is a nice plus.

## Weaknesses

### Fatal
None.

### Major

1. **No statistical uncertainty reported anywhere.** The paper makes strong comparative claims ("average MSE reduction of 36.0% on Atmospheric Physics and 44.3% on NYC Traffic Speed," "FIATS consistently outperforms all baselines") but reports zero standard deviations, confidence intervals, or multiple-seed results across all experiments. Without variance estimates, the reader cannot assess whether observed differences (e.g., FIATS 0.003 vs. PatchTST 0.006 on FM Toy pred len 14, or the 12.6% improvement on GAUD) are statistically meaningful or reflect random variation. For the controlled synthetic experiments, the absence of repeated trials is particularly hard to justify.

2. **GAUD dataset results lack absolute performance numbers.** The GAUD results (RQ3) are presented only as improvement percentages relative to PatchTST in a scatter plot (Figure 4), with no table of absolute MSE/MAE values. The paper claims "12.6% average improvement" and "ranks first on 59.6% of games," but without absolute error values, readers cannot evaluate the practical significance of these results or perform cross-model comparisons. This is a major evidential gap for an entire research question.

### Minor

3. **FIITS baseline is never defined.** The column "FIITS" appears in Table 1's header but is never described anywhere in the paper. It is unclear whether this is an ablation variant, a different encoder configuration, or something else. The comparison table is partially uninterpretable without this information.

4. **Rhetorical overclaiming on FM Toy.** The paper states that self-stimulated methods "fail spectacularly" on FM Toy, producing "collapsed, averaged-out forecasts." At the shortest horizon (pred len 14), PatchTST achieves 0.006 MSE (vs. FIATS 0.003). The gap grows substantially with longer horizons (3.6x at len 28, 4x at len 60, 6.2x at len 120), which does support the general thesis. However, the "fail spectacularly" rhetoric overstates the results for the easiest condition and could mislead readers about the strength of the evidence.

5. **Theoretical propositions are basic.** Propositions 2.1 and 3.1 correctly formalize the self-stimulation limitation and the benefit of incorporating influences, but they express standard facts from conditional expectation and variance decomposition (a model ignoring a source of variation converges to the conditional mean; conditioning on more variables reduces conditional variance). The contribution is in the framing and terminology for the TSF setting, not in new mathematical results. The paper's rhetoric ("control-theoretic analysis," "hard, mathematical barrier") overstates the theoretical depth relative to what is delivered.

### Trivial

6. **FIATS-Pretrained is mentioned in Figure 4 but never described.** The figure includes "FIATS-Pretrained" as a method on GAUD, but the paper never defines what pretraining entails or how this variant differs from the standard FIATS model.

## Nice-to-Haves

- Parameter counts, FLOPs, or a runtime comparison would substantiate the "lightweight" claim, which is currently stated but unquantified.
- For the weather-based datasets, analyzing how realistic weather forecast errors (rather than direct embedding corruption) affect results would strengthen the noise-robustness analysis.

## Removed Points

- **"FM Toy results contradict the paper's strongest claim"** — REMOVED. The critic speculated about information leakage in the FM Toy design without evidence. Across all four horizons, the gap between FIATS and the best self-stimulated model grows consistently (2x, 3.6x, 4x, 6.2x), supporting the paper's thesis. The critic cherry-picked only the shortest horizon. The "fail spectacularly" rhetoric is overclaimed (handled in Minor #4), but the results do not contradict the thesis.
- **"Figure 1 inconsistency with ablation"** — REMOVED. The parser-extracted alt-text is ambiguous and may not accurately represent the figure's actual labels. The figure shows a frequency-modulated system visualization; "FIATS w/o Influence" in that figure may refer to a test-time condition different from the "Zero News" training-time ablation.
- **"Full observability assumption is strong"** — REMOVED. The paper explicitly states "for analytical clarity" and acknowledges the simplification at line 43.
- **"Weather forecasts are predictions, not ground truth"** — REMOVED. The paper acknowledges this directly at line 113 ("Predictions of U_f from expert sources").
- **"Instantaneous influence effects assumption untested"** — REMOVED. The paper acknowledges this modeling choice and provides justification at line 113.
- **"Dataset descriptions are too vague"** — REMOVED. Deferring detailed descriptions to the appendix is standard practice.
- Typos, formatting, style nitpicks — REMOVED per instructions.
- Missing related works — REMOVED per instructions (no external confirmation possible).

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a perspective that the paper itself does not articulate.

## Suggestions

- Add standard deviations from 3–5 random seeds to all reported metrics.
- Add a table of absolute MSE/MAE values for GAUD across all compared methods.
- Define FIITS (or remove the column if it is not a meaningful baseline).
- Define FIATS-Pretrained and explain how it differs from standard FIATS.
- Calibrate the rhetorical claims to match the evidence (e.g., "self-stimulated models show substantially larger errors that grow with forecast horizon" rather than "fail spectacularly").
- Add parameter counts to substantiate the "lightweight" characterization.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>