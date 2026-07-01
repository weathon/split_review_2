## Summary

This paper proposes Critique-RL, a two-stage reinforcement learning approach for training language models to critique model outputs without relying on stronger supervisors. The key insight is that discriminability (judging whether a response is correct) and helpfulness (providing constructive feedback) should be optimized separately. Stage I uses direct rule-based reward signals to train the critic's discrimination ability, while Stage II optimizes helpfulness using indirect rewards from actor refinement while regularizing to preserve discriminability. Experiments on math reasoning tasks across multiple model sizes show consistent improvements over baselines.

## Strengths

1. **Clear empirical diagnosis of a real optimization problem (Section 4.1, Figure 3).** The paper concretely demonstrates that RL training with indirect reward signals (from actor output correctness) produces critics that are either overly conservative or overly aggressive, because discriminability degrades for one class of inputs while improving for the other. This diagnostic analysis is the paper's strongest intellectual contribution and clearly motivates the proposed method.

2. **Principled two-stage decomposition with well-justified design.** The insight that discriminability and helpfulness should be optimized separately—with discriminability established first and helpfulness built on top with KL regularization to prevent erosion—is clean and methodologically sound. The reward design ($r_{\text{dis}}$ in Stage I, $r_{\text{refine}} + \beta_1 r_{\text{dis}} - \beta_2 \text{KL}$ in Stage II) directly targets the diagnosed failure modes.

