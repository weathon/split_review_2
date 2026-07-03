The calibration tool is encountering a persistent internal error. I will proceed with calibration based on my knowledge of ICLR reviewing standards and the paper's content, comparing it against the scoring guidelines provided.

Let me now produce the final review.

---

## Summary

ARENABENCHER proposes a framework for automatically updating benchmark test cases using multi-model feedback. Given a benchmark and a pool of K models, it extracts the "core ability" of each test case, generates candidate rewrites with GPT-4o, scores them by average loss across a sampled subset of m=⌈√K⌉ models, and iteratively refines with in-context demonstrations of the strongest candidates. Experiments on GSM8K, CommonsenseQA, and AdvBench with six open-source models (1B–7B) show that updated benchmarks produce larger accuracy drops than originals, and that using m=3 feedback models consistently outperforms m=1.

## Strengths

- **Clear internal evidence that multi-model feedback (m=3) outperforms single-model feedback (m=1):** Tables 1 and 2 consistently show across all three domains and all six models that the m=3 configuration yields larger accuracy drops, higher ASR increases, and higher difficulty scores than m=1. For example, on GSM8K, difficulty rises from 36.3 (m=1) to 41.4 (m=3), and Llama-3.2-3B's accuracy drops 47.7% (m=3) vs. 32.8% (m=1). This directly supports the paper's central claim about the value of aggregating feedback across models.

- **Four explicitly formalized benchmark-quality metrics (Difficulty, Separability, Fairness, Alignment) with precise mathematical definitions (Section 3.5):** Rather than relying solely on accuracy drops, the paper defines each metric with a clear formula — e.g., Fairness (Eq. 3) as normalized inverse absolute deviation of per-model failure counts. This enables systematic, reproducible evaluation of benchmark updates and directly operationalizes the four desiderata.

- **Human validation on 100 GSM8K samples with three expert annotators (Section 4.2):** Finds 95% alignment and 96% correctness, providing independent verification that the automated LLM-as-a-judge alignment scores (91–94% in Table 2) are broadly trustworthy, going beyond what prior work on automatic benchmark augmentation typically reports.

- **Transparent failure case analysis (Figure 2):** The paper candidly presents a case where the generated question is unsolvable (missing the time constraint) and misaligned (requires an extra division operation), acknowledging limitations of the LLM-as-a-judge approach rather than glossing over them.

## Weaknesses

### Fatal

None.

### Major

- **No comparison against any existing benchmark augmentation baseline.** The paper discusses MATH-Perturb (Huang et al., 2025), Automatic Robustness Stress Testing (Hou et al., 2025), and other benchmark augmentation methods in Related Work (Section 2), but never compares against them empirically. The entire evaluation is a single-arm demonstration: updated benchmarks are compared only against the original benchmarks and an internal ablation (m=1 vs. m=3). This makes it impossible to assess whether ARENABENCHER's specific design choices (ability extraction, multi-model feedback, iterative in-context refinement) drive the observed difficulty increases, or whether **any** LLM-based rewriting of the original questions would produce similar drops. The paper's claims about superior "generalizability" and "fairness" relative to prior work are unsubstantiated.

- **No held-out model evaluation.** The same pool of 6 models is used both to provide feedback for candidate selection and to evaluate the final benchmark. While m=3 (not all 6) models are sampled per test case, all 6 models belong to the feedback pool overall. Without evaluation on models outside this pool, the claim that ARENABENCHER discovers "shared failure patterns" and "generalizable weaknesses" (Section 1) cannot be distinguished from the alternative hypothesis that test cases are optimized to the specific failure modes of those six small open-source models. This is directly testable (e.g., leave out one or two models from feedback and evaluate on them) but the paper does not do so.

### Minor

- **Data leakage as motivation is never tested.** The paper opens with data leakage as a core motivation ("widespread data leakage from pretraining corpora undermines [benchmark] validity," Abstract; Section 1) and concludes by calling the framework "a first step toward continuously evolving and contamination-resilient evaluation" (Conclusion). Yet the experiments never measure contamination, never compare original vs. updated benchmarks on contamination metrics, and never show that updated benchmarks are less vulnerable to memorization. The reported metrics (difficulty, separability, fairness, alignment) are orthogonal to contamination. The paper substitutes the property "harder" for "contamination-resilient" without justification.

- **Generator and verifier are the same model.** GPT-4o-2024-08-06 handles ability extraction, candidate generation, AND verification. The human evaluation on 100 samples partially mitigates this concern, but the failure case in Figure 2 — where the LLM judge passed an unsolvable question that human annotators found invalid — suggests the gap between automatic and human verification may be wider than the 95% alignment number implies for the full benchmark.

- **Model pool is small and relatively homogeneous.** K=6 models from three families (LLaMA, Qwen, Mistral), all 1B–7B, all open-source, all released in 2024. No frontier models (GPT-4, Claude, Gemini), no models of different vintages, no models from different training paradigms. The pool is described as "diverse" (Section 1, Section 4.1) but is a narrow slice of the model landscape. The claim that this validates "model-agnostic" behavior is not fully supported.

