Now I have all the calibration information I need. Let me write the final review.

**Round 1 bracket**: [6.5, 7.5]. The paper is clearly above the ~6.0 anchors (Multi-Power Law for Loss Curve Prediction, Scaling Optimal LR) because it offers broader contributions (model family + theoretical framework + practical applications) at larger scale (3.9B vs. 400M params). It is slightly below the 7.33 u-μP anchor, which had cleaner claims with fewer caveats, and well below the 8.0 Small-Scale Proxies paper, which was exceptionally clean.

**Narrowing**: The 6.50 "Language models scale reliably" anchor had comparable experimental scale but its weaknesses (-9.26, -9.96, -9.98) were about scope limitations (no multimodal, no post-training). My paper's two major weaknesses (-10.00, -9.91) are about overclaiming and narrow evaluation — real but bounded. My paper's strengths include theoretical grounding (noisy-quadratic model) that the 6.50 anchor lacks, plus an actual trained model family. This places it above 6.50. Compared to u-μP (7.33), my paper has more breadth but less clean execution on the diagnostic claim. Final score: **7.0**.

## Summary

The paper shows that training loss curves (TLCs) collapse across model sizes (100M–3.9B parameters) under μP when tokens-per-parameter (TPP) and the AdamW timescale τ are matched. It identifies τ as the key operational variable governing TLC shape, explains this via a noisy-quadratic model (Eq. 3), and introduces the Celerity model family trained in this collapse regime. Two applications are demonstrated: (1) collapse residuals as a diagnostic for training pathologies, and (2) early stopping in hyperparameter tuning via a parametric surrogate fitted at small scale.

## Strengths

- **Extending collapse to practical LLM scale with a clear explanatory framework.** The paper demonstrates TLC collapse at 100M–3.9B parameters (10× larger than Qiu et al. 2025) under practical co-scaling of width, depth, batch size, and weight decay. The identification of τ (AdamW timescale) as the specific optimizer control governing collapse — and the connection to a bias–variance trade-off via the noisy-quadratic model (Eq. 3) — is a genuine conceptual advance. The empirical sweep in Fig. 3 convincingly shows that curves cluster by τ value across sweeps of η, λ, or B. **[impact=+10.00]**

- **Celerity is a concrete, competitive model family.** The compute-efficiency frontier plot (Fig. 2) places Celerity models at the upper-left edge comparing average accuracy vs. training FLOPs against diverse open models (Llama-2, OLMo, Gemma, SmolLM, etc.). The 75% FLOP reduction vs. BTLm at comparable accuracy is striking. The paper is transparent about where Celerity is weaker (parameter efficiency at inference, Sec. 4). The TPP=234 trade-off analysis (Fig. 5) and the "bands" philosophy (fixed-TPP bands with optimal τ) are well-reasoned design choices. **[impact=+9.65]**

- **The early-stopping procedure is practical and well-evaluated.** The core idea — fit a parametric surrogate (Eq. 4–5) for normalized TLCs at small scale, then align partial large-scale curves to predict final loss — is grounded in collapse. Fig. 9 shows that "predicted best" achieves near-zero loss gap after 10–30% of training, while "current best" (standard practice in some labs) fails in the 1.7B case. The alternating fitting procedure for b and q is pragmatic and reduces grid-search cost. **[impact=+10.00]**

- **The diagnostic case study is compelling.** The 1.8B run where collapse residuals revealed divergence at ~60% of training — well before the raw loss showed an uptick at ~90% — provides a concrete demonstration of practical value. The debugging story (confirming a numerical kernel issue via ablation, restarting with the fix, tracking the reference afterwards) is complete and credible. **[impact=+8.07]**

## Weaknesses

### Fatal
None.

### Major

- **The diagnostic claim (collapse residuals as an early warning system) is overclaimed given the evidence.** The abstract states "deviation-from-collapse provides a sensitive, early diagnostic of training pathologies" as a core contribution, and the same tone recurs in the conclusion. The entire evidence is a single case study (the 1.8B/234-TPP run with a numerical kernel issue). This is a compelling anecdote but does not constitute a validated diagnostic method: we are not shown whether deviations from collapse *always* precede visible loss issues, what the false-positive rate is, whether the residual threshold generalizes across architectures/tokenizers/data distributions, or whether some deviations are benign (the paper itself notes that at 234 TPP "divergences appear late in training for larger models... loss improves disproportionately on training data, while held-out data remains aligned with projections," indicating some deviations are benign data-distribution effects). The claim should be scoped down to "a promising demonstration" or accompanied by systematic validation (e.g., simulated pathologies at small scale with characterization of detection latency vs. false alarms). This does not invalidate the paper's core contributions (collapse at scale, τ as operative variable, Celerity, early stopping), all of which are solidly supported. **[impact=-10.00]**

- **The evaluation of Celerity is narrow for a "compute-efficiency frontier" claim.** Only 7 multiple-choice commonsense reasoning tasks (arc-c, arc-e, boolq, hellaswag, piqa, siqa, winoqrande) are used. Modern LLM evaluation typically spans knowledge (MMLU, MMLU-Pro), coding (HumanEval, MBPP), math (GSM8K, MATH), instruction following, and long-context tasks. The paper's philosophy — avoiding task-specific data annealing that makes evaluation problematic — is reasonable, but the claim of being on the "compute-efficiency frontier" is supported only by this thin slice of capabilities. Broader evaluation (even without data annealing) or more qualified claims would strengthen the paper. **[impact=-9.91]**

