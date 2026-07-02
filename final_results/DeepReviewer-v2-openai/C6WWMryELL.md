## Summary
This paper addresses the problem of output length volatility in long-form text generation by LLMs — the observation that repeated generations from the same prompt produce wildly varying output lengths and content. The authors make three contributions: (1) VOLTBench, a heterogeneous-task benchmark (unstructured + structured tasks, English + Chinese, multiple instruction complexities) that systematically quantifies across-run length volatility using metrics LSD, LVC, and MLA; (2) an attention-trace analysis that identifies two internal failure patterns — Attention Collapse and Attention Instability — that precede observable generation failures; and (3) SELB (Structural Enforcement via Logits Boosting), a training-free decoding strategy that applies structural boosting to enforce section transitions and proactive suppression to block early-termination tokens.

Experiments on VOLTBench across 9 models and 4 decoding baselines confirm that output length volatility is widespread. The proposed SELB method is reported to improve mean output length by 148% and reduce length volatility by 69% compared to the LongWriter-8B baseline on a 100-section structured generation task, while achieving 100% Structured Content Accuracy (SCA) and 86.7% Unstructured Content Accuracy (UCA).

The paper tackles a genuinely underexplored problem — across-run volatility rather than single-generation quality — and provides both a diagnostic benchmark and a practical mitigation method. However, significant methodological concerns (N=5 runs for volatility estimation, no confidence intervals, selective baseline comparison, underspecified hyperparameters, correlational attention analysis without causal validation) temper the strength of the claims. Novelty assessment is deferred because external literature retrieval was unavailable in this run.

