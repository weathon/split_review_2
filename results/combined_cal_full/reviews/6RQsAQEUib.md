## Summary

This paper introduces GHPO (Guided Hybrid Policy Optimization), a difficulty-aware RL framework that addresses reward sparsity in on-policy RLVR (Reinforcement Learning with Verifiable Rewards) for LLM reasoning. When GRPO generates all-zero-reward responses for a query (all G samples are incorrect), the advantage becomes zero and no learning signal propagates. GHPO detects this condition by checking whether all group rewards are zero and, when it occurs, provides partial ground-truth solution traces as guidance — effectively switching from pure RL to guided imitation learning for difficult queries. The method reuses GRPO's group reward statistics for detection, adding negligible overhead. Experiments on six math benchmarks with two Qwen2.5 base models (7B and Math-7B) show consistent improvements over GRPO and curriculum-learning baselines.

## Strengths

- **Clearly identified and well-motivated problem (Section 2.3):** The paper precisely diagnoses reward sparsity in on-policy RLVR — when all G responses for a query yield zero reward, GRPO's advantage estimate collapses to zero. The empirical verification showing Qwen2.5-7B-Instruct fails 52% of NuminaMath-1.5 grounds this concern in real data rather than speculation.

- **Practical difficulty detection with negligible overhead (Section 3.3):** The mechanism reuses group reward statistics already computed by GRPO (all-zero reward → difficult query), requiring no auxiliary model, separate classifier, or additional LLM calls. This is a sensible design for resource-efficient fine-tuning.

- **Consistent empirical gains across settings (Tables 1–2):** GHPO outperforms GRPO on almost every individual benchmark across two training datasets (Math3to5, NuminaMath-S) and two base models (Qwen2.5-Base-7B, Qwen2.5-Math-7B). Improvements like +10 pp on AMC23 and +8.6 pp on GPQA-Diamond (Table 1) are individually noteworthy. The gains persist when moving from a general base model to a math-specialized one.

- **Training dynamics analysis provides supporting evidence (Figure 4):** The comparison of gradient norm curves — GHPO maintains smaller, stabler gradients than GRPO — offers mechanistic support for the claimed training stability benefit, going beyond final accuracy numbers.

## Weaknesses

### Major

- **Missing ablation that directly tests the core claim.** The paper's central claim is that GHPO's *adaptive* difficulty detection and guidance produces the gains. However, there is no comparison to a simple baseline: GRPO + always-on hints (providing partial traces for *every* problem, not only detected-difficult ones). The existing baseline GRPO-CL-H(0.5) uses a static pre-split of the dataset and fixed 50% hints on pre-labeled difficult problems — a fundamentally different approach that does not isolate the effect of adaptivity. If GRPO + always-on hints also matches GHPO, then adaptivity is unnecessary — the gains come from the traces themselves. If always-on hints underperform GHPO, the adaptive mechanism is validated. This ablation is the cleanest test of the paper's claimed innovation — without it, the attribution of gains to the adaptive mechanism remains unsubstantiated.

- **Missing DAPO comparison.** DAPO (Yu et al., 2025) is discussed in the related work (Section 5) as a method that also addresses reward sparsity in zero-RL training — but through filtering (discarding too-easy/too-hard prompts) rather than guidance. Despite being the most directly related competitor targeting the same problem with a conceptually different approach, it is never compared against experimentally. This omission weakens the claim of outperforming "state-of-the-art RL methods."

### Minor

- **No statistical significance or variance reporting.** Results in Tables 1 and 2 are single numbers with no confidence intervals, multiple seeds, or variance measures. LLM RL training is known to be high-variance, and some comparisons are close (e.g., Math-500 in Table 2: GRPO 0.774 vs GHPO 0.776; OlympiadBench: GRPO-CL 0.395 vs GHPO 0.389 — in the opposite direction). While single-run evaluation is common practice in this subfield, the complete absence of any variance estimate limits confidence, particularly for smaller-margin comparisons.

