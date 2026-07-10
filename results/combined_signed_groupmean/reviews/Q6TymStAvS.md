Let me write the final review now.

## Summary

This paper introduces ShadowFM, a non-autoregressive flow matching framework for learning distributions of classical shadows of quantum many-body states, conditioned on Hamiltonian parameters. The key insight is that Pauli-6 POVM shadows naturally live on the Bloch sphere (S²), and the paper develops two complementary geometric approaches: (1) Riemannian Flow Matching on S² (Spherical Flow) that respects the spherical geometry, and (2) Anisotropic Dirichlet Flow (AD Flow) that modifies the probability simplex path to push toward a target shadow outcome while pulling away from its antipodal (spin-flip) counterpart. Experiments on TFIM, Heisenberg (1D and 2D), and time-evolution tasks show consistently strong improvements over existing generative baselines.

## Strengths

- **Well-motivated geometric framing with convincing toy experiment (Figure 2).** The paper demonstrates that spin flips (antipodal moves on S²) cause substantially larger reconstruction errors than basis flips (rotations around the sphere), grounding the method in a concrete physical observation rather than importing geometry for its own sake (evidence: lines 87–105). The impact model scores this as the strongest strength (+10.00).

- **Consistently strong empirical results across diverse settings.** Across 6 tables (TFIM L=10/L=30, Heisenberg L=10/L=30, time evolution, 2D Heisenberg), both proposed methods outperform all baselines, often by large margins. For example on TFIM L=10 (Table 1), AD at 100k shadows achieves RMSE 0.021 vs. next-best StatisticalFM at 0.126 — roughly a 6× improvement. The gap exceeds what minor implementation differences would explain (+10.00).

- **Two distinct, principled approaches.** Rather than a single method, the paper develops both Riemannian Flow Matching on S² (Spherical Flow) and an anisotropic generalization of Dirichlet Flow (AD Flow), each grounded in a different aspect of the shadow geometry. The mathematical development in Section 3 builds explicitly on prior work (RFM, Dirichlet flow) (+8.83).

- **Demonstration beyond ground states.** The time-evolution extrapolation (Table 5) and 2D Heisenberg (Table 6) experiments show the method is not narrowly tailored to ground-state learning, addressing a natural concern about scope (+9.05).

## Weaknesses

### Major

- **Missing comparison against autoregressive baselines despite claiming to address their limitations.** The paper's introduction (line 39) criticizes autoregressive methods (Yao & You, 2024; Carrasquilla et al., 2019) for "sequential bottlenecks," yet these methods are not included as baselines in any experiment. The conclusion honestly acknowledges this gap: "it remains unclear whether they can consistently match or surpass autoregressive methods" (line 333). For a paper whose stated motivation partly rests on being non-autoregressive, the absence of this comparison is a significant evidential gap. Impact score: -9.05.

- **No evidence that the Anisotropic Dirichlet modification is actually beneficial.** The paper states (line 223): "For our AD flow, we evaluate for γ ∈ {0, 0.05, 0.1} and report the best value" — but does not state which γ was selected per experiment. Since γ=0 recovers standard (isotropic) Dirichlet flow, the claim that the anisotropic modification (γ>0) is a meaningful contribution is unsubstantiated without per-table γ reporting or a direct γ=0 vs. γ>0 comparison. Additionally, line 167 says "We set this to γ = 0.1 in the experiments," which is somewhat inconsistent with the grid-search statement. This weakness directly impacts whether the AD Flow method is a genuine contribution or simply standard Dirichlet flow. Impact score: -10.00.

### Minor

- **No ablation for Spherical Flow design choices.** The Spherical Flow uses a specific pushforward noise distribution (from the cross-polytope via π). It is not ablated whether improvements come from the S² geometry itself, this specific noise distribution, or their combination (e.g., a baseline of RFM on S² with a simpler noise distribution like uniform on S² would resolve this). Evidence: lines 137–141. Impact: -0.03.

- **Phase transition experiment (Figure 5) is only described qualitatively.** The text claims (line 251) that "LinearFM and StatisticalFM fail to accurately capture the phase transition" while "our spherical and AD flow succeed," but provides no quantitative measure (e.g., error in the estimated critical coupling c*). A quantitative comparison would substantially strengthen this result. Impact: -1.32.

- **Architecture details are referenced only to the appendix.** The paper refers to Section D for experimental details, but a brief summary of the neural network architecture (model type, layers, hidden dimensions, how Hamiltonian parameter c is embedded) would aid reproducibility assessment without relying on the appendix. Impact: -0.01.

- **The explicit coordinate mapping from 6 discrete shadow labels to S² is not formally stated.** While the Bloch map provides the conceptual framework and Figure 3 shows the 6 points on the sphere, a table of coordinates would clarify the embedding. Impact: -0.00.

### Trivial

- The text states "We set this to γ = 0.1 in the experiments" (line 167) but also says "we evaluate for γ ∈ {0, 0.05, 0.1} and report the best value" (line 223). These statements are somewhat inconsistent. Impact: -0.00.

## Nice-to-Haves

