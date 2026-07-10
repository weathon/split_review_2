Now I have sufficient calibration information. Let me compile the final review.

## Summary of calibration:

**Round 1 bracket:** Score 1.5–3.5 (Reject range).

**Closest anchors:**

1. **fUz6Qefe5z** (avg 3.00, "How Neural Networks With Derivative Labels Work: A Neural Tangent Kernel Perspective") — shares the profile of a paper attempting a meaningful NTK extension but with a central result presented in an unverifiable way. Key weaknesses: "handwaviness of the mathematical treatment" (-9.09), "mathematical structure treated carelessly" (-10.00). Our paper has a stronger secondary contribution (Proposition 4/Theorem 2 at impact +9.96, lacking in fUz6Qefe5z) but similarly severe central-theorem issues.

2. **2NwHLAffZZ** (avg 2.33, "Weak Correlations...") — even worse presentation: undefined notation, unsupported claims, no experiments. Our paper is clearly above this.

3. **YN4uWzcbtt** (avg 4.25, "On the Positive Definiteness of the NTK") — clean theoretical paper with rigorous proofs. Different profile; our paper's central result is far less verifiable.

**Narrowing:** Within the 1.5–3.5 bracket, fUz6Qefe5z (3.00) is the best proxy. Our paper's clean secondary results (Proposition 4/Theorem 2) are a genuine strength above fUz6Qefe5z, but the Theorem 3 issues (undefined notation, self-contradictory statement, unjustified proof steps, unsubstantiated rough path theory application) are equally severe. I place the paper at **score 3.0**.

Now let me write the final review.

Wait, I notice the abstract overclaim about "order of magnitude" - let me reconsider whether this should be Minor or Trivial. Actually it's a real overclaim — the abstract says they "empirically evaluate the order of magnitude in network depth required to observe this convergent behavior" but they only test up to depth 30 with n_0=128. No scaling analysis of any kind. This is a minor overclaim.

Also, for the "list of properties not used" criticism — this is real. The paper lists three bullet-point criteria but provides no proof that these conditions are sufficient for Theorem 3 to hold. Only one additional example is mentioned but not analyzed. This is a minor weakness — the section amounts to speculation.

Let me finalize my review now.Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper studies the Neural Tangent Kernel (NTK) of infinitely wide, fully-connected ReLU networks as depth L → ∞ (with L ∈ o(min n_i)). The key observation — that the normalized kernel converges to the all-ones matrix (Theorem 2), making it singular — correctly identifies a limitation in prior work (Xiao et al. 2020). The non-core results (Lemma 1, Proposition 4, Theorem 2) are clean and verifiable. However, the paper's central claimed contribution (Theorem 3), which asserts that the NTK predictor still converges to a well-defined limit despite the singularity, is presented in a form that cannot be verified or properly evaluated.

## Strengths

- **The paper identifies a genuine technical gap.** Prior work (Xiao et al. 2020) assumed the limiting predictor analysis required factoring the kernel into a non-singular part. Theorem 2 shows this assumption fails for the ReLU NTK because the normalized kernel converges to the all-ones matrix. This is a real problem worth addressing. (Section 5, paragraph following Theorem 2.) [impact=+5.79]

- **Proposition 4 and Theorem 2 are clean, verifiable results.** The alternative formulation of the normalized kernel and the proof that it strictly increases to 1 are well-motivated and follow from known ReLU NTK recursions. These are modest but solid contributions. [impact=+9.96]

- **Lemma 1 and its use as a building block** for later results is correctly reasoned. [impact=+7.81]

## Weaknesses

### Fatal
None.

### Major

- **Theorem 3 uses an undefined quantity ̃Θ_∞^(L).** The paper defines Θ_∞^(L) (Definition 2, Theorem 1) and Θ̄_∞^(L) (Definition 4), but Theorem 3 and its proof rely entirely on ̃Θ_∞^(L) without ever defining it. The discussion preceding Theorem 3 (line 155) frames the result in terms of Θ_∞^(L), then the theorem statement switches to ̃Θ_∞^(L) without explanation. The paper's central claimed result cannot be evaluated as written. [impact=-10.00]

- **The statement of Theorem 3 is self-contradictory as presented.** It asserts paths v_{ij}^{(L)} that "drive" the solution u^{(L)} of d/dt u_i^{(L)}(t) = 0. If du/dt = 0, u is constant regardless of any driving signal — yet the theorem claims u^{(L)}(1) equals an expression depending on the NTK at layer L. The proof indicates the intended meaning (the driving signal converges to 0 as L → ∞, so the limiting equation is du/dt = 0), but the theorem conflates the finite-L RDE with its limit. This requires a complete rewrite. [impact=-10.00]

