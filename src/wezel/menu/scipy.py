import numpy as np
import wezel
from dbdicom.wrappers import scipy


def all(parent): 
    parent.action(FunctionOfOneSeries, text='series => new series')
    parent.action(FunctionOfTwoSeries, text='(series 1, series 2) => new series')
    parent.separator()
    parent.action(Zoom, text="Resample images")
    parent.action(Resample3Disotropic, text="Resample 3D volume (isotropic)")
    parent.action(Resample3D, text="Resample 3D volume")
    parent.separator()
    parent.action(ResliceAxial, text='Reslice (axial)')
    parent.action(ResliceCoronal, text='Reslice (coronal)')
    parent.action(ResliceSagittal, text='Reslice (sagittal)')
    parent.separator()
    parent.action(OverlayOn, text='Overlay on..')
    parent.separator()
    parent.action(DistanceTransformEdt, text="Euclidian distance transform")
    parent.action(BinaryFillHoles, text="Fill holes")
    parent.action(Label2D, text="Label structures (2D)")
    parent.action(Label3D, text="Label structures (3D)")
    parent.separator()
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
    


class FunctionOfOneSeries(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            seriesList = series.parent().children()
            seriesLabels = [s.label() for s in seriesList]
            value = seriesList.index(series)
            operation = [
                '1 - series', 
                '- series',
                '1 / series',
                'exp(- series)',
                'exp(+ series)',
                ]
            input = wezel.widgets.UserInput(
                {"label":"series", "type":"dropdownlist", "list": seriesLabels, 'value':value},
                {"label":"Operation: ", "type":"dropdownlist", "list": operation, 'value':0},
                title = "Please select series and operation")
            if input.cancel:
                return
            series = seriesList[input.values[0]["value"]]
            operation = operation[input.values[1]["value"]]
            result = scipy.series_calculator(series, operation)
            app.display(result)
        app.refresh()


class FunctionOfTwoSeries(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        selected = app.selected('Series')
        if selected == []:
            return
        seriesList = selected[0].parent().children()
        value1 = seriesList.index(selected[0])
        try:
            value2 = seriesList.index(selected[1])
        except:
            value2 = value1
        seriesLabels = [s.label() for s in seriesList]
        operation = [
            'series 1 + series 2', 
            'series 1 - series 2',
            'series 1 / series 2',
            'series 1 * series 2',
            '(series 1 - series 2)/series 2',
            'average(series 1, series 2)',
            ]
        input = wezel.widgets.UserInput(
            {"label":"series 1", "type":"dropdownlist", "list": seriesLabels, 'value':value1},
            {"label":"series 2", "type":"dropdownlist", "list": seriesLabels, 'value':value2},
            {"label":"Operation: ", "type":"dropdownlist", "list": operation, 'value':1},
            title = "Please select factors and operation")
        if input.cancel:
            return
        series1 = seriesList[input.values[0]["value"]]
        series2 = seriesList[input.values[1]["value"]]
        operation = operation[input.values[2]["value"]]
        result = scipy.image_calculator(series1, series2, operation)
        app.display(result)
        app.refresh()
        


class OverlayOn(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            seriesList = series.parent().parent().series()
            seriesLabels = [s.instance().SeriesDescription for s in seriesList]
            input = wezel.widgets.UserInput(
                {"label":"Overlay on which series?", "type":"dropdownlist", "list": seriesLabels, 'value':0}, 
                title = "Please select underlay series")
            if input.cancel:
                return
            underlay = seriesList[input.values[0]["value"]]
            mapped = scipy.map_to(series, underlay)
            app.display(mapped)
        app.refresh()


class Resample3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            input = wezel.widgets.UserInput(
                {"label":"New voxel size in mm (height)", "type":"float", 'value':1.0, 'minimum':0.01}, 
                {"label":"New voxel size in mm (width)", "type":"float", 'value':1.0, 'minimum':0.01},
                {"label":"New voxel size in mm (depth)", "type":"float", 'value':1.0, 'minimum':0.01},
                title = "Please select new voxel size")
            if input.cancel:
                return
            voxel_size = [
                input.values[0]["value"], 
                input.values[1]["value"], 
                input.values[2]["value"]]
            resliced = scipy.resample(series, voxel_size=voxel_size)
            app.display(resliced)
        app.refresh()


class Resample3Disotropic(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            input = wezel.widgets.UserInput(
                {"label":"New voxel size (mm)", "type":"float", 'value':1.0, 'minimum':0.01}, 
                title = "Please select new voxel size")
            if input.cancel:
                return
            voxel_size = [
                input.values[0]["value"], 
                input.values[0]["value"], 
                input.values[0]["value"]]
            resliced = scipy.resample(series, voxel_size=voxel_size)
            app.display(resliced)
        app.refresh()


class ResliceAxial(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            resliced = scipy.reslice(series, orientation='axial')
            app.display(resliced)
        app.refresh()


class ResliceCoronal(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            resliced = scipy.reslice(series, orientation='coronal')
            app.display(resliced)
        app.refresh()


class ResliceSagittal(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            resliced = scipy.reslice(series, orientation='sagittal')
            app.display(resliced)
        app.refresh()


class Zoom(wezel.gui.Action): 

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
            resized = scipy.zoom(sery, factor)
            app.display(resized)
        app.refresh()


class FourierShift(wezel.gui.Action): 

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
            resized = scipy.fourier_shift(
                sery, [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class DistanceTransformEdt(wezel.gui.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        series = app.selected('Series')
        for sery in series:
            transformed = scipy.distance_transform_edt_3d(sery)
            app.display(transformed)
        app.refresh()


class BinaryFillHoles(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {   "label": "Size of the structuring element", 
                "type": "dropdownlist", 
                "list": ['1 pixel', '3 pixels', '5 pixels'], 
                "value": 0,
            },
            title = 'Select settings for filling holes.')
        if cancel: 
            return

        # update defaults
        if f[0]['value'] == 0:
            structure = None
        elif f[0]['value'] == 1:
            structure = np.array([   
                [0,1,0],
                [1,1,1],
                [0,1,0]])
        elif f[0]['value'] == 2:
            structure = np.array([   
                [0,0,1,0,0],
                [0,1,1,1,0],
                [1,1,1,1,1],
                [0,1,1,1,0],
                [0,0,1,0,0]])
        
        # Filter series
        series = app.selected('Series')
        for sery in series:
            filtered = scipy.binary_fill_holes(
                sery, 
                structure=structure
            )
            app.display(filtered)
        app.refresh()


class Label2D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {   "label": "Size of the structuring element", 
                "type": "dropdownlist", 
                "list": [
                        '3 pixels (plus)', 
                        '3 pixels (square)', 
                        '5 pixels (diamond)', 
                        '5 pixels (fat plus)',
                        '5 pixels (square)',
                        ], 
                "value": 0,
            },
            title = 'Select settings for image labelling.')
        if cancel: 
            return

        # update defaults
        if f[0]['value'] == 0:
            structure = np.array([   
                [0,1,0],
                [1,1,1],
                [0,1,0]])
        if f[0]['value'] == 1:
            structure = np.array([   
                [1,1,1],
                [1,1,1],
                [1,1,1]])
        elif f[0]['value'] == 2:
            structure = np.array([   
                [0,0,1,0,0],
                [0,1,1,1,0],
                [1,1,1,1,1],
                [0,1,1,1,0],
                [0,0,1,0,0]])
        elif f[0]['value'] == 3:
            structure = np.array([   
                [0,1,1,1,0],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [0,1,1,1,0]])
        elif f[0]['value'] == 4:
            structure = np.array([   
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1]])
        
        # Filter series
        series = app.selected('Series')
        for sery in series:
            filtered = scipy.label_2d(
                sery, 
                structure=structure
            )
            app.display(filtered)
        app.refresh()


class Label3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        series = app.selected('Series')
        for sery in series:
            result = scipy.label_3d(sery)
            app.display(result)
        app.refresh()


class FourierEllipsoidFilter(wezel.gui.Action): 

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
            resized = scipy.fourier_ellipsoid(
                sery, size,
            )
            app.display(resized)
        app.refresh()


class FourierUniformFilter(wezel.gui.Action): 

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
            resized = scipy.fourier_uniform(
                sery, size,
            )
            app.display(resized)
        app.refresh()


class FourierGaussianFilter(wezel.gui.Action): 

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
            resized = scipy.fourier_gaussian(
                sery, sigma,
            )
            app.display(resized)
        app.refresh()


class GaussianGradientMagnitudeFilter(wezel.gui.Action): 

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
            resized = scipy.gaussian_gradient_magnitude(
                sery, sigma,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class GaussianLaplaceFilter(wezel.gui.Action): 

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
            resized = scipy.gaussian_laplace(
                sery, sigma,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class LaplaceFilter(wezel.gui.Action): 

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
            resized = scipy.laplace(
                sery,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class SobelFilter(wezel.gui.Action): 

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
            resized = scipy.sobel_filter(
                sery,
                axis = axis,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class PrewittFilter(wezel.gui.Action): 

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
            resized = scipy.prewitt_filter(
                sery,
                axis = axis,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class MedianFilter(wezel.gui.Action): 

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
            resized = scipy.median_filter(
                sery,
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class PercentileFilter(wezel.gui.Action): 

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
            resized = scipy.percentile_filter(
                sery, percentile,
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class RankFilter(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        rank = 3
        size = 6
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
            try:
                resized = scipy.rank_filter(
                    sery, rank,
                    size = size,
                    mode = modes[mode],
                    cval = cval,
                    origin = [hshift, vshift],
                )
            except Exception as e:
                msg = str(e) + '\n Please try again with different parameters'
                app.dialog.error(msg)
            else:
                app.display(resized)
        app.refresh()


class MaximumFilter(wezel.gui.Action): 

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
            resized = scipy.maximum_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class MinimumFilter(wezel.gui.Action): 

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
            resized = scipy.minimum_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class UniformFilter(wezel.gui.Action): 

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
            resized = scipy.uniform_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class GaussianFilter(wezel.gui.Action): 

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
            resized = scipy.gaussian_filter(
                sery, f[0]['value'],
                order = f[1]['value'],
                mode = modes[f[2]['value']],
                cval = f[3]['value'],
                truncate = f[4]['value'],
            )
            app.display(resized)
        app.refresh()

