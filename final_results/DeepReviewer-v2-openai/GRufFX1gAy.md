## Summary
This paper introduces InnoGym, a benchmark and evaluation framework for assessing the innovation potential of AI agents. The core idea is to move beyond correctness-only evaluation by defining two complementary metrics: Performance Gain (G), measuring improvement over the best-known solution, and Novelty (N), capturing methodological dissimilarity from prior approaches. The benchmark includes 18 improvable tasks from engineering and scientific domains, curated via a two-stage filtering process from 197 competition items. A companion execution environment (iGym) provides reproducible, long-horizon agent evaluation.

The authors evaluate three agent frameworks (MLAB, CodeAct, AIDE) on 10 tasks using DeepSeek-v3.1, with additional ablation on CirclePacking varying time budget, foundation model, and sampling temperature. Results show that no agent surpasses human SOTA; all performance gains are negative. MLAB achieves the highest average novelty (56.55) and least negative gain (-24.32), while CodeAct and AIDE lag. A key claimed finding is that agents produce novel approaches but lack the robustness to translate them into performance gains.

The paper tackles an important and timely problem—current agent benchmarks do conflate solution quality with methodological originality. The formal framework (P,S,V,D) is well-structured, and the task curation process is documented in detail. However, several significant issues limit the paper's current contribution: the novelty metric relies on an unvalidated LLM-as-judge pipeline, the empirical comparisons are confounded by uneven task success rates and best-of-3 reporting, and the central "primacy of robustness" narrative is partially contradicted by the paper's own aggregate data. External novelty verification is deferred due to Retrieval-Disabled Mode.

**Overall assessment:** The paper presents a valuable conceptual framework and a solid benchmark infrastructure, but the empirical validation and metric validation need substantial strengthening before the claimed contributions are fully supported.

## Strengths
**1. Important and timely problem formulation.** The paper identifies a genuine gap in agent evaluation: existing benchmarks measure whether an answer is correct or how well a solution performs, but they do not distinguish between methodologically novel approaches and straightforward refinements. This distinction matters for scientific progress, where the originality of a solution can be as important as its raw performance. The formalization of a task as a quadruple (P,S,V,D) and the decomposition of innovation into Performance Gain (G) and Novelty (N) is a clean, principled foundation.

**2. Rigorous task curation pipeline.** The authors invest significant effort in collecting 197 tasks from diverse competition sources and filtering them through resource-availability checks, evaluator validation, domain balancing, and standardization. The resulting 18 tasks span multiple domains (computational, biological, financial, mathematical, physical) and hardware profiles (CPU, GPU). The detailed documentation of the curation process (Fig. 2) sets a high standard for reproducibility.

**3. Rich ablation experiments on CirclePacking.** The controlled experiments varying execution time, foundation model, and sampling temperature provide useful insights into agent behavior. The complex-plane representation combining G and N into a joint visualization is a creative and informative way to track the innovation trajectory. The temperature analysis revealing a trade-off between novelty and performance is a concrete, actionable finding for practitioners.

**4. Unified execution environment (iGym).** Providing a shared SDK that abstracts away environment differences is a practical contribution that strengthens the reproducibility of cross-framework comparisons. The design addresses real engineering challenges (robust recovery, concurrency, tool management) that are often overlooked in benchmark papers.

**5. Transparent comparison table (Table 1).** The explicit comparison of iBench against seven prior benchmarks along dimensions (source, domain, reference solutions, difficulty, compute profile, performance evaluation, novelty evaluation) helps readers quickly understand the claimed differentiation. The "Eval Novelty ✓" column succinctly captures the paper's unique selling point.

**6. Honest reporting of negative results.** The paper openly reports that no agent surpasses human SOTA and that many agent-task combinations fail entirely ("/" entries). This transparency is valuable for the community and sets realistic expectations about current agent capabilities.

## Weaknesses
The weaknesses are ordered by severity and impact on the paper's core claims.

### W1. Unvalidated Novelty Metric (Critical)

**Location:** Page 1 (Section 4.1, Metrics and Evaluation Protocol paragraph); Pages 2-3 (Section 2.1-2.2, formal definitions)

