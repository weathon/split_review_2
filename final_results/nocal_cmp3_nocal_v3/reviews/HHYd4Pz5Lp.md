Now let me write the final review.

## Summary

This paper introduces DelRec, the first surrogate gradient learning (SGL) method for training delays in recurrent connections of spiking neural networks. The approach extends differentiable interpolation (used in prior feedforward delay learning) to the recurrent setting via a scheduling matrix with progressive annealing of the spread parameter σ, supporting both axonal (per-neuron) and synaptic (per-synapse) delays. It achieves strong results on SSC and PS-MNIST using only simple LIF neurons.

## Strengths

- **First SGL-based method for learning delays in recurrent SNN connections.** Prior work targets either feedforward connections (DCLS, Deckers et al.) or uses non-SGL approaches (EventProp-based Mészáros et al., softmax-based Xu et al.). DelRec fills a clear gap: adapting differentiable interpolation to recurrent connections. The scheduling matrix and σ-annealing schedule are cleanly implemented and compatible with any spiking neuron model.

- **Well-designed ablation study on SHD (Section 3.2).** The three-phase procedure (validation → simplification → comparative) is methodical. The comparison of six model variants (vanilla SNN, vanilla RSNN, fixed random recurrent delays, learned feedforward delays, learned recurrent delays, combined) in Fig. 3B-C directly targets the role of recurrent delays. The finding that learned recurrent delays outperform all other variants at low parameter counts (Fig. 3C, top) is the paper's strongest evidence.

- **SSC result is credible and moderately incremental.** DelRec (only recurrent delays) achieves 82.58±0.08% on SSC with 0.37M parameters and simple LIF neurons, surpassing SiLIF (82.03±0.25%, 0.35M) and DCLS (80.69±0.21%, 2.5M). The improvement (~0.55pp over SiLIF) is modest but the standard errors are small (3 seeds), and achieving this with *simpler* LIF neurons strengthens the case that recurrent delays are the source of improvement.

## Weaknesses

### Fatal
None.

### Major

1. **The central comparison of recurrent vs. feedforward delays is confounded by parameterization asymmetry.** The paper claims "trainable recurrent delays outperform feedforward ones" (abstract) and builds this on the SHD ablation. Section 3.2 notes: *"we are comparing synaptic feedforward delays (one delay per synapse), with axonal recurrent delays (one delay per neuron)."* An axonal scheme has O(N) delay parameters; a synaptic scheme has O(N²). When total parameter count is matched, the axonal scheme allocates more parameters to weights, so the advantage could reflect a richer weight matrix rather than functional superiority of recurrent delays. The paper acknowledges the asymmetry but does not grapple with its consequences. Without an experiment equating parameterization (e.g., axonal feedforward vs. axonal recurrent delays at identical budgets), this headline claim is not cleanly demonstrated.

2. **The gradient-mitigation claim is asserted but never tested.** The introduction and Figure 1B argue that recurrent delays *"reduce the risks of exploding or vanishing gradients by bridging distant time steps."* This is presented as key motivation. Yet no experimental evidence supports it — no gradient norm analysis, no comparison of training curves, no measurement showing learned delays create skip connections. The only indirect evidence (random fixed recurrent delays outperform vanilla RSNN, Fig. 3B) could be explained by heterogeneity or better temporal alignment. A central motivational claim should be backed by evidence or removed.

3. **PS-MNIST result rests on a single seed with no variance estimate.** The paper reports 96.21% and notes *"we only test one seed as all the previous state-of-the-art models on the dataset."* The improvement over ASRC-SNN (95.77%) is 0.44pp — smaller than the standard deviations reported on SSC (0.08–0.16%). Other papers reporting single-seed results does not make a single-seed result interpretable. The paper should either report multiple seeds or temper the "outperforms SOTA" claim for PS-MNIST.

### Minor

1. **SHD "SOTA" claim is contradicted by own Table 2.** The body text states: *"Whether using both feedforward and recurrent delays or only recurrent delays, our models achieve state-of-the-art performance on SHD."* Table 2 shows DelRec (Rec. and Ff. delays, 93.73±0.69%) behind DCLS (93.77±0.68%) and SE-adLIF (2L, 93.79±0.76%). The paper correctly notes the test set is small and differences above 93% are not statistically significant, and the abstract uses "match the SOTA," which is accurate. The body text overclaims and should be corrected.

2. **No analysis of learned delay values.** The paper learns per-neuron delays but never shows what values they converge to — whether they spread across a range, cluster, or correlate with temporal structure. This analysis would directly support (or undermine) the claim that delays implement temporal skip connections.

3. **No computational cost analysis.** The scheduling matrix overhead scales with σ (at σ=5, each spike spreads over ~12 time steps). The paper mentions a buffer with pointer mechanism but provides no wall-clock time, memory, or scaling analysis. Given the energy-efficiency motivation, even brief discussion would help.

### Trivial
- The conclusion says DelRec *"outperforms the previous SOTA on both the PS-MNIST...and the SSC"* — for PS-MNIST, given the single-seed issue, "outperforms" is too definitive.

## Nice-to-Haves
- **Disentangle the axonal-vs-synaptic confound:** compare axonal recurrent delays against axonal *feedforward* delays (one per neuron) at identical budgets, or implement synaptic recurrent delays vs. synaptic feedforward delays at matched N² budgets.
- **Add multiple seeds for PS-MNIST** (inexpensive) to support the SOTA claim.
- **Test the gradient-mitigation hypothesis or remove it:** a gradient-norm comparison across time for vanilla RSNN vs. DelRec on a synthetic task would settle the question.
- **Include an analysis of learned delay distributions** to show whether delays converge to interpretable values.

## Removed Points
The following points from the input review are removed with justification:

- *SSC/PS-MNIST SOTA should be restricted to LIF-derived models:* The paper already states this scope restriction in the main text ("We deliberately leave out of this table models that rely on substantially more complex neuron models") and provides a footnote listing excluded models. This is transparent and reasonable.
- *Xu et al. positioning clarity:* The paper correctly cites Xu et al. as learning "a single recurrent delay parameter per layer" and distinguishes its own per-neuron, SGL-based approach. The distinction is clear enough in the current text.
- *Algorithm 1 reference missing:* This is a parser artifact (appendix stripped). The substantive point about computational cost analysis is kept above as Minor weakness 3.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- For revision: (1) qualify the SHD claim to "competitive with SOTA" or remove it; (2) add a paragraph acknowledging the axonal-vs-synaptic confound and discussing what can and cannot be concluded from the recurrent-vs-feedforward comparison; (3) run 3+ seeds on PS-MNIST or remove the "outperforms" language; (4) either add a gradient analysis or remove the gradient-mitigation claim from the motivation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>