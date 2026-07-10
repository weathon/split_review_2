Now I have the impact scores clearly. Let me finalize the review.

**Analysis of the impact scores:**
- Strengths: all very high (+8.9 to +9.5) — the paper's core contributions are genuinely strong
- The biggest negative is the narrow irreversibility evidence (-8.5) and diffusion overclaim (-7.4)
- The ablation issue (-5.4) is moderate
- Minor items (-2.2, -0.2) barely move the needle

The weaknesses are about overclaiming and framing, not about faulty methodology or invalid results. The core contribution — PO projection + remapping experts achieving dramatic gains in KR — is solid and well-supported. The paper is clearly above the acceptance threshold. Score: **8 (Accept)**.

---

## Summary

MoRE proposes a training-free framework for feature-level machine unlearning that addresses the vulnerability of prior methods (especially ESC) where forget features remain cohesive and separable in latent space, enabling recovery via linear probing. The approach combines (i) prototype-orthogonal projection to decorrelate forget/remain prototypes before editing, (ii) erasure and remapping of forget prototypes into remain prototypes, and (iii) a mixture-of-experts extension with stochastic routing to scatter forget features across multiple remain prototypes. Experiments on CIFAR-10/100, Tiny-ImageNet, and diffusion models show competitive HM scores and dramatically lower KR (knowledge retention) metrics — indicating forget knowledge cannot be recovered by linear probing — while requiring under 10 seconds and <200 MB GPU memory.

## Strengths

- **Well-motivated problem targeting a genuine limitation.** The paper clearly articulates that ESC (the current SOTA feature-level unlearning method) leaves forget features cohesive and separable in latent space, making unlearning reversible via linear probing. This vulnerability is convincingly demonstrated with t-SNE visualization (Fig. 1) and cosine similarity analysis showing remain prototypes dropping from 1.0 to 0.52 after ESC unlearning (Fig. 3).

- **Clean and principled mathematical formulation (Equations 2–6).** The progression from prototype-orthogonal projection via pseudoinverse (Eq. 2), to erasure via coordinate sparsification (Eq. 3–5), to remapping via detection-and-redirection (Eq. 6) is derivationally sound and reproducible from the text. The complement-space projection term (Eq. 4) is a practical touch preventing information loss outside the prototype span.

- **Strong KR results demonstrating resistance to probing.** Under the KR (linear probing) evaluation, MoRE achieves HM_f = 10.79 on CIFAR-10, 0.07 on CIFAR-100, and 0.50 on Tiny-ImageNet (Table 1) — dramatically lower than all baselines including Retrain (41.44, 52.96, 37.00 respectively), showing forget knowledge cannot be recovered by a well-tuned linear probe.

- **Impressive efficiency.** The method performs complete unlearning on CIFAR-10/100 in under 10 seconds and <200 MB GPU memory (Fig. 5). The O(Nd) time and O(dk) memory complexity is a concrete practical advantage over ESC's O(N_f d) SVD memory requirement.

## Weaknesses

### Fatal
None.

### Major

- **The ablation study (Table 3) reveals that the simplest variant — Erase with PO projection — outperforms both Remap and MoRE on the standard (non-KR) HM metric.** Erase+PO achieves HM = 99.68, while Remap achieves 95.38 and MoRE achieves 95.23. The paper frames remapping as its core innovation, but Erase+PO (a simpler erasure approach) beats it on the utility-unlearning tradeoff. The paper's text (lines 330–332) discusses that "PO yields the strongest results" without squarely addressing why a reader should prefer Remap/MoRE. The answer — that remapping's advantage is specifically in irreversibility (KR), not standard HM — is present implicitly but never clearly stated, weakening narrative coherence. This is fixable with sharper framing that explicitly delineates the two regimes.

- **The claim of "irreversibility" (used throughout: abstract, introduction, conclusion) is supported by only one probing configuration: linear probe at lr = 0.1 (Table 1, KR columns).** The paper provides no evidence on whether stronger recovery attacks — such as k-NN probes, shallow MLPs, or a few epochs of full-model fine-tuning — can extract forget knowledge. The main paper defers metric details to Appendix §B.3 (line 239) and gives no justification for why a single probing configuration suffices to establish the strong property of irreversibility. While the KR results are impressive and clearly demonstrate resistance to linear probing, the evidential basis for the absolute term "irreversible" is narrower than the claim warrants.

### Minor

- **The diffusion model results are overclaimed.** The paper states it "outperforms SOTA diffusion model unlearning methods both quantitatively and qualitatively" (line 326), but Table 2 shows MoRE achieves the best LPIPS_d tradeoff score only, not the best individual LPIPS_f or LPIPS_r metrics. For Van Gogh removal, UCE achieves LPIPS_f = 0.25 vs MoRE's 0.33, and SLD-Medium achieves LPIPS_r = 0.55 vs MoRE's 0.08. The LPIPS_d tradeoff is the most informative single-number summary, but claiming to "outperform" on all fronts is overstated.

- **The paper enforces full mutual orthogonality among all prototypes (Footnote 1, line 168) while acknowledging only forget-remain orthogonality is needed.** It does not evaluate whether this stricter constraint causes any utility degradation compared to a hypothetical selective-orthogonality variant, leaving the impact of this design choice unexamined.

- **The ablation table (Table 3) and sensitivity analysis (Table 5) do not report standard deviations**, unlike the main results (Table 1) which use three trials with mean ± std. This makes it harder to assess whether differences between variants (e.g., Erase+PO vs Remap) are significant.

### Trivial
None.

## Nice-to-Haves

- The paper would benefit from explicitly separating two regimes: acknowledge Erase+PO suffices for standard HM utility, and position Remap/MoRE's advantage specifically in irreversibility under probing (KR).
- Testing stronger recovery attacks (k-NN, shallow MLP, partial fine-tuning) would substantially strengthen the irreversibility claim and make the paper's framing more defensible.
- Comparing activation-mean prototypes against SVD-based prototypes (used by ESC) would isolate whether the efficiency gain comes at any quality cost.
- Adding standard deviations to ablation/sensitivity tables would improve rigor.

## Removed Points

- *ImageNet results deferred to appendix*: REMOVED per hard rule — the parser strips appendix content; these results exist in the original submission.
- *Stochastic router mechanism is unclear*: REMOVED — the paper clearly explains (Section 3.3) that random routing distributes forget features across different experts, each remapping to different remain prototypes, and provides quantitative evidence (Figure 7, Table 6) of the effect. Requesting distributional metrics beyond t-SNE is a nice-to-have, not a weakness.
- *Related works narrow focus*: REMOVED — the paper positions itself against ESC specifically; this focused scope is acceptable.
- *Formatting/table parsing artifacts*: REMOVED — these are parser errors, not paper issues.
- *Observation about D_f=0 being trivially achieved*: REMOVED — the KR metric is specifically designed to capture the real challenge beyond trivial D_f=0, and the paper appropriately uses both.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure the narrative to explicitly separate the two evaluation regimes (standard HM vs. KR irreversibility) and position each variant's contribution accordingly. This would address the ablation discrepancy naturally.
2. Broaden the KR evaluation to include at least one stronger recovery attack (e.g., a 2-layer MLP probe, partial fine-tuning) to better support the "irreversibility" framing, or alternatively adopt more measured language (e.g., "strong resistance to probing").
3. Add standard deviations to the ablation and sensitivity tables.
4. Tone down the diffusion results claim to match what the data show: e.g., "achieves the best overall tradeoff (LPIPS_d)."

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>