## Strengths
1. **Well-motivated problem selection.** Across-run output volatility is a practically important yet underexplored problem in long-form LLM generation. The paper convincingly demonstrates that length variance across repeated generations is large (LongWriter-8B's standard deviation reaches 103% of its mean length), with direct implications for reliable deployment, cost predictability, and user trust. This fills a clear gap relative to prior benchmarks that only measure single-instance quality.

2. **Comprehensive benchmark design.** VOLTBench covers multiple dimensions that existing benchmarks lack: both unstructured (story, dialogue) and structured (code, math) tasks, multiple languages (English, Chinese), multiple instruction complexity levels, and crucially, multiple sampling with dedicated stability metrics. The chapter-based scaling from 5 to 500 sections (up to 100k words) systematically tests model behavior at the limits of context utilization.

3. **Mechanistic analysis effort.** The attention-trace analysis in Section 5 provides an interpretable diagnostic framework by connecting observable generation failures (incomplete generation, section skipping) to measurable internal signals (Attention Collapse, Attention Instability). This goes beyond purely phenomenological benchmarking and offers a template for future work on decoding-time failure prediction.

4. **Practical mitigation strategy.** SELB is training-free, operates at decoding time, and is clearly motivated by the identified failure patterns. The method is computationally lightweight (logit modification only) and directly addresses the volatility problem without requiring model fine-tuning or data collection. The reported improvements on structured tasks (100% SCA, substantial volatility reduction) are practically meaningful for applications requiring predictable output structure, such as automated report generation or code synthesis.

5. **Clean experimental framework.** The paper evaluates a diverse set of 9 models spanning architectures (dense, MoE, state-space), sizes (1.5B to 70B+), and families (open-source, API-based). The inclusion of 4 training-free decoding baselines helps contextualize SELB's performance relative to simpler alternatives. The three-stage structure (benchmark → probe → mitigate) provides a coherent narrative arc.

## Weaknesses
The weaknesses below are ordered by severity, with the most impactful issues first.

### 1. Insufficient statistical rigor for core volatility claims (Major)

The paper's headline claims — 148% length improvement and 69% volatility reduction — are based on only N=5 generation runs per configuration. With such a small sample, the estimated Length Variation Coefficient (LVC) and Mean Length Accuracy (MLA) have wide confidence intervals. For example, the approximate 95% CI for an LVC of 20% with N=5 ranges from ~7.6% to ~32.4%. No bootstrap confidence intervals, standard errors, or significance tests are reported for any of the main effect sizes. The paper also does not report the variance of LSD/LVC/MLA across different random seeds, making it impossible to assess whether the reported improvements are statistically significant rather than within the range of sampling noise. **Fix:** Report 95% bootstrap confidence intervals for all main metrics, increase N to at least 10 for key comparisons, and add paired significance tests (e.g., Wilcoxon signed-rank) between SELB and each baseline.

### 2. Selectively chosen comparisons inflate reported gains (Major)

Section 6.3 compares SELB almost exclusively against LongWriter-8B, which has unusually poor metrics (LVC=45.4%, SCA=32.6%). Several baseline methods in Table 2 — such as Repetition Penalty (LVC=18.6%, SCA=98%), Length Constraint (LVC=28.65%, SCA=96%), and Lookahead Decoding (LVC=9.3%, SCA=94%) — achieve substantially better results than LongWriter-8B. A direct comparison of SELB against these stronger baselines is missing from the main results paragraph. On UCA, SELB's 86.7% is actually lower than Deepseek-R1's 93.3% and comparable to several baselines, yet the paper claims "a 30% improvement over LongWriter-8B" without acknowledging this context. **Fix:** Present SELB results alongside all Table 2 baselines in the Section 6.3 comparison. Reframe UCA claims to note that SELB matches strong baselines on quality while improving length accuracy and structural compliance. Explicitly state which base model is used for the 148%/69% calculations.

### 3. Attention-volatility link is correlational, not causal (Major)

Section 5 identifies attention patterns that correlate with generation failures, but the analysis does not establish causation. The observed Attention Collapse and Attention Instability could be epiphenomena of underlying causes such as hidden-state saturation, KV-cache pressure, or softmax saturation in long sequences. Critically, the proposed SELB method does not validate the attention hypothesis: SELB modifies output logits (not attention), so its success in reducing volatility does not confirm that attention failures are causal. If SELB improves stability without measurably increasing constraint attention, the attention-collapse theory is incomplete. **Fix:** (a) Replace causal language ("causes," "drives") with correlational language ("is associated with," "precedes"). (b) Add an analysis showing that SELB increases ᾱ(t) compared to baseline decoding, or conduct an intervention experiment (e.g., artificially suppress attention to induce volatility). (c) Discuss alternative explanations explicitly (hidden-state drift, positional encoding degradation).

### 4. Underspecified method parameters hinder reproducibility (Major)

The SELB method relies on several critical parameters that are not specified: the boosting constant β is only described as "a large positive constant"; the section length threshold τ_max is not given; the banned token set V_banned is illustrated with only one example; the title token vocabulary V_title^{(p+1)} is not defined. Without these details, the method cannot be independently reproduced or applied to new settings. Additionally, Equation (2) uses an undefined superscript 'l' on the LHS s_{t,j}^l, creating notation ambiguity. The composition order M = M_fail ∘ M_struct is specified but potential conflicts (what if a token is both boosted and suppressed?) are not addressed. **Fix:** Report concrete values (β=100.0, τ_max = specified per-section word count), provide V_banned as a complete appendix table, clarify V_title identification logic, fix the notation in Eq. (2), and specify conflict resolution priority (e.g., suppression takes precedence).

### 5. No ablation study isolating SELB components (Major)

SELB combines two mechanisms: structural enforcement (M_struct, logit boosting for section transitions) and failure prevention (M_fail, suppression of banned tokens and early EOS). Without an ablation study that tests each component separately, readers cannot determine which mechanism drives the observed improvements. It is plausible that the EOS suppression alone (a simple and well-known technique) accounts for most of the volatility reduction, with M_struct providing only marginal benefit on structured tasks. **Fix:** Add an ablation study with four conditions: (a) baseline only, (b) M_struct only, (c) M_fail only, (d) full SELB. Report LSD, LVC, MLA, SCA, and UCA for each condition.

### 6. Key experimental results relegated to appendix (Minor)

The free-form generation extension (Section 6.4) and the Representational Stability Analysis (Appendix H) contain critical validation evidence but are only summarized in the main text. The SELB-Hybrid method for free-form tasks introduces a substantially different mechanism (Keep-Alive, Stop Token Suppression) that is not described in the main method section. Readers relying only on the main text cannot evaluate the validity of the generalization claim. **Fix:** Move the key SELB-Hybrid mechanism description and at least a summary of free-form results to the main text, or expand Section 6.4 with sufficient method detail.

### 7. Two-thousand-word threshold claim is overstated (Minor)

The introduction claims LLM outputs "struggle to surpass the 2k-word threshold" as a universal limitation, citing Bai et al. (2024). However, the paper's own experiments show LongWriter-8B producing 6,320 words mean output (Table 2), and several models generate well above 2k. This over-generalization weakens the motivation. **Fix:** Qualify the threshold claim by model family or cite evidence for the specific models tested.

### 8. No inference cost or latency analysis (Minor)

Since SELB performs per-token logit modification and section-title pattern matching, its computational overhead should be quantified. The paper claims SELB is "lightweight" but provides no wall-clock time comparison against standard decoding or other baselines. For practical deployment, a method that adds latency may be less attractive regardless of quality gains. **Fix:** Report average generation time (seconds per 1000 tokens) for SELB vs. standard greedy/top-k decoding on a controlled GPU environment.

### 9. Failure pattern detection not operationalized (Minor)

The two failure patterns (Incomplete Generation, Section Skipping) are described qualitatively but not defined as measurable metrics. Without operationalization (e.g., Section Completion Ratio, Section Gap Index), these patterns cannot be reliably detected or compared across experiments. **Fix:** Define concrete operational metrics and report their values across models and conditions.

### 10. Conclusion lacks limitations and future work directions (Minor)

The conclusion restates the same quantitative claims without synthesizing new insights, acknowledging limitations, or proposing concrete next steps. An honest limitations paragraph is absent from the entire paper. **Fix:** Add a limitations paragraph covering SELB's dependence on task-specific parameter tuning, the correlational nature of the attention analysis, and the need for automated hyperparameter selection in future work.

**Novelty Note:** External literature retrieval was unavailable in this run (Retrieval-Disabled Mode). All novelty-related conclusions are deferred for manual verification. The contributions appear to offer clear practical value (VOLTBench as a diagnostic tool, SELB as a practical mitigation), but the degree of overlap with existing decoding-time control methods and length-adherence benchmarks cannot be assessed from the manuscript alone.

## Score
**Final Score: 6/10**

**Rationale:** This score reflects the paper's genuine practical contribution (a well-motivated benchmark and a functional mitigation method) weighed against significant methodological limitations that reduce confidence in the headline claims.

**Positive factors supporting this score:**
- The problem of across-run output volatility is practically important and genuinely underexplored.
- VOLTBench provides a useful multi-dimensional evaluation framework that fills gaps in existing benchmarks.
- SELB demonstrates clear practical improvements on structured generation tasks, with 100% SCA and substantial volatility reduction.

**Factors limiting the score:**
- The statistical basis for core claims is weak (N=5, no confidence intervals, no significance tests), which is a major concern for a benchmark-focused paper.
- Selective baseline comparisons (primarily against the weak LongWriter-8B) inflate the apparent gains.
- The attention-based mechanistic analysis is correlational and not causally validated by the proposed mitigation.
- Method reproducibility is limited by underspecified hyperparameters (β, τ_max, V_banned).
- No ablation study isolates the contribution of each SELB component.
- Novelty relative to prior work cannot be fully assessed due to retrieval unavailability; manual verification is required.

**Score Interpretation on 10-point scale:**
6/10 = Acceptable with major revisions. The core ideas have merit and practical value, but the experimental evidence, statistical rigor, and method specification need substantial strengthening before the claims can be fully trusted. The paper would benefit from additional runs, comprehensive baseline comparison, ablation studies, and honest limitation disclosure.

**Post-Revision Target:** [7, 8]/10 — achievable if the authors address the major weaknesses (statistical rigor, baseline comparisons, ablation, method specification) and strengthen the mechanistic validation.