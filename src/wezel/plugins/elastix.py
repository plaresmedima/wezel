from dbdicom.wrappers import elastix
from wezel.gui import Action


def if_a_series_is_selected(app):
    return app.nr_selected('Series') != 0

def calculate_coregistration(app):
    for series in app.selected('Series'):
        seriesList = series.parent().children()
        seriesLabels = [s.instance().SeriesDescription for s in seriesList]
        transform = ['Rigid', 'Affine', 'Freeform']
        metric = ["AdvancedMeanSquares", "NormalizedMutualInformation", "AdvancedMattesMutualInformation"]
        cancel, f = app.dialog.input(
            {"label":"Coregister to which fixed series?", "type":"dropdownlist", "list": seriesLabels, 'value':0},
            {"label":"Transformation: ", "type":"dropdownlist", "list": transform, 'value':1},
            {"label":"Metric: ", "type":"dropdownlist", "list": metric, 'value':1},
            {"label":"Final grid spacing (mm)", "type":"float", 'value':25.0, 'minimum':1.0},
            title = "Please select coregistration settings")
        if cancel:
            return
        fixed = seriesList[f[0]["value"]]
        coregistered = elastix.coregister(series, fixed,
            transformation = transform[f[1]["value"]],
            metric = metric[f[2]["value"]],
            final_grid_spacing = f[3]["value"],
        )
        app.display(coregistered)
    app.refresh()


action_coregistration = Action('Coregister', on_clicked=calculate_coregistration, is_clickable=if_a_series_is_selected)
