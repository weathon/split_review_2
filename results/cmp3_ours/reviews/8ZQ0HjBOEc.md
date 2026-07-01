Now I'll write the final consolidated review.

## Summary

This paper studies the deterministic Neural Tangent Kernel (NTK) of infinitely wide fully-connected ReLU networks as depth L → ∞ (with width growing much faster than depth). It shows that (1) the correlation coefficient ρ^(L) between neurons converges to 1 (Lemma 1), (2) the normalized NTK entries converge to 1 (Theorem 2, making the kernel matrix singular), and (3) despite this singularity, the closed-form NTK prediction formula κ_x^T κ^{-1} converges to a well-defined bounded limit (Theorem 3, via rough path theory). Experiments illustrate convergence rates for kernel quantities.

## Strengths

- **Lemma 1 (ρ^(L) → 1) and Theorem 2 (normalized kernel entries → 1) are clean, verifiable results** that correctly identify a genuine singularity at infinite depth: the kernel matrix becomes all-ones, hence singular. The recurrence for ρ^(L) (from Arora et al. 2019b / Cho & Saul 2009) defines a map whose dynamics are correctly analyzed, and the proof that the normalized kernel strictly increases to 1 (Proposition 4 + Theorem 2) is sound.

- **The problem is well-motivated.** The NTK prediction formula (Proposition 3) requires kernel inversion. Understanding when and how this expression remains well-defined as depth increases and the kernel becomes singular is a meaningful theoretical question that deserves analysis.

- **The use of rough differential equations** to handle the singular limit, while not fully executed, is a novel technical approach in the NTK context that could be productive in future work.

## Weaknesses

### Major

1. **The notation \tilde{Θ}_∞^{(L)} used throughout Theorem 3 and its proof is never defined.** Definition 4 defines \bar{Θ}_∞^{(L)} (the normalized kernel), but Theorem 3 (line 183) and its entire proof (lines 183–227) use \tilde{Θ}_∞^{(L)} without any definition or stated relation to \bar{Θ}_∞^{(L)}. If \tilde{Θ} = \bar{Θ}, this must be stated explicitly (the interpolation A_n^{(L+1)}(t) at line 195 mixes \tilde{Θ}_∞^{(L)} and \tilde{Θ}_∞^{(L+1)}, making the normalization scaling critical). If \tilde{Θ} is something else (e.g., the unnormalized kernel), the proof fails because the entries grow with L and the interval bounds in the proof would not hold. This is not a minor presentation issue — the theorem statement and proof are unverifiable as written.

2. **Theorem 3 does not deliver what the paper advertises.** The abstract claims the paper "characterizes" the limiting kernel and the closed-form solution "approaches a fixed limit on the sphere." The Introduction says Theorem 3 provides "the limiting solution to the output of a fully-connected ReLU network." In reality, Theorem 3 proves only that a bounded limit exists — not what it is for any given input x (beyond the trivial fact that at training points x_i the limit is e_i, which follows from interpolation). The limiting ODE is du/dt = 0, so the limit is constant in t, but the theorem never computes or characterizes this constant as a function of x. This is a structural mismatch between the advertised contribution and what is proved.

3. **The proof sketch of Theorem 3 has significant gaps beyond the notation issue:**
   - **Convergence in 1-variation is asserted without verification.** The proof states the terms v_{ij}^{(L)} "are all of bounded total variation" and "converge to 0 in the 1-variation metric" based on the smoothness of ψ_D and pointwise convergence. Pointwise convergence does not imply 1-variation convergence, and the dependence of ψ_d's parameter D = det(Θ^{(L+1)})det(Θ^{(L)}) on L (which drives d → 0) is not analyzed. Lyons' Universal Limit Theorem requires convergence in a rough-path topology, but the needed estimates are not provided.
   - **The determinant inequality chain (lines 219–223) lacks justification.** The first inequality (bounding 1/det(A(t)) by products of determinants) relies on concavity of log-det on positive definite matrices — a step that is not mentioned in the proof. The second inequality (replacing ψ and 1-ψ by 1) is directionally correct for a∈(0,1) (since a^ψ ≥ a), but the paper's justification that "the strictly positive determinants are all smaller than 1" does not explain the first, more subtle inequality. The connection to "property (4) of ψ_D" is unclear.

4. **The experiments do not validate the paper's central claim about the network output.** Figure 1 plots kernel quantities (ρ, η, normalized kernel entries, and the normalized κ_x^T κ^{-1} expression), which show convergence of the kernel expression. But there is no experiment that computes the actual NTK prediction (κ_x^T κ^{-1} y) for increasing L and demonstrates convergence to the (unspecified) limit. For a paper whose main advertised result is about the network's output, the experiments only show convergence of kernel entries, which is already established by Theorem 2. The paper also claims L=30 is "sufficient to show convergence" for a logarithmic convergence rate, without justification.

### Minor

5. **The comparison to Xiao et al. (2020) is overstated.** The paper presents its result as generalizing prior work by not requiring kernel invertibility assumptions. However, Xiao et al. characterize three phases and prove exponential convergence to a *characterized* constant predictor in the chaotic phase. This paper proves only that a limit exists — without characterizing it. These are different types of results, and the paper's framing suggests a stronger advance than is delivered.

6. **The conclusion contains a confusing sentence:** "while convergence for the limiting kernel is sublinear, the convergence for the limiting kernel is experimentally fast" — the same object appears twice. Context makes clear the intended contrast is between kernel convergence and κ_x^T κ^{-1} convergence, but the phrasing conflates them.

