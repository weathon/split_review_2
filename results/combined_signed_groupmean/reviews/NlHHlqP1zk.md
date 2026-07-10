## Summary

This paper proposes the Fast and Slow Effect (FSE) framework, a fully autonomous evaluation pipeline for assessing whether LLM/VLM-generated concept annotations for XAI are *semantically sufficient* to discriminate target classes from semantically similar alternatives. The framework has two components: (1) a coarse-to-fine multi-step concept annotation process transitioning from "fast mode" (visual classification without concepts) to "slow mode" (concept-only classification after progressive concept gathering), and (2) the Class Representation Index (CRI), a metric measuring classification accuracy when the model reasons only from its own accumulated concepts. Experiments across six LLMs and five datasets show that slow-mode CRI is ~25% lower than fast-mode CRI on fine-grained datasets, and that fused (image+concept) prediction achieves ~90% CRI while concept-only prediction reaches only ~50% — demonstrating that high downstream accuracy does not guarantee annotation sufficiency.

## Strengths

- **Critique of the "utility-as-proxy" assumption is well-supported.** Table 4 is the paper's strongest piece of evidence: fused (image+concept) prediction achieves ~90% CRI while concept-only (slow mode) achieves ~50% CRI under identical conditions. This demonstrates convincingly that downstream accuracy alone is not a reliable signal of annotation quality — a valuable warning to the field. [impact=+10.00]

- **Broad model and dataset coverage.** Evaluating six LLMs (GPT-4o, GPT-4o-mini, Llama-3.2-vision-90b/11b, QwenVL2-72b/7b) across five datasets spanning both fine-grained (CUB-200, Cars-196, Flowers-102) and general categories (CIFAR-100, Caltech-101) strengthens the descriptive generality of the empirical observations. The finding that the gap reverses on general datasets (slow mode > fast mode) adds nuance. [impact=+9.98]

- **The paper identifies a genuine underexplored problem.** The observation that LLMs can generate plausible concepts and make correct visual classifications yet fail to discriminate between semantically similar classes when reasoning *only from their own concepts* is a real and important issue for concept-based XAI. The motivating example in Figure 1 is effective and well-chosen. [impact=+0.43]

## Weaknesses

### Major

- **The core evaluation confounds concept quality with the model's text-based reasoning ability.** Definition 3.1 defines sufficiency as concepts that "enable accurate inference," but the paper operationalizes this by having the **same model** that generates the concepts also perform reasoning from them. When the LLM fails at concept-only classification, the failure could equally stem from a limitation in the model's text-based reasoning ability — the model may struggle to faithfully reason from text descriptions of fine-grained visual distinctions even if those descriptions are perfectly sufficient (as a human domain expert would find them). This is not speculation: the fast mode achieves ~93% CRI on fine-grained datasets (Table 4, GPT-4o), meaning the *visual* classification is nearly perfect, and the problem only appears when switching to text-based reasoning. The finding that slow mode works well on general datasets (Table 3, >90% CRI) is partially mitigating — if the problem were purely about reasoning ability, performance would be poor across all datasets — but the central claim that "current annotation methods fail to provide sufficient semantic coverage" is stated more strongly than the evidence supports. The finding is better characterized as: VLMs show a significant gap between visual recognition accuracy and text-based reasoning accuracy from their own self-generated concepts, particularly for fine-grained discrimination.

### Minor

- **CRI formula typo in Equation (2).** The paper defines $\mathcal{D}_{\text{test}} = \{(c_i^t, y_i^t) \mid t = 1, \dots, T; i = 1, \dots, l\}$ where $l$ is the number of test instances. CRI at step $t$ should be $(1/l)\sum_{i=1}^l \mathbb{1}[y_i^t = y_i]$, but Equation (2) writes $(1/t)\sum_{i=1}^t$ — the upper bound and divisor are $t$ (the annotation step, 0–5) instead of $l$ (the number of test instances, presumably much larger). The reported CRI values in Tables 2–4 are numerically sensible, suggesting the implementation uses the correct formula, but this notational error should be fixed.

