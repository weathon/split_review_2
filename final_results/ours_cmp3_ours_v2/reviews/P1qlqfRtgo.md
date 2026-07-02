Now I have a clear calibration picture. Let me produce the final review.

**Bracket assessment:** Based on the calibration search, the most topically similar papers are EPINN (avg 2.50, rejected), Atmospheric Radiation Parameterization (avg 3.00, rejected), Res-F-FNO (avg 3.00, rejected), Hottel Zone Physics-Constrained Networks (avg 4.50, rejected), Open-CK (avg 6.25, accepted), and KinFormer (avg 6.00, accepted). The current paper has a well-motivated problem and reasonable data pipeline, but suffers from an architecture mislabeling that undermines its interpretive claims, a species inconsistency in figure captions, and an ambiguous DeepONet implementation. Its contribution is considerably narrower than accepted papers like Open-CK or KinFormer, but it is more coherent than the lowest-scoring papers (EPINN at 2.50). The plausible range is 3.0–4.0.

## Summary

This paper investigates how neural network architecture affects the accuracy of data-driven surrogates for thermal explosion dynamics in a hydrogen–oxygen–air mixture. It compares three architectures—a plain MLP, a U-Net-style residual network, and a DeepONet-style model—on a generated dataset of chemical kinetic trajectories. The residual network achieves substantially lower MSE (0.00137) than MLP (0.0203) and DeepONet (0.0181), leading the authors to conclude that architectural design choices (particularly the U-Net's encoder-decoder structure and multi-scale representation) significantly improve surrogate accuracy for stiff chemical kinetics.

## Strengths

- **Well-motivated problem (Sections 1–2).** The paper correctly identifies the stiff ODE bottleneck in computational combustion and explains why architectural choices matter for multi-scale reactive dynamics. The problem framing is clear and practically relevant to the combustion community.
- **Careful data generation pipeline (Section 3).** The dataset covers practically relevant ranges (T ∈ [250, 5000] K, p ∈ [10⁴, 2×10⁷] Pa, Δt ∈ [10⁻¹⁰, 10⁻⁵] s) using a stiff ODE solver, intentionally covering extreme regimes (slow induction, abrupt ignition, equilibrium). This is a reasonable and well-described simulation setup.
- **Multi-step training loss (Section 4.4, Eq. 4).** The loss function uses a decaying weighted sum over 30 recursive prediction steps, encouraging stability across rollouts rather than optimizing only the one-step-ahead error. This is a sensible design choice for surrogate modeling of stiff systems.

## Weaknesses

### Fatal

None. The empirical comparison is valid as executed; the problems lie in interpretation and presentation.

### Major

- **Architecture mislabeling leads to unsupported interpretive claims (Section 4.2 vs. Section 5).** The network labeled "U-Net-style" (Section 4.2) is a feedforward MLP with two residual skip connections: a local skip adding the expansion-layer output to the block output, and a global skip adding the original input to the final output. There are no convolutional layers, no down/up-sampling operations, and no multi-resolution hierarchy—the defining features of a U-Net (Ronneberger et al., 2015). Yet Section 5 attributes its performance to "encoder-decoder design," "hierarchical feature extraction," and "multi-scale representation" (lines 157, 180)—properties this architecture does not possess. The reported performance advantage over the plain MLP can be explained by residual connections (a result known since ResNet, 2015), not by any U-Net-specific mechanism. This gap between the paper's narrative and the actual design is the paper's central interpretive weakness.

- **DeepONet implementation is ambiguously described and non-standard (Section 4.3, Figure 2).** The main text (line 121) says a "matrix product" of branch (12×10) and trunk (32×10) outputs yields a "12-component fused vector," while the Figure 2 caption says "element-wise product." These are dimensionally incompatible operations without specifying transposes or reshapes, and they describe different merging schemes. Additionally, the branch network takes 12 scalar state variables rather than an input function evaluated at sensor points, deviating from the standard DeepONet paradigm (Lu et al., 2021). This makes it difficult to interpret the three-way comparison: is the DeepONet's poorer performance a limitation of operator learning, or just a poorly configured instance?

### Minor

- **Limited architectural insight from the comparison.** The three architectures differ in multiple confounded ways (parameter count, presence of skip connections, architectural paradigm compliance). Without ablations (e.g., removing the local or global skip, matching parameter counts, or comparing against a proper DeepONet implementation), the paper offers little insight beyond "residual connections help," which is already well-established. The paper's own statement that "the problem remains unresolved" (Abstract) signals the limited actionable takeaway.
- **Species inconsistency in figure captions (Figures 3, 4 vs. Section 2).** The reaction mechanism (Section 2) explicitly lists 9 hydrogen-oxygen compounds plus N₂ and Ar—no carbon- or nitrogen-oxide species. Yet Figures 3 and 4 captions list CO and NO among the plotted quantities. This inconsistency (which may be a PDF-parsing artifact rather than an author error) needs clarification: were the figures generated from the described mechanism or a different one?
- **Error reported only in normalized coordinates (Section 5, Table 1).** The MSE is dimensionless in normalized space. A combustion engineer cannot assess whether MSE = 0.00137 translates to acceptable error in physical units (e.g., temperature error in Kelvin or species concentration in mol/m³). Reporting physically interpretable error metrics would substantially strengthen the paper's practical contribution.
- **Dataset structure is underspecified (Section 3).** The paper states "50,000 training, 15,000 validation, 5,000 test samples" without clarifying whether these are individual time steps or full trajectories. If they are individual steps sampled from a smaller number of trajectories, the effective sample independence is much lower than the raw count suggests.

### Trivial

None.

## Nice-to-Haves

- Ablation study isolating the contribution of each skip connection (local vs. global) in the U-Net-like network.
- Reporting parameter counts and training time for each architecture to assess whether the U-Net's advantage reflects capacity rather than design.
- Comparison against a standard DeepONet implementation following the original paradigm, with matched parameter counts.
- Specifying the equivalence ratio or mixture composition for the dataset.

## Removed Points

The following points from the input review were removed or downgraded during filtering, with brief justification:

- **"Modest contribution / shallow for ICLR"** as a standalone weakness — This is a judgment about venue fit, not a specific verifiable problem. Reframed as a Minor weakness about limited architectural insight, which is concrete and verifiable.
- **"STD > 10× mean MSE indicates skewed distribution"** — Removed. Many ML error distributions on multi-trajectory test sets are skewed; this is an observation, not a flaw. The paper acknowledges the high-variance trajectories.
- **"Practical utility unclear due to high error variance"** — Removed. The paper is transparent about the problem remaining unresolved; this is accurate characterization, not a weakness.
- **"Missing equivalence ratio / mixture composition"** — Demoted to Nice-to-Have. A relevant detail, but its absence does not invalidate the comparison.
- **"Parameter count and training budget"** — Demoted to Nice-to-Have.
- **"Figure caption spatial arrangement"** — Removed as a formatting nitpick.
- **Various concerns about the abstract framing it as a negative result** — Removed. The abstract honestly states the finding; this is not a weakness.
- **"Missing comparisons in related work"** — Removed per filtering rules (cannot confirm existence of unmentioned works without external sources).

## Novel Insights

None beyond the paper's own contributions. The core observation from the input review—that the "U-Net" is actually a residual MLP and the paper's interpretive claims about multi-scale processing are unsupported—is valuable but identifies a gap in the paper's reasoning rather than offering a positive insight.

## Suggestions

1. **Rename the architecture.** Replace "U-Net-style" with "residual MLP" throughout the paper, and remove all claims about encoder-decoder design, hierarchical feature extraction, and multi-scale representation. The architecture's actual mechanism—skip connections improving gradient flow—is well understood and does not need a misattributed justification.
2. **Resolve the DeepONet ambiguity.** Specify the exact operation used to combine branch and trunk outputs (including dimensional details), and justify any deviations from the standard DeepONet paradigm. If the goal is to compare operator learning against other architectures, use a standard reference implementation.
3. **Clarify the CO/NO issue.** Either correct the figure captions to match the 11-species mechanism described in Section 2, or confirm which mechanism was actually used and update the text accordingly.
4. **Report errors in physical units.** Add a column to Table 1 reporting temperature error in K and species concentration error in mol/m³, so the combustion community can assess practical significance.
5. **Specify dataset structure.** Clarify whether the 70,000 samples are individual time steps or full trajectories, and report how many independent trajectories were simulated.

## Score and Decision

The paper addresses a genuine problem with a reasonable data pipeline, but the architecture mislabeling undermines its central interpretive claims, the DeepONet comparison is too ambiguous to interpret, and the overall contribution (residual connections improve accuracy on one combustion dataset) is modest. While the empirical results are likely valid, the paper does not meet the bar for a top-tier venue in its current form.

Calibration anchors used (all rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| SYiOxXWlKU (EPINN, stiff ODEs) | 2.50 | R1 | Weaker paper; proposed method with minimal experiments. Current paper is more coherent. |
| otXB6odSG8 (Atm. Radiation Neural ODE) | 3.00 | R1 | Similar domain (physical surrogate), rejected. Comparable quality. |
| yGdoTL9g18 (Res-F-FNO, turbulence) | 3.00 | R1 | Similar contribution level (residual connections help). Rejected. |
| hz3NtNpDNv (Hottel Zone furnaces) | 4.50 | R2 | Similar application domain; current paper has clearer experiments but more serious interpretive problems. |
| YNQF003Ad3 (FIGConv, CFD) | 4.00 | R2 | Stronger methodology; accepted contribution level. Current paper is weaker. |
| A23C57icJt (Open-CK, combustion benchmark) | 6.25 | R1 | Much larger scope and stronger contribution. Accepted. |
| nhrXqy5d5q (KinFormer, reaction kinetics) | 6.00 | R1 | More sophisticated methodology. Accepted. |

Round 1 bracket: 3.0–4.0. Final score anchored at 3.5 based on comparison with EPINN (2.50, clearly weaker) and Hottel Zone (4.50, similar quality but with a clear proposed method vs. the current paper's interpretive issues).

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>