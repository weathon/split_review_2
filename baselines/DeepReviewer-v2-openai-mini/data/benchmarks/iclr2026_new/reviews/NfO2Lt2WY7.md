## Summary
This paper investigates whether the full GRPO loss function—combining group-relative advantage estimation, PPO-style clipping, and KL regularization—is necessary for improving mathematical reasoning in LLMs. Through controlled ablations on small models (Qwen2.5 0.5B/1.5B, Llama3.2 1B), the authors identify two main findings: (1) negative feedback from below-baseline completions is essential for stable training and preventing reward hacking; (2) PPO-style clipping and policy ratio terms can be removed without harming performance. Based on these insights, they propose RGR (REINFORCE with Group Relative Advantage), which drops clipping while retaining group-relative advantage and KL regularization. Experiments across 9 math and STEM benchmarks show that RGR achieves competitive or better accuracy than GRPO on most comparisons (17/27 individual model-benchmark pairs), while simplifying the training objective.

**Strengths**: The research question is timely and well-motivated—understanding which components of GRPO are truly needed has direct implications for LLM post-training efficiency. The systematic ablation methodology is sound, testing three distinct simplifications (positive-only advantages, removing PPO constraints, removing advantage estimation) to isolate essential components. The paper also compares against RAFT and plain REINFORCE baselines, providing a broad empirical landscape.

**Key weaknesses**: (1) No statistical significance or variance reporting—all benchmark results are single-run point estimates, making it impossible to assess whether reported differences are meaningful. (2) Experiments are limited to models ≤1.5B parameters, while GRPO's impact has been most significant at larger scales (e.g., DeepSeek-R1 at 67B+). (3) The RGR formulation uses on-policy sampling ($\pi_{\theta}$) while GRPO uses off-policy sampling ($\pi_{\theta_{\text{old}}}$), introducing a confound between removing clipping and changing the sampling distribution. (4) RGR retains KL regularization against a reference model, which itself adds memory and compute overhead. (5) The paper trains on only 1,800 GSM8K samples, which is a small fraction of the available data.

**Novelty assessment**: The core finding—that PPO-style clipping can be removed—is valuable, but the paper does not perform external literature verification due to retrieval limitations in this run. The claim partially overlaps with prior work by Ahmadian et al. (2024) on REINFORCE for RLHF, and the group-relative advantage idea is inherited from GRPO. The main novelty lies in (a) demonstrating that negative feedback (not just positive filtering) is critical for stable training, and (b) isolating which GRPO components contribute to reasoning-specific gains. These findings are practically useful but incremental. Manual literature verification is recommended before final publication decisions.

## Strengths
**S1. Timely and well-motivated research question.** The paper asks whether GRPO's complex loss function is overengineered for LLM reasoning—a question that has direct implications for both practical training efficiency and scientific understanding of how RL objectives shape reasoning behaviors. This is a relevant and useful investigation given GRPO's widespread adoption following DeepSeek-R1.

**S2. Systematic ablation methodology.** Rather than proposing yet another GRPO variant, the paper takes the principled approach of stripping components away. The three ablation variants (positive-only advantages, removing PPO constraints via RGR, removing advantage estimation via plain REINFORCE) are well-designed to isolate the key factors. This allows the authors to attribute the observed effects to specific components rather than aggregate method changes.

**S3. Diverse evaluation suite.** The use of 9 benchmarks spanning English math (GSM8K, MATH, Gaokao2023-Math-En, OlympiadBench, AMC23), Chinese math (CMATH, CN-Middle-School), and STEM (MMLU-STEM, Gaokao2024) provides reasonable coverage across difficulty levels and languages. This strengthens the generalizability of the empirical observations within the tested domain.

**S4. Useful negative result identification.** The finding that positive-only training (discarding below-baseline completions) leads to collapse, even with PPO clipping still active, is a clean and practically important result. It demonstrates that negative feedback is a necessary condition for stable RL-based post-training, independent of the clipping mechanism.

