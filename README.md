# GMM-quiescent

This repo contains a tool for probabilistic selection of quiescent galaxies at z>2 from photometric data. 

## The basics of colour selections 

The most straight forward way to select a sample of quiescent galaxies from a photometric catalog is using criteria based on colour, e.g. the classical rest frame UVJ method ([Whitaker et al., 2012](https://iopscience.iop.org/article/10.1088/0004-637X/745/2/179), [Williams et al., 2009](https://iopscience.iop.org/article/10.1088/0004-637X/691/2/1879)), which requires galaxies to have red colours (i.e, _U-V_ and _V-J_ are positive). The foundation of colour selections is great because essentially you're measuring the shape of the observed SED (if your rest frame colours are calculated via some kind of interpolation method), and rest frame colours are relatively fast and easy to compute. Then, making a binary selection based on these properties is also fast and easy. 

## Why probabilistic selection? 

The idea behind probabilistic selection is that each galaxy occupies a locus in colour space because of the uncertainties, and the intrinsic galaxy populations cluster in those spaces in a way that can be modelled using N dimensional Gaussians, where each Gaussian represents a colour. You can then use these pieces of information to make flexible (or strict) population samples. This can come in handy when the observed colour space has large scatter, because instead of galaxies being assigned to a population based on the chance they fall on one side of a dividing line, the "blurriness" is taken into account. 

## How does it work?

In this case, I computed the boot strapped* _NUV-U_, _U-V_ and _V-J_ colours of massive (log(mstar/msun)>10.6) galaxies at 2<z<3 and then fit the colour space with a Gaussian Mixture Model. The number of components is unimportant, what we care about is the probability of each galaxy to be contained within the cloud we expect quiescent galaxies to occupy.  Because its calculated using the boot strapped colours, you can decide not only how far into this cloud the galaxy needs to be, but also how much of the galaxy's colour distribution needs to be inside this cloud.


* Assume rest frame fluxes X,Y and their uncertainities Xe,Ye are the mean and standard deviation of a normal distribution and draw samples from each distribution to create a distribution of colour _X-Y_

## How do I use it?

In numbers, this means deciding a threshold T (0<T<1) for how far into the cloud, and a p(q) percentile that has to be above that threshold. The model returns the 1 and 2 sigma percentiles as well as the median p(q), so all you need to do is decide how strict you want to be. 

If you don't want to think about that, you can also use the thresholds in [Gould et al., 2023](https://iopscience.iop.org/article/10.3847/1538-3881/accadc) or [Valentino et al., 2023](https://iopscience.iop.org/article/10.3847/1538-4357/acbefa)

Please see the tutorial notebook for a walk through example.  

### If you use this code, please cite the following works: 

[Gould et al., 2023](https://iopscience.iop.org/article/10.3847/1538-3881/accadc)
[Valentino et al., 2023](https://iopscience.iop.org/article/10.3847/1538-4357/acbefa) 

This method uses the GMM tool from SciKit Learn, so I also suggest you cite that too: 

[Scikit-learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.](https://ui.adsabs.harvard.edu/abs/2011JMLR...12.2825P/abstract)
