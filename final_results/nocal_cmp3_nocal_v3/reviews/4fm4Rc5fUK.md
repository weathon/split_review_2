## Summary

This paper proposes ATF (Autoformalizer with Tool Feedback), a framework that augments a learned formalizer with external tools — a Lean 4 compiler for syntax checking and a multi-LLM-as-judge for semantic consistency checking — and trains the model to iteratively refine formal statements based on tool feedback. The training pipeline has three stages (cold start on synthetic tool-calling trajectories, expert iteration, and DPO to reduce ineffective revisions). Experiments across three benchmarks show strong gains over existing formalizers (e.g., 29.13 percentage point improvement on CombiBench consistency), with human evaluation confirming the trends and an open-source dataset of 750K formal statements released.

## Strengths

1. **Well-motivated problem decomposition and clean solution.** The paper correctly identifies that existing formalizers fail on two distinct axes — syntactic validity (~37–40% failure rate reported for state-of-the-art models) and semantic consistency (subtle misalignments like swapped quantifiers or wrong constants). The tool-feedback loop directly targets both failure modes by giving the model access to compiler errors and consistency judgments during generation — a natural and sensible attack.

2. **Thoughtful engineering of the syntax check tool.** The grouped Lean 4 execution (Section 3.1.1, Figure 3) is a practical contribution: batching code by import library and mapping results by line number substantially reduces the overhead of compiler calls, which would otherwise be prohibitive at training scale. The pre-check stage further filters trivial errors before compilation. These design details matter for whether the approach is viable in practice.

3. **Consistent empirical gains across all benchmarks with human validation.** In Table 3, ATF-32B outperforms every baseline on every metric across all three datasets. The gains are large on the hardest benchmark (CombiBench consistency: 65.38% vs. 36.25% at Pass@1) and meaningful even on the easiest. The 8B distilled model also beats most 32B baselines. Human evaluation on 100 samples per benchmark with 3 expert annotators confirms the rank ordering, and the Pearson correlation of 0.746 between tool-based and human-based consistency scores provides evidence that the automated judge captures something real.

4. **Clean ablation study isolating each component.** Table 4 cleanly separates the contributions of each tool and training stage: without tools, performance is poor (23.69% CombiBench CC at best); syntax check alone improves it; both tools improve further; and the three training stages (cold start → expert iteration → DPO) each add incremental value. This makes the method's success interpretable rather than a black box.

5. **Open-source dataset contribution.** The release of Numina-ATF (750K formal statements synthesized from Numina-v1.5 queries) is a concrete resource that supports reproducibility and future work in autoformalization and ATP.

## Weaknesses

### Fatal

None.

### Major

1. **Evaluation metric circularity between training signal and headline results.** The primary consistency metric (CC in Table 3) is measured using the same multi-LLMs-as-judge tool that ATF was trained to satisfy. Section 4.1 states that evaluation uses "the tools designed above" — i.e., the same syntax and consistency checks. The training pipeline (cold start, expert iteration, DPO) all filter and score data using this judge. The baselines (Kimina, StepFun, Goedel-V2) were trained on static datasets without access to this judge. This creates a systematic advantage: ATF is optimized to produce statements that pass *this specific judge*, while baselines are not. The paper partially addresses this with human evaluation (100 samples per benchmark, 3 expert annotators), but the sample is small — for FormalMath-Lite the human-evaluated gap is only 3% (95% vs. 92%), which is within the margin of error for 100 binomial samples. While the CombiBench human gap (49% vs. 22%, a 27-point difference) is clearly beyond sampling noise, the main quantitative claims in the abstract and Section 4.2 rest on the automated metric. **Why it matters:** The headline comparisons are systematically biased in ATF's favor. Reporting confidence intervals on the automated metric or a larger human evaluation sample would substantially strengthen the evidence.

2. **Inference cost asymmetry is not accounted for, making the comparison unequal.** ATF uses iterative refinement with tool feedback at inference time. A single formalization involves: initial generation, syntax check via Lean 4 compiler (potentially re-batched), possible revision and re-check, consistency check via two 32B LLMs, possible revision and re-check. The paper states that "max revision attempts < 4 which results in output lengths roughly equivalent to those of Goedel-V2-Formalizer-32B" — but this comparison is about *generated token count*, which is the wrong quantity. The actual cost includes multiple Lean 4 compiler executions (up to ~8 for a single successful formalization on CombiBench, as shown in Figure 5a) and consistency checks requiring inference from two 32B LLMs. The baselines generate once without any tool calls. **Why it matters:** Framing the comparison as "ATF outperforms baselines" without transparently accounting for this cost differential conflates a capability advantage with a compute-budget advantage. A system that trades compute for accuracy is still valuable, but the paper should explicitly report the total inference cost per successful formalization or compare baselines with the same tool access.

### Minor

