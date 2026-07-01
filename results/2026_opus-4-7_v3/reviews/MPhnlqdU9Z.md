Now I've read the full paper. Let me verify a few key details before drafting.Now let me submit my draft review before calibration.Now let me do Round 1 calibration — bracketing across score bands.Let me read key anchors for calibration comparison.Now I have sufficient calibration data. Let me form my bracket and finalize the review.

**Round 1 Bracket Analysis:**

- **Score 1.0 anchors**: Completely broken/pseudoscience papers (financial news NN, UMAP time-dependent). MIRA is clearly far above these.
- **Score 2.5-3.0 anchors**: "Red Pill or Blue Pill" (3.0, NN monitoring thresholds) was rejected for limited contribution and unsurprising findings; "Unified AL+OOD" (2.5) rejected for overclaims and limited improvement. MIRA has a stronger novel concept than both.
- **Score 4.5 anchors**: NC-OOD papers (4.5) with weak hypothesis justification and limited novelty over Mahalanobis/KNN. Similar theory-practice gap to MIRA.
- **Score 5.25 anchor**: KAN-based OOD (5.25) — novel approach with scalability concerns but clearer validation. Borderline accepted.
- **Score 6.5 anchor**: "Double Descent + OOD" (6.5) — stronger theoretical grounding via Random Matrix Theory with formal theorems and comprehensive experiments. Above MIRA.
- **Score 7.0+ anchors**: Strong papers with convincing theory-experiment bridges. Above MIRA.

**Initial bracket: 4.0–5.5.** The concept is genuinely novel (above 3.0 anchors), but the validation methodology has multiple interrelated weaknesses (definition-metric gap, circularity, no statistics, capacity confound) that prevent it from reaching the 6.0+ level of papers with convincing validation.

Now let me write the final review.Now I have enough calibration to finalize. Let me write the complete review.

---

## Summary
This paper introduces *monitorability* as an intrinsic property of neural networks — capturing whether a model's internal activations permit runtime detection of erroneous predictions — distinct from the effectiveness of any particular OoD detector. The authors provide a formal definition (Definition 1) and propose the MIRA Score, a practical metric based on Mahalanobis-distance surprisal of FGSM-perturbed inputs computed without external OoD data. Validation across vision (CIFAR-10/100), tabular (Sensorless Drive), and NLP (SST-2) modalities shows MIRA's rank ordering of models matches the best-achievable OoD detection performance.

## Strengths
- **Novel and well-motivated concept.** The distinction between *detecting* OoD inputs (detector-dependent) and whether a model's representations *permit* such detection (intrinsic model property) is clearly articulated and genuinely fills a gap. Figure 1 concretely demonstrates that two models with identical ID accuracy can differ dramatically in feature-space separability of OoD inputs, motivating the concept with a visual that is immediately intuitive (Section 3.1).

- **No dependence on external OoD data.** MIRA is computed using only ID data and FGSM perturbations (Section 3.3, Eq. 4), making it usable as a pre-deployment evaluation tool without requiring curated OoD datasets or detector-specific hyperparameters — a genuine practical advantage stated clearly in the paper: *"MIRA is not designed as a runtime detection method but as a pre-deployment evaluation metric"* (line 103).

- **Consistent rank ordering across three modalities.** Tables 1–3 show perfect rank agreement between MIRA scores and best-achievable OoD detection performance across vision (4 models), tabular (5 models), and NLP (4 models), spanning CNNs, MLPs, and transformer architectures. While sample sizes are small, consistent agreement across such diverse settings is non-trivial for a first metric paper.

- **Sound dimension-calibrated normalization.** Converting Mahalanobis distance into surprisal via the chi-square survival function (Eq. 3) enables meaningful comparison across layers/architectures of different dimensionality — a necessary design choice that is well-justified.

## Weaknesses

### Fatal
None

