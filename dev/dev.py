# To develop the package
# create virtual environment
# py -3 -m venv .venv
# activate virtual environment
# .venv/Scripts/activate
# install editable version of wezel into virtual environment
# pip install -e C:\Users\steve\Dropbox\Software\QIB-Sheffield\wezel
# Any changes in src will now automatically be reflected.

import wezel

app = wezel.app(wezel.apps.dicom.Windows)
app.show()