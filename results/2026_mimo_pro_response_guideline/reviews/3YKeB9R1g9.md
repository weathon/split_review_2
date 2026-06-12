Now I have a clear picture from calibration. Let me finalize my review.

**Anchors summary:**
- "Small-scale proxies for large-scale Transformer training instabilities" (8.00, accepted): More thorough ablations, Google DeepMind team. Our paper has stronger practical applications.
- "u-μP" (7.33, accepted): Focused on parameterization improvement. Our paper is broader in scope.
- "Scaling Law with LR Annealing" (6.75, rejected): Similar topic but weaker practical validation. Our paper has a model family, monitoring, and early stopping.
- "Language models scale reliably" (6.50, accepted): Similar empirical breadth. Our paper has more novel mechanism.
- "Multi-Power Law" (6.00, accepted): Very similar topic, weaker practical grounding.
- "Scaling Optimal LR" (6.00, accepted): Simpler empirical study.
- "Hitchhiker's Guide" (5.20, rejected): Less practical validation.

**Round-1 bracket:** 6.5–7.5. The paper is clearly above the 6.0 papers (stronger practical grounding, model family, real debugging case, theoretical backing) but has gaps that prevent it from reaching 8.0 (no multi-seed, limited scale, narrow early-stopping scope). Given the overall quality, 7.0 seems right.

---

## Summary
This paper extends the training loss curve (TLC) "collapse" phenomenon to practical LLM training, identifying three scale-invariant controls (AdamW timescale τ, tokens-per-parameter ratio, and LR schedule) that govern normalized TLC shape. The authors train the Celerity LLM family (300M–3.9B) at fixed TPP with optimal τ, demonstrating tight collapse, competitive downstream accuracy, and two practical applications: early detection of training pathologies via collapse residuals, and early stopping in hyperparameter tuning via alignment with small-scale reference curves.

## Strengths
- **Real-world debugging case study (Sec. 4, Fig. 1 right, Fig. 6 right):** The paper documents a genuine 1.8B training run where a numerical kernel bug was invisible in unnormalized loss until ~90% of training, but clearly visible as a collapse residual deviation starting at ~60%. The residual also enabled targeted debugging by identifying the microbatch size trigger. This concrete demonstration goes beyond theoretical motivation and validates the monitoring application.

- **Systematic characterization of three scale-invariant controls with theoretical backing (Sec. 3, Figs. 3–4, Eq. 3):** Sweeping η, λ, and B independently shows curves with matching τ exhibit nearly identical shapes regardless of which hyperparameter produced that τ (Fig. 3). TPP's effect is shown to be scale-invariant across 111M–3.3B (Fig. 4). The noisy quadratic model (Eq. 3) provides clean mechanistic explanation linking τ to the bias-variance trade-off, and the scale-invariance argument (curvature factor h cancels after normalization) gives theoretical grounding.

- **Demonstrated early stopping with quantitative results (Sec. 5, Fig. 9):** The 6-step procedure achieves negligible loss gaps when stopping after 10–30% of training for 1.7B and 3.3B models. The parametric surrogate model trained on 111M data (1000× cheaper) produces accurate predictions at 3.3B scale (Fig. 8), demonstrating practical cross-scale transfer.

- **Principled TPP trade-off analysis and competitive model family (Sec. 4, Figs. 2, 5):** The iso-loss compute-compression trade-off analysis justifies the 234 TPP choice (~62% parameter reduction with ~67% compute increase). Celerity models form the accuracy/compute Pareto frontier among open models of their scale, achieving comparable accuracy to BTLm with 75% fewer FLOPs.

## Weaknesses

### Fatal
None.

### Major
- **No inter-run variation reported (Secs. 3–4):** The paper's central claim is precise alignment of training curves, yet no multi-seed experiments are reported. Qiu et al. (2025)'s original "supercollapse" claim specifically relied on curves collapsing to within inter-run noise from different random seeds (line 68: "they *supercollapse*, meaning they differ by less than the noise from inter-run variation"). Without multi-seed data, it is impossible to assess whether visible scatter in collapsed curves (Figs. 1, 6) represents genuine curve mismatch or ordinary seed-to-seed variation. The residual plot (Fig. 1, right) and the claim that residuals provide "early detection" both depend on knowing the baseline noise level. This is the most significant omission for a paper whose central contribution is precisely aligned TLCs.

- **Early stopping application validated only on weight-decay sweeps (Sec. 5):** The early stopping pipeline (Fig. 9) is demonstrated exclusively on λ (weight decay) sweeps at 1.7B and 3.3B. The paper acknowledges at line 224 that fixing τ during batch size sweeps preserves curve ordering (Fig. 7), but does not run the full early-stopping pipeline on learning rate or batch size sweeps — the most consequential hyperparameters in practice. This leaves the most practically valuable use case under-supported.

