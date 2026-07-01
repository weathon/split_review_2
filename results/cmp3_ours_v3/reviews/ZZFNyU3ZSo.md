Now let me write the final consolidated review.

## Summary

This paper proposes UniMoD, a task-aware Mixture-of-Depths (MoD) token pruning method for unified multimodal transformers that handle both generation (e.g., text-to-image) and understanding (e.g., VQA) tasks. The authors first conduct an empirical analysis of token redundancy across layers and tasks in models like Show-o and Emu3, finding that redundancy profiles differ substantially by task. Based on these observations, they introduce separate, task-specific routers with different pruning ratios for each task, converting a subset of dense transformer layers into MoD layers. Experiments show ~15% FLOPs reduction on Show-o and ~40% on Emu3 while roughly maintaining performance on several benchmarks.

## Strengths

- **The empirical analysis (Section 3) provides genuine motivation for the method.** The paper systematically examines attention weight patterns across four unified transformers (Show-o, JanusFlow, Emu3, Lumina-mgpt), uses the ARank metric to quantify token redundancy per layer and per task, and tests task-interaction effects. The finding that generation and understanding tasks have measurably different redundancy profiles (Fig. 3) is the paper's strongest piece of evidence and directly motivates the design of task-specific routers.

- **The Emu3 result is noteworthy.** A 40% FLOPs reduction while maintaining competitive performance on most benchmarks is a non-trivial efficiency gain, if it holds under scrutiny. The Show-o results (~15% reduction) are more modest but still positive.

- **The ablation study (Table 5) provides useful signal.** It demonstrates that a single router for both tasks ("w/o task-aware router") underperforms task-specific routers, particularly on generation (GenEval: 0.50 vs. 0.61). The "w/o layer switch module" and "Basic MoD" ablations also help isolate the contributions of individual design choices.

## Weaknesses

### Fatal
None.

### Major

- **Unexplained baseline inconsistency between Table 2 and Table 3.** The Show-o* baseline in Table 2 (MME=1032.0, GQA=52.5, POPE=77.9) differs substantially from the "Full Computation" baseline in Table 3 (MME=1056.0, GQA=56.3, POPE=79.8). Both are described as the same Show-o model trained on both tasks, but the gap — 24 points on MME, 3.8 points on GQA — is large enough to suggest different training setups, datasets, or evaluation protocols. The paper offers no explanation for this discrepancy, which undermines confidence in the reliability of all reported numbers.

- **The key ablation comparison (task-specific vs. single-router MoD) is not at matched compute.** In Table 5, "w/o task-aware router" (single router) operates at 40.8 TFLOPs while UniMoD operates at 43.3 TFLOPs — a ~6% compute advantage. This confounds the comparison: it is unclear whether UniMoD's better performance comes from task-specific routing or simply from having more compute budget. A precisely matched comparison is needed to directly test whether the additional complexity of task-specific routers is justified.

- **Several understanding benchmarks show non-trivial degradation, with no statistical characterization.** Under UniMoD, Show-o's GQA drops from 56.3→54.5 and VQAv2 from 68.3→66.2; Emu3's GQA drops 46.0→45.2, POPE 76.0→74.7, and VQAv2 54.8→53.9. No variance estimates, confidence intervals, or multi-run statistics are reported anywhere in the paper. Without these, it is impossible to determine whether these degradations are systematic or noise, especially given that the improvements on other metrics (MME, DSG) are small and could also fall within normal variance.

### Minor

- **The router architecture is underspecified.** The router function \(R_t\) is the central component of the method, but its architecture (linear layer? MLP? what dimensionality?), parameterization, and training loss are never described. The paper only states it "assigns scores to tokens" (Section 4.1). This is a reproducibility gap — a reader cannot reimplement the method from the description provided.

- **The method is evaluated only during fine-tuning, but framed as reducing "training FLOPs."** Section 5.1 states "The model is finetuned on 8 H100 GPUs," yet the abstract and introduction describe the contribution as reducing "training" cost without flagging that the scope is limited to fine-tuning from a pretrained checkpoint. Fine-tuning is a small fraction of total training cost, and the ARank-based analysis — computed from the converged model's attention maps — may not transfer to the pre-training setting where attention patterns evolve.

- **The paper does not compare against γ-MoD (Luo et al., 2024), the most directly related prior work.** γ-MoD applies MoD to MLLMs using the same ARank metric and is discussed in the Related Work. While UniMoD targets unified transformers (generation + understanding) rather than MLLMs, a comparison would help position the contribution and quantify the benefit of task-specific routing over the shared routing approach in γ-MoD.

### Trivial

- Table 4 uses the notation "1.30x/iter" without specifying what "x" represents (presumably seconds), making the units ambiguous.

## Nice-to-Haves

