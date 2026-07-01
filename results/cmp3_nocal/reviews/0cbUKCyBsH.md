## Summary

This paper identifies a fundamental limitation in time series forecasting: "self-stimulation," where models predict future values using only a target series' own history, ignoring the external influences that drive real-world systems. The authors formalize this as a control-theoretic error bound (Proposition 2.1), introduce the Influence-Aware Time Series Forecasting (IATSF) paradigm, build a leak-free benchmark of temporally-synced textual influences, and propose FIATS—a lightweight, LLM-free model with channel-aware cross-attention mechanisms (CASM/CAPS). Empirical results show FIATS outperforming standard baselines across synthetic, physics-based, and market datasets.

## Strengths

- **Clean, well-motivated observation with formal backing.** The core insight—that self-stimulated models converge to conditional expectations, creating an irreducible error floor—is articulated clearly and formalized through Propositions 2.1 and 3.1. The control-theoretic framing (Eq. 4: Cov(ε) ≥ BΣB^T) makes the intuition transparent and gives practitioners a principled vocabulary for a genuine limitation.

- **The benchmark datasets are a real contribution.** Creating leak-free, temporally-synced textual influence datasets across toy, physical, and market domains is labor-intensive and fills a genuine gap. The design constraints (independently-evolving influences, synchronization windows, no access to future system states) are thoughtfully justified (Section 4.1) and, if released, could catalyze a line of work on influence-conditioned forecasting.

- **The ablation design probes the right questions.** Removing influence inputs ("Zero News") causes performance to drop to self-stimulated levels; removing channel descriptions ("Zero Desc.") also degrades performance (Table 3). The noise-tolerance experiment (Fig. 6) directly tests practical viability under imperfect influence predictions. These ablations correctly target whether the information matters.

## Weaknesses

### Fatal
None.

### Major

- **The undefined "FIITS" column in Table 1 makes the paper's central empirical exhibit partially uninterpretable.** The column labeled "FIITS" (line 188) appears in every row of the main results table with values that differ dramatically from FIATS (e.g., FM Toy horizon 14: FIATS=0.003, FIITS=0.282). Yet "FIITS" is never defined anywhere in the visible main text—it appears only in the table header. Readers cannot determine whether FIITS is an important ablation, a baseline variant, or something else entirely. This is not a minor labeling issue; it is a primary column of the paper's headline experiment whose meaning is inaccessible from the main text.

- **Headline quantitative claims conflate "having more information helps" with "the FIATS architecture is effective," and the missing controls prevent disentangling the two.** The paper reports "a 36.0% MSE reduction on Atmospheric Physics" and "44.3% on NYC Traffic Speed" compared to PatchTST (Section 6.2), and claims performance gains "stem from principled influence modeling, not architectural complexity" (line 29). However, the baselines (DLinear, PatchTST, Chronos, MOIRAI) have no access to textual influence information, so these large improvements primarily demonstrate that providing external information helps—a practically useful but unsurprising result. The paper lacks a controlled comparison where a baseline receives the *same* text embeddings through a simpler integration mechanism (e.g., concatenation with DLinear or a linear projection). TimeLLM is the only multimodal baseline but uses a prompting format that is architecturally very different. Without a simple text-conditioned baseline, the paper cannot substantiate the claim that its specific CASM and CAPS mechanisms are responsible for the gains, as opposed to the information itself processed through any reasonable architecture. The ablation studies (Table 3) show the information is necessary but do not isolate the mechanism.

### Minor

- **No model size, FLOPs, or inference latency reported despite repeated "lightweight" claims.** The paper calls FIATS "lightweight" and "LLM-free" (lines 9, 23, 131) and contrasts it with LLM-based approaches that incur "significant overhead" (line 131). Yet no parameter counts, FLOPs, or wall-clock inference times are provided for FIATS or any baseline. Given that FIATS uses a patch-based time series encoder, multiple cross-attention blocks, a stacked self-attention influence encoder, and a decoder with cross-attention, its parameter count may be non-trivial. This claim needs quantitative support.

- **The "fail spectacularly" characterization oversells the gap for the FM Toy dataset at short horizons.** The paper states that "all self-stimulated TSF methods… fail spectacularly" on FM Toy (line 184). Yet at horizon 14, PatchTST achieves MSE of 0.006 vs. FIATS's 0.003—a small absolute gap that is far from a "failure." The gap widens at longer horizons (e.g., horizon 120: PatchTST=0.168 vs. FIATS=0.027), so the claim is defensible at longer horizons but hyperbolic for short ones.

