## Summary

Motion-R1 proposes a three-component framework for text-to-motion generation: (1) the Motion2Motion dataset of 7,132 text-to-motion dialogues annotated with ERA-CoT reasoning chains, (2) an enhanced GRPO training algorithm that replaces KL-divergence with JS-divergence for generating motion descriptions, and (3) a low-level RL-based kinematic optimization policy for producing physically plausible motion trajectories. The paper evaluates only the text generation component, not the motion generation pipeline it claims to deliver.

## Strengths

- **JS-divergence consistently outperforms KL-divergence in GRPO across all seven reported metrics (Tables 1–2).** The JS-regularized variant beats the KL variant on every metric for both action generation (SS 0.2178 vs. 0.2111) and skill generation (Jaccard 0.0616 vs. 0.0531), with relative improvements of 2.4–16%. This is a clear and internally consistent empirical result within the paper's own evaluation setup.

- **First application of the R1/GRPO reasoning paradigm to the motion domain, supported by a structured dataset.** The paper identifies two specific barriers to applying GRPO to motion synthesis — lack of a motion-reasoning dataset and lack of motion reasoning abilities (Abstract, Section 1) — and addresses them with the Motion2Motion dataset (7,132 samples) and the ERA-CoT annotation framework.

## Weaknesses

### Fatal

None that are speculative. The fatal issue below is verifiable from the paper as written.

### Major

- **The paper's central claim — physically consistent motion generation — is not evaluated.** The title, abstract, and introduction consistently frame Motion-R1 as a motion generation system that produces "contextually appropriate, lifelike motions" and "physically consistent latent-intent motion generation" (lines 5–9). Yet every quantitative experiment (Tables 1, 2, and the GPT-4-as-judge evaluation in Section 4.3) evaluates only **text generation quality**: Semantic Similarity, Keyword Matching Rate, Information Completeness, Jaccard similarity, Precision, Recall, and GPT-4-assessed rationality/relevance of generated text. There are zero motion-specific metrics — no FID, no diversity, no foot skating, no penetration, no joint-limit violations, no physics plausibility scores. The "low-level kinematic and dynamic optimization" (Section 3.3), presented as the component that "translates GRPO-generated motion descriptions into executable policies" and "ensures physical realizability in simulation environments" (lines 75, 187–189), is described mathematically (Eqs. 11–14) but never evaluated — no ablation, no quantitative results, no demonstration that it produces valid motion trajectories. The sole motion-related result is a qualitative comparison with Anyskill (Figure 3), which is framed as a test of whether the model can "understand long text" (line 261), not as a measure of motion quality. The abstract's assertion that "Motion-R1 delivers contextually appropriate, lifelike motions" is unsupported by any experiment in the paper.

- **Section 4.3 uses undefined model names, making the GPT-4-as-judge evaluation uninterpretable.** The table in Section 4.3 (lines 283–295) lists models named "Formal3.0," "Formal3.0B," "Formal3.0B+," and "Omni3.0" — none of which are defined anywhere in the paper (not in the method description, not in related work, not in the experimental setup). The rows compare "Our Model" against "Other Models" and "Human" for each of these four unidentifiable variants. It is impossible to determine what these variants are, what "Other Models" refers to, or how this evaluation relates to the proposed Motion-R1 framework.

- **Suspicious baseline numbers in Table 1.** Larger models perform dramatically worse than smaller variants of the same family (Qwen2.5 7B: SS=0.0330 vs. Qwen2.5 3B: SS=0.1701; a 5× drop in the wrong direction). More critically, **Qwen2.5 7B and Llama3.2 8B report identical values across all four metrics** (SS=0.0330, KMR=0.1186, IC=0.1287, CPS=0.0616). This exact match across different model families strongly suggests a systematic error (e.g., a failure to run inference on the larger models, with placeholder values used instead). This undermines the quantitative comparisons that the paper relies on to demonstrate improvement.

