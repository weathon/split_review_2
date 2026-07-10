Now let me compile my final synthesis and score.

**Round 1 bracket:** After reviewing the paper and impact scores, the narrowest plausible range is **4.5–6.5**. The paper's strengths (AMP novelty +10.00, consistent improvements +9.98, broad evaluation +9.47, diagnostic analysis +8.81) are substantial, but the two decisive weaknesses (PTB overclaim -10.00, AMP heuristic gap -9.88) pull it down significantly. This puts it above rejected papers like PrefixQuant (3.00) and SliM-LLM (5.40, rejected for fatal practicality flaws), but below strong accepts like ARB-LLM (7.00).

**Round 2 narrowing:** Comparing to anchors in the 4.5–6.5 band:
- **STBLLM (6.00, accepted):** Had comparable weakness magnitudes (-9.99, -9.93, -9.63) but for methodological opaqueness rather than evidential/truthfulness issues. The current paper's diagnostic analysis (+8.81) and AMP novelty (+10.00) are stronger contributions. Slightly above STBLLM.
- **OSTQuant (6.20, accepted):** Had similar weakness profile (-10.00, -9.83, -9.95) but for mathematical/notational errors. Current paper's weaknesses are more about analysis gaps than errors. Comparable.
- **I-LLM (5.00, rejected):** Had fatal novelty concerns + evaluation gaps. Current paper is clearly stronger.
- **OmniQuant (6.40, accepted):** Had -9.96 novelty concerns but strong empirical showing. Current paper has stronger analytical novelty but a truthfulness concern (PTB overclaim). Slightly below OmniQuant.

The paper sits between STBLLM (6.00) and OmniQuant (6.40). Given the PTB truthfulness concern (abstract claims "consistently" but the body acknowledges an exception), I place it at **6.0** — borderline accept, comparable to STBLLM.

Let me also note from the calibration data that STBLLM (6.00, accepted) had a similar weakness profile with multiple -9.xx impact weaknesses but was still accepted. The current paper has two -10.00/-9.88 weaknesses but also stronger strengths. A score of 6.0 is reasonable — the paper has real contributions and should be accepted, but the overclaiming issue needs to be addressed.

Now let me write the final review.

Let me organize my final output.

Summary: The paper investigates why naive output-matching fails in 1-bit PTQ for LLMs, identifying three failure modes. It proposes a selective output-alignment strategy with Attention Matrix Preservation (AMP). The diagnostic analysis in Section 3 is a genuine contribution, AMP is a novel mechanism addressing a previously unexplored problem, and results show consistent improvements on most benchmarks.

Strengths:
1. Diagnostic analysis (Section 3) - three concrete failure modes identified
2. AMP is novel and shows dramatic empirical benefits
3. Consistent improvements on C4, WikiText2, AveQA across all model sizes
4. Broad evaluation across model families

Weaknesses:
- Major: PTB failure on LLaMA-2-7B (3166 PPL vs ARB-RC 763) contradicts the abstract's "consistently outperforms" claim; paper dismisses it rather than analyzes it.
- Major: AMP lacks theoretical analysis — it's a heuristic with only ablation evidence.
- Minor: Selective-layer design choice is not ablated.
- Trivial: Notation imprecision in Eq. 9.

Nice-to-haves: calibration details, confidence intervals.

Score: 6.0 - Borderline Accept

Decision: Accept (with caveats that the authors should address the PTB issue and AMP analysis in the final version).

Wait, actually the guidelines say "If the weaknesses identified would, if true, invalidate or severely undermine the paper's core contribution, the review should reflect that clearly." Do these weaknesses severely undermine the core contribution? The PTB failure doesn't invalidate the contribution — the method still works on most benchmarks, and the diagnostic analysis is independent of that result. The AMP heuristic gap doesn't invalidate AMP's empirical effectiveness. So the core contributions stand, just with caveats. The paper should be accepted but the authors should address these issues.

Let me finalize the review now.## Summary

This paper investigates why naive output-matching (minimizing $\|\hat{X}W - \hat{X}\hat{W}\|$) fails in 1-bit post-training quantization (PTQ) for LLMs, and proposes a selective output-alignment strategy with Attention Matrix Preservation (AMP). The diagnostic analysis in Section 3 identifies three failure modes: layer-wise output matching does not guarantee block-level loss reduction, quantization errors accumulate because the objective conditions on corrupted activations $\hat{X}$, and token similarity matrices drift. The method restricts output alignment to the last layer per block, switches to the true Output Error $\|XW - \hat{X}\hat{W}\|$, and adds AMP gradient-sign masking. Experiments on OPT (1.3B–30B), LLaMA-2, and LLaMA-3 show consistent perplexity improvements on C4 and WikiText2, with modest but uniform gains over ARB-RC.

---

## Strengths

