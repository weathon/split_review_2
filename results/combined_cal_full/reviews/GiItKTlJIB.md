## Summary

This paper proposes a deletion-based probing framework to evaluate how LLMs use chain-of-thought (CoT) traces in physics reasoning. It intercepts CoT scratchpads mid-generation, removes tokens using three strategies (end deletion, random deletion, physics-aware deletion), and measures downstream effects on accuracy, answer length, and information overlap. Experiments across three open-source models (Phi-4, Qwen-A3B, Magistral) and three physics benchmarks (UG Physics, PhyBench, PhysReason) show that accuracy remains stable under moderate deletion (40–60%) while answer length increases compensatorily—a behavior termed "cramming" where models reconstruct missing steps in the final answer.

## Strengths

- **Well-motivated question.** The paper identifies a genuine gap: accuracy-based benchmarks dominate LLM evaluation, but in scientific domains like physics, whether models genuinely depend on their CoT traces matters for trustworthiness. The introduction (Sec. 1) clearly situates this within the AI-for-Science context and grounds it in prior CoT faithfulness work (Turpin et al., Lanham et al., Lyu et al.).

- **Simple, intuitive probing paradigm.** The deletion framework—removing k% of CoT tokens via three strategies (end, random, physics-aware) and measuring downstream effects (Sec. 3.2)—is straightforward and easy to understand. This methodological simplicity is a virtue: it could be adopted and extended by other researchers working on CoT faithfulness.

- **Systematic empirical characterization across conditions.** The paper presents consistent patterns across 3 models × 3 datasets × 3 deletion strategies: accuracy remains stable under moderate deletion (40–60%) before declining, while answer length increases compensatorily. The overlap analysis (Sec. 4.2) showing deleted content reappearing in answers adds a useful second dimension. The internal consistency across diverse conditions suggests the effects are robust.

- **Open-source focus enables reproduction.** By using open-source models (Phi-4, Qwen-A3B, Magistral) rather than closed APIs (Sec. 2.2), the experiments could be reproduced and extended by the community—a concrete advantage over closed-model faithfulness studies.

## Weaknesses

### Major

- **The deletion mechanism is critically underspecified.** The paper states it "intercepts the scratchpad and removes k% of CoT tokens before the final answer" (Sec. 3.2, line 118) and "intercepts CoT traces mid-generation and removes tokens before decoding" (Sec. 1, line 29), but never clarifies the implementation. Two fundamentally different interpretations exist: (A) the deletion happens within a single generation pass via editing internal states (KV-cache manipulation), or (B) the model generates its CoT, the scratchpad is edited externally, and the model is re-prompted with the edited scratchpad in a separate forward pass. The language "prior to decoding" (Sec. 2, line 41) and "before the final answer" (Sec. 3.2, line 118) more naturally suggests Interpretation B (re-prompting). Under Interpretation B, the experiment tests the model's ability to work with partial information in its prompt context—not its *dependence on its own internally-generated reasoning trace*. The observed "cramming" behavior would then reflect the model doing what it was trained to do (complete a reasoning trace from whatever context it is given). Since the paper does not resolve this ambiguity, the interpretation of every downstream claim about "faithfulness" is affected. This is the paper's most significant methodological gap.

- **The primary evaluation metric (Claude-4 Sonnet as judge) has zero validation.** The paper's quantitative results (accuracy scores, deletion curves) rest entirely on evaluations by Claude-4 Sonnet scoring each solution on "correctness, derivation accuracy, logic, formatting, and clarity" (Sec. 2.4). There is no validation against human expert evaluation, ground-truth answers, or any external standard. This is especially concerning because: (1) the experimental manipulation produces *unusual* outputs (answers generated under heavy CoT deletion with crammed content) that an LLM judge may systematically misjudge; (2) the paper uses Claude-4 Sonnet both to annotate physics tokens for the physics-aware deletion strategy AND to score the resulting answers (Sec. 3.2), creating a dependency; (3) the source of "expected full answers" provided to the judge is not specified. Without human calibration, the numerical accuracy scores are of unknown reliability.

- **The evidence does not fully support the central claim about CoT unfaithfulness.** The paper defines faithfulness as "whether the scratchpad faithfully represents the computations that yield the final answer" (Sec. 4.3). However, the central experimental finding—accuracy remains stable under moderate deletion—demonstrates *redundancy* or *robustness*, not *unfaithfulness*. A model could faithfully use its CoT for internal computation AND have redundant internal knowledge that allows compensation when external tokens are removed. The paper conflates "bypassable" with "unfaithful." The information overlap metrics (Jaccard similarity and Manhattan distance on bag-of-words, Sec. 4.2) are shallow lexical measures that cannot distinguish genuine faithful reconstruction from superficial lexical similarity. Two physics answers could use identical equations and vocabulary while making different claims. The paper's Section 4.4 acknowledges that conclusions are drawn from "observable outputs" but does not bridge this logical gap.

### Minor

- **Inconsistent model name.** "Magistral" (abstract, intro, figures) vs. "Magistrall" with double 'l' (Sec. 2.2, line 59). While likely a typo, this creates ambiguity about which specific model variant was evaluated.

