Now I will write the final consolidated review.

## Summary

This paper proposes Augmented Intermediate Representations (AIR), a defense against indirect prompt injection attacks in LLMs. The key insight is that existing methods inject instruction hierarchy (IH) signals only at the input layer (via delimiter tokens or segment embeddings), and these signals degrade through deeper layers. AIR addresses this by adding small, learnable per-layer embedding tables to the residual stream at every decoder block, so the IH signal is reinforced at each layer. Evaluated across three models (Llama-3.2-3B, Qwen2.5-7B, Llama-3.1-8B), two training paradigms (SFT, DPO), and multiple attack types, AIR achieves 1.6×–9.2× reduction in ASR on gradient-based attacks compared to prior IH injection mechanisms (Delimiters, ISE) while maintaining model utility.

## Strengths

1. **Well-supported diagnosis of a concrete limitation.** Figure 3 quantitatively demonstrates that input-only IH methods lose privilege-level separation as representations propagate — cosine similarity between tokens of different privilege levels increases from ~0.55 at layer 0 to ~0.92–1.0 by layer 25, while AIR maintains ~0.85. This provides a clear, measurable motivation for per-layer injection.

2. **Simple and minimally invasive design.** AIR introduces one trainable embedding table per decoder layer (one entry per privilege level). For Llama-3.1-8B with 3 privilege levels, this is ~0.4M extra parameters (0.005% increase). The modification is architecturally straightforward — essentially one vector addition per token per layer — and could be adopted in existing transformer-based models with negligible inference overhead.

3. **Strong, consistent empirical results on the core comparison.** On gradient-based attacks (GCG, Astra), AIR outperforms both Delimiters and ISE across all three models and both training paradigms (SFT, DPO) in Table 1. The improvements are large and practically meaningful (e.g., GCG ASR: 4.1 vs. 38 for Llama-3.2-3B SFT; 1.6 vs. 7.7 for Qwen-2.5-7B DPO). These results support the paper's central claim that per-layer IH injection is more robust than input-only injection.

## Weaknesses

### Major

1. **Confounded utility comparison with the "None" baseline.** The paper claims in the abstract and conclusion that AIR achieves these robustness gains "without significantly degrading the model's utility." However, the utility comparison (Section 6.1, Figure 6) compares AIR — which received both Round 1 (non-adversarial instruction tuning) and Round 2 (adversarial training) — against the "None" baseline, which received only Round 1. This is not a controlled comparison. In several cases AIR shows *higher* win rates than None (e.g., 91.9% vs. ~80% for Qwen-2.5-7B DPO), which likely reflects the benefit of additional training rather than the absence of degradation. The SEP section (line 260) partially acknowledges this confound for SFT, but the abstract and conclusion state the utility claim without qualification. The comparison that matters for the paper's core thesis — AIR vs. Delim/ISE on robustness — is unaffected, but the utility-preservation claim is overstated.

### Minor

2. **Missing DPO-None baseline in Table 1.** The SFT column includes a "None" sub-column (adversarial SFT without IH signals), which allows attribution of improvements to the IH signal. The DPO column has no equivalent — only DPO-Delim, DPO-ISE, and DPO-AIR. This makes it impossible to disentangle how much of AIR's DPO robustness comes from the IH mechanism versus DPO training itself. While the SFT comparisons already demonstrate AIR's advantage over Delim/ISE independent of DPO (so this does not undermine the core claim), the missing baseline weakens the completeness of the DPO analysis.

3. **No variance or statistical significance reported for Table 1 ASR values.** The ASR values in Table 1 are single point estimates with no indication of run-to-run variation. GCG involves random initialization and stochastic optimization; the stability of the reported improvements (e.g., 4.1 vs. 38, or 1.6 vs. 7.7) is unknown. Figure 7 does show mean ± std for the loss curves, which lends some confidence, but the ASR numbers themselves should be reported with variance.