**Evidence and mechanism:** The entire novelty evaluation rests on an LLM-as-judge pipeline: Codex extracts solution features, then GPT-5 rates dissimilarity along six rubric dimensions (not described in main text). The distance function D(N(s)=C(s)·min D(s,h)) is the second of two core metrics, yet **no human validation, inter-rater reliability, or calibration study is reported anywhere in the main text.** The paper references Appendix F for details, but the main text must stand on its own for critical evaluation. Without evidence that the LLM-as-judge scores correlate with expert human judgments, the N metric's validity is unknowable. Furthermore, using LLMs to evaluate LLM-generated solutions creates a circularity risk: the metric may favor solutions that match the LLM's training distribution rather than truly novel approaches.

**Impact:** This is a foundational issue. If the N metric is unreliable, all claims about agent novelty—including the paper's central finding that agents achieve "high novelty" without robust performance—are unsupported. The paper's primary differentiation from prior benchmarks (Eval Novelty ✓) cannot be trusted without metric validation.

**Recommended repair:** (a) Add a human validation study comparing LLM-as-judge novelty scores against expert annotators on at least 30-50 solution pairs, reporting Spearman/Kendall correlation. (b) Report the six rubric dimensions explicitly in the main text. (c) Compare against a simpler deterministic baseline (e.g., CodeBERT embedding cosine similarity) to justify the complexity of the LLM pipeline. (d) Add a caveat about the circularity risk and how the rubric-based scoring (rather than free-form judgment) mitigates it.

---

### W2. Best-of-3 Reporting Without Variance (Major)

**Location:** Page 1 (Section 4.1, Implementation Details paragraph and Table 2)

**Evidence and mechanism:** The paper reports "the best score over these three runs" and marks empty entries ("/") when all three runs fail. This protocol has three problems. First, **best-of-3 inflates performance** relative to the expected single-run outcome, especially for high-variance tasks. Second, **no standard deviations or confidence intervals are reported**, making it impossible to assess the stability of the findings. Third, the **selective valid-submission filter** means that an agent that succeeds in only 1 of 3 runs is treated equivalently to one that succeeds consistently—the single valid run automatically becomes the "best." This conflates capability with reliability. For a benchmark whose goal is to evaluate agents for real-world deployment, reliability is a first-class attribute that should be measured, not filtered away.

**Impact:** The empirical comparisons in Table 2 are potentially unreliable. The claim that "MLab leads in both Performance Gain and Novelty" may be an artifact of differential task success rates rather than a true capability difference. The "/" entries for MLab on CDML, PTTALC, and RCIC suggest it simply avoids hard tasks.

**Recommended repair:** (a) Report mean ± std over runs with explicit N (number of valid runs). (b) Report success rate (e.g., "2/3 runs valid") for each configuration. (c) Provide per-run scores in an appendix. (d) When comparing frameworks, either (i) restrict to the common task subset where all frameworks succeeded, or (ii) use a statistical model that accounts for missing data.

---

### W3. Uneven Task Success Confounds Framework Comparison (Major)

**Location:** Page 1 (Section 4.2, Main Results paragraphs and Table 2)

**Evidence and mechanism:** The average performance gain and novelty for each framework are computed **over different subsets of tasks.** MLab's average (-24.32, 56.55) is based on 6 tasks; CodeAct's average (-41.58, 54.86) is based on 6 tasks but a partially different set; AIDE's average (-42.68, 46.67) is based on only 5 tasks. Crucially, CodeAct and AIDE attempted RCIC (G=-99.67) and TrojanDetection, which MLab did not. These are the hardest tasks, and their inclusion drags down CodeAct's and AIDE's averages. The paper claims "MLab leads in both" without acknowledging that MLab's lead may simply reflect an easier task subset.

**Impact:** The central empirical comparison of the paper is confounded. The claim that "MLab leads in both Performance Gain and Novelty, indicating a rare blend of innovation and execution" is not supported by a fair comparison.

**Recommended repair:** (a) Report averages over the **intersection** of tasks where at least two frameworks have valid scores. (b) Use a per-task matched comparison (e.g., difference scores within each task) rather than global averages. (c) Explicitly note which tasks each framework succeeded on and discuss selection effects.

---

### W4. "Primacy of Robustness" Claim Contradicted by Aggregate Data (Major)

