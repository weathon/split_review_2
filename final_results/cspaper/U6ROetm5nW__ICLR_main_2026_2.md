---
job_id: 15f5ca33-aaef-4aa8-8e6d-34964f55293f
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: U6ROetm5nW.pdf
paper: 
main_score_norm: 0.4
desk_reject: false
note: desk_rejection_enabled=false rerun
---
# Preliminary Observations:
N/A

# Expected Review Outcome:
## Summary
This paper studies sublinear-time Gaussian kernel density estimation in high dimensions through a hashing-based reduction to density-constrained approximate nearest neighbor search. The main claim is a new query-time/space tradeoff based on asymmetric LSH, including a polynomial-space regime with query exponent about \(0.05\), and a linear-space regime with query exponent \(0.1865\), which improves over the prior non-adaptive \(0.25\) bound.

## Strengths
The paper targets a concrete and important theoretical problem at the intersection of kernel methods, sublinear algorithms, and ANN/LSH. The high-level idea, replacing the symmetric LSH used in prior KDE reductions with an asymmetric ANN tradeoff, is interesting and well motivated.

I also found the overall structural reduction reasonably clear at a high level: Section 3 cleanly explains how KDE is decomposed into level-wise recovery problems, and Equation (8) / Equation (5) makes explicit the underlying ANN tradeoff that drives the result. This helps the reader see where the claimed improvement is supposed to come from.

Figure 1 is useful. The left panel gives an interpretable view of how \(\xi(\delta,x)\) changes with the space budget, and the right panel communicates the claimed plateau around query exponent \(0.05\). In other words, the figure does support the central qualitative message that more space initially helps, but only up to a point.

The paper also has a potentially meaningful contribution in the linear-space regime. If correct, the claimed \(1/\mu^{0.1865}\) query time would improve over the previous data-independent \(1/\mu^{0.25}\) exponent while staying in essentially linear space, which is the most compelling regime in the submission.

## Weaknesses
I have several concerns, and unfortunately some of them are not cosmetic, they affect whether the main statements are even well specified.

1. **There are serious inconsistencies in the core sampling definitions, and they propagate into the main analysis.**  
   The most problematic issue is **Definition 10 on Page 6**. It defines
   \[
   p_j := \min\!\left(\frac{1}{2^{jn\mu}},1\right), \quad m_j := \frac{1}{2^{jn\mu}}.
   \]
   This is inconsistent with the paper’s earlier description in **Equation (3) on Page 3**, where the sampling rate is
   \[
   p_j = (1/\mu)^{1-x_j}\cdot \frac{1}{n}.
   \]
   Later, the proof of **Lemma 31 on Pages 16-17** again uses
   \[
   p_j = \frac{1}{2^j n\mu} = \frac{\mu^{1-x_j}}{n},
   \]
   and \(m_j=(1/\mu)^{1-x_j}\). These are not the same as Definition 10. This is not a typo I can safely ignore, because \(p_j\) and \(m_j\) directly determine the sample size, the ANN dataset size, the space exponent, and the query exponent. If Definition 10 is wrong, then the formal algorithmic statement is wrong as written. If Definition 10 is merely a typo, then the authors need to correct it everywhere and re-check all downstream derivations. Right now the central data structure is not specified consistently.

2. **The definition of level sets is also internally inconsistent.**  
   In **Definition 9 on Page 6**, the level set is defined as
   \[
   \mathcal{L}_j^{\mathbf q}:=\{p_i\in \mathcal P: K(p_i,\mathbf q)\in (2^{-j},2^{-J+1}]\}.
   \]
   This interval does not make sense as a per-level geometric partition. It appears the upper endpoint should likely be \(2^{-j+1}\), not \(2^{-J+1}\). The surrounding text on **Pages 2-3** clearly discusses logarithmically many distance scales with \(K(p,q)\approx 2^{-j}\), and later arguments in Section 3 and Appendix B rely on such a partition. As written, Definition 9 does not define disjoint geometric bands in the standard way, and it is hard to verify the claims built on it. Again, this is not a minor nit: the reduction from KDE to Level-\(j\) Recovery depends on the level sets being correct.

