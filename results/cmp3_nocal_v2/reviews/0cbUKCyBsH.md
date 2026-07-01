## Summary

This paper identifies the "self-stimulation" assumption in time series forecasting (predicting future solely from past values of the same series) as a fundamental limitation, arguing it treats unobserved external influences as noise and thereby imposes an irreducible error bound. The authors introduce Influence-Aware Time Series Forecasting (IATSF), a paradigm that augments forecasting with textual influence information. They provide a control-theoretic analysis (Propositions 2.1 and 3.1), a "leak-free" benchmark with temporally-synced textual influences, and FIATS — a lightweight, LLM-free model with a Channel-Aware Adaptive Sensitivity (CASM) mechanism. Experiments on synthetic, physics, traffic, and gaming datasets show FIATS outperforming standard TSF baselines that lack influence information.

## Strengths

1. **The self-stimulation critique is well-articulated and addresses a genuine limitation.** Section 2's framing of standard TSF as a dynamical systems problem (Eq. 1–2) makes explicit an assumption that practitioners have long recognized but lacked a formal vocabulary for. The "self-stimulation" terminology is memorable and captures a real issue: models that predict the future from only the past cannot anticipate the effects of external events not encoded in the historical series.

2. **The leak-free benchmark design is a principled methodological contribution.** Section 4.1's requirement that influences must be *independently* evolving — not retrospective summaries of the time series they are meant to predict — directly addresses a real leakage problem in prior multimodal TSF datasets (e.g., Time-MMND, GPT4MTS). This principle is concretely operationalized in the benchmark, and the community should adopt it.

3. **The CASM mechanism is thoughtfully designed and its contribution is isolated by ablation.** Using channel descriptions as queries to learn channel-specific sensitivity to textual influences (Section 5) is architecturally elegant. The ablation in Table 3 ("Zero Desc." vs. "Zero News") convincingly shows that *both* the influence input and the channel-conditioning mechanism contribute to performance, which is a nontrivial architectural finding.

## Weaknesses

### Fatal

None.

### Major

1. **"FIITS" appears in Table 1 but is never defined in the main paper.** This column is presented alongside FIATS, DLinear, PatchTST, etc., but the reader cannot determine whether FIITS is (a) an ablated version of FIATS without influences, (b) a variant with a different architecture, or (c) something else. The figure caption references "FIATS w/o Influence" but does not connect this to "FIITS." The ablation section (6.4) discusses "Zero News" but never mentions FIITS, so the reader cannot triangulate. This is a basic reporting gap that makes the results in Table 1 partially uninterpretable.

2. **The paper's architectural claim — that performance gains "stem from principled influence modeling, not architectural complexity" (abstract) — is not fully supported by the experimental design.** The main comparison (Table 1) pits FIATS, which receives textual influence information, against standard TSF baselines (DLinear, PatchTST, Chronos, MOIRAI, etc.) that receive *only* historical time series data with *no* influence information. This comparison validates the thesis that *having* external influence information helps, but it does not demonstrate that FIATS's *specific architectural approach* to incorporating that information is better than alternatives. The paper would need to compare against models that also receive the same influence data:
   - **As numerical exogenous variables** (e.g., DLinear+exog, PatchTST+exog), to test whether textual representation adds value over a simpler numerical encoding of the same information (e.g., weather forecasts → temperature, precipitation).
   - **Against ChronosX** (Arango et al., 2025), which is *designed* for exogenous-variable time series forecasting and is cited in the paper (lines 15, 99) but never used as a baseline.
   
   The ablation "Zero News" (removing influence input) shows that the influence information is necessary, but does not show that FIATS's *method* of incorporating it is superior. The "Zero Desc." ablation comes closer, but isolates only the channel-conditioning component. Without the missing controls, the paper's central architectural claim is not convincingly supported.

3. **No measures of variance or statistical significance are reported.** Every result in Table 1 is a single MSE value, with no standard deviations, confidence intervals, or multi-seed runs. Some claimed margins are small (e.g., Electricity Utility pred_len 96: FIATS 0.124 vs. PatchTST 0.130 — a ~4.6% gap), making it impossible to assess whether differences are statistically meaningful. The same applies to the GAUD results (Figure 4) and the ablations (Table 3). While single-run evaluation is common in some large-benchmark settings, it weakens the paper's quantitative claims, especially given the strong language ("decisively validate," "consistently outperforms").

### Minor

