Now I have all the information needed. Let me produce the final review.

## Summary

This paper proposes the Fast and Slow Effect (FSE) framework for evaluating whether LLM/VLM-generated concept annotations for XAI are "sufficient." FSE has an LLM/VLM progressively annotate concepts over 5 refinement stages, then measures classification accuracy from the accumulated concepts (slow mode) compared to direct visual classification (fast mode) using the Class Representation Index (CRI). Experiments on 5 datasets with 6 models show that slow mode underperforms fast mode by ~25% on fine-grained datasets but actually outperforms on coarse-grained datasets. A fusion experiment (image+text → ~90% accuracy vs. text-only → ~50%) is used to argue that downstream utility does not guarantee annotation quality.

## Strengths

1. **Well-motivated problem with cogent critique of existing evaluation.** The paper correctly identifies a genuine gap: automated concept annotation for XAI is proliferating without systematic validation. The critique of human evaluation (expensive, inconsistent) and the utility-as-proxy assumption (downstream accuracy can improve even with irrelevant/shortcut-laden concepts, §3) is well-reasoned and identifies a real community need.

2. **Semantically-related distractor design is methodologically sound.** The preliminary experiment (§5.3, Table 1) convincingly shows that random distractors yield low contradiction rates (14–20%) while semantically related distractors yield 34–45%, demonstrating that a challenging candidate set is necessary for meaningful evaluation.

3. **Fusion experiment provides a concrete demonstration against utility-as-proxy.** Table 4 (Fast ≈ 90%, Slow ≈ 50%, Fuse ≈ 90%) empirically shows that high end-to-end accuracy can coexist with poor isolated concepts. This is a genuine and useful empirical finding.

4. **Dataset-dependent findings are informative.** Table 3 shows that on coarse-grained datasets (CIFAR-100, Caltech-101), slow mode achieves CRI > 90% and outperforms fast mode — the opposite of fine-grained results. The paper discusses this nuance (§6), revealing where LLM/VLM concept generation actually works (coarse discrimination) and breaks down (fine-grained).

## Weaknesses

### Major

- **The fast vs. slow mode comparison is confounded by modality, making the central claim ambiguous.** Fast mode (t=0) classifies from images — the model's native, trained capability. Slow mode (t>0) classifies from only the textual concepts the model itself generated — a fundamentally different and harder task. The paper attributes the ~25% CRI gap to "annotation insufficiency" (abstract, §6), but the more parsimonious explanation is that text-based classification from self-generated descriptions is a harder task than image-based classification. The paper has no control to distinguish between "the concepts are insufficient" and "the model cannot use text for classification effectively." A control condition where human-written gold-standard concepts replace LLM-generated concepts in slow mode would resolve this: if human concepts also yield low CRI, the bottleneck is text-classification difficulty; if human concepts yield high CRI, the bottleneck is annotation quality. Without this control, the headline claim that "current annotation methods fail to provide sufficient semantic coverage" is not directly supported by the evidence.

### Minor

- **CRI operationalizes a narrow definition of "sufficiency" that does not match the paper's broader rhetorical claims.** Definition 3.1 defines sufficiency as "concepts alone enable accurate inference of the corresponding class," and CRI (Eq. 2) measures exactly this — classification accuracy from concepts. This is internally consistent. However, the abstract and introduction describe CRI as measuring whether concepts "sufficiently characterize their corresponding classes" and "capture sufficient semantic relationships" — language implying semantic content, faithfulness, or essential properties. CRI only measures whether concepts discriminate between classes (including semantically similar ones). A concept like "has a beak longer than 3cm" could achieve high CRI by being discriminative without capturing anything semantically meaningful about the class. The gap between the operationalization and the framing should be addressed.

- **No human-written concept control condition.** For an evaluation framework claiming to assess annotation sufficiency, the absence of a human baseline is a gap. Without showing that human-written concepts (which the community would agree are "sufficient") achieve high CRI, the metric's behavior relative to ground truth is unknown. A small-scale validation against human expert ratings would significantly strengthen the framework.

- **The "self-assessment" framing is misleading.** The paper states (line 95) that "Recent advances in LLM research have demonstrated promising self-assessment capabilities... enabling models to critically evaluate their own outputs." This sets an expectation that FSE uses self-assessment, but it does not — FSE uses accuracy-based CRI. The connection to self-assessment is never operationalized.

- **No ablation of the five-stage refinement process.** The paper uses a specific five-stage hierarchical process (Background → Superclass → Salient Features → Detailed Features → Auxiliary Features) without validating whether all five stages are necessary, whether fewer suffice, or whether the ordering matters. Since prior works use 1–3 stages, the choice of 5 needs empirical justification beyond "extending established methods."

### Trivial

None.

## Nice-to-Haves

- Validating CRI against human expert judgments of annotation sufficiency on a held-out subset.
- Statistical significance testing (confidence intervals for the CRI gaps in Tables 2–4).
- Analysis of which concept types (shape-based, color-based, habitat-based, etc.) correlate with high vs. low CRI, to make the framework more diagnostic.

