## Summary

This paper presents a systematic empirical study of benchmark contamination detection in large reasoning models (LRMs), organized around two realistic contamination scenarios. In Stage I (pre-LRM), contamination introduced during SFT is initially detectable but can be actively concealed by subsequent GRPO training. Through a clean ablation design and supporting theoretical analysis, the paper identifies PPO-style importance-sampling and clipping as the specific algorithmic mechanism responsible. In Stage II (post-LRM), SFT contamination with chain-of-thought on advanced LRMs produces substantial performance gains while leaving minimal detectable evidence, because LRMs generalize to distributionally similar non-members. The paper evaluates 10 detection methods across 6 reasoning benchmarks and multiple model families, providing the most comprehensive study of contamination detection failure in LRMs to date.

## Strengths

- **Clipping-as-concealment mechanism is convincingly isolated.** Table 3 and Fig. 2 provide clean causal evidence: RAFT (no clipping) preserves detectability (77.51% AUROC, +2.03% vs. baseline), while RAFT++ and GRPO (with clipping) sharply reduce it (57.58% and 61.26%, −17.91% and −14.22%). Removing clipping from GRPO restores performance to near-baseline levels (73.28%, −2.20%). This goes beyond demonstrating the phenomenon and pinpoints the specific algorithmic component responsible.

- **The two-stage contamination framework is well-motivated.** Organizing the study around pre-LRM contamination (active concealment via RL training) and post-LRM contamination (inherent undetectability via generalization) captures qualitatively different threat models that existing work conflates, and the paper correctly treats them with different experimental designs.

- **Comprehensive evaluation breadth.** The paper tests 10 detection methods spanning generation-based, perturbation-based, reference-based, and reference-free approaches across 6 reasoning benchmarks (Olympiad, GPQA, AIME25/24, Minerva, AMC23) and multiple base model families (Qwen2.5, Llama-3.1, DeepSeek-R1-Distill, OpenThinker). This breadth makes the negative results harder to dismiss as method- or benchmark-specific.

- **The "more GRPO, less evidence" monotonic trend (Fig. 2).** Showing AUROC decreasing steadily with more RL steps (64 → 110 → 156) is more informative than a single before/after comparison, and enables the argument that at real-world training budgets detection would degrade to near-random performance.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Stage II "near random guess" claim is imprecise.** The paper repeatedly states that detection methods "perform near random guesses (i.e., AUROC ≈ 50%)" in Stage II (abstract, Section 1, Table 5 caption). However, Table 5 shows average AUROCs of 55–65% for several methods — LiRA reaches 65.55% on DS Qwen-14B, Min-K% reaches 59.95%, and Loss reaches 60.23% — with individual entries as high as 77.33% (Min-K% on AIME24 for DS Qwen-14B) and 75.56% (LiRA on AIME25 for DS Qwen-14B). While these values are far too low for practical contamination detection (a correct finding), the characterization as "AUROC ≈ 50%" overstates the data. The evidence supports "well below reliable detection levels" more accurately than "near random guess."

- **Theory-experiment mapping: PPO formalism vs. GRPO experiments.** The theoretical analysis (Section 3.2) is built on PPO constructs — state-value functions *V*(*s*), advantage functions *A*(*s*,*a*), value baselines — and Theorem 3.1 is stated for "a PPO style loss." However, the primary experimental results use GRPO, which computes advantages via group-normalized rewards without a learned value function. The paper acknowledges this in one sentence (line 241: "we consider an idealized setting...") and the empirical ablation (Table 3) independently confirms the clipping mechanism in GRPO. Thus the empirical claim is solid, but the theory overstates its direct applicability to the specific algorithm tested. The paper would benefit from either re-deriving the analysis for GRPO's group-advantage formulation or explicitly framing the theory as a PPO-based intuition verified by the ablation.

- **Stage II explanation is a plausible hypothesis but not uniquely demonstrated.** The paper attributes Stage II detection failure to LRMs "internalizing the underlying knowledge and reasoning process" (line 330) rather than memorizing training sequences, supported by overlapping log-prob distributions (Fig. 4). However, alternative explanations exist: (a) the LRM's extensive pre-training may already cover much benchmark knowledge (reducing the marginal effect of contamination), (b) CoT response diversity may prevent any single sequence from being memorized, or (c) the log-prob overlap may reflect standard fine-tuning generalization rather than something specific to LRMs. The paper does not run controls (e.g., contaminating a non-reasoning model on the same QA pairs) to distinguish these possibilities. This does not weaken the empirical finding that detection fails, but it means the mechanistic explanation for *why* remains underdetermined.

- **No variance or confidence intervals.** All AUROC and pass@1 results are reported as point estimates without standard deviations, confidence intervals, or significance tests. With 8 rollouts per question and random member/non-member splits, sampling noise is present. For key comparisons (e.g., before vs. after RL in Table 2, the 64-step vs. 156-step comparisons in Fig. 2), uncertainty estimates would strengthen the empirical claims, especially where differences are modest.

