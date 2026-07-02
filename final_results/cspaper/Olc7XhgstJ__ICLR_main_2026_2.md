---
job_id: fbc03279-28f3-4380-80d6-97147f4e280e
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: Olc7XhgstJ.pdf
paper: Steady Thought: Mitigating LLM Under-Thinking via Thought-Level Preference Optimization
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope, it studies post-training/alignment for large reasoning models, preference optimization, and reasoning efficiency in language models.

## Minimum Quality
Pass ✅. The paper contains the required components, including abstract, introduction, related work, methodology, experiments/results, and conclusion, and it presents a coherent empirical study. While I have significant concerns about rigor, novelty positioning, and some methodological details, these are review-level weaknesses rather than desk-rejection-level failures.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find hidden prompts, reviewer-targeted instructions, or other manipulative content in the provided manuscript text or figures.

# Expected Review Outcome:
## Summary
This paper targets the "under-thinking" behavior of large reasoning models, defined here as unnecessarily abandoning promising reasoning thoughts and switching to other trajectories. The proposed Steady Thought (ST) framework has three stages: entropy-based thought segmentation, thought completion under token-level suppression of switching cues, and a thought-level preference optimization objective (STPO) that prefers a successful completion of a thought over the original subsequent switched trajectory.

The paper evaluates ST on three base reasoning models and four benchmarks, reporting improved accuracy together with shorter outputs. The authors also include analyses of thought counts, proportion of final-thought tokens, entropy threshold sensitivity, and comparisons to SFT/DPO variants.

## Strengths
1. The paper addresses a timely and practically relevant problem. There is clear value in going beyond "make CoT shorter" and instead asking when a model should persist versus when it should switch. That framing is useful, and the paper gives it a more operational treatment than many purely decoding-based heuristics.