## Removed Points

These points were raised by the input reviewer but are removed with justification:

1. **"Slow Mode Superiority hypothesis is ungrounded"** — REMOVED. The hypothesis is a reasonable assumption grounded in the idea that if concepts capture the relevant information, using them should be at least as good as raw visual processing. The paper draws an analogy to dual-process theory, not a formal claim about LLM cognition. Violation of the hypothesis is informative regardless of its psychological grounding.

2. **"Definition of sufficiency is circular with the metric"** — REMOVED as it substantially overlaps with the retained construct-validity point, and the paper is internally consistent in defining sufficiency as classifiability from concepts and measuring exactly that. The issue is about rhetorical overclaiming, not logical circularity.

3. **"Central conclusion reverses on general datasets, which is not well-explained"** — REMOVED. The paper explicitly acknowledges and discusses this reversal (§6, lines 223–227), offering a reasonable interpretation (coarse vs. fine-grained discrimination). This is an informative finding, not a flaw.

4. **"Fuse mode experiment does not support its claim"** — REMOVED. Whether the model uses the concepts or ignores them when the image is present does not affect the paper's core point: high end-to-end utility does not guarantee annotation quality. The experiment supports this claim regardless of mechanism.

5. **"Missing prompts / appendix"** — REMOVED per parser rules (appendices are stripped).

6. **"Construct validity failure: CRI measures classification accuracy not semantic sufficiency"** — MERGED into the retained Minor weakness about definitional scope, since the paper's Definition 3.1 is internally consistent with what CRI measures.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the modality confound as a structural issue but do not offer new explanations for the paper's findings that the paper itself does not already provide.

## Suggestions

1. **Add a human-written concept control condition** — the most impactful single addition. Replace LLM-generated concepts with human-written gold-standard concepts in the slow mode. If CRI for human concepts is also low, the problem is text-classification difficulty, not annotation insufficiency. If human concepts yield high CRI, the framework genuinely measures annotation quality.

2. **Reframe the contribution as measuring the "conceptualization gap"** — the discrepancy between implicit visual knowledge and explicit textual concepts — rather than making broad claims about "annotation sufficiency." This would better align the method with what it actually measures and resolve the construct-validity concern.

3. **Add an ablation of the five-stage refinement process** against simpler alternatives (e.g., 1-stage, 3-stage).

4. **Remove or retask the "self-assessment" framing** since FSE does not use self-assessment.

---

## Score and Decision

### Calibration Anchors

| Anchor | Avg Human Score | Decision | Round | Comparison to this paper |
|--------|----------------|----------|-------|------------------------|
| Automating High-Quality Concept Banks (KLUDshUx2V) | 3.40 | Reject | R1 | Topically similar (evaluating LLM concepts) but weaker — this paper has a more novel framework and cleaner experiments |
| Evaluating the Unseen (kTjEPEy96Q) | 3.00 | Reject | R1 | Similar framing (evaluation framework for CBMs) but had a conceptual fallacy; this paper is methodologically stronger |
| Zero-shot CBMs (5Aem9XFZ0t) | 4.83 | Reject | R2 | Methodologically comparable; both have interesting ideas but with confounds/limitations |
| Boosting CBMs (Q9Z0c1Rb5i) | 5.00 | Reject | R2 | Comparable quality — solid experiments but some concerns; this paper has a more fundamental confound |
| Faithful V-L Interpretation (rp0EdI8X4e) | 6.25 | Accept | R1 | Stronger paper — clear formulation, cleaner experimental design, no structural confound |
| Bootstrapping VIP (9bmTbVaA2A) | 5.75 | Accept | R1 | Clear contribution with clean experiments; this paper's central finding has a confound that paper lacks |
| Concept Bottleneck Gen Models (L9U5MJJleF) | 6.00 | Accept | R2 | Strong, well-executed paper; this paper is weaker in both experimental design and contribution clarity |

**Round 1 Bracket:** The paper sits between 3.5 and 5.5 based on topical similarity and overall quality. It is clearly stronger than the 3.0–3.4 papers (which had more fundamental methodological problems) but weaker than the accepted papers at 5.75+ (which have cleaner experimental designs and no structural confounds in their central findings).

**Narrowing:** After reading key anchors, the paper is most comparable to the 4.83–5.00 range. However, it has a structural confound (modality) that the papers in that range do not face to the same degree, placing it slightly below them.

**Final Score:** 4.5 — Borderline Reject. The paper tackles an important problem and has genuine contributions (utility-as-proxy critique, distractor design, informative dataset-dependent findings). However, the central experimental finding — the 25% CRI gap — is confounded by a modality difference (image vs. text) that the paper does not disentangle from annotation insufficiency. Without a control condition to isolate this confound, the headline claim that "current annotation methods fail to provide sufficient semantic coverage" is not adequately supported by the evidence as presented. The paper could be substantially strengthened by adding a human-written concept control and reframing the contribution around the "conceptualization gap."

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>