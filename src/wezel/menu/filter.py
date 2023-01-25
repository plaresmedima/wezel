
from wezel.menu.scipy import (
    FourierShift,
    GaussianFilter,
    UniformFilter,
    MinimumFilter,
    MaximumFilter,
    RankFilter,
    PercentileFilter,
    MedianFilter,
    PrewittFilter,
    SobelFilter,
    LaplaceFilter,
    GaussianLaplaceFilter,
    GaussianGradientMagnitudeFilter,
    FourierGaussianFilter,
    FourierUniformFilter,
    FourierEllipsoidFilter,
)


def all(parent): 
    parent.action(GaussianFilter, text="Gaussian Filter")
    parent.separator()
    parent.action(UniformFilter, text="Uniform Filter")
    parent.action(MinimumFilter, text="Minimum Filter")
    parent.action(MaximumFilter, text="Maximum Filter")
    parent.action(RankFilter, text="Rank Filter")
    parent.action(PercentileFilter, text="Percentile Filter")
    parent.action(MedianFilter, text="Median Filter")
    parent.separator()
    parent.action(PrewittFilter, text="Prewitt Filter")
    parent.action(SobelFilter, text="Sobel Filter")
    parent.action(LaplaceFilter, text="Laplace Filter")
    parent.action(GaussianLaplaceFilter, text="Gaussian Laplace Filter")
    parent.action(GaussianGradientMagnitudeFilter, text="Gaussian Gradient Magnitude Filter")
    parent.separator()
    parent.action(FourierShift, text="Shift image")
    parent.action(FourierGaussianFilter, text="Fourier Gaussian Filter")
    parent.action(FourierUniformFilter, text="Fourier Uniform Filter")
    parent.action(FourierEllipsoidFilter, text="Fourier Ellipsoid Filter")
