---
job_id: 0c5bcd5e-019a-4149-8f75-4775b64dedba
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: 0lW2UBiEWN.pdf
paper: Mesa and Mask: A Benchmark for Detecting and Classifying Deceptive Behaviors in LLMs
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope as a datasets/benchmarks and AI safety evaluation submission for LLMs.

## Minimum Quality
Pass ✅. The paper contains the expected components for a benchmark paper, including abstract, introduction, related work, methodological framing, dataset construction, experiments/results, and conclusion/limitations. I have substantial concerns about construct validity, evaluation design, and strength of evidence, but these are review-time weaknesses rather than desk-rejection issues.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find hidden prompts, concealed reviewer-targeting instructions, or other obvious manipulation attempts in the provided paper content.

# Expected Review Outcome:
## Summary
This paper introduces MESA & MASK, a benchmark for diagnosing deceptive behaviors in LLMs by comparing model reasoning and outputs under a neutral context (MESA) and a pressure-inducing context (MASK). The benchmark contains 2,100 instances spanning six professional domains and six deception categories, and the paper reports evaluations on more than twenty open- and closed-source models. The proposed framework uses an LLM judge to compare baseline and pressured responses and assigns instances to a four-quadrant taxonomy including consistent behavior, superficial alignment, deception tendency, and explicit deception.

## Strengths
The paper tackles a timely and important problem. The community does need better tools for evaluating strategic behavioral shifts in LLMs beyond standard factuality or refusal benchmarks, and the neutral-vs-pressure comparative framing is an intuitively appealing way to probe brittleness of alignment.

The benchmark scope is fairly broad. Covering six domains and six deception types is useful, and the balance statistics in **Figure 4** show that the dataset is at least numerically well distributed across categories and domains, which is preferable to many narrowly scoped safety benchmarks. The paper also gives enough concrete scenario examples, especially in Appendix E and the full worked example around **Table 6**, to make the intended task style understandable.

I found **Figure 2** helpful for understanding the intended pipeline and behavioral taxonomy. In particular, panel (a) makes the MESA-vs-MASK comparison setup immediately legible, and panel (b) clarifies the four-way classification logic. For a benchmark paper, having the evaluation abstraction visualized this early is a genuine clarity advantage.

The authors make a reasonable effort toward reproducibility. The paper describes data generation, iterative refinement, human annotation, and judge validation, and it provides explicit prompt templates in the appendix. Compared with many safety benchmark papers that stay at a high level, this submission is unusually transparent about the operational details of scenario construction and LLM-judge prompting.

The empirical sweep is large enough to be interesting. **Table 1** provides a wide cross-model comparison and does reveal heterogeneous behavior across families, including notable variation among proprietary systems and among distilled vs non-distilled open models. Even if I am not fully convinced by the causal interpretation, the raw descriptive results are potentially useful to practitioners who want a stress-test for alignment brittleness.

The worked side-by-side comparison in **Table 6** is also a strong pedagogical element. It concretely illustrates the kind of behavioral shift the benchmark is trying to capture, and it is much more convincing than abstract verbal descriptions alone.

## Weaknesses
I have several substantial concerns, mostly about construct validity, evaluation circularity, and over-interpretation of the empirical results.

1. **The paper’s central construct, “deception,” is not operationalized as cleanly as the text suggests, especially because it leans heavily on chain-of-thought as evidence of internal intent.**  
   This issue appears throughout **Sections 3.1, 3.2, and 4.3**. The framework treats CoT as “an observable proxy” for motivational and control-mode shifts (**Page 4, Section 3.1**), and the final classification depends directly on reasoning consistency and output consistency. That is a strong assumption. A model’s exposed reasoning is not a validated window into latent intent, and the paper does not provide evidence that the elicited CoT faithfully tracks the underlying policy rather than post hoc rationalization, prompt-sensitive narration, or provider-specific reasoning style. This matters because the benchmark’s headline claim is not merely that outputs change under pressure, but that it can distinguish “genuine deception,” “deceptive tendencies,” and “superficial alignment.” Without stronger justification for using visible CoT as a reliable latent variable, those labels look sharper than the evidence supports.

2. **The benchmark’s dependence on reasoning traces substantially limits usability and fairness across models.**  
   The core formalization in **Section 3.2** uses \((C_{me}, R_{me})\) and \((C_{ma}, R_{ma})\), and the judge prompts in the appendix explicitly compare reasoning chains as first-class evidence. But many frontier APIs do not expose faithful internal reasoning, expose summarized reasoning, or expose reasoning in provider-specific formats. This means the benchmark is partly evaluating the availability and style of surfaced reasoning, not just behavior. The paper should be much clearer about whether the evaluated models all expose comparable CoT and how the method would work for models that do not. As written, this is a major practical limitation for a benchmark presented as general “infrastructure” for deception diagnosis.

