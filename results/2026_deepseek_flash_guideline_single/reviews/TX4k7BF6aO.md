Now let me write the final consolidated review.

## Summary

This paper proposes ARPO (Agentic Reinforced Policy Optimization), an RL algorithm for training multi-turn LLM agents that interact with external tools (search, code interpreter, web browser). The key idea is to branch rollouts at high-entropy token positions following tool-call feedback, replacing trajectory-level sampling with step-level adaptive exploration. ARPO also introduces an advantage attribution estimation (hard vs. soft) to handle the shared/divergent token structure created by branching. Evaluated across 13 benchmarks and two backbone families, ARPO shows consistent gains over GRPO, DAPO, and REINFORCE++ and claims reduced tool-use budget during training.

## Strengths

1. **Empirically grounded motivation (§2).** The paper identifies a real, measurable phenomenon: token-level entropy spikes sharply in the first 10–50 tokens after each tool call. This observation is independent of ARPO itself and cleanly motivates why trajectory-level rollouts may be suboptimal for agentic settings. The pilot experiment distinguishing search vs. Python feedback adds useful nuance.

2. **Broad and systematic evaluation (Tables 1, 2).** ARPO is tested across 13 datasets spanning math reasoning (AIME, MATH, GSM8K), knowledge-intensive QA (HotpotQA, 2WikiMultihopQA, MuSiQue, Bamboogle), and deep search (GAIA, WebWalker, HLE, xBench), using Qwen2.5-7B, Llama3.1-8B, Qwen3-8B/14B — two backbone families. The consistent positive trend across settings strengthens the case that the method provides a real benefit.

3. **Sample efficiency in deep search (§5.1).** Training with only 1k RL samples on deep search tasks (Qwen3-14B achieving 43.7% on GAIA) is noteworthy and suggests the method makes effective use of limited experience.

## Weaknesses

### Fatal
None.

### Major

1. **No ablation isolates the core mechanism.** ARPO bundles two novel components: (a) entropy-based adaptive branching and (b) advantage attribution estimation. The only ablation (Figure 5) compares hard vs. soft advantage, but both use the same entropy-based branching. There is no experiment that compares:
   - GRPO vs. GRPO + branching (without advantage attribution)
   - ARPO with entropy-based branching vs. ARPO with random branching at a matched rate
   - ARPO vs. a trajectory-level baseline with matched total trajectory count
   
   Without these controls, the central claim — that *entropy-guided* step-level exploration is responsible for the improvement — is not directly tested. The gains could come from the increased effective sample size, the branching structure itself, or the advantage attribution, rather than the entropy guidance.

2. **Statistical significance is absent; several comparisons are essentially tied (Table 1).** All results are single point estimates with no variance estimation. Multiple cells in Table 1 show negligible or negative differences: Qwen2.5-7B on MATH (ARPO 88.8 vs. Reinforce++ 88.8, identical), GSM8K (ARPO 92.2 vs. GRPO 92.8, ARPO lower). Without multiple seeds, confidence intervals, or any measure of variability, it is impossible to assess which differences reflect genuine improvement and which are noise. The claimed 4% average gain is computed from these point estimates.

3. **The "half the tool-use budget" claim is overstated and insufficiently supported (Figure 7a).** The efficiency comparison shows ARPO using ~250–300 calls vs. GRPO ~400–450 — about 55–67%, not 50%. This is against a single baseline (GRPO) on a single model (Qwen2.5-7B), with no data for larger models (8B/14B) or against DAPO/REINFORCE++. The abstract and conclusion's claim of "only half the tool-use budget" exceeds what the evidence supports.

4. **Entropy-based branching hyperparameters are underspecified in the main text (§3.1).** The core decision rule (Eq. 2) uses α (base sampling probability), β (stability entropy), threshold τ, monitored token count k, and branching count Z. The paper never states the numeric values used or how they were chosen. While the appendix (stripped from the review copy) likely contains these details, the main text should state default values and ideally a sensitivity analysis.

### Minor

1. **The "Generalized Policy Gradient Theorem" (§3.3) is oversold.** Equation (6) restates that the policy gradient theorem applies when actions are macro-level segments rather than individual tokens. This is a standard result — policy gradients are agnostic to action granularity. Presenting this as a distinct "GPG Theorem" that provides ARPO's "robust theoretical foundation" gives a misleading impression of theoretical novelty. The theorem does not constrain the algorithm's specific design choices (entropy thresholds, branching criteria, advantage attribution).

2. **LLM-as-Judge from the same model family.** Evaluations use Qwen2.5-72B-instruct as the judge for all non-F1 tasks. Since the trained models are also from the Qwen family, there is a risk that the judge favors stylistic patterns produced by Qwen-family models. The 72B judge is much larger than the trained models (7–14B), which mitigates this, but it remains a concern.

3. **Mathematical reasoning tasks may not cleanly test the entropy motivation.** Math tasks (AIME, MATH, GSM8K) primarily use the code interpreter, not search. The paper's own §2 finding (Ob.3) is that "Search feedback introduces more uncertainty than Python feedback." If the entropy spikes motivating ARPO are smaller for Python feedback, the mechanism's relevance to these tasks is less directly supported. The paper does not break down results by tool type.

