Now I have enough to write the draft review and calibrate. Let me proceed.Based on my calibration search, I can now establish my bracket and finalize the review.

**Round 1 Bracket**: The paper compares most favorably to VLN-related continual learning papers scoring 6.0–6.5 (e.g., "General Scene Adaptation for VLN" at 6.4, "C-CLIP" at 6.5, and Tucker/tensor PEFT papers at 5.75–6.0). The paper is clearly stronger than rejected continual learning works scoring 4.5–5.0. Initial bracket: **5.5–6.5**.

The paper has solid technical contributions and large empirical margins. The table incompleteness (SD-LoRA missing T23/T24/Avg) and Figure 7 label errors are real editorial issues that reduce confidence in results as currently presented. These push the score slightly toward the lower end of the bracket. I settle on **6.0**.

---

## Summary
This paper formalizes the All-day Multi-scenes Lifelong Vision-and-Language Navigation (AML-VLN) problem, where VLN agents must continually adapt across multiple scenes and diverse illumination environments (normal, low-light, overexposure, scattering) without catastrophic forgetting. The authors propose Tucker Adaptation (TuKA), which represents multi-hierarchical knowledge as a 4th-order tensor via Tucker decomposition, decoupling scene and environment expert vectors from shared core and encoder-decoder subspaces. They introduce a Decoupled Knowledge Incremental Learning (DKIL) strategy and build the AllDay-Habitat simulation platform with physically grounded degradation models.

## Strengths
- **Well-motivated problem with quantified evidence**: Figure 2 documents catastrophic forgetting empirically (79% forgetting rate by task 10), making the problem concrete rather than hypothetical.
- **Technically sound Tucker decomposition design**: Eq. (3) cleanly reduces a 4th-order tensor to a 2D weight update for LLM adaptation via expert vector contraction — a non-trivial dimensional alignment that §3.2 explicitly identifies as a bottleneck in prior tensor-LLM work.
- **Physically grounded benchmark**: Eqs. (10)–(12) use the atmospheric scattering model, camera noise model (shot + read noise), and saturation clipping from established computational photography literature, not ad hoc augmentation, making degradations reproducible and interpretable.
- **Large and credible performance margin**: Table 1 shows AllDayWalker achieving avg SR of 65% vs. next-best BranchLoRA at 44%, with consistently lower forgetting rates (F-SR of 11% vs. 36%) across 24 tasks — a margin large enough that it is not a statistical artifact.
- **Comprehensive baseline coverage and real-world validation**: 12 baselines spanning sequential fine-tuning, EWC, knowledge distillation, and multiple MoE-LoRA variants, plus real-world deployment results.

## Weaknesses

### Fatal
None.

### Major
- **Unexplained blank cells in the primary comparison Table 1**: SD-LoRA's SR results are absent for T23, T24, and the Avg column (line 206). Multiple other baselines (Seq-FT, Lwf-LoRA, O-LoRA, FeedTTA) are also missing Avg values. The paper gives no explanation for why these entries are blank. If methods failed to run on those tasks, this must be stated explicitly; as presented, the primary comparison table has structural gaps that prevent a complete assessment of AllDayWalker's advantage over SD-LoRA — the strongest-performing baseline across its available results.
- **Figure 7 legend shows incorrect model names**: The extracted figure description lists "Ours (blue), BaseModel (orange), Recall (green), Task2Vec (red), and CLIP (purple)" as the five compared models. None of these match the actual baselines in the paper (BranchLoRA, SD-LoRA, HydraLoRA, etc.). This appears to be a leftover legend from an earlier experiment version, and it undermines confidence in whether the SPL/OSR/F-SPL/F-OSR results in Figure 7 reflect the correct comparisons.

### Minor
- **"Two hierarchies" claim is asserted, not proved**: §3.1 states MoE-LoRA variants are "restricted to representing only two hierarchical knowledge structures" as if this were a formal impossibility. In practice, it is a design choice — nested MoE structures or per-level shared matrices could represent more hierarchies. The Figure 8 ablation (3rd-order vs. 4th-order) provides empirical support but does not isolate the structural decoupling benefit from additional capacity.
- **Inference-time expert retrieval receives no accuracy analysis**: §3.4 describes CLIP cosine similarity for scene/environment identification at test time — a critical failure point if retrieval is wrong. No retrieval accuracy metric is reported; Table 5's generalization results conflate retrieval quality and adaptation quality and cannot separate them.
- **Table 3 duplicate rows with inconsistent values**: The full TuKA configuration (Sd-*G*✓, Sd-*U*¹✓, Sd-*U*²✓) appears in rows 3 and 6 of Table 3, with SR=65 in both but OSR=69 vs. OSR=68. This cannot both be correct and requires clarification.
- **Table 5 drops 10 of 12 baselines without justification**: Only BranchLoRA and SD-LoRA are compared in the generalization experiment; no rationale is given for excluding O-LoRA and other baselines.

### Trivial
- §5.1 states task order is "randomized" but does not clarify whether the same random seed is used across all compared methods (required for fair comparison) or whether variance across orderings was evaluated — a known sensitivity in continual learning.

