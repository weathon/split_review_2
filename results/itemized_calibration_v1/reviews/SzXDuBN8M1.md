## Summary

This paper introduces TD-JEPA, a method for zero-shot unsupervised RL that uses a temporal-difference (TD) latent-predictive loss to learn state representations, task representations, policy-conditioned predictors, and latent-conditioned policies entirely from offline, reward-free transitions. The key algorithmic innovation is replacing the Monte Carlo target in prior latent-predictive losses (which requires on-policy trajectory data) with a bootstrapped TD target that can be estimated from off-policy, offline transitions (Eq. 7, 9). Theoretically, the paper shows that idealized variants of this loss have matching gradients with successor-measure factorization losses (Theorems 1–4), connecting latent-prediction to zero-shot RL. Empirically, TD-JEPA is evaluated on 65 tasks across 13 datasets with two observation modalities, showing competitive or state-of-the-art performance.

## Strengths

1. **Novel, well-motivated algorithmic contribution (Eq. 7, Section 3.1).** The TD-based latent-predictive loss directly addresses a genuine limitation of prior work: existing latent-predictive methods in RL are restricted to single-task, one-step, or on-policy data. Replacing the MC target with a bootstrapped TD target enables learning from arbitrary offline, off-policy datasets, substantially expanding the practical scope of these methods. This is not an incremental modification — it changes what data these methods can use.

2. **Gradient matching theoretical framework (Theorems 1 and 3, Section 4).** The paper shows that latent-predictive losses (both MC and TD variants) and successor-measure factorization losses have matching optimal predictors and matching gradients w.r.t. the representations. This is a nontrivial extension of prior theory (Tang et al., 2023) to the multi-policy, TD setting and provides a formal connection between latent-prediction and successor-feature-based zero-shot RL that is genuinely new.

3. **Broad and methodical empirical evaluation (Table 1, Figures 2–4).** The evaluation spans 65 tasks across 13 datasets (ExoRL and OGBench), 2 observation modalities (proprioception and pixels), and 7 baselines from 3 methodological families. The probability-of-improvement analysis (Figure 2) and ablations (Figure 3) are informative. The fast-adaptation experiments (Figure 4) demonstrate a practical downstream benefit: frozen pre-trained representations enable rapid online and offline fine-tuning, often matching or exceeding training-from-scratch within 400K steps.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Framing vs. evidence.** The abstract claims TD-JEPA "matches or outperforms state-of-the-art baselines ... especially in the challenging setting of zero-shot RL from pixels." Table 1 supports this: TD-JEPA is clearly best on DMC_RGB (628.8 vs. 582.4, non-overlapping CIs), ties on OGBench_RGB (41.34 vs. 41.58), ties on DMC proprio (661.2 vs. 648.2), and is slightly below FB on OGBench proprio (37.98 vs. 39.04). The conclusion is well-calibrated, but the abstract and introduction lean toward implying broader superiority than the evidence strictly shows. TD-JEPA is a strong, consistently competitive method that is unambiguously best in one challenging setting — this is a real contribution, and the framing should match it precisely.

2. **Three of seven baselines are novel implementations, not established methods.** BYOL*, BYOL-γ*, and ICVF* are described as "representation learning methods: their instantiation in a zero-shot framework is novel and designed to investigate the impact of different representations" (footnote 5). This is transparently disclosed, but it means the signature result (DMC_RGB advantage over BYOL-γ*) compares against a baseline the authors designed and tuned. However, TD-JEPA also performs strongly against established baselines (e.g., FB at 456.2 vs. TD-JEPA at 628.8 on DMC_RGB), which mitigates this concern substantially. The paper would be strengthened by reporting results for the original (unmodified) implementations of FB, HILP, and RLDP in parallel.

3. **Theoretical assumptions are strong.** Theorems 1–3 require (A1) orthonormal representations, (A2) uniform state distribution, and (A3) symmetric transition matrices. The symmetry assumption (A3), requiring reversible dynamics under each policy, is restrictive and does not hold in most practical environments. The paper acknowledges that these assumptions "have been considered in all these related works" and claims they "can be relaxed" via the appendix, but the appendix is stripped from the reviewed version. The theory provides intuition and formal connections rather than provable guarantees for the practical algorithm — this is standard in RL theory but should be kept in perspective.

4. **Missing experimental details.** (a) The number of seeds is not stated in the main text or table captions. (b) Compute requirements (training time, GPU hours) are not mentioned, which matters for practical adoption. (c) The BC regularization applied to OGBench (footnote 4) is deferred to the appendix without explaining in the main text whether it is applied uniformly to all methods or whether it interacts differently with different algorithmic components.

### Trivial
None.

## Nice-to-Haves

- A summary row showing average rank across all settings in Table 1 would improve interpretability.
- The inference procedure (linear regression to find z_r) does not discuss how many rewarded samples are needed for reliable estimation or how robust the procedure is to small inference datasets.
- Computing the constants c in Theorem 4 on actual learned representations to show the bound is non-vacuous would help bridge theory and practice.

