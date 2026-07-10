Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper proposes NuSA-CL, a memory-free continual learning method for vision-language models (CLIP) that constrains weight updates to the approximate null space of current parameters, identified via SVD. The method uses a novel persistent constraint mechanism (freezing the null-space bases during training) which differentiates it from prior work like MiLoRA that only uses the low-energy subspace for initialization. Experiments on MTIL (11-task) and CIFAR-100 benchmarks show NuSA-CL achieves state-of-the-art results among storage-free methods and approaches the performance of storage-based approaches with substantially lower resource requirements (1.5M parameters, zero additional storage, 1.21 GPU-hours).

## Strengths

- **Clean, well-motivated idea (Sections 3 and 6.2).** The core mechanism — identifying an approximate null space via SVD and persistently constraining low-rank weight updates to it — is conceptually simple and clearly differentiated from prior work. The key distinction from MiLoRA — that the constraint is enforced throughout training, not just at initialization — is well drawn and empirically validated by the ablation in Table 4a, where unfreezing the bases causes a significant performance drop.

- **Clear SOTA in the storage-free regime (Tables 1 and 2).** On the MTIL benchmark, NuSA-CL (68.6/75.1/82.8) decisively beats LoRA (63.9/70.1/79.9) and MiLoRA (62.8/68.7/77.4) across all three metrics. The 5-shot results (Table 2) are even more convincing, with Transfer of 68.1% vs. 60.4% (LoRA) and 59.4% (MiLoRA) — substantial margins that genuinely support the claim that the persistent null-space constraint is a more data-efficient strategy.

- **Genuinely memory- and parameter-efficient (Table 1).** 1.5M trainable parameters, zero additional storage, 6.6 GB peak GPU, 1.21 GPU-hours. The 40× parameter reduction vs. MoE-Adapters and 3× speedup are real operational advantages that stem from the method's design (merge-and-update cycle avoids parameter growth).

- **Well-designed ablations (Section 6, Figures 3 and Table 4).** The Tail vs. Top vs. Random ablation (Fig. 3a) cleanly isolates the subspace selection effect, the rank sweep (Fig. 3b) identifies r_max=128 as the stability-plasticity sweet spot, and the persistent constraint ablation (Table 4a) confirms the necessity of freezing the SVD bases during training. The spectral dynamics analysis (Fig. 2) provides direct evidence that the method accumulates knowledge in previously underutilized directions rather than overwriting principal components.

## Weaknesses

### Fatal
None.

### Major

- **Missing LoRA/MiLoRA baselines in the CIFAR-100 evaluation (Table 3).** Table 3 compares NuSA-CL against ZSCL, LwF, ICaRL, LwF-VR, and Continual-FT — but not against LoRA or MiLoRA, which are the paper's own storage-free baselines from Tables 1 and 2. Without these comparisons, it is impossible to determine whether NuSA-CL's strong CIFAR-100 performance (especially on the 50-task split, where the gap over ZSCL is ~4.4% on Last) is due to its null-space mechanism or simply because any PEFT method applied to CLIP would achieve similar results on this benchmark. The paper's claim that "the advantage of our method becomes increasingly pronounced as the task sequence lengthens" (line 196) would be much stronger if the comparative forgetting trajectory of LoRA and MiLoRA were shown under the same 50-step protocol.

### Minor

- **The theoretical analysis (Section 4) is ornamental rather than foundational.** Lemma 1 bounds |⟨W, ΔW⟩_F| ≤ σ_max^null · ‖M‖_F. This inequality is a direct algebraic consequence of the construction ΔW = U_n M V_n^T — orthogonality guarantees most terms vanish, leaving only Tr(Σ_n M), which is bounded by σ_max^null · ‖M‖_F. The bound restates what the method already enforces by design and does not connect to why constraining parameter-space inner products controls forgetting of task-relevant *functions*. The paper acknowledges this limitation (lines 122–123). The real evidence for why the null space works comes from the ablations (Section 6.2), not from Section 4. This does not weaken the empirical contribution but means the theory section should either be upgraded to a genuine function-space analysis or reduced to a brief note.

- **The comparison with storage-based methods is framed to imply near-parity that the numbers do not fully support.** Table 1 shows NuSA-CL's Last accuracy at 82.8% vs. MoE-Adapters at 85.0% and DIKI at 85.1% — a 2.2–2.3 percentage point gap. The paper's prose ("highly competitive," "rivals," "superior performance-to-cost tradeoff") understates this gap. Since Last accuracy measures retention after all tasks, a gap of 2.3% on an 11-task benchmark is meaningful and could widen on longer sequences where storage-based methods have explicit rehearsal mechanisms. The paper should state more plainly that NuSA-CL establishes SOTA among storage-free methods and reduces but does not close the gap with storage-based approaches on the Last metric.

- **The LoRA rank used for baseline methods (LoRA, MiLoRA) in Tables 1 and 2 is not specified.** The paper states only that methods were re-implemented "with a consistent rank." Since NuSA-CL uses r_max=128 and LoRA/MiLoRA have 15.7M parameters vs. NuSA-CL's 1.5M, it is unclear whether the same rank was used for all methods or what the rank value was. This implementation detail should be documented to allow readers to assess the fairness of the comparison.

- **No task-ordering analysis.** The paper acknowledges this as future work (line 292), but it is a known factor in continual learning evaluations. Since NuSA-CL's null space for task t depends on W_{t-1}, which depends on the entire history of prior tasks, different orderings could produce very different null spaces. For instance, if early tasks are visually similar and fill the null space in related directions, later tasks may have less usable null capacity. This weakens the scalability claims for uncontrolled lifelong deployment.

### Trivial

