## Summary

CausalNovo proposes a model-agnostic framework for de novo peptide sequencing that learns representations focused on causal signal ions rather than noise peaks. It introduces a Causality Extraction Module (CEM) with an information-theoretic objective—using causal interventions (noise peak replacement) plus contrastive learning for invariance and cross-entropy loss for sufficiency—that can be inserted into existing encoder-decoder sequencing models. Experiments across three public datasets and three baselines show consistent improvements of up to 10%+ in amino acid, peptide, and PTM-level metrics.

## Strengths

- **Empirically grounded motivation.** Figure 1 directly demonstrates that replacing noise peaks degrades precision of three existing models, with degradation worsening as m/z tolerance tightens. This concrete evidence that the problem is real is a strength most papers in this area lack.
- **Broad and consistent improvements.** Tables 1 and 2 show CausalNovo improves every baseline on nearly every metric across three datasets. Gains are large in several cases (e.g., CasaNovo + CausalNovo improves amino acid precision from 0.357→0.477 on Seven-species, a +12.0% absolute gain). The pattern is not cherry-picked.
- **Model-agnostic modular design.** The CEM module adds a learned gating mechanism inserted into an existing encoder-decoder pipeline. The core contribution does not require redesigning the underlying sequencing model, increasing practical value.
- **Attention analysis provides mechanistic insight.** Table 7 shows the proportion of predictions attending to three causal peaks among the top three attended positions increases from 19.26% (baseline) to 32.87% (CausalNovo), and the proportion attending to zero causal peaks drops from 12.73% to 10.76%. This intermediate evidence explains why improvements occur.
- **Honest disclosure of limitations.** The paper acknowledges the ~2.3× training cost and notes the evaluation follows the NovoBench protocol rather than the more realistic large-scale cross-corpus protocol, showing transparency.

## Weaknesses

### Fatal
None.

### Major
- **No variance or statistical significance reported for any result.** Every table and figure reports point estimates without error bars, standard deviations, or confidence intervals. Several improvements are modest in absolute terms (e.g., +2.2% for π-HelixNovo on Nine-species in Table 1), the ablation study (Table 4) shows incremental gains of +0.4% to +1.2% per component, and retrained baselines differ substantially from published values (CasaNovo published AA precision 0.697 vs. retrained 0.741, a +6.3% discrepancy). Without variance estimates, the reader cannot assess whether the smaller improvements and ablation increments are reliable or within run-to-run noise. This does not invalidate the large improvements (e.g., +12% on Seven-species), but it weakens the evidentiary basis for the modest-range claims. Note that this weakness is shared with some accepted papers in this sub-field (e.g., ReNovo at ICLR 2025 also had missing variance noted by a reviewer) and does not by itself negate the contribution, but it is the single most impactful issue to address.

### Minor
- **"Causal" framing is overdrawn relative to the technical implementation.** The SCM (C⟂S, X=f(C,S), Y=g(C)) is operationalized via contrastive learning (Eq. 5) and cross-entropy loss (Eq. 6)—both standard representation learning objectives that can be motivated without a causal framework. The method is better described as "robust representation learning via targeted noise perturbation and contrastive invariance" than as "causality-informed." The empirical results stand regardless, but the framing oversells the depth of the causal contribution.
- **Missing hyperparameters α and γ.** The fraction of noise peaks replaced (α, line 111) and the m/z tolerance threshold (γ, Eq. 4) are introduced but never specified numerically in Section 4.2 (Implementation Details). The vulnerability analysis uses thresholds 16, 12, 8, 4, 2 (Figure 1), but the training-time values are not stated. These control which peaks are treated as causal vs. non-causal and the strength of the intervention, so their omission creates a reproducibility gap.
- **Noise-peak identification procedure creates a partial circularity in the vulnerability analysis.** The same procedure (Eq. 4) is used to define noise peaks for both the vulnerability diagnosis (Figure 1) and the training intervention. This means the method is trained to be invariant to perturbations of peaks identified the same way the evaluation perturbs them. This does **not** affect the main results (Tables 1–3 are on clean, unperturbed data) or the cross-species validation (Table 3), but it weakens the independence of the vulnerability evaluation as evidence of robustness to general noise beyond the specific instrumentation whose noise characteristics match the theoretical fragment model.
- **Purification objective justification is incomplete.** The paper claims that maximizing I(z_s; Y) "can indirectly lead to the purification of z_c" (line 97) without a theoretical argument or empirical evidence. Maximizing I(z_s; Y) could also incentivize the model to move predictive information into z_s rather than concentrate it in z_c. The reasoning is asserted rather than demonstrated.

