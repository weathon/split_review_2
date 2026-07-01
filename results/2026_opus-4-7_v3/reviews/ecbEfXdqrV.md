Now I have read the full paper. Let me draft the review before calibration.Now let me run the calibration search — Round 1 bracketing:Let me read some of the most topically relevant anchors to calibrate:Now let me form my bracket and finalize.

**Round 1 Bracket Analysis:**

Comparing the paper under review against the retrieved anchors:

- **Score <1.5**: Papers with fundamental flaws — clearly not applicable here. The paper under review is a complete, well-executed study.
- **Score 1.5-3.5**: 6Z8rZlKpNT (3.40) — NF for OOD via latent density. Rejected for limited novelty and insufficient experiments. The paper under review is substantially stronger experimentally.
- **Score 3.5-5.5**: Vi6p2TeujL (4.25) — PTAD tabular AD. SabhfFUfA1 (4.67) — VAE for OOD. These have merit but significant weaknesses. The paper under review has stronger experiments.
- **Score 5.5-7.5**: 7QDIFrtAsB (5.75) — score-based tabular AD, rejected despite extensive experiments, criticized for limited novelty (applying existing NCSN to AD). Very similar in scope to this paper. jQ596tXT3k (5.67) — explaining OOD paradox, rejected, thematically very close but proposes a novel method. 7VkHffT5X2 (6.75) — AnoLLM, accepted, introduces novel framework. lNZJyEDxy4 (6.67) — MCM, accepted, novel masking strategy.
- **Score 7.5-8.5**: Strong papers with clear novel contributions.

**Initial bracket: 4.5–6.0**

The paper has comprehensive experiments but no novel method; its definition has real issues; the theory relies on too-strong assumptions. It's stronger than 3.5-4.5 papers but lacks the methodological novelty of 6.5+ accepted papers. The closest comparator (7QDIFrtAsB, score 5.75) was rejected despite similar scope and even proposes modifications to the model — this paper uses NICE unchanged.

Now let me write the final consolidated review.

---

## Summary
This paper investigates whether the well-known "counterintuitive likelihood" phenomenon — where deep generative models assign higher likelihoods to out-of-distribution data than in-distribution data — transfers from the image domain to tabular anomaly detection. Through comprehensive experiments on all 47 tabular and 10 CV/NLP embedding datasets from ADBench, the authors show that a simple normalizing flow (NICE) with likelihood thresholding (NF-SLT) consistently outperforms 12 baselines. The paper proposes a formal definition of the counterintuitive phenomenon (Definition 3.3) and provides theoretical/empirical analysis linking the rarity of the phenomenon in tabular data to lower dimensionality and weaker feature correlation.

## Strengths

- **Comprehensive, selection-bias-free empirical evaluation**: Table 1 shows NF-SLT achieves the best average AUROC (0.8575 vs. next-best ICL at 0.8208), best average rank (3.43), highest Top2 Ratio (0.45), and lowest Fail Ratio (0.02) across all 47 ADBench tabular datasets. The ~4-point AUROC gap over the next-best method is substantial. Using all datasets without cherry-picking directly addresses the selection-bias concern of Shwartz-Ziv & Armon (2022). NF-SLT also outperforms all deep models on 9 of 10 CV/NLP embedding datasets (Table 1, bottom).

- **Practically actionable finding**: Demonstrating that a simple, off-the-shelf normalizing flow outperforms 12 established baselines (including deep methods like ICL, NeuTraLAD, MCM) challenges the widespread assumption that likelihood-based detection is unreliable. This is directly useful for practitioners in the tabular domain where most real-world anomaly detection is deployed.

- **Dimensionality-reduction experiments provide directional support for theory**: Table 2 shows that under the H(P) > H(Q) condition, reducing dimensionality via ICA consistently improves AUROC for the counterintuitive direction (e.g., CIFAR-10/SVHN from 0.3311 at d=1024 to 0.3143 at d=30) while degrading it for the trivial direction (SVHN/CIFAR-10 from 0.9917 to 0.8520). This matches Theorem 5.4's predictions.

- **Quantitative contrast between tabular and image domains via d Ratio**: Table 4 shows tabular d Ratios (~0.3–0.8) are orders of magnitude higher than image d Ratios (~0.002–0.02), providing a concrete, measurable axis of comparison. The right panel of Figure 1 visually confirms this — tabular points cluster near the identity line while image points fall far below.

## Weaknesses

### Fatal
None

