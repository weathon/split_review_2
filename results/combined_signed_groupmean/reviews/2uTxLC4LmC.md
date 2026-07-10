## Summary

This paper addresses the problem of unsafe reasoning in Large Reasoning Models (LRMs), where chain-of-thought traces can contain harmful content even when final responses appear safe. The authors first empirically study how safety evolves during reasoning, identifying *safety triggers* (steps after which safe continuation is almost certain) and *compliance cues* (steps strongly correlated with unsafe continuations, Pearson R=0.85). Building on these insights, they propose **Intervened Preference Optimization (IPO)**, which replaces compliance cues in unsafe trajectories with sampled safety triggers, then applies DPO on the resulting preference pairs at the divergence point. Experiments across three LRM families (DS-8B, DS-7B, Qwen3-8B) and three safety benchmarks show consistent improvements: e.g., DS-8B reasoning harmfulness drops from 71.5% to 15.3%, outperforming the best baseline STAR at 22.6%. IPO also preserves/enhances reasoning capabilities on math, coding, and science benchmarks while being more sample-efficient than GRPO (~14 generations vs ~40).

---

## Strengths

1. **The problem gap is convincingly quantified (Section 2.2, Figure 2).** RealSafe-7B exhibits 52.2% harmful reasoning vs 2.4% harmful answers on WildJailbreak. Figure 3 shows that for DS-8B, 40.5% of outputs have unsafe reasoning paired with safe responses. This is persuasive evidence that reasoning-level safety is a distinct and overlooked problem.

2. **The empirical discoveries (Sections 3.1–3.3) are genuine contributions.** The systematic identification of safety triggers, the strong correlation (Pearson R=0.85) between compliance cues and unsafe continuations, and the causal intervention experiment (Figure 6) — where replacing a compliance cue with a safety trigger reduces harmful continuation from 100% to ~15% after 5 iterations — go beyond qualitative observations in prior work.

3. **IPO flows directly from the empirical findings.** Figure 4 shows 36.2% of prompts yield zero safe rollouts, directly explaining why GRPO with group-based advantage estimation underperforms (Table 1 confirms this). IPO's design — artificially creating safe rollouts via intervention and providing a localized preference signal at the divergence point — is a principled solution to a clearly identified bottleneck.

4. **Results in Table 2 are strong and consistent across all settings.** Across three model families and three safety benchmarks, IPO achieves the lowest reasoning harmfulness in every case: DS-8B 15.3% vs STAR 22.6%, DS-7B 18.4% vs GRPO 24.7%, Qwen3-8B 13.9% vs GRPO 23.3%. The improvement is uniform, not cherry-picked.

5. **Efficiency is a practical virtue.** IPO requires ~14 generations per prompt vs GRPO's ~40, and ~40 minutes vs 2+ hours of training time — a genuine advantage that complements the safety gains.

---

## Weaknesses

### Fatal
None.

### Major

1. **Safety trigger pool is derived from only 30 JailbreakBench prompts, with only 6 triggers used for training.** Section 3.1 identifies triggers from 30 prompts on a single benchmark. Section 4.1 then uses only 6 sampled triggers from this pool to construct training data for all 1,000 harmful prompts. The paper provides no analysis of whether this small pool captures sufficient diversity, whether the trigger set saturates with more prompts, or what coverage it achieves on the training data. This does not invalidate the results (which are strong regardless), but it weakens the claim that the trigger-identification process is systematic rather than manual-and-small-scale. The authors should analyze trigger coverage and show performance as a function of pool size.

2. **The training pipeline includes multiple components whose individual contributions are not fully isolated.** Beyond the core IPO (intervention + partial DPO), the pipeline includes (a) an additional DPO stage on benign prompts to mitigate over-refusal, and (b) an auxiliary SFT loss (RPO-style) to stabilize training (Section 4.1). The ablation in Table 3 only compares SFT vs DPO on full trajectories vs DPO on partial trajectories — the over-refusal mitigation and auxiliary SFT loss are not ablated. It is unclear how much these auxiliary components contribute to the final results, or whether the core IPO already delivers most of the gain.

### Minor

3. **Both data construction and evaluation rely on GPT-4o.** Compliance cue detection (Section 3.2, ~80% consistency against manual annotation) and safety evaluation (Section 2.1) both use GPT-4o. The detector ablation (Table 3) shows robustness to different detectors (DS-8B: 19.4%, DeepSeek-R1: 13.6%, GPT-4o: 13.7%), which partially addresses the concern. However, evaluation still uses GPT-4o, creating a potential circularity where the method may learn to satisfy GPT-4o's specific safety judgments. This is a bounded concern — baselines are evaluated identically — but it limits the generality claim.

### Trivial

4. **The "over 30% relative reduction" claim is slightly imprecise.** It holds cleanly for DS-8B vs STAR (32.3%) and Qwen3-8B vs GRPO (40.3%), but is borderline for DS-7B vs STAR (30.6%) and does not hold against GRPO on DS-7B (25.5%). The claim is approximately correct and not misleading, but warrants tightening.

