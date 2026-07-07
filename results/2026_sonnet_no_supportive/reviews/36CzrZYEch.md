Now I have enough information to produce the final review. My initial bracket from calibration: papers on autoregressive image generation methods with solid contributions but some weaknesses cluster around 5.5–6.5. The IRIS paper has a genuine novel finding, clean ablations, and a practical contribution (no external supervision needed), but the main claims are slightly overstated and the scope is limited to one architecture.

---

## Summary
IRIS proposes using Negative Self-Certainty (NSC)—the negation of the KL divergence between a model's output distribution and the uniform distribution—as an intrinsic reward for RL fine-tuning of autoregressive text-to-image (T2I) models via GRPO. The paper's central finding is that minimizing self-certainty improves T2I generation quality, in direct contrast to LLM reasoning settings where maximizing self-certainty is beneficial. Experiments on Janus-Pro 1B and 7B demonstrate IRIS achieves performance broadly competitive with T2I-R1 across GenEval, T2I-CompBench, and WISE benchmarks without any external supervision or labeled data.

## Strengths
- **Genuine counter-intuitive diagnostic (Figure 2):** The paper shows that RL training with external rewards *decreases* image-token self-certainty in Janus-Pro (T2I) while *increasing* text-token self-certainty in Qwen2.5 (math). This clean empirical observation motivates the NSC design non-trivially — it is not a post-hoc rationalization but a direct measurement that drives the method.
- **Baseline bug identification and correction (Section 4.1):** The paper identifies that T2I-R1's official implementation applied Janus's (not Janus-Pro's) chat template when training and evaluating Janus-Pro models, which corrupts all numerical results. Correcting this before comparison is scientifically responsible and benefits the broader community.
- **Thorough ablations (Section 4.3):** The paper isolates direction of SC for image tokens (Figure 6), direction of SC for text tokens (Figure 7), forward vs. backward KL (Figure 8), CoT vs. no-CoT (Figure 5), and RL vs. direct optimization (Figure 9). The collapse under maximized image self-certainty is especially informative.
- **WISE natural science advantage (Table 1c):** IRIS matches or exceeds T2I-R1 on biology (0.36 vs. 0.36 at 1B; 0.46 vs. 0.48 at 7B) and physics sub-tasks, consistent with the hypothesis that domain-specific external rewards (HPSv2, DINO, GIT, ORM) do not generalize to natural science prompts.

## Weaknesses

### Fatal
None.

### Major
- **Overstated framing of comparative results.** The abstract and contributions state IRIS achieves performance "competitive with or superior to external rewards." Looking at Table 1 across all aggregate metrics: IRIS-1B scores 0.72 vs. T2I-R1's 0.75 on GenEval; 0.3793 vs. 0.3820 on T2I-CompBench; 0.37 vs. 0.38 on WISE. IRIS-7B scores 0.77 vs. 0.78 on GenEval; 0.3916 vs. 0.3992 on T2I-CompBench; 0.48 vs. 0.50 on WISE. IRIS trails T2I-R1 on nearly all aggregate metrics. "Competitive" is defensible within the error bars, but "superior" is not supported by the aggregate evidence. This overstated framing — combined with Figure 3 showing IRIS above T2I-R1 on training curves while Table 1 shows T2I-R1 ahead on best-checkpoint scores — creates a misleading impression that should be corrected. The paper should either (a) qualify "superior" to the specific WISE natural science sub-tasks where it holds, or (b) explicitly reconcile Figure 3 vs. Table 1 (noting smoothing, checkpoint selection, or variance effects).

### Minor
- **Correlational rather than mechanistic explanation.** The paper observes that lower self-certainty correlates with visually richer images (Figs. 1, 2) and proposes minimizing self-certainty as the reward, but does not explain why. The text-token explanation in Section 3.2 ("maximizing NSC encourages diverse semantic CoTs") explicitly acknowledges "this appears to contradict our observation in Fig. 2" and speculates without direct evidence. An analysis of CoT diversity (n-gram diversity, CLIP embedding variance) between minimize-text-SC and maximize-text-SC runs would directly test this claim.
- **Scope limited to one architecture.** Section 4.4 acknowledges IRIS is only tested on Janus-Pro, yet the paper makes broad claims about autoregressive T2I models. Given the diversity of T2I architectures (continuous diffusion, masked modeling, MAE-style), a brief proof-of-concept on a second autoregressive backbone would substantially strengthen the generality argument.

### Trivial
None.

## Nice-to-Haves
- A mechanistic analysis tracking NSC values alongside image diversity metrics (e.g., LPIPS between same-prompt samples or CLIP embedding variance) over training to explain *why* minimizing NSC produces richer images.
- A human pairwise preference evaluation between IRIS and T2I-R1 outputs, since the core motivation is human preference alignment and automated benchmarks may not fully capture this.
- Clarification in Figure 3's caption or the main text explaining why training-curve trajectories show IRIS above T2I-R1 while Table 1 best-checkpoint scores favor T2I-R1.

## Removed Points
*These points are flagged to be removed, treat them with caution.*
- **"RL vs. direct optimization" explanation imprecision:** The reviewer noted that describing GRPO as "conservative" vs. "aggressive" direct optimization is imprecise (the two are qualitatively different signals). While true, the practical conclusion (RL avoids collapse; Figure 9) is clearly demonstrated, and prior art supports this practice. Demoted — not a substantive flaw.
- **Missing human evaluation as weakness:** The absence of human preference evaluation is noted, but large-scale T2I benchmark evaluation without human studies is standard in the field. Moved to Nice-to-Haves.
- **Strength about "important problem":** Dropped as generic/not specific to this paper's contribution.

## Novel Insights
The most genuinely novel insight is the task-dependent directionality of self-certainty as an RL signal: maximizing self-certainty benefits discrete reasoning (math) but harms visual generation, where lower self-certainty correlates with higher visual richness. This cross-modality asymmetry has implications beyond IRIS — it suggests that intrinsic RL rewards for multimodal generation tasks may need to be specifically re-examined rather than borrowed from LLM practice. The T2I-R1 chat-template correction is a practically valuable secondary finding that benefits the entire community reproducing T2I-R1 results.

## Suggestions
- Revise the abstract to say "competitive with" rather than "competitive with or superior to" external rewards, unless specifically restricted to natural science sub-tasks where IRIS does outperform.
- Add a sentence in Section 4.2 explaining the Figure 3 vs. Table 1 discrepancy (smoothing window, best-checkpoint selection, variance).
- Include a brief quantitative measure of CoT diversity (n-gram or embedding) to support the text-token NSC hypothesis in Section 3.2.

---

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| u1cQYxRI1H.md (IC-Light) | 10.0 | R1 | Unrelated (strong accept) |
| Uj0h13lVrR.md (GFlowNets KL) | 1.0 | R1 | Much weaker — lacks novelty and experiments |
| TJHB4ySVZM.md (T2I data extrapolation) | 3.4 | R1 | Weaker — poor presentation, limited novelty |
| b9dBNNeDd3.md (Set AR Modeling) | 4.6 | R1 | Comparable scope but less novel core insight |
| zfIxlvKq4u.md (AR model design space) | 4.0 | R1 | Weaker — design survey without clear novel finding |
| PQpvhUrA1C.md (Mamba autoregressive) | 5.75 | R1 | Similar quality — solid contribution, borderline accepted |
| ControlAR (BWuBDdXVnH) | 6.25 | R1 | Similar — method paper on AR image generation, accepted |
| wkbx7BRAsM.md (AR zero-shot video imitator) | 7.0 | R1 | Stronger — broader scope and stronger results |
| HFAIxjBB6K.md (GS-Softmax AR) | 4.75 | R1 | Slightly weaker — incremental fix, mixed reviews |
| 4KqkizXgXU.md (Curiosity red-teaming) | 8.0 | R1 | Stronger — more rigorous and broader impact |

**Round 1 bracket:** 5.5–6.5. IRIS is more novel in finding than the 4–5 papers, has cleaner ablations and a concrete baseline correction, but the overstated framing and limited architecture scope place it below the 7+ papers.

**Narrowing:** ControlAR (6.25) is a method paper on controllable AR image generation — solid contribution, accepted. IRIS has a more interesting *finding* (cross-modality self-certainty asymmetry) and arguably a more novel premise (first intrinsic-reward T2I RL), but trailing comparative results and architecture-scope limitation hold it back. Placing IRIS at **6.0**: a borderline accept reflecting a genuine and interesting contribution that is modestly overstated in framing and limited in empirical scope, but provides a real finding and a practically useful baseline correction.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>