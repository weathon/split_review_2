The paper proposes MoEP (Modular Expert Paths), which combines layer-level parallelism (à la PaPaformer) with top-k routing to introduce sparsity while keeping total parameters fixed by operating parallel blocks at a reduced hidden dimension. Evaluated on the BabyLM strict-small track, MoEP modestly outperforms GPT-2 but does not outperform GPT-BERT on the standard macro average excluding the anomalous AoA task.

## Strengths

1. **The core architectural idea is genuinely creative and non-obvious.** The "shrink → parallel compute → grow" sandwich (Section 3.1, Figure 2) that interleaves dense layers with a sparse, reduced-dimension parallel stack, keeping total parameters fixed, is a worthwhile design space to explore. The goal of adding sparsity without inflating total parameters is a real and interesting problem.

2. **The evaluation faithfully follows the BabyLM strict-small pipeline** (Section 4), using the official data split, evaluation tasks, and fine-tuning protocol. Code and models are released, enabling reproducibility.

3. **The Conclusion (Section 6) is refreshingly honest**, explicitly acknowledging that scaling up may not preserve MoEP's relative performance and that reduced-dimensional parallel blocks may struggle with more complex data. This self-awareness is rare and should be recognized.

## Weaknesses

### Major

1. **Introduction overclaims relative to the experimental results.** The Introduction (line 31) states MoEP "was able to outperform all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models as well." However, Table 1 shows that on the macro average **excluding AoA** (the metric reported first by the paper), GPT-BERT (causal) scores **54.10** versus MoEP's **49.00** — a 5.1-point gap in GPT-BERT's favor. MoEP only surpasses GPT-BERT when the AoA task is included in the macro average (where GPT-BERT's anomalous -3.90 score pulls its average down). The paper later qualifies this in Section 5.1, but the Introduction's unqualified claim of outperforming "all" baselines is misleading and conflates metric selection with genuine superiority.

2. **No efficiency or sparsity measurements are reported, despite sparsity being the core motivation.** The entire framing (abstract, introduction, Section 2.2) is about sparsity — activating fewer parameters per token. Yet the paper never reports: (a) the fraction of parameters activated per token, (b) FLOPs per forward pass, (c) training or inference throughput, or (d) memory usage. From the hyperparameters (P=4, top-k=2) one can infer that roughly 50% of parallel-block parameters are activated, but this is never stated or quantified. Without any efficiency numbers, the sparsity claim is qualitative and the paper cannot demonstrate that MoEP is actually more efficient than a dense baseline — it only demonstrates it's different.

3. **No standard FFN-level MoE baseline is included.** The most natural comparison is against a GPT-2 with standard MoE replacing the FFN layers (e.g., E=4, top-k=2) at the same parameter count. Without this baseline, the paper cannot isolate whether MoEP's benefit comes from its novel layer-level parallelism or merely from having any MoE-style routing. The related work section (2.2.2) correctly identifies that "layer-level expert networks remain a relatively unexplored area," but the experiment does not establish that layer-level routing offers anything beyond what FFN-level MoE already provides.

4. **The claimed improvement over GPT-2 is marginal when controlling for the training pipeline.** The paper's own GPT-2 reimplementation scores 48.10 versus MoEP's 49.00 on the macro average excluding AoA — a 0.9-point gap. The official HF GPT-2 baseline scores 46.60, but comparing against it conflates architectural differences with pipeline differences. The paper acknowledges (Section 5.1) that its GPT-2 "slightly outperformed the BabyLM GPT-2 baseline," meaning the most controlled comparison (MoEP vs the authors' own GPT-2) shows only a small gap, and no variance or significance is reported. The reader cannot distinguish signal from noise.

### Minor

5. **No analysis of routing behavior**, despite being listed as a contribution (item 3). The paper claims "diverse computational pathways" and "modular expert paths" but never analyzes whether different tokens actually route to different parallel blocks, whether the routing is stable, or whether blocks specialize. The learning-curve analysis in Appendix A.3 is about training dynamics (scores over time), not routing behavior.

6. **No ablation studies on any architectural knobs.** The architecture has several design choices — number of parallel blocks (P=4), number of parallel layers (N=10), top-k (2), number of MoE experts (E=4), and the shrink/grow mechanism — none of which are ablated. It is possible that the reduced dimension of the parallel stack acts as a regularizer, and any 28M-parameter model with a similar bottleneck would perform similarly.

7. **MoEP-SwiGLU's parameter count increase (38M vs 28M) reveals a fragility in the "fixed parameter count" property.** The main MoEP (linear experts) does maintain parameter parity with GPT-2, which is good. But any step toward more expressive experts (SwiGLU) increases parameters by 36%, showing the approach's core constraint is tight.

### Trivial

None.

## Nice-to-Haves

- Adding a standard FFN-level MoE baseline at the same parameter count would substantially strengthen the paper's interpretation.
- Reporting actual sparsity (ratio of activated to total parameters per token) and wall-clock time per training step would ground the paper's central claim.
- An analysis of gating probabilities (e.g., load distribution across parallel blocks, whether blocks specialize) would substantiate the "modular expert paths" narrative.
- Ablating P, N, top-k, and E would clarify which design choices drive the results.

## Removed Points

These points appeared in the input review but were removed for the following reasons:

- **Criticism of entropy-based load balancing loss as "unusual":** This is a design preference, not an error. Entropy regularization is a valid approach for encouraging balanced routing.
- **Formatting complaints about Table 1 and Table 2:** Parser artifacts and presentation nitpicks; the original submission would not have these issues.
- **"Cherry-picked checkpoints" concern:** The paper is transparent about best-checkpoint selection, which is common practice.
- **"No variance/significance reported":** Single-run evaluation without variance is standard for BabyLM evaluations.
- **Criticism of the dense-to-sparse fine-tuning discussion as "generic":** The paper's scope is pre-training sparsity, and the related work section appropriately situates the paper.
- **Section-by-section notes about framing and literature survey:** These are presentation preferences, not substantive weaknesses.

## Novel Insights

The input review's most valuable observation is the tension between the paper's metric-dependent claims: MoEP's apparent superiority over GPT-BERT vanishes on the standard macro average (excluding AoA), yet the Introduction presents the results as an unqualified win. This is not simply a "missing experiment" — it is a framing issue that the authors should address by either (a) clearly stating that the "all baselines" claim holds only when AoA is included and explaining why, or (b) adjusting the claims to match what the non-AoA data supports. Beyond this, no genuinely novel insight emerges from the reviews beyond the paper's own contributions.

## Suggestions

1. Tone down the Introduction's claim about outperforming "all" baselines to match what the data actually shows — MoEP outperforms GPT-2 but is outperformed by GPT-BERT on the standard macro average.
2. Add a standard FFN-level MoE baseline to the BabyLM evaluation.
3. Report the activated parameter ratio per token and, ideally, throughput measurements.
4. Add at least a small ablation (e.g., varying P or top-k) and a routing-distribution analysis.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>