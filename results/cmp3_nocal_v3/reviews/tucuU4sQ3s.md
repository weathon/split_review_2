Now I have all the verification I need. Here is the final consolidated review.

---

## Summary

This paper proposes NuSA-CL, a continual learning method for CLIP-style vision-language models. At each task, NuSA-CL performs SVD on the current weight matrices to identify a low-energy "null space," then constrains low-rank updates (via a trainable intermediate matrix M sandwiched between frozen SVD basis vectors) to strictly stay within that subspace. After training, the update is merged back into the backbone so parameter count stays fixed. The method requires no replay buffer, no distillation, and no growing module library.

## Strengths

1. **Well-motivated design addressing a real scalability bottleneck.** The paper correctly identifies that existing CL paradigms (storage-based methods whose memory grows with tasks, expansion-based methods whose parameter count grows) are poorly suited for lifelong deployment of foundation models. Section 1 (lines 14–27) makes this case concretely.

2. **Clean, differentiated mechanism with decisive ablation evidence.** The persistent constraint (freezing U_n, V_n and training only M in Equation 3) is a clear design distinction from related work like MiLoRA that uses the null space only for initialization. Table 4a confirms this matters: unfreezing U_n, V_n drops Transfer from 68.58 to 62.60 and Last from 82.79 to 77.32.

3. **Impressive efficiency numbers.** NuSA-CL uses 1.5M trainable parameters (vs. 59.8M for MoE-Adapters), 1.21 GPU-hours (vs. 47.24 for ZSCL), and 6.6 GB peak GPU memory (tied for lowest). These are specific, verifiable, and substantiated in Table 1.

4. **Strong evidence of long-sequence scalability.** On CIFAR-100 (Table 3), NuSA-CL's Last accuracy drops only ~2.7% from 10-step to 50-step, while ZSCL drops ~6.3%. At 50 steps, NuSA-CL achieves 71.85% Last accuracy vs. 67.36% for ZSCL, a gap that widens with sequence length.

5. **Principled analysis of null-space dynamics.** Section 6.1 provides spectral evidence (Figure 2) showing NuSA-CL's effective rank increasing over tasks while LoRA/Full-FT remain static, supporting the "accumulation vs. overwriting" narrative. The claim that even after 10 tasks the most saturated layer retains 313.58 null directions (>2× the update rank of 128) is specific and testable.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **"Memory-free" and "zero storage overhead" framing overstates the case.** The paper describes NuSA-CL as "memory-free," "storage-free," and having "zero storage overhead" (abstract, lines 28, 50, 190; Tables 1–2). However, during training the SVD basis matrices U_n and V_n are stored in GPU memory for every adapted layer (Section 3.2: "the basis matrices U_n and V_n are … kept frozen during training"). For ViT-B/16's vision encoder alone (12 layers × 4 projections, d=768, r_max=128), this is roughly 9.4M additional stored values (~37 MB in float32) — more than InflLoRA's 9MB gradient projection memory. The paper's Table 1 lists "None" for NuSA-CL's additional storage while flagging InflLoRA's 9MB. The key distinction — that NuSA-CL's storage is per-task and does not accumulate — is valid and important, but the categorical "zero storage overhead" and "strictly storage-free" framing creates an artificially sharp contrast. The claim should be qualified as "no accumulating external storage."

2. **No statistical significance or variance reporting despite modest performance margins.** The paper reports only single-run numbers throughout. In Table 2, the Transfer gap between NuSA-CL (68.1) and InflLoRA (66.8) is just 1.3 pp, and on individual datasets NuSA-CL leads on some (EuroSAT: 55.8 vs. 52.1) but trails on others (DTD: 43.3 vs. 44.5). No confidence intervals, standard deviations, or multi-seed results are reported anywhere. Given that CL results can vary with random seed, initialization, and data ordering, the claim that NuSA-CL "decisively outperforms" InflLoRA (line 194) would be better supported by reporting means and standard deviations over 3–5 runs.

