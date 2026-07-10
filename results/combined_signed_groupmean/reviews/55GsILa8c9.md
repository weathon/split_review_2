Now I have all the information needed. Let me write the final consolidated review.

## Summary

CausalNovo introduces a causality-inspired, model-agnostic framework for *de novo* peptide sequencing. It formulates peptide sequencing via a Structural Causal Model (SCM), deriving two principles (independence and sufficiency), and operationalizes them through a Causality Extraction Module (CEM) with information-theoretic objectives to disentangle causal representations from spurious noise peaks. The method uses theoretical spectra (known b, y, a fragment ions) to label causal vs. non-causal peaks and enforces representation invariance under interventions on non-causal peaks. Experiments across three datasets and three baseline models (CasaNovo, AdaNovo, π-HelixNovo) show consistent improvements of up to 10% at amino acid, peptide, and PTM levels.

## Strengths

- **Clean SCM framing.** The Structural Causal Model in Section 3.2 (Figure 2A, Equations 2) is concise and principled. The two derived properties — independence (C ⟂ S) and sufficiency (Y = g(C)) — follow directly from the model and provide a clear, testable specification for what the learned representation should satisfy. (Draft impact: **+9.97**)

- **Comprehensive and consistent experimental results.** Tables 1–3 show that CausalNovo improves all three baselines across three datasets at amino acid, peptide, and PTM levels with no cherry-picked metrics. The cross-species validation (Table 3) and NSR analysis (Figure 4) demonstrate generalization beyond the standard test split. (Draft impact: **+10.00**)

- **Model-agnostic design.** CausalNovo is applied to three different Transformer-based models (CasaNovo, AdaNovo, π-HelixNovo) and improves all of them. The integration is lightweight (a CEM module and additional loss terms) and does not require modifying the base architecture. (Draft impact: **+9.72**)

- **Well-structured ablation studies.** Tables 4 and 5 isolate each component's contribution, showing that the independence principle, purification objective, and symmetric training each provide measurable gains. The causal intervention ablations (replace vs. enhance vs. drop) are informative. (Draft impact: **+9.73**)

- **Empirically motivated problem.** The vulnerability analysis (Figure 1) clearly demonstrates that three established models degrade when noise peaks are perturbed, and that tightening the m/z tolerance threshold amplifies the degradation. This grounds the paper's motivation in actual observed behavior rather than hypothetical concerns. (Draft impact: **+1.27**)

## Weaknesses

### Fatal

None.

### Major

- **The purification objective (maximizing I(z_s; Y)) is insufficiently explained.** The paper's stated rationale (Section 3.3, line 97) — that maximizing mutual information between the *non-causal* representation z_s and the label Y "can indirectly lead to the purification of z_c" — lacks a clear formal mechanism. If z_s is designed to capture noise and spurious correlations, encouraging it to also predict Y appears to work against the disentanglement goal. The paper references Chen et al. (2022) but does not explain how this specific objective aligns with the causal framing. The ablation (Table 4) shows it helps empirically (+0.8% precision), which suggests it is doing something useful, but the paper does not articulate what that something is in a way that is consistent with the stated causal principles. The authors should either provide a clear explanation of the mechanism, or replace it with a more principled alternative (e.g., a disentanglement or independence penalty between z_c and z_s). (Draft impact: **-4.79**)

- **The evaluation protocol does not fully match the causal robustness claims.** The paper frames its core motivation around OOD generalization (noise peaks that change due to different co-elutions or contaminants), yet the main evaluation (Tables 1–2) follows the standard NovoBench protocol with in-distribution train/test splits. The cross-species validation (Table 3) provides partial OOD evidence but is still within the same set of nine species. The paper honestly acknowledges this limitation (Section 5, lines 296–299), which is commendable, but this does narrow the scope of the claims relative to the abstract and introduction. Testing under true distribution shift (e.g., different instrument types, lab protocols) would more directly support the claim that the framework confers genuine robustness to distribution shift. (Draft impact: **-0.97**)

### Minor

- **The causal framing somewhat overstates what the method does mechanistically.** The method identifies "causal" peaks by computing a theoretical spectrum from the ground-truth peptide sequence (using known b, y, and a ion types) and labeling peaks within a tolerance threshold γ as signal. This is using well-established physical domain knowledge about peptide fragmentation, not discovering causal mechanisms from data. The SCM describes the true data-generating process, but the method does not learn this SCM — it uses known physics to supervise the representation. The contribution is better described as a principled way to incorporate domain knowledge (theoretical fragmentation patterns) into deep learning with causal-inspired invariance objectives. This is still a solid contribution, but the framing should be calibrated accordingly. (Draft impact: **-0.56**)

- **The default tolerance threshold γ used in the main experiments is not clearly stated.** Table 6 varies γ from 1 to 8 and shows that CausalNovo's relative improvement increases as γ tightens (from 1.3% at γ=8 to 8.4% at γ=1 on Nine-species). However, the paper does not explicitly report which γ value produces the results in Tables 1–3. This makes it harder to assess how sensitive the main results are to this hyperparameter choice. (Draft impact: **-0.00**)

