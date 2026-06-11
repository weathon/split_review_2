## Summary
This paper introduces DelRec, a method for learning transmission delays in the recurrent connections of spiking neural networks (SNNs) using surrogate gradient learning (SGL) and backpropagation. The core technical innovation is a differentiable interpolation scheme: real-valued delay parameters are optimized during training via a triangular spreading function that anneals to zero width, converging to integer delays at inference. This allows gradient-based optimization of per-neuron (axonal) delays without predefining a maximum delay range.

DelRec is evaluated on three spiking benchmarks: Spiking Speech Commands (SSC), Permuted Sequential MNIST (PS-MNIST), and Spiking Heidelberg Digits (SHD). Using only simple Leaky-Integrate-and-Fire (LIF) neurons without normalization or data augmentation, DelRec achieves 82.58±0.08% on SSC (outperforming prior LIF-based SOTA of 82.03%) and 96.21% on PS-MNIST. A systematic ablation study on SHD shows that learned recurrent delays consistently outperform fixed or feedforward-only delays under low-parameter regimes.

The paper is clearly written, the method is technically sound, and the ablation study provides useful insights into when recurrent delays are beneficial. However, the SOTA claims require caveating due to selective baseline exclusion, the PS-MNIST result lacks statistical reliability (single seed), and several writing improvements are needed to align claim strength with evidence. Novelty verification is deferred due to external literature search being unavailable in this run.

## Strengths
**1. Clear technical contribution.** DelRec's core method — differentiable interpolation via triangular spreading combined with progressive sigma annealing — is a clean and practical extension of the DCLS framework to recurrent connections. The method removes the need for predefining a maximum delay range, which is a meaningful practical advantage over prior approaches (e.g., Xu et al.'s fixed-set softmax selection).

**2. Strong empirical results on LIF-based models.** Achieving 82.58% on SSC and 96.21% on PS-MNIST using only simple LIF neurons (no adaptive mechanisms, no normalization) is a solid empirical demonstration. The parameter efficiency (0.37M for the best SSC model vs. 2.5M for DCLS) is noteworthy and strengthens the practical motivation.

**3. Systematic ablation study.** The three-phase study on SHD (validation → simplification → comparison) is well-designed and provides clear evidence about the relative benefits of different delay configurations. The comparison of 6 model variants (vanilla SNN, vanilla RSNN, fixed random delays, learned feedforward, learned recurrent, combined) is thorough and yields actionable insights.

**4. Methodological awareness.** The paper correctly identifies the SHD test-set contamination problem, uses a clean validation split, and acknowledges the Bayesian confidence interval overlap for SHD accuracies above 93%. This demonstrates responsible evaluation practices.

**5. Energy-efficiency analysis.** The spike-rate vs. accuracy tradeoff analysis (Fig. 3C) provides a practically useful dimension beyond pure accuracy comparison, acknowledging that different delay types have different energy profiles.

**6. Reproducibility.** The code is provided via an anonymous repository, datasets are publicly available, and hyperparameters are documented in the appendix. This facilitates verification and extension.

## Weaknesses
**W1. Selective SOTA framing and incomplete comparison.** (Severity: Major)

The paper claims "new state-of-the-art" on SSC but excludes models with higher accuracies (e.g., Wang et al. 2024 report 83.69% on SSC) from the comparison table, justified by their use of more complex neuron mechanisms. While comparing within LIF-based models is scientifically valid, the abstract and introduction do not caveat the SOTA claim as restricted to LIF-derived models. This selective framing could mislead readers. The paper should either present a full comparison table with all SNN architectures (with clear annotations on architectural differences) or explicitly bound the SOTA claim to "among LIF-based models" in the abstract and title.

**W2. PS-MNIST result lacks statistical reliability.** (Severity: Major)

The PS-MNIST accuracy of 96.21% is reported from a single seed, with no variance or confidence interval. The paper's own justification — "we only test one seed as all the previous state-of-the-art models on the dataset" — is inconsistent with its criticism of other works for the same practice (Footnote 1). The gap over the closest competitor (ASRC-SNN at 95.77%) is only 0.44 percentage points, which could easily fall within run-to-run variance. Multi-seed evaluation is needed before this result can be considered a reliable SOTA.

**W3. Mathematical error in Eq. (12) — support set definition.** (Severity: Major)

Equation (12) states: "∀τ, h_{σ,d}(τ) = 0 ⇔ τ ∈ supp(h_{σ,d})". This is logically inverted. The support of a function is the set where it is non-zero, not where it is zero. The correct statement should be "h_{σ,d}(τ) > 0 ⇔ τ ∈ supp(h_{σ,d})" or equivalently "h_{σ,d}(τ) = 0 ⇔ τ ∉ supp(h_{σ,d})". While the practical implementation is likely unaffected (the rest of the derivation correctly relies on scheduling within the finite interval), this formal error weakens mathematical rigor and should be corrected.

