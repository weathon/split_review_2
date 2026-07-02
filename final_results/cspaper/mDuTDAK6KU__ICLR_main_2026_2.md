---
job_id: 9b414620-c8ef-465f-beaa-8f7a4ce111ad
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: mDuTDAK6KU.pdf
paper: KOALA: KL–L0 Adversarial Detector via Label Agreement
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope, it studies adversarial robustness and detection for neural representations, with a prototype-based detector, theoretical claims, and empirical evaluation on vision models.

## Minimum Quality
Pass ✅. The paper contains the necessary scientific components, including abstract, motivation, related work, methodology, experiments, quantitative results, and analysis; while I have serious concerns about the correctness and support of the central claims, these rise to the level of a substantive review rather than a desk reject.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find any hidden prompts or obvious attempts to manipulate automated reviewing in the provided paper text or figures.

# Expected Review Outcome:
## Summary
This paper proposes KOALA, an adversarial detector built on disagreement between two nearest-prototype classifiers defined by KL divergence and a thresholded \(L_0\)-style metric in a normalized embedding space. The method replaces the original classifier head with a prototype-based detector head, fine-tunes the encoder on clean data using a combined KL and smoothed \(L_0\) objective, and flags an input as adversarial when the two metric-induced labels disagree. The paper also presents a theorem claiming guaranteed detection under stated assumptions and reports experiments on ResNet-18/CIFAR-10 and CLIP/Tiny-ImageNet.

## Strengths
The paper has a clear, simple high-level idea. Using disagreement between two complementary prototype metrics as a detection signal is easy to understand and, in implementation terms, relatively lightweight compared with adversarial training or detector-specific auxiliary networks.

I appreciated that the method is stated in a concrete form in **Equations (1)-(6)**, rather than only verbally. The training objective in **Section 3.3** is reasonably explicit about the use of positive/negative image-prototype pairs and the smoothed surrogate for the non-differentiable \(L_0\) score.

The figures help explain the intended intuition. In particular, **Figure 1** communicates the central motivation well: the paper argues that dense low-amplitude shifts and sparse high-impact shifts are better exposed by different metrics, and that the overlap structure of their respective “stability bands” drives detection through disagreement. Likewise, **Figure 2** gives a useful end-to-end picture of how prototypes, the two metric heads, and the attack detection logic interact during training and inference.

The empirical section does try to connect theory and practice, which is better than simply presenting benchmark numbers. **Table 1** is especially important in that regard, because it explicitly partitions data into “Theorem 1 compliant” and “non-compliant” subsets and shows perfect reported recall/precision on the compliant subset. Even though I have concerns about how this subset is defined and used, I do think the authors are at least attempting to make the theorem operational and testable.

On ResNet/CIFAR-10, the proposed KL+\(L_0\) pairing looks materially stronger than several alternative metric combinations in the reported detector metrics. In **Table 2**, for \(\ell_\infty^{2/255}\), KL+\(L_0\) reaches accuracy/precision/recall/F1 of \(0.88/0.94/0.81/0.87\), which is clearly above the other pairings shown for that setup. This supports the narrower claim that the specific metric combination can be useful empirically in at least one regime.

## Weaknesses
I have substantial concerns, and several of them strike at the core claims of the paper rather than being peripheral issues.

1. **The “formal proof of correctness” claim is overstated relative to what is actually established in the main paper.**  
   The abstract and **Section 3.2** repeatedly frame the result as a proof of correctness with “mild and practical assumptions.” But the statement of **Theorem 1** on **Page 5** is vague at exactly the point where the guarantee matters most: it requires the existence of a coordinate gap larger than some threshold \(\Gamma_i(\epsilon)\), but \(\Gamma_i(\epsilon)\) is not defined in the theorem statement itself. In the main paper, the reader never gets a clean, usable theorem of the form “if condition X holds, then KOALA detects all attacks in class Y.” Instead, the operative condition is deferred into a very long appendix derivation with many auxiliary quantities that themselves depend on attack- and sample-specific terms such as \(v_i\), \(\Delta KL(\mathbf p^*)\), \(\|\delta\|_1\), and \(\mu(\cdot,\cdot)\). That is not a minor presentational issue, because the practical meaning of the theorem depends entirely on whether these conditions are checkable before the attack or are only certifiable post hoc.

