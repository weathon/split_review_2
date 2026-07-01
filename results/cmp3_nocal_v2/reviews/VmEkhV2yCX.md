Now I have all the information I need to write the final consolidated review. Let me produce it.

---

## Summary

This paper studies whether and how reasoning data should be introduced during pretraining vs. post-training (SFT/RL). The authors train 8B models from scratch for 1T tokens with varying reasoning data configurations (diverse/large-scale vs. high-quality/small-scale), then apply SFT and RL. They report three main findings: (1) front-loading reasoning into pretraining yields a compounding 19% gain after RL; (2) an asymmetric principle — diversity matters more in pretraining (11% gain), quality matters more in SFT (15% gain); (3) high-quality pretraining data can have latent benefits unlocked by SFT, and naively scaling SFT data can be harmful.

## Strengths

- **Large-scale end-to-end pretraining experiments.** Training 8B models from scratch for 1T tokens with controlled data ablations (512 H100s) is computationally expensive and rare. The scale of these experiments provides empirical evidence that small-scale studies cannot.

- **Multi-stage evaluation design.** The three-phase pipeline (pretraining → SFT → RL) is well-suited to the research question. The RL result (Table 3: 56.66 vs. 37.92, an 18.74 point gap) is the most compelling finding — it demonstrates that the pretraining advantage compounds through post-training and is largest on the hardest benchmarks (AIME24/25).

- **Clean ablation of SFT data scaling.** Table 8 provides a useful counterpoint to naive scaling: naively doubling mixed-quality SFT data (D_LDQ) harms math reasoning (28.38 → 23.46 on MATH), while a 0.4% addition of high-quality data (D_ALF*) improves it. This is a clean, practically relevant finding.

## Weaknesses

### Major

- **The diversity vs. quality comparison in pretraining is confounded by repetition rate.** The paper's central claim — "pretraining benefits most from broad diversity" — rests primarily on comparing M_LDQ (trained on D_LDQ: 268M unique samples) against M_SHQ (trained on D_SHQ: 1.2M unique samples). Both use a fixed budget of 80B reasoning tokens (Section 2.3), meaning D_SHQ is repeated orders of magnitude more times than D_LDQ. The paper states "When a reasoning dataset is small, it is repeated" (line 93) but never discusses this as a confound. The key question is whether M_LDQ outperforms M_SHQ because D_LDQ is more diverse or because D_SHQ's extreme repetition causes the model to overfit / memorize surface patterns. This confound runs through every claim attributing pretraining gains to "diversity" specifically. The same issue also affects the latent-advantage finding (M_LMQ > M_LDQ post-SFT, line 215), which could partly reflect the repeated D_SHQ portion of D_LMQ being memorized rather than a general "quality" benefit.

### Minor

- **Limited test of the "catch-up" hypothesis.** The paper tests catch-up by doubling SFT epochs on M_base (Table 4: 2× epochs reaches 34.01, still below M_SHQ+SFT_SHQ at 37.33). Doubling epochs is a single, modest intervention. The claim that SFT "cannot fully replicate" pretraining advantages (line 213) overstates what a single 2× epoch comparison supports. A stronger test would involve more aggressive SFT data scaling, curricula, or multiple SFT rounds.

- **RL comparison is too narrow to support the full claim.** Table 3 compares only two conditions (M_base+SFT_SHQ+RL vs. M_LMQ+SFT_SHQ+RL). The paper concludes that "pretraining strategy dictates final accuracy on expert-level tasks" (line 193). While the RL results are striking, with only two data points they constitute a case study rather than systematic evidence. RL results from additional pretraining conditions (e.g., M_SHQ, M_LDQ) would substantially strengthen this claim.

- **No statistical precision reported for any result.** All tables report point estimates without standard deviations, confidence intervals, or measures of variance. While the paper averages multiple evaluation runs (16 for AIME, 4 for others), no variance is reported. Many comparisons involve small margins (e.g., 60/40 vs. 80/20 in Table 6: 67.28 vs. 64.07), making it impossible to assess which differences are reliable.

- **No discussion of potential data contamination.** The SFT data D_SHQ (Guha et al., 2025) covers 71% math, 21% code, and 8% science — the very domains of the evaluation benchmarks (AIME24/25, MATH-500, GSM8K, GPQA-Diamond, LiveCodeBench). The paper does not check or discuss whether the SFT datasets contain solutions to evaluation problems, which could inflate the SFT and RL results.

### Trivial

None.

## Nice-to-Haves

- Include standard deviations for the main comparisons, especially where margins are small (e.g., Table 6 ratio sensitivity).
- Run a more thorough catch-up test (e.g., 5× or 10× SFT data, multiple SFT rounds) to strengthen the claim.
- Extend the RL comparison to cover at least M_SHQ and M_LDQ in addition to the two existing conditions.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Criticism about the 19% figure being "the most extreme comparison"* — removed because the paper transparently reports this as the RL-phase result, not misleadingly. The 19% comes from the full pipeline (PT+SFT+RL), which is the most practically relevant comparison.
- *Criticism about the two-phase pretraining schedule (600B/400B) being unusual* — removed because the paper explains the schedule choice, and it is applied consistently across all conditions; there is no evidence it biases the comparisons.
- *Generic strength about "scientifically important question"* — removed because it is generic and applies to many papers; not specific enough to this paper's execution.
- *Criticism about Table 5 SFT comparison being confounded* — partially removed because the paper states "each 8B LLM is finetuned on 4.8M reasoning samples from D_res" (line 124), but whether this refers to unique samples or total samples processed is ambiguous without the appendix. The ambiguity itself is a minor presentation issue, but the severity claimed by the reviewer (that D_LDQ at 0.018 epochs vs D_SHQ at 4 epochs would invalidate the comparison) depends on an interpretation that may not match the actual training procedure. Left ambiguous in the available text.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's key observation — that the repetition confound severely weakens the "diversity matters in pretraining" claim — is the most valuable signal for the authors. The paper's other contributions (front-loading helps, RL compounding, SFT quality sensitivity, naive scaling harms) are supported and useful, but are incremental extensions of existing knowledge rather than novel discoveries.

## Suggestions

1. **Address the repetition confound directly.** Either (a) run a controlled experiment where D_SHQ is subsampled from D_LDQ to match in number of unique examples, or (b) upsample D_LDQ to match D_SHQ's repetition rate, or (c) at minimum discuss the confound explicitly and estimate its direction. This is the single biggest threat to the paper's central claim.

2. **Add error bars** to all main tables, using the multiple evaluation runs already collected.

3. **Check for benchmark contamination** in the SFT datasets and report overlap rates.

4. **Tone down the catch-up claim** from "cannot be fully replicated" to "cannot be replicated by a simple 2× epoch increase" unless stronger evidence is added.

5. **Clarify the SFT training setup** — specify whether the 4.8M "samples" are unique or total, and whether gradient steps / tokens seen are controlled across different SFT datasets.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>