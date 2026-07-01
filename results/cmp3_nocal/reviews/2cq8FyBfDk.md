Now I'll produce the final consolidated review.

## Summary

This paper introduces ProteinVista, a 3D CNN that voxelizes full-atom protein structures into density grids and is pre-trained (via contrastive distillation from ESM-2 embeddings) on ~500K AlphaFold2 structures — two orders of magnitude less data than large protein language models. At 123M parameters, it matches or outperforms ESM-2 variants on two of three protein–ligand interaction benchmarks (transporter-substrate classification and IC50 regression) while requiring dramatically less compute (48 hours on 4 A100s vs. 7 days on 128 H100s for ESM-2₆₅₀M). An ensemble with ESM-2 yields further gains and can exceed dedicated state-of-the-art substrate predictors.

## Strengths

1. **Compute efficiency is genuinely striking and well-documented.** Pre-training on 4 A100 GPUs for 48 hours (versus 128 H100 GPUs for ~7 days for ESM-2₆₅₀M) and inference throughput of 20s vs. 426s per 1000 proteins on an A100 (Section 4.3, Figure 3) make this practically useful even before considering accuracy. The storage trade-off is also transparently discussed.

2. **Contrastive distillation from ESM-2 to a 3D CNN is a principled and effective design choice.** The symmetric InfoNCE loss (Section 2.3) aligning structure and sequence embeddings transfers sequence-level information into the structure encoder while letting the 3D CNN retain geometric details that sequence models miss. The ablation showing that even Rosetta-only pretraining (no distillation) yields R²=0.68 on IC50 — above ESM-2's 0.61 — strengthens the claim that the 3D structure signal itself, not just the distillation, drives the improvement.

3. **Honest reporting of negative results.** Section 3.4 transparently shows ProteinVista underperforms ESM-2 on GO term prediction (Fmax 0.57 vs. 0.62), and Section 4.1 stratifies performance by structural similarity and pLDDT to show where the model fails and where it works. This candor increases confidence in the positive results.

4. **Adaptive boxing for varying protein sizes** (Section 2.1) is a practical contribution that makes 3D CNNs feasible at scale for proteins of widely differing sizes. The voxel resolution analysis (Section 4.2) provides useful guidance for practitioners.

## Weaknesses

### Fatal
None.

### Major

1. **"Outperforms sequence transformers on three benchmarks" (Abstract, line 9) is overstated for the ESP task.** Table 1 shows that on enzyme-substrate prediction (ESP), ProteinVista achieves 91.8% accuracy — identical to ESM-2₁₅₀M (91.8%) and marginally below ESM-2₆₅₀M (91.9%). The ROC-AUC is 0.951 vs. 0.957 (ESM-2₁₅₀M) and 0.955 (ESM-2₆₅₀M). This is a tie or slight underperformance, not an outperformance. The claim recurs in the abstract, introduction (line 33), and conclusion; it should be corrected to reflect that the model outperforms on two tasks (TSP, IC50) and matches on a third (ESP).

2. **"ProteinVista surpasses current best methods" (Introduction, line 33) conflates ProteinVista alone with an ensemble + optimized pipeline.** ProteinVista *alone* underperforms SPOT on TSP (90.8% vs. 92.4%) and ProSmith-ESP on ESP (91.8% vs. 94.2%). The SOTA-beating results are achieved by **ESM-ProteinVista_OP** — an ensemble that averages predictions from both ProteinVista and ESM-2₆₅₀M, fine-tunes MolFormer embeddings jointly, and adds a contrastive network. Section 3.3 correctly attributes these results to the ensemble system ("ESM-ProteinVista_OP surpasses the current best models," line 140), but the Introduction's blanket claim "ProteinVista surpasses current best methods" creates a misleading impression. This is a framing problem that needs correction.

### Minor

