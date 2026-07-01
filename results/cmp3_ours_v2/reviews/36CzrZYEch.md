Now I have sufficient calibration context. Let me write the final consolidated review.

## Summary

This paper proposes IRIS, which uses Negative Self-Certainty (NSC) — the KL divergence from a uniform distribution over the vocabulary — as an intrinsic reward for RL-based fine-tuning of autoregressive T2I models (specifically Janus-Pro). The key finding is that minimizing self-certainty (maximizing uncertainty) improves T2I generation quality, which is the opposite of what has been observed in text-only LLM reasoning. The method requires no human preference data, no external reward models, and no domain-specific verifiers. Evaluated on GenEval, T2I-CompBench, and WISE benchmarks, IRIS improves substantially over the base Janus-Pro model and narrows the gap with external-reward-based training (T2I-R1).

## Strengths

1. **Non-obvious finding about self-certainty in T2I.** The core empirical observation — that minimizing self-certainty (rather than maximizing it, as in text-domain LLMs) improves T2I generation — is genuinely interesting and counterintuitive. Figure 1 provides visually compelling evidence that overconfident models generate uniform, simplistic images. If correct, this finding has practical value: a simple intrinsic signal requiring no human labels or domain-specific verifiers can serve as a training signal for T2I alignment.

2. **Thorough ablation design.** Section 4.3 systematically ablates five design choices: with/without semantic CoTs (Fig. 5), maximizing vs. minimizing image SC (Fig. 6), maximizing vs. minimizing text SC (Fig. 7), forward vs. backward KL (Fig. 8), and with vs. without RL (Fig. 9). Each ablation is evaluated on four independent reward metrics (HPSv2, GIT, DINO, ORM) not used in training. The finding that maximizing image SC causes rapid performance collapse (Fig. 6) and that forward KL outperforms backward KL (Fig. 8) provides meaningful guidance.

3. **Clean, self-contained formulation.** The IRIS reward is simply the negative KL divergence between the model's output distribution and a uniform distribution — requiring no external reward models, human preference data, or domain-specific heuristics. This parsimony is a genuine virtue: if the method works, it is far more scalable and generalizable than approaches requiring separate reward models or labeled preference data.

## Weaknesses

### Fatal
None.

### Major

1. **Abstract overstates empirical results relative to what Table 1 shows.** The abstract claims IRIS "achieves performance that is competitive with or superior to external rewards." However, Table 1 shows IRIS is numerically *behind* T2I-R1 (external rewards) on GenEval Overall (0.72 vs. 0.75 for 1B; 0.77 vs. 0.78 for 7B), on WISE Overall (0.37 vs. 0.38 for 1B; 0.48 vs. 0.50 for 7B), and on most T2I-CompBench sub-metrics. "Competitive" (within 1–3 points) is fair; "superior" is not supported by the paper's own main table. The 9.1%, 13.3%, and 28.8% gains cited in the introduction (line 44) are improvements over the *base* Janus-Pro model (which is a legitimate result), but presenting these without making the reference point explicit creates an inflated impression of the method's standing against external-reward baselines. The contribution list (line 50) uses the more measured phrase "competitive performance," which better reflects the data.

2. **Inconsistency between Figure 3 and Table 1.** Figure 3's caption (line 126) states that "IRIS with CoT achieves higher scores than T2I-R1 (external) after approximately 200 training steps" on GenEval, T2I-CompBench, and WISE. Yet Table 1 — which reports the *best checkpoint* from steps 100–800 — shows T2I-R1 ahead of IRIS on GenEval (0.75 vs. 0.72) and WISE (0.38 vs. 0.37). If IRIS leads from step 200 onward, its best checkpoint should reflect this advantage. These two statements cannot both be correct without further explanation. The authors must clarify what exactly Figure 3 plots (e.g., running averages, a different metric) and resolve the discrepancy. This inconsistency undermines reader trust in the results.

### Minor

3. **Evidence for the task-dependent self-certainty claim is confounded.** Figure 2 compares text self-certainty in Qwen2.5-1.5B-Instruct during math reasoning (left y-axis, range 31–38) against image self-certainty in Janus-Pro-1B during T2I generation (right y-axis, range 18.75–20.50). These are different models on different tasks with different y-axis scales. This does not cleanly demonstrate that self-certainty behaves differently across *tasks* — it demonstrates that different models on different tasks behave differently. A controlled experiment tracking both text and image SC within the *same* multimodal model during both task types would directly test the central motivating claim. The paper's ablations (Figs. 6–7) provide empirical support for minimizing SC in T2I even without this controlled comparison, so this is not fatal, but the framing in Section 1 and Figure 2 overclaims what the evidence supports.

