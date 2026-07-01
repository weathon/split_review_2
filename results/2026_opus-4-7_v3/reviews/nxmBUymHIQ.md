Now let me verify some specific claims in the tables more carefully.Now I have thoroughly read the paper. Let me draft my review before calibration.Now let me run calibration Round 1 — Bracketing:Let me read some of the most relevant anchor papers, especially EVA (which this paper directly builds on) and some rejected LoRA papers.Now I have a thorough understanding of the calibration landscape. Let me form my bracket and finalize the review.

**Round 1 Bracket:** Based on comparison with anchor papers:
- The paper is clearly above the 1.0 strong-reject tier (not fundamentally broken)
- It is better than score-3.0 papers like HoLoRA (which had limited novelty and narrow experiments) — LoLoRA has a genuine theoretical contribution
- It is comparable to EVA (4.75, rejected) — LoLoRA provides the theoretical justification EVA lacked, but its iterative method adds nothing beyond EVA empirically
- It is weaker than DeLoRA (5.25, accepted) and ReLoRA (5.75, accepted), which showed clear empirical improvements
- **Initial bracket: 3.5 – 5.0**

The critical distinction: LoLoRA's theory is genuine but confirmatory (formalizes what EVA showed), and the method adds no value over LoRA-FA(EVA). Compared to EVA (4.75), LoLoRA adds theory but fails to show its iterative mechanism helps. This puts it around **4.0**.

Now let me write the final review:

---

## Summary
LoLoRA proposes a hybrid LoRA fine-tuning approach that replaces gradient-based updates of the A matrix with local, forward-pass-only updates (Hebbian PCA or autoencoder), while retaining backpropagation for B. The paper provides a theoretical analysis (Theorem 4.4) proving that PCA-based initialization of A is optimal under random regression assumptions, and Theorem 4.5 establishing a formal asymmetry between A and B. Experiments are conducted on GLUE (RoBERTa-large), MetaMathQA (LLaMA-3.1-8B), and LLaVA-v1.5-7B, with ablations on TinyLlama-1.1B.

## Strengths
- **Theorem 4.4 is a genuine theoretical contribution.** It provides a precise, formally stated characterization of the optimal A initialization under the random regression assumption, showing A should span the top-r eigenspace of the input covariance matrix (Section 4). This fills a theoretical gap noted in reviews of the EVA paper, which showed empirically that PCA initialization works but lacked formal justification. Theorem 4.5 cleanly establishes the A/B asymmetry: any full-rank B is equally good, while A benefits from data-dependent initialization.

- **The ablation in Table 6 constructively validates the theory.** Comparing HPCA, HPCA no mean, AE, and SoftHebb across ranks 2/4/8, all PCA-convergent methods achieve nearly identical performance (e.g., 2.535 at r=8 for HPCA vs. 2.536 for AE), while SoftHebb (which does not converge to the PCA subspace) degrades substantially (2.572 at r=8). This is a clean empirical validation of Theorem 4.4's prediction.

- **The method is simple and well-specified.** Algorithm 1 (Section 3.3) is concise: A is updated during the forward pass, z is freed from the computation graph, and B is trained normally. Easy to integrate into existing LoRA codebases.

- **Honest reporting and acknowledged limitations.** The paper explicitly notes that "classical LoRA remains the strongest overall" on GLUE (Section 5.1 summary) and acknowledges theoretical limitations (stationary targets, isolated submodules) in Section 6.

## Weaknesses

### Fatal
None.

### Major

- **The paper's core methodological contribution — that iterative local updates of A improve over one-shot PCA initialization — is not supported by any experiment.** On MetaMathQA (Table 3), LoLoRA HPCA and LoRA-FA (EVA) both achieve 82.9% accuracy with identical memory (26 GB). On LLaVA (Table 4), LoLoRA HPCA (2.93 perplexity) is slightly *worse* than LoRA-FA (EVA) (2.92). On ablations (Tables 5–6), LoLoRA HPCA (2.535 at r=8) matches LoRA-FA (EVA) (2.536 at r=8). The iterative updates introduce extra compute and optimizer state without demonstrable benefit over simply initializing A with PCA and freezing it. This undermines the paper's raison d'être: the method converges to the same subspace as one-shot EVA initialization, but through a more expensive path.

