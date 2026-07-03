Now I have enough to write the final review. Let me anchor:

**Round 1 bracket:** 4–5.5. CoRAL is more complete than WtHKqtHVXo (LLM for contact-rich manipulation, avg 4.0, reject) due to better system design and ablation, but the verified Figure 4 inconsistency undermining RQ3, n=10 evaluations with 2-trial margins claimed as "significant," and misframed VLA comparison keep it below Residual-MPPI (avg 6.25, accept). Final score: **4.0**.

---

## Summary
CoRAL is a modular, neuro-symbolic framework for zero-shot contact-rich robotic manipulation. It decouples VLM-based perception (FoundationPose + GPT-4o for physical parameter estimation) from LLM-based strategic planning (MPPI cost function formulation and contact strategy generation), with nested inner/outer feedback loops for online adaptation and a RAG-based memory unit for experience reuse. The system is evaluated in MuJoCo/ROBOSUITE simulation on six tasks, including custom contact-rich scenarios and LIBERO benchmarks.

---

## Strengths

- **Role-separation ablation is concrete and compelling.** The CoRAL (Unified VLM) variant collapses to near-zero success on all complex tasks (Table 1: 0/10 on T1, T3, T5, T6; 2/10 on T2; 1/10 on T4), while the full system achieves meaningful performance. This directly and specifically validates the paper's central architectural claim that separating VLM perception from LLM planning is critical.

- **Human expert baselines as upper bound.** Including both single-stage and FSM expert-designed MPPI baselines is an informative and unusual choice that situates CoRAL's performance against an engineering ceiling, giving clear context on the gap between zero-shot LLM formulation and carefully tuned task-specific costs.

- **Ablation design is internally coherent.** Each ablation removes exactly one mechanism, and the patterns are consistent: removing pose tracking is catastrophic (0/10 on all but T2), removing refinement collapses multi-stage tasks (T1: 4/10 → 0/10, T3: 10/10 → 3/10), and removing memory uniformly degrades timing and some success rates.

---

## Weaknesses

### Fatal
None.

### Major

- **Figure 4 is visually inconsistent with the text describing the same experiment.** Section 4.1.4 states: *"we intentionally initialized the Evaluation World with a severely overestimated mass (2.0 kg vs. a ground truth of 0.1 kg) and friction coefficient (0.9 vs. 0.5)."* Yet Figure 4's y-axis runs from 0.75 to 1.00 kg, with the initial estimate at 1.00 kg and the corrected value stabilizing near 0.85 kg. Neither the stated 2.0 kg initial value nor the 0.1 kg ground truth appears in the figure; the displayed correction is less than 20%, not the claimed ~20× factor. The text and figure cannot both correctly describe the same experiment. This directly undermines the RQ3 robustness analysis, one of the paper's three evaluation questions, and is verifiable from the manuscript as written.

- **Statistically thin evidence for the memory component and other marginal comparisons.** Every task is evaluated over exactly 10 trials. Key distinctions the paper interprets as meaningful — full CoRAL (4/10) vs. w/o Memory (2/10) on T1; CoRAL (7/10) vs. w/o Memory (5/10) on T6 — differ by 2 trials. With binary outcomes over 10 trials, these gaps are fully consistent with sampling noise. Binomial tests on these pairs yield p-values far above any conventional threshold. Section 4.1.3 characterizes memory as providing a "significant boost" and demonstrating that "CoRAL can learn from its experiences," but neither claim is statistically supported at n=10. No uncertainty quantification or statistical testing is reported anywhere in the paper.

- **The VLA baseline comparison does not support the conclusion drawn.** OpenVLA-OFT and π₀.₅ are evaluated on LIBERO-fine-tuned checkpoints applied to CoRAL's novel MuJoCo environments. Section 4.1.1 concludes that the results show "even fine-tuning an end-to-end policy is **insufficient** for scenarios that demand explicit physical modeling." This is too strong: zero scores on T1/T4/T6 primarily demonstrate out-of-distribution transfer failure — a known limitation of checkpoint reuse — not a fundamental incapacity of the VLA paradigm for contact-rich tasks. The paper explicitly states it uses "the officially released **LIBERO-OBJECT** checkpoint for pick-and-place tasks and the **LIBERO-GOAL** checkpoint for all other tasks," making the transfer gap the primary confounder, not the capacity of the approach.

### Minor

- **Memory evaluation protocol is unspecified.** Section 3.2 describes episodes as being stored upon success, but the 10-trial evaluation protocol is not described: is the memory pre-populated before the 10 trials begin, or accumulated during them? If accumulated, early trials in the w/ Memory condition have no memory while later trials do, making the memory vs. no-memory comparison partially confounded and uninterpretable without trial-order data.

- **Broken cross-reference ("Appendix ??") in Section 4.1.4.** The explainability and failure-recovery discussion concludes with *"The LLM provided a correct natural language diagnosis of a poorly weighted cost function and proceeded to adjust the specific weights to remedy the failure (Appendix ??)"*. The broken reference means the supporting example for the explainability claim is not accessible from the main text, leaving the claim partially unsubstantiated in the main body.

- **LLM-to-executable-cost-code mechanism not described.** Section 3.2 states that the LLM "generates the mathematical structure and relative weights of a cost function" and "is free to introduce any cost terms constructible from the available state." The mechanism for translating this text output into an executable MPPI running cost — whether via structured JSON, free-form code generation, or templated substitution — is not described. Without this, it is unclear whether the LLM is composing genuinely novel cost terms or selecting from a predefined set, which is central to the paper's claim about LLM-driven cost formulation.

### Trivial

