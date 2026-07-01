Now I have all the evidence I need. Here is the final consolidated review.

---

## Summary

MermaidFlow proposes using Mermaid, a declarative graph markup language, as an intermediate representation for agentic workflows, separating graph-level planning from code-level execution. The paper argues that this representation enables static verification and safe evolutionary search via constraint-preserving graph operators (node substitution, edge rewiring, crossover, etc.), leading to more reliable workflow generation. Experiments across GSM8K, MATH, HumanEval, and MBPP show consistent (if sometimes small-margin) improvements over baselines including AFlow, MaAS, and ADAS, with a reported >90% success rate in producing valid executable code versus ~50% for AFlow's direct code editing.

---

## Strengths

1. **Well-motivated and concrete problem diagnosis.** Sections 1–2 identify a genuine limitation: existing agentic workflow systems encode plans in imperative Python or loose JSON where validity can only be tested at runtime, making search brittle. The paper grounds this in recent studies (Cemri et al., 2025; Zhang et al., 2024a, 2025c) and the diagnosis is specific, not generic.

2. **Principled separation of planning from execution.** Representing workflows as Mermaid declarative graphs (typed nodes with I/O signatures, role-labeled edges) cleanly separates graph-level planning from code-level implementation. Figure 1 makes this concrete with real Mermaid code. This separation is not merely aesthetic—it enables graph-level operations (node substitution, edge rewiring, subgraph replacement) that would be harder to define and verify on Python ASTs or token sequences directly.

3. **Practically meaningful improvement in generation reliability.** The reported >90% success rate in producing valid Python code from Mermaid, versus ~50% for AFlow's direct code editing (Section 5.3), is a concrete operational advantage. Even if benchmark score gains were smaller, this reliability improvement would be valuable for practitioners who deal with debugging invalid generated code during search.

4. **Consistent directional improvement across all four benchmarks (Table 1).** MermaidFlow achieves the best result on every benchmark without exception. The ablation showing that better optimization LLMs yield better outcomes (Table 2) further supports that the method's improvement is real rather than an artifact of a specific LLM choice.

---

## Weaknesses

### Fatal
None.

### Major

1. **Overclaimed "static verification" guarantee conflates Mermaid's syntax validation with the authors' custom semantic checker.** The paper repeatedly states that MermaidFlow offers "compiler-verifiable" (line 98), "built-in static verifiability" (line 50), and "guaranteed valid by construction" workflows (line 30), attributing these properties to Mermaid's syntax. However, the standard Mermaid parser validates syntax (graph rendering) but does *not* enforce the paper's type compatibility, role consistency, or I/O format constraints. The paper acknowledges on line 136 that "when using an LLM to generate a new Mermaid graph, the resulting Mermaid code may sometimes violate predefined safety constraints. To address this, we implement a checker." The verifiability guarantee thus depends on this custom checker and the correct design of the type system—not on Mermaid's compiler. The framing (e.g., line 90: "automatically enforced by Mermaid's parser and extended structural schema") suggests a tighter guarantee than the paper actually demonstrates. Readers cannot assess whether the checker is complete or has edge cases without a full description or analysis.

2. **Benchmark results lack variance reporting, making small-margin improvements uninterpretable.** Table 1 reports "results averaged over three runs" but provides no standard deviations, confidence intervals, or significance tests. On MBPP, MermaidFlow scores 82.31% versus MaAS at 82.17%—a margin of 0.14 percentage points. On GSM8K, the margin over MaAS is 0.92 points. Without variance estimates, it is impossible to determine whether these differences reflect genuine improvement or random variation, especially since all methods use the same base LLM. This is a straightforward omission that should be addressed.

3. **The LLM-as-judge selection mechanism is completely unvalidated.** Section 4.2 describes using an LLM to score candidates "based on semantic fit, structure, and task relevance" to avoid "expensive rollout-based evaluation." Only the highest-scoring candidate is actually executed. The paper provides no analysis—not even a simple correlation study—showing that the LLM judge's scores correlate with actual execution performance. If the judge systematically favors certain structures (e.g., more ensemble nodes, longer pipelines) that do not correspond to real quality, the search could waste iterations on superficially appealing but poor workflows. This is a central methodological component and its reliability should be established.

4. **The comparison with AFlow conflates two independent changes (representation + search algorithm).** MermaidFlow differs from AFlow in both the workflow representation (Mermaid graphs vs. Python code) *and* the search algorithm (evolutionary programming vs. MCTS with LLM code editing). The experiments never isolate these factors—for example, EP on Mermaid graphs vs. EP on Python code, or MCTS on Mermaid graphs vs. MCTS on Python code. Without such an ablation, it is unclear whether improvements come from the representation, the search algorithm, or their interaction. This is particularly important given that MermaidFlow's core claim is about the benefits of the representation itself.

