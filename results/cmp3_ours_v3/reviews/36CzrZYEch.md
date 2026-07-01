Now I have all the information I need. Let me write the final comprehensive review.

## Summary

This paper proposes IRIS, the first framework to improve autoregressive text-to-image (T2I) models with reinforcement learning using only an intrinsic reward (Negative Self-Certainty, NSC) rather than external reward models or human-labeled data. The key empirical finding is that self-certainty behaves differently across modalities: RL training with external rewards increases self-certainty on text tokens (in math-reasoning LLMs) but decreases it on image tokens (in T2I models). Based on this, IRIS uses NSC (the negative KL divergence between the model's output distribution and a uniform distribution) as the reward signal within GRPO optimization. Experiments on Janus-Pro 1B and 7B models show IRIS achieves results close to external-reward-based methods on GenEval, T2I-CompBench, and WISE benchmarks, supported by thorough ablations.

## Strengths

1. **Genuinely interesting empirical finding (Sec. 3, Fig. 2).** The observation that RL alignment *decreases* image-token self-certainty in T2I models while *increasing* text-token self-certainty in math-reasoning LLMs is non-obvious and directly motivates the method. The controlled comparison (both trained with GRPO on verifiable rewards) cleanly isolates the modality/task difference.

2. **Clean experimental design with strong internal validity.** The paper establishes a causal chain: (a) external-reward training decreases image self-certainty → (b) hypothesize that minimizing self-certainty is beneficial → (c) propose IRIS using NSC as intrinsic reward → (d) verify benchmark improvement → (e) ablate that improvement comes from minimizing (not maximizing) self-certainty. This logical structure is well-executed and rare in empirical RL papers.

3. **Thorough ablations (Sec. 4.3).** The paper systematically addresses five natural questions: CoT vs no CoT, minimize vs maximize image SC, minimize vs maximize text SC, forward vs backward KL, and RL vs direct optimization. Each ablation yields a clear takeaway. The forward-vs-backward KL comparison (Fig. 8) is particularly valuable as it distinguishes self-certainty (KL(U||π)) from entropy (KL(π||U)), showing the specific forward-KL formulation matters.

4. **Honest baseline correction.** The paper identifies and corrects a chat-template inconsistency in the T2I-R1 implementation (line 120), re-running the baseline with the correct template. This is a service to the community and strengthens comparison validity.

5. **Competitive results without external supervision.** For the 1B model, IRIS reaches 0.72 (vs 0.75 external) on GenEval, 0.3793 (vs 0.3820) on T2I-CompBench, and 0.37 (vs 0.38) on WISE. These are close enough to demonstrate that purely intrinsic rewards are a viable path, which is the paper's core empirical claim.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Abstract overstates "superior to" (Abstract, Table 1).** The abstract claims IRIS "achieves performance that is competitive with or superior to external rewards." However, the best-checkpoint results in Table 1 consistently show IRIS slightly *below* T2I-R1 on all three overall benchmark scores (GenEval: 0.72 vs 0.75 for 1B, 0.77 vs 0.78 for 7B; T2I-CompBench Complex: 0.3793 vs 0.3820 for 1B, 0.3916 vs 0.3992 for 7B; WISE: 0.37 vs 0.38 for 1B, 0.48 vs 0.50 for 7B). While IRIS edges ahead on a few submetrics (e.g., Color in GenEval, Physics in WISE), the overall picture is that IRIS is close but not superior. The contribution — that intrinsic rewards can get surprisingly close to external ones — is already impressive and should be stated accurately.

2. **Training prompts for main results not clearly specified (Sec. 4.2).** The ablation section (Sec. 4.3) states it uses "553 GenEval prompts" for evaluation, but the main results (Table 1, Fig. 3) do not explicitly state what prompt dataset was used for training. If GenEval prompts were used for both training and evaluation, this could raise data-leakage concerns. The paper should clarify this.

3. **Mechanistic gap between NSC reward and benchmark improvements (Sec. 3.2, Sec. 4.4).** The intrinsic reward operates at the token-distribution level, yet the reported improvements are on benchmarks requiring compositional understanding, spatial reasoning, and world knowledge. The paper's explanation ("lower self-certainty → visually rich images") is plausible but does not fully explain why minimizing token-level uncertainty leads to *correct* object compositions and attribute binding. The GRPO group-relative advantage does important work here (preventing the collapse shown in Fig. 9), but the paper does not analyze what property of high-NSC samples actually drives quality. The authors acknowledge this is speculative; a mechanistic analysis would strengthen the contribution but does not invalidate the empirical finding.

4. **Limited evidence for "reasoning enhancement" claim (Sec. 1, Sec. 4.2).** The paper claims IRIS "can significantly enhance the reasoning capabilities of T2I models." The evidence is WISE benchmark improvements (which does test world knowledge) and one qualitative CoT example (Fig. 4). The WISE gains (28.8% on 1B) are legitimate evidence of improved knowledge-informed generation. However, the single CoT example does not systematically demonstrate *reasoning* improvement as distinct from more diverse/verbose textual generation (which NSC directly incentivizes). A more systematic CoT quality analysis (e.g., tracking CoT length, attribute diversity, or semantic specificity over training) would substantiate this claim.

### Trivial

None.

## Nice-to-Haves

- A mechanistic analysis of what the group-relative advantage selects for (e.g., sampling GRPO group generations at a fixed step, sorting by NSC, and comparing highest-NSC vs lowest-NSC images with quantitative measures like color histogram entropy, number of detected objects, or CLIP score variance).
- Distinguishing more explicitly between the *reward function* (NSC) and the *optimization mechanism* (GRPO group-relative advantage), since the per-token NSC is not directly maximized — the advantage normalizes it within each group.
- A more substantive limitations section (Sec. 4.4 is three sentences and does not address the mechanistic gap or training-prompt ambiguity).

## Removed Points

These points from the input review were removed with justification:

1. *"How the '1 image per text string' interacts with GRPO"* — This is already clarified in the paper (line 124: "generate 8 text strings per query and subsequent 1 image per text string in GRPO's advantage computation").

2. *"The mechanism gap is a structural/fatal issue"* — The paper acknowledges this as speculation, and many empirical RL papers have similar gaps between reward signal and measured outcome. It is a valid limitation but does not threaten the core empirical claim.

3. *"The reasoning claim is unsupported because WISE gains could come from diversity"* — This is speculative. WISE explicitly tests world knowledge (cultural common sense, spatio-temporal reasoning, natural science). A 28.8% improvement on a knowledge-reasoning benchmark is valid evidence of improved knowledge-informed generation; the criticism was over-stated.

4. *"Missing related works"* — Not permissible per review guidelines; no external validation possible.

## Novel Insights

The most interesting observation emerging from the review is that the paper's key vulnerability is **framing precision rather than experimental quality.** Every identified weakness is about overclaiming or underspecifying — not about the experiments being wrong, the method being unsound, or the results being uninformative. This is an unusual profile: the paper's actual substance (finding, method, ablations) is solid, but the packaging (abstract "superior to," "reasoning enhancement," underspecified training data) creates unnecessary vulnerability. The paper would benefit more from careful reframing than from additional experiments.

## Suggestions

1. Reword the abstract: replace "competitive with or superior to" with "competitive with" (reflecting the best-checkpoint data).
2. Explicitly state what prompt dataset was used for training the main results (Table 1, Fig. 3) and discuss any overlap with evaluation benchmarks.
3. Add a brief qualitative or quantitative analysis of what high-NSC vs low-NSC images look like within a GRPO group at a fixed training step.
4. For the "reasoning" claim, either provide systematic CoT analysis (e.g., tracking CoT length, attribute diversity, or semantic specificity over training) or soften the claim to "improves knowledge-informed generation."

## Score and Decision

**Bracket (Round 1):** 5.5 – 6.5, based on calibration against papers on similar topics (scaling AR T2I models, reward-based T2I alignment, intrinsic rewards for generation).

**Narrow calibration (Round 2):** Anchored at 6.0 against:
- "Confidence-aware Reward Optimization for Fine-tuning Text-to-Image Models" (avg 6.00): both address T2I alignment, similar level of contribution and rigor.
- "Scaling Autoregressive Text-to-image Generative Models with Continuous Tokens" (avg 5.75): similar empirical focus on AR T2I, similar level of novelty.
- "ControlAR" (avg 6.25): stronger practical contribution but similar methodology depth.
- "Transfusion" (avg 7.60): substantially stronger paper (pretraining from scratch, scaling laws, multi-modal) — IRIS does not reach this level.

IRIS has a genuinely novel finding (modality-dependent self-certainty), thorough ablations, and clean experimental design. Its weaknesses are about framing and missing details rather than fatal flaws. This places it solidly in the Accept range, comparable to the 6.0 anchor papers.

**Final score:** 6.0

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>