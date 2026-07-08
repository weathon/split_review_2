Now let me produce the final consolidated review.

---

## Summary

This paper proposes Critique-RL, a two-stage reinforcement learning approach for training language models to critique and provide feedback on model outputs, without requiring stronger supervisors or oracle verifiers at test time. The key insight is that training critics using only indirect reward signals from actor refinement (commonly done in prior work) collapses discriminability — critics become either conservatively inert or aggressively overcorrecting. Critique-RL addresses this by first optimizing discriminability via direct rule-based rewards (Stage I), then optimizing helpfulness while regularizing to preserve discriminability (Stage II). Experiments on mathematical reasoning tasks (MATH, GSM8K, AQuA, SVAMP, TheoremQA) with Qwen2.5-3B/7B show consistent improvements over SFT, STaR, Retroformer, and CTRL baselines.

## Strengths

1. **Well-motivated problem decomposition (Section 4.1, Figure 3).** The paper convincingly demonstrates that training critics with only indirect reward signals (from actor refinement correctness) leads to collapsed discriminability — critics become either conservatively inert or aggressively overcorrecting. The training dynamics in Figure 3 provide concrete evidence of this failure mode. The decomposition into discriminability and helpfulness as separable but interacting objectives is clean and empirically compelling. [weight=11.87]

2. **Two-stage design that follows logically from the diagnosis (Section 4.2).** Stage I (optimizing discriminability with direct rule-based reward) and Stage II (optimizing helpfulness with regularization to preserve discriminability) are a natural response to the identified failure modes. The KL regularization back to the Stage I model (Eq. 9) is a sensible mechanism for maintaining discriminability during helpfulness optimization. [weight=8.73]

3. **Consistent and substantial improvements across settings (Tables 1, 4).** The method outperforms all baselines (SFT, STaR, Retroformer, CTRL) across 3 in-domain tasks and 2 OOD tasks, for both 3B and 7B model sizes. The gains are practically meaningful: e.g., on MATH with 7B, Critique-RL achieves 58.40% vs. CTRL's 53.86% (+4.54 pts); on GSM8K with 7B, 87.72% vs. CTRL's 81.35% (+6.37 pts). The OOD results on SVAMP and TheoremQA show generalization beyond the training distribution. [weight=10.08]

4. **Informative ablations (Table 3).** The ablation isolating Stage I (w/o Stage II: 45.9→48.6 drop) and Stage II (w/o Stage I: 47.6→48.6 drop) confirms both stages contribute. The 'Stage II w/o discrimination' condition shows that removing both r_dis and the KL term causes a sharp drop in Acc@Dis (82.8→77.7 on MATH, 69.9→61.6 on AQuA) and Acc@Refine, validating the central claim that maintaining discriminability during helpfulness optimization is necessary. [weight=10.01]

5. **Iterative training improvement (Table 2).** Showing that a second iteration of the two-stage procedure further improves performance (Acc: 48.6→51.0, Acc@Dis: 82.8→86.5) demonstrates the method can compound its gains beyond a single pass. [weight=9.23]

## Weaknesses

### Fatal
None.

### Major

1. **Unexplained numerical discrepancy between Figure 1 and Table 1.** Figure 1 (left panel) reports for Qwen2.5-7B on MATH: SFT Acc=48.5, Discrimination=55.3; SFT+RL Acc=51.0, Discrimination=57.0; Critique-RL Acc=54.5, Discrimination=60.5. However, Table 1 for the same model and task reports: SFT Acc=51.84, Acc@Dis=67.59; Critique-RL Acc=58.40, Acc@Dis=85.20. The Accuracy values differ by 3-4 points and the "Discrimination" metric (Figure 1) differs from Acc@Dis (Table 1) by ~25 points. The paper does not define what "Discrimination" in Figure 1 measures versus Acc@Dis, nor does it explain why the values differ. Additionally, "SFT+RL" appears in Figure 1 but is not a method described in the paper's experimental setup. This inconsistency undermines trust in the reported results and must be resolved. [weight=1.06]

