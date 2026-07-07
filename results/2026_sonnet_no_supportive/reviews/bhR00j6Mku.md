## Summary
This paper presents the first systematic study of benchmark contamination detection in Large Reasoning Models (LRMs), structured around two contamination scenarios: Stage I, where SFT contamination of the base model is later concealed by GRPO RL training, and Stage II, where CoT contamination applied directly to advanced LRMs produces substantial performance inflation while leaving nearly undetectable traces. The paper spans 10 detection methods across four method families, 6 benchmarks, 2 base models (Stage I), and 4 advanced LRMs (Stage II), and provides both theoretical analysis and controlled ablations identifying PPO-style importance-sampling/clipping as the mechanism behind Stage I concealment.

---

## Strengths
- **Systematic experimental breadth**: 10 detection methods (generation-based, perturbation-based, reference-based, reference-free), 6 benchmarks, and multiple base/advanced models. A finding that persists across all method families and benchmarks simultaneously is far more credible than one limited to a specific method.
- **Clean clipping ablation (Table 3)**: The RAFT vs. RAFT++ vs. GRPO comparison with/without clipping isolates the causal mechanism cleanly. Loss AUROC drops from ~75% to ~57.58% when clipping is enabled in RAFT++ (clipping present vs. absent), while RAFT alone (no IS/clipping) leaves detectability essentially unchanged. This is a controlled experiment, not mere correlation.
- **Stage II log-probability finding (Figure 4)**: Showing that both member and non-member log-probabilities shift upward at similar margins after CoT SFT contamination identifies *why* detection fails (the distributional gap does not materialize), not just that it does.
- **Dual-prong threat established**: Table 4 documents genuine performance inflation (up to +11.76 avg pass@1 for DeepSeek-R1-Distill-Qwen-14B) while Table 5 shows AUROC near 50–65% for almost all detectors, jointly establishing that contamination is real and practically undetectable.
- **Forgetting hypothesis ruled out**: The controlled comparison showing continued SFT on the contaminated model cannot conceal contamination (Figure 2, Appendix Tab. 23) while GRPO can, rules out "more training = forgetting" as an alternative explanation — this is a key methodological contribution that strengthens the claim that GRPO's objective specifically drives concealment.

---

## Weaknesses

### Fatal
None.

### Major
- **Overclaiming "near random" for Stage II**: The abstract and main text repeatedly state that detection "performs near random guesses" in Stage II. Table 5 does not fully support this characterization: LiRA on DeepSeek-R1-Distill-Qwen-14B achieves 65.55% average AUROC (75.56% on AIME25 specifically); Min-K% and Loss on DS Llama-8B reach 62.42% and 62.59%, respectively; some individual-benchmark AUROCs exceed 77%. These are meaningfully above chance and should not be called "random." The defensible claim — "below the AUROC threshold required for reliable deployment-level detection" — is distinct from "statistically indistinguishable from chance" and the paper conflates them. This overstatement appears in the abstract and throughout Section 4, and risks misleading readers about whether the detection problem is fundamentally hopeless or merely inadequately solved with current tools.

### Minor
- **Unverified intermediate step in the theoretical analysis**: Theorem 3.1's key asymmetry depends on the claim (Section 3.2) that "correct paths with higher loss are anomaly and typically got clipped more" for non-members, making Cov(ℓ_k, Σρ_t m_t) more negative for non-members due to "high variance in correct trajectories loss." This variance difference between members and non-members is the critical mechanism but is never directly measured or plotted. The Table 3 ablation validates the aggregate outcome (AUROC drops with clipping) but not the specific mechanism (differential trajectory variance). The theory is useful framing but this intermediate step remains an assertion.
- **Stage I RL-contamination null result underdiscussed**: Table 1 shows RL contamination alone produces no significant performance inflation despite introducing benchmark questions with reward-based feedback. The paper acknowledges this ("contamination inflation mainly comes from SFT") but does not explain *why*. The same GRPO objective claimed to conceal prior SFT contamination apparently cannot produce contamination on its own — these two properties need reconciliation. Is it training-step count? The absence of CoT annotations in RL? The paper offers no analysis.
- **Mild overstatement in Table 2 discussion**: The paper states GRPO "consistently decreases AUROC across all detection methods and benchmarks." Table 2 shows Neighbor increasing from 50.71% to 54.90% (RL w/ Clean&Mem) and Verbatim slightly increasing from 52.76% to 53.35% (RL w/ Clean&Mem). The average AUROCs do decline, but the "consistent across all methods" claim is not precisely supported by individual numbers.

### Trivial
- **GRPO case treated more lightly in theory**: Section 3.2 handles GRPO with "by similar argument" without spelling out the covariance sign explicitly, while RAFT and RAFT++ receive full derivations. Since GRPO is the primary algorithm of interest, an explicit treatment would improve completeness.

---