4. **No discussion of adaptive attacks.** The evaluated attacks (GCG, Astra) are standard white-box attacks not designed with AIR in mind. An adversary aware of AIR's per-layer embeddings could potentially optimize to neutralize them (e.g., by adding a term to the loss that minimizes the IH-enforced separation). This is a standard limitation shared by most defense papers — it does not invalidate the reported results, but it should be acknowledged to properly scope the claims.

### Trivial

None.

## Nice-to-Haves

- Adding a DPO-None baseline to Table 1 for completeness.
- Reporting ASR with standard deviation over multiple seeds for gradient-based attacks.
- Analyzing what the learned per-layer IH embeddings encode (e.g., visualizing layer-specific embedding vectors via PCA or cosine similarity).
- Evaluating against a defense-aware version of GCG that explicitly targets the IH embeddings.
- Discussing whether an ordinal inductive bias (rather than independent categorical embeddings per privilege level) would be more principled for the hierarchy.

## Removed Points

These points from the input review are removed with justification:

- *"Training dataset details are relegated to the appendix"* — The appendix was stripped by the paper parser; this is not an author error.
- *"The IH signal injection point is ambiguous"* — Equation (1) and Figure 4 clearly specify injection at the input of each decoder block, plus an additional augmentation after the last decoder layer (line 101). The description is unambiguous.
- *"The paper conflates Delimiters and ISE"* — The paper correctly identifies their shared limitation (input-only injection) and Figure 3 explicitly shows they behave differently. This is accurate description, not conflation.
- *"No discussion of cross-privilege-level interactions / ordinal structure"* — This is a design choice (independent embeddings), not a flaw. It could be explored in future work but is not a weakness.
- Generic formatting nitpicks, speculative criticisms, and reproducibility concerns about cited references/tools — these are either parser artifacts or violate the rule that cited entities are assumed to exist.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the utility claim framing in the abstract and conclusion: either qualify that the comparison is against a model with only non-adversarial instruction tuning, or better, add a controlled utility comparison where the baseline also receives two rounds of training (with or without IH signals).
2. Add a DPO-None baseline to Table 1.
3. Report ASR with standard deviation over multiple seeds for the gradient-based attacks (Table 1).
4. Add a brief discussion of adaptive/defense-aware attacks to the threat model section.

## Score and Decision

**Calibration.** Round 1 bracketing searched the human-review corpus for "defense against prompt injection attacks in LLMs" across six score bands. The most informative anchors for this paper (a novel defense method evaluated on gradient-based attacks) are:

| Anchor | Avg Score | Comparison to this paper |
|---|---|---|
| PFT (l3bUmPn6u5) — position-enhanced SFT against prompt injection | 4.25 / Reject | Weaker evaluation (naive attacks only, single model), weaker baselines, questionable real-world relevance. AIR is substantially stronger. |
| Baseline Defenses (0VZP2Dr9KX) — survey of simple baselines against GCG | 5.25 / Reject | Not a novel method paper. Different contribution type, but AIR's novelty and evaluation depth are higher. |
| BEAT (EbxYDBhE3S) — black-box backdoor defense | 6.00 / Accept | Similar-profile defense paper with well-designed experiments. AIR has comparable evaluation breadth but a simpler, more elegant method. |
| Beyond Mere Token Analysis (rnJxelIZrq) — hypergraph defense against social engineering | 6.50 / Accept | Novel method with theoretical guarantees. AIR has stronger empirical results but no theory component. |
| Tensor Trust (fsW7wJGLBd) — prompt injection attack dataset | 7.00 / Accept | Different contribution (dataset/benchmark). Not directly comparable. |

The paper sits between PFT (4.25) and BEAT (6.0) in terms of the strength of its evaluation and novelty, but closer to BEAT because its core comparison is well-controlled and the results are large and consistent. The weaknesses (confounded utility claim, missing DPO-None, no variance) are real but do not undermine the central claim. The initial bracket (5.5, 7.5) narrows to **6.0** given the gap between this paper and the PFT anchor below, and the presence of addressable but non-fatal evaluation gaps that keep it from reaching the 6.5–7.0 level of more comprehensive evaluations.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>