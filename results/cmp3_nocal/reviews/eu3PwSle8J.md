## Summary

This paper proposes Augmented Intermediate Representations (AIR), a method for enforcing instruction hierarchy (IH) in LLMs to defend against indirect prompt injection attacks. While prior defenses inject IH signals only at the input layer (via delimiter tokens or segment embeddings), AIR adds a small per-layer trainable embedding table that injects privilege-level information at every decoder layer. Evaluated across three model families (Llama-3.2-3B, Qwen2.5-7B, Llama-3.1-8B), two training methods (SFT, DPO), and multiple attack types, AIR achieves 1.6×–9.2× reduction in ASR on gradient-based attacks compared to prior IH methods, with negligible parameter overhead (~0.4M parameters / 0.005% increase) and no significant utility degradation.

## Strengths

- **Well-motivated architectural insight (Figure 3).** The paper identifies a concrete, measurable limitation of prior IH injection methods: the cosine similarity between token representations at different privilege levels increases as information propagates through decoder layers, indicating signal degradation. This is a specific, falsifiable claim with clean supporting evidence.

- **Clean and lightweight method (Section 4).** AIR adds a per-layer embedding table indexed by privilege level. The overhead is negligible (0.4M parameters for Llama3.1-8B, a 0.005% increase). The parallel to RoPE (injecting information at every layer rather than only at the input) is apt and situates the contribution within a familiar architectural pattern. The method is simple enough that improvements can be attributed to the design principle rather than engineering complexity.

- **Strong and consistent results on gradient-based attacks (Table 1, Figure 7).** The improvements on GCG and Astra attacks are large and systematic across all three model sizes and both training methods. For example, on Llama-3.2-3B SFT+GCG: Delim ASR=38%, ISE ASR=48.1%, AIR ASR=4.1%. On Qwen-2.5-7B DPO+GCG: Delim ASR=32%, ISE ASR=7.7%, AIR ASR=1.6%. These are reductions that in many cases bring ASR close to zero.

- **Systematic evaluation scope.** Three model families (Llama-3.2-3B, Qwen2.5-7B, Llama-3.1-8B), two training methods (SFT, DPO), two evaluation datasets (AlpacaFarm, SEP), and multiple attack types (four static, two gradient-based). This breadth makes the results more convincing than evaluations limited to a single model or setting.

## Weaknesses

### Fatal
None.

### Major

- **No discussion of adaptive attacks or limitations of the defense.** This is a security-defense paper, yet the Conclusion (Section 7) is only three sentences with no limitations discussion. A grep for "adaptive" returns zero matches. An attacker aware of AIR's architecture could potentially design stronger attacks — since the per-layer embeddings $S_j$ are learnable parameters, an adversary might optimize tokens that explicitly counteract or override the per-layer privilege signals. Even a brief discussion of when and how the defense might fail (even without experimental evaluation) would substantially strengthen the paper's scientific integrity. This is the most significant omission and should be addressed in the final version.

### Minor

- **Utility comparison against the "None" baseline is confounded by unequal training budgets.** The "None" model receives only Round 1 (non-adversarial instruction tuning), while all IH-injection models (Delim, ISE, AIR) undergo both Round 1 and Round 2 (adversarial robustness training). The paper's claim that AIR "does not significantly degrade model utility" (Section 6.1) compares against a model with less total training. AIR-DPO often achieves *higher* win rates than None (e.g., 85.4% vs. ~80% for Llama-3.2-3B), which the paper acknowledges but does not remark may partly reflect the extra training stage. The within-method comparisons (AIR vs. Delim vs. ISE, all under the same two-stage protocol) are fair and still favor AIR. A counterfactual baseline — a model that undergoes two-stage training with *no* IH mechanism — would make the utility claim cleaner. The paper should acknowledge this confound more explicitly.

- **The cosine similarity analysis (Figure 3) is conducted on a pre-trained model, not on a fine-tuned one.** The analysis shows that delimiter-based IH signals maintain high cosine similarity (near 1.0) across all layers in the pre-trained Llama-3.2-3B model, yet the trained Delim model achieves a non-trivial 38% ASR on GCG (SFT) — far better than the undefended model (77.5%). This suggests that fine-tuning itself can teach the model to use delimiter tokens, partially compensating for the lack of input-layer separation measured on the pre-trained model. The analysis is motivation, not proof, but repeating it on *trained* models would verify that the hypothesized mechanism holds after optimization and would strengthen the paper's causal narrative.

### Trivial
None.

## Nice-to-Haves

- **Layer ablation study.** Training variants of AIR that inject IH signals at (a) only early layers, (b) only late layers, or (c) every $m$-th layer would directly test the paper's hypothesis about signal degradation and provide actionable guidance for practitioners.
- **Confidence intervals or variance reporting for ASR numbers (Table 1).** Many ASR values are very small (e.g., 0.1%, 0.0%) on 208 test instances; a few successful attacks could shift the metric meaningfully.
- **Varying the adversarial target.** All robustness evaluations use the same target response ("hacked!"). Varying the target (different exfiltration commands, response formats) would strengthen ecological validity.

## Removed Points

- **"SEP evaluation conflates utility and security through the separation score definition."** — Removed. This is a critique of the SEP methodology (Zverev et al., 2024), not of this paper's contribution. The paper uses SEP as an established evaluation framework; its potential limitations apply equally to all compared methods and do not affect the relative comparisons.
- **"The utility score only measures probe-following within the instruction segment, not general instruction-following ability."** — Removed. Same reason: this describes a property of the SEP metric from prior work, not a flaw in the paper's design or analysis.
- **"Fixed adversarial target ('hacked!') limits generalizability."** — Moved to Nice-to-Haves. Using a fixed target is a standard controlled experimental choice that reduces variance; it is a limitation worth acknowledging but not a weakness.

## Novel Insights

None beyond the paper's own contributions. The reviewer identified the adaptive-attack omission and the pre-training vs. post-training analysis gap, but these are gaps in coverage rather than novel observations about the paper's substance.

## Suggestions

1. Add a limitations paragraph (even brief) in the Conclusion discussing the threat model boundary and potential adaptive attacks.
2. Repeat the cosine similarity analysis (Figure 3) on the fully trained models to verify the mechanism persists after optimization.
3. Add a counterfactual utility baseline: a model that undergoes both rounds of training with no IH injection mechanism.
4. Consider reporting bootstrap confidence intervals for the main ASR numbers in Table 1.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>