**S5. Transparent claims about many findings.** The paper correctly identifies that PPO-style clipping is unnecessary when initializing from strong pre-trained policies, aligning with and extending prior observations by Ahmadian et al. (2024). The scope of this claim is appropriately connected to the experimental setup.

## Weaknesses
### W1. Missing statistical rigor (Major, Fixable)
All benchmark results (Tables 1-3) are single-run point estimates without standard deviations, confidence intervals, or significance tests. Most RGR-vs-GRPO differences are small (1-4 percentage points), and the paper's headline claim—"RGR surpasses GRPO in 17 out of 27 individual comparisons"—cannot be assessed for statistical reliability. Without multi-seed variance or a paired significance test, these differences could be noise. This undermines the paper's central comparative conclusion.

**Required fix**: Report mean ± std over ≥3 seeds for at least the main model-benchmark pairs (Qwen2.5-1.5B on GSM8K, MATH, CMATH). Add a paired bootstrap significance test for RGR vs GRPO. Qualify the 17/27 claim as preliminary.

---

### W2. Small model scale limits contribution scope (Major, Partially fixable)
All experiments use models ≤1.5B parameters. While the authors acknowledge hardware constraints, the paper's narrative does not consistently qualify claims by scale. GRPO's practical significance has been demonstrated at large scale (DeepSeek-R1 at 67B+), and it is unknown whether findings about PPO clipping's irrelevance transfer to larger models where training dynamics differ substantially. The paper currently presents RGR as "a competitive reinforcement learning objective for reasoning tasks" without specifying the scale regime.

**Required fix**: 
- Explicitly bound all contribution claims to models <2B parameters in abstract and conclusion.
- Add a scaling discussion analyzing why findings might or might not transfer to larger models (e.g., citation of empirical scaling laws for RL fine-tuning).
- Ideally, add one experiment at 7B scale for the key comparison.

---

### W3. On-policy vs off-policy confound in RGR comparison (Major, Fixable)
The RGR gradient (Eq. 2) uses on-policy sampling $\pi_{\theta}$, while GRPO (Eq. 1) uses off-policy sampling $\pi_{\theta_{\text{old}}}$. This difference is not mentioned or justified in the paper. The observed comparable or better performance of RGR could be due to on-policy sampling rather than the removal of clipping. This is a confound in the central comparison.

**Required fix**: 
- Explicitly discuss the sampling difference.
- Add an ablation comparing (a) on-policy RGR vs (b) off-policy RGR with importance ratios but no clipping, to isolate the effect of clipping removal from the sampling change.

---

### W4. RGR retains KL regularization and reference model (Moderate, Fixable)
The paper emphasizes "simplification" by removing PPO clipping, but RGR retains the KL divergence penalty against a reference model $\pi_{\text{ref}}$. This requires storing a full separate copy of the model and computing its log-probabilities at each step—a significant memory and compute cost. The "transparency and efficiency" claim is weakened by this retained component.

**Required fix**: 
- Add an ablation removing the KL term from RGR to test its necessity.
- In the text, explicitly compare the memory/compute profile: RGR (policy + reference model + advantage) vs GRPO (policy + reference model + advantage + clipping computation). Quantify the actual savings.

---

### W5. On-policy RGR's gradient formulation has subtle bias (Moderate, Fixable)
The RGR gradient (Eq. 2) is written as:
$$\nabla_{\theta} \mathcal{J}_{\text{RGR A}}(\theta) = \mathbb{E} \left[ q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta}(O \mid q) \right] \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \left\{ \nabla_{\theta} \log \pi_{\theta}(o_{i,t} \mid q, o_{i,<t}) \cdot \hat{A}_{i,t} - \beta \nabla_{\theta} \text{D}_{\text{KL}} \left[ \pi_{\theta} \parallel \pi_{\text{ref}} \right] \right\}$$

There is a subtle issue: using on-policy samples $\pi_{\theta}$ in the expectation while also computing the gradient of $\log \pi_{\theta}$ with respect to $\theta$ creates a double-counting dependency. The standard REINFORCE gradient uses samples from $\pi_{\theta_{\text{old}}}$ with a stop-gradient on the sampling distribution, or uses the score function estimator which handles this automatically. The paper's formulation is mathematically valid under the score function estimator, but the KL gradient term's interaction with on-policy sampling needs careful handling in implementation. The paper does not discuss whether $\pi_{\theta}$ is used with stop-gradient on the sampling trajectory.

