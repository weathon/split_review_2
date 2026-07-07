Now let me produce the final consolidated review.

## Summary

This paper addresses the underexplored problem of Test-Time Adaptation (TTA) for Vision-Language Models under long-tailed test distributions. It proposes L-TTA, a method with three co-designed components: Synergistic Prototypes (SyPs) with Deterministic and Exclusionary Prototypes to enrich tail-class representations, Rebalancing Shortcuts (RSs) with a class re-allocation loss for dynamic adaptation, and Balanced Entropy Minimization (BEM) to counteract head-class bias in entropy minimization. The method is evaluated across 15 datasets, three benchmarks (OOD, Cross-Domain, Corruption), three imbalance ratios (10/20/50), and five backbone architectures, consistently outperforming 12 baselines.

## Strengths

1. **Novel problem framing with grounded failure-mode analysis.** The paper identifies two failure modes specific to VLM long-tailed TTA — text-induced tail erosion and modality-bias amplification (Figure 1) — and designs components explicitly motivated by these observations. This grounded connection between identified failure and proposed remedy is a structural strength that goes beyond a simple application of existing long-tailed techniques to the TTA setting.

2. **Extensive and well-structured evaluation.** Experiments span 15 datasets across OOD, Cross-Domain, and Corruption benchmarks, with three imbalance ratios (10/20/50), five backbones (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG), and 12 baselines. Macro-F1 is reported alongside accuracy, which is appropriate for long-tailed settings. The reported gains, while modest in some settings (1–3%), are consistent across benchmarks — L-TTA achieves the best results on most dataset × imbalance combinations.

3. **Thorough ablation and sensitivity analysis.** Table 6 ablates each component (DPs, EPs, RSs, BEM) individually and in combination, confirming all three contribute. Figure 4 systematically varies the key hyperparameters (λ₁, λ₂, η, K, β). Table 7 tests robustness to dynamic head/tail-class shifts, addressing temporal ordering concerns. The ablation study is more comprehensive than many comparable TTA papers.

4. **Theoretical propositions address a real gap.** Proposition 1 formalizes why standard EM amplifies head-class bias under long-tailed conditions, and Proposition 2 claims BEM reduces this gap. Even without verifying the deferred proofs, these propositions articulate clear testable claims about the method's mechanism.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or uncertainty reported despite 5 runs.** Tables 1–3 and 5 state "5 runs for each experiment" but report only point estimates without standard deviations, confidence intervals, or significance tests. Several gains over strong baselines are modest (e.g., Table 1, imb=50 OOD Average: L-TTA 64.68 vs. DPE 63.71, ~1%; ImageNet-A: L-TTA 60.07 vs. DPE 60.21 — DPE actually wins). Without variance estimates, the reader cannot distinguish genuine improvement from noise. This is especially important for macro-F1, which is more sensitive to tail-class changes. The paper's central empirical claim of "superior performance" is weakened by this omission. (This is a common issue in the field, but still a significant gap for a paper whose main evidence is empirical.)

2. **Hyperparameter inconsistency: K = 0.3 used in main experiments vs. K = 0.2 reported as optimal.** The Implementation Details (Section 4) state "K = 0.3", but the ablation (Section 4.2, Figure 4.c) varies K from 0.1 to 1 and reports "setting K = 0.2 yields the best performance." If these refer to the same parameter, the main experiments use a suboptimal value. Additionally, K = 0.3 does not make sense as an integer count of hyper-class vectors — the ablation range (0.1–1.0) suggests K is a fraction rather than an integer, but this is never stated. This harms reproducibility.

3. **CRA loss uses a non-differentiable argmax without comment.** Eq. 7 defines c_{c,j}(v) = 𝟙(j = Argmax_{j'}(Attn([v_c, t_c], q_{j'}))), a hard indicator with zero gradient almost everywhere. The paper mentions no technique to handle this (straight-through estimator, Gumbel-Softmax, soft assignment). While the loss can still be optimized through the avg_c(Attn(·, q_j)) term, the c_{c,j} term either receives no gradient or receives incorrect gradients. The optimization of the CRA loss is incompletely specified.

### Minor

4. **Exclusionary Prototype mechanism lacks empirical analysis despite a strong interpretability claim.** The paper states EPs store "the most improbable features of each class" (line 98). Eq. 5 updates every class's EP with the same visual embedding f(ẋ_i), where φ_c modulates the old prototype's weight (N − φ_c) rather than the new sample's weight. The paper provides no visualization of EP embeddings (e.g., t-SNE), no EP-class correlation analysis, and no ablation showing the φ_c weighting scheme matters more than a simple average. The mechanism's stated motivation may not match how it actually functions. Ablation (Table 6) confirms EPs help empirically, but the interpretability claim is unsupported.

5. **BEM prior estimation creates a potential self-reinforcing loop.** The class prior π is "continually updated based on the current predicted pseudo-labels" (Eq. 9, line 138). If the model over-predicts head classes early in the stream (as is natural under long-tailed distributions), the estimated π will overestimate head-class frequency. The paper does not analyze this feedback loop's stability or the reliability of the prior estimates. The head/tail shift experiment (Table 7) partly addresses ordering sensitivity but does not validate the prior estimates themselves.

