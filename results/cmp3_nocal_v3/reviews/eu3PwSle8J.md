## Summary

This paper addresses indirect prompt injection vulnerabilities in LLMs by proposing Augmented Intermediate Representations (AIR), a method that injects instruction hierarchy (IH) signals into every decoder layer rather than at only the input layer. Prior defenses (Delimiters, Instructional Segment Embedding) add IH information solely at the input, and the paper provides empirical evidence (Figure 3) that these signals degrade as they propagate through the network. AIR adds a small trainable embedding table per layer (0.4M parameters for an 8B model), yielding multi-factor reductions in attack success rate against gradient-based attacks while maintaining utility.

## Strengths

- **Well-motivated architectural insight with direct mechanistic evidence.** The paper identifies that input-only IH signals degrade through the network, and Figure 3 provides concrete cosine-similarity measurements showing this degradation. This motivates the core proposal cleanly and independently from the final ASR results.

- **Consistently strong results on gradient-based attacks across multiple settings.** On GCG (momentum-boosted), AIR achieves 4.1% ASR vs. 38% (Delim) and 48.1% (ISE) for Llama-3.2-3B SFT; 22.6% vs. 88% and 36.6% for Qwen-2.5-7B SFT; and similar advantages across nearly all configurations (Table 1). These are multi-factor reductions that are practically meaningful.

- **Thorough evaluation scope.** The paper evaluates across three model sizes (3B, 7B, 8B), two training paradigms (SFT, DPO), two evaluation datasets (AlpacaFarm, SEP), and multiple attack types (static, GCG, Astra). This breadth strengthens the claims considerably.

- **Minimal utility degradation.** Utility (win rate) is maintained or slightly improved with AIR relative to the non-adversarial baseline (Figure 6), addressing the common concern that defenses trade utility for safety.

- **Parameter efficiency.** AIR adds only 0.4M parameters (0.005% increase for an 8B model), making the overhead negligible in practical terms.

## Weaknesses

### Fatal

None.

### Major

- **Parameter capacity confound: the experimental design does not isolate the effect of per-layer injection from increased representational capacity.** AIR adds a separate trainable embedding table per layer: (33 × 3 × 4096) ≈ 0.4M parameters for Llama-3.1-8B. By contrast, ISE adds K × d = 12K parameters, and Delimiters add 2 × d = 8K parameters — AIR has roughly 30–50× more IH-dedicated parameters. The paper's causal claim is that *distributing the IH signal across layers* drives the improvement, but the experiment does not rule out the simpler explanation that the baselines simply have too few parameters dedicated to encoding privilege information. An ablation comparing AIR against an input-level ISE variant with proportionally scaled-up capacity (matched to AIR's total) would be necessary to isolate the effect of per-layer injection. Without this control, the improvement may partly reflect a capacity effect. The paper's own Figure 3 does provide mechanistic evidence that AIR maintains better per-layer separation, which directly supports the architectural claim, but Figure 3 also confounds capacity with distribution.

- **Gradient-based attacks are evaluated at a fixed step budget without convergence analysis, making it unclear whether AIR hardens the model or merely increases attack cost.** GCG is run for 50 (SFT) or 200 (DPO) steps, but loss curves in Figure 7 show AIR's curves are still decreasing at the final step — they have not converged to a floor. Without running attacks to convergence (e.g., 500–1000 steps on a subset) or sweeping over step budgets, it is unclear whether the ASR gap represents a genuine robustness improvement or simply a cost increase that would shrink under longer attacks. The paper frames the result as reduced ASR (which is accurate at the measured step counts), but the broader implication of "improved robustness" would be strengthened by convergence analysis. The different step budgets for SFT (50) vs. DPO (200) models are also not justified.

### Minor

- **Overstated reduction range.** The abstract and conclusion claim "1.6× to 9.2× reduction in attack success rate." The minimum ratio across all GCG configurations in Table 1 is 1.43× (Llama-3.1-8B DPO: ISE=4.0, AIR=2.8 → 4.0/2.8≈1.43×), below the stated 1.6× floor. The range should be corrected (e.g., "up to 9.2×, with reductions as low as 1.4×").

- **Underspecified inference-time determination of privilege levels (k_i).** The paper defines privilege levels by segment (P0 for system/user instructions, P1 for data, P2 for response) and uses delimiter tokens during training, but it does not explicitly state how k_i is determined for each token at inference. While this can be inferred from the segment structure, explicit documentation would aid reproducibility.

### Trivial

None.

## Nice-to-Haves

- **Convergence analysis for GCG.** Running GCG to 500+ steps on a subset of configurations would resolve whether AIR's advantage persists under longer attacks.
- **Parameter-controlled ablation.** A version of ISE with matched parameter capacity (e.g., a larger embedding bank at the input layer) would cleanly isolate the effect of per-layer injection from capacity scaling.
- **Error bars or variance on ASR.** ASR numbers in Table 1 are point estimates; variance over multiple random seeds would strengthen the results, especially given GCG's stochastic nature.
- **Training overhead measurement.** The paper states overhead is "similar to prior works" but provides no wall-clock or FLOPs comparison, which would be useful since AIR requires a separate embedding lookup at each layer.

## Removed Points

- Several section-by-section observations that were generic praise or minor clarifications without substantive criticism were not carried forward as weaknesses.
- The observation about the alignment function A(O,I) being "never operationalized in the experiments" was noted but is acknowledged as a formalism, not a flaw.
- The comment about AIR being used "in combination with" delimiter tokens was already reasonably implicit from the paper's description and is not a weakness.

## Novel Insights

The harsh critic's observation that AIR's design confounds parameter capacity with architectural distribution is a genuinely insightful methodological critique that goes beyond what the paper acknowledges. The critic also rightly notes that the fixed-step GCG evaluation conflates two distinct interpretations (hardness vs. cost), which the paper does not discuss. These are both valuable lenses for interpreting the results.

## Suggestions

1. Add a controlled ablation where an input-level ISE variant is scaled to match AIR's parameter budget, and compare ASR and per-layer cosine similarity. If AIR still outperforms, the per-layer injection thesis is strongly supported; if not, reframe the contribution accordingly.
2. Run GCG to convergence (≥500 steps) on a representative subset of configurations (e.g., one model, both training methods) to determine whether the ASR gap closes or persists.
3. Correct the stated reduction range to accurately reflect the minimum observed ratio (1.43×), or state the range as "up to 9.2×."
4. Explicitly document how k_i is assigned at inference in the final version.

## Score and Decision

<score>7</score>
<decision>Accept</decision>