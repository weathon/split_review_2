Now I'll write the final consolidated review.

## Summary

This paper re-evaluates claims that programmatic policies generalize better than neural policies in RL. Through experiments on TORCS, KAREL, and PARKING, it shows that much of the reported gap arises from confounds (reward shaping in TORCS, observability design in KAREL) rather than representational superiority. The paper introduces an expressivity/discoverability framework and then identifies classes of problems—those requiring input-dependent working memory—where programmatic representations offer a genuine advantage, supported by a proof-of-concept using FUNSEARCH to synthesize BFS in Python.

## Strengths

- **Clean identification of the reward-function confound in TORCS (Section 4.1, Table 1).** The paper demonstrates that neural policies trained with β=1.0 crash on OOD tracks because they optimize for speed, while NDPS's programmatic policies are less capable of optimizing speed and therefore generalize. The β=0.5 ablation showing 76% and 69% generalization from G-TRACK-1 cleanly isolates this confound. This is the paper's strongest empirical contribution.

- **The expressivity/discoverability framework (Section 5, Definitions 2 and 3).** Separating "does a generalizing solution exist in the policy class?" (expressivity) from "can the search algorithm find it?" (discoverability) provides useful conceptual clarity. The paper applies this lens effectively to explain why prior comparisons were unfair: both representations satisfied expressivity, but discoverability was only controlled in the programmatic space.

- **The memory-scaling argument (Section 5, lines 290–302).** The observation that feedforward and recurrent networks have fixed capacity and therefore provably cannot represent algorithms with input-dependent memory (BFS, stack-based nested subproblems) is theoretically sound. The information-theoretic argument that "indexing a vertex among |V| candidates requires Ω(log |V|) bits" (line 298) is a clean justification. The connection to Weiss et al. (2018) and Delétang et al. (2023) grounds this in the empirical literature.

## Weaknesses

### Major

None.

### Minor

- **The proof-of-concept (FUNSEARCH + Python) uses a much richer language than the DSLs from the re-evaluated papers, and the paper does not explicitly acknowledge this gap.** Section 5 transitions from discussing the re-evaluated DSLs (which the paper correctly notes "induce spaces similar to those of neural networks," line 284) to arguing that "programmatic representations can produce policies whose memory capacity grows according to the input size" (line 302). This is illustrated with FUNSEARCH synthesizing a Python BFS implementation. However, the TORCS DSL (Figure 1) and KAREL DSL (Figure 2) also cannot express BFS or any memory-scaling algorithm—they lack arrays, queues, or dynamic data structures. The paper never states this explicitly, which creates an unacknowledged gap between the re-evaluation and the proof-of-concept. The paper would benefit from a sentence acknowledging that the DSLs in prior work are similarly limited to neural networks in this dimension, and that the FUNSEARCH demonstration illustrates what *richer* programmatic representations can do. This does not undermine the paper's core thesis (since Section 5 is forward-looking), but the missing acknowledgment weakens narrative coherence.

- **Definition 3 (Discoverability) lacks specificity.** The definition requires existence of an algorithm that returns a generalizing policy "within a bounded time limit" (line 282), but no bound is specified. Without one, the definition is nearly vacuous—any finite hypothesis space is discoverable with a sufficiently large bound. The paper uses discoverability qualitatively (post-hoc explanation) rather than as a formal tool, so this is not a fatal flaw, but greater precision would strengthen the framework.

- **The KAREL re-evaluation compares against a different architecture than the original work (Section 4.2, Table 2).** Trivedi et al. (2021) tested PPO with ConvNet (full observability) and PPO with LSTM (partial observability). The paper's "PPO with a_{t-1}" (feedforward network with last-action augmentation) is a genuinely different baseline not tested in the original work. The result is valuable—it shows a simple neural architecture that also works—but the framing as correcting an "unfair comparison" is slightly imprecise; the original papers did not test this architecture. The paper would benefit from acknowledging this distinction.

### Trivial

- **Limited engagement with the neural algorithmic reasoning literature.** Given that the memory-scaling argument is a core contribution, the paper only briefly mentions stack-RNNs and neural Turing machines (line 312) without engaging with work on neural execution of algorithms (e.g., the CLRS benchmark, or broader work on algorithmic reasoning with neural networks). Situating the memory-scaling argument within this literature would strengthen the framing.

## Nice-to-Haves

- The paper notes that NDPS's programmatic policies produce slower cars. An experiment running NDPS with a neural oracle trained on β=0.5 would cleanly test whether NDPS's generalization is solely attributable to producing slower policies.
- A characterization of what properties a DSL needs (arrays? recursion?) to support memory-scaling solutions would make the Section 5 contribution more actionable.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **PROPEL results are absent (Critical Issue 2 from Harsh Critic).** The paper claims to re-evaluate "Verma et al. (2018) and Verma et al. (2019)" on TORCS (line 195) and references Appendix B for additional details. Since the appendix is stripped by the parser, the presence of PROPEL re-evaluation results in the original submission cannot be verified. Per policy, this criticism is removed as it relates to potentially missing appendix content.