### Major
- **Gap between formal definition and practical metric.** Definition 1 (Section 3.2) defines l-monitorability as the existence of a set Z^l such that *loss ≤ ε ⟺ f^l(x) ∈ Z^l* — a biconditional about separating correct from incorrect predictions. The MIRA Score (Eq. 4) measures how much Mahalanobis-based surprisal of FGSM-perturbed inputs exceeds that of clean inputs — measuring perturbation separability, not error separability. The paper acknowledges this gap (*"Definition 1 provides an abstract formalization... but it does not quantify how monitorable a neural network is"*, line 81) and offers a thin informal bridge via Lee et al. (2018a)'s finding that *"local boundary behavior can generalize to unseen shifts"* (line 89), but no formal or substantial informal argument maps MIRA values to the properties of Z^l in Definition 1. Additionally, Definition 1 is binary (Z^l exists or it does not) while MIRA is continuous, with no explanation of what a higher score means in terms of the formal definition. This leaves the theoretical and practical contributions loosely coupled.

- **Partial circularity in validation.** MIRA is built on Mahalanobis distance (Eq. 3). The validation is against "best-of" ODIN, Mahalanobis distance, and Energy scoring. Inspecting Tables 1–3, the Mahalanobis detector is bolded as the best-performing method in the vast majority of cells (e.g., every single model in Table 2, every model in Table 3). When the best-of is Mahalanobis-dominated, correlation between MIRA (Mahalanobis-based) and the validation target is partially tautological — both rely on the same Gaussian class-conditional fit. The paper does not report correlations with each detector separately, so it is impossible to assess whether MIRA correlates equally well with ODIN or Energy scoring, which do *not* share MIRA's mathematical core.

- **No formal correlation statistics for a metrics paper.** The paper's central empirical claim is that MIRA *"correlates with"* OoD detection performance (Section 4.4, Section 6), yet no correlation coefficient (Spearman ρ, Kendall τ), confidence interval, or hypothesis test is reported anywhere. With only 3–5 models per setting, the claim rests entirely on visual rank agreement. With n=4, perfect rank agreement by chance has probability 1/24 ≈ 4%, which is marginally suggestive but insufficient for a paper whose primary contribution is a quantitative metric. This is especially concerning because the models span very different capacities (CustomNet vs. pretrained ViT), so any capacity-correlated metric would likely produce similar orderings.

### Minor
- **Proxy mismatch with stated definition.** Definition 1 covers detection of all errors including misclassified ID inputs (the paper acknowledges in Section 2: *"misclassifications may also occur for ID inputs, which is a distinct scenario not directly addressed by OoD detection"*), but validation uses exclusively OoD detection. The paper honestly calls this a "proxy" (Section 4.1), but the absence of misclassification detection experiments represents a gap between what the formal definition covers and what the experiments validate.

- **S₀ normalization creates cross-modality interpretability issues.** MIRA scores range from single-digits (vision, Table 1) to thousands (NLP, Table 3: DeBERTaV3 at 3793). This order-of-magnitude variation likely arises because S₀ can be very small when the Gaussian assumption fits well, inflating the ratio. While MIRA is designed for within-modality comparison, the paper does not discuss this interpretability limitation.

- **ε selection confound.** The model-dependent perturbation range (ε_min from accuracy threshold, ε_max = 2·ε_min, Section 4.2) confounds MIRA with model gradient norms. Models with smoother loss landscapes require larger ε, potentially producing different MIRA values for reasons unrelated to monitorability. The paper acknowledges this as a limitation (Section 6), but it remains unresolved.

- **Weak support for RQ3.** The claim that *"MIRA captures intrinsic monitoring potential even when individual detectors disagree"* (Section 4.4) is supported by a single observation (DenseNet + Places365 in Table 1 where the Mahalanobis detector underperforms), which is anecdotal rather than systematic evidence.

### Trivial
None

