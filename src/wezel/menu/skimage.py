import wezel
from dbdicom.wrappers import skimage


class VolumeFeatures(wezel.gui.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0 

    def run(self, app):
        for series in app.selected('Series'):
            result = skimage.volume_features(series)
            #display


class AreaOpening2D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        cancel, f = app.dialog.input(
            {"label":"Remove bright structures with an area less than.. (in pixels)", "type":"integer", "value": 9, "minimum": 1},
            {"label":"Connectivity (in pixels)", "type":"integer", "value": 1, "minimum": 1},
            title = 'Select area opening settings')
        if cancel: 
            return
        for series in app.selected('Series'):
            result = skimage.area_opening_2d(
                series, 
                area_threshold = f[0]['value'],
                connectivity = f[1]['value'])
            app.display(result)
        app.refresh()


class AreaOpening3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        cancel, f = app.dialog.input(
            {"label":"Remove bright structures with a volume less than.. (in pixels)", "type":"integer", "value": 9, "minimum": 1},
            {"label":"Connectivity (in pixels)", "type":"integer", "value": 1, "minimum": 1},
            title = 'Select area opening settings')
        if cancel: 
            return
        for series in app.selected('Series'):
            result = skimage.area_opening_3d(
                series, 
                area_threshold = f[0]['value'],
                connectivity = f[1]['value'])
            app.display(result)
        app.refresh()


class AreaClosing2D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        cancel, f = app.dialog.input(
            {"label":"Remove dark structures with an area less than.. (in pixels)", "type":"integer", "value": 27, "minimum": 1},
            {"label":"Connectivity (in pixels)", "type":"integer", "value": 1, "minimum": 1},
            title = 'Select area opening settings')
        if cancel: 
            return
        for series in app.selected('Series'):
            result = skimage.area_closing_2d(
                series, 
                area_threshold = f[0]['value'],
                connectivity = f[1]['value'])
            app.display(result)
        app.refresh()


class AreaClosing3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        cancel, f = app.dialog.input(
            {"label":"Remove dark structures with volume less than.. (in pixels)", "type":"integer", "value": 27, "minimum": 1},
            {"label":"Connectivity (in pixels)", "type":"integer", "value": 1, "minimum": 1},
            title = 'Select area opening settings')
        if cancel: 
            return
        for series in app.selected('Series'):
            result = skimage.area_closing_3d(
                series, 
                area_threshold = f[0]['value'],
                connectivity = f[1]['value'])
            app.display(result)
        app.refresh()


class Opening2D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            result = skimage.opening_2d(series)
            app.display(result)
        app.refresh()


class Opening3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            result = skimage.opening_3d(series)
            app.display(result)
        app.refresh()


class Closing2D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            result = skimage.closing_2d(series)
            app.display(result)
        app.refresh()


class Closing3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            result = skimage.closing_3d(series)
            app.display(result)
        app.refresh()


class RemoveSmallHoles2D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        cancel, f = app.dialog.input(
            {"label":"Remove dark structures with an area less than.. (in pixels)", "type":"integer", "value": 9, "minimum": 1},
            {"label":"Connectivity (in pixels)", "type":"integer", "value": 1, "minimum": 1},
            title = 'Select area opening settings')
        if cancel: 
            return
        for series in app.selected('Series'):
            result = skimage.remove_small_holes_2d(
                series, 
                area_threshold = f[0]['value'],
                connectivity = f[1]['value'])
            app.display(result)
        app.refresh()


class RemoveSmallHoles3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        cancel, f = app.dialog.input(
            {"label":"Remove dark structures with volume less than.. (in pixels)", "type":"integer", "value": 27, "minimum": 1},
            {"label":"Connectivity (in pixels)", "type":"integer", "value": 1, "minimum": 1},
            title = 'Select area opening settings')
        if cancel: 
            return
        for series in app.selected('Series'):
            result = skimage.remove_small_holes_3d(
                series, 
                area_threshold = f[0]['value'],
                connectivity = f[1]['value'])
            app.display(result)
        app.refresh()


class Skeletonize_3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        for sery in app.selected('Series'):
            result = skimage.skeletonize_3d(sery)
            app.display(result)
        app.refresh()


class Skeletonize(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        for sery in app.selected('Series'):
            result = skimage.skeletonize(sery)
            app.display(result)
        app.refresh()


class ConvexHullImage(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        for sery in app.selected('Series'):
            result = skimage.convex_hull_image(sery)
            app.display(result)
        app.refresh()


class CannyFilter(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        sigma = 1.0
        low_threshold = 25.
        high_threshold = 75.
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":sigma, "minimum": 1.0},
            {"label":"low threshold (%)", "type":"float", "value": low_threshold, "minimum": 0.0, 'maximum':100.0},
            {"label":"high threshold (%)", "type":"float", "value": high_threshold, "minimum": 0.0, 'maximum':100.0},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Canny Edge Filter settings')
        if cancel: 
            return

        # update defaults
        sigma = f[0]['value']
        low_threshold = f[1]['value']/100
        high_threshold = f[2]['value']/100
        mode = f[3]['value']
        cval = f[4]['value']

        # Filter series
        for sery in app.selected('Series'):
            filtered = skimage.canny(
                sery, 
                sigma = sigma,
                low_threshold = low_threshold,
                high_threshold = high_threshold,
                use_quantiles = True,
                mode = modes[mode],
                cval = cval,
            )
            app.display(filtered)
        app.refresh()


class PeakLocalMax3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        selected = app.selected('Series')
        series_list = selected[0].parent().children()
        series_labels = [s.instance().SeriesDescription for s in series_list]

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"Find local maxima of series..", "type":"dropdownlist", "list": series_labels, "value": series_list.index(selected[0])},
            {"label":"Region to search for peaks", "type":"dropdownlist", "list": ['Entire image'] + series_labels, "value": 0},
            {"label":"Minimal distance between peaks (in pixels)", "type":"integer", "value": 1, "minimum": 1},
            {"label":"Size of the image border (in pixels)", "type":"integer", "value": 2, "minimum": 0},
            title = 'Select Local Maximum settings')
        if cancel: 
            return

        if f[1]['value'] == 0:
            labels = None
        else:
            labels = series_list[f[1]['value']-1]

        # Filter series
        filtered = skimage.peak_local_max_3d(
            series_list[f[0]['value']], 
            labels = labels,
            min_distance = f[2]['value'],
            exclude_border = f[3]['value'],
        )
        app.display(filtered)
        app.refresh()


class CoregisterToSkImage(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            seriesList = series.parent().children()
            seriesLabels = [s.instance().SeriesDescription for s in seriesList]
            input = wezel.widgets.UserInput(
                {"label":"Coregister to which fixed series?", "type":"dropdownlist", "list": seriesLabels, 'value':0},
                {"label":"Attachment (smaller = smoother)", "type":"float", 'value':0.1, 'minimum':0.0}, 
                title = "Please select fixed series")
            if input.cancel:
                return
            fixed = seriesList[input.values[0]["value"]]
            coregistered = skimage.coregister(series, fixed, attachment=input.values[1]["value"])
            app.display(coregistered)
        app.refresh()


class Watershed2D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Filter series
        series = app.selected('Series')
        for sery in series:

            # Get user input
            desc = sery.label()
            all_series = sery.parent().children()
            all_series_desc = [s.label() for s in all_series]
            siblings = sery.siblings()
            sibling_desc = [s.label() for s in siblings]
            cancel, f = app.dialog.input(
                {   "label": "Landscape for watershed: ", 
                    "type": "dropdownlist", 
                    "list": all_series_desc, 
                    "value": all_series.index(sery),
                },
                {   "label": "Initial labels: ", 
                    "type": "dropdownlist", 
                    "list": ['use local minima'] + sibling_desc, 
                    "value": 0,
                },
                {   "label": "Label pixels in: ", 
                    "type": "dropdownlist", 
                    "list": ['Entire image'] + sibling_desc, 
                    "value": 0,
                },
                {   'label': 'Compactness: ',
                    'type': 'float',
                    'value': 0.0, 
                },
                {   'label': 'Include watershed line?',
                    'type': 'dropdownlist',
                    'list': ['Yes', 'No'],
                    'value': 1,
                },
                title = 'Select settings for watershed segmentation of ' + desc)
            if cancel: 
                return

             # Calculate watershed
            result = skimage.watershed_2d(
                all_series[f[0]['value']], 
                markers = None if f[1]['value']==0 else siblings[f[1]['value']-1],
                mask = None if f[2]['value']==0 else siblings[f[2]['value']-1],
                compactness = f[3]['value'],
                watershed_line = f[4]['value'] == 0,
            )
            app.display(result)

        app.refresh()


class Watershed3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Filter series
        series = app.selected('Series')
        for sery in series:

            # Get user input
            desc = sery.label()
            all_series = sery.parent().children()
            all_series_desc = [s.label() for s in all_series]
            siblings = sery.siblings()
            sibling_desc = [s.label() for s in siblings]
            cancel, f = app.dialog.input(
                {   "label": "Landscape for watershed: ", 
                    "type": "dropdownlist", 
                    "list": all_series_desc, 
                    "value": all_series.index(sery),
                },
                {   "label": "Initial labels: ", 
                    "type": "dropdownlist", 
                    "list": ['use local minima'] + sibling_desc, 
                    "value": 0,
                },
                {   "label": "Label pixels in: ", 
                    "type": "dropdownlist", 
                    "list": ['Entire image'] + sibling_desc, 
                    "value": 0,
                },
                {   'label': 'Compactness: ',
                    'type': 'float',
                    'value': 0.0, 
                },
                {   'label': 'Include watershed line?',
                    'type': 'dropdownlist',
                    'list': ['Yes', 'No'],
                    'value': 1,
                },
                title = 'Select settings for watershed segmentation of ' + desc)
            if cancel: 
                return

             # Calculate watershed
            result = skimage.watershed_3d(
                all_series[f[0]['value']], 
                markers = None if f[1]['value']==0 else siblings[f[1]['value']-1],
                mask = None if f[2]['value']==0 else siblings[f[2]['value']-1],
                compactness = f[3]['value'],
                watershed_line = f[4]['value'] == 0,
            )
            app.display(result)

        app.refresh()


class CoregisterSeries(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        input = wezel.widgets.UserInput(
            {"label":"Attachment (smaller = smoother)", "type":"float", 'value':0.1, 'minimum':0.0}, 
            title = "Please select coregistration settings")
        if input.cancel:
            return
        for series in app.selected('Series'):
            coregistered = skimage.coregister_series(series, attachment=input.values[0]["value"])
            app.display(coregistered)
        app.refresh()


class MDRegConstant2D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        input = wezel.widgets.UserInput(
            {"label":"Attachment (smaller = smoother)", "type":"float", 'value':0.1, 'minimum':0.0}, 
            {"label":"Stop when improvement is less than (pixelsizes):", "type":"float", 'value':1.0, 'minimum':0},
            {"label":"Maximum number of iterations", "type":"integer", 'value':10, 'minimum':1}, 
            title = "Please select coregistration settings")
        if input.cancel:
            return
        for series in app.selected('Series'):
            coregistered = skimage.mdreg_constant_2d(series, 
                attachment = input.values[0]["value"],
                max_improvement = input.values[1]["value"],
                max_iter = input.values[2]["value"])
            app.display(coregistered)
        app.refresh()


class MDRegConstant3D(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        input = wezel.widgets.UserInput(
            {"label":"Attachment (smaller = smoother)", "type":"float", 'value':0.1, 'minimum':0.0}, 
            {"label":"Stop when improvement is less than (pixelsizes):", "type":"float", 'value':1.0, 'minimum':0},
            {"label":"Maximum number of iterations", "type":"integer", 'value':10, 'minimum':1}, 
            title = "Please select coregistration settings")
        if input.cancel:
            return
        for series in app.selected('Series'):
            coregistered = skimage.mdreg_constant_3d(series, 
                attachment = input.values[0]["value"],
                max_improvement = input.values[1]["value"],
                max_iter = input.values[2]["value"])
            app.display(coregistered)
        app.refresh()