### Minor
- **Architecture shift between characterization experiments and Celerity (Secs. 3 vs. 4):** Section 3 uses a GPT2-like architecture (SwiGLU, GPT2 vocab, 2048 context, μP) while Celerity uses Squared ReLU, Llama-3 vocab, 8192 context, and CompleteP (Table 2 vs. line 99). The paper does not discuss this gap or whether the architecture choices were necessary for collapse or incidental. Showing collapse persists across both architectures would strengthen generality claims.

- **234 TPP band shows late-training divergence (Sec. 4):** At the most-emphasized TPP band, "divergences appear late in training for larger models" (line 202), with loss improving disproportionately on training data while held-out data remains aligned. Collapse holds for the first ~80% of training at this band, which somewhat undermines the narrative.

- **Scale limitation (3.9B max) bounds practical claims:** The motivation centers on frontier-scale training ("$1B runs," line 300), yet all validation tops out at 3.9B. The paper does not discuss whether collapse might break down at larger scales. This limits confidence in extrapolation.

- **Directionality of "signature of compute-efficient training" (abstract, line 38):** The evidence shows one direction: optimal τ + fixed TPP → collapse. The converse (collapse → compute-optimal) is not established. Suboptimal but internally consistent hyperparameters might also produce collapse.

### Trivial
- Seven evaluation benchmarks (arc-c, arc-e, boolq, hellaswag, piqa, siqa, winoqrande) are all relatively easy/common; adding MMLU or coding benchmarks would strengthen downstream positioning.

## Nice-to-Haves
- Multi-seed experiments at one or two model sizes would most strongly validate the central claim.
- Extension of early stopping to LR sweeps at 1.8B or 3.9B.
- Brief discussion of expected limitations at 7B–70B+ scales.
- Explicit acknowledgment of the architecture shift between Sections 3 and 4.

## Removed Points
These points are flagged to be removed, treat them with caution.
- Harsh critic's concern about "reversibility of the collapse implies efficiency claim" — kept as a minor point about directionality framing, but demoted from "critical issue" because the paper's core contribution is demonstrating collapse under practical conditions and showing applications, not proving an if-and-only-if equivalence.
- Harsh critic's concern about Figure 2 comparison fairness — the paper explicitly acknowledges this in the "Philosophy" subsection (line 159), noting different data mixtures and evaluation pipelines. This is standard for model family papers.

## Novel Insights
The paper's most novel contribution is identifying the AdamW timescale τ as the key optimizer-level control governing TLC shape, providing a unifying view where TPP sets the pace of improvement and LR schedule phases the effects. The noisy quadratic model (Eq. 3) offers clean mechanistic understanding linking τ to bias-variance trade-off, and the scale-invariance argument (h cancels after normalization) explains why curves collapse. The practical demonstration that collapse residuals catch real training issues 30% earlier than raw loss monitoring (60% vs 90% of training) is a genuinely novel and actionable finding.

## Suggestions
- Report inter-run variation: Run 3 seeds for at least one model size (e.g., 900M) at 234 TPP and compare seed-to-seed residuals to cross-scale collapse residuals.
- Extend early stopping to LR sweeps at 1.8B or 3.9B.
- Tighten the "signature of efficiency" claim to "collapse is a *consequence* of training with optimal controls."
- Add a brief discussion of potential scale limitations (7B+).

## Reporting — Calibration Anchors

| Round | Anchor | Avg Human Score | Comparison |
|-------|--------|----------------|------------|
| 1 | Small-scale proxies for large-scale Transformer training instabilities | 8.00 | More thorough ablations; our paper has stronger practical applications |
| 1 | u-μP: The Unit-Scaled Maximal Update Parametrization | 7.33 | Focused parameterization work; our paper is broader |
| 1 | Scaling Law with Learning Rate Annealing | 6.75 | Similar topic, weaker practical validation; our paper has model family + monitoring + early stopping |
| 1 | Language models scale reliably with over-training and on downstream tasks | 6.50 | Similar empirical breadth; our paper has more novel mechanism |
| 1 | A Multi-Power Law for Loss Curve Prediction | 6.00 | Very similar topic, weaker practical grounding |
| 1 | Scaling Optimal LR Across Token Horizons | 6.00 | Simpler empirical study, fewer practical applications |
| 1 | Deconstructing What Makes a Good Optimizer | 6.00 | Different topic but similar empirical depth |
| 1 | A Hitchhiker's Guide to Scaling Law Estimation | 5.20 | Less practical validation |
| 1 | Different Rates for Different Weights | 2.50 | Weaker empirical validation |
| 1 | Training Mice to Compete with Elephants | 6.00 | Different focus, similar depth |

**Round-1 bracket: 6.5–7.5.** The paper is clearly above the 6.0 band (better practical grounding, model family, real debugging case, theoretical backing) and comparable to but slightly below the 7.33 paper (which had fewer gaps in validation). Score: **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>