- **The low-level kinematic optimization (Section 3.3) is entirely disconnected from the experiments.** This component is one of the three claimed contributions (line 53: "We design a reinforcement learning-driven low-level optimization framework that explicitly enforces kinematic feasibility and environmental dynamics"). Despite a detailed mathematical exposition (Eqs. 11–14), there are zero experiments showing it produces valid motion, no ablation of reward weights (w_G, w_S), no comparison to alternative motion synthesis methods, and no motion quality results. The component is asserted but never substantiated.

### Minor

- **Baselines cover only text generation, not motion generation.** Even accepting the paper's framing, the quantitative comparisons are against Qwen2.5 and Llama3.2 — general-purpose LLMs — on text-based metrics. There is no comparison against any existing text-to-motion method (MDM, MLD, MotionGPT, Tender) or physics-based motion synthesis method (AnySkill, physics-based character controllers) for the claimed motion generation component.

- **Low absolute metric values are presented without context or error bars.** The best method (Our (JS)) achieves SS=0.2178, KMR=0.3191, Jaccard=0.0616. These are reported as point estimates without standard deviations, confidence intervals, or significance tests. Without calibrated baselines on these specific metrics, the reader cannot assess whether these scores represent meaningful improvement.

- **The equation in Figure 1 is inconsistent with the main formulation in Eq. 3.** Figure 1 (line 46) shows a KL-based objective with the clipping term `(1 - ε + r)`, while Eq. 3 uses JS-divergence with standard PPO clipping `min(..., 1-ε, 1+ε)`. The relationship between these formulations is not explained, creating confusion about which objective is actually used.

### Trivial

None.

## Nice-to-Haves

- Report standard motion generation metrics (FID, diversity, R-precision, foot skating, penetration) if the low-level optimization actually produces motion trajectories.
- Clarify whether Motion2Motion contains text paired with motion sequences or text paired only with text descriptions of motion. The experiments suggest the latter, but the paper's framing implies the former.
- Add error bars or confidence intervals to all tables.
- Include a limitations section discussing what the approach cannot do.

## Removed Points

These points were raised by reviewers but are excluded from the main review under the filtering rules:

- **"No code or dataset release details beyond 'Code will be released'"** — Removed per Hard Rule: questions about the existence or release status of cited entities are not valid weaknesses. The paper states code will be released.
- **"No discussion of limitations"** — Removed as a generic expectation; the paper does not include this section but this is common in submissions and does not constitute a specific identifiable flaw.
- **"Generic concerns about missing related works"** — Removed per Hard Rule: cannot confirm existence of missing references without external sources.
- **"Weakness about missing appendix/supplementary"** — Removed per Hard Rule: the parser strips these sections; they exist in the original submission.
- **Strength Finder's generic strengths** (e.g., "this paper addresses an important problem") — Removed as generic/superficial.
- **Strength Finder's claim about the low-level optimization as a strength** — Weakened to the point of removal because this component is unevaluated; including it as a strength would conflict with the verified weakness that this component is never tested.
- **Pure formatting nitpicks** — Removed per Hard Rule.

## Novel Insights

The calibration database was unavailable, so no anchor-based comparison was possible. Beyond the paper's own contributions, no novel cross-paper insight emerged from the reviews.

## Suggestions

1. **Reconcile the paper's claims with its evaluation.** Either (a) substantially reframe the paper as a method for generating text descriptions of motion (renaming it to avoid claiming "motion generation" and "physical consistency"), or (b) provide quantitative evaluation of the full pipeline including motion-specific metrics, ablation of the low-level optimization, and comparison against T2M baselines.

2. **Investigate and correct the baseline numbers in Table 1.** The identical values for Qwen2.5 7B and Llama3.2 8B across all four metrics must be explained or corrected. If the larger models could not be evaluated, state this explicitly.

3. **Define all model variants in Section 4.3.** Without definitions for "Formal3.0," "Formal3.0B," "Formal3.0B+," and "Omni3.0," the GPT-4-as-judge evaluation is uninformative.

4. **Resolve the inconsistency between the equation in Figure 1 and Eq. 3**, or add a note explaining that Figure 1 depicts an earlier/ablated variant.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>