### Minor

- **Collapse has documented deviations whose boundaries are not crisply characterized.** The paper honestly acknowledges small early deviations at 20 TPP (attributed to differing LR warmup proportions, Table 2: "min(10% of total tokens, 375M tokens)" applies proportionally differently across model sizes) and late-training divergences at 234 TPP (attributed to data-distribution effects). While these explanations are plausible, practitioners lack guidelines for when collapse can be expected to hold and how to handle these boundary cases. The warmup design directly explains the 20-TPP deviations but the paper does not discuss whether matching warmup proportions would further improve collapse. **[impact=-0.19]**

- **The normalization strategy for in-training diagnostics has an unanalyzed circularity risk.** The "early-align" method selects L(T) by best-aligning the partial curve with the smallest-scale curve over the 25–50% portion of training. If a divergence begins within that alignment window, the normalization itself becomes contaminated. The paper acknowledges this worked safely for the 1.8B case (detection at 60%, alignment window 25–50%), but there is no analysis of how robust the diagnostic is to the choice of alignment window or how to detect contamination. **[impact=-0.00]**

### Trivial

- **The "r" values reported in Fig. 6 (r=0.175, r=0.087, r=0.051) are never defined or explained.** It is unclear what quantitative measure of collapse quality is being reported. **[impact=-10.00]** *(Note: despite the high impact magnitude, this is genuinely a trivial presentation issue — easily fixable by adding a definition.)*

## Nice-to-Haves

- Broaden Celerity evaluation to include at least one knowledge benchmark (e.g., MMLU subset) and one coding benchmark to strengthen the compute-efficiency frontier claim.
- Provide systematic validation of the diagnostic application: simulate known training pathologies (e.g., spike injection, LR schedule corruption) at small scale and characterize detection latency vs. false-alarm rate.
- Compare normalization schemes (dividing by final loss vs. Qiu et al.'s affine method) to justify the simplification more rigorously.
- Discuss guidelines for when collapse can be expected to hold (proportionally matched warmup, TPP not too extreme, etc.).

## Removed Points

- *"No statistical characterization of collapse quality"* — Removed because the paper reports "r" values (even if undefined, a quantitative measure exists). The undefined "r" concern is folded into the Trivial weakness above.
- *"Surrogate model not validated against held-out controls"* — Removed. The paper evaluates the surrogate at 3.3B scale while fitting on 111M data, which is cross-scale held-out validation. Cross-HP withheld validation is a nice-to-have.
- *"Missing a limitations section"* — Removed. This is a formatting preference, not a scientific weakness.
- *"Lack of normalization scheme comparison (L̂=0 vs. affine)"* — Removed. A brief comparison would strengthen the paper but the absence is at most a nice-to-have.
- *"ROC trade-off between detection latency and false alarms"* — Removed. This goes beyond the paper's stated scope and is folded into the suggestion for systematic diagnostic validation.

## Novel Insights

None beyond the paper's own contributions — the reviews largely validate the paper's framing without introducing new perspectives on the content.

## Suggestions

1. Scope down the diagnostic claim from "provides a sensitive, early diagnostic" to "provides a promising early warning signal, demonstrated in one case study."
2. Add at least one knowledge benchmark (MMLU subset) and one coding benchmark to the Celerity evaluation.
3. Define the "r" metric reported in Fig. 6.
4. Discuss warmup-matching guidelines for maintaining collapse at low TPP values.

## Score and Decision

**Calibration Summary:**

| Anchor | Avg Human Score | Round | Itemized? | Comparison to this paper |
|--------|----------------|-------|-----------|--------------------------|
| A Multi-Power Law for Loss Curve Prediction | 6.00 | R1 | Yes | Narrower scope (LR schedules only), smaller models (400M max), weaker theory. This paper is stronger. |
| Scaling Optimal LR Across Token Horizons | 6.00 | R1 | Yes | Similar empirical scale but narrower contribution (LR scaling only). This paper is broader and more impactful. |
| u-μP: Unit-Scaled Maximal Update Parametrization | 7.33 | R1 | Yes | Cleaner execution, fewer caveats. Similar-strength strengths but this paper has more overclaiming issues. |
| Small-scale proxies for large-scale Transformer training instabilities | 8.00 | R1 | Yes | Exceptionally clean paper. This paper has more breadth but less clean execution. |
| Scaling Law with Learning Rate Annealing | 6.75 | R1 | Yes | Had fatal flaw about zero-LR padding despite high scores. This paper's flaws are bounded. |
| Language models scale reliably with over-training and on downstream tasks | 6.50 | R2 | Yes | Similar scale but this paper has stronger theoretical grounding (noisy-quadratic model) and an actual model family. |

**Bracket (Round 1):** [6.5, 7.5]. The paper is above 6.0–6.5 anchors (broader contribution, larger scale, theoretical grounding) and below the 8.0 anchor (less clean execution). **Narrowing (Round 2):** The paper sits above the 6.50 over-training anchor (stronger theory, actual model family) and slightly below the 7.33 u-μP anchor which had fewer overclaiming issues. Shared high-magnitude items with u-μP: both have +10.00 strengths and ~-10.00 major weaknesses. The deciding factor is that u-μP's weaknesses were about missing comparisons, while this paper's major weaknesses are about overclaiming from thin evidence (diagnostic case study) and narrow evaluation — both real but bounded and fixable.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>