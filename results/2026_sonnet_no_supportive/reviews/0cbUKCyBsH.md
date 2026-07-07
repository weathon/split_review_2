## Summary

This paper proposes Influence-Aware Time Series Forecasting (IATSF), arguing that the universal "self-stimulation" assumption imposes a mathematically provable error floor on any model that uses only historical observations. Through a control-theoretic lens, the authors derive Proposition 2.1 (an irreducible covariance lower bound) and Proposition 3.1 (any partial influence reduces that bound), then build FIATS — a lightweight, LLM-free model with Channel-Aware Adaptive Sensitivity Modeling (CASM) and Channel-Aware Parameter Sharing (CAPS) — together with a new leak-free benchmark pairing time series with independently-evolving textual influences.

---

## Strengths

- **Control-theoretic grounding directly informs architecture** (Sections 2–3, Propositions 2.1 and 3.1): The paper derives an explicit covariance lower bound $B\Sigma B^\top$ for linear systems and shows it collapses when influence is observed. This is not boilerplate motivation — the bound directly motivates learning $CB_{U_f}$ in CASM and justifies why imprecise textual signals still reduce error (Proposition 3.1). The theory-to-architecture connection is tighter than in most text-aided forecasting papers.

- **FM Toy experiment is a genuinely clean theoretical validation** (Table 1, Section 6.1): In a fully synthetic frequency-modulated system where influence precisely controls frequency and the theoretical bound is zero, FIATS achieves MSE ≈ 0.003–0.027 while all self-stimulated baselines fail catastrophically (MSE ≈ 0.1–0.9, including billion-parameter foundation models). This is an unusually vivid and verifiable confirmation of Proposition 2.1.

- **Leak-free benchmark design is carefully motivated** (Section 4.1): The paper correctly identifies that many existing multimodal forecasting datasets leak future state information through textual summaries of the time series itself. Restricting influence inputs to independently-evolving factors (weather forecasts, holiday calendars, developer logs) with temporal synchronization is well-designed, and the paper articulates why standard datasets like ETT are unsuitable.

- **LLM-free design outperforms LLM-based baselines**: FIATS consistently outperforms TimeLLM across all datasets, supporting the paradigmatic claim that the bottleneck is the self-stimulation assumption and not model capacity.

---

## Weaknesses

### Fatal
None.

### Major

