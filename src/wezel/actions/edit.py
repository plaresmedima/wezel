import dbdicom as db
import wezel


def all(parent):

    parent.action(Delete, text='Delete', generation=3)
    parent.separator()
    parent.action(Copy, text='Series > Copy', generation=3)
    parent.action(NewSeries, text='Series > New')
    parent.action(MergeSeries, text='Series > Merge')
    parent.action(GroupSeries, text='Series > Group')
    parent.action(SeriesRename, text='Series > Rename')
    parent.action(SeriesExtract, text='Series > Extract subseries')
    parent.separator()
    parent.action(Copy, text='Studies > Copy', generation=2)
    parent.action(NewStudy, text='Study > New')
    parent.action(MergeStudies, text='Studies > Merge')
    parent.action(GroupStudies, text='Studies > Group')
    parent.separator()
    parent.action(Copy, text='Patients > Copy', generation=1)
    parent.action(NewPatient, text='Patient > New')
    parent.action(MergePatients, text='Patients > Merge')
    

class Copy(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(self.generation) != 0

    def run(self, app):

        app.status.message("Copying..")
        records = app.get_selected(self.generation)        
        for j, record in enumerate(records):
            app.status.progress(j, len(records), 'Copying..')
            record.copy()               
        app.refresh()


class Delete(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(self.generation) != 0

    def run(self, app):

        app.status.message("Deleting..")
        records = app.get_selected(self.generation)        
        for j, series in enumerate(records):
            app.status.progress(j, len(records), 'Deleting..')
            series.remove()               
        app.refresh()


class NewSeries(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected('Studies') != 0

    def run(self, app): 
        app.status.message('Creating new series..')
        studies = app.selected('Studies')
        for study in studies:
            study.new_series(SeriesDescription='New series')
        app.refresh()


class NewStudy(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected('Patients') != 0

    def run(self, app): 
        app.status.message('Creating new study..')
        patients = app.selected('Patients')
        for patient in patients:
            patient.new_study(StudyDescription='New study')
        app.refresh()


class NewPatient(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return True

    def run(self, app): 
        app.status.message('Creating new patient..')
        self.folder.new_patient(PatientName='New patient')
        app.refresh()


class MergeSeries(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected('Series') != 0

    def run(self, app): 

        app.status.message('Merging..')
        records = app.selected('Series')
        study = records[0].new_pibling(StudyDescription='Merger')
        series = study.new_series(SeriesDescription='Merged series')
        db.merge(records, series)
        app.refresh()





class MergeStudies(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected('Studies') != 0

    def run(self, app): 
        app.status.message('Merging..')
        studies = app.selected('Studies')
        patient = studies[0].new_pibling(PatientName='Merger')
        db.merge(studies, patient.new_study(StudyDescription='Merged studies'))
        app.refresh()

class MergePatients(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected('Patients') != 0

    def run(self, app): 
        app.status.message('Merging..')
        records = app.selected('Patients')
        patient = records[0].new_sibling(PatientName='Merged Patients')
        db.merge(records, patient)
        app.refresh()


class GroupSeries(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected('Series') != 0

    def run(self, app): 
        app.status.message('Grouping..')
        records = app.selected('Series')
        study = records[0].new_pibling(StudyDescription='Grouped')
        db.group(records, study)
        app.status.hide()
        app.refresh()

class GroupStudies(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected('Studies') != 0

    def run(self, app): 
        app.status.message('Grouping..')
        records = app.selected('Studies')
        patient = records[0].new_pibling(PatientName='Grouped')
        db.group(records, patient)
        app.status.hide()
        app.refresh()


class SeriesRename(wezel.Action):

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
            s.SeriesDescription = f[0]['value']
        app.refresh()

class SeriesExtract(wezel.Action):

    def enable(self, app):

        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app):

        # Get source data
        series = app.get_selected(3)[0]
        _, slices = series.get_pixel_array(['SliceLocation', 'AcquisitionTime'])
        nz, nt = slices.shape[0], slices.shape[1]
        x0, x1, t0, t1 = 0, nz, 0, nt

        # Get user input
        invalid = True
        while invalid:
            cancel, f = app.dialog.input(
                {"type":"integer", "label":"Slice location from index..", "value":x0, "minimum": 0, "maximum": nz},
                {"type":"integer", "label":"Slice location to index..", "value":x1, "minimum": 0, "maximum": nz},
                {"type":"integer", "label":"Acquisition time from index..", "value":t0, "minimum": 0, "maximum": nt},
                {"type":"integer", "label":"Acquisition time to index..", "value":t1, "minimum": 0, "maximum": nt},
                title='Select parameter ranges')
            if cancel: 
                return
            x0, x1, t0, t1 = f[0]['value'], f[1]['value'], f[2]['value'], f[3]['value']
            invalid = (x0 >= x1) or (t0 >= t1)
            if invalid:
                app.dialog.information("Invalid selection - first index must be lower than second")

        # Extract series and save
        study = series.parent().new_sibling(StudyDescription='Extracted Series')
        indices = ' [' + str(x0) + ':' + str(x1) 
        indices += ', ' + str(t0) + ':' + str(t1) + ']'
        new_series = study.new_child(SeriesDescription = series.SeriesDescription + indices)
        db.copy_to(slices[x0:x1,t0:t1,:], new_series)
        app.refresh()