- **No qualitative analysis of crammed content.** The paper measures answer length and lexical overlap (Sec. 4.2) but never examines whether the reconstructed content is actually *correct*. Do the crammed equations and steps solve the problem, or are they plausible-sounding but wrong? A few qualitative examples showing what models reconstruct would substantially strengthen the claim that reconstruction is "heuristic and opportunistic."

- **Incomplete dataset statistics.** PhysReason is described as 1,200 problems (Sec. 2.1), but UG Physics has no size reported and PhyBench is described only qualitatively. This makes it difficult to assess the statistical power of the reported deletion curves.

### Trivial

None.

## Nice-to-Haves

- Ablate the judge dependency: using Claude-4 for both physics-token annotation and answer scoring creates a circular dependency. Validating or swapping one of these roles would strengthen the physics-aware deletion results.
- Explicitly distinguish "dependence" from "faithfulness" in the framing. The evidence directly supports claims about CoT *dependence/redundancy*; the faithfulness claim is a plausible but indirect implication.
- Compare against prior faithfulness probing methods (Turpin et al., Lanham et al., Lyu et al.) to clarify what deletion-based probing reveals that prior approaches did not.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. The reviewer claimed the paper uses "Qwen-A3B" vs "Qwen" inconsistently — "Qwen" appears only in figure captions (natural abbreviation for space), not in the body text. Removed as not a genuine inconsistency.
2. The reviewer suggested the UG Physics benchmark "does not appear as a widely known benchmark" — this approaches questioning a cited reference's validity/notability. Removed per hard rules.
3. The reviewer claimed the paper "never explains what its deletion-based method reveals that prior approaches did not" — this is scope creep; the paper is an empirical study, not a methods comparison. Demoted to nice-to-have.
4. Section-by-Section Notes containing generic observations, parser-artifact complaints (alt-text only figures), and speculation about missing appendix content. Removed.
5. The claim about calibration not generalizing across datasets is speculative and not grounded in any evidence from the paper. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Clarify the deletion mechanism explicitly.** Specify whether the model is re-prompted with an edited scratchpad (Interpretation B) or the intervention happens within a single generation pass (Interpretation A). If the former, acknowledge that the experiments test the model's ability to work with partial context, and reframe faithfulness claims accordingly.
- **Validate the LLM judge against human experts** on a subset of at least 50–100 examples. Report agreement rates (e.g., Cohen's κ). Without this, the numerical accuracy scores lack a reliability anchor.
- **Add a qualitative analysis** of 3–5 example outputs per deletion condition showing what crammed content looks like: are the reconstructed equations correct? Do they solve the problem?
- **Reframe the central claim** from "CoT is unfaithful" to "CoT is partially redundant / models can bypass substantial portions of CoT while maintaining accuracy through compensatory reconstruction." This is what the evidence actually supports.

## Score and Decision

**Bracket rationale (Round 1):** The paper's deletion-based probing paradigm is novel and its empirical scope (3 models × 3 datasets × 3 deletion strategies) is substantial, placing it above pure reject territory (>3). However, the unvalidated LLM judge (-7.17 in model-weighted score), the faithfulness/dependence conflation (-4.52), and the underspecified deletion mechanism (-2.88) are too severe to reach borderline-accept territory (≥6). Comparing against anchor **1OyE9IK0kx** (avg 5.00, "On the Hardness of Faithful CoT Reasoning"): that paper's heaviest negatives concern limited technical novelty, while this paper has stronger novelty but weaker execution rigor. Comparing against anchor **LSB2mRJdgZ** (avg 3.75, "The Stochastic Parrot on LLM's Shoulder"): this paper has a more original methodology but similar evaluation-validity concerns. The paper sits in the 4–5 band: a promising methodological contribution undermined by execution gaps that prevent the claims from being fully supported.

**Calibration anchors consulted:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1OyE9IK0kx.md` (avg 5.00, Round 3, itemized): similar topic (CoT faithfulness), shares the "well-motivated" quality but its weaknesses are about technical novelty rather than execution rigor. My paper is slightly weaker on execution validation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/w6nlcS8Kkn.md` (avg 6.67, Round 3, not itemized): CoT meta-analysis with strong empirical rigor. My paper does not match this level of evaluation validation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ouRX6A8RQJ.md` (avg 6.40, Round 3, itemized): information-theoretic CoT evaluation. Stronger theoretical foundation and better-validated experiments.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LSB2mRJdgZ.md` (avg 3.75, Round 3, itemized): physics understanding benchmark. Shares evaluation-rigor concerns; my paper has stronger methodological novelty.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/qit4pa6PpY.md` (avg 3.00, Round 3, not itemized): LLM evaluation benchmark with similar scale but limited innovation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RuY1r1PDdQ.md` (avg 3.00, Round 3, not itemized): evaluation methodology paper with unvalidated evaluation as a core weakness.

**Final score grounded in weighted-item comparison:** My paper's heaviest positive weights (+4.17 systematic characterization, +4.14 probing paradigm) are comparable to the mid-range anchors' positives. But its heaviest negatives (-7.17 unvalidated judge, -4.52 faithfulness conflation) are more severe than any single weakness in the 5+ anchors. The -7.17 unvalidated-judge weight is the deciding factor: it pulls the paper below the 5.0 anchor (1OyE9IK0kx) into the 4–5 range.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>