## Nice-to-Haves
- Evaluate MIRA against misclassification detection on ID data (directly aligned with Definition 1).
- Report MIRA sensitivity to perturbation method (PGD, random noise vs. FGSM) and to layer choice (not just penultimate).
- Compare models of similar capacity but different training procedures (e.g., same architecture with different augmentation, regularization, or objectives) to isolate the monitorability signal from the capacity signal.
- Formally connect Definition 1 to MIRA: define a continuous degree of monitorability in terms of correct/incorrect prediction separability, then show MIRA approximates it under Gaussian assumptions.
- Report per-detector correlation statistics (Spearman/Kendall) to address the circularity concern.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"The formal definition and metric are essentially independent contributions"**: Overstated by the reviewer. The paper explicitly positions Definition 1 as an abstract formalization and MIRA as a practical estimation tool (line 81). While the connection is informal, calling them "independent" ignores the shared intuition about feature-space structure supporting error detection. The gap is real but the characterization as total independence is too strong.

- **"Definition 1 only covers P_in, not OoD"**: This framing misunderstands the design intent. The perturbation-based approach is specifically designed to probe boundary behavior using only ID data, which is MIRA's value proposition. The formal definition scoping to P_in is a design choice aligning with the no-OoD-data requirement, not a flaw.

- **"The claim about DenseNet + Places365 (RQ3) is anecdotal evidence"**: While technically correct that one observation is anecdotal, the reviewer elevated this to a critical issue when it is actually a minor observation in the Discussion section (Section 4.4), not a central claim of the paper.

## Novel Insights
The paper introduces a genuinely novel conceptual reframing: separating the question "can this OoD detector detect anomalies?" from the more fundamental "does this model's representation even permit anomaly detection?" This shifts evaluation from detectors to models themselves and could influence how practitioners select architectures for safety-critical deployment. The observation that models with identical ID accuracy can have vastly different monitorability (Figure 1; CustomNet receiving a negative MIRA score while ViT scores 89.25 on the same CIFAR-10 task) is an actionable insight for model selection.

## Suggestions
- Report Spearman ρ and Kendall τ correlations for each OoD detector individually (not just the best-of aggregate) across all experimental settings.
- Include same-architecture experiments varying only training procedure (augmentation, regularization, objective) to disentangle monitorability from model capacity.
- Add misclassification detection experiments as a second validation axis aligned with Definition 1's scope.
- Provide at minimum an informal theoretical argument (ideally a proposition under stated assumptions) showing that higher MIRA implies a Z^l with simpler geometry or wider margins, bridging Definition 1 and the metric.

## Score and Decision

**Calibration anchors (all rounds):**

