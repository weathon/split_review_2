## Summary

TWINFLOW extends the flow matching time interval from $[0,1]$ to $[-1,1]$, creating twin trajectories where the positive branch maps noise to real data and the negative branch maps noise to self-generated "fake" data. The core objective matches the velocity fields of these two trajectories, combining a base any-step loss ($\mathcal{L}_{\text{base}}$), an adversarial flow-matching loss on fake data ($\mathcal{L}_{\text{adv}}$), and a rectification loss ($\mathcal{L}_{\text{rectify}}$) that aligns the two velocity fields. The key practical advantage is that the method requires no auxiliary discriminator network, no frozen teacher model, and no separate fake-score network — a single model handles everything. This enables full-parameter 1-step training at the 20B-parameter scale (Qwen-Image-20B), where competing methods (DMD2, SANA-Sprint) OOM even at batch size 1.

## Strengths

1. **Clean architectural simplicity with measurable memory advantage.** Table 1 and Figure 2b make the practical case concretely: DMD2 + Qwen-Image-20B OOMs at batch size 1, while TWINFLOW fits batch size 24 in 76 GB. No auxiliary discriminators, no frozen teacher models, no separate fake-score networks — this is a genuine simplification over DMD, DMD2, and SANA-Sprint.

2. **Impressive scaling to 20B parameters is the paper's strongest result.** Table 3 shows full-parameter training on Qwen-Image-20B achieving GenEval 0.85 (1-NFE) and 0.89 (longer training), closely matching the original 100-NFE model's 0.87. All competing methods (VSD, DMD\*, SiD, sCM, MeanFlow, RCGM) score substantially lower at 1-NFE. The OOM rows for VSD/DMD/SiD in their raw (non-LoRA) configurations underline the practical difficulty of scaling prior approaches.

3. **Consistent improvement demonstrated across architectures.** Figure 4b shows that adding $\mathcal{L}_{\text{TwinFlow}}$ produces large gains on OpenUni, SANA, and especially Qwen-Image (from 59.50 to 86.52 DPG-Bench). The $\lambda$ sweep in Figure 4a is well-motivated and shows a clear, interpretable optimum at $1/3$.

4. **Competitive 1-NFE results on standard text-to-image benchmarks.** On GenEval at 1-NFE, TWINFLOW-0.6B scores 0.83, outperforming SANA-Sprint-1.6B (0.76), RCGM-1.6B (0.78), and FLUX-Schnell (0.69). With longer training on Qwen-Image-20B, the model reaches 0.89 GenEval at 1-NFE — genuinely state-of-the-art for single-step generation at this scale.

## Weaknesses

### Fatal
None.

### Major

1. **The Qwen-Image-RCGM baseline (GenEval 0.52, Table 2) is suspiciously low and inflates the claimed advantage.** In Table 2, Qwen-Image-RCGM achieves only 0.52 GenEval at 1-NFE. But RCGM achieves 0.80 at 1-NFE on OpenUni-512 (same table) and 0.80 on SANA-0.6B (Table 4). A 35% relative drop on the same metric, on the same architecture family, strongly suggests undertuning or a suboptimal training setup rather than a fundamental limitation of RCGM. The paper highlights a "notable improvement of 0.34" over this baseline, but this number is not credible without evidence that RCGM received comparable hyperparameter tuning or training resources on Qwen-Image. The paper's core results (Table 3 full-parameter 20B, Table 4 SANA-based) are strong enough to stand without this comparison; the authors should either substantiate the RCGM-0.52 result or remove the comparison and let the more credible results speak for themselves.

### Minor

2. **The theoretical derivation (Section 3.2, Eqs. 3–9) claims more than it proves and should be reframed.** The derivation shows that if the network outputs $F_\theta(x_t, t)$ and $F_\theta(x_t, -t)$ correctly approximate the score functions of $p_{\text{real}}$ and $p_{\text{fake}}$ respectively, then matching them minimizes KL divergence. This is a valid algebraic relationship *given* the score approximations. However, the derivation does not address the key practical concern: a single network with shared parameters is asked to simultaneously learn two different velocity fields (one for $p_{\text{real}}$ on positive time, one for $p_{\text{fake}}$ on negative time) using different loss terms ($\mathcal{L}_{\text{adv}}$ and $\mathcal{L}_{\text{base}}$), and whether these roles remain separated during joint optimization is an empirical question the theory does not resolve. The method works empirically, but the presented derivation is a motivation (velocity matching ≈ distribution matching under certain ideal conditions), not a proof. The paper would be strengthened by acknowledging this gap and characterizing $\mathcal{L}_{\text{rectify}}$ more honestly (e.g., as a regularizer encouraging time-consistency of the velocity field).

