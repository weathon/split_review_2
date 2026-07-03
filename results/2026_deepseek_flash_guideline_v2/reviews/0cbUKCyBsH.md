Based on my careful analysis of the paper, let me now produce the final consolidated review. The calibration tool encountered a persistent file system error, so I will proceed with my best judgment calibrated against my knowledge of the ICLR reviewing standards.

---

## Summary

This paper introduces Influence-Aware Time Series Forecasting (IATSF), a paradigm that breaks the standard "self-stimulation" assumption in time series forecasting (predicting the future using only historical values) by explicitly incorporating external textual influences. The authors provide a control-theoretic analysis proving that self-stimulated models face an irreducible error bound, introduce a leak-free benchmark with temporally-synced textual influences across synthetic, physics-based, and market datasets, and propose FIATS, a lightweight LLM-free model with channel-aware mechanisms (CASM and CAPS) for incorporating textual influence information. Experiments show FIATS substantially outperforming standard baselines and foundation models across all datasets.

## Strengths

1. **Formal theoretical framing of a real limitation.** Proposition 2.1 gives a control-theoretic proof that any model using only historical time series data has a hard lower bound on prediction error due to unobserved external influences (Eq. 3–4). While the underlying mathematics is a standard property of conditional expectation, the paper's contribution is in explicitly formalizing this for the TSF domain and using it to motivate a concrete design paradigm. The connection is clearly articulated and useful.

2. **Leak-free benchmark with explicit design principles.** The benchmark (Section 4) explicitly defines criteria for temporal synchronization and independence of influences, directly addressing a genuine problem with prior multimodal TSF datasets that may leak future state information. The datasets span synthetic, physics-based, and human-driven systems, providing a useful testbed for the community.

3. **Clean empirical validation on the FM Toy dataset.** FIATS achieves near-zero MSE (0.003 at pred. len 14, 0.027 at pred. len 120) on a synthetic system where the theoretical error bound is zero, while all self-stimulated baselines — including billion-parameter foundation models — produce substantially larger errors (e.g., PatchTST: 0.168, Chronos-L: 0.374 at pred. len 120). This directly validates the core theoretical claim that the performance bottleneck is the lack of influence information, not model capacity.

4. **Ablation study that isolates the contribution of influences from architectural complexity.** Table 3 shows that removing influence inputs ("Zero News") degrades MSE from 0.182 to 0.249 (horizon 96), and removing channel descriptions ("Zero Desc.") degrades it further to 0.209. This cleanly attributes performance gains to the influence signal and the CASM mechanism rather than to raw model capacity. The robustness to different text embedding models (OpenAI 512, MiniLLM, mpnet) further supports the architecture's generality.

5. **Interpretable attention mechanisms.** The CASM and CAPS designs produce attention maps (Figures 3, 5) that reveal how different channels weight different influence factors, providing interpretability beyond raw performance numbers — a practical advantage over black-box models.

## Weaknesses

### Fatal
None.

### Major

1. **"FIITS" in the main results table (Table 1) is never defined.** The central experimental exhibit includes a column labeled "FIITS" that appears nowhere in the method description, ablation study, or any other section of the paper. Given the naming, FIITS is likely an ablation variant of FIATS (possibly FIATS without CASM or without textual input), but the paper never says so. This makes a significant portion of the main experimental results uninterpretable. A reader cannot evaluate what "FIITS" represents or what conclusion to draw from its comparison to FIATS and other baselines.

2. **Missing comparison against models receiving influence information as numerical exogenous variables.** The paper argues that numerical exogenous variables "lack the flexibility to capture nuanced, non-quantifiable events" (Section 3.2), but never includes a baseline that receives the *same* influence information (e.g., weather forecast features) in a simpler numerical or structured form. ChronosX (Arango et al., 2025) is cited but not compared against. Without this control, the experiments cannot distinguish between "FIATS's specific textual-influence mechanism is uniquely effective" and "any model receiving relevant external information improves." The Zero News ablation partly addresses this (showing influence information matters), but the comparison against a numerical exogenous variable baseline would substantially strengthen the paper's claims about the advantages of textual influence modeling specifically.

3. **Theoretical novelty is overstated relative to substance.** Propositions 2.1 and 3.1, while correctly presented, are recognizable as standard properties of conditional expectation — conditioning on more informative variables reduces expected MSE. The paper repeatedly frames these as a novel "mathematical barrier" discovered through control theory (e.g., "overturning a universally adopted yet flawed assumption"), which overclaims. The real novelty is the *specific proposal* to use textual influence descriptions and the architecture to process them, not the observation that external information helps. The paper would be stronger if it acknowledged this more modestly.

### Minor

4. **Weather forecasts as "independently evolving" influences in the Atmospheric Physics dataset.** The paper uses weather forecasts as textual influences for predicting atmospheric variables (solar radiation, pressure, etc.). These forecasts are outputs of numerical weather models that model the *same physical system* as the target variables. They are not truly "independently evolving" in the strict sense implied by the leak-free principle. The paper should either justify why this still satisfies its independence criterion or explicitly acknowledge this as a limitation.

