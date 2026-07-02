Here is the final consolidated review.

---

## Summary

ProteinVista is a 3D CNN that voxelizes full-atom protein structures (123M parameters) and is pretrained on ~500K AlphaFold2 structures. It is evaluated on enzyme-substrate prediction (ESP), transporter-substrate prediction (TSP), drug-target IC50 regression, and GO annotation. The paper reports that ProteinVista matches or exceeds ESM-2 on binding tasks while requiring substantially less compute (48 hrs on 4 A100s vs. ~7 days on 128 H100s for pretraining) and two orders of magnitude less data.

## Strengths

- **Compelling compute efficiency.** Pretraining on ~500K structures in 48 hours on 4 A100 GPUs vs. ESM-2<sub>650M</sub>'s ~7 days on 128 H100 GPUs using ~250M sequences is a striking result. Training throughput of 20s per 1K proteins vs. 426s for ESM-2<sub>650M</sub> on a single A100 is well-substantiated (Section 4.3, Figure 3).

- **Honest negative results and candid analysis.** The paper reports the GO annotation benchmark where ProteinVista underperforms ESM-2 (Fmax 0.57 vs. 0.62, Section 3.4), and stratifies results by pLDDT, sequence identity, and TM-score (Section 4.1), giving readers an accurate picture of where structure helps and where it does not.

- **Informative ablation studies.** Section 4.2 quantifies the impact of key design choices: number of inference views (-6.4% R² for 1 vs. 5 views), pretraining objective (~1% difference between contrastive and Rosetta), and voxel resolution (~1.1% for 1.5Å vs. 1.0Å). These allow readers to calibrate each component's importance.

- **Good analytical depth on complementarity.** The stratification by sequence identity, TM-score, and pLDDT (Section 4.1, Figure 2) provides nuanced insight into when 3D structure adds value versus when sequence is sufficient. The finding that the ensemble consistently outperforms either single model across similarity bins is informative.

## Weaknesses

### Fatal
None.

### Major

- **Confounded pretraining comparison against ESM-2.** ProteinVista is pretrained with a contrastive objective that aligns its embeddings to ESM-2's sequence embeddings (Section 2.3). The model whose performance is reported across all benchmarks had direct access to ESM-2's representational signal during pretraining. The paper provides a Rosetta-pretraining ablation on IC50 (Section 4.2) showing only ~1% R² difference — which partially mitigates the concern for that task. However, this ablation was **run only on IC50 regression**, not on the TSP/ESP classification benchmarks where the reported improvements over ESM-2 are much smaller (1.5 pp on TSP, essentially tied on ESP). The primary results in Tables 1 and 2 all use contrastively-pretrained weights, and the paper's headline claims ("outperforms sequence transformers") rest on those results. Without the ablation extended to TSP/ESP, readers cannot assess how much of the reported advantage comes from 3D structure versus from absorbing ESM-2's sequence-derived representations through the contrastive objective — especially on the tasks where the gap is narrowest.

- **No variance estimates on any main result; several reported improvements are very small.** Every metric in Tables 1 and 2 is a single point estimate with no standard deviation, confidence interval, or multi-run replication. This is especially problematic because several claimed improvements are marginal. On ESP (Table 1), ProteinVista alone scores 91.8% accuracy — identical to ESM-2<sub>150M</sub> (91.8%) and below ESM-2<sub>650M</sub> (91.9%), with slightly lower ROC-AUC (0.951 vs. 0.957/0.955). On TSP, the 1.5 pp gain over ESM-2<sub>650M</sub> is modest. Without variance estimates, and given the confound above, these could be null results. The IC50 regression gap (R² 0.69 vs. 0.61) is larger and more convincing, but still lacks variance estimates. Furthermore, the McNemar test (p < 10⁻¹³ for TSP, p < 10⁻¹⁷ for ESP) compares the **ensemble** against ESM-2<sub>650M</sub> alone, not ProteinVista alone — showing that combining two models outperforms one is not an informative result for proving the structure encoder's individual merit.