**Required fix**: Clarify whether the sampling distribution uses stop-gradient or detached copies of $\theta$ during training. This is crucial for reproducibility.

---

### W6. Limited training data and steps (Moderate, Fixable)
The paper trains on only 1,800 of 7,473 GSM8K training samples (24%) for approximately 70 steps. This limited training budget raises questions about whether observed patterns hold with full-data training. The paper does not analyze whether performance had plateaued by step 70.

**Required fix**: (a) Report training curves beyond 70 steps for at least one condition. (b) Add a small experiment training on the full GSM8K training set to verify that findings about negative feedback and clipping are not artifacts of small-data training.

---

### W7. Per-sequence advantage is constant across tokens (Minor, Not a fix priority)
The GRPO advantage $\hat{A}_{i,t}$ uses the same sequence-level reward $r_i$ for all token positions $t$ within a completion. This means the model cannot learn fine-grained credit assignment within a reasoning trace. While the paper's results suggest this is not limiting for simple math tasks, it may be important for tasks requiring longer, more structured reasoning (e.g., multi-step theorem proving). This limitation is not discussed.

**Required fix**: Add a brief discussion of the per-sequence advantage assumption and its potential limitations, particularly for tasks beyond the current evaluation scope.

---

### W8. Introduction and conclusion contain overclaims (Minor, Fixable)
- The introduction claims to "contribute both conceptual clarity and practical guidance" without specifying what clarity or guidance is provided.
- The conclusion claims to "advance our understanding of how reinforcement learning objectives shape the post-training of large language models" broadly, but the paper only tests math reasoning on small models.
- The conclusion introduces "generalization in LLMs" as a contribution, but no generalization experiments are performed.

**Required fix**: Replace overclaims with evidence-grounded phrasing. See specific annotations (A1, A10) for copy-ready revisions.

---

### W9. Related work is a descriptive survey rather than comparative positioning (Minor, Fixable)
The related work section lists papers chronologically rather than organizing them by comparison axes (e.g., supervision type, credit assignment mechanism, stability approach). This makes it harder for readers to understand the precise gap being filled.

**Required fix**: Reorganize the related work around comparative dimensions rather than paper-by-paper summaries.

## Score
**Final Score: 5/10**

**Rationale**: The paper addresses a well-motivated question about GRPO simplification and provides useful ablation results (particularly the necessity of negative feedback and the dispensability of PPO clipping). The systematic ablation methodology is sound. However, the score is limited by several factors:

1. **Statistical evidence is incomplete** — all comparisons are single-run point estimates without variance or significance testing (W1). This fundamentally limits confidence in the central comparative claim.
2. **Scale restriction** — results are demonstrated only on models ≤1.5B parameters (W2), while GRPO's relevance is mainly at larger scales. The paper's title, abstract, and conclusion do not consistently bound their claims by scale.
3. **Confound in key comparison** — the RGR formulation changes both the clipping mechanism AND the sampling distribution (on-policy vs off-policy) relative to GRPO (W3), making it difficult to attribute the observed performance to the removal of clipping alone.
4. **Incremental novelty** — the core finding (PPO clipping removal is fine) is consistent with and extends prior work by Ahmadian et al. (2024). The paper does not conduct external literature verification (deferred due to retrieval limitations in this run), so novelty assessment is preliminary.

The paper has strengths in its clear ablation design, diverse benchmark evaluation, and practically valuable negative findings about positive-only training. With the addition of statistical significance testing, scaling validation, and confound-controlled comparisons, the work could be strengthened considerably. The topic is timely and the core investigation is worth pursuing.

**Post-Revision Target**: [6.5, 7.5]/10 — achievable if W1 (statistical rigor), W2 (scale bounding), W3 (confound resolution), and W4 (KL reference model analysis) are addressed in revision.