**Location:** Page 1 (Section 4.2, "The Primacy of Robustness over Novelty" paragraph)

**Evidence and mechanism:** The paper claims that "the primary bottleneck for agents on complex tasks is not a deficit of novel ideas, but rather the inability to translate them into correct and robust implementations." However, the aggregate data in Table 2 shows that **the framework with the highest average novelty (MLab, 56.55) also has the highest (least negative) average performance gain (-24.32).** CodeAct has lower novelty (54.86) and lower gain (-41.58). Across the full table, higher novelty is associated with better performance, not worse. The exceptions (RCIC, TrojanDetection) are outliers where high-novelty agents perform poorly. These outliers support a more nuanced claim—"novelty alone does not guarantee performance"—but not the stronger claim that robustness is more important than novelty.

**Impact:** The paper's headline finding is at odds with its own data. This weakens the narrative coherence and may mislead readers about the actual relationship between G and N in the evaluated settings.

**Recommended repair:** Reframe the conclusion to reflect the actual pattern: novelty and performance are positively associated on average, but they decouple on tasks requiring high execution precision. The bottleneck is the joint requirement (novel + correct), not one dimension over the other.

---

### W5. "First Benchmark" Claim Unverifiable and Potentially Overstated (Major)

**Location:** Page 1 (Abstract, Introduction para 3, Contribution list)

**Evidence and mechanism:** The paper repeatedly claims to be "the first benchmark specifically targeting innovation potential." While the paper's own Table 1 shows that iBench is the only benchmark with "Eval Novelty ✓," this claim cannot be verified without external literature access (Retrieval-Disabled Mode is active for this review). The paper's related work cites InnovatorBench (Wu et al., 2025) as a prior benchmark for open-ended improvement tasks. Whether InnovatorBench or other creativity-oriented benchmarks (e.g., research ideation benchmarks) already measure methodological novelty requires independent verification. Furthermore, the "first" claim conflates "first to include novelty" with "first to target innovation potential"—these are distinct assertions.

**Impact:** If the "first" claim is found to be inaccurate during review, it damages overall paper credibility and may require substantial repositioning.

**Recommended repair:** (a) Qualify the claim: "To our knowledge, the first benchmark..." (b) Explicitly discuss the closest prior work (InnovatorBench and any other creativity/novelty benchmarks) and explain precisely why they do not constitute "innovation potential" evaluation. (c) Clarify what "novelty" means in the context of the claimed priority.

---

### W6. Formula-Level Issue in Novelty Definition (Moderate)

**Location:** Page 1 (Section 2.2, Eq. 3)

**Evidence and mechanism:** The novelty definition N(s) = C(s) · min_{h∈S_known} D(s, h) has a formal subtlety: when C(s)=0 (infeasible solution), N(s)=0 regardless of how novel the solution is. This conflates "infeasible but interesting" with "feasible but trivial." While the paper notes that novelty is "only computed for feasible solutions," the multiplication by C(s) mechanically assigns N=0 to infeasible solutions, losing information about their methodological originality.

**Impact:** Minor formal issue. Does not affect empirical results since novelty is only reported for feasible solutions, but the equation is technically misleading.

**Recommended repair:** Replace Eq. (3) with a conditional definition: "N(s) = min_{h∈S_known} D(s, h) if C(s)=1, otherwise undefined." Remove the C(s) multiplier to avoid the formal conflation.

---

### W7. LLM-as-Judge Pipeline Confound Not Addressed (Moderate)

**Location:** Page 1 (Section 4.1, Metrics and Evaluation Protocol paragraph)

**Evidence and mechanism:** The novelty pipeline uses Codex for feature extraction and GPT-5 for pairwise comparison. Both are LLMs. This creates a potential **auto-evaluation confound:** if the agent being evaluated uses the same LLM family (e.g., DeepSeek-v3.1 for generation, GPT-5 for evaluation), the novelty score may reflect inter-model agreement rather than genuine methodological novelty. The paper does not discuss this confound or any mitigation strategy.

**Impact:** The novelty scores may be systematically biased for agents using different base LLMs. For example, agents built on GPT-5 may receive lower novelty scores against GPT-5-evaluated references due to shared training distribution artifacts.

