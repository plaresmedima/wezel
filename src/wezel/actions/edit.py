import dbdicom as db
import wezel


def all(parent):

    parent.action(Copy, text='Copy series')
    parent.action(Delete, text='Delete series')
    parent.action(Merge, text='Merge series')
    parent.action(Group, text='Group series')
    parent.separator()
    parent.action(Rename, text='Rename series')
    parent.action(Extract, text='Extract subseries')
    

class Copy(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app):

        app.status.message("Copying..")
        series_list = app.get_selected(3)        
        for j, series in enumerate(series_list):
            app.status.progress(j, len(series_list), 'Copying..')
            series.copy()               
        app.status.hide()
        app.refresh()


class Delete(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app):

        app.status.message("Deleting..")
        series_list = app.get_selected(3)        
        for j, series in enumerate(series_list):
            app.status.progress(j, len(series_list), 'Deleting..')
            series.remove()               
        app.status.hide()
        app.refresh()


class Merge(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app): 

        app.status.message('Merging..')
        series_list = app.get_selected(3)
        db.merge(series_list, status=app.status)
        app.status.hide()
        app.refresh()


class Group(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app): 

        app.status.message('Grouping..')
        series_list = app.get_selected(3)
        study = series_list[0].new_pibling(SeriesDescription='Grouped series')
        nr = str(len(series_list))
        for j, series in enumerate(series_list):
            msg = 'Grouping series ' + series.label() + ' (' + str(j+1) + ' of ' + nr + ')'
            series.copy_to(study, message=msg)
        app.status.hide()
        app.refresh()


class Rename(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app): 
        series_list = app.get_selected(3)
        for s in series_list:
            cancel, f = app.dialog.input(
                {"type":"string", "label":"New series name:", "value": s.SeriesDescription},
                title = 'Enter new series name')
            if cancel:
                return
            db.set_value(s.instances(), SeriesDescription=f[0]['value'])
        app.status.hide()
        app.refresh()

class Extract(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app):

        series = app.get_selected(3)[0]
        ds = series.dataset(['SliceLocation', 'AcquisitionTime'], status=True)
        nz, nt = ds.shape[0], ds.shape[1]
        x0, x1, t0, t1 = 0, nz, 0, nt
        invalid = True
        while invalid:
            cancel, f = app.dialog.input(
                {"type":"integer", "label":"Slice location from index..", "value":x0, "minimum": 0, "maximum": nz},
                {"type":"integer", "label":"Slice location to index..", "value":x1, "minimum": 0, "maximum": nz},
                {"type":"integer", "label":"Acquisition time from index..", "value":t0, "minimum": 0, "maximum": nt},
                {"type":"integer", "label":"Acquisition time to index..", "value":t1, "minimum": 0, "maximum": nt},
                title='Select parameter ranges')
            if cancel: return
            x0, x1, t0, t1 = f[0]['value'], f[1]['value'], f[2]['value'], f[3]['value']
            invalid = (x0 >= x1) or (t0 >= t1)
            if invalid:
                app.dialog.information("Invalid selection - first index must be lower than second")
        name = ' [' + str(x0) + ':' + str(x1) 
        name += ', ' + str(t0) + ':' + str(t1) + ']'
        new = series.new_cousin(
            StudyDescription = 'extracted',
            SeriesDescription = series.SeriesDescription + name, 
            )
        db.copy(ds[x0:x1,t0:t1,0], new, status=app.status)
        app.refresh()