## Summary

MoRE proposes a training-free, feature-level unlearning framework that extends the Erasing Space Concept (ESC) approach. The paper introduces three innovations: (1) prototype-orthogonal (PO) projection that decorrelates forget and remain prototypes before modification, (2) remapping (rather than simple erasure) of forget prototypes onto remain prototypes, and (3) a multi-expert router that scatters forget features across the latent space. The method achieves strong resistance to linear probing recovery (KR metric) while being computationally efficient (O(Nd) time, O(dk) memory).

---

## Strengths

1. **Prototype-orthogonal projection is a principled solution to a genuine problem.** The paper demonstrates (Section 3.1, Figure 3) that forget and remain prototypes have high cosine similarity (~0.5–0.77), so naive erasure damages remain representations. Constructing D as the pseudoinverse of P (Equation 2, DP = I_k) is mathematically clean. The ablation (Table 3) confirms that without PO, remain accuracy degrades substantially (Remap without PO: D_rt=79.64 on CIFAR-10; with PO: 99.94). This is the paper's strongest technical contribution.

2. **KR evaluation results are genuinely strong.** Under the KR setting (Table 1), where a linear probe attempts to recover forgotten knowledge, MoRE suppresses forget accuracy far below all baselines — including the retrain model (e.g., CIFAR-10 KR: Retrain HM_f=41.44 vs. MoRE HM_f=10.79; CIFAR-100: Retrain HM_f=52.96 vs. MoRE HM_f=0.07; Tiny-ImageNet: Retrain HM_f=37.00 vs. MoRE HM_f=0.50). This is a non-trivial improvement in probing resistance.

3. **Computational efficiency is impressive.** The method reduces unlearning to a single forward pass plus lightweight linear algebra. Figure 5 shows <10 seconds and <200MB GPU memory for CIFAR-10/100, orders of magnitude cheaper than training-based methods and more memory-efficient than ESC (which requires O(N_f d) memory for activations and SVD).

4. **The t-SNE visualization (Figure 1) effectively communicates the qualitative behavior.** ESC leaves a distinct red forget cluster; remapping merges it into one remain cluster; MoRE scatters it across the latent space. This directly illustrates the motivation for multi-expert remapping.

---

## Weaknesses

### Fatal
None.

### Major

1. **"Irreversible" is a materially stronger claim than the evidence supports.** The word "irreversible" or "irreversibility" appears ~14 times in the main text (title, abstract, introduction, method, conclusion). The abstract claims the method impedes "recovery via fine-tuning" (line 9), and the introduction states it "significantly impedes the recovery of forgotten knowledge through fine-tuning or linear probing" (line 82). However, the experiments only evaluate resistance to *linear probing* at a single learning rate (KR metric, lr=0.1). No fine-tuning recovery attack, varying-probe-strength analysis, or nonlinear probing is presented. The method operates through a linear transformation (Equation 6), and the complement-space term (I − PD) in Equation 4 explicitly preserves information outside the prototype span — yet the paper does not analyze whether those preserved components retain discriminative power for forget classes under stronger attacks. **Why it matters:** The paper's central selling point — "irreversibility" — is the claim that distinguishes MoRE from prior work. Without evidence that the method resists recovery beyond linear probing at one learning rate, the claim is not commensurate with the data. The KR results are real and valuable, but they support "resists linear probing recovery" rather than "irreversible."

### Minor

2. **Standard evaluation benchmarks are saturated, making "SOTA" claims on those metrics uninformative.** Under the "Standard" columns of Table 1, nearly every method achieves near-perfect scores (D_f ≈ 0.00, D_r ≈ 100%, HM ≈ 99%+). MoRE's numbers are essentially identical to ESC-T, Remap, and Finetune — differences are in the second decimal place. The paper claims "consistently outperforms existing methods" (line 364), which is technically true but practically vacuous for these saturated metrics. MoRE's real contribution is in the KR setting, and the paper would benefit from positioning itself accordingly. **Why it matters:** This doesn't invalidate the KR contribution, but the current framing conflates two very different findings (saturated standard metrics vs. meaningful KR improvements), which can mislead readers about where the method actually advances the state of the art.

