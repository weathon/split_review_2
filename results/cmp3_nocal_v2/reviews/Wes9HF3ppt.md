Now let me write the final consolidated review.

## Summary

This paper proposes Insertion Language Models (ILMs), a sequence generation approach where tokens are inserted one at a time at arbitrary positions, using a denoising training objective with a tailored transformer parameterization and a stopping classifier. The key claimed advantages are (1) overcoming the fixed-length infilling and simultaneous-unmasking limitations of Masked Diffusion Models (MDMs), and (2) outperforming ARMs and MDMs on planning/symbolic tasks while being competitive on text tasks.

## Strengths

- **Clear diagnosis of MDM limitations (Section 2).** The paper concretely identifies two structural problems with MDMs — fixed-length mask tokens preventing variable-length infilling, and simultaneous unmasking violating sequential dependencies — with a compelling illustrative example ("The conference, \<mask\> was postponed" → cannot produce "originally planned for March"). These limitations are not widely discussed in this form, and the paper motivates its alternative clearly.

- **Strong planning-task experimental design and results (Section 5.1.1, Table 1).** The star graph progression (easy → medium → hard) is carefully constructed to isolate MDMs' reliance on absolute positions when arm lengths vary. The results are striking: ILM achieves 99.1% on Star_hard where MDM gets 21%, and 100% on Star_medium where MDM gets 36.5%. These large, clean gaps provide the paper's strongest evidence for ILMs' advantages.

- **Effective conceptual exposition (Figure 1).** The three-panel comparison showing actual generation trajectories for ARMs, MDMs, and ILMs communicates the architectural differences efficiently.

## Weaknesses

### Major

- **Unexplained MDM infilling comparison contradicts the paper's own claims (Section 5.3.2, Table 3; Section 2).** The paper prominently states that MDMs have "no flexibility in terms of infilling length" because "the number of masks between any two unmasked tokens is fixed" (line 71-72). Yet Table 3 reports MDM results on single-segment and multi-segment variable-length infilling tasks, with no explanation of how the MDM was adapted to overcome the very limitation the paper argues is inherent. The paper must specify: (a) whether the ground-truth infill length was provided to the MDM (making the comparison unfair), (b) whether a heuristic was used (potentially disadvantaging the MDM), or (c) whether the MDM can in fact handle this setting in some known way. Without this information, the infilling results in Table 3 are uninterpretable and the comparison cannot be evaluated. This is a methodological transparency gap that directly affects the paper's central narrative about MDM limitations.

### Minor

- **Text generation claims are modestly overstated (Abstract, Section 5.3.1, Table 2).** The abstract claims ILMs "perform on par with ARMs" in unconditional text generation. On Stories, the gap is small (ILM 2.14 vs ARM 2.11, +0.03 NLL). On LM1B, the gap is substantial (ILM 4.67 vs ARM 3.94, +0.73 NLL) — ILM is much closer to MDM (4.81) than to ARM. Separately, the Prometheus LLM judge evaluation (Figure 5) shows ILM outperforming ARM on coherence/consistency metrics, which appears to contradict the NLL results. The paper reports both without discussing or reconciling this tension. The results support "competitive with ARMs" (as stated in the introduction and contributions), but "on par" overstates the LM1B evidence, and the NLL/Judge discrepancy merits discussion.

- **The "biased training objective" is acknowledged but never analyzed (Section 3, line 79).** The paper states that to avoid high-variance Monte Carlo estimation, it uses a "biased training objective" that predicts normalized token counts across gaps rather than marginalizing over insertion trajectories. However, it provides no analysis of what this bias is, how large it might be, or under what conditions it distorts the learned insertion policy. While the empirical results suggest the approximation is practically effective, the paper does not characterize the gap between the biased objective and an exact insertion-model loss, leaving the theoretical grounding of the core training loss unclear.

