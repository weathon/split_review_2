## Summary
# Final Review Report

## Summary

This paper presents a comparative study of three neural network architectures—a plain MLP, a residual network with skip connections (called "U-Net-style"), and a two-branch model inspired by DeepONet—for surrogate modeling of hydrogen-oxygen thermal explosion kinetics. The authors generate a synthetic dataset (70,000 trajectories) using a stiff ODE solver across realistic temperature (250-5000 K), pressure (10^4-2×10^7 Pa), and timestep ranges, and compare models under matched training conditions.

The main finding is that the residual MLP (labeled "U-Net") achieves substantially lower mean squared error (MSE 0.0014) than MLP (0.0203) and DeepONet-style (0.0181) models, with narrower confidence intervals and qualitatively better phase alignment on challenging trajectories. This result is credible and practically relevant for surrogate modeling of stiff chemistry.

However, the paper has several significant weaknesses: (1) the "U-Net" naming is inaccurate—the architecture is a residual MLP without any convolutional encoding/decoding, misleading readers about the claimed architectural contribution; (2) key statistical details are missing or inappropriate (no justification for CI computation, skewed error distributions not analyzed with robust statistics); (3) the conclusion overclaims by asserting architecture importance equals dataset-size importance without testing this; and (4) the research question as framed exceeds what the experimental design can answer. Novelty assessment is deferred due to external literature verification being unavailable in this run.

## Strengths
1. **Relevant and practical problem domain.** The paper addresses the important challenge of accelerating stiff chemical kinetics using neural surrogates, which has direct implications for combustion CFD simulations. The choice of hydrogen-oxygen thermal explosion as a test case is well-motivated given its relevance to propulsion and energy systems.

2. **Systematic comparison under matched conditions.** All three architectures are trained with the same optimizer (Adam, lr=0.001), same batch size (5000), same number of epochs (100), and same multi-step loss function. This controlled setup strengthens the internal validity of the comparative finding.

3. **Realistic parameter ranges.** The dataset covers broad ranges of temperature (250–5000 K), pressure (10^4–2×10^7 Pa), and timestep (10^{-10}–10^{-5} s), which span practically relevant combustion regimes including both slow induction and rapid ignition phases.

4. **Qualitative trajectory analysis.** The inclusion of representative low-MSE and high-MSE trajectory plots (Figures 3–4) with visual phase-alignment assessment provides useful insight beyond aggregate MSE numbers. The observation that the residual MLP maintains better phase alignment on challenging cases is a meaningful qualitative finding.

5. **Multi-step training loss.** The use of recursive multi-step prediction (30 steps) during training is a sensible design choice for surrogate models that must be stable over extended rollout horizons, aligning well with the downstream application.

## Weaknesses
### W1. Misleading "U-Net" naming (Severity: Major)
The so-called "U-Net-style residual network" is not a U-Net. Standard U-Net (Ronneberger et al., 2015) is characterized by a convolutional encoder-decoder with spatial downsampling/upsampling and skip connections between corresponding resolution levels. The architecture in this paper is a fully connected residual network with one local skip (expansion → block output) and one global skip (input → output). It has no convolutional layers, no spatial operations, and no multi-resolution feature maps. Calling it "U-Net" or "U-Net-style" throughout the paper (including title, abstract, figures, tables) is misleading and inflates the perceived architectural contribution. This affects how readers interpret the comparative conclusion. *Action:* Rename to "residual MLP (ResMLP)" or "skip-connected feedforward network" throughout.

### W2. Statistical analysis gaps (Severity: Major)
The paper reports mean MSE and standard deviation, but for all three models Std > Mean, indicating heavily right-skewed error distributions. Under these conditions, mean is a poor summary statistic and normal-based confidence intervals are unreliable. The claimed "statistically significant improvement" based on non-overlapping 95% CIs is insufficiently justified. No paired significance test (e.g., Wilcoxon signed-rank or paired t-test on per-trajectory MSE) is reported. No median, percentiles, or win-rate analysis is provided. *Action:* Add (a) median and quartile MSE, (b) per-trajectory win rates, (c) bootstrap or non-parametric significance tests, and (d) clarify how the CIs were computed.

