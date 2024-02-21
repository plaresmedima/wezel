from dbdicom.extensions import vreg
from wezel.gui import Action, Menu


def _if_a_series_is_selected(app):
    return app.nr_selected('Series') != 0

def _if_a_database_is_open(app):
    return app.database() is not None


def _translation(app):
    series = app.database().series()
    sel = app.selected('Series')
    metric = ['sum of squares', 'mutual information']
    cancel, f = app.dialog.input(
        {"label":"Moving series", "type":"select record", "options": series, 'default':sel},
        {"label":"Static series", "type":"select record", "options": series, 'default':sel},
        {"label":"Target region", "type":"select optional record", "options": series},
        {"label":"Apply transformation to:", "type":"select records", "options": series, 'default':[]},
        {"label":"Tolerance (smaller = slower but more accurate)", "type":"float", 'value':0.1, 'minimum':0.001}, 
        {"label":"Cost function", "type":"dropdownlist", 'list':metric, 'value':1}, 
        title = "Please select coregistration parameters (translation)")
    if cancel:
        return
    params = vreg.find_translation(f[0], f[1], tolerance=f[4]["value"], metric=metric[f[5]["value"]], region=f[2])

    # Save results as new dicom series
    f[0].message('Applying translations..')
    to_move = f[3] if f[0] in f[3] else [f[0]] + f[3]
    for series in to_move:
        try:
            series_moved = vreg.apply_translation(series, params, target=f[1])
            app.display(series_moved)
        except ValueError:
            msg = 'Series ' + series.instance().SeriesDescription + ' cannot be moved. \n'
            msg += 'If it consists of multiple slice groups, split the series first.'
            app.dialog.information(msg)
    app.refresh()


def _rigid(app):
    series = app.database().series()
    sel = app.selected('Series')
    metric = ['sum of squares', 'mutual information']
    cancel, f = app.dialog.input(
        {"label":"Moving series", "type":"select record", "options": series, 'default':sel},
        {"label":"Static series", "type":"select record", "options": series, 'default':sel},
        {"label":"Target region", "type":"select optional record", "options": series},
        {"label":"Apply transformation to:", "type":"select records", "options": series, 'default':[]},
        {"label":"Apply passive transformation?", "type":"dropdownlist", 'list':['Yes', 'No'], 'value':1},
        {"label":"Tolerance (smaller = slower but more accurate)", "type":"float", 'value':0.1, 'minimum':0.001}, 
        {"label":"Cost function", "type":"dropdownlist", 'list':metric, 'value':1}, 
        title = "Please select coregistration parameters (rigid transformation)")
    if cancel:
        return
    params = vreg.find_rigid_transformation(f[0], f[1], 
            tolerance=f[5]["value"], 
            metric=metric[f[6]["value"]], 
            region=f[2])

    # Save results as new dicom series
    f[0].message('Applying rigid transformation..')
    to_move = f[3] if f[0] in f[3] else [f[0]] + f[3]
    for series in to_move:
        try:
            if f[4]['value'] == 1:
                series_moved = vreg.apply_rigid_transformation(
                    series, params, target=f[1])
            else:
                series_moved = vreg.apply_passive_rigid_transformation(
                    series, params)
            app.display(series_moved)
        except ValueError:
            msg = 'Series ' + series.instance().SeriesDescription + ' cannot be moved. \n'
            msg += 'If it consists of multiple slice groups, split the series first.'
            app.dialog.information(msg)
    app.refresh()


def _sbs_translation(app):
    series = app.database().series()
    sel = app.selected('Series')
    metric = ['sum of squares', 'mutual information']
    cancel, f = app.dialog.input(
        {"label":"Moving series", "type":"select record", "options": series, 'default':sel},
        {"label":"Static series", "type":"select record", "options": series, 'default':sel},
        {"label":"Target region", "type":"select optional record", "options": series},
        {"label":"Apply transformation to:", "type":"select records", "options": series, 'default':[]},
        {"label":"Tolerance (smaller = slower but more accurate)", "type":"float", 'value':0.1, 'minimum':0.001}, 
        {"label":"Cost function", "type":"dropdownlist", 'list':metric, 'value':1}, 
        title = "Please select coregistration parameters (slice-by-slice translation)")
    if cancel:
        return
    params = vreg.find_sbs_translation(f[0], f[1], tolerance=f[4]["value"], metric=metric[f[5]["value"]], region=f[2])

    # Save results as new dicom series
    f[0].message('Applying slice-by-slice translation..')
    to_move = f[3] if f[0] in f[3] else [f[0]] + f[3]
    for series in to_move:
        try:
            series_moved = vreg.apply_sbs_translation(series, params, target=f[1])
            app.display(series_moved)
        except ValueError:
            msg = 'Series ' + series.instance().SeriesDescription + ' cannot be moved. \n'
            msg += 'If it consists of multiple slice groups, split the series first.'
            app.dialog.information(msg)
    app.refresh()


