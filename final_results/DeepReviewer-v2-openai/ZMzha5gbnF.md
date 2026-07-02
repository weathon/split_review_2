## Summary
# Final Review Report

## Summary

This paper identifies and characterizes the **priming vulnerability** in Masked Diffusion Language Models (MDLMs): the property that affirmative tokens appearing at intermediate denoising steps can steer generation toward harmful responses, even in safety-aligned models. The authors propose **Recovery Alignment (RA)**, a training method that teaches MDLMs to recover safe responses from contaminated intermediate states.

The paper makes three contributions: (C1) discovery and quantitative characterization of the priming vulnerability under two threat models (intervention-based anchoring attack and non-intervention First-Step GCG); (C2) a theoretical lower bound (Theorem 4.1) that enables tractable optimization-based attacks on MDLMs; and (C3) Recovery Alignment, which demonstrably mitigates the vulnerability across three MDLM architectures (LLaDA, LLaDA 1.5, MMaDA) while preserving general task performance on 11 benchmarks.

**Strengths**: Timely research question, clean experimental design with two complementary threat models, strong empirical validation of RA (ASR reduced from >90% to <10% on several settings), and a practical training framework that uses existing datasets and reward models.

**Core limitations**: (a) A critical notational error in Eq. (5) where optimization is over q (query) instead of θ (model parameters); (b) central Theorem 4.1 relies on an unproven monotonicity assumption whose validation is deferred to the appendix; (c) overclaiming in abstract ("critical vulnerability" without qualifying threat model constraints); (d) the concept of "affirmative token" lacks a formal operational definition; (e) several notation/equation clarity issues (Eq. 1 integrals over discrete space, Eq. 7 ambiguous cases environment). Novelty assessment is deferred due to external literature search being unavailable in this run.

**Overall assessment**: A solid, well-executed paper that addresses an important safety gap for an emerging model class. The technical core is sound, the results are convincing, and the method is practical. However, the notational errors, overclaiming, and deferred assumption validation should be addressed before publication.

## Strengths
**S1 — Timely and important research question.** The paper addresses a genuine safety gap: MDLMs are gaining traction as alternatives to ARMs, yet their vulnerability to jailbreak attacks from their unique denoising mechanism was largely unexplored. The identification of the "priming vulnerability" is a meaningful contribution to ML safety.

**S2 — Clean experimental design with two threat models.** The paper's two-phase analysis (intervention-based anchoring attack and non-intervention First-Step GCG) provides a comprehensive evaluation of the vulnerability. The anchoring attack cleanly isolates the vulnerability mechanism, while First-Step GCG demonstrates real-world exploitability. This dual approach strengthens both the scientific characterization and the practical relevance.

**S3 — Strong empirical validation of Recovery Alignment.** RA consistently and substantially reduces ASR across all three models. For example, on LLaDA Instruct, RA reduces ASR from 17.3% to 0.0% at anchoring step 1, from 88.7% to 8.3% at step 16, and from 58.0% to 11.3% for First-Step GCG (Tables 2-3). These results represent dramatic improvements over existing alignment methods (SFT, DPO, MOSA).

**S4 — Practical training framework.** RA uses existing datasets (BeaverTails) and off-the-shelf reward models (DeBERTaV3), requiring no additional data collection or annotation. The GRPO-based optimization and linear curriculum scheduling are well-motivated and backed by ablation studies.

**S5 — General capability preservation.** RA does not cause substantial degradation on 11 diverse benchmarks (Table 4). Average accuracy remains within 0.1 points of the original model (e.g., 52.6% vs 52.2% for LLaDA). The method even improves TruthfulQA scores, likely due to reward-model-based alignment effects.

**S6 — Clear writing and good structure for most parts.** The paper is generally well-organized, with clear notation introduced in Section 3, a logical flow from vulnerability discovery to mitigation, and informative figures/tables that support the main claims.

## Weaknesses
### W1 — Critical: Optimization target error in Equation (5) [Major]
**Evidence:** Page 5 - Section 5, Eq. (5) reads $\min_{\mathbf{q}} p_{\pi, m_t}(\mathbf{r}_T = \mathbf{r} \mid \mathbf{q}, \mathbf{r}_0)$, minimizing over the **query** $\mathbf{q}$ rather than model parameters $\theta$.
**Impact:** This is not merely a typo — it describes a different operation (adversarial query optimization) than what the paragraph intends (alignment training that updates model parameters). This inconsistency undermines reader trust in the technical precision of the paper. Standard alignment minimizes the probability of harmful outputs by updating $\theta$, not $\mathbf{q}$.
**Fix:** Replace $\min_{\mathbf{q}}$ with $\min_{\theta}$. See annotation `f6ed9a7b-8965-4900-a70b-bc33a52e58c8` for the corrected version.

