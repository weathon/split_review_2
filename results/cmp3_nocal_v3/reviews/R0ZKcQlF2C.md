## Summary

The paper introduces ARENABENCHER, a framework that automatically evolves benchmark test cases by: (1) extracting the core ability of each original test case, (2) generating candidate variants via an LLM, (3) using a multi-model feedback loop (aggregated loss across sampled models) to select variants that consistently degrade performance, and (4) iteratively refining via in-context demonstrations of strong candidates. Experiments on GSM8K (math), CommonsenseQA (reasoning), and AdvBench Harmful Behaviors (safety) show the updated benchmarks are substantially harder while maintaining reasonable alignment, fairness, and separability.

---

## Strengths

- **Multi-model feedback is well-motivated and empirically tested.** The paper identifies a known failure mode of single-model adversarial benchmark construction (model-specific bias) and directly addresses it by aggregating loss across multiple sampled models. The m=1 vs. m=3 comparison (Tables 1 and 2) provides concrete, consistent evidence that multi-model feedback yields harder test cases than single-model feedback across all three domains and all six models. This is a non-trivial empirical finding.

- **Iterative refinement with in-context demonstrations (Section 3.4).** The design of reusing top candidates as demonstrations for subsequent generation rounds is a clean and practical mechanism for steering generation toward more diagnostic cases. Prior benchmark augmentation work has not systematically exploited this pattern.

- **Honest case study and human annotation.** The paper includes human evaluation of 100 GSM8K samples (95% alignment, 96% correctness) as ground-truth verification beyond LLM-as-a-judge. More importantly, it openly discusses a failure case (Figure 2) where the generated query is unsolvable and drifts in required skills — a mark of intellectual honesty that most papers omit.

---

## Weaknesses

### Fatal

None. The method is sound, the design rationale is clear, and the experimental results demonstrate that the framework produces harder test cases while preserving alignment on multiple benchmarks.

### Major

1. **Absence of any baselines from prior work or simpler alternatives.** The paper discusses MATH-Perturb (Huang et al., 2025), Automatic Robustness Stress Testing (Hou et al., 2025), and simple numerical perturbation methods (Yang et al., 2025; Mirzadeh et al., 2024) in the related work (§2), but evaluates ARENABENCHER against *nothing* except the original unmodified benchmarks and its own m=1 variant. A simple LLM-based paraphrase-only baseline (without multi-model feedback selection) would isolate whether the benefit comes from the generation pipeline itself or from the multi-model aggregation. Without any external baseline, the paper cannot support the claim that ARENABENCHER is *better* than existing approaches — only that it produces harder test cases relative to the original. This is the most significant gap in the experimental evaluation.

2. **Circularity in the evaluation design.** The same model pool of K=6 models is used both for selecting test case variants (via the multi-model feedback loop, §3.3) and for evaluating the updated benchmarks (Tables 1 and 2). For each test case, m=3 models are randomly sampled from the pool for selection — but over the full benchmark, every model participates in selection roughly uniformly. Consequently, the reported accuracy drops (e.g., 47.7% for Llama-3.2-3B on GSM8K) are partially expected artifacts of selecting variants that maximize loss for these very models. Holding out at least one model entirely from the selection process and evaluating it separately would break this circularity and provide genuine evidence that the updated test cases test shared capabilities rather than selection-optimized artifacts.

3. **Disconnect between the contamination motivation and the evaluation.** The abstract and introduction (§1) are heavily framed around data leakage / contamination: "widespread data leakage from pretraining corpora undermines [benchmark] validity," "models can exploit memorized content rather than demonstrating true generalization." The conclusion describes ARENABENCHER as "a first step toward continuously evolving and contamination-resilient evaluation." Yet the experiments (§4) contain *no* test of contamination resistance — no contamination scenario, no measurement of whether generated queries overlap less with training data, no comparison of models with/without exposure to the original benchmark. The experiments measure difficulty, fairness, separability, and alignment — which are all reasonable quality metrics for evolved benchmarks, but they do not address the contamination threat that motivates the paper. The paper's explicit contribution claims (§1 end) are appropriately narrower (ability-aware updates, multi-model feedback, iterative refinement), but the framing creates an unmet expectation.

### Minor

1. **The fairness metric conflates equal failure rates with fairness.** The metric (§3.5) penalizes deviation from equal failure counts across models: it is maximized when all models fail on exactly the same number of items. This can penalize a benchmark that correctly reveals genuine capability differences (e.g., a 1B model failing on more items than a 7B model). The paper partially mitigates this by also reporting separability (which measures variance in accuracy), but the fairness metric as a standalone quantity is ambiguous — a high score could mean "no model is disproportionately targeted" or "the benchmark fails to differentiate capabilities." The paper's claim that fairness "remains high" for original benchmarks (84.8% for GSM8K, 82.9% for Harmful Behaviors, Table 2) is consistent with the metric being uninformative.

