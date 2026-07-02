## Summary

This paper identifies the "self-stimulation" assumption in time series forecasting (TSF)—using only historical observations to predict future values—as a fundamental bottleneck. Through a control-theoretic lens, the authors formalize this bottleneck, showing that ignoring external influences (U) imposes irreducible error. They propose the Influence-Aware Time Series Forecasting (IATSF) paradigm, contribute a leak-free benchmark with temporally-synced textual influences across three categories (toy, real-world, business), and develop FIATS, a lightweight LLM-free model with channel-aware mechanisms (CASM and CAPS). Experiments show that FIATS with influence information outperforms self-stimulated baselines.

## Strengths

- **The core problem framing is a genuine conceptual contribution.** The observation that TSF models operate closed-loop while real systems are open-loop, and the identification of "self-stimulation" as a distinct bottleneck (separate from architecture scale or design), is well-articulated in Section 2 and usefully reframes the field's focus from architectural innovation to input scope.

- **The benchmark is a real service to the community.** Constructing leak-free, temporally-synchronized datasets with textual influences is non-trivial. The three-category structure (controlled toy → complex real-world → human-driven business) covers different validation needs. The design criteria (independence, temporal synchronization, no leakage) are clearly motivated, making this a resource the community can build on.

- **The CASM mechanism is a sensible and interpretable architectural design.** Using cross-attention with channel descriptions as queries and influence text as keys/values is a clean way to model heterogeneous channel responses to a common influence. The attention map visualizations (Fig. 5) provide interpretability that goes beyond what most TSF models offer.

- **The ablation study (Table 3) is informative and properly controlled.** Showing that removing influence inputs ("Zero News") collapses performance to self-stimulated levels, while removing channel descriptions ("Zero Desc.") causes intermediate degradation, correctly attributes the gains to the influence information itself and partially to the channel-awareness mechanism.

- **The noise robustness analysis (Fig. 6) provides a clean empirical validation of Proposition 3.1.** The graceful degradation as influence quality decreases demonstrates practical support for the theoretical framework.

## Weaknesses

### Major

- **Missing numerical-exogenous baselines.** The paper argues in Section 3.2 that textual influence information is uniquely valuable over numerical exogenous variables, claiming that text captures "nuanced, non-quantifiable events." However, this claim is never tested. For the Atmospheric Physics and NYC Traffic datasets, the textual influences are weather forecasts—information that can be straightforwardly encoded as numerical features and fed as exogenous channels to standard TSF models (e.g., DLinear or PatchTST with exogenous inputs, or Chronos-X which is cited but not compared against). Without this comparison, the paper cannot support the claim that textual modality provides unique value over numerical exogenous variables.

- **The experimental design conflates paradigm-level and model-level claims.** The headline results (36–44% MSE reductions over PatchTST in Table 1) compare FIATS—which receives influence information—against models that only see historical time series. This validates the paradigm-level premise (influence information helps forecasting) but does not establish that FIATS is an effective architecture for using that information, since no comparison is made against other models that also receive influence data. The paper presents these numbers as evidence for FIATS's effectiveness (Section 6.2: "FIATS consistently outperforms all baselines"), which conflates having more information with having a better model.

- **The independence criterion for the Atmospheric Physics dataset is questionable.** Section 4.1 requires influences to be "independently evolving—external factors that influence the system but are not outcomes of it." However, weather forecasts for atmospheric variables (solar radiation, air pressure, dew point) are predictions produced by the same underlying physical system—they are functions of the system state, not independent external factors. A "clear skies" forecast is a qualitative description of the same atmospheric dynamics that produce the target variables (e.g., SWDR). This violates the stated design principle and weakens the benchmark's primary real-world dataset.

### Minor

- **The theoretical propositions (2.1 and 3.1) are correctly stated but are standard results.** Proposition 2.1 (omitting relevant variables induces irreducible error proportional to their variance) and Proposition 3.1 (adding relevant information reduces the lower error bound) are standard misspecification/omitted-variable results in statistics and control theory. The framing as a "hard, mathematical barrier" discovered through a control-theoretic lens overstates the novelty of the formalism.

- **The FM Toy experiment is demonstrative but not informative for architectural evaluation.** The system is constructed so that the "influence" is the frequency control signal—knowing it makes prediction nearly deterministic, and without it, prediction is impossible. The experiment validates the paradigm premise (having the right input features matters) but provides no signal about whether FIATS's architectural approach is effective or efficient relative to alternatives.

- **FIITS appears in Table 1 but is not defined in the main text.** The acronym appears as a column in the main results table with competitive performance but is never explained in the body text (only the appendix, which is stripped). A main-table entry should be interpretable from the main text alone.

### Trivial

None.

## Nice-to-Haves

- Add the critical missing baseline: feed numerical weather variables (temperature, precipitation, cloud cover) as exogenous channels to standard TSF models. Compare FIATS (text-based influences) against these to test whether text provides unique value.
- Restructure claims to separate the paradigm question ("does influence information improve forecasting?") from the model question ("is FIATS an effective architecture for using that information?").
- For the Atmospheric Physics dataset, discuss whether weather forecasts qualify as "independently evolving" influences or whether they constitute a form of information leakage.
- Report variance or confidence intervals for the main results in Table 1.

## Removed Points

These points from the input review were removed with brief justifications:

