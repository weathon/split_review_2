### Summary

This paper presents a new diffusion-based approach for time series generation. The proposed method includes transforming the time series into a video representation, then training a video diffusion model, and finally converting the output back to time series. The authors conduct experiments on several time series datasets and achieve state-of-the-art performance.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

The idea of treating time series as videos is novel, and the experimental results are impressive.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is limited to multivariate time series with a fixed number of variables. It cannot handle missing values or time series with a varying number of variables. This significantly restricts its applicability in real-world scenarios, where data is often incomplete or involves a dynamic set of variables. For instance, in sensor networks, some sensors might fail, leading to missing data, or new sensors might be added, resulting in a varying number of variables. The current method would require imputation or padding, which could introduce bias or reduce the quality of the generated time series.

2. The proposed STFT-to-video transformation requires a fixed window size, which limits the model to generating time series of a fixed length. This is a significant limitation because many real-world time series have varying lengths. The need for a fixed window size also means that the model may not be able to capture both short-term and long-term dependencies effectively. If the window is too small, long-term dependencies may be missed; if it's too large, short-term variations may be smoothed out.

3. The model is designed to handle only stationary data, as it uses STFT to capture time series dynamics. Stationarity is a strong assumption that is often violated in real-world time series. Many real-world time series exhibit non-stationary behavior, such as changes in mean, variance, or frequency content over time. The use of STFT, which assumes stationarity within the analysis window, may not be appropriate for such data, potentially leading to poor performance.

### Suggestions

The authors should address the limitations of their method regarding variable cardinality, time series length, and stationarity. For variable cardinality, the authors could explore methods that allow for variable-length input, such as using masking techniques or recurrent neural networks to handle missing values or a varying number of variables. This would make the method more robust and applicable to real-world datasets where the number of variables is not always fixed. For instance, the model could be modified to include a variable-length encoder that can process inputs with different numbers of variables, and then map them to a fixed-size latent space before applying the diffusion process. This would allow the model to handle time series with missing values or a varying number of variables without the need for imputation or padding.

To address the limitation of fixed-length time series, the authors could explore methods that allow for variable-length output. One approach could be to use a hierarchical diffusion process, where the model first generates a coarse representation of the time series and then refines it at different scales. Another approach could be to use a recurrent diffusion model that can generate time series sequentially, allowing for variable-length output. The authors could also consider using overlapping windows in the STFT, which could allow the model to capture both short-term and long-term dependencies more effectively. This would make the method more flexible and applicable to real-world datasets where the length of the time series is not always fixed. The authors should also investigate the impact of different window sizes on the performance of the model and provide guidelines for selecting the appropriate window size for different datasets.

Finally, to address the stationarity assumption, the authors could explore methods that are more robust to non-stationary data. One approach could be to use a time-frequency representation that is more adaptive to changes in the data, such as the wavelet transform. Another approach could be to use a model that can learn the dynamics of the time series directly, without relying on the STFT. The authors could also consider using a conditional diffusion model that can generate time series conditioned on some external information, such as the time of day or the day of the week, which could help to capture non-stationary behavior. The authors should also provide a more detailed analysis of the stationarity of the datasets they used in their experiments and discuss the potential impact of non-stationarity on the performance of their model.

### Questions

1. What is the length of the time series used in the experiments, and how is it determined? Is it possible to generate time series of arbitrary lengths?

2. What is the rationale behind using the EMA trend? Why not consider the trend component as part of the stationary residual?

3. How does the proposed method handle time series with a varying number of variables?

4. How does the proposed method handle time series of varying lengths?

### Rating

3

### Confidence

4

**********