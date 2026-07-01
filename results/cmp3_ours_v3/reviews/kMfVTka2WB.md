## Summary

This paper proposes a Covariance-Adjusted SVM (CSVM) that derives class-specific Cholesky whitening transformations from covariance matrices, performs SVM on the transformed data, and uses an iterative algorithm (the SM Algorithm) to refine covariance estimates by incorporating test data. The paper claims the input space is "non-Euclidean" and that standard SVM is invalid there. Experiments on five datasets compare CSVM against linear, RBF, sigmoid, and polynomial kernel SVMs as well as PCA/ZCA whitening.

## Strengths

- **The paper identifies a meaningful operational question**: whether and how class covariance structure should influence SVM margin allocation. The algebraic derivation showing that transforming data by class-specific inverse Cholesky factors makes the margin depend on the inverse covariance matrix (equations 8–14) is mathematically sound and captures a genuine observation about how class dispersion could affect the optimal separating hyperplane.

- **The paper is clearly structured**, proceeding from mathematical motivation → algorithm → experiments, making it easy to follow the proposed method.

## Weaknesses

### Fatal
None.

### Major

- **The SM Algorithm uses test data features (with pseudo-labels) to refine the model but is compared against purely supervised baselines — a structurally unfair comparison.** Steps 2(f)–2(i) of the SM Algorithm label the held-out 20% test points using the current classifier, add them to the training set, recompute covariance matrices from the augmented set, and re-train. This places CSVM in a transductive/semi-supervised regime: it has access to test data features during training. The baselines (Linear, RBF, Sigmoid, Polynomial SVMs, PCA/ZCA whitening) are trained only on the 80% split and evaluated on the held-out 20%. The paper never acknowledges this asymmetry. Any observed improvement could be partially or fully attributable to this transductive advantage rather than to the covariance adjustment itself. A proper comparison would need to either (a) compare against semi-supervised/transductive baselines, or (b) use a purely supervised variant of CSVM where covariance is estimated from training data only.

- **Class-specific whitening creates incompatible coordinate systems, and the algorithm does not resolve this inconsistency.** Equations (3) define separate transformations for each class: $X_{y=1}^{\text{Euclidean}} = \Psi_{y=1}^{-1}X_{y=1}^{\text{Input}}$ and $X_{y=-1}^{\text{Euclidean}} = \Psi_{y=-1}^{-1}X_{y=-1}^{\text{Input}}$. When $\Psi_1 \neq \Psi_{-1}$ (the general case when class covariances differ), the two classes are mapped to different inner product spaces. Yet Step 2(c) of the SM Algorithm attempts to "perform support vector classification on Train_1 and Train_{-1} data in the Euclidean space" — but these two sets reside in different coordinate systems. A separating hyperplane cannot be meaningfully defined across two different vector spaces. The paper recognizes this tension in Lemma 2.2 (N classes → N classifiers) but the SM algorithm (step 2c) still seeks a single $\theta_{\text{Euclidean}}$, and the experiments evaluate a single classifier. How the N per-class classifiers from Lemma 2.2 are combined to make a single prediction is never addressed. The theoretical derivation and the implemented algorithm are inconsistent.

- **The empirical evaluation lacks basic statistical rigor.** Results are reported from a single 80:20 train/test split with no replication. There are no confidence intervals, no standard deviations, no cross-validation, and no statistical significance tests. On several datasets the reported differences are very small and well within the noise of a single split (e.g., Pulsar accuracy: CSVM 0.981 vs. Linear 0.979, a 0.2% absolute difference; Diabetes AUC: CSVM 0.74, Linear 0.74, PCA 0.74, ZCA 0.74 — identical). On OSHA, CSVM accuracy (0.752) is *lower* than RBF (0.760). On Pulsar precision, Linear SVM (0.962) beats CSVM (0.954). Without variance estimates, these comparisons are uninterpretable. The paper's claim of "marked improvement" (abstract) is not supported by the evidence presented.