- Equation (7): `x_des` is described only as "calculated from real-time sensors" without formal definition, leaving the reactive control formulation underspecified at the notation level.

---

## Nice-to-Haves

- A mechanistic walkthrough of one full LLM → MPPI cost generation cycle (exact prompt, raw LLM output, parsed/executable code, resulting behavior) would directly validate whether the LLM is generating substantive novel cost terms or drawing from a template library.
- The 83.9% speed improvement from LLM-guided contact strategy (Section 4.1.4, Figure 5) is quantitatively compelling; including this figure in the main paper and extending it to additional tasks would strengthen the contact-strategy contribution.
- Real robot experiments on even a subset of tasks would directly address the paper's stated motivation and acknowledged sim-to-real concern.
- Increasing to 20–30 trials, or at minimum including confidence intervals, would allow statistical conclusions to be drawn from the numeric comparisons.

---

## Removed Points

*These points are flagged as removed; treat them with caution.*

- **Simulation-only evaluation as a direct weakness**: The paper explicitly discloses the simulation setting and acknowledges the sim-to-real gap as a limitation. For a methodology paper, requiring real-robot experiments is scope creep. Retained only as a nice-to-have.

- **Eq. (7) K_f choice as a reproducibility gap**: Impedance/PD gain choice is a standard engineering parameter not typically described at this level of detail for papers of this type. Retained only at Trivial level.

- **Introduction claim about "explainability" being overstated**: The claim "significantly enhancing both the explainability…" is a framing choice; ablation studies do show the benefit of role separation. This is not a scientific error and is not retained as a weakness.

- **Unfair VLA comparison (structural)**: The comparison is imperfect in conclusion, but the experimental setup is explicitly disclosed. The flaw is in the *interpretation* of zero-shot transfer failure as fundamental incapacity — this is retained as a Major weakness about the conclusion, not a claim that the comparison is invalid in design.

- **Appendix reference as parser artifact**: The "Appendix ??" is a verifiable manuscript preparation error (not a parser artifact — the text literally contains "??"), so it is retained as a Minor weakness.

---

## Novel Insights

The most substantive insight from the review is the confirmed Figure 4 inconsistency: the described experiment (2.0 kg initial → 0.1 kg true value) and the displayed figure (1.0 kg → 0.85 kg) cannot coexist. This is a verifiable problem that directly undermines the quantitative robustness analysis for RQ3. Combined with statistically thin n=10 evaluations and an unspecified memory protocol, the paper's quantitative conclusions systematically exceed what its evidence supports. The underlying architecture — nested LLM feedback loops grounding into MPPI cost formulation with explicit role separation — is genuinely novel compared to prior VLM-in-the-loop planning work, and the ablation structure is well-designed; the evidential problems are execution gaps, not architectural ones.

---

## Suggestions

1. **Resolve Figure 4**: Ensure the figure and text describe the same experiment with consistent parameter values (initial estimate, true value, converged estimate). If the figure depicts a different setup than the one described in the text, replace or re-caption it.
2. **Clarify memory evaluation protocol**: Specify whether memory is pre-populated before the 10-trial evaluation or accumulated within it, and report trial-order effects if relevant.
3. **Describe the LLM-to-code mechanism**: Specify how LLM text output is parsed into executable MPPI cost code (structured output schema, free-form code, templated generation), as this is central to reproducibility and to the paper's core claim.
4. **Correct statistical language**: Replace "significantly boosted" and similar claims with "directionally improved" or "trending toward improvement" given n=10, or increase trial count to support stronger claims.
5. **Scope the VLA conclusion**: Reframe Section 4.1.1's conclusion from "insufficient for contact-rich tasks" to "fails to zero-shot transfer to out-of-distribution contact-rich scenarios," which is what the evidence actually shows.

---

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| WtHKqtHVXo.md (LLM for contact-rich manipulation) | 4.00 | R1 | Most topically similar; CoRAL has better ablation but similar evaluation thinness and an additional Figure 4 inconsistency |
| iTsHStJKcm.md (LLM zero-shot deformable manipulation) | 5.25 | R1 | Borderline reject; CoRAL's verified figure inconsistency and statistical issues keep it below this range |
| gVnJFY8nCM.md (Residual-MPPI) | 6.25 | R1 | Accept; stronger evaluation rigor and no figure inconsistency — CoRAL falls below this |
| 9pKtcJcMP3.md (Video Language Planning) | 7.00 | R1 | Well above CoRAL's quality bar |
| OI3RoHoWAN.md (GenSim) | 8.00 | R1 | Strong accept, substantially more rigorous than CoRAL |
| I0To0G5J7g.md (Online self-improvement embodied) | 3.20 (labeled wrong) | R1 | More closely aligned reject; CoRAL is marginally better due to clearer architecture |
| uaKBM9sGEm.md (Off-road MPPI) | 4.00 | R1 | Similar score bracket; evaluation-limited MPPI paper |
| qGL6fE1lqd.md (LLMPhy) | 4.40 | R1 | LLM for physical reasoning; similar concerns about evaluation robustness |

**Round 1 bracket:** 4–5.5. The most topically similar paper (LLM for contact-rich manipulation) scored 4.0; CoRAL is more complete architecturally but has a confirmed Figure 4 inconsistency and n=10 evaluations with unsupported "significant" claims. This places it at the low end of the bracket.

**Final score: 4.0** — borderline reject. The architectural idea is novel and the ablation is coherent, but the Figure 4 inconsistency directly undermines RQ3, the statistical evidence cannot support the conclusions drawn about memory, and the VLA comparison conclusions are overclaimed. These are the kind of issues that would require substantial revision to resolve, not rebuttal clarifications.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>