2. **Several mathematical steps in the proof chain are difficult to accept as correct or even well-posed.**  
   The proof machinery in Appendix B contains multiple places where notation, signs, and dimensions appear inconsistent. A concrete example is the transition around **Equation (14)** on **Page 15**, where the paper concludes
   \[
   \Delta KL(\mathbf p^*) < (\hat{\mathbf c} - \mathbf c^*) \frac{\mathbf \delta^T}{\mathbf p^*}.
   \]
   This mixes vector and scalar notation in a way that is not properly defined. Earlier, in **Equation (11)**, the Taylor expansion is written for \(\log(\hat{\mathbf p})\), but the expression alternates between vector-valued and quadratic-form notation without carefully keeping track of whether the result is coordinatewise, scalarized, or summed. Similar issues recur in the proof of Proposition 4, where sets are indexed over \(\{1,\dots,m\}\) even though the ambient feature dimension is \(d\); for example, \(\mathbb S^{\text{unchange}} = \{ i \in \{1,\dots,m\} \mid |\delta_i^{\max}| \ge \min_i\}\) in **Page 18** should apparently be over feature coordinates, not classes. These are not cosmetic problems. They make it hard to verify whether the key inequalities actually hold.

3. **The KL divergence formulation assumes probability-simplex embeddings, which is an unusually strong modeling choice that is not convincingly justified.**  
   In **Assumption A1** on **Page 5**, all feature embeddings and class prototypes are assumed to be strictly positive and sum to 1, so that KL divergence in **Equation (1)** is well-defined. This means the embedding space is not a generic penultimate feature space, but effectively a simplex-valued representation produced by a softmax-like normalization. That is a major architectural and geometric restriction, yet the paper repeatedly markets KOALA as “plug-and-play” and requiring “no architectural changes.” Replacing a standard classifier head by a normalized simplex embedding plus prototype matching is already a nontrivial intervention. More importantly, for CLIP the image and text embeddings are normally cosine-oriented latent vectors, not positive normalized probability vectors. The paper does not explain in sufficient detail how CLIP features are transformed to satisfy **A1**, how this affects representation geometry, or whether the theorem would survive without this assumption.

4. **The attack model used in theory and the attack model used in experiments are misaligned.**  
   The theoretical development in **Section 3.2** is built on a bounded perturbation \(\delta\) in feature space, see **Assumption A2**, with the justification that this “follows from the Lipschitz continuity of the backbone encoder.” But the experiments in **Section 4.1** attack the *input image* under an \(\ell_\infty\) budget. The mapping from input-space \(\ell_\infty\) perturbations to feature-space \(\ell_2\) or coordinatewise bounds is never quantified. Invoking Lipschitz continuity is not enough unless a specific Lipschitz constant is known or bounded for the actual model, and nothing like that is provided. This matters because the theorem is then disconnected from the reported empirical setting. In other words, the proof is about one threat model, while the experiments are about another.

5. **Assumption A3 is not “mild” in the way the paper claims, and it is particularly problematic near small coordinates.**  
   **Assumption A3** requires \(|\delta_i| \le \frac{3}{2}|p_i^*|\) for every coordinate. Since **A1** enforces positive simplex coordinates, many coordinates can be extremely small. Then A3 can become extremely restrictive, not mild. This assumption is also doing real work in the Taylor remainder argument around **Equations (12)-(14)**, so it is not an innocuous technicality. The paper should either show empirically how often A3 is satisfied on real attacked examples, or stop presenting the result as broadly practical.

6. **The core incompatibility claim depends on a threshold \(\tau\) that seems to be chosen to make the argument go through, rather than fixed as part of the method.**  
   In the proof sketch on **Page 5**, item (iii) states: “for any given adversarial perturbation, we can always find a threshold \(\tau\) for the \(L_0\) metric that forces a trade-off.” This is a serious issue. In the actual method, \(\tau\) is a detector hyperparameter fixed before test time, not something selected adversary-by-adversary after seeing \(\delta\). A theorem that asserts existence of a favorable \(\tau\) for each perturbation does not establish correctness of a single deployed detector with one fixed \(\tau\). This gap undermines the claimed “proof of correctness” for the algorithm as instantiated in practice.

