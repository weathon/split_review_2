## Summary

This paper proposes MoRE (Mixture of Remapping Experts), a training-free framework for feature-level machine unlearning. The core technical contributions are: (i) a prototype-orthogonal (PO) projection that decorrelates forget and remain prototypes before editing, preventing utility degradation; (ii) a remapping mechanism that redirects forget prototype activations toward remain prototypes (rather than simply erasing them), disrupting the residual separable structure; and (iii) a multi-expert extension that scatters forget features across multiple remain prototypes. The method is computationally efficient (O(Nd) time, O(dk) memory, under 10 seconds on CIFAR-10/100) and extends naturally to diffusion model concept unlearning.

## Strengths

- **Principled, well-motivated methodology.** The PO projection (Eq. 2, pseudoinverse of the prototype matrix via SVD) cleanly addresses a verified problem: forget and remain prototypes exhibit cosine similarities of ~0.5–0.77 (§3.1), so naive erasure degrades remain utility. The paper provides both theoretical justification (avoiding squared condition number) and empirical validation (Fig. 6 shows remain autocorrelation preserved near 1.0). The use of SVD-based pseudoinverse over the normal-equation form demonstrates good technical judgment.

- **Remapping is a genuine advance over erasing.** Rather than merely suppressing forget prototype activations (ESC's approach), MoRE detects when a forget prototype is activated and redirects that contribution toward remain prototypes (Eq. 6). The "detector" design (the diag(s)D term) ensures that the operation is conditional on forget prototype activation, so remain features that do not activate forget prototypes are not affected. The t-SNE visualization (Fig. 1) qualitatively demonstrates the difference: ESC leaves a distinct forget cluster, while MoRE scatters forget features into the remain distribution.

- **Genuinely efficient and scalable.** The method is training-free, has O(Nd) time complexity and O(dk) memory, and completes CIFAR-10/100 unlearning in under 10 seconds with <200 MB GPU memory (§4.1, Fig. 5). This is a substantial practical advantage over training-based unlearning methods.

- **Broad applicability demonstrated.** The framework extends to diffusion model concept unlearning out of the box with competitive LPIPS_d tradeoffs (0.25 for Van Gogh, 0.26 for Kelly McKernan in Table 2), without architecture-specific adaptations.

## Weaknesses

### Major

- **The "irreversible" claim significantly exceeds the evidence.** The word "irreversible" or "irreversibility" appears in the title, abstract, §1, §3, and §5 (11+ occurrences) and is the paper's headline claim. The primary quantitative evidence is the KR metric, referenced in the main paper only as a fine-tuning-at-lr=0.1 protocol (details in appendix §B.3). Stronger recovery threats — full-model fine-tuning, non-linear probes (e.g., MLP), adversarial recovery methods, or mutual information estimation — are not tested. The conclusion goes further to claim "real-world unlearning guarantees stronger than retrain-from-scratch," which requires substantially more evidence than a single recovery protocol at one learning rate. The core technical contribution (PO projection + remapping) is valuable on its own terms and does not depend on the "irreversible" framing, but the gap between the claim and the evidence is significant. The paper would be better served by language calibrated to the actual evidence, such as "strongly resistant to linear probing recovery."

### Minor

- **The MIA result is discussed only superficially.** The MIA evaluation (Table 4) shows the Remap variant achieving 79.31% MIA vs. Retrain's 74.64% on CIFAR-10 random data forgetting. While MIA and class-level unlearning measure different properties (membership detection vs. knowledge recovery), the observation that a retrained model yields lower membership inference success than the unlearned model merits dedicated analysis — e.g., is this a side-effect of the remapping mechanism, or does it indicate a genuine information leak the current evaluation framework misses? The paper's single sentence ("comparable or superior performance") does not address this.

- **Framing tension between KD formulation and retrain comparisons.** The paper adopts the Knowledge Deletion (KD) formulation (§2), which "no longer treats the retrain-from-scratch model as the sole point of reference." Yet the paper repeatedly presents "outperforming retrain" as a headline result (§4.1, Conclusion). If retrain is not the definitive reference under KD, the paper should clarify why surpassing it is the central result, or de-emphasize retrain comparisons.

- **Marginal benefit of multiple experts in standard evaluation.** Under standard evaluation, multi-expert MoRE shows minimal improvement over single-expert Remap (HM 95.30 vs. 95.38 on CIFAR-10, Table 1). The claimed benefit of "scattering forget features to break residual cohesion" mainly manifests in the KR setting, where the single-expert variant already achieves strong results. The paper's narrative emphasizes the multi-expert design as critical for irreversibility, but the empirical advantage is limited to specific evaluation conditions.

### Trivial

None.

## Nice-to-Haves

- Test against stronger recovery attacks (full-model fine-tuning, non-linear probes, adversarial recovery methods) would substantially strengthen the evidence for the paper's strongest claim.
- A dedicated analysis of the elevated MIA (Table 4) — whether it is a side-effect of the remapping mechanism or indicates a systematic information leak.

## Removed Points

These points were raised in the source review but removed or downgraded after verification against the paper:

1. **"KR metric is never defined in the main paper"** — Removed. The paper explicitly states "details in §B.3" (appendix). Per guidelines, missing appendix content from the parser is not a valid weakness.
2. **"Mixture of Experts framing is strained"** — Removed. The paper explicitly acknowledges (line 180): "Unlike the standard MoE, where experts improve prediction accuracy, in our proposed method, each expert specializes in remapping..." The paper qualifies the analogy.
3. **"UCE has a better LPIPS_d tradeoff"** — Removed as factually incorrect. Table 2 shows Ours LPIPS_d = 0.25 (Van Gogh) and 0.26 (Kelly McKernan), both higher than UCE's 0.20 and 0.22 respectively. Higher LPIPS_d is better per the paper's definition.
4. **"Stochastic router cannot selectively scatter forget features"** — Removed. The critic misunderstood Eq. 6: remapping is conditional on forget prototype activation via the diag(s)D detector term. Remain features that do not activate forget prototypes are not remapped.
5. **"Complement space analysis is missing"** — Removed. The paper explicitly derives the complement-space term (I − PD) in Eq. 4 and discusses it at lines 156–160.
6. **"t-SNE is not quantitative evidence"** — Downgraded. The paper uses t-SNE as qualitative illustration, not as primary quantitative evidence. Quantitative evidence comes from accuracy metrics and the KR metric.
7. **"Need d ≥ k for well-defined projection"** — Removed as a standard requirement acknowledged by the full-rank condition.
8. **Raising the MIA result as a "contradiction with the irreversibility narrative"** — Downgraded. MIA (membership inference) and class-level knowledge recovery measure different properties. The result deserves analysis but does not directly contradict the paper's core claim about feature-level unlearning.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Replace "irreversible" with language calibrated to the actual evidence, such as "strongly resistant to linear probing recovery" or "feature-level unlearning that prevents recovery via standard fine-tuning protocols."
2. Analyze the MIA results (Table 4) in more depth: discuss whether elevated MIA is a side-effect of the remapping mechanism or indicates a genuine information leak.
3. Clarify the relationship between the KD formulation (which de-emphasizes retrain as the reference) and the repeated "outperforming retrain" framing.

## Score and Decision

**Calibration summary:** All retrieved anchors with their avg scores and how they compare:

| Anchor | Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| SUN (training-free subspace unlearning) | 4.00 | R1 | Yes | Multiple fatal weaknesses (−8 to −10). MoRE is much stronger — cleaner methodology, broader evaluation. |
| Deep Unlearning (SVD-based class unlearning) | 5.25 | R1 | Yes | Had −9.89, −9.99, −9.82 weaknesses about missing theory/prior work. MoRE's weaknesses are less fundamental. |
| Unlearning via Sparse Representations | 5.25 | R1 | Yes | Incremental; model-specific. MoRE is more general and technically substantive. |
| Pseudo-Probability Unlearning (PPU) | 3.00 | R1 | Yes | Severe writing and methodological issues. Not comparable. |
| Decoupling Class Label (TARF) | 5.75 | R1/R2 | Yes | Had −9.94, −9.99, −9.67 weaknesses. MoRE is technically stronger. |
| Label-Agnostic Forgetting (LAF) | 6.00 | R2 | Yes | Multiple −9.xx weaknesses about flawed VAE formulation. MoRE's core methodology is sounder. |
| NegMerge | 6.00 | R2 | Yes | Incremental contribution; no fatal weaknesses. MoRE has a clearer technical advance. |
| Machine Unlearning for I2I Generative Models | 6.00 | R1 | Yes | Had −9.05, −9.12 weaknesses. MoRE's −10.00 overclaiming is a framing issue, not a methodological flaw. |

**Round 1 bracket:** [5.5, 7.5]. The paper is clearly above the 4–5 range (SUN, Deep Unlearning) which had fatal methodological or evaluation flaws. It sits in the 6–7 range alongside NegMerge (6.00) and Label-Agnostic Forgetting (6.00), but with one decisive weakness (−10.00 on overclaiming) that is a **framing/presentation issue** rather than a core methodological flaw. The paper's strengths are uniformly strong (+9.5 to +10). The core contribution (PO projection + remapping) is sound and well-validated. **Final score: 6.5** — the paper has a strong, practical contribution that merits acceptance after addressing the overclaiming.

**MY FINAL SCORE:** <score>6.5</score>
**MY FINAL DECISION:** <decision>Accept</decision>