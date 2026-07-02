## Summary

This paper addresses the **copy-paste artifact** in identity-consistent image generation—a failure mode where models replicate the reference face exactly rather than synthesizing the identity across natural variations. The authors contribute (1) **MultiID‑2M**, a large-scale paired dataset of 500k multi-person images with references per identity; (2) **MultiID‑Bench**, a benchmark that explicitly quantifies copy-paste artifacts via a new metric; and (3) **WithAnyone**, a diffusion-based model that uses a four-stage training pipeline with a ground-truth-aligned ID loss and an ID contrastive loss to achieve high identity fidelity while substantially reducing copy-paste. Experiments show that WithAnyone breaks the typical trade-off between identity similarity and copy-paste, achieving state-of-the-art results among face-customization models.

## Strengths

- **Clear identification and formalization of an underexplored problem.** The “copy-paste” failure mode is well motivated with concrete evidence (Fig. 2) and a precise metric (Eq. 2). This provides a valuable lens for evaluating and designing ID‑consistent models.
- **Large-scale paired dataset and benchmark.** MultiID‑2M (500k paired multi‑person images + 1.5M unpaired) and MultiID‑Bench fill a critical gap in the community. The benchmark includes a novel copy‑paste metric and uses Sim(GT) rather than Sim(Ref), which penalizes trivial copying.
- **Strong empirical results.** WithAnyone consistently outperforms state-of-the‑art face‑customization models on both identity metrics and generation quality (Tables 1–2). Figure 5 convincingly shows it lies above the trade‑off curve. Ablations (Table 3, Fig. 7) isolate the contribution of each component.
- **Thorough evaluation.** The paper compares against 14 baselines, includes user studies (Fig. 8), and provides ablation studies on both the dataset and training losses.
- **Open source and ethical considerations.** The dataset, code, and benchmark are released. The ethics section addresses data sourcing, anonymization, and dual‑use risks.

## Weaknesses

### Fatal
None.

### Major
- **Reproducibility limited by FLUX license.** WithAnyone is built on the FLUX backbone, which is released under a non‑commercial license. While the authors open‑source their code and dataset, the base model license restricts practical adoption and full reproducibility for many research groups.
- **Dataset bias and ethical concerns.** The dataset is constructed from web‑scraped images of public figures. Even with CC filtering, this raises concerns about consent and potential misuse. The paper acknowledges these but does not provide a mechanism for individuals to request removal or opt out.

### Minor
- **Copy‑paste metric relies on ground‑truth images.** The benchmark requires a ground‑truth target image to compute the copy‑paste metric. This limits its use to controlled evaluation; practitioners cannot easily measure copy‑paste when ground truth is unavailable.
- **Some baselines are missing or constrained.** DynamicID is excluded due to unavailability, and GPT‑4o may have prior knowledge of public figures (acknowledged). The comparison set, while broad, is still incomplete.
- **Complex training pipeline.** The four‑phase training recipe is effective but computationally expensive and may be sensitive to hyper‑parameters. The paper does not discuss the total compute cost or sensitivity to phase durations.

### Trivial
- Figure 8 uses placeholder names (“Cure”, “iDetch” instead of “WithAnyone”, “ID‑Patch”). This appears to be a formatting issue from the PDF extraction; the authors should correct it.
- The paper is dense; some architectural details (e.g., the exact negative pool size) are only in the appendix.

## Nice-to-Haves

- Release model weights (under a suitable license) to increase reproducibility despite FLUX restrictions.
- Provide a non‑celebrity test set to evaluate generalization beyond public figures.
- Analyze failure cases where WithAnyone still shows copy‑paste or identity blending.
- Investigate the computational cost and provide a comparison of training wall‑time with other methods.

## Novel Insights

The key insight is that existing metrics (Sim(Ref)) inadvertently reward copy‑paste, and the paper introduces a principled way to measure and penalize it. The observation that most methods lie on a trade‑off curve while WithAnyone escapes it (Fig. 5) is particularly compelling. The paired‑training strategy—using different reference and target images of the same identity—is a simple but effective idea that directly breaks the reconstruction shortcut.

## Suggestions

- Clarify in the main text the size of the negative pool used in the contrastive loss (currently only mentioned in the ablation as “extended to 4096”).
- Consider adding a per‑identity consent mechanism or a takedown policy for the dataset.

## Score and Decision

The paper makes strong, well‑validated contributions to an important problem in identity‑consistent generation. The dataset, benchmark, and method are significant and likely to have lasting impact. While the reliance on FLUX and data‑sourcing ethics are non‑trivial concerns, they do not invalidate the core contributions. The paper is clearly within the top tier of ICLR submissions.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>