5. **No confidence intervals or statistical significance tests.** No error bars, significance tests, or confidence intervals are reported for any result. Given that some margins are small (e.g., Electricity Utility: FIATS 0.124 vs. PatchTST 0.130 at horizon 96), it is unclear whether certain gains are statistically reliable.

6. **"LLM-free" claim is slightly imprecise.** FIATS is called "LLM-free" but uses pre-trained text embeddings from models that are based on LLM architectures (OpenAI embeddings, MiniLLM). The intended meaning — no generative LLM inference at test time — is reasonable, but the phrasing could mislead readers into thinking the model has no connection to LLM-based representations at all.

### Trivial

7. The CASM block description in the figure caption (line 152) includes an Argmax operation in the formula for computing sensitivity weights. Argmax is non-differentiable; if this is part of the actual training-time forward pass, it would break gradient flow. This is almost certainly a figure-notation imprecision (the main text description on lines 135–142 describes standard cross-attention without Argmax), but should be clarified.

8. The main text lacks dataset statistics (sizes, frequencies, number of channels, train/val/test splits), which are only in the appendix. Providing a summary table in the main text would improve readability.

## Nice-to-Haves

- A comparison against ChronosX or a model receiving the same weather forecast information as numerical exogenous channels (e.g., DLinear with exogenous features) would transform the evidence from "extra information helps" to "textual influence modeling is specifically advantageous."
- Parameter counts and compute costs to substantiate the "lightweight" claim (FIATS is described as lightweight but no evidence of parameter/FLOP counts is given).
- Error bars or confidence intervals on key results.

## Removed Points

These points were raised by reviewers but are not included as weaknesses; they are documented here for transparency:

- **"The evaluation amounts to a staged comparison"** — Removed. The paper's primary claim is that influence-aware modeling outperforms self-stimulation. Comparing FIATS (with influences) against models without influences directly tests this claim. Calling the comparison "staged" mischaracterizes the experimental design. The missing exogenous-variable baseline is a real gap (retained in Major #2), but the core comparison is appropriate for the paper's main thesis.
- **"Proposition 2.1's bound depends on ∇_U F which requires knowledge of true dynamics"** — Removed. Theoretical lower bounds that depend on unknown quantities are standard (e.g., Cramér-Rao bound depends on the true Fisher information). This does not invalidate the bound's structural insight.
- **"Self-stimulation framing is a straw man"** — Removed. The paper correctly identifies that standard TSF benchmarks and models operate in a closed-loop setup without external information, and characterizes this as an implicit assumption. This is an accurate description of the field's standard practice, not a straw man.
- **"FIATS is not actually tested"** — Removed. This is contradicted by the paper's content: FIATS is tested against 8 baselines across 5+ datasets with ablations and noise robustness analysis.
- **"Argument that the paper's performance gains are trivial"** — Removed. The ablation studies (Table 3) directly show that removing influences degrades performance, and the FM Toy results show that even billion-parameter foundation models fail without influence information — evidence that the gains are not trivial.
- Various formatting nitpicks, grammar concerns, and generic scope-expansion requests — Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface an observation about the paper that the authors themselves do not already articulate in the manuscript.

## Suggestions

1. **Define FIITS.** Clarify what FIITS represents — is it FIATS without CASM, without textual input, or some other ablation? State this explicitly and discuss what the FIATS vs. FIITS comparison reveals.
2. **Add an exogenous-variable baseline.** Include at least one model (e.g., DLinear with weather features concatenated as channels, or ChronosX) that receives the same influence information in numerical form. This would directly address the most significant open question about the comparison.
3. **Moderate the theoretical novelty claims.** Acknowledge that Propositions 2.1 and 3.1 are standard properties of conditional expectation, and focus the novelty claim on the textual influence design and FIATS architecture, which are genuinely novel.
4. **Add confidence intervals** or error bars for the main results, especially on the Electricity Utility dataset where margins are small.
5. **Clarify the independence criterion** for weather forecasts in the Atmospheric Physics dataset, or acknowledge the limitation explicitly.
6. **Clarify the "LLM-free" terminology** or replace with "generative-LLM-free" to avoid misleading readers.
7. **Clarify the Argmax notation** in the CASM figure caption.

## Score and Decision

Based on my analysis of the paper against ICLR reviewing standards:

**Score reasoning:** The paper makes a genuinely useful contribution — it identifies a real limitation in TSF (the lack of external influence modeling), provides a theoretical motivation, builds a benchmark to address the gap, and proposes a concrete model with strong empirical results. The writing is clear and the experimental design (including ablations) is generally thorough.

However, there are notable weaknesses: the undefined FIITS baseline undermines Table 1's interpretability, the missing exogenous-variable baseline limits the strength of the comparison, and the theoretical framing overclaims novelty relative to substance. These are real but not fatal — they can be addressed with revisions.

The paper's core contributions are solid enough for borderline acceptance. It does not reach the bar for an 8 (strong accept) due to the FIITS omission and the exogenous-variable comparison gap, but it is clearly above the reject threshold given the quality of the benchmark, architecture, and main empirical results.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>