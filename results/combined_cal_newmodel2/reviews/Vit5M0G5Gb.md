Now I have all the information I need. Let me compile the final review.

## Final Consolidated Review

### Summary of Round 1 Bracket

Based on the calibration anchors retrieved, this paper sits in the **5.5–7.0 range**. The closest comparators are:

- **ZXaocmXc6d** (6.67, Accept) — "From Lazy to Rich": Clean exact solutions for deep linear networks; similarly strong theoretical contribution but limited scope. My paper's major weaknesses (favorability 0.56, 1.75) are more concerning than that anchor's weakest point (-5.42 for limited novelty).
- **J4Dvxv7WnG** (7.00, Accept) — "Deep Matrix Factorization EOS": Very similar weakness profile — overclaiming abstract (favorability 1.57), missing nuance (-0.56), impractical assumptions (0.25). Despite these, scored 7.0 after rebuttal.
- **CQF8mTF7qx** (6.00, Reject) — "Simplicity Bias Sharpness": Real theoretical contribution undermined by unrealistic assumptions (favorability 0.07, 0.57).
- **PvJnX3dwsD** (6.40, Accept) — "Quadratic models catapult": Similar in using quadratic models for dynamics analysis.

My paper's key low-favorability items (0.56 for overclaiming, 1.75 for quadratic analysis gap) are comparable to **J4Dvxv7WnG**'s lowest items (1.57, -0.56, 0.25) — that paper scored 7.0 but had stronger experiments and more focused analysis. My paper's strengths (favorability 11–15) are stronger than CQF8mTF7qx (6.0), suggesting the paper is above pure reject territory. Placing inside the bracket: the paper's structural overclaiming and quadratic analysis gap prevent it from reaching the 6.5–7.0 range, but the genuinely novel theoretical infrastructure (Sections 3–4) keeps it above 5.0.

---

## Summary

The paper develops a theoretical framework for understanding saddle-to-saddle learning dynamics as a unifying explanation for simplicity bias across neural network architectures. It contributes (i) a general infrastructure of embedded fixed points (Theorem 1) and invariant manifolds (Theorem 3) spanning linear, ReLU, convolutional, quadratic, and linear self-attention networks, (ii) two distinct dynamical mechanisms for saddle-to-saddle transitions (data-driven timescale separation for linear φ, initialization-driven for quadratic φ), and (iii) concrete predictions validated in small-scale experiments.

## Strengths

- **Genuinely unifying theoretical infrastructure (Sections 3–4).** The paper identifies embedded fixed points (Theorem 1) and invariant manifolds (Theorem 3) that span linear networks, ReLU networks, convolutional networks, quadratic networks, and linear self-attention under a single framework (Equation 1). This synthesis is a real contribution that goes beyond prior work (Fukumizu & Amari, 2000) by extending the analysis to convolutions and attention, and by adding invariant manifolds. The mathematical formulation elegantly unifies diverse architectures into a common template.

- **Novel distinction between data-driven and initialization-driven timescale separation (Section 5).** The paper cleanly separates two mechanisms—singular value spectrum of Σ_yz for linear networks (Theorem 4) vs. spread of random initial weights for quadratic networks (Proposition 5)—and shows they lead to distinct, testable predictions (e.g., width scaling helps in self-attention but not in linear FC networks, Figure 2A). This distinction is more than a technical detail; it generates architecture-specific predictions.

- **Concrete predictions validated experimentally (Section 6).** Figure 2C (initialization near an invariant manifold but away from saddles still produces saddle-to-saddle dynamics) is a genuinely non-obvious prediction that the theory generates and the experiment confirms. This tight theory–experiment coupling is valuable.

## Weaknesses

### Major

1. **The abstract and introduction overclaim the scope of the dynamical analysis.** The abstract states "we show that... ReLU networks learn solutions with an increasing number of kinks" and "convolutional networks learn solutions with an increasing number of convolutional kernels." However, Section 5 explicitly limits the dynamical analysis to "two-layer networks where φ(x; **u**) is a homogeneous polynomial in the weights **u**, studying the linear and quadratic cases in detail" (lines 120–123). The fixed-point and invariant-manifold infrastructure (Sections 3–4) does apply to ReLU and convolutions, but the dynamical mechanism (timescale separation producing saddle-to-saddle transitions) is proven only for linear and quadratic polynomial activations. For ReLU networks and convolutional networks beyond the linear setting, the paper provides empirical demonstration (Figure 1D–E) but not theoretical proof of the dynamics. The abstract does not distinguish between what is proven generally vs. observed empirically. The introduction's framing of a "universal mechanism" (line 27) sets expectations the paper does not fully meet.

