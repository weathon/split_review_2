## Summary

This paper proposes Motion-R1, a framework that applies GRPO (inspired by DeepSeek-R1) with JS-divergence regularization to fine-tune LLMs for generating motion descriptions from multi-turn dialogue inputs. The authors construct a Motion2Motion dataset of 7,132 text-to-motion dialogue samples with ERA-CoT annotations and describe a low-level RL-based kinematic optimization component. The main experiments evaluate text outputs (action descriptions, skill labels) using text metrics against LLM baselines, with a single qualitative comparison against Anyskill in simulation.

## Strengths

- **Identifies a genuine gap in text-to-motion research**: The paper correctly notes that existing methods handle single-turn commands and largely ignore multi-turn dialogue context or implicit user intent (Section 1, lines 13–15). This is a real limitation worth addressing.
- **Conceptually interesting application of GRPO to motion-related tasks**: Drawing inspiration from DeepSeek-R1's GRPO paradigm for LLM reasoning and applying it to motion description generation is a novel direction. The replacement of KL with JS divergence (Section 3.2.1, lines 145–151) is a reasonable technical variation with a stated motivation (symmetry, gradient stabilization).
- **Motion2Motion dataset with ERA-CoT annotations**: Constructing a dedicated dialogue-to-motion dataset with structured entity-relationship annotations (Section 3.1) is a potentially useful resource contribution, assuming public release.

## Weaknesses

### Fatal

- **The central claim ("motion generation with physical consistency") is not supported by the evaluation.** The title, abstract, and introduction frame the paper as a motion generation system. Yet the main experiments (Sections 4.1, 4.2, 4.3) evaluate only **text outputs**—action descriptions and skill labels—using text-to-text metrics (Semantic Similarity, Keyword Matching Rate, Information Completeness, Jaccard similarity, and GPT-4 judging the rationality/relevance of text). Standard text-to-motion metrics (FID, R-precision, diversity, foot skating ratio, penetration depth) are never reported. The Low-Level Kinematic Optimization component (Section 3.3), which is the only part of the pipeline that connects to "motion generation" and "physical consistency," receives no quantitative evaluation whatsoever—no physics violation analysis, no trajectory accuracy metrics. The sole motion-related evidence is Figure 3, a single qualitative comparison with Anyskill lacking any numeric result. This is a fundamental disconnect between what the paper claims to contribute and what it actually measures. The paper could be reframed as a text-generation method for motion descriptions, but as written, the claims are mismatched with the evidence.

### Major

- **Tables 1 and 2 contain suspicious identical/near-identical scores across different models.** In Table 1, Qwen2.5 7B and Llama3.2 8B produce identical scores across all four metrics (SS=0.0330, KMR=0.1186, IC=0.1287, CPS=0.0616). These are different model families of similar size; identical results are not plausible and strongly suggest a data handling or reporting error. Additionally, larger models (7B/8B) score dramatically worse than smaller ones (3B), which is unexplained. Since these are the only quantitative baselines, this undermines the entire comparison.

- **The GRPO clipping equation (Eq. 3) is incorrectly specified.** The paper writes: `min(π_θ/π_θ_old, 1-ε, 1+ε) * A_i`. The standard PPO/GRPO clipping is `min(ratio * A, clip(ratio, 1-ε, 1+ε) * A)`. As written, `min(ratio, 1-ε, 1+ε)` reduces to a one-sided truncation at `1-ε` whenever `ratio > 1-ε`, losing the upper clipping bound. This either reflects a mathematical error or a typesetting mistake that makes the objective non-functional as intended.

- **GPT-4 evaluation table has inconsistent percentage sums and undefined model variants.** In the rationality table (Figure 4a), Omni3.0 sums to 110.0% (94.1+4.0+11.9) and Formal3.0 sums to 101.6% (82.3+4.4+14.9). In the relevance table (Figure 4b), Formal3.0 sums to 60.1% (49.7+1.2+9.2) and Omni3.0 to 87.3% (83.0+4.3+0.0). The model variants "Formal3.0," "Formal3.0B," "Formal3.0B+," "Omni3.0" are never defined in the paper.

- **The main quantitative comparisons (Tables 1, 2) do not include standard text-to-motion baselines.** The paper compares a fine-tuned Qwen2.5-3B against non-fine-tuned Qwen2.5 and Llama3.2 models—general-purpose LLMs not designed for motion tasks. Standard T2M baselines (MDM, MLD, T2M-GPT, MotionGPT, AvatarGPT) are cited in the related work but never used as comparators. The sole motion comparison (Figure 3 against Anyskill) is purely qualitative with no metrics.

### Minor

- **Absolute performance is very low.** The best model achieves Jaccard similarity of only 0.0616 on skill generation (Table 2) and CPS of 0.2176 on action generation (Table 1). These scores indicate very poor absolute performance, raising questions about practical utility even for the text-generation subtask.
- **No variance or statistical significance reported.** All tables report single-point estimates without standard deviations or significance tests, making it impossible to assess whether observed differences (e.g., JS 0.2176 vs KL 0.2117) are meaningful.
- **The "hierarchical attention mechanism" is mentioned once (line 131) but never described.** No architecture, equations, or experiments demonstrate this claimed innovation.
- **The dataset size (7,132 samples) is modest for fine-tuning even a 3B LLM with RL.** The construction methodology lacks key validation details (inter-annotator agreement, validation statistics).