2. **No statistical significance or variance reporting.** The paper reports only single point estimates ("best results" across training steps, §5.1) for all experiments in Tables 1-4. RL training on LLMs is notoriously sensitive to random seeds, sampling noise, and hyperparameters. Several claimed improvements are small enough that variance could matter (e.g., on TheoremQA with 7B: Critique-RL 21.4 vs. CTRL 21.1 — a 0.3 point gap; on AQuA with 7B: 65.75 vs. 64.96 — a 0.79 point gap). Without standard deviations, multi-seed runs, or confidence intervals, the reader cannot assess whether these differences are meaningful or within the noise of the experimental setup. [weight=0.66]

3. **Confound between reward design and RL algorithm across baselines.** Retroformer uses PPO, CTRL uses GRPO, and Critique-RL uses RLOO (as stated in §5.1). These are meaningfully different RL algorithms with different variance properties, KL penalty mechanisms, and optimization dynamics. The observed advantage of Critique-RL could partially stem from the choice of RLOO over PPO/GRPO rather than from the two-stage reward design itself. The paper should either use the same RL algorithm across all methods or demonstrate that the two-stage advantage holds within each algorithm separately. [weight=1.61]

### Minor

4. **The binary r_dis reward (Eq. 7) provides a coarse learning signal** (1 for correct judgment, 0 otherwise). For a critic already reasonably accurate after SFT, most training examples yield reward 1, providing limited gradient signal. The paper does not discuss this potential sparsity issue or whether it causes optimization difficulties, especially in Stage I. [weight=4.77]

5. **Training cost comparison not reported.** The paper states 500 training steps per stage for Critique-RL but does not specify the number of steps/epochs used for baselines (Retroformer, CTRL). The reader cannot assess whether the two-stage approach requires proportionally more compute, which is relevant for practical adoption. [weight=5.25]

### Trivial
None.

## Nice-to-Haves
- The abstract could more precisely distinguish between "stronger labeling" (human annotation) and the use of ground-truth answer labels (oracle reward) during training, which the method still requires. The paper acknowledges this later but the abstract could be sharper.
- The transition from §4.1 to §4.2 could explicitly state which indirect reward ($r_{\text{refine}}$, $r_\Delta$, or $r_{\text{correction}}$) Stage II's helpfulness optimization most closely corresponds to, and why $r_{\text{refine}}$ is the default choice.

## Removed Points
These points were extracted from the input review and removed with justification:

- **Duplicated label in Figure 1 right panel ("w/o Critique-RL (3B)" appears twice):** REMOVED — This is a parser/image-extraction artifact from the PDF, not an author error. The paper contains an actual image; text extraction from images is unreliable.
- **Related work discussion is too thin / missing references:** REMOVED — Per review guidelines, critiques about missing related works should not be included.
- **Abstract overstates "without stronger labeling":** REMOVED — The distinction between "stronger human labeling" and "ground-truth answer labels" is nuanced and the paper acknowledges the oracle reward usage during training. This is not a genuine flaw.
- **"SFT+RL" is not defined in Figure 1:** MERGED into Major weakness #1 (Figure 1 vs Table 1 discrepancy), as it is part of the same inconsistency issue.
- **The critic's note about "please check code release" / reproducibility concerns about missing artifacts:** REMOVED — Per hard rules about reproducibility nitpicks.
- **Generic concerns about whether the metric measures the right thing / whether confounders are controlled:** REMOVED — These are area-of-concern speculations, not specific identified problems in the paper.

## Novel Insights
The most interesting observation from the review process is how the harsh critic's "Figure 1 discrepancy" concern interacts with the paper's overall strength. The inconsistency is real and damaging to trust, but it is a presentation issue — the main tables (1-4) are internally consistent and the ablations (Table 3) cleanly validate the central claim. This is a case where a genuine presentation flaw coexists with a solid methodological contribution, and the severity of the weakness depends on whether the authors can cleanly explain the discrepancy (e.g., different evaluation setup for Figure 1). None of the weaknesses are fatal or methodological.

## Suggestions

1. **Resolve the Figure 1 vs. Table 1 inconsistency.** Clarify what "Discrimination" in Figure 1 measures (e.g., is it a per-step judgment accuracy rather than the per-response Acc@Dis?) and what "SFT+RL" represents. If the figure uses a different evaluation protocol or temperature, state this explicitly.

