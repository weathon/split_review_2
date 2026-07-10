Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes LoLoRA, a method that combines local Hebbian PCA (HPCA) updates for the A matrix in LoRA during the forward pass with standard backprop for the B matrix, aiming to reduce activation memory while maintaining performance. The paper also provides a theoretical analysis (Theorem 4.4) showing that the optimal initialization of A under certain assumptions is any nonsingular linear transformation of the top-r eigenvectors of the input covariance, formalizing and extending the empirical EVA approach.

## Strengths

- **Theoretical analysis of optimal A initialization (Theorem 4.4, Section 4).** The paper provides a clean theoretical result: under stated assumptions, the optimal A for frozen-A LoRA is any nonsingular linear transformation of the top-r eigenvectors of the input covariance. This formalizes and extends the empirical findings of EVA (Paischer et al., 2024). The proof structure is coherent and the asymmetry between A and B adapters is well-supported.

- **The HPCA-based local update mechanism is novel and well-motivated.** Combining Hebbian PCA updates (SNL algorithm) for A during the forward pass with standard backprop for B is a reasonable design choice. Algorithm 1 correctly shows how activations can be freed after A's local update while retaining the compressed representation u = Az for B's backward pass.

- **Experimental breadth across three substantially different settings.** The paper evaluates on RoBERTa-large on GLUE (NLU), LLaMA-3.1-8B on MetaMathQA (mathematical reasoning), and LLaVA-v1.5-7B (multimodal), plus ablations on TinyLlama. This provides reasonable coverage across model sizes and task types.

## Weaknesses

### Fatal
None.

### Major

- **LoLoRA and LoRA-FA (EVA) are empirically tied across all experimental settings, undercutting the paper's central narrative.** On GLUE (Tables 1-2), LoLoRA is numerically ahead of LoRA-FA(EVA) on 5/8 tasks but all differences are within one standard deviation. On MetaMathQA (Table 3), both achieve 0.829±0.004/0.005 — an exact tie. On LLaVA (Table 4), LoRA-FA(EVA) slightly edges LoLoRA (2.92 vs 2.93 perplexity). On TinyLlama ablations (Tables 5-6), LoRA-FA(EVA) at r=8 achieves 2.536±0.010 vs LoLoRA HPCA's 2.535±0.011. The paper's own text acknowledges that "LoRA-FA with EVA initialization achieves comparable performance" (line 328). LoLoRA's performance advantage is only relative to uniform-initialized LoRA-FA, yet the abstract and introduction frame LoRA-FA's performance degradation as a problem that LoLoRA uniquely addresses, without clarifying that EVA initialization already fixes this. The strongest honest claim supported by the evidence is that LoLoRA provides an online approximation of the EVA initialization that avoids a separate PCA pre-training pass, but this is not the paper's emphasized narrative.

- **Standard LoRA consistently outperforms LoLoRA across most evaluations.** On GLUE (Tables 1-2), standard LoRA achieves the best result on 6/8 tasks; LoLoRA never wins any task and trails on several by non-trivial margins (CoLA: 69.6 vs 66.3, a 3.3-point gap; QQP: 91.7 vs 90.6). On LLaVA (Table 4), standard LoRA achieves 2.90 perplexity vs LoLoRA's 2.93. The abstract claims the method "maintains performance comparable to standard LoRA," which is defensible in aggregate but understates the consistent gap on NLU tasks. The memory savings (~0.5 GB on LLaVA, ~4 GB on MetaMathQA) are real but modest relative to the performance gap.

### Minor

- **The theoretical result (Theorem 4.4) relies on Assumption 4.1: entries of ΔW₀ are i.i.d. Gaussian with zero mean.** This is an isotropic noise assumption that strips away task-relevant structure from the optimal weight change, making the result (optimal A = top eigenvectors of input covariance) largely a consequence of the assumption itself — under this assumption the target has no structure, so the only signal comes from the input covariance. The paper acknowledges the submodule isolation limitation in the conclusion but does not discuss how violations of the i.i.d. Gaussian assumption would affect the practical implications.