### Trivial
None.

## Nice-to-Haves
- Reporting wall-clock training time or FLOPs (entropy computation requires a full softmax over the vocabulary at each monitored position).
- Inference-time tool-call efficiency comparisons in addition to training-time.
- Clarification of the ΔH normalization in Eq. (2) — summing over k tokens then dividing by vocabulary size V is an unusual choice that warrants additional explanation.
- Breakdown of results by tool-use type (search vs. Python vs. browser).

## Removed Points

These points were raised by the harsh critic but are removed from the main review with justification:

- **Reproducibility based on missing appendix content.** The criticism that hyperparameters are "underspecified to the point of non-reproducibility" was softened because the appendix (which the parser stripped) likely contains specification details. The remaining criticism (Weakness #4 in Major) is about main-text underspecification, not appendix absence.
- **Unfair comparison with prompting methods.** The comparison between TIR Prompting (zero-shot) and RL methods (trained) is presented as a finding about prompting's limitations, not as a head-to-head competition. This is a reasonable negative result, not a methodological flaw.
- **Missing related works, missing proofs, formatting nitpicks.** Removed per policy (parser strips these; no external verification possible; parser artifacts, not author errors).
- **Speculative concerns about confounds in the evaluation.** The reviewer's speculation about the LLM-as-Judge favoring Qwen outputs was kept in weakened form (Minor #2); the more extreme framing was removed.

## Novel Insights

None beyond the paper's own contributions. The reviews highlight a useful diagnostic perspective: the paper's empirical scope is commendably broad (13 datasets, two backbones), but this breadth comes at the cost of depth in isolating what actually drives the reported improvements. The entropy-motivation observation (§2) is the cleanest part of the paper and could be valuable even as a standalone finding. The main methodological gap — whether entropy guidance, branching structure, or increased sample count causes the improvement — is a straightforward ablation study away from being resolved.

## Suggestions

1. **Add ablations to isolate the core mechanism.** Compare: (a) GRPO vs. GRPO + branching (without advantage attribution) to measure the branching effect alone; (b) ARPO with entropy-guided branching vs. ARPO with random branching at the same rate to test whether entropy guidance matters; (c) ARPO vs. trajectory-level RL with matched total trajectory count to rule out the "more samples" confound.

2. **Report statistical significance.** Run each experimental condition with at least 3 random seeds and report mean ± std or confidence intervals. This would immediately clarify which differences in Table 1 are meaningful.

3. **Correct the efficiency claim.** Specify the actual reduction ratio (~35–45% based on Fig. 7a, not "half") and expand the comparison to include at least one additional model size (e.g., Qwen3-8B) and one additional baseline (DAPO or REINFORCE++).

4. **State hyperparameter defaults.** Report the values of α, β, τ, k, and Z used across all experiments, ideally with a sensitivity analysis showing how ARPO's performance varies with these choices.

## Score and Decision

**Bracket determination (Round 1):** Topically similar calibration papers span from 5.5 (StepTool, a step-grained RL method for tool learning — rejected, with concerns about missing ablations) to 6.67 (ARMAP, an agentic reward modeling framework — accepted, with broader scope but simpler environments). The ARPO paper is empirically broader than StepTool but shares its weakness of insufficient ablation. This places the paper in the 5.5–6.5 range.

**Calibration anchors inspected:**

| Anchor Paper | Avg Score | Comparison to ARPO |
|---|---|---|
| StepTool (step-grained RL for tool learning) | 5.50 | Very topically similar; ARPO has broader eval but similar ablation gaps |
| Entropic Activation Steering (entropy for LLM agents) | 4.75 | Narrower experiments (simple 2-arm bandit); ARPO is stronger empirically |
| ARMAP (automatic reward modeling for agents) | 6.67 | Broader framework but simpler environments; ARPO has comparable scope |
| TWOSOME (RL for LLM in embodied environments) | 6.00 | Similar profile — novel framework, solid eval, some methodological concerns |
| TPO (tree preference optimization for LLMs) | 6.33 | Topically related (tree-structured sampling); stronger on ablations |

**Narrowing (Round 2):** Comparing against closely matched papers, ARPO's empirical breadth (13 datasets, two backbones) exceeds StepTool (5.5) and is comparable to TWOSOME (6.0) and TPO (6.33). However, the missing ablations and lack of statistical rigor are more severe in ARPO than in the 6+ papers. The core idea is genuinely novel and well-motivated, and the broad evaluation provides evidence that ARPO works, but the paper does not yet demonstrate *why* it works.

**Final score: 6.0.** The paper presents a novel and well-motivated algorithm with an unusually broad empirical evaluation. The entropy-based branching idea is clean and the consistent positive results across 13 datasets are encouraging. However, the lack of ablations isolating the mechanism, the absence of statistical significance measures, and the overstated efficiency claim are significant weaknesses that prevent a stronger score. These are addressable in a major revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>