- **The theoretical result (Theorem 4.4) motivates initialization, not iterative updates, creating a gap between theory and method.** The theorem characterizes the optimal *fixed* A under the assumption that the target ΔW₀ has i.i.d. Gaussian entries (Assumption 4.1). This proves one-shot PCA initialization is optimal when targets are unknown — but it says nothing about whether iteratively updating A during training is beneficial when B is being simultaneously updated via backpropagation and the input distribution shifts. The paper claims HPCA updates converge to the optimal subspace (Section 4), which is true, but this convergence is to the *same* subspace EVA reaches at initialization. The stationarity assumption, acknowledged in Section 6, is load-bearing: if input statistics shift during training, iterative adaptation might help, but the experiments show it doesn't.

### Minor

- **Memory savings are not differentiated from LoRA-FA.** On MetaMathQA, both LoLoRA and LoRA-FA use 26 GB (Table 3). On LLaVA, LoLoRA uses 24.1 GB vs. LoRA-FA's 23.9 GB — LoLoRA actually uses *more* memory due to extra optimizer state (Table 4). The paper's abstract claims to "further reduc[e] the memory required for fine-tuning," but the savings come entirely from freezing A (the LoRA-FA paradigm), not from the local update mechanism.

- **Full LoRA consistently outperforms LoLoRA.** In Table 6, Full LoRA (uniform) beats all LoLoRA variants at every rank: 2.537 vs. 2.557 (r=2), 2.528 vs. 2.545 (r=4), 2.521 vs. 2.535 (r=8). On GLUE (Tables 1–2), LoRA outperforms LoLoRA HPCA on all 8 tasks. This suggests the local update approach has a small but systematic performance cost relative to end-to-end gradient-based training.

- **The LLaVA evaluation uses only validation perplexity on held-out data from the same instruction pool** (Section 5.3), not independent benchmarks. Perplexity on in-distribution held-out data is a weak proxy for actual multimodal capabilities, limiting what can be concluded from this experiment.

### Trivial
None.

## Nice-to-Haves
- An experiment explicitly isolating the value of iterative updates vs. one-shot PCA initialization in a non-stationary setting (e.g., distributional shift within training data, or very long training runs where input statistics evolve substantially as B is updated). This is the central empirical question for the method and remains unanswered.
- Wall-clock time comparisons across all experiments (currently only reported for LLaVA in Table 4).
- Memory breakdown in the main text rather than deferred to Appendix D, given that memory savings are the paper's primary practical selling point.
- Comparison of LoLoRA (EVA init) vs. LoRA-FA (EVA init) across all experiments to cleanly isolate the iterative update effect at matched initialization.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Criticism about MetaMathQA checkpoint selection and standard deviation underestimation** — Selecting best checkpoint over training with reporting across seeds is standard practice in the field. The ±0.004–0.005 standard deviations are reasonable given three seeds.
- **Algorithm 1 consistency issue (line 5 using pre-update A)** — This is a standard online learning pattern; the forward computation uses the pre-update value and the model stores the post-update, which is applied next step. Not a meaningful issue.
- **Concern that Assumption 4.1 (i.i.d. Gaussian ΔW₀) is unrealistic** — While factually true, this was retained as context for the theory-method gap (Major weakness 2) but should not be counted as a separate weakness. The assumption is reasonable for a worst-case/uninformed analysis; the issue is the leap from initialization theory to iterative method justification, not the assumption itself.
- **"LoLoRA underperforms LoRA on 7 of 8 GLUE tasks"** — Actually 8 of 8, but the point is already captured in the minor weakness about Full LoRA consistently outperforming.
- **Positioning LoRA-FA as "naive"** — The introduction calls LoRA-FA "A naive implementation" (Section 1), which is somewhat dismissive given that LoRA-FA (EVA) matches LoLoRA. However, this is a framing issue, not a substantive weakness.

## Novel Insights
The theoretical formalization that PCA-based initialization of A is provably optimal (Theorem 4.4) under random regression assumptions, combined with the formal proof of A/B asymmetry (Theorem 4.5), are useful theoretical contributions that complement and formalize the empirical EVA work. The ablation demonstrating that all PCA-convergent local learning rules (HPCA, AE) converge to equivalent performance while non-convergent ones (SoftHebb) fail (Table 6) is a clean empirical result connecting Hebbian learning theory to practical LoRA fine-tuning. However, the paper also inadvertently demonstrates a negative result: that iterative PCA adaptation during training provides no advantage over one-shot PCA initialization in the settings tested, which is informative for the community.

