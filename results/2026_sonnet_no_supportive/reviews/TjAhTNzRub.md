Based on Round 1, I place MoRE in the **6–8 range**. The paper is clearly above the rejected subspace-unlearning papers (4–5.25) and on par with or better than the borderline-accept papers at 5.75–6.75. Let me narrow further.## Summary
MoRE (Mixture of Remapping Experts) is a training-free framework for irreversible feature-level machine unlearning. The key insight is that existing subspace-erasure methods (e.g., ESC) leave forget features cohesive and separable in the latent space even after erasing the forget subspace, making unlearning recoverable via light fine-tuning. MoRE counters this by projecting features into a prototype-orthogonal space and *remapping* forget prototypes into the remain prototype distribution — rather than merely erasing them — distributed across multiple stochastic experts to scatter forget features across the latent space, achieving dramatic resistance to fine-tuning recovery.

---

## Strengths

- **Decisive irreversibility advantage on the KR metric.** On Tiny-ImageNet under the KR setting, ESC-T achieves HM_f=95.47 while MoRE achieves 0.50; on CIFAR-100 KR, the best competitor has HM_f=51.88 while MoRE achieves 0.07 (Table 1). These are not marginal improvements — they represent a qualitatively different regime of unlearning resistance to fine-tuning recovery, and hold consistently across three datasets and model families.

- **Mathematically coherent framework.** The prototype-orthogonal (PO) projection (Sec. 3.1, Eq. 2) is a clean use of the pseudoinverse to decouple forget and remain editing. The derivation from erasure (Eq. 3–5) to remapping (Eq. 6) is well-structured and logically complete.

- **Empirically grounded design choices.** Figure 3 provides direct empirical motivation (cosine similarity ~0.5 between forget/remain prototypes) for the PO projection step. Figure 1's t-SNE visualization concretely shows cluster absorption distinguishing MoRE from ESC. Figure 6 validates that remapping preserves remain prototype autocorrelations. These are specific, verifiable claims.

- **Training-free scalability.** O(Nd) compute and O(dk) memory for prototype construction is a genuine theoretical advantage over training-based methods. The method beats training-based baselines at a fraction of the cost, and the ablation (Table 3) confirms the contribution of each component.

- **Out-of-box generalization to diffusion models.** MoRE achieves LPIPS_d=0.25 vs UCE's 0.20 (Table 2) applied directly to cross-attention layers with no architecture-specific adaptation, hyperparameter tuning, or additional engineering — the only training-free method among those outperforming training-based SOTA on this tradeoff metric.

---

## Weaknesses

### Fatal
None.

### Major

- **Direct, verifiable contradiction between Section 4.1 prose and Figure 5 on memory consumption.** Section 4.1 states MoRE performs unlearning "consuming less than 200 MB of GPU memory," but Figure 5 (bottom panel) explicitly shows MoRE consuming 540 MB — nearly 3× the stated figure, and more than both ESC (491 MB) and ESC-T (447 MB). This is not a speculative inference; it is a direct contradiction between a specific numerical prose claim and a specific bar in the paper's own figure. The theoretical O(dk) memory advantage (vs. ESC's O(N_f d)) may hold asymptotically and is correctly stated, but the main-paper prose framing is incorrect at the tested scale.

- **No irreversibility evaluation for diffusion model unlearning.** The paper's central and distinguishing contribution is irreversibility; yet the entire diffusion model section (Table 2) provides only LPIPS metrics, with no KR-equivalent evaluation of resistance to fine-tuning recovery. Since the paper claims irreversibility is ensured "at the feature level" generally, and the diffusion application is the most visible real-world use case, the absence of irreversibility measurement here is a structural inconsistency. The claim that MoRE "outperforms SOTA diffusion model unlearning methods both quantitatively and qualitatively" is also partially overstated: the LPIPS_d advantage over UCE (0.25 vs 0.20) is modest, and RECE achieves LPIPS_d=0.23 for Van Gogh erasure.

### Minor

- **Target remapping class sensitivity is non-trivial for single-expert Remap.** Table 5 shows HM_t for Remap under the KR setting ranges from 29.26 (target 9) to 69.78 (target 0) on CIFAR-10, a ~2.4× variation. The paper describes this as "mild preference" (Sec. 4.2) and defers deeper investigation to future work. While MoRE's multi-expert design substantially reduces this sensitivity (HM_f=10.79 in Table 1), the single-expert Remap results — and the default target-class choice — lack any principled selection criterion, making those results hard to reproduce reliably. A simple distance-based heuristic would strengthen this.

- **HM_f is undefined in the main paper.** HM_f is the primary metric that differentiates MoRE from all baselines, yet it is defined only in Appendix §B.3. At minimum, a one-line definition should appear in Section 4 where it first appears in Table 1.

- **KR fine-tuning data not stated in main body.** The paper does not specify in the main text what data is used for the KR fine-tuning step (deferred to Appendix §B.3). This matters for result interpretation: the Retrain baseline achieves D_f=72.62% after KR on CIFAR-10, implying non-trivial forget-class information is reintroduced during fine-tuning.

