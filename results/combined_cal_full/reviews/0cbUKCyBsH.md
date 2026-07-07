Now I have sufficient calibration data. Let me synthesize the final review.

---

## Summary

This paper makes three main contributions: (1) a control-theoretic analysis formalizing why ignoring external influences creates an irreducible error bound in time series forecasting (Propositions 2.1 and 3.1); (2) the IATSF paradigm and a leak-free benchmark with temporally-synced textual influences; and (3) FIATS, a lightweight LLM-free architecture that channels textual influence signals through a Channel-Aware Adaptive Sensitivity (CASM) mechanism. The theory is clean and sound, the benchmark design is principled, and the architecture-theory alignment is genuine. However, the experimental evaluation has a significant gap that prevents full validation of the FIATS architecture claims.

## Strengths

- **Sound control-theoretic formalization.** Proposition 2.1 (Eq. 3) cleanly captures why models blind to external influences converge to conditional expectations. The decomposition into self-stimulated dynamics ($A$) and influence-driven dynamics ($B$) is mathematically precise and pedagogically effective.

- **Proposition 3.1 directly motivates the paradigm.** The formal result that any measurable influence reduces the error covariance provides rigorous justification for incorporating even imperfect or partial influence signals. This is the paper's strongest theoretical anchor.

- **Well-articulated leak-free benchmark design.** Section 4.1 correctly identifies information leakage as a problem in existing multimodal time series datasets, and the restriction to independently evolving influences is a principled design choice. The recognition that ground-truth future influences are unavailable at deployment (points 1–3) shows honest thinking about the evaluation setup.

- **Clean and informative ablation study.** Table 3's "Zero News" vs. "Zero Desc." comparison effectively isolates the contributions of influence information and channel-specific modeling. The stability across embedding models (OpenAI 512, MiniLLM, mpnet) strengthens the claim that performance does not hinge on a specific embedding choice.

- **CASM mechanism is well-motivated by theory.** The mapping from the linear system analysis ($\frac{dx_f^i}{dU_f^j} = c^i B^j$) to query/key/value roles in cross-attention (Section 5) is a genuine architectural-theoretical alignment that gives interpretable sensitivity weights.

## Weaknesses

### Major

- **Undefined "FIITS" in the main results table (Table 1).** The column "FIITS" appears in the header and results rows with large performance differences from FIATS (e.g., 0.282 vs. 0.003 on FM Toy, pred len 14), but is never defined anywhere in the paper. The ablation study (Table 3) uses "Zero News" for the without-influence variant, not "FIITS." This is a basic reporting failure that prevents the reader from interpreting a substantial portion of the empirical results. The paper must clarify what FIITS is, how it differs from FIATS, and why these performance gaps exist.

- **Headline comparisons do not validate the FIATS architecture's specific design.** Table 1 compares FIATS (which receives textual influences: weather reports, developer logs, holiday indicators) against DLinear, PatchTST, Chronos, MOIRAI, Time-MoE, and TimeLLM — none of which receive this information. The result that FIATS outperforms them is unsurprising and tells us little about whether FIATS's *way* of incorporating influences is better than simpler alternatives. The paper claims that "performance gains stem from principled influence modeling, not architectural complexity" (Section 5, line 29), but this claim cannot be evaluated from the current evidence because the baselines are systematically disadvantaged — they lack the influence inputs entirely.

  A critical missing baseline is a standard TSF model (e.g., DLinear or PatchTST) that receives the same textual influences as additional numerical features (e.g., concatenated text embeddings). The paper cites ChronosX (Arango et al., 2025), a variant specifically designed to handle exogenous variables, but does not include it as a baseline. Without this comparison, the paper's contributions as a *method paper* (validating FIATS over simpler influence-aware alternatives) are substantially weakened, though the paradigm-level contribution (influence-aware > self-stimulated) remains supported.

### Minor

- **The FM Toy experiment validates the paradigm but not the architecture.** The experiment shows FIATS succeeding because it sees the control signal while baselines do not. This is architecturally uninformative — it confirms the theory that influence-aware models outperform self-stimulated ones, but does not test FIATS's specific design. The paper's framing (RQ1: "Can IATSF overcome the limitations of self-stimulation?") is appropriately about the paradigm, but the discussion sometimes oversells this as architectural validation.

- **Weather forecast independence for the Atmospheric Physics dataset.** Weather forecasts and atmospheric physics variables (solar radiation, air pressure, dew point) are outputs of the same underlying physical system. A weather forecast predicts the atmospheric state being modeled, which may violate the benchmark's stated requirement of "independently evolving influences — external factors that influence the system but are not themselves outcomes of it" (Section 4.1). The paper does acknowledge using predictions of $U_f$ from expert sources, which partially addresses the concern, but this subtle leakage risk merits explicit discussion.

- **Noise experiment (Figure 6) lacks sufficient detail.** The paper does not specify what type of noise is added, at what levels, or how many trials were run. A single line plot without error bars or replication details is insufficient to support robust claims about noise tolerance.

- **TimeLLM results reported as "—" without explanation.** In Table 1, TimeLLM shows "—" on the Atmospheric Physics 2014-24 dataset. If the model could not be run (e.g., due to context length limits), this should be stated.

- **"Zero Desc." ablation does not directly isolate the CASM mechanism.** Removing channel descriptions is a proxy for disabling CASM, but the performance drop could also stem from reduced model capacity. The claim that this "confirms the critical role of the CASM mechanism" over-interprets the result.

