## Summary

This paper develops a unified theoretical framework for saddle-to-saddle dynamics and simplicity bias across neural network architectures (fully-connected, convolutional, attention). The authors establish three key results: (1) embedded fixed points forming a nested saddle hierarchy (Theorem 1, extending Fukumizu & Amari to convolutional and attention architectures with new constructions), (2) invariant manifolds connecting these saddles that effectively reduce network width (Theorem 3), and (3) two distinct timescale-separation mechanisms — data-induced for linear activations (Theorem 4, producing low-rank weights) and initialization-induced for quadratic activations (Proposition 5, producing sparse weights). The theory is validated on small-scale simulations and yields testable predictions about width, data distribution, and initialization effects on learning dynamics.

## Strengths

- **Theorem 1 extends the classic Fukumizu & Amari (2000) embedded-fixed-point result with genuinely new constructions (Eqs. 6–7) for homogeneous and linear activations.** Remark 1 correctly observes that these new constructions — not the original ones — correspond to the saddles actually visited during training, making the extension necessary for the dynamical analysis, not incremental.

- **Theorem 3 establishes invariant manifolds that connect embedded fixed points, providing a concrete dynamical pathway for saddle-to-saddle transitions.** This goes beyond the static fixed-point analysis in prior work by showing that gradient flow can move a network from effective width *h* to effective width *(h+1)* along a constrained trajectory (lines 118–119, Appendix F.4).

- **The paper cleanly disentangles two distinct timescale-separation mechanisms — data-induced (via singular-value gaps in the input-output correlation) and initialization-induced (via a rich-get-richer process) — and ties each to a different weight structure (low-rank vs. sparse).** This dichotomy is not present in prior unified accounts and generates testable, architecture-specific predictions.

- **Testable predictions are stated clearly and verified in simulations: width affects plateaus in quadratic-activation (self-attention) networks but not in linear networks (Figure 2A); equal singular values eliminate plateaus in linear networks but not in quadratic networks (Figure 2B); large low-rank initialization produces saddle-to-saddle dynamics without an initial plateau (Figure 2C).**

- **Section 7 explicitly states two necessary conditions for saddle-to-saddle dynamics and provides concrete counterexamples (tanh networks violating condition i, large random initialization violating condition ii), making the theory falsifiable rather than a universal claim that always trivially holds.**

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The abstract and introduction frame the contribution as applying uniformly to "linear networks, ReLU networks, convolutional networks, quadratic networks, and linear self-attention," but the rigorous dynamical analysis (Theorem 4, Proposition 5) covers only the linear and quadratic activation cases.** For ReLU and convolutional networks, the paper provides structural results (Theorems 1, 3) and empirical evidence (Figure 1D,E) but no analytical proof of the timescale separation that drives the dynamics. The paper explicitly acknowledges this scope in Section 5 ("To analyze learning dynamics, however, we must work with concrete architectures," line 121–122), so this is not a structural flaw, but the framing conflates analytical proof with empirical demonstration. The contribution would be more precisely described as (i) general structural prerequisites, (ii) rigorous dynamical analysis for linear/quadratic cases, (iii) empirical evidence for extension to ReLU/convolutional networks.

- **The quadratic-case dynamical analysis (Section 5.2) builds intuition via a scalar simplification** (Eq. 15: $\dot{v}_i = v_i^2$), but the full dynamics (Eq. 14) involves coupling through $\Sigma_{yZ}$, which is more complex. The paper acknowledges that the general case is deferred to Appendix H.2, but a reader may reasonably question whether the scalar caricature captures the essential mechanism or omits critical interactions. The gap between the simple intuition and the full coupled dynamics is not bridged in the main text.

- **The notion of simplicity is defined relative to each architecture's own building blocks** (number of hidden neurons, kernels, or attention heads). While internally coherent and standard in the literature, the paper does not connect this definition to independent complexity measures (VC dimension, Rademacher complexity, approximation-theoretic metrics). The claim that earlier stages are "simpler" would be strengthened by such a connection, even if only as a brief discussion.

- **The paper uses gradient flow throughout but validates its predictions with discrete-step gradient descent (Figure 2).** A brief discussion of whether finite-step discretization effects could disrupt the invariant manifold structure would strengthen the connection between theory and experiments, especially since gradient descent can leave invariant manifolds that gradient flow preserves.

### Trivial
None.

## Nice-to-Haves

- A ReLU-specific dynamical analysis (even a heuristic argument about ReLU near zero behaving like the linear case, and how the dead-neuron regime differs) would bridge the gap between the structural results and the advertised architectural coverage.
- Quantified scaling laws for plateau durations (e.g., "plateau duration scales as ~1/(s_k − s_{k+1}) for linear networks" or "~1/log(v_max/v_second) for quadratic networks") would sharpen the connection between theory and experiment.
- A discussion of mixed cases where both data-induced and initialization-induced mechanisms interact (real architectures like transformers have both linear and quadratic components).

## Removed Points

These points from the reviewer inputs were removed or downgraded after cross-checking against the paper:

- **"Evidence for predictions is qualitative and uses toy data"** (Harsh Critic, Critical Issue 3). Removed because for a theoretical paper, toy-data validation is standard and sufficient; the critic themselves acknowledges "For a theoretical paper, this level of validation is acceptable." The predictions are conceptual, not quantitative scaling laws.
- **"Missing discussion of the rank-1-first phenomenon"** (Harsh Critic, Section-by-Section). The paper already discusses subsequent iterations extensively (lines 152–158, Appendix G.3) and explains the recursive mechanism via a projected covariance matrix. The connection is adequately made.
- **"Gradient descent vs. gradient flow is a critical issue"** (Harsh Critic, Missing Parts). Downgraded to Minor since the paper acknowledges this ("Gradient flow captures the behavior of gradient descent in the limit of a small learning rate," line 53) and it is standard practice in theory papers to analyze gradient flow and validate with GD.
- **Generic/superficial strengths from the Strength Finder** (e.g., "this paper addressed an important problem") were removed per the filtering instructions. Only concrete, evidence-grounded strengths are retained.
- **"The key distinction between data-induced and initialization-induced timescale separation could be sharpened"** — moved to Nice-to-Haves as a suggestion rather than a weakness, since the paper does clearly make the distinction; the critic's request for a discussion of mixed cases is scope-extension.
- **Claims about missing appendix/references** — removed per instructions: these sections exist in the original submission but were stripped by the parsing system.

## Novel Insights

The most interesting synthetic observation across the reviews is that the paper's two timescale-separation mechanisms (data-induced vs. initialization-induced) map directly onto two different "simplicity" notions (low-rank vs. sparse) and two different architectural classes. This means the framework does not just unify existing observations — it generates *differential predictions* that distinguish between architectures (e.g., width helps quadratic/self-attention networks but not linear ones). The paper's explicit statement of necessary conditions for saddle-to-saddle dynamics (Section 7) and its honest counterexamples (tanh, large random init) are a methodological strength that many theoretical papers omit.

## Suggestions

1. In the abstract and introduction, replace "we show that ReLU networks learn solutions with an increasing number of kinks" with more precise language distinguishing analytical results from empirical demonstrations (e.g., "we prove analytically for linear/quadratic activations and demonstrate empirically for ReLU/convolutional architectures").
2. Add a brief ReLU-specific discussion to Section 5 or Section 7, even if only heuristic: why ReLU near small initialization behaves similarly to the linear case via Taylor expansion, and why the dead-neuron regime does not break the mechanism.
3. Provide approximate scaling laws for plateau durations in the main text to sharpen the connection between theory and experiment.

---

### Calibration Notes

**Round 1 — Bracketing (wide pass):** 6 queries covering score bands (-∞,1.5], (1.5,3.5], (3.5,5.5], (5.5,7.5], (7.5,8.5], (8.5,∞). No results in the top band. Key anchors:
- Papers scoring 1.0–1.4: fundamental flaws or nonsensical content — not comparable.
- Papers scoring 2.5–3.4: weak or flawed papers (e.g., "Simplicity Bias in Overparameterized Machine Learning" at 3.00, "Understanding Gradient Descent through the Training Jacobian" at 3.40) — the current paper is clearly stronger.
- Papers scoring 4.0–5.0: moderate quality, mostly rejected (e.g., "A simple connection from loss flatness to compressed representations" at 5.00, Reject) — current paper is significantly stronger.
- Papers scoring 6.0–7.33: **most comparable** (e.g., "Dichotomy of Early and Late Phase Implicit Biases Can Provably Induce Grokking" at 6.00, Accept; "Analyzing Neural Scaling Laws in Two-Layer Networks with Power-Law Data Spectra" at 7.33, Accept; "Simplicity Bias of SGD via Sharpness Minimization" at 6.00, Reject due to restrictive assumptions).
- Papers scoring 8.0: deeper and more complete analysis (e.g., "Exploring The Loss Landscape Of Regularized Neural Networks Via Convex Duality" at 8.00) — current paper falls short of this level due to the framing/scope gap and incomplete dynamical coverage for some architectures.

**Round 2 — Narrowing pass:** 1 query in (6.5,7.5] returned "Generalization of Scaled Deep ResNets in the Mean-Field Regime" (7.00, Accept), "Implicit regularization of deep residual networks towards neural ODEs" (7.00, Accept), and "Sharper Guarantees for Learning Neural Network Classifiers with Gradient Methods" (7.00, Accept), confirming that 7.0 is the calibration anchor for papers with solid contributions but non-trivial caveats.

**Final bracket:** [6.5, 7.5] → narrowed to 7.0.

**Final Score:** 7.0 — this paper has significant theoretical contributions (Theorems 1, 3, 4, Proposition 5), a genuine unified framework, and clear testable predictions. Its main limitations (framing overreach in the abstract, dynamical analysis only for linear/quadratic, toy-data validation) are addressable and do not undermine the core results. This places it solidly in the Accept range, comparable to other accepted theory papers at ICLR.

---

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>