| Anchor | Avg Score | Round | Comparison to MIRA |
|---|---|---|---|
| `nSDOkm0SKo.md` (Financial NN) | 1.0 | R1 | Completely broken paper; MIRA far above |
| `P49gSPmrvN.md` (UMAP scientific discourse) | 1.0 | R1 | Trivial/pseudoscience; MIRA far above |
| `Uj0h13lVrR.md` (KL Divergence GFlowNets) | 1.0 | R1 | Fundamentally flawed; MIRA far above |
| `gwZ90hFSL2.md` (Chinese NLP robots) | 1.0 | R1 | Not a real ML paper; MIRA far above |
| `l5ouuojPGe.md` (NN monitoring thresholds) | 3.0 | R1 | Same domain (NN monitoring), rejected for limited contribution and unsurprising findings; MIRA has a stronger novel concept |
| `rcKzU0Vns0.md` (Unified AL + OOD) | 2.5 | R1 | Rejected for overclaims and limited improvement; MIRA has clearer novelty |
| `6Z8rZlKpNT.md` (NormFlow OOD) | 3.4 | R1 | Rejected for limited novelty; MIRA introduces a genuinely new concept |
| `KK29oh8jZs.md` (Synthetic OOD benchmarks) | 3.0 | R1 | Rejected for limited scope; MIRA covers more ground |
| `VAmVEghgoC.md` (NC-OOD) | 4.5 | R1 | Similar theory-practice gap; comparable methodology concerns |
| `Gr8nHvOivO.md` (Neural Collapse OOD) | 4.5 | R1 | Duplicate of above topic; both have weak hypothesis-validation bridge |
| `YMgMGPjUPg.md` (Neural Activation Prior) | 4.75 | R1 | Feature-based OOD scoring; mixed reviews with some similar validation concerns |
| `1F8xTfv6ah.md` (KAN OOD) | 5.25 | R1 | Novel approach with clearer direct validation; MIRA has broader scope but weaker per-claim evidence |
| `ljwoQ3cvQh.md` (DNNs Extrapolate Predictably) | 7.0 | R1 | Much stronger theoretical backing and empirical breadth; MIRA below |
| `mUXdysoxEP.md` (Feature Separation NC) | 6.75 | R1 | Stronger methodology with formal feature-space analysis; MIRA below |
| `9ROuKblmi7.md` (NECO OOD) | 5.75 | R1 | Clearer theory-practice connection; MIRA below |
| `eN0RyRVbSm.md` (Double Descent + OOD) | 6.5 | R1 | Formal theorems from RMT with comprehensive experiments; MIRA clearly below |
| `kbjJ9ZOakb.md` (Neuron invariance manifolds) | 8.0 | R1 | Strong paper on all axes; MIRA clearly below |
| `Trg9qb0d5U.md` (DNN accuracy without test data) | 3.67 | R2 | Same concept (model property without test data) but much weaker execution; MIRA above |
| `9H91juqfgb.md` (Safety Alignment) | 5.0 | R2 | Different domain; mixed reviews with similar ambition-execution gap |
| `zUtl4kJa0C.md` (Critical Learning Periods) | 4.75 | R2 | Novel concept with Fisher Information but limited experiments; comparable |
| `BRDqmYU8A0.md` (Model Developmental Safety) | 5.5 | R2 | Safety-centric framework, rejected; stronger formalization than MIRA |
| `todLTYB1I7.md` (Neuron Explanation Framework) | 5.0 | R2 | Unifies evaluation metrics under mathematical framework; similar concept-execution profile |
| `KCTHM2Ffh3.md` (Runtime Learning Machine) | 6.33 | R2 | Runtime safety with stronger formal backing; MIRA below |

**Bracket narrowing:**
- Round 1 bracket: 4.0–5.5. MIRA is clearly above the 3.0 reject-level papers (it has a genuine novel concept, broader experiments, and practical utility), but clearly below the 6.0+ papers (which have stronger theory-practice connections, formal statistics, and more rigorous validation).
- Round 2 refinement: Comparing to papers at 4.5–5.0, MIRA is most similar to the NC-OOD papers (4.5) in having a novel concept with a significant theory-validation gap, and to the Neuron Explanation Framework (5.0) in proposing an evaluation framework with execution shortcomings. MIRA's novel concept gives it a slight edge, but the compounding of multiple major validation issues (circularity, no statistics, capacity confound) keeps it from reaching 5.0+.

**Final assessment:** The paper introduces a genuinely novel and practically useful concept (monitorability), with consistent experimental results across three modalities. However, three interrelated major weaknesses — the definition-metric gap, partially circular validation, and absence of formal correlation statistics over small model counts confounded by capacity — collectively prevent the paper from convincingly demonstrating that MIRA measures what it claims to measure. The paper is above clear-reject territory (the concept is real and the initial evidence is directionally consistent) but below borderline-accept territory (the validation methodology has too many interrelated shortcomings for a metrics paper at a top venue). With the suggested revisions — particularly bridging the formal definition to the metric, deconfounding model capacity, and adding formal statistics — this could become a solid contribution.

**Score: 4.5** — Borderline reject. Novel concept with insufficient validation rigor.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>