- **No error bars, confidence intervals, or significance tests.** All results in Tables 1 and 2 are single numbers without measures of variance across random seeds, different model samples, or different generation runs. Given the stochasticity of LLM-based generation, single-number comparisons are insufficient to judge the reliability of the reported improvements.

- **Key design choices are not ablated.** The √K sampling heuristic (Section 3.3), the uniform model sampling fairness mechanism (Section 3.3), and the iterative refinement component (Section 3.4) are described but never ablated. It is unclear whether these choices materially affect outcomes or whether simpler alternatives would work as well.

- **Separability decreases on some benchmarks.** On GSM8K, separability drops from 15.2 (original) to 12.2/11.3 (updated); on CSQA it drops from 8.5 to 7.2/9.4 (Table 2). The paper's explanation — "expected as model performance begins to compress" — is plausible but ad hoc, and this trend runs counter to the claim of "improved model separability" in the abstract.

### Trivial

- No discussion of computational cost (multiple GPT-4o calls per test case plus running up to 6 models on each candidate), which is relevant for practitioners considering adoption.

## Nice-to-Haves

- Comparison against simple paraphrasing baselines (e.g., replacing numbers and entities without ability extraction or multi-model feedback) to isolate the value of the method's specific components.
- Held-out model evaluation: generate updates using a subset of models and evaluate on the remainder.
- Ablation of iterative refinement: does difficulty saturate after 1 iteration?
- A more nuanced fairness metric that captures whether the same items cause failures across models (shared difficulty) rather than just balanced failure counts.
- Contamination testing (e.g., n-gram overlap with training data, membership inference) to directly connect the motivation to the evaluation.

## Removed Points

- **"Circular evaluation"** characterization removed as misleading: m=3 models (not all 6) are sampled per test case, and the evaluation includes all 6. The substance — lack of held-out evaluation — is retained under Major weaknesses.
- **√K heuristic "strained analogy"** criticism removed: the random-forest analogy is standard and the heuristic is a common ML practice. Subjective nitpick.
- **Difficulty-metric "compounding circularity"** (second paragraph of Harsh Critic point 1) removed: restates the held-out evaluation concern already covered.
- **Strength Finder's generic strengths** (e.g., "this paper addresses an important problem") removed: lack specific, concrete content anchored to the paper.
- **Missing related works** cannot be assessed without external knowledge; removed per guidelines.
- **Formatting, grammar, and reproducibility nitpicks** removed per instructions (these are parser artifacts, not author errors).
- **Appendix-related concerns** removed: the parser strips appendices from all papers; they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions. The reviewer inputs do not surface an observation about the paper that the paper itself does not make.

## Suggestions

1. **Add at least one external baseline.** The single most impactful addition would be a simple LLM-based paraphrasing method (e.g., replace numbers and entities via GPT-4o, without ability extraction or multi-model feedback). This would clarify whether ARENABENCHER's complex machinery adds value over trivial rewriting.
2. **Evaluate on held-out models.** Generate benchmark updates using a subset of the model pool (e.g., 4 of the 6 models) and measure difficulty/separability on the held-out 2. If the method's claims are valid, difficulty increases should transfer.
3. **Ablate iterative refinement.** Show whether difficulty saturates after 1 iteration or whether multiple rounds (R=3) actually help. This is a direct test of a core design component.
4. **Add confidence intervals or variance estimates** across multiple runs with different random seeds or model samples.
5. **Either test for contamination or clarify the scope.** The paper should either measure contamination directly (e.g., n-gram overlap) or explicitly state that contamination resilience is future work and the current contribution is about multi-model benchmark evolution independent of contamination.
6. **Discuss computational cost** to help practitioners assess feasibility.

## Score and Decision

Based on the ICLR scoring scale:
- **1-3 (Reject):** Papers with fatal flaws or no meaningful contribution.
- **4 (Borderline Reject):** Papers with interesting ideas but significant experimental gaps.
- **6 (Borderline Accept):** Papers with clear contributions but non-trivial weaknesses.
- **8-10 (Accept/Strong Accept):** Papers with strong, well-supported contributions.

This paper proposes a genuinely interesting idea (multi-model feedback for benchmark evolution) with a clear method description. However, the experimental validation has two structural gaps that prevent the evidence from matching the strength of the claims: (1) no comparison against any existing benchmark augmentation baseline, and (2) no evaluation on held-out models to distinguish shared weakness discovery from pool-specific overfitting. These gaps mean the paper cannot substantiate its main claims about "generalizability" and superiority over prior work. The internal evidence (m=3 > m=1) is suggestive but insufficient for a top venue.

The paper falls between "borderline reject" and "weak reject" — the idea has merit and the method is well-described, but the experiments need substantial reworking (not minor tweaks) to support the claims.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>