3. **The claim of "severe mode collapse" against Qwen-Image-Lightning lacks quantitative support.** The paper states that Qwen-Image-Lightning "suffers from severe mode collapse" and "generates almost identical images for the same prompt" (Table 2 footnote, Section 4.2). Yet Lightning achieves DPG-Bench 87.79 (vs. TWINFLOW 86.52) and GenEval 0.85 (vs. TWINFLOW 0.86 at 1-NFE). The paper references visual comparisons in Appendix E.1, but this is a strong claim about a direct competitor that should be backed with quantitative diversity metrics (e.g., LPIPS variance across noise seeds, FID recall, or intra-class diversity). If the claim is true, provide the metrics; if not, remove the claim.

4. **No individual ablation of $\mathcal{L}_{\text{adv}}$ and $\mathcal{L}_{\text{rectify}}$.** Figure 4b ablates $\mathcal{L}_{\text{TwinFlow}}$ as a unit but never separates its two components. Given that $\mathcal{L}_{\text{adv}}$ (flow matching on fake data) and $\mathcal{L}_{\text{rectify}}$ (velocity matching) are motivated differently, understanding their independent contributions would strengthen the paper and guide future applications.

5. **Baselines in Table 3 use LoRA (r=64) for the fake score function while TWINFLOW uses full parameters.** The paper is transparent about this constraint (the raw "separate models" configuration OOMs), and it is a genuine memory limitation of multi-model approaches. However, the comparison partly reflects an implementation constraint — if LoRA approximation degrades the baselines — rather than a purely algorithmic advantage. The authors should discuss this caveat explicitly when interpreting Table 3.

### Trivial

6. **Equation (8) uses "$\propto$" to mask an incomplete Jacobian derivation.** The term $-\frac{\partial \mathbf{F}_\theta(\mathbf{x}_t^{\text{real}}, r)}{\partial \theta}$ appears without clear justification from the stated definition of $\mathbf{x}^{\text{fake}}$, and the proportionality symbol obscures the algebra.

7. **The batch-splitting mechanism for $\lambda$ (Section 3.3) is an unusual design choice.** Using separate batch subsets for $\mathcal{L}_{\text{base}}$ and $\mathcal{L}_{\text{TwinFlow}}$ increases gradient variance compared to a standard weighted-loss formulation. The ablation in Figure 4a does not compare these two approaches, so it is unclear whether the batch-splitting is essential or incidental.

## Nice-to-Haves

- **Individual ablation of $\mathcal{L}_{\text{adv}}$ vs. $\mathcal{L}_{\text{rectify}}$** (see Weakness 4 above).
- **EMA or target network discussion.** Self-distillation and consistency-training methods typically use an EMA or target network when a model learns from its own outputs. If TWINFLOW does not need one, that is worth explaining, as it is a notable design distinction.
- **Clarify whether $\mathbf{x}^{\text{fake}}$ is generated using the current model parameters at each step** and whether this requires an additional forward pass. The information is present in the text but could be clearer for reproducibility.

## Removed Points

These points were flagged in the input review but removed or redirected after verification against the paper:

- **"Understates relationship to consistency models"** — The paper explicitly mentions consistency models in the introduction, Table 1 (row: "Consistency training & distillation"), and Section 2 (as instances of the any-step framework). The depth of discussion is appropriate for a method paper. Removed per the rule against faulting a paper for not expanding related work to the reviewer's preferred depth.
- **"Appendix E.1 not verifiable from the main paper"** — The core concern (lack of quantitative diversity metrics) is retained in Weakness 3. The specific complaint about the appendix being unverifiable is removed per the rule that the parser strips appendices and they exist in the original submission.
- **Some framing of the theoretical derivation as "fatal circularity"** — The actual concern (shared-parameter gap between theory and practice) is retained in Weakness 2 but downgraded from fatal to minor, as the derivation is a valid algebraic relationship under stated conditions, not a circular argument.

## Novel Insights

The most valuable observation emerging from the reviews is that the paper's strongest evidence is its 20B full-parameter results (Table 3), where TWINFLOW's memory advantage is simultaneously a practical enabler and a confound: the method wins partly because it *can* run full-parameter while competitors are forced into LoRA approximations. The second insightful point is that the theoretical framing (Section 3.2) would be more honest and more useful as a "velocity-consistency regularizer" motivation rather than as a KL-divergence derivation, since the shared-parameter joint optimization is the actual empirical novelty, not the algebraic manipulation.

## Suggestions

1. **RCGM comparison (Table 2):** Either provide evidence that RCGM on Qwen-Image received a comparable hyperparameter search and training budget, or remove the Qwen-Image-RCGM row. The 0.52 number undermines credibility; without it, the remaining results are still strong.

2. **Mode collapse claim:** Either add quantitative diversity metrics for Qwen-Image-Lightning (and all compared 1-NFE methods, for fairness) or remove the claim.

3. **Theoretical framing:** Reframe Section 3.2 as a motivation showing that *under idealized conditions* velocity matching corresponds to distribution matching, and clearly note that the single-network shared-parameter setting introduces practical complexities not captured by this derivation.

4. **Ablation:** Add separate ablation of $\mathcal{L}_{\text{adv}}$ and $\mathcal{L}_{\text{rectify}}$ to clarify their individual contributions.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>