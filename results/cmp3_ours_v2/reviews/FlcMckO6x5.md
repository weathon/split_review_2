## Summary

This paper establishes theoretical foundations for Separable Neural Networks (SepNNs): a universal approximation theorem covering CP, TT, and Tucker variants via Stone-Weierstrass; a Neural Tangent Kernel (NTK) analysis characterizing two asymptotic regimes (deterministic under infinite rank, random under fixed rank); and a Separable Preconditioned Gradient Descent (SepPGD) algorithm achieving O(nD) complexity for n^D grid-structured training samples. Experiments on kernel ridge regression, INRs, and PINNs validate the approach.

## Strengths

1. **Clean universal approximation theorem for SepNNs (Theorem 1).** The proof via Stone-Weierstrass — showing that the class of CP-separable functions forms an algebra that separates points and contains constants, then approximating univariate factors with MLPs via the standard universal approximation theorem — is elegant and unifies CP, TT, and Tucker variants. This generalizes prior bivariate-only results (Cho et al., 2023).

2. **Novel NTK derivation for SepNNs (Lemma 1, Theorem 2, Corollary 1).** The SepNN NTK is derived in structured form (sum over factor NTKs weighted by products of other factors' outputs). The characterization of two distinct asymptotic regimes (infinite rank → deterministic kernel via law of large numbers; fixed rank → random kernel) is novel and correctly identified, going beyond simply applying standard NTK theory to a new architecture.

3. **SepPGD's O(nD) complexity is a genuine computational advance.** Table 1 makes this concrete: O(nD) vs O(n^D) (Geifman et al., 2024) and O(n^D/p) (Shi et al., 2025). For D=3 and n=256, this is ~768 vs ~16 million operations. The connection to Kronecker-product structure in Lemma 2 provides a clean theoretical grounding.

## Weaknesses

### Fatal
None.

### Major

1. **The "provably" claim for spectral bias alleviation is not supported by the arguments given.** The abstract states SepPGD "provably adjusts its NTK spectrum" and the contributions list states it "provably adjusts the eigenvalue distribution of NTK matrix." The actual argument in Section 4 (line 201) has three gaps:
   - (i) The reasoning transitions from "S̃ has better spectrum than K̃" to "K·S̃ has better spectrum than K" without accounting for eigenvector misalignment between K and S̃. The condition number of a product depends on eigenvector alignment, not just individual spectra.
   - (ii) The argument depends on the supposition "Suppose that K̃ is close to the true NTK matrix K which can be verified using the NTK matrix formulation in Lemma 3" — this is a supposition, not a proven fact, and the verification is not carried out.
   - (iii) The argument is only established for D=2; extension to D>2 is stated as "it is believed" rather than proved.
   
   The algorithmic contribution (SepPGD's efficiency) remains valid regardless, but the theoretical claim of *provable* spectral bias alleviation is overclaimed relative to what is actually demonstrated.

2. **Rank R is not stated for any experiment, severing the connection between theory and experiments.** The NTK theory (Theorem 2 vs. Corollary 1) makes a sharp distinction between the infinite-rank (deterministic NTK) and fixed-rank (random NTK) regimes. The rank determines which regime applies and critically affects the model's behavior. Yet the main text never reports what rank was used in the KRR, INR, or PINN experiments. The paper states "Detailed experimental settings are placed in Appendix Section A.12" (line 205), but the rank is essential context that should appear in the main text.

### Minor

3. **Convergence curves are mainly plotted against execution time, conflating computational efficiency with optimization improvement.** The paper acknowledges this (line 221: "Because the efficiency advantage... comes from the lower complexity in an iteration, we plot the convergence curve w.r.t. execution time"). However, the claim of "alleviating spectral bias" specifically refers to changing the optimization landscape, not just reducing per-iteration cost. The surface representation experiment (Fig. 3, right) is reported "under the same iteration number" and shows SepPGD improving IoU from 0.983 to 0.992, which partially addresses the concern — but the KRR and image representation experiments lack iteration-matched comparisons, making it unclear how much of the benefit comes from genuine optimization improvement vs. cheaper iterations.

4. **Lack of statistical reporting on main experimental results.** No error bars, confidence intervals, or standard deviations are reported for Figs. 2–4 (unlike Fig. 1 which reports mean/variance over ten runs). The image representation result (Fig. 3, left) reports PSNR for a single image. The PINN improvement (0.042 → 0.037 MSE) and surface IoU improvement (0.983 → 0.992) are modest, and without error bars it is unclear whether these differences are significant.

5. **The grid-input restriction is a significant limitation that deserves more prominence.** Footnote 2 (line 158) states that for non-grid inputs, "the computational complexity for NTK evaluation and SepPGD becomes equivalent to standard networks." This substantially limits the practical applicability of SepPGD's efficiency advantage, yet it is only mentioned in a footnote.

### Trivial
None.

## Nice-to-Haves

- Provide MSE-vs-iteration plots alongside the MSE-vs-time plots to disentangle computational speedup from optimization improvement.
- Measure and report the eigenvalue distribution of K·S̃ (or the effective NTK under SepPGD) vs. the plain NTK K, to directly validate the claimed spectral bias alleviation mechanism.
- Report the rank R used in each experiment in the main text.
- Include error bars or confidence intervals on the main experimental results.
- Ablate the preconditioner update frequency (the paper mentions every 10 iterations but provides no analysis).

## Removed Points

- **"Surface/PINN improvements are marginal and within run-to-run variance"** — Removed because without reported error bars this is speculation, not an identified problem. The lack of error bars is the real issue (covered in Weakness 4).
- **"Footnote 3 contradicts Table 1 complexity"** — Removed because Table 1's header explicitly states "in terms of applying the preconditioner," and construction cost is separately discussed in Remark 4. No contradiction.
- **"No comparison of SepPGD vs SepNN (MSK)"** — Removed because Fig. 2 includes both SepNN (MSK) and SepNN (SepPGD) in the legends, and the text mentions comparing with MSK. The baseline is present.
- **"Remark 1 understates complexity of multi-layer extension"** — Removed because referencing existing NTK formulas (Arora et al., 2019b) is standard practice.
- **Pure formatting/style nitpicks and reviewer-speculative concerns** — Removed per filtering rules.

## Novel Insights

The reviews surface a consistent asymmetry: the paper makes genuinely solid theoretical contributions (the universal approximation theorem and NTK regimes are well-executed and fill clear gaps), but overclaims the theoretical backing for the algorithmic component. The "provably" language is not matched by the argument in Section 4, which contains unverified suppositions, an incomplete eigenvector argument, and a D=2 limitation. The experiments are too sparse and statistically under-powered to fully support the spectral bias alleviation claim. This reveals an important pattern: a paper can have strong core theoretical contributions while simultaneously over-selling an algorithm derived from them — and a careful review will correctly penalize the algorithm claims without dismissing the theory.

## Suggestions

1. Replace "provably" with "effectively" or "with theoretical motivation" when describing SepPGD's spectral bias adjustment, and honestly characterize the gaps (the K̃≈K supposition, eigenvector alignment issue, D=2 limitation) in the main text.
2. Report the rank R used in all experiments directly in the main text or in an experiment table.
3. Add MSE-vs-iteration plots for at least one experiment to separate computational speedup from optimization improvement.
4. Add error bars or report statistics over multiple seeds for the main experimental results.

## Score and Decision

**Calibration anchors (all from the human-review corpus):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| "Inductive Gradient Adjustment for Spectral Bias in INRs" | 4.75 | 1 | Closest domain (spectral bias, NTK preconditioning, INRs). SepNN paper has stronger theory but similar empirical weakness. |
| "On the expressiveness and spectral bias of KANs" | 6.25 | 1 | Theory + experiments on spectral bias. Accepted. SepNN has broader theoretical scope but similar experimental gaps. |
| "Deep Learning Alternatives of KST" | 7.50 | 1 | Strong well-rounded paper; SepNN paper is not at this level (weaker experiments). |
| "Preconditioning for PINNs" | 5.00 | 1 | Had serious theory concerns but strong experiments. SepNN paper has stronger theory but weaker experiments. |
| "Minimum width for universal approximation" | 7.00 | 2 | Clean pure theory paper. SepNN paper has comparable theory quality but overclaims an algorithm. |
| "Connecting NTK and NNGP" | 6.00 | 2 | Pure NTK theory, mixed reviews. SepNN has comparable NTK theory plus broader contributions. |
| "On the Disconnect Between Theory and Practice of Overparametrized NNs" | 6.00 | 2 | NTK theory paper. Similar theory level. |

**Initial bracket (Round 1):** Between 5 and 7 — the theory is solid and comparable to accepted theory papers (6.25 KAN paper), but the experiments are notably weaker and the overclaimed "provably" language is a meaningful issue.

**Final assessment:** The theoretical contributions are genuine and novel; the SepPGD algorithm's complexity advantage is compelling. However, the overclaimed "provably" language for spectral bias alleviation is not supported by the argument given, and the experiments lack statistical rigor (no error bars, rank not reported, time-based convergence curves). The paper is stronger than the 4.75 INR-spectral-bias paper (better theory) but weaker than the 7.0 min-width paper (weaker experiments). It sits near the KAN paper at 6.25 but with more significant empirical gaps and an overclaiming issue, placing it slightly lower.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>