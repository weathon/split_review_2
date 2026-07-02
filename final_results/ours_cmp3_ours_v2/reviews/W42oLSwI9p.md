## Summary

This paper proposes three one-step diffusion-based solvers (CMILP, SCMILP, MFILP) for non-binary Integer Linear Programming (ILP). It introduces an Iterative Integer Projection (IIP) layer to handle non-binary integer variables differentiably, and an objective-guided sampling with momentum. The key motivation is that existing diffusion-based ILP solvers have prohibitively long inference times (hours), and the proposed methods achieve massive speedups (minutes/hours → seconds) while maintaining competitive solution quality on some benchmarks.

## Strengths

- **Massive speed improvements over prior diffusion-based ILP solvers.** The paper addresses a real bottleneck: inference time of diffusion-based ILP solvers measured in hours. The proposed one-step methods reduce inference to seconds on most benchmarks — e.g., from 65 minutes (DDIM) to ~20 seconds on Set Cover (Table 1), from hours to seconds on synthetic non-binary datasets (Table 6). This is a genuine and important practical improvement.

- **The Iterative Integer Projection (IIP) layer (Eq. 3) is a technically clean contribution for non-binary variables.** The function f_proj(x) = x − sin(2πx)/(2π) is differentiable, has integer values as fixed points, and converges to integer values in a few iterations. This extends neural ILP solvers beyond the binary-only case without the exponential blowup of binary encoding (confirmed in Table 4), which is a meaningful step forward for the field.

- **Strong results on large-scale synthetic non-binary ILP (Table 6).** On Random-(500,20,2) through Random-(2000,20,2), the proposed methods achieve gaps of 0.0–1.1%, competitive with or better than IP Guided DDIM (0.3–0.7%), in seconds rather than minutes/hours. This is the strongest evidence that the approach can work well.

## Weaknesses

### Fatal
None.

### Major

- **Headline claims overstate binary ILP results.** The abstract states the methods "outperform existing learning-based methods on both binary and non-binary instances." Table 1 shows the opposite on binary benchmarks: IP Guided DDIM achieves substantially better optimality gaps (SC: 68.5% vs 88.4–91.6%; CF: 54.6% vs 76.1–82.9%; CA: 25.4% vs 79.2–85.3%). The paper's own experimental text acknowledges that "IP Guided DDIM consistently produces the lowest gap across all datasets." The methods trade solution quality for speed on binary problems, but the abstract and introduction present this as an unqualified improvement. Similarly, Contribution 1 claims "higher solution feasibility compared to previous neural solvers, reaching nearly 100% on binary ILP problems" — sample feasibility on CF is 88.3–92.1% (DDIM achieves 89.7%), and only the less demanding dataset feasibility metric hits 100% uniformly. The paper needs to honestly characterize the speed–quality trade-off rather than claiming overall superiority.

- **Duplicate method labels in Tables 2–4 make results partially uninterpretable.** In Tables 2, 3, and 4, two rows are both labeled "SCMILP (Ours)" with different performance figures (e.g., Table 2: Gap 16.5% vs 12.2%, Sample Feasibility 69.2% vs 42.4%). CMILP, described as a co-equal method alongside SCMILP and MFILP, is absent from these tables. The natural reading is that one row should be "CMILP (Ours)," but the reader cannot determine which is which. This makes it impossible to compare results across tables (e.g., with Table 1 where all three methods are distinctly labeled). The error must be corrected.

### Minor

- **Momentum ablation shows modest gains on a dataset where absolute performance is poor.** Table 5 on IM-(50,5,10) shows momentum reducing gap from 104.5%→101.8% (10 steps) and 99.8%→95.8% (20 steps), with 1–4% dataset feasibility improvement. The improvement is directionally correct but small, and all configurations have gaps >95%, meaning the method performs poorly on this dataset regardless of optimizer choice. The paper's claim that momentum "improves the search quality significantly" is overstated.

- **IIP training–inference iteration mismatch lacks discussion of gradient behavior.** The paper uses K=1 projection iteration during training and K>1 during testing (line 89). Since the derivative of f_proj at integer points is zero (cos(2πx)=1 → 1−cos(2πx)=0), repeated iteration during training would drive gradients to zero — explaining the single-iteration training choice. This design rationale is not discussed in the main text.

### Trivial
None.

## Nice-to-Haves

- An ablation study varying the IIP iteration count K would strengthen understanding of this key component.
- A dedicated analysis of why binary results degrade compared to DDIM (e.g., problem structure vs training data quality) would be more valuable than additional synthetic datasets.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Missing appendix details for SCMILP/MFILP.** The harsh critic noted that shortcut and meanflow models are deferred to the appendix. Removed because the parser strips appendix content from all papers; the details exist in the original submission.
- **No code available.** Removed because code will be released after acceptance, which is standard practice for ICLR.
- **Loss function (Eq. 6) Dirac delta target questioned.** The harsh critic questioned why the Dirac delta is the right target for the consistency loss. Removed because this design choice is motivated by the optimization setting (where the goal is a specific solution, not a distribution), and further details may be in the appendix.
- **No statistical significance/variance reported.** Removed because single-run evaluation is standard in this literature; not a specific flaw of this paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the abstract and introduction to honestly characterize the speed–quality trade-off on binary problems rather than claiming unqualified "outperformance" over all learning-based methods.
2. Fix the duplicate method labels in Tables 2–4 — clearly label all three methods (CMILP, SCMILP, MFILP) so results are interpretable.
3. Add a brief discussion of why K=1 is used during training (the gradient vanishing at integer fixed points) to clarify the IIP design.
4. Temper the claim about momentum's effectiveness given the modest improvements on a dataset where all gaps exceed 95%.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| joMMM9eadc (IP via Guided Diffusion) | 6.25 | R1/R2 | Similar diffusion-for-IP topic; current paper has IIP non-binary contribution but also overclaiming and table errors |
| FPfCUJTsCn (DiffILO) | 7.20 | R1 | Stronger paper; unsupervised ILP learning is more novel than applying one-step models to ILP |
| 6JDpWJrjyK (DISCO) | 5.75 | R1/R2 | Similar CO+diffusion+speed focus; current paper has IIP novelty but concrete reporting flaws |
| 2oWRumm67L (Light-MILPopt) | 5.00 | R1 | Accepted despite presentation issues; similar profile of genuine contribution + presentational problems |
| K6kt50zAiG (CAMBranch) | 5.75 | R2 | Accepted with presentation concerns; current paper has more serious overclaiming |
| xQVxo9dSID (Consistency Models Made Easy) | 6.75 | R2 | Stronger execution on consistency models; accepted despite novelty questions |

**Round 1 bracket:** 5.0–6.5  
**Final score narrowed to:** 5.5 — The paper has genuine contributions (IIP layer for non-binary ILP, massive speedups) but the abstract overclaims relative to the binary results, and the duplicate method label in Tables 2–4 is a concrete reporting error that makes parts of the evidence uninterpretable. These issues are fixable but prevent a positive recommendation in the current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>