6. **Undefined symbol P̃ in Eq. 9.** The symbol P̃ is used in Eq. 9 without explicit definition — it presumably refers to the prediction probability from Eq. 8, but this should be stated.

### Trivial
7. The "Harmonic Mean of Accuracy and Macro-F1" in Table 4 is labeled under "efficiency" but conflates two performance metrics; runtime and memory are reported separately, making this column unnecessary and potentially misleading.

## Nice-to-Haves
- Add standard deviations to all main tables (the 5 runs are already performed).
- Analyze what EPs actually learn (t-SNE visualization, EP-class correlation matrix, ablation of φ_c weighting).
- Clarify gradient handling for the argmax operation in CRA loss (Eq. 7).
- Analyze the BEM prior estimation loop: correlation between estimated π and true class frequencies over the stream; sensitivity to initialization of π.
- Resolve the K = 0.3 vs. K = 0.2 discrepancy and clarify whether K is a fraction or integer count.
- Define P̃ explicitly in Eq. 9.

## Removed Points

These points are flagged to be removed — treat them with caution:
- **The critic's specific mathematical description of EP weighting was inaccurate.** The critic claimed the sample embedding f(x) is "weighted by φ_c" for different classes, but the equation shows f(x) always contributes with weight 1; φ_c modulates the OLD prototype's weight (N − φ_c), not the new sample's weight. The core concern (lack of EP analysis) is retained but re-framed above.
- **MTA identical accuracy observation** — This describes a baseline artifact, not a weakness of L-TTA.
- **"First attempt" claim softening** — A stylistic suggestion, not a substantive weakness.
- **Data stream ordering underspecified** — Partially addressed by Table 7 (head/tail shift experiment). Moved to nice-to-have.
- **Missing related works** — Not verified; the paper cites relevant non-i.i.d. TTA work (SAR, DA-TTA, DELTA, LAME) and distinguishes its VLM-specific focus.
- **Affinity function not fully explained** — Minor; merged into the undefined symbol point.

## Novel Insights

The reviews collectively highlight a tension not fully resolved in the paper: the Exclusionary Prototypes have an intuitive but potentially misleading verbal description that may not match their mathematical behavior. Eq. 5 updates every class's EP with the same visual embedding, differing only in how heavily the old prototype is discounted (via φ_c). This means EPs across classes are all averages over the same pool of visual features with different discount rates — raising a legitimate question about how discriminative they can be in practice. The paper's empirical results show they work, but the mechanism may be more prosaic (a form of soft negative mining) than the "most improbable features" framing suggests. This is worth deeper analysis.

## Suggestions
- Add standard deviations to Tables 1, 2, 3, and 5.
- Resolve the K = 0.3 vs. K = 0.2 discrepancy and clarify the parameter semantics.
- Add a discussion of gradient propagation through the CRA loss argmax.
- Include EP embedding analysis (t-SNE, correlation matrix) to validate the stated motivation.

## Score and Decision

**Bracket determination (Round 1):** The strongest comparable anchors are: (a) lF9QXpfNHm (avg 4.67, "Open-world TTA for VLMs") — similar topic, but that paper had weaker novelty (incremental over TDA) and missing baselines; L-TTA is stronger in problem framing and evaluation scope; (b) yD2JMeKumt (avg 6.00, "DOTA: Distributional TTA") — also similar topic; that paper had cleaner methodology but less thorough ablation and sensitivity analysis; L-TTA has similar-level issues (specification gaps, no error bars) but more extensive experiments; (c) eXrUdcxfCw (avg 4.80, "Continual TTA with prototypes") — had major concerns about lack of innovation and marginal improvements; L-TTA is clearly stronger in novelty.

**Narrowing (Round 2):** Itemizing these anchors reveals that L-TTA shares the "no error bars" weakness of weaker papers (lF9QXpfNHm at 4.67 flagged this as weight=-1; eXrUdcxfCw at 4.80 had marginal improvements flagged as weight=-4). However, L-TTA has stronger novelty and evaluation breadth than these anchors, placing it above 4.8. The cleanest comparison is to yD2JMeKumt (6.00), which shared similar specification issues but lacked L-TTA's ablation thoroughness. L-TTA's additional methodological gaps (CRA argmax, K inconsistency, EP analysis gap) push it slightly below 6.0.

**Final score: 5.5.** The paper tackles a genuinely novel problem with an extensive evaluation campaign and thorough ablation studies. However, the absence of variance reporting, the hyperparameter inconsistency (K=0.3 vs. K=0.2), the underspecified CRA loss optimization, and the unanalyzed EP mechanism collectively prevent full confidence in the presented narrative. These issues are fixable, but as presented, the paper sits between borderline reject and borderline accept.

**Decision: Reject** (borderline; the paper needs to address the major weaknesses before acceptance).

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>