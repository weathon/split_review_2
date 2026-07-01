## Summary

Motion-R1 proposes a three-component framework for text-to-motion: (1) a Motion2Motion dataset of 7,132 annotated text-to-motion dialogue samples, (2) an enhanced GRPO algorithm replacing KL-divergence with JS-divergence for motion description generation, and (3) a low-level RL-based kinematic optimization for physically plausible motion execution. The paper claims to generate physically consistent motions by combining LLM-based reasoning with kinematic constraints.

## Strengths

- **Problem framing connects two active research areas.** The motivation — that existing motion generation methods either neglect physical constraints or fail at nuanced semantic understanding — is genuine, and framing it through the DeepSeek-R1 reasoning-paradigm lens is a topical and reasonable connection (Fig. 1, §1).

- **Dataset construction methodology has a reasonable core.** Using GPT-4 for entity extraction with self-consistency validation and ERA-CoT for relationship decomposition (§3.1) is a sensible approach to generating structured annotations from motion dialogues.

## Weaknesses

### Fatal

**1. The experiments evaluate text generation, not motion generation — the paper's central claim is untested.** The title, abstract, and conclusion (line 303: "Experimental results show that Motion-R1 surpasses prior approaches in generating motions that are both semantically coherent and physically plausible") promise a system that generates *physically consistent motions*. However, §4 evaluates only text generation: action description quality via Semantic Similarity, Keyword Matching Rate, Information Completeness, and CPS (Table 1), and skill summary quality via Jaccard, precision, and recall (Table 2). There are **no quantitative metrics for motion output** — no foot skating, penetration depth, joint limit violations, ground contact consistency, or any physical plausibility measure. The low-level kinematic optimization (§3.3) — one of the three claimed contributions — is described but never quantitatively evaluated. The only motion-related result is a single qualitative example in Figure 3 with no comparison metrics or systematic evaluation. This is a structural mismatch between claims and evidence that invalidates the paper's core assertion.

### Major

**2. Baselines are uninformative.** Tables 1 and 2 compare the fine-tuned model against Qwen2.5 and Llama3.2 in their *untuned, pre-trained* forms (§4, line 215: "comparing them with both non-fine-tuned variants"). This only establishes that fine-tuning on domain data improves over the base model — a trivial and expected result. The relevant comparisons (supervised fine-tuning on the same data, standard GRPO with KL on base models, existing motion-language models like MotionGPT) are absent.

**3. GPT-4 evaluation in §4.3 uses undefined model names and has internally inconsistent numbers.** The models evaluated are "Formal3.0," "Formal3.0B," "Formal3.0B+," and "Omni3.0" — none are defined anywhere in the paper. The reader cannot determine whether these are ablations, competing methods, or different configurations. Additionally, the three columns (supposedly a percentage decomposition) are inconsistent: e.g., Formal3.0 rationality sums to 101.6% (82.3+4.4+14.9), Omni3.0 rationality sums to 110.0% (94.1+4.0+11.9), and Formal3.0 relevance sums to only 60.1% (49.7+1.2+9.2).

**4. No ablation studies.** The paper contains no ablation of the dataset size, the JS vs. KL replacement in isolation, the reward components (α, β, γ), or the low-level optimization. The "Our (KL)" result is only reported for the proposed model, not for base models, so it does not cleanly isolate the effect of the JS modification.

**5. No statistical rigor.** Every quantitative result (Tables 1, 2) is a point estimate with no error bars, standard deviations, or confidence intervals across multiple runs or seeds.

**6. The interface between GRPO-generated text and the low-level motion policy is never explained.** Section 3.3 (Eqs. 11–14) describes a standard adversarial imitation learning setup, but never specifies how the textual description from the GRPO model (e.g., "Kick the Door" from Table 3) becomes a goal vector g for the RL policy. This critical bridge between the two claimed contributions is absent.

### Minor

**7. Low absolute performance.** The best Jaccard similarity for skill generation is 0.0616 (Table 2) — approximately 6% token overlap with the reference. Semantic Similarity scores in Table 1 are around 0.2 on a cosine similarity scale of [-1, 1]. These indicate very weak alignment, but the paper presents them without critical discussion.

**8. The JS divergence justification (§3.2.1) describes text formatting, not motion generation.** Line 151 states that JS divergence "enables balanced policy adjustments crucial for structured generation tasks like XML/JSON formatting" and "maintaining strict syntactic compliance — vital for high-precision formatting requirements." This language is about structured text generation and appears adapted from a different context without tailoring to motion. Similarly, the format reward in Eq. (9) rewards XML parse-tree validity — a text-generation concern, not a motion-generation one.