## Nice-to-Haves
- The paper evaluates contamination at 50% member fraction. Testing smaller fractions (e.g., 10–20%) would clarify whether detection becomes easier at lower contamination rates, which would identify realistic operating regimes for current methods.
- Figure 2 shows a monotone decline in AUROC but the claim that "extensive GRPO training would render all existing detection methods to near-random performance" is stated as expectation. An extrapolation or trend analysis quantifying convergence rate would strengthen this argument.
- Section 4's explanation that LRMs "internalize the underlying knowledge" rather than memorize is plausible but also consistent with a simpler alternative: domain-adaptive fine-tuning uniformly shifts log-probabilities for reasoning-style inputs regardless of membership, a known effect of narrow-distribution SFT. Acknowledging or ruling out this alternative would sharpen the mechanistic claim.
- A brief comparison of the inflation magnitudes in Table 4 to actual ranking margins on public leaderboards would make the practical significance more concrete for readers.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Critic's suggestion to show detection failures permit real-world leaderboard manipulation via actual ranking comparisons**: This is a scope extension, not a methodological flaw. Tables 1 and 4 document inflation magnitudes. The comparison to leaderboard margins is a Nice-to-Have.
- **Critic's note that the SFT-vs-GRPO controlled comparison deserves more prominent treatment**: Figure 2 (main text) already includes GRPO vs. "further SFT" comparison, and the text (Section 3.1) describes the finding explicitly. The appendix-deferred table does not negate this. Not a genuine weakness.

---

## Novel Insights
The paper contributes two genuinely novel mechanistic insights. First, it identifies PPO-style importance-sampling/clipping — not just "more RL training" — as the specific algorithmic feature driving contamination concealment in Stage I, supported by a clean RAFT vs. RAFT++ (±clipping) ablation. This generalizes immediately: any RL algorithm adopting PPO-style clipping inherits this concealment property. Second, it demonstrates in Stage II that advanced LRMs undergoing CoT SFT contamination fail to exhibit the member/non-member log-probability gap that all existing memorization-based detectors rely on, because the model generalizes the probability boost to distributionally similar non-members. This challenges the foundational assumption that benchmark contamination is primarily about memorization and reframes what "contamination" means for LRMs — a qualitative shift from prior work.

---

## Suggestions
- Revise all instances of "near random guesses" in the abstract and Section 4 to language like "below the reliability threshold for deployment-level detection (AUROC ≤ 65% even for the best method)," accurately reflecting Table 5.
- Directly measure and visualize the distribution of trajectory losses for members vs. non-members before and after GRPO, to empirically validate the key variance asymmetry assumed in the Section 3.2 theoretical derivation.
- Add a paragraph in Section 3.1 explaining why RL contamination (Table 1) fails to inflate performance — ruling out the most plausible alternatives (training-step count, absence of CoT, similarity of contamination to clean RL data) would make the mechanistic picture internally consistent.
- Explicitly acknowledge the alternative explanation for Figure 4 (domain-adaptive SFT uniformly shifts log-probabilities for reasoning-type inputs regardless of membership) and provide evidence distinguishing it from the "generalization" interpretation.

---

## Score and Decision

**Calibration Anchors Retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `Nk1MegaPuG.md` | 4.25 | R1 | Similar topic (evading contamination detection), but weaker: no theoretical analysis, poorly organized, short method description — paper under review is substantially stronger |
| `rAylWUIKtu.md` | 4.25 | R1 | Retro-holdout approach to contamination, narrower scope, no RL-specific mechanism — paper under review is broader and more mechanistic |
| `m2NVG4Htxs.md` | 6.75 | R1 | Longitudinal contamination study, strong empirical rigor but limited scope (only cutoff analysis, no theory) — comparable breadth but paper under review has better mechanistic grounding |
| `zWqr3MQuNs.md` | 6.25 | R1 | Detecting pretraining data (Min-K% paper), foundational but narrower — paper under review builds on this and is more specific to LRM setting |
| `hpeyWG1PP6.md` | 5.75 | R1 | TDDBench, a benchmark for training data detection — less novel than the LRM-specific mechanistic findings here |
| `sKYHBTAxVa.md` | 7.33 | R1 | LiveBench (contamination-free benchmark) — different approach, strong community value but simpler mechanistic contribution |
| `jOmk0uS1hl.md` | 8.00 | R1 | "Training on the Test Task" — cleaner framing, stronger claims, very clean experiments — paper under review is somewhat below this tier due to overclaiming and unverified mechanism |
| `Nsms7NeU2x.md` | 6.75 | R2 | "How much can we Forget?" — uses theory + experiments on contamination forgetting, rejected despite high scores from some reviewers — paper under review has more novel findings and better controlled experiments |
| `EUSkm2sVJ6.md` | 7.60 | R1 | Dataset usage cardinality inference — tighter theoretical contribution, but narrower scope — paper under review is broader |

**Round 1 bracket**: 6.5–7.5. The paper is substantially stronger than the 4.25 comparators and somewhat stronger than the 6.75 comparators, but does not reach the 8.0 tier due to the major overclaiming issue and the unverified mechanism.

**Round 2 narrowing**: Among the 6.75–7.5 range, the paper's two clean controlled findings and novel theoretical framing are stronger than both "To the Cutoff" and "How much can we Forget." The overclaiming in Stage II is a real issue but addressable in revision — it doesn't invalidate the core finding. Final score: **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>