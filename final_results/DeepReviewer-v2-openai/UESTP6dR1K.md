## Summary
This paper proposes ASPEC, a framework for creating stateful teams of specialist LLM agents that accumulate cross-query expertise. The framework consists of three components: (1) an offline **Discovery** phase that uses evolutionary search (creation + crossover) to generate diverse specialist agent archetypes; (2) a **Cultivation** phase where selected specialists deepen expertise through post-execution reflection stored in a persistent memory module; and (3) a lightweight "retain-then-escalate" **Meta-Controller** — a learned binary policy — that decides whether to reuse the current agent architecture or resample a new one at query time.

ASPEC is evaluated on five benchmarks (MATH, HumanEval, MMLU, GPQA, SciCode) against 13 baselines covering hand-designed single/multi-agent systems, automated specialization methods, and autonomous agent design frameworks. The main results show ASPEC achieving best average performance (69.6%) with particularly strong gains on expert-level benchmarks: GPQA (+6.5% over vanilla) and SciCode (+2.6%). Ablation studies confirm that specialist operators are the primary driver of both accuracy and efficiency, and that the meta-controller provides near-oracle accuracy at substantially lower cost than LLM-as-gate alternatives.

**Key strengths:** The lifecycle concept (discover-then-cultivate) is a sensible approach to reconciling the static vs. per-query trade-off in agent design automation. The efficiency analysis (Table 2) convincingly demonstrates that ASPEC achieves its accuracy gains at lower inference cost than comparable query-level methods. The sensitivity analyses and convergence visualizations provide useful insight into the discovery process.

**Key weaknesses found in this audit:** (1) The Architect's objective function (Eq. 2) has a notation error — V_π(s_{t+1}) is referenced but not defined, and the reference to Equation 3 is incorrect. (2) The specialist selection objective (Eq. 5) double-counts performance between the two terms, making the optimization not well-principled. (3) The confusion matrices in Figure 8 contain percentage values that do not sum to 100%, indicating a numerical error that undermines the rationality analysis. (4) The cultivation phase is described at a high level without the implementation details needed for reproducibility (reflection format, chunking, retrieval top-k, memory update policy). (5) No variance or statistical significance is reported for any experimental result. (6) The claim that performance gains are "robustly transferable" attributes the cross-domain transfer to "T-shaped reasoning" without direct evidence. (7) The limitations section focuses on future work rather than naming concrete weaknesses of the current experiments.

**Novelty & Literature Context (deferred due to Retrieval-Disabled Mode):** External literature verification is unavailable in this run. Novelty and comparison claims regarding the paper's positioning relative to prior agent design automation work are deferred pending manual verification. The two claimed contributions — a discovery-cultivation lifecycle and a retain-then-escalate control policy — appear plausible against the cited literature but require systematic cross-referencing for final verdict.

## Strengths
**S1. Novel integration of discovery and cultivation into a unified lifecycle.** ASPEC's two-stage framework — first evolutionary search over agent archetypes, then experience-grounded cultivation — provides a coherent solution to a recognized tension in automated agent design (static vs. per-query). The evolutionary operators (creation, crossover, selection) are well-motivated and the ablation study isolating each component's contribution (Figure 6) is informative. The convergence analysis (Figure 7) showing that discovery converges to similar archetypes across trials on focused domains (GPQA) but diversifies on broad domains (MMLU) adds credibility.

**S2. Strong empirical efficiency.** Table 2 is a highlight of the paper. ASPEC's training cost ($1.38, 53 minutes) and inference cost ($0.88) on GPQA are substantially lower than comparable automated design frameworks (AFlow: $20.14 training, $1.58 inference; MaAS: $3.43 training, $2.07 inference), while achieving the highest accuracy (62.8%). The ablation showing that removing specialists triples cost while dropping accuracy by 5.4% cleanly demonstrates the value of the learned specialist pool.

**S3. Principled gating mechanism.** The retain-then-escalate meta-controller is a lightweight learned policy that addresses a real practical bottleneck — the Architect's invocation cost. The rationality analysis (Section 5.3.1) revealing a deliberate accuracy-cost trade-off (high "overconfident retain" rate reduces cost while only modestly impacting accuracy) provides empirical evidence that the controller is solving the right optimization problem, even if its individual decisions diverge from the oracle proxy.

