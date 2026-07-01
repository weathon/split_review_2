I've verified all claims against the paper. Everything checks out. Let me now produce the final review.

---

## Summary

The paper proposes MoEP (Modular Expert Paths), a decoder-only architecture that combines layer-level parallelism with MoE-style routing to introduce sparsity while keeping total parameter count fixed relative to a dense baseline. The design interleaves two full-size dense layers with a middle stack of reduced-dimension parallel blocks gated by top-k routing, coupled with MoE shrink/grow projections. The method is evaluated on the BabyLM strict-small track against GPT-2 and GPT-BERT baselines.

## Strengths

1. **Structurally creative architectural idea (Sections 3.1–3.3).** Interleaving full-size dense layers with a routed stack of reduced-dimension parallel blocks, wrapped by MoE shrink/grow projections, is a novel way to introduce token-level routing without increasing total parameters. The paper correctly identifies a real tension in standard MoE (more total parameters for the same activation budget) and proposes a concrete alternative.

2. **Controlled evaluation within a fixed framework (Section 4).** Training on the BabyLM strict-small track using the official evaluation pipeline provides a reproducible comparison. The paper trains its own GPT-2 reimplementation and reports it closely matches the BabyLM GPT-2 baseline (48.10 vs. 46.60), indicating a well-calibrated pipeline.

3. **Honest limitations section (Section 6).** The conclusion candidly acknowledges that reduced-dimension parallel blocks may not suffice on more complex data and that scaling may change the picture.

## Weaknesses

### Fatal

None.

### Major

1. **The abstract's central claim is misleading and depends on an unexplained single-task anomaly.**  
   The abstract states MoEP "was able to outperform all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models as well" (L31). However, Table 1 shows that on the primary macro average (excluding AoA), all three GPT-BERT variants outperform MoEP by 3.4–5.1 points (GPT-BERT causal: 54.10 vs. MoEP: 49.00). The claim holds only on the secondary macro average that includes AoA (MoEP: 44.50 vs. GPT-BERT causal: 41.20). This reversal is almost entirely driven by the AoA task, where scores range from −3.90 to 53.70 across models—an extraordinary, unexplained variation that the paper never discusses. The body (Section 5.1) attempts to retreat by treating GPT-2 as the "primary comparison point," an ad hoc justification that appears after seeing the results. A reader who reads only the abstract is misled.

2. **No efficiency evidence to support the "compact and efficient" claim.**  
   The paper's stated motivation is to "add sparsity while keeping the total parameter count fixed" (Abstract), and the title asserts "Compact and Efficient" sparsity. Yet the paper reports no FLOPs measurement, no wall-clock throughput, no memory usage, and no sparsity ratio (fraction of parameters activated per token). The only efficiency-related statement is the coarse "approximately 1-2 hours per model." Without any efficiency measurement, the core premise that this architecture provides meaningful sparsity is asserted but not evidenced.

### Minor

3. **Single-run evaluation with no uncertainty quantification.**  
   All comparisons rest on single-point macro averages. The difference between MoEP (49.00) and the paper's own GPT-2 (48.10) is 0.9 points. No variance, confidence intervals, or significance tests are reported. Given the small data scale (~10M words) and known variance in BabyLM evaluations, this gap may be noise.

4. **Missing hyperparameter values for the load-balancing loss.**  
   Equation (3) defines λ^block and λ^expert, but the paper never specifies their values (L134: "and λ learning weight"). The regularization setup is therefore unreproducible.

5. **Load-balancing formulation (Eq. 2) has an ambiguous sign convention.**  
   The balancing term is L_balance = −∑ p_i log p_i, which is the entropy H(p). Adding H(p) to the total loss and minimizing would minimize entropy (encouraging routing toward collapse), the opposite of load balancing. The paper calls this "the standard load-balancing regularizer" without citation or clarification.

6. **Claimed "analysis of routing behavior" is not delivered.**  
   Contribution 3 states: "We analyze expert networks routing behavior and show that layer level parallelism enable fast and stable training." However, Section 5.1 and Appendix A.3 only present learning curves (accuracy over time). There is no analysis of routing entropy, expert utilization distributions, or whether different parallel blocks specialize.

