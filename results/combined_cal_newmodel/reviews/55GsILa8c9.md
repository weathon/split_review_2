Now let me construct the final review.

## Summary

This paper introduces CausalNovo, a model-agnostic framework for *de novo* peptide sequencing that aims to improve robustness to spectral noise by learning representations focused on signal (causal) peaks rather than spurious noise peaks. The method identifies signal peaks via theoretical spectrum matching (a well-established domain knowledge approach), learns an attention mask to upweight them, and applies contrastive invariance regularization. Evaluated on three public datasets with three baseline models, CausalNovo reports consistent improvements of +2–12% across amino acid, peptide, and PTM-level metrics, with mechanistic evidence from attention analysis.

## Strengths

- **Well-motivated problem and convincing vulnerability analysis (Figure 1):** The preliminary experiment — replacing noise peaks in trained models and observing performance drops — provides concrete evidence that existing deep learning models rely on spurious correlations with non-signal peaks. The effect is demonstrated across three different models and multiple perturbation thresholds, establishing the problem as systematic rather than model-specific.

- **Consistent improvements across a broad evaluation grid:** CausalNovo is evaluated on 3 datasets × 3 baseline models × 3 metric levels (amino acid, peptide, PTM) plus cross-species validation. Improvements hold across essentially every cell in this grid. On Nine-species, AA precision improves by +2.4–6.3%; on Seven-species, improvements range from +5.0–12.0%. This breadth of consistent improvement is the paper's strongest evidentiary asset.

- **Mechanistic evidence via attention analysis (Table 7):** The paper goes beyond aggregate metrics and analyzes *why* the method works — the fraction of predictions where the model attends to 0/1/2/3 causal peaks among top-3 attended positions. The shift from 12.73% → 10.76% (zero causal peaks) and from 19.26% → 32.87% (all three causal peaks) directly ties the performance gains to the intended mechanism. This internal validation is rare in the peptide sequencing literature.

- **Honest treatment of limitations:** The conclusion explicitly acknowledges the 2.3× training time overhead and the gap between the NovoBench evaluation protocol and the more realistic large-scale-training protocol used by some recent methods.

- **Analysis of peak distinguish strategies (Table 6):** Shows that CausalNovo's advantage grows as the tolerance threshold tightens (from +2.1% RI at threshold 8 to +14.3% RI at threshold 1 on HC-PT), providing evidence that the method specifically helps when distinguishing signal from noise is harder.

## Weaknesses

### Fatal
None.

### Major

- **No measure of variance or statistical significance:** Every result in Tables 1–7 and Figures 1–4 is reported as a single number with no standard deviation, confidence interval, or mention of how many random seeds/trials were run. For improvements as small as +2.2% (AA precision, Nine-species, π-HelixNovo) and +2.4% (CasaNovo), the reader has no way of knowing whether these differences are reliable. The ablation in Table 4 shows increments of +0.4–1.2% per component — these could easily fall within run-to-run variance. This is particularly important because the Seven-species and HC-PT datasets show much larger improvements (+9–14%), but these are datasets where baseline performance itself is very low, meaning higher variance is expected. The paper reports results to three decimal places as if they are deterministic.

- **Missing control for additional training signal:** CausalNovo adds three objectives beyond the baseline cross-entropy loss: (a) a contrastive loss for the independence principle (Eq. 5), (b) a cross-entropy loss on the non-causal representation z_s for purification, and (c) a symmetric version of the contrastive loss. The baseline model is trained with only the standard cross-entropy loss. This means CausalNovo has strictly more training signal and more regularization. The paper does not include a control where the baseline receives comparable auxiliary losses (e.g., a contrastive loss on the *full* representation z, without causal/non-causal splitting). Without this control, some of the gains attributed to causal disentanglement could come from the extra learning signal. The ablation (Table 4) shows each component adds, but it does not test a "baseline + extra contrastive loss (no causal splitting)" condition, which is the most important missing control.

### Minor

- **The causal framing is somewhat inflated relative to what the method actually does.** The paper frames the approach using Structural Causal Models (SCM), Reichenbach's Common Cause Principle, and do-calculus. However, the "causal" peaks are identified by matching to the theoretical spectrum of the ground truth peptide (Eq. 4) — which is direct supervision from known domain knowledge, not causal discovery. The method then learns an attention mask and applies contrastive invariance regularization. The causal formalism (SCM, do-calculus, RCCP) is rhetorical scaffolding applied to what is essentially supervised attention learning with an invariance regularizer. A more accurate description would be: "we use domain knowledge (theoretical spectrum matching) to supervise which peaks are signal, then train representations to be invariant to non-signal peaks." This does not invalidate the method's practical value, but it misrepresents the contribution's nature.

- **The retrained baselines (†) substantially outperform published results** (e.g., CasaNovo on Nine-species: 0.697 → 0.741; on HC-PT: 0.442 → 0.525), meaning a large fraction of the total improvement over published numbers comes from better training configuration, not from CausalNovo. The paper should discuss what changed in retraining and whether the baselines were tuned independently.

