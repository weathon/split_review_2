Now let me compile all the anchors and make the final calibration.

**Anchor summary (all papers retrieved across rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| u1cQYxRI1H.md | 0.50 | R1 | No | Completely different topic (illumination) — irrelevant |
| gwZ90hFSL2.md | 1.00 | R1 | No | Irrelevant topic (humanoid robots) |
| P49gSPmrvN.md | 1.00 | R1 | No | Irrelevant topic (scientific discourse) |
| nSDOkm0SKo.md | 1.00 | R1 | No | Irrelevant topic (financial markets) |
| m9zWBn1Y2j.md | 3.00 | R1 | No | Ligand conformation generation — distantly related, lower quality |
| rEQ8OiBxbZ.md | 3.00 | R1/R2 | No | 3D molecular pretraining — similar topic but rejected with score 3 |
| An87ZnPbkT.md | 3.00 | R1 | No | GNN docking algorithm selection |
| 1JgWwOW3EN.md | 2.50 | R1 | No | Molecular representation benchmark |
| ZuU4mZILBB.md | 4.38 | R1 | No | Deep learning docking survey |
| xNDydjYBmC.md | 4.60 | R1 | Yes | PPB affinity prediction — has similar "missing baselines" issues |
| 0sU4myabw1.md | 4.25 | R1 | No | Molecular docking speed |
| gB2ZeqDpl6.md | 4.00 | R1 | No | DTI benchmark — survey paper |
| AXbN2qMNiW.md | 5.67 | R1/R3 | Yes | Protein-ligand binding SSL — has data leakage concerns |
| RgE1qiO2ek.md | 6.25 | R1 | No | 3DMolFormer — docking/drug design |
| zDC3iCBxJb.md | 6.75 | R1 | No | GroupBind — ligand docking, strong |
| ARQIJXFcTH.md | 6.75 | R1/R2 | Yes | **AtomSurf** — most comparable: protein structure representation, has surface-vs-graph comparison gap |
| 0ctvBgKFgc.md | 8.00 | R1 | No | Protein generation — different task, very strong |
| kJFIH23hXb.md | 8.00 | R1 | No | Protein backbone generation — different task |
| zMPHKOmQNb.md | 8.00 | R1 | No | Protein discrete generative model — different |
| NSVtmmzeRB.md | 8.00 | R1 | No | Molecular generative model — different |
| jqx5XI4Yr3.md | 3.40 | R2 | No | ProteinAdapter — similar integration approach |
| N4lUNwEn1c.md | 3.00 | R2 | No | Chemical features — tangential |
| vVlNBaiLdN.md | 3.00 | R2 | No | ESMGain — mutation effect prediction |
| iBAWiEjogY.md | 3.67 | R2 | Yes | **ProteiNexus** — structure+sequence integration, rejected, lower quality |
| i6jYK0hd0B.md | 4.00 | R2 | No | 3D interaction pretraining |
| tNAucRS0QQ.md | 5.25 | R2 | No | BIT — biomolecular interaction transformer |
| K3tHTPjFBM.md | 4.00 | R2 | No | Equivariant multi-task learning |
| BIveOmD1Nh.md | 6.33 | R3 | No | Equivariant scalar fields for docking |
| BEH4mGo7zP.md | 5.75 | R2 | Yes | **ProteinINR** — sequence+structure+surface pretraining, accepted |
| sTYuRVrdK3.md | 6.25 | R2/R3 | Yes | **ProteinWorkshop** — benchmark suite, accepted |
| QKywN4BbqA.md | 5.25 | R2 | No | E3former — equivariant transformer |
| O0dW800ukz.md | 5.67 | R2/R3 | No | Multimodal distillation of protein sequence+structure+function |
| 760br3YEtY.md | 5.60 | R3 | No | Enzyme promiscuity prediction |
| jsQPjIaNNh.md | 5.25 | R3 | No | Protein function prediction |

**Round 1 bracket:** Initially bracketed between ~3.5-6.5 based on preliminary search.

**Narrowing (Round 2):** The most comparable papers are **AtomSurf (6.75)**, **ProteinINR (5.75)**, and **ProteinWorkshop (6.25)**. These are all protein structure representation papers with similar evaluation setups.

**Final comparison with most relevant anchors:**

- **AtomSurf (6.75):** Had very high favorability strengths (up to 11.81) and a devastating -5.71 weakness (low novelty). Our paper's strengths are comparably high (7.93-10.67), and our worst weakness (-0.95 for missing GNN comparison) is far less damaging than -5.71. But AtomSurf had a clear contribution (surface+graph integration) with direct SOTA comparisons. Our paper is weaker on the key comparison dimension.

- **ProteinINR (5.75):** Had similar weaknesses — "performance in line with existing work" (-0.20), "lacks important baselines" (-0.73), "many components not new" (-1.47). Our paper's worst weakness (-0.95) sits between theirs, and our other weaknesses are milder. Our strengths are stronger (9.64-10.67 vs 7.32-9.38). Our paper is somewhat stronger than ProteinINR.

- **ProteinWorkshop (6.25):** A benchmark paper with different evaluation standards. Not directly comparable.

My draft's items: strengths 7.93-10.67 (high), weaknesses ranging from -0.95 to 6.58, with one strongly damaging (-0.95), one moderately damaging (2.43), and the rest mild.

I place this paper between ProteinINR (5.75) and AtomSurf (6.75), closer to ProteinINR. **Final score: 5.5**. The paper has solid contributions but the unaddressed motivating claim (atom-level > residue-level GNN, not tested) and the overclaiming title/abstract are significant issues that need to be resolved before acceptance.

Now let me see... should I say Reject or Accept? At 5.5, the ICLR guidelines would put this between borderline reject (4) and borderline accept (6). I'll say Reject but with clear instructions on what would make it acceptable.

Actually wait, let me reconsider. The hard rules say "do not pull a clearly strong paper down to the middle out of caution." But is this a clearly strong paper? No — it has real issues. And "A strong, well-supported contribution should be scored high." The compute efficiency and complementarity demonstrations are strong, but the missing comparison against the very methods the paper motivates against is a real gap.

I'll go with 5.5 and Reject, noting that the paper could rise to 6+ with revisions addressing the main concerns.Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper introduces ProteinVista, a 3D CNN encoder that operates on voxelized full-atom protein structures, pretrained on ~500K AlphaFold2 structures, and evaluated on protein-ligand interaction benchmarks (enzyme-substrate prediction, transporter-substrate prediction, and drug-target IC50 regression). The model demonstrates impressive compute efficiency (20s per 1000 proteins vs 426s for ESM-2_650M on an A100), requires ~1% of the GPU-hours for pretraining, and provides representations that are complementary to sequence-based ESM-2 embeddings.

## Strengths

- **Well-documented compute efficiency advantage.** Section 4.3 provides concrete numbers: ProteinVista processes 1,000 proteins on one A100 in 20 seconds during training versus 426 seconds for ESM-2_650M. Pretraining used ~1% of the GPU-hours of ESM-2_650M (48h on 4 A100s vs 7 days on 128 H100s). These runtime differences are stark and well-supported.

- **Complementarity between sequence and structure convincingly demonstrated.** The ESM-ProteinVista ensemble consistently outperforms either model alone across nearly all tasks (Tables 1, 2). Section 4.1's analysis by sequence identity, TM-score, and pLDDT bins (Figures 2a-c) reveals when each representation type helps — ProteinVista excels in high-identity bins (where few mutations matter structurally) while ESM-2 leads in low-identity bins (remote homology). This is actionable and well-supported.

- **Honest about limitations.** The paper tests a case where the approach is expected to perform poorly (GO term prediction, Section 3.4) and reports that ProteinVista underperforms ESM-2 (F_max 0.57 vs 0.62). It also stratifies by pLDDT confidence (Figure 2c), showing gains concentrate in high-confidence structures. This boundary-testing is valuable.

- **Good ablation coverage.** Section 4.2 tests multiple design axes — number of test-time augmentations (1/5/10 views), voxel resolution (1.0 vs 1.5 Å), pretraining objective (contrastive vs Rosetta regression), and training-time augmentation. The finding that disabling training-time augmentation has near-zero impact on IC50 (−0.1% R²) while reducing test-time views from 5 to 1 drops R² by 6.4% is informative and non-obvious.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed title and abstract relative to evidence.** The title claims ProteinVista "OUTPERFORMS SEQUENCE TRANSFORMERS" across the evaluated benchmarks. However, on the ESP benchmark (Table 1), ProteinVista matches or slightly trails ESM-2_650M across all four metrics (Acc 91.8% vs 91.9%, ROC-AUC 0.951 vs 0.955, MCC 0.78 vs 0.79) — it does not outperform. The abstract similarly states it "outperforms sequence transformers on three benchmarks" without qualification. The paper's own text more accurately says "surpasses or equals" (line 115), but the title and abstract overstate the case. The framing should be scoped to the tasks where improvement is real (IC50 regression, TSP classification).

- **No comparison against residue-level structure-aware GNNs, despite motivating against them.** The Introduction (lines 17-25) motivates ProteinVista by arguing that residue-level GNNs like GearNet, DeepFRI, and ESM-GearNet "ignore the precise arrangement of atoms" and yield only incremental gains over ESM-2. Yet the experiments compare ProteinVista primarily against ESM-2 (a sequence-only model), not against GearNet or other structure-aware GNNs. The SOTA comparison in Section 3.3 compares against SPOT, ProSmith-ESP, and Fusion_ESP — specialized substrate prediction models. A direct comparison against GearNet or ESM-GearNet on the same tasks with the same training protocol would directly test whether atom-level 3D CNNs capture more than residue-level GNNs, which is the paper's claimed novelty. Its absence means the paper demonstrates that structure (via 3D CNN) helps over sequence alone, but not that atom-level structure helps over residue-level structure. This is a significant gap.

- **Contrastive pretraining depends on ESM-2 as teacher, partially undermining the independence claim.** Section 2.3 describes the primary pretraining objective: contrastive alignment of ProteinVista's embeddings with ESM-2's via InfoNCE loss. This means the pretrained weights used for downstream tasks carry information distilled from ESM-2. The paper does compare against a Rosetta-regression pretraining variant (which is ESM-2-independent) on IC50 and finds only a 1.0% R² drop (Section 4.2), which is good evidence that ESM-2 dependence is not the sole driver. However, the Rosetta-pretrained variant's results are not reported on the TSP and ESP benchmarks, so the reader cannot assess whether headline claims hold for a model genuinely independent of ESM-2. Reporting Rosetta-pretrained performance on all benchmarks would clarify this.

### Minor

- **Limited rotation augmentation (only 90° axis-aligned flips).** Section 2.4 describes augmentations as rotations by 90° around Cartesian axes and mirror reflections, covering at most 24 discrete orientations. The claim in the abstract of "rotation-robust representations" is overstated for this limited set. The ablation confirms sensitivity: reducing test-time views from 5 to 1 drops IC50 R² by 6.4% (Section 4.2). The paper should explicitly acknowledge this as a limitation rather than describing it as "extensive 3D augmentations" (line 31).

- **Inconsistencies between prose and table in ablation values.** Section 4.2 (prose) reports: reducing 5→1 view lowers R² by 6.4%, Rosetta vs CL pretraining decreases R² by 1.0%, and 1.5Å vs 1.0Å resolution decreases R² by 1.1%. However, the embedded table (Figure 2 caption, lines 183-189) reports different values: ~-5.5%, ~1.2%, and ~0.8% respectively. These should be reconciled.

- **Discrepancy in number of Rosetta scores.** Line 73 says 23 Rosetta scores were used for regression pretraining, while line 219 in the Discussion says 33 Rosetta scores. One of these is incorrect.

- **No confidence intervals or variance estimates reported.** Tables 1 and 2 report point estimates without standard deviations, confidence intervals, or multiple-run statistics. The statistical tests (McNemar's, Wilcoxon) are applied to some ensemble comparisons but not the core ProteinVista vs ESM-2 comparison. Without variance estimates, the stability of the reported margins (e.g., +1.5% TSP accuracy) cannot be assessed.

### Trivial
None.

## Nice-to-Haves

- Report the Rosetta-pretrained variant's performance on all three benchmarks (not just IC50) to clarify whether ProteinVista's gains are independent of ESM-2 distillation.
- Add a comparison against a residue-level GNN (e.g., GearNet or ESM-GearNet) on at least one task to directly test the motivating claim.
- Add confidence intervals or standard deviations for main results to show stability.
- Consider continuous SO(3) rotation sampling during training for genuine rotation invariance, or explicitly note the limitation.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "Data splits and leakage concerns" — The paper's similarity-binned analysis (Figure 2a) implies controlled splits exist; no concrete evidence of leakage was presented.
- "Heavy-atom coverage — what about metals/halogens?" — The paper explicitly scopes to the five most common heavy atoms (C, N, O, S, P); this is a design choice, not a flaw.
- "Missing reproducibility details (hyperparameters)" — The paper references supplementary tables (S1, S2, S3) and mentions learning rate search; detailed hyperparameters are likely in the stripped appendix.
- "ESM-ProteinVista ensemble performs worse than ProteinVista alone on IC50" — The paper acknowledges this and offers a reasonable biochemical explanation (lines 119-125).
- "Only molecular-function GO tested, not BP or CC" — The paper acknowledges this and frames GO evaluation as a test where the approach should not work well.
- "Rotation augmentation should use full SO(3)" — The paper describes what it does; demanding full SO(3) sampling is beyond standard practice for 3D CNNs and would dramatically increase data complexity.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the title and abstract to lead with complementarity rather than superiority. The ensemble results and similarity-binned analysis (Section 4.1) are the paper's most convincing and original findings. A title like "ProteinVista: A Compute-Efficient Atom-Level 3D CNN Providing Complementary Signal to Sequence Transformers for Protein-Ligand Prediction" would better align with the evidence.
- Reconcile the ablation prose/table discrepancies and the Rosetta-score count (23 vs 33).
- Correct the figure label in Figure 3c which says "Inference Time" but the prose (line 174) clarifies it's training throughput.

## Score and Decision

**Bracket (Round 1):** Initial calibration placed this paper in the 3.5–6.5 range based on similarity to protein structure representation papers.

**Narrowing (Round 2/3):** The most comparable itemized anchors are AtomSurf (6.75), ProteinINR (5.75), and the Protein-ligand binding SSL paper (5.67). Our paper's strengths have comparable favorability (7.93–10.67) to these anchors' top items. Our most damaging weakness (missing GNN baseline comparison, favorability=-0.95) is less severe than ProteinINR's worst (-1.47 for "many components not new," -0.73 for "lacks baselines") but more severe than the binding SSL paper's worst (-0.43 for data leakage concerns, -0.76 for narrow encoder ablation). The overclaiming weakness (2.43) is moderately damaging. Overall, the paper sits between ProteinINR (5.75) and AtomSurf (6.75), closer to ProteinINR, given the significant gap in testing the core motivating claim.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>