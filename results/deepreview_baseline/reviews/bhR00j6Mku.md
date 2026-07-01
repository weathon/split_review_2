## Summary

This paper presents the first systematic study of benchmark contamination in Large Reasoning Models (LRMs), structured around two contamination scenarios: (I) contamination introduced during the base model's evolution into an LRM via SFT and RL, and (II) contamination applied to an already-advanced LRM as a final SFT step. The authors demonstrate that existing contamination detection methods are alarmingly fragile—RL training (particularly GRPO) can conceal SFT contamination evidence, and SFT contamination with CoT on advanced LRMs leaves barely detectable traces. Through theoretical analysis and controlled experiments, they identify PPO-style importance sampling and clipping as the root cause of concealment in Stage I, and the generalization capacity of LRMs as the confounding factor in Stage II.

## Strengths

- **Timely and important research question.** As LRMs become dominant on leaderboards, understanding whether existing contamination detection methods remain effective is a critical and underexplored problem. The paper addresses a genuine vulnerability in the evaluation ecosystem.

- **Comprehensive empirical evaluation.** The authors evaluate 10 representative detection methods across 6 benchmarks and multiple base models (Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct, DeepSeek-R1-Distill variants, OpenThinker), providing a thorough picture of detection failure modes.

- **Theoretical analysis with empirical validation.** The paper provides a formal analysis (Theorem 3.1) showing that PPO-style importance sampling and clipping drive the contraction of the member/non-member NLL gap, and validates this through controlled ablations (RAFT vs. RAFT++ vs. GRPO, with/without clipping). This moves beyond mere observation to mechanistic understanding.

- **Clear and well-motivated experimental design.** The two-stage contamination framework (pre-LRM and post-LRM) is natural and covers the most practically relevant scenarios. The controlled experiments ruling out "forgetting" as an explanation (further SFT does not conceal, GRPO preserves performance inflation) are well-designed.

## Weaknesses

### Fatal
None.

### Major
- **Limited practical threat assessment.** The paper convincingly shows that detection methods fail, but does not quantify how much undetected contamination would be needed to meaningfully move a model up a leaderboard. The "extensive SFT contamination" in Stage II uses all member data; it would be informative to see a sensitivity analysis showing how detection AUROC degrades as a function of contamination fraction or degree of performance inflation. Without this, the practical severity of the vulnerability is somewhat abstract.

- **The theoretical analysis, while insightful, relies on several strong assumptions** (tabular setting, small step size, idealized advantage formulation for GRPO, focus on correct trajectories only). The connection to practice is supported by the ablation experiments, but the theory's generality is limited. The paper would benefit from a clearer statement of which assumptions are critical and which are for analytical convenience.

- **The "post-LRM" scenario (Stage II) is less deeply analyzed than Stage I.** The explanation that LRMs "internalize the underlying knowledge" rather than memorize is plausible but not directly evidenced. The paper does not attempt to verify whether the model actually generalizes to non-members via reasoning or simply becomes more confident on all distributionally similar inputs. A simple experiment comparing log-prob shifts on out-of-distribution (non-benchmark) questions would help distinguish generalization from mere confidence calibration.

- **The paper does not discuss potential defenses or detection methods that might work.** The conclusion mentions two high-level directions but does not evaluate any candidate approach. While this is acceptable for a paper focused on exposing a vulnerability, the practical impact would be strengthened by at least a preliminary exploration of whether any existing method (e.g., watermarking, dynamic benchmark generation, or probing on held-out reasoning traces) shows promise.

### Minor
- **The paper uses "extensive SFT contamination" in Stage II but does not specify how many epochs or steps this corresponds to** (beyond "extensive"). Table 4 shows performance gains, but the training budget is not reported, making it harder to assess how cheap the attack is.

- **The detection methods are evaluated only on the member/non-member split within the same benchmark.** In practice, a detector might compare across benchmarks (e.g., a model that suspiciously excels on AIME but not on similarly difficult non-benchmark problems). The paper does not explore this cross-benchmark detection signal.

- **The paper focuses on AUROC as the sole detection metric.** While standard, AUROC can be misleading when the base rate of contamination is unknown. Reporting precision-recall curves or TPR at low FPR would give a more complete picture of detection utility.

### Trivial
- The paper uses "Conta" as an abbreviation for "Contamination" in tables and figures; this is clear in context but slightly informal.

## Nice-to-Haves
- A sensitivity analysis showing detection AUROC vs. contamination fraction (e.g., 10%, 25%, 50% of benchmark data contaminated) would greatly strengthen the practical threat assessment.
- An experiment comparing log-prob shifts on non-benchmark, out-of-distribution questions to test whether the Stage II effect is truly generalization or just increased confidence on all inputs.
- A brief discussion of whether any existing detection method (e.g., probing on intermediate activations, or using a held-out verifier) might be robust to the identified concealment mechanisms.

## Novel Insights

The paper's key novel insight is that the training objective itself—specifically, PPO-style importance sampling and clipping—can systematically erase the statistical signals that contamination detectors rely on, even when the model retains the contaminated knowledge (as evidenced by sustained performance inflation). This is fundamentally different from prior work on contamination concealment, which focused on data augmentation (rephrasing) or training dynamics (forgetting). The finding that a "broad class of RL methods" may inherently conceal contamination is a significant and actionable observation for the community. Additionally, the Stage II finding—that LRMs' generalization capacity makes them "naturally" evade memorization-based detectors—challenges a core assumption underlying most existing detection work.

## Suggestions

- Add a sensitivity analysis showing how detection AUROC degrades as a function of the fraction of benchmark data contaminated (e.g., 10%, 25%, 50%, 100%) for at least one representative detection method and one benchmark. This would help readers assess the practical risk.
- For Stage II, include an experiment measuring log-prob shifts on a set of non-benchmark, out-of-distribution questions (e.g., from a different domain) to test whether the observed effect is generalization or just increased confidence on all inputs.
- Clarify the training budget (number of epochs/steps) for the "extensive SFT contamination" in Stage II to make the attack's cost transparent.

## Score and Decision

The paper makes a timely, well-executed, and important contribution to a critical problem in LLM evaluation. The combination of comprehensive empirical evaluation, theoretical analysis, and controlled ablations provides strong evidence for the core claims. The weaknesses (limited threat quantification, less deep analysis of Stage II, no exploration of potential defenses) are real but do not invalidate the paper's main contribution. The paper is clearly above the acceptance threshold and represents a significant step forward in understanding the fragility of benchmark contamination detection in the LRM era.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>