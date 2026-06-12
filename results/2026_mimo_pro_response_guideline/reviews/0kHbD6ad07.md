Now I have enough calibration data. Let me finalize my analysis.

**Round 1 bracket: 7.0–8.0**

The paper under review compares favorably to the 7.00 anchors ("Learn-to-Optimize" and "Percolation Model") due to its more fundamental contribution and vastly more extensive empirical validation. It sits near "When can transformers reason with abstract symbols" (7.60) — both have clean theoretical proofs + empirical validation. The paper's theory-algorithm gap and presentation issues pull it slightly below the 8.00 "Retrieval Head" anchor, which had minimal weaknesses.

**Round 2 narrowing: 7.0–7.5** — confirmed by "Factual Recall" (7.33) and "Polynomial Width" (7.25) anchors, which are solid but less empirically grounded than this paper.

**Final score: 7.5** — the paper's theoretical contribution is genuinely novel (first proof of injectivity under training, not just initialization), the empirical validation is the most extensive among all anchors (~5 billion collision tests), the practical algorithm adds operational value, and the privacy implications add broader significance. The theory-algorithm gap is a real but acknowledged weakness that doesn't undermine the core theoretical claim.

---

## Summary
This paper proves that decoder-only Transformer language models are almost-surely injective maps from discrete prompts to continuous last-token hidden states, via a three-theorem chain using real-analyticity and measure theory (Theorems 2.1–2.3). It operationalizes this via SIpIT, a linear-time algorithm for exact input recovery from hidden states, validated across 8+ model families with ~5 billion pairwise collision tests (zero collisions found) and 100% inversion accuracy.

## Strengths
- **Elegant three-theorem proof chain (Theorems 2.1–2.3):** The progression from real-analyticity → injectivity at initialization (via measure-zero collision sets, with concrete non-colliding parameter constructions at lines 85–88) → preservation under GD training (via Inverse Function Theorem on the real-analytic step map, lines 105–109) is clean, well-structured, and avoids hand-wavy existence arguments.

- **Rigorous differentiation from closest prior work (Sutter et al., 2025):** Line 333 clearly states: Sutter et al. prove injectivity for the full hidden-state matrix only at initialization, whereas this paper proves injectivity at the task-relevant last-token state and critically shows it *persists under training*. The GD-preservation argument addresses a genuine gap left by prior work.

- **Massive empirical collision search confirming theory at scale:** ~5 billion pairwise L₂ comparisons across 100K prompts and 8+ model families, finding zero collisions. Minimum distances of 0.001–18.368 (Table 1) are many orders of magnitude above the 10⁻⁶ threshold. The quantization experiments (Tables 2–3) testing FP4 and INT8, which violate the real-analyticity assumption, show quantized models *more than double* minimum pairwise distances — even for 70B-parameter models.

- **SIpIT achieves provable exact recovery with practical efficiency:** Theorem 3.1 guarantees correctness in at most T|V| steps. Empirically (Table 4), 100% accuracy on FP4-quantized Mistral-7B (32K vocab) and Llama-3.1-8B (128K vocab) while exploring <0.22% of vocabulary, confirming linear scaling. Table 5 shows ~139× speedup over BruteForce.

- **Explicit failure-case analysis (lines 124–135):** Identifies specific adversarial constructions that could break injectivity (identical embeddings, tied positional embeddings) and explains why these are measure-zero events, strengthening credibility.

## Weaknesses

### Fatal
None

### Major
- **Disconnect between theoretical guarantee and algorithm's operating assumptions:** The theorems prove injectivity of the last-token map s → r(s; θ) ∈ ℝ^d, but SIpIT requires the full hidden-state matrix H^(ℓ) ∈ ℝ^{T×d} (all per-position states). The paper acknowledges this at line 141 ("designing an efficient algorithm for that setting is nontrivial and left to future work") and explains the logical chain at lines 143–145 (last-token state is a deterministic function of H^(ℓ), so injectivity extends to the full matrix). However, the paper's narrative — "injective → hence invertible → hence privacy risk" — treats these as one continuous story when there is a genuine gap: the title overstates the connection, and a reader who has access only to the final-layer last-token representation (the map the theory guarantees is injective) has no constructive method for recovery. This gap should be stated more prominently as a feature (the theory guarantees something stronger than the algorithm exploits) rather than conceded in a single sentence.

### Minor
- **Inconsistent algorithm naming:** The algorithm is called "SIFT" in the abstract (line 9), introduction (line 17), and Figure 1 (lines 21–25); "SIPIT" in §3 (line 139) and Algorithm 1; and "SiPT" in Tables 4–5 (lines 309, 319, 321). This inconsistency could confuse readers and should be unified.

