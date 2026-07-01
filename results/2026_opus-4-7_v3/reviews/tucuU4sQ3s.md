Now let me read the remaining sections to check training details and any additional claims:Now I have a thorough understanding of the paper. Let me submit my draft review and then proceed with calibration.Now let me run the calibration Round 1 — bracketing across score bands:Let me read the most relevant anchor papers to calibrate my score:Now I have enough calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket Analysis:**
- Score 1-2 papers: Fundamentally flawed or poorly written papers. NuSA-CL is clearly above.
- Score 3.8 (G9Ea7mlqGO, "CLIP as Online CL"): Interesting idea but lacks insights, inconsistent. NuSA-CL is significantly stronger.
- Score 5.0-5.67 (PROOF, VLM CL papers): Reasonable contributions with notable weaknesses. NuSA-CL has more novel mechanism, better ablations, efficiency analysis.
- Score 6.25-6.5 (C-CLIP, TiC-CLIP): Accepted papers with clear contributions, some shared weaknesses (single backbone, no variance). NuSA-CL is comparable.
- Score 8.0: Strong papers with comprehensive novelty. NuSA-CL doesn't reach this level.

**Initial bracket: 5.5 to 7.0**

Now let me write the final consolidated review:

---

## Summary
NuSA-CL proposes a memory-free continual learning framework for vision-language models (specifically CLIP) that constrains task-specific weight updates to lie within an approximate null space of the model's current parameters. The method performs SVD on weight matrices to identify low-energy subspaces, trains only a small intermediate matrix M within frozen null-space bases (U_n, V_n), then merges updates into the backbone before repeating the cycle for the next task. The paper demonstrates strong efficiency-performance tradeoffs on the MTIL benchmark and long-sequence scalability on CIFAR-100 (up to 50 steps).

## Strengths

- **Persistent null-space constraint is validated with a well-designed ablation (Table 4a).** Unfreezing the null space bases causes substantial degradation (Transfer drops from 68.58 to 62.60 when both U_n and V_n are made trainable). This is the paper's sharpest differentiator from prior SVD-guided work like MiLoRA, and it is backed by controlled evidence showing that persistent confinement—not mere initialization—is the operative mechanism.

- **Subspace selection ablation (Figure 3a) isolates the mechanism convincingly.** By comparing Tail, Top, and Random subspace strategies across five rank values, the paper provides direct evidence that the low-energy spectral region is genuinely less disruptive. The gap is consistent (e.g., at r=128: 2.57% forgetting for Tail vs. 4.44% for Top and 4.57% for Random). This goes beyond showing the full method works—it isolates why.

- **Efficiency gains are substantial and unusually well-documented (Table 1).** NuSA-CL achieves 1.5M trainable parameters, 6.6 GB peak GPU memory, and 1.21 GPU-hours—while approaching the accuracy of storage-based methods requiring 40x more parameters (MoE-Adapters) or 39x more compute (ZSCL). This represents a qualitatively different operating point on the efficiency-performance frontier.

- **Strong long-sequence scalability on CIFAR-100 50-step (Table 3).** NuSA-CL achieves 71.85% Last accuracy, outperforming ZSCL by 4.49 points. This is the most challenging evaluation setting and provides the strongest evidence for the method's practical value, since 50-step sequences are where cumulative forgetting most severely penalizes methods without principled interference mitigation.

## Weaknesses

### Fatal
None

### Major
- **Merge-cycle protection mechanism is unanalyzed despite being central to the method's viability.** After merging ΔW_t into W_t, the SVD is recomputed to define the null space for task t+1. The paper never analyzes whether task t's knowledge migrates into the principal subspace of W_t (where it would be protected) or remains in the low-energy tail (where it could be overwritten). Figure 2 shows the effective rank increases only marginally (e.g., 51.8% to 52.4% for the vision encoder over 10 tasks), suggesting merged updates contribute very little energy to the principal subspace. This raises the question of whether the null space for task t+1 substantially overlaps with the subspace encoding task t's knowledge. The strong empirical results (especially Table 3) suggest this doesn't cause catastrophic failure in practice, but the paper's narrative presents a principled protection mechanism whose key link—how recently learned knowledge survives subsequent null-space recomputation—is left entirely to empirical observation. A spectral overlap analysis (achievable with data already computed at each step) would directly close this gap.

