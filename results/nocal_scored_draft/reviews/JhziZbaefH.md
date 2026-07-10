## Summary

This paper proposes OML, a brain-inspired hierarchical modular network for online multimodal learning that incorporates precise reference extraction, conflict detection, and human-in-the-loop interaction. The architecture features distinct neuron types (FNs, UANs with OIAM/ODAM variants, MANs) with explicit ascending/descending/lateral pathways, plus a reference extraction mechanism that identifies stable feature dimensions via coefficient of variation. Experiments on small-scale fruit and home-object datasets with visual, auditory, and taste modalities show consistent improvements over online baselines.

## Strengths

- **The paper identifies and formalizes an underexplored problem configuration** — online multimodal learning with precise reference extraction, conflict detection, and human-in-the-loop interaction — that goes beyond both static multimodal learning and standard continual learning. The motivation (Section 1, Fig. 1) is clear and compelling.

- **The reference extraction mechanism (Section 3.4), which identifies referring dimensions via coefficient of variation across varying visual inputs, is a well-motivated and elegantly formalized contribution.** The running example in Fig. 3(a) concretely illustrates the idea. This is the most distinctive and novel component of the work.

- **The hierarchical modular architecture with distinct neuron types (FNs, UANs in OIAM/ODAM variants, MANs) and explicit ascending/descending/lateral pathways is structurally novel** and goes beyond standard engineering adaptations of existing methods.

- **OML achieves consistent and non-trivial improvements over online baselines in open-environment settings** across all three experiments (Tables 1–3), with margins of 3–5 points over the best online competitor, and the advantage is particularly clear in the modality extension experiment (Table 3).

## Weaknesses

### Fatal
None

### Major

- **Evaluation metric undefined.** The paper reports "accuracy" in Tables 1–3 but never defines what constitutes a correct retrieval (top-1? top-5? precision@k?), over what candidate set, or how retrieval is scored. The description ("we use one channel input to get outputs from other channels") describes the task but not the metric. Without this definition, the numerical results are uninterpretable. This is the single most critical gap because the entire experimental contribution rests on these numbers.

- **No variance or statistical significance estimates.** All results in all three tables are single point estimates with no standard deviations, confidence intervals, or significance tests. Given that online learning involves stochastic data ordering and random initialization, the reader cannot assess whether reported advantages (e.g., 89.8 vs. 86.2, a 3.6-point gap) are meaningful or within run-to-run noise.

- **Conflict detection claim is unsupported.** The paper asserts that "OML is able to detect all conflicts and raise appropriate questions" based on one sentence in Section 4 describing a single condition (10% mismatched pairs). There is no description of trial count, no precision/recall/F1 analysis, no ablation of the conflict-checking mechanism, and no baseline comparison. A claim of 100% detection accuracy is extraordinary and the evidence provided is anecdotal.

- **Human-in-the-loop is not actually evaluated.** The experiments simulate user responses by setting unanswered questions to "yes," reducing the interactive component to a constant positive signal. The paper's title, abstract, and introduction frame human-in-the-loop interaction as a core contribution, yet the experiments only test the network's learning capability, not its ability to pose appropriate questions or calibrate its confidence.

### Minor

- **The claim that OML "retains the characteristics outlined in Srivastava & Salakhutdinov (2014)"** (classification, retrieval, and filling in missing modalities) is only partially supported — the experiments evaluate retrieval but not classification or missing-modality imputation.

- **Citation error (Lin & Hu, 2024).** The related work describes this as "a multimodal mixup network," but the reference list shows a title about "repetitive motor learning" and "dendritic spines" — a clear mismatch between description and cited source. This needs correction.

- **No ablation studies.** The architecture has many components (ascending/descending/lateral pathways, frequency encoding, reference extraction, conflict checking) but none are ablated. The reader cannot tell which components drive the observed performance.

### Trivial
None

## Nice-to-Haves
- Sensitivity analysis for key thresholds ($\theta$, $\vartheta$, $r$) would increase confidence in robustness.
- A dedicated evaluation of the conflict detection capability (precision, recall, F1) with controlled test sets.
- Discussion of limitations (toy-scale datasets, simulated user feedback, hand-crafted features).

## Removed Points
- **Asymmetric scoring criteria in Tables 2 and 3:** The paper is transparent that baselines receive more lenient scoring (returning wrong attributes still counted as correct). This asymmetry favors the baselines, not OML, making it a conservative comparison. Removed per Hard Rule.
- **Method under-specification claims (Eq. 1 frequency encoding, Eq. 6 Fourier transform):** The paper specifies these mechanisms in the text; the motivation could be clearer but the mechanisms are described. These are design-justification requests bordering on scope creep.
- **Experimental scope is narrow / datasets are small:** The paper follows established datasets and protocols from prior work in this sub-area (Xing et al. 2019, 2021). Criticizing scale without acknowledging the niche problem framing is not a fair weakness.
- **Lateral connection threshold ambiguity:** A very minor specification issue that does not threaten core claims.
- **Generic or category-driven concerns:** Removed as they lacked concrete anchors in the paper text.

## Novel Insights
None beyond the paper's own contributions. The strongest non-obvious point — that reference extraction via coefficient-of-variance on stable dimensions maps naturally to cognitive invariant-attribute isolation — is already well-articulated in the paper itself (Section 3.4).

## Suggestions

1. **Define the evaluation metric explicitly** in the main paper (top-1 retrieval accuracy, precision@k, or whatever is used) and specify the candidate set over which retrieval is evaluated.
2. **Run all experiments multiple times** with different random seeds and report means ± standard deviations.
3. **Design a proper evaluation of conflict detection** — controlled test sets with known mismatches at varying rates, reporting precision, recall, and F1.
4. **Either evaluate with real human interaction** or transparently acknowledge that the human-in-the-loop aspect is not experimentally validated and is deferred to future work.
5. **Correct the Lin & Hu (2024) citation** mismatch.
6. **Add ablation studies** that isolate reference extraction, conflict checking, and lateral connections.

## Score and Decision

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>