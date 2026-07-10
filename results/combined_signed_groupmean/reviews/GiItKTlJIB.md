## Summary

This paper introduces a deletion-based probing methodology to evaluate whether LLMs genuinely depend on their chain-of-thought (CoT) traces during physics problem solving. The approach intercepts CoT mid-generation, removes tokens using three strategies (end-deletion, random, physics-aware), and measures downstream effects on accuracy, answer length, and information overlap. Experiments across three open-source models (Phi-4, Qwen-A3B, Magistral) and three physics benchmarks show that accuracy remains stable under moderate deletion (40–60%) while answer length increases — a pattern the paper terms "cramming."

---

## Strengths

- **Novel methodological framework for probing CoT dependence.** The deletion-based probing approach (Section 3.2, line 118) is a genuinely new way to ask whether models depend on their own reasoning traces. Unlike prior work that mainly measures CoT correctness against answer correctness, this method actively intervenes in generation and measures downstream effects. This is a clean, well-motivated paradigm for physics, where equations, units, and structured terminology make the question testable.

- **Broad and systematic empirical evaluation.** The paper evaluates three open-source models (Phi-4 14B, Qwen-A3B 30.5B MoE, Magistral 24B) spanning different architectures and training regimes, across three physics benchmarks of varying difficulty (UG Physics, PhysReason, PhyBench). This breadth strengthens the empirical base and provides coverage across model families and problem types.

- **Meaningful distinction between physics-structured and non-structured content.** The comparison of annotated (equations, units) vs. non-annotated deletion (Figure 3, line 116) is well-motivated and yields the interesting finding that removing physics-specific content is more detrimental to accuracy than removing generic text. This is the cleanest finding in the paper and genuinely speaks to content-specific reasoning dependence.

- **Multi-metric evaluation goes beyond accuracy alone.** Using answer length and information overlap alongside accuracy (Section 2.4, lines 80–85) provides a richer characterization of model behavior than accuracy-only evaluation, even if individual metrics have limitations.

---

## Weaknesses

### Major

- **The "cramming" claim asserts a causal link the evidence does not support.** The abstract (line 9) states that models "remain accurate under heavy deletions (40–60%) by 'cramming' reconstructed steps into final answers," implying that length-increase *causes* accuracy maintenance. This causal claim is confounded with a mechanical property of autoregressive generation: when CoT tokens are deleted, the model generates from a shorter prefix, and longer continuations are expected regardless of any "compensatory" mechanism. The paper provides no control experiment (e.g., deleting the same proportion from the problem statement) to distinguish these explanations. The body text uses hedging ("possibly indicates," line 128), but the abstract and conclusion do not. The empirical observation that accuracy is stable under moderate deletion is interesting on its own; the unsupported causal interpretation weakens rather than strengthens the paper.

- **The LLM-as-judge is used as both annotator and evaluator without validation.** Claude-4 Sonnet serves as (a) the annotator identifying physics-related tokens for physics-aware deletion (lines 128, 148) and (b) the sole evaluation instrument scoring all model outputs on a 0–1 scale (line 82). No calibration against human expert grading, inter-rater reliability, or error analysis is reported. For a paper whose central argument is that accuracy-based evaluations are insufficient for scientific reasoning (§4.3), relying on an unvalidated LLM judge creates a methodological tension: the paper's own evaluation instrument could suffer from the same faithfulness problems it critiques.

- **The experimental procedure is critically under-specified for reproducibility.** The paper states it "intercept[s] the scratchpad and remove[s] k% of CoT tokens before the final answer" (line 118) but does not explain: (a) how the boundary between CoT and the final answer is programmatically identified in the generated sequence when models may output both as a single stream; (b) whether generation resumes from the truncated prefix, whether the model is re-prompted, or whether a separate decoding pass is performed; (c) how token positions, attention masks, or KV-cache state are handled after deletion. These details are essential for interpreting the results and for any follow-up work.

- **Several essential baselines are missing.** (1) Deleting from the problem statement (not the CoT) is needed to establish that length effects are specific to CoT rather than a generic response to prefix shortening. (2) Replacing deleted tokens with neutral tokens rather than deleting them would disentangle information loss from sequence-length reduction. The paper's annotated vs. non-annotated comparison (Figure 3) partially addresses the content-type question, but the core controls to distinguish CoT-specific from generic effects are absent. Without these, the specificity of the paper's findings to CoT faithfulness is unsubstantiated.

### Minor

- **The information overlap metrics have fundamental limitations for measuring faithfulness.** Jaccard similarity and Manhattan distance operate on bag-of-words representations (lines 170–180). Physics has fixed terminology and equations (e.g., F=ma, E=mc²), so high lexical overlap between original CoT and final answer is expected from any correct solution, regardless of whether the model faithfully uses its CoT. Conversely, a model could solve a problem via a different but equally valid derivation (e.g., energy methods instead of kinematics), producing a correct answer with low overlap. The metrics conflate domain-appropriate language with reasoning faithfulness.

- **The reported increase in information overlap may be partially artifactual.** As more CoT content is deleted, the pool of tokens available for overlap (which enters the Jaccard denominator) shrinks, which could inflate the overlap ratio even if the absolute amount of reconstruction remains constant. The paper does not normalize for this denominator effect.

- **Statistical testing is largely absent.** Claims such as "accuracy remains stable until approximately 40% deletion" (line 130) are presented as observed trends without significance tests, confidence intervals on the threshold, or formal quantification of variability across runs.

- **Dataset sizes are not fully reported.** PhysReason is quantified (1,200 problems, line 50), but UG Physics and PhyBench are not. The calibration study uses "50 UG-Physics questions" (line 112) — it is unclear whether this is the full dataset or a sample.

