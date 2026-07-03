Now let me produce the final review.

## Summary

SteadyThought (ST) addresses the "under-thinking" problem in Large Reasoning Models (LRMs)—excessive thought switching that wastes computation and abandons promising reasoning paths. ST operates in three stages: (1) entropy-based thought segmentation, (2) thought completion via logit suppression of switch tokens to generate correct trajectories, and (3) thought-level preference optimization (STPO, a SimPO variant conditioned on (Q, T_i)) that teaches the model to commit to promising thoughts. Experiments across DeepSeek-R1-Distill 1.5B/14B and Qwen3-8B on four datasets (including OOD code) show accuracy improvements up to 5.3% with token reductions of 19–39%.

## Strengths

1. **Simultaneous accuracy improvement and token reduction across model scales and architectures (Table 1):** ST improves or maintains accuracy in 11 of 12 model×dataset settings while reducing tokens. E.g., Qwen3-8B on MATH500: accuracy +3.0%, tokens −39.3%. No baseline achieves this combination—NoThink sacrifices accuracy heavily, NOWAIT is inconsistent, and SEAL sometimes increases tokens. The consistency across model families and sizes is a genuine empirical result.

2. **Out-of-distribution generalization to code reasoning (LiveCode):** Training data is purely mathematical (omni-math), yet ST improves LiveCode accuracy by up to 5.3% (Qwen3-8B) while reducing tokens by 19.0%. This demonstrates that ST teaches a generalizable thought-switching discipline, not dataset-specific memorization.

3. **STPO is a principled formalization of the under-thinking problem:** The paper formalizes under-thinking as a preference between "commit" and "switch" trajectories at each thought boundary (Eq. 2), then instantiates STPO (Eq. 7) which conditions on (Q, T_i) rather than the full response. Table 4's ablation (STPO vs. DPO vs. SFT on the same thought-level pairs) shows that STPO's length-normalized thought-level objective drives simultaneous accuracy and efficiency gains, while DPO preserves accuracy but barely cuts tokens, and SFT hurts accuracy.

4. **PCT evidence (Table 2) for the claimed mechanism:** The Proportion of Correct intermediate Thoughts drops consistently after ST training (e.g., DeepSeek-1.5B on MATH500: 54.90% → 40.40%), providing direct behavioral evidence that the model abandons promising thoughts less often.

## Weaknesses

### Fatal
None.

### Major

1. **Missing baseline: whole-response SimPO with the same training data.** Table 4 compares STPO against DPO and SFT on thought-level pairs, but a critical control is absent: standard SimPO applied to *whole-response* preference pairs constructed from the same suppression-generated data. Without this, we cannot determine whether STPO's gains come from (a) thought-level conditioning on (Q, T_i) as claimed, or (b) simply training on high-quality data via any preference optimization method. Since STPO (Eq. 7) is structurally SimPO with the context changed from (Q) to (Q, T_i), the burden is on the authors to demonstrate that thought-level conditioning, not data quality, drives the improvements.

2. **Internal evaluation metrics rely on a segmentation pipeline not validated for trained models.** The in-depth exploration and thinking switching analyses (Section 4.4.1, 4.4.2) use the entropy-based segmentation method from Section 3.1, whose threshold was tuned on the base model. When applied to ST-trained models—which have different entropy dynamics at decision points—the same threshold may systematically bias metrics (thought counts, proportion of last thought, PCT). The paper's mechanistic claims about *why* ST works rest heavily on these metrics. For instance, the DeepSeek-1.5B result on AIME2024 (more thoughts but shorter responses after ST) could partly reflect segmentation fragmentation rather than genuine behavioral change.

3. **NOWAIT baseline on Qwen3-8B is catastrophically poor and unexplained.** NOWAIT on Qwen3-8B: accuracy drops from 91.4% to 61.0% on MATH500 and 62.1% to 26.3% on AIME2024, while tokens *increase* by 84.6% overall—the opposite of what suppression should do. This strongly suggests hyperparameters were not properly tuned for Qwen3-8B. The paper does not discuss this anomaly, which distorts the comparison by making ST look better against an artificially weak baseline.