### Minor
- **No variance or statistical significance reported.** All results appear to be single-run numbers. Continual learning results are sensitive to random initialization and task ordering. Some margins are narrow enough that significance is uncertain—e.g., NuSA-CL vs. InflORA on Last accuracy in Table 2 (75.4 vs. 74.8, a 0.6-point difference). The paper acknowledges in limitations that task-order sensitivity is unstudied.

- **Theoretical section (Section 4) overstates its contribution through its formalism.** Lemma 1 bounds ⟨W, ΔW⟩_F by σ_max^null · ‖M‖_F—a direct algebraic consequence of null-space projection that restates the construction's definition. Theorem 2 simply sums this across tasks without analyzing interaction effects between successive updates. The paper commendably acknowledges this is "a local stability condition rather than a full function-level guarantee" (line 122), but the theorem-proof presentation suggests more than it delivers. Additionally, ‖M‖_F is unconstrained during training, making the bound potentially vacuous. This is a presentation issue, not a methodological flaw—the empirical results stand independently.

- **Some overclaiming in framing.** The introduction mentions "true lifelong learning" and applicability to "autonomous agents or on-device AI" (line 28), but the longest evaluation is 50 two-class splits of CIFAR-100. The limitations section (line 292) appropriately qualifies the scope, but the introductory language is stronger than the evidence supports.

### Trivial
None

## Nice-to-Haves
- Task-order sensitivity analysis (even 2-3 permutations of the MTIL sequence), which the authors themselves identify as an important future direction in their limitations section.
- Comparison with O-LoRA or other orthogonal-subspace continual learning methods would round out the baseline set, since the related work positions NuSA-CL against these approaches.
- Replacing or supplementing the theoretical section with empirical function-level interference measurements (e.g., how do predictions on task t's validation set change after training on tasks t+1 through T).
- The interaction between the energy cutoff ρ and r_max—specifically, how often the available null-space dimensions (d − k) bind below r_max, and in which layers.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Eq. 3 orthogonality language allegedly blurred:** The reviewer argued the paper blurs the distinction between orthogonality to the principal subspace vs. full W. However, the paper's actual claim (line 84) is "mathematically guaranteed to be orthogonal to the principal subspace of W," which is technically correct as stated.
- **Training details missing from main text:** Learning rate, optimizer, epochs not fully specified in the main body. These are likely in the appendix (stripped by parser) and this is a common practice for page-limited submissions.
- **CIFAR-100 baselines "from a different era":** The paper includes ZSCL (2023) as the strongest and most recent baseline. LwF, ICaRL, and LwF-VR are standard baselines for this benchmark configuration.
- **Storage-free baselines not CL-specific:** The reviewer noted LoRA and MiLoRA aren't designed for continual learning. This is true but the paper explicitly frames them as sequential-PEFT baselines in a unified comparison framework (line 169), and the comparison favors the baselines (they aren't burdened with CL constraints), making the asymmetry favorable to the paper's argument rather than inflating its results.
- **ρ and r_max interaction:** Minor under-specification unlikely to affect core claims; moved to nice-to-have.

## Novel Insights
The paper's central empirical insight—that *persistent* confinement to the null space, not just null-space initialization, is the critical factor for forgetting prevention—is a meaningful and well-supported contribution. The ablation in Table 4a directly demonstrates this, showing a 6-point Transfer gap between persistent and unconstrained null-space adaptation. Combined with the subspace selection ablation (Figure 3a), this provides a mechanistic understanding of why the approach works that goes beyond most continual learning method papers. The observation that effective rank increases progressively under NuSA-CL but remains static under LoRA and Full-FT (Figure 2) offers an interesting spectral lens on how different adaptation strategies use model capacity.

## Suggestions
- Conduct spectral overlap analysis between the null space identified for task t+1 and the subspace used by task t's update—this is achievable with data already computed and would directly address the main weakness.
- Report variance across 2-3 random seeds and/or task orderings, particularly for the MTIL and few-shot results where margins are narrow.
- Consider reframing Section 4 as an "intuition" or "motivation" section rather than using theorem-proof formalism, or supplement with empirical function-level interference measurements.
- Tone down "true lifelong learning" and "autonomous agents" language to match the scope of the empirical evaluation.

## Score and Decision

