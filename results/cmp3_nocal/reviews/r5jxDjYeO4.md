## Summary

This paper proposes ASPD, a framework for accelerating LLM inference by identifying and exploiting "intrinsic parallelism" within autoregressive outputs. It has two components: (1) a data pipeline that rewrites serial responses into parallel form with branch structure markup, and (2) an architectural modification (branch-invisible attention masks + shared position IDs + hybrid decoding engine) that enables interleaved serial/parallel decoding within a single model. Experiments on general QA (Vicuna/MT Bench), RAG, and mathematical reasoning (MATH500, AIME) with Vicuna-7B and Qwen2.5-7B/32B show 1.3–1.82× average speedup while maintaining quality close to a sequentially fine-tuned baseline.

## Strengths

1. **The core insight — that LLM responses contain intrinsically parallelizable segments — is genuine and underexploited.** The paper makes a concrete case that not all tokens in an autoregressive response need to be generated sequentially, and validates this by constructing parallel training data and a decoding mechanism to exploit it. This is a worthwhile and well-motivated direction.

2. **The architectural mechanism — branch-invisible attention masks (Eqs. 2–3) with shared position IDs (Eq. 4) — is clean and well-designed.** It specifically addresses two known failure modes of prior work: APAR's discarded KV-caches (quality loss) and PASTA's pre-allocated position ranges (encoding conflicts when branch lengths diverge from predictions). The ablation in §4.4.3 provides clear evidence that the *Same-Seq* position encoding strategy outperforms alternatives, including PASTA's *Predict* approach (7.64 vs. 6.75 on the ablation metric).

3. **The empirical scope is reasonably broad.** Evaluation spans three domains (general dialogue, RAG, mathematics), two model families (Vicuna-7B, Qwen2.5-7B/32B), and multiple prior methods (APAR, APAR*, PASTA, SoT). The math evaluation (Table 2) includes competition-level problems (AIME 2024/2025) where ASPD modestly but consistently outperforms the sequential fine-tuned baseline (e.g., AIME2024: ASPD 62.08 vs. Seq 58.75), suggesting the parallel structure may provide a regularization or reasoning benefit on certain hard tasks.

## Weaknesses

### Major

1. **Figure 1 reports exactly 44% Proportion of Parallel Data across all four datasets — this is not credible as presented and needs explanation.** Lines 28–31 show that ShareGPT Vicuna, MRC, RAG, and Math-220K — four unrelated datasets from different domains — each show identically 44% PPD, while their Degree of Parallelism and Average Branch Number vary. This cannot be rounding noise. Four entirely different datasets producing exactly the same percentage strongly suggests either a systematic error in the pipeline that computes this statistic or a data reporting issue. Since Figure 1 is the paper's primary exhibit for the motivating claim that "model responses consistently reveal significant potential for parallelization" (line 13), this anomaly undermines confidence in the data characterization. The authors must explain how four different datasets yield identical PPD figures, or provide corrected numbers.

### Minor

2. **Section 4.4.2 contains a direct contradiction between the textual claim and the data in Table 4.** The text states: "Our empirical evaluation shows that *Shared* masks consistently outperform *Indep* masks across both *Seq* and *Max* position id configurations" (line 239). Table 4 shows the opposite in both configurations: Indep scores 7.64 vs. Shared's 4.64 under Seq, and Indep scores 6.78 vs. Shared's 3.70 under Max. The concluding sentence ("strongly validates our design decision to maintain strict branch isolation") is correct if read as supporting independent (Indep) masks, so this is almost certainly a swapped-term writing error. But the contradiction as written damages the paper's reliability.

3. **The paper's narrative framing somewhat overstates the quality contribution of the parallel mechanism on Vicuna-7B.** On MT Bench, V-ASPD and V-Seq are identical (5.59 vs. 5.59); on Vicuna Bench, the gap is 0.04 points (7.74 vs. 7.70). The quality improvements over V-Ori come from fine-tuning, while the parallel mechanism preserves those gains while enabling speedup. The abstract's "unprecedented performance in both effectiveness and efficiency" and similar framing could more precisely acknowledge that the quality gains over the original model are attributable to fine-tuning, while the parallel mechanism provides speedup without further quality loss. (On Qwen-7B and math, ASPD does sometimes outperform Seq — this is worth highlighting separately.)

