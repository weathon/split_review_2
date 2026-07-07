Now I have all the calibration data I need. Let me compile the final review.

Here are the calibration anchors for comparison:

1. **o9YC0B6P2m.md** (Avg: 6.75) - "Scaling Law with Learning Rate Annealing" - Very similar topic (loss curve prediction/form). Stronger on principled mathematical form but less practical application. The paper under review has comparable quality but different strengths.
2. **KnoS9XxIlK.md** (Avg: 6.00) - "A Multi-Power Law for Loss Curve Prediction" - Similar topic. Also limited in scope and theoretical depth. The paper under review has more practical demonstrations (diagnostics, early stopping).
3. **WYL4eFLcxG.md** (Avg: 6.00) - "Scaling Optimal LR Across Token Horizons" - Related (hyperparameter transfer). Similar empirical style at comparable model scales.
4. **d8w0pmvXbZ.md** (Avg: 8.00) - "Small-scale proxies for large-scale Transformer training instabilities" - More rigorous experimental methodology, cleaner claims.
5. **xGM5shdGJD.md** (Avg: 5.20) - "Hitchhiker's Guide to Scaling Law Estimation" - Weaker due to methodological issues.
6. **MLhquJb1qN.md** (Avg: 5.25) - "Time Transfer" - Related topic but less compelling.
7. **iZeQBqJamf.md** (Avg: 6.50) - "Language models scale reliably with over-training" - Stronger empirical work in a similar area.

**Round 1 Bracket:** I place this paper between 5.5 and 7.0.

The paper shares heavy-weight positive items with o9YC0B6P2m (6.75): novel loss-curve analysis with practical utility. But it also shares heavy-weight negative items: unsupported claims (like "optimal τ") and missing rigor (no quantitative collapse metric) that push it below the d8w0pmvXbZ (8.00) anchor. The negative weight items (-5.14, -5.22) are more severe than those in the 6.75 anchor, suggesting the score should be below 6.75. Comparing against KnoS9XxIlK (6.00) and WYL4eFLcxG (6.00), the paper under review has more practical contributions but also more significant unsubstantiated claims. I place it at 6.0.

## Summary

This paper studies the collapse phenomenon of normalized training loss curves (TLCs) across model scales in LLM training. It identifies τ (AdamW timescale), TPP (tokens-per-parameter), and LR schedule as the three controls governing TLC shape, demonstrates that collapse persists at LLM scale (100M–3.9B), introduces the Celerity model family trained under collapse conditions, and shows two practical applications: using collapse residuals as a diagnostic tool for training issues and enabling early stopping in hyperparameter tuning via a parametric surrogate model.

## Strengths

- **Diagnostic application of collapse residuals is genuinely useful and well-demonstrated.** The 1.8B run example (Fig. 1, right panel) shows the collapse residual detects a numerical instability around 60% of training, whereas the raw loss only shows the problem after 90%. The paper traces the root cause to a loss kernel issue at specific microbatch sizes and verifies the fix — a concrete, practical contribution.
- **Scaling of collapse to practical LLM regimes is a real empirical extension.** Qiu et al. (2025) validated collapse only on small autoregressive models with vanilla Adam and no weight decay. This paper demonstrates collapse persists at 100M–3.9B scale with AdamW, weight decay, and a practical µP-based scaling recipe (CompleteP for depth). The identification of τ, TPP, and LR schedule as the three controls (Sec. 3) usefully synthesizes and extends prior scattered observations.
- **The early-stopping procedure (Sec. 5) is well-motivated and the results are clear.** The insight that fixing τ (by co-varying λ) during batch-size sweeps preserves curve ordering (Fig. 7) is practically valuable. The demonstration that the parametric surrogate fit at 111M scale enables reliable hyperparameter selection at 10–30% of training (Fig. 9) is the cleanest experiment in the paper.
- **Celerity provides a useful reference family** trained on open data with consistent methodology, explicitly avoiding benchmark-specific annealing or mid-training practices.

## Weaknesses

### Major

- **The claim that τ is set "optimally" (abstract, lines 31, 139, 210) — and that Celerity is "the first LLM family trained with optimal τ scaling" (line 33) — is not supported by evidence.** There is no τ sweep, no plot showing how τ values were chosen, and no comparison with suboptimal τ alternatives. The optimization section (line 165) says only "LR, τ, batch size tuned small, transferred via scaling rules," but "tuned" is not the same as "optimized to optimality." The paper's thesis that collapse arises when τ is optimal is weakened by this lack of evidence. This is not a fatal flaw — the core collapse phenomenon depends on τ being *matched* across scales, not necessarily *optimal* — but the paper oversells the optimality claim.

- **No quantitative measure of collapse quality.** Qiu et al. (2025) defined "supercollapse" with a clear criterion: normalized curves differ by less than inter-run noise. This paper provides no comparable metric — claims about collapse being "tight" (line 202) are subjective. This also weakens the diagnostic application: without a noise floor for the collapse reference, it is unclear how large a residual must be before it signals a real problem vs. normal variation. The reviewer model weights this as the most severe weakness (-5.22), and rightly so: the paper's main practical tool (diagnostics via residuals) lacks a principled threshold.

### Minor

