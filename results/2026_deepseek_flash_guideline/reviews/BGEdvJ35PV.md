## Summary

This paper identifies that molecular data distributions exhibit a "dense-concentrated structure" (DC-structure) — narrow probability peaks separated by low-density regions — which makes diffusion model reverse inference fragile: small errors can overshoot valid molecular peaks and accumulate irrecoverably. The authors formalize this overshoot condition (Eq. 6-7) and propose DIST (Diffuse and Steer), a plug-in corrective sampling method that at an intermediate timestep evaluates trajectory batches via pilot inference, filters batches based on a score, and continues only for selected batches. DIST is applied to EDM, GeoLDM, and RADM backbones on QM9 and GEOM-Drugs, showing consistent improvements across all metrics while reducing inference timesteps to roughly half.

## Strengths

1. **Formal overshoot condition (Eq. 6–7)**: The paper derives a precise inequality — $\beta_t \frac{\Delta}{\sigma_*^2} > c\sigma_*$ — characterizing when a reverse diffusion step overshoots a valid molecular peak. This explicitly links peak width $\sigma_*$, inter-peak separation $\Delta$, and noise schedule $\beta_t$ to the drift failure mode, going beyond prior qualitative discussions (Choi et al., 2025). This is the paper's sharpest conceptual contribution.

2. **Universal improvement across diverse architectures (Table 2)**: DIST improves all three backbone models — GNN-based (EDM), latent-space (GeoLDM), and Transformer-based (RADM) — on both QM9 and GEOM-Drugs across every metric. For example, EDM molecule stability on QM9 jumps from 82.0% to 89.9%, and validity from 91.9% to 96.9%. The across-the-board improvement directly supports the model-agnostic claim.

3. **Simultaneous quality improvement and efficiency reduction (Tables 2 & 3)**: DIST reduces average inference timesteps to roughly half (e.g., EDM+DIST uses 556.1 vs. 1000 steps on QM9) while improving quality on all metrics, a distinctive result since most methods face a quality-efficiency trade-off.

4. **TV-contraction bound (Corollary 3.1)**: Proves that if the intermediate model distribution $q_t$ is closer to the true marginal $p_t$, the final distribution $q_0$ is also closer to $p_0$ via a contraction coefficient $\kappa \in [0,1]$, providing formal motivation for the corrective-sampling strategy.

5. **Ablation of pilot sample size (Table 4)**: Systematically varies pilot subset size from 30 to 100, showing monotonic quality improvement (molecule stability from 89.5% to 90.5%) while documenting the computational cost trade-off, providing specific evidence that the pilot evaluation mechanism drives improvements.

6. **Error propagation diagnostic (Table 1)**: Shows clean monotonic degradation in atom stability (99.0%→98.7%), molecule stability (95.2%→82.0%), and validity (97.7%→91.9%) as the starting timestep increases from 0 to 1000, supporting the error-accumulation motivation.

## Weaknesses

### Fatal
None.

### Major

1. **The pilot score $s_j$ is not concretely specified in the main text.** The paper states the score could be "round-trip residual, self-consistency, ensemble variance, or chemistry-based penalty" (line 150) — a list of qualitatively different possibilities — but never states which one (or what combination) was actually used in the experiments producing Tables 2–4. This is the central selection mechanism of DIST: it determines which batches are kept and which are discarded. Whether $s_j$ checks chemical validity rules (which would make improvement on validity metrics partly circular) or uses a metric-independent measure (a stronger result) is critical to interpreting the claimed improvements. Without this information, the nature of the contribution remains ambiguous. The examples given span such different approaches that the specific choice matters enormously.

2. **No comparison against a post-hoc rejection sampling baseline.** DIST filters batches at an intermediate timestep based on pilot evaluation. Without a baseline that generates $N$ molecules with the backbone model and then selects the top-$k$ using a similar scoring criterion, it is unclear whether DIST's improvement comes from its claimed "steering" mechanism (early mid-trajectory correction) or simply from discarding low-quality outputs identifiable after full generation. This experiment would isolate the value of intervening mid-trajectory versus post-hoc filtering.

### Minor

3. **The simplified efficiency formula is incomplete.** The main text presents the cost as $(T-t)/|B| + t$ (line 221), which does not account for pilot inference overhead on discarded batches. The empirical results in Tables 3–4 (e.g., average 556.1 steps vs. the simplified 307 for the example parameters) naturally include all real costs and honestly support the "nearly half" claim, but the simplified formula could mislead readers. The paper references Appendix G.1 for detailed quantification.

4. **Theory provides conceptual motivation but limited practical guidance.** Proposition 3.1's error bound depends on unknown quantities (true coverage $\alpha(\tau)$, true batch weights $\pi_j$, conditional TV distances), and Corollary 3.1 assumes an ideal reverse kernel with an uninstantiated contraction coefficient $\kappa$. The theory motivates the approach but does not constrain implementation choices (how to set $\tau$, choose batch size, or design $s_j$).

5. **Cross-method comparisons in Table 2 are from different sources.** Baseline numbers for non-DIST methods are "directly obtained from their original work" (line 205), potentially using different evaluation protocols. The within-row comparisons (backbone vs. backbone+DIST) are fair since they use the same official weights, but the "new state-of-the-art" claim and global-best underlining across different-source numbers should be interpreted with caution.

