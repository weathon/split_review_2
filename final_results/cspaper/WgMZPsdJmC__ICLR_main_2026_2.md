---
job_id: 52da69ca-905e-4c35-b6b1-5624d92bf574
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: WgMZPsdJmC.pdf
paper: 
main_score_norm: 0.2
desk_reject: false
note: desk_rejection_enabled=false rerun
---
# Preliminary Observations:
N/A

# Expected Review Outcome:
## Summary
This paper studies steepest descent on convex quadratic objectives through the scalar quantity \(r_k\), defined as the reciprocal of twice the exact Cauchy stepsize, and then introduces a multiplicative steplength coefficient \(s=1/t\). The authors derive a one-dimensional update map \(r_{k+1}=G(r_k)\), analyze its fixed points in the two-dimensional quadratic case, and argue that different values of \(t\) lead to convergence to a fixed value, 2-cycle behavior, or chaotic/unstable behavior. The paper also presents numerical illustrations in high dimensions and a brief qualitative comparison to the BB method.

## Strengths
The paper tackles a classical optimization topic from an unusual angle, namely by tracking the dynamics of the Rayleigh-quotient-like scalar \(r_k\) rather than only the iterate \(x_k\) or objective value. For simple quadratic models, this perspective is potentially interesting and could in principle offer an interpretable dynamical-systems view of step selection.

The 2D focus in Section 2 is a reasonable starting point. In particular, the attempt to derive an explicit map \(G(r)\) in **Equation (16)** and then study fixed points through **Equations (22)-(23)** is directionally sensible for understanding why steepest descent on quadratics exhibits oscillatory behavior.

Some figures do help communicate the intended qualitative story. For example, **Figure 4(a)** and **Figure 5(a)** visually suggest different behaviors for \(t=0.9\) and \(t=1\), respectively, and this matches the paper’s qualitative narrative that under-relaxation may drive \(r_k\) toward a single band while classical steepest descent produces a two-point alternation. Similarly, **Figure 7** conveys that the authors are trying to contrast the trajectory structure of the proposed scaled-SD dynamics with a more spectral method such as BB.

The paper also references several classical works on steepest descent, randomized steepest descent, and Yuan’s stepsize, so the authors are at least engaging with some established optimization literature rather than presenting the topic in isolation.

## Weaknesses
1. **The central recurrence is mathematically inconsistent, and this undermines the entire analysis.**  
   The most serious issue is the definition of the \(r\)-update itself. In **Equation (11)** on Page 2, the numerator and denominator are written identically:
   \[
   r_{k+1} = \frac{\sum_{i=1}^{n} a^{(i)} g_k^{(i)2}(r_k-a^{(i)})^2}{\sum_{i=1}^{n} a^{(i)} g_k^{(i)2}(r_k-a^{(i)})^2}.
   \]
   As written, this gives \(r_{k+1}=1\) for every iterate, which is obviously incompatible with the rest of the paper. The same problem appears again in **Equation (13)**. However, in **Equation (15)** the denominator no longer contains the factor \(a^{(i)}\), which suggests that either **Equation (11)** or **Equation (15)** is wrong. This is not a cosmetic typo, because the paper’s whole contribution depends on the map \(r_{k+1}=G(r_k)\). If the defining recurrence is inconsistent, then the derivation of **Equations (16)-(31)** and the later experimental interpretation are not trustworthy.

2. **Equation (12) appears to drop a factor of 2, again at the core of the method.**  
   From **Equation (4)**, the paper defines
   \[
   r_k = \frac{1}{2\alpha_k^{SD}},
   \]
   so \(\alpha_k^{SD} = \frac{1}{2r_k}\). With \(s=1/t\), **Equation (7)** implies
   \[
   x_{k+1}=x_k - s\alpha_k^{SD}\nabla f(x_k)
   = x_k - \frac{1}{t}\frac{1}{2r_k}\nabla f(x_k)
   = x_k - \frac{\nabla f(x_k)}{2tr_k}.
   \]
   But **Equation (12)** states
   \[
   x_{k+1}=x_k-\frac{\nabla f(x_k)}{tr_k},
   \]
   which is off by a factor of 2. This is not a secondary detail. It changes the effective stepsize, shifts the fixed-point analysis, and likely invalidates the thresholds claimed for the regimes \(t<1\), \(t=1\), and \(t>1\).

3. **Several derivative/fixed-point expressions are internally incorrect or self-contradictory.**  
   A few examples:
   - In **Equation (30)** on Page 5, the derivative is written as
     \[
     G(r_e)'=\frac{t a^{(1)}-a^{(2)}}{t a^{(1)}-a^{(2)}} \approx \frac{t}{t-1}< -1.
     \]
     The fraction on the left is identically 1, so it cannot be approximated by \(\frac{t}{t-1}\), nor can it be \(< -1\).  
   - In **Equation (23)**, the second line
     \[
     1 - \frac{8(ta^{(1)}a^{(2)} + \frac{(a^{(1)}+a^{(2)})}{2})}{(a^{(1)}-a^{(2)})^2}
     \]
     does not obviously follow from the preceding line, and the algebra looks dimensionally suspicious.  
   - The paper states on Page 4 that when \(t\to 1^+\), \(G(r_e)'\) reaches its maximum at \(-1\), and then immediately concludes \(G(r_e)'<-1\). This transition is not justified.  
   These are not isolated slips. They occur exactly in the equations that are used to classify stability and “chaos”.

