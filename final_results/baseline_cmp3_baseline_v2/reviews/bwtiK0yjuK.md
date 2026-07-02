## Summary

The paper proposes a two-stage algorithm for offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs). Stage I uses seeded binary segmentation with CUSUM statistics to generate candidate change points; Stage II refines these estimates via low-rank tensor estimation (TH-PCA). The authors establish consistency of the number and locations of change points, derive limiting distributions for the refined estimators under vanishing and non-vanishing jump regimes, and provide a data-driven procedure for constructing confidence intervals. Numerical experiments demonstrate improved performance over existing generic change point detection methods.

## Strengths

- **First work on offline change point detection in dynamic multilayer networks.** The problem is well-motivated and the paper fills a clear gap in the literature, which has focused primarily on single-layer or online settings.  
- **Strong theoretical contributions.** The consistency guarantees and, notably, the derivation of limiting distributions for change point estimators in network data are novel and represent a significant advance beyond existing high-probability bounds.  
- **Well-designed algorithm.** The two-stage approach combining seeded binary segmentation with tensor-based refinement is principled, computationally feasible, and naturally handles the multilayer structure. The use of TH-PCA for low-rank estimation is appropriate.  
- **Extensive and carefully designed experiments.** The simulation covers four scenarios, some violating the model assumptions, demonstrating robustness. The real data analysis on agricultural trade networks yields interpretable change points aligned with known geopolitical events, and confidence intervals are provided.  
- **Practical utility.** The confidence interval construction (Section 3.1) gives practitioners a way to quantify uncertainty, which is rare in network change point analysis.

## Weaknesses

### Fatal
None.

### Major
- **The confidence interval evaluation raises concerns.** For Scenario 1 with \(n=100\), the reported 95% confidence interval average length is 0.003 on a time grid of length \(T=200\). This essentially covers a single integer point, yet coverage is 100%. Such extreme narrowness suggests either the variance estimator is systematically too small, the simulated limiting distribution is not properly scaled, or the jump size \(\kappa_k\) is so large that the estimator is essentially exact. While a large \(\kappa\) can produce tiny intervals, the coverage result then becomes trivial because the estimator always lands on the true change point. The paper should clarify whether these intervals are useful in practice (e.g., do they ever exclude a neighboring time point?), and discuss the role of the jump size in interval length.  
- **Gap between theoretical assumptions and practical implementation.** The theory requires four mutually independent tensor sequences, but the experiments (and presumably any application) use odd-even splitting of two sequences. The paper does not discuss whether this degrades the theoretical guarantees (e.g., the independence used in the proofs is stronger than the splitting design). A brief justification or reference to analogous practice in related work would be helpful.

### Minor
- **Assumption \(\Delta = \Theta(T)\) is restrictive.** It implicitly bounds the number of change points \(K\) to be constant or at most \(O(1)\). The paper notes this can be relaxed but does not provide concrete results or simulations with more frequent changes. Given that real-world networks may exhibit many change points over a long horizon, the practical reach of the current theory is limited.  
- **The model assumes fixed latent positions with only weight matrices changing.** While the paper mentions an extension in Appendix C (not available in the main text), this assumption is central to identifiability and the theoretical analysis. It would strengthen the paper to discuss how violations (e.g., evolving node attributes) affect the method’s robustness, extending the empirical robustness already shown in Scenarios 2 and 3.  
- **Comparison to existing network-specific methods is limited.** The main competitors (gSeg, kerSeg) are generic change point methods, not designed for networks. The paper references online methods and deep-learning baselines in the appendix, but these are not shown in the main table. A brief summary of how the proposed method compares to the closest network-based offline method (e.g., Padilla et al. 2022, which handles single-layer RDPGs) would place the contribution more clearly.

### Trivial
- None beyond the parser-induced formatting issues.

## Nice-to-Haves

- A sensitivity analysis regarding the rank selection in TH-PCA (currently fixed to \(r_1=r_2=15\)) over a wider range would strengthen the practical guidance.  
- The paper could include a discussion of computational cost breakdown to help practitioners anticipate runtime for large \(T,n,L\).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the confidence interval construction.** Explain why intervals can be sub-unit length and how the jump size \(\kappa_k\) affects coverage and length. Provide a simulation where the true change point is not exactly hit, to demonstrate that the interval genuinely captures it with good coverage rather than trivially covering the point estimate.  
2. **Address the independence gap.** Add a brief remark on why the odd-even splitting satisfies the independence condition approximately in practice, and whether the theoretical rates degrade under the splitting design.  
3. **Provide guidance on parameter choice.** The threshold \(\tau\) and rank inputs are crucial; a simple rule-of-thumb or a sensitivity plot over a range would increase practical usability.

## Score and Decision

The paper makes a solid theoretical and methodological contribution to a timely problem. The weaknesses are not fatal and mostly relate to clarity and practical scope rather than correctness. I recommend acceptance.

**MY FINAL SCORE:** <score>8</score>  
**MY FINAL DECISION:** <decision>Accept</decision>