6. **Table 1's evidence for DC-structure fragility is suggestive but not conclusive.** The monotonic degradation as starting timestep increases could partly reflect the general property that any generative model performs better starting closer to the data distribution. A control experiment comparing molecules to images under the same schedule would more directly demonstrate that DC-structure causes *additional* fragility beyond this baseline effect.

7. **Diversity analysis is limited.** The paper relies on "validity $\times$ uniqueness" as a combined metric but does not directly analyze whether DIST reduces molecular diversity (e.g., number of distinct scaffolds, property value distributions) by preferentially filtering out unusual but valid structures.

### Trivial
- Batch construction details (radius $r$, perturbation noise magnitude, how batches $\{B_j\}$ are geometrically defined) are mentioned only at a high level in the main text.

## Nice-to-Haves
- An ablation of the threshold $\tau$ (or equivalent selectivity parameter) in the main paper rather than deferred to Appendix H.
- A brief discussion acknowledging the potential for reduced molecular diversity from selective filtering.

## Removed Points
- **"Efficiency claim is internally inconsistent" (strong framing)**: The harsh critic claimed Table 3 numbers "substantially undercount the true computational cost." However, the paper states these values are "computed from the total timestep consumption needed to generate 10,000 molecules" — the empirical results already account for all costs including pilots (the average 556.1 steps vs. simplified 307 confirms this). The criticism is retained in weakened form as Minor #3 (simplified formula presentation), not as a fundamental inconsistency.
- **Missing appendix content**: Complaints about hyperparameter details ($\tau$ ablation, $r$, perturbation intensity) being deferred to the appendix are removed per hard rules — the appendix exists in the original submission.
- **"Generic criticism about batch underspecification"**: Demoted to trivial.

## Novel Insights

The cross-reviews surface an important tension that the paper's own framing does not resolve: the central mechanism — batch-level pilot scoring — is described at a level of abstraction encompassing qualitatively different approaches (from round-trip consistency to chemistry-based penalties). This makes it impossible to distinguish between two interpretations. If $s_j$ is computed using the same chemical validity rules used in evaluation metrics, then DIST is effectively a learned rejection sampling scheme filtering mid-trajectory, which is practically useful but not conceptually novel as a form of "steering." If $s_j$ uses a metric-independent measure (e.g., ensemble variance or round-trip consistency), the contribution would be substantially stronger. The paper's uniformly positive empirical results suggest the method works, but the nature of the contribution remains ambiguous without this specification.

## Suggestions
1. **Specify $s_j$ precisely**: State exactly how the pilot score was computed in the experiments and whether it uses the same chemical validity rules as the evaluation metrics. If it does, acknowledge this and reframe the contribution accordingly.
2. **Add a rejection sampling baseline**: Generate $N$ molecules with the backbone, select the top-$k$ using the same scoring criterion, to isolate whether mid-trajectory intervention adds value over post-hoc filtering.
3. **Present a complete efficiency formula** in the main text that includes pilot overhead, or clarify that the simplified formula is a lower bound.
4. **Provide a diversity analysis**: Report scaffold diversity or property distribution analysis to show DIST does not simply discard rare valid structures.

---

## Calibration Anchors

All anchors retrieved during calibration (avg human score, round, comparison to paper under review):

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| DynamicsDiffusion (molecular dynamics) | 3.00 | R1 low | Weaker — narrower scope, less novel theory |
| Ligand Conformation Generation | 3.00 | R1 low | Weaker — different task, averaged scores |
| Reducing Atomic Clashes (GDM) | 3.75 | R1 mid-low | Weaker — single model/dataset, limited novelty |
| Molecule Relaxation (MoreRed) | 4.75 | R1 mid | Comparable — rejected with similar theory-practice gap |
| Unlocking Gradient Guidance (MolJO) | 4.75 | R1 mid | Comparable — rejected, underspecified method components |
| Correcting Flows (Marginal Matching) | 5.25 | R2 narrow | Comparable — rejected, similar inference-time correction with theory gap |
| SFW sampling (diffusion correction) | 4.00 | R2 narrow | Weaker — narrower application, lower scores |
| Navigating Design Space (EQGAT-diff) | 5.75 | R1 mid-high | Comparable — accepted, but architectural not inference-time contribution |
| Chemistry-Inspired Diffusion (ChemGuide) | 6.00 | R1 mid-high | Stronger — accepted, clearly specified method, but fewer backbones |
| DreamTime (3D optimization) | 5.75 | R2 narrow | Different domain but similar score range |

**Round 1 bracket**: [4.5, 5.5]. **Narrowing**: Comparing directly to Correcting Flows (5.25, rejected) which shares the "inference-time correction with theory gap" profile, and ChemGuide (6.00, accepted) which has a cleaner method specification, the paper falls between them. DIST has stronger empirical breadth than Correcting Flows but a larger specification gap than ChemGuide.

**Final score**: 5.0 — The paper offers genuine contributions (DC-structure formalization, overshoot condition, universal empirical improvements) but the underspecification of $s_j$ and missing rejection-sampling baseline are significant gaps that prevent full evaluation of the method's novelty.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>