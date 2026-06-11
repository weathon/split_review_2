## Summary
# Final Review Report

## Summary

This paper introduces the Open Proof Corpus (OPC), a dataset of 5,062 human-evaluated LLM-generated proofs across 1,010 competition-level mathematical problems (IMO, USAMO, Putnam, etc.). The dataset was constructed by 13 expert judges (former IMO participants) over four weeks, with ~10% double-graded for consistency (90.4% agreement). Using the OPC, the authors address three open questions: (1) the gap between natural language and formal proof generation (informal outperforms formal by ~4× on PutnamBench), (2) the misalignment between final-answer accuracy and full proof correctness (up to 30% gap for o3), and (3) the effectiveness of best-of-n selection strategies (ranking-based methods improve accuracy by 17% over pass@1). The authors also fine-tune OPC-R1-8B, an 8B-parameter model that achieves 88.1% judgment accuracy (matching Gemini-2.5-Pro, approaching GPT-5), demonstrating the dataset's utility for training proof-evaluation models. The OPC is publicly released, making it a potentially valuable resource for the community.

**Strengths:** Large-scale human-validated dataset; rigorous annotation pipeline with expert judges; addresses timely open questions; open-source release with fine-tuned model; transparent contamination analysis.

**Weaknesses:** Formal-vs-informal comparison partially confounded and 4× gap claim inflated by excluding recent agentic formal systems; OPC-R1-8B evaluation confounded by train/test distribution overlap; best-of-n analysis affected by software bug (12% data exclusion); adaptive problem selection creates selection bias in aggregate statistics; limited discussion of several important limitations.

## Strengths
**1. Large-scale, human-validated resource for a critical gap.** The OPC is the first publicly available dataset of its scale (5,062 proofs, 1,010 problems) that includes human correctness judgments for LLM-generated mathematical proofs. This fills a tangible gap identified by the paper's own literature review: prior datasets were small, used outdated models, lacked human labels, or were not publicly released. The community need for such a resource is clear, and the open-source release (HuggingFace, dedicated website) maximizes its potential impact.

**2. Rigorous annotation methodology with expert judges.** The grading pipeline is thoughtfully designed: 13 former IMO participants or near-IMO-level judges, a custom web interface, clear grading guidelines collaboratively developed, a pilot phase with 35% double-grading, LLM-generated issue summaries to assist (but not bias) judges, and a 10% ongoing double-grading rate with 90.4% inter-judge agreement. The transparency about the annotation process (including uncertainty flagging, abstention, and coordinator oversight) sets a good standard for dataset construction papers.

**3. Addresses three timely and well-motivated research questions.** The paper identifies three questions—formal-vs-informal gap, final-answer vs proof-correctness alignment, and best-of-n selection—that are directly relevant to current LLM reasoning research. The empirical answers, even with caveats, provide useful evidence for the community: the formal-informal gap quantification, the model-specific nature of the final-answer misalignment (o3 particularly affected), and the finding that ranking-based selection significantly outperforms pointwise scoring.

**4. Transparent contamination and limitation analysis.** The paper devotes a full subsection (§5.6) to contamination analysis, including a controlled experiment comparing judge accuracy with and without ground-truth solutions. The limitations section (§6), while too brief, at least acknowledges the two most obvious limitations (model timing and problem level). The honest admission of a software bug affecting 18 best-of-n problems (footnote 1) further signals attention to rigor.

**5. The self-evaluation finding (Table 3) is a valuable empirical contribution.** The discovery that most LLMs judge their own proofs worse than others' proofs (and that QWEN3-235B-A22B is a notable exception) provides novel evidence about LLM metacognitive limitations. This finding has direct implications for the design of self-improving proof-generation systems and is likely to stimulate follow-up research.

**6. Practical demonstration of dataset utility.** The fine-tuning experiment (OPC-R1-8B achieving 88.1% judgment accuracy) shows the dataset can be used to improve model capabilities, not just evaluate them. The choice of GRPO (a reinforcement learning method) as the fine-tuning approach is technically interesting and shows the dataset supports advanced training paradigms beyond simple supervised learning.

## Weaknesses
### W1. Formal-vs-informal comparison partially confounded; "4×" claim inflated (Major)

**Evidence:** Page 1 - Introduction/Answering open questions (line 43) and Section 5.3 (line 161). The paper states "GEMINI-2.5-PRO solves 4 times more problems than the best formal model, GOEDEL-PROVER-V2" on PutnamBench.

