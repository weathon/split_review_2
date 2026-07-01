## Summary

This paper presents a streaming framework for adaptive stimulation and response modeling of latent neural dynamics. The method comprises three components: (1) real-time dimensionality reduction (including a novel streaming jPCA method), (2) nonparametric kernel regression to learn a mapping from stimulation patterns to their effects on latent neural states, and (3) a constrained optimization procedure that designs high-dimensional stimulation vectors to drive latent activity in a desired direction. The authors demonstrate the approach on a toy model and two real neural datasets (calcium imaging and electrophysiology) with simulated stimulation effects, showing that their method can learn stimulus-response mappings quickly and produce stimulations better aligned with target latent directions than random baselines.

## Strengths
- The problem is timely and important: causally testing neural manifold hypotheses via targeted stimulation is a key goal in modern neuroscience, and the paper tackles this with a principled pipeline that combines streaming latent tracking, adaptive response modeling, and optimization under realistic constraints (sparsity, non-negativity).
- The streaming jPCA (sjPCA) method is a novel contribution that extends an important existing dimensionality reduction technique to online settings, with convergence guarantees demonstrated against offline fits.
- The kernel regression framework for the stimulus-response mapping is flexible: it handles non-linearities, sample age (non-stationarity), and multiple latent spaces, which are all critical for real-world experimental conditions.
- The constrained optimization formulation (L1 relaxation for sparsity, box constraints for magnitude) is appropriate for common optogenetic and electrical stimulation hardware limitations.

## Weaknesses
### Fatal
None.

### Major
1. **Real data experiments use simulated, not real, stimulations.** The "stimuli" injected into the calcium and electrophysiology data are synthetic additive signals with an autoregressive target model, not actual optogenetic or electrical perturbations delivered to biological tissue. This significantly weakens the claim that the method is ready for *in vivo* applications—there is no evidence that the kernel regression would generalize to genuine neural responses (which are nonlinear, state-dependent, and often highly variable even for identical stimulation patterns). Without real closed-loop validation, the core contribution remains untested in the regime for which it is intended.

2. **Baseline comparisons are insufficient.** The only comparison models shown are a "blind" dynamics model that ignores stimulation and random stimulation selection (single neurons, groups, shuffled designed stimuli). No existing methods for adaptive stimulation design (e.g., Bayesian optimization [Minai et al., 2024], active learning [Wagenmaker et al., 2024], or other online response modeling approaches [Draelos & Pearson, 2020]) are included. The paper claims to address limitations of prior work but does not quantitatively compare against it, making it difficult to assess whether the proposed framework offers a meaningful improvement.

3. **The streaming jPCA (sjPCA) contribution is under-evaluated.** While sjPCA convergence is shown on simulated data (Figure 1a), its performance is not compared against a baseline online dimensionality reduction method (e.g., incremental PCA or Candid Covariance-Free IPCA) that could also track rotational structure. Furthermore, sjPCA's utility in the stimulation pipeline is not isolated: it is unclear whether using sjPCA rather than proSVD leads to better stimulation design or response modeling outcomes.

4. **Many details essential for reproducibility are missing (even accounting for the missing appendix).** The kernel regression estimator's hyperparameter tuning (RBF length scales, temporal kernel constant) is described only as "optionally tuned by stochastic coordinate descent at each new observation." The delay parameter $d$ is set to 4 timepoints in one experiment but no principled selection method is given. The optimization in Eq. (8) uses the approximation $\|u\|_0^{\max} - \|u\|_1$—how is $\|u\|_0^{\max}$ set? These implementation choices directly affect performance and are not fully specified.

### Minor
- The paper uses a linear dynamical system (Kalman filter) as the primary dynamics model for real data; results with VJF and Bubblewrap are relegated to Appendix C (not visible). It would be helpful to see a direct comparison across dynamics models in the main text.
- Figure 3c shows error for Blind vs Reg models but lacks error bars or confidence intervals; the claim of "significantly lower error" is plausible but not statistically supported.
- The "proportion of magnitude aligned with v" metric (Figure 5b) is introduced without clear definition—what exactly is being plotted? "Proportion of magnitude" could mean the cosine of the angle times the norm ratio, but this needs explanation.

### Trivial
- The term "minimization-maximization" for mmICA appears to be a typo; it should be "majorization-minimization" (which the text correctly states once but then uses the incorrect form elsewhere).
- Some figure labels are difficult to read due to font size (e.g., Figure 1 axis labels, Figure 4 labels in appendix-referenced material).

## Nice-to-Haves
- A comparison against a simple online Gaussian process or linear regression baseline for the stimulus-response mapping would strengthen the argument for the chosen kernel regression method.
- Discussing how the framework could be extended to handle multiple concurrent stimulations (e.g., in a multi-region recording) would broaden its applicability.
- A brief section on failure modes (e.g., what happens if the stimulation-response mapping is highly non-smooth or if the latent space is poorly estimated) would improve practical guidance.

## Novel Insights
The paper's key insight is that high-dimensional stimulation design for latent dynamics can be decomposed into a differentiable mapping from stimulation to latent displacement (learned via kernel regression) and a constrained optimization that exploits differentiability to handle non-trivial stimulus-response relationships. This is a practical engineering contribution rather than a theoretical breakthrough, but the integration of streaming latent estimation, nonparametric response modeling, and constrained optimization in one real-time loop is not present in prior work.

## Suggestions
1. Conduct a proof-of-concept closed-loop experiment using real optogenetic stimulation in a model system (e.g., in vitro or a simple in vivo preparation like zebrafish) to demonstrate that the learned mapping actually transfers to the biological system and that the optimization yields stimulations that drive latent dynamics as intended.
2. Add two baseline comparisons: (a) an open-loop optimization that assumes identity mapping (which the paper mentions) to quantify the benefit of learning $\hat{S}$; (b) a Bayesian optimization approach on a small set of pre-defined stimulation patterns, as in Minai et al. (2024), to compare against existing adaptive methods.
3. Provide a sensitivity analysis showing how the performance (prediction error and angle alignment) varies with the number of observed stimulations, the dimensionality of the latent space, and the noise level in the system.

## Score and Decision
**Score**: 4.0  
**Decision**: Reject

**Reasoning**: The paper proposes a novel and integrated framework for adaptive stimulation of latent neural dynamics, which is an important problem. However, the experimental validation is a critical weakness: all real-data results use simulated stimulations rather than genuine neural perturbations, and the baselines do not include existing methods from the literature. Without evidence that the pipeline works in a real closed-loop setting or at least outperforms simpler alternatives on realistic simulated data, the contribution remains largely conceptual. The streaming jPCA extension is a nice addition but not sufficient to carry the paper over the acceptance threshold.

MY FINAL SCORE: 4.0  
MY FINAL DECISION: Reject