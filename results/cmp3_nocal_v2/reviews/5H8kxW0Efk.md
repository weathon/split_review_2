Now let me write the final consolidated review.

## Summary

This paper proposes neural network parameterized Ising machines (NPIM), applying algorithm unrolling to dynamical Ising machines for NP-hard combinatorial optimization (Max-Cut/Ising). The continuous-time update rule of an Ising machine is replaced by a small MLP whose weights are learned via zeroth-order evolutionary optimization. Two variants are presented—cNPIM (continuous coupling) and dNPIM (discrete coupling). The method is evaluated on neural CO benchmarks (Table 1) and G-set Ising machine benchmarks (Table 2), achieving competitive results on most problem categories.

## Strengths

- **Novel methodological combination.** The paper connects algorithm unrolling to dynamical Ising machines, a connection that (to the best of the paper's knowledge) has not been made for NP-hard combinatorial optimization (Section 2.3, line 35). Parameterizing the update function *F* of an Ising machine with a small MLP and learning its weights from data cleanly bridges two previously separate literatures.

- **Well-motivated choice of optimizer.** The use of zeroth-order evolutionary optimization over backpropagation or policy gradient is specifically justified (Section 2.4, lines 39–40): long dynamical trajectories make gradient estimation via backpropagation (vanishing/exploding gradients) or policy gradient (noisy credit assignment over many steps) impractical. This is not a generic rationale; it engages with the actual difficulty of the training problem.

- **Interpretability analysis in a simplified setting.** Section 4.1 and Figure 2 show that a single-layer network (M=1, Tc=10) first learns greedy steepest descent (all weights negative) and then develops positive weights that the authors interpret as "momentum." Whether or not one accepts the momentum analogy fully, this demonstrates that the learned dynamics are inspectable at the parameter level, which is a hallmark of successful algorithm unrolling.

- **Competitive results across two evaluation traditions.** The method is tested against both neural CO approaches (Table 1) and classical Ising machine algorithms (Table 2). On 4 out of 5 neural CO benchmarks, dNPIM achieves a better average objective value (Table 1), and on 4 out of 5 G-set categories, dNPIM achieves the best median TTS (Table 2).

## Weaknesses

### Major

- **G-set comparison is between a distribution-trained algorithm and general-purpose baselines, which weakens the "SOTA" claim.** For the G-set (Table 2, line 170), dNPIM is trained on synthetic instances generated to match each G-set category's graph parameters—hundreds of distribution-matched training examples. The baselines (CAC, CFC, dSBM) are general-purpose dynamical systems. The paper notes that baseline parameters are "also tuned for each instance type" (line 170), but tuning a handful of hyperparameters is qualitatively different from training on distribution-matched instances. This asymmetry matters because a learned method *should* outperform a handcrafted one when given training data from the test distribution. The headline claim that dNPIM "outperforms the existing Ising machine state-of-the-art" (line 170) is therefore weaker than it appears and should be scoped to specify the training advantage. The more informative comparison would pair learned baselines (e.g., Sanokowski et al.'s methods, which appear in Table 1) against dNPIM under the same training-data conditions.

- **Table 1's "top 30" methodology makes the quality and time comparisons uninterpretable as reported.** dNPIM results are labeled "dNPIM (top 30)" (line 183), meaning the best of 30 parallel trajectories is reported. The baselines (DiffUCO, SDDS) report mean ± std from what appear to be single-trajectory runs. This gives dNPIM a quality advantage (cherry-picking the best of 30) while the time metric is muddied: on large instances, dNPIM takes 1:20 vs. 0:03 for DiffUCO and SDDS. The paper attributes this to dense vs. sparse matrix operations (lines 168–169), which makes the time comparison implementation-dependent. Additionally, dNPIM reports no error bars or variance in Table 1, while baselines all include ± ranges. Together, these issues prevent the reader from assessing whether dNPIM's reported quality advantage is real or an artifact of the evaluation methodology.

### Minor

- **Tension between aggregate "SOTA" claims and per-instance performance.** The introduction claims "state-of-the art performance on many commonly used benchmarks" (line 13), and the conclusion repeats this (line 201). However, Section 4.5 (lines 156–160) shows that cNPIM struggles on the hardest instances relative to CAC, and Figure 3b shows many points above the diagonal (cNPIM slower than CAC). The abstract uses the more measured "competitive performance" (line 9). This inconsistency in framing—aggregate metrics vs. per-instance behavior—should be reconciled. The method achieves strong median performance but does not consistently dominate on individual instances, which the introduction and conclusions should reflect.