- **Limited generalization evaluation.** The generalization experiment (Section 4.3) tests only one additional base model (Qwen2.5-Math-7B), which is from the same model family. Testing on a different model family (e.g., Llama) or a genuinely smaller model (e.g., Qwen2.5-1.5B, where the paper claims the problem is "particularly acute") would substantially strengthen claims of robustness.

- **Naming inconsistency for a baseline.** The baseline that combines fixed hints with curriculum learning is called "Qwen2.5-7B-GHPO-CL-H0.5" in the text (line 189) but "Qwen2.5-7B-GRPO-CL-H(0.5)" in Table 2. This makes it unclear whether the base algorithm is GRPO or GHPO.

- **Underspecified key hyperparameters.** (a) The group size G is never given a numerical value in the main text, yet the difficulty detection depends entirely on examining G responses per query. (b) The cold-start N=20 steps (Section 3.5) is stated without justification or sensitivity analysis.

### Trivial

- Equation (2) uses ∑_{i=1}^n f(a, o_i) where n appears to mean the group size G, but the paper consistently uses G elsewhere. Minor notation inconsistency.
- The volatility in Figure 3 (difficulty detection proportion oscillating between ~0.2 and ~0.9) is not discussed. While not necessarily a problem, this fluctuation merits some explanation relative to the "smooth learning curriculum" claim.
- The abstract claims "approximately 5%" average improvement, but the clearest reported number is 4.4% (Table 1), and Mixed dataset results show 3.3–3.5 pp. Minor rounding upward.

## Nice-to-Haves

- Testing on a genuinely small model (e.g., Qwen2.5-1.5B) would directly support the stated motivation about capacity-constrained on-device models.
- A comparison of training wall-clock time or FLOPs between GHPO and GRPO would help assess the practical trade-off, since inserting solution traces increases prompt length for difficult queries.
- Sensitivity analysis for the cold-start N value and the group size G.

## Removed Points

*These points were flagged and removed per meta-reviewer rules; treat with caution.*

1. **"Multi-stage ω schedule is underspecified because it is only in the appendix"** — Removed per rule: the parser strips appendix sections from all papers; the original submission includes them.
2. **"Trace-memorization concern from increasing ω"** — Speculative; the ω schedule is available in the appendix of the original submission and cannot be verified from the main text alone.
3. **"GRPO baseline may be underpowered compared to other implementations"** — Speculative claim referencing unreported third-party implementations, not verifiable from the paper.
4. **"Assumption 1 is not an assumption but a hypothesis"** — Semantic framing quibble that does not affect method soundness.
5. **"No discussion of computational cost"** — A helpful addition but not a weakness of the current results; moved to Nice-to-Haves.
6. **"DAPO discussed but not contrasted conceptually"** — The paper does contrast DAPO's filtering approach as data-inefficient versus GHPO's full-data approach (Section 5, last paragraph). The missing *experimental* comparison is already kept as a Major weakness.

## Novel Insights

None beyond the paper's own contributions. The review surfaces standard methodological concerns (missing ablation, missing baseline, no variance reporting) but does not identify structural flaws or alternative interpretations that the paper overlooks. The reviews correctly identify that the central claim about adaptivity needs a cleaner test, but this is a call for stronger evidence, not a discovery of a flaw in the method itself.

## Suggestions

1. **Add the key ablation**: Train GRPO + always-on hints (provide partial traces for *every* problem) and compare to GHPO. This directly tests whether the adaptive detection mechanism is essential or merely incidental.
2. **Add DAPO as an experimental baseline**, since it directly targets the same reward-sparsity problem via a different mechanism (filtering vs. guidance).
3. **Report results from at least 3 random seeds** with means and standard deviations, particularly for benchmarks with small differences (Math-500, OlympiadBench).
4. **Clarify the naming** of the GRPO-CL-H(0.5) / GHPO-CL-H0.5 baseline.
5. **State the numerical value of G** and provide sensitivity analysis for cold-start N.

## Score and Decision

**Score:** 5.5  
**Decision:** Borderline Accept

