Now I have enough calibration context. Let me produce the final review.

## Summary

This paper proposes L-TTA, the first method for online test-time adaptation of vision-language models under long-tailed test distributions. The method has three co-designed components: Synergistic Prototypes (two types of prototypes that accumulate visual features to enrich tail-class representations), Rebalancing Shortcuts (learnable cross-attention with hyper-class vectors regularized by a class re-allocation loss), and Balanced Entropy Minimization (a modified entropy objective that down-weights confident head-class predictions via a penalty term). The paper evaluates extensively across 15 datasets, three benchmarks (OOD, Cross-Domain, Corruption), three imbalance ratios, and five backbones, showing consistent improvements over baselines.

## Strengths

1. **First study of a genuinely underexplored setting.** While TTA for VLMs and long-tailed learning are active areas, their intersection — online TTA where the test stream itself follows a long-tailed distribution — has not been studied. The paper clearly motivates why this matters: real test distributions are rarely balanced, and the online one-epoch nature of TTA precludes standard long-tailed remedies (up-sampling, data augmentation). This framing is the paper's strongest contribution.

2. **Two specific, VLM-specific failure modes are identified.** "Text-induced Tail Erosion" (Sec. 1) and "Modality-bias Amplification" go beyond generic "long tail is hard" and point to mechanisms specific to VLM architectures — text priors that persist into test predictions and unimodal TTA methods that worsen cross-modal misalignment. These observations are insightful regardless of the specific method proposed.

3. **Extensive and well-structured evaluation.** The paper evaluates on three benchmarks across 15 datasets at three imbalance ratios (10, 20, 50) and five backbones (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG). The inclusion of macro-F1 alongside accuracy is appropriate for the long-tailed setting. This is substantially more thorough than typical TTA papers, and the efficiency comparison (Table 4) shows L-TTA achieves strong results with reasonable compute (1.45h, 1.89G).

4. **Consistent empirical advantage.** L-TTA outperforms baselines on nearly every dataset × imbalance ratio × backbone combination across all three benchmarks. The improvements are modest (typically 1–3% in accuracy and macro-F1) but consistent — a pattern that holds across all benchmarks and backbones. The method is particularly strong on macro-F1, which directly reflects its balancing capability.

## Weaknesses

### Major

1. **Inconsistency and ambiguity in the $K$ hyperparameter.** $K$ is introduced as the *number* of hyper-class vectors (Eq. 6, line 112: "assume there are $K$ hyper-class vectors $\mathbf{q} = \{\mathbf{q}_j\}_{j=1}^K$"), but takes fractional values throughout: the main experiments use $K=0.3$ (line 208), and the ablation varies $K$ from 0.1 to 1.0 (line 334). Moreover, the ablation identifies $K=0.2$ as yielding the best performance (line 334), yet the main experiments use $K=0.3$ without explanation. The figure caption also refers to this hyperparameter as "$b$" (Figure 4.c). These issues must be resolved for reproducibility: clarify whether $K$ is a count or a fraction (e.g., proportion of classes), and explain or correct the discrepancy between the ablated optimal value and the value used in main experiments.

### Minor

