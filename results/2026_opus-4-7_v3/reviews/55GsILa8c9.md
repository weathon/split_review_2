Now let me read the remaining sections to check architectural details about the decoder sharing and other specifics.Now I have enough context to draft the review. Let me submit the draft first, then proceed with calibration.Now proceeding to Round 1 calibration — bracketing.Let me read a few anchor papers to calibrate my score bracket.Now I have a clear picture for bracketing. Let me form my initial assessment:

**Round 1 Bracket: 5.5 to 7.0**

Reasoning:
- CausalNovo is far above the 1.0-3.0 papers (broken/fundamentally flawed work).
- It's stronger than the 5.25 "Distribution Shifts CRL" paper — CausalNovo has much stronger empirical execution.
- Comparable to the 6.0 "Causal Alignment" paper — both apply causal reasoning to domain-specific problems with solid empirical results but have framing/depth concerns.
- Below the 7.0 "Multi-View CRL" paper — that has genuine theoretical identifiability proofs; CausalNovo's causal contribution is more motivational than rigorous.

Now let me do a Round 2 narrowing search within this bracket.Let me read the most relevant anchor — ReNovo, which is in the same domain (de novo peptide sequencing):Now I have comprehensive calibration. Let me finalize my assessment.

**Round 1 Bracket: 5.5 – 7.0**

**Round 2 Narrowing to: 6.0 – 6.5**

Key comparisons:
- CausalNovo is clearly stronger than the rejected "Fine-Tuning PLMs for Robust CRL" (5.6) — broader evaluation, clearer method
- Comparable to "Learning Causal Alignment" (6.0) — similar causal-application framing, CausalNovo has broader evaluation
- Comparable to ReNovo (6.5) — same domain, but ReNovo introduces a more paradigmatically novel idea (RAG for peptides) while CausalNovo applies well-established techniques with causal framing
- Below SmartPretrain (6.75) — whose model-agnosticism is better demonstrated

Now let me write the final consolidated review.

---

## Summary
CausalNovo proposes a model-agnostic training framework for de novo peptide sequencing that improves robustness to spectral noise by disentangling causal from non-causal representations in latent space. It introduces a Causality Extraction Module (CEM) that uses contrastive learning (for "independence" from noise) and cross-entropy objectives (for "sufficiency" and "purification"), with noise-peak replacement as a simulated causal intervention. Evaluated across three baselines (CasaNovo, AdaNovo, π-HelixNovo), three datasets, and three metric levels, the framework yields consistent improvements of up to ~14% in amino acid precision.

## Strengths
- **Compelling empirical motivation (Figure 1).** The vulnerability experiment — systematically replacing noise peaks in trained models and observing performance degradation across three baselines at multiple tolerance thresholds — concretely demonstrates that existing models rely on spurious correlations with noise peaks. This is not hypothetical; it is quantified.

- **Exceptionally thorough evaluation matrix (Tables 1–3, Figures 1, 3, 4, Tables 6–7).** CausalNovo improves all three baselines across all three datasets at amino acid, peptide, and PTM levels. The cross-species leave-one-out validation (Table 3, +2.6% average peptide precision over 8 species) provides additional generalization evidence. PTM-level gains are particularly notable (e.g., +15.1% PTM precision on Seven-species with π-HelixNovo, Table 2).

- **Analyses directly test the paper's thesis.** The vulnerability analysis (Table 6) showing increasing relative improvement under tighter perturbation thresholds (1.3% → 8.4% RI as threshold tightens from 8 to 1), the NSR analysis (Figure 4) showing consistent gains across noise levels, and the attention analysis (Table 7) showing CausalNovo shifts top-3 attention from 19.26% to 32.87% causal peak focus — all provide concrete evidence that improvements stem from reduced noise reliance, not just better fitting.

- **Well-structured ablation (Tables 4, 5).** Each component (independence, purification, symmetric training, replace vs. enhance vs. drop) is isolated, showing incremental and complementary contributions.

