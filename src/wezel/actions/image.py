import wezel
import scipy
import numpy as np


def all(parent): 
    parent.action(Zoom, text="Resize")
    parent.separator()
    parent.action(GaussianFilter, text="Gaussian Filter")
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
    parent.action(FourierShift, text="Fourier Shift")
    parent.action(FourierGaussianFilter, text="Fourier Gaussian Filter")
    parent.action(FourierUniformFilter, text="Fourier Uniform Filter")
    parent.action(FourierEllipsoidFilter, text="Fourier Ellipsoid Filter")


class FourierEllipsoidFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        size = 2.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"size (of ellipsoid kernel)", "type":"float", "value":size, "minimum": 1.0},
            title = 'Select Fourier Ellipsoid Filter settings')
        if cancel: 
            return

        # update defaults
        size = f[0]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = fourier_ellipsoid(
                sery, size,
            )
            app.display(resized)
        app.refresh()


class FourierUniformFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        size = 2.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"size (of uniform kernel)", "type":"float", "value":size, "minimum": 1.0},
            title = 'Select Fourier Uniform Filter settings')
        if cancel: 
            return

        # update defaults
        size = f[0]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = fourier_uniform(
                sery, size,
            )
            app.display(resized)
        app.refresh()



class FourierGaussianFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        sigma = 2.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":sigma, "minimum": 1.0},
            title = 'Select Fourier Gaussian Filter settings')
        if cancel: 
            return

        # update defaults
        sigma = f[0]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = fourier_gaussian(
                sery, sigma,
            )
            app.display(resized)
        app.refresh()



