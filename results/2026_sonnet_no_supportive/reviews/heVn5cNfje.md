Now I have enough to draft the review. Let me call `draft_review`.**Round 1 bracket:** The paper sits between the 5.75–7.0 range based on comparable anchors. The contribution is empirically solid with no fatal flaws, but has two genuine Major weaknesses (length confound, hyperparameter tuned on eval benchmarks). Initial bracket: **6.0–7.0**.

**Round 2 narrowing:** The closest thematic match is `3OyaXFQuDl.md` (avg 7.0, "Smaller, Weaker, Yet Better: Training LLM Reasoners via Compute-Optimal Sampling"), which similarly proposes principled data selection strategies for LLM reasoning with comprehensive experiments. This paper has comparable empirical breadth but notable methodological gaps. The `SpTzsQjgxF` paper (5.75) is a weaker contribution with less comprehensive validation. This paper is stronger than 5.75 but the two Major weaknesses keep it below 7.0. **Final score: 6.5**.

---

## Summary
This paper introduces High-Entropy Sum (HES), a training-free metric that sums the top 0.5% highest-entropy tokens in a reasoning response to quantify "forking-point" complexity. HES is applied as a unified data selection signal across three training paradigms (SFT, RFT, RL) and validated across math, code, and STEM domains, showing that pruning the 20% lowest-HES data consistently improves over full-dataset training.

## Strengths
- **Discriminability concretely demonstrated.** Figure 1 and the accompanying table show a large separation between correct/incorrect responses under HES (normalized means 0.29 vs. 0.68) while average entropy over all tokens is essentially uninformative (0.52 vs. 0.53). The comparison is fair and the gap is substantial.
- **Counter-intuitive 80%-pruning result, replicated across four settings.** Table 1: Highest-HES-80% achieves 35.36% vs. Full-Dataset 32.61% (+2.75 pts); replicated on OpenR1-220k (Table 2: 32.35% vs. 30.22%), code (Table 3), and STEM (Table 4). The consistent finding that low-HES data is *actively harmful* — not merely uninformative — is substantive and practically actionable.
- **Cross-model proxy transfer is directly useful.** Table 1 shows Qwen3-0.6B scoring for 8B training achieves comparable selection quality (32.12% vs. 31.14% for self-scoring), reducing inference cost by over an order of magnitude. This result implies HES captures dataset-level complexity rather than model-specific uncertainty.
- **Asymmetric RL design validated by ablation.** Table 6 demonstrates that Pos-High, Neg-Low (19.50%) performs *worse* than the proposed Pos-High, Neg-Rand (21.30%), confirming the specific asymmetric design is non-obvious and the ablation table is comprehensive.

## Weaknesses

### Fatal
None.

### Major
- **HES and sequence length are not properly disentangled.** HES_relative sums the top p=0.5% tokens by percentile within each response. A 4,000-token response contributes 20 high-entropy tokens; an 8,000-token response contributes 40 — longer responses mechanically produce higher HES. The advantage over the Length baseline is only 31.14% vs. 30.67% = 0.47 pts (Table 1), and the advantage over Highest-ES (total entropy sum, also length-correlated) is 31.14% vs. 30.92% = 0.22 pts — both slender. The paper does not report sequence-length distributions within selected subsets, so the causal mechanism — that HES captures "forking complexity" beyond a simple length effect — is not established. While footnote 1 argues the relative threshold "makes this metric robust to variations in length," this is not a length-disentanglement argument; it simply normalizes within each sample, not across them.

- **Hyperparameter p selected on the evaluation benchmarks.** The sensitivity analysis (Figures 3 and 4) identifies p=0.005 as optimal using AIME 2024, AIME 2025, and HMMT 2025 — the same benchmarks that appear as primary evaluation targets in Table 1. This creates a circularity: p was effectively tuned on the evaluation set. The generalization to Code (LiveBench, AIME25, GPQA) and STEM (MMLU, GPQA, HMMT25) domains partially mitigates this, but the core math tuning/evaluation overlap remains a methodological concern that limits the credibility of "p=0.5% generalizes robustly."

### Minor
- **RL results overclaimed.** Section 4.3.2 and the abstract state that Pos-High, Neg-Rand "significantly surpasses existing training-free selection methods" and the Full-Batch. Table 6 shows the average gain over Full-Batch is 21.30% − 20.63% = 0.67 points. On HMMT25 specifically, the proposed method (11.88%) is notably *below* Full-Batch (15.21%). No variance across training seeds is reported. Given benchmark variance at 16 sampling paths per problem on small problem sets, the word "significantly" is not defensible for margins of this size. The directional finding may still be correct, but the framing is stronger than the evidence warrants.

- **RL experiments limited to 1.5B model.** SFT and RFT use 7B/8B models; RL is conducted only on DeepSeek-R1-Distilled-Qwen-1.5B (Table 6). Whether the asymmetric HES sampling strategy generalizes to larger-scale RL training targets, the practical use case, is unverified.

- **Abstract slightly overstates 20%-selection result.** The abstract states 20% HES data "matches full-dataset performance." Table 1 shows 31.14% vs. 32.61% — a 1.47-point gap. The stronger claim — that Highest-HES-80% *surpasses* the full dataset — is the more accurate and compelling finding.