### Anchor Comparison

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Clothing-Irrelevant Lifelong ReID | 5lUdTogEL3 | 1.0 | R1 | Fundamentally flawed; NuSA-CL far above |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.0 | R1 | Not a real research contribution; NuSA-CL far above |
| IC-Light | u1cQYxRI1H | 0.5* | R1 | Misranked anchor (actual 10.0); irrelevant topic |
| Time-dependent Scientific Discourse | P49gSPmrvN | 1.0 | R1 | Trivial contribution; NuSA-CL far above |
| Projected Subnetworks Scale Adaptation | WM5G2NWSYC | 2.0 | R1 | Similar topic but severely under-developed, poor writing; NuSA-CL clearly superior |
| LVLM-CL | JIlIYIHMuv | 2.5 | R1 | Weak benchmarks, limited novelty; NuSA-CL more rigorous |
| Multimodal Class-Incremental Benchmark | gNoqEdT2wO | 2.33 | R1 | Benchmark paper lacking depth; NuSA-CL has stronger method contribution |
| Prototypical evolution VLM | ZaudLwn0Hm | 2.5 | R1 | Overfitting concerns, limited analysis; NuSA-CL more thorough |
| CLIP Online CL | G9Ea7mlqGO | 3.8 | R1 | Interesting idea but lacks insight, inconsistent presentation; NuSA-CL has better ablations and mechanism isolation |
| VL Synergy Rehearsal Free CL | 9aZ2ixiYGd | 5.0 | R1 | Accepted despite mixed reviews; NuSA-CL has clearer mechanism and better efficiency narrative |
| Simple Efficiency IL Framework | rkAqvDnnmO | 5.25 | R1 | Reasonable but limited novelty; NuSA-CL has stronger ablations and efficiency gains |
| Continual LLaVA | rwmwFnmjAX | 4.75 | R1 | Different scope (LVLMs); comparable rigor but NuSA-CL has more focused contribution |
| C-CLIP | sb7qHFYwBc | 6.5 | R1 | Accepted; comparable contribution level, both adapt CLIP for CL. NuSA-CL has better efficiency analysis and mechanism ablations; C-CLIP has broader evaluation |
| TiC-CLIP | TLADT8Wrhn | 6.25 | R1 | Accepted; different angle (temporal CL), larger scale. NuSA-CL has more focused technical contribution |
| PROOF (VLM CIL) | k9NYnsC4Mq | 5.67 | R1 | Rejected; task-specific projections, similar weaknesses (no variance). NuSA-CL has more novel mechanism and better ablations |
| Continual Learning in Open-vocab | wE1I9IGqeH | 6.0 | R1 | Rejected despite 6.0 avg; complementary memory systems. NuSA-CL has comparable rigor |
| Compositional Entailment VLM | 3i13Gev2hV | 8.0 | R1 | Strong paper with comprehensive novelty; NuSA-CL doesn't reach this level |
| Two Effects One Trigger CLIP | uAFHCZRmXk | 8.0 | R1 | Analysis paper with deep insights; different class |
| Interpreting CLIP | 5Ca9sSzuDp | 8.0 | R1 | Strong interpretability contribution; NuSA-CL doesn't match depth |
| Multi-granularity Correspondence | 9Cu8MRmhq2 | 8.0 | R1 | Strong comprehensive contribution; NuSA-CL not at this level |

**Round 1 bracket: 5.5–7.0**

**Narrowing rationale:** NuSA-CL is clearly stronger than the 5.0-5.67 rejected papers (PROOF, VL Synergy) thanks to its novel persistent null-space mechanism backed by thorough ablations and strong efficiency gains. It is comparable to C-CLIP (6.5, accepted) and TiC-CLIP (6.25, accepted)—both of which share similar weaknesses (single backbone, no variance) but were accepted. NuSA-CL's main weakness (unanalyzed merge-cycle protection) is a gap in the narrative rather than evidence that the method fails. The efficiency contribution is genuinely distinct and well-documented. However, the missing variance, the tautological theory, and the overclaiming prevent it from reaching the upper end of the range. 

**Final score: 6.0**

The paper presents a clean, practical method with a well-validated core mechanism and substantial efficiency gains. The persistent null-space constraint is genuinely novel relative to prior SVD-guided work, and the ablations convincingly support it. The major weakness—unanalyzed merge-cycle protection—is a real gap in the mechanistic narrative but is partially mitigated by strong empirical results (especially the 50-step CIFAR-100 scalability). The missing variance reporting and oversold theory are notable but addressable concerns. Overall, this is a solid borderline-accept paper: the contribution is genuine and the experiments are competitive, but the paper doesn't fully close the case it sets out to make.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>