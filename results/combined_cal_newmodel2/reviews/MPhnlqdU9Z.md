Here is my final, consolidated review.

---

## Summary

This paper introduces *monitorability*, a novel concept formalizing the extent to which a neural network's internal representations make its errors detectable at runtime. The authors propose the MIRA Score, which measures this property by perturbing ID inputs with FGSM, computing Mahalanobis distances between perturbed and unperturbed penultimate-layer activations, and converting them to a dimension-calibrated surprisal score via the χ² survival function. MIRA is validated as a proxy for monitorability by comparing it against the best achievable OoD detection performance (across ODIN, Mahalanobis, and Energy detectors) on vision (CIFAR-10/100), tabular (Sensorless Drive), and NLP (SST-2) domains.

## Strengths

- **The concept of monitorability as an intrinsic model property is genuinely novel.** No prior work has formalized the idea that models, independent of their accuracy, differ in how *detectable* their errors are via internal activations. The distinction between "the model makes an error" and "the model's internal state reveals that error" is meaningful and well-articulated. The toy example (Figure 1) cleanly illustrates this: two 100%-accurate models produce feature spaces of radically different quality for anomaly detection.

- **Cross-domain empirical scope is genuine and uncommon for a first paper on a new concept.** Experiments cover vision (CIFAR-10/100 with ResNet-18, DenseNet, CustomNet, ViT), tabular (Sensorless Drive with MLPs and Transformers), and NLP (SST-2 finetuning with RoBERTa, DistilBERT, ELECTRA, DeBERTaV3). This breadth demonstrates the phenomenon is not specific to one modality or architecture family.

- **The monotonic ordinal relationship between MIRA Score and best average OoD AUROC holds consistently across all three domains.** For vision (CIFAR-10 and CIFAR-100, Table 1), tabular (Table 2: WideMLP > MLP > DeepMLP > Transformer > DeepTransformer in both MIRA and best AUROC), and NLP (Table 3: DeBERTaV3 > ELECTRA > RoBERTa > DistilBERT in both), the ordering matches perfectly. This consistency is non-trivial and suggests MIRA captures something real about feature-space structure.

- **Efficiency advantage is concrete and well-identified.** Computing MIRA requires only ID data and cheap FGSM perturbations — no OoD data, no detector tuning, no grid search over calibration parameters. This is a practical advantage over running full OoD detection evaluations for model selection.

## Weaknesses

### Fatal

None.

### Major

