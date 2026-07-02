---
job_id: 1c4b30ab-d36f-4497-9801-d00aaaeb0169
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: 1PIfB5w05x.pdf
paper: Price of Quality: Sufficient Conditions for Sparse Recovery Using Mixed-Quality Data
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope as a learning theory / high-dimensional statistics submission on sparse recovery, information-theoretic thresholds, and LASSO under heterogeneous noise.

## Minimum Quality
Pass ✅. The paper has the core components expected for a theory paper, including abstract, introduction with related work positioning, methodological/theoretical development, and conclusion. While I have substantial concerns about correctness and validation, these rise to the level of a strong technical review rather than a desk reject.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find any hidden prompts, instructions targeting automated reviewers, or other manipulative content in the provided paper text.

# Expected Review Outcome:
## Summary
This paper studies sparse support recovery with two data sources of different noise levels, a smaller high-quality set and a larger low-quality set. For the information-theoretic side, it gives sufficient recovery conditions in both an agnostic setting, where the decoder ignores per-sample noise levels, and an informed setting, where the decoder knows them, and introduces the notion of a “Price of Quality” measuring the exchange rate between the two sample types. For the algorithmic side, it analyzes LASSO in the agnostic setting and claims that the support-recovery threshold matches the classical homogeneous-noise case, depending on the noise only through the average variance.

## Strengths
The paper addresses a natural and timely variant of sparse recovery, namely mixed-quality data with heterogeneous noise, and frames it in a way that is easy to understand. The distinction between the agnostic and informed settings is meaningful, and the proposed “Price of Quality” quantity in Equation (5) gives a concrete way to reason about tradeoffs between expensive clean data and cheaper noisy data.

Theoretical ambition is reasonably broad. The paper does not stop at one estimator, but studies both exhaustive support recovery via the combinatorial estimator in Equation (8) and tractable recovery via LASSO in Equation (24). In particular, Theorem 3, if correct, would be the most interesting part of the submission, because the conclusion that the agnostic LASSO threshold depends only on the average noise level in Equation (6) is somewhat surprising and practically relevant.

The paper is generally well organized at the section level. The progression from setup, to information-theoretic sufficient conditions in Section 3, to algorithmic recovery in Section 4, is coherent. The remarks around Theorem 1 and Theorem 2 also help interpret asymptotic regimes such as high SNR, low SNR, and mixed high/low SNR regimes.

The main assumptions are stated explicitly: Gaussian design, exact sparsity, Gaussian additive noise, and binary signals for the information-theoretic part. This makes the intended scope clear.

## Weaknesses
1. **There is a serious mathematical inconsistency in the definition of the per-source SNRs on Page 5, and this undermines confidence in the paper’s technical precision.**  
   Right after Equation (7), the paper defines
   \[
   \mathrm{SNR}_1 := \frac{\mathbb{E}\left\|\left[y_i-x_i^\top \beta^*\right]_{i=1}^{n_1}\right\|_2^2}{\mathbb{E}\|Z^1\|_2^2} = \frac{s}{\sigma_1^2},
   \]
   and similarly for \(\mathrm{SNR}_2\). But \([y_i-x_i^\top \beta^*]\) is exactly the noise vector \(Z^1\), so the ratio on the left should be \(1\), not \(s/\sigma_1^2\). I understand what the authors likely intended, namely signal power over noise power, analogous to Equation (7), but as written this is simply wrong. This matters because the paper’s regime definitions on Page 5, and several interpretations in Section 3.1 and 3.2, are explicitly expressed in terms of \(\mathrm{SNR}_1,\mathrm{SNR}_2\). When a central quantity is misdefined, the reader is left unsure whether later asymptotic statements are merely notation slips or deeper derivational issues.

2. **The exposition of the main sufficient condition in Theorem 1 is not technically stable across the paper, with inconsistent formulas between the main text and proof materials.**  
   In Equation (9) on Page 5, the first logarithmic term is
   \[
   \log\!\left(1+\frac{\delta(2\sigma_2^2-\sigma_1^2)s}{2\sigma_2^4}\right).
   \]
   However, in Proposition A.1 on Page 14, the corresponding bound is written with a different denominator, and the progression of formulas in Appendix A later changes again. Even if one treats the appendix as non-essential for final judgment, this inconsistency directly affects the stated coefficient \(\alpha_1\) in the tradeoff \(\alpha_1 n_1+\alpha_2 n_2>n^*\), hence it also affects the “Price of Quality” in Equation (12). Since the paper’s central message is precisely about the quantitative exchange rate between sample qualities, inconsistency in these coefficients is not cosmetic, it strikes at the heart of the contribution.