4. **The paper repeatedly makes strong claims about chaos and attractors without the required evidence.**  
   The abstract, Section 2.1, Section 3.2, and the conclusion all claim chaotic behavior, repulsion, or “strange attractors.” But for a one-dimensional map, simply observing \(|G'(r_e)|>1\) at a fixed point is not enough to claim chaos. It only shows local instability of that fixed point. To support a chaos claim, the paper would need substantially stronger evidence, for example a precise definition of chaos in the present setting, a bifurcation analysis, a Lyapunov exponent calculation, a topological-conjugacy argument, or at least systematic numerical evidence ruling out simpler periodic behavior.  
   This matters because “the function actually describes a chaotic system” is one of the paper’s headline claims in **Section 5**, yet the supporting analysis does not reach that bar.

5. **The experimental section is far too weak for the claims being made.**  
   Section 4 is only a set of qualitative plots over one synthetic 10,000-dimensional diagonal quadratic with arithmetic-progression eigenvalues and random initialization. There are no quantitative metrics, no repeated runs, no sensitivity analyses, no convergence rates in \(f(x_k)-f(x^\*)\) or \(\|g_k\|\), no runtime cost, and no comparison of optimization quality. In fact, the paper contains **no results tables at all**, which is a major omission given the strength of the claimed phenomena.  
   This is particularly problematic because the conclusion claims that the unstable regime may be useful for acceleration, yet no experiment measures acceleration. A convincing paper would at least report iteration complexity or objective reduction versus SD, BB, randomized SD, and perhaps Yuan-type methods.

6. **The figures are mostly suggestive visuals rather than rigorous evidence, and some do not support the claimed interpretation.**  
   - In **Figure 1(b)**, the paper argues that the intersection geometry between \(G(r)\), \(G^{-1}(r)\), and \(y=x\) shows repulsion. This is not a standard or sufficient argument for instability. What matters is the derivative magnitude of \(G\) at the fixed point, not the angle formed with \(y=x\).  
   - **Figure 3** is used to support the existence of “several different orbits” in high dimension for \(t>1\), but the figure looks more like a cloud along curves than a principled orbit decomposition. No formal criterion is given for what counts as an orbit or a “narrow band.”  
   - **Figures 4-6** show trajectories or histograms of \(r\), but they do not connect the observed \(r\)-behavior to optimization performance. Seeing a single band, two bands, or a broad distribution is not the same as showing better or worse minimization behavior.  
   - **Figure 7** compares BB to SD with \(t=1.5\), but the comparison is only geometric in the \((r_k,r_{k+1})\) plane and does not establish any substantive algorithmic insight.  
   Overall, the figures are fine as exploratory visualizations, but they are over-interpreted relative to what they actually demonstrate.

7. **The paper does not sufficiently connect the \(r\)-dynamics to the actual optimization objective.**  
   The scalar \(r_k\) is central throughout the paper, but the paper never establishes why the reported regimes in \(r_k\) imply anything useful for minimizing \(f\). For example, the conclusion says the unstable state may accelerate convergence, but there is no theorem or experiment showing faster decrease in \(f(x_k)-f(x^\*)\), improved spectral filtering, or better dependence on condition number.  
   This gap matters scientifically. A paper on optimization cannot stop at an interesting internal statistic unless it shows that this statistic predicts or improves optimization behavior.

8. **The high-dimensional analysis in Section 3 is largely heuristic and not rigorous enough to support the claims.**  
   In **Equations (32)-(35)**, the argument is that terms involving extreme eigenvalues dominate because the weights \(A(a^{(i)},a^{(j)})\) and \(B(a^{(i)},a^{(j)})\) are larger when eigenvalues are far apart. But moving from that observation to
   \[
   r_k+r_{k+1}\approx a^{(1)}+a^{(n)}
   \]
   in **Equation (35)** is a substantial leap. There is no theorem, no error bound, and no condition specifying when the approximation is valid. The use of **Figure 2** to justify this is not sufficient. A heatmap of \(A(x,y)\) and \(B(x,y)\) does not prove that the actual weighted sums are dominated by extreme-eigenvalue components, because the coefficients \(g_k^{(i)2}g_k^{(j)2}\) also matter and themselves evolve with the method.

9. **The novelty and positioning relative to modern stepsize literature are weak.**  
   The paper cites some older works, but its positioning is incomplete given the actual contribution. Since the manuscript is essentially about spectral/reciprocal-step dynamics on convex quadratics, it should engage more seriously with more recent work on adaptive or Rayleigh-quotient-based stepsizes, spectral gradient methods, and two-dimensional quadratic termination properties. Relevant missing lines of work include recent harmonic/Rayleigh-quotient frameworks for gradient stepsizes, modern analyses of approximately optimal or inexact adaptive stepsizes on strictly convex quadratics, and more recent studies of two-dimensional termination-inspired gradient methods.  
   This matters because the current manuscript presents its scalar-dynamics viewpoint as if it is largely new, but the surrounding literature on spectral step behavior is richer than the paper acknowledges.

10. **The exposition is below ICLR standards for a technical paper.**  
   Beyond local grammar, the more important issue is conceptual clarity. Key definitions are vague or inconsistent: the paper switches between \(s\) and \(t\), calls \(r\) the “reciprocal of optimal steplength” while earlier defining it as \(1/(2\alpha_k)\), and uses terms like “stable orbit,” “chaos motion,” and “strange attractor” without precise definitions. The transition from the matrix form in **Equation (1)** to the diagonal hyper-ellipsoid in **Equation (8)** is also too abrupt; the paper asserts the “same conclusion can be obtained” without actually stating the assumptions needed, such as diagonalization in the eigenbasis.  
   Since the contribution is entirely analytical, the burden on notation and derivation quality is higher than average. Here, the presentation problems directly impair verifiability.

11. **The comparison baselines are underdeveloped and not fairly evaluated.**  
   The introduction mentions Yuan stepsizes, randomized SD, RSDA, and a randomized steepest descent variant, but the experiments only show a qualitative BB comparison in **Figure 7**. There is no empirical comparison against the methods most discussed in the introduction, no quantitative benchmark, and no effort to test whether the proposed \(t\)-scaled SD actually improves convergence relative to exact line search or known alternatives. Without that, the paper’s practical relevance is unclear.

12. **Some claims are simply stronger than what the paper establishes.**  
   The conclusion states that “the function actually describes a chaotic system” and that the unstable state “allows \(r\) to take on arbitrary values.” Neither statement is established by the analysis or experiments. The observed empirical spread of \(r_k\) in **Figure 6(b)** is not evidence that \(r\) can take arbitrary values in any rigorous sense. This kind of overclaiming lowers confidence in the paper’s scientific calibration.

## Questions
1. The first issue the rebuttal must address is the inconsistency between **Equations (11)**, **(13)**, and **(15)**. Which version is correct? Please provide a complete derivation of the \(r_{k+1}\) recurrence starting from \(x_{k+1}=x_k-s\alpha_k^{SD}g_k\), and verify every factor carefully.

2. Relatedly, can the authors clarify **Equation (12)**? From **Equation (4)**, I obtain
   \[
   x_{k+1}=x_k-\frac{1}{2tr_k}g_k,
   \]
   not \(x_k-\frac{1}{tr_k}g_k\). If the paper’s formula is correct under a different definition of \(r_k\), please state that definition explicitly and propagate it consistently through the manuscript.

3. Please provide a corrected derivation of the fixed-point and derivative formulas in **Equations (22)-(31)**, especially **Equation (23)** and **Equation (30)**. If these equations contain mistakes, how do the regime boundaries for \(t<1\), \(t=1\), and \(t>1\) change?

4. What is the precise definition of “chaos” used in this paper? What concrete evidence do the authors have beyond local fixed-point instability and qualitative scatter plots? A rebuttal that included a Lyapunov-exponent calculation, bifurcation diagram, or theorem for the 1D map would substantially increase my confidence.

5. Can the authors show that any of the observed \(r\)-regimes correlate with optimization performance? Specifically, please report \(f(x_k)-f(x^\*)\), \(\|g_k\|\), or iteration counts for several \(t\) values and compare against SD, BB, and at least one nontrivial alternative discussed in the introduction.

6. In Section 3, the claim
   \[
   r_k+r_{k+1}\approx a^{(1)}+a^{(n)}
   \]
   seems heuristic. Can the authors formalize under what assumptions this approximation holds, or provide counterexamples where it fails?

7. Why is the empirical study limited to a single synthetic diagonal quadratic with one eigenvalue schedule? I would like to see whether the claimed behavior persists across condition numbers, eigenvalue distributions, and non-diagonal SPD matrices related by orthogonal change of basis.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No ethics concerns identified from the paper content. The work is a theoretical/numerical study of optimization dynamics on synthetic quadratic problems.

## Soundness Rating
1: poor. The central technical claims are not adequately supported because the core recurrence and several derivative/fixed-point equations appear inconsistent or incorrect, and the empirical evidence is qualitative and insufficient.

## Presentation Rating
1: poor. The manuscript’s organization is understandable at a high level, but the notation, derivations, and claim statements are not clear or reliable enough for a theory-heavy paper.

## Contribution Rating
1: poor. The dynamical viewpoint on \(r_k\) is potentially interesting, but in the current form the contribution is not established with enough correctness, rigor, or empirical value to support publication at ICLR.

## Overall Rating
2: Reject, not good enough. The paper has an interesting intuition, but the current submission has fundamental mathematical inconsistencies at the core of the method, overstates its chaos claims, and provides only weak qualitative experiments. I do not think it is close to ICLR standard in its present form.

## Reviewer Confidence
4: confident. I am confident in the assessment, especially regarding the core algebraic inconsistencies and the mismatch between the strength of the claims and the evidence provided.