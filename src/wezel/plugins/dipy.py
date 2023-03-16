from dbdicom.wrappers import dipy
from wezel.gui import Action, Menu


def if_a_series_is_selected(app):
    return app.nr_selected('Series') != 0


def coregister(app):
    for series in app.selected('Series'):
        seriesList = series.parent().children()
        seriesLabels = [s.instance().SeriesDescription for s in seriesList]
        transform = ['Symmetric Diffeomorphic']
        metric = ["Cross-Correlation", 'Expectation-Maximization', 'Sum of Squared Differences']
        cancel, f = app.dialog.input(
            {"label":"Coregister to which fixed series?", "type":"dropdownlist", "list": seriesLabels, 'value':0},
            {"label":"Transformation: ", "type":"dropdownlist", "list": transform, 'value':0},
            {"label":"Metric: ", "type":"dropdownlist", "list": metric, 'value':0},
            title = "Please select coregistration settings")
        if cancel:
            return
        fixed = seriesList[f[0]["value"]]
        coregistered = dipy.coregister(series, fixed,
            transformation = transform[f[1]["value"]],
            metric = metric[f[2]["value"]],
        )
        app.display(coregistered)
    app.refresh()


def median_otsu(app):

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
        mask_series, mask = dipy.median_otsu(
            sery, 
            median_radius=f[0]['value'], 
            numpass=f[1]['value'],
        )
        mask_series.remove()
        app.display(mask)
    app.refresh()


action_coregister = Action('Coregister to..', on_clicked=coregister, is_clickable=if_a_series_is_selected)
action_median_otsu = Action('Median Otsu segmentation', on_clicked=coregister, is_clickable=if_a_series_is_selected)


menu_all = Menu('dipy')
menu_all.add(action_coregister)
menu_all.add(action_median_otsu)



