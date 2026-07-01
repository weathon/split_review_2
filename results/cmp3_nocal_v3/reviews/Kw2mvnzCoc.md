## Summary

TSPulse proposes a family of ultra-light (1M parameter) pre-trained time-series models for four diagnostic tasks: classification, anomaly detection, imputation, and similarity search. The architecture uses a TSMixer backbone with three embedding segments (temporal, spectral, semantic) trained via multi-objective reconstruction losses, alongside a hybrid masking strategy and lightweight post-hoc fusers (TSLens, Multi-Head Triangulation). The claimed contributions center on "disentangled representations across spaces and abstraction levels," a compact design enabling CPU-friendly inference, and zero-shot transfer across tasks.

## Strengths

1. **Genuine efficiency advantage is well-supported.** The 1M-parameter design delivers measured CPU inference of 0.387ms versus 5.51ms for MOMENT (14×) and 46.71ms for Chronos (120×) in Table 7 (similarity search). This concrete efficiency edge is the paper's most unqualified contribution and is supported by clear, verifiable numbers.

2. **Hybrid masking is a practical and well-ablated improvement.** The ablation in Table 1(c) is decisive: removing hybrid pre-training causes a 79% MSE degradation under hybrid-mask evaluation. The mechanism (exposing the model to diverse missing patterns beyond fixed block masking) is intuitive, and the effect size is large. This component likely works as claimed.

3. **Ablation studies are reasonably broad.** Table 1(b) tests 8 design variants with degradations from 2–16%, providing a useful map of which components matter most. The identity initialization for channel mixers (9% drop when removed) is a sensible if incremental improvement.

4. **Sensitivity analysis provides supporting evidence for embedding differentiation.** Table 2 shows temporal embeddings have 130% distortion under phase shifts while semantic embeddings have 12%, confirming the different segments encode different information. This does not prove "disentanglement" in the strong sense but shows the multi-objective losses induce different behaviors.

## Weaknesses

### Fatal

None.

### Major

1. **Imputation claim is contradicted by the paper's own results.** The paper states (Section 4.3): *"Compared to statistical interpolation methods, TSPulse shows 50%+ gains."* However, Table 6 (Figure 6) reports Interpol at MSE **0.039** and TSPulse (ZS) at MSE **0.074** — meaning Interpol outperforms TSPulse ZS by 47% (lower MSE is better). The IMP column for Interpol is marked "-" (blank), which obscures this contradiction. TSPulse FT (MSE 0.039) matches Interpol, so the fine-tuned variant is competitive, but the zero-shot imputation claim against statistical methods is false as written. This is not a matter of interpretation; the numbers are in the same table. The paper must either correct the claim or explain why Interpol is not comparable.

2. **"Disentanglement" is terminologically inflated.** The paper's central technical claim is that TSPulse learns "disentangled representations across spaces and abstraction levels." But the mechanism is straightforward multi-objective learning with separate output heads on pre-designated segments of a shared representation. The backbone receives `[Time_E; FFT_E; Reg_E]` as a concatenated sequence that passes through every Mixer layer together (Section 2, encoding: *"The full input to the backbone is constructed by concatenating time, frequency, and register tokens"*), allowing unrestricted information mixing across all three segments. The "disentanglement" is achieved solely by applying different loss functions to different output segments *after* the backbone has already mixed everything. This is not disentanglement in any standard representation-learning sense (β-VAE, FactorVAE, InfoGAN). It is multi-head reconstruction with segment-specific losses. The sensitivity analysis (Table 2) confirms the embeddings *differ*, which is consistent with multi-task learning but does not demonstrate disentanglement. The paper's headline contribution (contribution 2) is built on this framing, and a reader expecting standard disentanglement will find the method does not deliver what it promises.

3. **Task-specific pre-training undermines the generality framing.** Section 3.1 states: *"we specialize the pre-training for every task through reweighting loss objectives to prioritize heads most relevant to the target task."* This means TSPulse is a family of four separate models, each trained with different loss weights. The paper also notes *"there are no practical challenges in pre-training task-specific models."* When the abstract claims TSPulse "outperforms models 10–100× larger" across four tasks and "delivers state-of-the-art zero-shot performance," the comparison is between task-specialized models and general-purpose baselines (MOMENT, Chronos) that use a single set of weights across all tasks. This is an apples-to-oranges comparison. The efficiency and parameter count claims should be calibrated accordingly. A fairer framing would explicitly acknowledge that the user must know the task type in advance and use the corresponding pre-trained weights.

4. **AD "zero-shot" uses labeled data for head selection.** Section 4.1: *"We adopt this [labeled] tuning set for multi-head triangulation to select the best-performing head and report scores on the test set for both zero-shot (TSPulse-ZS) and fine-tuned (TSPulse-FT) variants."* Using a labeled validation set to choose among heads is a hyperparameter selection step that requires labeled data. This is not "zero-shot" in the standard sense (no task-specific labels). While the same tuning set is consistently used across all leaderboard methods, the labeling as "zero-shot" is still misleading and should be qualified.

### Minor