### Minor

5. **Token efficiency comparison is selectively reported.** The paper states MermaidFlow uses "only about half the cost of AFlow" (2.7e4 vs. 6.9e4 tokens) when both "surpass 52% on the MATH dataset" (Section 5.3). This measures tokens consumed *up to the point of first reaching 52%*, not total cost over the full search. Since MermaidFlow reaches higher final accuracy (55.42% vs. 52.81%), total cost over 20 iterations could be comparable or higher. The paper does not report total token consumption or API cost per full run.

6. **Several experimental setup details are unclear.** (a) Different iteration counts are used for different methods (20 for AFlow and MermaidFlow, 30 for ADAS—line 168) without justification. (b) The MATH subset selection criteria are mentioned as following AFlow and MaAS but the exact problem IDs are not given. (c) The validation split used for LLM-as-judge scoring is not specified—is it the same as the training set? (d) The claim that AFlow has "only a 50% success rate in generating executable code" (Section 5.3) is presented without a source or measurement protocol—is this from the AFlow paper, the authors' reimplementation, or a single observation?

7. **The optimal stopping point analysis (Table 3) is limited.** It reports only the round index at which the best workflow was found, not the performance at that round or the stability of scores across rounds. Calling this an "optimal stopping point" analysis is misleading since no stopping policy is evaluated.

8. **The formalization of the search space ($\mathcal{S}$) is underspecified.** Equation (2) defines $\mathcal{S} = \{G[\mathcal{V}, \mathcal{E}, \mathcal{C}] \in \mathcal{G}_{\text{Mermaid}} \mid G \models \mathcal{C}_{\text{static}}\}$, but $\mathcal{C}_{\text{static}}$ is described only through examples ("type compatibility, role-consistent edges, and connectivity," line 90) rather than formally defined. Lemma 1's claim of transformation invariance depends on $\mathcal{C}_{\text{static}}$ and the operators correctly implementing its constraints, which cannot be verified from the description given.

### Trivial
None.

---

## Nice-to-Haves
- An ablation that isolates representation from search algorithm (e.g., EP on Mermaid graphs vs. EP on Python code).
- Validation of the LLM-as-judge scoring mechanism (e.g., correlation between judge scores and actual execution scores on a sample of candidates).
- Reporting of total token consumption, wall-clock time, or API cost per full run, not just at a partial convergence point.
- A formal definition of $\mathcal{C}_{\text{static}}$ so that the closure claim can be assessed.

---

## Removed Points
- **"First to guarantee static correctness" claim is "overwrought" (from Section-by-Section Notes).** The reviewer asserts that GPTSwarm, MaAS, and FlowReasoner "represent workflows as graphs, some with type-like constraints," but does not establish that any of these systems *guarantee* static graph-level correctness. The paper qualifies its claim with "to our knowledge," and the reviewer provides no evidence contradicting it. *Removed due to lack of evidence.*
- **"The operators are standard graph edit operations—not novel contributions."** The paper does not claim novelty in the operators themselves; the claimed novelty is applying them within the Mermaid type system. This observation is accurate but not a weakness of the paper. *Removed as not a valid weakness.*
- **"Characterization of prior work as lacking formal semantics is self-serving."** The paper specifically says prior approaches "lack formal semantics, e.g., no type enforcement, role validation, or support for systematic search" (line 44). This is a concrete claim about specific missing properties, not a generic dismissal. *Removed as inaccurate characterization of the paper.*
- **Criticism about Appendix A.1 being "stripped."** The parser strips appendix content from all papers; the appendix exists in the original submission. *Removed per hard rule.*

---

## Novel Insights
None beyond the paper's own contributions.

---

## Suggestions
1. **Calibrate the verifiability claims.** Distinguish clearly between what Mermaid's syntax guarantees (well-formed graph notation) and what the custom checker enforces (type compatibility, role consistency). Describe the checker's rules, either in the main text or the appendix, so reviewers can assess its correctness and completeness.
2. **Add variance estimates** (standard deviations or bootstrapped confidence intervals) for all main results in Table 1 and for the learning curves in Figure 3.
3. **Validate or replace the LLM-as-judge mechanism.** Either show that judge scores correlate with actual execution scores, or switch to a simpler, auditable selection strategy (e.g., random sampling, round-robin).
4. **Run an ablation isolating representation from search.** The simplest version: apply the same EP search to Mermaid-represented workflows and to Python-represented workflows (the latter using the EP operators adapted for AST-level editing). This directly tests whether the representation drives the gains.
5. **Report total cost.** Provide total token consumption and estimated API cost for a full run of each method.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>