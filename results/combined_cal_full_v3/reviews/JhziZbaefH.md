## Summary

This paper proposes OML, a brain-inspired neural network for online multimodal learning with three claimed capabilities: (1) incremental learning of multimodal concepts without catastrophic forgetting, (2) precise reference extraction (identifying which feature dimensions a word refers to), and (3) conflict detection with human-in-the-loop interaction. The architecture uses feature neurons (FNs), unimodal association neurons (UANs), and multimodal association neurons (MANs) connected via ascending, descending, and lateral pathways, with Fourier transforms for cross-modal communication and a coefficient-of-variation-based mechanism for reference extraction.

## Strengths

- **Novel problem formulation.** The paper targets a genuinely underexplored problem: online multimodal learning where the model detects conflicts and interacts with a human user. The "garnet vs. red" example in Fig. 1 provides a compelling motivating scenario distinct from standard continual learning or multimodal learning tasks. *(favorability=6.96)*

- **Reference extraction via coefficient of variation (Section 3.4) is conceptually interesting.** The intuition that dimensions with low variance across examples are the ones a word refers to is sensible and goes beyond the simple image-word binding in prior online methods like AEN and ART. This is the most clearly motivated and novel component of the method. *(favorability=9.38)*

- **Multiple evaluation dimensions.** The paper evaluates three capabilities: baseline online multimodal learning (Table 1), precise referring (Table 2), and modal extension (Table 3). The design of enhanced datasets (E-Fruits, E-HomeF) to isolate reference extraction is a reasonable experimental choice. *(favorability=7.98)*

## Weaknesses

### Fatal
None.

### Major

- **The conflict detection and human-in-the-loop capability — claimed as a core contribution distinguishing this work from prior methods (line 37: "It can detect conflict…ask the user appropriate questions"; line 43: prior methods "cannot…detect conflicts or handle the conflicts through interaction with users") — receives essentially no quantitative evaluation.** The entire evidence is a single sentence (line 250): *"Moreover, when we randomly add 10% of word-image or word-taste data pairs with incorrect matches, OML is able to detect all conflicts and raise appropriate questions."* No precision, recall, F1, confusion matrices, or analysis varying the corruption rate is reported. The claim that questions are "appropriate" is subjective and unverified. Furthermore, the evaluation protocol (line 240: *"if the question posed to the user by OLM remains unanswered for a certain period of time, we set the answer to be positive"*) collapses the human interaction to an "assume positive" default, sidestepping the interactive aspect entirely. This is a decisive evidential gap for a central claimed capability. *(favorability=-0.80)*

- **Key aspects of the method are under-specified.** (a) Eq. (1) includes a parameter *T* (sum over *t=1..T* of cos(...)) with the statement *"its value does not affect the algorithm"* (line 71). However, the sum depends on *T* mathematically — changing *T* changes the number of terms, and for integer λ the sum evaluates to 0 unless λ is a multiple of *T*. The paper does not explain why *T* is claimed irrelevant, making the role of this equation unclear. (b) The Fourier transform in Eq. (6) transmits signals between channels via *"matching the λ parameter"* (lines 119, 250), but the matching mechanism is never specified — how does a signal *"find its correct descending pathways"* by matching a frequency? (c) The Gaussian probability density threshold in Eq. (2) uses ϑ=0.8, but the relationship between this threshold and a meaningful probability given the Gaussian parameters is not explained. These ambiguities make the method difficult to verify or reproduce. *(favorability=0.35)*

- **No ablation studies are conducted anywhere in the paper** (confirmed by grep — zero matches for "ablation"). The architecture has multiple components (lateral connections, Fourier transform, frequency encoding, reference extraction, conflict detection) whose individual contributions are never isolated. For example, lateral connections are claimed to *"improve the generalization ability"* (line 59), but this is never tested. Without ablations, it is impossible to determine which components drive the reported results. *(favorability=0.61)*

### Minor

- **No variance or statistical significance is reported.** Tables 1–3 present single numbers without standard deviations, confidence intervals, or significance tests. Given the small datasets and stochastic online learning process, the reliability of reported margins (e.g., OML 89.8 vs. AEN 86.2 in Fruits Open V→A) cannot be assessed. *(favorability=2.21)*

- **The open-environment comparison against offline methods (DAE, DBM, DJSRH, NRCH, FUME) compares methods never designed for continual learning against one that is.** The paper is transparent about this (lines 223-224: *"These five methods are offline paradigms"*), but the framing of this comparison as evidence of OML's superiority is not very informative — the gap largely reflects the experimental design mismatch rather than architectural superiority. *(favorability=3.22)*

- **The evaluation uses small, specialized datasets (Fruits, HomeF) with hand-crafted features** (Fourier descriptors of object boundaries, mean color, MFCCs). While SAM (2023) is used for segmentation, the overall feature pipeline is far removed from modern learned representations. This limits conclusions about scalability to real-world high-dimensional inputs. *(favorability=0.02)*

### Trivial
None.

## Nice-to-Haves

- Sensitivity analysis for the threshold *r* in Eq. (7) (currently set to 0.5 with no exploration).
- Analysis of model capacity/growth (number of neurons added during learning, scalability).

## Removed Points

These points were flagged by the harsh critic but removed per the filtering rules:

