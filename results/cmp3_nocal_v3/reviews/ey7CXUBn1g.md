## Summary

This paper proposes AdaSVD, an SVD-based LLM compression method with two components: **adaComp**, which alternately updates the truncated U and V^T matrices via a Moore-Penrose pseudoinverse formulation to compensate for truncation error, and **adaCR**, which assigns layer-specific compression ratios based on input-output cosine similarity. On LLaMA2-7B, OPT-6.7B, Vicuna-7B, and Mistral-7B across 40–80% compression, AdaSVD consistently improves over the prior SVD-LLM baseline (e.g., WikiText-2 perplexity 14.76 vs. 16.11 at 40%, 25.58 vs. 27.19 at 50%, 50.33 vs. 89.90 at 60%).

---

## Strengths

1. **Well-motivated problem decomposition.** The paper correctly identifies two genuine limitations in prior SVD-based LLM compression: (i) post-truncation weight matrices are used as-is without compensating for the removed singular components, and (ii) uniform compression ratios ignore varying layer importance. These are real gaps, not straw men.

2. **Clean mathematical formulation for adaComp.** The reformulation of post-truncation compensation as a least-squares problem solved via the Moore-Penrose pseudoinverse (Eq. 8–13) is a sensible design choice that avoids numerical instability of direct matrix inversion. The stack-of-batch technique (Eq. 14–15) is a practical engineering contribution for fitting more calibration data into fixed GPU memory.

3. **Consistent relative improvements across models and compression ratios.** AdaSVD outperforms SVD-LLM (the strongest prior SVD method) on every model tested and across all compression ratios from 40% to 80%. The improvement direction is consistent, not cherry-picked. The orthogonality with GPTQ quantization (Table 4) further confirms the method's utility.

---

## Weaknesses

### Fatal
None.

### Major

1. **Factually incorrect claim about adaCR in the ablation section.** The paper states: "AdaSVD already outperforms SVD-LLM without using **adaCR**" (Section 4.3, under "Effectiveness of Adaptive Compression Ratio"). Table 3b contradicts this at 50% compression: AdaSVD with constant CR (no adaCR) achieves 27.33 PPL, which is *worse* than SVD-LLM's 27.19 PPL. The claim holds at 40% and 60%, but is false at 50%. This is a clear factual error that must be corrected, and the non-monotonic behavior of the components should be discussed honestly rather than glossed over.

2. **Ablation reveals non-trivial component interactions that the paper does not explain.** At 50% compression:
   - AdaSVD without adaComp (i.e., adaCR alone): **30.00** PPL — *worse* than SVD-LLM's 27.19.
   - AdaSVD without adaCR (i.e., adaComp alone): **27.33** PPL — essentially tied with SVD-LLM's 27.19.
   - Full AdaSVD: **25.58** PPL — better than both.
   
   This pattern means that neither component alone reliably beats the prior art at 50%, yet they work together. The paper presents the components as independently beneficial but does not acknowledge this interaction or investigate its cause. Either the two components interact synergistically (which itself would be worth discussing), or there are uncontrolled implementation differences making the ablative baselines worse than expected.

### Minor

3. **The adaCR importance metric is unvalidated against alternatives.** The metric (Eq. 17) measures cosine similarity between layer input X and output Y = WX. A high similarity could indicate a layer that transforms the input very little — which could plausibly be compressed more aggressively, not less. The paper provides no theoretical justification for this choice and does not compare against any alternative importance measure (e.g., output norm sensitivity, gradient magnitude, random assignment). While the empirical results in Table 3b show that adaCR improves over constant CR at the *full method* level, the metric itself remains an ad-hoc design choice without validation.

4. **mrr (minimum retention ratio) and iteration count k not disclosed for main results.** The paper only varies mrr in the ablation (Table 3d) and iteration count in Table 3c, but does not state which values were used to produce the main results in Table 1. Both are tunable hyperparameters that affect performance, and their values should be reported.

5. **No variance or confidence intervals reported.** Calibration data is randomly sampled (256 samples from WikiText-2), so results likely have non-negligible variance. This is especially relevant given that some gaps between methods are small (e.g., 27.19 vs. 27.33 at 50%).

### Trivial
None.

---

## Nice-to-Haves

- **Generalizing adaComp to other SVD pipelines.** The paper evaluates adaComp only within its own pipeline (building on SVD-LLM's data whitening). Showing that the compensation scheme also improves FWSVD or ASVD would provide stronger evidence that the alternating update is the actual mechanism of improvement rather than an interaction specific to the whitening setup.
- **Wall-clock time comparison.** The alternating update requires multiple forward-backward passes through calibration data; reporting the computational overhead relative to SVD-LLM's single-step procedure would help practitioners assess the trade-off.

---

## Removed Points

- **"The paper overstates what 'narrowing the performance gap' means"** — Removed. The claim that AdaSVD "narrows the gap" (compared to prior SVD methods) is technically true: the gap from original model PPL 5.68 to AdaSVD's 14.76 is smaller than to SVD-LLM's 16.11. The gap remains large, but this framing is standard in compression papers and does not cross into factual overreach. The critic's complaint is about tone, not evidence, and there is no concrete alternative metric the paper should have used.
- **"No test of whether adaComp generalizes to other SVD methods"** — Downgraded to Nice-to-Have. The paper's scope is AdaSVD as an integrated method; testing component portability is a useful extension but not a required condition for the paper's core claims.
- **"The VLM results are qualitative only and add limited evidence"** — Removed. The VLM experiment is presented as a qualitative demonstration, which is a standard and appropriate format for image captioning evaluation; it does not claim to be a rigorous benchmark.
- **Section-by-section notes about parser artifacts (missing Table 2, missing appendix references)** — Removed per hard rules.

---

## Novel Insights

None beyond the paper's own contributions. The interaction pattern in the ablation (neither component alone reliably beats SVD-LLM at 50%, but combined they do) is worth investigating but is not discussed in the paper.

---

## Suggestions

1. **Correct the factual error:** In Section 4.3, revise the claim "AdaSVD already outperforms SVD-LLM without using adaCR" to acknowledge the 50% case where it does not, and discuss why the components interact non-monotonically.
2. **Report hyperparameters:** State the mrr and number of alternating iterations used for each target compression ratio in the main results (Table 1).
3. **Add variance estimates:** Report standard deviations across multiple random calibration data draws, especially for the compression ratios where method gaps are narrow.
4. **Validate or motivate the importance metric:** Either provide a theoretical justification for why cosine similarity of input-output is the right measure, or compare against one or two alternative importance metrics to show the choice matters.

---

## Score and Decision

The paper proposes a well-motivated method with clean mathematics and demonstrates consistent improvements over prior SVD-based compression. The main evidence supports the core claim (AdaSVD as a full method outperforms SVD-LLM). However, the factual inaccuracy in the ablation claim and the unacknowledged component interaction are significant enough to require correction. The paper is publishable with these revisions.

**Score:** 6

**Decision:** Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>