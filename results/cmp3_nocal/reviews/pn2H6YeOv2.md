## Summary

Pi-CCA proposes a replay-free continual learning framework for vision-language models that preserves cross-modal alignment by directly regularizing the spectral and subspace structure of canonical correlation analysis (CCA) rather than proxy signals like logits or similarities. The method uses a compact, sketched CCA certificate updated via EMA, combined with a prompt-invariance mechanism. Across four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL), Pi-CCA achieves state-of-the-art results among replay-free methods and is supported by thorough ablations and analysis.

## Strengths

1. **Principled reformulation of forgetting in VL-CL.** The core insight — that forgetting should be combated by preserving the geometry of cross-modal alignment (canonical correlations and subspaces) rather than matching proxy quantities — is well-motivated and conceptually clean. The paper clearly articulates why proxy-based methods permit slow drift of the alignment geometry (§1, §2).

2. **Comprehensive evaluation across four benchmarks.** The paper tests on MTIL (11-domain classification), X-TAIL (task-agnostic cross-domain), VLCL (retrieval), and ConStruct-VL (structured concepts), covering classification, retrieval, and structured prediction under both task-ID-aware and task-agnostic protocols. This is a thorough evaluation suite for a VL-CL method.

3. **Strong ablation and analysis depth.** Table 3 isolates each component (spectral, subspace, prompt invariance, EMAs, spectral moments, sketch type) and quantifies individual contributions. Figure 5 tests task-order sensitivity over 20 random permutations. The Pareto analysis of certificate capacity (Fig. 2) provides practical guidance for choosing k and h. These analyses go beyond what many new-method papers provide.

4. **Competitive results.** Pi-CCA achieves the best numbers among replay-free methods across all four tracks. On VLCL it even surpasses GIFT, which uses synthetic replay (Table 2). The margins over the strongest baselines (1–3 p.p.) are modest but consistent.

## Weaknesses

### Fatal
None.

### Major

1. **Unrealistically perfect correlation values in Figure 3.** The figure reports Pearson r=1.00 and Spearman ρ=1.00 (or 0.99) for all four panels showing the relationship between geometry drift (D_ang, D_ρ) and performance drops (ΔAvg, ΔR@1). The paper sweeps "certificate size, EMAs, invariance strength, whitening, pairing, LoRA capacity/LR, sketch type" (line 222) — at least seven varied hyperparameters. Perfect Pearson correlation (r=1.00) and perfect rank correlation (ρ=1.00) across such a diverse set of configurations is not credible for real experimental data; even an extremely strong linear trend would exhibit measurable deviations. Spearman ρ=1.00, which requires zero rank inversions across all settings, is especially implausible. These values could arise from a mathematical/procedural entanglement between the drift metrics and the performance metrics, or from rounding of values that are not actually 1.00. Either way, the paper needs to clarify how these values were computed, report them without rounding, and provide the raw data. Since the paper frames this analysis (§4.3, lines 222–223) as evidence for the causal link that validates its core approach, the credibility problem here is substantive.

### Minor

2. **Baseline comparison methodology is underspecified.** The paper reports results for 10+ baselines across Tables 1 and 2 but does not state whether these numbers were (a) taken from original papers, (b) re-implemented by the authors under controlled conditions, or (c) obtained from the authors of prior work. Given that the paper uses a specific LoRA-based parameter-efficient setup, and prior methods may have used different architectures, backbones, or full fine-tuning, it is unclear whether the 1–3 p.p. improvements are genuinely due to the method or could reflect implementation differences. This is a common limitation in CL papers, but the paper should clarify the source of baseline numbers.

3. **Confidence intervals reported inconsistently.** Table 2 (VLCL, ConStruct-VL) reports ± intervals, while Table 1 (MTIL, X-TAIL) reports single numbers without variance. The reproducibility statement mentions 3 seeds. Variance should be reported consistently across all main tables, or the paper should explain the asymmetry.

