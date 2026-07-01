## Summary

This paper proposes **GoalRank**, a one-stage generator-only ranking model for recommender systems. The core idea is to use a reward model (trained on real user feedback) to construct a reference policy via *group-relative normalization* — normalizing reward scores within a group of candidate lists — and then train a single large generator to approximate this reference policy. The paper proves an existence theorem (Theorem 1) that a sufficiently large generator-only model can achieve strictly smaller approximation error to the optimal ranking policy than any finite (Multi-)Generator–Evaluator system. Experiments include offline evaluation on three datasets (ML-1M, Amazon-Book, Industry) and large-scale online A/B tests on a platform with >500M DAUs, where GoalRank was deployed to full traffic.

## Strengths

- **Group-relative optimization is a well-motivated practical idea.** The intuition that a biased reward model can still preserve relative ordering within a group when reward gaps are sufficiently large (Section 3.2, lines 142–154) is clear and grounded. The ablation in Table 2 shows that moderate group sizes (8–20) outperform both smaller and larger ones, consistent with the stated rationale. This is a non-obvious training signal construction that the paper both motivates and empirically validates.

- **Online A/B evidence at industrial scale.** The online experiment uses proper traffic partitioning (eight buckets, tens of millions of users per bucket), runs for 14 days, and reports across five business metrics. The improvements (0.09–1.2%) are modest but typical for mature production systems. The fact that GoalRank+MG-E was deployed to full traffic (line 317) is the strongest possible endorsement from the authors' organization.

- **The paper acknowledges a genuine limitation.** The final paragraph (lines 323–327) concedes that a generator-only framework is less flexible than G-E models for adapting to shifting business objectives. This is a real practical concern that many papers omit, and it shows the authors understand the trade-offs of their approach.

- **Comprehensive ablation on the core design choice.** The ablation on group size (Table 2) and on reward model bias (Table 3) directly tests the assumptions underlying the method. These ablations go beyond superficial hyperparameter sweeps and genuinely probe the method's robustness.

## Weaknesses

### Major

