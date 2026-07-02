---
job_id: cb71f29a-08dc-4c69-a4ae-ed9b3c421f7b
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: 3wMdHl7JQ6.pdf
paper: Simplify to Amplify: Achieving Information-Theoretic Bounds with Fewer Steps in Spectral Community Detection
main_score_norm: 0.2
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope via learning theory and graph-based machine learning, specifically spectral methods for stochastic block models and recovery guarantees.

## Minimum Quality
Pass ✅. The submission has the required scientific structure, is written in English, and presents a complete argument with methodology, theory, experiments, and conclusion, although I have substantial concerns about the correctness and support of the main claims that I address in the full review.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find hidden prompts, manipulative instructions, or other signs of prompt injection in the provided paper content.

# Expected Review Outcome:
## Summary
This paper revisits the classic spectral approach for two-community SBM recovery and argues that a simplified version of Spectral Partition, specifically removing degree-threshold preprocessing and omitting the subsequent correction stage, is sufficient to obtain substantially better error bounds than previously attributed to the first stage alone. The paper combines a perturbation-based narrative, a Chernoff-based optimization surrogate, and a normal-approximation / Monte Carlo analysis to argue that the relationship between eigenvector alignment and classification error is much tighter than the standard quadratic bound. The empirical part compares these analytical curves to runs of the simplified spectral algorithm across several graph sizes.

## Strengths
The paper asks a concrete and interesting question: whether some of the extra machinery in older SBM spectral pipelines is actually necessary, or whether a more direct adjacency-spectrum method already captures most of the recoverability. That is a worthwhile angle, and if established rigorously it would be useful to both the theory and practice communities.

I appreciated that the submission does not merely claim “simpler is better” in vague terms, but points to a specific place where prior analysis may be loose, namely the passage from eigenvector alignment to misclassification error in Section 3.2. The optimization construction around Equation (9) is, at minimum, a good attempt to isolate where the classical worst-case argument may be pessimistic for the actual spectral vector produced by SBM.

The paper is also easy to follow at a high level. The progression from the original two-stage method in Figures 1 to 3, to the proposed simplification in Section 2.1, to the later analytical and empirical validation, is coherent. In particular, Figures 1 to 3 do a decent job of making the algorithmic difference explicit, and Figure 4 is helpful in showing what phenomenon the authors are trying to explain, namely that the empirical $\gamma$ versus $\sin \theta$ relationship appears much better than the coarse quadratic proxy from Theorem 3.2.

The experimental section, while limited, at least tries to connect several levels of analysis rather than reporting one isolated curve. Figure 5 is useful in that it overlays the baseline quadratic relationship, the Chernoff surrogate, the Monte Carlo / normal approximation, and direct spectral runs. Even though I do not think this is sufficient evidence for the paper’s main claims, it is a better visualization than a single cherry-picked plot.

The paper includes a reproducibility statement with fixed parameter choices, graph sizes, and repetition counts. That does not solve the deeper validity issues, but it is still a positive.

## Weaknesses
I have several serious concerns, and unfortunately they go to the core claims rather than to peripheral presentation details.

1. **The central theorem-level claim is not actually proved in the main paper.**  
The abstract, introduction, and conclusion repeatedly suggest that the simplified method “achieves” or “approaches” the information-theoretic inverse-log behavior associated with Theorem 1.3. However, the paper never states and proves a rigorous theorem for the modified algorithm of the form
\[
\gamma \le \exp\!\left(-c \frac{(a-b)^2}{a+b}\right)
\]
or the equivalent logarithmic relation. The key step in Section 4 is an *empirical fit*:
\[
\sin \theta = \frac{C}{\sqrt[4]{\log 2/\gamma}} \tag{13}
\]
and then the text on Page 8 says that this “combined with the claims of Theorems 2.2 and 3.1, directly yields the final result stated in Theorem 1.3.” This is much too loose. Equation (13) is not a theorem, the constant $C$ is obtained by OLS on the observed data, and there is no derivation connecting this fitted curve to a high-probability guarantee for the algorithm. As written, the paper provides a heuristic and empirical narrative, not a proof of the headline claim. For a theory paper, this is a major problem.

