import wezel
import time

def test_Function(start, end, signals):
  signals.log.emit("Calculation Started")
  for n in range(start, end):
    time.sleep(1)
    signals.log.emit("Message " + str(n))  
  return "Result of the calculation"


def test_Copy(series_list, signals):
    signals.log.emit("Copying {} series".format(len(series_list)))      
    for series in series_list:
        signals.log.emit('Copying {}'.format(series.label()))
        #series.copy()  
    return "Copying complete"
        

def all(parent):
    parent.action(Test_UserInput, text='Test UserInput')
    parent.action(Test_LoggingToGUI, text='Test Logging to GUI')
    parent.action(Test_Copy, text='Test Copy & Logging to GUI')
    

class Test_LoggingToGUI(wezel.Action):
    def enable(self, app):
        return True

    def run(self, app):
        window = wezel.widgets.LoggingWidget(test_Function, start=1,end=10)
        app.addAsSubWindow(window, "Test Logging to GUI")


class Test_UserInput(wezel.Action):
    def enable(self, app):
            return True

    def run(self, app): 
        filters = ["Gaussian", "Uniform", "Median", "Maximum", "Wiener"]
        flavours = ["Chocolate", "Vanilla", "Strawberry"]

        cancel, input = app.dialog.input(
            {"label":"Which filter?", "type":"listview", "list": filters},
            {"label":"Which filter?", "type":"dropdownlist", "list": filters, "value": 2},
            {"label":"Which flavour?", "type":"dropdownlist", "list": flavours},
            {"label":"Filter size in pixels", "type":"float"},
            {"label":"Type a string", "type":"string","value":"hello world!"},
            {"label":"Which flavour?", "type":"listview", "list":flavours},
            {"label":"An integer between 0 and 1000", "type":"integer", "value":20, "minimum": 0, "maximum": 1000}, 
            {"label":"An integer larger than -100", "type":"float", "value":20, "minimum": -100}, 
            {"label":"An integer less than 1000", "type":"integer", "value":30, "maximum": 1000},
            {"label":"Any integer", "type":"integer", "value":40},
            {"label":"Any integer", "type":"integer"},
            {"label":"Type a string", "type":"string","value":"hello world!"},
            title = "Can we have some input?")
        if not cancel: 
            for field in input:
                print(field["label"], ': ', field["value"])


class Test_Copy(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app):
        series_list = app.get_selected(3)
        window = wezel.widgets.LoggingWidget(test_Copy, series_list=series_list)
        app.addAsSubWindow(window, "Test Logging to GUI while copying DICOM series")
       