Now I'll write the final consolidated review.

## Summary

DelRec introduces the first surrogate-gradient-learning (SGL) method for learning per-neuron delays in recurrent connections of spiking neural networks. It uses a differentiable triangular interpolation with annealing and a scheduling-matrix buffer to enable gradient-based optimization of real-valued delays that are rounded at inference. The method achieves state-of-the-art accuracy on Spiking Speech Commands (82.58±0.08%, +2% over the best prior LIF+delay method DCLS) and Permuted Sequential MNIST (96.21%), and matches SOTA on the saturated SHD dataset, all using only simple LIF neurons with instantaneous synapses.

## Strengths

- **First SGL-based method for recurrent delays in SNNs.** Prior delay-learning methods either handle only feedforward connections (DCLS: Hammouamri et al., 2024) or rely on EventProp (Mészáros et al., 2025), which limits scalability. DelRec fills this gap with a practical, backpropagation-compatible approach built on SpikingJelly — a genuine methodological contribution.

- **SOTA on SSC with clean multi-seed evidence (3 seeds, 82.58±0.08%).** The improvement over DCLS (80.69±0.21%, the best prior LIF+delay method) is ~2% absolute and well outside standard error. SSC is noted as "far from saturated" (~80% best accuracy), making this the paper's strongest empirical result.

- **Clean attribution using simple LIF neurons.** Many competing approaches (SE-adLIF, SiLIF, Adaptive RSNN) rely on complex neuronal dynamics (adaptive thresholds, resonant dynamics, state-space formulations). By keeping the neuron model simple, the paper cleanly attributes gains to the delay mechanism itself.

- **Well-controlled small-model ablation on SHD (Figure 3B/C).** The systematic comparison of six configurations (~10k-parameter models, varying delay types) shows learned recurrent delays outperforming alternatives under parameter constraints. This is the best-controlled evidence in the paper.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed recurrent-vs-feedforward advantage in the abstract.** The abstract states as a factual finding that "trainable recurrent delays outperform feedforward ones." However, on the full-scale SHD benchmark (Table 2), DCLS (feedforward-only delays, 93.77±0.68%) numerically ties or slightly exceeds DelRec (recurrent-only delays, 93.39±0.45%). The paper acknowledges SHD saturation and that differences above 93% are not statistically significant, so the full-scale comparison is inconclusive rather than contradictory. But the strongest controlled evidence for the claim comes from the small-model ablation (Figure 3C, ~10k parameters), where recurrent delays (~82%) outperform feedforward delays (~80%). The abstract presents a blanket claim that the evidence supports only in a specific regime (under parameter constraints). The conclusion is more careful ("suggesting that recurrent delays can achieve better performance") and should be the standard used throughout.

- **Adding feedforward delays to recurrent delays hurts performance without explanation.** On SSC (Table 1), DelRec with recurrent-only delays scores 82.58±0.08% while adding feedforward delays drops to 82.19±0.16% — a ~0.4% decrease outside standard error. On the small SHD models (Figure 3B), the pattern is even more extreme: the combined model (~75%) substantially underperforms both recurrent-only (~82%) and feedforward-only (~80%). The paper notes "we found no advantage in using both types of delays in these small configurations" but offers no hypothesis for why. This weakens the narrative that feedforward and recurrent delays are complementary and suggests their interaction is not well understood. The paper's framing as "the first to combine" both types is fine, but the lack of analysis of when/why the combination fails is a gap.

### Minor

- **PS-MNIST result lacks variance and uses a restricted comparison set.** The PS-MNIST result (96.21%) is reported from a single seed with no standard deviation. The paper notes that prior SOTA on this dataset also uses single-seed reports, but this does not strengthen the evidence — it merely inherits the same weakness. The improvement over ASRC-SNN (95.77%) is 0.44%, which could fall within run-to-run variance. Additionally, Chen et al. (2024)'s 97.78% result is relegated to a footnote with the critique that it "us[es] the test set as the validation set." This is a legitimate methodological critique, but a reader scanning Table 1 could reasonably conclude DelRec is the absolute SOTA. The paper should make the restriction clearer in the main table.

- **SSC comparison with DCLS uses different architectures, not a controlled ablation.** DelRec uses 3 fully-connected hidden layers (256 neurons each, 0.37M parameters) built on Xu et al.'s codebase, while DCLS uses a different architecture (2.5M parameters). The paper notes this difference but does not run DCLS in the same architecture. The SOTA improvement (82.58% vs 80.69%) is still impressive, but without a same-architecture ablation, the causal attribution to recurrent delays is weakened by architecture and hyperparameter differences.

- **SHD results (Table 2) should more prominently note that DelRec does not outperform DCLS or SE-adLIF on this benchmark.** The paper acknowledges SHD saturation, but a reader may scan the table and misread the "state-of-the-art" claim.

