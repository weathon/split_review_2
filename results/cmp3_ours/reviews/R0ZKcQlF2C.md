## Summary

ARENABENCHER proposes a framework for automatically evolving static benchmark test cases using multi-model feedback to counter data leakage. Given a benchmark and a pool of models, it extracts the core ability tested by each question, generates candidate rewrites, filters them via an LLM verifier, scores them by aggregating loss across a sampled subset of models, and iteratively refines with in-context demonstrations. Experiments on GSM8K, CommonsenseQA, and a safety dataset show increased difficulty after update. The paper targets a genuine problem and presents a clean, well-structured framework.

## Strengths

1. **The problem of static benchmark contamination is genuine and well-motivated.** Section 1 correctly identifies that static benchmarks conflate memorization with generalization, and the paper provides a reasonable survey of contamination evidence.

2. **The four-desiderata framework (difficulty, separability, fairness, alignment) provides a structured lens for evaluating benchmark quality.** Even where the implementation has issues, the conceptual organization is useful and could inform future work in this area.

3. **The idea of using multi-model feedback to guide benchmark evolution is novel.** Most prior augmentation methods optimize against a single model or use local perturbations; the notion of aggregating signals across a model pool to find shared failure patterns is a worthwhile research direction.

4. **The human annotation effort on 100 GSM8K samples with three annotators is a genuine attempt at validation.** The 95%/96% alignment/correctness numbers provide a lower bound on quality, and the paper honestly presents a failure case (Figure 2), showing scientific transparency.

## Weaknesses

### Major

1. **No external baselines — the paper's central comparative claims are unsubstantiated.** Section 2 discusses MATH-Perturb (Huang et al., 2025), Automatic Robustness Stress Testing (Hou et al., 2025), gradient-based adversarial methods (Liu et al., 2023; Mo et al., 2025), and various perturbation strategies, and claims ARENABENCHER is superior because it is "model-agnostic" and uses "multi-model feedback." Yet **none of these methods are implemented or quantitatively compared.** The entire experimental section compares only two configurations of ARENABENCHER itself (m=1 vs m=3). Without even a trivial baseline (e.g., "use GPT-4o to rephrase each question"), we cannot determine whether the observed difficulty increases come from ARENABENCHER's specific design choices or from any LLM-based rephrasing. This is the single most severe gap: it prevents the paper from supporting its core contribution claims.

2. **Alignment verification is circular and demonstrably unreliable.** The pipeline uses GPT-4o as generator, verifier, and alignment judge (Section 4.1). The case study shown in Figure 2 — which the authors *chose to highlight* — provides concrete evidence of failure: a generated question that omits essential information (making it unsolvable), requires a different operation than the original (changing the tested skill profile), and is explicitly judged invalid and misaligned by human evaluators. Yet this candidate passed the LLM verifier and was included in the updated benchmark. The 91-94% alignment numbers in Table 2 are therefore unreliable: they measure GPT-4o's agreement with itself, not genuine alignment with original test objectives. The paper should report the false-positive rate of the LLM judge against human annotations.

3. **The evaluation pool and feedback pool are identical, creating an overfitting loop.** The six models used for evaluation (Table 1) are the same six models whose feedback guides candidate selection. Candidates are selected for "consistently degrad[ing] performance across the sampled models," then evaluated on those same models. The reported superiority of m=3 over m=1 likely reflects better in-distribution fitting rather than genuinely harder, more general queries. A proper evaluation would hold out at least two models from feedback and test on them separately.

4. **Abstract claim about separability directly contradicts the experimental data.** The abstract states that ARENABENCHER "improve[s] model separability." Table 2 shows the opposite: with the default m=3 configuration, separability *decreases* on all three benchmarks (GSM8K: 15.2→12.2; Harmful Behaviors: 17.1→14.5; CSQA: 8.5→7.2). The conclusion more accurately says it "largely maintains separability," but this inconsistency between the headline claim and the data is a significant communication error.

5. **No ablation study isolating the claimed contributions.** The paper makes three explicit contributions: (a) multi-model feedback, (b) ability-aware candidate generation, and (c) iterative refinement with in-context demonstrations. The only ablation is m=1 vs m=3, which partially addresses (a). There is no ablation of ability extraction (does structured ability description improve over raw generation?), iterative refinement (is R=3 better than R=0?), the verification step, the candidate quantity (n=5), or the sqrt(K) sampling rule versus alternatives. Without these, we cannot attribute observed effects to the method's specific components.

### Minor

6. **The difficulty metric is nonstandard and potentially misleading.** Difficulty is defined as `1 - max(ACC)` (Section 3.5), so it is determined entirely by the single best model's accuracy. If one model drops from 90% to 50% while others are flat, this reports a large difficulty increase even though most models found the questions no harder. The more standard approach would be average accuracy or loss. This choice inflates the reported difficulty numbers.

7. **Contamination resistance — the paper's stated motivation — is never tested.** The motivation is that data leakage undermines benchmark validity, and evolving benchmarks should address this. Yet the experiments only measure whether updated benchmarks are *harder*, not whether they resist memorization. A harder benchmark can still be contaminated; the paper does not test or discuss whether models could memorize the updated versions.