3. **The agnostic information-theoretic result is only a sufficient condition, yet several of the headline conclusions are phrased in a way that risks over-interpretation.**  
   The abstract states that in the agnostic setting “one high-quality sample is never worth more than two low-quality samples,” and Section 1.2.1 repeats this as a prominent message, citing Equations (13) and (14). But this statement is only about the authors’ sufficient condition from Theorem 1, not about the actual information-theoretic threshold of the problem. Remark 3.2 does acknowledge non-sharpness, but the headline takeaway is still much stronger than the proven result. This matters because the “Price of Quality” is a proof-dependent artifact unless the bound is shown to be close to necessary. A different Chernoff optimization, a different decoder, or an actual converse could substantially change the exchange rate. As written, the paper sells a strong conceptual conclusion from a one-sided bound.

4. **The paper provides no empirical validation at all, not even simple simulations, despite making practically framed claims.**  
   The abstract and introduction motivate the problem using weak labels, human versus LLM annotations, sensor calibration, and medical imaging. Yet there are no experiments, no synthetic phase transition plots, no finite-sample checks, and no robustness tests. For a theory paper, I do not require large benchmarks, but some numerical evidence is especially important here for three reasons:  
   - The main information-theoretic result in Theorem 1 is explicitly not sharp.  
   - The practical object of interest, the “Price of Quality,” is asymptotic and could behave differently at realistic scales.  
   - Theorem 3 claims a rather strong robustness phenomenon for LASSO under heterogeneous noise.  
   Even a compact simulation study showing support recovery probability versus \((n_1,n_2)\), and comparing agnostic versus informed decoding, would materially strengthen the paper. The complete absence of quantitative results makes it hard to judge whether the asymptotic story is informative beyond the proof machinery.

5. **There are no figures or tables in the paper, which significantly hurts clarity for a submission built around regime comparisons and tradeoff interpretation.**  
   The paper repeatedly distinguishes three SNR regimes on Page 5, two decoder settings, two classes of thresholds, and a tradeoff quantity \(\gamma\). This is exactly the kind of paper that benefits from at least one summary figure or one comparison table. For example, a table contrasting the agnostic and informed conditions, or a phase diagram over \((\sigma_1^2,\sigma_2^2)\), would have made the message much easier to verify and digest. The absence of any figure or table is not just a presentation issue, it also makes it harder to assess whether the paper’s claims are as sharp and as distinct as advertised.

6. **The novelty is somewhat incremental relative to standard proof templates, and the paper does not fully clarify what is conceptually new versus technically adapted.**  
   The proof sketches for Theorem 1 and Theorem 2 follow standard large-deviation plus union-bound arguments over supports, and Theorem 3 is framed as an extension of Wainwright-style LASSO threshold analysis to heteroscedastic noise. That can still be publishable, but then the paper should more clearly isolate what the truly nontrivial new ingredient is. For instance, Section 4 mentions Gram-Schmidt and Haar orthogonal tools, which suggests some technical novelty, but the main paper does not explain enough about why the classical proof breaks and exactly which step the new random matrix argument repairs. As a result, the contribution currently reads as a plausible extension rather than a clearly delimited theoretical advance.

7. **The paper’s central notion of “Price of Quality” is potentially sensitive to the chosen decoder and proof relaxation, but this limitation is not integrated deeply enough into the paper’s conclusions.**  
   This issue appears most clearly in Remark 3.2 on Pages 6 to 7, where the authors themselves suggest that even in the agnostic setting, a different reweighted objective might perform better:
   \[
   \arg\min_{\beta\in\mathcal{B}_{p,s}} \sum_{i=1}^n \frac{1}{Y_i^2}\big(Y_i-\langle x_i,\beta\rangle\big)^2.
   \]
   This is a remarkable admission, because it means the main object \(\gamma\) may depend strongly on the choice of decoder and not just the statistical model. If so, the paper should be more careful to present \(\gamma\) as “the exchange rate under this sufficient analysis and estimator,” rather than as a broadly meaningful characteristic of mixed-quality sparse recovery. The current framing overstates universality.

8. **Theorem 3 is potentially the strongest result, but the assumptions and scope are narrower than the paper’s narrative suggests.**  
   The theorem is only for the agnostic setting, Gaussian i.i.d. design, \(s=o(p)\), \(s\to\infty\), and \(n_1,n_2=\omega(s)\), with signed support recovery and a beta-min condition \(\rho>0\). Those are standard assumptions, but they should temper the broad messaging in the abstract and conclusion about robustness of algorithmic recovery to heterogeneity. In particular, the informed setting is not addressed algorithmically at all, and the design covariance is restricted to \(I_p\). Since the heterogeneity enters only through the noise, one would like a more careful discussion of whether the “average noise only” phenomenon is expected to survive beyond this highly symmetric Gaussian setup.

