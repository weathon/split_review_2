## Summary

This paper introduces a deletion-based probing framework that intercepts chain-of-thought (CoT) scratchpads mid-generation, removes tokens, and measures downstream effects on physics reasoning. Evaluating three open-source LLMs (Phi-4, Qwen-A3B, Magistral) across three physics benchmarks, the paper finds that models maintain accuracy under 40–60% CoT deletion by "cramming" reconstructed reasoning into final answers, and uses information overlap metrics to analyze how deleted content reappears. The work contributes a novel deletion methodology and reveals interesting behavioral patterns, but its central claims about "unfaithful" reasoning outstrip what the experiments can cleanly establish.

## Strengths

- **The physics-aware deletion strategy is a well-motivated and novel methodological contribution.** Selecting domain-relevant tokens (equations, constants, unit conversions) for targeted deletion leverages the structure of physics problems and distinguishes this work from prior generic deletion studies of CoT faithfulness (e.g., Lanham et al. 2023). The finding that physics-aware deletion produces a more gradual accuracy decline but sharp cramming spikes at 70–80% deletion is the paper's most distinctive empirical observation. (favorability=14.99)

- **Multi-model, multi-dataset evaluation provides meaningful breadth.** Testing three model families (Phi-4, Qwen-A3B, Magistral) across three physics benchmarks of varying difficulty (UG Physics, PhyBench, PhysReason) offers a reasonable basis for the behavioral patterns reported. The consistent "X-shaped" pattern in answer length (rising as CoT length declines) across models and datasets gives the cramming observation more weight than a single-model study would. (favorability=11.46)

- **The problem framing is clear and well-motivated.** The paper makes a coherent case that reasoning faithfulness matters specifically for AI-for-Science, and that physics provides a stringent testbed because of its structured, verifiable content. The distinction between accuracy-based evaluation and faithfulness evaluation is appropriately emphasized. (favorability=11.29)

## Weaknesses

### Fatal

None.

### Major

- **The paper's central interpretive claim that deletion sensitivity reveals "shallow and opportunistic reliance on CoT" (Abstract) is not cleanly separated from the plausible alternative: that CoT contains substantial redundancy.** The paper explicitly acknowledges that CoT traces are "simultaneously informative and redundant" (Section 4.3, line 198), which partially addresses this concern. However, the stronger framing—that results "raise concerns about faithfulness as evidence of reasoning" (Conclusion)—goes beyond what the deletion experiments alone establish, because a faithful reasoning process can have redundant steps that are safely deletable. A faithful model that has internalized the relevant physics could skip redundant derivation steps and still produce the correct answer, just as a human physicist could. The paper's claim that this reveals *unfaithfulness* requires a finer-grained decomposition (e.g., which specific types of steps cause accuracy collapse when deleted) than the current aggregate analyses provide. (favorability=3.97)

- **The information overlap analysis relies on bag-of-words metrics (Jaccard similarity and Manhattan distance) that are too coarse to support the stronger faithfulness claims.** These metrics capture vocabulary-level reuse but cannot distinguish between (a) genuine reconstruction of the deleted reasoning content and (b) generation of a plausible answer that uses the same thematic physics vocabulary (e.g., F, m, a, force, mass, equation, solve) but different derivational steps or numerical values. The paper partially acknowledges this by describing the overlap as "surface-level similarity" (Section 4.2, line 192), but the faithfulness argument leans heavily on these metrics without structure-aware matching (e.g., equation parse trees, numerical value overlap, operator matching) that could separate vocabulary-level overlap from actual reasoning content recovery. (favorability=-0.18)

### Minor

- **The LLM-as-judge evaluation (Claude-4 Sonnet) is used as the primary scoring metric without reported human validation or inter-annotator agreement.** Given the paper's central theme of questioning LLM reasoning faithfulness, relying on another LLM as the authoritative judge—with no evidence of calibration against human judgment—creates an ironic methodological gap that readers will notice. The paper would benefit from at least a small-scale human evaluation (e.g., 50–100 scored answers) to validate the judge's reliability. (favorability=1.33)

- **The practical suggestion that "early stopping of CoT generation may provide a cost-effective way to save tokens" (Section 4.3, line 204) is not directly supported by the experiments**, which delete tokens *after* generation rather than stopping generation early. Whether a model prompted to generate a shorter CoT would behave identically to having its full CoT truncated post-hoc is an open empirical question that the paper does not address. (favorability=3.89)

- **The information overlap analysis does not include a no-deletion baseline.** While the paper's method of measuring overlap between deleted CoT content and the regenerated final answer is reasonable in design, reporting the general lexical overlap between the original (undeleted) CoT and the final answer at 0% deletion would contextualize whether the observed increase under deletion is meaningful or reflects regression toward a naturally high baseline (both CoT and answer describe the same physics problem using a constrained vocabulary). (favorability=5.19)

### Trivial

