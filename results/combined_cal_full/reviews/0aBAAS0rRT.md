Now I have a good calibration picture. Let me write the final review.

## Summary

This paper proposes SigMap, a multimodal foundation model for wireless localization with two claimed innovations: (1) a cycle-adaptive masking strategy for self-supervised pre-training on CSI data that dynamically adjusts to signal periodicity, and (2) a "map-as-prompt" framework that encodes 3D building geometry via a GNN into soft prompts for parameter-efficient fine-tuning.

## Strengths

- **Well-motivated problem framing.** The paper correctly identifies two genuine limitations of existing self-supervised methods for wireless localization: generic masking that ignores CSI periodicity, and shallow integration of map geometry. The connection between multipath components and geometric constraints (Section 2.2) is grounded in actual propagation physics (Equation 1), which many wireless ML papers omit.

- **Architecturally sensible design.** The geographic prompt mechanism (Section 3.4) — encoding 3D building geometry via a GCN and injecting it as a prefix prompt to a frozen Transformer backbone — is clean and parameter-efficient by construction. Only the GNN, projection MLP, and task head are updated during fine-tuning.

- **Conceptually sound masking motivation.** The observation that fixed masking lets a model exploit periodic shortcuts in OFDM-based CSI (Section 3.3) is a legitimate concern for SSL on wireless signals. Designing a masking strategy that adapts to detected periodicity is a reasonable direction.

## Weaknesses

### Fatal
None.

### Major

1. **Undefined core component in results.** The paper attributes its main experimental advantage to an "NLoS-aware attention mechanism" introduced via Equation (11) in Section 4.2: "The key advantage stems from our NLoS-aware attention mechanism that explicitly models multi-path propagation." However, the variables $\mathbf{o}_s^{(i)}$, $\phi$, and $\mathbf{W}_{\text{NLoS}}$ are never defined, and the mechanism is not described anywhere in Section 3 (Methodology). The multi-BS attention mechanism from Section 3.5 (Equation 9) is a different component. Since the paper states this is the source of its performance gains, its absence from the methodology is a structural omission that prevents evaluation and reproducibility.

2. **Zero-shot claim contradicted by experimental design.** The abstract states "strong zero-shot generalization in unseen environments" and Contribution 3 claims "strong zero-shot generalization to unseen environments and base station configurations." Yet Section 4.5 explicitly fine-tunes task heads using "approximately 100 instances per scenario" and describes this as a "few-shot learning setup." No true zero-shot experiment (model applied to a new environment without any fine-tuning) is conducted. This is a direct misrepresentation of what was demonstrated.

3. **Evaluation on a single simulated dataset for main results.** All main results (Tables 1, 2) are evaluated on DeepMIMO O1\_3p5, a ray-tracing simulation, not real measured data. The generalization experiments (Section 4.5) add DeepMIMO O2 and WAIR-D Scenario-2 (also simulated) but compare against only one baseline (LWLM). The paper does not acknowledge this as a limitation or discuss how results might transfer to real over-the-air measurements with hardware impairments and noise. Claiming "state-of-the-art performance" against four baselines on one synthetic scenario is not well-supported.

4. **No uncertainty measures reported.** The paper states results are "averaged over 5 independent runs" (Section 4.1) but provides no standard deviations, confidence intervals, or individual run values anywhere. Without variance information, it is impossible to assess whether the reported improvements (e.g., 0.673 vs 0.789 MAE in Table 2) are meaningful.

5. **Factual error in reported numbers.** Section 4.5 states "SIGMAP reaches 1.026 m MAE on DeepMIMO O2 and **1.580 m** on WAIR-D Scenario-2," but the table directly above shows **1.880 m** for SIGMAP (w/ map) on WAIR-D. The 44.3% improvement over LWLM (3.375 m) is consistent with 1.880 m (3.375 × 0.557 ≈ 1.880), confirming the table is correct and the text is wrong. This concrete error undermines confidence in the reporting.

### Minor

6. **Masking ablation inconsistency unexplained.** In Table 3, "Strip-masking only" achieves RMSE of **0.972 m**, which is *better* than "Adaptive masking" at **1.099 m** RMSE. The paper claims adaptive masking yields "the best trade-off" but does not explain why a method intended to be superior performs worse on RMSE (which typically captures large-error tail behavior).

7. **Generalization comparison incomplete.** In Section 4.5, only LWLM (and the ablated SIGMAP w/o map) are compared on unseen scenarios. The other baselines (SWiT, CNN, OMP) from the main results are dropped without explanation. Without their generalization performance, the claim of superior cross-scenario adaptability is not fully contextualized.

8. **Wrong figure reference.** Section 4.4 states "Two-dimensional and three-dimensional map ablations are illustrated side-by-side in Figure 1," but Figure 1 (in Section 2.1) depicts wireless propagation paths, not 2D/3D map comparisons.