def _sbs_rigid(app):
    series = app.database().series()
    sel = app.selected('Series')
    metric = ['sum of squares', 'mutual information']
    cancel, f = app.dialog.input(
        {"label":"Moving series", "type":"select record", "options": series, 'default':sel},
        {"label":"Static series", "type":"select record", "options": series, 'default':sel},
        {"label":"Target region", "type":"select optional record", "options": series},
        {"label":"Apply transformation to:", "type":"select records", "options": series, 'default':[]},
        {"label":"Apply passive transformation?", "type":"dropdownlist", 'list':['Yes', 'No'], 'value':1},
        {"label":"Tolerance (smaller = slower but more accurate)", "type":"float", 'value':0.1, 'minimum':0.001}, 
        {"label":"Cost function", "type":"dropdownlist", 'list':metric, 'value':1}, 
        title = "Please select coregistration parameters (slice-by-slice rigid transformation)")
    if cancel:
        return
    
    params = vreg.find_sbs_rigid_transformation(f[0], f[1], 
            tolerance=f[5]["value"], 
            metric=metric[f[6]["value"]], 
            resolutions=[1], 
            region=f[2])

    # Save results as new dicom series
    f[0].message('Applying slice-by-slice translation..')
    to_move = f[3] if f[0] in f[3] else [f[0]] + f[3]
    for series in to_move:
        try:
            if f[4]['value'] == 1:
                series_moved = vreg.apply_sbs_rigid_transformation(series, params, target=f[1])
            else:
                series_moved = vreg.apply_sbs_passive_rigid_transformation(series, params)
            app.display(series_moved)
        except ValueError:
            msg = 'Series ' + series.instance().SeriesDescription + ' cannot be moved. \n'
            msg += 'If it consists of multiple slice groups, split the series first.'
            app.dialog.information(msg)
    app.refresh()





def _rigid_around_com_sos(app):
    series = app.database().series()
    sel = app.selected('Series')
    cancel, f = app.dialog.input(
        {"label":"Moving series", "type":"select record", "options": series, 'default':sel},
        {"label":"Static series", "type":"select record", "options": series, 'default':sel},
        {"label":"Tolerance (smaller = slower but more accurate)", "type":"float", 'value':0.1, 'minimum':0.001}, 
        title = "Please select coregistration parameters")
    if cancel:
        return
    coregistered = vreg.rigid_around_com_sos(f[0], f[1], tolerance=f[2]["value"])
    app.display(coregistered)
    app.refresh()


def _sbs_rigid_around_com_sos(app):
    series = app.database().series()
    sel = app.selected('Series')
    cancel, f = app.dialog.input(
        {"label":"Moving series", "type":"select record", "options": series, 'default':sel},
        {"label":"Static series", "type":"select record", "options": series, 'default':sel},
        {"label":"Tolerance (smaller = slower but more accurate)", "type":"float", 'value':0.1, 'minimum':0.001}, 
        title = "Please select coregistration parameters")
    if cancel:
        return
    coregistered = vreg.sbs_rigid_around_com_sos(f[0], f[1], tolerance=f[2]["value"])
    app.display(coregistered)
    app.refresh()


action_translation = Action('Translation', on_clicked=_translation, is_clickable=_if_a_database_is_open)
action_rigid = Action('Rigid transformation', on_clicked=_rigid, is_clickable=_if_a_database_is_open)
action_rigid_around_com_sos = Action('Rigid around center of mass (cost = sum of squares)', on_clicked=_rigid_around_com_sos, is_clickable=_if_a_database_is_open)

action_sbs_translation = Action('Slice-by-slice translation', on_clicked=_sbs_translation, is_clickable=_if_a_database_is_open)
action_sbs_rigid = Action('Slice-by-slice rigid transformation', on_clicked=_sbs_rigid, is_clickable=_if_a_database_is_open)
action_sbs_rigid_around_com_sos = Action('Slice-by-slice rigid around center of mass (cost = sum of squares)', on_clicked=_sbs_rigid_around_com_sos, is_clickable=_if_a_database_is_open)


menu_coreg = Menu('Coregister (vreg)')
menu_coreg.add(action_translation)
menu_coreg.add(action_sbs_translation)
menu_coreg.add_separator()
menu_coreg.add(action_rigid)
menu_coreg.add(action_sbs_rigid)
menu_coreg.add_separator()
menu_coreg.add(action_rigid_around_com_sos)
menu_coreg.add(action_sbs_rigid_around_com_sos)

menu_coreg_wip = Menu('Coregister (vreg)')
menu_coreg_wip.add(action_rigid_around_com_sos)
menu_coreg_wip.add(action_sbs_rigid_around_com_sos)