- **The stopping classifier's training signal may not transfer to inference (Section 3, Equation 3).** During training, the classifier learns to detect whether the current subsequence is missing tokens *relative to a known original sequence* (S=1 iff no tokens were dropped). During inference, it must decide whether the *currently generated sequence is semantically complete* without access to any reference. These are different tasks — a sequence could be semantically valid but shorter than some training example, or incomplete despite having no "missing" tokens relative to any reference. The paper does not validate whether the learned stopping behavior correlates with semantic completeness or simply with length statistics from the training data. The empirical lengths in Table 2 are reasonable, but this is not analyzed.

- **Insertion Transformer, the most directly related prior work, is omitted from text evaluation (Section 5.3).** The Insertion Transformer (Stern et al., 2019) is evaluated on planning tasks (Table 1) but not on text generation or infilling. Since ILM is an insertion-based model, comparing against this baseline on the text tasks that matter most for practical application would help isolate whether ILM's specific design choices (count-based objective, separate stopping classifier) provide concrete benefits over the simpler insertion framework.

### Trivial

None.

## Nice-to-Haves

- Analyze the training-objective bias in a small controlled setting (e.g., known bigram statistics) to quantify how the count-based target affects the learned insertion distribution.
- Reconcile the NLL and Prometheus judge results — discuss whether different metrics capture different quality dimensions and why they diverge.
- Analyze the stopping classifier's decisions: do stopping events correlate with semantic completeness or primarily with sequence length?
- Ablate position encoding choices for the MDM experiments (absolute vs. relative) to clarify the claim that MDMs fail on variable-length tasks because of absolute position reliance.

## Removed Points

The following points from the input review were removed with justification:

- **Oracle-ARM zebra puzzle framing (Critical Issue 5, second bullet):** The reviewer claimed the paper's framing is misleading because ILM (90.0%) does not beat the oracle-ordered ARM (91.2%). However, the paper explicitly says ILM "gets close to the performance achieved by the ARM trained on oracle solver decomposed sequence order" (line 180-181). This is transparent and accurate — removed as factually incorrect criticism.
- **Algorithms in appendix (Section-by-Section Notes):** The reviewer noted Algorithm 1 and 2 content is in the appendix. Per policy, the parser strips appendices from all papers; this is not a paper flaw.
- **Notation ambiguity in Equation 2 (Section-by-Section Notes):** The notation $c_{i_k, i_{k+1}}(v; \mathbf{x}) \log p_{\theta, \text{tok}}^{\text{ilm}}(k, v \mid \mathbf{x}[b])$ could be clearer about the implicit sum over $v$, but this is a formatting-level detail that does not affect the method's understandability.

## Novel Insights

None beyond the paper's own contributions. The reviews surfaced the MDM infilling contradiction (the paper argues MDMs can't handle variable-length infilling yet reports MDM results without explanation), which is a real methodological gap, and noted the tension between NLL and Prometheus evaluations that the paper does not address. These are good-faith concerns about presentation and transparency rather than novel analytical insights about the method itself.

## Suggestions

1. **Clarify the MDM infilling setup in detail.** Specify exactly how the MDM was adapted for variable-length infilling — whether ground-truth lengths were provided, a heuristic was used, or a different inference procedure was employed. Without this, the comparison cannot be interpreted.
2. **Calibrate the abstract's text claim.** Replace "perform on par with ARMs" with the more accurate "competitive with ARMs" used in the introduction and contributions. Discuss the NLL/Judge evaluation tension explicitly.
3. **Add a brief analysis of the biased training objective** — either a theoretical characterization of the bias or a small controlled experiment showing its empirical effect.

## Score and Decision

The paper makes a real contribution with the ILM formulation and demonstrates compelling advantages on planning/symbolic tasks where the improvements are large (up to 78 percentage points on Star_hard). The text results are more modest but still show ILM outperforming MDM. The main concern is the opaque MDM infilling comparison, which undermines the paper's central narrative about MDM infilling limitations and must be clarified. The other issues (slight overclaiming, unanalyzed training bias, stopping classifier validation) are addressable. Overall, the method is promising, the planning evidence is strong, and the paper is a meaningful step toward insertion-based generation — but the MDM infilling transparency gap and overclaiming on text results require resolution.

**MY FINAL SCORE:** <score>6</score>
**MY FINAL DECISION:** <decision>Accept</decision>