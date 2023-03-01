"""
A collection of wezel menu buttons with wrappers for elastix coregistration functions.

Requires optional dependencies:

dipy
"""

import wezel
from dbdicom.wrappers import dipy


def all(parent):   

    parent.action(CoregisterToDiPy, text='Coregister to (dipy)')
    parent.action(MedianOtsu, text="Median Otsu segmentation")


class CoregisterToDiPy(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            seriesList = series.parent().children()
            seriesLabels = [s.instance().SeriesDescription for s in seriesList]
            transform = ['Symmetric Diffeomorphic']
            metric = ["Cross-Correlation", 'Expectation-Maximization', 'Sum of Squared Differences']
            input = wezel.widgets.UserInput(
                {"label":"Coregister to which fixed series?", "type":"dropdownlist", "list": seriesLabels, 'value':0},
                {"label":"Transformation: ", "type":"dropdownlist", "list": transform, 'value':0},
                {"label":"Metric: ", "type":"dropdownlist", "list": metric, 'value':0},
                title = "Please select coregistration settings")
            if input.cancel:
                return
            fixed = seriesList[input.values[0]["value"]]
            coregistered = dipy.coregister(series, fixed,
                transformation = transform[input.values[1]["value"]],
                metric = metric[input.values[2]["value"]],
            )
            app.display(coregistered)
        app.refresh()



class MedianOtsu(wezel.gui.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"Median Radius", "type":"integer", "value": 2, 'minimum':1},
            {"label":"Numpass", "type":"integer", "value": 1, 'minimum':1},
            title = 'Select Thresholding settings')
        if cancel: 
            return

        # Filter series
        series = app.selected('Series')
        for sery in series:
            _, mask = dipy.median_otsu(
                sery, 
                median_radius=f[0]['value'], 
                numpass=f[1]['value'],
            )
            #app.display(masked_series)
            app.display(mask)
        app.refresh()