- **The "non-Euclidean space" framing and Lemma 2.1 are overstated.** The paper repeatedly claims the input space is "non-Euclidean" and that KKT conditions are "valid only" after transformation via $\Psi^{-1}$ (Lemma 2.1). This conflates "the Euclidean metric is suboptimal for this data" with "the space is non-Euclidean." The data points reside in $\mathbb{R}^d$, which is a Euclidean space under the standard inner product; using Mahalanobis distance corresponds to choosing a different inner product within the same space, not leaving Euclidean space. Claiming that standard SVM is "invalid" in the input space is incorrect — SVM produces a well-defined classifier on raw $\mathbb{R}^d$ data regardless of metric choice. The algebraic derivation in equations (8)–(14) is correct as a manipulation showing what happens when you class-whiten and back-transform, but the strong framing that prior SVM work is "not valid" is unsupported and overstates the paper's novelty relative to existing covariance-weighted SVM methods (MCVSVM, Mahalanobis TSVM, etc.).

### Minor

- **No comparison against the most relevant prior work.** The paper cites MCVSVM (Zafeiriou et al. 2007), Mahalanobis TSVM (Peng & Xu 2012), MD-BLSSVM (Ke et al. 2018), and claims they have "gaps in application of appropriate vector spaces and dimensional inconsistencies" (line 21), but does not include any of them as baselines in the experiments. Without empirical comparison against the methods the paper claims to improve upon, the practical advantage of CSVM cannot be assessed.

- **No ablation of the SM algorithm's iterative component.** The SM algorithm has two distinct parts: (a) the class-specific Cholesky transformation of the data, and (b) iterative self-training on test data (adding pseudo-labeled test points to the training set). There is no experiment isolating the contribution of each. A simple baseline — apply the Cholesky transformation using only training data covariance matrices, train SVM on transformed data, evaluate without iteration — is absent. Without this, it is impossible to determine whether any improvement comes from the covariance adjustment or from the semi-supervised self-training procedure.

- **Missing experimental details hinder reproducibility.** The paper does not specify the SVM solver, the cost parameter $C$ (or whether it was tuned), kernel hyperparameters ($\gamma$ for RBF, degree for polynomial, coef0), whether features were standardized, dataset sizes/class balance/number of features, or the convergence threshold/criteria for the SM algorithm. These omissions prevent independent verification.

### Trivial
None.

## Nice-to-Haves

- The paper would benefit from discussing conditions under which the method would fail: when class covariances are similar (reduces to standard SVM with added cost) or when a class has few training samples (making covariance estimates singular or poorly conditioned).
- A discussion of how the N per-class classifiers from Lemma 2.2 are combined for prediction would strengthen the clarity of the method.

## Removed Points

These points from the input review were removed or modified per the filtering rules:

1. **"Core premise that input space is non-Euclidean invalidates paper's framing and lemmas" (original Issue 1):** Modified from "fatal/structural" to a major weakness. The paper's "non-Euclidean" framing is imprecise and Lemma 2.1 is overstated, but the algebraic derivation itself (showing that class-specific covariance affects margin allocation) is mathematically sound. The characterization that this "invalidates the paper's core claims" is too strong — the mathematical derivation in equations (8)–(14) stands on its own regardless of the framing terminology. The lemmas are consequences of class-specific whitening, not artifacts of a mistaken premise.

2. **Criticism about missing SVM solver and C parameter details (original Issue 5):** Retained in condensed form under Minor weaknesses. The broader set of missing details (dataset sizes, convergence criteria) is more substantive than trivial hyperparameter nitpicks.

3. **Generic strength "the paper correctly identifies that Mahalanobis distance can be expressed as Euclidean distance after a linear transformation":** Removed because this is a standard linear algebra fact (appears in any textbook covering Mahalanobis distance), not a novel contribution of this paper. The strength about "surfacing an often-unstated assumption" was retained.

## Novel Insights