## Weaknesses

### Fatal
None

### Major
- **Causal framing substantially overclaims relative to what is operationalized.** The SCM in Figure 2A is a simple four-variable graph (X, C, S, Y). The derived "independence" principle is implemented as standard contrastive learning (Eq. 5), and "sufficiency" as cross-entropy loss (Eq. 6) — both well-established techniques in invariant representation learning. The paper uses SCM, do-calculus, and Reichenbach's Common Cause Principle vocabulary that suggests deeper causal engagement than what is actually implemented. The paper itself partly self-qualifies with "causality-inspired" in Section 3.3, but the title "CausalNovo" and heavy causal formalism (Section 3.2) create a gap between narrative and substance. This is a framing concern rather than a structural flaw: the method is sound as a noise-robust training framework, but the causal depth is oversold.

### Minor
- **Theoretical spectrum injection introduces an uninvestigated train/inference gap.** Section 3.4.1 defines x_intervene = x_replace ∪ x_theory, where x_theory is computed from ground-truth labels and injected into the training view. At inference, no theoretical spectrum is available. The ablation (Table 5) shows the "enhance" step adds +0.6% AA precision, so the contribution is real but modest. However, the paper does not analyze whether the contrastive learning signal quality degrades at inference when this idealized view is absent, nor whether x_theory's limitation to b/y/a ions means other real signal-carrying ions (internal fragments, neutral losses) are treated as noise during intervention construction.

- **No variance or statistical significance reported.** All results appear to be single runs. On Nine-species, some improvements are as small as +0.4% (symmetric training component in Table 4), where run-to-run variance could be relevant. The consistent pattern across 3 baselines × 3 datasets × 3 metrics provides strong informal evidence of reliability, but formal error bars or confidence intervals are absent.

- **Decoder architecture for purification unclear.** Both L_CE(z_c, t, y) and L_CE(z_s, t, y) in Eq. 6 use ρ notation, but the paper never clarifies whether a shared or separate decoder is used. If shared, the decoder must simultaneously learn to predict from clean causal features and noisy non-causal features, creating a potential training tension. The total training loss with balancing coefficients is also never written out explicitly.

- **Model-agnosticism has limited evidence.** All three baselines (CasaNovo, AdaNovo, π-HelixNovo) are Transformer-based encoder-decoder architectures. The CEM requires per-peak latent representations from a Transformer encoder. Whether the framework extends to CNNs (PepNet) or GNNs (GraphNovo) remains untested.

### Trivial
None

## Nice-to-Haves
- Directly evaluate CEM importance scores M against ground-truth signal/noise peak labels at inference time, to provide the strongest evidence that causal disentanglement (not just augmentation-based noise tolerance) is occurring.
- Evaluate under more realistic out-of-distribution protocols (training on large-scale external corpora, testing on truly novel samples), as the authors themselves acknowledge in Section 5.
- Report results across multiple random seeds with standard deviations — modest additional compute for substantially increased confidence.
- Discuss computational cost in more detail beyond "approximately 2.3× training time" — GPU-hours, memory overhead, wall-clock comparisons.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"RCCP application is somewhat circular"** — The reviewer argues the SCM doesn't add insight beyond formalizing that noise is independent of peptide identity. While the formalism is simple, it provides a structured motivation for the two optimization objectives. The circularity is more about elegance than correctness, and does not undermine the method.

- **"Paper doesn't discuss semi-supervised/unsupervised extension"** — Scope creep. The paper targets supervised peptide sequencing, which is the standard setting in this field. Criticizing absence of semi-supervised extension is outside the paper's stated scope.

- **"Comparison with SearchNovo/InstaNovo uses originally reported numbers"** — The paper properly marks retrained baselines with (†) and uses NovoBench-provided numbers for other methods. This is standard practice in the field.

