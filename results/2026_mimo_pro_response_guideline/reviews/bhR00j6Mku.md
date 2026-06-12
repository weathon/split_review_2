Now I have a strong calibration picture. Let me finalize the review.

**Calibration bracket analysis:**

Round 1 brackets found:
- Score band 1.5-3.5: Not topically relevant (jailbreaking papers)
- Score band 3.5-5.5: "Evading Data Contamination Detection" (avg 4.25, rejected) — most topically similar but much weaker than the paper under review (lacks theoretical analysis, weaker experiments)
- Score band 5.5-7.5: "Language Model Detectors Are Easily Optimized Against" (avg 6.00, accepted), "Detecting Pretraining Data" / Min-K% (avg 6.25, accepted), "How much can we Forget" (avg 6.75, rejected), "To the Cutoff" (avg 6.75, accepted), "LiveBench" (avg 7.33, accepted)
- Score band 7.5-8.5: "Proving Test Set Contamination" (avg 7.50, accepted) — stronger theoretical guarantees
- Score band 8.5+: No topically relevant results

Round 2 narrowed bracket to 6.5-7.5. The paper under review is clearly stronger than the 4.25 "Evading" paper (has theoretical analysis with clean ablation, broader evaluation, better structure). It's comparable to or slightly stronger than the 6.0-6.75 papers. The Table 3 ablation directly validating theory is a distinctive strength not present in most comparison papers. But it's slightly weaker than the 7.50 "Proving Test Set Contamination" paper which provides provable guarantees.

**Final score: 7.0** — Strong empirical study with convincing theoretical backing for Stage I, valuable but mechanistically underdeveloped Stage II contribution. The ablation in Table 3 is unusually clean evidence linking theory to practice.

---

## Summary
This paper presents the first systematic study of benchmark contamination detection fragility in Large Reasoning Models (LRMs), identifying two mechanisms through which detection fails: (Stage I) PPO-style clipping in RL training naturally conceals SFT contamination signals, validated through theoretical analysis and clean ablation studies; and (Stage II) CoT-based SFT contamination on advanced LRMs causes detection methods to perform near random guessing due to confidence generalization to unseen similar samples. The study evaluates 10 detection methods across 6 benchmarks and multiple model families.

## Strengths
- **Theoretical derivation with direct empirical validation (Section 3.2, Table 3).** Theorem 3.1 (Eq. 5) decomposes NLL gap dynamics into mean and covariance terms, predicting that PPO-style clipping contracts the member/non-member gap. Table 3 provides a clean ablation: RAFT (no clipping) preserves detection (Δ=+2.03), RAFT++ with clipping destroys it (Δ=−17.91), and removing clipping from both RAFT++ and GRPO restores detection (Δ=−1.09, −2.20). This tight theory-to-experiment pipeline is a genuine methodological contribution.

- **Systematic ruling out of the "simple forgetting" alternative (Section 3.1, Tabs 1-2, Fig 2).** The paper uses two independent experiments: (1) GRPO on clean+contaminated data still conceals while preserving 7.14% performance inflation (Tab 1), and (2) continued SFT on clean data for 4 epochs fails to conceal (Fig 2, Tab 23). This controls for the confound that additional training alone could explain the AUROC drop.

- **Broad and systematic empirical evaluation.** 10 detection methods spanning five categories (generation-based, perturbation-based, reference-based, embedding-based, reference-free) evaluated on 6 reasoning benchmarks and 4+ model variants. This breadth ensures findings are not artifacts of a particular detector or benchmark (Tabs 2, 5).

- **Clean mechanistic story through RAFT → RAFT++ → GRPO progression (Section 3.2).** Each step adds a component and the paper traces the concealment effect, isolating clipping as the specific driver. This is well-structured ablation science.

- **Stage II reveals a fundamental limitation of memorization-based detection (Section 4).** Table 5 shows near-random AUROC across most methods, and Figure 4 demonstrates that log-probs of members and non-members shift upward by similar margins, challenging the core assumption that contamination ≈ memorization.

## Weaknesses

### Fatal
None.

### Major
- **Stage II explanatory mechanism is underdeveloped (Section 4 Discussion, line 330).** The paper argues contaminated LRMs "internalize the underlying knowledge and reasoning process" rather than memorizing sequences. However, the evidence (Figure 4 showing both members and non-members increase in confidence) is equally consistent with the simpler explanation that SFT on high-quality reasoning data from a benchmark improves overall capability on that benchmark type. A control experiment — e.g., SFT-contaminating on one benchmark and testing whether detection fails on a *different* benchmark — would distinguish genuine generalization from generic capability improvement. Without this, the mechanistic claim remains plausible but unproven.

- **The "near random guesses" framing for Stage II is somewhat overstated (Table 5).** While the average AUROC across all models is low, LiRA achieves 65.55% on DS Qwen-14B and 62.74% on OpenThink-7B, with individual cells reaching 75%+ AUROC (AIME24 with DS Llama-8B: 75.33%, AIME25 with DS Qwen-14B: 75.56%). The paper's narrative would be more precise if it acknowledged that LiRA retains partial detection ability on certain model-benchmark combinations while most other methods are indeed near-random.

### Minor
- **Theoretical setup vs. experimental setup mismatch (Section 3.2 vs. Tab 2).** The theory assumes RL training on benchmark data (line 188: "training data is the combination of members M and non-members N"), but the key experiments show concealment also occurs with clean RL data ("RL w/ Clean" in Tab 2). The paper should either extend the analysis to cover the clean-data case or explicitly discuss why the mechanism generalizes beyond the theoretical assumption.