The reviewer analysis surfaces two methodological issues that go beyond what the paper acknowledges: (1) class-specific Cholesky whitening maps different classes to different inner product spaces, making it mathematically unclear how a single separating hyperplane can be defined across these spaces — an inconsistency between the theoretical derivation (N classes → N classifiers, Lemma 2.2) and the implemented algorithm (which seeks a single $\theta$); and (2) the SM Algorithm's use of test data features with pseudo-labels places the evaluation in a transductive regime that is incomparable to the supervised baselines, meaning the reported improvements cannot be attributed to the covariance adjustment. These are critical methodological observations.

## Suggestions

1. Reframe the theoretical claims: drop the "non-Euclidean space" framing and present the method as a covariance-weighted margin SVM where Mahalanobis distance (via Cholesky whitening) replaces Euclidean distance. This preserves the algebraic derivation without overclaiming.
2. Redesign the evaluation to remove the transductive confound. Two options: (a) use a purely supervised variant where covariance is estimated from training data only, or (b) properly frame CSVM as a transductive/semi-supervised method and compare against appropriate baselines (transductive SVM, self-training with standard SVM).
3. Address the class-specific whitening coordinate problem: either use a single pooled covariance whitening (resolving the incompatibility), or clarify how the N per-class classifiers from Lemma 2.2 are combined into a single prediction rule.
4. Add statistical rigor: report cross-validated results with confidence intervals or standard deviations across multiple train/test splits.
5. Include an ablation that separates the effect of Cholesky whitening from the effect of iterative self-training.
6. Compare against the most relevant prior work (MCVSVM, Mahalanobis TSVM, MD-BLSSVM) that the paper claims to improve upon.

## Score and Decision

### Calibration Anchors

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Sparse Covariance Neural Networks | 3.00 | R1 | Shares covariance focus with this paper; has theory + experiments but poor presentation. This paper has clearer presentation but deeper structural flaws (test data leakage, coordinate inconsistency) making it comparable or weaker. |
| Bridging PCA and Neural Networks | 2.50 | R1 | Methodologically cleaner but weaker contribution. This paper has a more developed algorithm but more severe evaluation issues. |
| Exploring Cov/Hessian Matrices | 5.00 | R2 | Similar topic (covariance for binary classification), similar theory claims. That paper is stronger — coherent method without evaluation confounds. This paper is clearly below it. |
| One-Hot Encoding Strikes Back | 3.50 | R2 | Methodologically cleaner despite modest contribution. This paper has deeper structural problems. |
| Universal Clustering Bounds | 3.50 | R2 | Theoretical paper with proper proofs. This paper has more severe empirical flaws. |
| Deterministic Error Bounds (Clustering) | 3.50 | R2 | Clean theoretical contribution. This paper's evaluation issues are more severe. |
| SymCL (Riemannian Contrastive) | 4.00 | R2 | Has proper evaluation pipeline. This paper is weaker. |
| Language Models + Mahalanobis (CIL) | 5.25 | R2 | Uses Mahalanobis for continual learning; solid experiments. This paper is clearly weaker. |
| Matrix Function Normalizations (GCP) | 6.00 | R2 | High-quality covariance paper with proper theoretical and empirical work. This paper is far weaker. |

### Round 1 Bracket
After initial filtering and inspection of the paper's content, the plausible score range was **2.5–4.0**.

### Round 2 Narrowing
Comparison with the anchors confirms that this paper sits below the 4.0–5.0 range papers (which generally have coherent methodologies and proper evaluation) and is comparable to or slightly weaker than the 3.0-range papers. The test-data leakage and coordinate-space inconsistency are structural problems absent from those anchors.

### Final Score
**3.0 (Reject)** — The paper has a legitimate intuition (class covariance should affect SVM margin) and a mathematically sound algebraic core, but the evaluation is compromised by a structurally unfair comparison (transductive vs. supervised), the method contains an unresolved mathematical inconsistency (class-specific whitening creates incompatible coordinate spaces), and the experimental evidence lacks basic statistical rigor. These problems are too deep to address through minor revisions; a substantially redesigned evaluation and reframed theory would be needed.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>