import wezel


if __name__ == "__main__":

    app = wezel.app()
    app.set_app(wezel.apps.dicom.Windows)
    app.show()