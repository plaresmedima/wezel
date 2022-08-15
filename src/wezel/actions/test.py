import wezel
import time

def testFunction(start, end, signals):
  signals.log.emit("Calculation Started")
  for n in range(start, end):
    time.sleep(1)
    signals.log.emit("Message " + str(n))  
  return "Result of the calculation"

def all(parent):
    parent.action(Test_UserInput, text='Test UserInput')
    parent.action(Test_LoggingToGUI, text='Test Logging to GUI')
    

class Test_LoggingToGUI(wezel.Action):
    def enable(self, app):
        return True

    def run(self, app):
        window = wezel.widgets.LoggingWidget(testFunction, start=1,end=10)
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