7. **The evaluation protocol and metrics definition are nonstandard enough that the reported numbers are hard to interpret.**  
   In **Section 4.2**, the paper defines
   \[
   \text{TP} := [a=1] \wedge [(\hat a,\hat y)=(1,\bot)\vee (\hat a,\hat y)=(0,y^*)].
   \]
   So an attacked input that is *not detected* but still correctly classified counts as a true positive. This is unusual for an attack detector, where TP usually means “attacked and flagged.” The authors may be aiming to measure attack handling rather than pure detection, but then the terminology and interpretation of precision/recall become muddled. This matters directly for **Table 1** and **Table 2**, because the headline precision/recall numbers are not straightforward detector precision/recall in the usual sense.

8. **The “Theorem-compliant subset” analysis in Table 1 risks circularity and is not sufficiently operationalized.**  
   **Table 1** reports perfect metrics on theorem-compliant samples, but the paper does not specify in the main text how compliance is checked in a way that is independent of the attack outcome and practical for deployment. Given the theorem’s dependence on quantities like coordinate gaps and derived thresholds, this subset could simply be selecting easy cases where the detector works by construction. The raw counts in **Table 5** make the issue more visible. For example, on CLIP/Tiny-ImageNet only \(510\) or \(556\) attacked samples are deemed compliant, versus roughly \(4.4\)k non-compliant, so the perfect results hold on a small minority of cases. That does not invalidate the experiment, but it sharply limits the practical significance of the guarantee.

9. **The empirical comparisons are incomplete for a detection paper.**  
   The paper mainly compares metric combinations within its own framework, see **Table 2**, and compares fine-tuning objectives within that same family, see **Tables 3-4**. What is largely missing is comparison against actual adversarial detection baselines, especially modern reactive detectors or simple uncertainty/prototype/OOD-style detectors that operate without adversarial training. The related work section cites several detector families, but the experimental section does not benchmark against them. As a result, it is impossible to tell whether KOALA is actually competitive as a detector, or merely preferable to other internal metric pairings.

10. **The CLIP results weaken the paper’s central narrative more than the authors acknowledge.**  
    In **Table 2**, KL+\(L_0\) is *not* the best metric combination on CLIP/Tiny-ImageNet; KL+\(L_0\)+Cosine performs better on all four reported detector metrics. The authors explain this away by arguing that the triple-metric model “breaks the underlying classification” and achieves disagreement by making all metrics guess randomly. But that explanation is post hoc and actually points to a deeper problem: disagreement alone is not a robust semantic indicator of adversariality. It can also arise from a poorly behaved representation. This substantially weakens the conceptual premise that KL and \(L_0\) are uniquely complementary in a principled way.

11. **The robustness claims in Section 4.4 are confusing, and some text appears inconsistent with the tables.**  
    On **Page 9**, the paragraph introducing **Table 4** states that “The KL+\(L_0\) objective demonstrates superior adversarial accuracy,” but the table itself shows otherwise for CLIP. For PGD, the KL-only objective is best; for AutoAttack and CW, the \(L_0\)-only objective is best. KL+\(L_0\) is actually much worse than those single-metric alternatives on CLIP. This is more than a typo, because it changes the substantive conclusion one would draw from the experiment.

12. **The method is less architecture-agnostic and less semantics-free than advertised.**  
    The “semantics-free” part is partly true in the sense of not using label descriptions for ResNet, but for CLIP the prototypes are explicitly derived from text prompts, see **Section 4.1** on **Page 7**. That means semantics are entering through the text encoder. Likewise, replacing the model’s original head by a nearest-prototype disagreement detector is not simply attaching a black-box module to an arbitrary classifier. The positioning in the abstract and introduction oversells how universally drop-in the method is.

13. **The exposition is often too loose where precision is needed.**  
    There are repeated places where definitions are under-specified or terminology shifts. For example, **Equation (2)** is called an “\(L_0\) distance,” but it is really a thresholded count based on a sample-adaptive mean offset, not the standard \(L_0\) norm of a difference vector. In **Figure 2**, the schematic is helpful, but it visually suggests a clean train/infer pipeline without surfacing the strong normalization assumptions, prototype construction details, or the difference between the hard inference metric and the smoothed training surrogate. Those are exactly the details on which the theorem-method connection hinges.