- **No statistical significance testing is reported.** Given that nearly all key comparisons (LoLoRA vs LoRA-FA(EVA)) differ by less than one standard deviation, significance tests would help assess whether any claimed advantage is meaningful.

- **The memory comparison reports aggregate "Extra Memory (GB)" but lacks a detailed breakdown** (activations for A vs B, optimizer states, HPCA optimizer state). This makes it difficult to verify why LoLoRA uses slightly more memory than LoRA-FA (24.1 GB vs 23.9 GB on LLaVA, Table 4) and to understand where the claimed savings originate.

### Trivial

- **The paper cites Local LoRA (Key et al., 2023) in the related work as a relevant local-learning PEFT method but does not include it as an experimental baseline.**

- **Weight_decay is set to 0.0 for all methods (line 235), which is atypical for LoRA fine-tuning (most implementations use small weight decay). This may differentially affect methods with different numbers of trainable parameters.**

## Nice-to-Haves

- Reframe the contribution to honestly position LoLoRA as an online alternative to EVA that avoids a separate PCA pre-training pass, rather than implying performance improvement over LoRA-FA broadly.
- Provide a controlled comparison isolating EVA's initialization overhead from HPCA's per-step overhead in wall-clock time.
- Directly measure subspace convergence (cosine similarity between learned A and top eigenvectors of Σ_zz) to strengthen the link between theory and practice.
- Provide a memory breakdown table showing contributions from activations (A), activations (B), optimizer states (A/B), and HPCA optimizer state.

## Removed Points

These points from the input review were removed with justification:

1. **"Memory claims are misleading / the word 'further' implies reduction relative to LoRA-FA"** — REMOVED: The abstract's memory claim compares to standard LoRA ("maintains performance comparable to standard LoRA while further reducing the memory"), not to LoRA-FA. The paper accurately describes both methods' memory profiles, and the conclusion acknowledges the extra optimizer state for LoLoRA.
2. **"The paper's framing inverts reality about memory savings"** — REMOVED: The paper accurately states LoRA-FA saves both activations AND optimizer states (line 15) while LoLoRA saves activations only. Both descriptions are factually correct.
3. **"Algorithm 1 ordering issue / Figure 1 clarity"** — REMOVED: The critic confirms the ordering is correct (local rule before FREE_MEMORY(z)); this is at most a presentation preference.
4. **"Lines 89-91 understate EVA contribution"** — REMOVED: The paper properly cites EVA and claims novelty in the theoretical proof. The sentence "We make the next step further by showing that just random initialization might not be the best for A" is about the theoretical derivation, not about discovering the phenomenon.
5. **"EVA initialization cost conflated with HPCA overhead"** — MERGED into the nice-to-have about controlled time comparison.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Rewrite the abstract and introduction to honestly position LoLoRA as providing comparable performance to EVA-initialized LoRA-FA without requiring a separate PCA pre-training pass, rather than implying performance improvement over LoRA-FA broadly.
2. Add significance testing or effect sizes for the main comparisons.
3. Include a memory breakdown table.
4. Add Local LoRA (Key et al., 2023) as an experimental baseline.
5. Discuss the implications of Assumption 4.1 — under what conditions would violations of the i.i.d. Gaussian assumption change the practical predictions?

## Score and Decision

**Calibration:** The paper was compared against 10 human-reviewed anchors across the score spectrum. The most directly relevant anchors are EVA (avg 4.75, Reject), LoRA-FA (avg 5.33, Reject), and ReLoRA (avg 5.75, Accept). LoLoRA has stronger theoretical contribution than EVA and LoRA-FA, but the experimental narrative (LoLoRA improves over LoRA-FA) is not supported when EVA initialization is considered — the two are empirically tied everywhere. This gap between claims and evidence is more severe than in ReLoRA (whose performance limitations were acknowledged upfront) and comparable to the narrative issues that led to EVA's rejection. The paper's strengths (strong theory, novel method) are genuine, placing it above ALLoRA (3.33) and EVA (4.75), but the framing problem prevents acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>