- **FIITS appears in every row of Table 1 but is never defined anywhere in the main text.** This is not a minor omission — FIITS is the second-best model in most dataset rows (e.g., MSE 0.282 vs. FIATS's 0.003 on FM Toy at horizon 14; 0.248 vs. 0.182 on Atmospheric Physics 2014-19 at horizon 96). The ablation logic of Table 1 cannot be interpreted without knowing what FIITS is. If FIITS is "FIATS without influence input," labeling it that way would make the internal ablation explicit and highly informative; as written, the reader must guess at the paper's most important comparison.

- **The main comparisons conflate paradigm access with architectural contribution.** In every result in Table 1, FIATS receives future-aligned influence signals ($U_f$) at test time. All competing baselines — DLinear, PatchTST, Chronos-L, MOIRAI-L, Time-MoE-U, TimeLLM — receive no such information. The 36% MSE reduction on Atmospheric Physics and 44.3% on NYC Traffic Speed relative to PatchTST cannot be attributed to CASM or CAPS versus a simpler influence-receiving alternative. The "Zero News" ablation in Table 3 establishes that influence information matters and "Zero Desc." demonstrates channel descriptions help — but neither ablation compares against an equally-equipped external baseline (e.g., PatchTST with weather embeddings concatenated, or ChronosX, which is cited at line 299 as a pretrained model adapted for exogenous variables). Without such a control, the paper demonstrates that receiving external information beats not receiving it — which Proposition 3.1 already proves must be true — but does not establish that FIATS's specific architecture extracts that information better than a simpler alternative.

### Minor

- **The practical validity of using weather forecasts as influence is unexamined for long horizons.** Section 4.1 states influences are "predictions of $U_f$ from expert sources (e.g., weather reports)," but the experiments do not specify whether test-time weather inputs are ground-truth future values or actual historical forecast archives. Weather forecast accuracy degrades substantially with horizon; the noise-robustness experiment in Figure 6 uses synthetic Gaussian noise rather than realistic forecast-error distributions. If ground-truth future weather is used at test time, the reported gains on Atmospheric Physics and NYC Traffic overestimate practical performance.

- **Proposition 2.1 assumes $U_t \perp X_h$** (influences independent of history). In practice, weather tomorrow is correlated with weather today, meaning self-stimulation models can implicitly capture some influence effects. The paper does not discuss how this loosens the practical interpretation of the "hard barrier," nor does it estimate how much of the theoretical bound is binding for its actual datasets.

- **Model parameter count is not reported.** The paper repeatedly claims FIATS is "lightweight" (abstract, Section 5) but provides no parameter count compared to PatchTST or DLinear. This makes the efficiency claim unverifiable in the main text.

### Trivial
None.

---

## Nice-to-Haves

- Add at least one external influence-receiving baseline to Table 1 — even naive concatenation of weather embeddings to PatchTST inputs — to isolate CASM/CAPS contribution from information access advantage.
- Include ChronosX (already cited) in Table 1 as a direct contemporary comparison.
- Specify whether ground-truth or historical forecast-quality weather is used at test time, and include a realistic-forecast experiment at longer horizons.
- Report parameter counts for FIATS vs. PatchTST to substantiate the lightweight claim.
- For GAUD (Section 6.3), clarify that 40.4% of games see another method win (Fig. 4) alongside the "ranks first on 59.6%" framing.

---

## Removed Points

*These points are flagged for removal; treat them with caution.*

- **GAUD temporal alignment concern**: The reviewer raised whether developer logs may be available only after a metric shift, suggesting possible leakage. The paper states this is handled in the appendix (Section 4.2). Since the appendix was stripped, this cannot be verified and is not treated as a confirmed weakness.
- **CAPS overhead not reported**: The reviewer flagged absence of CAPS parameter counts. Retained as a Minor weakness regarding efficiency claims, but not elevated since the model is LLM-free and cross-attention adds little overhead compared to full LLM baselines.
- **ChronosX omission as "conspicuous"**: The harsh critic labels this fatal. Since ChronosX is cited in related work (line 299) and the authors did not include it in Table 1, this is a real gap but folded into the Major weakness about paradigm-vs.-architecture conflation — not separately fatal.

---

## Novel Insights

The control-theoretic formalization of the self-stimulation barrier (Propositions 2.1–3.1) and the FM Toy experiment together provide an unusually clean demonstration that a paradigmatic assumption — not model scale — explains a documented performance plateau in time series forecasting. The insight that even imprecise, partial influence information provably reduces the error covariance floor (Proposition 3.1) provides principled motivation for text-based influence modeling that most prior text-augmented forecasting work lacks. The CASM design's grounding in the linear-system sensitivity matrix $CB_{U_f}$ is more principled than typical cross-attention formulations.

---

## Suggestions

1. **Define FIITS immediately** at its first appearance in Table 1 caption. If it is FIATS without influence inputs, rename it "FIATS (no influence)" — this makes it the primary ablation counterpart and resolves the table's interpretability gap.
2. **Add a naive influence-receiving baseline** (e.g., PatchTST + text embedding concatenation) to Table 1. If FIATS substantially outperforms this, CASM and CAPS are vindicated; if not, the contribution should be reframed around the paradigm and benchmark. Either outcome strengthens the paper.
3. **Specify influence quality explicitly**: State whether Atmospheric Physics and NYC Traffic use ground-truth future weather or historical forecast archives at test time, and run at least one experiment with realistic forecast-quality inputs at different horizons.
4. **Report model size**: Add a parameter count row or table footnote for FIATS vs. PatchTST to substantiate the "lightweight" claim.

---

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| mfc6FKgtQA.md | 5.0 | 1 | Closest analog: text-guided TSF with benchmark (TGForecaster), similar comparison-fairness weakness, weaker theory — rejected |
| 4F1a8nNFGK.md | 5.0 | 1 | Text+context benchmark (CiK), benchmark-focused paper, less model contribution — rejected |
| QE1ClsZjOQ.md | 4.5 | 1 | Multimodal dual-forecaster combining text and time series — rejected |
| uRXxnoqDHH.md | 5.0 | 1 | Multi-modal augmented TSF (MoAT), similar multimodal fusion — rejected |
| TYXtXLYHpR.md | 5.75 | 1 | Transparent TSF, accepted borderline |
| Tuh4nZVb0g.md | 6.0 | 1 | TEST: LLM for time series, accepted |
| dCcY2pyNIO.md | 6.25 | 1 | In-context TSF with Transformers, accepted |
| lfPkGWXLLf.md | 6.67 | 1 | ForecastBench dynamic benchmark, accepted |
| bWcnvZ3qMb.md | 8.0 | 1 | FITS (10k param TSF), strong accept — much tighter contribution |

**Round 1 bracket: 4.5–6.0.** The paper has stronger theoretical grounding than TGForecaster (5.0) and a cleaner experimental design, but shares the critical weakness of missing an external influence-receiving baseline. The FIITS-undefined issue is a significant presentation gap in the primary results table. The paper sits above pure benchmark papers (CiK, 5.0) due to the theory but below fully accepted TSF papers (score 6+) due to the structural comparison gap. Narrowing to **5.0**.

---

## Score and Decision

The paper makes a genuine paradigmatic and theoretical contribution — the self-stimulation barrier analysis, clean FM Toy validation, and leak-free benchmark are real advances. However, the central architectural claim (that CASM/CAPS specifically drive the performance gains) is not demonstrated by the experiments: FIITS is never defined, and no external influence-receiving baseline exists in Table 1. These are resolvable gaps but materially weaken the claim that FIATS's design, not information access, is the primary driver of observed gains.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>