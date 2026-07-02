---
job_id: fddc0a19-006d-4efc-9c44-4305afc85344
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: 5SQo2E9Ujj.pdf
paper: Curriculum as Selective Data Acquisition: Toward Reliable Generalization in Goal-Conditioned RL
main_score_norm: 0.2
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within reinforcement learning, specifically goal-conditioned RL and curriculum learning, which fits ICLR scope.

## Minimum Quality
Pass ✅. The submission contains the expected scientific components, including abstract, introduction, method, experiments/results, discussion, and conclusion. While the work has substantial weaknesses in novelty, rigor, and experimental support, these are better handled in full review rather than desk rejection.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find hidden prompts, manipulative instructions, or other signs of attempted review interference in the provided paper content.

# Expected Review Outcome:
## Summary
This paper studies curriculum learning in goal-conditioned reinforcement learning from a data-distribution perspective. Using a deterministic GridWorld and UVFAs trained with potential-based reward shaping, the authors compare uniform goal sampling against edge-biased goal sampling, and argue that curriculum acts as selective data acquisition by reallocating training mass toward underachieved goals. Empirically, the paper reports modest gains on edge goals and similar overall performance, with an additional weighted curriculum variant intended to amplify this effect.

## Strengths
The paper has a clear high-level intuition: reframing curriculum learning as a mechanism that changes the state-goal training distribution, rather than just an exploration trick, is a reasonable lens and is easy to understand. Even if the empirical setting is simple, this framing is conceptually cleaner than the usual vague “easy-to-hard” story.

I also appreciate that the paper isolates one factor, goal-sampling distribution, while keeping the model architecture and nominal training budget fixed. For a small controlled study, that is the right instinct. In particular, the setup in Section 2.4 and Section 2.5 tries to hold the UVFA and optimizer constant so that any change can be attributed to the curriculum-induced distribution shift.

The figures are directionally aligned with the paper’s main claim. **Figure 2** is the most informative visual element because it combines the distributional story and the success-rate story in one place: the left part suggests that curriculum indeed reallocates training emphasis toward edge goals, while the right part shows a corresponding increase in edge-goal success at \(H=16\). This is useful because the paper’s thesis is specifically about selective data acquisition, not just final return. Similarly, **Figure 3** provides a simple but relevant sensitivity check, showing that stronger edge weighting can increase the edge-goal effect.

The paper is appropriately modest in some places. Section 4.1 acknowledges that the setting is small, the curriculum is hand-designed, and gains are modest. That honesty is welcome.

## Weaknesses
I have several concerns, some conceptual and some technical. Collectively they make the paper fall short of ICLR standards in its current form.

1. **The empirical contribution is too small and too underpowered to support the broad claims.**  
   The entire paper rests on a tiny deterministic GridWorld with only three seeds, 1000 episodes per seed, and a single MLP of hidden size 64, as described in Section 2.2 and Section 2.5. The conclusion and abstract, however, reach toward “reliable generalization,” “persistent and open-ended agents,” and a “pathway toward more persistent and open-ended agents.” That is a very large rhetorical leap from a toy environment with manually defined edge goals. The issue is not merely scale. In deterministic GridWorlds, many confounds that dominate real GCRL, such as exploration failure, stochasticity, representation aliasing, and changing task structure, are absent. So the current evidence only supports a narrow statement about sampling bias in a toy setting, not the stronger claims about reliable generalization or open-ended learning.

2. **The novelty is limited and the paper does not adequately differentiate itself from standard curriculum sampling in GCRL.**  
   The core method in Section 2.4 is simply to upweight edge goals because they are harder under uniform sampling. That is a reasonable baseline manipulation, but it is not methodologically new. The paper’s claimed novelty is mainly interpretive, “curriculum as selective data acquisition,” rather than algorithmic. That can still be publishable if the analysis is deep, but here the analysis remains shallow. There is no formal characterization of how the altered sampling distribution affects approximation error, no decomposition of coverage vs. difficulty, and no comparison against established adaptive curriculum mechanisms beyond a strawman uniform sampler. As written, the paper risks rebranding an obvious reweighting experiment with bigger conceptual language than the evidence can sustain.