1. **Anomalously low AUC for MG-E baselines, unexplained.** In Table 1, MG-E methods (G-3, G-20, G-100) achieve AUC values dramatically lower than every other baseline on all datasets. Examples: on ML-1M, G-3 AUC = 60.73 and G-100 AUC = 76.48 vs. DNN at 86.87 and RankMixer at 92.47; on Industry, G-100 AUC = 75.30 vs. RankMixer at 91.03. An AUC near 60 is barely above random. Crucially, MG-E methods have *competitive or best* H@6/N@6 scores on the same datasets (e.g., G-100 achieves H@6=55.77 on Industry vs. RankMixer's 49.72), so the flaw appears specific to AUC computation rather than a general implementation failure. This suggests either: (a) AUC is computed differently for MG-E (e.g., only scoring the 6 output items rather than the full N=50 candidate set), (b) an evaluation bug, or (c) poor tuning of MG-E's evaluator for the AUC metric. The paper provides no explanation. While GoalRank's victory over MG-E is still supported by H@6/N@6/M@6/F1@6, and the online results provide independent validation, this discrepancy erodes confidence in the overall evaluation rigor.

2. **Large gap between offline and online improvement magnitudes.** Offline relative improvements (Table 1) reach +25.39% H@6 and +29.63% M@6 on Industry. Online improvements (Table 4) are 0.09–1.2%. While some gap is expected, a factor of 20×–450× in relative improvement magnitude suggests the offline evaluation may not measure what the paper claims. The offline ground-truth construction — "the last six interactions in each user's historical sequence" (line 202) — treats the chronological tail of user behavior as the optimal ranking. This conflates user behavior (which depends on the deployed recommender) with ground-truth preference, a known form of exposure bias. The paper does not discuss this limitation or provide any analysis bridging the offline-to-online gap (e.g., per-user improvement distributions, intermediate proxy metrics). This gap does not invalidate the online findings, which are independently strong, but it raises questions about what the offline numbers actually represent.

### Minor

3. **Theorem 1 is about representational capacity, not learnability, and its connection to the practical method is not fully bridged.** Theorem 1 states an existence result: a larger generator has sufficient capacity to approximate the optimal policy better than a finite mixture of small generators. This is a capacity argument (essentially: a bigger model can simulate an ensemble). The paper then treats this as motivation for the proposed training method, but the theorem says nothing about whether the *specific training objective* (group-relative optimization) actually realizes this capacity advantage. The leap from "a larger model *can* approximate π* better" to "our method *does* approximate π* better" is not bridged by the theory, which concerns representational capacity rather than optimization or generalization.

4. **The "generator-only" framing overstates the training-time independence.** The paper repeatedly characterizes GoalRank as a "generator-only" paradigm (title, abstract, lines 9, 31, 70, 122, 321), contrasting it against G-E models that use an evaluator at inference. At inference, this is accurate — Equation 6 shows the generator alone produces the output. However, during training, GoalRank depends critically on: (a) a separately trained reward model $\hat{r}$ (line 160), (b) an auxiliary set of ranking policies $\mathcal{M}$ (line 180), and (c) the reward model's scores to construct the reference policy (Equation 4). The method is better described as a distillation or knowledge-transfer method that uses a reward model and auxiliary rankers during training to produce a generator that is evaluator-free at inference. This is a valuable contribution on its own terms, but the framing invites scrutiny that the method does not fully survive. The paper should clarify this asymmetry.

5. **Scaling law demonstration is limited.** Figure 3 shows improving metrics from 1M to 0.1B parameters, but on only one dataset (Industry-0.1B) and one architecture. True scaling laws typically involve fits to power-law functions, multiple architectures, and multiple datasets. The evidence supports "performance improves with model size" more than it supports "scaling laws" as the term is used in the literature.

6. **Missing details about the reward model and auxiliary policy set in the main paper.** The reward model is central to the method — its quality determines the reference policy — but the main paper defers all details (data scale, architecture, training objective, evaluation of $\hat{r}$ itself) to Appendix B. Similarly, the auxiliary policy set $\mathcal{M}$ (used to construct training groups) is described only as "heuristic methods and lightweight neural models" (line 180), with details deferred to Appendix C. The paper should at minimum summarize the reward model's accuracy and the composition of $\mathcal{M}$ in the main text, as these directly affect the method's practical requirements and reproducibility.

### Trivial

7. The reproducibility statement says "we will release the implementation and training code at" with no URL provided (line 329). This should be completed.

## Nice-to-Haves

- A computational cost comparison (training FLOPs, inference latency, parameter count) between GoalRank and the MG-E baseline would help practitioners evaluate the trade-off. The paper focuses on ranking quality but does not discuss that GoalRank requires training a reward model, maintaining auxiliary policies, and running all auxiliary policies for group construction.
- Reporting confidence intervals or explicit p-values for the online metrics (beyond "All results are statistically significant") would strengthen the presentation.
- The theoretical condition in Equation 3 (sufficiently large reward gaps within a group) is stated but not quantified — e.g., how large must $\sigma^*$ be relative to the bias magnitude? A more principled analysis of what "sufficiently large" means would strengthen the theoretical motivation.

## Removed Points

These points from the input review were removed with justification:

- *"The statement 'all baselines share exactly the same evaluator (reward model) as GoalRank' is misleading"* — Removed because this is factually correct (same reward model is shared). The asymmetry of when it is used (training vs. inference) is inherent to the compared paradigms and does not constitute unfairness. If anything, the G-E baselines have the advantage of using the evaluator at inference time, which is their design.
- *"The paper implicitly inherits the claim about scaling laws for recommendation models without critical scrutiny"* — Removed as a generic framing critique without specific evidence of error.
- *"Without seeing the proof (deferred to Appendix A), I cannot fully evaluate the result"* — Removed per the hard rule about parser-stripped appendix content.
- *Various formatting/presentation nitpicks* — Removed per hard rules.
- *"Missing appendix" and "key technical details are not visible in the main paper"* — Removed per the rule that the parser strips these sections; they exist in the original submission.
- *"The paper does not discuss training cost"* — Moved to Nice-to-Haves as a non-critical suggestion.

## Novel Insights

The harsh critic correctly identifies that the paper's practical contribution — group-relative normalization of a reward model to supervise a generator — is genuinely novel and well-motivated. However, the critic also surfaces a tension that the paper glosses over: the method trains a "generator-only" model using components (reward model, auxiliary rankers) that closely mirror the evaluator and multiple generators of the G-E paradigm it claims to supersede. This is not a fatal contradiction but a framing choice that the paper should address more honestly. The reviewer also correctly notes that the huge offline-to-online gap warrants discussion the paper does not provide — this is a real opportunity for improvement, not merely a criticism.

## Suggestions

1. **Explain the MG-E AUC computation.** Clarify how AUC is computed for MG-E methods. If it only scores items in the output lists (L=6) rather than the full candidate set (N=50), state this explicitly and either recompute AUC over the full candidate set or explain why the current computation is meaningful. This single fix would remove the largest source of reviewer skepticism.

2. **Add a paragraph bridging offline and online results.** Discuss why offline improvements are an order of magnitude larger than online improvements. A simple analysis (e.g., correlation between offline and online metrics at the user or bucket level) would go a long way.

3. **Reframe the narrative around the training/inference distinction.** The paper should clearly state that GoalRank is evaluator-free at inference but uses a reward model and auxiliary policies during training. Rename the paradigm "evaluator-free inference" or "reward-distilled generator" rather than "generator-only" to avoid the implication that no evaluator-like component is involved at any stage.

4. **Provide a brief summary of the reward model and $\mathcal{M}$ in the main paper.** Even 3–4 sentences about the reward model's accuracy and the composition of the auxiliary policy set would substantially improve reproducibility and reader confidence.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>