- **MIA framing in random forgetting is overstated.** Table 4 shows Remap achieving MIA=79.31, which is worse than both SCRUB (86.41) and Prototype (87.73). The claim of "comparable or superior performance" (Sec. 4.3) is inaccurate for MIA. This is bounded — random data forgetting is not MoRE's design target — but the framing misleads.

### Trivial
None verified.

---

## Nice-to-Haves
- Extend the KR/irreversibility evaluation to the diffusion model setting (fine-tune on remain prompts and measure forget-style regeneration) to close the evidential gap for the paper's central claim.
- Report memory consumption across a range of forget-set sizes to empirically demonstrate the O(dk) vs. O(N_f d) advantage.
- Provide a principled heuristic for target class selection (e.g., maximum cosine distance from forget prototype) to improve single-expert Remap deployability.

---

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Table parsing artifacts in Table 1 (D_r=0.00 entries appearing catastrophic):** Reviewer flagged garbled column structure as a potential anomaly. Paper's prose clarifies these are PDF extraction artifacts. Removed per parser-artifact rule.
- **Table 4 listing "Remap" vs "MoRE":** Reviewer questioned whether MoRE and Remap are distinct entries. Section 4.3 explicitly explains this adaptation for random forgetting; no deception. Removed as strawman.
- **ESC memory inefficiency as a "core limitation":** The claimed O(dk) theoretical advantage is stated correctly. Only the specific prose claim "less than 200 MB" is erroneous (absorbed into the Major weakness). The broader efficiency claim remains valid.

---

## Novel Insights
The core insight — that subspace-erasure methods leave forget features *cohesive and separable* in the latent space even after removing the forget subspace, enabling recovery via fine-tuning, and that *remapping* into remain prototype distributions (rather than merely erasing) genuinely breaks both separability and cohesion — is a clean and valuable conceptual advance. The empirical magnitude (~0.5 vs ~95 HM_f on Tiny-ImageNet) is striking and suggests that cohesion-breaking is the critical property for irreversible unlearning, a hypothesis that prior work had not operationalized. The mixture-of-experts framing for scattering forget features across multiple remain prototypes is an elegant extension of this principle.

---

## Suggestions
1. **Correct the memory claim:** Fix the prose in Section 4.1 ("less than 200 MB") to align with Figure 5 (540 MB), or conduct an additional experiment at larger forget-set sizes where the O(dk) advantage becomes measurable.
2. **Move HM_f definition to main paper** (one sentence in Section 4).
3. **Add a KR-equivalent experiment for diffusion models** to substantiate the irreversibility claim in that setting.
4. **Clarify in main text** what data is used for KR fine-tuning, and confirm the default target class in Table 1 was not selected post-hoc after observing KR results.

---

## Calibration Anchors

| Path | Avg Score | Round | Comparison to MoRE |
|------|-----------|-------|---------------------|
| p7mgNvOD9Q (SUN: Training-free Subspace Unlearning) | 4.00 | R1 | Rejected; weaker contribution, no irreversibility metric, narrower evaluation |
| pUOesbrlw4 (Deep Unlearning: Fast Training-free) | 5.25 | R1 | Rejected; similar training-free concept but no irreversibility claim, weaker results |
| TLBPjECC5D (Unlearning via Sparse Representations) | 5.25 | R1 | Rejected; comparable efficiency claims, narrower evaluation, no feature-level irreversibility |
| OHOmpkGiYK (Decoupling Class Label/Concept) | 5.75 | R1 | Borderline reject; interesting extension but no strong irreversibility metric |
| wAemQcyWqq (Oblivious Unlearning by Learning) | 5.67 | R1 | Borderline reject; different problem formulation, comparable scope |
| oe51Q5Uo37 (Scalable Exact Unlearning via PEFT) | 6.75 | R1 | Accepted; strong contribution but focuses on exact unlearning via architecture, not feature-level |
| HVFMooKrHX (Utility/Complexity of Unlearning) | 6.60 | R1 | Accepted; theoretical depth but limited empirical scope |
| gjwhDHeAsz (Score Forgetting Distillation) | 6.50 | R2 | Accepted; diffusion-specific unlearning, similar scope but more limited task |
| SIZWiya7FE (Label-Agnostic Forgetting) | 6.00 | R2 | Accepted; interesting but narrower scope; comparable empirical depth |
| nb3VjILNVs (Low Compute Unlearning/Sparse) | 5.75 | R2 | Rejected; weaker results, narrower scope |

**Round 1 bracket:** 6–8 (above rejected subspace papers, comparable or better than borderline-accept papers at 6–6.75).

**Round 2 narrowing:** Comparing to the 6.0–6.75 accepted papers, MoRE has a more distinctive contribution (irreversibility), substantially stronger empirical results (3–4 dataset evaluation with qualitatively dominant KR metric), and broader scope (classification + diffusion). The major weaknesses (prose-Figure contradiction on memory, missing diffusion irreversibility evaluation) are real but bounded — they do not invalidate the core classification results. This places MoRE above the 6.5 anchor (Score Forgetting Distillation) but the prose error on memory and missing diffusion KR evaluation prevent a score of 8. I anchor at **7.0**.

---

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>