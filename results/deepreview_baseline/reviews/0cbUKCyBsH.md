## Summary

This paper identifies a fundamental limitation in time series forecasting: the widespread "self-stimulation" assumption, where models predict future values using only historical data, ignoring external influences. Through a control-theoretic analysis, the authors prove that this assumption imposes an irreducible error bound. They propose a new paradigm, Influence-Aware Time Series Forecasting (IATSF), introduce a leak-free benchmark with textual influences, and develop FIATS—a lightweight, LLM-free model that uses channel-aware cross-attention to incorporate external textual signals. Experiments on synthetic, atmospheric physics, traffic, and game user datasets show substantial improvements over self-stimulated baselines, including large pre-trained models.

## Strengths

- **Clear problem framing**: The paper convincingly argues that ignoring external influences is a key bottleneck in time series forecasting, and formalizes this as the "self-stimulation" assumption. This reframing is timely and relevant given the field's observed plateau.
- **Theoretical grounding**: Propositions 2.1 and 3.1 provide a formal control-theoretic justification for why incorporating external influences can reduce forecast error. While not mathematically deep, this explicit linking of omitted-variable bias to forecasting performance is a useful pedagogical contribution.
- **Well-designed benchmark**: The Temporal-Synced IATSF benchmark is carefully constructed to avoid information leakage, uses realistic temporal synchronization, and covers diverse domains (toy, physics, traffic, games). This will be a valuable resource for the community.
- **Principled and lightweight model**: FIATS is cleanly designed around the theoretical insights (CASM for channel-specific sensitivity, CAPS for decoding). The model is LLM-free, efficient, and interpretable via attention maps. Ablation studies convincingly show that the performance gains come from the influence channels and the CASM mechanism, not from increased model capacity.
- **Strong empirical results**: FIATS consistently outperforms all self-stimulated baselines by large margins (e.g., 36% MSE reduction on Atmospheric Physics, 44% on NYC Traffic) and also beats a text-based LLM method (TimeLLM). The cold-start advantage on the GAUD dataset is particularly compelling.

## Weaknesses

### Fatal

- **Missing critical baselines**: The paper does not compare against any method that uses numerical exogenous variables (e.g., ARIMAX, VARX, or a simple deep model with numeric weather features concatenated as inputs). Such baselines are essential to isolate the benefit of *textual* influence representations over numeric ones. Without them, the paper's claim that textual influences are the "primary path forward" is unsubstantiated—the gains could be equally achievable by feeding numeric weather forecasts into a standard model. This omission severely undermines the core contribution.

### Major

- **Overclaimed theoretical novelty**: Proposition 2.1 (the "self-stimulation barrier") is a direct consequence of omitted-variable bias in estimation—a well-known statistical fact. The paper presents it as a profound, hard barrier, but any first-year econometrics student can state that ignoring relevant variables inflates error. The control-theoretic dressing does not add depth. This overclaiming weakens the paper's narrative and credibility.
- **Potential information leakage in the benchmark**: The weather reports used as influences for the Atmospheric Physics dataset may be derived from weather forecast models that themselves depend on past atmospheric observations (the same variables being forecast). The paper asserts the influences are "independently evolving," but weather and atmospheric dynamics are tightly coupled. Without a rigorous argument that the weather text does not contain future information about the target series (e.g., by using only forecast sources that are independent of the historical time series used for evaluation), the leak-free claim is questionable.
- **Overly strong conclusions**: The paper states that "modeling external influences is not just an incremental improvement but the primary path forward for meaningful progress." This ignores the many real-world scenarios where time series are approximately autonomous or where it is difficult to obtain reliable external influence data. The claim is too bold and not properly contextualized.

### Minor

- The FIATS model architecture, while clean, relies on standard cross-attention and does not introduce fundamentally new mechanisms beyond the specific application. The novelty lies more in the paradigm than in the model itself.
- The benchmark datasets are relatively small and domain-specific (weather, traffic, games). Generalization to other important domains (e.g., finance, energy, healthcare) is not demonstrated.
- Experimental details about the construction of the textual influences (e.g., exact source of weather reports, how they were converted to text, how game logs were formatted) are not fully described in the main paper (likely in appendix, which is excluded from review).

### Trivial

- Figure 1 caption is duplicated and the figure quality is low.
- Some grammatical and formatting issues (e.g., "Collasped" in Figure 1).

## Nice-to-Haves

- Add experiments with numerical exogenous variables (e.g., numeric weather forecasts for temperature, humidity, wind) fed into a simple linear model or a standard TSF model. This would directly test whether text is necessary or if numeric data suffices.
- Provide a statistical test (e.g., Granger causality) to demonstrate that the textual influences contain information not already present in the time series history, strengthening the leak-free argument.
- Discuss the conditions under which self-stimulated models are sufficient (e.g., stationary, seasonal, or high-frequency series) to properly bound the claims.
- Release the benchmark datasets and code publicly to facilitate reproducibility and further research.

## Novel Insights

Beyond the paper's own contributions, the key insight is that textual influence descriptions can be systematically integrated into forecasting via a theoretically motivated attention mechanism that learns channel-specific sensitivities. This bridges the gap between unstructured text and structured forecasting in a principled way, and the attention maps provide a form of interpretability that connects external events to predicted dynamics. The paper also highlights that even perfect self-stimulated models are inherently limited when the system is perturbed by external forces, making this not just an engineering fix but a necessary paradigm shift for certain domains.

## Suggestions

1. **Add numerical exogenous baselines**: Without these, the contribution of textual influences over numeric ones is unknown. This is the single most important addition.
2. **Tone down the theoretical claims**: Acknowledge that the "barrier" is a known property and that the contribution is in applying it to motivate a new paradigm and benchmark, not in discovering a new mathematical bound.
3. **Provide more evidence for leak-free design**: Show that the weather reports are generated from independent data (e.g., from forecasts made at an earlier time using global models not trained on the specific station data) or perform a leakage detection experiment (e.g., train a model to predict the weather text from past time series and measure if it succeeds).
4. **Include a discussion of limitations**: When is influence information hard to obtain? How robust is FIATS to missing or misaligned influences? This would strengthen the paper.

## Score and Decision

The paper addresses an important limitation, provides a useful benchmark and a clean model, and presents strong empirical results. However, the critical omission of numerical exogenous baselines makes it impossible to assess the true contribution of textual influence modeling. Combined with the overclaimed theoretical novelty and potential leakage concerns, the paper does not yet meet the standard for acceptance. The strengths—especially the benchmark and the IATSF paradigm—are valuable, but the evaluation is incomplete.

**Score**: 4.0

**Decision**: Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>