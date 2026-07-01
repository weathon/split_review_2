## Summary
This paper studies data contamination in LLMs from a multilingual perspective. It fine-tunes models on Arabic-translated versions of English benchmarks (MMLU, XQuAD, MLQA) and evaluates on the original English benchmarks, using a variant of TS-Guessing with choice reordering to probe memorization. The main finding is that translation into Arabic obscures traditional surface-level contamination signals, yet models still benefit from exposure to the translated data, particularly those with stronger Arabic capabilities. The paper proposes a Translation-Aware Contamination Detection (TACD) framework as a forward-looking blueprint.

## Strengths
- The paper draws attention to an important and understudied problem: how contamination manifests in multilingual evaluation settings, where English-centric detection methods may fail.
- The idea of using choice reordering in TS-Guessing to detect memorization of index patterns in multiple-choice tasks is a sensible extension.
- The focus on translation as a potential masking mechanism for contamination is practically relevant given the growing use of multilingual LLMs.

## Weaknesses
### Fatal
- **The experimental setup does not model realistic contamination.** The authors fine-tune models directly on propositional subsets of the Arabic-translated test set of each benchmark (0%, 10%, 50%, 100% of the test examples). In real-world scenarios, contamination occurs during pretraining when the model sees benchmark data (or near-duplicates) among billions of web tokens, not during explicit supervised fine-tuning on the test set itself. This setup conflates "contamination" with "supervised training on the evaluation set via a different language wrapper," which is a fundamentally different phenomenon. The reported performance gains and TS-Guessing patterns therefore do not inform about how translation affects standard pretraining contamination; they only show that fine-tuning on a translated test set can improve English performance—a largely unsurprising result.

### Major
- **TS-Guessing results are too weak to support the core claims.** The IDR and EM/ROUGE-L-F1 scores reported in Table 3 are extremely low across all models and conditions (e.g., IDR often <0.01, RL-F1 <0.02 for LLaMA and Qwen). The authors interpret these near-zero values as contamination signals, but such low absolute scores raise serious questions about whether the TS-Guessing probe is detecting anything meaningful. Without statistically significant above-chance performance, the claim that "models still benefit from exposure" is not convincingly supported by the memorization probe.
- **Evaluation results are noisy and inconsistent.** The non-monotonic trends across contamination levels (e.g., Mistral XQuAD collapsing from 0.455 to 0.114 at 100%; Qwen MLQA spiking at 10% and then collapsing) are not systematically explained. The paper attributes these to "overfitting to distributional quirks" and "fragile transfer," but these post-hoc explanations are not supported by controlled analysis or statistical tests. The aggregate patterns do not provide a clear, reproducible signal about contamination dynamics under translation.
- **Lack of statistical rigor and ablation.** No confidence intervals, significance tests, or variance estimates are reported for any result. Given the small model sizes (1B-1.7B) and the fact that each condition is a single run, it is impossible to assess whether observed differences are reliable or due to random seed variation. The paper does not ablate the effect of translation quality, choice of Arabic dialect, or order of training mixtures.
- **Novelty is limited.** The central insight—that translation changes surface form while preserving semantics, thus masking standard n-gram based contamination checks—is fairly straightforward and has been acknowledged in prior work on cross-lingual transfer and data leakage. The paper does not provide a deeper theoretical or empirical characterization of when and how translation masks contamination, nor does it offer a deployable detection tool.

### Minor
- The TACD framework is presented only as a blueprint with no implementation, empirical validation, or analysis of its challenges. Its inclusion strengthens the motivation but does not constitute a contribution of the present work.
- The literature review is disproportionately long (Sections 2.1–2.3 catalog known contamination forms and methods) and could be significantly condensed.
- The reference to "embedding figure" in Section 4.3 appears to describe a figure that is not included in the main paper (only referenced textually), making the analysis incomplete.

### Trivial
- Several tables and figures lack adequate captions; Table 3 has sub-table labels (a) and (b) that are not clearly referenced in the main text.

## Nice-to-Haves
- Implement the TACD framework at least for one benchmark (e.g., compare standard English contamination detection vs. translation-aware detection on a realistic pretraining setting).
- Add statistical significance testing (e.g., bootstrapped confidence intervals, permutation tests) to support claims of monotonicity or difference across conditions.
- Include an ablation with paraphrasing instead of translation to disentangle the effect of language change from the effect of surface-form perturbation.

## Novel Insights
None beyond the paper's own contributions. The empirical observation that fine-tuning on a translated test set yields mixed and often non-monotonic effects on English evaluation performance is not accompanied by a new analytical framework, theoretical result, or reusable detection method that would advance the field beyond existing contamination taxonomies.

## Suggestions
1. Reframe the work as a cautionary study on the difficulty of contamination detection in multilingual settings, rather than claiming a contamination analysis comparable to prior work. Clearly distinguish the fine-tuning-on-test-set scenario from pretraining contamination.
2. Substantially improve statistical rigor: report results over multiple random seeds with standard deviations, and apply simple statistical tests to validate claimed trends.
3. If the TS-Guessing results remain low, explicitly discuss the ceiling effect and calibrate the probe's sensitivity on a positive control (e.g., models known to be contaminated).
4. Either implement TACD on a small scale (e.g., one benchmark, one translation language) or remove the implementation claim and present it purely as future work.

## Score and Decision

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>