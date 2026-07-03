**Round 1 bracket: 4.0–5.5**

Based on calibration anchors, the paper sits closest to borderline-reject territory. The methodological contributions are real (sjPCA, temporal kernel, constrained optimization), but the core evaluation claim—that the adaptive stimulus-response estimator handles biological complexity—is undermined by using purely synthetic AR stimulation overlays on real data, with no comparison to any prior adaptive stimulation method. Papers like interventional SSM (FwW3jqchtY, avg 5.0, Reject) and the closed-loop EEG stimulation framework (4ltiMYgJo9, avg 5.75, Reject) show the neighborhood for similar systems neuroscience engineering submissions with incomplete evaluation. Settling on **4.0**.

---

## Summary
This paper presents a real-time adaptive framework for designing neural stimulations that drive latent population dynamics along user-specified directions. The contributions include sjPCA (a streaming jPCA variant with Orthogonal Procrustes stabilization), a nonparametric kernel regression stimulus-response model (Eq. 7) with adaptive temporal discounting, a constrained differentiable optimization for high-dimensional stimulation design (Eq. 8), and a parallel streaming model-selection mechanism across competing latent representations. The system achieves sub-10 ms end-to-end latency and is tested on both simulated and real neural data (calcium imaging, electrophysiology).

---

## Strengths
- **sjPCA with Procrustes plane-stabilization (Section 2.1, Eq. 2)**: A principled, concrete improvement over naive streaming jPCA. Figure 1a confirms convergence to the offline fit on par with proSVD, which is non-trivial given jPCA's eigendecomposition step.
- **Realistic feasibility constraints (Eq. 8, Section 2.4)**: The optimization directly encodes non-negativity (excitation-only optogenetics), sparsity (limited simultaneous targets), and magnitude bounds—constraints that reflect real holographic photostimulation hardware. The paper demonstrates these coherently, e.g., correctly predicting that inhibition-targeted stimulations are infeasible (Fig. 4a 'Negative').
- **Adaptive temporal kernel (Eq. 7, Section 2.3, Fig. 2e)**: K3 with stochastic coordinate-descent length-scale tuning allows the model to recover from both jump discontinuities ('Flip') and continuous drift ('Rotate'). Recovery is demonstrated cleanly against a blind baseline.
- **Runtime credibility (Section 3)**: Hardware is fully specified (Intel i9, 3060 Ti, Ubuntu 22.04) and sub-10 ms average end-to-end times are reported, making real-time feasibility claims verifiable.

---

## Weaknesses

### Fatal
None.

### Major
- **Synthetic stimulations on all real data (Section 4.1)**: Every real-data experiment—both calcium imaging and electrophysiology—uses a linear AR model to simulate stimulation: `y_t = r_t + a_t`, `a_t = 0.8·a_{t-1} + u_t`. This is linear, time-invariant, spatially uniform, and trivially learnable by any regressor. The biological complexity the paper is designed to address (nonlinear, state-dependent, opsin-heterogeneous responses) is entirely absent from the real-data experiments. The paper therefore demonstrates that the framework *runs correctly* on real background dynamics with a synthetic overlay—not that the stimulus-response estimator captures genuine biological variability. The Discussion (Section 5) acknowledges offline testing but does not acknowledge this more consequential synthetic-stimulation limitation.

- **No comparison to any prior adaptive stimulation method**: The sole comparison throughout is against a "blind" dynamical model that ignores stimulation times (Figs. 2e, 3c, 5a). This sanity check confirms that knowing *when* stimulations occurred helps prediction—an unsurprising result. The paper explicitly cites Bayesian optimization (Minai et al., 2024) and active learning (Wagenmaker et al., 2024) as related methods on the same problem; none appear as baselines even on the toy model. Without this, the claim that the proposed kernel regression and constrained optimization outperforms alternatives is unsubstantiated.

### Minor
- **K2 stimulus kernel not exercised in any non-trivial regime**: Eq. 7 includes K2(u, Ui) to distinguish responses to different high-dimensional stimulation patterns—the key kernel for holographic optogenetics where distinct spatial neuron subsets evoke different latent perturbations. In the toy model (Eq. 9), u is binary and the response depends only on latent state; in the real-data experiments, the AR overlay adds uniformly regardless of which neurons are targeted. The capacity of the estimator to learn a u-dependent mapping is never tested in a regime where it would actually be needed.

- **mmICA convergence not discussed (Fig. 1a)**: Figure 1a shows mmICA converges markedly more slowly than proSVD and sjPCA, but the paper provides no guidance on when to prefer it. If convergence is too slow relative to experiment length, the model-selection mechanism (Fig. 1c) would never favor mmICA early on.

- **Streaming model selection lacks quantitative evaluation (Fig. 1c)**: The adaptive representation selection is presented only as a visualization heatmap. A metric comparing adaptive selection to fixed single-model baselines would make this a concrete evaluated contribution rather than a proof-of-concept.

### Trivial
None identified.

---

## Nice-to-Haves
- Testing with actual optogenetic perturbation data (e.g., existing holographic photostimulation datasets like Russell et al. 2024, already cited) would test the K2 kernel and validate the stimulus-response estimator in the biological regime the paper is designed for.
- A more demanding synthetic stimulus-response mapping where different sparse neuron subsets produce systematically different latent perturbations would strengthen the K2 kernel evaluation even within the simulation regime.
- Quantitative comparison of streaming model selection (Fig. 1c) against fixed-representation baselines.
- Explicit acknowledgment in Section 5 that real-data stimulations are synthetic AR overlays, which is the more important limitation than offline testing alone.

