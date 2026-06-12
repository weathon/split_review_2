Good. Now I have a clear calibration picture. Let me finalize:

**Round 1 bracket: 4.0–5.0**

FF-Erase is above Meta-Unlearning (4.0) due to better problem formulation, more systematic evaluation (GA sweep, ablation), and genuine first-mover status. It is below Contrastive Unlearning (5.0) and SPE-Unlearn (5.0) due to more severe evaluation concerns (G-MIA near chance, single main-text dataset, limited baselines). It sits alongside Blind Unlearning (3.6) and Auditing Privacy (4.2) in terms of having novel ideas but evaluation gaps.

**Final score: 4.5**

Now let me write the final review.

---

## Summary

This paper proposes FF-Erase, the first machine unlearning framework designed specifically for Forward-Forward (FF) models, along with G-MIA, a goodness-based membership inference attack for unlearning verification. The core method uses a guidance model (via mini-retraining or fast distillation) to provide target goodness distributions, then applies KL-divergence minimization to shift the original model's layer-wise goodness scores away from the forgetting data while periodically recovering on remaining data.

## Strengths

- **First formalization of FF unlearning with well-motivated problem identification.** The paper clearly articulates two unique challenges for FF models (parameter sensitivity and layer-wise independent training) and supports these with concrete evidence: Figure 5 systematically sweeps λ ∈ {10¹, 10⁰, 10⁻¹, 10⁻², 10⁻³, 0} showing GA either collapses (utility below 60%) or fails to unlearn (G-MIA scores 0.60–0.61), providing rigorous evidence that the problem cannot be solved by tuning existing methods.

- **Control experiment validates guidance model necessity.** Table 1 (R.G.M. row) shows that using a randomly initialized guidance model causes catastrophic degradation (Acc_t drops from ~80% to 55.53%), empirically confirming that both the guidance model design and the FF-specific approach are essential, not just cosmetic choices.

- **G-MIA outperforms existing black-box MIAs on fully-trained models.** Figure 3 shows G-MIA consistently outperforms FL-MIA across all architectures and datasets (TinyCNN, AlexNet, VGG13), and achieves competitive accuracy with white-box MIAs on deeper models (VGG13/CIFAR-100), demonstrating that goodness-based features capture membership information beyond what standard black-box attacks access.

- **Comprehensive ablation on guidance model hyperparameters.** Table 1 systematically varies α₁ ∈ {0.3, 0.5} and α₂ ∈ {0.1, 0.2, 0.5} for both strategies, providing actionable efficiency-performance trade-off insights with detailed time decomposition (t₀ vs t_unl − t₀).

- **Concrete efficiency gains with rigorous time breakdown.** Table 1 separates guidance model acquisition time from goodness-decrease time, showing FF-Erase achieves unlearning in 29–39% of retraining time with time breakdowns that enable practitioners to estimate costs for their settings.

## Weaknesses

### Fatal

None

### Major

- **G-MIA verification scores are barely above chance, undermining the central verification claim.** The paper's second key contribution is G-MIA as a reliable verification tool. However, the reported G-MIA ACC scores in the unlearning verification scenario are near the 0.5 random baseline: retraining (gold standard) achieves 0.532 in Figure 4(c) and 0.551 in Table 1; FF-Erase variants range from 0.5245 to 0.587. These margin-of-noise differences mean the attack cannot reliably distinguish members from non-members after unlearning. While G-MIA works well for general membership inference on fully-trained models (Figure 3), its near-chance performance in the verification context means the paper cannot rigorously demonstrate that FF-Erase actually removes information rather than behaving like a well-generalizing model. The paper claims G-MIA provides "a reliable tool for unlearning verification," but the verification-scenario numbers contradict this.

- **Same-distribution random forgetting setup conflates unlearning with generalization.** The experimental design randomly samples 20% of training data as D_forget, sharing the same distribution as D_test. The paper acknowledges: "effective unlearning algorithms will produce models that their accuracy on D_forget are similar to the original model's accuracy on D_test." FF-Erase achieves 81.31% on D_forget vs RE's 81.61% — essentially identical. But a model that simply failed to memorize specific samples would also achieve ~80% on D_forget due to generalization. Since G-MIA (the intended bridge for this gap) is itself near chance, the combination of same-distribution setup and weak verification leaves the evidence for actual unlearning circumstantial.

- **Only one failing baseline compared alongside retraining.** The only methods compared are retraining (gold standard) and gradient ascent (which the paper shows fails for FF models). No comparison against any adapted approximate unlearning method — no Fisher forgetting, no knowledge-distillation-based approaches adapted for FF, no SISA-style sharding. This creates a comparison where FF-Erase is the *only* working method, which is uninformative about its relative merit. Even simple adaptations (per-layer GA with independent learning rates, or random-label unlearning) would strengthen the evaluation.

### Minor

- **Main-text experiments limited to a single dataset-model pair.** Only VGG13 on CIFAR-10 appears in the main text (§6.2–6.4); all other results are deferred to appendices. For a paper claiming "extensive experiments," this limits the reader's ability to assess generalizability without consulting supplementary material.

- **No statistical significance or variance reporting.** No error bars, no multiple seeds, no confidence intervals. Given that G-MIA differences between FF-Erase and retraining are ~0.01–0.03, variance reporting is critical to determine if these differences are meaningful.

- **G-MIA methodology does not address potential distribution shift between shadow and target models.** The shadow model is trained on synthetic data while the target model is trained on real data. This distribution gap could explain why G-MIA produces near-chance scores in the verification scenario, but the paper does not discuss or diagnose this as a potential cause.

### Trivial

None

## Nice-to-Haves