- **Bootstrapping requirement limits the "scalable" claim.** The paper states that "training a network from scratch at the larger problem size (N=500) is not possible" (line 148), requiring pre-training on N=100 and fine-tuning. This is a practical limitation that the paper acknowledges but does not analyze—is it a fundamental limitation of the zeroth-order optimizer or of the architecture? Since the abstract claims the method "is able to learn efficient and scalable algorithms," this limitation on training scalability should be discussed more prominently.

- **No error bars or variance reported for dNPIM in Table 1.** While DiffUCO and SDDS report ± ranges from multiple runs, dNPIM gives a single point estimate (Table 1). This makes it impossible to assess whether the reported quality improvements are statistically significant.

- **No discussion of training cost.** The paper reports inference cost (TTS, wall time) but does not report how long training takes, how many instances are needed, or how sensitive performance is to training set size. Since the method requires training and fine-tuning, a reader cannot evaluate the cost-benefit trade-off.

### Trivial

- **The activation function choice ($f_{\text{nl}}(x) = x + \tanh(x)$) is not motivated.** The odd-symmetry rationale is given for omitting biases (line 79), but the specific choice of activation is not discussed. A brief justification would be helpful.

## Nice-to-Haves

- **Add an ablation that isolates the value of learning directly.** For a fixed architecture (e.g., the ~50-parameter network that saturates performance), compare three conditions: (a) learned weights, (b) random weights, (c) weights designed to approximate a known Ising machine (e.g., CAC's dynamics). This would show how much of the gain comes from learning vs. the dynamical system formulation itself.

- **Report single-trajectory dNPIM results** alongside the "top 30" results in Table 1, so readers can assess the quality-time trade-off without relying on the "top 30" methodology.

- **Provide a comparison against M=1 (time-independent weights) on the G-set** to clarify whether the temporal basis expansion is essential for the main empirical results, building on the analysis in Section 4.1.

- **Include a sensitivity analysis on training distribution mismatch** for the G-set: how well does the synthetic training distribution match the actual G-set instances, and does performance degrade gracefully when the match is imperfect?

## Removed Points

- Criticism about the Section 2.3 claim ("algorithm unrolling has not been explored for NP-hard CO") being too strong. *Reason: The paper already qualifies with "to the best of our knowledge" and explicitly notes the ILP exception. This is standard academic hedging.*
- Criticism about missing reward function details in Section 3.4 (deferred to Appendix F). *Reason: Per the rules, weaknesses about content in parser-stripped appendices are removed; the appendix exists in the original submission.*
- Criticism about G-set training instance generation details (deferred to Appendix I). *Reason: Same as above—appendix-stripping issue.*
- Concern about the Section 2.3 claim potentially missing related work on learned iterative heuristics. *Reason: Per the rules, missing-related-work criticisms are not permitted without external sources to confirm existence.*
- Strength 4 (competitive empirical results across two traditions) is kept but weakened from the input review's framing. *Reason: The results are genuinely competitive, but the "SOTA" framing is overstated given the comparison asymmetries identified above.*
- Several suggestions from "Strengthening the Paper on Its Own Terms" are moved to Nice-to-Haves since they are constructive recommendations rather than identified weaknesses.

## Novel Insights

The harsh reviewer insightfully notes that the core tension in this paper is between the value of its genuinely novel methodological contribution (algorithm unrolling + Ising machines + zeroth-order optimization) and the overstatement of its empirical claims. The method is clearly innovative and the experiments show it works, but the headline claims of "state-of-the-art" performance are supported by comparisons that systematically favor the proposed method (distribution-matched training vs. general-purpose baselines; best-of-30 trajectory selection vs. single-trajectory baselines). This tension—between a solid contribution and an inflated empirical narrative—is the central issue that the authors should address, not by weakening the method but by scoping the claims precisely. None of the comparison issues invalidate the core idea; they merely require more careful framing and a few additional experiments to disentangle the effects of learning from the effects of the evaluation protocol.

## Suggestions

1. **Separate quality and time dimensions in Table 1.** Report single-trajectory dNPIM performance alongside "top 30," with error bars, so the comparison is on equal footing.
2. **Scope the Ising machine comparison explicitly.** Replace "outperforms the existing Ising machine state-of-the-art" with "achieves better median TTS on 4 of 5 G-set categories when trained on distribution-matched data and compared to algorithms with parameter tuning per instance type."
3. **Add the learning-ablations suggested above** (learned vs. random vs. hand-designed weights for the same architecture) to demonstrate that the improvements come from learning, not just from the dynamical system formulation.
4. **Report training cost** (wall time, instance counts, sensitivity to training set size) so readers can assess the practical cost of the approach.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>