- Compare UniMoD against single-router MoD at precisely matched TFLOPs to cleanly isolate the benefit of task-specific routing.
- Provide variance estimates (standard deviations over ≥3 seeds) for all main benchmark results.
- Validate the ARank-based layer selection strategy against simple alternatives (e.g., last-N layers, random layers) beyond the "w/o layer switch module" ablation.
- Report the computational overhead of the routers themselves to confirm that net savings account for added router computation.
- Compare against γ-MoD applied to unified transformers to quantify the task-specific advantage.

## Removed Points

These points appeared in the harsh critic review but were removed for the following reasons:

- **"The baselines (interleaved layer skipping, early exit) are too weak"** — Partially removed. Interleaved layer skipping and early exit serve as lower-bound sanity checks, not as the primary baselines. The core concern (unmatched compute in the single-router ablation, missing γ-MoD comparison) is retained in the Major and Minor sections above. The demand for "training the dense model with fewer steps" as a baseline is removed: this conflates token pruning (which preserves representational capacity per step) with simply reducing training iterations, and is not a standard baseline for token pruning methods.
- **"The competitive token pruning experiment (Fig. 4) conclusion is an artifact of the setup"** — Removed. The paper's interpretation of Fig. 4 is reasonable given the stated Gumbel-Softmax setup. The critic's speculation about different capacities yielding different conclusions is not grounded in any experimental evidence presented.
- **"Observation in Section 3.2 is intuitive and unsurprising"** — Removed. The value of empirical analysis lies in confirming and quantifying intuitions, not in being surprising.
- **"ARank-based pruning ratio estimation not validated"** — Moved to Nice-to-Haves. The approach is methodologically reasonable; exhaustive validation would strengthen but is not required.
- **"No analysis of what determines optimal pruning ratio"** — Moved to Nice-to-Haves.
- **"Scaling to more than two tasks deferred to appendix"** — Removed. The parser strips appendix content from all papers; this analysis exists in the original submission.
- **"Paper claims 'few studies explored efficient training' while citing MoMa"** — Removed. The claim refers to task-aware pruning specifically, not MoD application generally, and is accurate when read in context.
- **Missing MoMa comparison** — Removed. MoMa lacks generation benchmarks and applies MoD in a "simplistic combination" as the paper notes; the omission is not a critical gap.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Explain the baseline discrepancy.** Clarify why the Show-o numbers differ between Table 2 and Table 3 (different training data? different evaluation protocol?). This is the most pressing issue because it affects trust in all reported results.
2. **Match compute in the ablation.** Either run the "w/o task-aware router" at 43.3 TFLOPs or run UniMoD at 40.8 TFLOPs to allow a clean comparison.
3. **Add variance estimates.** Report standard deviations over multiple seeds for the main benchmarks. This is especially important given the small and inconsistent performance differences.
4. **Specify the router architecture.** Describe the router's structure, parameter count, training loss, and how it operates alongside the base model.
5. **Scope the contribution precisely.** Clarify in the abstract and introduction that the FLOPs savings are demonstrated during fine-tuning, not full pre-training.
6. **Add a γ-MoD comparison** to position the work against the most directly related prior method.

---

### Score Calibration Details

**Round 1 bracket:** 5.0 – 7.0

**Anchors retrieved and compared:**

| Paper (Path) | Avg Score | Round | Comparison |
|---|---|---|---|
| γ-MoD (q44uq3tc2D.md) | 6.67 | 1, narrow | Most directly related: same ARank metric, MoD for multimodal models. γ-MoD tested on 3 MLLMs with more thorough evaluation. UniMoD tackles a harder problem (unified transformers with heterogeneous task types) but has weaker evaluation (unexplained baseline gap, unmatched compute in key ablation). UniMoD is notably weaker. |
| Show-o (o6Ynz6OIQ6.md) | 6.50 | 1, narrow | Base model paper — introduces the unified transformer architecture. A different contribution type (model proposal vs. efficiency method), but both rely on the same base model. UniMoD's evaluation is less thorough. |
| MoE++ (t7P5BUKcYv.md) | 8.00 | 1 | Strong efficiency paper with clean, comprehensive evaluation. UniMoD does not match this quality bar. |
| LLM-VTP (Acdd83rF1s.md) | 5.80 | 1, narrow | Token pruning for video understanding. Rejected due to sensitivity of design choices and limited evaluation — comparable in evaluation quality to UniMoD. |
| EMMA (QPDbIFumQ8.md) | 5.33 | 1 | Efficient multimodal adaptation — similar score range. |
| From Unimodal to Multimodal (jHVJQybLXi.md) | 3.75 | 1 | Weaker paper, lower relevance. |

**Final score decision:** UniMoD is below γ-MoD (6.67, Accept) in evaluation thoroughness but has genuine and clearly-motivated contributions. The baseline inconsistency and unmatched-compute ablation are significant gaps that need resolution. Score: **5.5** — the paper is between borderline reject and borderline accept; the evaluation weaknesses are real but addressable.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>