3. **DPO preference signal conflates efficiency with quality.** Section 3.2 defines positive samples as trajectories with *fewer* revision attempts and negative samples as those with more attempts (difference ≥ 3). The assumption that fewer revisions implies better formalizations is unvalidated. A fast trajectory could produce a statement that passes both checks but captures a narrower or simpler interpretation of the original problem. The paper does not analyze whether faster trajectories produce semantically narrower results.

4. **Decontamination procedure is mentioned but opaque.** Section 4.1 states that "similarity-based decontamination" was performed on all training data against evaluation sets, but provides no details about the method, similarity threshold, or results. For a paper making claims about generalization (especially OOD performance on CombiBench), this omission makes it difficult to assess whether data leakage could contribute to the reported gains.

5. **Consistency check judge is only benchmarked on two open-source models.** Table 1 evaluates only QWQ-32B and Qwen3-32B for the consistency check role. No comparison against stronger models (e.g., GPT-4o, Claude) is provided. While using open-source models is a reasonable design choice, the ensemble achieves a recall of only 0.5967 (missing ~40% of inconsistent statements). The paper does not characterize the failure modes of the judge or validate it against human judgments beyond the 100-sample correlation.

6. **Cold-start training depends on a proprietary model.** The cold-start trajectories (Section 3.2) are generated by Claude-4-Sonnet, which is not open-source. While the released Numina-ATF dataset provides the resulting data, researchers cannot reproduce or modify this training stage. The paper does not discuss this limitation.

### Trivial

None.

## Nice-to-Haves

- **Error analysis of remaining failures.** The paper reports aggregate pass rates but never analyzes *what kinds* of errors persist (e.g., quantification errors vs. missing lemmas vs. structural misalignments). A breakdown of failure modes would be substantially more informative than the aggregate numbers.
- **Downstream theorem proving validation.** Showing that ATF-formalized statements lead to higher proof success rates would make the practical significance of the consistency gains concrete and connect the contribution to the stated end goal of ATP.
- **Cost-aware comparison.** Reporting total compute (FLOPs or approximate GPU-hours) per successful formalization for ATF vs. baselines would make the accuracy–cost trade-off explicit.
- **Larger human evaluation sample.** The current 100 samples per benchmark limits statistical resolution, especially for the smaller gaps on FormalMath-Lite and ProverBench.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"Figure 1 caption appears three times"* and *"poorly formatted in the text"* — These are PDF-extraction artifacts (parser issues), not author errors.
- *"63% remaining contradicts approximately 40% fail syntax"* — 37% (100% − 63%) is approximately 40%. This is not a contradiction.
- *"y-axis in Figure 4b starts at ~88%, making the improvement look more dramatic"* — Starting axes above zero is a common visualization choice and does not misrepresent the data.
- *"29.13% framing needs more precise wording"* — The improvement is an absolute percentage-point difference (65.38 − 36.25 = 29.13), which is a standard reporting convention. The numbers check out.
- *"No error analysis" / "no downstream theorem proving"* — These are scope extensions, not flaws in what the paper actually claims. Error analysis would strengthen the paper but its absence does not weaken the existing contribution.
- *"No limitations section"* — The paper does not have a formal limitations section, but relevant constraints (recall sacrifice of the ensemble judge, proprietary cold-start model, limited to Lean 4) are stated or implied in the main text. This is a structural preference, not a substantive omission.

## Novel Insights

The harsh reviewer's most insightful observation is the evaluation circularity concern — that ATF is both trained and evaluated on the same multi-LLM-as-judge signal, which biases the metric in its favor relative to baselines that never saw this judge. This is an important caution for any paper that uses a learned evaluator as both a training signal and an evaluation metric. The reviewer's suggestion to report results via both the automated judge and a larger human sample is the correct corrective, and the paper's existing human evaluation partially addresses it but at insufficient scale. The cost asymmetry point is also well-taken but less novel — it is a general issue with iterative refinement systems, not specific to this paper.

Beyond the reviewer's own contributions, the paper itself provides the more genuinely novel insights: the finding that ATF generalizes beyond its training revision budget (Figure 4a), the declining consistency check success rate across revision attempts (from 69.5% to 8.8%, Figure 5c), and the clean demonstration that each training stage (cold start → expert iteration → DPO) contributes additive value.

## Suggestions

1. **Report main consistency results with both the automated judge and a larger human evaluation sample** (400+ instances per benchmark). This would directly address the circularity concern and provide tighter confidence intervals for the comparisons.

2. **Add a cost analysis section** that reports total inference compute (e.g., approximate NPU-seconds per successful formalization) for ATF and compares it to baseline generation costs. Acknowledging the trade-off explicitly would make the comparison fairer and more informative.

3. **Describe the decontamination procedure** (similarity metric, threshold, number of removed examples) so that readers can assess the risk of data leakage, which is particularly important for the OOD generalization claims on CombiBench.

4. **Validate the DPO preference signal** by analyzing whether trajectories with fewer revisions produce semantically broader/worse formalizations in a held-out sample, or at minimum discuss the assumption and its limitations.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>