2. **The independence story in Section 2.1 / Section 3 is not justified, and in places it is simply incorrect.**  
On Page 3, Section 2.1 claims that by eliminating the degree-based deletion step and working directly with $A$, the method “can subsequently maintain independence in the entries of eigenvector $w_2$.” That is a very strong statement, and I do not see support for it anywhere. The entries of an eigenvector of a random matrix are complicated global functions of all matrix entries; independence of edge indicators in $A$ does not imply independence, or even approximate independence, of the coordinates of $w_2$. This matters a lot because Sections 3.3 to 3.5 effectively treat the coordinates used in the sorting-and-thresholding argument as if they follow a tractable i.i.d.-like distribution, which is exactly the kind of step that needs a very careful justification. Right now the paper slides from “the adjacency entries are independent” to “the relevant eigenvector entries behave independently enough,” but the latter is the nontrivial statement, and it is not established.

3. **The distributional approximation around Equation (10) is underspecified and appears inconsistent with the actual spectral quantity being analyzed.**  
Section 3.3 cites Abbe et al. for
\[
\left\|w_2 - \frac{A u_2}{a-b}\right\|_\infty = o(1/\sqrt{n}),
\]
then says the denominator $a-b$ is irrelevant because $w_2$ will be scaled to unit norm, and proceeds to analyze $A u_2$. There are several issues here.

First, the actual entry of $A u_2$ for $i \in V_1$ should inherit the $1/\sqrt{2n}$ scaling from Equation (4). More precisely, up to the diagonal convention and the $n$ versus $n-1$ detail,
\[
(Au_2)_i \approx \frac{1}{\sqrt{2n}}\Big(\mathrm{Bin}(n-1,a/n)-\mathrm{Bin}(n,b/n)\Big),
\]
not simply a raw difference of two binomials as in Equation (10). The paper explicitly discards this scaling and later reintroduces normalization by fitting curves, but that changes a derivation into a shape-matching exercise.

Second, even if one accepts the approximation to $A u_2$, the ordered coordinates $x_1,\dots,x_{2n}$ used in Section 3.4 are not raw i.i.d. samples from Equation (10); they are order statistics of a normalized spectral vector. The gap between those objects is exactly where the paper needs technical control, and instead it makes several informal leaps.

Third, the coordinates are not independent because vertices share edges, and because the final spectral vector is normalized globally. These dependencies may be weak asymptotically in some sense, but the paper does not state the sense, the regime, or the error terms needed for the later optimization arguments.

4. **The Chernoff-based optimization in Section 3.4 is not convincingly derived, and Equation (11) is especially troubling.**  
The move from tail bounds to deterministic ratio constraints on adjacent order statistics,
\[
x_{i+1} \le \frac{\ln C + \ln(2n+1)-\ln(i+1)}{\ln C + \ln(2n+1)-\ln i}x_i,
\]
is not well justified. A Chernoff upper bound on $P(X_i \ge a)$ does not directly imply that one particular ordered sample vector must satisfy these consecutive ratio constraints. The appendix admits a lot of looseness here, and on Pages 12 to 13 the argument becomes even shakier by saying, in effect, that the optimizer can set middle entries to zero because the constraints do not prevent it. That is not evidence that the formulation captures the true spectral vector; it is evidence that the relaxation may be far too weak.

More seriously, Equation (11) is advertised as an upper bound on $\cos \theta$:
\[
\cos \theta \le \frac{\sqrt{2n}}{t^*}(1-\gamma)\left(\ln C + 1 + \ln \frac{2+1/n}{1-\gamma}\right). \tag{11}
\]
Since $\cos \theta \le 1$ always, any bound that scales like $\sqrt{n}$ should immediately raise alarms unless the bracketed factor is correspondingly vanishing or negative in a controlled way. The paper never discusses this basic sanity check. A theorem predicting a quantity in $[-1,1]$ should at least be examined for whether it respects the range. Instead, the curve is then OLS-fitted to blue points in Figure 4a. At that point the result is better interpreted as an empirical parametric fit than as a predictive theoretical upper bound.