- **"Up to 10% improvements is borderline misleading"** — Verified against Tables 1-2: improvements on Seven-species and HC-PT reach +12.0%, +14.2% in AA precision. The "up to 10%" claim is if anything conservative, not misleading.

- **"Abstract framing invites reader to expect 10% as typical"** — The abstract says "up to 10%", which is standard phrasing and accurately reflects the results. Nine-species improvements are smaller (2-6%), but the claim is qualified with "up to."

## Novel Insights
The paper's most genuinely novel contribution is the systematic demonstration that existing de novo peptide sequencing models are vulnerable to noise peak perturbations (Figure 1), combined with a practical and effective framework to address this. The increasing relative improvement under tighter perturbation thresholds (Table 6) and across higher NSR values (Figure 4), together with the attention analysis (Table 7) showing measurably increased focus on causal peaks, form a convincing end-to-end narrative linking the method's mechanism to its empirical gains. While the individual techniques are not new, their composition and application to this domain problem is well-motivated and effective.

## Suggestions
- Reframe the causal narrative more honestly as "causality-motivated" throughout; acknowledge explicitly that the implementation uses standard invariant representation learning techniques, principled by a causal analysis rather than constituting rigorous causal inference.
- Write out the full combined training loss with balancing coefficients, and clarify whether the decoder ρ is shared between z_c and z_s pathways.
- Report error bars from at least 3 random seeds on primary metrics (AA precision, peptide precision) for the main benchmark.
- Design a controlled experiment to measure the train/inference gap from theoretical spectrum injection — e.g., compare CausalNovo trained with vs. without the enhance step, evaluating both on clean and noisy test spectra.
- Evaluate CEM importance scores M directly against ground-truth signal/noise labels at inference to verify causal disentanglement.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to CausalNovo |
|---|---|---|---|---|
| KL Divergence Optimization for GFlowNets | Uj0h13lVrR | 1.0 | R1 | Fundamentally flawed; CausalNovo far stronger |
| Neural Network News Impact Assessment | nSDOkm0SKo | 1.0 | R1 | Hypothetical scenario paper; CausalNovo far stronger |
| Chinese NLP for Humanoid Robots | gwZ90hFSL2 | 1.0 | R1 | Fundamentally unscientific; CausalNovo far stronger |
| IC-Light (scaling diffusion) | u1cQYxRI1H | 10.0 | R1 | Exceptional work; CausalNovo not at this level |
| Causal Structure Learning for Outcome Prediction | AvXrppAS2o | 3.0 | R1 | Weak assumptions, limited novelty; CausalNovo much stronger |
| Conditional Density Estimation (video) | mHkbi3XM58 | 3.25 | R1 | Polarizing reviews; CausalNovo has much stronger evaluation |
| Biological Motifs via Sufficient/Necessary | qi5dkmEE91 | 3.0 | R1 | Weaker empirical support; CausalNovo stronger |
| Matrix VAE for Variant Effect Prediction | yIRtu2FJvY | 3.0 | R1 | Limited evaluation; CausalNovo much broader |
| Distribution Shifts in CRL | q07DDpu8Xb | 5.25 | R1 | Theoretical CRL with restrictive assumptions; CausalNovo better executed empirically |
| Denoising Diffusion Causal Discovery | Z756zcjNcC | 4.5 | R1 | Mixed reviews; CausalNovo has more consistent evidence |
| Causal Framework for Image Quality | ctvVXwUlnw | 5.25 | R1 | Similar causal-application spirit; CausalNovo has broader evaluation |
| Learning Latent SCMs | 0sO2euxhUQ | 4.0 | R1 | Theoretical focus with weak experiments; CausalNovo much stronger empirically |
| Multi-View CRL (partial observability) | OGtnhKQJms | 7.0 | R1 | Genuine theoretical depth with identifiability proofs; CausalNovo doesn't match this theoretical contribution |
| OOD Generalization of SSL | 22ywev7zMt | 5.67 | R1 | More theoretically ambitious but messy execution; CausalNovo better executed |
| Causal Alignment for Disease Diagnosis | ozZG5FXuTV | 6.0 | R1 | Similar spirit (causal reasoning for domain problem); CausalNovo has broader evaluation |
| Counterfactual Concept Bottleneck Models | w7pMjyjsKN | 6.75 | R1 | Stronger conceptual novelty; similar empirical effort |
| Intervention Extrapolation | 3cuJwmPxXj | 8.0 | R1 | Strong theoretical + empirical; CausalNovo below |
| Cross-Entropy Inverts DGP | hrqNOxpItr | 8.0 | R1 | Strong identifiability theory; CausalNovo below |
| Selection meets Intervention | xByvdb3DCm | 8.0 | R1 | Deep theoretical contribution; CausalNovo below |
| Granger Causal Root Cause Analysis | k38Th3x4d9 | 8.0 | R1 | Strong method + evaluation; CausalNovo below |
| SmartPretrain (motion prediction) | Bmzv2Gch9v | 6.75 | R2 | Model-agnostic framework with broader architecture diversity; CausalNovo slightly below |
| Understanding Label Noise in Pre-training | TjhUtloBZU | 6.25 | R2 | Noise robustness with solid evaluation; comparable to CausalNovo |
| Contrastive Learning Synthetic Audio | XRtyVELwr6 | 6.25 | R2 | Contrastive learning with causal augmentation; comparable |
| Multi-View Representation Learning | fPYJVMBuEc | 6.0 | R2 | Contrastive multi-view framework; comparable |
| **ReNovo** (de novo peptide sequencing) | uQnvYP7yX9 | **6.5** | R2 | **Same domain — ReNovo introduces more paradigmatically novel idea (RAG) but CausalNovo has broader evaluation matrix** |
| MADGEN (de novo molecular generation) | 78tc3EiUrN | 6.0 | R2 | Similar domain spirit; comparable evaluation |
| PepHAR (peptide design) | jqmptcSNVG | 6.2 | R2 | Related bioinformatics; comparable |
| Deep Signature (molecular dynamics) | xayT1nn8Mg | 6.67 | R2 | Novel framework for dynamics; CausalNovo slightly below |
| Robust Causal/Anticausal Discovery | Q0s6kgrUMr | 6.67 | R2 | Causal discovery with noise injection; CausalNovo comparable |
| Nonlinear Representation Learning (general noise) | 7oT1X8xjIk | 5.8 | R2 | Theoretical CRL, rejected; CausalNovo stronger empirically |
| Fine-Tuning PLMs for Robust CRL | tlH4vDii0E | 5.6 | R2 | Similar causal framing overclaim, weaker experiments; CausalNovo clearly stronger |

### Scoring Rationale

**Round 1 bracket: 5.5 – 7.0.** CausalNovo is clearly above the 3.0–5.0 range (solid method, comprehensive evaluation) but below the 7.0+ range (lacks theoretical depth of identifiability/causal discovery papers).

**Round 2 narrowing: 6.0 – 6.5.** CausalNovo is most comparable to:
- ReNovo (6.5): same domain, but ReNovo has a more paradigmatically novel core idea; CausalNovo has broader evaluation
- Causal Alignment for Disease Diagnosis (6.0): similar "apply causal reasoning to domain problem" spirit
- Understanding Label Noise (6.25): similar noise robustness framework

CausalNovo's strengths (comprehensive evaluation, consistent improvements, well-designed analyses) push toward 6.5, but the causal overclaim (Major weakness) and use of well-established techniques rather than genuinely novel methodology pull it back toward 6.0. The missing variance reporting and train/inference gap from theoretical spectrum injection are additional concerns.

**Final score: 6.0.** This is a solid empirical contribution with a well-executed evaluation, but the methodological novelty is limited (standard invariant representation learning techniques with causal framing) and the presentation oversells the causal depth. The paper delivers consistent practical improvements that would benefit the proteomics community, placing it at the borderline accept level.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>