## Nice-to-Haves
- Add a retrieval accuracy analysis (oracle task-id vs. CLIP retrieval) as a supplementary ablation to show navigation improvements are not entangled with retrieval quality.
- Extend Figure 8 to hold parameter count constant between 3rd- and 4th-order tensors, and compare a 4th-order tensor where scene and environment are *not* decoupled, to isolate the structural benefit.
- Briefly discuss the α=1 edge case in DKIL (§3.3): when a scene is revisited, the orthogonal push on that scene expert is zero (Eq. 8), meaning the scene expert can drift toward the new environment's data distribution, which may degrade performance when that scene is retested under its original environment.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **§2 problem formulation OOD mismatch**: The reviewer noted a tension between in-distribution continual learning and out-of-distribution generalization. However, the paper explicitly includes both regimes (Table 1 = in-dist, Table 5 = OOD generalization) and discusses both settings. This is presentation-level at most.
- **Generic "important problem" strength**: Removed per filtering rules — not a specific, evidence-backed strength.
- **Reproducibility concerns about hyperparameters**: Removed — hyperparameters are listed in §5.1 (*λ*₁=0.2, *λ*₂=0.2, *λ*₃=0.1, *ω*=0.95, etc.) and the appendix is referenced for full details.
- **"Representation quality argument is entirely indirect"**: Removed as speculative — the paper's empirical results are the standard evidence for downstream task adaptation methods in this community; linear probing of latent factors is not standard practice here.

## Novel Insights
The explicit factorization of multi-hierarchical navigation knowledge into decoupled scene and environment expert *vectors* within a Tucker-decomposed 4th-order tensor — combined with alignment to 2D LLM weight matrices via expert vector contraction (Eq. 3) — is a genuinely clean architectural solution to what the authors correctly identify as a dimensional alignment bottleneck in applying high-order tensors to LLM fine-tuning. Prior work either treated LLM matrices as 2nd-order tensors or spliced attention matrices into 3rd-order tensors, both failing to achieve true high-order representation learning. TuKA's reduction from 4th-order to 2D via row-slicing of expert factor matrices is an elegant engineering contribution.

## Suggestions
- Fill or explain all blank cells in Tables 1 and 2 before publication; incomplete comparison tables should not appear in a camera-ready submission.
- Correct the Figure 7 legend to match the actual baselines compared in the paper.
- Add a retrieval accuracy table (% correct scene and environment identification via CLIP vs. oracle) as a simple supplementary result.
- Clarify that task ordering uses the same fixed random seed across all compared methods, and consider reporting performance variance across 2–3 orderings.
- Clarify the Table 3 duplicate-row discrepancy (OSR=69 vs. 68 for the same configuration).

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `JIlIYIHMuv` | 2.50 | R1 | Continual learning for LVLMs, weak contribution → much weaker |
| `gc8QAQfXv6` | 3.00 | R1 | Catastrophic forgetting in LLMs, avg 9.0 human (likely bimodal) → not comparable |
| `gNoqEdT2wO` | 2.33 | R1 | Multimodal CIL benchmark, limited contribution → weaker |
| `9aZ2ixiYGd` | 5.00 | R1 | Prompt-based continual VLN learning, accepted → comparable scope but narrower |
| `eWFkMCBySw` | 5.00 | R1 | Zero-shot VLN-CE, rejected → different approach, no lifelong component |
| `rwmwFnmjAX` | 4.75 | R1 | Continual LLaVA with benchmark, rejected → similar structure but weaker method |
| `EKfcngSxwD` | 4.67 | R1 | Task Codebook for VLMs incremental learning, rejected → comparable but simpler |
| `sb7qHFYwBc` | 6.50 | R1 | C-CLIP multimodal continual learning, accepted → this paper has stronger technical contribution |
| `2oKkQTyfz7` | 6.40 | R1 | General Scene Adaptation for VLN, accepted → closest topical match, single-scene focus vs. lifelong multi-scene here |
| `TLADT8Wrhn` | 6.25 | R1 | TiC-CLIP continual training, accepted → large-scale benchmark emphasis |
| `k9NYnsC4Mq` | 5.67 | R1 | Learning without forgetting for VLMs, rejected → narrower contribution |
| `OALIb8oNfl` | 5.75 | R1 | High-dim parameter space PEFT → related tensor PEFT angle, smaller margin |
| `dh4t9qmcvK` | 6.00 | R1 | Transformer² self-adaptive LLMs → MoE expert routing analog |
| `cgCKm5DOnu` | 6.00 | R1 | ROSA orthogonal subspace adaptation → related PEFT contribution |

**Bracketing**: This paper sits between the 5.0-score papers (narrower problem scope, simpler methods) and 6.5 papers (accepted continual VLN/multimodal works). The Tucker decomposition idea and real-world validation are stronger than `9aZ2ixiYGd` (5.0), comparable to `2oKkQTyfz7` (6.4, General Scene Adaptation for VLN). The table completeness issues and Figure 7 error are real editorial problems that prevent a confident 6.5, but the technical contribution is solid enough to avoid a reject. **Final score: 6.0 (borderline accept)**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>