3. **No dedicated discussion of MoRE's own limitations.** The paper discusses ESC's limitations thoroughly but does not reflect on MoRE's. Several issues are visible in the presented data that should be acknowledged: (a) Substantial sensitivity to target class choice in KR setting — Table 5 shows HM_t ranging from 15.24 (target 9) to 69.78 (target 0), a 4.6× variation; (b) MIA performance (Table 4, 79.31) is notably worse than SCRUB (86.41); (c) Performance degrades at shallower layers (Table 7), with the third-last layer showing forget accuracy lingering around 25% vs. near 0% at the last layer. These are real constraints that should be discussed rather than deferred to "future work."

4. **The claim of "exact feature-level unlearning" (line 9, abstract) is undefined.** The term "exact" appears only in the abstract and is never formally defined, justified, or used elsewhere. The paper does not provide any theoretical guarantee of exactness. This appears to be an imprecise use of terminology that should be clarified or removed.

5. **The paper's framing of the comparison with training-based methods in the KR setting could be sharper.** Training-based baselines (Finetune, SCRUB, etc.) were designed to approximate retrain-from-scratch, not to resist feature-level probing. MoRE was specifically designed for probing resistance. The current framing ("outperforms training-based methods") is not incorrect, but the paper would better serve readers by acknowledging that these methods optimize different objectives, and that MoRE achieves a *different property* (probing resistance) that prior methods did not target.

### Trivial
None.

---

## Nice-to-Haves

- **Test stronger recovery attacks** to support the irreversibility claim: full fine-tuning of the backbone on forget data, varying probe learning rates, and nonlinear (MLP) probing. The claim of "impeding recovery via fine-tuning" (line 9, 82) would be well-supported by a fine-tuning experiment.
- **Add error bars to Table 2** (diffusion LPIPS results), consistent with the standard deviations already reported in Table 1.
- **Clarify the rank constraint on PO projection.** The paper enforces DP = I_k (full mutual orthogonality) and notes (footnote 1) that only forget–remain orthogonality is needed. The paper does not discuss what happens when k > d (more prototypes than feature dimensions) or when P is near-rank-deficient.
- **Include a dedicated limitations paragraph** covering the issues noted in Weakness #3.

---

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Diffusion results claim contradicts the numbers (Critical Issue 2 from harsh review).** The critic claimed that UCE outperforms MoRE on LPIPS_f (0.25 vs. 0.33), but the paper states that *higher* LPIPS_f is better for forgetting (line 276). MoRE's 0.33 > UCE's 0.25, so MoRE is superior on the primary forgetting metric. The critic's comparison is factually inverted. Additionally, MoRE achieves the best LPIPS_d tradeoff (0.25 vs. UCE's 0.20 for Van Gogh). This criticism is removed per the hard rule against factually wrong claims.

- **"Release code and model weights"** (from Missing Parts section). This requests the existence/release of artifacts not required for evaluation; per hard rules, questioning availability of cited entities is not permitted.

- **General area-sweep concerns from the harsh review** (e.g., "could the metric be measuring a proxy?", "are confounders controlled?") that lack specific grounding in the paper. These are speculative rather than identified problems.

---

## Novel Insights

The harsh review's core insight is that the paper's strongest technical contribution (PO projection, remapping, multi-expert scattering) is solid, but the claims systematically outrun the evidence. The gap is clearest in the use of "irreversible" when only linear probing resistance at one learning rate has been tested. A secondary insight is that the standard unlearning benchmarks are saturated — MoRE's meaningful improvement is exclusively in the KR setting, and the paper would benefit from acknowledging this rather than claiming generic "SOTA." The review also surfaces the substantial target-class sensitivity (Table 5) that the paper under-discusses. None beyond the paper's own contributions and the above observations.

---

## Suggestions

1. Replace "irreversible" with language like "resists linear probing recovery" or "strongly inhibits feature-level recovery" — this is consistent with the evidence and still positions the method ahead of ESC and training-based baselines.
2. Add a dedicated limitations section that discusses target-class sensitivity (Table 5), shallow-layer degradation (Table 7), MIA results (Table 4), and the rank constraint on PO projection.
3. Re-frame the "SOTA" discussion to distinguish between saturated standard benchmarks (where all methods tie) and the KR setting (where MoRE genuinely advances the state of the art).
4. Clarify or remove the undefined term "exact" from the abstract.
5. Add at least one fine-tuning recovery experiment to support the claims about impeding recovery via fine-tuning.

---

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>