## Removed Points

These points from the harsh critic input are removed with justification:

- **"Latent prediction is not auxiliary claim is overstated"** — Removed because the paper's architecture genuinely uses the latent-predictive predictor as the core object from which zero-shot policies are distilled; the actor loss (line 130) directly uses the predictor output. This claim is defensible.
- **"Probability of improvement bootstrap computation is unexplained"** — Removed because the paper states: "We report symmetrized 95% simple bootstrap confidence intervals. Dotted lines surround matches in which the improvement is statistically significant" (Figure 2 caption).
- **"Theorem 4 connection is overstated"** — Removed because the paper says "indirectly optimized" (line 190), which accurately describes the relationship (bounds → upper bounds → policy evaluation error).
- **Pure formatting, grammar, and typos** — Removed per instructions; these are parser artifacts.
- **Missing related work** — Removed per instructions (cannot verify existence of external sources).

## Novel Insights

Beyond the paper's own contributions, the reviews highlight that TD-JEPA's value proposition could be sharpened: rather than claiming broad superiority, the paper's strongest and most defensible claim is that TD-JEPA is clearly state-of-the-art on pixel-based DMC (a genuinely hard setting), matches the best methods elsewhere, and the theoretical gradient-matching framework is independently interesting as a connection between latent-prediction and successor-feature-based zero-shot RL. The fast-adaptation experiments (Figure 4) are also an underexploited strength — they show that the learned representations have practical value beyond zero-shot performance.

## Suggestions

1. State the number of seeds for all experiments in the main text or table captions.
2. Add a sentence in the main text clarifying whether the BC regularization in OGBench is applied uniformly to all methods.
3. Calibrate the abstract's opening claim to more precisely reflect that TD-JEPA's clearest advantage is on pixel-based tasks, while it remains competitive on proprioceptive tasks.
4. Include compute requirements (training time, GPU hours) for practical adoption.
5. Consider reporting results for original (unmodified) baseline implementations in parallel to address the concern about author-implemented baselines.

## Score and Decision

### Anchor Papers for Calibration

| File | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Uj0h13lVrR.md (KL GFlowNets) | 1.00 | R1 | No | Unrelated topic; not comparable |
| gwZ90hFSL2.md (Cross-lingual robots) | 1.00 | R1 | No | Unrelated topic; not comparable |
| fnO5h1CFyh.md (Hebbian SR) | 3.00 | R1 | No | Distant topic; much weaker empirically |
| X5qi6fnnw7.md (Conservative World Models) | 4.75 | R1 | Yes | Zero-shot RL + FB; limited novelty (CQL+FB); narrower evaluation; less novel than TD-JEPA |
| 9sOR0nYLtz.md (FB-CPR Humanoid) | 6.50 | R1 | Yes | Zero-shot RL + FB; less methodological novelty; narrower evaluation (humanoid only) |
| s9SVlWOcLt.md (Proto Successor Measure) | 6.75 | R1 | Yes | Zero-shot RL + successor measures; comparable theory, much weaker empirical work (2 environments vs. 65) |
| ms0VgzSGF2.md (Bridging State/History) | 6.75 | R2 | Yes | Self-predictive RL theory; weaker empirical evaluation; unifying framework rather than new algorithm |
| agPpmEgf8C.md (Predictive aux + brain) | 8.00 | R2 | No | Different contribution type (neuroscience connection); not directly comparable |

**Round 1 bracket:** After comparing against the 4.75, 6.50, and 6.75 anchors, the narrowest plausible range was [6.0, 7.5]. The 4.75 anchor (Conservative World Models) was below TD-JEPA on every relevant dimension (novelty, empirical breadth, theoretical depth). The 6.5–6.75 anchors (FB-CPR, Proto SM, Bridging State/History) each had a clear deficiency relative to TD-JEPA: FB-CPR had less novelty and narrower evaluation; Proto SM had much weaker empirical work; Bridging State/History was a unifying framework rather than a new algorithm. TD-JEPA combines genuine algorithmic novelty, nontrivial theory, and thorough empirical evaluation — none of the anchors in the 6.0–7.0 range match this combination.

**Narrowing:** The weighted-item comparison with the 6.75 anchors shows that TD-JEPA shares their positive heavy-weight items (novel theoretical connections, clean method) while lacking their negative heavy-weight items (weak empirical work in Proto SM, trivial results in Bridging State/History). The missing negative items push TD-JEPA above these anchors.

**Final score:** 7.0. This is a strong paper with a genuine algorithmic contribution, novel theory, and thorough empirical evaluation. The weaknesses are minor and correctable (framing calibration, missing experimental details) and do not threaten the core claims. The paper is clearly above the reject threshold and above the 6.0–6.5 borderline range.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>