3. **Consistent and often large improvements across models, tasks, and settings.** Critique-RL outperforms all baselines on nearly every metric for both 3B and 7B models (Table 1). Gains are substantial (e.g., GSM8K 7B: 87.72% vs. CTRL's 81.35%). OOD results (Table 4) and iterative training results (Table 2) further support that improvements are not dataset-specific memorization. Experiments across different architectures (Llama3.2, DeepSeek-R1 variants in Appendix) strengthen the generality.

## Weaknesses

### Fatal
None.

### Major

**1. No variance estimates or statistical significance for any result.** All results in Tables 1–4 are reported as point estimates with no confidence intervals, standard deviations, or multiple training seeds. Several comparisons are tight (e.g., TheoremQA 7B: 21.4% vs. CTRL's 21.1% — a ~1.4% relative improvement), and without variance estimates it is impossible to assess whether these gaps are meaningful or within noise. Additionally, the paper states it "report[s] best results" (line 274) without clarifying whether this means the best checkpoint on a held-out validation set or the best across multiple runs/random seeds—a choice that can systematically inflate reported performance. RL training of LLMs is notoriously seed-sensitive, making this gap particularly consequential for the smaller-margin results.

**2. The RL algorithm is not controlled between methods, partially confounding the comparison.** Critique-RL uses RLOO as its base RL algorithm, while Retroformer uses PPO and CTRL uses GRPO. Without an ablation that applies the same RL algorithm to the baseline reward designs, some fraction of the observed gains could be algorithm-driven rather than reward-design-driven. The paper's ablations (Table 3) partially address this by comparing different reward designs within RLOO, showing that the two-stage reward design matters even holding the algorithm fixed. However, the main comparisons against Retroformer and CTRL remain confounded by the algorithm choice.

### Minor

**3. Headline results (Acc@Refine) are an end-to-end metric that conflates critique quality with actor capability.** The 9.02% and 5.70% gains reported in the abstract are Acc@Refine improvements—the accuracy of the actor's refinement after receiving a critique. This is a joint function of critic discriminability, critic helpfulness, and the actor's ability to follow critiques. The paper *does* report decomposition metrics (Acc@Dis, Δ, Δ^{c→i}, Δ^{i→c}) and includes an oracle-verifier analysis (Figure 5) to isolate helpfulness, so no information is hidden. Nevertheless, the primary framing (abstract, introduction) would benefit from explicitly noting that Acc@Refine is an end-to-end measure and anchoring the headline claims more directly on critique model properties.

**4. Evaluation is confined almost entirely to math reasoning, limiting the connection to the broader motivation.** All three in-domain datasets (MATH, GSM8K, AQuA) and two OOD datasets (SVAMP, TheoremQA) are math problems with deterministic answer matching. The method requires a rule-based oracle reward function for training, which is trivially available for math but not for the tasks the introduction frames as motivating the work ("complex reasoning, sequential decision-making, and coding"). Summarization experiments (CNN/DailyMail, Appendix G) are mentioned but relegated to the appendix. The paper would better serve its stated framing by including results in at least one non-math domain (e.g., coding with unit tests) in the main paper.

### Trivial

**5. The function $f$ that extracts the critique's correctness judgment is not described.** In Algorithm 1, $f(x, y, c)$ is used to compute the discrimination reward but its implementation is never specified (e.g., keyword matching, structured output parsing). This is a small reproducibility detail.

**6. The "No Critic" baseline does not include self-refinement.** The "No Critic" baseline is the actor without any refinement step. A self-refinement baseline (the actor critiquing and refining its own output) would be a more natural comparison for assessing the marginal value of a separate critic.

## Nice-to-Haves
- Computational cost comparison (training steps, inference cost) between Critique-RL and baselines would help readers assess the cost-benefit trade-off of the two-stage approach.
- Running the trained critic with a different actor model to test whether helpfulness generalizes beyond the specific actor used during training.
- Clarification of "report best results" (line 274): best checkpoint on a held-out validation set? Best across multiple random seeds? This affects how interpretable the reported numbers are.
- A self-refinement baseline for the two-player comparison.

## Removed Points

The following points from the input review were removed or demoted after verification against the paper:

- **"The primary evaluation metric (Acc@Refine) conflates critique quality with actor capability"** → Demoted to Minor (listed above as Weakness #3). The paper clearly defines all metrics in Section 3.3, reports Acc@Dis and Δ alongside Acc@Refine, and includes an oracle-verifier analysis (Figure 5) that isolates helpfulness. The end-to-end metric is standard for this setup, and the decomposition metrics are all present. The concern is about framing clarity, not a technical flaw.

- **"The method is evaluated almost exclusively on math reasoning"** → Demoted to Minor (listed above as Weakness #4). The paper explicitly states "Focusing on mathematical reasoning tasks" (Section 5.1). The requirement for a rule-based oracle is inherent to the method. This is a scope limitation, not a flaw in what the paper does. Summarization experiments exist in the appendix.

- **"Preliminary experiments conducted only on GSM8K with Qwen2.5-3B"** → Removed. The paper describes these as preliminary experiments to diagnose an optimization phenomenon (Section 4.1). The level of generality claimed is appropriate for a diagnostic finding.

- **"The SFT critique data filtering threshold and resulting data quality not discussed"** → Removed. The paper states "filter the critique data based on the correctness of refinement to ensure the quality" (line 148), which is a reasonable level of detail for a non-central implementation choice.

- **"The RL dataset D_RL is mentioned but not clearly defined"** → Removed. The RL dataset is constructed from the training splits of MATH, GSM8K, and AQuA as described in Section 5.1. The construction is adequately described.

- **Weaknesses about missing appendix sections, formatting, references, or reproducibility artifacts** → Removed per policy (parser strips these or they reflect reviewer knowledge gaps).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation that the ablation experiments (Table 3, using RLOO with different reward designs) partially address the RL algorithm confound is worth noting for the authors' rebuttal planning, but does not constitute a novel analytical insight.

## Suggestions

1. **Report results with multiple random seeds** (at least 3) and provide variance estimates or confidence intervals for the main comparisons, especially tight ones (TheoremQA, AQuA). This is the most impactful improvement the authors could make.

2. **Add an ablation** that applies the Critique-RL two-stage reward design using PPO or GRPO (the same algorithm as the baselines) to isolate the contribution of the reward design from the algorithm choice.

3. **Clarify "report best results"** (line 274): specify whether performance was selected by a held-out validation set or as the best across multiple runs, and report the selection procedure.

4. **Include results for at least one non-math domain** (e.g., coding tasks with unit test verification) in the main paper, not just the appendix, to strengthen the connection to the broader scalable oversight motivation.

5. **Describe the implementation of function $f$** in Algorithm 1 for reproducibility—even a brief note about how the critique's final judgment is extracted (keyword matching, structured format parsing, etc.) would suffice.

## Score and Decision

**Calibration details.** All anchor papers retrieved across rounds (listed with avg human score, round, and comparison):

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| Critic-CoT (JEehcb48Vp) | 5.75 | R1 (5.5–7.5) | Similar topic, weaker method (SFT from stronger model vs. RL). Critique-RL > Critic-CoT. |
| Critique-out-Loud (e3odKmatZr) | 5.25 | R1 (3.5–5.5) | Related but different focus (reward models). Critique-RL > CLoud. |
| RL Contemplation (38E4yUbrgr) | 6.00 | R1 (5.5–7.5) | Similar scope (RL for self-improvement). Critique-RL ≈ RLC. |
| Multiagent Finetuning (JtGPIZpOrz) | 6.67 | R1 (5.5–7.5) | Similar multi-agent paradigm. Broader experiments. Critique-RL slightly ≤ Multiagent FT. |
| CRITIC (Sx038qxjek) | 6.50 | R1 (5.5–7.5) | Similar critique/refinement, prompting-based. Critique-RL has more methodological depth. Critique-RL ≈ CRITIC. |
| Critique Ability (50P9TDPEsh) | 4.67 | R1 (3.5–5.5) | Benchmark/evaluation paper. Critique-RL > this. |

Round-1 bracket: 5.5–7.5. The paper sits comfortably above the 5.0–5.75 band (weaker papers with SFT-based methods or limited evaluation) and below the 8.0+ band (papers with theoretical contributions or exceptionally broad validation). Within the 5.5–7.5 bracket, Critique-RL's clean diagnosis, principled two-stage method, and consistent strong results place it in the upper portion, comparable to CRITIC (6.50) and Multiagent Finetuning (6.67). The main weaknesses (no variance estimates, RL algorithm confound) prevent a higher score but do not undermine the core contribution.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>