4. **Confound between data generation mechanism and claimed novelty.** The paper criticizes existing methods for "global" suppression (Section 1), yet Stage 2 generates training data using the same logit-suppression mechanism: "sharply decrease the logits for these [trigger] words…driving their prediction probability close to zero" (Section 3.2). The chosen responses in preference pairs are products of this suppression. While the final model does not use suppression at inference (a genuine difference from NOWAIT/SEAL), the pipeline does not cleanly separate whether ST's gains come from thought-level preference optimization or from distilling suppression behavior into model weights. The missing ablation (Major #1) would help resolve this.

### Minor

1. **No error bars or variance on any accuracy or token numbers.** The paper reports 8 runs for AIME2024 (30 problems, ~3.3% per problem) and 2 for LiveCode, but no standard deviations, confidence intervals, or per-run results are reported anywhere. Several improvements are small enough to be within noise range (e.g., DeepSeek-1.5B GSM8K: 81.9 → 81.3, a decrease). The "Overall" column in Table 1 is an unweighted average across datasets of vastly different sizes (30–1319 problems), which is misleading.

2. **Underspecified training data and hyperparameters.** Training data: "sampled problems from various difficulty levels" from omni-math—how many, what selection strategy? Trigger word list: "e.g., 'wait' and 'alternatively'"—a small hand-picked set that may miss model-specific switch vocabulary. Suppression magnitude: "sharply decrease"—not quantified. Training hyperparameters (learning rate, batch size, epochs) absent from main text. These underspecifications harm reproducibility.

3. **Overweighting of correlational motivation (Figures 1a/1b).** The correlation between more thoughts and later first-correct-thought position is used as primary motivation. But correlation does not establish causation—models with more thoughts may be tackling harder problems, and early correct thoughts do not mean subsequent thoughts are wasteful (they may be verification steps).

### Trivial
None.

## Nice-to-Haves

- Validate the segmentation method on ST-trained models (e.g., human annotation on a subset of 50–100 responses) to address the metric bias concern.
- Quantify inference-time latency savings alongside token reductions.
- Study problems where the initial thought is wrong to directly test whether ST preserves exploration when it is actually needed.
- The SFT baseline's accuracy drop below the base model on MATH500 (80.4% vs. 82.2%) is interesting and deserves analysis: why does fitting to correct-but-suppressed completions hurt accuracy?

## Removed Points

- The Harsh Critic's Critical Issue 1 ("fundamental confound") was downgraded and merged into Major #4. The framing that ST is "the same" as global suppression overlooks the key distinction: ST uses suppression only during data generation, not at inference, and the preference optimization is conditioned on thought prefixes. The criticism has partial merit but was overstated as "fundamental."
- Strength Finder's claim that ST is "a genuinely different approach" was retained but is acknowledged to be in tension with Major #4.
- Various section-by-section nitpicks (e.g., that the SFT result "deserves more analysis") were moved to Nice-to-Haves.
- The critic's point about DeepSeek-1.5B on AIME2024 (Section 4.4.1) was subsumed into Major #2.

## Novel Insights

The paper's central insight—that under-thinking can be addressed by constructing preference pairs at the exact thought-boundary divergence point and optimizing a length-normalized objective conditioned on the promising thought prefix—is genuinely novel and structurally different from prior work that applies global suppression. The consistent pattern across model scales and the OOD generalization to code suggest this approach captures a general principle of reasoning discipline rather than a dataset-specific hack. The PCT evidence (Table 2), while subject to the segmentation confound concern, provides a rare mechanistic look at *why* the method works, going beyond aggregate accuracy numbers. The key open question (which the missing ablation would resolve) is whether the thought-level conditioning is the essential ingredient or whether standard preference optimization on suppression-generated data would suffice.

## Suggestions

1. **Critical:** Add whole-response SimPO trained on the same Stage 2 preference pairs. If STPO outperforms it, the thought-level conditioning claim is supported. If not, the contribution is better characterized as "SimPO with a specific data generation strategy."
2. Validate the segmentation pipeline on ST-trained models using an independent method (human annotation or a held-out model) to ensure the mechanistic metrics (PCT, thought counts) are not artifacts of threshold mismatch.
3. Investigate and explain the NOWAIT collapse on Qwen3-8B; either re-tune its hyperparameters properly or acknowledge the limitation transparently.
4. Report variance (standard deviations or bootstrapped confidence intervals) for all main results, especially AIME2024 (small N) and LiveCode (only 2 runs).
5. Specify training data size, selection strategy, trigger word list, suppression magnitude, and training hyperparameters to improve reproducibility.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>