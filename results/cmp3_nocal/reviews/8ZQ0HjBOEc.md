## Summary

This paper studies the Neural Tangent Kernel (NTK) of infinitely wide fully-connected ReLU networks as depth \(L \to \infty\). It aims to prove two results: (1) the normalized NTK converges entrywise to the all-ones matrix (Theorem 2), and (2) despite this singularity, the NTK predictor \(\kappa_x^\top \kappa^{-1}\) converges to a well-defined bounded limit (Theorem 3), proved via rough differential equations (RDEs). The paper also provides empirical illustrations of convergence rates and a list of properties for generalizing the result to other kernel families.

## Strengths

1. **The question is well-motivated and non-trivial.** The convergence of the NTK to a singular matrix as depth increases is known (Seleznova & Kutyniok 2022), but what happens to the NTK *predictor* in the singular limit is a genuinely interesting open theoretical question. The paper correctly identifies this gap in prior work, particularly the limitation in Xiao et al. (2020) that assumes a non-singular decomposition of the limiting kernel.

2. **The rough differential equations approach is a novel technical choice.** Using rough path theory to handle the singular limiting kernel is creative and, if correctly executed, would provide a clean framework that avoids the invertibility assumptions of prior work.

3. **The identification of necessary properties for kernel generalization (Section 6, bullet list)** is a useful conceptual contribution that could guide analysis of other kernel families.

## Weaknesses

### Fatal