3. **The MESA-vs-MASK intervention is not as controlled as the paper claims, because the pressure prompt often changes the effective objective, not merely the context.**  
   This is the most important methodological concern. The paper repeatedly argues that the system prompt introduces “implicit environmental pressure” without explicit instructions to deceive, thereby isolating strategic shifts from instruction following. I do not think the paper demonstrates that. In the examples, the pressure condition often changes the reward structure so strongly that different outputs are expected from straightforward goal conditioning alone. **Figure 1** is illustrative here: the MASK condition tells the model that hyper-personalization triggers oversight and reduced autonomy. Choosing a safer-looking strategy under that condition can be read as complying with a changed institutional incentive, not necessarily “deception” in the stronger sense claimed by the paper. Likewise, many appendix scenarios define very specific professional stakes and hidden costs; that can easily induce ordinary objective re-optimization. The paper needs a sharper argument for why the measured deviation reflects deception rather than rational adaptation to a changed prompt-specified utility.

4. **There is a serious circularity concern in dataset filtering.**  
   In **Appendix B.4, Stage 2** (**Page 21**), scenarios are retained if at least two of three validation models display detectable shifts under the MESA-MASK evaluation framework. This is a nontrivial problem. Even though the authors say this step is “not used to select scenarios” but to validate them, it still filters the benchmark based on whether the proposed evaluation machinery can detect a shift. That makes the benchmark partly self-fulfilling. It biases the dataset toward instances that elicit the benchmark’s target phenomenon under the same style of judgment, and likely toward the behaviors of the three validation model families specifically. For a benchmark paper, this weakens claims of neutrality and external validity.

5. **The evaluation metric design is underspecified and somewhat idiosyncratic, and the main paper does not provide enough evidence that the thresholds are stable.**  
   In **Section 5.1** the paper defines deception rates using \(Q_1\) and \(Q_2\), but these symbols are not formally introduced in the main paper in a way that makes the mapping to the four quadrants fully explicit. More importantly, the binary classification depends on thresholding 7 reasoning indicators and 8 output indicators, with inconsistency declared at 5/7 and 6/8 respectively (**Appendix C.2, Pages 21-22**). This is effectively a hand-designed decision rule. The authors report agreement statistics, which is good, but the validation set is only 300 response pairs and the main paper omits breakdowns by deception type, domain, or model family. A benchmark that hinges on these thresholds should either report sensitivity analyses in the main paper or avoid presenting the resulting categories as especially robust. Mathematically, the derived stability score
   \[
   S = \frac{D@k}{D@1}
   \]
   is also somewhat awkward. Since \(D@k\) here means “deceptive across all \(k\) samples” rather than a standard top-\(k\) notion, \(S\) conflates persistence with the strictness of an all-samples criterion, and the paper provides no uncertainty intervals for any of these estimates.

6. **The paper over-interprets descriptive correlations in the experiments as if they support architectural or training-mechanism conclusions.**  
   This is especially visible in **Section 5.3** and **Figure 5**. The discussion attributes patterns to distillation, foundation architecture, and MoE capacity, but the comparisons are highly uncontrolled. The authors themselves briefly acknowledge parameter mismatch in the MoE-vs-dense discussion, yet still make broad claims such as “architectures with vast parameter spaces... correlate with a higher propensity for strategic behaviors” (**Page 9**). From **Table 1** and **Figure 5**, one can say there are observed differences. One cannot confidently infer the causes without matched training data, matched instruction tuning, matched safety interventions, and some statistical treatment of variance. Right now the causal language is doing too much work.

7. **The empirical section is missing key baselines and ablations needed to justify the proposed design choices.**  
   For example:
   - There is no direct comparison to a simpler “pressure-only output deviation” metric without CoT.
   - There is no ablation on using a single MESA sample versus the consensus MESA aggregation.
   - There is no main-paper comparison against a benchmark that uses only final outputs, which would test whether CoT actually adds diagnostic value.
   - There is no comparison against prior honesty/deception evaluations on overlapping scenarios.  
   Since the method’s main idea is comparative diagnosis, these ablations are central, not optional.

8. **The “first benchmark” and positioning claims are overstated relative to the cited literature.**  
   The abstract says this is “the first benchmark designed for the differential diagnosis of LLM deception.” The introduction also positions the work against MASK and other deception evaluations. Even taking that wording literally, the novelty is narrower than the paper sometimes implies. The related work already cites multiple deception benchmarks and pressure-based studies. What seems new here is a particular combination of pressure contrast, domain breadth, and four-quadrant classification, not the existence of deception benchmarking per se. The paper would be stronger if it made a more careful originality claim and explicitly disentangled what is new in dataset design versus what is inherited from existing comparative-evaluation ideas.

9. **Some quantitative results look striking, but the paper does not provide sufficient uncertainty quantification or significance analysis.**  
   **Table 1** reports many rates to two decimal places across 22 models and six categories, and **Figure 6** discusses small changes from fine-tuning, such as a 2.7-point drop for Qwen3-4B. Without confidence intervals, repeated runs, or statistical tests, it is hard to know which differences are meaningful. This matters particularly because the paper draws substantive conclusions about safety interventions from modest deltas. For a benchmark paper, descriptive statistics alone are not enough when the interpretation is this strong.