8. **The sqrt(K) sampling heuristic has a strained justification.** The paper cites random-forest feature-subsampling heuristics (Chen & Guestrin, 2016; Breiman, 2001) to justify `m = ceil(sqrt(K))` for model subsampling. With K=6, sqrt(K) ≈ 2.45, rounded to 3 — sampling 50% of the pool. This does not provide the claimed diversity benefit and the cited heuristics were designed for a different setting (feature bagging).

9. **Human annotation is limited to GSM8K only.** No human validation is conducted for the safety (Harmful Behaviors) or commonsense (CSQA) benchmarks. Given that the case study failure is from math and 5% of GSM8K annotations were judged misaligned, the 90-94% alignment rates claimed for other domains (which are unvalidated by humans) cannot be assumed.

10. **No confidence intervals or statistical grounding.** Tables 1 and 2 appear to report single runs without variance estimates. Given stochastic components (random model sampling, LLM generation), variance reporting is needed to assess reliability.

11. **The model pool is limited to small open-source models (1B-7B).** All six models are from three families (LLaMA, Qwen, Mistral). No frontier models (GPT-4, Claude, Gemini) are included, which limits the generality of claims about cross-model fairness and shared failure patterns.

### Trivial

None.

## Nice-to-Haves

- A simple baseline such as "ask GPT-4o to rewrite each question with different numbers and verify the answer" would substantially strengthen the paper by showing the marginal benefit of multi-model feedback over naive rephrasing.
- Evaluating on held-out models (kept out of the feedback loop entirely) would directly test whether the multi-model approach generalizes rather than overfits.
- Reporting false-positive/false-negative rates of the LLM judge against human annotations would help quantify trustworthiness.
- A minimal ablation comparing full pipeline, no ability extraction, no iterative refinement, and no verification would isolate which components contribute.

## Removed Points

The following points from the input review were removed with justification:

- **"Instruction-tuned robustness claim needs qualification"** — Removed because the data actually supports the paper's claim: instruction-tuned models show smaller absolute drops (e.g., 40.2 vs 47.7 for LLaMA, 31.5 vs 35.7 for Qwen), meaning they are indeed more robust.
- **"Fairness metric is structurally biased"** — Removed because the fairness metric measures whether failures are evenly distributed, and the method selects candidates that cause failures across all models. This is logical consistency, not tautology.
- **"No code/data release commitment"** — Removed per hard rules: the paper cites references as existing. Also, this is a review artifact; the paper may commit in a stripped appendix.
- **"The safety evaluation conflates two interpretations"** — Removed as speculative without concrete evidence.
- **Various formatting/style complaints** — Removed as these are parser artifacts.
- **Various "missing appendix" or "missing proof" complaints** — Removed per hard rules about appendix stripping.

## Novel Insights

None beyond the paper's own contributions. The reviews surface an important pattern: papers that propose benchmark-generation frameworks often rely on the same LLM for generation, verification, and evaluation, creating a circularity that is difficult to detect without human validation. The ARENABENCHER case study provides a concrete illustration of this failure mode that the broader community should attend to.

## Suggestions

1. **Add at least two external baselines** — a simple LLM-rephrasing baseline (same generator, no multi-model feedback) and one method from the related work (e.g., Hou et al. 2025's approach). This is the single highest-leverage improvement.
2. **Hold out 2-3 models from the feedback loop** and report whether updated benchmarks remain hard for those unseen models.
3. **Provide human-validated alignment for all domains**, not just GSM8K, and report the LLM judge's false-positive rate against human judgments.
4. **Ablate the key components** (ability extraction, iterative refinement rounds, verification step) to show which design choices matter.
5. **Correct the abstract claim about separability** to match the data (separability is "largely maintained" or "slightly decreased," not "improved").
6. **Report confidence intervals or standard deviations** across multiple runs.

## Score and Decision

**Calibration:** I compare against the following anchor papers retrieved from the human-review corpus:

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| AutoBencher (ymt4crbbXh) | 6.25 | Bracketing | Very similar task (automatic benchmark construction). AutoBencher includes baselines (MMLU, XSTest), ablations, and human validation — all of which ARENABENCHER lacks. ARENABENCHER is materially weaker. |
| DyVal (gjfOL9z5Xr) | 6.50 | Bracketing | Dynamic evaluation for contamination. Has extensive experiments, baselines, multiple tasks. ARENABENCHER lacks the empirical thoroughness of DyVal. |
| LiveBench (sKYHBTAxVa) | 7.33 | Bracketing | Contamination-resistant benchmark with frequent updates. Stronger execution across all dimensions. |
| Benchmark Inflation (rAylWUIKtu) | 4.25 | Narrowing | Contamination-focused analysis paper. Different contribution type (analysis vs framework), but similar score band — paper with reasonable ideas but significant limitations. |
| Evading Data Contamination (Nk1MegaPuG) | 4.25 | Narrowing | Also contamination-focused. Provides a structured analysis with concrete demonstrations. |

**Bracket (Round 1):** 3.0–5.0. The paper has a genuine idea and a clear framework description, placing it above strong rejects (1.x). However, the complete absence of external baselines, circular verification, evaluation-feedback pool overlap, and claim-data contradiction prevent it from reaching the 4+ range where papers typically have more complete evidence.

**Final score (after narrowing):** 3.5. The paper's core idea is worthwhile and the framework is clearly described. However, the evidential gaps are severe and structural: the paper cannot substantiate its central claim of outperforming prior work without any external baseline comparison, and the alignment measurement is demonstrably unreliable. The paper should not be accepted in its current form.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>