5. **The normal-approximation analysis in Section 3.5 is likewise post-hoc rather than predictive.**  
Equation (12) is presented as a theoretical prediction under a normal approximation, but the paper itself concedes on Page 7 that the unit-variance assumption is not valid and that the resulting curve must be rescaled:
“the theoretical prediction in Equation 12 captures the correct functional relationship ... but with a scaling factor that depends on the actual variance.”  
Then the green dashed line in Figure 4b is fit to the simulation data using OLS. Again, this is not a theorem, and it is not a clean approximation with known error. It is a shape hypothesis plus regression. That may be useful for exploratory work, but it does not support the strong claims in the abstract about achieving tighter bounds and approaching information-theoretic limits.

Figure 4b actually illustrates this concern quite vividly. The green band is a simulation cloud, the dashed green curve is fitted to that cloud, and the paper then treats their agreement as validation of the theoretical derivation. But when the main free scaling is learned from the same data being “validated,” the evidentiary value is limited.

6. **There is a major regime mismatch between the theoretical setup and the experiments.**  
The introduction and theorems are all framed around the sparse SBM with edge probabilities $a/n$ and $b/n$ for *constants* $a>b>0$, which implies constant expected degree. But the experiments on Pages 6 to 8 use
\[
a = 0.06n,\quad b = 0.04n.
\]
Plugging that into the model $a/n$ and $b/n$ means the actual edge probabilities are $0.06$ and $0.04$, which is a dense regime with expected degree $\Theta(n)$, not the sparse constant-degree regime emphasized throughout the theory. This is not a cosmetic detail. The spectral behavior, concentration, and recoverability are much easier in the dense regime, and several asymptotic approximations differ qualitatively. So the experiments do not actually test the paper’s stated theory in the intended setting. This significantly weakens the empirical support.

7. **The empirical evaluation does not compare against the key baselines needed to support the paper’s claims.**  
The paper’s whole thesis is that one can remove step 2 of Spectral Partition and also omit the Correction stage. Yet the experiments do not include the original Chin et al. pipeline with correction, nor the original Spectral Partition with deletion, nor an ablation isolating the effect of each modification. Figure 5 compares the paper’s own analytical surrogates and direct runs of the modified algorithm, but not the actual competing algorithmic procedures that the paper claims to improve upon.

This is particularly noticeable because there are no results tables at all. A compact table comparing, for example, original Spectral Partition, no-deletion Spectral Partition, full two-stage Partition, and perhaps a simple sign-thresholding baseline across several $(a,b,n)$ settings would have made the empirical case much stronger. As it stands, the reader gets curve overlays but not a clean algorithmic benchmark.

8. **Theorem 2.2 and the appendix proof are not checked at the level I would expect for the role they play.**  
The appendix proof of Theorem 2.2 invokes Füredi-Komlós and Krivelevich-Vu in a very broad-brush way. But the result in the main paper is not just “$\|M\| = O(\sqrt{a+b})$ in some regime”; it is the claim that the deletion step is unnecessary for the exact spectral-norm control needed by the original proof architecture. The appendix does not carefully discuss diagonal entries, heteroskedastic Bernoulli variances, or the precise asymptotic regime under which the constants are uniform. This is not automatically wrong, but given how central Theorem 2.2 is to the simplification claim, the proof sketch feels too casual.

9. **The literature positioning is too narrow for the scope of the claims.**  
The paper positions itself mainly against Chin et al. (2015), Coja-Oghlan (2009), Abbe et al. (2019), and Zhang and Zhou (2015). For a paper claiming near information-theoretic behavior of a simple spectral method, the discussion should be more complete with respect to more recent work on spectral thresholds and sharp SBM recovery limits. This matters because some of the “surprising” narrative in the paper may be less surprising once placed against the broader modern literature, and the paper currently overstates how isolated its perspective is.