### Major
1. **Definition 3.3 is operationally incomplete and conceptually misaligned with the phenomenon** — This is listed as the paper's first contribution, but threshold parameters β and γ are never specified with concrete values. Section 4 applies the definition qualitatively ("the minimum performance difference between MCM and AUROC is 0.02" — line 124), not as a formal test. More fundamentally, Definition 3.3 captures *relative underperformance against baselines* rather than *likelihood inversion* per se. A generative model could underperform baselines due to insufficient capacity, poor optimization, or misspecified architecture — none of which constitute the counterintuitive phenomenon. Conversely, mild likelihood inversion could occur without triggering the definition if baselines also struggle. The paper acknowledges the difficulty of directly measuring likelihood inversion (Section 1, page 2: "the argument would consider any result outside 100% AUROC as counterintuitive"), but the proposed alternative introduces its own logical gap — it substitutes a different, only loosely related quantity for the phenomenon of interest. Since this is claimed as a primary contribution, the gap is significant, though it does not undermine the empirical results in Table 1.

2. **Theorem 5.4's independence assumption is too restrictive for its claimed explanatory role** — The theorem requires P = ∏pᵢ and Q = ∏qᵢ (product distributions), meaning exactly independent features. The paper acknowledges this for Table 3 ("independence between pixels is not guaranteed, so the theorem presented in Appendix D cannot be applied" — line 164), but the same caveat applies to tabular data. No real tabular dataset has exactly independent features, yet the paper presents the theorem as explaining *why* tabular data avoids the counterintuitive phenomenon. The theorem provides useful directional intuition — higher dimension can amplify likelihood inversion under the H(P) > H(Q) condition — but the paper overreaches in drawing a causal explanation for real data from a result that strictly holds only for product distributions.

### Minor
1. **Feature correlation analysis is associational, not causal** — Section 5.2 argues: low feature correlation → high d Ratio → better likelihood-based detection. The evidence is that tabular datasets have higher d Ratios than images (Table 4, top), and that among datasets where NF-SLT underperforms (rank ≥ 3), most have lower d Ratios (Table 4, bottom). But confounders are not controlled — lower d Ratio could correlate with other dataset properties (sample size, anomaly type, distributional overlap) that independently affect detection. An intervention (e.g., injecting correlations into tabular features and measuring NF-SLT degradation) would move this from associational to causal.

2. **Table 3 shows non-monotonic and contradictory results** — CIFAR-100/SVHN at 16×16 has AUROC 0.4448 but drops to 0.3918 at 8×8 (non-monotonic, unexplained). The CelebA/SVHN case with SVHN as in-distribution shows *increasing* AUROC (0.9830→0.9968→0.9982) as dimension decreases, which contradicts the theorem's prediction for the H(P) < H(Q) direction. The paper attributes this to bilinear interpolation "strengthening the correlation between image pixels" (line 176), which is post-hoc reasoning that is difficult to verify.

3. **Only NICE architecture in main results** — The main experiments use only NICE, one of the simplest and oldest normalizing flow architectures. The paper mentions other flows in Appendix G, but a finding about normalizing flows in general would be more convincing if the main body demonstrated robustness across architectures (e.g., RealNVP, MAF).

### Trivial
None

## Nice-to-Haves
- Replace Definition 3.3 with a direct measure of likelihood inversion (e.g., fraction of anomalous test points assigned higher likelihood than the median normal test point) to ground the paper in the actual phenomenon.
- Close the causal loop in Section 5.2 by running NF-SLT on tabular datasets with artificially injected feature correlations of varying strength.
- Relax Theorem 5.4's independence assumption to bounded pairwise correlation, making it applicable to real datasets.
- Discuss connections to the broader literature on tabular vs. image domain differences (e.g., why tree-based methods outperform deep learning on tabular data), which may share causal factors with the paper's findings.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Equation (3) formulation concern**: The reviewer claimed the min-based formulation doesn't naturally capture the intended phenomenon. On re-reading, the min ensures that ALL models outperforming NF-SLT do so by at least γ — a reasonable (if strict) way to operationalize Assumption 3.2. The reviewer's specific example was partially confused about the mechanics of the equation.
- **Hyperparameter selection bias toward simple methods**: The concern that selecting a single hyperparameter set across all datasets may favor architecturally simple methods is speculative. The paper's approach (selecting best average performance) is standard and avoids per-dataset overfitting.
- **Missing direct measurement of likelihood inversion**: Moved to Nice-to-Haves — this is a suggestion for a stronger alternative methodology, not a weakness of the current work.
- **Missing engagement with broader tabular ML literature**: Removed per the rule against mentioning missing related works.

## Novel Insights
The paper's most distinctive contribution is the empirical demonstration — across an unusually comprehensive benchmark — that the image-domain intuition about likelihood failure does not transfer to tabular settings, coupled with the d Ratio metric as a quantitative proxy for feature correlation. The observation that CV/NLP *embeddings* also avoid the counterintuitive phenomenon because their d Ratios are higher than raw pixels (Section 5.2, estimated ID of 23 and 18 vs. ambient dimension 1000) provides a unifying perspective connecting the tabular and image findings and is consistent with Kirichenko et al. (2020)'s observation that embeddings alleviate the phenomenon.