- **The proof sketch of Theorem 3 contains unjustified steps.** (a) The chain of determinant inequalities (lines 220–222) is asserted without any justification linking det(A_n^{(L+1)}(t)) to the expression involving determinants of ̃Θ raised to powers of ψ_D. (b) The application of Lyons' Universal Limit Theorem is stated without verifying that the necessary hypotheses (bounded p-variation of the driving paths, convergence of the rough path lift, continuity of the Itô-Lyons map in the relevant topology) are satisfied. The paths v_{ij}^{(L)} are defined implicitly through equation (5) and their properties are not analyzed. These are not minor gaps; they affect the paper's central result. [impact=-10.00]

- **The experimental section does not validate Theorem 3**, which is the paper's main theoretical claim. Column 3 of Figure 1 plots the predictor term κ̄^{(l)}(x^T X^T)(κ̄^{(l)}(XX^T))^{-1}, but this is barely discussed. No finite-width neural network is trained, no NTK regression is performed, and no test accuracy is reported. The experiments primarily validate Lemma 1 and Theorem 2 (which are secondary results), not the core claim that the NTK predictor converges to a well-defined limit despite the kernel singularity. [impact=-10.00]

### Minor

- **The abstract overclaims** by stating it "empirically evaluate[s] the order of magnitude in network depth required to observe this convergent behavior." The experiments only test depths up to 30 on synthetic/MNIST data with n_0=128. No analysis of how convergence depth scales with input dimension or other parameters is provided. [impact=-10.00, but this is a minor issue relative to the Theorem 3 problems]

- **The list of "properties that enable generalization to other kernels"** (Section 6, three bullet points) is stated without proof that these conditions are sufficient for Theorem 3 to hold. Only one example (η^(L)) is mentioned but not analyzed theoretically. This section reads as speculative, not a contribution. [impact=-10.00]

### Trivial

- **The conclusion contains garbled text:** "while convergence for the limiting kernel is sublinear, the convergence for the limiting kernel is experimentally fast" — "limiting kernel" is repeated, conflating two different objects. The conclusion also references "Proposition 8" which is in the (stripped) appendix without context. [impact=-10.00]

## Nice-to-Haves

- An experiment connecting the theoretical predictor limit to actual finite-width NTK training would ground the result.
- Quantitative convergence rates or scaling laws with input dimension would strengthen the "order of magnitude" claim in the abstract.
- A self-contained sketch of the rough paths machinery in the main text, clarifying what the machinery achieves that simpler arguments cannot.

## Removed Points

These points were considered but removed from the main weaknesses:

- **"Exponentiating a determinant to a power is not a standard operation"** — This is mathematically incorrect. For a positive scalar (determinant of a positive definite matrix), raising to any real power is standard. The broader point that the inequality chain is unsubstantiated is already covered.
- **"The regime L ∈ o(min i n_i) is not discussed in terms of its implications"** — The paper clearly states this regime and contrasts it with prior work. This is scope creep.
- **"No experiments on actual neural network training"** — The paper studies the NTK as a mathematical object; training networks is beyond its stated scope.
- **"Proposition 1 proof sketch too brief"** — Standard for a main-text proof sketch.
- **Various formatting/style nitpicks** — These are parser artifacts, not author errors.

## Novel Insights

Beyond the paper's own contributions, the review reveals a fundamental tension: the paper correctly identifies that prior work's assumption (factoring the kernel into a constant plus invertible part) fails for the ReLU NTK, but its own proposed resolution (Theorem 3 via rough differential equations) is presented too incompletely to assess. The determinant inequality manipulations appear to conflate matrix operations with scalar operations, and the rough path theory application is asserted without establishing the necessary hypotheses. This suggests the proof strategy may be salvageable but requires substantial rewriting to be verifiable.

## Suggestions

1. **Define ̃Θ_∞^(L) explicitly** in the main text, or clarify its relationship to Θ_∞^(L) and Θ̄_∞^(L).
2. **Rewrite Theorem 3** to clearly distinguish the finite-L RDE (where the driving signal is non-zero) from its limit as L → ∞ (where it vanishes). The current wording conflates the two.
3. **Provide a self-contained proof sketch** that at minimum states which hypotheses of Lyons' Universal Limit Theorem are satisfied and why, and justifies the determinant inequality chain.
4. **Add an experiment that directly tests the claimed convergence** of κ_x^T κ^{-1} by computing it numerically at several depths and showing stabilization, ideally compared against a finite-width NTK regression baseline.

## Score and Decision

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>