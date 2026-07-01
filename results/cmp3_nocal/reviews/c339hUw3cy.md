## Summary

This paper introduces ConCuR, a curated dataset of 4,892 CUDA kernels paired with chain-of-thought reasoning traces, and KernelCoder, a QwQ-32B model fine-tuned on this dataset via LoRA SFT. The core idea is that concise reasoning traces are associated with correct and high-performance kernel generation, and a pipeline is designed to select data points that satisfy both conciseness and speedup criteria. On KernelBench Levels 1 and 2, KernelCoder achieves pass@1 Exec of 58/59, outperforming DeepSeek-R1-0528 (52/55), Kevin (50/46), and all other baselines with substantially lower training cost (64 A100 GPU hours vs. >600 H200 hours).

## Strengths

1. **Empirical results are clean and strong.** KernelCoder (32B, SFT only) achieves pass@1 Exec of 58/59 on KernelBench Levels 1/2 (Table 1), outperforming DeepSeek-R1-0528 (685B), Kevin (32B, RL), and all frontier models. At pass@10, it reaches 91/95. These are clear, non-marginal improvements on correctness.

2. **Training efficiency is compelling.** Table 3 shows 64 A100 GPU hours and 4,892 training samples vs. >600 H200 hours for Kevin and 25,000 samples for KernelLLM. This makes a strong practical case for the curation pipeline.

3. **Ablation study (Table 4) is well-constructed.** The paper directly tests its stated criteria (conciseness, speedup) against natural baselines (random, max-length, min-length, speedup-only). The combination consistently outperforms any single criterion, providing clear evidence that the curation method matters.

4. **Cross-base-model generalization (Table 5)** shows that ConCuR improves Qwen3-8B, Qwen3-32B, and QwQ-32B, demonstrating that the dataset's value is not tied to one architecture.

## Weaknesses

### Major

- **The "for the same task" claim about reasoning length vs. correctness is not evidenced by the data shown.** The paper asserts (Section 3.4, line 82) that "for the same task, CUDA kernels generated after shorter reasoning traces tend to be correct more frequently." However, Figure 3 shows only aggregate data across all tasks, not a within-task analysis. The confound is clear: easier tasks may both require less reasoning and be easier to get correct. The paper references "detailed analyses (see Appendix B)" but the appendix is not available for verification. This is a gap between a central motivating claim and the evidence presented for it. The authors should either provide within-task plots (for each task, comparing CoT lengths of correct vs. incorrect generations) or soften the claim to the aggregate observation the data actually supports.

### Minor

- **Data leakage between training and evaluation is not discussed.** The training data is generated from KernelBook tasks, while evaluation is on KernelBench — two different cited benchmarks. The paper provides no analysis of whether the PyTorch programs in KernelBook overlap with those in KernelBench Level 1 or 2. While there is no evidence of actual contamination, standard practice in ML is to explicitly address this. The authors should state whether these task collections are disjoint and, if there is overlap, evaluate on the non-overlapping subset.

- **The speed advantage is modest at pass@1 on Level 1.** From Table 1, KernelCoder achieves fast₁ = 17% on Level 1 pass@1, which is *worse* than DeepSeek-R1-0528 at 18%. The headline correctness gains (Exec) are the primary contribution, but the paper's framing as "capable of generating correct and efficient CUDA kernels" (Contribution 3) slightly overstates the efficiency advantage at single-attempt inference.

- **The difficulty division metric (ARL) has partial circularity.** The paper uses Kevin-32B's ARL to partition tasks into easy/medium/hard (Section 6.1), then validates this division by showing that models perform worse on "hard" tasks. Since Kevin-32B is also the model that generated the ConCuR training data, this is partially circular — performance on ARL-defined bins is not an independent validation. A stronger test would use an independent model (e.g., DeepSeek-R1-0528) to compute ARL for the division and check whether rankings are consistent.

- **The ablation does not isolate what conciseness alone contributes.** The ablation (Table 4) compares the full combination against single-criterion baselines (5K-min for conciseness-only, 5K-speedup for speedup-only). The full method differs from 5K-speedup on at least three dimensions: conciseness filtering, speedup thresholding, and task balancing. Adding an ablation that removes only the conciseness criterion while keeping the other two would clarify whether conciseness specifically drives the improvement or whether the combination simply broadens data diversity.

### Trivial

- Figure 3 bins are very fine-grained (256-token intervals up to 20,000 tokens), making the trend harder to read than a coarser binning would be.
- Table 1 shows "fast₁" but the caption uses "fast<sub>1</sub>" — minor notation inconsistency.

## Nice-to-Haves

- Report confidence intervals or standard errors for the main metrics, especially given the finite task counts (Levels 1 and 2 have finite numbers of tasks).
- Include qualitative examples of good vs. bad reasoning traces in the main paper (currently deferred to the stripped appendix).
- Discuss why Levels 3 and 4 are excluded and provide at least qualitative analysis of failure modes there — even if no model succeeds, characterizing the gap would be informative.
- Clarify in Table 3 what "Kevin used 180 problems of KernelBench" means for the comparison.

## Removed Points

These points were raised in the input review but are removed after verification against the paper:

1. **"Potential data leakage could invalidate the experimental results (Structural/Fatal)"** — Demoted from Fatal to Minor (see above). The concern is speculative (no evidence of actual overlap between KernelBook and KernelBench, which are distinct cited references), and the critic's framing as "could invalidate" overstates the certainty. The rule on speculative-fatal claims applies.

2. **"Conciseness/speedup correlation undermines the thesis"** — Removed. The critic argued that because r=-0.047, "selecting for short CoTs is not selecting for high speedup." This misunderstands the curation method (Section 3.5, line 110): part (a) selects samples where the kernel with the *shortest* reasoning trace achieves the *highest* speedup — a conjunction of both criteria. The paper is not using conciseness as a proxy for speedup.

3. **"Abstract claim about 'first model trained on curated dataset' is overstated"** — Removed. The paper qualifies this with "to our knowledge." The cited prior works (KernelLLM, AutoTriton, Kevin) do not have datasets combining PyTorch programs + reasoning traces + CUDA kernel pairs, so the claim is accurate as stated.

4. **"Kevin* footnote suggests data leakage is known"** — Removed. The paper's footnote about Kevin's training data is transparent disclosure about a baseline, not a weakness of this paper.

5. **"Paper does not release dataset/model weights"** — Removed per the hard rule: reproducibility concerns about large artifacts in a preprint submission are not valid criticisms of the paper's scientific content.

6. **"Qualitative analysis of reasoning traces missing (Appendix B)"** — Removed. The appendix exists in the original submission (visible in the stripped paper as referenced but not included by the parser).

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface an unexpected pattern or framing that the paper itself does not already articulate.

## Suggestions

1. **Provide within-task evidence for the conciseness/correctness relationship.** For each task with multiple generations, plot CoT lengths of correct vs. incorrect kernels. This would substantiate the "for the same task" claim that currently relies on aggregate data.
2. **Explicitly address training/evaluation task overlap.** State whether KernelBook and KernelBench are disjoint. If they share tasks, evaluate on the non-overlapping subset and re-report results.
3. **Add an ablation that removes only the conciseness criterion** from ConCuR while keeping the speedup threshold and task balancing, to isolate conciseness's specific contribution.
4. **Validate the ARL difficulty metric using an independent generator** (e.g., DeepSeek-R1-0528) to compute ARL and re-run Table 7. If rankings are consistent, the metric is more credible.

## Score and Decision

<score>6</score>
<decision>Accept</decision>