- A quantitative metric for the phase-transition experiment (e.g., error in estimated critical coupling c*) would substantiate the qualitative claim.
- Reporting the selected γ value per experiment table would resolve the AD contribution question.
- Including confidence intervals or standard deviations across seeds in all tables (they are currently reported for some but not all).
- The overhead of the AD flow pre-computation (acknowledged as a limitation) could be quantified.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"No neural network architecture specified (fatal/structural)":** The paper references Section D for experimental details; the parser strips appendices from the extracted text. The architecture details exist in the original submission's appendix. Downgraded from fatal to a minor point about main-text presentation.
- **"AD flow derivation not verifiable from main paper":** The derivation is in Appendix B, removed by the parser. This is standard practice for page-limited papers.
- **"RBFK/NTK only evaluated at 10k shadows":** This reflects the nature of kernel methods requiring fixed training sets; not a weakness of this paper.
- **"CS gap reflects both bias and variance":** This is standard in generative modeling comparisons and not specific to this paper.
- **"Autoregressive methods not discussed" (removed redundancy):** The paper does discuss them in related work (§5); the weakness is the missing comparison, not the discussion.

## Novel Insights

The key insight that emerges from this review is that the paper's genuine novelty — the Bloch sphere geometry of Pauli shadows and its connection to generative modeling — is convincingly demonstrated by the toy experiment (Figure 2) and the consistently strong empirical results. However, the paper's credibility is undermined not by a flawed core idea but by incomplete reporting of design choices (γ selections, architecture) and a missing comparison against the very methods it claims to supersede. The evidence that the anisotropic component (γ>0) drives the AD Flow results is absent from the paper as written, making it impossible to tell whether one of the two claimed contributions is substantiated. These are fixable issues that a revision could resolve, but they are real gaps in the current submission.

## Suggestions

1. **Report which γ value was selected for each experiment** in Tables 1–6, or include a full γ-sweep table showing performance at γ∈{0, 0.05, 0.1} for each setting. This is the single most impactful fix as it directly substantiates or reframes the AD Flow contribution.
2. **Include autoregressive baselines** (Yao & You, 2024) or provide a substantive quantitative discussion of why a direct comparison is difficult, referencing reported numbers from that paper.
3. **Add a brief architecture summary** (model type, number of layers, hidden dimensions, embedding scheme for c) in the main experimental setup section.
4. **Add a Spherical Flow ablation** comparing the current noise distribution against simple uniform noise on S² to isolate the contribution of geometry vs. noise design.
5. **Add a quantitative measure for the phase transition experiment** (e.g., error in estimated critical coupling or derivative at the critical point).

## Score and Decision

**Calibration anchor summary** (all anchors retrieved across rounds):

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| QuaDiM | P7f55HQtV8 | 6.50 | 1 | Yes | Most similar paper. Conditional diffusion for quantum property estimation. Had missing baselines (-9.98) and unclear setup (-10.00) weaknesses. ShadowFM has stronger novelty but similar comparison gaps. |
| Stiefel FM | 84WmbzikPP | 7.00 | 2 | Yes | Flow matching on Stiefel manifold for molecular generation. Strong geometric novelty + good presentation. ShadowFM is structurally similar but slightly weaker on presentation/completeness. |
| Wasserstein FM | HB4lr0ykTi | 6.33 | 2 | Yes | Rejected (5,8,6). Method only worked well for Gaussians — a fundamental limitation. ShadowFM's weaknesses are fixable, not fundamental. |
| LLM4QPE | vrBVFXwAmi | 8.00 | 1 | Yes | Higher-scored quantum property paper with comprehensive experiments. ShadowFM has more technical novelty in the geometric methods but less experimental breadth. |
| Quantum Complexity | tmSWFGpBb8 | 6.00 | 1 | Yes | Theoretical paper on quantum state complexity with classical shadows. Less directly comparable. |
| GSBM | SoismgeX7z | 7.00 | 2 | No | Generalized Schrödinger Bridge — less topically relevant. |
| Meta FM | 9SYczU3Qgm | 6.25 | 2 | No | Flow matching on Wasserstein manifold — less topically relevant. |
| OC-Flow | 61ss5RA1MM | 6.50 | 2 | No | Training-free guided flow matching — less topically relevant. |

**Round-1 bracket:** 6.0–7.5 (between weak accept and accept).

**Narrowing:** Comparing scored items, ShadowFM shares QuaDiM's missing-baseline weakness but has substantially stronger methodological novelty (geometric framing vs. "standard diffusion applied to quantum" for QuaDiM). Unlike Wasserstein FM (6.33, reject), ShadowFM's weaknesses are fixable omissions rather than fundamental methodological limitations. Stiefel FM (7.00) is the closest positive anchor: both introduce flow matching on a non-Euclidean geometry for a scientific application. ShadowFM has comparably strong novelty but the unsubstantiated γ contribution and missing AR baseline place it slightly below Stiefel FM's polish. The two decisive negative items (-9.05 and -10.00) pull the score down from the 7.0+ range, while the two +10.00 strengths and the absence of any fundamental methodological flaw prevent a lower score.

**Final score:** 6.5 — a borderline accept with strong core contributions but incomplete evidence for one of the two claimed methods and a significant missing comparison.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>