4. **The role of group-relative normalization in GRPO is under-discussed.** The ablation in Figure 9 shows that directly maximizing NSC (without GRPO's group-relative advantage computation) leads to collapse, while RL with GRPO succeeds. The paper attributes this to GRPO's "conservative strategy" (line 262), but the mechanism is worth deeper analysis: the effective training signal is not NSC itself but the *z-scored NSC within a group of G samples*. Collapse from direct NSC optimization suggests that the group normalization is not merely an optimization convenience but may be essential. A brief discussion of what properties the group-relative signal provides (e.g., why it prevents the trivial solution of near-uniform output distributions) would strengthen the paper.

### Trivial

None.

## Nice-to-Haves

- **Controlled experiment for the task-dependent claim**: Tracking both text SC and image SC of Janus-Pro during both a text-only reasoning task and T2I generation would directly test whether SC's optimal direction depends on modality/task within the same model, which is the paper's central motivating narrative.
- **Report computational cost**: Training time or GPU hours would help readers assess the method's practical accessibility.
- **Limited to autoregressive T2I**: The paper acknowledges this in Section 4.4, noting that most production T2I models are diffusion-based. This is an honest limitation but is worth elevating.
- **No human evaluation**: The benchmarks are automated; a small human evaluation study would strengthen alignment claims.
- **Chat template discrepancy with T2I-R1**: The paper notes (lines 120–121) that its T2I-R1 numbers differ from the original Jiang et al. (2025) paper due to a chat template mismatch. Reporting both configurations side-by-side would help readers assess the impact.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"The mechanism is under-explained: is NSC the reward, or is it the group-relative advantage?"** — The paper's ablation study (Fig. 9) and Section 3.2 explicitly discuss this. Direct NSC optimization collapses; GRPO prevents this. The reviewer's framing treats this as an omission when it is actually addressed. Demoted to Minor above (point 4 in Minor) with a narrower formulation.
- **"No comparison with diffusion-based T2I models"** — The paper acknowledges this limitation in Section 4.4. Also, the paper's scope is autoregressive T2I. This is a scope limitation, not a flaw.
- **"Chat template inconsistency"** (lines 120–121) — This is a minor implementation detail that the paper transparently discloses.
- **"No human evaluation"** — Not a standard requirement for automated benchmark evaluation.
- **"Computational cost not reported"** — Minor omission; moved to Nice-to-Haves.
- **Pure formatting/style nitpicks** — Removed per policy.
- **Missing related works** — Removed per policy (no external knowledge to verify).
- **"Missing appendix/proofs"** — The parser strips appendices; they exist in the original submission.

## Novel Insights

The harsh critic's most valuable observation is the Figure 3 vs. Table 1 inconsistency, which goes beyond a generic "results are overstated" complaint to identify a specific numerical contradiction. This is the kind of concrete, actionable issue that can help the authors improve the paper significantly. The critic also correctly notes that the paper's strongest result (closing the gap with external rewards by 1–4 points without any human labels) is genuinely interesting and should be the headline, not the unsupported "superior" claim. The observation that direct NSC optimization collapses while group-relative NSC works suggests the method's real mechanism is more nuanced than the paper currently acknowledges.

## Suggestions

1. **Reframe the headline result** from "competitive with or superior to external rewards" to "narrows the gap with external rewards to 1–4 points without any human labels or domain-specific verifiers." This is equally compelling and accurately reflects Table 1.

2. **Resolve the Figure 3 vs. Table 1 inconsistency.** If the figure plots smoothed/averaged values while the table reports discrete checkpoints, or if the figure uses a different evaluation protocol, state this explicitly. If it is an error in the figure, correct it.

3. **Add a controlled experiment for Figure 2** tracking both text SC and image SC in Janus-Pro during T2I training (or alternatively, track Janus-Pro during a text-only reasoning task). This would cleanly support the task-dependent claim that is central to the paper's narrative.

4. **Discuss the role of group normalization** in preventing NSC collapse more thoroughly. Explain what properties the group-relative advantage provides that direct NSC optimization lacks.

5. **Remove "superior to"** from the abstract and introduction claims unless the authors can identify a benchmark where IRIS is clearly ahead of external rewards at the best checkpoint (rather than early in training).

## Score and Decision

### Calibration anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| bO31lfEdos (Human-Free RL for hallucination mitigation) | 5.0 | R1 | Similar "no human feedback" RL for vision-language; IRIS has more thorough ablations and a more novel finding, but also has more significant framing issues |
| fXkoROek1M (Avoiding mode collapse in RL-finetuned diffusion models) | 4.0 | R1 | Different technical approach; IRIS is stronger in novelty and ablation depth |
| jQP5o1VAVc (Scaling AR T2I with continuous tokens) | 5.75 | R1 | Solid empirical scaling paper; IRIS has a more novel conceptual finding but weaker quantitative results vs. baselines |
| xreOs2yjqf (EvalAlign for T2I evaluation) | 4.75 | R1 | Different contribution type (evaluation metric); similar score range |
| kGvXIlIVLM (Guidance-free AR visual generation) | 7.0 | R1 | High-quality paper with clean theory and strong experiments; IRIS is weaker across all dimensions |

### Calibration

Round 1 bracket: 3.5–6.0 (between the reject-quality RL-for-vision papers at ~4–5 and the accept-quality AR generation papers at ~6–7).

The paper has a genuinely interesting core finding and thorough ablations, placing it above the 4.0 papers. However, the significant framing issues (abstract overclaiming, Figure 3/Table 1 inconsistency) and confounded evidence for the central motivating claim prevent it from reaching the 6+ level. The most comparable anchor is bO31lfEdos (avg 5.0), which had similar "no human feedback" RL for vision-language but fewer framing issues.

**Final score: 5.0**

The paper's core contribution is real and the ablations are thorough. However, the gap between the claims (in abstract, introduction, and Figure 3 caption) and the evidence (Table 1) is too large to accept in current form. The issues are fixable with careful revision, but they are significant enough to warrant rejection at this stage.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>