## Summary
This paper presents two novel algorithms, MadDist and TDMadDist, for learning the Minimum Action Distance (MAD) from state trajectories in MDPs, without requiring reward signals or action labels. The authors propose a novel simple quasimetric distance function and introduce a comprehensive benchmark suite with known ground-truth MAD values. The methods are evaluated across deterministic/stochastic dynamics and discrete/continuous state spaces, demonstrating superior performance over existing quasimetric and Hilbert-space baselines, particularly in asymmetric environments.

## Strengths
- **Strong empirical evaluation with known ground truth**: The paper introduces a well-designed benchmark suite where the exact MAD is known, enabling rigorous quantitative evaluation with Spearman correlation, Pearson correlation, and Ratio CV metrics. This is a significant improvement over prior work that lacks such controlled evaluation.
- **Addresses an important limitation of prior work**: The explicit support for asymmetric quasimetrics is a meaningful contribution, as the true MAD is inherently asymmetric in many realistic environments (e.g., KeyDoorGridWorld, CliffWalking). The paper convincingly demonstrates that symmetric Hilbert-space methods fail to capture this asymmetry.
- **Clean, principled loss formulation**: The scale-invariant loss in MadDist (Equation 5) is a well-motivated improvement over prior approaches, as it prevents state pairs with large temporal distances from dominating the gradient. The combination of direct supervision, contrastive separation, and upper-bound constraints is thoughtfully designed.

## Weaknesses
### Major
- **TDMadDist underperforms MadDist but is presented as a core contribution**: The TD variant consistently underperforms the simpler MadDist across nearly all environments. Given that TDMadDist adds significant complexity (target networks, bootstrapped targets) without empirical benefit, its inclusion as a primary contribution is questionable. The paper would be stronger if it explained why bootstrapping fails to improve results or dropped TDMadDist as a main contribution.
- **Limited comparison to the most relevant prior work**: The paper compares against QRL (Wang et al., 2023b) and a Hilbert-space method (Park et al., 2024b), but does not compare against Steccanella & Jonsson (2022), which is the direct predecessor using symmetric distances with the same trajectory-based supervision. While the motivation for asymmetry is clear, a direct comparison showing how much of the improvement comes from asymmetry vs. the scale-invariant loss vs. other design choices would strengthen the paper.

### Minor
- **The novel simple quasimetric (Equation 3) is not well motivated theoretically**: The paper shows it satisfies the triangle inequality (Appendix B), but does not analyze its properties or limitations compared to IQE or Wide Norm in any depth. Given that the main results use IQE (as implied by the QRL comparison), it is unclear whether the simple quasimetric contributes meaningfully to the empirical results.
- **Evaluation on stochastic environments is limited**: The paper includes NoisyGridWorld with stochastic transitions, but the main figures focus on KeyDoorGridWorld and CliffWalking. The stochastic case is important for understanding the robustness claim, yet receives less attention in the main results.

### Trivial
- Equation (9) appears to have formatting issues ("12(9)") and is difficult to parse.

## Nice-to-Haves
- An analysis of what types of trajectories (e.g., coverage, length distribution) are sufficient for accurate MAD learning would be practically valuable.
- Testing on environments where the MAD and SSP diverge significantly (e.g., low-probability shortcuts) could illuminate the limitations of MAD-based approaches.
- A study of how the learned MAD representations benefit downstream RL sample efficiency, beyond the planning task, would strengthen the value proposition.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Consider whether TDMadDist merits equal billing with MadDist given its weaker empirical performance, or whether it should be presented as a speculative variant with clear limitations.
- Add a comparison to Steccanella & Jonsson (2022) to isolate the benefit of asymmetric loss vs. other improvements.
- Provide a clearer breakdown of which design choices (scale-invariant loss, contrastive loss, quasimetric) contribute most to the performance gap over QRL.

## Score and Decision
The paper presents a solid, well-executed contribution with clear empirical improvements over relevant baselines. The benchmark suite is a valuable resource for the community. However, the core algorithmic novelty is incremental—the main contributions are a careful combination of existing ideas (quasimetric learning, trajectory supervision, scale-invariant loss) rather than a fundamentally new learning paradigm. The inclusion of the underperforming TDMadDist as a main contribution slightly weakens the paper.

Score: 6 (borderline accept)

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>