- **The "broad class of RL methods" claim is stated more confidently than the evidence supports.** The paper tests three methods (RAFT, RAFT++, GRPO), two of which share the importance-sampling/clipping mechanism. Other popular RL methods for LM training (DPO variants, entropy-regularized PPO, rejection sampling without clipping) are not tested. The paper uses hedging language ("suggests," "may inherently," line 255), so this is not a factual error, but the generalization could be tempered.

- **Dense notation in the theory section (lines 170–176).** Multiple quantities (*A*_t, *w*_t, *p*_t, *m*_t, *p*_k(*x*), *q*_k(*s*,*a*), *B*(*s*), *C*(*s*)) are introduced in rapid succession without intuitive glosses, making the derivation hard to follow for readers not deeply familiar with PPO implementation details.

### Trivial
None.

## Nice-to-Haves

- Add a Stage II control: contaminate a non-reasoning model (e.g., Qwen2.5-7B-Instruct without CoT training) on the same QA pairs and measure AUROC. If the non-reasoning model shows larger log-prob gaps, this would directly support the claim that LRMs' generalization capacity is the specific confound.
- Discuss the finding from Table 1 (rows 4–5) that RL contamination alone produces essentially no performance gain — this limits the practical threat model to SFT contamination followed by clean RL concealment, a useful scoping observation.
- Report standard deviations or confidence intervals for key AUROC comparisons (e.g., via bootstrapping over random splits).
- Acknowledge the PPO–GRPO gap explicitly in Section 3.2, stating that the derivation uses PPO formalism for tractability while the ablation confirms the mechanism in GRPO.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Timely and high-stakes problem"** (removed as a generic strength about problem importance, which the rules specify to drop).
- **"First systematic study" claim questioning** (removed per rule that we cannot verify priority claims or question cited references).
- **"50% split for contamination misses 100% contamination scenario"** (removed as an observation, not a weakness; the 50% split is actually a more informative test).
- **"Conclusion proposals are too high-level"** (removed per rule about evaluating papers on their stated scope; this is a problem-finding paper and does not need to propose a complete solution).
- **Covariance argument for RAFT relies on assertion about variance differences** (removed since the paper states this as a reasonable assumption and the theory is backed by the empirical ablation in Table 3).
- **LiRA achieves 65.55% on DS Qwen-14B — not all methods equivalently fail** (merged into the Stage II "near random guess" imprecision point above).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Tighten the Stage II framing: replace "near random guess (AUROC ≈ 50%)" with the actual AUROC range (roughly 46–77%, averages 55–65%) and argue explicitly that this level of detection is insufficient for leaderboard integrity — a claim the data fully support without overstatement.
- Add variance estimates for the key experimental comparisons to improve statistical rigor.
- Clarify in Section 3.2 that the theoretical derivation uses the PPO formalism for analytical tractability and that the GRPO extension is approximate; note that the empirical ablation (Table 3) independently verifies the mechanism for GRPO despite architectural differences.
- Add a control experiment for Stage II to strengthen the mechanistic explanation.

## Score and Decision

**Calibration anchors (all from the deepreview_13k_calibration corpus):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `Evading Data Contamination Detection for Language Models is (too) Easy` (Nk1MegaPuG) | 4.25 | R1 bracketing | Most directly comparable paper: same topic (evading contamination detection) but proposes a specific attack method. Had significant presentation and technical depth weaknesses. The current paper is substantially stronger in experimental design, breadth, and rigor. |
| `Benchmark Inflation: Revealing LLM Performance Gaps Using Retro-Holdouts` (rAylWUIKtu) | 4.25 | R1 bracketing | Methodological paper with narrow scope (TruthfulQA only). Current paper is more comprehensive. |
| `Detecting Pretraining Data from Large Language Models` (zWqr3MQuNs) | 6.25 | R1 bracketing | Proposed novel detection method with strong empirical validation. Comparable in quality but different contribution type (method proposal vs. empirical study). |
| `How much can we Forget about Data Contamination?` (Nsms7NeU2x) | 6.75 | R1 bracketing | Strong theoretical + empirical paper about contamination forgetting. Had concerns about theory applicability but was well-regarded. Current paper is similarly thorough. |
| `To the Cutoff... and Beyond?` (m2NVG4Htxs) | 6.75 | R1 bracketing | Pure empirical analysis (no new method), similar to current paper's contribution type. Accepted. Current paper is more comprehensive (two stages, more models/methods). |

**Round 1 bracket:** [5.5, 7.5] — based on comparison with anchors: clearly stronger than the 4.25 papers, competitive with the 6.25–6.75 papers.

**Narrowing:** The paper's Stage I finding (clipping mechanism) is well-supported by a clean ablation, comparable to the empirical rigor of the 6.75 anchors. The Stage II finding is directionally correct but has framing imprecision and an underdetermined mechanistic explanation. The theory–experiment mapping gap is real but addressable and does not invalidate the empirical core. Overall, the contribution is significant and timely, with minor weaknesses in precision and mechanism explanation.

**Final score: 6.5** — borderline accept. The paper convincingly demonstrates a genuine vulnerability, provides a clean causal isolation of the concealment mechanism in Stage I, and covers impressive breadth. The weaknesses (imprecise Stage II framing, PPO–GRPO theory gap, speculative Stage II mechanism, lack of variance estimates) are all addressable and do not undermine the core empirical findings.

**Decision: Accept**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>