### W2 — Critical: Theorem 4.1 depends on an unproven monotonicity assumption [Major]
**Evidence:** Page 4 - Section 4.2, Theorem 4.1 assumes $\log \pi_\theta(\tilde{\mathbf{r}}_{t+1} = \mathbf{r} \mid \mathbf{q}, \mathbf{r}_t) \geq \log \pi_\theta(\tilde{\mathbf{r}}_1 = \mathbf{r} \mid \mathbf{q}, \mathbf{r}_0)$ for all $t$. The main text provides only heuristic justification ("compatible with the current denoising process") and defers empirical validation to Appendix C.2.
**Impact:** The whole First-Step GCG approach rests on this inequality. If the assumption fails for certain query-response pairs, the lower bound may not hold and the attack's theoretical justification weakens. The paper should either prove the assumption (at least for the specific noise schedule used) or discuss conditions under which it might break.
**Fix:** (a) Move a concise version of the empirical validation from Appendix C.2 into the main text, showing the log-likelihood across steps for representative queries. (b) Add a caveat about when the assumption could fail (e.g., semantic inconsistency between fixed tokens and target response $\mathbf{r}$). See annotation `ed309774-6eac-44d8-80b0-a3e1478c1606`.

### W3 — Major: Undefined concept of "affirmative token" [Major]
**Evidence:** Page 3 - Section 4 defines the priming vulnerability as occurring when "affirmative tokens, which endorse or advance a harmful intent" appear at intermediate steps. The term is never formally defined — not by toxicity threshold, semantic similarity, or any operational criterion.
**Impact:** This makes the vulnerability hard to falsify and reproduce. Different evaluators may disagree on what constitutes an "affirmative token." The paper's experimental setup (anchoring attack replaces the full predicted response with a harmful one) sidesteps this definitional issue rather than addressing it, but the conceptual definition remains ambiguous.
**Fix:** Provide a formal operational definition in Section 3 or 4. Options include: (a) tokens whose toxicity score (via a classifier) exceeds a threshold; (b) tokens listed in an appendix that are empirically identified as steering toward harm; or (c) tokens whose inclusion in $r_t$ increases the conditional probability of harmful continuations. See annotation `84fde05c-2590-42f2-8423-3e225d4d44e6`.

### W4 — Major: Abstract and introduction overclaim the vulnerability's practical severity [Moderate]
**Evidence:** Page 0 - Abstract states "DLMs have a critical vulnerability" without qualifying the threat model. Page 1 - Introduction states ASR "increases from 2% to 21% even with an intervention only at the first step," blending two different threat models (natural refusal vs. anchoring attack under a strong attacker assumption).
**Impact:** Reading the abstract alone, one could conclude that any DLM can be trivially jailbroken. The actual findings are nuanced: the vulnerability requires either denoising-process intervention (strong attacker) or query optimization (non-trivial attack design). Overclaiming can reduce reviewer trust and mislead practitioners.
**Fix:** Qualify the vulnerability scope explicitly. The abstract should read "a vulnerability under specific attack conditions" rather than "a critical vulnerability." The introduction should separate the two threat models clearly. See annotations `a4346962...` and `8e0a33fd...`.

### W5 — Moderate: Notational inconsistency in Equation (1) [Moderate]
**Evidence:** Page 3 - Eq. (1) uses integrals ($\int$) over $\tilde{r}_t$ and $r_t$, which are discrete sequences over a finite vocabulary $\mathcal{V}^L$. The notation $\pi_\theta: \mathcal{V}^{|q|} \times \mathcal{V}^L \rightarrow \mathcal{P}(\mathcal{V}^L)$ maps to a discrete probability distribution.
**Impact:** While mathematically permissible as measure-theoretic notation, using integrals for discrete distributions is confusing and inconsistent. This can raise reviewer flags about technical rigor.
**Fix:** Replace integrals with sums, or add a clarifying sentence that integrals are over the discrete space. See annotation `0468dc30-8f69-41c5-b729-87c19f369a70`.