- Testing at smaller forgetting rates (1%, 5%, 10%) in addition to the 20% used, as typical unlearning scenarios involve much smaller sets.
- Hyperparameter sensitivity analysis for K, η, λ, E, ε₁, ε₂ beyond the α₁/α₂ ablation.
- Investigation of why G-MIA scores are near chance in the verification scenario — if the low scores actually indicate successful unlearning (attack can't distinguish members), this should be explicitly analyzed with appropriate statistical tests.
- More nuanced exploration of GA baselines (per-layer learning rates, scheduled λ) rather than a single global λ sweep.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"FF-Erase achieves higher test accuracy than retraining (80.85 vs 77.87)"** — This was a factual misreading by the harsh critic. Table 1 clearly shows RE Acc_t = 80.85 and D-(0.3,0.5) Acc_t = 77.87. FF-Erase has *lower* test accuracy than retraining, which is expected and not counterintuitive.
- **"Efficiency analysis is misleading"** — The harsh critic argued that guidance model training dominates time, making the speedup "misleading." However, the paper explicitly decomposes t_unl into t₀ and t₁ in Table 1 and §4.3, and the speedup (1.9–3.1×) refers to total time vs retraining, which is the correct practical comparison.
- **"Algorithm 1 notation inconsistency"** — Minor notation clarification about FFwd inputs; the algorithm is functional if slightly imprecise in notation.
- **"20% forgetting rate is unusually large"** — Valid suggestion but a nice-to-have, not a weakness.

## Novel Insights

The paper makes a genuine first contribution by identifying that FF models' layer-wise independent training creates unique challenges for unlearning that cannot be solved by simple adaptation of BP-based methods. The systematic λ-sweep for GA (Figure 5) is particularly valuable — it exhaustively demonstrates that no single λ value works (either collapse or failure to unlearn), which is a strong empirical contribution that will benefit future work on FF unlearning regardless of the fate of FF-Erase itself. The R.G.M. ablation showing that unguided approaches catastrophically fail provides clear design insights for the community.

## Suggestions

- Strengthen G-MIA by exploring alternative threat models (e.g., class-specific forgetting where D_forget comes from a different class distribution) that would naturally create more separable member/non-member distributions.
- Add at least one adapted baseline beyond GA (e.g., per-layer GA with independent learning rates, or knowledge distillation from a model trained only on D_remain).
- Report results on at least 2–3 dataset-model combinations in the main text to substantiate the "extensive experiments" claim.
- Investigate and explicitly discuss why G-MIA scores are near chance in the verification scenario — consider whether this actually indicates successful unlearning and provide supporting analysis.
- Add variance reporting (multiple seeds) especially for G-MIA comparisons where differences are marginal.

## Reporting

**All anchors retrieved:**
- Round 1:
  - `5lUdTogEL3.md` (1.00) — Clothing-ReID paper, unrelated topic, very low score
  - `5kMwiMnUip.md` (1.40) — Jailbreaking LLMs, unrelated
  - `Uj0h13lVrR.md` (1.00) — GFlowNets, unrelated
  - `hwXUmwJAq5.md` (3.00) — UGradSL: gradient-based unlearning, similar domain, weaker novelty
  - `85X9awoVtv.md` (2.50) — Data withdrawal auditing, related domain
  - `Xagys9QD3T.md` (3.00) — Pseudo-Probability Unlearning, similar domain
  - `drrXhD2r8V.md` (5.00) — SPE-Unlearn: structure-aware unlearning for Transformers, architecture-specific like FF-Erase
  - `lgnAEBE1Xq.md` (5.00) — Contrastive Unlearning: novel framework, comprehensive experiments
  - `pUOesbrlw4.md` (5.25) — Deep Unlearning: SVD-based class unlearning, strong results
  - `xmQuUqSynb.md` (5.75) — Rethinking Adversarial Robustness: unlearning + security
  - `wAemQcyWqq.md` (5.67) — Oblivious Unlearning: privacy-preserving unlearning
  - `Hj1D0Xq3Ef.md` (5.67) — Minority populations in LLM unlearning
  - `EUSkm2sVJ6.md` (7.60) — Dataset usage inference, higher tier
  - `P7KIGdgW8S.md` (8.00) — Holder stability, unrelated
  - `KbetDM33YG.md` (8.00) — Online GNN evaluation, unrelated
- Round 2:
  - `TLBPjECC5D.md` (5.25) — Unlearning via Sparse Representations
  - `okRSNTMdFg.md` (4.00) — Meta-Unlearning on Diffusion Models, similar novelty level with evaluation concerns
  - `Uv7bWrIucU.md` (4.20) — Auditing Privacy Protection of Unlearning
  - `7tpMhoPXrL.md` (4.80) — Forget Vectors at Play
  - `KEeTRb8GLf.md` (3.60) — Blind Unlearning
  - `E6rpTruK4v.md` (3.80) — CodeUnlearn
  - `KvFk356RpR.md` (4.80) — Unlearning Mapping Attack

**Round 1 bracket: 4.0–5.0.** FF-Erase is above Meta-Unlearning (4.0) due to more systematic evaluation and stronger problem formalization, but below Contrastive Unlearning (5.0) and SPE-Unlearn (5.0) due to more severe evaluation concerns (G-MIA near chance, single main-text dataset, limited baselines).

**Round 2 narrowing: 4.0–5.0 → 4.5.** The anchors in the 4.0–5.0 range confirm this placement. FF-Erase has stronger novelty than Meta-Unlearning (4.0) and Blind Unlearning (3.6), comparable novelty to Auditing Privacy (4.2), but more concerning evaluation gaps than Forget Vectors (4.8) or Unlearning Mapping Attack (4.8). Final score: 4.5.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>