Now let me write the final review.

## Summary

This paper introduces a deletion-based probing framework to study whether LLMs genuinely depend on their chain-of-thought (CoT) traces in physics reasoning. By intercepting CoT mid-generation, deleting tokens (end, random, or physics-aware), and measuring downstream accuracy, length, and information overlap, the authors find that models remain accurate under moderate deletions (40–60%) while producing longer final answers that attempt to reconstruct missing reasoning—a behavior they term "cramming." The study evaluates three open-source models (Phi-4, Qwen-A3B, Magistral) on three physics benchmarks.

## Strengths

1. **The deletion-based probing methodology is creative and well-motivated.** Intercepting CoT mid-generation and deleting tokens is a clean interventionist strategy that avoids post-hoc faithfulness checks requiring knowledge of the "correct" reasoning trace. The three deletion strategies (end, random, physics-aware) provide complementary views, and the choice of open-source models (enabling direct scratchpad interception) is a principled design decision. This framework is a genuine methodological contribution that other researchers could adopt.

2. **The "cramming" observation (increased answer length under deletion) is robust and interesting.** The fact that final answers get longer as CoT gets shorter is documented consistently across Figures 5 and 6, across all three models and benchmarks. Unlike the accuracy scores, this finding depends only on a straightforward character-count measurement, making it the paper's most trustworthy empirical result.

3. **The annotated vs. non-annotated deletion comparison is a clean within-experiment finding.** The observation that deleting physics-structured tokens (equations, units) is more detrimental than deleting non-annotated tokens (Section 3.2, Figure 3) relies on a within-experiment contrast rather than absolute accuracy values, making it one of the more reliable results.

## Weaknesses

### Major

1. **The LLM-as-judge (Claude-4 Sonnet) is unvalidated, undermining all quantitative accuracy results.** The paper's central accuracy curves—used to claim that performance is "stable until 40-60% deletion"—depend entirely on Claude-4 Sonnet scoring solutions on a 0–1 scale based on "correctness of the final answer, accuracy of the physics derivation, logical coherence, formatting, and clarity" (§2.4, §3.1). The paper provides no human validation study, no correlation with programmatic correctness checks (e.g., whether the final numerical answer matches ground truth), and no analysis of the judge's bias or variance. This is especially concerning because LLM judges are known to confound answer quality with surface features like length—and the paper's own experimental manipulation (CoT deletion) systematically affects answer length. Without validation, the reader cannot assess whether the observed accuracy curves reflect genuine physics correctness or are artifacts of the judge's length/formatting preferences. This is an evidential gap that could be fixed, but in the current form the paper's quantitative backbone is unverifiable.

2. **The headline interpretive claims are broader than the evidence supports.** The abstract states that the results "expos[e] shallow and opportunistic reliance on CoT," and the conclusion claims "CoT traces are both informative and redundant." What the experiments actually show is: (a) accuracy remains somewhat stable under moderate deletion, (b) answer lengths increase, and (c) lexical overlap between original CoT and final answers increases with deletion. These findings are consistent with multiple interpretations, including: the model faithfully using the remaining CoT and doing calculations internally; the model having internalized physics knowledge that supplements the CoT; or the CoT containing useful scaffolding but also redundancy. The paper does not rule out these alternatives because it does not analyze *what* is being reconstructed—whether crammed content is correct, whether it accurately reproduces the physics that was deleted, or whether it represents genuine recovery versus coincidental vocabulary overlap. The "opportunistic" characterization is an interpretive gloss that goes beyond what the experimental design can distinguish.

### Minor

3. **The information overlap metric only partially supports the "reconstruction" interpretation.** The paper measures lexical overlap (Jaccard similarity, Manhattan distance) between the original CoT and final answers under deletion (§4.2). While Figure 7 does show a baseline at 0% deletion and overlap increases with deletion—which is partially responsive to the concern about natural vocabulary overlap—the metric still conflates at least two distinct phenomena: (a) genuine reconstruction of deleted reasoning content, and (b) the model simply producing longer answers (which mechanically increases Jaccard similarity through higher token counts). Additionally, there is an ambiguity in the metric definition: the text (§4.2) says "original CoT prior to deletion" while the Figure 7 caption says "deleted CoT content"—these are different sets. The paper would benefit from a cleaner comparison (deletion vs. no-deletion baseline for the *incremental* overlap specifically attributable to deletion) and from qualitative analysis of whether reconstructed content is correct or hallucinated.

4. **The same model (Claude-4 Sonnet) is used for both physics token identification and answer scoring** (§2.4 for scoring, §3.2 for tagging). If Claude-4's token identification has systematic biases in which physics content it labels, and the evaluator (also Claude-4) has corresponding preferences, the physics-aware deletion results could be subtly distorted. This is a minor methodological gap—not fatal, but worth noting and easily fixable.

### Trivial