- **Criticism about missing comparison with CLIP/ALIGN/etc.** — Removed. CLIP is a pretrained foundation model on 400M pairs; the paper compares against the relevant online multimodal learning literature. Demanding this comparison is scope creep and speculative about relative performance.
- **Criticism about "outdated framing from Srivastava & Salakhutdinov (2014)"** — Removed as a stylistic opinion.
- **Criticism about not discussing EWC/SI/replay continual learning literature** — Weakened: the paper's scope is online multimodal learning specifically, and it cites the relevant prior work in that area. General unimodal continual learning is a different subfield.
- **Criticism about Fourier descriptors being "unusual and outdated"** — Removed: using SAM (2023) for segmentation is modern; Fourier descriptors for shape are a standard technique.
- **Criticism about "no analysis of model capacity or growth"** — Moved to Nice-to-Haves; not a core requirement.
- **Criticism that the mathematical framework is "impossible to verify" or "structurally fatal"** — Downgraded to Major (method clarity issues). The paper does describe the algorithm procedurally in Section 3.5 with four concrete cases, even if the equations are incompletely specified.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Provide a concrete numeric worked example** tracing one input pair through the entire network — this would resolve the method clarity concerns about Eq. (1), the Fourier transform, and λ matching.
2. **Run controlled experiments for conflict detection:** vary the fraction of corrupted pairs (1%, 5%, 10%, 20%), report precision/recall/F1, and evaluate whether the questions match ground-truth conflicts. This is essential to substantiate a core claimed capability.
3. **Add ablation studies** removing lateral connections, the Fourier transform mechanism, and the reference extraction module separately to quantify each component's contribution.
4. **Report standard deviations** across multiple random seeds and add variance estimates to Tables 1–3.
5. **Add sensitivity analysis** for the threshold *r* in Eq. (7) and clarify the role of *T* in Eq. (1).
6. **Consider evaluating on a standard multimodal benchmark** (e.g., with learned features) to demonstrate scalability beyond hand-crafted features.

---

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated topic (cross-lingual robotics); much weaker |
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated (finance); much weaker |
| u1cQYxRI1H.md | 0.50 | R1 | No | Unrelated (diffusion); score is artifact |
| 5lUdTogEL3.md | 1.00 | R1 | No | Related topic (lifelong Re-ID); much weaker |
| gNoqEdT2wO.md | 2.33 | R1,R2 | Yes | Multimodal CIL benchmark; similar weakness scope but less novel contribution |
| WM5G2NWSYC.md | 2.00 | R1 | No | Projected subnetworks; less related |
| JIlIYIHMuv.md | 2.50 | R1 | No | LVLM continual learning; clearer method but similar evaluation gaps |
| HCCkCjClO0.md | 3.00 | R1 | No | Online weight approximation; different approach |
| vSOTacnSNf.md | 4.33 | R1 | No | Multimodal meta-learning INR; different area |
| Pa6SiS66p0.md | 4.33 | R1,R2,R3 | Yes | Multimodal lifelong learning benchmark; clearer evaluation than our paper but less novel architecture |
| CagdoUkvvl.md | 4.50 | R1,R2,R3 | Yes | Multimodal CL with ablations; stronger experimental rigor but less novel architecture |
| UhKkWHkvfg.md | 5.00 | R1 | No | Analytic TTA; different problem |
| sb7qHFYwBc.md | 6.50 | R1,R2 | Yes | C-CLIP; significantly stronger evaluation and clearer method |
| Y7jJN0VQ4y.md | 5.71 | R1 | No | Video anomaly detection; different area |
| bfRDhzG3vn.md | 5.75 | R1 | No | Spoken language understanding; different area |
| RnxwxGXxex.md | 5.67 | R1 | No | Dynamic benchmarking; different area |
| TPZRq4FALB.md | 8.00 | R1 | No | Test-time adaptation; far stronger paper |
| kbjJ9ZOakb.md | 8.00 | R1 | No | Neuroscience; far stronger paper |
| RWJX5F5I9g.md | 8.00 | R1 | No | Brain-inspired RL; far stronger paper |
| aWXnKanInf.md | 8.00 | R1 | No | Topographic LM; far stronger paper |
| G9Ea7mlqGO.md | 3.80 | R2,R3 | Yes | CLIP online CL; simpler method, stronger empirical evaluation |
| 0CtIt485ew.md | 4.00 | R2,R3 | Yes | Brain-inspired CL; similar bio-inspiration but clearer evaluation |
| 04TRw4pYSV.md | 3.50 | R2 | No | LMM prompt CL; similar evaluation gaps |
| f1uXrAjpOH.md | 5.40 | R2 | No | Emotion recognition; different problem |
| 3YQYo1O01W.md | 3.67 | R2 | No | Vision-knowledge conflicts; different problem |
| sMFqEror1b.md | 4.75 | R2 | No | Theory of mind; different problem |

**Round-1 bracket:** The most relevant anchors sit between 2.33 and 4.50. Papers below 2.33 are either unrelated or have fundamentally weaker contributions. Papers above 4.50 have either clearer methodology or stronger experimental validation.

**Round-2 narrowing:** Compared against G9Ea7mlqGO (3.80), Pa6SiS66p0 (4.33), and 0CtIt485ew (4.00), our paper has a more novel architecture (reference extraction mechanism at 9.38 favorability vs. these anchors' simpler methods), but falls short on two key axes: (1) the conflict detection evaluation gap (-0.80) is a weakness these anchors do not share to the same degree — they evaluate their claimed capabilities, even if imperfectly; (2) the method clarity issues (0.35 favorability) are worse than in the anchors, where the mathematical framework is standard and clearly described. The absence of ablation studies also places this paper below CagdoUkvvl (4.50), where ablations strengthened the evaluation. Balancing the genuinely novel reference extraction concept against the unverified core claim and method ambiguities, the paper sits slightly below the 3.80–4.50 anchor range.

**Final score:** 3.5

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>