3. **The main quantitative theorem is based on numerics without accuracy guarantees, and the paper does not make that dependence sufficiently rigorous.**  
   **Theorem 17 on Page 9** states concrete exponents \(0.05\), \(4.1\), and \(0.1865\), but the proof in **Appendix D, Pages 19-20** says these come from numerical evaluations, and **Section D.1 on Page 20** says the values are obtained by a grid search. There is no discretization error analysis, no certified optimizer, no interval bound, and no sensitivity study showing that the quoted constants are stable. This matters because the contribution is almost entirely about shaving exponents. If the main theorem is numerical, then the numerical procedure needs to be much more carefully documented in the main paper. Right now, Theorem 17 reads like a formal theorem, but it is really a theorem-plus-uncertified-computation package.

4. **There are mathematical inconsistencies in the optimization domains and variable ranges.**  
   The paper alternates between several different maximization ranges for the same quantity:
   - **Equation (10) on Page 8** uses \(y\in[x,1]\),
   - **Equation (11) / Lemma 31 on Page 16** first states \(y\in[x,1]\),
   - the derivation on **Page 18** writes \(\max_{y\in[0,1]}\),
   - and on **Page 17** there is even a line with \(\max_{y\in[r,1]}\), mixing a radius and a normalized level variable.
   
   The paper tries to justify later that using \([0,1]\) does not hurt because no \(y<x\) maximizer should appear, but this is not proved carefully. Since the result hinges on taking a nested \(\min_\rho\max_y\max_x\), even small domain mismatches can change the exponent. The authors need to standardize the definition of \(\gamma(\rho,x)\), \(\xi(\delta,x)\), and \(\xi(\delta)\), and show rigorously which domain is valid.

5. **The exposition around the key ANN-to-KDE derivation is much looser than it should be for a theory paper.**  
   A representative example is the derivation in **Lemma 31, Pages 16-18**. The proof repeatedly says terms are \(o(1)\), moves between the original space and the sphere-reduced space, and substitutes \(r_i,r_j,c,R\) into the collision exponent, but many intermediate steps are compressed enough that checking correctness is difficult. For example, the collision exponent \(\chi(\rho_q,x_j,x_i)\) is rewritten across multiple lines with several substitutions and dropped terms, yet the paper does not clearly isolate which asymptotic is with respect to \(n\), which with respect to \(1/\mu\), and how the reduction distortion interacts with the exponent. Given that the paper’s main value is an exponent improvement, this level of derivational compression is not ideal.

6. **The claimed practical significance is limited by the space blow-up, and the paper does not sufficiently quantify that tradeoff beyond exponents.**  
   The headline result in **Theorem 1 / Theorem 17** is a query exponent of about \(0.05\), but it comes with space about \(1/\mu^{4.1}\) or \(1/\mu^{4.15}\). That is a very substantial cost. The right panel of **Figure 1** does show the plateau visually, and this is actually informative: it suggests that after a point, throwing more space does little. But that also undercuts the practical attractiveness of the best-query regime. The paper would be stronger if it gave more interpretation of what these exponents mean for realistic \(\mu\), rather than only asymptotic comparisons. As written, the most attractive regime is actually the linear-space one, not the headline \(0.05\) result.

7. **The literature positioning is narrower than it should be for an ICLR audience.**  
   The paper compares itself almost exclusively to the Charikar et al. line of work. That is fair for the precise asymptotic-theory niche, but there are directly relevant ANN-based and fast-KDE works that would help position the contribution more honestly. In particular, I did not see discussion of **Karppa et al. (2021), DEANN: Speeding up Kernel-Density Estimation using Approximate Nearest Neighbor Search**, which is highly relevant conceptually because it also connects KDE acceleration to ANN search. Even if the guarantees are different, omitting such a close conceptual neighbor makes the paper look more insulated than it should. For ICLR, I would expect stronger contextualization relative to both theory-first and implementation-oriented fast KDE approaches.

8. **The paper’s main theorem statements are somewhat over-polished relative to the actual level of formal support.**  
   This is related to Point 3, but distinct. For instance, **Theorem 17 on Page 9** states exact-looking exponents, while the proof says they come from numerical evaluation. Also the theorem statement contains
   \[
   \mu^* := K(\mathcal P,\mu),
   \]
   which should presumably be \(K(\mathcal P,q)\). On its own that last issue is minor, but combined with the definitional inconsistencies above, it contributes to a broader impression: the paper often presents a polished final claim before the underlying formal scaffolding has fully settled.

