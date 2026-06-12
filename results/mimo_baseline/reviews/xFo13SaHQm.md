## Summary

This paper identifies and formalizes the "copy-paste" artifact in identity-consistent image generation, where models overfit to reference images rather than preserving identity across natural variations. The authors contribute: (1) MultiID-2M, a large-scale paired multi-identity dataset (~500k group photos with per-identity reference banks); (2) MultiID-Bench, a benchmark with novel copy-paste metrics; and (3) WithAnyone, a FLUX-based model trained with a contrastive identity loss leveraging extended negatives and GT-aligned landmarks, demonstrating reduced copy-paste while maintaining strong identity fidelity.

## Strengths

- **Well-identified and formalized problem.** The copy-paste artifact is a genuine and previously under-quantified failure mode in identity-preserving generation. The copy-paste metric (Eq. 2) is well-designed, and the scatter plot in Fig. 5 convincingly demonstrates the fidelity-vs-copying trade-off across 12+ methods, with WithAnyone visibly breaking this trade-off.

- **Large-scale paired dataset contribution.** MultiID-2M is a significant resource with ~500k labeled group photos across ~25k identities with diverse reference images per identity. The four-stage construction pipeline is clearly described, and the inclusion of 1.5M additional unpaired images adds value. This addresses a genuine data bottleneck in the field.

- **Comprehensive benchmark and evaluation.** MultiID-Bench with 435 test cases using long-tail identities not in training data is well-designed. Evaluating 12+ diverse baselines (both general customization and face-specific methods) on both single and multi-person subsets provides thorough coverage. The decision to use Sim(GT) as primary metric rather than Sim(Ref) is a meaningful methodological contribution that corrects a subtle evaluation bias in prior work.

- **Effective technical approach.** The GT-aligned landmark ID loss is a clever and practical solution that avoids unreliable landmark detection on noisy/denoising images while enabling supervision at all noise levels. The contrastive loss with extended negatives (4096 from the reference bank) is well-motivated by the paired dataset structure. Ablation studies (Table 3, Fig. 7) provide clear evidence for each component's contribution.

## Weaknesses

### Fatal
None.

### Major

- **Inconsistency between automated aesthetic scores and user study claims.** WithAnyone consistently achieves the *lowest* or near-lowest automated aesthetic scores across all settings (4.783 in Table 1 vs. 5.255 for InstantID, 5.344 for GPT-4o; 4.883 in ablation Table 3). Yet the paper claims "superior visual quality" from user studies. This discrepancy is not discussed and raises questions about whether quality is being traded off for identity consistency. This deserves explicit acknowledgment and analysis.

- **Small user study.** Only 10 participants ranking 230 groups is quite limited for drawing reliable conclusions, especially regarding aesthetics where subjective variance is high. The claim that the copy-paste metric shows "moderate positive correlation" with human judgments would benefit from formal statistical reporting (confidence intervals, inter-rater agreement metrics).

### Minor

- **Celebrity-only benchmark may limit generalizability.** MultiID-Bench evaluates only on celebrity/long-tail public figures. Since the model is trained on celebrities, the benchmark tests interpolation rather than true out-of-distribution generalization to arbitrary identities. A brief discussion of this limitation would strengthen the paper.

- **ArcFace threshold of 0.4 for identity matching.** The paper uses cosine similarity threshold 0.4 for assigning identities between single-ID and multi-ID images, but provides no analysis of false positive/negative rates. Given that the entire training pipeline depends on correct identity pairing, some validation of matching accuracy would be reassuring.

- **Ablation of Phase 3 shows mixed results.** Removing Phase 3 (paired tuning) actually *improves* Sim(GT) from 0.405→0.406 and Sim(Ref) from 0.551→0.625 while only worsening CP from 0.161→0.239. The full model's advantage in this ablation appears primarily in CP reduction rather than identity improvement, suggesting the paired tuning mainly suppresses copying rather than enhancing identity preservation—a nuance worth discussing.

## Nice-to-Haves

- A discussion of failure cases where WithAnyone still exhibits copy-paste or identity loss.
- Analysis of how the method performs on non-celebrity, truly novel identities not seen during training.
- Formal reporting of inter-rater agreement in the user study and explicit discussion of the aesthetic score discrepancy.

## Novel Insights

The paper makes a genuinely novel conceptual contribution by formalizing the copy-paste artifact as a distinct failure mode and demonstrating that traditional Sim(Ref) metrics inadvertently reward it. The key insight—that reconstruction-based training creates a shortcut that incentivizes direct copying rather than identity understanding—is well-supported by the density plot analysis in Fig. 2 and the comprehensive trade-off analysis in Fig. 5. The finding that this trade-off can be broken through paired training with contrastive objectives on identity-labeled data is an important practical contribution that extends beyond this specific model architecture.

## Suggestions

- Add explicit discussion of the aesthetic score trade-off and reconcile it with user study findings.
- Expand the user study or provide statistical analysis of significance.
- Include a brief analysis of identity matching accuracy in the dataset construction pipeline.

## Score and Decision

The paper addresses a real and under-studied problem in identity-consistent generation, provides a large-scale dataset and benchmark that will benefit the community, and demonstrates a technically sound approach that convincingly breaks the fidelity-vs-copying trade-off. The aesthetic quality trade-off and limited user study are notable but do not invalidate the core contributions. The dataset alone represents a significant community resource.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>