9. **Cycle-adaptive masking details underspecified.** The computation of $d_{\text{final}}$ (detected periodicity shift) from cross-correlation is not explained. It is unclear whether $d_{\text{final}}$ is computed per sample, per batch, or globally, and how cross-correlation operates over the tensor dimensions.

### Trivial
None.

## Nice-to-Haves
- Include at least one real-world measured CSI dataset or prominently acknowledge the limitation of purely simulated evaluation.
- Compare against baselines that also use map information (not just CSI-only methods) to better isolate the benefit of the geographic prompt approach.
- Quantify the computational cost of Delaunay triangulation for the geographic prompt, especially if the method targets real-time deployment.

## Removed Points
These points are flagged to be removed, treat them with caution:

- **Missing related work on periodic-signal SSL**: Removed per instructions — missing related works should not be mentioned.
- **Contribution 3 is "a property of the design, not a distinct contribution"**: This is a framing judgment, not a concrete weakness.
- **Prompt-based fine-tuning is well-known**: Generic observation that applies broadly; not a specific problem with this paper.
- **Hyperparameters relegated to appendix**: The parser strips appendices; content exists in the original submission.
- **Delaunay triangulation computational cost not discussed**: Nice-to-have, not a core flaw.
- **No baselines using map information**: The paper's key comparison (w/ map vs w/o map) already isolates the map contribution; other baselines also lack map info.
- **Single-vector prompt capacity concern**: Speculative without experimental evidence of a problem.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Describe the NLoS-aware attention mechanism in the Methodology (Section 3) with all variables defined, or remove it from the results if it is not part of the actual model.
2. Conduct a true zero-shot experiment (no fine-tuning at all) and report results, or adjust the claims in the abstract and conclusion to honestly describe the few-shot setup.
3. Report standard deviations from the 5 independent runs that were conducted.
4. Correct the numerical error (1.580 → 1.880) in Section 4.5.
5. Add the missing baselines (SWiT, CNN, OMP) to the generalization experiments.
6. Explain the RMSE discrepancy in the masking ablation (Table 3).

---

### Calibration Anchors

The following anchors were retrieved across calibration rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `9TClCDZXeh.md` | 7.00 | R1 | Yes | Differentiable wireless simulation with Geometric Algebra Transformer; much stronger evaluation (both synthetic and real data, new datasets, thorough baselines). Our paper is significantly below this. |
| `q3WzT2mrhB.md` | 4.00 | R1 | Yes | WiFi-based mesh regression; similar evaluation limitations (single setting, thin baselines). Our paper has stronger methodological novelty but similar evaluation weaknesses. |
| `29JDZxRgPZ.md` | 6.00 | R1 | Yes | EM-GANSim for wireless simulation; stronger experimental setup, GAN-based approach. Our paper is below this. |
| `7zJDTnogdG.md` | 3.33 | R1 | Yes | ECG foundation model; significant novelty concerns. Our paper has stronger claimed novelty but also shares some weaknesses (no confidence intervals, limited comparison). |
| `pQdei0Zb7a.md` | 4.67 | R2 | Yes | BiSSL for SSL pre-training; limited experimental scope but clean framework. Our paper's weighted weakness profile (strong negatives on evaluation scope, undefined component, claim misrepresentation) places it below this anchor. |
| `hPq9weqiwp.md` | 3.50 | R2 | No | Self-supervised visual pre-training; not wireless-related. |
| `MnE8iIBCfO.md` | 3.67 | R2 | No | Data brittleness estimation; not directly comparable. |
| `9GKMCecZ7c.md` | 3.40 | R2 | No | Robot policy from visual PTMs; not directly comparable. |

**Bracket from Round 1:** between 3.5 and 5.0 (below the wireless simulation paper at 7.00, comparable to or slightly above the WiFi mesh paper at 4.00 and ECG FM at 3.33, but above strong rejects at 1.0).

**Final score placement:** Compared to the closest anchor `q3WzT2mrhB.md` (4.00), our paper shares the weakness of limited evaluation scope. However, our paper has additional heavy-weight negatives that `q3WzT2mrhB.md` does not: (a) an undefined core component (the NLoS-aware attention mechanism), (b) a zero-shot claim directly contradicted by the experimental setup, and (c) a factual error in reported numbers. These push this paper *below* the WiFi mesh anchor despite stronger claimed novelty. The `pQdei0Zb7a.md` anchor (4.67) had a much cleaner weighted-item profile (fewer and weaker negative items). Given the accumulation of issues — especially the undefined key component and the claim misrepresentation — a score of **4.0** best reflects where this paper sits: borderline reject territory, with interesting ideas that are not yet supported by sufficient evidence.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>