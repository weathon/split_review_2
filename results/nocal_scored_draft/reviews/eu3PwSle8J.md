## Summary

This paper proposes Augmented Intermediate Representations (AIR), a defense against indirect prompt injection attacks in LLMs. The key insight is that existing defenses inject the Instruction Hierarchy (IH) signal only at the input layer, and this signal degrades through subsequent layers. AIR addresses this by adding small trainable embedding tables to each decoder layer (one per privilege level), injecting the IH signal recurrently. Evaluated across 3 model families, 2 training methods (SFT and DPO), 6 attack configurations, and 2 datasets, AIR consistently improves robustness over delimiter-based and ISE-based defenses, especially against gradient-based attacks (GCG and Astra), with negligible utility degradation and only 0.005% parameter overhead.

## Strengths

1. **Well-motivated with diagnostic evidence.** Figure 3 empirically demonstrates that input-level IH signals (ISE, Delim) converge in cosine similarity across layers, while AIR maintains better separation. This diagnostic directly supports the paper's central hypothesis — a type of evidence prior work typically does not provide. *(Favorability: 1.00)*

2. **Consistently strong empirical results on gradient-based attacks.** AIR substantially reduces ASR on GCG and Astra across nearly all model/training configurations. For example, on Qwen-2.5-7B SFT, Astra ASR drops from 69% (Delim)/39.2% (ISE) to 2.4% (AIR). On Llama-3.2-3B SFT, GCG ASR drops from 38% (Delim)/48.1% (ISE) to 4.1% (AIR). These are large and systematic improvements. *(Favorability: 1.00)*

3. **Utility is not sacrificed.** AlpacaEval win rates show AIR does not degrade instruction-following quality (it is often slightly better than the non-adversarial baseline), addressing the practical concern that security defenses trade off against capability. *(Favorability: 1.00)*

4. **Simple, low-overhead method.** AIR is conceptually clean: one trainable embedding table per decoder layer, indexed by privilege level. For Llama-3.1-8B, this is only 0.4M parameters (0.005% increase), making it practically deployable with negligible inference overhead. *(Favorability: 0.92)*

5. **Systematic evaluation.** The paper evaluates 3 model families (3B–8B), 2 training methods (SFT and DPO), 4 static attacks, 2 gradient-based attacks (GCG and Astra), and 2 datasets — a broader experimental matrix than most prior defense papers in this area. *(Favorability: 0.88)*

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Overstated lower bound on the claimed performance ratio.** The abstract and conclusion claim "1.6× to 9.2× reduction" for gradient-based attacks. For GCG on Llama-3.1-8B DPO, the ratio of next-best-defense ASR to AIR ASR is 4.0/2.8 ≈ 1.43×. For Astra on the same configuration, the ratio is 1.2/1.0 = 1.2×. The overall dominance is clear, but the stated lower bound does not hold for every tested configuration. The range should be corrected or qualified (e.g., "up to 9.2×, with most configurations showing 1.4–9.2×"). *(Favorability: 0.62)*

2. **Logit-based ASR for gradient-based attacks without generation-based validation.** For static attacks, ASR measures whether the output actually contains "hacked!" (generation-based). For GCG and Astra, ASR uses the logit likelihood of generating the target phrase (Section 5.4). Logit-based ASR does not guarantee the model would generate the target under sampling — a well-known distinction in the adversarial literature. While comparisons between methods using the same metric remain meaningful, the absolute ASR values may not reflect real attack outcomes, and the inconsistency with the static-attack metric is unexplained. *(Favorability: 0.64)*

3. **SFT vs. DPO comparison is confounded by different training setups.** The paper's secondary claim that "adversarial training with DPO yields more robust models than SFT" (Section 6.1) is based on comparing SFT (full fine-tuning, LR 1e-5) against DPO (LoRA, LR 2e-4). The objective and the parameter update scheme differ simultaneously, making it impossible to attribute the advantage to the preference objective vs. LoRA's implicit regularization. This does **not** affect the primary AIR vs. Delim/ISE comparison, which is controlled within each training method, but the SFT-vs-DPO comparison should be acknowledged as confounded. *(Favorability: 0.43)*

4. **No variance reported for ASR numbers in Table 1.** The paper reports standard deviation for the GCG loss curves (Figure 7, shaded regions) but not for the ASR values in Table 1, which are the paper's headline robustness numbers. Since ASR values can be sensitive to initialization, multi-run statistics (or at minimum a note about single vs. multiple runs) would strengthen confidence. *(Favorability: 0.63)*

### Trivial
None.

## Nice-to-Haves

- **Limitations section.** The paper does not discuss what types of attacks AIR might *not* defend against, whether the defense assumes a specific structure of the IH signal, or whether protection transfers to out-of-distribution attack prompts. A brief limitations subsection would strengthen the paper.
- **Adaptive attack analysis.** Even a brief experiment showing whether an attacker aware of AIR can design a prefix that minimizes distinctiveness across privilege levels would preempt a natural reviewer concern. The existing GCG/Astra attacks are already white-box and backpropagate through AIR, but a targeted adaptive analysis would be stronger.
- **Control for parameter count.** Giving ISE or Delim additional trainable parameters at each layer to match AIR's parameter count would control for the possibility that AIR's advantage comes from increased capacity rather than the multi-layer injection mechanism.
- **Generation-based ASR for gradient-based attacks.** Supplementing the logit-based metric with generation-based results (even for a subset) would close the gap between the proxy and actual behavioral robustness.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **"Training data details deferred to appendix."** The paper references Appendix B.1 for dataset details. The appendix exists in the original submission but was stripped by the parser. Removed per meta-review policy.
- **"Figure 3 shows Delim maintaining cosine similarity of 1.0."** This observation about Delim is not a weakness of the paper — the diagnostic's main comparison (ISE vs. AIR) still supports the paper's motivation, and Delim's mechanism is fundamentally different.
- **"No limitations discussion" and "Adaptive attack analysis" and "Parameter-count control."** These are suggestions for improvement, not weaknesses. Moved to Nice-to-Haves.
- **"SEP score definition is confusing."** Minor presentation observation, not a substantive weakness.
- **"RoPE analogy imprecise."** Minor presentation observation, not a substantive weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct or qualify the "1.6×" lower bound on the claimed performance range to reflect the actual minimum ratios (1.2× for Astra, 1.43× for GCG on certain configurations).
2. Add a brief justification for using logit-based ASR for gradient-based attacks, or supplement with generation-based results for a representative subset.
3. Report variance (standard deviation or range across seeds) for ASR values in Table 1, or explicitly state the number of runs.
4. Add a limitations subsection discussing the scope and potential failure modes of AIR.

---

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>