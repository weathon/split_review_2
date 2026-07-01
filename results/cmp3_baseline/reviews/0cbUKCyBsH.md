## Summary

This paper argues that time series forecasting has plateaued due to the "self-stimulation" assumption—predicting the future using only historical values while ignoring external influences. Using a control-theoretic framework, the authors prove this assumption imposes a mathematical error bound. To break this barrier, they propose Influence-Aware Time Series Forecasting (IATSF), introduce a leak-free benchmark with textual influences, and develop FIATS, a lightweight LLM-free model with channel-aware mechanisms. Experiments on synthetic, physics, and market datasets show FIATS significantly outperforms state-of-the-art self-stimulated baselines including large foundation models.

## Strengths

- **Novel problem framing**: The paper identifies and formalizes a genuinely fundamental limitation in time series forecasting—the self-stimulation assumption—and provides a rigorous control-theoretic analysis (Proposition 2.1, Proposition 3.1) that explains why even billion-parameter models hit a performance ceiling.
- **Clean theoretical grounding**: The error bound analysis (Eq. 3, Eq. 4) and the proof that incorporating any measurable influence reduces error covariance (Eq. 6) provide a principled foundation for the entire framework. This moves beyond ad-hoc multimodal approaches.
- **Well-designed validation**: The benchmark includes controlled toy systems (where the theoretical lower bound is known) alongside complex real-world systems, enabling unambiguous attribution of gains to influence modeling rather than architectural complexity.
- **Principled model design**: FIATS is designed from first principles (CASM for channel-specific sensitivity, CAPS for channel-aware decoding) rather than retrofitting LLMs, and the ablations cleanly isolate the contribution of each component.
- **Strong empirical results**: FIATS achieves dramatic improvements on FM Toy (near-zero error vs. failed baselines), 36% MSE reduction on Atmospheric Physics, and 44% on NYC Traffic, with consistent gains across settings.

## Weaknesses

### Major

- **Limited scope of influence types**: The paper focuses exclusively on textual influences via weather reports and developer logs. Many real-world forecasting problems involve numerical exogenous variables, categorical interventions, or irregularly-sampled events. The approach's generalizability beyond text-heavy domains (e.g., industrial sensor data, financial tick data) is unclear.
- **No comparison with structured exogenous variable methods**: The paper compares against self-stimulated models but not against classical time series methods that natively handle exogenous variables (ARIMAX, VARX, or modern deep learning approaches that incorporate numerical exogenous features). This missing baseline makes it difficult to assess whether textual influence provides unique value beyond what standard exogenous variable methods already offer.
- **Potential data leakage concerns**: The benchmark uses weather forecasts as influences for physics data. Since weather forecasts are themselves model predictions that may have been trained on historical observations of the same physical variables, there is a risk of information leakage about the future through the "influence" channel. The paper's "leak-free" claim needs closer scrutiny for the Atmospheric Physics dataset.

### Minor

- **Proposition 3.1 assumes independence of influences**: The claim that incorporating any single influence reduces error by a fixed amount assumes influences are independent (U_t = sum U_t^i). In practice, influences may be correlated, and the additive error reduction may not hold.
- **FIATS architecture description is dense**: The CASM mechanism, its relationship to linear system sensitivity (c^i B^j), and the CAPS decoder could benefit from clearer exposition or a step-by-step algorithmic description.
- **No analysis of computational cost**: While FIATS is described as "lightweight," the paper provides no parameter counts, FLOPs, or runtime comparisons against baselines, making it hard to assess the practical efficiency advantage.

### Trivial

- The "FIITS" baseline in Table 1 is mentioned but not defined in the main text; it appears to be FIATS without influence, but this should be explicit.

## Nice-to-Haves

- Adding numerical exogenous variable baselines (e.g., DLinear with Weather features as numerical inputs) would strengthen the claim that textual influences specifically are valuable, not just any external information.
- A discussion of how to handle stale, missing, or temporally misaligned influence inputs during deployment would increase practical utility.

## Novel Insights

The central insight—that the self-stimulation assumption places a provable mathematical ceiling on forecasting accuracy, and that this ceiling can be systematically lowered by incorporating textual influence signals—is genuinely novel and reframes the time series forecasting research agenda. The connection between attention mechanisms in transformers and channel-specific sensitivity matrices from control theory (c^i B^j → query-key-value formulation) is an elegant theoretical-to-architectural mapping that goes beyond typical "attention is all you need" application. The empirical demonstration that a simple, principled model can outperform massive pretrained foundation models on systems where external influences matter is a significant result that challenges the current scaling-centric trajectory of the field.

## Suggestions

- Add a comparison against a variant of FIATS or DLinear that uses weather variables as numerical exogenous inputs instead of text, to isolate the benefit of the textual modality.
- Analyze and report whether the attention patterns in CASM block correspond to physically meaningful sensitivity weights for the Atmospheric Physics dataset (e.g., does the "pressure sentence" indeed get high weight for pressure channels?).

## Score and Decision

Score: 8 - Accept

This is a strong paper with a clean theoretical contribution, well-designed experiments, and results that genuinely advance the field's understanding of time series forecasting limitations. The weaknesses (missing numerical exogenous baselines, potential leakage concern) are addressable and do not invalidate the core claims.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>