- **No confidence intervals or error bars across runs (Tabs 1-5).** All AUROC values are single numbers. While aggregate patterns are robust, individual cell comparisons (e.g., 52% vs. 58% AUROC in Stage II) cannot be assessed for statistical significance. This is a standard limitation but matters for the Stage II "near random" claim.

- **Limited model scale (7-14B parameters).** All experiments use 7-14B models. The paper does not discuss whether findings would extend to 70B+ frontier models most susceptible to leaderboard pressure. Acknowledging this limitation would strengthen the paper.

## Nice-to-Haves
- A brief discussion of what detection approaches might counteract RL concealment (adaptive defenses) would motivate future work and strengthen the paper's contribution.
- The 50/50 member/non-member split is standard practice, but a sentence acknowledging that in practice developers contaminating entire benchmarks would require cross-benchmark detection would be useful context.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Criticisms about typos/formatting/grammar — parser artifacts, not author issues.
- Generic "missing related work" claims — cannot verify external references exist.
- Reproducibility nitpicks about undisclosed hyperparameters — standard for the field.
- The harsh critic's claim that 77.56% AUROC on AIME24 with DS Qwen-14B belongs to LiRA — verified that this value belongs to the Loss method (line 310), not LiRA. LiRA's actual value on that cell is 66.00% (line 285). The broader point about high individual cells still holds via other verified values (e.g., LiRA 75.33% on AIME24/DS Llama-8B, 75.56% on AIME25/DS Qwen-14B).
- Harsh critic's concern about "confounders" and "proxy metrics" for Stage II — these are generic area sweeps not anchored to specific paper content.

## Novel Insights
The identification of PPO-style clipping as a structural mechanism for contamination concealment is genuinely novel and non-obvious. The insight that a standard training stabilization technique (clipping) has the side effect of destroying the statistical separability between members and non-members — by differentially reducing the covariance term for non-members — provides a clean mechanistic explanation that goes well beyond prior empirical observations about evasion. The Stage II finding that CoT-based contamination generalizes rather than memorizes, challenging the foundational assumption of most detection methods, is also an important observation for the field.

## Suggestions
- Add a control experiment for Stage II: SFT-contaminate on benchmark A and test detection on benchmark B to distinguish generalization from capability improvement.
- Either extend the theoretical analysis to the clean-data RL case or explicitly acknowledge this gap with intuition for why concealment still works.
- Report confidence intervals from multiple random seeds for key AUROC claims.
- Moderate the Stage II framing to acknowledge LiRA's partial detection ability on specific model-benchmark combinations.

## Reporting — Calibration Anchors

**Round 1 anchors:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 8QTpYC4smR.md (Systematic Review of LLMs) | 1.00 | R1 | Irrelevant — low-quality survey, completely different contribution |
| 5kMwiMnUip.md (NEMESIS Jailbreaking) | 1.40 | R1 | Irrelevant — jailbreaking paper with weak methodology |
| lUyYX9VFgA.md (Code-of-thought) | 3.00 | R1 | Weak safety evaluation paper, much less rigorous |
| Nk1MegaPuG.md (Evading Contamination Detection) | 4.25 | R1 | Most topically similar. Same topic but much weaker: no theoretical analysis, poor presentation, simple experiments, overclaimed |
| Vf5ZUalFk8.md (Conformal Reasoning) | 4.75 | R1 | Different topic — uncertainty estimation in interactive environments |
| DIuSX4HqDZ.md (Abductive Logical Reasoning) | 5.00 | R1 | Different topic — knowledge graph reasoning |
| XgYZT35N76.md (VLM CoT Reasoning) | 4.25 | R1 | Different topic — vision-language CoT |
| 4eJDMjYZZG.md (LM Detectors Easily Optimized) | 6.00 | R1 | Related — RL-based evasion of text detectors. Less comprehensive than the paper under review |
| zWqr3MQuNs.md (Detecting Pretraining Data / Min-K%) | 6.25 | R1 | Foundational detection method paper. The paper under review builds on and evaluates this work |
| m2NVG4Htxs.md (To the Cutoff) | 6.75 | R1 | Accepted — longitudinal contamination analysis. Paper under review has stronger technical depth |
| Nsms7NeU2x.md (How much can we Forget) | 6.75 | R1 | Rejected — contamination forgetting study. Paper under review has cleaner theory-ablation pipeline |
| WrBqgoseGL.md (Putnam-AXIOM) | 5.80 | R1 | Tangentially related — benchmark with contamination mitigation |
| sKYHBTAxVa.md (LiveBench) | 7.33 | R1 | Accepted — contamination-free benchmark. Different contribution type |
| KS8mIvetg2.md (Proving Test Set Contamination) | 7.50 | R1 | Accepted — provable guarantees of contamination. Stronger theoretical contribution |

**Round 2 anchors:** Confirmed bracket 6.5-7.5 with repeated hits on the same papers.

**Bracket:** Round 1 placed the paper between 6.5 and 7.5. Round 2 confirmed this range. The paper is clearly stronger than the 4.25 "Evading Detection" paper (which shares the same topic but lacks theoretical analysis and has weaker experiments), comparable to the 6.0-6.75 accepted papers, and slightly below the 7.50 "Proving Test Set Contamination" paper. The Table 3 ablation directly validating theory is a distinctive strength not found in most comparison papers, pushing toward the upper end of the bracket.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <score>Accept</score>