- **The magnitude of improvement on NYC Traffic Speed (FIATS~0.443 vs. PatchTST~0.858, nearly 50%) is suspiciously large.** The paper itself notes that weather has a "subtle, indirect relationship" with urban traffic (line 125). An improvement of this magnitude suggests either that PatchTST may be poorly tuned for this dataset, or that the textual influence information is supplying something beyond weather signals (e.g., temporal markers). A simple text-concatenation baseline would clarify whether this gain is reasonable or an artifact of the comparison setup.

- **No confidence intervals, standard deviations, or significance tests are reported.** Table 1 appears to be single-seed results. Readers cannot assess whether the reported gaps are statistically reliable.

- **The connection between Proposition 2.1 and observed model behavior is asserted rather than empirically verified.** The paper claims that "averaging effects in practice" (line 67) result from self-stimulated models converging to E_U[F(X_h, U)], but does not demonstrate that the observed "collapsed" forecasts (Fig. 1) are in fact the conditional expectation. This link is plausible but not tested.

### Trivial
None.

## Nice-to-Haves

- Add a simple text-conditioned baseline: take the same text embeddings used by FIATS and feed them into a linear model (or DLinear) by concatenating text embeddings with the time series. This is the most direct way to test whether CASM/CAPS provide value beyond the information itself.
- Clarify what FIITS is in the main text and discuss what its performance reveals.
- Report parameter counts and inference speeds to support the "lightweight" claim.
- Add evaluation on a standard benchmark (e.g., ETT with hand-crafted exogenous variables or weather) to enable external validation.
- Run ARIMAX on datasets where numerical exogenous variables are available (e.g., Electricity Utility with holiday indicators) as a natural baseline for the influence-aware setting.

## Removed Points

- **"Performance plateau claim is contested"**: This is a framing debate about a statement in the introduction; it is not a substantive weakness of the paper's contribution. Removed.
- **"Benchmark cannot be compared against standard TSF benchmarks"**: The paper explicitly discusses why ETT is unsuitable (Section 4.1); this is a design choice, not a flaw. Removed.
- **"CASM requires per-dataset metadata"**: This is a reasonable design property of the approach, acknowledged implicitly by the dataset construction. Not a weakness. Removed.
- **"Missing limitation about needing future influence predictions"**: The paper already discusses this in Section 4.1 (lines 113-114), noting that deployment uses known info, expert predictions, or hypothetical scenarios. Removed as already addressed.
- **"Self-stimulation framing is overclaimed as a discovery"**: This is a matter of opinion about presentation. The formalization is genuinely novel even if the broad intuition is familiar. Removed.
- **Strengths removed as generic/superficial**: None removed—all listed strengths are concrete and evidence-backed.
- **Speculation about simple concatenation baseline "would likely also outperform"**: The reviewer's speculation about how a simple baseline would perform is not evidence. The core request for the baseline is kept in Weaknesses (Major) and Nice-to-Haves; the speculative assertion is removed.

## Novel Insights

Beyond the paper's own contributions, the reviews highlight a recurring structural pattern in multimodal time series work: when the proposed model receives strictly more input information than baselines, large performance gaps are unsurprising. The reviews surface the need for a clear separation between testing "whether additional modality helps" (a paradigm-level question) and "whether the specific architectural mechanism for fusing that modality is effective" (a model-level question). The paper answers the first question well and the second question incompletely.

## Suggestions

1. In the main text, define FIITS the first time it appears, or rename the column to something self-explanatory (e.g., "FIATS w/o CASM").
2. Add a controlled experiment where a simple architecture (e.g., DLinear, a linear layer) receives the same text embeddings through basic concatenation or addition, and compare its performance to FIATS. This directly tests whether the CASM/CAPS mechanisms matter.
3. Add a table with parameter counts, FLOPs, and/or inference times for FIATS and all baselines to substantiate the "lightweight" claim.
4. Run experiments with multiple seeds and report standard deviations or confidence intervals.
5. Tone down the "fail spectacularly" characterization or qualify it by prediction horizon.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>