- **InstaNovo's very poor performance (0.420 AA precision on Nine-species — far below even DeepNovo at 0.696 from 2017) is included without comment.** Either the evaluation configuration is inappropriate for InstaNovo, or it is a very weak method on this benchmark. Including such a poor baseline without explanation weakens the comparison table.

### Trivial
None.

## Nice-to-Haves

- A control experiment where the baseline receives the same *amount* of additional training signal (contrastive loss + auxiliary cross-entropy) applied to the full latent representation z (without causal/non-causal splitting). If CausalNovo still outperforms this control, the claim that the causal splitting itself is beneficial would be substantially strengthened.
- Reporting results across multiple random seeds (at least 3) to allow readers to assess whether improvements of 0.4–2.4% are reliable.
- A brief discussion of what changed in retraining that caused baselines to substantially outperform their published numbers.

## Removed Points

- **"Figure 4 caption error ('CausalNovo + CausalNovo')":** The parser-extracted text shows "CausalNovo + CausalNovo (ours)" in the legend, but this is a known parser artifact from figure caption extraction of embedded images, not an error in the submitted figure. Removed as a formatting artifact.
- **"Missing comparison with GraphNovo or PepNet":** These are mentioned in Related Work but the paper follows the NovoBench protocol which provides standardized comparisons. The paper already compares with 7 other methods including the most recent ones. Removed as scope creep — no paper can compare with every method.
- **Harsh critic's claim that the causal framework is a "structural issue":** Demoted from structural/fatal to Minor because the method genuinely uses causal principles (causal intervention via do-operator approximation, independence and sufficiency principles derived from the SCM). The concern is about framing precision, not methodological validity.
- **Harsh critic's claim that the paper "does not discover causal structure from data":** The paper never claims to discover causal structure — it claims to "learn the causal representations" and "disentangle causal representations from spurious noise peaks." The reviewer set up a strawman. The actual claim (using domain knowledge to supervise causal factor identification) is accurately described in the paper.

## Novel Insights

None beyond the paper's own contributions. The reviews surface one useful observation: the causal framing, while not incorrect, is heavier than necessary — the core contribution is well-described as supervised attention learning with invariance regularization using known domain knowledge. This reframing would help readers better understand what the method actually does.

## Suggestions

1. Add variance/error bars for all main results by running multiple random seeds (at least 3).
2. Add the missing control experiment: train the baseline with the same auxiliary losses applied to the full latent representation z (without causal/non-causal splitting).
3. Temper the causal framing — acknowledge explicitly that causal factors are identified using known domain knowledge (theoretical spectrum matching) rather than discovered from data.
4. Explain what changed in retraining that caused baselines to substantially outperform their published numbers.
5. Add a brief note about InstaNovo's poor performance — whether it reflects a misconfiguration or a genuine limitation.

## Score and Decision

**Calibration summary:**

| Anchor Paper | Path | Avg Human Score | Round | Itemized | Comparison |
|---|---|---|---|---|---|
| RankNovo | 87B3zDRMjv.md | 5.50 | Bracketing | Yes | Same domain, similar contribution type. RankNovo's weaknesses were more severe (limited novelty -2.58, reliance on base models -2.58) and its strengths lower than my paper's. My paper is clearly stronger. |
| ReNovo | uQnvYP7yX9.md | 6.50 | Bracketing | Yes | Same domain, accepted. ReNovo had similar "missing variance" weakness (favorability=1.09) plus more negative weaknesses (missing RAG work -3.54, unfair comparison -3.33). My paper's worse weakness is "missing control" (-1.61), which is less severe. Comparable quality. |
| MADGEN | 78tc3EiUrN.md | 6.00 | Narrowing | Yes | Mass-spec domain. Had major weaknesses (no baseline comparison -3.03, novelty concerns -1.74, very low predictive retrieval). My paper's evaluation is substantially stronger. |
| Distilling NAT→AT | I2ZYngkRW6.md | 4.25 | Bracketing | Yes | Same domain, rejected primarily on novelty/engineering concerns. My paper has much clearer novelty. |

**Round 1 bracket:** After comparing against RankNovo (5.50, below my paper) and ReNovo (6.50, comparable), I bracketed the paper at **5.5–6.5**.

**Round 2 narrowing:** After itemizing MADGEN (6.00) and comparing its weaknesses against my paper's, I narrowed to **5.5–6.5**, favoring the upper half.

**Final score determination:** My paper shares key strengths with accepted papers in this domain (broad evaluation, mechanistic evidence, honest limitations) while having fixable weaknesses (missing variance, missing control). ReNovo was accepted at 6.50 despite having missing variance and more severe related-work omissions. My paper's main gap — the missing control for extra training signal — is a genuine concern but is addressable in a revision (simply running one additional experiment). The core method is sound and practically useful. Placing the score just below ReNovo to reflect the extra control issue yields **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>