- **The framing that collapse is a "signature of compute-efficient training" (abstract, line 9, line 31) is in tension with the paper's own primary experimental regime.** Celerity's main TPP band is 234, which the paper's own analysis (Fig. 5, line 145) says requires 67% more FLOPs than the compute-optimal TPP of ~20. While the paper acknowledges this trade-off (lines 143–145: "a responsible balance point"), the abstract and introduction repeatedly use "compute-efficient" without this qualification. The claim conflates "well-tuned training (optimal τ given TPP)" with "compute-efficient training (optimal TPP given budget)." This is a real framing issue that could confuse readers.

- **The comparison with Llama-2 (Fig. 1, left) is presented as evidence that τ is "mis-scaled" in that family (line 31).** However, Llama-2 models vary in TPP from 29 (70B) to 286 (7B) — a 10× range. The paper's own Sec. 3 shows TPP alone modulates TLC shape (Fig. 4). Since both TPP and τ vary, the non-collapse does not specifically isolate τ mis-scaling. The figure caption accurately notes both factors vary, but the text over-attributes to τ.

- **The early-stopping procedure (Sec. 5) is only demonstrated on λ sweeps (Fig. 9; line 284), not on LR or batch-size sweeps.** While the surrogate model is designed to handle varying τ and TPP, the tuning evaluation only tests one type of sweep, limiting the generality of the empirical validation.

### Trivial

- **The concluding claim that "For $1B runs, collapse provides a valuable reference trajectory" (line 300) is speculative** — the paper's largest model is 3.9B parameters, and no evidence is provided for runs at that scale.

## Nice-to-Haves

- The paper's diagnostic application would benefit from an evaluation of specificity: how often does the collapse residual produce false positives? A noise floor for the collapse reference would allow practitioners to know what residual magnitude is actionable.
- The surrogate model could be tested on transferring to a different architecture family or data mix, which would increase practical applicability.
- A comparison against standard learning-curve extrapolation methods (e.g., Domhan et al. 2015) would strengthen the early-stopping evaluation beyond the simple "choose current best" baseline.

## Removed Points

- **Normalization difference from Qiu et al.:** The harsh critic claimed the paper should be explicit about using a different normalization than Qiu et al. (2025). However, the paper states at line 101: "we consistently found simply dividing by the final training loss (i.e., L̂ = 0 in Eq. (1)) resulted in optimal alignment across scales, so use this for all curves." The paper is already explicit. REMOVED (factually inaccurate).
- **Scope of surrogate model (architecture/data constant):** The critic noted the surrogate is tested only with held-constant architecture and data distribution. The paper's stated scope is transfer within the same model family; demanding cross-family validation is scope creep. REMOVED.
- **Weak baselines in early stopping:** The critic asked for Bayesian optimization baselines. The paper's contribution is a specific collapse-based approach, not a general HPO benchmark; the chosen baselines (random, current best) are natural comparisons for practitioners. REMOVED.
- **Number of parameters in surrogate model:** The critic questioned whether the parametric complexity is justified. The paper explains the fitting procedure and demonstrates it works; this is a descriptive model, not a theoretical claim. REMOVED.
- **Scale-invariance assumption unverified:** The paper explicitly states "Provided residual bias at end-of-training is negligible relative to the variance floor" — this is a stated caveat. REMOVED.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide evidence for the claimed τ optimality: show a τ sweep at one representative scale demonstrating that the chosen τ minimizes final loss, or else qualify the "optimal" language.
2. Add a quantitative collapse metric (e.g., RMS deviation across normalized curves) to make collapse quality assessments objective and to calibrate the diagnostic residual threshold.
3. Qualify the "compute-efficient" framing in the abstract/introduction to distinguish between "being on the compute-accuracy Pareto frontier" and "Chinchilla/Hoffmann compute-optimal."
4. Consider testing the early-stopping procedure on LR or batch-size sweeps to demonstrate generality.
5. Run a controlled experiment where TPP is fixed and τ is varied to directly demonstrate τ's causal role in enabling/breaking collapse.

## Score and Decision

**Bracket determination (Round 1):** I place this paper between 5.5 and 7.0 based on comparison with the calibration anchors. The paper shares heavy-weight positive items with the 6.75 anchor (o9YC0B6P2m: novel loss-curve analysis with practical utility) — both have strong positive weights for empirical findings and practical applications. However, the paper under review also carries heavier negative items: the unsupported "optimal τ" claim (-5.14) and the missing quantitative collapse metric (-5.22) are more severe than the negative items in that anchor (max -3.98 for the 6.75 paper). Compared to KnoS9XxIlK (6.00) and WYL4eFLcxG (6.00), the paper has more practically demonstrated contributions (diagnostics, early stopping) but also more significant evidentiary gaps. The most methodologically rigorous anchor (d8w0pmvXbZ, 8.00) shows that cleaner claims and fuller evidence raise the score considerably above this paper.

**Final score: 6.0.** The paper makes two genuine contributions — scaling collapse to practical LLM regimes with clean identification of the three controls, and demonstrating the practical diagnostic value of collapse residuals. The early-stopping procedure is also well-executed. However, the unsupported "optimal τ" claim and the absence of a quantitative collapse metric are significant gaps that prevent the paper from being a strong accept. The framing overreach (equating collapse with compute-efficiency) further detracts. These issues are addressable, and the paper's core empirical findings are sound.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>