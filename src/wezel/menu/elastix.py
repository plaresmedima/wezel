"""
A collection of wezel menu buttons with wrappers for elastix coregistration functions.

Requires optional dependencies:

SimpleITK
itk-elastix
"""

import wezel
from dbdicom.wrappers import elastix


def all(parent): 
    parent.action(CoregisterToElastix, text='Coregister to')


class CoregisterToElastix(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            seriesList = series.parent().children()
            seriesLabels = [s.instance().SeriesDescription for s in seriesList]
            transform = ['Rigid', 'Affine', 'Freeform']
            metric = ["AdvancedMeanSquares", "NormalizedMutualInformation", "AdvancedMattesMutualInformation"]
            input = wezel.widgets.UserInput(
                {"label":"Coregister to which fixed series?", "type":"dropdownlist", "list": seriesLabels, 'value':0},
                {"label":"Transformation: ", "type":"dropdownlist", "list": transform, 'value':1},
                {"label":"Metric: ", "type":"dropdownlist", "list": metric, 'value':1},
                {"label":"Final grid spacing (mm)", "type":"float", 'value':25.0, 'minimum':1.0},
                title = "Please select coregistration settings")
            if input.cancel:
                return
            fixed = seriesList[input.values[0]["value"]]
            coregistered = elastix.coregister(series, fixed,
                transformation = transform[input.values[1]["value"]],
                metric = metric[input.values[2]["value"]],
                final_grid_spacing = input.values[3]["value"],
            )
            app.display(coregistered)
        app.refresh()