2. **All framework components depend on a single proprietary model (GPT-4o).** Test objective extraction, candidate generation, and verification all use GPT-4o-2024-08-06 (§4.1). This creates a single point of failure and raises questions about generality (would results transfer to other generators/judges?) and reproducibility (can the method be independently replicated or deployed without access to this specific model?). The case study failure (Figure 2) — where the verifier passes an unsolvable query — underscores the risk of this dependence.

3. **No variance or significance estimates.** All results in Tables 1 and 2 are reported as point estimates without confidence intervals, standard deviations, or significance tests. Given the small model pool (K=6), some observed differences (especially between m=1 and m=3 where values are close) may not be stable.

4. **Iterative refinement rounds (R=3) not ablated.** The paper claims iterative refinement as a contribution but does not ablate the number of rounds or compare against a single round of generation. It is unclear how much value the iterative process adds over a single-pass generation with multi-model selection.

5. **Model pool is limited to small open-source models (1B–7B).** The six models (Table 1) are all from three families (LLaMA-3.2, Qwen3, Mistral) and all in the 1B–7B parameter range. No frontier or larger models are included, so the "shared weaknesses" identified may be specific to this class of relatively small models.

6. **Human evaluation is limited in scope (100 GSM8K samples only).** The 95% alignment and 96% correctness rates are encouraging, but the sample is drawn from a single benchmark, and the case study shows the automated verifier can fail on examples it passes, raising questions about the verifier's false positive rate not measured in the paper.

### Trivial

None.

---

## Nice-to-Haves

- **Add at least one baseline from prior work** — a simple numerical perturbation baseline or LLM-based paraphrase-only variant — to quantify the marginal benefit of multi-model feedback selection over the generation pipeline itself.
- **Hold out one model from the selection loop** (i.e., use K' = 5 models for feedback and reserve the 6th for evaluation) to break the circularity and test whether selected variants truly reflect shared weaknesses.
- **Measure contamination resistance directly** (e.g., membership inference tests, or fine-tune a model on the original GSM8K train set and measure performance gain on the updated vs. original test set) if the contamination framing is retained.
- **Ablate the number of iterative refinement rounds (R)** to isolate the contribution of the in-context demonstration mechanism.
- **Add confidence intervals** to Tables 1 and 2 via bootstrapping over the model pool or over test instances.
- **Systematically analyze failure modes** in generated queries (skill drift, underspecification, incorrect answers) and measure the verifier's false positive rate.

---

## Removed Points

These points were flagged for removal from the harsh critic's review. They are recorded here for completeness but do not appear in the main weaknesses above.

1. **"Related work does not establish clear limitations that existing methods cannot address"** — Removed because the paper *does* explicitly state a limitation: "they typically optimize against a single model or rely on local perturbations that target narrow error patterns" (§2). The characterization may be debatable for specific methods (e.g., MATH-Perturb's template perturbations are model-agnostic), but the general limitation is stated. This was downgraded from what might have been a minor point to removed.

2. **"The paper never explains why multi-model feedback is superior to model-agnostic alternatives"** — This is effectively subsumed by the absence-of-baselines weakness (Major #1). If the paper had included such baselines, the explanation could be evaluated empirically. As a standalone criticism without a specific textual anchor beyond the related work, it is better addressed by the baseline gap.

3. **"Section-by-section: Related work catalogues methods without establishing limitations"** — Overlaps with point 1 above. The related work section's purpose is to contextualize the method, and it does identify a limitation (single-model focus / narrow perturbations). The degree of thoroughness is a judgment call, not an identified error.

4. **"Scope of verification: case study shows verifier passes an invalid question; paper only acknowledges in passing"** — The paper devotes an entire subsection and an extended figure (Figure 2 + ~15 lines of text) to discussing this failure case. It is not "in passing." The paper transparently discusses the failure and identifies two specific failure modes. This criticism is inaccurate.

5. **"Strength: the paper addressed an important problem"** — Generic/superficial strength not specific to this paper. Removed per instructions to drop generic strengths.

---

## Novel Insights

None beyond the paper's own contributions. The most interesting finding from the review process is the tension between the paper's strong contamination framing and its clean but narrower evaluation — the multi-model feedback mechanism demonstrably produces harder test cases, but whether that hardness translates to contamination resistance is an untested hypothesis that future work could either validate or refute.

---

## Suggestions

1. The most impactful improvement is **adding at least one baseline**: a simple LLM-based paraphrase of the original questions (without multi-model feedback selection). This directly isolates the value of the multi-model selection mechanism from the LLM generation pipeline itself, and would significantly strengthen the empirical case for acceptance.

2. If the contamination framing is to be kept, **add one targeted contamination experiment** — for example, fine-tune a small model on the original GSM8K training data and compare its performance gain on the original vs. ARENABENCHER-updated test set. If the gain is smaller on the updated set, that directly demonstrates contamination resistance.

3. **Hold out one model** (e.g., Mistral-7B-I) from the selection loop and evaluate it separately on the updated benchmark. If it also shows meaningful degradation, this would powerfully demonstrate that the selected variants test shared weaknesses rather than selection artifacts.

---

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>