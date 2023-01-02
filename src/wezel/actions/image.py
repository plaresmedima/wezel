import wezel
import scipy

def all(parent): 
    parent.action(Resize, text="Resize")




class Resize(wezel.Action): # copy at series level

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {"type":"float", "label":"Resize with factor..", "value":2.0, "minimum": 0},
            title='Select parameter ranges')
        if cancel: 
            return
        factor = f[0]['value']

        # Resize series
        series = app.selected('Series')
        for sery in series:
            resized = zoom(sery, factor)
            app.display(resized)
        app.refresh()






# Functions for a new package dbimage -- a dbdicom wrapper for scipy.ndimage


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.zoom.html#scipy.ndimage.zoom
def zoom(input, zoom, **kwargs):
    """
    wrapper for scipy.ndimage.zoom.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    zoomed : dbdicom series
    """
    suffix = ' [Resize x ' + str(zoom) + ' ]'
    desc = input.instance().SeriesDescription
    zoomed = input.copy(SeriesDescription = desc + suffix)
    images = zoomed.instances()
    for i, image in enumerate(images):
        input.status.progress(i, len(images), 'Resizing ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.zoom(array, zoom, **kwargs)
        image.set_array(array)
        pixel_spacing = image.PixelSpacing
        image.PixelSpacing = [p/zoom for p in pixel_spacing]
        image.clear()
    return zoomed


def affine_transform(input, matrix, **kwargs):

    suffix = ' [affine transform]'
    array, headers = input.array('SliceLocation', pixels_first=True)
    mapped = scipy.ndimage.affine_transform(array, matrix, **kwargs)
    desc = input.instance().SeriesDescription 
    mapped_series = input.new_sibling(SeriesDescription = desc+suffix)
    # Get header from input but insert correct geometry information
    # Apply the inverse transformation to the coordinate vectors
    mapped_series.set_array(mapped, headers, pixels_first=True)
    return mapped_series
