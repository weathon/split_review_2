## Summary

This paper presents ConCuR, a curated dataset of CUDA kernels with reasoning traces, and KernelCoder, a model fine-tuned on this dataset. The core contribution is a data synthesis-and-curation pipeline that selects kernels based on a conjunction of two criteria: kernel speedup and reasoning trace conciseness (preferring short reasoning). KernelCoder achieves strong results on KernelBench Levels 1 and 2 with only 4,892 SFT samples and 64 A100 GPU hours—dramatically less than RL-based alternatives like Kevin (600+ H200 hours). The paper also proposes using average reasoning length (ARL) as a difficulty metric for kernel generation tasks.

## Strengths

- **A clearly motivated and practical data curation pipeline.** The paper identifies a genuine bottleneck—scarcity of high-quality open-source CUDA kernels for SFT—and builds a synthesis-and-curation pipeline that directly addresses it. The two-criterion curation (speedup and reasoning length) is simple, interpretable, and validated through a clean ablation (Table 4) showing it outperforms random, max-length, min-length, and speedup-only selection. (Favorability: 13.10)

- **Impressive training efficiency.** KernelCoder achieves strong results with only 4,892 training samples and 64 A100 GPU hours, compared to Kevin's 600+ H200 GPU hours and AutoTriton's combined 640 GPU hours (Table 3). This demonstrates that careful SFT data curation can substitute for massive RL computation. (Favorability: 12.23)

- **Well-structured ablation study.** Table 4 provides clean, controlled comparisons isolating the effect of each curation criterion. KernelCoder (combining all criteria) outperforming the 5K-random baseline confirms that the curation logic itself—not just having more data—drives improvement. (Favorability: 11.96)

- **Reasoning length as a difficulty metric is a useful empirical observation.** The finding that ARL correlates broadly with task difficulty across models (Table 7) is interesting and potentially useful for future benchmark design. (Favorability: 11.51)

## Weaknesses

### Fatal
None.

### Major

- **The headline claim that KernelCoder "surpasses all frontier models, including DeepSeek-R1-0528" is contradicted by the paper's own data.** At line 177, the paper states: "Moreover, it surpasses all frontier models, including DeepSeek-R1-0528, GPT-4o, and Claude-4-sonnet." Yet Table 2 (Pass@10) shows DeepSeek-R1-0528 outperforms KernelCoder on Level 2 by both Exec (97.0 vs 95.0) and fast₁ (82.0 vs 68.0). Qwen3-Coder-Plus also beats KernelCoder on Level 1 fast₁ Pass@10 (35.0 vs 32.0). The paper's own evidence contradicts its strongest claim. While KernelCoder does well on Pass@1 and on Level 1 Pass@10, the unqualified "surpasses all frontier models" statement is inaccurate and undermines trust in the paper's framing. (Favorability: -1.21)

- **The causal claim about conciseness is not supported by the evidence presented.** The paper repeatedly frames conciseness as a causal principle ("concise yet informative reasoning traces result in robust generation of high-performance kernels"—line 9; "We argue that conciseness and informative reasoning trace results in a well-performed generated kernel"—line 33) but provides only correlational evidence. Figure 3 shows shorter reasoning correlates with higher correctness, and Figure 2 shows speedup is essentially independent of reasoning length (r=-0.047, R²=0.002). Correlation does not establish causation—easier tasks may naturally produce both shorter reasoning and higher correctness rates, and the paper does not control for task difficulty when making this claim. The curation pipeline works empirically (Table 4), which is valuable, but the causal narrative is not justified by the evidence. The paper would be stronger with a descriptive framing: a joint selection heuristic based on reasoning length and kernel speedup yields better SFT data than single-criterion or random selection. (Favorability: -1.08)

### Minor

- **Evaluation is limited to KernelBench Levels 1 and 2 without reporting any results on Levels 3 and 4.** The paper states (line 146) that Levels 3 and 4 "exceed the capabilities of current LLMs to generate meaningful kernels" and excludes them. Even if all models score 0 or near-0, reporting this would fully bound the SOTA claim. The absence leaves the comparison incomplete. (Favorability: 0.11)

- **No variance or statistical significance information is reported.** All results are presented as single percentages without standard deviations, confidence intervals, or run-to-run variability. With modest task counts (~200 tasks across Levels 1+2), observed differences of a few percentage points (e.g., 95% vs 97%) could be within noise range. (Favorability: 1.69)

- **It is unclear which baseline numbers were reproduced in-house versus taken from prior publications.** Line 177 states "All evaluations are run on a node with 8 RTX 5090 GPUs," but it is ambiguous whether all baseline model results (including DeepSeek-R1-0528 and GPT-4o) were obtained on this same hardware or taken from other papers. Different GPU architectures and driver versions can affect generation quality and timing, making this distinction important for fair comparison. (Favorability: 0.22)

- **The ARL-based difficulty metric shows inconsistencies.** In Table 7, DeepSeek-R1-0528's G_speedup on Medium (2.515) exceeds Easy (1.869), and Qwen3-8B's Hard G_speedup (0.675) exceeds Medium (0.428). This partially undermines the claim that the ARL cleanly separates tasks by difficulty. (Favorability: 1.19)

- **Line 227 speculates that 5K-random's ARL "potentially approaches the optimal reasoning length" without evidence.** No justification or citation supports this claim about optimality. (Favorability: 0.66)