- **Discrepancy between originally reported and retrained CasaNovo performance.** The originally reported CasaNovo achieves 0.697 precision on Nine-species, while the retrained version (†CasaNovo) achieves 0.741 — a 4.4% absolute difference that is larger than typical variance from random seeds. The paper correctly uses retrained baselines for fair comparison, but this gap warrants an explanation (e.g., differences in training configuration, data preprocessing, or hyperparameters). (Draft impact: **-0.02**)

- **Anomalously low InstaNovo results.** InstaNovo achieves only 0.420 precision on Nine-species in Table 1, far below what the original paper reports. The paper uses numbers "provided by NovoBench," but this raises questions about whether evaluation configurations (beam size, max peaks, etc.) are consistent across all methods compared. (Draft impact: **-0.15**)

### Trivial

None.

## Nice-to-Haves

1. Clarify the mechanism of the purification objective, either with a formal argument or by replacing it with a more principled alternative (e.g., a variational information bottleneck or a disentanglement penalty).
2. Add an OOD evaluation (e.g., training on Nine-species and testing on data from a different instrument or lab) to directly support the causal robustness claims.
3. Explicitly state the default γ value used and discuss sensitivity to this choice.

## Removed Points

1. **SCM figure inconsistency (C=charge state vs. C=causal factors):** The figure caption labels C as "charge state" and S as "spectrum augmentation" — these are concrete examples of the abstract causal factors and non-causal factors described in the text. The text correctly uses the abstract framing. This is not an inconsistency, just a difference in level of description. **REMOVED: not a real issue.**

2. **Missing wall-clock training time:** The paper reports 2.3x training overhead on an RTX 4090 GPU. Specific wall-clock time is a minor implementation detail. **REMOVED: trivial.**

3. **Missing related work discussion:** Per instructions, I cannot verify the existence of missing citations and should not mention them. **REMOVED.**

4. **Formatting/typo nitpicks:** These are parser artifacts, not author errors. **REMOVED.**

## Novel Insights

None beyond the paper's own contributions. The review does not surface any pattern or connection that the paper itself does not already present.

## Suggestions

1. Rewrite the explanation of the purification objective (Section 3.3) to provide a clear formal mechanism for why maximizing I(z_s; Y) purifies z_c, or replace it with a more standard disentanglement objective.
2. Explicitly state the default γ value used and discuss the method's sensitivity to this hyperparameter.
3. Explain the large gap between originally reported CasaNovo performance and the retrained version.
4. Conduct at least one OOD generalization experiment to directly support the causal robustness claims.

## Score and Decision

**Calibration summary.**

All anchors retrieved:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| uQnvYP7yX9.md (ReNovo) | 6.50 | R1+R2 | Yes | Same domain (de novo peptide sequencing); had far more impactful weaknesses (-9.99 each for missing related work/comparisons) but scored 6.50. My paper shares similar strong experiments but has less severe weaknesses. |
| I2ZYngkRW6.md (CrossNovo) | 4.25 | R1 | Yes | Same domain; rejected for lacking methodological novelty. My paper's clear SCM framing distinguishes it sharply. |
| 8GhwePP7vA.md (FMI) | 4.25 | R1 | Yes | Causal representation learning; rejected for strong assumptions. My paper's assumptions are grounded in established domain knowledge. |
| 78tc3EiUrN.md (MADGEN) | 6.00 | R2 | Yes | MS-based molecular generation; Accept. Comparable quality but different task. |
| pudmhZdV78.md (ICL spurious) | 5.25 | R1 | Yes | Spurious correlations; Reject. Different domain. |
| jqmptcSNVG.md (PepHAR) | 6.20 | R2 | No | Peptide design; Accept. Different task. |
| 1iuaxjssVp.md (InvMSAFold) | 7.25 | R2 | No | Protein sequence generation; different domain. |
| Q0s6kgrUMr.md (Causal/Anticausal) | 6.67 | R2 | No | Causal discovery; different domain. |

**Bracket analysis (Round 1):** The paper sits in the 5.5–7.5 band, with the best topical anchor ReNovo at 6.50. My paper's most impactful weakness (-4.79 for the purification objective) is far smaller than ReNovo's most impactful weaknesses (-9.99 each), while my top strengths (+9.97 to +10.00) match ReNovo's (+10.00). CrossNovo (4.25) was rejected for lacking methodological novelty — my paper has a clear SCM contribution.

**Narrowing (Round 2):** Compared against ReNovo (6.50), my paper has stronger methodological grounding (clean SCM vs. retrieval augmentation) and no -9.99-level weaknesses. This suggests a score at or slightly above 6.5. I conservatively calibrate to 6.5, considering that the purification objective (-4.79) is a meaningful methodological gap that the authors should address.

**Final score: 6.5 (borderline accept, leaning toward accept).**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>