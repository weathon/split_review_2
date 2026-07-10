## Summary

This paper systematically ablates the GRPO loss function for training LLMs on mathematical reasoning. Through controlled experiments on 0.5B–1.5B models, it finds that (1) negative feedback via advantage estimation is essential, (2) PPO-style clipping is unnecessary, and (3) group-relative advantage estimation is critical for stability. The paper proposes RGR, which retains group-relative advantage estimation and KL regularization but removes policy ratio clipping.

## Strengths

- **Clear, well-motivated ablation design.** The paper systematically ablates GRPO components (positive-only advantages, removing PPO clipping via RGR, removing advantage estimation via REINFORCE, rejection sampling via RAFT) while keeping other factors fixed, making attributions clean and interpretable. This logical decomposition is the paper's strongest asset. [favorability=14.13]

- **Multi-dimensional evaluation across 9 benchmarks.** Results span English math (GSM8K, MATH, Gaokao2023, OlympiadBench, AMC23), Chinese math (CMATH, CN-Middle-School), and STEM (MMLU-STEM, Gaokao2024), plus training dynamics. This breadth provides reasonable confidence that findings are not benchmark-specific. [favorability=10.92]

- **Core finding extends prior work.** The result that PPO-style clipping is unnecessary when initializing from a pre-trained policy is consistent with and extends Ahmadian et al. (2024) from the RLHF/PPO setting to the GRPO setting — a non-trivial replication that is valuable for practitioners choosing among post-training methods. [favorability=14.77]

## Weaknesses

### Major

- **No variance or uncertainty estimates.** Every result in Tables 1–3 is a single number with no standard deviation, confidence interval, or indication of multiple seeds. The paper claims "RGR outperforms GRPO in 17 out of 27 individual comparisons," yet many margins are tiny (e.g., Llama3.2-1B GSM8K: 43.3 vs 43.0; Llama3.2-1B Gaokao2023-Math-En: 19.0 vs 17.4). Without knowing whether these differences exceed run-to-run noise, the central comparative claim is unsubstantiated. This is especially concerning given the small training set (1,800 instances) and small models (0.5B–1.5B), where variance is likely high. [favorability=-2.21]

### Minor

- **Framing overreach relative to actual ablations.** The title asks whether "complicated loss functions" are necessary and the abstract questions whether "all components" of GRPO are needed. However, KL regularization — a major source of complexity that requires maintaining a reference model of equal size, computing per-token KL divergences, and tuning its own hyperparameter β — is never ablated. RGR still uses KL + reference model. The paper convincingly shows that PPO clipping is unnecessary, but the broader framing implies a more thorough simplification than was actually tested. The findings are narrower than the title and abstract advertise. [favorability=4.00]

- **Limited training scale limits generalizability.** Experiments use 0.5B–1.5B models, 1,800 training examples, and ~70 training steps. The paper acknowledges larger models as future work (line 272), but the core argument — that "clipping is unnecessary because pre-trained LLMs are strong policies" — is less compelling at these tiny scales; a 0.5B instruction-tuned model may not be a "strong policy" in the relevant sense. The practical conclusion about clipping's dispensability would be much better supported by at least one experiment at a larger scale (e.g., 7B+). [favorability=4.28]

- **Countdown behavioral analysis is purely qualitative.** The Countdown dataset evaluation (Figure 2, line 254) presents only one cherry-picked example per condition, with no systematic quantitative metrics (accuracy, response length statistics). A qualitative example cannot support the claimed systematic behavioral differences between methods. [favorability=-2.70]

- **Efficiency claims are unmeasured.** The abstract describes RGR as "more efficient" than GRPO, but the computational cost of PPO-style clipping is negligible. The dominant costs (generating G=8 completions per prompt, maintaining a reference model for KL) are identical between RGR and GRPO. No training time or FLOP measurements are provided. [favorability=0.93]

### Trivial

- **Naming inconsistency.** The method is referred to as "RGR A" (line 125), "RGR" (Tables 1–3), and "RGRA" (conclusion, lines 252, 268). [favorability=2.19]

## Nice-to-Haves

- An ablation of KL regularization itself would make the contribution more complete. Without it, the paper only tests the necessity of one of GRPO's three components.
- Hyperparameter search details (learning rate, β, clipping ε) per method, if not already in the stripped appendix, would improve confidence in fair comparisons.
- Explicit specification of whether the REINFORCE baseline retains KL regularization would help reproducibility.

## Removed Points

- **GRPO formulation difference (KL in loss vs. in reward):** The paper transparently notes this implementation choice (line 77). Not a weakness.
- **Missing "ft" baseline description:** Standard supervised fine-tuning is a well-understood baseline; this omission is minor and not actionable.
- **Hyperparameter tuning parity concern:** The paper refers to Appendix A for full parameters, which was stripped by the parser. Per guidelines, this is not a verifiable weakness.
- **REINFORCE+KL ambiguity:** The paper says REINFORCE with direct rewards "starts from RGR A and removes advantage estimation." Since RGR A (Eq. 2) explicitly includes KL, the specification is clear enough.