1. **The theoretical contribution (Propositions 2.1 and 3.1) reformulates standard statistical facts rather than providing novel insight.** Proposition 2.1 — that omitting relevant variables increases prediction error variance — is a straightforward consequence of treating unobserved variables as random noise, which has been understood in statistics, econometrics, and control theory for decades. Proposition 3.1 — that adding any relevant variable reduces error — is similarly immediate from the setup. The paper presents these as a "hard mathematical barrier" and a novel discovery, but they are formalizations of well-known principles (omitted variable bias, variance reduction from additional features). The control-theoretic framing is pedagogically useful, but it does not constitute a significant formal contribution.

2. **The paper argues for textual over numerical influences (Section 3.2) but never directly tests this premise.** The main experimental datasets (Atmospheric Physics, NYC Traffic) use weather forecasts — which are inherently quantifiable (temperature, wind speed, precipitation amount). The paper asserts that textual representation captures "qualitative or uncertain dynamics missed by traditional variables" (abstract) and handles "non-quantifiable events" (line 15), but never demonstrates a case where text is genuinely necessary or beneficial over a numerical encoding of the same information. A direct ablation (text vs. numerical encoding of identical weather forecast data) would substantiate this core design choice.

3. **The FM Toy experiment does not discriminate between the paper's architectural claims and a trivial "oracle access" explanation.** The dataset is constructed so that the influence *completely* determines the signal frequency, and FIATS (which receives this influence) achieves near-zero error. While this serves as a controlled validation that influence information can help, it does not distinguish FIATS's specific mechanism from any other method that could read the same input. A more informative test would involve corrupting the influence at varying noise levels and comparing FIATS against a simpler model (e.g., linear regression on influence + history) to see whether FIATS's architecture recovers the signal more robustly.

4. **The claim that "even billion-parameter foundation models struggle to outperform simple linear baselines" (introduction) is presented as settled fact** but is contested in the TSF literature; several subsequent works have shown that proper evaluation protocols reduce or eliminate this gap. The paper overstates this premise.

### Trivial

None.

## Nice-to-Haves

- Compare FIATS against standard TSF models that receive the same influence information as numerical exogenous variables, to isolate the benefit of textual representation.
- Benchmark against ChronosX (Arango et al., 2025), the most directly relevant baseline for exogenous-variable TSF.
- On the FM Toy dataset, test with corrupted/noisy influence signals and compare against a simple model (e.g., linear regression on influence + history) to assess whether FIATS's architecture provides robustness benefits.
- Report standard deviations or confidence intervals from multiple seeds.
- Clarify what "FIITS" denotes in Table 1.

## Removed Points

These points were flagged in the harsh critic review but are removed here; treat them with caution:

- **"Atmospheric Physics weather-forecast circularity" (Section 4.2 note):** The critic argues that weather and atmospheric physics are causally coupled, undermining the "independent influence" requirement. However, the paper defines independently evolving influences as *external factors that are not outcomes of the system* (line 111). Weather forecasts from meteorological models are external to the measurement system for the atmospheric physics variables — they are predictions from a separate source, not retrospective summaries of the target series. This criticism misunderstands the paper's benchmark design principle.
- **"Weather forecast archival availability" (Section 5 note):** The critic speculates about whether 2014–19 weather forecasts were archived. This is a logistical question about dataset construction that is not verifiable from the paper as written and should not be treated as a demonstrated flaw.
- **"Table 2 missing from main text":** The parser strips appendix content from all papers. Table 2 exists in the original submission; this is not a weakness of the paper.
- **"Ablation should keep influence info but use simpler mechanism":** This is a constructive suggestion for strengthening the paper, not a demonstrated flaw. It has been moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's primary insight — that the experimental design does not adequately separate the benefit of *having* influence information from the benefit of FIATS's *specific architecture* for using it — is a real methodological gap, but it is a critical observation about the paper's evaluation rather than a novel insight about the subject matter.

## Suggestions

1. Define FIITS explicitly (or remove it from the table if it is redundant with the "Zero News" ablation).
2. Add a controlled experiment where standard TSF baselines receive the same influence information as numerical features (e.g., DLinear+exog, PatchTST+exog), and benchmark against ChronosX. This would directly test whether FIATS's textual processing and channel-aware architecture provide measurable benefits over simpler alternatives.
3. Report variance estimates (multiple seeds, confidence intervals) for all quantitative results.
4. Add an explicit test comparing text vs. numerical encoding of identical influence information to substantiate the motivation for textual influences.
5. Tone down the claims about the theoretical propositions being a "hard mathematical barrier" and clarify that they formalize known principles in the specific TSF context.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>