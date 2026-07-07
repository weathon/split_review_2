## Summary

Atomos is a training-free test-time reasoning framework that decomposes complex problems into "atomic steps," executes each within a propose-verify-retry self-checking loop (using the same base model as verifier), and allocates compute along two orthogonal axes: world sampling (breadth) and path sampling (depth). The paper derives two "Reliability Laws" governing the cost-reliability trade-off and offers a single case study — an autonomous solution to IMO 2025 Problem 6 — as empirical validation.

---

## Strengths

- **Conceptually clean architecture.** The separation of planning from execution, the propose-verify-retry loop, and the formalization of two compute axes (world vs. path) provide a principled vocabulary for analyzing test-time reasoning that goes beyond heuristic prompting schemes.

- **Law 2 (polylogarithmic cost of reliability) is non-trivial.** The claim that achieving extreme reliability scales only polylogarithmically in 1/δ (rather than polynomially) is a genuinely useful insight for practitioners and provides motivation for reliability engineering at inference time.

- **IMO 2025 P6 as a demonstrator.** Solving a current-year IMO problem (P6, the hardest) provides a memorable, concrete demonstration of what the framework is capable of at the frontier of creative mathematical reasoning.

---

## Weaknesses

### Fatal

1. **Empirical validation is a single anecdote.** The entire experimental section consists of one case study on one problem. There are no quantitative results on any benchmark (MATH, AMC, AIME, GSM8K, etc.), no ablations varying the retry budget R or the number of worlds N_w, and no comparison to baselines using the same total compute. The tables (Tables 1–3) are purely qualitative "Atomos says X vs. Standard CoT says Y" descriptions with no statistical grounding. For a method paper claiming quantitative reliability laws and "predictable accuracy–compute trade-offs across benchmarks," the complete absence of such cross-benchmark results is a fatal evidentiary gap.

2. **Correctness of the IMO 2025 P6 solution is not independently verified.** The paper asserts the model produces a correct proof, but correctness is assessed entirely by the same model acting as its own verifier — the very mechanism whose reliability is under scrutiny. No external verifier (e.g., a formal proof assistant, a human mathematician, an independent oracle) confirms the proof. This makes the headline result unverifiable and potentially circular.

3. **The framework is underspecified to the point of being irreproducible.** The paper never specifies: (a) how atomicity is determined — what criterion decides that a subproblem is "safely within the model's reliable operating zone"; (b) the exact prompt structure for the planning phase vs. execution phase; (c) how the dependency graph is represented and traversed; (d) what the verification prompt looks like and how pass/fail is decided. The system exists essentially as a narrative without an algorithm.

### Major

4. **Law 1 is nearly tautological.** The "depth-return factor α" is defined implicitly as the exponent in a power-law return function q(C_p) ∝ C_p^α. The result C_p* = αC is then a routine application of Lagrange multipliers to that power law. Since α characterizes the return function by assumption, the law reduces to "use the fraction of the budget equal to the elasticity of the return function." No guidance is given for how to measure α in practice, making the law descriptive rather than prescriptive.

5. **The verification-asymmetry assumption is asserted but never empirically demonstrated.** The claim c_ver ≪ c_gen (Eq. 5) is central to the framework's feasibility — if verification is expensive, the retry loop is not cheap and the polylogarithmic cost bound may not hold. For hard mathematical reasoning (like IMO problems), the paper's own trajectory shows the verifier often produces multi-page critiques. No token-count comparison is provided.

6. **The Kolmogorov complexity motivation (Section 2.2) is unfalsifiable as stated.** The Unitary Reasoning Complexity C_u(s_i) = K(s_i | s_{<i}) / |s_i| and the threshold Λ_max are uncomputable and never operationalized. The "proxy" (length of the most compressed instruction for an oracle LLM) is informal and unmeasured anywhere in the paper. This section is motivational rhetoric rather than a rigorous theoretical foundation that the later laws are derived from.

### Minor

- Law 2 requires independence of step errors across the reasoning chain, an assumption that is not discussed and is violated when earlier errors affect the context of later steps.
- The isoperformance curves that Law 1 predicts (straight lines in log space) are claimed to be empirically validated in the abstract ("across benchmarks, consistent with the theory") but no such curves are shown in the paper.

### Trivial

None beyond the above.

---

## Nice-to-Haves

- Quantitative experiments on standard math benchmarks (AIME 2024/2025, MATH-500) with varying world budget and path budget to empirically validate the predicted isoperformance curves.
- A token-level breakdown comparing generation cost vs. verification cost per atomic step to empirically ground the verification-asymmetry claim.
- A concrete algorithmic description (pseudocode) of the planner, executor, and verifier components.
- Independent human or formal-system verification of the IMO P6 proof.

---

## Novel Insights

The framing of test-time compute allocation as a two-dimensional optimization problem (world breadth vs. path depth) and the resulting polylogarithmic scaling of reliability cost with 1/δ is a genuinely useful conceptual contribution. If empirically validated, the insight that near-perfect reliability is "surprisingly affordable" in compute terms would be influential. However, these insights remain theoretical constructs without the experimental grounding needed to confirm that they describe real model behavior rather than idealized assumptions.

---

## Suggestions

- Run quantitative experiments on at least AIME 2024 and MATH-500, reporting accuracy as a function of total compute budget for multiple (N_w, R) configurations, and show that the isoperformance contours are indeed linear in log space.
- Either remove the Kolmogorov complexity framing (Section 2.2) or replace it with an empirically measurable proxy (e.g., per-step token consumption as a proxy for complexity density) and show the threshold Λ_max can be calibrated per model.
- Provide a formal definition of "atomic": a machine-checkable criterion (e.g., the verifier can assess correctness within K tokens) rather than the intuitive "within the model's reliable operating zone."
- Have the IMO P6 proof checked by a formal system or published mathematician before claiming it as a solved grand challenge.

---

## Score and Decision

The paper presents a conceptually interesting framework with a memorable headline result, but the empirical section is essentially absent (one qualitative case study), the core framework is too vague to reproduce, the theoretical laws are partially circular or untested, and the headline IMO result is unverified externally. These are not minor polishing issues; they concern the paper's basic evidentiary standards as a method contribution. The idea deserves development into a complete paper.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>