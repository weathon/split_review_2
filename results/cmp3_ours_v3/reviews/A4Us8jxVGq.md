Now I have enough information to produce the final calibrated review.

## Summary of Calibration

**Anchors retrieved:**

| Paper | Avg Score | Decision | Comparison |
|---|---|---|---|
| "Scaling In-the-Wild Training..." (u1cQYxRI1H) | 0.50 | Accept | Unrelated topic |
| "Systematic Review of LLMs" (8QTpYC4smR) | 1.00 | Reject | Survey paper, no comparison |
| "On the Entropy of Language Models..." (z3DMFpaP6m) | 3.00 | Reject | Limited theory, our paper is stronger |
| "Transformers Learn Higher-Order Optimization" (YKzGrt3m2g) | 4.25 | Reject | Similar theory-exp gap; our paper has stronger empirical validation |
| "The mechanistic basis of data dependence" (aN4Jf6Cx69) | 4.50 | Accept (split) | Interpretability focus; our paper has cleaner quantitative results |
| "Mind the Gap" (X6xzYP2cMk) | 4.75 | Reject | Purely theoretical at init; our paper has dynamics analysis |
| "Stagewise Development in Transformers" (xEZiEhjTeq) | 5.50 | Reject | Comparable theoretical ambition but limited scale; our paper has stronger weight-level validation |
| "How Transformers Implement Induction Heads" (1lFZusYFHq) | 6.20 | Reject | Cleaner theory on simpler setup; our paper more realistic but messier validation |
| "One Step of GD is Provably Optimal" (8p3fu56lKc) | 6.00 | Accept | Clean theory with specific assumptions; our paper more ambitious but gaps larger |
| "On Optimization and Generalization..." (97rOQDPmk2) | 7.33 | Accept | Well-aligned theory and experiments; our paper has less alignment |

**Round 1 bracket:** 4.5 – 6.0

**Narrowing:** Our paper sits between the 4.25–4.75 range (theory-exp gaps, limited baselines) and the 5.5–6.2 range (cleaner alignment). The theoretical contribution is stronger than the 4.25 papers, but the validation gaps are wider than the 6.0 papers.

**Final score: 5.0** — The paper has genuine theoretical novelty (realistic setup, differential timescale prediction, interpretable decomposition) and strong quantitative agreement on the toy model (>0.998 cosine similarity). However, the full-batch GD vs SGD mismatch, the 5-step formal guarantee vs 100-epoch validation, and the absence of baseline comparisons significantly weaken the claim that the theory *explains* how associations emerge during training. The paper contributes valuable ideas but in its current form does not fully substantiate its central claims.

---

## Summary

This paper studies how semantic associations emerge in attention-based transformers during training. Using a gradient leading-term expansion, the authors derive closed-form expressions for transformer weights (output, value, query-key, and positional) early in training, expressing them as compositions of three basis functions: bigram mapping, interchangeability mapping (token functional similarity), and context mapping (prefix-suffix co-occurrence). The theory predicts different weights acquire structure at different timescales (W_O at O(η), V at O(η²), W/P at O(η⁴)). Predictions are validated on a 3-layer attention-only transformer trained on TinyStories (cosine similarity >0.99) and qualitatively extended to Pythia-1.4B via covariance matrix comparisons.

## Strengths

1. **Realistic theoretical setup.** The theory incorporates relative positional encodings, causal masking, and residual connections — components typically stripped in prior theoretical analyses (e.g., Bietti et al. 2023, Tian et al. 2023, Huang et al. 2025). This reduction in the gap between theory and practice is a genuine advance.

2. **Non-trivial differential timescale prediction.** Theorem 4.1 predicts that W_O, V, and W/P acquire structure at different orders in the learning rate (O(η), O(η²), O(η⁴)). This is a concrete, falsifiable prediction about the relative rate at which different components learn associative structure.

3. **Clean interpretable decomposition.** The three basis functions (bigram mapping B̄, interchangeability mapping Σ_{B̄}, context mapping Φ̄) provide a linguistically motivated vocabulary for discussing what the weights encode. The qualitative examples in Figure 5 show plausible semantic relationships ("fish" → "pond," "red" → "truck," "happy" ↔ "excited").

4. **Strong quantitative agreement on the 3-layer model.** Minimum cosine similarity >0.998 across 100 epochs for all weight types (Table 1, small η setting) is genuinely strong evidence that the theoretical forms capture the actual learned weights under the conditions tested.

## Weaknesses

### Fatal
None.

### Major

1. **Full-batch gradient descent theory vs. SGD experiments.** The theory is developed under full-batch gradient descent (Section 3.3, line 84: "We analyze the evolution of the parameters under full-batch gradient descent"), but the main validation experiments (Section 5.1, line 210) use SGD with batch size 2048. Stochastic gradient noise changes the effective dynamics and could disrupt the leading-term expansion, especially for higher-order terms (V at O(η²), W at O(η⁴)) where small parameter updates compete with fluctuations. The paper neither acknowledges this mismatch nor provides any argument (e.g., that batch 2048 approximates full-batch gradients on this dataset). This means the experimental validation tests a different optimization procedure from what the theory addresses.