10. **There are several smaller but still important notation and exposition issues that make the mathematical story harder to trust.**  
A few examples: Section 3.2 suddenly uses $w_i$ as the true community indicator values, even though $w_2$ was already used for the empirical eigenvector earlier, which is confusing. Equation (10) uses $\mathrm{Binomial}(n,a/n)$ rather than clarifying the diagonal convention or the $n-1$ within-community count. The paper sometimes treats scaling as irrelevant because vectors are normalized later, but then later compares quantities that do depend on those scales before fitting by OLS. None of these alone would sink the paper, but together they reinforce the sense that the mathematics is being handled too informally for the strength of the claims.

## Questions
1. The most important issue for me is the theorem gap. Can the authors provide a rigorous, self-contained statement and proof, in the main-paper regime, that the modified Spectral Partition alone achieves an inverse-logarithmic relation between $\gamma$ and $\frac{(a-b)^2}{a+b}$? Right now the paper moves from empirical fits in Equation (13) to theorem-level language without a proof.

2. Please clarify the exact quantity modeled by Equation (10). Should the entry of $A u_2$ not be scaled by $1/\sqrt{2n}$, and should the within-community count not be $\mathrm{Bin}(n-1,a/n)$ unless self-loops are allowed? If the answer is “normalization later absorbs this,” please explain how that preserves the subsequent derivations rather than merely the curve shape.

3. Can you justify the claim in Section 2.1 that removing high-degree deletion preserves or induces independence in the entries of $w_2$? If you only mean approximate entrywise asymptotics or weak dependence, please state that precisely and explain which steps in Sections 3.3 to 3.5 actually require independence versus merely concentration.

4. Why are the experiments run in the dense regime $a=0.06n$, $b=0.04n$, when the theory is written for constant $a,b$ and sparse probabilities $a/n$, $b/n$? I would like to see experiments in the actual stated regime, with fixed constants $a,b$ as $n$ varies.

5. Can you provide direct algorithmic comparisons, ideally in a table, among: original Spectral Partition, modified no-deletion Spectral Partition, full Chin et al. Partition with Correction, and perhaps a simple sign-thresholding variant? This would materially strengthen the empirical case that the removed steps are unnecessary.

6. For Equation (11), can you provide a sanity-check discussion of the range of the bound, since $\cos \theta \in [-1,1]$ but the expression appears to scale with $\sqrt{n}$? If the expression is only meant up to a fitted rescaling or only in a restricted asymptotic range, that needs to be stated clearly.

7. For Figure 5, can the authors separate what is theoretically predicted without any fitted constant from what is obtained only after OLS fitting? Right now the figure blends prediction and post-hoc calibration in a way that makes it difficult to assess what the theory actually explains.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No specific ethics concerns arise from the submission. The work is a theoretical/algorithmic study of community detection in synthetic stochastic block models.

## Soundness Rating
1: poor. The main claims are not adequately supported by rigorous theory or by appropriately matched experiments, and several core mathematical steps are either unjustified or inconsistent with the stated setting.

## Presentation Rating
2: fair. The paper is readable at a high level and the figures are helpful, but the mathematical exposition is too loose in key places, notation is occasionally inconsistent, and the empirical section does not cleanly support the claimed conclusions.

## Contribution Rating
2: fair. The underlying question is interesting, and the attempt to simplify classical spectral SBM recovery is worth exploring, but in its current form the paper does not convincingly establish the claimed contribution.

## Overall Rating
2: Reject, not good enough. The paper has an interesting premise, but the current submission overclaims relative to what is actually proved, relies on shaky distributional and independence assumptions, and validates theory in a different regime from the one the paper states. I would encourage the authors to tighten the mathematical argument substantially and add direct algorithmic comparisons.

## Reviewer Confidence
4: confident. I am confident in this assessment, having checked the main logical steps, equations, and the alignment between the stated theorems and the experiments, though I have not independently reconstructed every appendix derivation in full detail.