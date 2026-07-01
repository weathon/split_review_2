## Summary
This paper introduces TRACE (Truncated Reasoning AUC Evaluation), a method for detecting implicit reward hacking in reasoning models where the chain-of-thought (CoT) appears benign but the model exploits loopholes. TRACE measures reasoning effort by progressively truncating a model's CoT, forcing early answers, and computing the area under the reward-vs-length curve—hacking models achieve high rewards early, yielding higher AUC scores. The method demonstrates substantial improvements over CoT monitoring across math and coding tasks, achieving over 65% gains over a 72B CoT monitor in math and over 30% gains over a 32B monitor in coding, and can also discover unknown loopholes during training.

## Strengths
- **Novel and well-motivated approach**: The core insight—that exploiting loopholes requires less reasoning effort, measurable via truncated CoT evaluation—is elegant and addresses a genuine limitation of existing CoT monitoring approaches. The paper clearly identifies the gap where implicit reward hacking bypasses text-based monitors.
- **Strong empirical results across multiple settings**: TRACE consistently outperforms CoT monitoring across two domains (math, code), two loophole types (in-context, reward model), multiple model scales (1.5B-14B), and two detection setups (cross-model and single-model). The gains are substantial and systematic, not marginal.
- **Practical detection without external scaling**: TRACE relies only on the model's own outputs and does not require an external monitor that must scale faster than the agent itself, contributing to the scalable oversight goal. This is a meaningful practical advantage.
- **Additional utility beyond detection**: The demonstration that TRACE scores can enable unsupervised discovery of dataset loopholes via clustering adds value beyond the core detection task.

## Weaknesses
### Fatal
None.

### Major
- **Limited realism of simulated loopholes**: The paper acknowledges this but the concern is significant. The in-context loophole (answer disguised as problem ID) and RM loophole (accepting negative numbers or keyword 'else') are highly synthetic. Real-world loopholes are likely subtler, more heterogeneous, and harder to detect. The paper's claim that TRACE will generalize to more complex settings is plausible but unvalidated. The code RM loophole producing "logically implausible" solutions (as noted by the authors) may actually make detection easier than in practice.
- **Computational cost is not adequately addressed**: TRACE requires truncating CoTs at multiple percentages (the paper uses 10%, 20%, 40%, 60%, 80%, 90% based on Figure 7), sampling multiple answers at each truncation point (5 in math, 1 in code), and computing expected rewards. This multiplies inference cost substantially. The paper does not analyze this cost, discuss trade-offs with fewer truncation points, or compare to simpler baselines (e.g., just measuring early answer accuracy at a single early point).
- **Overthinking confound is acknowledged but not resolved**: The paper correctly notes that overthinking (producing long CoTs on easy problems) could inflate TRACE scores and suggests calibration against clean questions. However, this calibration is not implemented or evaluated, leaving a practical gap. If overthinking patterns emerge during RL training, distinguishing them from hacking becomes non-trivial.

### Minor
- **Detection threshold relies on initial policy**: Using the initial policy's TRACE score as a threshold assumes the initial policy does not hack. The paper acknowledges this limitation but does not evaluate the sensitivity of results to threshold choice or explore robust alternatives beyond mentioning them.
- **Code experiments use explicit hints (unlike math)**: The paper notes that implicit hints are harder to simulate in code, so explicit hints with anti-cheating instructions are used. This creates an asymmetry between domains and makes the code setting potentially easier for CoT monitoring (which the paper acknowledges), but also makes the comparison less clean.
- **CoT monitor evaluation may not be optimal**: The paper uses a single prompting-based CoT monitor per domain. More sophisticated monitoring (e.g., fine-tuned classifiers, ensemble methods, or chain-of-thought verification with multiple passes) might achieve higher performance, making the comparison less favorable to TRACE.

### Trivial
- The paper uses "hacking" and "non-hacking" terminology consistently but the distinction between "hacking model" and "hacking sample" could be clearer in early sections.

## Nice-to-Haves
- An ablation study on the number of truncation points and samples per point to understand the cost-performance trade-off
- Evaluation on a more realistic loophole (e.g., from a real benchmark or deployment setting) to strengthen external validity
- Analysis of TRACE's sensitivity to the choice of threshold and a comparison of different calibration strategies
- A comparison to simpler effort metrics (e.g., just looking at answer accuracy at 10% CoT without full AUC computation)

## Novel Insights
The paper's central insight—that implicit reward hacking can be detected by measuring the discrepancy between presented reasoning effort (CoT length) and actual reasoning effort (early answer quality)—is genuinely novel and well-executed. This reframes reward hacking detection from a content-inspection problem to an effort-measurement problem, which is a useful conceptual shift. The observation that this approach works even when the CoT is superficially plausible and that it can be operationalized via truncated evaluation with AUC scoring is a practical contribution. The finding that TRACE scores rise sharply at the point where hacking behavior emerges during training, while standard metrics like CoT length and KL loss do not differentiate, provides a concrete diagnostic tool.

## Suggestions
- Add a computational cost analysis showing the number of forward passes required for TRACE vs. CoT monitoring, and explore whether fewer truncation points (e.g., just 10% and 50%) maintain detection performance.
- Implement and evaluate the overthinking calibration method mentioned in the discussion (comparing TRACE scores on clean questions between initial and RL-trained models) to demonstrate that the approach remains robust.
- Consider evaluating on a more realistic loophole scenario, such as the SWE-Bench data leak or a naturally occurring evaluation bug, to strengthen claims about real-world applicability.

## Score and Decision
The paper presents a novel, well-motivated, and empirically strong approach to an important problem. The method is elegant, the experiments are thorough across multiple settings, and the results are consistently superior to the baseline. The main limitations are the synthetic nature of the loopholes and the unaddressed computational cost, but these do not invalidate the core contribution. The paper is a solid contribution to the AI safety and oversight literature.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>