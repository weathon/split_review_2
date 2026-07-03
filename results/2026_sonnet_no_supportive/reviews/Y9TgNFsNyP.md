Round 1 bracket: **4–6**. The paper's novel problem scope and principled design push above the 3.0 rejects, but the numerical inconsistency (Figure 4 vs Table 1 RE baseline) and G-MIA/FF-Erase circularity pull it below the 6+ accepts. Let me narrow.## Final Review

## Summary
FF-Erase introduces the first machine unlearning framework for Forward-Forward (FF) neural network models, which train via layer-wise greedy optimization of "goodness" scores rather than backpropagation. The paper diagnoses specific failure modes of naive gradient ascent for FF models, proposes a KL-divergence-based goodness-guided unlearning strategy using a lightweight guidance model, and introduces G-MIA — a black-box membership inference attack exploiting multi-layer goodness vectors — as a verification tool for unlearning effectiveness.

---

## Strengths

- **Precise problem diagnosis** (§1, Figure 1, §6.3): The paper identifies two concrete failure modes of applying standard gradient ascent to FF models — divergent layer update directions and uneven per-layer forgetting — and confirms them experimentally in §6.3 (Figure 5) across six values of λ, rather than simply asserting failure.
- **Principled method design** (§4.1, Eq. 5): Anchoring the goodness decrease to a guidance model's distribution via KL divergence is a well-motivated response to the identified instability, providing a natural target distribution without requiring manual per-layer goodness thresholds.
- **Architecturally appropriate G-MIA** (§5, Figure 3): Exploiting multi-layer goodness vectors as a membership signal is specific to FF models. The empirical finding that goodness vectors across all layers outperform final-output-only black-box attacks — and approach white-box performance on VGG13/CIFAR-100 (Figure 3c) — is a concrete and non-trivial result.
- **Informative ablation** (§6.4, Table 1): The R.G.M row (randomly initialized guidance model) directly demonstrates that the *guidance signal* — not merely the KL update form — drives stable unlearning, distinguishing the contribution from a vanilla KL baseline.

---

## Weaknesses

### Fatal
None.

### Major

- **Numerical inconsistency between Figure 4 and Table 1 for the RE baseline.** Figure 4(c) labels RE G-MIA ACC = **0.5320**, while Table 1 shows RE G-MIA ACC = **0.551**; Figure 5(c) also shows RE ≈ 0.550, consistent with Table 1 but not Figure 4. Both figures/the ablation table claim VGG13/CIFAR-10 with 20% forgetting. The gap is material: in Figure 4, FF-Erase(D)'s score of 0.5245 falls *below* RE (i.e., "better than retraining"), while in Table 1 all FF-Erase variants are *above* RE (0.551). The paper's text in §6.2 explicitly compares to the 0.532 figure as the primary effectiveness claim. If the two setups are identical, at least one set of numbers is wrong; if they differ, the paper never says so. This inconsistency directly undermines the primary quantitative comparison between FF-Erase and the retraining gold standard.

- **Structural circularity between G-MIA and FF-Erase.** FF-Erase (Eq. 5) explicitly optimizes the forgetting samples' goodness distribution toward the guidance model's distribution. G-MIA (§5, Eq. 10) judges membership by feeding exactly those goodness vectors from all layers into a trained binary classifier. The optimization target of the unlearning method and the feature space of the verification metric are structurally identical. A model that merely redistributes goodness representations toward a non-member pattern — without genuinely reducing parameter-level data influence — would still achieve low G-MIA scores. The paper presents G-MIA as "a reliable verification tool" and uses its score as the *primary* effectiveness evidence in §6.2, but the metric's independence from the method's own optimization target is never established or even acknowledged. The D_forget accuracy metric provides partial corroboration but is described in §6.2 as noisier; the paper's own framing leans on G-MIA as the "more precise" signal.

### Minor

- **Overstated G-MIA performance claim.** §1 and §6.1 state "G-MIA even matches the performance of white-box attacks with deep networks and complex datasets." However, Figure 3's own caption reads: "In all cases, G-MIA is the best black-box MIA, and ST is the best overall MIA." These two characterizations are directly inconsistent; the body text overstates what the paper's own figure shows.

- **Unjustified 20% forgetting fraction.** §6.2 selects 20% of training data as D_forget without justification or prior-work comparison. Most unlearning literature uses ≤5% or class-level forgetting. The large fraction may mask fine-grained failures and limits the comparability of reported metrics to existing work.

- **Fast-distilled guidance model's potential information leakage** (§4.2, Eq. 8). The distillation teacher is θ_o, trained on all data including D_forget. The paper claims θ_g should be "ignorant of the forgetting data," but θ_g is trained to mimic θ_o's outputs on D_remain, which may carry indirect D_forget signals through the teacher's representations. No theoretical or empirical analysis of this leakage is provided.

### Trivial
None.

---