9. **Some claims of sharpness and threshold matching are stronger than what the main paper substantiates.**  
   On Page 10, the conclusion states that “within the Gaussian design framework considered here, the informed information-theoretic threshold and the LASSO threshold are sharp, whereas the agnostic information-theoretic condition is sufficient but not proven tight.” For the informed information-theoretic side, Theorem 2 in the main paper is only a sufficient condition. The “sharpness” appears to rely on analogy with homogeneous-noise optimizations and appendix-level arguments, not on a stated converse theorem in the main text. Similarly, for LASSO, Theorem 3 gives necessary and sufficient asymptotic sample size conditions under the stated assumptions, but the phrasing in the conclusion risks sounding more general than what is actually proved.

10. **The presentation contains avoidable notation and indexing ambiguities that make technical verification harder.**  
   A few examples:  
   - In Equation (4), the block form of \(\Sigma\) is easy to infer, but the indexing around \(n_1,n_2,n\) is not always cleanly distinguished from source-specific sample counts.  
   - On Page 5, the low-quality vector definition uses indices \(i=n_1+1\) to \(n_2\) in one place, which is inconsistent with the earlier statement that there are \(n_2\) low-quality samples and total \(n=n_1+n_2\).  
   - In Equation (29), the first line uses \(X_S\) and the second line seems to contain \(X_{S^*}^T X_S\), which appears to be a typo for \(X_{S^c}^T X_S\), later corrected in Proposition D.1.  
   These may be fixable, but in a theory paper built on precise threshold formulas, such slips accumulate and reduce confidence.

## Questions
1. The most important clarification is the SNR definition on **Page 5**. Can the authors correct the definition of \(\mathrm{SNR}_1,\mathrm{SNR}_2\) and confirm whether all regime statements that use these quantities remain unchanged after correction? If the intended numerator was signal power rather than residual power, please rewrite those equations explicitly.

2. Please reconcile the inconsistent formulas around **Theorem 1 / Equation (9)** and the corresponding proposition in the proof. What is the exact coefficient multiplying \(n_1\) in the sufficient condition, and therefore what is the exact definition of the agnostic Price of Quality in **Equation (12)**? A precise correction here would significantly increase my confidence.

3. Can the authors state more explicitly, in the main paper, which of their conclusions are properties of the actual sparse recovery problem and which are properties of their chosen sufficient analysis? In particular, is the statement “one high-quality sample is never worth more than two low-quality samples” intended only as a property of the bound in **Theorem 1**, or do the authors believe it reflects the true threshold?

4. Since the paper is heavily motivated by practical mixed-quality data settings, why are there no simulations? Even a small synthetic study comparing empirical recovery boundaries to the sufficient conditions in **Equations (9), (16), (27), (28)** would help a lot. I would especially like to see whether the agnostic bound is loose or reasonably predictive, and whether the LASSO “average noise only” claim is visible at moderate \(p,s,n\).

5. For **Theorem 3**, can the authors explain more concretely, in the main paper rather than only by brief mention, which step of Wainwright (2009) fails under heterogeneous noise and how the QR/Haar argument repairs it? This would help distinguish technical novelty from a straightforward adaptation.

6. The paper suggests in **Remark 3.2** that a variance-proxy reweighting using \(1/Y_i^2\) might outperform the agnostic decoder. Do the authors have any heuristic evidence or theoretical intuition for whether such a decoder could break the “\(\gamma<2\)” phenomenon in the agnostic setting? An answer here could materially change how I interpret the significance of the Price of Quality result.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No ethics concerns based on the content of the main paper.

## Soundness Rating
2: fair. The paper contains interesting theoretical ideas, but there are central definitional inconsistencies and some over-strong interpretations relative to what is actually proved.

## Presentation Rating
2: fair. The overall structure is readable, but the lack of figures/tables, several notation/indexing issues, and inconsistent formulas make the paper harder to verify than it should be.

## Contribution Rating
2: fair. The problem is relevant and the agnostic versus informed framing is useful, but the empirical absence, one-sided nature of the main information-theoretic result, and limited clarity on what is fundamentally new reduce the overall contribution.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted.  
I see real potential here, especially in the framing and in the LASSO result if it is fully correct, but in the current form the paper does not clear the bar for me. The combination of a serious SNR-definition error, inconsistent formulas around the main sufficient condition, no empirical validation, and some over-interpretation of one-sided bounds leaves the submission short of ICLR standard.

## Reviewer Confidence
4: confident. I am confident in the assessment, especially regarding the technical clarity issues and the mismatch between claims and what is directly supported in the paper.