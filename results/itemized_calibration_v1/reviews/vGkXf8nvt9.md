Now let me write the final review with all the calibration data properly integrated.

## Summary

The paper proposes Forget-to-Focus (F2F), a two-stage protocol that performs targeted unlearning on general-domain data before fine-tuning LLMs on specialized domains (coding, math, medical). F2F uses gradient ascent on a "forget set" of general data (plus gradient descent on a small "retain set" for stability) and then standard fine-tuning. Experiments cover five model scales (0.6B–72B) across multiple architectures.

## Strengths

1. **Novel framing of unlearning for domain adaptation.** Repurposing machine unlearning (normally for privacy) as a preparatory tool for domain specialization is conceptually interesting and, to the authors' knowledge, not studied at this scale before. The idea that suppressing interfering pretraining knowledge before fine-tuning can help is worth investigating.

2. **Broad experimental coverage.** The paper tests across three domains (coding, math, medical) and five models spanning 0.6B to 72B parameters across Qwen, LLaMA, and Gemma families — genuinely different architectures and scales.

3. **Representational analysis provides a plausible mechanistic story.** Section 4.5 uses CKA and SVCCA to show that F2F shifts representations further from the base model than standard fine-tuning, and that the shift is structured divergence rather than random drift. This goes beyond reporting only accuracy numbers.

## Weaknesses

### Fatal

None.

### Major

1. **Structural confound: retain set is drawn from the fine-tuning data, giving F2F extra exposure to the target domain.** The paper states *"The retain set is a small subset of the fine-tuning data"* (Section 3.3). The unlearning phase applies gradient descent on this retain set (Equation 3), meaning the model sees and trains on a portion of downstream data *before* the fine-tuning phase begins. Standard baselines (SFT, LoRA, DAPT, CurlLoRA) do not receive this extra exposure. Any performance gain could be driven by additional training signal rather than by the unlearning mechanism itself. A controlled comparison would need either (a) a baseline where the same subset of D is also used for additional training before fine-tuning, or (b) an F2F variant where the retain set is held out from D. Without this control, the paper's central claim — that gains come from *forgetting* irrelevant general knowledge — cannot be disentangled from the trivial explanation that F2F simply trains on more domain-relevant data.

2. **Major claims in abstract and contributions are not evidenced in the main body.**
   - **Calibration improvement:** The abstract states *"unlearning prior fine-tuning helps improved calibration on medical QA tasks, reducing overconfidence"* and the contributions list claims *"improving calibration on sensitive tasks such as medical QAs."* The conclusion repeats this. Yet the main body contains *zero* calibration results — no ECE, no reliability diagrams, no confidence analysis. The word "calibrat" appears only in the abstract, contributions list, and conclusion (verified by grep).
   - **Fisher information and PCA-shift analyses:** Contribution 4 claims the paper uses *"Fisher information, PCA-shift analyses"* to show *"unlearning reshapes representational geometry, reallocated parameter sensitivity."* These analyses are mentioned only in the contributions list and conclusion — they do not appear in the main body. Section 4.5 presents only CKA and SVCCA.
   These are clear evidential failures: the conclusions may be true, but the paper does not present the promised evidence.

3. **No statistical significance or variance reporting.** Every result in Tables 1–3 is a single scalar with no variance estimate. There is no mention of random seeds, number of runs, or confidence intervals. Given that many claimed gains are modest (e.g., Qwen 0.6B MBPP: DAPT 29.30 → F2F 31.60, a 2.3-point gain) and some are very large (LLaMA 8B PubMedQA: SFT 45.31 → F2F 89.90), it is impossible to assess whether differences are meaningful or noise.

4. **Table 3 contains data that appears to be a copy-paste error.** The "Baseline" row for LLaMA3.1-8B under BC-Cosine reports MBPP=22.60 and HumanEval=19.50. These are *exactly* the Qwen3-0.6B base model values from Table 1. The actual LLaMA-8B base model values from Table 1 are MBPP=49.00, HumanEval=33.54. The BC-Cosine Baseline medical values (PubMedQA=57.80, MedMCQA=32.25) also differ substantially from Table 2's SFT values for LLaMA 8B (45.31, 13.06) with no explanation. This undermines confidence in the entire table.

5. **Unlearning mechanism is not verified.** The paper never evaluates whether the unlearning step actually reduces the model's performance on the forget set or general-domain benchmarks. The "Unl_GA+GD" rows in Table 1 show mixed results (e.g., Qwen 0.6B slightly *improves* on both MBPP and HumanEval after unlearning, contrary to the forgetting narrative), and the GA-only variant causes catastrophic forgetting for LLaMA 8B (HumanEval drops from 33.54 to 1.20) but barely affects Qwen 0.6B. Without verification that forgetting is actually occurring in the intended way, the mechanism is conjectural.

