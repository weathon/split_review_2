## Summary

This paper identifies a critical limitation in existing prompt injection defenses that rely on instruction hierarchy (IH) signals: they inject IH information only at the input layer, causing the signal to degrade as it propagates through the model. To address this, the authors propose Augmented Intermediate Representations (AIR), which injects layer-specific trainable IH embeddings at every decoder layer. Experiments across multiple models (3B–8B), training methods (SFT, DPO), and attacks (static, GCG, Astra) show that AIR reduces attack success rates by 1.6× to 9.2× compared to prior methods on gradient-based attacks, with minimal utility degradation.

## Strengths

- **Clear motivation and well-identified problem.** The paper provides empirical evidence (Figure 3) that IH signals injected only at the input layer progressively lose distinguishability across deeper layers, and it convincingly argues why this limits existing defenses. The hypothesis is grounded in an interesting analogy to positional encoding research (RoPE).

- **Simple, principled, and low-overhead solution.** AIR is elegantly simple: adding a small, trainable embedding table per layer (0.005% parameter increase for Llama-3.1-8B) to augment intermediate representations with privilege information. The overhead is minimal, making the method practical.

- **Thorough and well-controlled evaluation.** The paper compares three IH injection mechanisms (Delimiters, ISE, AIR) under two adversarial training schemes (SFT, DPO) across three model families and sizes, using two evaluation datasets (AlpacaFarm, SEP) with multiple attack types (static, GCG, Astra). The results consistently show AIR outperforming prior methods, often by large margins (e.g., 1.6×–145× ASR reduction for gradient-based attacks).

- **Good utility-robustness tradeoff.** AIR maintains comparable win rates to non-adversarially trained baselines (within 2% degradation) while achieving substantially better robustness, especially when combined with DPO. The SEP results further confirm improved instruction-data separation.

- **Well-structured and clearly written.** The paper is easy to follow, with clear definitions, a helpful figure comparing IH injection mechanisms, and appropriate connections to related work.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Causal link between representation similarity and robustness is only correlational.** The paper shows that AIR yields lower cosine similarity between representations of different privilege levels (Figure 3) and also achieves lower ASR. However, it does not directly demonstrate that this specific property is the cause of the improved robustness—other factors (e.g., the layer-specific trainable parameters providing more capacity) could contribute. A controlled ablation (e.g., injecting noise instead of IH signals at intermediate layers) would strengthen the causal claim.

- **The reported improvement factors are not uniform.** The abstract claims "1.6× to 9.2× reduction in ASR" for gradient-based attacks, but the actual numbers vary widely across models and training methods. For example, on Llama-3.2-3B with DPO, AIR achieves only a ~1.1× reduction over Delim for GCG (Table 1: 5.2 vs. 29.1, but the next best is Delim at 29.1; ISE is worse). The factor is computed relative to the best prior defense, which is reasonable, but the range might give a misleading impression of uniformity.

- **Evaluation is limited to AlpacaFarm and SEP datasets.** Both are instruction-following benchmarks. It would be valuable to test on more diverse or realistic agentic tasks (e.g., AgentDojo) to assess generalization, though the authors acknowledge this as future work.

- **The paper does not discuss potential adaptive attacks.** The gradient-based attacks evaluated (GCG, Astra) assume the attacker has full white-box access to the model, including AIR’s IH embedding tables. An adaptive attacker might try to directly manipulate or disrupt the IH signals themselves (e.g., by optimizing an adversarial prefix that cancels the added embeddings). The defense’s resilience to such attacks is not explored.

### Trivial

- In Table 1, the "None" column under SFT/DPO (no IH injection) and the "None" attack (no adversarial training) are both labeled "None", which can be confusing on first reading. The meaning is clear from context, but a small clarification would help.

## Nice-to-Haves

- An ablation comparing AIR with adding IH embeddings only to a subset of layers (e.g., first and last few) would further disentangle the effect of per-layer injection from total added capacity.
- A brief quantification of inference time increase, even if negligible, would strengthen the claim about practical overhead.
- Discussion of how AIR interacts with other defense components (e.g., instruction hierarchy training via DPO) and whether the gains are additive or synergistic.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- To strengthen the causal argument, consider an experiment where, instead of IH embeddings, random noise (or a fixed constant) is added to intermediate layers. If robustness does not improve, it would support the claim that the IH signal itself, not just the additional parameters, is responsible for the gains.
- Add a discussion of potential adaptive attacks and why AIR might (or might not) be robust to them. For example, an attacker could try to optimize a prefix that drives the IH embedding retrieval to produce a zero vector or to confuse the privilege levels. Acknowledging this limitation would improve the paper’s completeness.

## Score and Decision

**Score:** 8  
**Decision:** Accept  

The paper makes a clear, novel, and practically impactful contribution to an important security problem. The method is simple, well-motivated, and shows consistent and large improvements across diverse settings. The evaluation is thorough, and the writing is clear. The minor weaknesses do not undermine the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>