- **No comparison against the structure-aware baselines the paper critiques.** The Introduction argues that residue-level GNNs (GearNet, ESM-GearNet, DeepFRI) are limited because they "omit atom-level details" (Abstract) and that "most investigated protein graph encodings only slightly outperformed the sequence-only ESM-2 baseline" (Line 23). Yet the paper never benchmarks against GearNet, ESM-GearNet, or any other structure-aware GNN on the TSP/ESP/IC50 tasks. The evaluation compares ProteinVista only against ESM-2 (a sequence-only model) and against prior task-specific methods (SPOT, ProSmith-ESP). To substantiate the claim that atom-level 3D CNNs solve a problem that residue-level GNNs cannot, the paper must demonstrate improvement over those GNNs. This is a critical gap in the empirical evaluation.

### Minor

- **Rotation invariance relies on discrete 90° rotations and multi-view averaging at inference.** The augmentation strategy covers only 90° rotations around axes plus mirror reflections (Section 2.4). Generalization to arbitrary rotations is untested. More importantly, inference requires averaging 5 randomly augmented views; dropping to 1 view reduces R² by 6.4% (Section 4.2), confirming that the model has not learned true rotation invariance, only a test-time averaging strategy. This dependency means inference throughput is effectively ~5× the single-pass cost, which narrows the reported speed advantage: the 20s vs. 426s figure reports single-pass **training** throughput (one augmented view per protein), not inference with 5 views.

### Trivial
None.

## Nice-to-Haves
- Running the Rosetta-pretrained variant on all benchmarks (TSP, ESP) would cleanly disentangle the structure contribution from the ESM-2 distillation signal.
- Adding one or two structure-aware baselines (e.g., ESM-GearNet) on a shared benchmark would directly test the paper's central thesis about atom-level resolution mattering beyond residue-level graphs.
- Reporting results across 3 random seeds (mean ± std) would allow readers to assess statistical significance, especially for the close results on ESP.

## Removed Points
These points are flagged to be removed; treat them with caution.
- *Garbled equation in Section 2.1.* The reviewer noted the density-spreading formula appears malformed. Per guidelines, this is treated as a parser artifact, not an author error.
- *Hyperparameter underspecification.* The reviewer noted missing learning rate ranges, batch sizes. Per guidelines, undisclosed hyperparameter details of this kind are considered nitpicks about reproducibility.
- *Dataset sizes/splits only in appendix.* The reviewer noted that dataset details are deferred to Table S3 (stripped appendix). Per guidelines, missing appendix content is not a valid weakness.
- *"First" claim difficult to verify.* The reviewer questioned whether ProteinVista is "the first compute-efficient full-atom 3D CNN." Per guidelines, missing related works cannot be cited as a weakness.
- *The paper's storage footprint criticism (75GB vs 3MB).* This was noted by the reviewer as a trade-off, not a weakness; it is correctly presented by the paper as an acknowledged limitation.

## Novel Insights
None beyond the paper's own contributions. The reviews identify the key confounding issue (contrastive pretraining aligning with ESM-2) and the missing structure-aware baselines, but these are methodological gaps rather than novel observations about the method or problem.

## Suggestions
1. Run the Rosetta-pretrained variant on TSP and ESP to decouple the 3D structure signal from the ESM-2 distillation signal.
2. Add at least one structure-aware GNN baseline (e.g., ESM-GearNet) on IC50 regression, where atom-level detail should matter most, to empirically validate the paper's core critique of residue-level methods.
3. Report all main results across 3 random seeds with mean and standard deviation.
4. Clarify in Section 4.3 that the reported 20s/1K proteins figure is single-pass training throughput, and provide separate inference throughput numbers (with 5 views vs. 1 view).
5. Soften the framing of the ESP results, where ProteinVista alone is essentially tied with ESM-2, to avoid overclaiming.

## Score and Decision
The paper presents a promising and compute-efficient 3D CNN for protein structure encoding, with thoughtful analysis and honest reporting of limitations. However, the core comparative evaluation has three significant gaps: (1) the contrastive pretraining confound between structure and sequence-model signal is not fully disentangled on all benchmarks; (2) no variance estimates are provided, making it impossible to assess whether the small improvements on TSP/ESP are meaningful; (3) the paper critiques structure-aware GNNs but never benchmarks against them, leaving its central thesis empirically ungrounded. These weaknesses collectively prevent the paper's claims from being convincingly established in its current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>