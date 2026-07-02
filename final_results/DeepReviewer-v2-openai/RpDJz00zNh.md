## Summary
# Final Review Report

## Summary

This paper proposes ConciseHint, a framework that reduces the token usage of large reasoning models (LRMs) by injecting concise hints (e.g., "make answer concise!") during the generation process — an approach the authors term "in-reasoning intervention." This contrasts with prior work that either adds control prompts before generation or fine-tunes models for conciseness offline. ConciseHint has three core components: (1) a complexity-adaptive injection interval (τ_k = α + β·l_k), which increases hint spacing as the reasoning gets longer to protect accuracy on complex queries; (2) a dynamic injection position strategy that moves from head to tail as generation proceeds to balance compute and effectiveness; and (3) ConciseHint-T, which learns hint embeddings via SFT on concise reasoning data (MixChain-Z-GSM8K), enabling controllable conciseness through interpolation. Experiments on GSM8K, AIME24, and GPQA-Diamond with Qwen3-4B/8B and DeepSeek-R1-14B show 27–49% token reduction while maintaining accuracy within ~1 point. ConciseHint also integrates as a plugin with existing baselines (BeConcise, Prompt, Deer, NoWait), achieving additional reductions of 14–40%.

**Strengths:** The in-reasoning intervention paradigm is practically motivated and orthogonal to existing methods. The adaptive interval mechanism is intuitive and supported by ablation studies showing that fixed intervals degrade complex-task accuracy. The plugin integration results demonstrate practical compatibility. The paper is clearly written and the experimental methodology is reproducible in principle.

**Weaknesses:** (1) The core adaptive formula (Eq. 1) has an unexamined positive-feedback property where long reasoning → fewer hints → potentially even longer reasoning. (2) Accuracy comparisons lack variance/confidence intervals, making small differences uninterpretable. (3) The ConciseHint-T training procedure omits key details (fixed injection interval used during training, dataset construction). (4) The Related Work section does not explicitly differentiate from early-exit methods that also intervene during generation. (5) The conclusion overclaims ("upper bound of efficiency") without discussing limitations. (6) The dynamic position formula (Eq. 3) uses ad-hoc constants (1024, 0.8) without sensitivity analysis.

**Score:** 6/10 — The paper presents a novel and practical paradigm with solid empirical support, but is held back by missing statistical rigor, incomplete methodological disclosure, and overclaiming in key statements. With revisions addressing the weaknesses, the paper could make a meaningful contribution.

## Strengths
1. **Novel paradigm with practical motivation.** The central idea — intervening during generation rather than before it — is well-motivated and genuinely distinct from the two dominant paradigms (prompting and fine-tuning). The paper correctly identifies that prior methods set conciseness behavior statically, while dynamic conditioning during token generation could provide finer-grained control.

2. **Clear technical design with ablation support.** The two key design choices (adaptive interval via Eq. 1 and dynamic position via Eq. 3) are each backed by ablation studies (Tables 3 and 4) that convincingly demonstrate their necessity. The ablation on AIME24 showing that fixed interval=64 drops accuracy from 67.00 to 45.33 is particularly compelling evidence for adaptive control.

3. **Strong empirical coverage across models and baselines.** The evaluation spans three model families (Qwen3-4B/8B, DeepSeek-R1-14B), three benchmarks with varying difficulty, and four baseline methods. The plugin integration results (Ours+X across all baselines) consistently show additional token reduction of 14–40%, demonstrating practical compatibility.

4. **ConciseHint-T with controllable length.** Training hint embeddings on concise data and enabling control via interpolation (γ) is a clean extension. The controllability curves (Figure 3) show predictable behavior across datasets, which is useful for deployment scenarios where users want to dial in a specific efficiency-accuracy tradeoff.

5. **Reproducibility-friendly elements.** The algorithm pseudocode (Algorithm 1), fixed hyperparameters (α=128, β=0.2), and explicit multi-run averaging (5/10 runs) make the core method relatively straightforward to reproduce.