9. **The reliance on appendix-only technical support is heavy enough that the main paper underspecifies the core contribution.**  
   The main paper repeatedly points to Appendix A, B, C, and D for the actual argument. That is normal to some extent, but here the formal derivation of the new Level-\(j\) Recovery bound is concentrated in **Lemma 31 in the appendix**, and the main body gives only a high-level sketch. Since the central novelty is exactly this exponent calculation, I think the main text should contain a crisper and self-contained derivation of the query exponent, rather than deferring nearly all hard steps.

10. **There is no empirical validation beyond plotting the derived exponent functions.**  
   I understand this is primarily a theory paper, so I am not asking for large-scale benchmarks as a requirement. Still, the only “results” in the main paper are the numerically evaluated exponents shown in **Figure 1**. There are no experiments checking whether the proposed scheme behaves as expected on synthetic data, whether the relevant scales \(x\) identified by the optimization indeed dominate in practice, or even whether the tradeoff is robust to finite-size effects. Since the headline improvement is modest in the linear-space regime, some sanity-check experiments would have materially increased confidence. Figure 1 is helpful, but it is not a substitute for validation.

## Questions
1. **Can the authors explicitly correct and reconcile the sampling-rate definitions?**  
   In particular, please clarify whether **Definition 10** should read
   \[
   p_j=\frac{1}{2^j n\mu}=\frac{\mu^{1-x_j}}{n}, \qquad m_j=\frac{1}{2^j\mu}=(1/\mu)^{1-x_j},
   \]
   or something else. This is my biggest soundness concern, because the current version is inconsistent with Equation (3), Lemma 31, and the rest of the analysis.

2. **Can the authors fix Definition 9 and restate the level-set partition precisely?**  
   I would like to see a corrected definition of \(\mathcal L_j^{\mathbf q}\), and a short explanation confirming that the level sets form the geometric partition required by Algorithms 1-2 and Claim 26.

3. **How accurate are the reported numerical exponents in Theorem 17?**  
   Please provide the grid resolution, the observed stability of the optimum under refinement, and ideally an interval such as “the exponent is in \([0.049,0.052]\)” rather than a point estimate \(0.05\). The same applies to \(0.1865\) and the threshold around \(\delta\approx 3.15\).

4. **Can the authors standardize the optimization domains in Equations (10), (11), and the proof of Lemma 31?**  
   Is the correct domain \(y\in[x,1]\) or \(y\in[0,1]\)? If the latter is safe, can the authors prove that no maximizer occurs at \(y<x\), rather than asserting it informally?

5. **What exactly is the formal status of Theorem 17?**  
   Is it meant as a theorem conditional on numerical optimization, or as a rigorous theorem with certified constants? A sharper statement would help calibrate expectations.

6. **Can the authors comment on the finite-parameter meaning of Figure 1?**  
   The right panel suggests a plateau around query exponent \(0.05\) after space exponent roughly \(4.1\). Some discussion translating this into concrete parameter regimes would help, especially since the headline tradeoff may be less attractive than the linear-space regime in realistic settings.

7. **Could the authors position the work more carefully relative to other ANN-based fast KDE methods, such as DEANN?**  
   Even a short discussion of differences in goals, guarantees, and regimes would improve the paper’s contextualization.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
None.

## Soundness Rating
2: fair. The high-level idea is plausible and interesting, but the paper has multiple formal inconsistencies in its definitions and theorem support, especially around the sampling rates, level sets, and the numerical nature of the headline exponents.

## Presentation Rating
2: fair. The high-level story is understandable and Figure 1 is helpful, but the notation and formal statements are inconsistent often enough that they materially hinder verification.

## Contribution Rating
2: fair. If all claims are corrected and validated, the linear-space improvement over prior data-independent bounds would be worthwhile. In the current form, however, the contribution is undermined by specification issues and by the fact that the strongest headline result requires a very large space exponent.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted.  
The core idea is interesting and there may be a real technical contribution here, especially in the linear-space regime. However, the current manuscript has too many issues in its formal setup and too much reliance on uncertified numerical optimization for me to recommend acceptance as is.

## Reviewer Confidence
4: confident. I am confident in the assessment and carefully checked the main definitions, equations, and theorem dependencies, though some appendix-level derivations are dense enough that a few implementation details of the underlying ANN machinery could still benefit from author clarification.