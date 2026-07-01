Here is my final consolidated review:

---

## Summary

This paper introduces FF-Erase, the first machine unlearning framework for Forward-Forward (FF) models. It uses a guidance model to provide target goodness distributions, steering the original model to "forget" specific training data via KL-divergence minimization on layer-wise goodness vectors. The paper also proposes G-MIA, a membership inference attack that leverages FF-specific goodness signals for unlearning verification. Experiments on CIFAR-10/100, MNIST, and Fashion-MNIST with various architectures (TinyCNN, AlexNet, VGG13) show speedups of 1.9–3.1× over retraining.

## Strengths

1. **Genuinely novel problem identification.** The paper correctly identifies that machine unlearning for FF models is an unexplored problem and articulates specific challenges — FF models' sensitivity to parameter tuning due to the absence of consistent global update directions, and the difficulty of allocating per-layer forgetting pressure under independent layer-wise training (Section 1, ¶3-4). These challenges are well-reasoned and specific to FF architectures.

2. **Architecturally faithful unlearning mechanism.** The idea of shifting goodness distributions toward a guidance model's goodness via KL divergence (Section 4.1) is a natural adaptation of the FF paradigm: goodness is the native currency of FF models, so operating on goodness is architecturally coherent. Using KL divergence rather than direct goodness minimization is a deliberate design choice for stability. The ablation on the randomly-initialized guidance model (Table 1, R.G.M row, Acc_f=55.53%) convincingly shows the guidance model is doing meaningful work.

3. **FF-specific verification tool.** G-MIA uses layer-wise goodness vectors for membership inference — a genuinely new idea that exploits FF-specific signals no existing MIA captures. Figure 3 shows G-MIA consistently outperforms the standard black-box baseline (FL, using only final-layer output), and matches or beats white-box attacks on deeper models and complex datasets.

## Weaknesses

### Major

1. **No statistical significance or variance reporting.** All numerical results in the main paper are single-point estimates with no indication of whether they come from a single run or multiple runs, and no error bars or confidence intervals are provided. For key comparisons where differences of 0.01–0.03 in G-MIA scores or 1–2% in accuracy are treated as meaningful (e.g., FF-Erase(D) G-MIA 0.5245 vs RE 0.532; Table 1 cross-variant comparisons), the absence of variance information makes it impossible for the reader to assess whether observed differences are real or within the noise floor. This is the single most significant methodological gap.

### Minor

2. **The "black-box" framing of G-MIA is overstated.** G-MIA requires access to goodness vectors from *all* layers of the model (Section 5, Step 4). Standard black-box access in the MIA literature means only the final output (softmax logits or hard labels). Accessing per-layer goodness vectors is substantially more privileged — it is closer to gray-box or white-box access in terms of the information revealed. The abstract (line 9) and contributions list (lines 52-53) describe G-MIA as a "black-box attack" without qualification, and Section 2 calls it "under a strict black-box constraint" (line 62). This framing conflates G-MIA with the less-privileged FL baseline. The paper should either qualify the term or clarify that in FF models the goodness vectors are naturally exposed as part of the inference output, making this a different threat model.

3. **Baseline comparison is too narrow.** Only retraining from scratch (RE) and gradient ascent (GA) are compared as baselines (Section 6.2–6.3). The paper claims that "existing machine unlearning methods are not feasible for FF models" (Section 1, line 17) but tests only one family of approximate methods. Several other potentially applicable paradigms are not explored:
   - Fine-tuning on remaining data only (a simple and common baseline)
   - The "incompetent teacher" approach (Chundawat et al. 2023a), which is structurally similar (teacher-student framework for unlearning) and cited in the references but never discussed as a potential baseline or point of comparison
   
   Given that the paper claims "problem identification" as a contribution, a more systematic discussion of why other method classes would fail for FF models would strengthen the paper. The current experiments are sufficient to show GA fails, but not to support the broader claim about all existing methods.