4. **"Constant-memory" framing slightly overstates the method's resource footprint.** The certificate itself is compact (O(hk), constant in d_v, d_t due to sketching, as noted in line 75). However, the streaming estimation mechanism (Eq. 12) maintains EMA of the full covariance matrices Σ_vv ∈ ℝ^{d_v×d_v}, Σ_tt ∈ ℝ^{d_t×d_t}, and Σ_vt ∈ ℝ^{d_v×d_t}, which are O(d²) in the embedding dimension. The paper should acknowledge the full memory picture rather than characterizing the entire mechanism as "constant-memory" (abstract, line 25) without qualification.

5. **No analysis of how the EMA certificate evolves over time.** The paper tracks geometry drift in Figure 3 but never reports how the certificate itself (ρ_{1:k}^*, S_v^*, \bar{S}_t^*) changes as training progresses across tasks. Do canonical correlations shrink, grow, or remain stable? Does the subspace rotate significantly? Since the paper claims to "preserve alignment," reporting the certificate's trajectory would strengthen this claim and address the natural question of whether the EMA update eventually causes the certificate to track the model rather than constrain it.

### Trivial
None.

## Nice-to-Haves

- Show that the geometry–performance correlation from Figure 3 holds out-of-sample (e.g., fit on one hyperparameter subset, evaluate on a held-out set) rather than relying solely on in-sample correlation.
- Add a simple baseline like L2 regularization on LoRA weights or feature distillation to the original frozen model to further clarify the benefit of the CCA-geometry approach.
- Analyze the half-life of the original pre-training signal in the EMA certificate as a function of α and task length.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Equation 12 has a garbled/parser-error line."** The line "M^(t) = (∑...S_v^{(t)})^{-1/2}..." on line 129 is a PDF-extraction artifact, not an author error. Per policy, formatting/parser errors are not counted as weaknesses.
- **"Prompt perturbation distribution 𝒫 is not specified in the main text."** The paper says "synonym/template variation" (line 81) and references the appendix (§A.2) for full details. The appendix was stripped during parsing; this is not a missing specification by the authors.
- **"EMA certificate update creates tension with 'preservation' framing."** The paper explicitly acknowledges this trade-off: "allowing controlled plasticity" (line 133). The language ("alignment skeleton," "controlled plasticity") is precise about what is being preserved and what is allowed to drift. This is not a contradiction.
- **"Computational overhead of differentiable SVD is not discussed."** The paper presents a detailed Pareto analysis of compute vs. performance (Fig. 2), which addresses the efficiency question at a holistic level. A breakdown would be a nice addition but its absence is not a weakness.
- **"No comparison to simple baselines like L2 regularization."** Requesting additional baselines is always possible; the paper already compares against 10+ SOTA methods. This is scope creep.
- **"Missing related works."** Per policy, missing related work criticisms are not included because I cannot independently verify the existence of omitted references.
- **"Code cannot be released during review."** The paper includes a detailed reproducibility statement specifying all hyperparameters, EMA rates, sketch dimensions, and task-order permutations. The reproducibility concern about Figure 3 is already addressed in Major Weakness #1 above; the broader code-release policy concern is not a valid weakness per ICLR norms.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Address the Figure 3 credibility issue directly.** Report actual (unrounded) Pearson and Spearman values. If the values round to 1.00, state this explicitly and show the raw data. Alternatively, explain any mathematical relationship between the drift metrics and performance metrics that would produce near-deterministic correlation. Without this clarification, the mechanistic evidence for the paper's core claim remains suspect.

2. **Clarify the baseline methodology.** State explicitly whether all baseline numbers were obtained from the original papers or re-implemented under controlled conditions. If numbers are from original papers, note any differences in backbone, LoRA rank, training recipe, etc. that could affect comparability.

3. **Add variance to Table 1** or explain why confidence intervals are omitted for the classification tracks.

4. **Qualify the "constant-memory" claim** by noting that while the certificate is compact, the overall method requires O(d²) storage for the EMA covariance matrices, though this is constant in the number of tasks (not growing with data).

5. **Show the certificate's trajectory** over the course of training to empirically demonstrate how much the canonical correlations and subspaces drift.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>