2. **The quadratic-case dynamical analysis (Proposition 5) relies on a scalar heuristic in the main text.** Proposition 5 claims timescale separation between units when one unit reaches O(1) and the rest remain O(ε). The main text's intuition uses a scalar equation v̇_i = v_i² (Equations 15–16), but the actual dynamics (Equation 14) couples v_i and **u**_i through Σ_yZ, which is neither scalar nor diagonal in general. The paper states "We provide derivations in Appendix H.2 and the intuition here" (line 178) and asserts "the timescale separation between units essentially comes from the same mechanism" (line 186), but the main text does not bridge the gap between the scalar intuition and the coupled system. Since the appendix is inaccessible for review, this analysis cannot be verified. This weakens the paper's central dynamical claim for the entire quadratic class of architectures.

### Minor

3. **No error bars or variance estimates in experimental results (Figure 2).** Given that the quadratic dynamics depends sensitively on random initialization (Proposition 5), reporting variability across seeds would substantially strengthen the empirical claims. The loss curves are shown as single trajectories without any measure of variance.

4. **Limited engagement with alternative dynamical explanations.** The paper cites Jacot et al. (2018) and Chizat et al. (2019) in passing (in the context of initialization effects, line 13 and line 214) but does not contrast the saddle-to-saddle framework with NTK-based analyses or the rich-vs-lazy learning framework, both of which also predict progressive learning in certain regimes. A discussion of what the saddle-to-saddle framework adds that these alternatives do not capture would strengthen the paper's positioning.

5. **Invariant manifold tracking from random initialization requires a separate dynamical argument.** The paper correctly notes that following an invariant manifold path requires "a carefully chosen small perturbation" (line 118), which Section 5 partially addresses for two specific activation classes. However, this limits the generality of the claimed mechanism for architectures beyond those analyzed, and the paper's Discussion acknowledges this only briefly.

### Trivial

None.

## Nice-to-Haves

- Add error bars or display multiple random seeds in Figure 2's loss curves.
- Provide a proof sketch for Proposition 5 in the main text that addresses the coupling between v_i and **u**_i through Σ_yZ, rather than relying solely on the scalar analogy.
- The small-scale synthetic experiments are appropriate for theory validation but a note on how the predictions might scale would strengthen practical relevance.
- The interesting discussion of permutation symmetry as a deeper unifying principle (Section 7, lines 238–239) could be developed further.

## Removed Points

These points from the input review were removed:

- *"Proposition 5 rests on a heuristic analogy, not a proof"* — Removed because the paper explicitly defers to Appendix H.2 for the full analysis; the scalar analogy is presented as intuition, not as the formal proof. However, the gap between the scalar analogy and the coupled dynamics is a valid concern (retained as Major weakness #2).
- *"Self-attention reformulation limitation"* — Removed because the paper explicitly says "this is not a common notation... we present it solely to show that Equation (1) incorporates self-attention" (line 47).
- *"ReLU differentiability issue"* — Removed because Theorem 1(iii) and Theorem 3(iii) explicitly cover positively homogeneous functions like ReLU.
- *"Invariant manifold insufficiency" (as framed by harsh critic)* — Weakened and retained as Minor weakness #5; the paper acknowledges this gap and Section 5 partially addresses it.
- *Generic strengths about "addressing an important problem"* — Removed as they lack specific content tied to this paper.
- *"Missing related works"* — Removed as I cannot verify what works are missing from external knowledge.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one observation worth highlighting: the paper's clean separation of timescale separation mechanisms (data-driven vs. initialization-driven) and their different architectural implications (width-scaling in self-attention vs. FC linear networks) is a genuinely useful diagnostic that could guide architecture design decisions. This is a stronger meta-contribution than the paper itself emphasizes, and it provides a concrete way for practitioners to reason about which architecture-specific scaling behaviors to expect.

## Suggestions

1. **Revise the abstract and introduction** to clearly distinguish between (a) the universal fixed-point/invariant-manifold infrastructure (proven generally) and (b) the dynamical mechanism for saddle-to-saddle transitions (proven for linear and quadratic polynomial activations, observed empirically for ReLU and convolutional networks). This would make the actual contribution clearer and more defensible.

2. **Provide a proof sketch for Proposition 5** in the main text that addresses the coupling between v_i and **u**_i through Σ_yZ. Even a partial analysis showing the system approximately decouples per unit under certain conditions would substantially strengthen the argument.

3. **Add error bars or multiple-seed displays** to the experimental loss curves (Figure 2) to demonstrate robustness.

4. **Add a brief discussion** of how the saddle-to-saddle framework relates to NTK or rich-vs-lazy analyses of progressive learning, even if only to clarify where the frameworks diverge in predictions.

---

**MY FINAL SCORE:** <score>6.0</score>

**MY FINAL DECISION:** <decision>Accept</decision>