- **Distractor selection strategy is validated by the phenomenon it is designed to produce.** The preliminary experiment (Section 5.3) selects "Semantically Related" distractors because they produce higher contradiction rates (34–45% vs. 14–20%), where a "contradiction" is defined as the model's concept-based prediction differing from its initial visual prediction. This is the same type of gap that the CRI measures, creating a mild selection bias: the evaluation setup is validated by its tendency to reproduce the paper's main finding. An external reference (e.g., human-judged semantic similarity or an independent embedding space) would be a cleaner validation.

- **The Semantic Similarity Dictionary (SSD) is a noisy proxy.** The SSD is built from a pretrained ResNet-18's confusion patterns — the classes the ResNet-18 most frequently confuses. This captures the model's inductive biases, not necessarily human-judged semantic similarity. Since the LLM is then asked to discriminate among classes selected because a *different* model confused them, the test may partly measure how well the LLM replicates ResNet-18's confusion patterns rather than genuine concept-class mapping quality.

- **No ablation for the five-stage prompting chain.** The concept chain (Background → Superclass → Salient Features → Detailed Features → Auxiliary Features) extends prior work from 1–3 stages to 5, but no analysis shows whether all five stages are individually useful, whether the ordering matters, or how many concepts are generated at each stage on average.

### Trivial

None.

## Nice-to-Haves

- **Human-authored concept baseline.** Feeding human-written gold-standard concept descriptions through the same LLM evaluator would help disentangle the confound: if human concepts achieve significantly higher CRI, the claim about annotation insufficiency would be substantially strengthened; if similarly low, the finding would need reframing as a limitation of text-based reasoning for fine-grained discrimination.
- **Cross-model evaluation.** Having Model A generate concepts and Model B evaluate them (e.g., GPT-4o concepts evaluated by Llama) would reduce the self-evaluation confound.
- **Sample size reporting.** The paper reports "100 images" for the contradiction test (Table 1) but does not state how many images are used for the main CRI experiments (Tables 2–4), which would aid interpretability.

## Removed Points

These points were raised in the input review but are removed with justification:

- **"Slow/fast mode compares different tasks, not different annotation qualities"** — This is the same issue as the Major confound weakness above, not a separate structural flaw; merged.
- **"Fused mode's high CRI could simply mean the visual channel dominates prediction"** — This is the paper's *own argument* in Section 6 ("Utility-as-Proxy ≠ Annotation Sufficiency"). The paper uses this result precisely to show that utility does not imply sufficiency, so it is not a weakness.
- **"Missing acknowledgment of self-evaluation limitation in Section 8"** — Subsumed by the Major weakness; Section 8 should include this discussion but the criticism adds no new substance beyond what the Major weakness already states.
- Various section-by-section commentary that does not identify concrete problems with the paper's claims or evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the CRI formula in Equation (2) — replace both instances of $t$ in the divisor and summation upper bound with $l$ (the number of test instances).
2. Reframe the paper's central claim: the evidence more strongly supports "a gap between visual recognition and text-based concept reasoning" than "annotation methods fail to provide sufficient semantic coverage." The current claim is defensible under the paper's operational definition but the broader interpretation needs tempering.
3. Add a paragraph to Section 8 explicitly discussing the self-evaluation confound and its implications for interpreting the results.
4. Add a human-authored concept baseline or a cross-model evaluation experiment to strengthen the claim that the insufficiency arises from annotation quality rather than reasoning limitations.

## Score and Decision

**Calibration**: Round 1 bracketed this paper at 4.0–5.0. Round 2 narrowed against the closest anchor, Zero-shot CBMs (4.83), which has similar strength magnitude but more severe documented weaknesses (-10.00 novelty concerns vs. our -6.86 confound). The "Automating Concept Banks" anchor (3.40) and "Evaluating the Unseen" anchor (3.00) are topically similar but have weaker experimental evidence and more fundamental design issues, placing our paper above them.

**Final score**: 4.5 — The paper identifies a genuine problem and presents a clean framework with strong empirical breadth, but the central claim about annotation insufficiency is weakened by a design that conflates concept quality with text-based reasoning ability. The finding itself (a gap between visual and text-based performance exists) is solid, but the causal attribution to annotation quality specifically is not fully supported without additional controls (human baselines or cross-model evaluation).

**Decision**: Reject

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>