### Trivial
- **Duplicate paragraph in Section 4.2.** The paragraph beginning "HES shows robust performance in both Per-Query and Global Pool settings" appears verbatim at two locations (the paragraph appears to have been copy-pasted). Manuscript error.
- **Self-referential typo in Equation 3 definition.** Section 3.1 states: "It is designed to isolate the average complexity of key-fork tokens, different from AvgHE." This should read "different from HES."

## Nice-to-Haves
- Report average response length within each selected subset (Highest-HES-20%, Highest-ES-20%, Length-20%, Random-20%) and show HES advantage persists in length-matched buckets. This would make the "forking point" narrative compelling rather than suggestive.
- Report variance across RL training seeds; the HMMT25 regression in Table 6 deserves discussion — whether it is sampling noise or systematic.
- Qualitative analysis of the lowest-HES samples (are they degenerate outputs, trivial problems, templated solutions?) would give practitioners concrete intuition for the "low-HES data is harmful" finding.
- Wall-clock or FLOPs comparison: HES scoring vs. reward model inference vs. LLM-as-judge would concretize the efficiency claim beyond the proxy-model argument.
- Conduct the hyperparameter sensitivity sweep on a held-out dataset to establish that p=0.005 truly generalizes.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Table 1 bolding inconsistency**: The reviewer noted confusion in the bolding scheme. Examining the table, the bolding within certain rows (e.g., Medium-Difficulty) appears to indicate within-row bests among certain groupings, not column bests — a presentation choice that is confusing but does not affect conclusions. Removed as below-trivial threshold.
- **Claim that OpenR1-80% does not clearly beat full dataset**: The reviewer noted Highest-HES-80% on OpenR1-220k (32.35%) vs. Full-Dataset (30.22%) is a +2.13 pt gain, which the paper presents as consistency. This is a valid result; the claim holds. The reviewer's framing as a weakness is removed.
- **Missing compute time / FLOPs**: Removed as trivial (proxy model transfer results already address the core efficiency argument; absolute wall-clock numbers are a nice-to-have, not a methodological gap).

## Novel Insights
The most robust and actionable novel finding is that low-HES data is *actively harmful* — not merely less useful — across all three training paradigms and four domains. This is replicated eight times across Tables 1–4. The cross-model proxy transfer result adds a further insight: because a 0.6B model and an 8B model produce statistically equivalent HES rankings, HES appears to capture intrinsic data complexity rather than model-specific uncertainty distributions. Together, these two findings suggest that token-level entropy structure is a more fundamental quality signal than outcome-based proxies, and that even a small model can serve as a reliable "data difficulty auditor" for much larger training runs.

## Suggestions
1. Add sequence-length distributions per selected subset and a length-controlled comparison (within-length-bucket HES vs. Random) to disentangle the length-confound.
2. Run the hyperparameter sensitivity sweep on a strictly held-out dataset (e.g., a domain not used in main evaluation) to validate p=0.005 generalization.
3. Report at least 2–3 RL training seeds and recalibrate the language from "significantly" to "modestly" or "consistently" for the 0.67-point RL margin.
4. Fix the duplicate paragraph and AvgHE self-reference typo.
5. Add an analysis of the characteristics of Lowest-HES samples to sharpen the "harmful data" narrative.

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `Uj0h13lVrR.md` | 1.00 | 1 | Weak GFlowNet paper; far below this work |
| `OdoS6cH8MP.md` | 2.00 | 1 | Simple embedding-based data valuation; less rigorous |
| `z3DMFpaP6m.md` | 3.00 | 1 | Entropy metric for LLM semantics, narrow scope |
| `qUJsX3XMBH.md` | 4.40 | 1 | Data selection at scale, argues random selection is sufficient; negative result, less contribution |
| `OegBJMucyM.md` | 4.25 | 1 | Pre-memorization accuracy predictor; narrower scope |
| `SpTzsQjgxF.md` | 5.75 | 1 | Rule-based data selection for LLMs; similar topic, less empirical breadth |
| `huuKoVQnB0.md` | 6.00 | 1 | Perplexity-correlation data selection; comparable contribution level |
| `ouRX6A8RQJ.md` | 6.40 | 1 | CoT analysis via information theory; narrower than this paper |
| `3OyaXFQuDl.md` | 7.00 | 1 | "Smaller, Weaker, Yet Better" — most thematically similar; comparable empirical breadth and practical impact |
| `f4gF6AIHRy.md` | 8.00 | 1 | Submodular pretraining data selection with strong theoretical grounding; stronger than this work |
| `WJaUkwci9o.md` | 8.00 | 1 | Self-improvement sharpening mechanism; strong theoretical + empirical |
| `WrBqgoseGL.md` | 5.80 | 2 | Putnam benchmark paper; different contribution type |
| `GtpubstM1D.md` | 5.71 | 2 | Math data synthesis/stages study; comparable breadth, less focused |
| `yaqPf0KAlN.md` | 6.75 | 2 | Olympiad-level benchmark; different contribution type |
| `nDvgHIBRxQ.md` | 6.25 | 2 | MathCheck evaluation; different contribution type |
| `KUNzEQMWU7.md` | 7.25 | 2 | MathVista multimodal benchmark; different contribution |

**Bracket:** Round 1 set 6.0–7.0. Round 2 confirmed: closest thematic anchor is `3OyaXFQuDl` (7.0), which has more theoretical grounding. The two Major weaknesses (length confound, eval-set hyperparameter tuning) pull this below 7.0. The strong empirical evidence across paradigms and domains, practical proxy-transfer result, and concrete findings about harmful data keep it above 6.0. **Final score: 6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>