### W3. Unsupported conclusion claims (Severity: Major)
The conclusion states that "the choice of architecture can be as critical as the size or the diversity of the dataset." This claim is not tested—no experiment varies dataset size while holding architecture fixed. Similarly, the abstract and conclusion mention "interpretable" predictive models, but no interpretability analysis is conducted anywhere in the manuscript. *Action:* Remove unsupported comparative claim about dataset size; remove or define "interpretable" if not evaluated.

### W4. Research question vs. design mismatch (Severity: Major)
The paper asks whether "operator-learning architectures such as DeepONet provide superior accuracy compared to hierarchical models (e.g., U-Net-style residual networks)." However, the experimental design compares three specific, non-standard implementations without controlling for parameter count, depth, or training dynamics. The DeepONet-style model deviates substantially from standard DeepONet (no function encoding over sensor points, single-scalar trunk input). The residual MLP is not a hierarchical model in the sense of multi-scale processing. Thus the experiment cannot answer the stated question. *Action:* Narrow the research question to match the actual comparisons, or add controlled experiments (matched parameter count, matched depth).

### W5. Equation (1) notation error (Severity: Major)
The partial derivative ∂X/∂t is used in Eq. (1) for a system that has no spatial coupling (each cell solved independently). The correct notation for a purely temporal ODE is dX/dt. While this may seem minor, it signals a gap between the PDE-level framing and the actual zero-dimensional modeling approach. *Action:* Replace ∂/∂t with d/dt and add a clarifying sentence about the cell-wise independent ODE treatment.

### W6. Loss function weighting not justified (Severity: Major)
Equation (4) uses 1/k weighting in the multi-step loss, which de-emphasizes longer-horizon predictions. The text claims this "encourages the models to account for error accumulation," but lower-weighting on later steps actually discourages long-term error minimization. No justification or ablation of this weighting is provided. *Action:* Either justify the 1/k weighting with evidence/citation, or replace with uniform weighting and re-evaluate.

### W7. Unsupported multi-scale attribution (Severity: Major)
The paper attributes U-Net's gains to "multi-scale representation" and "encoder-decoder design with skip connections" without any supporting evidence (e.g., representation analysis, feature visualization, or controlled ablations). For a fully connected residual network, the advantage could equally come from better gradient flow, higher effective capacity, or implicit regularization. *Action:* Either add representation analysis or replace causal attribution with observational language.

### W8. Dataset generation details missing (Severity: Minor)
The sampling strategy over (T, p, Δt) space is not described (uniform vs. log-uniform vs. Latin hypercube). The split ratio (71%/21%/7%) is unusual and not justified. The relationship between the 70,000 samples and the 30-step rollout trajectories is unclear (independent trajectories vs. overlapping windows). *Action:* Add detailed sampling methodology, clarify trajectory structure relative to training examples, and justify the split ratio.

### W9. Minor writing and grammar issues (Severity: Minor)
- Incomplete comparative structure in the Introduction: "exert a profound influence on both the stability of predictions" (missing "and" completion).
- "teh" typo appears in extracted text.
- The abstract's "Despite testing various architectures ... the problem remains unresolved" is candid but undermines the paper's contribution framing.

### Novelty Assessment (Deferred)
Due to external literature search being unavailable in this run, novelty and related-work completeness judgments are deferred for manual verification. Key questions that require verification: (1) whether residual MLPs have been previously applied to combustion kinetics surrogate modeling, (2) whether the specific comparison with DeepONet for stiff chemistry has been reported, and (3) whether the dataset generation methodology matches or advances prior work.

## Score
**Final Score: 5.5/10**

The paper addresses a practically relevant problem and presents a controlled comparative evaluation that yields a credible core finding (residual skip connections improve surrogate accuracy for stiff chemistry). However, the score is reduced by:

- **Misleading architectural naming** (the "U-Net" is a residual MLP, not a U-Net), which inflates the perceived contribution and undermines technical precision throughout the paper.
- **Incomplete statistical reporting** (no median/quantile analysis despite Std > Mean, no explicit significance test, CI computation method unspecified).
- **Unsupported conclusion claims** (architecture vs. dataset importance not tested; "interpretable" claim not validated).
- **Research question–design mismatch** (the framing asks about operator-learning vs. hierarchical models, but the experiments compare three specific non-standard implementations).
- **Deferred novelty verification** (external literature comparison unavailable in this run limits assessment of contribution novelty).

The empirical comparison has genuine value for the combustion surrogate modeling community, but the paper requires substantial revision in statistical rigor, architectural naming, and scope of claims before it meets a higher publication standard.