- **Strong diagnostic analysis (Section 3).** The paper identifies three concrete, well-motivated failure modes of naive output-matching in 1-bit PTQ: (i) layer-wise optimization does not guarantee block-level loss reduction, (ii) conditioning on $\hat{X}$ causes error accumulation, and (iii) token similarity matrices drift, degrading attention. This analysis uses appropriate comparisons (ARB vs. ARB-X) and constitutes a useful contribution independent of the proposed method. [impact=+8.81]

- **AMP is a genuinely novel mechanism addressing an unexplored problem.** No prior 1-bit PTQ work has explicitly tackled the degradation of token-token similarity structure during binarization. The ablation (Table 3) shows AMP has a dramatic effect on LLaMA models (10+ PPL points on C4), confirming this is a real issue and that AMP provides substantial benefit. [impact=+10.00]

- **Consistent improvements on C4, WikiText2, and AveQA across all model sizes.** The method beats all baselines on perplexity for every model tested (OPT 1.3B–30B, LLaMA-2 7B/13B, LLaMA-3 8B) on C4 and WikiText2, and on AveQA accuracy. Improvements over ARB-RC are modest on large models but substantial on smaller ones (e.g., OPT-1.3B: 3–5 PPL reduction). [impact=+9.98]

- **Broad evaluation across model families and scales.** The paper covers OPT (1.3B–30B), LLaMA-2 (7B/13B), and LLaMA-3 (8B) with standard benchmarks (C4, WikiText2, PTB, 7 QA datasets) and appropriate baselines (PB-LLM, BiLLM, ARB-RC, ARB-X). [impact=+9.47]

---

## Weaknesses

### Fatal

None.

### Major

- **The PTB result on LLaMA-2-7B contradicts the paper's central claim and is handled dishonestly.** The proposed method achieves perplexity **3166** on PTB for LLaMA-2-7B, compared to ARB-RC (763.19), ARB-X (681.24), and PB-LLM (657.24) — i.e., it is substantially *worse* than all baselines. The paper dismisses this at line 233: *"However, the large perplexity indicates that the metric cannot provide a meaningful evaluation."* This is not a valid argument — the same metric distinguishes methods elsewhere. While the paper body does note the exception (lines 175–176: *"with the exception of Llama-2-7B model evaluated on PTB dataset"*), the abstract claims the method *"consistently outperforms existing 1-bit PTQ methods"* without caveat, which is misleading. A proper treatment would analyze *why* this happens (e.g., does the output-error objective overfit to the calibration distribution? Do attention patterns in deeper layers fail?) rather than dismissing the metric. [impact=-10.00]

- **AMP is introduced as a heuristic with no theoretical grounding or analysis.** The AMP "mask" is defined as the sign of the gradient of $\mathcal{L}_{AMP}$ with respect to each parameter (Eq. 10–11). The paper provides no analysis of *why* sign-based gating should preserve attention structure — no proof, no toy example, no discussion of when gradient signs might be unreliable (e.g., near saddle points, or with small calibration sets). The only evidence is the ablation in Table 3, which shows AMP works but not *why*. As the most novel component, the lack of deeper analysis is a significant gap. [impact=-9.88]

### Minor

- **The selective-layer design choice is not ablated.** Section 4.2 states that output alignment is restricted to *"only the last fully connected layer of each block, since it has the most direct impact on the block loss."* This claim is unsupported — no ablation compares output alignment on all layers vs. only the last layer, last vs. first vs. middle layer, or one vs. multiple layers per block. Given the paper's own analysis shows naive layer-wise output matching can hurt block-level performance (Section 3.1), this design decision should be empirically validated. [impact=-3.93]

- **Calibration details are underspecified.** The paper does not state the number of calibration samples, sequence length, or whether the same calibration set is used consistently across all methods. This matters for reproducibility, especially since the method requires running the full-precision model to obtain inputs $X$. [impact=-0.01]

### Trivial

- **Notation imprecision in Eq. 9.** The objective is written as maximizing $\|A \odot B\|$ (Frobenius norm of element-wise product) but then expanded as $\text{Tr}[AB]$ (the Frobenius inner product / sum of element-wise products). These are not equivalent — the norm involves a square root that the trace does not. The objective should be written as the Frobenius inner product $\langle A, B \rangle_F$ rather than the norm of the element-wise product. [impact=-0.01]

---

## Nice-to-Haves