**S4. Thoughtful sensitivity and convergence analyses.** The exploration of the k parameter (specialist pool size) and m parameter (sliding window length) in Figure 6 goes beyond typical sensitivity checks by connecting the observed "Goldilocks" effect to a mechanistic explanation (experience fragmentation at high k). The convergence visualizations (Figure 7) provide an intuitive check that the discovery process behaves as expected on narrow vs. broad domains.

**S5. Transfer analysis across models and domains.** The cross-model evaluation (Figure 5 left) showing consistent gains across Gemini 2.0 Flash, GPT-4o-mini, and Llama 3.3 70B, and the ONLYSPEC cross-benchmark analysis (Figure 5 right), demonstrate that the ASPEC methodology is not tied to a specific backbone. This is practically important for adoption.

## Weaknesses
### W1. Mathematical/Notation Errors in Core Formulations (Critical)

**W1a. Architect's objective (Eq. 2) contains an undefined value function.** The paper states "$\mathcal{G}_t^* = \arg\max_{\mathcal{G}_t \in \mathcal{G}} \mathbb{E}[U_t - \lambda C_t(\mathcal{G}_t) + V_{\pi_\theta}(s_{t+1})]$ (2)" and claims "$V_{\pi_\theta}(s_{t+1})$ is the expected future value given the next state, formally defined in Equation 3." However, Equation 3 defines $s_t = (e_q(q_t), e_g(\mathcal{G}_{t-1}))$, which is the *state representation*, not a value function. No equation in the paper actually defines $V_{\pi_\theta}$. This is a significant clarity gap: a reader cannot determine whether $V_{\pi_\theta}$ is the meta-controller's expected return (which would be circular since the meta-controller policy is being trained), a separately learned critic, or an approximation. **Impact:** This error directly affects the interpretability of the core optimization objective of the Architect, which is central to the entire framework. **Fix:** Either define $V_{\pi_\theta}$ as a learned value function (e.g., a neural network trained via TD learning on the meta-controller's reward stream) or remove the term and make the Architect's objective purely myopic.

**W1b. Specialist selection objective (Eq. 5) double-counts performance.** The selection objective sums $\sum p(O_i^S)$ over selected specialists and then adds $\sum_{j=1}^k \max_{O_i^S \in C_j \cap \mathbb{O}_{\text{spec}}} p(O_i^S)$ as a diversity term. Since the second term also sums performance values (per-cluster max performance), a specialist that is both high-performing and falls in a distinct cluster contributes to both terms, creating an objective function whose optimization target is unclear. Additionally, the unweighted sum of performance and "diversity" (which is also a function of performance) means the optimization does not have a clear trade-off parameter. **Impact:** The selection phase, which determines which specialists proceed to cultivation, is not based on a well-defined optimization criterion. **Fix:** Introduce an explicit trade-off coefficient $\lambda$: $\text{Objective} = \sum p(O_i^S) + \lambda \cdot \sum_{j} \max_{O_i^S \in C_j \cap \mathbb{O}_{\text{spec}}} p(O_i^S)$, or replace with a standard multi-objective approach (e.g., Pareto frontier selection).

### W2. Numerical Error in Confusion Matrices (Major)

**W2. Figure 8 percentages do not sum to 100%.** For GPQA: 17.8% + 45.9% + 5.6% + 41.9% = 111.2%. For MMLU: 33.0% + 7.2% + 12.8% + 15.0% = 68.0%. A confusion matrix showing "fraction of all queries" must by definition sum to 100%. This is a factual error. The raw counts (20, 149, 20, 149 for GPQA) suggest ~338 total queries; global percentages would be approximately 5.9%, 44.1%, 5.9%, 44.1%. **Impact:** The rationality analysis (Section 5.3.1) — which draws conclusions about the meta-controller's "overconfident" vs. "wasteful caution" trade-off — is based on potentially incorrect numbers. **Fix:** Verify the counts, recompute percentages (specifying whether they are row-normalized, column-normalized, or global), and correct all values in Figure 8 and associated text.

### W3. Missing Variance and Statistical Significance (Major)

**W3. No result in the paper includes variance.** Every number in Table 1, Figure 5, Figure 6, and all ablation tables is a single-point estimate. The improvements on several benchmarks are small (e.g., ASPEC 69.6% average vs. AFlow 68.4% — a 1.2% gap; on MMLU, ASPEC 90.0% trails AFlow 90.5%). Without standard deviations over multiple seeds, a reader cannot determine whether any of these differences are statistically reliable. The sensitivity plots (Figure 6) show "mean over 4 runs" but the variability is only shown as the central line — no error bars, no individual run markers. **Impact:** Readers cannot assess the robustness of the claimed gains. **Fix:** Report mean ± std over ≥3 seeds for all key results, add pairwise significance tests against the strongest baseline for each benchmark, and add error bars/confidence bands to all plots.

### W4. Reproducibility Gaps in Method Description (Major)

**W4. The Cultivation phase lacks implementation detail.** Section 3.2 describes cultivation as "post-execution reflection on a training corpus" with "semantic retrieval mechanism" but omits: (a) the exact reflection format (structured fields vs. free text), (b) how the training corpus is constructed, (c) the chunking strategy for memory, (d) the retrieval model and top-k setting, (e) whether memory is append-only or consolidated, and (f) how retrieved chunks are integrated into the specialist's prompt. The paper references Appendix A.3 for "examples" but the main text should provide enough detail for basic reproducibility. **Impact:** Without these details, other researchers cannot implement or fairly compare against ASPEC. **Fix:** Add a specification paragraph describing the memory format, retrieval parameters, and integration method in the main text.

**W4b. Meta-controller training is not described.** The meta-controller is a learned neural policy $\pi_\theta$, but no information is given about: the reward function $R_t(s_t, a_t)$, the training algorithm (policy gradient? Q-learning? behavioral cloning?), the data collection procedure (online? from offline trajectories of the Architect?), the network architecture beyond "MLP," or the training hyperparameters. **Impact:** This is a critical reproducibility gap for the paper's second main contribution. **Fix:** Add a subsection describing meta-controller training (or clarify if it is trained via supervised learning on decisions made by the LLM-as-gate oracle).

### W5. Overclaimed and Unsupported Statements (Moderate)

**W5a. "Robustly transferable" claim lacks mechanistic evidence.** The text states "performance gains from the ASPEC methodology are robustly transferable across different models and benchmarks" and attributes this to "T-shaped reasoning strategies." While the empirical observation is interesting, the causal attribution is speculative — no analysis of what the specialists actually learn (e.g., memory content analysis, cross-domain chunk overlap) is provided. The ONLYSPEC ablation showing transfer might also be explained by simpler hypotheses (e.g., the base reasoning structure is more important than domain-specific knowledge). **Impact:** The transfer claim is overstated relative to the evidence provided. **Fix:** Add a brief analysis showing that memory chunks retrieved in cross-domain settings overlap with native-domain chunks, or revise the claim to acknowledge that the mechanism remains to be verified.

**W5b. "Significant performance gains" without significance testing.** The abstract claims "significant performance gains on expert-level scientific benchmarks like GPQA" — but no statistical significance test is reported anywhere in the paper. "Significant" in a scientific paper should mean statistically significant unless clearly qualified. **Impact:** Misleading framing. **Fix:** Replace "significant" with "substantial" (6.5% absolute) or add significance tests.

**W5c. "Matching state-of-the-art" on broader tasks.** ASPEC does not match SOTA on all tasks: on MMLU, AFlow (90.5%) outperforms ASPEC (90.0%); on HumanEval, MaAS (91.6%) outperforms ASPEC (91.4%). The claim should be bounded to specific benchmarks. **Impact:** Overclaim reduces credibility with informed readers. **Fix:** Restate as "achieving competitive results on broader-domain benchmarks while leading on expert-level benchmarks GPQA and SciCode."

### W6. Limitations Section Focuses on Future Work Rather Than Current Weaknesses (Moderate)

**W6. The Limitations section (Section 6) reads primarily as a future work agenda rather than an honest assessment of current experimental limitations.** It discusses theoretical frameworks, SWE-bench extension, bias amplification, and meta-controller improvement, but does not acknowledge the most obvious limitations of the present study: (1) no variance reporting; (2) only 5 benchmarks, all academic; (3) no out-of-distribution generalization test; (4) reliance on a single LLM backbone for most experiments (Gemini 2.0 Flash); (5) the Architect's LLM calls introduce variability and potential hallucination that is not analyzed. **Impact:** A candid limitations section increases reviewer trust. **Fix:** Add 2-3 sentences that explicitly name what the current experiments do and do not establish.

### W7. Minor Writing and Structural Issues

**W7a.** The first Introduction paragraph (Motivation) is a dense literature dump that lists ~15 references in a single paragraph without clear organizational structure. Readers unfamiliar with the specific papers may lose the thread. **Fix:** Either shorten the literature coverage to the most important 3-4 references per paradigm, or provide a comparison table.

**W7b.** The Related Work section mixes two distinct streams (role prompt optimization vs. team generation) without explicit sub-categorization. **Fix:** Split or add an organizing sentence.

**W7c.** The paper uses "similar" (typo for "similar") in the crossover description. Minor but suggests insufficient proofreading.

**W7d.** The claim that LLMs were used in writing (footnote 1) is transparent but the paper would benefit from a pass to reduce occasional verbose/phrasal constructions.

### Ranked Priority Defect Board

| Rank | Issue | Severity | Validity Risk | Fix Effort | Confidence |
|------|-------|----------|--------------|------------|------------|
| 1 | Eq (2) notation error: V_π undefined | High | Medium | Low | High |
| 2 | Confusion matrix percentages incorrect (Fig 8) | High | High | Low | High |
| 3 | No variance/significance reporting | High | Medium | Medium | High |
| 4 | Selection objective (Eq 5) double-counts | Medium | Medium | Low | High |
| 5 | Cultivation & meta-controller reproducibility gaps | High | Medium | Medium | High |
| 6 | Overclaimed transfer / significance wording | Medium | Medium | Low | High |
| 7 | Limitations section evades current weaknesses | Medium | Low | Low | High |

## Score
**Final Score: 6/10**

**Scoring rationale:**

- **Research value (primary):** The core idea — a two-stage lifecycle (evolutionary discovery + experience cultivation) governed by a retain-then-escalate controller — is well-motivated and addresses a genuine tension in automated agent design. The efficiency analysis is the strongest contribution, demonstrating that the ASPEC approach can match or exceed both static and per-query baselines at lower cost. **Value score: 7/10.**

- **Novelty (primary, deferred verification):** The two claimed contributions (lifecycle framework, retain-then-escalate controller) appear plausible based on the authors' own literature survey, but novelty cannot be fully verified without external literature retrieval. The paper cites relevant work in both task-level and query-level agent design, and the integration of discovery and cultivation into a unified lifecycle does not have a directly matching prior citation in the paper. **Novelty estimate: 6/10 (pending verification).**

- **Validity/Soundness:** Three significant concerns reduce confidence: (1) Equation (2) contains an undefined value function referenced to the wrong equation, making the core optimization objective unclear; (2) Figure 8's confusion matrix percentages are arithmetically incorrect (not summing to 100%); (3) No variance or significance testing is reported for any result. These are fixable but currently material. **Soundness score: 5/10.**

- **Reproducibility:** The method section omits critical implementation details for both the cultivation phase (reflection format, chunking, retrieval parameters, memory update policy) and the meta-controller training (reward function, training algorithm, data collection). These gaps prevent independent reimplementation. **Reproducibility score: 4/10.**

- **Presentation:** The paper is generally well-written with clear section organization, informative figures, and understandable equations. However, the first Introduction paragraph is overly dense, the Related Work mixes distinct sub-threads, and some claims exceed what the evidence supports. **Presentation score: 6/10.**

**Summary:** ASPEC presents a promising approach to automated agent design with a compelling efficiency story. The mathematical errors (Eq. 2 reference, confusion matrix percentages) must be corrected, variance reporting must be added, and the method description must be substantially expanded for reproducibility. With these revisions, the paper would be a solid contribution at 7-8/10. In its current form, the notation errors and missing variance are major concerns.

**Post-Revision Target:** 8/10 — achievable if the notation errors are fixed, variance is reported, and reproducibility details are added.