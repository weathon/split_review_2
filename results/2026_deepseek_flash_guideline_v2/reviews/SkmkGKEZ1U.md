# Final Review: O-Forge: An LLM + Computer Algebra Framework for Asymptotic Analysis

## Summary

O-Forge proposes a framework that combines a frontier LLM (to propose domain decompositions) with Mathematica's `Resolve` function (to verify inequalities in each subdomain) for proving asymptotic inequalities. The paper presents two research-level case studies motivated by Terry Tao and claims the system is "remarkably effective." However, the paper provides no evidence that the tool actually works as a system, and the implementation section contains placeholder content, making this an incomplete submission that does not support its core claims.

## Strengths

1. **Well-motivated problem.** Proving asymptotic inequalities is a genuine bottleneck in analysis and analytic number theory. The paper correctly identifies the "divide-and-conquer via domain decomposition" strategy that mathematicians use and frames it as a natural target for AI assistance. The connection to Terry Tao's public comments adds context.

2. **Meaningful contrast with prior work.** The paper identifies a real capability gap: Tao's Lean-based `linarith` tool handles only linear estimates, and SMT solvers (CVC5, MetiTarski) struggle with transcendental functions (the paper reports they fail on `log x ≤ log y ⇒ exp(x) ≤ exp(y)`). This positions the work within the broader AI-for-math landscape.

3. **Two non-trivial case studies.** The inequality `xy ≪ x log x + e^y` and the series estimate from analytic number theory are genuine research-level examples where the decomposition strategy works in principle. The paper shows the mathematical reasoning behind the splits.

4. **Transparency about limitations.** Section 7 acknowledges that `Resolve` does not emit externally verifiable proof objects and requires trust in Wolfram's closed-source implementation — an honest admission.

## Weaknesses

### Fatal
None. The conceptual approach (LLM proposes, CAS verifies) is not fundamentally flawed; the paper fails on execution and evidence, not on theoretical invalidity.

### Major

1. **No empirical evidence that O-Forge actually works as a system.** This is the paper's single most serious problem. For a submission that presents itself as a tool paper, the absence of any demonstration is structural:
   - The two case studies in Section 3 are presented as human-written mathematical narratives. Nowhere does the paper show the actual LLM output, the Mathematica input/output, or confirm that the O-Forge pipeline completed these problems. The paper says "we delegate the task of guessing the correct decompositions to frontier LLMs...which do a commendable job" (line 132) but provides no evidence the LLM actually proposed these splits.
   - The "empirical evaluation" in Section 5 claims "an extensive suite of around 40-50 easier problems" but reports **zero quantitative results** — no success rate, no timing data, no failure analysis, no comparison with baselines, no tables, no metrics. The only examples given are `350 ∑ 1/n^p ≪ 1` (p > 1) and `∑ r^n ≪ 1` (|r| < 1), which are first-year calculus exercises.
   - The paper asserts that O-Forge is "remarkably effective" (abstract) and "robust" (line 281), but these claims are unsupported by any data. A tool paper must demonstrate that the tool works on concrete problems.

2. **Section 4 (Implementation) contains placeholder content.** The prompt template (lines 199–224) shows empty XML tags with only dashes as content:
   ```
   <guiding_principles> - </guiding_principles>
   <task> - </task>
   <requirements_for_breakpoints> - </requirements_for_breakpoints>
   ```
   The Mathematica code snippet (lines 229–236) is a fragment that cannot execute as shown. Line 43 contains the literal note `(\*\* describe the structure of the prompt\*\*)`, which appears to be a reminder to the authors. These are not parser artifacts — they indicate the submission is an incomplete draft.

3. **The LLM's role is unsubstantiated.** The paper provides no evidence that the LLM actually produced the specific decompositions shown, nor any ablation to quantify what the LLM adds. For Case Study 2, the paper admits that LLM suggestions were "sporadic" and unreliable (line 165) and that the decompositions are "natural" to a trained analyst (line 153). Without baselines (e.g., user-provided split, heuristic split, random split), the claimed novelty of "LLM-proposed decomposition" remains an assertion. The paper also does not identify which specific LLM version was used beyond naming "Gemini and ChatGPT" once — version, temperature, and prompt strategy are absent.

### Minor

1. **"In-Context Symbolic Feedback loop" is an overclaim.** The abstract uses this term, but the actual pipeline (Figure 1, lines 97–104) is linear: LLM proposes once → CAS checks each subdomain. There is no iteration, no feedback from the CAS back to the LLM. The paper explicitly states "we only prompt the LLM once in the entire process" (lines 169–173). The "feedback" framing should be removed or the system should implement a genuine refinement loop.