3. **The theoretical analysis provides parameter-space intuition but not a forgetting guarantee.** Lemma 1 and Theorem 2 bound the Frobenius inner product ⟨W, ΔW⟩_F, a parameter-space quantity. The paper acknowledges this (line 122: "should be viewed as a local stability condition rather than a full function-level guarantee"). However, Section 4 is titled "Theoretical Motivation" and frames the bounds as a "principled mechanism for mitigating catastrophic forgetting" (line 120). The connection from small parameter-space inner products to small function-level forgetting requires smoothness assumptions that are mentioned in passing but never formalized. This is not a flaw in the method — the empirical results carry the weight — but the section title and framing should be adjusted to better match what is delivered.

4. **Task-order sensitivity is acknowledged but not empirically investigated.** The method is cyclical: the null space available for task t depends on the cumulative weight trajectory from all previous tasks, making order a first-order property. The paper acknowledges this as future work (line 292) but provides no empirical investigation — not even a single order permutation experiment on a subset of tasks. While not fatal, this is a gap in understanding the method's robustness given that the MTIL benchmark uses a single fixed order.

### Trivial

- **SVD cost breakdown not provided.** Table 4b reports SVD takes "<1 min" but does not specify how many decompositions are computed per task (number of layers × projections) or the wall-clock time scaling.
- **Effect of energy cutoff ρ on null-space size not analyzed.** The ablation in Table 4b shows robustness to ρ, but how ρ determines d−k and hence the effective update rank is not discussed mechanistically.
- **No task-by-task zero-shot transfer tracking.** Transfer is reported only at the end; tracking how zero-shot capability evolves across tasks would be more informative.

## Nice-to-Haves

- A task-order permutation study on a subset of the MTIL dataset (e.g., 5 tasks, 5 random orders) would directly address the core vulnerability of a sequence-dependent null-space recomputation strategy.
- Multi-seed results (3–5 runs with standard deviations) for the main tables would confirm whether the modest margins over InflLoRA are systematic or within noise.
- Repositioning Section 4 as "Intuition" rather than "Theoretical Motivation" would better match the heuristic nature of the parameter-space analysis.

## Removed Points

These points appeared in the input review but were removed after verification against the paper:

- **"Data-agnostic" framing criticism:** The critic claimed "the method still requires standard supervised training data for each task" as an objection to the "data-agnostic" claim. However, the paper uses "data-agnostic" to specifically describe the SVD-based null space identification (line 58), not the overall training. The SVD is computed on weights, not data, so the description is correct. This criticism misunderstands the paper.
- **Missing per-dataset results for Aircraft Transfer row:** The critic flagged the "-" entries in Table 2's Aircraft/Transfer cell as unexplained. These are standard: Aircraft is the first task, so it cannot be "unseen" for a zero-shot Transfer measurement after task 1.
- **Criticism that theory is "simple linear algebra" and title should change:** The paper already titles the section "Theoretical Motivation" (not "Theoretical Guarantee") and explicitly acknowledges the parameter-space limitation in line 122. The retained Minor weakness #3 already captures the residual concern.

## Novel Insights

None beyond the paper's own contributions. The input review identifies standard review concerns (variance reporting, framing precision, task-order sensitivity) that are well-recognized in the CL literature.

## Suggestions

1. Qualify the "memory-free" and "zero storage overhead" terminology throughout: replace with "no accumulating external storage" or "fixed per-task storage" to accurately describe the method's properties.
2. Add multi-seed results with standard deviations for the main tables (Table 1, Table 2, Table 3), especially given modest margins over InflLoRA.
3. Reposition Section 4 as "Intuition" or "Motivation" to more accurately reflect the heuristic nature of the parameter-space analysis, or formally connect the bound to function-level forgetting via Lipschitz constants.
4. Include at least a small-scale task-order permutation experiment to demonstrate robustness to ordering.
5. Break down the SVD computation cost per task (number of decompositions × matrix sizes) to contextualize the "<1 min" claim.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>