class FourierShift(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        hshift = 64
        vshift = 64

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"horizontal shift", "type":"float", "value":hshift},
            {"label":"vertical shift", "type":"float", "value":vshift},
            title = 'Select Sobel Filter settings')
        if cancel: 
            return

        # update defaults
        hshift = f[0]['value']
        vshift = f[1]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = fourier_shift(
                sery, [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class GaussianGradientMagnitudeFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        sigma = 2.0
        mode = 0
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":sigma, "minimum": 1.0},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Gaussian Gradient Magnitude Filter settings')
        if cancel: 
            return

        # update defaults
        sigma = f[0]['value']
        mode = f[1]['value']
        cval = f[2]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = gaussian_gradient_magnitude(
                sery, sigma,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class GaussianLaplaceFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        sigma = 2.0
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":sigma, "minimum": 1.0},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Gaussian Laplace Filter settings')
        if cancel: 
            return

        # update defaults
        sigma = f[0]['value']
        mode = f[1]['value']
        cval = f[2]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = gaussian_laplace(
                sery, sigma,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class LaplaceFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Laplace Filter settings')
        if cancel: 
            return

        # update defaults
        mode = f[0]['value']
        cval = f[1]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = laplace(
                sery,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()



class SobelFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        axis = 0
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"axis", "type":"dropdownlist", "list":['Horizontal', 'Vertical'], "value":axis},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Sobel Filter settings')
        if cancel: 
            return

        # update defaults
        axis = f[0]['value']
        mode = f[1]['value']
        cval = f[2]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = sobel_filter(
                sery,
                axis = axis,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class PrewittFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        axis = 0
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"axis", "type":"dropdownlist", "list":['Horizontal', 'Vertical'], "value":axis},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Prewitt Filter settings')
        if cancel: 
            return

        # update defaults
        axis = f[0]['value']
        mode = f[1]['value']
        cval = f[2]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = prewitt_filter(
                sery,
                axis = axis,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()



class MedianFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"size (of the median filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Median Filter settings')
            if cancel: 
                return
            # update defaults
            size = f[0]['value']
            mode = f[1]['value']
            cval = f[2]['value']
            hshift = f[3]['value']
            vshift = f[4]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = median_filter(
                sery,
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class PercentileFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        percentile = 50
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"percentile", "type":"float", "value":percentile, 'minimum':0, 'maximum':100},
                {"label":"size (of the percentile filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Percentile Filter settings')
            if cancel: 
                return
            # update defaults
            percentile = f[0]['value']
            size = f[1]['value']
            mode = f[2]['value']
            cval = f[3]['value']
            hshift = f[4]['value']
            vshift = f[5]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = percentile_filter(
                sery, percentile,
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()



class RankFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        rank = 10
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"rank", "type":"integer", "value":rank},
                {"label":"size (of the rank filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Rank Filter settings')
            if cancel: 
                return
            # update defaults
            rank = f[0]['value']
            size = f[1]['value']
            mode = f[2]['value']
            cval = f[3]['value']
            hshift = f[4]['value']
            vshift = f[5]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = rank_filter(
                sery, rank,
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class MaximumFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"size (of the maximum filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Maximum Filter settings')
            if cancel: 
                return
            # update defaults
            size = f[0]['value']
            mode = f[1]['value']
            cval = f[2]['value']
            hshift = f[3]['value']
            vshift = f[4]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = maximum_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class MinimumFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"size (of the minimum filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Minimum Filter settings')
            if cancel: 
                return
            # update defaults
            size = f[0]['value']
            mode = f[1]['value']
            cval = f[2]['value']
            hshift = f[3]['value']
            vshift = f[4]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = minimum_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class UniformFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"size (of the uniform filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Uniform Filter settings')
            if cancel: 
                return
            # update defaults
            size = f[0]['value']
            mode = f[1]['value']
            cval = f[2]['value']
            hshift = f[3]['value']
            vshift = f[4]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = uniform_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class GaussianFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":2.0, "minimum": 1.0},
            {"label":"order (0 = Gaussian, n = nth derivative of Gaussian)", "type":"integer", "value":0, "minimum": 0},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": 1},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":0.0},
            {"label":"truncate (at this many standard deviations)", "type":"float", "value":4.0, "minimum": 1.0},
            title = 'Select Gaussian Filter settings')
        if cancel: 
            return

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = gaussian_filter(
                sery, f[0]['value'],
                order = f[1]['value'],
                mode = modes[f[2]['value']],
                cval = f[3]['value'],
                truncate = f[4]['value'],
            )
            app.display(resized)
        app.refresh()


class Zoom(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {"type":"float", "label":"Resize with factor..", "value":2.0, "minimum": 0},
            title='Select parameter ranges')
        if cancel: 
            return
        factor = f[0]['value']

        # Resize series
        series = app.selected('Series')
        for sery in series:
            resized = zoom(sery, factor)
            app.display(resized)
        app.refresh()






# Functions for a new package dbimage -- a dbdicom wrapper for scipy.ndimage


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.fourier_uniform.html#scipy.ndimage.fourier_ellipsoid
def fourier_ellipsoid(input, size, **kwargs):
    """
    wrapper for scipy.ndimage.fourier_ellipsoid

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fourier Ellipsoid x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = np.fft.fft2(array)
        array = scipy.ndimage.fourier_ellipsoid(array, size, **kwargs)
        array = np.fft.ifft2(array).real
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.fourier_uniform.html#scipy.ndimage.fourier_uniform
def fourier_uniform(input, size, **kwargs):
    """
    wrapper for scipy.ndimage.fourier_uniform

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fourier Uniform x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = np.fft.fft2(array)
        array = scipy.ndimage.fourier_uniform(array, size, **kwargs)
        array = np.fft.ifft2(array).real
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.fourier_shift.html#scipy.ndimage.fourier_shift
def fourier_gaussian(input, sigma, **kwargs):
    """
    wrapper for scipy.ndimage.fourier_gaussian.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fourier Gaussian x ' + str(sigma) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = np.fft.fft2(array)
        array = scipy.ndimage.fourier_gaussian(array, sigma, **kwargs)
        array = np.fft.ifft2(array).real
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.fourier_shift.html#scipy.ndimage.fourier_shift
def fourier_shift(input, shift, **kwargs):
    """
    wrapper for scipy.ndimage.fourier_shift.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fourier Shift]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = np.fft.fft2(array)
        array = scipy.ndimage.fourier_shift(array, shift, **kwargs)
        array = np.fft.ifft2(array).real
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_gradient_magnitude.html#scipy.ndimage.gaussian_gradient_magnitude
def gaussian_gradient_magnitude(input, sigma, **kwargs):
    """
    wrapper for scipy.ndimage.gaussian_gradient_magnitude.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Gaussian Gradient Magnitude x ' + str(sigma) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.gaussian_gradient_magnitude(array, sigma, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_laplace.html#scipy.ndimage.gaussian_laplace
def gaussian_laplace(input, sigma, **kwargs):
    """
    wrapper for scipy.ndimage.gaussian_laplace.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Gaussian Laplace x ' + str(sigma) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.gaussian_laplace(array, sigma, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.laplace.html#scipy.ndimage.laplace
def laplace(input, **kwargs):
    """
    wrapper for scipy.ndimage.sobel.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Laplace Filter]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.laplace(array, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.sobel.html#scipy.ndimage.sobel
def sobel_filter(input, axis=-1, **kwargs):
    """
    wrapper for scipy.ndimage.sobel.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Sobel Filter along axis ' + str(axis) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.sobel(array, axis=axis, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.prewitt.html#scipy.ndimage.prewitt
def prewitt_filter(input, axis=-1, **kwargs):
    """
    wrapper for scipy.ndimage.prewitt.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Prewitt Filter along axis ' + str(axis) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.prewitt(array, axis=axis, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.median_filter.html#scipy.ndimage.median_filter
def median_filter(input, size=3, **kwargs):
    """
    wrapper for scipy.ndimage.median_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Median Filter with size ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.median_filter(array, size=size, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered



#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.percentile_filter.html#scipy.ndimage.percentile_filter
def percentile_filter(input, percentile, **kwargs):
    """
    wrapper for scipy.ndimage.percentile_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Percentile Filter x ' + str(percentile) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.percentile_filter(array, percentile, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.rank_filter.html#scipy.ndimage.rank_filter
def rank_filter(input, rank, **kwargs):
    """
    wrapper for scipy.ndimage.rank_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Rank Filter x ' + str(rank) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.rank_filter(array, rank, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.minimum_filter.html#scipy.ndimage.maximum_filter
def maximum_filter(input, size=3, **kwargs):
    """
    wrapper for scipy.ndimage.maximum_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Maximum Filter x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.maximum_filter(array, size=size, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.minimum_filter.html#scipy.ndimage.minimum_filter
def minimum_filter(input, size=3, **kwargs):
    """
    wrapper for scipy.ndimage.minimum_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Minimum Filter x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.minimum_filter(array, size=size, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.uniform_filter.html#scipy.ndimage.uniform_filter
def uniform_filter(input, size=3, **kwargs):
    """
    wrapper for scipy.ndimage.uniform_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Uniform Filter x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.uniform_filter(array, size=size, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html#scipy.ndimage.gaussian_filter
def gaussian_filter(input, sigma, **kwargs):
    """
    wrapper for scipy.ndimage.gaussian_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Gaussian Filter x ' + str(sigma) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    images = filtered.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.gaussian_filter(array, sigma, **kwargs)
        image.set_array(array)
        if 'order' in kwargs:
            if kwargs['order'] > 0:
                _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered





# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.zoom.html#scipy.ndimage.zoom
def zoom(input, zoom, **kwargs):
    """
    wrapper for scipy.ndimage.zoom.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    zoomed : dbdicom series
    """
    suffix = ' [Resize x ' + str(zoom) + ' ]'
    desc = input.instance().SeriesDescription
    zoomed = input.copy(SeriesDescription = desc + suffix)
    images = zoomed.instances()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Resizing ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.zoom(array, zoom, **kwargs)
        image.set_array(array)
        pixel_spacing = image.PixelSpacing
        image.PixelSpacing = [p/zoom for p in pixel_spacing]
        image.clear()
    input.status.hide()
    return zoomed


def affine_transform(input, matrix, **kwargs):

    suffix = ' [affine transform]'
    array, headers = input.array('SliceLocation', pixels_first=True)
    mapped = scipy.ndimage.affine_transform(array, matrix, **kwargs)
    desc = input.instance().SeriesDescription 
    mapped_series = input.new_sibling(SeriesDescription = desc+suffix)
    # Get header from input but insert correct geometry information
    # Apply the inverse transformation to the coordinate vectors
    mapped_series.set_array(mapped, headers, pixels_first=True)
    return mapped_series


# Helper functions

def _reset_window(image, array):
    min = np.amin(array)
    max = np.amax(array)
    image.WindowCenter= (max+min)/2
    image.WindowWidth = 0.9*(max-min)