7. **MoEP-SwiGLU variant is framed as a contribution but provides only negative evidence.**  
   MoEP-SwiGLU adds 10M parameters (38M vs. 28M) and achieves the lowest macro average (47.70). The paper frames this as "lightweight simplicity is better than adding complexity" (Contribution 4), but this reads as a post-hoc rationalization of a failed experiment. Including it as a contribution inflates parameter counts without providing positive evidence.

8. **AoA task scores show extreme unexplained variation.**  
   Scores on the AoA task range from −3.90 (GPT-BERT causal) to 53.70 (MoEP), a nearly 58-point swing. The paper never describes what AoA measures or why such variation occurs. Since the macro-average claim that MoEP "outperforms all" hinges on this task, the omission is significant.

### Trivial

9. **Checkpoint selection procedure not reported alongside results.**  
   Section 4 notes that the best fast-evaluation checkpoint was used per model, but this is not stated alongside Table 1. The reported scores are therefore cherry-picked per model at their respective best checkpoints.

## Nice-to-Haves

- Report per-token FLOPs/MACs and throughput (tokens/second) to substantiate the sparsity/efficiency claim.
- Run multiple seeds (≥3) and report variance.
- Compare against a standard MoE baseline at the same parameter budget (e.g., smaller dense layers + more experts).
- Include actual routing analysis (expert utilization, routing entropy over time, block specialization).
- Discuss why MoEP excels at Entity Tracking and WSC relative to GPT-2—these could be genuine strengths that deserve analysis.
- Discuss the AoA task and why MoEP performs so differently from baselines.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Writing quality / formatting artifacts** (ungrammatical sentences, line breaks, garbled characters): These are parser errors, not author errors. Removed per instructions.
- **Citation concern about Llama 4 being unreviewed**: The paper itself acknowledges this (footnote 1). The "name-dropping" characterization is speculative. Removed.
- **"MoEP may not work at scale" contradicting the abstract**: Section 6 is an honest limitations paragraph; presenting limitations is a strength, not a contradiction. Removed.
- **Missing comparison with true sparse MoE baseline**: A reasonable suggestion but not a weakness of what the paper does. Moved to Nice-to-Have.
- **Analysis of specific task scores as "anomalous" where MoEP outperforms**: The critic flags entity tracking (MoEP 35.65 vs. GPT-2 13.15) and WSC (MoEP 67.30 vs. baselines 61.50–65.40) as unexplained. These could be strengths, not weaknesses; flagged as missed opportunities. Moved to Nice-to-Have.
- **The MoEP-SwiGLU discussion being "contradictory" to fixed-parameter framing**: This is already covered under Weakness #7.

## Novel Insights

The most incisive observation from the review is that the paper's central empirical claim does not survive a careful reading of its own Table 1. The abstract promises outperformance over "all" baselines including GPT-BERT, but the data show GPT-BERT outperforming MoEP on the primary aggregate by a clear margin, with the abstract's claim only holding on a secondary aggregate that is entirely carried by an anomalous, unexplained 58-point swing on a single task (AoA). This framing-vs-evidence mismatch is paired with a second striking gap: a paper whose entire framing revolves around sparsity and efficiency provides zero computational measurements (no FLOPs, no throughput, no sparsity ratio). Together these two issues mean the paper's contribution is structurally under-supported by the evidence presented.

## Suggestions

1. Reframe the abstract and introduction to accurately reflect what the data shows: MoEP outperforms GPT-2 on the BabyLM strict-small track, but GPT-BERT models outperform MoEP on the primary aggregate. Explicitly discuss the AoA task and why it produces extreme variation.
2. Add FLOPs, throughput, or sparsity ratio measurements to substantiate the "compact and efficient" claim in the title.
3. Run multiple seeds and report variance, especially given the 0.9-point margin with the paper's own GPT-2.
4. Provide actual routing behavior analysis (expert utilization distributions, routing entropy over training) or remove this from the contributions.
5. Specify the missing λ values and clarify whether the load-balancing loss in Eq. 2 has the intended sign.
6. Remove or honestly reframe the MoEP-SwiGLU variant as a negative result rather than enumerating it as Contribution 4.

## Score and Decision

The paper proposes an architecturally interesting idea but does not provide credible evidence for its central claims. The headline result is misleading (the abstract claims outperformance over "all" baselines, but GPT-BERT outperforms MoEP on the primary aggregate), the core efficiency premise is entirely unmeasured, and multiple details needed for reproducibility are missing. The architectural idea may have merit, but the paper as presented does not meet the bar for acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>