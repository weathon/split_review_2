## Summary
This paper proposes MoEP (Modular Expert Paths), a sparse decoder-only architecture that adds top-k routing over parallel Transformer blocks at reduced dimensionality, combined with MoE-style shrink/grow projection blocks, to achieve sparsity without increasing total parameter count compared to a dense GPT-2 baseline. The authors evaluate MoEP on the BabyLM strict-small track and report modest improvements over GPT-2 baselines, claiming that modular sparse routing accelerates early learning.

## Strengths
- **Interesting research direction**: The goal of achieving sparsity benefits without inflating parameter count is a worthy problem. The combination of layer-level parallel routing with dimensionality-reducing MoE projections is a reasonable architectural idea worth exploring.
- **Reproducibility effort**: The authors release code, use a standardized evaluation pipeline (BabyLM), and train on identical data with matched random seeds, which is commendable for a low-resource study.
- **Honest discussion of limitations**: The paper acknowledges scalability concerns (Section 6) and that MoEP-SwiGLU underperforms, which reflects good scientific practice.

## Weaknesses
### Fatal
None.

### Major
- **Insufficient evidence that sparsity itself helps**: The paper's own GPT-2 reproduction outperforms the official BabyLM GPT-2 baseline by ~4.7 points in macro average (48.10 vs 43.60 approx from columns), yet MoEP's advantage over their own GPT-2 is only ~0.9 points (49.00 vs 48.10) when including AoA, and negligible otherwise. The training curves (Section A.3) claim MoEP "extracted useful patterns earlier" but this is not quantified with statistical tests or formal metrics—the description is qualitative and anecdotal. The core claim that sparsity improves performance is not convincingly supported.

- **Cherry-picked comparison framing**: The paper repeatedly emphasizes MoEP outperforming "all BabyLM strict-small baseline models including GPT-2 and GPT-BERT," but this comparison is against the *official* BabyLM GPT-2 baseline, which their own GPT-2 already beats by ~4.7 points. Against their own well-trained GPT-2 (which they acknowledge as the "primary comparison point"), MoEP's advantage is marginal at best and depends entirely on whether AoA is included.

- **MoEP-SwiGLU contradicts the paper's narrative**: MoEP-SwiGLU has 38M parameters (vs 28M for GPT-2 and MoEP) yet performs worse than both. This undermines the claim that layer-level sparsity is broadly beneficial and raises the question of whether MoEP's gains are architecture-specific artifacts rather than evidence for the sparsity mechanism. The paper acknowledges this but does not provide analysis to explain why.

- **Lack of ablations**: No systematic ablation isolates the contribution of (a) parallel blocks vs. (b) MoE shrink/grow projections vs. (c) reduced dimensionality. Without these, it is impossible to determine which component drives any observed gains or whether the full pipeline is necessary.

### Minor
- **Checkpoint selection via fast evaluation on the same tasks**: The best checkpoint is selected using fast evaluation on the benchmark tasks, then the full evaluation is run on that checkpoint. This introduces a form of test-set leakage—essentially selecting for performance on the final evaluation tasks, which can inflate reported scores.

- **No comparison to other sparse or MoE methods**: The paper positions itself within the MoE literature but compares only to dense baselines (GPT-2, GPT-BERT). Comparing to other sparse methods (e.g., Switch Transformer-style FFN-level MoE with matched parameters) would be essential to validate that layer-level routing has advantages over standard approaches.

- **Routing analysis is superficial**: Contribution (3) claims analysis of "expert networks routing behavior and show that layer level parallelism enable fast and stable training," but the actual analysis consists of qualitative observations about checkpoint learning curves without metrics like routing entropy, load imbalance ratios, or expert utilization statistics.

- **Single experimental setting**: All experiments use BabyLM strict-small (~10M words) with a single GPT-2-scale architecture. The paper itself acknowledges (Section 6) that results may not generalize to larger scales, but offers no evidence beyond the BabyLM setting.

### Trivial
- The paper conflates "modularity" with "routing," since the parallel blocks in MoEP are not independently trainable modules (unlike PaPaformer), yet the name "Modular Expert Paths" and framing suggest modularity.

## Nice-to-Haves
- An analysis of routing entropy and load balance statistics over training would strengthen the claim that training is "stable."
- A comparison to FFN-level MoE with matched parameter count would clarify whether layer-level routing offers genuine advantages.
- Statistical significance testing or confidence intervals for the reported scores, given the small margins involved.

## Novel Insights
The paper's primary insight—that combining layer-level parallel routing with dimensionality-reducing MoE projections can maintain parameter count while introducing sparsity—is conceptually interesting. However, the empirical evidence does not convincingly demonstrate that this mechanism provides meaningful gains beyond what a well-tuned dense baseline achieves. The MoEP-SwiGLU result, where more parameters with the same sparsity mechanism hurts performance, suggests the observed gains may be fragile and setting-dependent rather than reflecting a robust architectural principle.

## Suggestions
- Add ablation studies decomposing the contribution of parallel blocks, MoE projections, and reduced dimensionality.
- Compare to FFN-level MoE with matched parameters to establish that layer-level routing is the right granularity.
- Report routing statistics (entropy, load balance, expert utilization) to substantiate the "stable training" claim.
- Consider a slightly larger scale (e.g., 100M+ parameters) to test whether the approach generalizes beyond BabyLM's very constrained setting.

## Score and Decision
The paper addresses an interesting question and shows some care in experimental methodology, but the core claims are not well supported by the evidence. The margin over a properly matched dense baseline is small and possibly an artifact of checkpoint selection, the most informative comparison (MoEP-SwiGLU) actually works against the paper's thesis, and there are no ablations to isolate which architectural components matter. The contribution is incremental and fragile.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>