---

## Nice-to-Haves

- **Compare against step-level reward models (safety PRMs).** The paper could benchmark against methods that train a process reward model for safety and use it for RL at each step — a natural competitor for process-level safety alignment. The absence is not fatal given the breadth of comparisons already provided.
- **Show more qualitative before/after reasoning traces.** Beyond Figure 1, showing 3–4 concrete examples where IPO changed the reasoning pattern (e.g., where compliance cues were replaced by safety triggers) would strengthen the claim that IPO genuinely restructures reasoning rather than just learning safe continuations.
- **Analyze distribution shift:** Show whether IPO-trained models generate more safety triggers and fewer compliance cues at inference time, to confirm that training shifts the distribution at the identified critical steps.

---

## Removed Points

These points from the input review are excluded with justification:
- *"Table 1 reports GRPO results with only two reward variants"* — The critic notes this is "acceptable as a motivation," and the paper's contribution is IPO, not a GRPO study. Removed.
- *"The Remark connecting IPO to reward shaping is loose"* — The critic says "this is not a flaw." Removed.
- *"Missing step-level reward model comparison"* — This is a suggestion for expansion, not a criticism of what is presented. Moved to Nice-to-Haves.
- *"Reproducibility dependence on GPT-4o"* — The paper already provides a detector ablation (Table 3); the core concern is covered by Weakness 3. Removed.

---

## Novel Insights

None beyond the paper's own contributions. The review surfaces that the trigger-pool limitation (Weakness 1) is the most impactful concern, but it does not reveal a structural flaw the paper itself does not acknowledge.

---

## Suggestions

1. **Expand trigger-pool analysis:** Report how many distinct safety triggers emerge from the 30-prompt analysis, what fraction of the 1,000 training prompts have their compliance cues successfully matched to a trigger, and whether performance varies with pool size.
2. **Ablate auxiliary components:** Isolate the over-refusal mitigation DPO stage and the auxiliary SFT loss to clarify their contribution. If core IPO already delivers most of the gain, the pipeline is simpler than it appears.
3. **Tighten the "over 30%" claim** to specify the comparator baseline and models for which it holds.

---

## Score and Decision

### Calibration Anchors

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5kMwiMnUip.md` | 1.40 | R1 | No | Weak jailbreaking paper, far below this one |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pXIbcRPxWR.md` | 2.50 | R1 | No | Supervised CoT paper, lower quality and scope |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1OyE9IK0kx.md` | 5.00 | R1 | No | CoT faithfulness paper; less empirical depth |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/O0sQ9CPzai.md` | 6.33 | R1 | No | Tree preference optimization; similar DPO-based approach but no safety focus |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/MoJSnVZ59d.md` | 6.40 | R1 | Yes | SafeDPO: DPO for safety. Lower evaluation breadth; paper here is stronger |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GOoVzE9nSj.md` | 6.50 | R1 | Yes | SaLoRA: safety-preserved fine-tuning. Similar topic but less comprehensive evaluation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/shgx0eqdw6.md` | 7.00 | R2 | Yes | ARGS: decoding-time alignment. Novel but weaker empirical grounding |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TyFrPOKYXw.md` | 7.50 | R2 | Yes | Safe RLHF: decoupled reward/cost models. Comparable scope; both strong |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Bo62NeU6VF.md` | 8.00 | R1 | Yes | Backtracking: generation-time safety. Similar quality; paper here has milder weaknesses |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6Mxhg9PtDE.md` | 9.50 | R1 | Yes | Shallow safety alignment analysis. Higher-scoring but different focus (analysis vs method) |

### Calibration Reasoning

**Round 1 bracket:** Between 6.5 (SaLoRA) and 8.0 (Backtracking). The paper has stronger empirical grounding than SaLoRA (which scored 6.50 with a -9.54 theory weakness) and milder weaknesses than Backtracking (which had a -7.98 comparison weakness). Safe RLHF at 7.50 is the closest anchor: both papers have strong empirical evaluation and high-impact strengths, but this paper's weaknesses (-1.91 max) are far milder than Safe RLHF's (-10.00 for incremental contribution).

**Narrowing (Round 2):** Compared against Safe RLHF (7.50) and Backtracking (8.00). Our paper shares Safe RLHF's thorough evaluation and clear methodology, but has no weakness as severe as "incremental" (-10.00). It has milder weaknesses than Backtracking (-7.98) but is somewhat less novel in mechanism (DPO extension vs a new token-based paradigm). The final placement is between these two anchors.

**Final score: 7.5** — reflecting a strong paper with genuine contributions (novel empirical insights, well-motivated method, comprehensive evaluation) and only mild-to-moderate weaknesses (limited trigger-pool coverage, incomplete ablation of auxiliary components). Neither weakness threatens the core claims, and both are addressable.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>