3. **No variance or error bars for any main result.** All numbers in Tables 1 and 2 are single point estimates with no standard deviations or confidence intervals. Given that performance margins on TSP are modest (1.5 pp over ESM-2₆₅₀M), the reader cannot assess whether the reported improvements are stable across runs. The statistical tests (McNemar's, Wilcoxon) are performed on the ensemble vs. ESM-2, not on ProteinVista alone vs. ESM-2. Reporting results from multiple seeds would substantially strengthen the paper.

4. **Potential train/test overlap with the pre-training set is not addressed.** ProteinVista was pre-trained on >500K Swiss-Prot AlphaFold2 structures. The downstream tasks involve well-studied proteins that are likely to be in Swiss-Prot. While Section 4.1's stratification by sequence identity partially addresses this, a direct analysis of whether test proteins (or close homologs) appear in the pre-training set would strengthen confidence in the comparison. The asymmetry matters: ESM-2 cannot "see" 3D structure during its MLM pre-training, so overlap would benefit ProteinVista differently.

5. **No comparison with structure-aware/graph-based methods, despite motivating against them in the Introduction.** The paper criticizes graph-based encoders (DeepFRI, GearNet, ESM-GearNet) for capturing only "residue connectivity" and yielding "incremental gains" (Introduction, lines 17–25), but never evaluates ProteinVista against any of them. This gap does not undermine the paper's core claim (outperforming *sequence* transformers), but it leaves the stated motivation unsubstantiated.

6. **The rotation-robustness claim is slightly overstated.** The model is described as learning "rotation-robust representations" (Abstract) and the Figure 1 caption says augmentations "enforce rotational invariance." However, the ablation (Section 4.2) shows that reducing inference from 5 to 1 augmented views lowers R² by 6.4%, meaning the architecture is not intrinsically invariant but relies on test-time multi-view averaging. The paper acknowledges this ("multiple orientations are essential for robust inference"), but the Abstract and Figure 1 phrasing goes beyond what the architecture delivers on its own.

7. **Factual inconsistency: Rosetta score count.** Section 2.3 (line 73) says the model predicts "23 Rosetta scores," but the Discussion (line 219) says "33 Rosetta scores." Also, the text says replacing contrastive pretraining with Rosetta regression decreases R² by "1.0%" (line 170), while the Figure 2 table reports "~1.2%." These discrepancies should be resolved.

8. **Optimized pipeline (OP) description is underspecified.** Section 3.3 describes several simultaneous changes (joint fine-tuning of MolFormer, training a contrastive network, ensemble averaging) without architectural details or hyperparameters for the contrastive network. This makes the SOTA comparison difficult to interpret or reproduce.

9. **Negative pair construction for the InfoNCE loss is not specified.** Section 2.3 says the loss pushes embeddings from "different proteins" apart but does not describe the sampling strategy (in-batch negatives, mined negatives, etc.). Since InfoNCE effectiveness depends heavily on negative quality, this methodological detail merits clarification.

### Trivial
10. **Equation notation issue in Section 2.1 (line 57).** The density contribution is written as "$\vec{v} = \exp(-\|\vec{v} - \vec{r}\|/\sigma^2)$" which appears to define the voxel center coordinate $\vec{v}$ recursively. The intended meaning (a scalar density value) is clear from context but the notation is garbled.

## Nice-to-Haves
- A comparison with GearNet or ESM-GearNet on the TSP/ESP/IC50 benchmarks would close the evidential gap created by the Introduction's critique of graph-based methods.
- Reporting 3–5 seed runs with standard deviations for all main results would address the variance concern and solidify the modest margins.
- A direct analysis of whether test proteins (or close homologs) appear in the pre-training set would strengthen confidence in the comparison.
- Separately presenting (a) ProteinVista alone, (b) the simple ensemble, and (c) the optimized pipeline ensemble in a more transparent breakdown would prevent the conflated narrative that currently appears in the Introduction.

## Removed Points
*(Points from the input review filtered out under the specified rules.)*

- **"No discussion of the voxelization preprocessing cost"** — Moved to Nice-to-Haves. The paper's inference timing is a fair comparison for end-to-end usage; voxelization is a one-time preprocessing step, and its computational cost is small relative to training/inference.

- **"No description of the validation split or early stopping criteria for any task"** — Removed. Section 3.1 states models were "trained until no further improvement... was observed" with the best validation model selected. This is a standard description.

- **"The MolFormer variant is not identified"** — Removed. Ross et al. (2022) is cited; the specific variant can be found in that reference and the embedding dimension (768) is provided.

- **"No discussion of how the 500K pre-training structures were selected"** — Removed. Useful for full reproducibility but not a weakness; the paper states they are from Swiss-Prot via AlphaFoldDB.

- **"The 'surpasses SOTA' narrative is a structural issue"** — Demoted from "structural issue" to Major weakness #2. The paper correctly attributes the SOTA results to the ensemble in Section 3.3; the overclaim is concentrated in the Introduction/Abstract framing, not a structural flaw in the experimental design itself.

- **Complaints about missing appendix content, proofs, or references** — Removed per rule; these sections were stripped by the parser.

## Novel Insights
None beyond the paper's own contributions. The reviews do not surface a novel interpretation of the results that the paper itself does not already present.

## Suggestions
1. Correct the Abstract/Introduction claims: replace "outperforms on three benchmarks" with "outperforms on two benchmarks (TSP, IC50) and matches on a third (ESP)." Clarify that SOTA-beating results come from the ensemble/OP system, not ProteinVista alone.
2. Add 3–5 independent runs with standard deviations to Tables 1 and 2.
3. Resolve the 23 vs. 33 Rosetta score inconsistency.
4. Add a comparison with at least one graph-based method (e.g., GearNet) to substantiate the Introduction's motivation, or tone down the critique of graph methods if the comparison is infeasible.
5. Describe the negative pair sampling strategy for the contrastive pretraining.
6. Provide architectural details and hyperparameters for the optimized pipeline's contrastive network.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>