3. **The paper’s mathematical setup is underspecified and in places inconsistent.**  
   The reward-shaping equation in Section 2.3 is written as
   \[
   r_t = \lambda[\gamma \phi(s_t + 1, g) - \phi(s_t, g)] - c
   \]
   which appears to use \(\phi(s_t + 1, g)\) rather than \(\phi(s_{t+1}, g)\). I assume this is intended to mean the next state, but as written the notation is incorrect. More importantly, the training target is not rigorously defined. The paper says “Targets are constructed as discounted returns-to-go under this shaped reward” and then says “For evaluation, we negate returns so that greedy action selection corresponds to arg max over predicted values.” This is confusing. If the network predicts \(V(s,g)\), then action selection requires either a model to simulate successor states or an action-value estimate \(Q(s,a,g)\). The paper never clearly states how greedy action selection is performed from a scalar state-goal value function. Do the authors enumerate actions and evaluate \(V(s',g)\) on successor states? If so, this should be explicitly stated. If the sign of the return is flipped only at evaluation, then the semantics of the learned target are also unclear. This matters because the evaluation protocol is central to every reported number.

4. **The use of PBRS is not well justified relative to the paper’s claim about curriculum.**  
   Potential-based shaping already injects dense geometric structure via Manhattan distance, which may dominate the effect attributed to the curriculum. In this environment, \(\phi(s,g) = -d(s,g)\) is extremely informative and arguably makes the value approximation problem almost trivial compared to sparse-reward GCRL. As a result, it is hard to tell whether the reported gains are really about curriculum-driven selective acquisition or simply minor changes on top of an already heavily shaped problem. A key missing experiment is a sparse-reward or weaker-shaping comparison. Without that, the paper’s central claim, that curriculum is the structural mechanism driving better approximation, is not isolated.

5. **The experimental evidence is inconsistent across the paper, including contradictory quantitative reporting.**  
   The most serious presentation issue is that the numbers in Section 3.1 do not match **Table 1**. In Section 3.1 on Page 3, the paper states that at \(H=16\), NoCurr achieved \(0.361 \pm 0.060\) overall and \(0.183 \pm 0.131\) on edge goals, while Curr achieved \(0.370 \pm 0.151\) overall and \(0.217 \pm 0.125\) on edge goals. But **Table 1** on Page 5 reports NoCurr \(0.276 \pm 0.055\) overall and \(0.060 \pm 0.055\) on edge goals, versus Curr \(0.297 \pm 0.056\) overall and \(0.143 \pm 0.107\) on edge goals. These are not small rounding discrepancies, they are materially different results. Since the paper’s contribution is empirical, this inconsistency is a major problem. I cannot tell which numbers are correct, whether they come from different evaluation sets, or whether one is stale. That directly undermines confidence in the conclusions.

6. **The figures are only weakly informative and, in one case, do not support as much as the text claims.**  
   **Figure 1** and **Figure 2** present mean \(\pm\) standard deviation over only three seeds, with large overlap between conditions. In **Figure 1**, the overall bars are nearly indistinguishable, and the edge-goal bars also have large relative variance. The text says the curriculum “improves performance on harder edge goals while maintaining comparable performance overall,” which is directionally true, but the figure also visually suggests that the effect size is small relative to uncertainty. **Figure 3** goes a bit further by including the weighted curriculum, but it still does not establish robustness because there is no horizon sweep, no significance analysis, and no demonstration that the weighted scheme does not hurt other subsets in a more granular breakdown. In short, the figures are consistent with a hypothesis, but they are not strong evidence for the stronger general claims the paper makes.

7. **The paper lacks essential baselines and ablations.**  
   The comparison set is too narrow: uniform sampling, a hand-crafted edge curriculum, and a more strongly weighted edge curriculum. There is no comparison to alternative simple curricula such as distance-based sampling, learning-progress sampling, success-rate-adaptive sampling, reverse curriculum, or even a difficulty-matched non-edge heuristic. This matters because the claimed principle is not “edge goals are useful,” but “curriculum as selective data acquisition improves approximation by reallocating mass toward underachieved regions.” To test that principle, the paper should compare multiple acquisition policies, not just two manually chosen variants tailored to this grid. Right now it is impossible to know whether the observed gain is about “underachieved goals” in general or simply about one convenient hand-designed subset.

8. **The evaluation of “generalization” is not convincing.**  
   Section 2.5 says evaluation is “zero-shot on held-out goals,” but the paper does not specify how goals are split, whether held-out goals are spatially disjoint, whether all states remain covered during training, or how many held-out goals there are. In a small GridWorld, goal holdout can be quite weak if the model has seen nearly every state-goal neighborhood. Also, because the agent is trained on shaped returns with full state observability and a very low-dimensional state-goal representation, “held-out goals” do not automatically imply meaningful generalization. This needs a much more careful protocol description and stronger tests, for example systematic extrapolation to corners, larger grids, obstacle layouts, or shifted goal distributions.

9. **The claim about reduced approximation error is unsupported in the main paper.**  
   The abstract and introduction say curricula “reduce approximation error,” but the main paper does not provide an explicit approximation-error metric, plot, or table that quantifies this. I do not see an error curve, a value-prediction MSE on a shared test set, calibration statistics, or a state-goal heatmap of prediction residuals. The closest evidence is indirect success-rate improvement. That is not enough to support a distinct claim about function approximation quality. If approximation error is central to the paper’s thesis, it needs direct measurement in the results.

10. **The paper is underdeveloped as a scientific argument and reads more like a short pilot study than a conference paper.**  
    Several signs point in this direction: the missing rigor around the training/evaluation pipeline, the contradictory numbers, the absence of statistical tests, the very limited baseline set, and incomplete contextualization. There are also signs of rushed preparation, for example **Table 1** is captioned only as “Table 1: Pc”, and the conclusion ends with “open-ended systems (?)”, suggesting unresolved placeholder text or citation cleanup. These are not mere cosmetic issues. They signal that the paper is not yet assembled carefully enough for archival publication.

11. **The literature positioning is incomplete for the specific shaping-plus-GCRL angle and the open-ended framing.**  
    The introduction cites some standard curriculum and GCRL references, but the paper does not sufficiently position itself relative to broader GCRL surveys, reward shaping work tailored to goal-conditioned settings, or formal discussions of open-ended goal-conditioned learning. This hurts the paper in two ways. First, the contribution can appear more original than it is. Second, the paper’s “bridge to open-ended learning” remains mostly rhetorical because it is not grounded in a stronger conceptual or experimental comparison to that literature.

12. **Results tables are too limited to substantiate robustness claims.**  
    **Table 1** is the only quantitative table, and it reports just one horizon, \(H=16\), for two metrics. But Section 2.5 and Section 3.1 say evaluation used varying horizons \(H \in \{30,20,16,12,10\}\). Where are those results? If the central story is that curriculum helps difficult goals, the dependence on horizon is not optional, it is the point. Reporting a single table at one horizon makes it too easy to overstate a favorable slice. A stronger paper would include a full table across horizons and perhaps across edge/interior partitions, ideally with confidence intervals or paired-seed analysis.

## Questions
1. Please clarify the exact training target and evaluation policy induced by the UVFA. If the model predicts \(V(s,g)\), how is greedy action selection performed? Do you enumerate actions and evaluate successor states via \(V(s',g)\)? The current description in Section 2.2, Section 2.3, and Section 2.5 is too vague, and this is central to understanding the reported success rates.

2. Which quantitative results are correct, those in Section 3.1 or those in **Table 1**? Please reconcile the discrepancy and explain whether they come from different evaluation splits, different checkpoints, or a reporting mistake. This point materially affects my confidence.

3. Can you provide direct evidence for the claim that curriculum reduces approximation error? For example, a shared held-out state-goal regression set with MSE, stratified by edge/interior or by goal difficulty, would substantially strengthen the paper.

4. How exactly are “held-out goals” defined in Section 2.5? Are they disjoint from training goals per seed? Are they sampled uniformly? How many are there, and are they edge-heavy or balanced? A precise description is necessary to assess the generalization claim.

5. Can you disentangle the effect of curriculum from the effect of PBRS? An experiment with sparse terminal reward only, or at least a much weaker shaping signal, would help establish that the reported benefits are not an artifact of the Manhattan-distance shaping already solving most of the problem.

6. Why is the curriculum defined specifically over edge goals? If the underlying principle is selective acquisition of underachieved goals, I would expect either an adaptive success-based sampler or at least a comparison with other hand-crafted notions of difficulty, such as distance-to-start or low empirical success regions not tied to geometry. Can you provide such a comparison?

7. Please report results across all stated horizons in table form. Since the paper emphasizes difficulty and harder-to-reach goals, a full horizon sweep is important, not an optional detail. This is particularly relevant because **Figure 1**, **Figure 2**, and **Table 1** only expose a narrow slice of the evidence.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No specific ethics concerns arise from the paper’s toy GridWorld experiments and methodological scope.

## Soundness Rating
2: fair. The paper’s core empirical observation is plausible, but the methodological description is incomplete, key quantitative results are inconsistent across the manuscript, and the evidence does not adequately support several central claims.

## Presentation Rating
2: fair. The paper is readable at a high level, but there are important clarity problems, especially around the UVFA evaluation protocol, the shaped-return target, and contradictory result reporting. The incomplete table caption and unresolved citation placeholder also hurt presentation quality.

## Contribution Rating
1: poor. The main idea is a limited reweighting study in a toy domain, with modest gains and weak differentiation from standard curriculum intuition. The framing is broader than the actual contribution delivered in the paper.

## Overall Rating
2: Reject, not good enough. The paper has a reasonable intuition and a controlled toy experiment, but in its current form it is too limited, under-specified, and internally inconsistent to meet ICLR standards. The quantitative contradictions, missing direct evidence for approximation-error claims, and narrow experimental scope are the main reasons for rejection.

## Reviewer Confidence
4: confident. I am confident in this assessment based on familiarity with goal-conditioned RL, curriculum learning, and value-function approximation, though some implementation details are missing from the paper and cannot be fully verified from the main text alone.