5. The calibration study (§3.1) uses only 50 questions from one benchmark (UG-Physics) to determine that "5 prompts" are sufficient, but the description is vague about whether "prompts" means independent completions or prompt templates. The basis for generalizing this calibration to all three benchmarks is thin.

## Nice-to-Haves

- A small-scale human validation study (e.g., 50–100 answers scored by a physics student or instructor) would substantially strengthen the quantitative claims.
- A qualitative analysis of what "crammed" content actually looks like—is it correct physics, garbled hallucination, or partial recovery? This would make the paper's central phenomenon concrete.
- The paper uses medium-reasoning prompts by default for deletion experiments (§2.3) but does not justify why this is the most informative setting. Full-reasoning prompts (longer CoT = more to delete) would provide a stronger test of CoT dependence.

## Removed Points

- **"The evaluation metric (LLM-as-judge) is unvalidated, making the quantitative results uncertain"** — Kept as Major Weakness #1.
- **"The information overlap metric does not cleanly measure what it claims to measure"** — The harsh critic's claim that the paper "provides no controlled comparison (deletion vs. no-deletion baseline)" is partially inaccurate: Figure 7 does show the metric at 0% deletion as a baseline. However, the metric still has confounds (longer answers inflate Jaccard similarity; ambiguity in what "original CoT" vs. "deleted CoT content" means). Demoted from "structural/fatal" to Minor Weakness #3.
- **"The paper shares a model between the intervention and evaluation"** — Kept as Minor Weakness #4.
- **"Headline claim about shallow and opportunistic reliance is broader than evidence supports"** — Kept as Major Weakness #2.
- Generic strengths about the problem being important or timely — Removed per filtering rules. The kept strengths are specific and evidence-grounded.
- Criticisms about missing appendix content, formatting nits — Removed per hard rules.
- Criticism about "no analysis of what cramming actually produces" — Moved to Nice-to-Haves since it's a missed opportunity but not a flaw in what the paper does present.
- Criticism about using medium-reasoning prompts — Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The harsh critic usefully identifies specific evidential gaps (unvalidated judge, confounded overlap metric) and the disconnect between claims and evidence, but these are critical observations about the paper's limitations, not novel insights about the subject matter. The insight that the cramming observation (length increase) is the paper's most robust finding because it doesn't depend on the LLM judge is a reviewer synthesis worth noting.

## Suggestions

1. **Validate or replace the LLM judge.** At minimum, show that the judge's scores correlate with programmatic correctness checks (e.g., final answer matching, unit correctness) or a human-annotated subset. Better yet, supplement with programmatic verification where possible.
2. **Add a controlled overlap baseline.** Compare overlap between final answer and original CoT *with* and *without* deletion to isolate how much additional overlap is specifically attributable to cramming. Also analyze the *correctness* of reconstructed content.
3. **Tone down the interpretive claims** to match what the evidence directly supports. The evidence shows that models can compensate for missing CoT content, but characterizing this as "shallow and opportunistic" goes beyond what is demonstrated.
4. **Provide qualitative examples** of crammed answers to make the phenomenon concrete and allow readers to assess whether the reconstruction is faithful or hallucinated.

## Score and Decision

**Calibration papers retrieved:**

| Path | Avg. Score | Round | Comparison |
|------|-----------|-------|------------|
| 1OyE9IK0kx (On the Hardness of Faithful CoT) | 5.00 | R1 | Directly comparable topic (CoT faithfulness); similar methodological concerns; rejected |
| rpbzBXdo4x (Mind Your Step by Step) | 5.00 | R1 | Empirical CoT study; comparable quality and weakness profile; rejected |
| asGQQc7gNo (Factuality Enhancement vs. Context-Faithfulness) | 6.67 | R1 | Higher quality; accepted; stronger evaluation methodology |
| LSB2mRJdgZ (Stochastic Parrot physics) | 3.75 | R2 | Physics evaluation paper; weaker methodology; rejected |
| u6jbcaCHqO (SciBench) | 5.60 | R2 | Benchmark paper; better validated but still rejected |
| lUyYX9VFgA (Code-of-Thought Prompting) | 3.00 | R1 | Safety evaluation paper; lower quality |
| pXIbcRPxWR (Supervised CoT) | 2.50 | R1 | Lower quality |

**Round 1 bracket:** 4.0–5.5

**Final score rationale:** The paper's core methodological contribution (deletion-based probing) is genuinely novel and the cramming observation is robust. However, the paper's quantitative claims depend on an unvalidated LLM judge, making the central accuracy curves unverifiable. The interpretive claims also outrun the evidence. Comparing to the anchor papers: this is stronger than "Stochastic Parrot" (3.75) but has similar evaluation weaknesses to "On the Hardness of Faithful CoT" (5.00), which was rejected. The paper has real potential but needs stronger evaluation to support its claims.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>