2. **Formal guarantee covers ~5–6 gradient steps; validation covers 100 epochs.** For the TinyStories setup (T=200, L=3, η=0.005), Theorem 4.1's validity condition gives s ≤ η⁻¹·min(5/(8√T), 1/(12L)) ≈ 5.6 steps. For η=0.05, the bound gives s ≤ ~0.56 — not even covering the first gradient update. Yet the experiments validate for 100 epochs (thousands of parameter updates). The paper notes (line 210) that features "remain informative well beyond" the formal range, but this is an empirical observation, not a theoretical result. The core claim — that the theory *explains* how semantic associations emerge during training — is only formally supported for the first handful of steps. The persistence of agreement at later steps is a phenomenon in need of its own explanation.

3. **No baseline comparisons.** The paper validates by computing cosine similarity between theoretical and learned weights, but never tests whether simpler alternatives would fit equally well. For example: would a simple uncentered bigram count matrix (without the subtractive centering term -P(e_i)/|V| in Eq. 9) show comparable cosine similarity to W_O? Would a random matrix with the same Frobenius norm? For the Pythia experiments, would the covariance matrix of embeddings from an *untrained* model show significant similarity simply because data statistics are reflected in embedding geometry? Without controls, it is unclear whether the specific functional forms are uniquely supported or whether any reasonable data statistic would show comparable agreement.

### Minor

4. **Pythia validation is indirect.** Because Pythia-1.4B uses multi-head attention and MLP layers (absent from the theoretical model), the paper compares covariance matrices of embeddings and attention maps rather than the weights themselves. Two very different matrices can have similar covariance structures. The results also show poor agreement for early layers (Layer 0–2 in attention mapping, Figure 6), which the paper attributes to "slower" learning but could equally indicate the theory's predictions do not hold there. The paper acknowledges the architectural gap (line 236), which is appropriate, but the indirectness limits how much evidence this experiment can provide for the core claims.

5. **Error bound for W (QK) has a multiplicative T factor.** In Eq. (7), the leading term for W is O(s⁴η⁴), while the error is O(s⁵η⁵T). The ratio error/leading is O(sηT). With T=200, this imposes a tighter constraint for the bound to be meaningful than the formal validity range suggests. The paper does not discuss whether these bounds are tight or whether the actual error is much smaller.

6. **Initialization for the 3-layer experiment is unstated.** Theorem 4.1 assumes "sufficiently small Gaussian initialization" (with zero initialization also covered in Theorem D.10). The TinyStories experiment (Section 5.1) does not state which initialization was used, making it difficult to verify that experimental conditions satisfy the theorem's assumptions.

7. **Table 1 and surrounding text are ambiguous about which learning rate corresponds to which result.** Table 1 reports minimum cosine similarities >0.998 for "(small η)," while the text mentions 0.9 (30 epochs) and 0.7 (100 epochs) — apparently for the η=0.05 setting — but the distinction is not clearly drawn. Clarifying which numbers correspond to which setting would help.

8. **Qualitative examples in Figure 5 are cherry-picked.** The paper shows selected tokens from "top 30 correlated tokens" under each basis function without quantitative evaluation (e.g., fraction of tokens with semantically coherent top-30 lists, or a word similarity benchmark). This makes the qualitative analysis illustrative but not evidential.

### Trivial
None.

## Nice-to-Haves
- Report statistical significance (error bars, variance across runs or heads) for experimental results.
- Provide a theoretical discussion — even informal — of why the leading terms might persist beyond the formal validity range.
- Compare the theoretical weight forms against simple baselines (raw bigram matrix, random matrix with same norm, principal components of data statistics).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **MLP ablation hypothesis presented as a weakness:** The harsh critic claimed the MLP hypothesis was presented "as a result without supporting evidence." The paper explicitly calls it "one possible hypothesis" (line 265), making this transparent. REMOVED.
- **"First" claim needs qualification:** The reviewer notes the novelty claim (line 33) needs qualification. Without external knowledge to verify related work, I cannot assess whether this is accurate. REMOVED per hard rules.
- **Missing experimental details (embedding dimension, number of heads):** These are stated to be in Appendix C (removed by parser). REMOVED per hard rules.
- **Stronger/fatal framing of theory-experiment gap:** The harsh critic described the theory-experiment gap as potentially "fatal." It is a significant major weakness but not fatal — the core theoretical contribution stands; what is undermined is the directness of the validation. RECLASSIFIED as Major.

## Novel Insights

One observation from the harsh review that goes beyond the paper's own framing: the differential timescale prediction (W_O at O(η), V at O(η²), W at O(η⁴)) is not just an interpretability result but also a testable hypothesis about neural network training that could be probed with much larger models and different optimizers. If the leading-term framework generalizes, it predicts that output matrices should specialize first, value matrices second, and QK matrices last — a temporal ordering that has not been systematically studied at scale. The paper's current validation on Pythia does not directly test this prediction, which would be a natural direction for future work.

## Suggestions
1. Either (a) prove that the leading-term analysis holds under SGD with sufficiently large batch size, or (b) run the 3-layer experiment with full-batch GD to directly test the theoretical conditions.
2. Add baseline comparisons: compare theoretical weight forms against (a) randomly initialized weight matrices, (b) raw uncentered bigram matrices, (c) principal-components truncation of data statistics.
3. Provide a discussion (even informal) of why the leading terms might persist beyond the formal validity range, e.g., by showing higher-order corrections remain bounded or the dynamics converge near the leading-term direction.
4. State the initialization scheme used for the TinyStories experiment explicitly.
5. Clarify which experimental results correspond to which learning rate setting in the text.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>