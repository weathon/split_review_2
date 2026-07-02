## Summary
This paper identifies a theoretical limitation in HiResCAM interpretability methods, proving that HiResCAM explanations are not uniquely determined and can be arbitrarily shifted by a common matrix M without changing the model's probability predictions. The authors propose ContrastiveCAMs that are invariant to this spurious shift and provide granular class-versus-class explanations. Using ContrastiveCAMs to reveal that models often rely on non-core regions, they introduce Core-Focused Cross-Entropy (CFCE) that penalizes contributions from non-core regions during training, demonstrating improved feature alignment on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC.

## Strengths
- The theoretical analysis of HiResCAM's non-uniqueness (Theorem 3.2) is a novel and rigorous contribution that identifies a genuine limitation of a widely-used interpretability method. The proof is clear and the implication—that explanations can be arbitrarily corrupted—is significant for the interpretability community.
- The proposed ContrastiveCAMs elegantly resolve the identified redundancy while additionally providing class-versus-class comparisons, which yield richer insights than standard CAM approaches. The invariance result (Theorem 3.5) is clean and well-motivated.
- The connection between interpretability and feature alignment is compelling. The paper provides theoretical reasoning (Proposition 4.2) for why cross-entropy can incentivize reliance on non-core features, and the CFCE loss directly addresses this. The consistency result (Theorem 4.6) supports the soundness of the approach.
- Experimental results are thorough, covering multiple datasets (Hard-ImageNet, Oxford-IIIT Pets, PASCAL VOC), multiple classification settings (binary, multiclass, multilabel), and downstream segmentation tasks. The ablation studies with approximate masks (SAM, bounding boxes) demonstrate practical applicability.

## Weaknesses
### Fatal
None.

### Major
1. **The practical significance of the HiResCAM redundancy is overstated.** Theorem 3.2 shows that adding the same arbitrary matrix M to all class-level CAMs preserves the probability predictions. However, the paper does not demonstrate that this theoretical non-uniqueness actually leads to misleading explanations in practice. The redundancy ratio γ reported in Table 1 (0.201–0.367) measures the Frobenius norm of the average CAM relative to a specific class CAM, not the degree to which arbitrary M corrupts explanations. The paper would be significantly stronger with an experiment showing that different but plausible M choices produce qualitatively different, misleading explanations for trained models.

2. **Computational and practical overhead is unaddressed.** ContrastiveCAMs require computing HiResCAMs for all pairs of classes, which scales quadratically with the number of classes C. For ImageNet-scale classification (C=1000), this means computing 1,000 HiResCAMs per image per training iteration. The CFCE loss then aggregates over all pairwise ContrastiveCAMs. The paper does not discuss this computational cost, nor does it report training time comparisons. This is a critical practical concern for adoption.

3. **The core mask requirement is a significant limitation.** CFCE requires pixel-level or bounding-box masks H for every training image. The paper attempts to address this with SAM-generated and bounding-box masks, but the experiments show that CFCE+KL with SAM masks underperforms ground-truth masks on some metrics (e.g., IoU on Oxford-IIIT Pets binary: 83.54% vs 92.72%). More importantly, the paper does not establish that CFCE works on datasets *without* any mask supervision available, which is the majority of real-world scenarios. This limits applicability.

4. **Accuracy degradation is not adequately discussed.** On Hard-ImageNet, CFCE reduces un-ablated accuracy from 94.25% to 90.53% (Table 2). The paper frames this as "at the cost of some un-ablated performance," but a ~4% drop on a fine-tuned model is substantial. Without analysis of whether this drop is due to the loss function itself, training instability, or a genuine trade-off, it's unclear whether the approach is practical for high-stakes applications where accuracy matters most.

### Minor
- The paper claims that cross-entropy "can motivate feature misalignment" (Section 4.1), providing a theoretical basis via Proposition 4.2. However, this proposition simply shows that cross-entropy can be decomposed into core and non-core contributions—it does not prove that cross-entropy *preferentially* encourages non-core feature use. The statement "does not inherently favor using the core or non-core regions" is accurate, but the stronger claim of "motivating misalignment" is not fully supported.
- The divergence regularization term (Definition 4.7) introduces three hyperparameters (λ₁, λ₂, λ₃) without sensitivity analysis. The paper would benefit from an ablation study showing how performance varies with these choices.
- Figure 2 is difficult to interpret: the "dog sled" panel shows ContrastiveCAM visualizations labeled as "1/2" and "1/3" without clear explanation of what these pairs represent in the caption.

### Trivial
- In Table 1, the "Redundancy (γ)" column for PASCAL VOC is marked with a dash and a superscript "1", but the footnote is not present in the provided content.
- In Equation (12), the summation over CAM *after* the elementwise product with (1-H) appears to be summing over all spatial locations, but the notation is slightly ambiguous.

## Nice-to-Have
- An experiment demonstrating that HiResCAM explanations from real trained models can be flipped or significantly altered by adding an M that is non-arbitrary (e.g., constructed from known spurious features) without changing predictions would strongly validate the practical importance of Theorem 3.2.
- A discussion of whether the quadratic class-pair computation for ContrastiveCAMs can be approximated (e.g., using only top-k competing classes) for large-scale settings.
- A comparison to alternative feature alignment methods beyond CORM and DFR, such as simple input masking (removing backgrounds during training) or attention-based regularization.

## Novel Insights
Beyond the paper's own contributions, the most novel insight is the formal connection between the *scale-invariance* of softmax and the *non-uniqueness* of CAM-based explanations. While it is well-known that softmax is invariant to constant shifts, the paper's key observation that this invariance amplifies to a *spatial redundancy* in HiResCAMs (allowing an entire matrix M to be added to every class explanation) is a genuinely non-obvious and important theoretical finding. This illustrates a subtle failure mode in interpretability: explanations that are mathematically consistent with model outputs can nevertheless be arbitrarily misleading. The paper's framing of this as a "redundancy" rather than outright incorrectness is precise and useful.

## Suggestions
1. Add an experiment showing a practical case where the M-shift ambiguity leads to qualitatively different explanations for a real trained model, using a plausible M derived from the data (e.g., the average of all class CAMs or a prototypical background pattern).
2. Report training time overhead for CFCE relative to standard cross-entropy, especially for the Hard-ImageNet (C=10) and PASCAL VOC (C=20) settings, and discuss scalability.
3. Provide a sensitivity analysis for the divergence regularization hyperparameters (λ₁, λ₂, λ₃).
4. Discuss the accuracy trade-off more thoroughly: is the ~4% drop on Hard-ImageNet a fundamental limitation, or could it be mitigated with additional training or architectural modifications?

## Score and Decision
The paper makes a strong theoretical contribution in identifying and resolving a genuine limitation of a popular interpretability method, and the proposed training approach is well-motivated by this theory. The experiments convincingly demonstrate improved feature alignment on multiple benchmarks. The main concerns are the overstatement of practical impact of the theoretical finding (not demonstrated to cause misleading explanations in practice), the computational cost of the approach, and the requirement for core-region masks that limits applicability. These are significant but not fatal. The paper is a solid contribution to the interpretability and alignment literature.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>