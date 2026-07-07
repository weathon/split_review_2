## Summary

OMMP-Bench identifies and corrects three systematic problems in the emerging protocol for online map based motion prediction: (1) a severe train-validation gap caused by evaluating motion prediction with maps generated from a model's own training data (87.6 vs. 50.3 mAP shift, Fig. 3); (2) a perception-range mismatch between online mapping (~30×60m) and motion prediction agents (>100m), hidden by ego-only metrics; and (3) non-discriminative metrics that include easily-predicted static agents. The paper proposes a new spatially-disjoint data split, classified metrics (close/far/ego), and a boundary-free baseline that supplements out-of-range agents with raw image features.

---

## Strengths

- **Concrete, quantified train-val gap.** The 87.6 vs. 50.3 mAP drop (Fig. 3) is directly attributable to the two-stage protocol design and is large enough to be consequential. Table 1 confirms the practical benefit: the proposed split achieves minADE 0.6308 vs. 0.6839 under the default split.

- **Striking spatial overlap finding.** Fig. 4 demonstrates that 87% of nuScenes validation data spatially overlaps training under the default split; the proposed split reduces this to 5%. This is precisely quantified and visually clear.

- **Well-structured range-mismatch argument.** Tables 2 and 3 form a clean diagnostic chain: extending online map range to 100×100m collapses mAP (0.164→0.002 for MapTRv2-CL, Table 2), yet GT maps at the extended range improve motion prediction (Table 3). The conclusion—that current online mapping models structurally cannot meet motion prediction range requirements—is presented with direct empirical evidence.

- **Table 7 reveals practically important and novel findings.** The breakdown across Ego / Moving Non-Ego Close / Moving Non-Ego Far across four method combinations shows that ego-focused improvements (unc, bev) sometimes *degrade* close non-ego performance—an unexpected finding that is invisible under the prior ego-only protocol.

---

## Weaknesses

### Fatal
None.

### Major
- **Small validation set without statistical grounding.** The benchmark's motion validation set contains only 86 scenes (Sec. 4.1). No variance estimates, confidence intervals, or bootstrap error bars are reported for any table. For a benchmark paper whose central purpose is to enable reliable method comparison, this is a meaningful gap: the close vs. far agent performance differences in Table 7 are presented as conclusions (e.g., minADE improvements of 1–13% between methods) without any evidence they exceed noise. The paper should report variance over multiple seeds or bootstrap resamples, or explicitly flag that Table 7's fine-grained comparisons should be read directionally.

### Minor
- **Reduced map training data not discussed.** The proposed split allocates only 367 scenes for map model training vs. ~700 in the standard nuScenes training set (Sec. 4.1). This tradeoff is introduced by fixing the spatial overlap problem but is neither quantified (e.g., no map model mAP under the new split is reported) nor discussed as a limitation. The benchmark's motion prediction conditions may be more pessimistic than real deployment partly due to data starvation rather than purely from eliminating the train-val gap.

- **Unexplained performance anomaly in Table 7.** Sec. 4.2 notes that unc and bev methods improve ego prediction but sometimes hurt Close non-ego performance (e.g., MapTRv2-CL+DenseTNT unc: minADE increases 4.1% for Close agents). This is the paper's most surprising finding, but no hypothesis is offered. Without even a speculative explanation, it reads as an anomaly rather than a transferable insight.