### Trivial

None beyond those already covered above.

## Nice-to-Haves

- If the paper were reframed as a method for improving action/skill **text descriptions** via GRPO+JS (dropping the motion generation claims), the experiments would match the framing and the contribution would be clearer.
- Releasing the Motion2Motion dataset would strengthen the resource contribution.
- An ablation study separating the effects of the dataset, the GRPO+JS training, and the low-level optimization would clarify which components drive improvement.
- Reporting standard deviations or confidence intervals for all metrics would improve reproducibility assessment.

## Removed Points

These points from the input review were removed per filtering rules:

- **Criticism about the GSM8K experiment being relegated to an appendix**: Removed per rule (appendix content is stripped by the parser; the paper states this content exists in the appendix).
- **Criticism about "Code will be released" not mentioning dataset release**: Removed per rule about not questioning the release status/availability of resources cited or described in the paper.
- **Claim of "no simulation results"**: Slightly overstates—Figure 3 does show a simulated environment with a robot character. The retained criticism about lack of *quantitative* motion evaluation is the correct framing.
- **Criticism about Section 2.3 being too broad/unfocused**: Subjective editorial judgment, not a substantive technical weakness.
- **Criticism about the Anyskill comparison lacking specificity in the figure caption**: This is a minor presentation issue that does not affect the core assessment.
- **Complaint that the paper "does not mention releasing the Motion2Motion dataset"**: Removed per the rule about not questioning release status; noted as a nice-to-have instead.
- **Criticism about "no analysis experiments" for contribution 1**: The contribution claim about "systematically analyzing the effects of semantic ambiguity" is somewhat overblown, but this is subsumed by the fatal claim-evidence mismatch weakness.

## Novel Insights

The reviews collectively highlight a critical observation that goes beyond the paper itself: when the GRPO/RL-fine-tuning paradigm is transferred from a reasoning domain (mathematics/logic, where output quality is directly measurable via correctness) to a generation domain (motion descriptions, where quality is subjective and multi-faceted), the evaluation becomes the central challenge. The paper inherits the RL methodology without inheriting the evaluation methodology that makes it rigorous in its source domain, leading to a situation where the proxy task (text generation) is evaluated thoroughly while the claimed target task (motion generation) is not. This observation underscores a broader risk in "X meets LLMs" research: borrowing a method's framework without its validation standards can produce papers with strong conceptual hooks but weak empirical foundations.

## Suggestions

1. **Reframe the paper honestly.** Either acknowledge that the contribution is about improving text-based action/skill description generation (matching the actual experiments), or add proper motion evaluation (FID, R-precision, diversity, physics violation metrics, comparison against actual T2M models like MDM, MLD, MotionGPT).
2. **Investigate and correct the suspicious identical scores** in Tables 1 and 2. Explain why larger models score worse than smaller ones.
3. **Fix the GRPO equation (Eq. 3)** to match the standard clipping formulation, or explain the intended variant.
4. **Define all model variants** (Formal3.0, Formal3.0B, Formal3.0B+, Omni3.0) and ensure percentage sums are consistent.
5. **Provide quantitative results for the low-level kinematic optimization component** if it is to remain part of the claimed contribution.
6. **Report variance/confidence intervals** for all metrics.

## Score and Decision

**Anchors consulted for calibration:**

| Paper (path) | Avg Score | Round | Comparison |
|---|---|---|---|
| 8QTpYC4smR (LLM survey) | 1.00 | 1 | A literature survey with no technical contribution; our paper has more substance |
| OZ3NXrF3gQ (RFPO) | 2.50 | 1 | Creative RL method but simple maze-only eval; our paper has a more serious claim-evidence mismatch |
| oyXoGJQlUf (GRAIL) | 3.00 | 1 | Reasonable LLM+robotics pipeline but limited eval; our paper has data integrity issues theirs lacks |
| VRRuYBaq9u (GPO) | 3.25 | Narrow | Policy optimization with overlap to prior work; still has proper benchmark eval |
| SXMTK2eltf (GPT-Driver) | 5.00 | 1 | LLM driving planner with actual nuScenes evaluation; clearly stronger than our paper |
| 80faVLl6ji (Kinematic Phrases) | 6.00 | 1 | Motion paper with actual motion metrics and T2M baselines; far stronger evaluation |

**Round 1 bracket:** 2.0–3.0 (below the 3.25–5.0 papers due to fatal claim-evidence mismatch and data integrity concerns)

**Final score determination:** The paper's fatal weakness (claiming motion generation with physical consistency while evaluating only text outputs), combined with data integrity red flags (identical cross-model scores, percentages not summing to 100%, undefined model variants) and a mathematically incorrect core equation, places it decisively in the reject range. However, the paper does have some technical substance (novel application of GRPO+JS, a new dataset, the conceptual pipeline) that separates it from the score-1.0 papers. Score **2.0** reflects a strong reject with interesting ideas undermined by fundamental evaluation and reporting problems.

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>