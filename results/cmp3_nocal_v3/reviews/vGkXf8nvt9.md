Now I have all the information I need. Let me compose the final consolidated review.

---

## Summary

This paper proposes **Forget-to-Focus (F2F)**, a two-stage protocol that first performs targeted machine unlearning on a "forget set" (general-domain data) and then fine-tunes on a domain-specific dataset. The central idea — repurposing unlearning from a privacy tool into a preparatory step for domain specialization — is genuinely novel. Experiments span 5 model families (0.6B–72B), 3 domains (coding, medical, mathematics), 4 unlearning variants, and 4 fine-tuning baselines, showing consistent accuracy gains.

## Strengths

1. **Novel and well-motivated research question.** Reframing machine unlearning — almost exclusively studied for privacy — as a preparatory intervention for domain adaptation is a non-obvious inversion. The motivation (suppressing interfering pretraining priors) is clearly articulated in Section 1.

2. **Unusually broad empirical scope.** The evaluation covers 5 model families (Qwen-0.6B, Gemma-2B, LLaMA-8B, LLaMA-13B, Qwen-72B), 3 domains (coding, medical, mathematics), 4 unlearning variants (GA, GA+GD, GA+KL, NPO), and 4 fine-tuning baselines (SFT, DAPT, LoRA, CurlLoRA). Tables 1 and 3 are information-dense and this breadth reduces the risk of findings being artifacts of a single setup.

3. **Representational analysis (CKA, SVCCA) in Section 4.5 goes beyond reporting accuracy.** Characterizing *why* F2F works via representational geometry — showing that F2F produces more pronounced representational shifts than standard fine-tuning — is a real strength, even if the interpretation is correlational.

4. **Well-designed analysis of forget-set quality (Section 4.4, Table 3).** Varying the forget set from curated (BC-Select) to mixed (BC-Mixed) to cosine-similarity-ranked (BC-Cosine) provides meaningful insight into how the choice of what to forget affects downstream performance. This ablation helps isolate the mechanism.

## Weaknesses

### Fatal
None.

### Major

1. **Claims of calibration improvement, Fisher information analysis, and PCA-shift analysis are asserted in the abstract, contributions list, and conclusion but are not substantiated in the main text.** The abstract states F2F "improves calibration on medical QA tasks, reducing overconfidence and mitigating reliability issues." The contributions list (bullet 4) claims "Fisher information, PCA-shift analyses." The conclusion repeats these claims. No calibration scores, reliability diagrams, Fisher information plots, or PCA shift analyses appear in the main paper. The CKA/SVCCA analyses *are* presented; the missing items are additional claimed analyses. This is an evidential gap — the claims may be true, but the paper as written does not demonstrate them. *(Evidence: abstract lines 9–10, contribution list line 30, conclusion line 301; no calibration/Fisher/PCA content in main body.)*

2. **The DAPT baseline is likely underpowered, making F2F appear more advantageous.** DAPT (Domain-Adaptive Pretraining) is the closest relative to F2F because both methods involve additional training *before* fine-tuning. A properly configured DAPT has been shown to produce substantial gains (Gururangan et al., 2020). Yet in Table 1, DAPT barely outperforms SFT on several configurations and is *worse* on others (e.g., LLaMA-8B MBPP: SFT 56.60 vs DAPT 53.55). The paper provides no details on how much domain text was used for DAPT, for how many steps it was trained, or whether its hyperparameters were tuned. Without this, the comparison against F2F — which receives a dedicated unlearning phase with its own hyperparameter budget — is fundamentally asymmetric. *(Evidence: Section 3.2 gives only a one-sentence description of DAPT; no training details in Section 3.4; Table 1 shows DAPT underperforming SFT on multiple configurations.)*

3. **No variance or statistical significance is reported for any result.** Every number in Tables 1, 2, and 3 is a single point without error bars, standard deviations, or confidence intervals. The forget sets are small (100–1000 samples) and the unlearning step introduces stochasticity through gradient ascent. Without multiple runs or significance testing, it is impossible to assess whether observed gaps (e.g., the 31.60 vs. 29.90 on MBPP in Table 3) are reliable or noise. *(Evidence: all tables report single-point values only.)*

### Minor

1. **LLaMA-13B base model scores 0.60 pass@1 on HumanEval, which is anomalous.** This is far below any reasonable expectation for a LLaMA-2 13B checkpoint (LLaMA-8B, by comparison, scores 33.54). This makes F2F's improvement (0.60 → 46.15) appear dramatic, but the gain is largely an artifact of an unusually low baseline. The paper does not explain why this model scores so low, or whether it is a legitimate checkpoints or a evaluation configuration issue. *(Evidence: Table 1, LLaMA-13B base row: 27.22 MBPP, 0.60 HumanEval.)*