## Nice-to-Haves
- Including at least one non-goodness-based effectiveness metric (e.g., Euclidean/cosine parameter distance between θ_u and θ_r, or activation-level similarity on D_forget) would corroborate G-MIA scores without the shared feature-space concern and decisively address the circularity concern.
- Reporting main-text results on a second dataset/architecture would make the claimed 1.9–3.1× speedup range more interpretable; the current main text shows only VGG13/CIFAR-10, with the range's bounds appearing only in the appendix.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Eq. 4 loss formulation presentation gap**: The reviewer noted Eq. 4 uses a generic "loss" notation without explicitly flagging it as the layer-wise FF goodness loss. This is a minor clarity issue self-evident to readers of §3.1; not a substantive flaw. Removed.
- **Thin main-text evaluation (single model/dataset)**: The reviewer treated this as a significant weakness. However, the paper states broader results are in the appendix, which was stripped by the PDF parser but exists in the original submission. Removed per the hard rule on stripped appendices.
- **Missing related work references**: No external sources available to confirm, per hard rules. Not raised by this reviewer but preemptively excluded.

---

## Novel Insights
The paper surfaces a genuinely interesting dual-use property of FF goodness vectors: the same multi-layer goodness signals that drive efficient FF training also leak membership information more strongly than final-layer logits — and more robustly than gradient-based white-box signals under regularization. The empirical observation that layer depth amplifies this leakage (deeper models → G-MIA's advantage over black-box baselines grows) is a concrete, non-obvious finding about FF model privacy that extends beyond the unlearning context itself. If validated independently, this would be a useful result for the broader FF model security literature.

---

## Suggestions
1. Resolve the RE baseline discrepancy between Figure 4 (0.532) and Table 1/Figure 5 (0.551): specify exactly what differs between the two experimental setups and report consistently.
2. Add a parameter-distance or activation-similarity table comparing θ_u to θ_r on D_forget — even a single supplementary entry — to provide an independent corroboration channel for G-MIA unlearning scores.
3. Correct the G-MIA performance claim in §1/§6.1 to match Figure 3 ("best black-box MIA, approaching white-box on deep models" rather than "matching white-box").
4. Add a brief analysis (or empirical check) of whether distillation from θ_o in Eq. 8 transmits D_forget membership signals into θ_g.
5. Justify the 20% forgetting fraction or add a smaller-fraction experiment (e.g., 5%) to demonstrate generalizability.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| Xagys9QD3T (PPU Unlearning) | 3.00 | R1 | Generic method, no novel problem domain; weaker than this paper |
| hwXUmwJAq5 (UGradSL) | 3.00 | R1 | Simpler gradient label-smoothing approach; less novel problem |
| BJfIDS5LsS (MASIMU) | 2.50 | R1 | Multi-agent unlearning, poorly motivated; weaker |
| Uv7bWrIucU (Auditing Privacy) | 4.20 | R1/R2 | MIA-based unlearning audit; similar structure but less novel setting |
| KvFk356RpR (Unlearning Mapping Attack) | 4.80 | R1/R2 | Adversarial unlearning attack paper; comparable novelty, better evaluation clarity |
| 7tpMhoPXrL (Forget Vectors) | 4.80 | R1 | Input-perturbation unlearning; novel angle, similarly thin evidence |
| iQIQT88prm (Adversarial MU Stackelberg) | 5.33 | R1/R2 | Integrates MIA into unlearning design — very similar dual-contribution structure; rejected |
| wAemQcyWqq (OUbL) | 5.67 | R2 | Privacy-preserving unlearning; accepted at 6+, well-evaluated |
| xmQuUqSynb (Adversarial Robustness+MU) | 5.75 | R2 | Novel security angle on unlearning; rejected despite 5-6 scores |
| OHOmpkGiYK (Decoupling MU) | 5.75 | R1 | More systematic evaluation across settings; stronger evidence |
| SIZWiya7FE (Label-Agnostic MU) | 6.00 | R1 | Accept; supervision-free, systematic, no major inconsistencies |
| EUSkm2sVJ6 (Dataset Usage Inference) | 7.60 | R1 | Strong accept; rigorous and clean evaluation |
| 84n3UwkH7b (Memorization Diffusion) | 8.00 | R1 | Strong accept; clean detection+explanation, no eval inconsistencies |

**Calibration narrative:**

- **Round 1 bracket: 4–6.** The paper's novel problem domain and principled design clearly exceed the 3.0 rejects (generic gradient-smoothing approaches, poorly motivated methods). The two major weaknesses (numerical inconsistency, circularity) prevent it from reaching accepted papers like SIZWiya7FE (6.0) or OUbL (5.67 mean, 6 modal).
- **Round 2 narrowing: 4–5.** The most structurally similar accepted paper at this range is wAemQcyWqq (5.67) which has clean, independent evaluation. The most structurally similar rejected paper is iQIQT88prm (5.33, reject) which also intertwines MIA with unlearning design. This paper's numerical inconsistency in the primary figure (Figure 4 vs Table 1 RE baseline) is a concrete verifiable problem — the kind that makes reviewers doubt all numbers — and the circularity concern is substantial. **Final score: 4.5** (borderline reject).

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>