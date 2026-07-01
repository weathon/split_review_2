## Summary

The paper introduces **MoEP (Modular Expert Paths)**, a sparse decoder-only architecture that adds sparsity to a dense baseline without increasing the total parameter count. MoEP stacks a small number of full-size dense layers around a middle module composed of a dimensionality-reducing MoE block, several parallel layers (each containing multiple lightweight blocks with top‑k routing), and a dimensionality-increasing MoE block. The authors evaluate MoEP and a SwiGLU variant on the BabyLM strict‑small track, comparing against GPT‑2 and GPT‑BERT baselines under matched conditions, and report modest gains over their own GPT‑2 replica.

---

## Strengths

1. **Fixed‑parameter sparsity is a worthwhile goal.** Most MoE methods increase total parameters while activating only a subset; MoEP aims to keep the parameter count identical to a dense baseline while still introducing token‑level sparsity. This design goal is clearly stated and addresses a practical concern in deploying sparse models.

2. **Evaluation on a shared, small‑scale benchmark (BabyLM) with a good level of detail on training protocols.** The authors faithfully follow the BabyLM strict‑small pipeline, pre‑tokenize with the same stride, and report many individual task scores in addition to macro averages. This makes comparisons reproducible and grounded in a known setup.

3. **Open‑source code and model weights are released**, which is valuable for follow‑up work.

4. **The training‑dynamics analysis (Figures 3 and 4 in the appendix) is informative.** It shows that MoEP reaches its best evaluation scores earlier than GPT‑2, suggesting better sample efficiency—an interesting property that is worth further investigation.

---

## Weaknesses

### Fatal

None.

### Major

1. **Overstated performance claim.** The paper states that “MoEP was able to outperform all BabyLM strict‑small baseline models, including the GPT‑2 and GPT‑BERT models as well.” Looking at Table 1, the GPT‑BERT (causal) baseline achieves a macro average (excluding AoA) of **54.10**, while MoEP achieves **49.00**. Even on the text‑average macro, GPT‑BERT (causal) scores **41.20** vs. MoEP’s **44.50** (a small advantage). The claim that MoEP outperforms *all* baselines is therefore not supported by the presented numbers; the paper should have qualified this to say it outperforms the GPT‑2 baselines and is competitive with GPT‑BERT variants.

2. **Very modest improvement over the direct baseline.** MoEP’s macro average (excl. AoA) is 49.00, compared to the authors’ own GPT‑2 at 48.10—a gain of less than one point. Many individual tasks favour GPT‑2 over MoEP (e.g., EWOK 57.85 vs. 50.20, WUG 36.00 vs. 33.00, BoolQ 67.50 vs. 66.20). This marginal improvement, especially on a small‑scale benchmark, weakens the claim that the architectural sparsity provides a clear advantage.

3. **No ablation or justification of the specific design choices.** The architecture includes two dense layers, shrink/grow MoE blocks, and a stack of parallel layers with top‑k routing. There is no experiment that ablates any of these components (e.g., removing the dense layers, varying the number of parallel blocks, comparing different routing top‑k values, or replacing the shrink/grow mechanism with a single linear projection). Without such ablations, it is unclear which parts of the design are responsible for the observed behavior and whether simpler alternatives would perform similarly.

4. **The SwiGLU variant underperforms significantly** (macro avg 47.70 excl. AoA vs. GPT‑2 48.10), yet the paper does not analyze why. The explanation that “lightweight linear experts are more effective at small scale” is speculative. If a component of the proposed family is clearly worse, a deeper investigation is needed to understand the failure mode.

### Minor

1. **The experimental setup uses a small dataset (~10M words) and an outdated base architecture (GPT‑2).** The authors acknowledge this limitation, but it nonetheless limits the generality of the conclusions. The method’s benefit may not transfer to larger scales or more modern architectures.

2. **The paper occasionally makes imprecise statements** (e.g., “accelerates model learning” without quantifying wall‑clock time or number of steps, or “outperforms” without specifying the baseline). Some of these are clarified by the tables, but the overall narrative is sometimes stronger than the evidence.

3. **The “load‑balancing” regularizer** (Equation 2) is actually an entropy term, not the standard auxiliary load‑balancing loss (which usually penalizes imbalance). The authors compute it separately for blocks and experts. They do not compare this choice to other balancing methods or show that it is needed.

### Trivial

None.

---

## Nice‑to‑Have

- A comparison against a dense variant with the **same parameter budget** but a different depth/width configuration would test whether the MoEP structure itself, rather than just having more layers, provides the benefit.
- Measuring actual FLOPs per token for MoEP vs. the dense baseline would quantify the computational sparsity achieved.
- A small‑scale scaling study (e.g., training on 2× or 4× more data) would give preliminary evidence on whether the fixed‑parameter advantage holds at larger budgets.

---

## Novel Insights

None beyond the paper’s own contributions. The observation that MoEP reaches peak evaluation scores earlier in training (sample efficiency) is the most interesting insight, but it is not deeply analyzed (e.g., whether it is due to the reduced hidden dimension, the routing, or something else).

---

## Suggestions

1. Correct the overstatement about outperforming all baselines; clearly state that MoEP outperforms the GPT‑2 baseline and is competitive with the best GPT‑BERT variant.
2. Add ablation experiments (at least remove the shrink/grow MoEs, or vary the number of parallel blocks) to isolate which components contribute to the results.
3. Discuss why the SwiGLU variant fails; if it is a matter of convergence, provide evidence (e.g., longer training runs).
4. Report wall‑clock training time for MoEP vs. GPT‑2 to substantiate the “accelerates learning” claim.
5. Clarify that the load‑balancing term is an entropy regularizer and justify its use compared to the more common squared coefficient‑of‑variation loss.

---

## Score and Decision

**Score:** 4.0

**Decision:** Reject

**Reasoning:** The paper tackles a meaningful problem and provides a reproducible small‑scale evaluation, but the claimed outperformance over all baselines is inaccurate, the improvement over the direct baseline is marginal, and the lack of ablation studies makes it difficult to attribute the results to the proposed architectural innovations. The work has merit as a preliminary exploration, but as presented it does not provide sufficient evidence of a substantial contribution to warrant acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>