4. **Efficiency framing understates guidance model overhead.** In Table 1, the best-performing variant D-(0.5,0.5) has t_unl = 583.5s (52.7% of RE's 1107s), of which 410.5s (70%) is spent training the guidance model. The actual forgetting-forward step takes only 173s (15.6% of RE time). The paper's efficiency estimate in Section 4.3 claims guidance model acquisition at "about 15% of t_ret" for the recommended α₁=0.3, α₂=0.5 (line 194), but actual numbers for D-(0.3,0.5) show t_0/t_ret = 26% — the 15% figure matches α₁·α₂ = 0.15 but does not account for the additional overhead of distillation forward passes through the teacher. The 1.9–3.1× speedup is real, but the presentation would benefit from clearly separating guidance-model time from the core unlearning mechanism time and acknowledging the efficiency–performance trade-off evident in Table 1 (fastest variants produce the worst unlearning).

### Trivial

None.

## Nice-to-Haves

- Compare with the "incompetent teacher" approach (Chundawat et al. 2023a) to clarify how FF-Erase differs from structurally similar distillation-based unlearning, and explain why it cannot be straightforwardly applied to FF models.
- Quantify the guidance model's own forgetting level on D_forget to disentangle the contribution of guidance model selection vs. the forgetting-forward step itself.
- Include at least one additional dataset-model combination (e.g., VGG on CIFAR-100) in the main text rather than only in the appendix.
- Discuss the potential data leakage in the fast-distillation strategy: since the teacher (original model θ_o) was trained on all data including D_forget, its outputs on D_remain may indirectly encode information about D_forget.

## Removed Points

These points are flagged for removal and should be treated with caution.

1. **G-MIA scores are too close to random (near 0.5) to support unlearning claims (Harsh Critic #1).** REMOVED. This criticism misunderstands the verification objective. When unlearning is effective, G-MIA is *supposed* to give near-random scores because the model no longer contains membership information about the forgetting data. RE (retraining from scratch) is the gold standard *because* it removes all influence, so RE's G-MIA score at ~0.5 is correct and expected. FF-Erase matching this is evidence *for* the method, not against it. The fact that GA methods with λ=0.001 achieve 0.608 (Figure 5c) — substantially above the RE baseline — shows the metric has discriminative power when unlearning fails. The useful sub-point about lack of dynamic range is subsumed by Weakness #1 (variance reporting).

2. **Potential issue with goodness calculation in Eq. (1) (Section-by-Section notes).** REMOVED. The critic questioned subtracting L1 norm from h^l as non-standard normalization. This operation follows the Forward-Forward algorithm's design (Hinton 2022), and the paper uses both "Norm" (L1-norm to compute g^l) and "LayerNorm" (standard layer normalization) as separate operations in Algorithm 1. The description is consistent with the FF literature.

3. **Efficiency formula concern in Eq. (9).** REMOVED. The critic questioned whether t₁ ≈ (K⁻¹+β)·t_ret properly accounts for two forward passes vs. one forward+backward. This is an approximation that affects constant factors but not the core validity of the efficiency analysis. The actual measured times in Table 1 are more informative than any formula.

## Novel Insights

The harsh critic observed that G-MIA's accuracy drops from ~0.8 (standard MIA setting, Figure 3) to ~0.5 (unlearning verification setting, Figure 4c), but misinterpreted this as a flaw. In fact, this drop is exactly what one would expect from a well-designed verification metric: when the model has been properly unlearned, membership signals should disappear, causing G-MIA to approach random guessing. The fact that the drop is clean and consistent across methods (RE and FF-Erase both at ~0.52-0.53) indirectly validates the metric's behavior. A more interesting question — which the paper does not fully address — is why GA with λ=10⁻² achieves G-MIA 0.598 (intermediate) while GA with λ=10⁻¹ achieves 0.554 (close to RE), given the latter represents a collapsed model. This suggests G-MIA may not linearly track unlearning quality and deserves further characterization.

## Suggestions

1. **Add multi-run statistics.** Report all quantitative results (G-MIA scores, accuracy, time) over at least 3-5 random seeds with standard deviations or confidence intervals. This is essential for the credibility of the reported comparisons.
2. **Qualify the "black-box" framing of G-MIA.** Either use a different term (e.g., "gray-box") or explicitly clarify that in FF models, goodness vectors are part of the natural model output, making this a different threat model than standard black-box access.
3. **Expand baseline discussion.** Even if additional baselines cannot be added experimentally, provide a reasoned discussion of why fine-tuning on remaining data, incompetent teacher, and influence-function variants would fail for FF models, rather than asserting this broadly.
4. **Clarify efficiency accounting.** Provide actual percentages alongside the idealized α₁·α₂ estimate and acknowledge the efficiency-performance trade-off visible in Table 1.

---

**Calibration Details**

All anchor papers retrieved from the calibration corpus:

| Path | Avg Score | Round | Comparison to this paper |
|------|-----------|-------|------------------------|
| 5lUdTogEL3 | 1.00 | R1 (strong-reject bracket) | Unrelated topic (person re-ID) |
| 5kMwiMnUip | 1.40 | R1 (strong-reject bracket) | Unrelated topic (LLM jailbreaking) |
| Uj0h13lVrR | 1.00 | R1 (strong-reject bracket) | Unrelated topic (GFlowNets) |
| nSDOkm0SKo | 1.00 | R1 (strong-reject bracket) | Unrelated topic (financial markets) |
| Xagys9QD3T | 3.00 | R1 (1.5–3.5 bracket) | MU paper with methodological flaws (wrong optimization goal); our paper is significantly stronger |
| 85X9awoVtv | 2.50 | R1 (1.5–3.5 bracket) | MU audit paper with weaker evaluation |
| BJfIDS5LsS | 2.50 | R1 (1.5–3.5 bracket) | MU paper with MARL; limited scope |
| hwXUmwJAq5 | 3.00 | R1 (1.5–3.5 bracket) | MU paper with simpler gradient-based approach |
| 7tpMhoPXrL | 4.80 | R1 (3.5–5.5 bracket) | Novel MU approach (forget vectors) but limited experiments; comparable novelty but our problem ID is stronger |
| KvFk356RpR | 4.80 | R1 (3.5–5.5 bracket) | MU attack paper; less relevant |
| drrXhD2r8V | 5.00 | R1 (3.5–5.5 bracket) | MU paper on Transformers; similar evaluation gaps (missing error bars, narrow scope) |
| okRSNTMdFg | 4.00 | R1 (3.5–5.5 bracket) | MU for diffusion models; different domain |
| pUOesbrlw4 | 5.25 | R2 (4.0–7.0 narrow) | "Deep Unlearning" — similar MU method paper, rejected (8/3/5/5). Key criticism: no variance, no theoretical guarantees. Our paper has similar evaluation gaps but stronger novelty. |
| 3p4raemLAH | 5.75 | R2 (4.0–7.0 narrow) | "SLUG" — MU paper rejected (8/5/5/5). Main criticism: "lack of variance experiments" (same as our paper). |
| OHOmpkGiYK | 5.75 | R1 (5.5–7.5 bracket) | MU decoupling paper; mixed reviews (6/6/3/8) |
| xmQuUqSynb | 5.75 | R1 (5.5–7.5 bracket) | MU + adversarial robustness; different focus |
| Q1MHvGmhyT | 6.00 | R1 (5.5–7.5 bracket) | MU for LLMs — Accept. Stronger evaluation with multiple metrics. |
| 9hjVoPWPnh | 6.00 | R1 (5.5–7.5 bracket) | MU for Image-to-Image Gen Models — Accept. Had theoretical analysis and large-scale experiments (ImageNet). |
| EUSkm2sVJ6 | 7.60 | R1 (7.5–8.5 bracket) | Strong paper on data usage inference; not comparable |
| KbetDM33YG | 8.00 | R1 (7.5–8.5 bracket) | GNN evaluation; unrelated |
| vrBVFXwAmi | 8.00 | R1 (7.5–8.5 bracket) | Quantum property estimation; unrelated |
| 84n3UwkH7b | 8.00 | R1 (7.5–8.5 bracket) | Diffusion model memorization; unrelated |

**Round 1 bracket:** I initially placed this paper between 4.0 and 6.5, based on comparison with MU papers scoring 4.80–6.00.

**Round 2 narrowing:** I examined "Deep Unlearning" (5.25) and "SLUG" (5.75) in detail — both are MU papers rejected primarily due to evaluation gaps (no variance, limited baselines). This paper shares those gaps but has stronger problem novelty (first FF unlearning). The accepted 6.0 papers had theoretical analysis and/or large-scale experiments that this paper lacks. Thus the final score of 5.5 reflects a paper with genuine contributions held back by addressable but consequential evaluation deficiencies.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>