2. **Quantifier elimination claims need qualification.** The paper repeatedly states that `Resolve` verifies via "quantifier elimination over the reals" for formulas involving log and exp (lines 43, 89, 141, 189, 311, 323). True quantifier elimination over the reals (e.g., via cylindrical algebraic decomposition) is a complete decision procedure only for the first-order theory of polynomial inequalities. Whether the real exponential field (ℝ with +, ×, exp) is decidable is a famous open problem. Mathematica's `Resolve` likely uses heuristic, numerical, or special-case methods for transcendental functions — but the paper does not clarify this, nor does it discuss what guarantees (if any) `Resolve` provides in such cases. The paper's footnote (line 89) hedges with "can often decide," which is at odds with the confident statements elsewhere.

3. **Grid search for C is not explained in context.** Step 4 (lines 81–87) describes searching over a discrete grid for the constant C (1 to 10^4). It is unclear how this grid search interfaces with `Resolve`'s claimed quantifier elimination: does the system call `Resolve` separately for each candidate C? How is the grid resolution determined?

### Trivial

- The paper says "we tested our tools" (line 256) but reports none of the test results beyond qualitative observations.
- Figure 1 is referenced in the text but the image is rendered as a broken placeholder `(2fa4a1bf91d0f34e87c689fbc1211fe3_img.jpg)`.
- The claim that "all the examples that we tested were completed for C ≤ 2" (line 87) is stated without any list of what those examples were.

## Nice-to-Haves

- A proper benchmark of 50–100 inequalities with success rates, failure modes, and runtime, including a breakdown by problem difficulty.
- A baseline comparison where the decomposition is provided by the user or a simple rule-based heuristic, to isolate the LLM's contribution.
- Implementation of a genuine feedback loop: if `Resolve` returns False on a subdomain, feed that information back to the LLM to refine the decomposition.
- Clarification of what mathematical guarantee `Resolve` actually provides for non-polynomial constraints.

## Removed Points

These points from the inputs were filtered per the review guidelines; they should be treated with caution and not factored into the overall assessment:

- **Reproducibility concerns about code/website existence**: The paper cites an anonymized repository and o-forge.com. Per rules, these are assumed to exist; questioning their availability is not a valid criticism.
- **Claim that "the paper was submitted in an incomplete state"**: The placeholder content observation is kept (Major #2), but the characterization of the submission status is removed as it is an unsupported inference beyond the observed facts.
- **Claim that the SMT comparison is "trivial" or insufficient**: The paper's claim about CVC5/MetiTarski is a stated experimental result; dismissing it without counter-evidence is not a valid weakness.
- **Claim that the decomposition in Case Study 1 is "obvious"**: This is subjective and contradicted by the paper's contextualization; not a valid technical criticism.
- **Formatting/style nitpicks and parser artifacts**: Removed per rules.
- **Missing related work**: Cannot be verified; removed per rules.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no observations that the paper itself does not already contain or imply.

## Suggestions

1. **Run O-Forge on both case studies and report the results verbatim.** Show the exact LaTeX input, the LLM's proposed decomposition (including failed attempts), the Mathematica input/output for each subdomain, and the overall proof status with multiple trials to assess reliability.
2. **Fill in the placeholder content in Section 4.** The prompt template, code snippet, and CLI example should contain actual, runnable content.
3. **Construct a proper benchmark.** Test on ≥50 problems of varying difficulty, report success rates, failure modes, runtime, and number of LLM calls. Include baselines.
4. **Clarify the verification mechanism.** Explain what Mathematica's `Resolve` does when transcendental functions appear, and what guarantee the user should infer from a "True" return.
5. **Either implement a genuine feedback loop or remove the "feedback" framing** from the abstract and title.
6. **Specify exactly which LLM model, version, temperature, and prompt strategy was used.**

## Score and Decision

The calibration search was unable to retrieve anchor papers due to a directory access issue. Absent external anchors, I calibrate against the ICLR scoring guidelines directly.

The paper identifies a real and well-motivated problem, and the conceptual "LLM proposes, CAS verifies" framework is sound. However, for a paper presenting a tool, the complete absence of empirical evidence that the tool works is a decisive weakness. The placeholder content in Section 4 (empty prompt template, broken code snippet, author note `(\*\* describe the structure of the prompt\*\*)`) confirms the submission is an unfinished draft that does not meet the evidentiary bar for a conference publication. The core claims — that O-Forge is "remarkably effective" and "robust" — are asserted but never demonstrated.

A paper at this tier of incompleteness and missing evidence clearly falls in the **reject** range. It is not a "strong reject" (1) because the underlying idea and case studies have merit, but it is below the borderline.

**Score: 3 (Reject)**

**Decision: Reject**

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>