**Issue:** This comparison includes a critical confound: GOEDEL-PROVER-V2 is not the best available formal system. The paper itself notes (line 191) that Seed-Prover (Chen et al., 2025) achieves 50% on PutnamBench—meaning a 4× gap is actually closer to ~1.6× (83% vs 50%). The paper dismisses this comparison because Seed-Prover uses "agentic techniques" while the informal results do not. However, this exclusion is arbitrary: the original claim was about "formal proof generation" broadly, not "non-agentic formal proof generation." If the paper intends to bound the comparison, the headline claim should be revised to explicitly state "non-agentic formal models" to avoid misleading readers about the current state of formal automated theorem proving.

**Impact:** The 4× claim appears in the abstract, introduction (line 43), and conclusion, and is highlighted in Fig. 1(b). If this claim is interpreted as a general statement about formal vs informal reasoning, it overstates the gap and could mislead researchers about the viability of formal approaches.

**Repair path:** Revise the claim to either (a) include Seed-Prover as a baseline and update to ~1.6× with an explicit note about the agentic confound, or (b) add "non-agentic" qualifier throughout. The introduction and Fig. 1(b) should be updated correspondingly.

---

### W2. OPC-R1-8B evaluation confounded by train/test distribution overlap (Major)

**Evidence:** Section 5.2 (lines 157-158). The paper acknowledges that "the train set for OPC-R1-8B shares the same distribution as this test set, which may inflate its performance."

**Issue:** Despite this acknowledgment, the abstract (line 14) and contribution list (lines 48-49) present OPC-R1-8B as "matching GEMINI-2.5-PRO and performing close to GPT-5" without prominently surfacing this caveat. The headline claim creates a misleading impression of cross-model parity, because GEMINI-2.5-PRO and GPT-5 were evaluated on the same test set without any distribution overlap advantage. The out-of-distribution analysis (§C) mitigates this concern but is only referenced, not presented in the main text.

**Impact:** A reader skimming the abstract and conclusion would reasonably conclude OPC-R1-8B is competitively close to state-of-the-art closed models, when in reality the in-distribution evaluation may significantly overstate its generalization capability. This weakens the contribution claim for the fine-tuned model.

**Repair path:** (a) Add the distribution caveat to the abstract, (b) include a brief OOD result summary in the main text (not just appendix), and (c) restructure the contribution claim to separate "in-distribution fine-tuning success" from "cross-model comparison."

---

### W3. Adaptive problem selection creates selection bias in aggregate statistics (Major)

**Evidence:** Section 3.1 (lines 63-64). Problem difficulty was adaptively titrated: "initial results indicated that models were performing very well (~65%) on national-level problems," leading to the addition of harder problems to maintain ~50% accuracy.

**Issue:** The final dataset composition is not a random or representative sample of competition problems but a dynamically curated set. This means aggregate statistics (e.g., "43% correct proofs overall" from line 42) are partly artifacts of the curation rule rather than intrinsic properties of LLM proof-generation capability on competition problems. If problem selection had been fixed rather than adaptive, the overall accuracy could be substantially different.

**Impact:** Any claim about LLM proof-generation "accuracy" or "success rate" derived from the full OPC should be interpreted as conditional on the adaptive selection process. The paper does not discuss this caveat when presenting the 43% figure or model-wise accuracy comparisons.

**Repair path:** (a) Report the number and timing of difficulty adjustments, (b) provide accuracy histograms showing the distribution of per-problem model accuracy, (c) add a limitation discussing how adaptive selection affects aggregate statistics.

---

### W4. Best-of-n analysis undermined by software bug and incomplete comparisons (Major)

**Evidence:** Footnote 1 (line 226) and Section 5.5 (line 205). A "small bug in the Rank (Swiss) method caused incorrect selections for 18 questions," requiring exclusion of 12% of the best-of-n subset. Additionally, Rank (Bracket) was not evaluated on the larger subset.

**Issue:** Excluding 18 of 152 problems (12%) without describing the bug's nature, impact, or whether the excluded problems differ systematically from the remaining set is a significant transparency gap. Furthermore, without Rank (Bracket) results on the larger subset, the claim that ranking methods generally outperform pointwise methods is only supported on 60 problems—a small sample for drawing general conclusions.

**Impact:** The headline best-of-n result ("17% improvement") relies on data that required an unexplained 12% exclusion and omits a key comparison method. This weakens confidence in the generalizability of the ranking-method advantage.

**Repair path:** (a) Provide a detailed bug description and impact analysis, (b) re-run on the full 152-problem set after bugfix, (c) include Rank (Bracket) on the larger subset.

---

### W5. Limitations section omits several important caveats (Major)

**Evidence:** Section 6 (lines 222-223). The Limitations section covers only two points: (1) model timing and (2) high-school-level problem focus.