2. **The theoretical analysis (Section 2) uses a convex linear surrogate with strong convexity and orthogonality assumptions that do not hold for LLMs.** While the paper acknowledges this ("While LLM training objective is non-convex, we use a convex linear surrogate"), the theory is not connected to any experimental observation. No attempt is made to verify whether the predicted contraction (Equation 5–6) actually occurs in practice, or whether the decomposition into orthogonal relevant/irrelevant subspaces is meaningful for billion-parameter neural networks. The theory provides post-hoc intuition at best and is misleading at worst. *(Evidence: Section 2, lines 57–85.)*

3. **Table 2 is titled in a section labeled "F2F w/ Fine-Tuning Variants" but contains no F2F results.** It only shows baselines (SFT, LoRA, CurlLoRA, DAPT) on medical QA. The actual F2F medical results appear in Figure 3 and Table 3, but the text does not clearly direct the reader there. This breaks the narrative flow. *(Evidence: Section 4.2, Table 2; no F2F entries in the table.)*

4. **The Qwen-72B model uses QLoRA with 4-bit quantization and rank-16 adapters during unlearning, but full fine-tuning afterward.** The paper does not discuss whether quantization noise interacts with gradient-ascent-based unlearning in ways that could affect results, nor whether the unlearning and fine-tuning happening at different levels of parameter fidelity is a confound. *(Evidence: Section 3.4, lines 135 and 148–149.)*

5. **The CKA/SVCCA analysis (Section 4.5) shows that F2F representations diverge more from the unlearned model than standard fine-tuning does, but "more change" is not shown to be "better change."** The paper interprets this as "shifting away from generalist initialization toward structures more conducive to in-domain specialization," but without a quantitative link between CKA divergence and downstream accuracy (or a rigorous causal analysis), this remains suggestive rather than probative. *(Evidence: Section 4.5, Figure 4 caption.)*

### Trivial
None.

## Nice-to-Haves

- **Provide the calibration results or remove the claim from abstract/conclusion.** If calibration data, Fisher information, and PCA-shift analyses exist (e.g., in the appendix), cite specific figures/tables in the main text.
- **Report variance across multiple runs.** Even 2–3 seeds per configuration would provide a sense of stability, given the small forget sets.
- **Document DAPT in detail** — data amount, training steps, hyperparameter tuning — or acknowledge that the DAPT comparison is preliminary.
- **Explain the LLaMA-13B HumanEval anomaly** (the 0.60 baseline), or replace this configuration with one where the baseline is credible.
- **Discuss computational cost** — how much additional compute does the unlearning phase add, and is the accuracy gain worth it?

## Removed Points
These points were flagged for removal (treated with caution):
- **Section 4.1 Gemma-2B "collapse and recovery" alternative interpretation.** The reviewer offered "destruction + restoration" as an alternative reading. This is a matter of interpretation, not a factual error in the paper. The paper presents the results transparently, so the criticism is speculative framing rather than a concrete weakness.
- **"Section 3.3 — using HumanEval in the forget set is unusual."** The paper acknowledges this explicitly (the BC-Mixed set combines 800 BookCorpus samples with 200 domain-related samples) and provides t-SNE visualization showing domain separation. The concern is addressed within the paper.
- **"t-SNE exaggerates separation."** While technically true, this is a well-known property of t-SNE and applies equally to all visualizations in the field. It does not undermine the stated purpose of the figure.
- **General scope-creep criticisms** (e.g., "the paper never systematically addresses challenge (3) — optimization stability"). The paper is a broad empirical study, and demanding a dedicated stability analysis for every challenge listed in the introduction is outside the paper's stated scope.

## Novel Insights
None beyond the paper's own contributions. The reviews surface unsupported claims and baseline calibration issues that the paper should address, but they do not produce a novel interpretation of the results that the paper itself misses.

## Suggestions

1. **Fix the evidential gap:** Either move the calibration/Fisher/PCA results from the (stripped) appendix into the main text (or add explicit cross-references), or remove those claims from the abstract, contributions list, and conclusion. Do not repeat unsupported claims in the paper's most prominent sections.
2. **Address the DAPT asymmetry:** Document the DAPT setup in detail, or acknowledge the limitation and treat DAPT as a lower bound rather than a matched comparison.
3. **Add variance information** to the key tables, even if only from a small number of seeds.
4. **Clarify the LLaMA-13B HumanEval result** — explain why it scores 0.60 or, if it is an error, fix or remove that configuration from the main results.

## Score and Decision

**Score:** 6

**Decision:** Borderline Accept

The paper's central idea — using unlearning as a preparatory step for domain specialization — is genuinely novel. The empirical scope is impressively broad, and the core accuracy results consistently show F2F outperforming standard fine-tuning. The major issues (unsupported claims in high-profile sections, an underpowered DAPT baseline, and no variance reporting) are evidential rather than structural — they can be fixed. However, the paper should not be accepted as-is: the abstract and conclusion claim calibration improvements and Fisher/PCA analyses that are not supported by the presented evidence, and the DAPT comparison needs to be calibrated or qualified. With these resolved, this would be a solid contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>