### Trivial

- The proof sketch of Proposition 1 (line 77: "μ = 0 implies x^T x' ≥ 0 with probability 1/2") is unclear and does not constitute a complete proof.

## Nice-to-Haves

- Computing or characterizing the actual limiting predictor (not just proving existence) would turn the existence result into a genuine, impactful contribution. The paper notes the limit is "dependent on x and non-trivial" — determining what it is (e.g., a nearest-neighbor or centroid-based rule) would be highly valuable.
- Including an experiment that trains a finite-width ReLU network at various depths and compares its output to the NTK prediction would strengthen empirical validation.
- Clarifying the convergence rate analysis: the paper hypothesizes that "small determinants indicate fast convergence" but does not test this hypothesis on cases where determinants are not small.

## Removed Points

- **"Inequality chain is backwards"** (from harsh critic): REMOVED. The direction is correct given a∈(0,1)⇒a^ψ≥a for ψ∈[0,1]. However, the missing justification for the first inequality (concavity of log-det) is addressed in Major 3(b).
- **"No experiment that trains a neural network"** as a critical flaw: DEMOTED from critical to Minor. In the infinite-width NTK regime, the kernel expression IS the prediction; training a finite-width network is an approximation check, not a validation of the core theoretical claim. The retained criticism is that experiments don't show convergence of the actual NTK prediction to any characterized limit.
- **"The limiting ODE is trivial (du/dt = 0)"** as a separate flaw: REMOVED. The theorem's purpose is to establish existence of the limit, not that the ODE has interesting dynamics. This duplicates the characterization issue already in Major 2.
- **Claims about missing appendix content**: REMOVED. The appendix is stripped by the parser; claims about missing appendix details are not verifiable.
- **Generic "Strengthening the Paper on Its Own Terms" suggestions**: MOVED to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The review identifies a gap between what the paper advertises (a characterization of the limiting NTK output) and what it delivers (an existence result with an incomplete proof), but this is a critique, not a novel insight about the subject matter.

## Suggestions

1. Define \tilde{Θ} explicitly in relation to \bar{Θ} (or replace \tilde{Θ} with \bar{Θ} throughout, if they are meant to be the same).
2. Either compute the limiting predictor or honestly reframe the paper's claims as proving "existence of a well-defined limit" rather than "characterization of the network output."
3. Provide rigorous estimates for the 1-variation convergence of the driving signal v_{ij}^{(L)}, with explicit analysis of how the parameter D = det(...) → 0 interacts with the smoothness of ψ_d.
4. Include at least one experiment where the actual NTK prediction (κ_x^T κ^{-1}y) is computed for increasing L and shown to converge.

## Score and Decision

**Calibration report:**

All anchor papers retrieved (6 queries, 24 total hits):
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| nSDOkm0SKo.md | 1.00 | R1 (high<1.5) | Strong reject, not comparable (unrelated topic) |
| Uj0h13lVrR.md | 1.00 | R1 (high<1.5) | Strong reject, not comparable |
| P49gSPmrvN.md | 1.00 | R1 (high<1.5) | Strong reject, not comparable |
| bEgDEyy2Yk.md | 1.00 | R1 (high<1.5) | Strong reject, not comparable |
| 2NwHLAffZZ.md | 2.33 | R2 (low=1.5, high=4.0) | Weaker theoretical NTK paper; this paper is stronger |
| GxrVyYoLSx.md | 3.50 | R2 (low=1.5, high=4.0) | Theory paper on overparametrized networks; comparable rigor |
| fUz6Qefe5z.md | 3.00 | R2 (low=1.5, high=4.0) | NTK extension paper; similar quality but cleaner proofs |
| bWz8aOPwsJ.md | 3.75 | R1+R2 | Empirical NTK paper; this paper is comparable but more theoretical |
| kOtFuzoA93.md | 4.00 | R1 (low=3.5, high=5.5) | Kernel models theory; cleaner results than this paper |
| WH9NhxOeu9.md | 5.00 | R1 (low=3.5, high=5.5) | Sharp generalization bounds; stronger theory than this paper |
| YN4uWzcbtt.md | 4.25 | R1 (low=3.5, high=5.5) | NTK positive definiteness; clean proofs, incremental; this paper has less complete proofs |
| 3LLkES6nNs.md | 4.25 | R1 (low=3.5, high=5.5) | Infinite-depth ResNet theory; similar ambition, cleaner execution |
| 5EtSvYUU0v.md | 6.00 | R1 (low=5.5, high=7.5) | NTK-NNGP unification; stronger and cleaner than this paper |
| GqI4fTVUXC.md | 6.00 | R1 (low=5.5, high=7.5) | NTK theory-practice disconnect; solid empirical paper |
| S04xvGXjEs.md | 6.00 | R1 (low=5.5, high=7.5) | Collective variables / NTK analysis; stronger results |
| VEJzjAvaIy.md | 5.75 | R1 (low=5.5, high=7.5) | NTK divergence in classification; clear result despite limitations |

**Round 1 bracket:** 3.0 – 4.5 (based on comparison to anchors in 3.5–5.5 band)

**Narrowing:** The paper's partial results (Lemma 1, Theorem 2) are clean and would place it near 4.0, but the central Theorem 3 has verifiable proof gaps and the paper overclaims its contribution. The undefined \tilde{Θ} notation alone makes the main theorem unverifiable as submitted. This pulls the score down to 3.0 — the paper has some merit but the central contribution does not hold up under scrutiny.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>