## Suggestions
- Reframe the contribution more honestly: the primary contribution is a theoretical justification for PCA-based A initialization (formalizing EVA), with the iterative method as one practical realization whose advantages over one-shot initialization remain to be demonstrated in non-stationary settings.
- Design experiments where input distributions shift substantially during training — this is where iterative adaptation should theoretically shine. Candidates: curriculum learning, domain-shift fine-tuning, or very long training runs.
- Provide LoLoRA (EVA init) vs. LoRA-FA (EVA init) comparisons across all experiments to cleanly isolate the iterative update effect. Table 4 already does this for LLaVA (where the updates don't help); extending to MetaMathQA and GLUE would complete the picture.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to LoLoRA |
|-------|------|-----------|-------|---------------------|
| HoLoRA | igGeaxOiFM | 3.00 | R1 | Weaker: narrow experiments (DeBERTa only), limited novelty; LoLoRA has broader experiments and genuine theory |
| ALLoRA | 7X65yoKl3Y | 3.33 | R1 | Comparable: identifies LoRA issues but method's improvements are questioned; LoLoRA has cleaner theory but weaker empirical case |
| UnoLoRA | 49ti6LOUw5 | 3.00 | R1 | Weaker: more limited scope; LoLoRA has stronger theoretical grounding |
| L-MSA | xi3sDtf8A0 | 3.00 | R1 | Weaker: less rigorous; LoLoRA is better executed overall |
| SiVA | VpeAsLmcvg | 3.75 | R1 | Comparable: both have theory-method gaps and questionable assumptions; LoLoRA's theory is cleaner |
| EVA | DM6Q45HWSk | 4.75 | R1 | Most directly comparable: LoLoRA provides the theoretical justification EVA lacked, but EVA's method (PCA init + rank redistribution) showed clearer empirical gains; LoLoRA's iterative method adds nothing over EVA |
| NoRA | 6nZwOYDcQx | 4.00 | R1 | Similar tier: incremental LoRA improvement with limited novelty |
| DeLoRA | X1U74IwuxG | 5.25 | R1 | Stronger: DeLoRA shows consistent improvements over baselines; LoLoRA does not |
| ReLoRA | DLJznSp6X3 | 5.75 | R1 | Stronger: ReLoRA demonstrates clear empirical value for high-rank training |
| LoRAM | s7DkcgpRxL | 6.20 | R1 | Stronger: clearer empirical contribution with memory-efficient training |
| LQ-LoRA | xw29VvOMmU | 6.75 | R1 | Stronger: clear memory savings with maintained performance |
| VeRA | NjNfLdxr3A | 7.25 | R1 | Significantly stronger: dramatic parameter reduction with maintained performance |
| HiRA | TwJrTz9cRS | 8.00 | R1 | Much stronger: clear improvements with broad experiments |

### Scoring Rationale

**Round 1 bracket: 3.5 – 5.0.** LoLoRA is clearly above the score-3.0 papers (HoLoRA, UnoLoRA, L-MSA) due to its genuine theoretical contribution and broader experiments. It is comparable to EVA (4.75) — LoLoRA provides the theoretical justification EVA lacked, but LoLoRA's iterative method adds nothing over EVA empirically, and EVA at least showed improvements from its initialization + rank redistribution. LoLoRA is clearly below DeLoRA (5.25) and ReLoRA (5.75), which demonstrate clear empirical value.

The paper's core methodological premise (iterative local updates improve over one-shot PCA initialization) is unsubstantiated across all experiments. The theoretical contribution (Theorem 4.4) is genuine and useful but confirmatory — it formalizes what EVA demonstrated empirically. The theory-method gap is significant: the theorem motivates initialization, not iterative updates. Standard LoRA also consistently outperforms LoLoRA, suggesting a systematic (if small) performance cost.

Considering that EVA (which this paper builds on and largely replicates empirically) scored 4.75 and was rejected, and that LoLoRA's incremental contribution over EVA is a theoretical justification that doesn't translate to empirical gains, a score of **4.0** is appropriate — at the low end of the bracket, reflecting the unsupported central method claim.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>