4. **The LLM used in the data pipeline is not identified.** The pipeline (parallel rewriting, independence verification, integrity/answer verification) invokes "an LLM" (lines 105, 117) but never specifies which model. The judge LLM is Qwen3-235B-A22B (line 159), and this model is mentioned for enhancing APAR*'s training data (line 185), but whether the same model is used in the ASPD pipeline is unclear. This is necessary for reproducibility.

5. **No variance or statistical significance is reported for LLM-as-judge scores.** Tables 1–2 report point estimates only. LLM-as-judge evaluations are known to have substantial variance across runs and judge models. Reporting multi-run means with standard deviations (or at minimum, the number of judge calls and the agreement rate) would strengthen the evidence.

6. **The data pipeline yield rate is not reported.** The pipeline has four stages with rejection at each step. The fraction of samples that survive all stages (and whether this biases the training data toward easy-to-parallelize responses) is unknown, making it difficult to assess the pipeline's practical utility.

### Trivial

None.

## Nice-to-Haves

- **Comparison against at least one speculative decoding method** (e.g., Medusa or Eagle on the same Vicuna-7B model) would help practitioners assess ASPD's practical value relative to the dominant acceleration paradigm. The paper mentions speculative decoding as "orthogonal" (line 67) but provides no quantitative comparison.
- **Wall-clock latency measurements** would complement the TPS metric, since practical overheads (mode switching, special token handling) affect end-to-end latency.
- **Analysis of failure cases** — when does ASPD fail to identify parallel segments, or produce incoherent output due to incorrect parallelism?

## Removed Points

These points were raised in the input review but are removed here with justification:

- **"Figure 1 statistics are fabricated"** — The accusation of fabrication is speculative and unsupported by evidence. The factual anomaly (44% across all datasets) is real and is retained as Major weakness 1, but the characterization of fabrication is removed.
- **"P-TPS speedup claims are misleading"** — The paper clearly defines P-TPS (line 159: "TPS in parallel stage") and transparently reports both TPS and P-TPS in Table 3 and line 219. Both metrics are presented side-by-side; there is no inflation.
- **"Missing speculative decoding baselines is a critical gap"** — Speculative decoding is a fundamentally different approach (draft-verify) from exploiting intrinsic parallelism within a single response. The paper scopes itself to the latter. A comparison would strengthen the paper (see Nice-to-Haves) but its absence is not a structural gap.
- **"Section-by-section presentation issues"** (abstract bound on 3.10×, claim about "inherently sequential" token-level constraint, various scope-creep demands) — These are either already addressed in the paper or are minor presentational preferences that do not affect the core contribution.
- **Demands for theoretical proofs of behavioral consistency** — The paper is an empirical systems contribution; theoretical proofs are not standard for this type of work.
- **Formatting/typo/grammar complaints** — Parser artifacts, not author errors.

## Novel Insights

The most useful observation from the input review is the 44% PPD anomaly across four datasets, which the paper does not explain. This is a sharp, data-grounded finding that a careful reader would catch. The second is the precise identification of the writing error in §4.4.2 (text claims Shared > Indep, data shows the opposite). These are specific, verifiable issues that would improve the paper if corrected. Beyond these, no novel insight surfaced that fundamentally reinterprets the paper's contribution.

## Suggestions

1. **Explain the 44% PPD in Figure 1** — provide corrected figures if there is an error, or explain the systematic reason why four different datasets produce identical PPD values.
2. **Correct the swapped "Shared"/"Indep" claim in §4.4.2** to match Table 4.
3. **Specify the pipeline LLM** and report the pipeline yield rate.
4. **Reframe the contribution** to explicitly note that on Vicuna-7B, the quality gains over Ori come from fine-tuning, and the parallel mechanism's role is to preserve those gains while providing speedup. The math results where ASPD exceeds Seq can then be highlighted as a secondary finding.
5. **Add variance information** for the LLM-as-judge scores.

## Score and Decision

The paper addresses a genuine and underexploited direction with a well-motivated technical design. However, the anomalous 44% PPD statistic (Major weakness 1) undermines confidence in the paper's motivating data characterization and requires explanation before the empirical claims can be fully evaluated. The writing error in §4.4.2, while minor, compounds the reliability concern. The remaining issues (pipeline LLM unspecified, missing variance, framing) are addressable. The technical core — speedup with quality preservation — is real and useful. The paper is borderline and would benefit from a revision round that addresses these issues.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>