- *"No discussion of how influence predictions are obtained at test time"* — The paper does address this in Section 4.1 (known information, expert forecasts, hypothetical events, with reference to Appendix B.3). The reviewer appears to have missed this.
- *"The foundation model plateau is a non-sequitur"* — The paper uses the plateau as motivation, not as logical proof. This is a reasonable rhetorical framing.
- *"Section-by-section presentation notes"* — These are commentary about what the paper does, not substantive weaknesses.
- *"Missing related works"* — Removed per rules (cannot verify presence/absence of cited works).
- Generic or superficial strengths from the input were dropped.

## Novel Insights

The most interesting observation from the review process is how consistently papers in this emerging "text-guided time series" area share the same weakness pattern: they argue for the unique value of textual information but never compare against the obvious baseline of encoding the same information numerically and feeding it through standard exogenous-variable channels. This is a recurring blind spot shared by this paper, the TGTSF paper (scored 5.00), and the CiK benchmark paper (scored 5.00). For the field to move forward, this comparison needs to become standard practice—without it, the added value of the text modality remains an untested claim.

## Suggestions

1. **Add the critical missing baseline** (most important): Feed numerical weather variables as exogenous channels to standard TSF models. If FIATS with text outperforms these, the case for textual influence modeling is supported. If not, the contribution narrows to "having influence information helps."
2. **Recalibrate the claims:** The paradigm claim is well-supported; the model claim needs fairer baselines.
3. **Revise the Atmospheric Physics dataset framing** to acknowledge that weather forecasts are not truly independent external factors, or replace them with more clearly independent influences.
4. **Define FIITS in the main text** so Table 1 is self-contained.
5. Consider adding variance estimates across multiple runs or seeds.

## Score and Decision

**Calibration procedure:**

Bracket determined by comparing against 12 retrieved anchor papers across 6 score bands.

**Round 1 anchors retrieved (all bands):**

| Band | Path | Avg Score | Round | Comparison |
|------|------|-----------|-------|------------|
| <1.5 | nSDOkm0SKo.md | 1.00 | R1 | Financial news paper; much weaker |
| <1.5 | Uj0h13lVrR.md | 1.00 | R1 | GFlowNet paper; not comparable |
| <1.5 | P49gSPmrvN.md | 1.00 | R1 | UMAP visualization; not comparable |
| <1.5 | 8QTpYC4smR.md | 1.00 | R1 | LLM survey; not comparable |
| 1.5–3.5 | GvzL4LuycW.md | 3.00 | R1 | TimeRAG; weaker (problem formulation issue) |
| 1.5–3.5 | Y89o3LAEHX.md | 2.00 | R1 | Hybrid loss; weaker |
| 1.5–3.5 | ZT33ACedmn.md | 3.00 | R1 | LLM-ABBA; weaker |
| 1.5–3.5 | RDLvnUJ5JZ.md | 3.00 | R1 | Diffusion model; weaker |
| 3.5–5.5 | 7egJb0X9m2.md | 5.00 | R1 | TILDE-Q loss function; comparable reception |
| 3.5–5.5 | PLYqJVV7dm.md | 4.25 | R1 | CRAFT; weaker (data leakage) |
| 3.5–5.5 | yGv5GzlBwr.md | 5.25 | R1 | Diffusion Transformer; slightly stronger |
| 3.5–5.5 | 9VRFPC29nb.md | 4.50 | R1 | Mamba paper; similar quality |
| 5.5–7.5 | aFWUY3E7ws.md | 7.33 | R1 | Sparse System ID; stronger |
| 5.5–7.5 | TYXtXLYHpR.md | 5.75 | R1 | Transparent TSF; stronger |
| 5.5–7.5 | Vz0CWFMPUe.md | 5.80 | R1 | TimeInf; stronger |
| 5.5–7.5 | ecIvumCyAj.md | 5.75 | R1 | MoE-F; stronger |
| 7.5–8.5 | vpJMJerXHU.md | 8.00 | R1 | ModernTCN; much stronger |
| 7.5–8.5 | bWcnvZ3qMb.md | 8.00 | R1 | FITS; much stronger |
| 7.5–8.5 | k38Th3x4d9.md | 8.00 | R1 | Root cause analysis; stronger |
| 7.5–8.5 | xriGRsoAza.md | 8.00 | R1 | Interpretable TSC; stronger |
| >8.5 | (none) | — | R1 | No anchors found |

**Round 2 (narrowing, 3.5–6.5):**

| Path | Avg Score | Comparison |
|------|-----------|------------|
| 4F1a8nNFGK.md (CiK) | 5.00 | Most directly comparable; text+TSF benchmark; *same score range* |
| hKeHfOUCXL.md | 4.25 | Energy forecasting benchmark; weaker |
| 3rBu7dR7rm.md | 4.33 | Unified TSF benchmark; weaker |
| 9EBSEkFSje.md | 5.25 | GIFT-Eval benchmark; comparable |
| 53gU1BASrd.md | 4.50 | Financial TSF; weaker |
| mfc6FKgtQA.md (TGTSF) | 5.00 | Most directly comparable; text-guided TSF with cross-attention; *same score range, same weaknesses* |

**Initial bracket (Round 1):** 4.5–5.5

**Narrowed assessment (Round 2):** Score 5.0 — The paper sits firmly alongside the TGTSF paper (5.00) and CiK benchmark (5.00), which share the same core idea (text + time series), the same types of contributions (benchmark + model), and the same critical weakness (missing exogenous-variable baselines). The paper is stronger than CRAFT (4.25) due to better benchmark design, but weaker than TimeInf (5.80) and Interpretable Sparse System ID (7.33) which have more complete evaluations.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>