- **Boundary-free baseline underspecified in main text.** Eq. (1) leaves $A_i$ initialization (is it the agent's positional embedding? trajectory feature?) and multi-level feature handling unspecified. Code release (Sec. 7) addresses reproducibility, but a brief clarification in the main text would help readers understand the design rationale.

### Trivial
- Table 5 rows 2 and 3 as parsed both show configuration (✗ ✓ ✗ ✗), yet report different minADE values (0.6829 vs. 0.6558). This is likely a parser artifact—the original table likely has a distinct configuration in row 3 (e.g., pedestrian crossing only). The Sec. 3.5 conclusions are internally consistent with the surrounding text, but the table as presented is ambiguous.

---

## Nice-to-Haves
- A controlled experiment demonstrating a **ranking reversal**—a method that wins under the default protocol but loses under OMMP-Bench—would make the benchmark's corrective contribution decisive rather than merely diagnostic.
- An ablation of the boundary-free baseline with scrambled image features would confirm that far-agent improvements come from structural road information rather than a regularization effect.
- Reporting map model mAP under the new 367-scene split alongside the default would confirm whether the benchmark's conditions introduce a meaningful performance floor.

---

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Table 5 row duplication as a substantive flaw**: The critic explicitly calls this "almost certainly a parser artifact." Per filtering rules, formatting/parser artifacts are not author errors. Retained only as Trivial to alert readers.
- **Boundary-free baseline underspecification treated as Major**: Code release is promised (Sec. 7) and appendix details exist (stripped by parser). Per policy, undisclosed implementation details addressable by code release are not Major. Retained as Minor.

---

## Novel Insights
The paper's most novel observation is that the train-validation gap in the two-stage online-map-based motion prediction pipeline is not a minor calibration issue but a ~37-point mAP swing that causes systematic overestimation of motion prediction quality during training. Equally novel is the demonstration that ego-centric evaluation metrics—used exclusively in prior work—may actively obscure degraded performance for non-ego close agents when certain map-uncertainty or BEV-feature methods are applied. These two findings together suggest that prior benchmarks in this emerging space may have drawn incorrect methodological conclusions about which approaches are beneficial.

---

## Suggestions
- Report bootstrapped confidence intervals (or at minimum standard deviations over multiple seeds) for Table 7's key comparisons to give the benchmark statistical credibility.
- Report map model mAP under the new 367-scene training split to quantify the data-reduction tradeoff.
- Offer a brief mechanistic hypothesis for why ego-focused methods (unc, bev) sometimes hurt Close non-ego agents—this is the paper's most surprising empirical result and deserves at least a conjecture.

---

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| pzZjyYee6L.md | 2.50 | R1 | Trajectory prediction with kinematic models; weaker contribution, AD topic |
| ZPCBcR7Drg.md | 5.00 | R1/R2 | MapDR benchmark for HD maps+traffic signs; similar benchmark genre, rejected |
| ubuGgIPVD0.md | 5.00 | R2 | TSTTC dataset; new dataset paper, rejected |
| k3y0oyK7sn.md | 5.40 | R2 | BEV segmentation benchmark+uncertainty; similar scope |
| sEJYPiVEt4.md | 5.25 | R1 | ESDMotion SD map motion prediction; very close topic, borderline reject |
| LsURkIPYR5.md | 6.00 | R1 | LaneSegNet online map learning; accepted, stronger technical contribution |
| efeBC1sQj9.md | 7.00 | R1 | SEPT motion prediction pretraining; accepted, stronger algorithmic contribution |
| mDIXfHvoqH.md | 6.75 | R1 | ITPNet trajectory prediction; accepted, introduces novel task |
| npBAHV5BJI.md | 7.00 | R2 | Inductive KGC benchmark correction; very analogous (identifies protocol flaw, fixes split); **closest analog** |
| S8gbnkCgxZ.md | 7.00 | R2 | Bioactivity prediction task redefinition; analogous reframing paper, accepted |
| RyWypcIMiE.md | 6.50 | R2 | SBDD evaluation reframing; analogous metric correction, accepted |
| Im2neAMlre.md | 7.33 | R2 | T2I evaluation stability; benchmark correction genre, accepted |

**Round 1 bracket:** 5.0 – 7.0  
**Narrowing:** The strongest analog is npBAHV5BJI (avg 7.0, "Towards Better Benchmark Datasets for Inductive KGC"), which similarly identifies a concrete data-construction flaw (PPR shortcut), demonstrates it empirically, and proposes a corrected dataset. OMMP-Bench does the same but in a narrower niche (nuScenes only) with a smaller validation set (86 scenes) and no statistical variance reported. That combination of narrow scope and missing statistical grounding is the key differentiator pulling it below npBAHV5BJI. Against RyWypcIMiE (6.50, accepted) and LsURkIPYR5 (6.00, accepted), OMMP-Bench is similarly rigorous in its diagnostic chain but weaker in scale. Against ZPCBcR7Drg (5.00, rejected), OMMP-Bench offers clearer problem diagnosis and more actionable fixes. Final calibrated score: **6.0** — borderline accept; the genuine and specific contribution to a field that has been building on a flawed foundation outweighs the evidential limitations, but the small validation set and missing statistical grounding are real concerns for a benchmark paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>