- **Proposition 2.1's error bound is presented without discussing its practical significance.** The lower bound on error covariance is $\nabla_U F \Sigma (\nabla_U F)^\top$, which may be negligible when influence variance ($\Sigma$) or system sensitivity ($\nabla_U F$) is small — a condition that may hold for many real-world time series where external influences are weak relative to internal noise. The paper does not discuss when the bound is practically meaningful.

- **Overclaimed rhetoric relative to actual novelty.** The paper repeatedly uses "break the barrier," "paradigm shift," and "primary path forward" language. Incorporating exogenous variables into time series models is decades-old practice (ARIMAX, VARX, state-space models with inputs). The genuine novelty is in using textual descriptions as the exogenous signal and the control-theoretic formalization, which are real contributions that do not require hyperbolic framing.

### Trivial

None.

## Nice-to-Haves

- **Add influence-augmented baselines.** The single most informative experiment would be giving a simple model (e.g., DLinear or PatchTST) access to the same influence information (as concatenated text embeddings or numerical encodings) and comparing against FIATS. This would directly test whether the FIATS architecture's specific design choices matter.
- **Add error bars / statistical variability** to the main results (Table 1) across multiple runs or seeds.
- **Test a simple numerical encoding baseline** (e.g., label-encoding weather types instead of using text embeddings) to evaluate the claimed advantage of textual over numerical modalities.
- **Report statistical significance** for the performance differences between FIATS and the strongest baselines.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Noise about missing related work.** The harsh critic raised concerns about missing related works, but per the hard rules, I cannot verify whether any work is actually missing without external sources.
- **Reproducibility concerns about undisclosed hyperparameters.** Per the hard rules, undisclosed implementation details are not valid criticisms.
- **Generalized "evaluation lacks rigor" without specific anchor.** The input contained some sweeping statements without specific textual evidence; these have been removed.
- **Complaint that the paper does not address problems outside its stated scope.** Some criticisms demanded the paper solve additional problems (e.g., chaotic systems, varying credibility of news sources) that the paper explicitly scopes as future work.

## Novel Insights

The most interesting observation emerging from the reviews is that this paper's contributions operate at two distinct levels — the *paradigm* (influence-aware forecasting) and the *architecture* (FIATS) — and the evaluation supports only one. The paradigm-level claim is well-supported by the theory (Propositions 2.1, 3.1), the benchmark design, and the paradigm-level experiments. The architecture-level claim requires a controlled comparison where baselines receive the same information, which the paper does not provide. This disconnect between what the paper claims about FIATS and what the experiments actually demonstrate is the central tension. The paper would be stronger if it clearly separated these two claims and matched the evidence to each at the appropriate level.

## Suggestions

1. **Define FIITS** — this is a basic reporting requirement that must be fixed.
2. **Add a controlled influence-augmented baseline** — give DLinear or PatchTST the same textual influence embeddings as additional input channels and compare against FIATS. This directly tests whether FIATS's specific design is superior.
3. **Add error bars / standard deviations** to Table 1 results.
4. **Explicitly discuss** the weather forecast independence concern for the Atmospheric Physics dataset.
5. **Add a numerical encoding baseline** (e.g., one-hot or label-encoded weather types) to test the claimed advantage of textual influences over numerical exogenous variables.
6. **Tone down the rhetoric** to match what the evidence actually supports.

## Score and Decision

### Calibration Anchors

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| KokerNet (w7vn6ah0Qg.md) | 5.00 | R1 | Yes | Koopman operator TSF paper with theory+experiments but severe novelty/obfuscation issues; our paper has cleaner theory and fewer foundational errors |
| Time-LLM (Unb5CVPtae.md) | 7.00 | R1 | Yes | ICLR-accepted LLM-for-TSF paper; stronger evaluation breadth but narrower theoretical contribution |
| FITS (bWcnvZ3qMb.md) | 8.00 | R1 | Yes | Very strong lightweight TSF paper; comprehensive evaluation, no comparable evaluation gaps |
| Spline stabilization (43Ckmku1fC.md) | 5.50 | R2 | Yes | Control-theoretic TSF paper with identified theoretical errors in core results; our paper's theory has no identified errors |
| DAM Foundation Model (4NhMhElWqP.md) | 7.00 | R2 | No | Strong universal forecasting paper with comprehensive evaluation |
| Periodicity Decoupling (dp27P5HBBt.md) | 6.75 | R2 | No | TSF with solid evaluation and clear contributions |
| In-context Predictor (dCcY2pyNIO.md) | 6.25 | R2 | No | TSF reformulation with clean evaluation |

**Bracket from Round 1**: 4.0–7.0, narrowed to **5.5–7.0** after considering that the theory is sound (unlike the 5.5 anchor which had theoretical errors) but the evaluation gap prevents it from reaching the 7.0 range.

**Final calibration**: The paper's weighted items show strengths (+3.61 to +5.14) comparable to Time-LLM's positive items, but a critical weakness at -5.32 (missing baselines) and -3.33 (FIITS undefined) that Time-LLM's -6.59 (limited experiments) and -6.48 (novelty) didn't fully prevent it from reaching 7.0. However, Time-LLM's evaluation gap was about *breadth* (more datasets would strengthen it), while this paper's evaluation gap is about *fairness of comparison* (baselines don't get the same inputs) — a more central issue. The 5.50 anchor (spline work) had its core theoretical results questioned, which our paper does not. On balance, this paper sits between 5.50 and 7.00, closer to 6.0, reflecting real theoretical and benchmark contributions weighed against an evaluation design that does not support the architectural claims made about FIATS.

**Score**: 6.0

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>