## Novel Insights

None beyond the paper's own contributions. The review confirms the core finding (clipping is unnecessary in GRPO for small models) but does not surface new technical insights beyond what the paper itself reports.

## Suggestions

1. **Add variance estimates** (multiple seeds, standard deviations) to all benchmark tables. Without these, the paper's strongest comparative claim ("RGR surpasses GRPO") cannot be evaluated. If differences are within noise, reframe to "RGR matches GRPO while being simpler."
2. **Run at least one experiment at a meaningful scale** (e.g., 7B+ model) to test whether the clipping-is-unnecessary finding holds where the policy initialization is genuinely strong.
3. **Either ablate KL regularization** or adjust the title/framing to accurately reflect that the paper tests the necessity of PPO clipping specifically, not the full complexity of the GRPO loss function.
4. **Supplement the Countdown analysis** with quantitative metrics or remove it.
5. **Remove the unsupported efficiency claim** or back it with timing/FLOP measurements.

## Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Uj0h13lVrR.md | 1.00 | R1 (bracket) | No | Unrelated GFlowNet paper; not comparable |
| 8QTpYC4smR.md | 1.00 | R1 (bracket) | No | Survey paper; not comparable |
| 5kMwiMnUip.md | 1.40 | R1 (bracket) | No | Jailbreaking paper; not comparable |
| gwZ90hFSL2.md | 1.00 | R1 (bracket) | No | Cross-lingual robotics; not comparable |
| ZK1NnjpjEs.md | 3.00 | R1 (bracket) | No | LLM NLU via RL; weaker evaluation |
| 28TLorTMnP.md | 2.50 | R1 (bracket) | No | Soft preference optimization; different focus |
| jOuHjFw71C.md | 3.00 | R1 (bracket) | No | LLM planning evaluation; not comparable |
| vyHFTsOUWu.md | 3.00 | R1 (bracket) | No | Instruction following; different topic |
| **F0GNv13ojF.md** | **5.17** | **R1+R2** | **Yes** | **RL Reward at Training Time: stronger evaluation (7B models) but mixed novelty; similar rejection profile** |
| 6UQaXJm53B.md | 5.25 | R1+R2 | Yes | DfPO: more complex method with theory concerns |
| D9GoWJJxS5.md | 5.00 | R1 (bracket) | No | LLM pruning via policy gradient; different topic |
| **gdzpnRBP4F.md** | **4.50** | **R1+R2** | **Yes** | **RLSF: similar limitation (single small model), comparable evidential quality** |
| fWRBheSJth.md | 6.67 | R1 (bracket) | No | Prompt optimization; different topic |
| 0nxocR2qx4.md | 5.67 | R1 (bracket) | No | Preference optimization; different focus |
| 86zAUE80pP.md | 6.25 | R1 (bracket) | No | Continual RLHF; different topic |
| 9Hxdixed7p.md | 6.25 | R1+R2 | Yes | 3D-Properties: strong DPO analysis; stronger experiments and novelty |
| mMPMHWOdOy.md | 8.00 | R1 (bracket) | No | WizardMath: large-scale math RL; substantially stronger |
| rfdblE10qm.md | 8.00 | R1 (bracket) | No | Reward modeling theory; different contribution type |
| OOxotBmGol.md | 8.00 | R1 (bracket) | No | LLM+Bayesian optimization; different topic |
| Iyrtb9EJBp.md | 8.00 | R1 (bracket) | No | RAG trustworthiness; different topic |
| 4Po8d9GAfQ.md | 3.80 | R2 (narrow) | Yes | LaTRO: novel idea but weak evaluation (2 datasets, no confidence intervals) |
| HHmnfVQagN.md | 5.75 | R2 (narrow) | Yes | Flow of Reasoning: stronger experiments but novelty/clarity concerns |
| YW79lAHBUF.md | 3.75 | R2 (narrow) | No | In-context RL; different focus |
| OD9pwKQzXl.md | 5.25 | R2 (narrow) | No | Verifier Q-learning; different approach |
| **fsX9nFwMNj.md** | **6.00** | **R2 (narrow)** | **Yes** | **BNF Loss: novel loss simplification with strong experiments; stronger than paper under review** |
| ZRDa2IT1sQ.md | 6.00 | R2 (narrow) | No | SCDPO: step-level DPO for math; stronger evaluation |
| KFjCFxiGk4.md | 6.00 | R2 (narrow) | No | Certified reasoning; different topic |

**Round-1 bracket:** 4–6 (not strong reject, not accept). **Round-2 narrowing to 5.0** grounded in favorability comparison: the paper shares LaTRO's/RLSF's "no variance estimates" weakness (a -2.21 drag item) but exceeds them in breadth of evaluation; it falls short of BNF Loss (6.00) and RL Reward (5.17) on evidential rigor (no variance, no larger-scale experiment). The paper's strongest items (14.13 for ablation design, 14.77 for extending prior work) are genuine assets, but the evidential gap prevents the central comparative claim from being properly supported.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>