### Trivial

- The paper does not state how delays are initialized (the convention that d=0 gives effective delay of 1 is stated, but not the initial values of d).

## Nice-to-Haves

- Run DCLS in the same 3×256 architecture used for DelRec on SSC to enable a controlled comparison that isolates the contribution of recurrent delays.
- Run PS-MNIST with multiple seeds to provide variance estimates.
- Analyze or hypothesize why combining feedforward and recurrent delays underperforms recurrent-only delays on SSC and small SHD models (e.g., optimization difficulty, overfitting, scheduling matrix becoming too dense).
- Characterize the regimes where each delay type is most beneficial (recurrent delays under parameter constraints vs. feedforward delays at larger scales), which is a more nuanced and informative story than the current blanket framing.

## Removed Points

These points were raised by the harsh reviewer but are excluded from the main review for the following reasons:

- **"The SHD primary evidence criticism"** — The harsh critic states that SHD is used as "primary evidence for the functional superiority of recurrent delays." In fact, the paper's functional study uses the full-scale SHD only as a validation phase (showing DelRec is competitive) and the small-model ablation (Figure 3C) as the controlled evidence for the recurrent-vs-feedforward comparison. The critic slightly mischaracterizes the evidence structure. The broader concern about inconsistent evidence is retained as a Major weakness above.

- **"The exclusion of Chen et al. should be in the table"** — This is a presentation suggestion, not a weakness. The paper is transparent about its exclusion criteria in both the main text and a footnote. Retained as a Minor weakness but with the emphasis on the footnote being easy to miss.

- **Criticisms about missing appendix content** — Removed per hard rules (the parser strips appendices; they exist in the original submission).

- **Pure formatting or presentation nitpicks** — None present in the original review.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reconcile the abstract with the evidence.** Replace the blanket claim "trainable recurrent delays outperform feedforward ones" with a qualified statement such as "we find that under parameter constraints, recurrent delays can outperform feedforward delays" and move the stronger claim to the experimental section where it is supported.

2. **Discuss the combined-model puzzle.** Add a paragraph analyzing why combining feedforward and recurrent delays sometimes hurts performance, even if the analysis is provisional (e.g., noting that in small models the scheduling matrix may become too dense, or that optimization becomes harder with more delay parameters).

3. **Provide multi-seed variance for PS-MNIST** or explicitly note the single-seed limitation in the main table rather than only in the text.

4. **Add delay initialization details** to the method section.

## Score and Decision

Round 1 bracket: [4.5, 6.5] (based on comparison with DeNN at 4.5, Forward Gradient at 5.0, Layer Synchronization at 5.75, Spatio-Temporal Dep. Aware at 5.75, and DeepTAGE at 6.25).

**Anchors considered across all rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| DeNN (pIJR9uPjy3.md) | 4.50 | R1/R2 | Delay SNN paper with major clarity issues; DelRec is much clearer and achieves SOTA |
| SOLO (vq75kRCYuY.md) | 4.00 | R1 | Online SNN learning, comparable performance not SOTA; DelRec achieves SOTA |
| Forward Gradient (yBP36xQhZl.md) | 5.00 | R1/R2 | Forward gradient for SNNs, decent but limited; DelRec has stronger empirical results |
| Temporal Flexibility (RmQAKu1wCe.md) | 5.00 | R2 | Mixed timestep training, limited temporal validation; DelRec has more relevant benchmarks |
| Layer Sync (6iM7mmVhXh.md) | 5.75 | R1/R2 | Async SNN exploration, mixed reviews; DelRec is comparable in quality |
| Spatio-Temporal Dep. Aware (eN4g4cjFX1.md) | 5.75 | R1/R2 | SNN optimization, solid but not compelling enough; DelRec comparable |
| DeepTAGE (drPDukdY3t.md) | 6.25 | R1 | Gradient enhancement for SNNs, clear SOTA, well-received; DelRec slightly weaker due to framing issues |

The paper makes a genuine methodological contribution (first SGL method for recurrent delays) and achieves SOTA on SSC with multi-seed evidence. The main weaknesses — an overclaimed abstract claim about recurrent-vs-feedforward superiority and an unexplained combined-model underperformance — are fixable framing issues rather than fatal methodological flaws. The SSC SOTA, the controlled small-model ablation, and the clean attribution using simple LIF neurons provide real value to the SNN community. Score is calibrated against the above anchors: clearly above DeNN (4.5) and Forward Gradient (5.0) in clarity and empirical strength, comparable to Layer Synchronization (5.75) and Spatio-Temporal Dep. Aware (5.75), but slightly below DeepTAGE (6.25) due to the framing gaps.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>