1. **No variance or confidence intervals reported.** Across all four tasks and ~75 datasets, not a single standard deviation, confidence interval, or significance test is reported. The classification improvement (0.733 vs. 0.701 for VQShape, a ~4.6% relative gain) could easily be within per-dataset variance. Without error bars, the reader cannot assess whether reported improvements are robust.

2. **Zero-shot classification results are referenced but not reported.** Figure 5 caption states *"TSPulse (FT) and TSPulse (ZS) consistently outperform other methods"* but the accompanying table shows only TSPulse (FT) at 0.733 with no ZS numbers. The text (Section 4.2) discusses only fine-tuned results. If the model supports zero-shot classification, the results should be shown; if not, the caption should not reference ZS.

3. **Chronos baseline for similarity search is a questionable comparison.** Chronos is a forecasting model, not designed for representation learning or similarity search. Its poor performance (PREC@3 of 0.23 vs. TSPulse's 0.68) is unsurprising and inflates the apparent improvement. The comparison with MOMENT is reasonable, but Chronos should be either justified as a relevant baseline or removed.

### Trivial

- The distortion metric in the sensitivity analysis (Section 6, Table 2) reports "130%" distortion for temporal embeddings under phase shift, but the metric is not defined in the main text (deferred to Appendix A.3) and the numerical scale is hard to interpret without normalization context. The qualitative pattern is clear, but the quantitative values lack an intuitive interpretation.

## Nice-to-Haves

- **Report per-dataset breakdowns for classification.** The mean accuracy across 29 datasets may hide significant variance. A per-dataset table or critical difference diagram would strengthen the analysis.
- **Single-model cross-task evaluation.** The most informative experiment would be training one TSPulse model with a single loss weighting and evaluating it zero-shot on all four tasks, providing a direct comparison to the MOMENT/Chronos paradigm.
- **Report AD zero-shot results without the labeled tuning set** (e.g., using Head_ensemble or a fixed head) to isolate the effect of the triangulation step.

## Removed Points

These points from the input review are removed with justification:

- **"Abstract/Introduction framing is overwrought"** — subjective opinion; the framing is within normal bounds for a conference paper.
- **"Loss weighting not specified"** — Appendix A.9 is referenced; the parser strips appendices, so this cannot be verified from the available text. Per rules, removed.
- **"Distortion metric not formally defined in main text"** — deferred to appendix; removed as an appendix-content concern, though the 130% interpretability issue is retained as Trivial.
- **"1 day with 8×A100 GPUs energy cost"** — a scope-creep nitpick about ethical considerations not standard for a methods paper.
- **"Existing models' entanglement is asserted rather than demonstrated"** — this is standard motivation rhetoric, not a factual claim requiring proof.
- **"Disentanglement overclassification is a 'structural issue'"** — downgraded from the reviewer's framing as Fatal/Structural to Major, since the actual method (multi-objective learning with segment-specific heads on a shared backbone) still produces useful representations with different properties; the term is inflated but the underlying engineering is functional.
- **Missing related works** — cannot verify from available sources.
- **"Mask ratios low (12.5-50%), real-world missingness exceeds 50%"** — speculation about different evaluation regimes; moved to Nice-to-Have.
- **"No per-dataset breakdown"** — a suggestion, not a weakness; moved to Nice-to-Have.

## Novel Insights

The most interesting observation from the review process is the gap between how the paper frames its contribution ("disentangled representations") and what the architecture actually implements. The three embedding segments are never truly separated in the representation space — they share a backbone, a decoder, and only receive different loss signals at the output heads. The sensitivity analysis shows these losses produce different behavioral profiles under perturbation, which is genuinely useful, but this is a property of multi-objective optimization, not of architectural disentanglement. The hybrid masking result (79% degradation when removed) is the strongest empirical finding, and it requires none of the disentanglement framing to stand on its own. This suggests the paper's strongest contribution is orthogonal to its headline claim.

## Suggestions

1. **Drop the "disentanglement" terminology.** Replace with "multi-view" or "multi-objective" representation learning. The paper would be stronger by claiming exactly what it does: three complementary embedding segments trained with different reconstruction objectives on a shared backbone, shown empirically to capture different properties.

2. **Correct the imputation claim.** Either explain why Interpol is not comparable to TSPulse ZS (e.g., Interpol requires knowing which points are missing while TSPulse doesn't) or remove the "50%+ gains over statistical methods" claim.

3. **Acknowledge task-specific pre-training explicitly** in the abstract and contributions. State that TSPulse is a family of task-specialized 1M-parameter models, not a single multi-task model.

4. **Report variance.** Add confidence intervals or per-dataset standard deviations for all main results, especially classification.

5. **Remove or justify the Chronos baseline** in similarity search.

## Score and Decision

The paper has genuine engineering contributions: a compact architecture with hybrid masking that achieves competitive results and a clear speed advantage. The hybrid masking ablation (79% degradation) is strong evidence that this component works. However, the paper contains a concrete numerical contradiction in its headline imputation claim (the 50%+ gains claim is false when compared to the Interpol baseline in the same table), and its central framing around "disentangled representations" and "zero-shot" transfer substantially overstates what the method delivers. These issues need correction, and the imputation claim especially undermines confidence in the reported numbers.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>