- **Abstract is "close to tautological" (Section-by-Section note).** This is a judgment about framing, not a specific verifiable weakness. The framework's value is in application, not definitional novelty.

- **Example 2 assumes BFS correctness (Section-by-Section note).** This is a standard illustrative example; the paper's formal framework already handles POMDPs.

- **Zero standard deviation in Table 2 suggests the problem is easy (Section-by-Section note).** This is an observation about results, not a weakness; zero std on a 1.00 success rate simply indicates consistent success across seeds.

- **The paper "should run NDPS with β=0.5 reward" (Strengthening section).** This is a nice-to-have experiment, not a weakness of the current paper.

- **The paper should "engage with neural algorithmic reasoning literature" (from Strengthening section).** Addressed in the Trivial section above in a milder form.

- **Missing related works.** Removed per policy; no external sources to verify existence.

- **Formatting/style nitpicks.** Removed per policy.

## Novel Insights

The most novel insight from the review process is that the paper's two halves—the confound-driven re-evaluation and the memory-scaling argument—are disconnected in a way that the paper does not adequately address. The proof-of-concept uses Python (a general-purpose language), while the re-evaluated DSLs are highly restricted and cannot implement the algorithms the proof-of-concept demonstrates. This creates an implicit narrative gap: the paper shows that prior comparisons were confounded, then pivots to argue for the value of programmatic representations on entirely different problems using an entirely different language. Recognizing and bridging this gap would substantially strengthen the paper's coherence.

## Suggestions

- Explicitly acknowledge that the DSLs used in the re-evaluated papers (NDPS, LEAPS, PSM) also cannot implement memory-scaling algorithms, and reframe the proof-of-concept as illustrating what *richer* programmatic representations can do (not as a continuation of the same comparison).
- Tighten Definition 3 by either specifying a concrete resource bound or clarifying that discoverability is used qualitatively.
- Add one sentence acknowledging that the PPO with a_{t-1} baseline in KAREL is a novel design not tested in the original work.

## Score and Decision

**Round 1 bracket:** (4.0, 6.5) — based on calibration against 19 anchors.

**Anchor comparisons:**

| Anchor Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/.../Uj0h13lVrR.md` | 1.00 | R1 (strong reject) | GFlowNets paper with major flaws; our paper is clearly stronger |
| `/home/wg25r/split_review_opus_repro/.../fvTaoyH96Z.md` | 2.33 | R1 (reject) | RL generalization paper with limited experiments; ours is stronger empirically |
| `/home/wg25r/split_review_opus_repro/.../NGVljI6HkR.md` | 3.67 | R1 (borderline) | Directly relevant (programmatic policies); ours has broader scope and more experiments |
| `/home/wg25r/split_review_opus_repro/.../lUWf41nR4v.md` | 4.50 | R1 (borderline) | Program synthesis + state machines; ours has stronger confound identification |
| `/home/wg25r/split_review_opus_repro/.../iMI4HRpZFc.md` | 5.25 | R1 (borderline) | RL delusions paper; comparable scope and significance |
| `/home/wg25r/split_review_opus_repro/.../ehSQZa4vuk.md` | 5.25 | R2 (narrow) | Policy confounding paper; similar structure (identify confound + framework); our experiments span more domains |
| `/home/wg25r/split_review_opus_repro/.../PH7ja3T0vN.md` | 4.50 | R2 (narrow) | Combinatorial generalization; less directly comparable |
| `/home/wg25r/split_review_opus_repro/.../X1p0eNzTGH.md` | 5.67 | R2 (narrow) | Level sampling for generalization; strong theory but debated; ours has more direct empirical contribution |
| `/home/wg25r/split_review_opus_repro/.../tErHYBGlWc.md` | 6.80 | R1 (accept) | Actor-critic representation study; stronger theory but different scope |
| `/home/wg25r/split_review_opus_repro/.../jOmk0uS1hl.md` | 8.00 | R1 (strong accept) | LLM evaluation confounds; cleaner execution and broader implications; our paper is not at this level |

**Round 2 narrowing:** The paper sits between the "Bad Habits" confound paper (5.25) and the stronger accept papers (6.8+). It has cleaner experiments than the former but a less coherent narrative than the latter. The disconnection between the confound re-evaluation and the memory-scaling proof-of-concept prevents the paper from reaching the 6.5–7+ range.

**Final score:** 6.0 — The paper makes a genuine contribution by identifying and experimentally demonstrating confounds in influential prior work, and the memory-scaling argument is theoretically sound. However, the narrative disconnection between the re-evaluation and the proof-of-concept limits its impact. With explicit acknowledgment of the DSL expressivity gap and tighter definitions, this could be a 7+ paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>