- Report inference efficiency metrics (latency, memory usage, throughput) to support the practical deployment motivation.
- Investigate the PTB failure on LLaMA-2-7B systematically: is it distribution mismatch from the C4 calibration set? Does the RMSNorm hypothesis (offered to explain AMP's importance on LLaMA) also explain this failure?
- Provide a synthetic diagnostic or probe showing that the AMP gradient-sign mask correlates with preserving token-similarity structure, rather than only showing that perplexity improves.
- Report standard deviations across multiple calibration runs, given that calibration is performed on small datasets.

---

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"Method is incremental over ARB-RC" (Critical Issue 2 from harsh critic):** This observation is factually correct but does not constitute a weakness — the paper is transparent about building on ARB-RC, and the combined effect of changes is positive. A well-motivated incremental improvement with clear diagnostic reasoning is a legitimate contribution. The removal is further supported by the scoring model giving this issue negligible impact weight.
2. **"No comparison to BitNet / training-based 1-bit methods":** The paper explicitly scopes to PTQ. Criticizing absence of comparison to training-based methods is scope creep.
3. **"No inference efficiency benchmarks":** The paper states "Overhead Analysis. Please refer to Appendix D" (line 265). The appendix was stripped by the parser; this is unverifiable.
4. **"No variance/confidence intervals":** Single-run reporting without CIs is standard practice in this subfield. This is a nice-to-have, not a weakness.
5. **"Missing related works":** Removed per hard rules — the reviewer does not have external sources to verify missing citations.
6. **Formatting/style nitpicks and typos:** Removed per hard rules — these are parser artifacts, not author errors.

---

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation that the PTB failure is a selective-reporting concern (the paper claims consistent improvement but dismisses a counterexample) is novel as a review-level insight, but it arises from the paper's own data.

---

## Suggestions

1. **Qualify the abstract.** Replace "consistently outperforms" with a more precise statement that acknowledges the PTB exception, or add a caveat.
2. **Analyze the PTB failure on LLaMA-2-7B.** Investigate whether the C4 calibration distribution causes the output-error objective to overfit, or whether attention degradation in LLaMA-2's specific architecture contributes to the collapse. Even a brief diagnostic discussion would substantially improve credibility.
3. **Ablate the selective-layer design.** Compare output alignment on the last layer only, the first layer only, all layers, attention layers only, and FFN layers only.
4. **Probe AMP's mechanism.** Provide evidence that the gradient-sign mask correlates with preserving token-similarity structure — e.g., a synthetic example, a diagnostic plot of similarity-matrix drift with and without AMP across layers, or analysis of when the gradient sign is reliable.
5. **Specify calibration details.** Report number of samples, sequence length, and whether the same calibration set is used for all methods.

---

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `BifeBRhikU.md` (PB-LLM) | 6.75 | 1 | Yes | Accepted; had -10.00 novelty concern but accepted at 6.75. Current paper has stronger analysis but a truthfulness concern (PTB). Slightly below. |
| `ZU8OdDLTts.md` (ARB-LLM) | 7.00 | 1 | Yes | Direct predecessor; accepted at 7.00 with mostly clarification-level weaknesses. Current paper has more severe weaknesses. Below. |
| `6XUSDvBFkV.md` (STBLLM) | 6.00 | 1 | Yes | Accepted with -9.99/-9.93/-9.63 weaknesses. Current paper has comparable weakness magnitude but stronger strengths. Comparable or slightly above. |
| `vw0NurJ7UX.md` (PrefixQuant) | 3.00 | 1 | Yes | Rejected for fatal novelty concerns. Current paper is substantially stronger. |
| `44pbCtAdLx.md` (I-LLM) | 5.00 | 1 | Yes | Rejected for novelty and evaluation gaps. Current paper is clearly stronger. |
| `rAcgDBdKnP.md` (OSTQuant) | 6.20 | 2 | Yes | Accepted with -10.00/-9.83 weaknesses. Comparable profile. |
| `8Wuvhh0LYW.md` (OmniQuant) | 6.40 | 2 | Yes | Accepted with -9.96/-9.93 novelty concerns. Current paper slightly below due to truthfulness issue. |
| `tjlTczcnPz.md` (SliM-LLM) | 5.40 | 2 | Yes | Rejected for fatal practicality flaw (inference slower than FP16). Current paper is stronger. |

**Round 1 bracket:** 4.5–6.5 (below ARB-LLM at 7.00, above I-LLM at 5.00).

**Narrowing (Rounds 2–3):** The paper's impact profile (two decisive negatives at -10.00 and -9.88, four strong positives at +8.81 to +10.00) most closely matches STBLLM (6.00, accepted) and OSTQuant (6.20, accepted). The PTB truthfulness concern distinguishes it from the cleaner accept at OmniQuant (6.40). The paper has stronger analytical novelty than STBLLM but a credibility issue that STBLLM did not have.

**Final placement:** Calibrated against anchors, the paper sits between STBLLM (6.00) and OmniQuant (6.40), closer to the lower end of that range due to the PTB overclaim issue. A score of **6.0** reflects that the paper has genuine, well-supported contributions (diagnostic analysis, AMP mechanism) and should be accepted, but the authors must address the PTB counterexample honestly and provide deeper analysis of AMP before final publication.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>