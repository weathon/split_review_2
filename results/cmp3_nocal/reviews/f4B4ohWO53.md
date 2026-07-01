## Summary

The paper proposes NVDP (Nonparametric Variational Differential Privacy), which uses a Nonparametric Variational Information Bottleneck (NVIB) layer integrated into a transformer to produce noisy multi-vector embeddings. The authors measure privacy via Rényi divergence and Bayesian Differential Privacy (BDP) computed between learned posterior distributions on test-set pairs, and evaluate on GLUE benchmarks.

## Strengths

- **Clean architectural design.** Using an NVIB layer to produce a posterior over multi-vector embeddings, sampling at test time for stochasticity, and removing residual skip connections to prevent information bypassing the bottleneck are sensible design choices that reflect careful thinking about information flow.
- **Informative NVIB-vs-VIB ablation.** The comparison shows that NVIB-based noise injection (NVDP) provides a better accuracy/privacy tradeoff than a VIB-based variant (VTDP) across multiple GLUE tasks. This validates that the nonparametric formulation adds practical value over a parametric alternative in this setting.

## Weaknesses

### Fatal

**The paper claims to provide differential privacy guarantees but only measures empirical divergence on test-set pairs.** A differentially private mechanism requires a worst-case bound on the divergence between output distributions for *all* adjacent inputs. The paper (a) trains a neural network that maps x to DP parameters (μ,σ²,α), (b) computes Rényi divergences between the resulting learned posterior distributions Q and Q' for specific test-set pairs, and (c) reports these as privacy measures. This is not a DP guarantee—it is an empirical audit on a fixed test set. Nothing bounds the worst-case divergence over all possible inputs, and the learned projection from BERT embeddings to DP parameters has no sensitivity analysis. The paper explicitly states *"We do not assume any specific notion of adjacency between examples"* (line 112), yet Definition 2.2 of RDP requires an adjacency relation. Without one, the computed divergences are pairwise distances, not RDP values. The title, abstract (*"ensures...strong privacy protection"*), introduction (*"differential privacy guarantees"*), and conclusion (*"strong privacy guarantees"*) all make claims the method cannot support. This is not fixable by additional experiments—it requires fundamentally different framing or theoretical analysis.

### Major

- **No comparison with any existing DP method or simple noise baseline.** The baselines are vanilla BERT, BERT+Dropout+WeightDecay (both non-private), and the authors' own VIB-based ablation (VTDP). There is no comparison with DP-SGD, calibrated Gaussian noise added to embeddings, or any established DP technique. Without such comparisons, the paper cannot substantiate the claim that NVDP provides a useful privacy-utility tradeoff relative to existing approaches. The comparison only shows NVIB beats VIB in this specific noise-injection setup.

- **Best-of-5 selection inflates reported accuracy and obscures variance.** The protocol selects the single best run out of five for final reporting (line 182). This systematically overestimates expected accuracy and distorts the reported privacy-utility frontier. Standard practice is to report mean ± std across runs.

- **The reported privacy numbers (ε_μ = 10.70–20.93) are inconsistent with claims of "strong, practical privacy budgets."** In the DP literature, ε < 1 is strong, ε ~ 8 is weak, and ε > 10 offers minimal meaningful protection. Even taking the paper's numbers at face value, the claims of "strong privacy" are unsupported. (The RD values of 0.19–1.66 are lower but do not correspond to calibrated (ε,δ)-DP bounds.)

### Minor

- **The BDP conversion uses test-set pairs rather than proper sampling from the data distribution as Definition 2.3 requires.** The BDP definition requires integrating over x' ~ X (the data distribution), but the paper reports divergence aggregated over test-set pairs and does not justify why this adequately approximates the required distribution.

- **Padding tokens contribute fixed amounts to the RD calculation without analysis of their effect.** Padding tokens are assigned (μ=0, σ=1, α=0), which contributes a fixed term to the RD regardless of text content. The potential distortion of reported privacy numbers from this treatment is not discussed.

- **No variance or confidence intervals reported for any result.** Combined with the best-of-5 selection, the reader cannot assess whether observed gaps between methods are real or within noise.

### Trivial

None.

## Nice-to-Haves

- A discussion of computational cost of the NVIB layer at inference relative to baselines.
- Comparison with a simple calibrated-Gaussian-noise baseline.

## Removed Points

These points from the input review were removed after verification against the paper:

- *"No formal DP analysis or proof"* → Absorbed into the Fatal weakness (it is a consequence, not a separate claim).
- *"The paper does not discuss the gap between measuring Rényi divergence and satisfying DP"* → Absorbed into the Fatal weakness.
- *"No discussion of computational cost"* → Moved to Nice-to-Haves (useful but not a core flaw).
- *"The BDP conversion from RD is referenced to Triastcyn & Faltings (2020) but not explained"* → The paper explicitly says "we refer the reader to the original work" (line 63); this is standard practice, not a weakness.
- Criticisms about the RD formula's ordering assumption → The paper explicitly acknowledges this gives an upper bound (lines 130–131); the padding concern is retained as Minor above.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's architectural novelty and the informative NVIB-vs-VIB ablation, but the central framing problem is decisive and well-documented.

## Suggestions

1. **Reframe honestly.** Drop all claims of providing "differential privacy guarantees." What the paper demonstrates is that NVIB-based noise injection reduces information leakage in transformer embeddings (measured via empirical Rényi divergence) more effectively than a VIB-based alternative. This is a legitimate empirical contribution.
2. **Report mean ± std** over multiple runs instead of best-of-5 selection.
3. **Add simple baselines** (e.g., calibrated Gaussian noise added to embeddings, with the same empirical divergence measurements) to contextualize the privacy-utility tradeoffs.
4. **Acknowledge limitations** of the empirical divergence measurement approach explicitly.

## Score and Decision

Score: 3. Decision: Reject.

The paper has a clear, verifiable fatal framing issue: it claims to provide differential privacy guarantees but provides only empirical divergence measurements on test-set pairs. This is not a minor overstatement—it is a category error about what the method achieves. The underlying empirical contribution (NVIB > VIB for information leakage reduction) is modest and could be viable if honestly reframed, but as submitted the central claim is unsupported.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>