2. The proposed training signal is reasonably intuitive. Conditioning the preference pair on a shared prefix \((Q, T_i)\) and comparing a successful completion \(T_i'\) to the original continuation \((T_{i+1}, \ldots, T_n)\) in **Equation (7)** is a sensible way to move supervision closer to the point of divergence, rather than treating an entire chain as uniformly good or bad.

3. The main empirical results in **Table 1** are directionally promising. In particular, for Qwen3-8B and DeepSeek-R1-Distill-Qwen-14B, ST improves average accuracy while also reducing tokens, which is the right tradeoff for the paper’s stated goal. The gains on LiveCode, despite training on math data only, are also potentially interesting as an indication of behavioral transfer.

4. The paper does attempt more than a single headline table. The analyses in **Figure 2**, **Table 2**, **Table 3**, and **Table 4** reflect an effort to probe mechanism rather than merely report end-task accuracy. I appreciated that **Figure 2** tries to connect the intervention to shorter trajectories, fewer thoughts in many settings, and a larger proportion of the final thought, which is at least qualitatively aligned with the intended behavior change.

5. The comparison against simple alternatives is useful. Including NoThink, NOWAIT, and SEAL in **Table 1** helps place the method relative to both aggressive shortening and inference-time anti-switching approaches, rather than only comparing against the base model.

## Weaknesses
1. **The central supervision pipeline depends on correctness labels for intermediate thought completions, but the data construction process is underspecified in several places, and this matters directly for validity.**  
   In **Section 3.2**, the paper says each segmented thought \(T_i\) is continued under token suppression to yield \(T_i' = \text{Model}(Q, T_i)\), and the final answer is then checked for correctness. However, the manuscript does not clearly specify:
   - whether *all* segmented thoughts are completed or only a subset,
   - how many decoding samples are taken per thought,
   - whether completion is deterministic or stochastic,
   - how ties or multiple correct completions are handled,
   - whether a thought is kept if the completion is correct but substantially longer/shorter than the original continuation,
   - and what happens when no thought in a response yields a correct completion.  
   These are not cosmetic omissions. They determine the actual distribution of preference pairs and therefore the optimization target in **Equation (7)**. A different sampling strategy could materially change both data quality and reported gains.

2. **There is a serious confound between "thought-level preference optimization" and "token-level suppression heuristics during synthetic data generation," and the paper does not disentangle them adequately.**  
   The method claims to teach the model when to persist and when to switch, but the chosen completions are themselves generated by explicitly suppressing tokens such as "wait" and "alternatively" in **Section 3.2** and Appendix **Table 5**. This means the preferred data are already heavily shaped by a hand-crafted anti-switch prior. It is therefore hard to know whether STPO is learning a general persistence criterion, or simply imitating outputs produced under a strong lexical constraint. The ablation in **Table 4** compares SFT, DPO, and STPO, but it does not isolate the effect of the thought-completion generator itself. A much stronger ablation would compare:  
   - STPO with suppressed-token completions,  
   - STPO with normal completions,  
   - SFT on the same completions,  
   - and perhaps pure data filtering without preference optimization.  
   Without that, the claimed conceptual contribution is murkier than the paper suggests.

3. **The formulation around "promising thoughts" is conceptually attractive but operationally circular.**  
   In **Section 2.1**, a promising thought is described as one that "can lead to a correct answer," and the commit trajectory is the one that correctly completes it. In practice, the paper identifies such thoughts by generating a completion and checking if the final answer is correct. This makes the notion retrospective and outcome-defined. That is acceptable as a heuristic, but then the paper should be more honest that it is not detecting intrinsic promise, it is constructing ex post labels through guided rollouts. Right now, the prose sometimes reads as if the method has isolated a meaningful latent decision point, while in reality it depends on whether a particular completion procedure succeeds.

4. **Some of the mathematical exposition is too thin relative to the claims, and a few definitions are not clean enough.**  
   - In **Equation (2)**, the "Steadiness Score" \(S_\pi(\tau \mid \mathbf{P}_i)\) is introduced as a latent quantity, then later instantiated by log-probability. But this is not really developed into a principled derivation; it mostly serves as a motivational wrapper around standard pairwise preference modeling.  
   - In **Equation (6)**, \(T_i' = \text{Model}(Q, T_i)\) is too informal for a core algorithmic step. The actual conditioning should be over the original question and the *prefix up to and including* \(T_i\), not merely the isolated thought token span, unless the prompt truly discards earlier thoughts. If the true conditioning context is \((Q, T_1, \ldots, T_i)\), then the notation is misleading; if it is only \((Q, T_i)\), then the model is being asked to continue from a partial thought without the original preceding reasoning context, which is a very different setup.  
   - In **Equation (7)**, the objective is essentially SimPO applied to thought-conditioned continuations. That is fine, but then the paper should spell out the exact tokenization/unit for \(|y_w|\) and \(|y_l|\), and whether these are measured after truncation or EOS termination. Since length normalization is central to the argument, this should not be left implicit.

5. **The evidence for the thought segmentation module is not strong enough in the main paper, yet the whole pipeline depends on it.**  
   **Section 3.1** uses entropy spikes at the beginning of pre-segmented steps to detect thought switches. This is plausible, but also quite brittle. The pre-segmentation itself depends on the delimiter ".\n\n", which is a formatting artifact of certain model outputs and may not generalize. More importantly, the main paper does not provide a robust validation of segmentation quality. The later appendix claim of 85% precision is not enough for a method whose training signal critically depends on identifying switch points. In the main paper, **Table 3** only shows downstream sensitivity to threshold choice for one model, not whether the segmentation is actually semantically correct. If segmentation is noisy, the preference pairs in **Equation (7)** may compare misaligned units, which weakens the scientific interpretation.

6. **The analyses in Figure 2 and Table 2 support the authors’ story only partially, and some interpretations overreach.**  
   **Figure 2** is helpful, but it also reveals that the behavior change is not uniformly "fewer thoughts and deeper exploration." For DeepSeek-R1-Distill-Qwen-1.5B on AIME2024, the number of thoughts actually increases under ST, as the authors acknowledge. That does not invalidate the method, but it shows the mechanism is more nuanced than the paper's recurring narrative of "stick to promising thoughts." Similarly, **Table 2** uses the percentage of correct intermediate thoughts before the final one as a proxy for "invalid switches." This is a rather indirect metric. A correct intermediate thought may be locally correct but incomplete, or one of several valid partial routes, and counting it as an invalid switch assumes a very specific interpretation of the trajectory. The paper treats this proxy more definitively than it deserves.

7. **The experimental protocol raises concerns about robustness and fairness of comparison.**  
   Several choices in **Section 4** make it difficult to judge how stable the reported improvements are:
   - AIME has only 30 problems, even if averaged over 8 runs. A 3 to 5 point swing is not very stable on such a small benchmark.
   - LiveCode is evaluated over only two runs. For code tasks, pass@k-style variance can be substantial.
   - The paper reports averages across heterogeneous tasks in **Table 1**, but the "Overall Acc" is a simple average over benchmark accuracies with very different sizes and noise levels. This is not wrong, but it can look more solid than it is.
   - Baseline tuning is unclear. The paper does not explain whether NOWAIT and SEAL were re-tuned per model/task or used with default settings. Given that NOWAIT performs extremely poorly for Qwen3-8B in **Table 1**, even increasing token counts by 84.6%, one wonders whether the baseline was in a favorable operating regime.
   These issues matter because the empirical claim is the backbone of the paper.

8. **Novelty is somewhat limited at the method level, even if the problem framing is useful.**  
   The core recipe is: segment a trajectory, generate an alternative continuation under anti-switch decoding, and run a SimPO-like objective on the resulting pair. That is a reasonable combination, but it is still a composition of known ingredients rather than a clearly new learning principle. The paper would benefit from stronger positioning against step-level or token-level preference optimization approaches already cited in **Section 5.2**, and from a crisper articulation of what is fundamentally enabled by "thought-level" units beyond heuristic segmentation plus conditional preference learning.

9. **The claimed generalization story is stronger than the evidence warrants.**  
   The authors interpret the LiveCode gains in **Table 1** as evidence that ST teaches a "more precise pattern of thought switching and retention" rather than memorizing math data. That is possible, but one OOD benchmark with modest scale is not enough to substantiate a broad generalization claim. Since the intervention partly relies on generic lexical suppression of switch markers, transfer to another domain is not surprising by itself and does not necessarily demonstrate learning of a domain-agnostic reasoning principle.

10. **There are presentation issues around algorithmic clarity.**  
   Although the paper is generally readable, the core training pipeline would benefit from pseudocode and a cleaner specification of what exactly becomes the prompt, chosen continuation, and rejected continuation. **Figure 1(c)** gives a high-level overview and is visually useful, but it abstracts away several important implementation choices, especially how a candidate step becomes a thought boundary and how completions are filtered into preference pairs. For a paper whose contribution is mainly in data construction and supervision granularity, this level of abstraction leaves too much hidden.

## Questions
1. In **Section 3.2**, what exactly is the prompt used to generate \(T_i'\)? Is the model conditioned on \((Q, T_1, \ldots, T_i)\) or only \((Q, T_i)\)? Please state the exact input format, because this substantially changes the interpretation of **Equation (6)** and **Equation (7)**.

2. How many completions are generated per thought, with what decoding parameters, and how is the chosen completion selected if multiple completions are correct? If only one completion is generated, please justify why that is sufficient given the stochasticity of reasoning rollouts.

3. Can the authors provide an ablation that isolates the effect of STPO from the anti-switch completion generator? For example, compare preference training on completions generated with and without suppressed switch tokens. This would significantly increase my confidence that the gains come from thought-level preference optimization rather than from the data-generation heuristic.

4. How are preference pairs filtered? Are pairs included only when \(T_i'\) is correct and the original continuation is incorrect, or also when both are correct but one is shorter, or when the original final answer is already correct? A precise data construction table would be very helpful.

5. For **Table 1**, were NOWAIT and SEAL tuned separately for each model? The poor NOWAIT behavior for Qwen3-8B, including longer outputs than vanilla on multiple tasks, makes it hard to tell whether the baseline is fairly optimized.

6. Could the authors report confidence intervals or per-problem win rates, at least for AIME2024 and LiveCode? The current small-sample evaluation leaves uncertainty about whether the reported gains are robust.

7. The metric in **Table 2** interprets correct intermediate thoughts before the final answer as invalid switches. Can the authors justify this proxy more carefully, or provide a more direct measure based on annotated or manually inspected switch quality?

8. Since segmentation quality is essential, can the authors move a quantitative validation of the entropy-based thought segmentation into the main paper and clarify how precision was computed? Even a small manually annotated study would make the central premise more convincing.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No major ethics concerns are evident from the main paper. The work studies post-training and inference behavior of reasoning models on benchmark datasets, and I did not identify dataset, human-subject, privacy, or harmful deployment issues that require separate ethics review based on the manuscript.

## Soundness Rating
2: fair. The method is plausible and the experiments are suggestive, but the paper leaves important details of data construction and conditioning ambiguous, and several core claims are supported more weakly than the narrative implies.

## Presentation Rating
3: good. The paper is readable, the motivation is easy to follow, and the figures/tables are useful, but the algorithmic specification is not precise enough for a method paper centered on data construction and training objective design.

## Contribution Rating
2: fair. The problem framing is interesting and the empirical direction is promising, but the method is largely a combination of existing ingredients, and the evidence does not yet fully establish a strong conceptual or empirical advance.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted. The paper has a worthwhile target and some promising results, especially in **Table 1**, but the current version does not adequately disentangle the main source of gains, leaves key training/data-construction details underspecified, and over-interprets some of its analyses. With stronger ablations and sharper methodological specification, this could become a more convincing ICLR submission.

## Reviewer Confidence
4: confident. I am confident in this assessment. The area is close to my expertise, and I checked the method, equations, figures, and tables carefully, though some implementation ambiguities in the paper itself limit absolute certainty.