2. **Undefined symbol in the core loss function.** Equation 9 defines $\mathcal{L}_{\text{BEM}} = \mathbb{H}'(\tilde{\mathbb{P}}) = -\sigma(z') \log(\sigma(z'))$ with $z' = z - (1 - \tilde{\mathbb{P}})^\beta \log(\pi/\sum_i \pi_i)$. The symbol $\tilde{\mathbb{P}}$ appears on both sides but is never defined in the main text. Based on context it is almost certainly the softmax probabilities (likely $\mathbb{P}_{\text{LTTA}}$ from Eq. 8), but this should be stated explicitly for reproducibility.

3. **Theoretical propositions lack main-text rigor.** Proposition 1 (line 132) asserts $\mathbb{E}_{i \sim C_{\text{head}}} \nabla_{z_i} \mathbb{H} < 0 < \mathbb{E}_{i \sim C_{\text{tail}}} \nabla_{z_i} \mathbb{H}$ and Proposition 2 (line 140) claims BEM reduces the head-tail gradient gap. The proofs are deferred to the appendix, but the main text does not specify the distribution over which the expectations are taken or the assumptions under which these claims hold. The paper would benefit from either including a sketch of the assumptions in the main text or explicitly framing these as intuitive motivations rather than formal propositions.

4. **CRA loss's claimed effect is unverified.** The paper states that the Class Re-Allocation loss (Eq. 7) "results in discernable feature clustering and reducing dominance of head-class prototypes" (line 120) but provides no direct empirical evidence — no attention visualizations, measurement of expert utilization entropy, or analysis isolating CRA's effect from BEM are provided. The ablation (Table 6) compares SyP+RS vs. SyP+RS+BEM, which does not isolate CRA since BEM also changes the objective. The CRA formulation (minimizing the dot product of average expert counts and average expert activations) could theoretically admit degenerate solutions where experts are uniformly inactive rather than uniformly utilized, but this is not discussed.

5. **Test set construction caveat may affect actual imbalance ratios.** The paper states (line 206): "if the calculated cardinality is less than the class cardinality itself, we simply keep that class unchanged." For datasets with inherently small class sizes (e.g., Aircraft with ~100 samples across 100 classes), this means the actual imbalance ratio may be substantially lower than the stated value (10, 20, or 50). The paper does not report the achieved imbalance ratios per dataset, making it difficult to assess whether the controlled variable is consistent across datasets and conditions.

6. **No variance reporting despite 5 runs and modest margins.** The paper states "5 runs for each experiment" but reports only point estimates in all main tables (Tables 1–3). Given the modest improvement margins (typically 1–3%), standard deviations or confidence intervals would be informative, especially for the Corruption Benchmark where some baselines show large variability.

### Trivial

7. **Variable naming inconsistency.** The hyper-class vector count is called $K$ in the text (lines 112, 208, 334) but "$b$" in the Figure 4.c caption.

## Nice-to-Haves

- Reporting head vs. tail accuracy breakdowns (currently deferred to Appendix C) in the main paper would directly support the core claim that L-TTA improves tail-class performance.
- An empirical analysis verifying that CRA actually produces more balanced expert assignments (e.g., entropy of attention distributions across hyper-class vectors).
- Clarifying whether the model state resets between test streams (i.e., whether the same model processes each dataset independently).

## Removed Points

These points are flagged to be removed, treat them with caution.

- The Harsh Critic's gradient analysis of Proposition 1 contained a sign error in the claimed formula for $\partial \mathbb{H}/\partial z_i$. The core criticism about the proposition lacking specification of the expectation distribution is valid and retained in Weakness 3.
- The criticism that "proof is in the appendix and cannot be inspected here" is a parser artifact (the appendix is stripped from PDF extraction). The criticism about main-text presentation rigor (not the missing proof) is retained.
- Criticisms about missing related works removed per rules (no external sources to verify).
- Pure formatting and presentation nitpicks removed.
- The criticism that the paper studies a "constructed" long-tailed stream rather than naturally long-tailed data is removed — subsampling to create controlled imbalance ratios is standard practice in long-tailed learning literature.

## Novel Insights

The observation that TPT and C-TPT show relatively minor variations with imbalance ratio because they do not accumulate temporal knowledge (Sec. 4.1) is a genuine insight — methods with memory (prototypes, caches) are more susceptible to long-tailed accumulation effects. This observation is worth deeper analysis and could inform future TTA method design more broadly.

## Suggestions

1. **Resolve the $K$ inconsistency.** Clarify whether $K$ is an absolute count or a fraction (e.g., proportion of classes). Explain why $K=0.3$ is used in main experiments when $K=0.2$ is identified as optimal in the ablation. Use consistent notation ($K$ vs. $b$) throughout.
2. **Define $\tilde{\mathbb{P}}$ explicitly** when introducing Eq. 9.
3. **Reframe Propositions 1 and 2** as empirical motivations in the main text, or include the key assumptions needed for the claims to hold.
4. **Report achieved imbalance ratios** for all datasets, especially smaller ones like Aircraft and DTD, to verify that the target imb values (10, 20, 50) are approximately realized.
5. **Add standard deviations or confidence intervals** to the main tables.
6. **Include a brief analysis of CRA's effect** — even a simple entropy measurement of attention distributions across hyper-class vectors would verify the claimed balancing behavior.

## Score and Decision

**Calibration details:**

All retrieved anchor papers (from 3 calibration rounds across ~30 queries):

| Paper | Avg Score | Round | Comparison to L-TTA |
|---|---|---|---|
| Active TTPT (pdzHpQbGrn) | 2.50 | R1 | Weaker novelty, marginal improvements; L-TTA has stronger problem framing and evaluation |
| LVLM-CL (JIlIYIHMuv) | 2.50 | R1 | Continual learning for LVLMs, narrower scope |
| BLG (BUDxvMRkc4) | 4.67 | R1 | Long-tailed CLIP, but for offline classification not TTA |
| Efficient Open-world TTA (lF9QXpfNHm) | 4.67 | R1 | Related open-set TTA for VLMs |
| Demystifying LT in LVLMs (9RnTw9YiXV) | 4.40 | R1 | Analysis paper on long-tail in LVLM training data |
| InCPL (Rc3RP9OoEJ) | 5.00 | R1 | Test-time prompt tuning, narrower scope |
| Learning w/o Forgetting for VLMs (k9NYnsC4Mq) | 5.67 | R2 | Continual learning for VLMs; L-TTA has stronger evaluation |
| C-CLIP (sb7qHFYwBc) | 6.50 | R2 | Multimodal continual learning; L-TTA comparable in scope and novelty |
| **DOTA (yD2JMeKumt)** | **6.00** | R1,R2 | **Most similar: TTA for VLMs with distribution estimation. L-TTA has clearer methodology, stronger problem framing, and more extensive evaluation, but both have clarity issues.** |
| RLCF with CLIP Reward (kIP0duasBb) | 6.67 | R1 | TTA with CLIP as reward; accepted. L-TTA addresses a different problem (long-tailed) |
| ML-TTA BEM (75PhjtbBdr) | 6.25 | R1 | Multi-label TTA with modified entropy; accepted despite clarity concerns |
| Adapting MLLM to Concept Drift (b20VK2GnSs) | 7.00 | R2 | Concept drift & long-tail; accepted. L-TTA similarly novel but with more presentation issues |
| Black Sheep (g1fkhbhHjL) | 7.00 | R2 | Spurious correlation in VLMs; less directly comparable |
| Test-time Adapt Multi-modal Reliability (TPZRq4FALB) | 8.00 | R1 | Multi-modal TTA, stronger analysis depth |

**Round 1 bracket:** Between 4 and 7 (papers addressing TTA or long-tailed learning for VLMs range from 4ish to 7ish).

**Round 2 narrowing:** Comparing directly to DOTA (6.00, Rejected) and C-CLIP (6.50, Accepted), L-TTA has a stronger problem framing (first to identify the long-tailed TTA setting for VLMs) and more extensive evaluation (15 datasets, 5 backbones vs. DOTA's 10+ datasets, 2 backbones). However, L-TTA has more presentation clarity issues (undefined symbol, K inconsistency, overclaimed propositions) than C-CLIP. The issues are fixable and do not undermine the core empirical contribution.

**Final score: 6.0** — The paper identifies a genuinely new and important problem, provides a well-motivated solution, and evaluates it with unusual thoroughness. The weaknesses are real but addressable (primarily presentation clarity and one reproducibility-affecting hyperparameter inconsistency). With revisions addressing the $K$ issue, undefined notation, and better-scoped claims, this would be a solid contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>