- **No quantitative correlation statistic is reported anywhere in the paper.** The paper repeatedly states that MIRA "correlates with" or "aligns with" OoD detection performance (Abstract, Section 4.4, Conclusion), but no correlation coefficient (Spearman's ρ, Kendall's τ, or Pearson's r) is ever computed or reported. The evidence is entirely visual/ordinal: readers are asked to inspect Tables 1–3 and notice that the ordering matches. With only 3–5 data points per domain, a rank correlation is trivial to compute and would give a precise, falsifiable number to substantiate the central claim (RQ1). **This is the most significant evidential gap** — the central empirical conclusion is stated as a correlation but never quantified.

- **Perturbation-range selection introduces a systematic confound that could explain the observed correlation.** The paper selects ε_min per model as "the smallest value that reduces accuracy to a certain threshold" (Section 4.2), with ε_max = 2·ε_min. Robust models (e.g., ViT) require larger ε to reach the accuracy-drop threshold; fragile models (e.g., CustomNet) reach it at much smaller ε. Since larger perturbations mechanically produce larger feature displacements, and MIRA measures the separability of perturbed vs. unperturbed features, the metric could systematically favor robust models *simply because they are probed with larger perturbations*, not because their feature space is inherently more separable in a way that transfers to OoD detection. The paper acknowledges this as a limitation (Section 6) but does not analyze its impact. A fixed-ε control experiment is the minimal mitigation.

- **Mahalanobis-distance confound in the validation.** MIRA uses Mahalanobis distance on penultimate-layer activations (converted to a surprisal score via χ² survival function) to measure feature separability under perturbation. One of the three OoD detection methods used as the validation proxy — the Mahalanobis-distance-based detector of Lee et al. (2018b) — also operates on penultimate-layer activations using the same distance metric. Since the validation uses "best of three" aggregation, and the Mahalanobis detector is the best-performing method for most model/OoD-dataset combinations (appearing as the bold entry in most rows of Tables 1–3), the correlation between MIRA and the "best AUROC" proxy could partly reflect the shared use of Mahalanobis distance rather than a genuine relationship between monitorability and monitoring potential. The paper should report the correlation between MIRA and each of the three methods *separately*, not just the best-of aggregate.

### Minor

- **Definitional disconnect between the formal definition and the experimental validation.** Definition 1 defines *l*-monitorability with respect to ID data: ∀(x,y)~P_in, L(f(x),y) ≤ ε ⇔ f^l(x) ∈ Z^l — i.e., detecting misclassifications on ID inputs from activation patterns. However, the intuition (Figure 1, using OoD samples), the MIRA metric (perturbations pushing ID inputs toward decision boundaries, simulating boundary crossing), and the experimental validation (OoD detection AUROC) are all centered on detecting OoD inputs, not ID misclassifications. The paper acknowledges in Section 2 that "misclassifications may also occur for ID inputs, which is a distinct scenario not directly addressed by OoD detection," but never bridges this gap in the validation. A targeted experiment using deliberately misclassified ID samples (via label noise or adversarial patches) would substantiate the claimed connection.

- **Definition 1 formulates monitorability as a perfect-separation condition** (there exists a set Z^l such that *all* correct predictions map into it and *all* errors map outside it). The paper concedes Z^l "may be arbitrarily complex" (line 73), meaning no real classifier is likely to satisfy this condition. The definition functions as an abstract ideal rather than a property that can be empirically tested or approximately measured. A relaxation (e.g., degree of *approximate* l-monitorability, measured by the AUC of a classifier trained on f^l(x) to predict whether L(f(x),y) ≤ ε) would bridge the gap between theory and practice.

- **No error bars, confidence intervals, or variance estimates are reported** for any MIRA score or AUROC value. Given that MIRA involves sampling perturbations and computing expectations (Equation 4), bootstrapped confidence intervals would be informative and straightforward to compute.

- **The interpretation of negative MIRA values is incomplete.** CustomNet receives MIRA = -0.07, which the paper interprets as "perturbed data are less detectable than ID data, showcasing very bad monitoring capabilities." However, since MIRA normalization uses S₀ = E[S(f^l(x))] as a baseline, a negative value could also indicate that the Gaussian assumption underlying the χ²-to-surprisal conversion is a poor fit for this model's features. This alternative explanation is not discussed.

- **The RQ3 claim that MIRA "provides insights not tied to the limitations of any single detection method" is overstated.** The evidence given (the Mahalanobis detector failed with Places365 for DenseNet but other methods performed well) only shows that using the maximum over three methods is more robust than any single method — it does not demonstrate that MIRA predicts performance on unseen detectors or captures monitoring potential independently of detector-specific properties. MIRA is validated against the *best* of three methods, not across a broader set of unseen detectors.

### Trivial

None.

## Nice-to-Haves

- The paper uses FGSM exclusively for perturbations. An ablation using a stronger adversarial method (e.g., a few PGD steps) or a weaker random perturbation would test whether the specific choice of perturbation method matters. The paper claims "the strength of the attack is not critical" (Section 4.2) but provides no evidence for this.
- All experiments use the penultimate layer, but the paper claims MIRA can "guide design decisions such as selecting the most suitable layer for feature-based monitoring" (Conclusion). Some demonstration of layer-wise MIRA would strengthen this claim.
- Validate against ID misclassifications (as noted in Minor weaknesses) to bridge the definitional gap.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Table 1 formatting complaint (Average column ambiguity)**: This is a PDF-extraction artifact; the original table formatting is not the authors' responsibility.
- **Formatting nitpicks (presentation issues, notation clarity complaints)**: These are parsable as PDF-extraction artifacts or minor style preferences that do not affect the paper's content.
- **Missing related works**: As the meta-reviewer, I cannot confirm relevant missing citations without external sources.
- **Missing appendix details**: The parser strips appendices from all papers; they exist in the original submission.
- **The critic's framing of the Mahalanobis confound as potentially "fatal"**: This is too strong. The shared distance metric creates a confound but does not invalidate the approach since MIRA uses the distance in a fundamentally different way (on perturbed ID inputs integrated over ε, converted to a χ²-based surprisal score) than the OoD detector (which operates on real OoD inputs at a single threshold).
- **Speculative claim that the Mahalanobis detector "happens to be the best-performing method for most model/OoD-dataset combinations"**: This is factually verified from Tables 1–3 (Mahalanobis appears in bold for most rows), so it is kept in the weakness but downgraded from the critic's implied severity.
- **Strength that "the density and format of Table 1 is ambiguous"**: This is a parser artifact.
- **Generic/inflated strengths from the harsh critic**: "The framing is clear and motivation is well-articulated" — dropped as generic and lacking specific evidence anchor.
- **Strengthen-the-paper suggestions that overlap with already-listed weaknesses**: These are absorbed into the relevant weakness entries above.

## Novel Insights

None beyond the paper's own contributions. The input reviews surface validity concerns but do not offer novel positive insights about the paper beyond what the authors themselves present.

## Suggestions

1. **Compute and report Spearman rank correlation** between MIRA and best average AUROC for each domain separately and, after normalizing MIRA values appropriately, pooled across domains. This immediately quantifies the paper's central claim.
2. **Run a fixed-ε control experiment**: compute MIRA while holding ε fixed at a common value across models and compare the resulting rankings to the current adaptive-ε procedure. If the rank-order is preserved, the confound is mitigated.
3. **Report correlation between MIRA and each of the three OoD detection methods separately**, not just the "best of" aggregate. This disentangles whether the shared Mahalanobis machinery drives the result.
4. **Add bootstrapped confidence intervals** to MIRA scores and AUROC values.
5. **Clarify the relationship between Definition 1 (ID error detection) and the OoD-based validation** — either by arguing why OoD detection is a reasonable proxy for ID-error detectability, or by adding a targeted experiment with deliberately misclassified ID samples.

## Calibration Anchors

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| nSDOkm0SKo (Financial markets NN) | 1.00 | R1 | No | Irrelevant topic, low quality — far below this paper |
| gwZ90hFSL2 (Humanoid robots) | 1.00 | R1 | No | Irrelevant topic — far below |
| P49gSPmrvN (Discourse visualization) | 1.00 | R1 | No | Irrelevant — far below |
| l5ouuojPGe (Thresholding for NN monitoring) | 3.00 | R1 | Yes | Related topic (NN monitoring) but more incremental; this paper's concept is more novel |
| hr4HTShC6l (Shortcut detection) | 3.00 | R1 | No | Related (detecting model issues) but different focus |
| KK29oh8jZs (OOD probing synthetic datasets) | 3.00 | R1 | Yes | Related domain (OOD detection) but simpler contribution |
| Nx8lVqyKeZ (Membership inference) | 4.25 | R3 | No | Different topic |
| hoEanaoP4i (**MD-LSM** — linear separability monitoring) | 6.00 | R1,R3 | Yes | **Closest anchor**: same type of contribution (new metric for hidden-layer analysis). MD-LSM has stronger theory but only CIFAR-10 experiments; MIRA has broader scope (3 domains) but weaker quantitative evidence. MIRA is slightly below MD-LSM due to missing statistics and confounds. |
| upALuXjdxc (Error Slice Discovery) | 6.00 | R3 | Yes | Similar structure (new metric + algorithm). Thorough experiments but limited domain scope. MIRA is comparable in novelty but weaker in quantitative rigor. |
| 83le3arfeA (Hyperbolic OOD) | 5.50 | R3 | No | Related (OOD detection). MIRA has a more novel concept. |
| 9ROuKblmi7 (NECO — neural collapse OOD) | 5.75 | R3 | No | Related (OOD detection). More polished empirical paper but less novel concept. |
| oKglS1cFdb (OOD generalization with ID data) | 5.67 | R3 | No | Related topic. |
| ByCV9xWfNK (Intermediate Layer Classifiers) | 6.33 | R3 | No | Related (hidden-layer analysis). Stronger empirical paper. |
| xQit6JBDR5 (OOD detection relative angles) | 5.50 | R3 | No | Related (OOD detection method). More mature but less novel concept. |
| 9qpdDiDQ2H (MetaOOD) | 5.25 | R3 | No | Related (OOD model selection). More polished but less foundational. |
| todLTYB1I7 (Neuron explanations evaluation) | 5.00 | R3 | Yes | Different topic (interpretability evaluation). |

**Bracket (Round 1):** 5.0 – 6.0 (based on MD-LSM at 6.00 being the closest methodological anchor, and the paper's missing statistics placing it slightly below that anchor).

**Narrowing (Rounds 2–3):** Comparing against MD-LSM (6.00), the MIRA paper shares the type of contribution (new metric for neural network representation analysis) but has a weaker quantitative foundation (no correlation statistics, unanalyzed confounds vs. MD-LSM's theoretical derivations). Its cross-domain breadth (3 domains vs. CIFAR-10 only) partially compensates, but the evidential gap in the central claim prevents it from reaching MD-LSM's level. Comparing against NECO (5.75, accepted), the MIRA paper has a more novel concept but weaker empirical validation. The final score of 5.5 reflects a paper with a genuinely novel idea and broad initial experiments, but whose central claim remains unquantified and subject to two unaddressed confounds.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>