### Trivial
None.

## Nice-to-Haves

- Clarify whether the "first curated dataset of CUDA kernels with reasoning traces" claim (line 283) is specific to the triple format (PyTorch + reasoning + CUDA) versus extending prior synthetic data work like Kevin and AutoTriton.
- Report results on KernelBench Levels 3 and 4 (even if all models score 0) to fully bound the comparison.
- Add variance information (e.g., multiple seeds or bootstrapped confidence intervals) for the main results.

## Removed Points

These points were flagged for removal; treat them with caution:

- Criticism about the paper not releasing the dataset or model weights: removed per hard rule (cited entities are assumed to exist; the appendix was stripped by the parser).
- Criticism about missing appendix content or references: removed per hard rule (the parser strips these sections; they exist in the original submission).
- The reviewer's specific argument that Figure 2 (r=-0.047) "undermines the claim that conciseness drives performance" was partially removed because the paper's conciseness claim is primarily grounded in correctness (Figure 3) rather than speedup (Figure 2). The paper's observation that speedup is independent of reasoning length supports its curation heuristic (selecting for short reasoning + high speedup is feasible because they are independent). The core issue—that the causal framing is unsupported—is retained as a Major weakness above.
- Pure formatting nitpicks removed per hard rule.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the headline claim.** Acknowledge where KernelCoder leads (Pass@1, efficiency, Level 1 Pass@10) and where it lags (Level 2 Pass@10 vs DeepSeek-R1-0528). The efficiency advantage (64 A100 hours vs 600+ H200 hours) is already a strong selling point without exaggerated claims.

2. **Replace the causal conciseness narrative with a descriptive framing.** The evidence supports: "a joint selection heuristic based on reasoning length and kernel speedup yields better SFT data than single-criterion or random selection." This is what the data actually shows and is still a useful contribution.

3. **Report Levels 3 and 4 results** even if they are uniformly low. This would completely bound the SOTA claim and increase the paper's thoroughness.

4. **Specify which baselines were reproduced in-house** versus cited from prior publications to clarify the fairness of the comparison.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 8QTpYC4smR.md | 1.00 | R1 | No | Survey paper; not comparable |
| 5kMwiMnUip.md | 1.40 | R1 | No | Jailbreaking paper; not comparable |
| pXIbcRPxWR.md | 2.50 | R1 | No | Supervised CoT; generic approach, weaker experiments |
| tKFZ53nerQ.md | 2.00 | R1 | No | Text inference; different domain |
| rO8QOHrCeA.md | 4.50 | R1 | Yes | GIFT4Code: synthetic data for code SFT. Weaker ablation, less convincing results than KernelCoder |
| U5TebOVpfd.md | 4.25 | R1 | Yes | CodeDPO: preference learning for code. Significant writing/novelty issues |
| SpTzsQjgxF.md | 5.75 | R1 | Yes | Rule-Based Rating: data curation for LLMs. Cleaner presentation, similar contribution level |
| DKkQtRMowq.md | 5.75 | R1 | Yes | DS^2: data curation for instruction tuning. Strong experiments, comparable contribution |
| ynguffsGfa.md | 6.33 | R1 | Yes | Curated LLM: tabular data augmentation. Similar curation theme, higher score |
| GcJE0HPy4X.md | 6.00 | R1 | Yes | ADC: automatic dataset construction. Mainly engineering contribution |
| Fq8tKtjACC.md | 5.33(R2) / 6.00(avg) | R2 | Yes | **phi-1**: most similar anchor. Curated synthetic data → strong small code model. No overclaiming issues, broader impact |
| suz4utPr9Y.md | 5.75 | R2 | Yes | ENAMEL: efficiency benchmark for LLM code. Clean, accepted |
| rZmQ2z7MPA.md | 5.33 | R2 | No | VERT: hardware verification dataset; different domain |
| QxbJYBZVbE.md | 6.00 | R2 | No | CursorCore: programming assistance; different task |
| w0es2hinsd.md | 5.25 | R2 | No | RD2Bench: R&D benchmark; different domain |

**Round 1 bracket:** 5.0–7.0 (between GIFT4Code at 4.50 and Curated LLM at 6.33).

**Round 2 narrowing:** The closest comparable anchor is **phi-1 (6.00)**, which also demonstrates that curated training data enables small models to achieve competitive results. Compared to phi-1, KernelCoder's strength favorabilities (11.5–13.1) are slightly higher, but its major weaknesses (overclaiming at -1.21, unsupported causal framing at -1.08) target the paper's core narrative credibility—a problem phi-1 did not share. The overclaiming issue is particularly damaging because it is a factual inaccuracy (the paper's own Table 2 contradicts its headline claim), not merely a matter of presentation.

The paper's contribution (data curation pipeline for CUDA kernels, strong efficiency) is solid and places it above reject-level work (scores 1–3) and above papers with weaker experimental validation like GIFT4Code (4.50) and CodeDPO (4.25). However, the overclaiming and causal framing issues prevent it from reaching the 6+ range occupied by papers like phi-1 (6.00) and DS^2 (5.75).

**Final score: 5.5** — The paper has genuine, practically useful contributions validated by clean ablation studies, but the narrative is weakened by unsupported causal claims and a headline result that is contradicted by the paper's own data. These issues are addressable with revisions.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>