14. **Some of the headline empirical gains are modest once one moves beyond the best-case setting.**  
    On CLIP/Tiny-ImageNet, the reported precision of KOALA in the abstract is only \(0.66\), and in **Table 2** the overall gains over alternative combinations are small or negative depending on the configuration. The method may still be useful, but the experimental evidence does not support the broad level of confidence expressed in the abstract and introduction.

## Questions
1. The most important point for rebuttal is the theorem claim. Can the authors provide a much cleaner, self-contained statement of **Theorem 1** in the main paper with an explicit definition of \(\Gamma_i(\epsilon)\), all quantities computable from pre-attack information, and a clear distinction between “there exists \(\tau\)” and “for the fixed deployed \(\tau\), detection is guaranteed”? This would materially affect my assessment.

2. How exactly are the embeddings constrained to satisfy **Assumption A1** for both ResNet and CLIP? Please specify the exact normalization layer or parameterization used before prototype comparison, and clarify whether the backbone architecture is modified to enforce positivity and unit sum. If this requires inserting a softmax-like layer, the “no architectural changes” claim should be softened.

3. Please clarify the bridge from input-space \(\ell_\infty\) attacks to feature-space perturbation assumptions. Do you estimate or bound the relevant Lipschitz constants in practice? Without that, why should the theorem be viewed as evidence for the actual experimental threat model?

4. For the proof in Appendix B, can the authors address the apparent indexing inconsistency between class count \(m\) and feature dimension \(d\), especially in **Proposition 4** and the definition of \(\mathbb S^{\text{unchange}}, \mathbb S^{\text{change}}, \mathbb S^{\text{remain}}\)**? If this is a notational shortcut, it should be fixed; if not, it may indicate a substantive issue.

5. Please justify the detector metrics in **Section 4.2** more carefully. Why should an attacked sample that is not flagged but remains correctly classified count as a true positive for “detection”? I would like to see standard detector operating characteristics as well, such as attacked-vs-clean detection rates where TP means attacked and flagged.

6. How is theorem compliance determined operationally for **Table 1**? Is the compliant/non-compliant partition determined using only clean sample and prototype information, or does it depend on attacked outcomes or post hoc quantities? A precise algorithm here is essential, because otherwise the “theory validated by perfect recall” claim is difficult to interpret.

7. Can the authors compare KOALA against at least a small set of external adversarial detectors, not just internal metric combinations? Even a limited comparison against uncertainty-based, Mahalanobis/prototype-based, or transformation-consistency detectors would make the empirical contribution much easier to evaluate.

8. For the CLIP setting, the tables seem to contradict the narrative around KL+\(L_0\). Can the authors reconcile the text on **Page 9** with **Table 4**, and explain whether the proposed metric pairing should really be considered the recommended default outside the ResNet/CIFAR-10 regime?

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
The paper studies adversarial robustness and attack detection in standard vision benchmarks and does not raise a distinct ethics concern beyond ordinary dual-use considerations already typical for this area.

## Soundness Rating
2: fair. The paper has a concrete method and nontrivial experiments, but the central theoretical claims are not adequately supported in their current form, and there are meaningful mismatches between assumptions, proofs, and empirical evaluation.

## Presentation Rating
2: fair. The high-level idea and figures are understandable, but the mathematical exposition, theorem statement, and some experiment narratives are not precise enough for a paper that leans heavily on a claimed correctness guarantee.

## Contribution Rating
2: fair. The disagreement-based detector idea is interesting and potentially useful, but the lack of convincing theoretical grounding, missing external baselines, and mixed empirical evidence reduce the overall contribution.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted. The paper has an appealing core idea and some promising results, especially on ResNet/CIFAR-10, but the current version overclaims on theory and under-supports competitiveness as an adversarial detector. A substantially revised version with a tighter theorem, corrected derivations, clearer evaluation protocol, and stronger baselines could become much more convincing.

## Reviewer Confidence
4: confident. I am confident in the main concerns, especially the theorem-method mismatch, proof issues, and the interpretation of the empirical results, although some appendix derivations are sufficiently dense that a full line-by-line formal verification would require more time.