## Suggestions
- Specify concrete values for β and γ in Definition 3.3 (or conduct sensitivity analysis across values) so it can function as an applicable test rather than a qualitative framing device.
- Add the interventional correlation experiment to move the Section 5.2 argument from associational to causal evidence.
- Include results for at least one additional flow architecture (e.g., RealNVP or MAF) in the main body to demonstrate architecture robustness.
- Consider a relaxation of Theorem 5.4 that permits bounded correlation to make the theoretical result applicable to real data.
- Reframe the paper's contributions more honestly: the primary contribution is the comprehensive empirical finding; the definition and theory are supporting analyses, not standalone contributions of equal weight.

## Score and Decision

### Calibration Anchors

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Uj0h13lVrR | 1.00 | R1 | KL for GFlowNets — fundamentally flawed, not comparable |
| nSDOkm0SKo | 1.00 | R1 | Neural networks for financial news — not comparable |
| P49gSPmrvN | 1.00 | R1 | UMAP for scientific discourse — not comparable |
| 5lUdTogEL3 | 1.00 | R1 | Lifelong person re-ID — not comparable |
| 6Z8rZlKpNT | 3.40 | R1 | NF for OOD via latent density — limited novelty and experiments; paper under review is substantially stronger experimentally |
| i28ZjVxl81 | 2.50 | R1 | OOD prediction on CPU — limited scope; paper under review is much stronger |
| rcmhydaEJp | 3.00 | R1 | Flow-based imputation — limited novelty; paper under review has stronger empirical contribution |
| 3qDhqj6qfu | 3.00 | R1 | TabKANet — different task; paper under review has more comprehensive experiments |
| Vi6p2TeujL | 4.25 | R1 | PTAD tabular AD — novel method proposed but weaker experiments; paper under review has stronger empirical results but less methodological novelty |
| SabhfFUfA1 | 4.67 | R1 | VAE for OOD — novel LPath principle; paper under review has stronger experiments but less novel method |
| SYI409tbsv | 4.60 | R1 | Clustering-based AD framework — novel theoretical framework; paper under review has stronger tabular experiments |
| ws0F5NTzGw | 4.50 | R1 | AdapTable TTA — different setting; paper under review is slightly stronger empirically |
| 7QDIFrtAsB | 5.75 | R1 | **Closest comparator** — score-based tabular AD with extensive ADBench experiments. Rejected despite good results. Proposes modifications to NCSN; paper under review uses unmodified NICE. Similar scope but paper under review has no novel method. |
| 7VkHffT5X2 | 6.75 | R1 | AnoLLM — accepted; introduces genuinely novel framework for tabular AD. Paper under review lacks comparable methodological novelty |
| lNZJyEDxy4 | 6.67 | R1 | MCM for tabular AD — accepted; novel masking strategy. Paper under review lacks comparable novelty |
| jQ596tXT3k | 5.67 | R1 | **Thematically close** — explains OOD paradox via likelihood peaks. Rejected. Proposes a novel LID-based detection method; paper under review proposes no new method |
| cJs4oE4m9Q | 8.00 | R1 | Deep orthogonal hypersphere — strong novel method, clearly stronger paper |
| ZCOwwRAaEl | 8.00 | R1 | Latent BO via normalizing flows — strong novel method, clearly stronger |
| k38Th3x4d9 | 8.00 | R1 | Granger causal for time series AD — comprehensive method and theory, clearly stronger |
| I5lcjmFmlc | 8.00 | R1 | Robust classification via diffusion — strong method, clearly stronger |

**Round 1 bracket: 4.5–6.0**

**Narrowing rationale:** The paper is clearly above the 3.0–4.5 range (stronger experiments, clearer contribution) but below the 6.5+ accepted papers (which all propose novel methods). The closest comparators are 7QDIFrtAsB (5.75, rejected — NCSN for tabular AD with extensive experiments, criticized for limited novelty) and jQ596tXT3k (5.67, rejected — explaining OOD paradox with likelihood peaks). Both were rejected despite having comparable or greater novelty than the paper under review. The paper under review has arguably the strongest empirical evaluation of any anchor in its range, but it proposes no new method at all — NF-SLT is unmodified NICE with a threshold — and its claimed theoretical/definitional contributions have significant gaps. The comprehensive evaluation is a genuine strength, but the theoretical framing (claimed as primary contributions) underdelivers.

**Final score: 5.0**

The paper addresses an interesting and practically relevant question with compelling empirical evidence (Table 1's comprehensive results are its strongest asset). However, two of its three claimed contributions — the definition and the theoretical analysis — have meaningful gaps. Definition 3.3 is operationally incomplete and conceptually misaligned with the phenomenon it purports to formalize. Theorem 5.4's independence assumption is too restrictive to explain real data. No novel method is proposed. Compared to rejected anchors at 5.67–5.75 that address similar questions but propose novel methods, this paper's contribution rests primarily on a useful empirical finding wrapped in underdeveloped formalism.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>