- **HARDPROMPTS baseline comparison is uninformative:** In Table 5, HARDPROMPTS (Wen et al., 2023) achieves 0.00 accuracy while SiPT achieves 1.00. The paper acknowledges at line 293 that HARDPROMPTS "tackles a different setting" (output logprobs, approximate optimization). The 0% vs 100% comparison creates a misleading impression of a method's failure when it was never designed for this task. The BruteForce comparison (3890s vs 28s, same information access) already demonstrates SiPT's efficiency clearly.

- **High variance in SIpIT runtime deserves discussion:** Table 5 shows 28.01 ± 35.87 seconds for SiPT, indicating substantial variance across prompts. What makes some prompts harder? This is not discussed and would inform practical deployment.

### Trivial
- The Remark on line 163 ("the one-step map is almost surely injective") should be stated as a formal corollary since SIpIT's correctness depends on it, though the logical connection is briefly explained.

## Nice-to-Haves
- A method or analysis for exact recovery from the last-token state alone would close the most important gap in the paper's argument.
- Discussion of hidden-state quantization during inference (e.g., KV-cache compression) since SIpIT operates on hidden states and their precision matters directly.
- More inversion experiments beyond 100 prompts on GPT-2 Small and 50 prompts on Mistral/Llama.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "Discussion of ReLU-based models" — The paper explicitly states the real-analyticity assumption (line 67) and GELU dominates modern architectures. This is a bounded limitation, not a flaw.
- Criticisms about missing appendix content, proofs, or references — parser-stripped.
- The harsh critic's point about "information-theoretic presence vs practical accessibility" being overstated at line 347 — the paper's statement ("if probes or inversion methods fail, it is not because the information is missing") is a correct inference from injectivity and is appropriately qualified.
- Criticisms that the paper doesn't discuss KV-cache compression or hidden-state quantization — this is scope creep beyond the paper's stated contribution.

## Novel Insights
The paper makes a genuinely novel contribution by rigorously proving that the discrete-to-continuous map in decoder-only Transformers is almost-surely injective and persists under training — a property long informally assumed but never formally established. The proof technique (real-analyticity + measure-theoretic arguments applied to the parameter space, combined with GD-preservation via Inverse Function Theorem) is reusable and establishes injectivity as a structural property rather than an empirical artifact. The operationalization via SIpIT with provable linear-time guarantees bridges theory and practice, and the connection to privacy/regulatory frameworks (Hamburg DPA argument, line 349) provides a concrete real-world consequence.

## Suggestions
- Unify the algorithm name across the paper (recommend "SIpIT" since it's used in the formal algorithm section and theorem statements).
- Reframe the HARDPROMPTS comparison or move it to an appendix; the BruteForce comparison already clearly demonstrates efficiency.
- Add a brief analysis of what drives the high variance in SIpIT runtime (28.01 ± 35.87s).
- Strengthen the framing of the theory-algorithm gap as a feature: "the theory guarantees something stronger than what our algorithm currently exploits."

## Calibration Report

**Round 1 anchors retrieved:**
- "NEMESIS Jailbreaking" (1.40, score band 1.5) — weak survey, unrelated topic
- "Prompt Recovery for Image Generation Models" (3.00, band 1.5–3.5) — empirical comparison study, much weaker contribution
- "Affine Invariance in CNNs" (3.00, band 1.5–3.5) — theoretical but narrow
- "Provable ICL for Mixture of Linear Regressions" (5.00, band 3.5–5.5) — theoretical, accepted at 5.0, narrower significance
- "Provable optimal transport with transformers" (5.25, band 3.5–5.5) — theoretical, rejected, narrower scope
- "Vocabulary ICL" (6.00, band 5.5–7.5) — theoretical, accepted, less extensive experiments
- "Learn-to-Optimize for Sparse Recovery" (7.00, band 5.5–7.5) — similar structure (proof + experiments), accepted
- "Transformers are Universal In-context Learners" (6.67, band 5.5–7.5) — pure theory, accepted
- "When can transformers reason with abstract symbols" (7.60, band 7.5–8.5) — theoretical + empirical, comparable
- "Retrieval Head" (8.00, band 7.5–8.5) — empirical mechanistic, very strong, accepted
- Band 8.5+: No results found

**Round 2 anchors:**
- "Learn-to-Optimize" (7.00) — confirms lower bound
- "Transformers can optimally learn regression mixture" (6.80) — theoretical, lower than paper
- "Percolation Model of Emergence" (7.00) — theory + experiments
- "Not All Features Are Linear" (7.00) — empirical + theoretical
- "Polynomial Width for Set Representation" (7.25) — theoretical
- "Understanding Factual Recall via Associative Memories" (7.33) — theoretical + empirical
- "When can transformers reason" (7.60) — confirmed as comparison anchor

**Bracket:** Round 1 established 7.0–8.0; Round 2 narrowed to 7.0–7.5. The paper's core contribution (novel theoretical proof + most extensive empirical validation among all anchors + practical algorithm) places it above the 7.0 anchors. The theory-algorithm gap and presentation issues prevent it from reaching 8.0. Final score: **7.5**.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>