### W6 — Moderate: "State-of-the-art" claims are overreaching given limited baselines [Minor]
**Evidence:** Page 1 (Introduction) and Page 7 (Section 6.2) claim "state-of-the-art robustness." The comparison set includes only SFT, DPO, and MOSA — all re-implemented by the authors.
**Impact:** Without comparison to external defense methods or a standardized leaderboard, "state-of-the-art" implies broader validation than the evidence supports. The results within the tested set are impressive enough on their own.
**Fix:** Replace "state-of-the-art" with "substantially outperforms existing alignment methods." See annotations `e9f1d265-87ac-48b0-83f1-a423aa2032b1` and `1a533009...`.

### W7 — Moderate: RA objective (Eq. 7) uses ambiguous cases notation [Minor]
**Evidence:** Page 5 - Section 5, Eq. (7) uses a cases environment ($\begin{cases} \dots \end{cases}$) where the two cases are actually sequential steps (first sample $\mathbf{r}_{t_{\text{inter}}}$, then denoise), not alternative conditions.
**Impact:** Misleading notation makes the method harder to parse and reproduce.
**Fix:** Replace the cases structure with a clear sequential description. See annotation `f4c1c489-6646-4427-a379-930378c94086`.

### W8 — Minor: Missing key training hyperparameters in main text
**Evidence:** Page 6 - Section 6.1 states "All models were trained for 2,500 steps" but does not report batch size, learning rate, optimizer, GPU hardware, or the specific $t_{\min}/t_{\max}$ values used.
**Impact:** Reduces readability for reviewers who may not consult the appendix for basic training details.
**Fix:** Add a summary sentence with key hyperparameters. See annotation `86df4a64-ea82-4a8d-8719-751b82d45d14`.

### W9 — Minor: Limitations section is too narrow
**Evidence:** Page 9 - Conclusion/Limitations only discusses a DPO-style supervised alternative. Does not mention RA's degraded performance at late intervention steps, reward model dependency, or limited evaluation scope.
**Impact:** The paper appears less self-critical than it could be, reducing scholarly depth.
**Fix:** Expand to include at least late-intervention robustness and reward model dependency. See annotation `49b32915-8bfc-41c1-9f21-ec20bff5abba`.

### W10 — Minor: Non-standard citations
**Evidence:** Page 1 - Introduction cites "(DeepMind, 2024; Labs et al., 2025)" which are not standard academic references.
**Impact:** Reduces verifiability and suggests unfinished manuscript preparation.
**Fix:** Replace with proper arXiv IDs or published references. See annotation `78174e8a-357e-40c6-ad4d-8a966f177cc5`.

---

**Novelty Note:** Due to external literature search being unavailable in this run (Retrieval-Disabled Mode), novelty and positioning claims are deferred for manual verification. The paper appears to make a genuine contribution in identifying a previously undocumented failure mode specific to MDLMs, but the extent of overlap with concurrent work (PAD, DiJA) and ARM-based safety research cannot be fully assessed without retrieval.

## Score
**Final Score: 7/10**

**Rationale**: The paper addresses a timely and important safety research question with a well-designed experimental framework and convincing empirical results. Recovery Alignment is a practical, effective mitigation that clearly outperforms existing approaches. However, the score is constrained by several issues: a critical notational error in Eq. (5) that must be corrected before publication, an important theoretical assumption (Theorem 4.1) that lacks rigorous justification in the main text, an undefined key concept ("affirmative token"), and a tendency toward overclaiming in the abstract and SOTA statements. With fixes for these issues (all feasible within a minor revision), the paper would be a strong 8/10 candidate.

**Scoring Dimensions**:
- **Research value and novelty**: 7/10 — Timely discovery of an MDLM-specific vulnerability; the concept of priming in the denoising process is novel and well-motivated. Novelty against concurrent work cannot be fully assessed without external retrieval.
- **Technical soundness and validity**: 6/10 — Core experiments are sound, but Eq. (5) error and unproven assumption reduce confidence. Fixable with minor corrections.
- **Empirical evidence**: 8/10 — Comprehensive benchmarks, multiple evaluators, ablations, and general capability tests. Good use of std over 3 runs.
- **Reproducibility and clarity**: 6/10 — Generally clear writing but missing key training details in main text, ambiguous notation (Eq. 1, Eq. 7), and undefined key concepts.
- **Presentation**: 7/10 — Well-structured, informative figures/tables, but some overclaiming and non-standard citations.