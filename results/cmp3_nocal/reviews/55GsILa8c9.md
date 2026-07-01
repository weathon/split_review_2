Now I'll write the final consolidated review.

## Summary
This paper proposes CausalNovo, a model-agnostic training framework for de novo peptide sequencing that aims to make models focus on signal fragment ions rather than noise peaks. The method uses domain knowledge from fragmentation chemistry to identify signal vs. noise peaks, applies a replacement-based perturbation to noise peaks, and trains models to learn representations invariant to such perturbations via contrastive learning and information-theoretic objectives. Experiments across three datasets and three baselines show consistent improvements at the amino acid, peptide, and PTM levels.

## Strengths
1. **Well-motivated problem with preliminary evidence (Figure 1):** A clean experiment shows that replacing noise peaks in test spectra causes existing models' precision to degrade, and tightening the m/z tolerance amplifies the degradation. This convincingly demonstrates that current models rely on spurious correlations with non-signal peaks.

2. **Consistent across-the-board improvements (Tables 1–3):** CausalNovo improves all three baseline models (CasaNovo, AdaNovo, π-HelixNovo) on all three datasets (Nine-species, Seven-species, HC-PT) at amino acid, peptide, and PTM levels. Improvements range from ~1% to ~15%, with larger gains on harder datasets. Cross-species validation (Table 3) shows gains on every held-out species.

3. **Mechanistic evidence via attention analysis (Table 7):** The fraction of predictions where the model attends to zero causal peaks drops from 12.73% to 10.76%, while the fraction attending to three causal peaks rises from 19.26% to 32.87%. This directly supports that the training objective changes model behavior in the intended direction.

4. **Robustness across noise-signal ratios (Figure 4):** Gains hold across varying NSR levels for all three baselines, supporting the claim that the method focuses on signal rather than noise.

## Weaknesses

### Fatal
None.

### Major
- **No variance or uncertainty estimates are reported anywhere in the paper.** All tables contain single numbers per metric with no standard deviations, confidence intervals, or mentions of multiple random seeds. Given that some improvements are small (e.g., +1–2% on several metrics), run-to-run variance could affect the interpretation of individual point estimates. While the overall pattern of consistent improvement across many settings provides implicit evidence of reliability, the paper should report variance for the main comparisons.

### Minor
- **The "causal" framing overstates what the method actually does.** The SCM in Eq. (2) (X = f(C,S), C ⟂ S, Y = g(C)) is assumed from domain knowledge about fragmentation chemistry, not learned or tested. The core procedure is: use the ground-truth label to compute a theoretical spectrum; classify peaks as causal/non-causal by proximity to theoretical peaks (Eq. 4); replace some non-causal peaks; and train for representation invariance. This is a well-engineered robust training procedure using label-informed data augmentation and contrastive learning. Characterizing it as "causal representation learning" or "causality-informed" stretches the term past its typical meaning. The empirical contribution stands on its own and would be better served by more measured framing.

- **Hyperparameters α (fraction of non-causal peaks replaced) and γ (m/z tolerance threshold for peak classification) are mentioned in Section 3.4.1 but never given numerical values.** These control the data augmentation strength and directly affect the method's behavior. The code is available, but these should be stated in the paper for reproducibility.

- **The RI ("Relative Improvement") metric in Table 6 is not clearly defined.** For example, at threshold=8, AA precision improves from 0.711 to 0.744 (a 4.6% relative increase), yet RI is reported as 1.3%. The values do not match a standard relative improvement formula, and the paper never states the formula used for this table. The definition provided in the vulnerability analysis section (Figure 3 context) appears to measure something different (reduction in performance degradation).

- **The training intervention adds all theoretical peaks to the intervened spectrum** (Section 3.4.1: x_intervene = x_replace ∪ x_theory). This means the contrastive objective aligns representations of natural spectra with a partially denoised version that is guaranteed to contain every signal peak. This is a legitimate and effective training strategy, but it should be discussed more transparently as such rather than framed as a strict causal intervention.

### Trivial
None.

## Nice-to-Haves
- Comparing CausalNovo against simpler augmentation baselines (e.g., random peak masking, mixup-style augmentation, or standard dropout) would help disentangle gains attributable to the causality-informed design from those arising from contrastive learning / data augmentation more broadly.
- Reporting the deployed γ and α values in the experimental setup section.

## Removed Points
These points are flagged to be removed — treat them with caution:
- **"The method uses the label to identify which peaks to perturb, creating a circular dependency"** (reviewer Issue 3): This is standard supervised learning, not a circular dependency. The paper correctly notes the strategy is well-established in database search and prior deep learning work. The reviewer acknowledges it is "not a fatal flaw."
- **"Retrained baselines differ substantially from published numbers"** (reviewer Issue 5): The paper transparently reports both published and retrained (†) results in Table 1. CausalNovo is compared against the retrained baselines under identical conditions, which is the correct experimental practice. The fact that CasaNovo retrained to a *higher* number (0.741 vs. 0.697) makes the baseline stronger, not weaker, and is favorable to the paper's claims.
- **Formatting nitpicks and speculation about missing appendix content** — these are parser artifacts.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Add variance estimates** — run the main experiments (at least Tables 1–2) with 3–5 random seeds and report mean ± std. This would directly address the most significant evidential weakness.
2. **Tone down the causal framing** — the method is best described as signal-informed robust training via contrastive learning. The SCM framework provides a useful conceptual scaffold but the paper would be stronger if it were more measured about what is assumed vs. discovered.
3. **Specify α and γ values** in the experimental setup section.
4. **Clarify the RI formula** used in Table 6 or replace it with a standard relative improvement metric.

## Score and Decision
The paper makes a genuine empirical contribution with consistently demonstrated improvements across a comprehensive evaluation. The main evidential weakness — absence of variance estimates — is significant but addressable and does not undermine the overall pattern of results. The framing overclaim is common and does not invalidate the technical contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>