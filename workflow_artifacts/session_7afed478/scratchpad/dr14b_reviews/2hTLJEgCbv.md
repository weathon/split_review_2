### Summary

The paper empirically studies different architectures for variational autoencoders (VAE) on MNIST. The authors vary the latent space size and different encoder/decoder architectures (CNNs, DNNs). They evaluate the models based on their reconstruction and generative performance, and also analyze the structure of the latent space. They find that simpler encoder architectures work best for encoding, while more complex decoder architectures with multiple convolutional layers are better at reconstructing the input data. They also find that non-zero KL divergence loss is important for preventing posterior collapse and maintaining meaningful latent representations.

### Soundness

1

### Presentation

1

### Contribution

1

### Strengths

The authors provide interesting insights about the structure of the latent space for different architectures. In particular, I was not aware of the negative trend between reconstruction and generative performance, as I would have assumed that better reconstructing the input data would also lead to better sample quality. It is interesting to see that this is not the case and that there is a sweet spot in between.

### Weaknesses

#### comment

The paper is unfortunately very thin on content. The authors only evaluate the models on MNIST, which is not a particularly complex dataset. I think applying the same methodology to other, more interesting datasets would make for a much more compelling paper. The paper is also pretty empirical and lacks theoretical insights. It also misses a lot of related work. For example, there has been a lot of work on improving VAEs in recent years, such as [1, 2, 3]. These references, and many others, propose various techniques for improving VAEs, including different architectures, which should be mentioned in the paper. Overall, I think the paper is not ready for publication at ICLR, but could perhaps be a good fit for a workshop.

There are also many grammar and spelling issues throughout the paper. I recommend using a service such as Grammarly to correct these.

[1] Dai, B. Y., & Wipf, D. (2019). Diagnosing and enhancing VAE models. Advances in neural information processing systems, 32.
[2] Ranganath, R., Blei, D., & Vehtari, A. (2016). Hierarchical variational models with normalizing flows. Advances in neural information processing systems, 29.
[3] Rezende, D. J., & Viola, F. (2018). Variational inference with normalizing flows. In Probabilistic machine learning: Proceedings of the 35th International Conference of the German Classification Society (Gesellschaft für Klassifikation e.V.) {GC 2017} (pp. 3-20). Springer Berlin Heidelberg.

### Questions

NA

### Rating

1

### Confidence

4

**********