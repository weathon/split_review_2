## Summary

IsingFormer is a decoder-only Transformer trained on equilibrium spin configurations at multiple inverse temperatures. It is integrated into Parallel Tempering (PT) as a global proposal generator, forming Transformer-Augmented Parallel Tempering (TAPT). The framework casts the pairing as a generator-verifier collaboration: the Transformer proposes nonlocal moves, and the Metropolis criterion in PT accepts or rejects them, preserving (approximately) detailed balance. The method is evaluated on 2D ferromagnetic Ising sampling, 3D spin glass optimization, and integer factorization encoded as Ising problems.

## Strengths

- **Physically rigorous validation.** IsingFormer is evaluated against the exact Onsager/Kac-Ward solution for the 2D Ising model. Reproducing free energy, magnetization, and energy variance (including across the critical region and under half-clamped boundary conditions unseen during training) is a non-trivial quantitative bar.
- **Principled theoretical grounding.** The choice of an autoregressive model is well-motivated: it allows exact computation of proposal probabilities, enabling a full Metropolis-Hastings correction (even if unused here). This clearly distinguishes the approach from encoder-decoder alternatives.
- **Generalization across problem instances.** The 16-bit factorization experiment demonstrates that a single trained model improves PT on ~64% of 190 held-out semiprimes, showing transfer beyond training distribution. This is the paper's most significant result and addresses a known failure mode of neural optimizers (per-instance retraining).
- **Clean ablations.** The comparison between warm-start-only and periodic proposals in the spin glass experiment clearly isolates the contribution of repeated global moves from a one-time initialization benefit.

## Weaknesses

### Fatal
None.

### Major

- **No generalization across spin glass instances.** For the 3D spin glass, the paper explicitly acknowledges: "the generator does not generalize to other instances (its proposals were entirely rejected)." This means training cost must be paid per instance for generic Ising optimization. The paper's strongest generalization claim rests entirely on factorization, which has a special shared circuit structure that makes conditioning natural. For the broad combinatorial optimization framing, this is a substantial limitation.
- **Small problem scales.** The spin glass uses L³ = 10³ spins, and factorization uses at most 200 spins (16-bit). Claims about replacing "thousands of local updates" and broader scalability are not demonstrated at problem sizes that would be practically relevant for hard combinatorial optimization. The transformer inference cost relative to MCMC sweeps at larger scales is uncharacterized in the main text.

### Minor

- **Uncorrected Metropolis criterion.** The paper uses the simplified acceptance rule (Eq. 2) rather than the full MH correction it argues is available. For the sampling use case (2D Ising), this formally undermines the detailed balance guarantee. The paper discusses this honestly but does not quantify the induced bias.
- **Factorization improvement magnitude.** On the 16-bit test set, TAPT wins on ~64%, is tied on ~9%, and loses on ~27% of instances. The scatter plots in Fig. 4 show many cases where PT already achieves high success and TAPT's improvement is marginal. A summary metric (e.g., average gain in success probability) would better characterize the practical benefit.
- **Single ground state reference.** The residual energy for the 3D spin glass uses an estimate of E_gnd from simulated annealing, not a certified ground state. The reported ρ values are therefore lower bounds on true residual energy.

### Trivial
- The figure captions appear duplicated in the parsed text (an OCR/parsing artifact, not a paper flaw).

## Nice-to-Haves

- Reporting wall-clock time comparisons in the main text rather than only the appendix would help readers assess the practical cost-benefit tradeoff, especially since transformer inference is substantially more expensive than a spin flip.
- A small experiment demonstrating the MH-corrected TAPT (even on 2D Ising) would strengthen the theoretical narrative.

## Novel Insights

The most genuinely novel contribution is the observation that conditioning a shared generative model on clamped output bits of a combinatorial circuit enables cross-instance generalization of learned MCMC proposals. This reframes the generalization challenge for neural combinatorial optimization: rather than generalizing over coupling matrices J (which the paper shows is hard), one can generalize over parameterically defined instance families where the shared structure is explicit. This suggests a productive middle ground between per-instance neural optimizers and fully general solvers.

## Suggestions

- Extend the factorization experiment to 32-bit semiprimes to probe the scaling limits of the approach.
- Characterize where TAPT loses to PT on the test set—does PT win when the correct factors are "easy" (close to random walk) or structurally atypical semiprimes?
- Explore whether training on random instances of Edwards-Anderson spin glasses with varying J can produce proposals that generalize across the ensemble, directly addressing the spin-glass limitation.

## Score and Decision

The paper presents a clean and well-motivated framework backed by physically rigorous validation. The factorization generalization result is genuinely interesting, though the spin glass limitation—requiring per-instance training for generic problems—significantly narrows the scope of the optimization claims. Problem scales are modest. Overall this is solid work with one clear major limitation that constrains its general claims.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>