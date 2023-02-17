import wezel
from dbdicom.wrappers import sklearn


class KMeans(wezel.gui.Action): 

    def run(self, app):
        all_series = app.database().series()
        features = app.selected('Series')
        series_labels = [s.label() for s in all_series]
        if features == []:
            features_index = []
            selected = 0
        else:
            features_index = [all_series.index(series) for series in features] 
            selected = features_index[0]
            features_index = features_index[1:]
        cancel, f = app.dialog.input(
            {"label":"Reference feature", "type":"dropdownlist", "list": series_labels, 'value':selected},
            {"label":"Additional features (optional)", "type":"listview", "list": series_labels, 'value':features_index},
            {"label":"Mask", "type":"dropdownlist", "list": ['None'] + series_labels, 'value':0},
            {"label":"Number of clusters", "type":"integer", 'value':2, 'minimum':2}, 
            {"label":"Save clusters in multiple series?", "type":"dropdownlist", "list": ['No', 'Yes'], 'value':1},
            title = "Please select input for K-Means clustering")
        if cancel:
            return
        features = [all_series[f[0]['value']]]
        features += [all_series[i] for i in f[1]['value']]
        if f[2]['value'] == 0:
            mask = None
        else:
            mask = all_series[f[2]['value']-1]
        clusters = sklearn.kmeans(features, mask, n_clusters=f[3]['value'], multiple_series=f[4]['value']==1)
        app.display(clusters)
        app.refresh()



class SequentialKMeans(wezel.gui.Action): 

    def run(self, app):
        all_series = app.database().series()
        features = app.selected('Series')
        series_labels = [s.label() for s in all_series]
        if features == []:
            features_index = []
            selected = 0
        else:
            features_index = [all_series.index(series) for series in features] 
            selected = features_index[0]
            features_index = features_index[1:]
        cancel, f = app.dialog.input(
            {"label":"Reference feature", "type":"dropdownlist", "list": series_labels, 'value':selected},
            {"label":"Additional features (optional)", "type":"listview", "list": series_labels, 'value':features_index},
            {"label":"Mask", "type":"dropdownlist", "list": ['None'] + series_labels, 'value':0},
            {"label":"Number of clusters (each iteration)", "type":"integer", 'value':2, 'minimum':2}, 
            {"label":"Save clusters in multiple series?", "type":"dropdownlist", "list": ['No', 'Yes'], 'value':1},
            title = "Please select input for sequential K-Means clustering")
        if cancel:
            return
        features = [all_series[f[0]['value']]]
        features += [all_series[i] for i in f[1]['value']]
        if f[2]['value'] == 0:
            mask = None
        else:
            mask = all_series[f[2]['value']-1]
        clusters = sklearn.sequential_kmeans(features, mask, n_clusters=f[3]['value'], multiple_series=f[4]['value']==1)
        app.display(clusters)
        app.refresh()