- **"Data-agnostic" (lines 28, 58, 284) is an overstatement when applied to the full three-stage cycle.** The SVD step is genuinely data-agnostic (it operates on weight matrices alone), but the constrained adaptation step requires task-specific data to train M. Describing the cycle as a "data-agnostic adaptation process" (line 58) is misleading — only the identification stage is data-agnostic. The method is memory-free (no replay), not data-agnostic.

- **GPU type is not specified.** The paper reports GPU-hours and peak GPU memory but does not state the GPU model (e.g., A100 vs. 3090), making these efficiency numbers difficult to calibrate against other work.

## Nice-to-Haves

- **Direct verification of the null-space claim.** The paper asserts that low-energy singular directions encode less important knowledge (line 66). This could be verified directly by measuring how perturbation of principal vs. null directions affects accuracy on seen tasks, connecting the spectral analysis to functional forgetting.

- **At least one task-order permutation experiment on MTIL** (e.g., reverse order and one random shuffle) would directly address the most obvious robustness concern for uncontrolled deployment.

## Removed Points

1. **Missing L2P, DualPrompt, CODA-Prompt baselines** — Removed as scope creep. The paper focuses on weight-space PEFT methods for CL continual learning, not prompt-based methods designed for different settings (class-incremental ViT learning). The MTIL benchmark is specific to multi-task incremental learning on diverse datasets.

2. **Statistical significance/variance estimates not reported** — Removed. Single-run evaluation on large-scale CL benchmarks is standard practice in this subfield. The margins over storage-free baselines on MTIL are substantial enough that variance estimates would not change the conclusions.

3. **Request for "why the theory section is justified"** — The reviewer's concern about the theory being ornamental is retained (as a Minor weakness). The request for the authors to add a more rigorous justification for the theory section is folded into the weakness text.

## Novel Insights

None beyond the paper's own contributions. The reviews validate the paper's strengths (clean method, convincing storage-free SOTA, thorough ablations) and identify several concrete gaps (missing CIFAR-100 baselines, unspecified LoRA rank, task-ordering sensitivity) that the authors should address. No reviewer identified a fundamentally new connection or framing that the paper itself does not provide.

## Suggestions

1. Add LoRA and MiLoRA baselines to the CIFAR-100 evaluation (Table 3). This is the single highest-impact addition.
2. Report the LoRA rank used for re-implemented baselines in Tables 1 and 2.
3. Add at least one task-order permutation experiment on MTIL.
4. Correct the over-broad use of "data-agnostic" to refer only to the SVD identification step.
5. Report the GPU model used for timing experiments.
6. Either upgrade the theory section to a function-space analysis (e.g., connecting weight orthogonality to output stability via Lipschitz constants) or reduce it to a short note, letting the ablations carry the main argument.
7. Add a direct verification experiment measuring how perturbation of principal vs. null directions affects accuracy on seen tasks.

---

## Calibration and Score

**Anchors considered (all rounds):**

1. **C-CLIP** (6.50, Accept) — round 2, itemized. Multimodal CL continual learning with LoRA+distillation. Similar scope; my paper has a more novel mechanism (persistent null-space constraint vs. distillation) but shares similar baseline-coverage gaps. C-CLIP's highest-favorability items (~13) are strong experimental results; my paper has similarly strong items (~13-14) for SOTA and ablations. C-CLIP's lowest favorability items (~0.65-2.24) are typos and missing details; my paper's lowest items (~0.68) is the missing CIFAR-100 baselines. The comparison places my paper at or slightly above C-CLIP.

2. **PROOF — Learning without Forgetting for VLMs** (5.67, Rejected) — round 2, itemized. Task-specific projections for CIL. Had severe core-novelty concerns (favorability -4.82 and -3.21) about lack of innovation. My paper has no such core-contribution doubts; the method is genuinely novel. This anchor establishes the lower bound.

3. **TiC-CLIP** (6.25, Accept) — round 2, not itemized. Benchmark-focused paper on continual CLIP training. Different contribution type; less directly comparable.

4. **Vision and Language Synergy for Rehearsal Free CL** (5.00, Accept) — round 1, not itemized. Mixed reviews (8,6,3,3). Had weak theory concerns (-0.87) similar to my theory section, but also had more severe fairness concerns (ChatGPT reliance, 0.27). Less comparable.

5. **Continual Learning in Open-vocabulary Classification** (6.00, Rejected) — round 2, not itemized. Had marginal improvement (-2.45) and similarity-to-existing-work (-3.25) concerns that my paper does not share.

**Round 1 bracket:** After initial sweep, the plausible range narrowed to ~5.0–7.0. The PROOF paper (5.67, rejected due to core novelty concerns) established that papers with fundamental innovation issues fall near the low end of this range. C-CLIP (6.50, accepted) established that papers with strong empirical work and clean methods but some baseline gaps can reach the upper-mid range.

**Round 2 narrowing:** Comparing itemized favorability ratings between my draft and C-CLIP's items: my paper shares C-CLIP's highly-rated experimental strengths (favorability 13-14 for SOTA and ablations) but lacks C-CLIP's most damaging low-favorability items (distillation "not new" at 1.59, missing-code concerns at 2.24). My paper's lowest-rated item (missing CIFAR-100 baselines at 0.68) is comparable to C-CLIP's missing-baselines criticism (2.35). Overall, my paper's favorability profile is slightly stronger than C-CLIP's.

**Final placement:** Score 6.5 — between "borderline accept" and "accept." The paper has a genuinely novel mechanism, strong storage-free SOTA on MTIL, and thorough ablations. The main weakness (missing CIFAR-100 baselines) is significant but fixable and does not undermine the core MTIL contribution. The minor weaknesses (theory section, framing, missing details) are typical for conference papers and addressable with standard revisions.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>