---

## Nice-to-Haves

- A direct-answer (no CoT) condition as a lower bound for calibration — the paper compares Full/Medium/Low reasoning prompts but never establishes what accuracy looks like with no CoT at all.
- Decomposition of which specific CoT elements (equations, unit conversions, algebraic manipulations, conceptual statements) matter most when deleted.
- Semantic-level (rather than bag-of-words) overlap metrics that handle equivalent equations and structurally equivalent reasoning.

---

## Removed Points

These points were raised in the input reviews but removed per filtering rules:

- **Claim that the paper mischaracterizes prior work as "ignoring" faithfulness:** The abstract says "benchmarks largely measure end-task accuracy while ignoring whether models genuinely depend on their own reasoning traces" — this refers to evaluation *benchmarks*, not prior *research*. The paper explicitly cites and engages with Lanham et al. (2023) and Turpin et al. (2023) in lines 13–14. The specific criticism is not accurate.
- **Complaint about prompt templates being in the appendix:** The parser strips all appendices; the original submission contains them.
- **Claim that the X-shaped pattern is "trivially expected" under constant-length assumptions:** Autoregressive models do not generate constant-length responses; whether total response length stays constant after prefix shortening depends on the model's learned behavior, not on a fixed property of the architecture.
- **Several scope-creep demands** (e.g., requiring analysis of latent representations, attention patterns) that go beyond what the paper sets out to do and would be outside the scope of most empirical papers at this stage.

---

## Novel Insights

None beyond the paper's own contributions. The reviews surface important methodological concerns (confounded interpretation, unvalidated evaluation, under-specified procedure) but do not introduce new scientific insight about the paper's results.

---

## Suggestions

1. **Address the cramming confound.** Add a control condition that deletes the same proportion of tokens from the problem statement (not the CoT). If answer-length increases only under CoT deletion, the effect is CoT-specific. If it also occurs under problem-statement deletion, it is a generic property of prefix shortening. This directly tests the paper's central interpretation.

2. **Validate the LLM judge.** Calibrate Claude-4 Sonnet's scoring against human physics expert grading on a held-out subset of at least 50–100 responses. Report agreement rates (e.g., Cohen's κ or Spearman correlation) and characterize systematic disagreements.

3. **Clarify the technical procedure.** Specify exactly how the CoT/answer boundary is detected (e.g., by searching for an answer-delimiter token, by parsing model-specific output format, by heuristic). Explain how generation resumes after deletion and how positional encoding/cache state is handled.

4. **Include a token-replacement baseline.** Replace deleted CoT tokens with neutral tokens (e.g., repeated "..." or stopwords) rather than removing them, to distinguish information loss from the mechanical effect of a shorter prefix.

5. **Normalize the overlap metric.** Report information overlap normalized by the size of the deleted set, or use a metric that is not sensitive to denominator shrinkage (e.g., reporting absolute counts of overlapping content alongside the ratio).

---

## Score and Decision

**Calibration anchors (all papers retrieved across rounds):**

| Path | Avg Score | Round | Itemized | Comparison to this paper |
|------|-----------|-------|----------|-------------------------|
| `/home/.../1OyE9IK0kx.md` (Hardness of Faithful CoT) | 5.00 | R1, R2 | Yes | Same topic (CoT faithfulness), broader methodological scope. Our paper has more novel methodology but weaker evidence for core claim. **Below this anchor.** |
| `/home/.../rpbzBXdo4x.md` (Mind Your Step) | 5.00 | R1, R2 | Yes | CoT performance effects, stronger controls and execution. Our paper has similar overclaiming severity. **Below this anchor.** |
| `/home/.../LSB2mRJdgZ.md` (Stochastic Parrot Physics) | 3.75 | R1 | Yes | Physics + LLM understanding, different methodology. Our paper has broader evaluation and a more direct methodology. **Above this anchor.** |
| `/home/.../OclSRDktp3.md` (Hopfieldian CoT) | 3.50 | R2 | No | Theoretical approach, less empirical. **Above this anchor.** |
| `/home/.../ON3QLXrwVb.md` (Cross-Generation Trees) | 4.67 | R2 | No | Different approach to reasoning analysis. **Comparable quality, slightly below.** |
| `/home/.../awtd0XhzKQ.md` (FLARE) | 5.75 | R2 | No | Faithful reasoning with symbolic verification, better-executed. **Below this anchor.** |
| `/home/.../Qyile3DctL.md` (Collaborative Verification) | 5.00 | R2 | No | LLM reasoning improvement, different focus. **Similar quality range.** |

**Round 1 bracket:** The paper sits between approximately 3.75 (Stochastic Parrot physics — weaker methodology but sound core idea) and 5.00 (Hardness of Faithful CoT — broader evaluation but similar overclaiming issues).

**Round 2 narrowing:** Compared to the closest anchor (Hardness of Faithful CoT, 5.00), this paper has a more distinctive methodology but weaker evidence for its headline claim. That anchor's weaknesses centered on incremental contribution (−10.00 impact) and rigor (−10.00). This paper's weaknesses are more structural (confounded interpretation, unvalidated judge, under-specified method), making its strongest claims harder to accept. Placing it below 5.00 but above 3.50.

**Final score:** The paper's novel deletion-based methodology and broad evaluation recommend it, but the core "cramming" claim is confounded, the evaluation instrument is unvalidated, the method is under-specified, and essential controls are missing. These are not minor issues — they affect the validity of the paper's main empirical findings. Score **4.0** (borderline reject): interesting research direction with some worthwhile findings, but the evidence does not adequately support the central claims in their current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>