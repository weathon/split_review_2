Here is the final consolidated review.

---

## Summary

This paper develops a unified theoretical framework for constructing equivariant machine learning architectures on tensors that respect the symmetries of the orthogonal group O(d), the indefinite orthogonal group O(s,d−s) (including the Lorentz group), and the symplectic group Sp(d). Using classical invariant theory, the authors characterize all polynomial (and by Stone–Weierstrass, all continuous) equivariant functions mapping tensor inputs to tensor outputs, and derive practical parameterizations for the vector-input case (Corollaries 1 and 3) and the symmetric‑2‑tensor case (Corollary 2). The framework is evaluated on three problems: stress‑strain prediction in materials science, path‑signature estimation for time series, and sparse vector estimation.

---

## Strengths

- **Unified and principled theoretical framework.** Sections 3–4 provide a clean characterization of equivariant tensor-to-tensor polynomials for O(d), O(s,d−s), and Sp(d) via invariant theory. Theorem 1 and its generalization Theorem 2 are precisely stated, and Corollaries 1–3 bridge abstract invariant theory to implementable architectures. The paper is honest about its theoretical debts (Jeffreys 1973, Roe Goodman 2009, Appleby et al. 1987) and does not overclaim novelty in the invariant theory itself — the contribution is in the packaging, connecting established theory to ML.

- **Strong empirical results on two of three problems.** The stress‑strain experiment (Table 1) shows the equivariant model outperforming all baselines (MLP, augmented MLP, and the prior equivariant method TFENN) by roughly 1–2 orders of magnitude across all three dataset sizes. The path‑signature experiment (Table 2) demonstrates substantial gains over multiple MLP baselines for both O(d) and Lorentz groups, with the Lorentz improvement being especially large (0.005 vs 0.186 for the best MLP baseline) — this is the paper's most novel group application.

- **Extension beyond SO(3)/O(3).** Unlike existing libraries such as e3nn, which are specific to SO(d)/O(d) for d = 2, 3, this framework extends to indefinite orthogonal groups (Lorentz) and the symplectic group, which have genuine relevance in physics (special relativity, classical and quantum mechanics).

---

## Weaknesses

### Major

1. **The sparse vector experiment (Table 3) has problems that weaken its support for the paper's claims.** (a) The MLP baseline is near chance (~0.2 ≈ 1/d for d = 5) in 9 of 12 configurations, yet the paper does not explain why a presumably well-tuned non-equivariant model cannot learn anything above random on a problem where SoS methods achieve 0.96. The paper reports that the MLP fits training data well (Table 7 in the appendix), so the failure is about generalization, but without more detail on MLP architecture and hyperparameter tuning, the reader cannot rule out that the baseline was simply not configured to succeed. (b) More importantly, **Ours(Diag) — a simplified variant using only vector norms — outperforms the full Ours model in 6 out of 12 configurations, often by a wide margin** (e.g., 0.914 vs 0.463 on Bernoulli‑Gaussian with Diagonal covariance; 0.908 vs 0.342 on Bernoulli‑Gaussian with Identity covariance). Since the full model is strictly more expressive (it has access to all pairwise inner products), this pattern suggests the cross‑product terms cause overfitting or that the simpler model is genuinely preferable in many settings. The paper reports this without analysis or explanation.

2. **The symplectic group appears in the title, theoretical development (Section 4, Corollary 3, Theorem 2), and contribution list, but is never tested empirically.** The path‑signature section mentions the problem is "also equivariant under the Lorentz and symplectic groups" (line 264) but only tests O(d) and Lorentz. None of the three experiments validate Sp(d). This is a significant gap between the advertised scope and what is demonstrated.

### Minor

3. **The data augmentation baselines use only 4 random transformations** in both the stress‑strain (Table 1) and path‑signature (Table 2) experiments. For O(d), 4 random rotations in d‑dimensional space cover essentially none of the symmetry group; for the non‑compact Lorentz group the coverage is even sparser. A properly augmented baseline would use substantially more augmentations (e.g., dozens or hundreds), especially since the equivariant model sees all possible transformations implicitly. This does not invalidate the method's advantage over non‑augmented baselines, but it weakens the headline claim that learning equivariance beats augmentation.

4. **The paper lacks a limitations section.** The Discussion (Section 6) is a single paragraph with no reflection on when the method might fail, the computational bottleneck for higher‑order tensor outputs (acknowledged but not discussed as a limitation), the mixed sparse‑vector results, or the symplectic validation gap. For a paper with as broad a claimed scope as this one, this is a notable omission.

5. **Minor presentation issues.** (a) The abstract claims "universally expressive" architectures but omits the Stone–Weierstrass-on-compact-sets caveat that the main text correctly includes. (b) The paper advises readers to focus on Corollary 1 for practical applications, but the stress‑strain experiment actually uses Corollary 2 (symmetric 2‑tensor to symmetric 2‑tensor), which is a structurally different construction based on eigenvalue decomposition. This mismatch could mislead a reader following the suggested path.

### Trivial

None.

---