**Recommended repair:** (a) Discuss this confound explicitly in the main text. (b) Run a sensitivity analysis comparing novelty scores when the evaluator LLM matches vs. differs from the agent's base LLM. (c) Consider using a deterministic distance function (e.g., code embedding) as a complementary or primary novelty measure.

---

### W8. Conclusion Lacks Limitations and Future Work (Minor)

**Location:** Page 1 (Section 6, Conclusion)

**Evidence and mechanism:** The conclusion is a single paragraph that restates the paper's contributions without discussing limitations (e.g., only 10/18 tasks evaluated, LLM-as-judge metric unvalidated, single-model backbone for main experiments) or actionable future directions.

**Impact:** Missed opportunity to guide follow-up work. The paper ends with a generic statement rather than a research agenda.

**Recommended repair:** Expand the conclusion to include (a) validated findings, (b) bounded limitations, and (c) 2-3 specific future research directions (e.g., validating the N metric, expanding to exploratory tasks, incorporating efficiency metrics).

---

### W9. iGym Description Deferred Without Validation (Minor)

**Location:** Page 1 (Section 3.5)

**Evidence and mechanism:** iGym's architectural description, technical details, and validation are entirely deferred to Appendix C. The main text claims iGym addresses limitations of OpenHands, AutoGen, and LangGraph but provides no evidence (failure rate comparisons, overhead benchmarks, or user studies) to support these claims.

**Impact:** A key infrastructure component is essentially black-boxed. Readers cannot verify that iGym provides a neutral evaluation platform.

**Recommended repair:** (a) Include a brief validation summary in the main text (e.g., "iGym reduces environment-related failures by X% compared to manual orchestration"). (b) Add an overhead comparison to direct execution to rule out framework-specific artifacts.

---

### W10. Related Work Lacks Depth on Creativity/Diversity Metrics (Minor)

**Location:** Page 1 (Section 5, first paragraph)

**Evidence and mechanism:** The related work correctly identifies the gap in existing benchmarks but does not engage with the broader literature on creativity assessment, diversity metrics in generative models, or novelty search in evolutionary computation. These fields have developed methods for measuring solution originality that may be relevant or provide alternative approaches.

**Impact:** The paper positions itself as the first to evaluate innovation, but a broader literature review would strengthen the positioning and reveal potential connections.

**Recommended repair:** Add a brief paragraph acknowledging related work in creativity/novelty assessment and explaining why these methods are not directly applicable to agent-generated algorithmic solutions.

## Score
**Final Score: 5/10**

**Score rationale (evidence-grounded):**

The paper addresses a genuinely important problem—measuring innovation in AI agents beyond correctness—and presents a well-structured formal framework (P,S,V,D) with two complementary metrics (G and N). The task curation pipeline is rigorous, and the 18-task benchmark is a potentially valuable community resource.

However, the score is limited by several critical and major weaknesses:

- **Metric validation gap (W1):** The novelty metric N, which is the paper's primary differentiation from prior benchmarks, relies on an LLM-as-judge pipeline with no reported human validation, inter-rater reliability, or calibration. This is a foundational issue: if N is unreliable, the paper's central empirical claims are unsupported.
- **Reporting confounds (W2, W3):** Best-of-3 reporting without variance, selective valid-submission filtering, and uneven task success across frameworks make the empirical comparisons unreliable. The claim that "MLab leads in both G and N" may reflect task selection artifacts rather than true capability differences.
- **Unverifiable novelty claim (W5):** The "first benchmark" assertion cannot be verified in this review and may require repositioning.
- **Internal contradiction (W4):** The paper's headline finding ("robustness primacy") is partially contradicted by its own aggregate data, where higher novelty correlates with better performance.

On the positive side, the formal framework, task curation methodology, and ablation experiments on CirclePacking are contributions with lasting value. The paper's transparency about negative results (no agent surpasses human SOTA) is commendable.

**Consistency check:** The score of 5/10 reflects that (a) the conceptual contribution is solid but unvalidated, (b) the empirical findings are confounded and may not survive rigorous review, and (c) substantial revision (metric validation, fairer comparisons, stronger rebuttal of internal contradictions) is needed before the paper's claims are fully supported.