None.

## Nice-to-Haves

1. Include structure-aware matching for the overlap analysis: match equations by parse structure, numerical values by equality within tolerances, and unit expressions by canonical form.
2. Conduct a control experiment where models are prompted to generate shorter CoT directly, testing the early-stopping suggestion.
3. Provide a more detailed description of the CoT interception mechanism (how token positions are mapped and how the deletion boundary is detected).

## Removed Points

- **Critic's concern that the paper does not describe the technical implementation of CoT interception:** This is a reasonable implementation detail request but falls under trivial reproducibility territory and is not central to the paper's claims.

- **Critic's note about calibration on 50 questions being small:** The calibration analysis is a secondary check, not a main result, and the paper reports confidence intervals. This is within acceptable practice for a convergence analysis.

- **Critic's point that from-the-end deletion means early tokens carry disproportionate weight:** This is an inherent property of that deletion strategy; the paper also tests random and physics-aware deletion, providing complementary evidence across strategies.

- **Critic's concern about the scoring rubric interacting with deletion experiments:** The paper specifies the judge is "provided with the expected full answer" and deviations are penalized, which is a reasonable approach. More detail would help but this is not a core flaw.

- **Several section-by-section notes** (non-annotated deletion interpretation, answer length measurement details) were too granular to rise to the level of review weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviewer's observation about the redundancy-vs-unfaithfulness tension is a well-known issue in CoT faithfulness literature (Lanham et al. 2023, Lyu et al. 2023) and is partially acknowledged by the paper itself.

## Suggestions

1. **Re-scope the paper's claims.** Instead of claiming to assess CoT *faithfulness*, more accurately characterize the contributions as a behavioral characterization of how models compensate for missing CoT content. The "cramming" phenomenon and the physics-aware deletion results are interesting with or without the faithfulness framing.
2. **Add a no-deletion baseline** for the information overlap analysis to contextualize the observed increase in overlap under deletion.
3. **Add structure-aware matching** (equation parse trees, numerical value overlap) to strengthen the information overlap analysis.
4. **Validate the LLM judge** with a small human evaluation on a subset of scored answers, or at minimum discuss the potential interaction between the judge's own faithfulness limitations and the paper's conclusions.

## Score and Decision

**Round 1 bracket:** 5.0 – 6.5

**Calibration anchors considered (all rounds):**

| Anchor | File | Avg Score | Decision | Round | Itemized? | Comparison |
|--------|------|-----------|----------|-------|-----------|------------|
| On the Hardness of Faithful CoT Reasoning | 1OyE9IK0kx | 5.00 | Reject | R1 | Yes | Similar topic (CoT faithfulness); the reviewed paper has more novel methodology but similarly overclaims relative to evidence |
| SciBench | u6jbcaCHqO | 5.60 | Reject | R2 | Yes | Physics/science benchmark paper; the reviewed paper has stronger methodological novelty but less exhaustive evaluation |
| FLARE | awtd0XhzKQ | 5.75 | Reject | R2 | Yes | Faithful reasoning method paper; the reviewed paper has different approach and comparable weakness severity |
| Understanding CoT through Information Theory | ouRX6A8RQJ | 6.40 | Reject | R1,R2 | Yes | CoT evaluation paper; the reviewed paper has better real-world evaluation but less theoretical grounding |
| To CoT or not to CoT? | w6nlcS8Kkn | 6.67 | Accept | R1,R2 | Yes | CoT efficacy paper; much broader empirical scope and stronger conclusions, setting a quality bar the reviewed paper does not meet |
| Supervised Chain of Thought | pXIbcRPxWR | 2.50 | Reject | R1 | No | Lower quality work; the reviewed paper is substantially stronger |
| Planning in Strawberry Fields | jOuHjFw71C | 3.00 | Reject | R1 | No | Different topic (planning); less relevant |
| Code-of-thought prompting | lUyYX9VFgA | 3.00 | Reject | R1 | No | Different topic (safety probing); less relevant |

**Narrowing:** Comparing favorability ratings, the reviewed paper's most negative weakness (BoW metrics, favorability=-0.18) is less severe than the worst weaknesses in the 5.00 anchor (favorabilities as low as -4.95 for incremental contribution). However, the paper lacks the comprehensive evaluation or theoretical depth of the 6.40–6.67 anchors. The physics-aware deletion strategy and consistent cross-model cramming findings are genuine contributions that place it above the 5.00 anchor, but the gap between claims and evidence confines it below the accept range.

**Final score:** 5.5 — Reject. The paper's methodology is novel and the behavioral findings are interesting, but the central interpretive claims about CoT unfaithfulness are insufficiently supported by the evidence, and the bag-of-words overlap metrics are too coarse for the faithfulness conclusions drawn. The paper would be substantially stronger if it were scoped as a behavioral characterization of compensation mechanisms rather than an assessment of faithfulness.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>