### Minor

6. **Qwen 72B experiments use a different protocol.** For the 72B model, the paper uses 4-bit quantization, only 50% of the dataset, and QLoRA (rank 16) for the unlearning step (Section 3.4). The baselines for this model are not described as using the same constraints. If baselines used full precision or the full dataset, the comparison is not controlled. Additionally, F2F for 72B operates entirely via LoRA adapters — a different regime from the full-parameter unlearning used for smaller models — and the paper does not discuss how this affects the comparison.

7. **Theoretical analysis does not bridge to practice.** The Proposition and Corollary (Section 2) analyze a convex linear surrogate with orthogonal feature decomposition, concluding that unlearning contracts irrelevant parameter directions. The paper acknowledges this is a "convex linear surrogate" but does not discuss how the analysis breaks down for deep nonlinear networks where the feature space does not decompose orthogonally into "relevant" and "irrelevant" directions, and gradient ascent on the forget set could suppress relevant directions as easily as irrelevant ones. The bound also depends on quantities (μ_F, G_R) that are never estimated, making the analysis purely qualitative.

8. **DAPT baseline is underdescribed.** The paper does not specify how many tokens or steps of domain-adaptive pretraining were used, or whether DAPT used unlabeled domain text while F2F used labeled data during its retain-set training. Without these details, the comparison is not fully specified.

### Trivial

9. **Figure 3 y-axis is not labeled** in the caption; the metric is not specified.

## Nice-to-Haves

- Report computational cost (GPU-hours) of F2F relative to standard fine-tuning, so practitioners can assess the cost-benefit tradeoff.
- Ablate retain-set size to show sensitivity to this key hyperparameter.
- Report multiple random seeds with standard deviations for all main results.
- Add verification of forgetting by evaluating the unlearned model on general-domain benchmarks (e.g., MMLU).

## Removed Points

*These points were raised by the harsh critic but are removed as invalid, inaccurate, or otherwise not suitable:*

- *"32.5% on HumanEval conflates percentage points with relative improvement"* — The abstract says "compared to standard fine-tuning." SFT scores 31.71, F2F scores 42.07; (42.07−31.71)/31.71 ≈ 32.7% relative improvement, which matches the paper's claim. The criticism mistakenly compares against the base model (19.50) instead of SFT. **Removed (factually wrong).**

- *"Figure 3 values differ from Table 2 SFT values"* — Figure 3 shows F2F results (unlearning + tuning), which are expected to exceed SFT if F2F works. Comparing F2F results to SFT baselines is not a discrepancy. **Removed (misunderstands figure).**

- *"CKA evidence could indicate overfitting"* — Speculative; the paper's interpretation of CKA is reasonable. **Removed (speculative).**

- *"Related work citation mismatch"* — Per meta-reviewer rules, missing or incorrect related work citations should not be raised. **Removed (per rule).**

- *Formatting/style nitpicks* — Removed as non-substantive.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Control for the retain-set confound.** Run an ablation where the retain set is held out from the fine-tuning data, or where the standard fine-tuning baseline receives equivalent additional exposure to a subset of D. This is the single most important experiment to salvage the paper's central claim.

2. **Present the promised evidence.** Either add calibration results (ECE, reliability diagrams) for medical tasks and Fisher/PCA analyses to the main body, or remove these claims from the abstract and contributions.

3. **Fix the Table 3 data error.** The BC-Cosine "Baseline" row for LLaMA 8B reports Qwen 0.6B's base model values instead of LLaMA 8B's. Verify and correct the entire table.

4. **Add multiple random seeds** (at least 3) with standard deviations for all main results.

5. **Verify forgetting** by evaluating the unlearned model on a general-domain benchmark.

## Calibration Note

The paper was compared against human-reviewed anchors in the deepreview_13k_calibration dataset. The closest topical anchor, **f5o6kWRC0A.md** (avg 4.00 — "Machine Unlearning For Alleviating Negative Transfer in Partial-Set SFUDA"), received a weight -5 weakness for "unfair experimental setup" and was rejected. The current paper's retain-set confound is similarly severe. Another close anchor, **CGfWyU28Pd.md** (avg 4.50 — "Why Fine-Tuning Struggles with Forgetting"), received scores 6,3,3,6 with weaknesses about missing connections between theory and practice. Both anchors share the pattern of an interesting idea undermined by evaluation concerns. The paper under review has additional problems (missing promised evidence, data error) that place it below both anchors. Papers in the 5.5–7.5 range (e.g., **6ESRicalFE.md** avg 6.50, **Q1MHvGmhyT.md** avg 6.00) all had stronger empirical validation, reproducibility practices, and supported their claims. This paper does not meet that bar.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>