10. **The presentation is decent overall, but some of the figures and tables are more decorative than analytically useful in the main paper.**  
   **Figure 4** is a good example. The table on the right is the informative part; the pie-like chart on the left adds little analytical value beyond signaling balance. By contrast, the paper would benefit more from a figure showing judge-human agreement by category, a sensitivity analysis over thresholds, or an ablation of MESA aggregation. Similarly, **Figure 3** is visually busy and summarizes a long pipeline, but it does not reveal which stages are empirically bottlenecks or which quality checks most affect final benchmark composition.

11. **The claim that the method disentangles deception from hallucination and instruction following is not convincingly established.**  
   This is a recurring claim in the abstract, introduction, and **Section 2.2**, but the evidence is mainly design intent rather than empirical validation. The worked example in **Table 6** does support a sycophancy-like case, but that is one carefully chosen illustration. The paper would need adversarial controls where pressure prompts are present but deception is not rational, or cases where hallucination produces output shifts without deceptive incentives, to really support disentanglement.

12. **The safety fine-tuning analysis in Section 5.4 is too limited to support the broader framing.**  
   The paper uses two Qwen models, one dataset, and apparently a single training trajectory per model. The authors do acknowledge this is a limited case study, which I appreciate. Still, the section title and surrounding discussion give the impression of a more general takeaway than the setup warrants. **Figure 6** is readable and shows the reported trend, but the evidence base is thin.

## Questions
1. **Can the authors provide a main-paper ablation showing how much diagnostic value comes from CoT versus final-output comparison alone?**  
   A concrete comparison between: (i) output-only MESA/MASK deviation, (ii) CoT-only deviation, and (iii) full MESA & MASK classification, would significantly clarify whether the reasoning channel is necessary or merely convenient.

2. **How exactly were reasoning traces obtained for each evaluated model family, and were they comparable in content and format?**  
   This is crucial for fairness. If some models expose full reasoning while others expose summarized or policy-filtered reasoning, the benchmark may not be comparing like with like.

3. **Please quantify sensitivity to the judge thresholds.**  
   In particular, how much do final model rankings and category rates change if the reasoning threshold is 4/7 or 6/7, and if the output threshold is 5/8 or 7/8? A stability analysis here would materially increase my confidence.

4. **Can the authors address the circularity introduced by Stage 2 validation in Appendix B.4?**  
   I would like a clearer justification for why retaining instances that already show detectable shifts under the same framework does not bias the benchmark toward the proposed method.

5. **Can the authors separate “deception” from “objective re-optimization under altered incentives” more rigorously?**  
   One productive way would be to include a set of control instances where the pressure prompt changes stakes but should not make deception instrumentally useful. If the method still flags many of those, that would indicate weak specificity.

6. **For Table 1, can the authors report uncertainty estimates and perhaps model-family-level aggregates with error bars?**  
   This matters for interpreting several of the cross-model differences and especially the safety fine-tuning deltas in **Figure 6**.

7. **What is the practical scope of the benchmark for models without exposed CoT?**  
   If the answer is “limited,” that limitation should be made much more explicit in the main paper. If the answer is “still usable,” the paper should explain the fallback protocol.

## Flag For Ethics Review
- Yes, Potentially harmful insights, methodologies and applications

## Details Of Ethics Concerns
The benchmark is explicitly designed to elicit and classify deceptive behavior in high-stakes domains including healthcare, law, military, and finance (**Section 4.1, Page 5**). While the intended use is diagnostic, releasing detailed pressure prompts and scenario templates could also help users stress-test or even induce deceptive behaviors more effectively in deployed systems. The paper does include an ethics statement and describes screening, which is good, but the deployment-risk side is real enough that I think an ethics check is warranted.

## Soundness Rating
2: fair. The paper has a plausible benchmark idea and a substantial experimental effort, but the central technical claims about diagnosing deception are only partially supported due to construct-validity issues, judge dependence, and limited ablations.

## Presentation Rating
2: fair. The paper is readable and includes helpful figures such as **Figure 2** and a useful worked example in **Table 6**, but several key assumptions and decision rules are not sufficiently clarified in the main paper, and some figures/tables are more illustrative than analytically decisive.

## Contribution Rating
2: fair. The problem is important and the benchmark may be useful, but the current evidence does not convincingly establish that the framework measures the strong behavioral categories it claims to measure.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted. The topic is important and the benchmark may prove useful, but I do not think the current paper makes a sufficiently rigorous case that MESA & MASK cleanly diagnoses deception rather than broader prompt-conditioned behavioral shifts.

## Reviewer Confidence
4: confident. I am familiar with LLM safety/deception evaluation work and checked the main methodology, metrics, tables, figures, and judge formulation carefully, though some confidence-limiting details reside outside the main paper.