**9. Dataset is small and poorly documented.** At 7,132 samples, the Motion2Motion dataset is small for LLM-based RL training. No train/test splits, dialogue length statistics, inter-annotator agreement, or skill distribution information is provided beyond a word cloud and frequency bar chart (Fig. 2).

**10. Notational issue in Eq. (3).** The expression `min(π_θ/π_θ_old, 1-ε, 1+ε)` is non-standard. The standard PPO/GRPO clipping form is `clip(r_t(θ), 1-ε, 1+ε)` or `min(r(θ)·A, clip(r(θ), 1-ε, 1+ε)·A)`. The three-argument min does not correctly represent the clipping operation.

**11. Multi-turn dialogue claims are not evaluated.** The introduction (§1, line 13) motivates the work by prior methods' failure on "multi-turn dialogue inputs," but the evaluation tasks (action generation, skill extraction) are all single-turn text-to-label tasks. No experiment tests multi-turn dialogue understanding.

## Nice-to-Haves

- Evaluate the full pipeline: text → GRPO-generated description → low-level policy → physics-simulated motion, with standard motion quality metrics (foot skating, penetration, joint limits).
- Include supervised fine-tuning (SFT) and standard GRPO (KL) baselines trained on the same data.
- Provide a clean ablation: train the same model from the same initialization with KL-based vs. JS-based GRPO.
- Clarify what the model names in §4.3 represent.
- Add error bars over multiple seeds.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- The harsh critic's strength about "Problem framing is timely and relevant" was partially generic but had specific elements (DeepSeek-R1 connection, multi-turn focus); kept in a reduced form.
- The harsh critic's claim that the paper "does not evaluate what it claims to build" was verified as fully accurate and elevated to Fatal.
- The harsh critic's criticism about missing appendix (GSM8K) was removed per rules (appendix stripped by parser).
- The harsh critic's claim about the paper "not evaluating motion in a physics simulator" — there is a qualitative example in Figure 3, but this is not a quantitative evaluation. The criticism is accurate.
- No strawman or factually incorrect weaknesses were identified — all criticisms verified against paper text.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's central observation — that the paper claims motion generation but evaluates only text generation — is an error in the paper's conduct, not a novel insight about the subject matter.

## Suggestions

The paper requires a fundamentally restructured experimental section. Specifically: (1) evaluate the full pipeline end-to-end by running the low-level policy in a physics simulator and measuring standard motion quality metrics; (2) compare against existing text-to-motion methods (e.g., MDM, MotionGPT) on motion-level metrics; (3) include proper baselines including SFT on the same data and standard GRPO (KL) on base models; (4) define the goal-vector interface between the GRPO text output and the low-level policy explicitly; (5) clarify or restructure §4.3 to use defined model names and consistent numerical reporting.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR (GFlowNets KL) | 1.0 | R1 | Entirely different topic; strong reject |
| gwZ90hFSL2 (Cross-lingual robotics) | 1.0 | R1 | Entirely different topic; strong reject |
| OZ3NXrF3gQ (Reward-free POMO) | 2.5 | R1 | Evaluates claimed task (maze policies) poorly; this paper is worse due to claim-evidence mismatch |
| Fk4Op9wpEp (Pose-Conditioned ControlNet) | 3.0 | R1 | Evaluates claimed task (pose-conditioned generation) with weak results |
| 5f0n5yi8qK (Video-prompt RL) | 3.4 | R2 | Evaluates claimed task (Minecraft agent) with methodology concerns |
| 30SmPrfBMA (GCML) | 4.75 | R1/R2 | Motion+LLM paper that *generates and evaluates* actual motion sequences |
| 8Rad5LwSv2 (Physics-based Dance RL) | 4.75 | R1 | Motion+RL paper that measures physical plausibility metrics |
| 80faVLl6ji (Kinematic Phrases) | 6.0 | R1 | Motion semantics paper with complete evaluation |
| IEul1M5pyk (HGM³) | 6.0 | R1 | Text-to-motion paper with proper motion evaluation |

**Round 1 bracket:** Score 1.5–3.0. Papers at scores 1.0 are on different/broken topics. Papers at scores 3+ evaluate their claimed task (even if poorly). This paper has a fatal claim-evidence mismatch (claims motion generation, evaluates only text) that is worse than score-3 papers but still has more structure than score-1 papers.

**Final score:** 2.0 within the bracket. The fatal evaluation gap — the central claim of physically consistent motion generation is never tested — places this paper below typical score-3 rejects that at least evaluate their stated task.

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>