**Issue:** Five additional limitations are worth discussing: (a) selection bias from adaptive problem titration, (b) the OPC-R1-8B distribution overlap confound, (c) label noise effects on downstream conclusions (estimated 5% judge error rate), (d) single-model generator in best-of-n experiments, and (e) lack of problem-difficulty-stratified analysis of judging accuracy. Omitting these creates the impression of incomplete self-assessment.

**Impact:** A thorough limitations section is essential for a dataset paper, where users need to understand the resource's boundaries to use it appropriately.

**Repair path:** Add at least the selection bias and distribution overlap limitations to §6. A thorough discussion of label noise and its implications for downstream analysis would further strengthen the paper.

---

### W6. Inter-judge agreement analysis uses simplistic error model (Minor)

**Evidence:** Section 4 (line 109). The paper estimates individual judge error rate $p=5\%$ by solving $0.904 = (1-p)^2 + p^2$.

**Issue:** This model assumes (a) independent judge errors, (b) equal error rates across judges, and (c) no systematic bias. However, the paper acknowledges systematic discrepancies exist (line 78-79: "most inconsistencies came from overlooked errors"). Correlated errors (e.g., both judges missing the same subtle mistake due to shared expertise) would invalidate the independence assumption and could make $p=5\%$ an underestimate. Cohen's kappa or another chance-corrected metric would provide a more robust reliability estimate.

**Repair path:** Report Cohen's $\kappa$ alongside raw agreement, and discuss how correlated errors could affect the estimated error rate.

---

### W7. Contamination analysis lacks post-training-cutoff evaluation (Minor)

**Evidence:** Section 5.6 (lines 206-210). The "worst-case experiment" provides ground-truth solutions alongside proofs.

**Issue:** This tests whether models *use* solutions to improve judging, but does not test whether models have *memorized* judging patterns from training data. A post-training-cutoff evaluation (e.g., on competitions after each model's knowledge cutoff) would directly test contamination effects on judging ability. The paper also does not test whether the aggregate Δ = +1.1% across all eight judges is statistically significant.

**Repair path:** Add at least one post-cutoff evaluation for a representative model, and report a paired test across all judges to determine whether the small aggregate improvement is significant.

---

### W8. Introduction narrative order could better establish problem significance (Minor)

**Evidence:** Page 1 - Introduction (lines 15-16). The introduction opens with LLM benchmark performance before establishing why proof generation matters.

**Issue:** A reader unfamiliar with the proof-generation subfield may not appreciate why the gap between final-answer benchmarks and proof correctness is important. The practical significance (theorem proving, education, verifiable AI reasoning) should be established in the first paragraph rather than mentioned in passing.

**Repair path:** Restructure the opening to: practical significance → benchmark limitation → research gap → proposed resource. See annotation on lines 15-17 for a concrete revised version.

---

### W9. Self-evaluation finding under-analyzed (Minor)

**Evidence:** Section 5.2 (line 159, Table 3). The finding that most LLMs judge their own proofs worse than others' is reported but not deeply analyzed.

**Issue:** The paper does not explore why QWEN3-235B-A22B is the exception, does not control for proof complexity or length as a confound, and does not discuss implications for self-improving systems. These would strengthen an already interesting finding.

**Repair path:** Add analysis of the QWEN3 exception, control for proof length/complexity, and add a dedicated discussion paragraph about implications for self-improvement pipelines.

---

### W10. Conclusion undersells contributions (Minor)

**Evidence:** Section 7 (line 225). The conclusion restores the three open questions but omits quantitative results and does not name the released model.

**Repair path:** Include specific numbers (4×, 30%, 17%) and the model name (OPC-R1-8B) in the conclusion.

## Score
**Final Score: 6/10**

**Rationale:** The Open Proof Corpus is a genuinely valuable resource for the community, filling a clear gap with its large-scale human-validated proof evaluations. The annotation methodology is rigorous and well-documented. However, the paper's impact is reduced by several inflated headline claims. The formal-vs-informal 4× gap is partially confounded and does not account for recent agentic formal systems. The OPC-R1-8B comparison against GPT-5 and Gemini-2.5-Pro is undermined by train/test distribution overlap that advantages the fine-tuned model. The best-of-n results are weakened by a software bug requiring 12% data exclusion and missing comparisons. The adaptive problem selection introduces an unacknowledged selection bias in aggregate statistics. These issues are fixable through more precise claim-bounding and additional analyses, and the core dataset contribution remains solid. A revised version that addresses these claim-precision issues and expands the limitations section could merit a higher score (7-8/10).