1. **Proposition 5, property (4) is incorrect — this invalidates the proof of Theorem 3, the paper's central claim.**  
   The function \(\psi_d\) is defined (Definition 6) as:  

   \[
   \psi_d(z) = \frac{1}{1 + \exp\left(\frac{-2z}{d(1-z^2)}\right)} \qquad (z \in ]-1,1[)
   \]

   Proposition 5 claims property (4):  

   \[
   \lim_{d \to 0^+} \frac{d^k}{dz^k} \psi_d(z) = 0 \quad \forall k \in \mathbb{N}_0.
   \]

   **This claim is false.** Direct computation at \(z=0\) (which lies inside the domain) gives:  

   \[
   \psi'_d(0) = \frac{1}{2d} \to \infty \quad \text{as } d \to 0^+.
   \]

   The \(k\)-th derivative at \(z=0\) scales as \((1/d)^k\) and diverges for all \(k \ge 1\).  
   The proof of Theorem 3 (lines 217–222) explicitly invokes property (4) of \(\psi_{\mathcal{D}}\) to argue that the terms \(v_{(i,j)}\) (which involve \(\frac{d}{dt}A_n^{(L+1)}(t)\), itself proportional to \(\psi'_{\mathcal{D}}(2t-1)\)) converge to 0 in the 1-variation metric, which then drives the RDE solution to the limiting equation \(u'_\infty(t)=0\). Because property (4) is false, this argument is unjustified. Theorem 3 — the paper's main claimed contribution — is therefore unsubstantiated as presented.

### Major

2. **The notation \(\tilde{\Theta}_\infty^{(L)}\) is never defined in the main text, making Theorem 3 difficult to follow.**  
   Definition 4 defines \(\bar{\Theta}_\infty^{(L)}\) (with a bar) as the normalized kernel. But Theorem 3 and its entire proof exclusively use \(\tilde{\Theta}_\infty^{(L)}\) (with a tilde), which is also used throughout the experiments section and the discussion after the proof. This is never formally defined or related to \(\Theta_\infty^{(L)}\) or \(\bar{\Theta}_\infty^{(L)}\) in the main text. For a theory paper, this is a significant expositional flaw — the reader cannot verify whether Theorem 3 applies to the normalized or unnormalized kernel.

### Minor

3. **Theorem 3 establishes boundedness but does not characterize the limit.**  
   The abstract and introduction claim that "the corresponding closed-form solution approaches a fixed limit on the sphere." However, Theorem 3 only shows existence of a bounded limit (entrywise bound \(< C(x)\mathbf{1}_n^\top\) and \(\mathcal{O}(n)\) norm bound). The limit itself is not characterized — its dependence on the data, its relationship to training targets, and whether it corresponds to a concrete meaningful predictor are not given. The gap between the advertised contribution and what is proved is notable.

4. **Empirical validation is thin for the paper's claimed scope.**  
   The main text shows results for one synthetic dataset (\(n_0=128\), uniform on sphere) with depths up to \(L=30\). The experiments compute only the NTK recursion analytically — they verify the *kernel's* convergence, not the *predictor's* convergence. No actual neural networks are trained, no quantitative convergence metrics for the predictor are reported, no comparisons across dataset sizes or random seeds are shown, and MNIST results are relegated to the (stripped) appendix. While this is a theoretical paper, the empirical component is too minimal to provide meaningful support.

### Trivial

5. **Proposition 1's proof sketch (line 77) is too terse to be informative.** The sketch says the product \(\sigma^2(f(z))\) "follows a squared rectified Gaussian distribution" but does not connect this to the claimed closed form. This does not affect the paper's main contribution (it is a restatement of a known result).

## Nice-to-Haves

- A reconstruction of Theorem 3's proof would require replacing \(\psi_d\) with a genuinely smooth function whose derivatives *do* vanish in the limit (e.g., bump-function smoothing rather than a sigmoid). If this can be done and the proof reworked, the theoretical contribution would be salvageable.
- Clarifying what Theorem 3 actually proves about the limit — whether the bounded limit can be further characterized, or whether only existence and boundedness are established.
- Adding experiments that train finite-width networks of increasing depth and compare their outputs to the NTK predictor at various depths would strengthen the paper.

## Removed Points

The following points from the harsh review were removed:
- *"Proposition 2's proof sketch on line 77 is essentially incoherent"* — This concerns Proposition 1, not Proposition 2, and it describes a known result from prior work. Removed as not central to the paper's contribution.
- *"No actual neural networks are trained"* — This is scope creep; the paper is a theoretical analysis of the NTK, not an empirical study of network training. Removed as not a fair expectation for this paper's genre.
- *"The proof of Theorem 3 in the main text is too compressed"* (missing appendix) — The appendix is stripped by the review system. Removed per policy.
- *"Contradictory statements in the conclusion"* — The paper distinguishes convergence speed of the kernel vs. the predictor; the phrasing is confusing but not contradictory. Demoted from strength-of-criticism and removed from weaknesses as it is a minor clarity issue rather than a substantive weakness.
- *"The proof is not reproducible"* style criticisms — Removed per policy.
- Generic or speculative criticisms without concrete paper anchors were removed.

## Novel Insights

The harsh review's most valuable insight is the verification that property (4) of Proposition 5 is mathematically false at \(z=0\). This is a genuine mathematical error — not a disagreement about interpretation or presentation — and it goes directly to the validity of Theorem 3. The observation that the derivative blow-up occurs precisely at the point where the smoothing function transitions (\(z=0\), corresponding to \(t=1/2\) in the RDE construction) is precise and shows why a different smoothing construction (e.g., bump functions with genuinely vanishing derivative norms) would be needed to salvage the proof. Beyond this, the review's observation that Theorem 3 proves boundedness rather than a concrete limit, and the notation gap (\(\tilde{\Theta}\) vs \(\bar{\Theta}\)), are useful but less novel.

## Suggestions

1. Reconstruct the smoothing function \(\psi_d\) so that property (4) genuinely holds — e.g., using a standard bump-function mollifier whose derivatives are bounded in \(L^\infty\) and vanish in the limit.
2. Formally define \(\tilde{\Theta}_\infty^{(L)}\) in the main text and explain its relationship to \(\Theta_\infty^{(L)}\) and \(\bar{\Theta}_\infty^{(L)}\).
3. Clarify the precise claim of Theorem 3 — is it a concrete limit formula, or only existence and boundedness? The abstract and body should match.
4. Add quantitative convergence metrics for the NTK predictor and, if feasible, validate on a small-scale finite-width network to substantiate the claim that the limiting predictor is meaningful.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>