2. **Add variance estimates for the main results.** Run each method with 3–5 random seeds and report means and standard deviations (or at minimum the range). This is especially important for the smallest gaps (AQuA 7B, TheoremQA).

3. **Control the RL algorithm across baselines.** Either re-implement all baselines using RLOO (the algorithm used by Critique-RL) or add an ablation showing that Critique-RL's advantage holds when Retroformer and CTRL are re-run with RLOO. This would eliminate the algorithm confound.

4. **Report the training steps/epochs for each baseline** to allow compute cost comparison.

5. **Discuss the potential sparsity of the binary r_dis reward signal**, especially in Stage I when the model is already reasonably discriminative after SFT.

## Score and Decision

### Calibration Anchors

| Anchor Path | Avg Score | Round | Itemized | Comparison to this paper |
|-------------|-----------|-------|----------|--------------------------|
| **F0GNv13ojF** (On Designing Effective RL Reward at Training Time for LLM Reasoning) | 5.17 | 1 | Yes | Similar topic (RL reward design for LLM reasoning). Has stronger baseline concerns (reward clipping known from RL). Weaker contribution but cleaner presentation. |
| **JEehcb48Vp** (Critic-CoT) | 5.75 | 1 | Yes | Similar topic (training critics for reasoning). Relies on GPT-4 annotations for data; improvements are marginal. Critique-RL has stronger, more consistent empirical evidence and doesn't rely on stronger models. |
| **50P9TDPEsh** (Critique Ability of LLMs) | 4.67 | 1 | Yes | Evaluates critique ability rather than training it. Lower relevance. |
| **38E4yUbrgr** (Language Model Self-improvement by RL Contemplation) | 6.00 | 2 | Yes | Self-improvement via RL. Accepted. Novelty concerns (similar to RLAIF). Critique-RL has a more novel problem diagnosis and cleaner validation. |
| **vf8iou7FNF** (RLSF: RL via Symbolic Feedback) | 5.75 | 2 | Yes | RL with symbolic feedback. Novelty concerns (straightforward combination of existing techniques). |
| **Sx038qxjek** (CRITIC: Self-Correct with Tool-Interactive Critiquing) | 6.50 | 2 | No | Tool-based critiquing. Different approach (uses external tools rather than training). |
| **mMPMHWOdOy** (WizardMath) | 8.00 | Narrowing | No | Much stronger paper with results surpassing proprietary models. Critique-RL is substantially weaker on result strength. |

### Weighted-Item Comparison

The model-assigned weights for Critique-RL's strengths (8.73–11.87) are comparable to or higher than the anchors' top strengths. The weaknesses have relatively low weights (0.66–1.61 for major issues, 4.77–5.25 for minor), indicating the model considers them manageable. By contrast, the ~5-range anchors had weaknesses with negative weights (novelty concerns at -3 to -5), reflecting more fundamental problems. This suggests Critique-RL is stronger than the 5.17–5.75 anchors despite its presentation issues. However, it is clearly weaker than WizardMath (8.0), which had substantially stronger results and no comparable Figure-level inconsistencies.

**Round-1 bracket:** 5.5 – 7.0  
**Narrowing rationale:** The paper is stronger than the 5.17–5.75 anchors (which had fundamental novelty/evidence concerns) primarily because its core problem diagnosis is genuinely novel and well-supported. However, it is held back by the Figure 1 vs Table 1 inconsistency (a presentation issue that damages credibility) and the missing variance estimates, which are more damaging than the anchors' novelty concerns because they affect trust in the reported numbers. Placing it at 6.0 reflects a borderline-accept paper with a sound core contribution that needs revision to address these presentation and rigor issues.

**Final score: 6.0** — The paper makes a genuine, well-motivated contribution with coherent methodology and consistent experimental support. The weaknesses are significant but addressable. The main issues are: (1) the Figure 1 vs Table 1 numerical discrepancy that must be resolved, (2) the absence of variance estimates or multi-seed runs, and (3) the confound between reward design and RL algorithm choice across baselines. None of these rise to the level of fatal flaws — the main empirical claims are well-supported by Tables 1–4 — but they must be addressed before the paper can be considered fully reliable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>