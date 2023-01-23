import wezel
from dbdicom.wrappers import skimage


class CannyFilter(wezel.Action): 

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



class CoregisterToSkImage(wezel.Action): 

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


class Watershed2D(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {   "label": "Number of labels: ", 
                "type": "integer", 
                "value": 250,
                'minimum': 0,
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
            title = 'Select settings for watershed segmentation')
        if cancel: 
            return

        # Calculate watershed
        series = app.selected('Series')
        for sery in series:
            filtered = skimage.watershed_2d(
                sery, 
                markers = f[0]['value'],
                compactness = f[1]['value'],
                watershed_line = f[2]['value'] == 0,
            )
            app.display(filtered)

        app.refresh()


class Watershed2DLabels(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Filter series
        series = app.selected('Series')
        for sery in series:

            # Get user input
            desc = sery.SeriesDescription
            siblings = sery.siblings()
            sibling_desc = [s.SeriesDescription for s in siblings]
            cancel, f = app.dialog.input(
                {   "label": "Labels: ", 
                    "type": "dropdownlist", 
                    "list": ['use local minima'] + sibling_desc, 
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
            if f[0]['value'] == 0:
                markers = None
            else:
                markers = siblings[f[0]['value']-1]

             # Calculate watershed
            filtered = skimage.watershed_2d_labels(
                sery, 
                markers = markers,
                compactness = f[1]['value'],
                watershed_line = f[2]['value'] == 0,
            )
            app.display(filtered)

        app.refresh()



class Watershed3D(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Calculate watershed
        series = app.selected('Series')
        for sery in series:

            desc = sery.SeriesDescription
            siblings = sery.siblings()
            sibling_desc = [s.SeriesDescription for s in siblings]

            # Get user input
            cancel, f = app.dialog.input(
                {   "label": "Number of labels: ", 
                    "type": "integer", 
                    "value": 250,
                    'minimum': 0,
                },
                {   "label": "Mask: ", 
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
            if f[1]['value'] == 0:
                mask = None
            else:
                mask = siblings[f[1]['value']-1]

            filtered = skimage.watershed_3d(
                sery, 
                markers = f[0]['value'],
                mask = mask,
                compactness = f[2]['value'],
                watershed_line = f[3]['value'] == 0,
            )
            app.display(filtered)

        app.refresh()


class CoregisterSeries(wezel.Action): 

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


class MDRegConstant2D(wezel.Action): 

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


class MDRegConstant3D(wezel.Action): 

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