**Calibration grounding:** All anchors retrieved across rounds are listed below. The final score of 5.5 is grounded in the weighted-item comparison between this paper's draft and the anchors.

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| KL Divergence Opt. for GFlowNets | Uj0h13lVrR.md | 1.00 | 1 | No | Unrelated topic, clear reject |
| Systematic Review of LLMs | 8QTpYC4smR.md | 1.00 | 1 | No | Survey paper, no novel contribution |
| Jailbreaking with CoT | 5kMwiMnUip.md | 1.40 | 1 | No | Different topic |
| LanGoal | hCfhfwSfCg.md | 2.00 | 1 | No | RL + LLM guidance in sparse-reward envs; gaps in evaluation |
| LLIT for Continual RL | zEhTnQZB3D.md | 2.33 | 1 | No | Similar theme but different setting |
| SPO (listwise rewards) | 28TLorTMnP.md | 2.50 | 1 | No | LLM alignment, not RLVR |
| Guided RL with Roll-Back | 5s1qpjrNvZ.md | 3.00 | 1 | No | RL guidance, but not LLM-specific |
| SparsitySolver | zZU69H8tcr.md | 3.75 | 1 | No | LLM pruning, different domain |
| IHAC (Imitation + HRL) | 6y00rooi7i.md | **4.75** | 1 | **Yes** | RL+LLM guidance; this paper is stronger — cleaner method, real benchmarks, no fundamental novelty concerns. |
| SparsePO | YOrN9vNrqo.md | 5.00 | 1 | No | LLM alignment via token masks |
| LLMs Are In-Context RL | YW79lAHBUF.md | 3.75 | 1 | No | Different framing (ICRL) |
| **On Designing Effective RL Reward...** | F0GNv13ojF.md | **5.17** | 2 | **Yes** | Closest topic (RL reward for LLM math reasoning); this paper has less extreme negatives (-4.67 vs -10.27) but also less extensive experiments. |
| **VerifierQ** | OD9pwKQzXl.md | **5.25** | 2 | **Yes** | RL verifier for LLM reasoning; this paper is stronger — results are sufficient and presentation is clearer. |
| MathError | ma4SUzeCLR.md | 5.33 | 2 | No | Math word problem detection, different task |
| COPRA (theorem proving) | XCMbagV0No.md | 5.00 | 2 | No | Theorem proving with LLM agents |
| Hint Marginalization | DzKdjWe59v.md | 5.75 | 2 | No | Uses hints at inference time, not training |
| TPO (Tree Preference Opt.) | O0sQ9CPzai.md | **6.33** | 2 | No | LLM math reasoning with DPO; stronger evidence base and more thorough evaluation |
| Step-Controlled DPO | ZRDa2IT1sQ.md | 6.00 | 2 | No | Math reasoning with stepwise DPO |
| LBS3 (curriculum learning) | ixoIAOcTSx.md | 5.67 | 2 | No | CoT prompting, not RL training |
| ProgressCounts | lvDHfy169r.md | **5.75** | 1 | **Yes** | LLM reward generation; similar quality — good motivation and results but doubt about significance |
| ORSO | 0uRc3CfJIQ.md | **5.83** | 1 | **Yes** | Reward design for RL; well-written with thorough experiments |
| WizardMath | mMPMHWOdOy.md | **8.00** | 1 | **Yes** | Math reasoning with RL; much stronger results across model scales, comprehensive baselines |

**Why 5.5 specifically:** The paper's strongest positive items (consistent gains +4.75, practical mechanism +4.59, training dynamics +3.58) are genuine and substantial. However, the most negative item (-4.67 for missing DAPO comparison) and the missing ablation for the core claim (-2.60) are significant gaps that keep it from being a clear accept. The paper is above the 4.75 anchor (which had fundamental novelty concerns) and comparable to the 5.17–5.75 anchors, but below the 6.33 (TPO) and 8.00 (WizardMath) anchors which had stronger evidence and more thorough evaluations. A score of 5.5 reflects a borderline accept — the method is sound and results are consistently positive, but the evidence base needs strengthening on the central claim before it can be considered a clear contribution.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>