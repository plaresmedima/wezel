import os
import wezel
import dbdicom as db

def all(parent):

    parent.addAction('Open', shortcut='Ctrl+O', on_clicked=open_database)
    parent.addAction('Read', on_clicked=read_database, is_clickable=is_database_open)
    parent.addAction('Save', shortcut='Ctrl+S', on_clicked=save_database, is_clickable=is_database_open)
    parent.addAction('Restore', shortcut='Ctrl+R', on_clicked=restore_database, is_clickable=is_database_open)
    parent.addAction('Close', shortcut='Ctrl+C', on_clicked=close_database, is_clickable=is_database_open)
    parent.separator()
    parent.addAction('Open subfolders', on_clicked=open_subfolders)
    parent.separator()
    parent.addAction('Export as DICOM', on_clicked=export_as_dicom, is_clickable=is_series_selected)
    parent.addAction('Export as CSV', on_clicked=export_as_csv, is_clickable=is_series_selected)
    parent.addAction('Export as PNG', on_clicked=export_as_png, is_clickable=is_series_selected)
    parent.addAction('Export as NIfTI', on_clicked=export_as_nifti, is_clickable=is_series_selected)
    parent.separator()
    parent.addAction('Import DICOM', on_clicked=import_dicom, is_clickable=is_database_open)
    parent.addAction('Import NIfTI', on_clicked=import_nifti, is_clickable=is_database_open)


def is_database_open(app): 
    if app.database() is None:
        return False
    return app.database().manager.is_open()

def is_series_selected(app):
    return app.nr_selected('Series') != 0


def open_database(app):
    """
    Open a DICOM folder and update display.
    """
    app.status.message("Opening DICOM folder..")
    path = app.dialog.directory("Select a DICOM folder")
    if path == '':
        app.status.message('') 
        return
    app.status.cursorToHourglass()
    app.close()
    app.open(path)
    app.status.hide()
    app.status.cursorToNormal()


def read_database(app):
    """
    Read the open DICOM folder.
    """
    app.status.cursorToHourglass()
    app.central.closeAllSubWindows()
    app.database().scan()
    app.status.cursorToNormal() 
    app.refresh()


def save_database(app):
    """
    Saves the open DICOM folder.
    """
    app.database().save()


def restore_database(app):
    """
    Restore the open DICOM folder.
    """
    app.database().restore()
    app.refresh()


def close_database(app):
    closed = app.database().close()
    if closed: 
        app.close()


def open_subfolders(app):
    """
    Open a DICOM folder and update display.
    """
    app.status.message("Opening DICOM folder..")
    path = app.dialog.directory("Select the top folder..")
    if path == '':
        app.status.message('') 
        return
    subfolders = next(os.walk(path))[1]
    subfolders = [os.path.join(path, f) for f in subfolders]
    app.close()
    app.status.cursorToHourglass()
    for i, path in enumerate(subfolders):
        msg = 'Reading folder ' + str(i+1) + ' of ' + str(len(subfolders))
        #app.open(path)
        app.status.message(msg)
        folder = db.database(path=path, 
            status = app.status, 
            dialog = app.dialog)
        folder.save()
    app.status.cursorToNormal()
    app.status.hide()
    app.display(folder)


def export_as_dicom(app):
    path = app.dialog.directory("Where do you want to export the data?")
    patients, studies, series = app.top_level_selected()
    selected = patients + studies + series
    if selected == []:
        app.dialog.information("Please select at least one series")
        return
    app.status.message('Exporting to ' + path)
    for i, record in enumerate(selected):
        app.status.progress(i, len(selected), 'Exporting to ' + path)
        record.export_as_dicom(path)
    app.status.hide()
    app.status.message('Finished exporting..')


def import_dicom(app):
    files = app.dialog.files("Select DICOM files to import")
    app.database().import_dicom(files)
    app.status.hide()
    app.refresh()


def export_as_png(app):
    path = app.dialog.directory("Where do you want to export the data?")
    patients, studies, series = app.top_level_selected()
    selected = patients + studies + series
    if selected == []:
        app.dialog.information("Please select at least one series")
        return
    app.status.message('Exporting to ' + path)
    for i, record in enumerate(selected):
        app.status.progress(i, len(selected), 'Exporting to ' + path)
        record.export_as_png(path)
    app.status.hide()
    app.status.message('Finished exporting..')


def export_as_csv(app):
    path = app.dialog.directory("Where do you want to export the data?")
    patients, studies, series = app.top_level_selected()
    selected = patients + studies + series
    if selected == []:
        app.dialog.information("Please select at least one series")
        return
    app.status.message('Exporting to ' + path)
    for i, record in enumerate(selected):
        app.status.progress(i, len(selected), 'Exporting to ' + path)
        record.export_as_csv(path)
    app.status.hide()
    app.status.message('Finished exporting..')


def export_as_nifti(app):
    path = app.dialog.directory("Where do you want to export the data?")
    patients, studies, series = app.top_level_selected()
    selected = patients + studies + series
    if selected == []:
        app.dialog.information("Please select at least one series")
        return
    app.status.message('Exporting to ' + path)
    for i, record in enumerate(selected):
        app.status.progress(i, len(selected), 'Exporting to ' + path)
        record.export_as_nifti(path)
    app.status.hide()
    app.status.message('Finished exporting..')


def import_nifti(app):
    files = app.dialog.files("Select NIfTI files to import")
    app.database().import_nifti(files)
    app.status.hide()
    app.refresh()