## Nice-to-Haves

- A small synthetic experiment validating Sp(d) equivariance (e.g., verifying the Sp(d) version of Corollary 3 on a known equivariant map) would substantially strengthen the paper's claimed generality.
- Increasing the number of augmentations (e.g., 50–100) for the data-augmentation baselines would provide a fairer comparison and strengthen the claim that equivariance beats augmentation.
- Analysis of why Ours(Diag) outperforms Ours in certain configurations (e.g., examining the learned q‑functions, regularization sensitivity, or the role of cross‑product terms) could illuminate the trade‑off between expressivity and overfitting.
- A brief limitations paragraph in the Discussion would improve scholarly completeness.

---

## Removed Points

These points were flagged by the harsh critic but are removed from the main review for the reasons given below:

- **"The MLP baseline is at chance in 12 out of 12 rows."** — Factually wrong. In the Bernoulli‑Rademacher rows, the MLP baseline achieves 0.845–0.923 (well above the 0.2 random baseline). The critic overstated the pervasiveness of the failure. The corrected observation (9 of 12 configurations) is retained as part of Major Weakness 1.

- **"The comparison 'equivariant beats non-equivariant' is trivially true but minimally informative."** — Overly dismissive. The paper shows the MLP fits training data well but generalizes poorly, which genuinely supports claims about the importance of inductive bias. This is not a trivial finding.

- **"Exponential complexity is a critical issue."** — The paper honestly acknowledges this limitation (complexity O(k′! n^k′ …), practical only for k′ ∈ {1,2,3,4}) and notes these values already capture many practical cases. This is an understood trade‑off, not a fatal unaddressed flaw. Retained implicitly as context.

- **"No code release mentioned."** — Per the hard rules, questioning availability of resources cited in the paper is not permitted.

- **"Comparing against e3nn understates the limitation."** — The paper explicitly compares with e3nn and states "computational and approximation power should be equivalent, however, the parameterization is different." This is a fair characterization.

---

## Novel Insights

None beyond the paper's own contributions. The calibration search revealed a previous version of this same paper ("Learning equivariant tensor functions with applications to sparse vector recovery", avg score 5.75, rejected) that had only the sparse vector experiment. The current paper significantly strengthens the experimental portfolio with two additional well‑executed applications (stress‑strain and path‑signature), which is the main advance over the earlier version. The core theoretical framework was already present in the earlier version.

---

## Suggestions

1. **For the sparse vector experiment:** Either (a) demonstrate that a substantially tuned non‑equivariant model (with adequate width, depth, learning rate scheduling, and regularization) still fails, confirming the need for equivariance, or (b) provide a detailed analysis of why the MLP fails in 9/12 configurations but succeeds on Bernoulli‑Rademacher. Crucially, analyze and explain why Ours(Diag) outperforms the full Ours model in half the configurations — this unexpected pattern undermines the claim that the full equivariant architecture is uniformly beneficial.

2. **Validate the symplectic group** on at least one small synthetic task. Even a toy problem demonstrating Sp(d) equivariance would close the gap between advertised scope and empirical validation.

3. **Add a limitations paragraph** discussing computational complexity for higher‑order outputs, the symplectic validation gap, the mixed sparse‑vector results, and when the method may not be the best choice.

---

## Score and Decision

**Score anchors used for calibration:**

| Path | Avg Score | Round | Comparison to this paper |
|---|---|---|---|
| `kyVzYpDxHg.md` ("Learning equivariant tensor functions") | 5.75 | R1+R2 | Previous version with only sparse vector experiment; this paper adds two strong experiments → clearly stronger |
| `tzpXhoNel1.md` (GRepsNet) | 4.25 | R1 | General equivariant network paper with clarity issues; our paper has clearer theory and stronger experiments → stronger |
| `79FVDdfoSR.md` (Characterization Theorem) | 7.00 | R1+R2 | Pure theory paper with strong formal results; different style of contribution |
| `gyfXuRfxW2.md` (SL(2,R)-equivariance) | 7.00 | R2 | Non-compact group equivariance with novel theoretical finding (non-universality); comparable mix of theory+experiments but has a result ours lacks |
| `5i6ZZUjCA9.md` (Affine Steerable Equivariant Layer) | 5.75 | R2 | General equivariant framework accepted; our paper has more experimental breadth |

**Bracket (Round 1):** 5.5–7.5  
**Narrowing (Round 2):** The previous version of this paper scored 5.75 with only one experiment. Our version adds two strong experiments but retains the same weaknesses in the sparse vector experiment and the symplectic gap. The 6.0–6.5 band fits: above the previous version (5.75) and above GRepsNet (4.25), but below the 7.0-level papers which either have cleaner experimental stories or additional novel theoretical findings.

**Final score:** 6.0 — borderline accept. The paper makes a genuinely useful theoretical contribution with clear practical value on two of three experiments. The issues with the sparse vector experiment and the missing symplectic validation are real but not fatal — they can be addressed in revision. Considering all anchors, this paper sits just above the acceptance threshold.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>