---

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Section 4.2 / Fig. 4b angle statistics (predicted vs. observed)**: The reviewer notes the "517/600" figure refers to predicted alignment (s vs v), not observed (s_obs vs v). The paper actually addresses this distinction explicitly—it discusses both and states that "predicted error functions as a loose lower bound on observed error" (Fig. 4c caption, Section 4.2). The paper is transparent here; this is not a hidden flaw.

- **Stimulation sparsity assumption could break in dense-stimulation regimes**: Section 2.3 explicitly states "We assume that a new stimulus is not delivered before we see the effects of a previous stimulus." This is an acknowledged modeling choice, not a concealed flaw.

- **Abstract overstates in vivo applicability**: The abstract says "compatible with future in vivo applications" (emphasis on *future*), and Section 5 explicitly notes "our real data experiments were performed offline." This is appropriate hedging; the criticism is overstated.

- **Missing related-work comparisons**: Per review policy, we do not flag missing related works as we cannot verify their existence from external sources. However, the *baseline* comparison issue (using cited methods as baseline comparisons) is retained above as a Major weakness.

---

## Novel Insights
The most technically clean novel contribution is sjPCA with per-plane Procrustes stabilization—a principled fix to an underappreciated problem in streaming jPCA. The parallel latent-model evaluation mechanism (Fig. 1c) is an elegant system design that allows adaptive representation switching. The most important open question—whether the K2 kernel can learn non-trivial, spatially-structured stimulus-response mappings in real biological preparations—remains the central validation gap. If answered positively with real optogenetic data, the framework would represent a meaningful advance for closed-loop neuroscience.

---

## Suggestions
- Replace the AR stimulation overlay in the real-data experiments with actual optogenetic perturbation data, or at least a simulation that exercises the spatial structure of u (different neuron subsets → different latent perturbations).
- Add one quantitative comparison on the toy model against Bayesian optimization or active learning (both cited) to situate the contribution in the existing landscape.
- Provide a quantitative metric for the streaming model-selection mechanism vs. fixed single-model baselines.
- Acknowledge in Section 5 that real-data stimulations are synthetic linear overlays, not actual biological stimulation responses.

---

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| nSDOkm0SKo.md | 1.0 | R1 | Strong reject anchor, unrelated topic |
| P49gSPmrvN.md | 1.0 | R1 | Strong reject anchor, unrelated |
| fnO5h1CFyh.md | 3.0 | R1 | Neuroscience streaming algorithm, limited baselines |
| BBldjKEBlJ.md | 3.0 | R1 | Neural forecasting, rejected for insufficient evaluation |
| LNp7KW33Cg.md | 5.0 | R1/R2 | BCI domain adaptation, rejected; better baselines than reviewed paper |
| 4AlNpszv66.md | 4.75 | R1 | Neural controllability, mixed scores (3-8), comparable scope |
| 3usdM1AuI3.md | 6.25 | R1 | BRAID—accepted; stronger evaluation with real neural-input modeling |
| WQwV7Y8qwa.md | 5.80 | R1 | Switching SSM, accepted; stronger theoretical grounding |
| wCUw8t63vH.md | 6.80 | R1 | Spectral learning shared dynamics, accepted |
| F5lcN7329a.md | 6.00 | R1 | Flow-based BCI alignment, rejected |
| kbjJ9ZOakb.md | 8.0 | R1 | Neuron invariance manifolds, high-quality accepted |
| 4ltiMYgJo9.md | 5.75 | R2 | Closed-loop EEG stimulation, rejected; most topically similar |
| FwW3jqchtY.md | 5.0 | R2 | Interventional SSM for neural dynamics, rejected |
| TVnkjz4MqV.md | 5.5 | R2 | Neural manifold regularization, rejected |
| eR1119aUlL.md | 4.25 | R2 | Real-time nonlinear neural decoding, rejected; evaluation thin |
| BYUdBlaNqk.md | 5.25 | R2 | Neural system identification, limited baselines, rejected |
| JAnyCnQ5In.md | 4.75 | R2 | Online streaming neuroscience algorithm, rejected |

**Round 1 bracket**: 4.0–5.5, based on topically similar papers being rejected in this range with evaluation gaps comparable to or smaller than the reviewed paper's.

**Round 2 narrowing**: The most topically similar paper (4ltiMYgJo9.md, closed-loop EEG stimulation, 5.75 avg, Rejected) has stronger evaluation than the paper under review—it uses real EEG responses, not synthetic overlays. Papers like FwW3jqchtY (5.0, Reject, interventional SSM) and eR1119aUlL (4.25, Reject, real-time neural decoding) have comparable evaluation depth. The two Major weaknesses here (synthetic-only real-data validation, no competitive baselines) are more serious than what was seen in the 5.5+ bracket. The paper has genuine algorithmic novelty (sjPCA, temporal kernel) but those alone, without validation against the core claim in the regime that matters, does not reach the 5.5 threshold.

**Final score: 4.0 (Borderline Reject)**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>