### Trivial
None.

## Nice-to-Haves
- Reporting results across multiple random seeds (3–5) with means and standard deviations would substantially strengthen the empirical case, particularly for ablation results where improvements are small.
- Specifying α and γ numerically and, if sensitive, providing an ablation over their values.
- Demonstrating the method under the more realistic large-scale cross-corpus evaluation protocol (e.g., training on MassIVE-KB, testing on out-of-distribution data) would address the deepest uncertainty about generalization.

## Removed Points
These points are flagged to be removed; treat them with caution:
- **" -10" threshold in Figure 3 caption**: Parser artifact—the original submission does not have this issue. Removed per formatting-artifact rule.
- **Tables 4 and 5 checkmarks in every column**: Parser artifact—the ablation checkmarks were rendered identically despite representing different ablation conditions (the text clearly describes which components are ablated). Removed per formatting-artifact rule.
- **"Peak Distinguish Strategies" title misleading**: The title accurately reflects the content (analyzing how peaks are distinguished with 3 vs. 18 ion types). Removed.
- **Cross-species honeybee improvement smaller**: Observing that one species had +2.0% vs. +3.7% for another is a factual observation but not a weakness. Removed.
- **SCM figure node naming inconsistency**: The caption "S (spectrum augmentation)" is consistent with S being non-causal factors upon which the intervention operates. Removed as misunderstanding.
- **NSR distribution not stated**: Vague and speculative. Removed.

## Novel Insights
The reviewer's observation that the purification objective (maximizing I(z_s; Y)) has an unclear justification that could potentially encourage the opposite of the intended effect is a genuine gap that was not identified in the paper's own discussion of limitations.

## Suggestions
- Add variance information: report results across 3–5 random seeds with means and standard deviations for all main tables and ablation studies.
- Specify α and γ in the Implementation Details section; if using standard values from prior work, cite them explicitly.
- Provide a theoretical or empirical justification for why maximizing I(z_s; Y) purifies z_c rather than distributing predictive information across both representations.
- Consider evaluating under the more realistic large-scale cross-corpus protocol (training on a large external corpus like MassIVE-KB, testing on out-of-distribution data) to strengthen generalization claims.

---

## Calibration Analysis

**Round 1 bracket: 4.5–6.5**

### Anchors retrieved (all rounds)

| Path | Avg Score | Round | Comparison to this paper |
|---|---|---|---|
| ReNovo (uQnvYP7yX9) | 6.50 | Round 2 | Directly comparable de novo sequencing paper, accepted despite same "no variance" weakness; CausalNovo has broader baseline coverage but less novel methodology |
| MADGEN (78tc3EiUrN) | 6.00 | Round 2 | MS-based molecular generation, accepted; CausalNovo has stronger empirical breadth |
| Causal Rep Learning Multimodal Bio (hjROBHstZ3) | 5.80 | Round 2 | Theory-heavy causal rep learning for biology, accepted; CausalNovo has weaker theoretical grounding but stronger empirical evaluation |
| On the Identifiability... (7oT1X8xjIk) | 5.80 | Narrowing | Causal identifiability theory paper, rejected; not directly comparable |
| Fine-Tuning PLMs Robust Causal (tlH4vDii0E) | 5.60 | Narrowing | Causal representation learning with similar "framing vs. implementation" gap, rejected |
| Turning Challenges... (q07DDpu8Xb) | 5.25 | Narrowing | Causal identifiability theory, rejected; not directly comparable |
| Causal Graph Learning (Lxst78Rrwj) | 5.00 | Narrowing | Causal graph discovery method, rejected |
| RNA Contrastive Learning (wRkfniZIBl) | 4.33 | Round 1 | Contrastive learning for bio data, rejected; CausalNovo has more comprehensive evaluation |
| Causal Differential Networks (cbFqqtJGtA) | 4.25 | Round 1 | Causal approach to perturbation biology, rejected; comparable framing issues |

**Narrowing**: Comparing most strongly to ReNovo (6.50, Accept) and MADGEN (6.00, Accept)—both in the same application domain—CausalNovo sits slightly below ReNovo (less novel core idea) and around the same level as MADGEN (broader evaluation but more framing concerns). The missing variance weakness is shared with ReNovo, suggesting the community finds this issue addressable rather than fatal. Score rounded to 6.0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>