**W4. Unsupported claims in conclusion and introduction.** (Severity: Major)

The conclusion introduces unsupported claims: "offers new tools for modeling neural populations dynamics in the brain" — no neural data or biologically constrained simulations are presented. Similarly, the abstract's "paving the way for efficient deployment on neuromorphic hardware" is speculative without any hardware evaluation. Several introduction paragraphs use promotional language ("compelling and energy-efficient," "establishes a foundation," "opening new opportunities") without corresponding evidence.

**W5. Motivation-method gap in Introduction.** (Severity: Moderate → Suggestion)

The introduction frames the problem as "vanishing and exploding gradients" in RSNNs, but the proposed solution (learnable recurrent delays) addresses temporal expressivity and routing rather than gradient issues per se. While delays can improve gradient flow via temporal skip connections (Fig. 1B), this mechanism is secondary to the paper's main contribution. The motivation would be stronger if centered on the temporal alignment/routing problem rather than generic gradient difficulties.

**W6. Causal overclaims in ablation analysis.** (Severity: Minor)

Section 3.2 uses "proving that delays... offer an invaluable tool" — the word "proving" is too strong for an empirical comparison with uncontrolled variables. The improvement could come from multiple mechanisms (temporal expressivity, increased effective timesteps, better signal alignment) beyond the stated gradient-mitigation hypothesis. Similarly, the energy-accuracy tradeoff conclusion (feedforward delays as "more energy-efficient alternative") lacks controlled comparison — accuracy and firing rate vary simultaneously across different model architectures.

**W7. Counterintuitive result of combined delays left unexplained.** (Severity: Minor)

On SSC, DelRec with only recurrent delays (82.58%) outperforms the combined recurrent+feedforward variant (82.19%). This pattern also appears in small SHD models. The paper notes this for SHD but does not discuss it for SSC. A plausible explanation (optimization interference, redundancy, overfitting) should be provided, as this finding has practical implications for users deciding which delay types to include.

**W8. Incomplete reference and missing equation cross-reference.** (Severity: Minor)

"Xu et al." is cited without year or full bibliographic details. Additionally, the text references "Eq.15" but the equation is actually labeled (12). These are likely editing artifacts from an earlier draft.

**W9. Limited discussion of training dynamics.** (Severity: Minor → Suggestion)

The sigma annealing schedule is a critical hyperparameter but its sensitivity is not analyzed. The initial sigma value (5) was adopted from DCLS without explanation of why this is appropriate for recurrent connections, which may have different temporal dynamics than feedforward layers. The convergence behavior of the learned delays (do they converge to interpretable patterns?) is also not analyzed.

**W10. Omitted limitation discussion.** (Severity: Minor)

The conclusion does not discuss any limitations of the proposed method. At minimum, limitations should include: (a) axonal vs. synaptic delay granularity tradeoff, (b) sigma annealing schedule tuning, (c) single-seed PS-MNIST result, and (d) lack of hardware evaluation for the claimed neuromorphic deployment pathway.

## Score
**Final Score: 6.5/10**

**Scoring rationale (research value + novelty prioritized):**

- **Novelty (moderate):** DelRec is the first SGL-based method for learning recurrent delays in SNNs, which is a clear but incremental extension of prior feedforward delay methods (DCLS). The differentiable interpolation and progressive sigma annealing are technically sound adaptations of existing techniques rather than fundamentally new algorithmic paradigms.
- **Research value (moderate-high within scope):** The empirical demonstration that recurrent delays outperform feedforward delays under low-parameter regimes is a practically useful finding. The ablation study provides actionable design guidance. However, the SOTA claims are restricted by selective baseline exclusion, and the PS-MNIST result lacks statistical verification.
- **Validity (moderate):** The core method is sound, but the mathematical error in Eq. (12), the single-seed PS-MNIST evaluation, and several instances of causal overclaiming reduce confidence in some presented conclusions.
- **Reproducibility (good):** Code is provided, data are public, and hyperparameters are documented.

**Weaknesses primarily responsible for score:**
1. Selective SOTA framing without caveat in abstract (W1)
2. Single-seed PS-MNIST with no variance (W2)
3. Mathematical error in Eq. (12) support definition (W3)
4. Several unsupported/overclaimed statements (W4, W6)
5. Novelty verification deferred due to external literature unavailability

The paper has solid technical merit and the main finding — that learnable recurrent delays improve temporal processing in simple LIF neurons — is well-supported. However, the presentation inflates claims beyond the evidence, and the statistical rigor is uneven across datasets. Addressing W1-W4 would materially strengthen the paper.