## Weaknesses
### W1. Positive feedback loop in the core adaptive formula (Major)
**Location:** Page 1 - Method, Equation (1) and surrounding text.
**Evidence:** Equation (1): τ_k = α + β·l_k. As l_k increases (indicating a potentially complex query), τ_k increases, so hints become less frequent, allowing more tokens per cycle, further increasing l_k.
**Impact:** This positive feedback can lead to under-intervention on the most complex queries, exactly where accuracy protection is most needed. The assumption that length correlates with complexity (citing Muenighoff et al., 2025) is plausible but not universally true — models may produce long outputs due to overthinking loops rather than genuine complexity. In such cases, the formula would reduce hint frequency when hints would be most beneficial.
**Recommended fix:** Add an upper bound τ_max to prevent unbounded interval growth (e.g., τ_k = min(α + β·l_k, τ_max)). Also discuss cases where length-complexity correlation may break down and how the method behaves in those scenarios.

### W2. Missing variance/confidence intervals for accuracy comparisons (Major)
**Location:** Page 1 - Experiments 4.2 (Main Results), Table 1 and surrounding text.
**Evidence:** The paper reports only mean accuracy and token usage across 5-10 runs. No standard deviations, confidence intervals, or significance tests are provided. For a benchmark like GPQA-Diamond (198 questions), the reported accuracy "rise of 0.91" (51.82→52.73) is within the expected binomial noise range (~3.5% standard error).
**Impact:** Readers cannot assess whether accuracy differences across methods are statistically significant or merely noise. The claim "maintaining the performance well" is weakened without statistical support.
**Recommended fix:** Report standard deviations for all metrics, add significance tests (e.g., paired bootstrap or McNemar's test) for key comparisons, and soften any language that implies directional improvement when differences are within noise.

### W3. Missing methodological details for ConciseHint-T training (Major)
**Location:** Page 1 - Method (ConciseHint-T subsection, around line 89).
**Evidence:** The paragraph states hint embeddings are injected "at a fixed interval" during SFT, but does not specify: (1) what that fixed interval is, (2) how it was chosen relative to the adaptive interval used at inference, (3) the size and construction of the MixChain-Z-GSM8K dataset, (4) what "concise reasoning responses" means (human-written? distilled? truncated?).
**Impact:** The train-test mismatch (fixed interval training vs. adaptive interval inference) is a potential confound that could limit the effectiveness of learned embeddings. Incomplete dataset description makes the result hard to reproduce.
**Recommended fix:** Specify the training injection interval, justify its selection, describe dataset construction, and ideally train with the same adaptive schedule used at inference for consistency.

### W4. Insufficient differentiation from early-exit methods in Related Work (Major)
**Location:** Page 1 - Related Work (Section 2.2), lines 48-50.
**Evidence:** The Related Work section groups methods into training-free, SFT-based, and RL-based categories. Early-exit methods (Fu et al., 2025; Yang et al., 2025) are mentioned as training-free methods that "terminate the thinking in advance when meeting certain confidence conditions." However, the paper claims prior work "does not dynamically intervene in the model during the token generation," which is not entirely accurate — early-exit methods do intervene during generation by deciding when to stop.
**Impact:** The claimed novelty ("orthogonal and largely unexplored") may be contested by reviewers familiar with early-exit literature, as the distinction (stop vs. re-condition) is subtle and needs explicit articulation.
**Recommended fix:** Add a paragraph explicitly contrasting early-exit methods (which terminate generation) from ConciseHint (which re-conditions the model). Note that the experimental results show ConciseHint and Deer are complementary, which supports the differentiation.

### W5. Ad-hoc constants in position formula without sensitivity analysis (Moderate)
**Location:** Page 1 - Method, Equation (3): p = τ_k * min((τ_k - α)/1024, 0.8).
**Evidence:** The constants 1024 and 0.8 are empirically chosen but no sensitivity analysis is provided. While the ablation (Table 4) shows that dynamic position outperforms fixed positions, the specific values are not justified.
**Impact:** If the method is applied to models with very different context lengths or generation patterns, these constants may need re-tuning. Without guidance, reproduction may fail on different model families.
**Recommended fix:** Add a sensitivity study for both constants in the appendix. Explain the 1024 denominator as approximately 1/8 of the typical 8K context window.

### W6. Overclaiming and missing limitations in Conclusion (Moderate)
**Location:** Page 1 - Conclusion, lines 192-195.
**Evidence:** The conclusion states ConciseHint "substantially rais[es] the upper bound of efficiency" and describes the approach as a "promising paradigm" without any discussion of failure cases, assumptions, or boundary conditions.
**Impact:** The lack of limitations reduces scientific credibility. Key unstated limitations include: (i) the length-complexity correlation assumption, (ii) limited domain coverage of the learned embeddings (GSM8K-only training), (iii) potential for hint injection to disrupt reasoning on very short queries, (iv) the overhead of prefilling when injection position is not at the head.
**Recommended fix:** Add a dedicated limitations paragraph that honestly discusses the assumptions and boundaries of the approach, as proposed in the annotation.

### W7. Transition word analysis overinterprets correlational evidence (Minor)
**Location:** Page 1 - Section 4.4, lines 182-183.
**Evidence:** The paragraph claims "reducing a large proportion of redundant transition words ... thereby promoting efficient self-reflections." However, the data only shows a reduction in count — it does not verify that the remaining self-reflections are of higher quality or that correctness is preserved at the step level.
**Impact:** The causal claim (fewer transitions → more efficient self-reflections) is unsupported. It could be that the model simply produces fewer self-correction attempts overall, including some that would have been beneficial.
**Recommended fix:** Add a step-level correctness analysis or soften the claim to descriptive language (e.g., "consistent with the model performing fewer redundant self-checks").

### W8. Inconsistent or missing details in experimental setup (Minor)
**Location:** Page 1 - Section 4.1, line 98.
**Evidence:** The evaluation configuration reports temperature and top-p but does not specify max generation length, stop conditions, or whether the generation runs until EOS. The phrase "the injected hints are also counted" is stated but the relative overhead of hint tokens versus savings is not analyzed.
**Impact:** Reproduction may be affected by unstated decoding parameters.
**Recommended fix:** Explicitly state generation limits or the absence thereof, and report the hint token overhead separately.

## Score
**Final Score: 6/10**

**Rationale.** The score is based on the following evidence-grounded assessment:

- **Research Value & Novelty (7/10):** The in-reasoning intervention paradigm is genuinely novel and well-motivated. The idea of conditioning on hints during generation is orthogonal to prior work and has practical value. However, the novelty claim is slightly softened by insufficient differentiation from early-exit methods (W4). The ConciseHint-T extension is a useful addition but trained only on one domain.

- **Experimental Soundness (5/10):** The core experiments are carefully executed across multiple models and baselines, and the ablation studies are convincing. However, the absence of variance reporting and significance tests (W2) is a significant gap that undermines statistical claims. The transition word analysis lacks causal validation (W7). The ConciseHint-T training procedure has unresolved methodological questions (W3).

- **Methodological Rigor (5/10):** The adaptive interval mechanism is well-motivated but has an unexamined positive-feedback dynamic (W1). The position selection formula uses ad-hoc constants without sensitivity analysis (W5). The algorithm pseudocode is helpful but missing details about training configuration.

- **Writing & Presentation (6/10):** The paper is generally clear and well-structured. The introduction has a grammatical issue in the opening sentence. The conclusion lacks limitations (W6), which is a significant omission for a methods paper. The Related Work section needs better positioning against the most relevant baselines.

- **Reproducibility (7/10):** The core method is straightforward to implement from Algorithm 1 and the fixed hyperparameters. However, missing details about ConciseHint-T training and decoding parameters (W8) reduce full reproducibility.

The weaknesses identified are fixable with moderate revisions. The most critical revisions are: adding variance/statistics (W2), addressing the positive feedback loop (W1), disclosing limitations (W6), and clarifying the ConciseHint-T training details (W3).