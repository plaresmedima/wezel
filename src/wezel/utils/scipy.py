import numpy as np
import scipy
import dbdicom
import nibabel as nib # unnecessary - remove


# SEGMENTATION


def label(input, **kwargs):
    """
    Labels structures in an image
    
    Wrapper for scipy.ndimage.label function. 

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [labels]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc+suffix)
    #images = filtered.instances() # setting sort=False should be faster - TEST!!!!!!!
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Labelling ' + desc)
        image.read()
        array = image.array() 
        array, _ = scipy.ndimage.label(array, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


def binary_fill_holes(input, **kwargs):
    """
    Fill holes in an existing segmentation.
    
    Wrapper for scipy.ndimage.binary_fill_holes function. 

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fill holes]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc+suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filling holes ' + desc)
        image.read()
        array = image.array() 
        array = scipy.ndimage.binary_fill_holes(array, **kwargs)
        image.set_array(array)
        #array = array.astype(np.ubyte)
        #_reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered



# FILTERS




# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.fourier_uniform.html#scipy.ndimage.fourier_ellipsoid
def fourier_ellipsoid(input, size, **kwargs):
    """
    wrapper for scipy.ndimage.fourier_ellipsoid

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fourier Ellipsoid x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = np.fft.fft2(array)
        array = scipy.ndimage.fourier_ellipsoid(array, size, **kwargs)
        array = np.fft.ifft2(array).real
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.fourier_uniform.html#scipy.ndimage.fourier_uniform
def fourier_uniform(input, size, **kwargs):
    """
    wrapper for scipy.ndimage.fourier_uniform

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fourier Uniform x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = np.fft.fft2(array)
        array = scipy.ndimage.fourier_uniform(array, size, **kwargs)
        array = np.fft.ifft2(array).real
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.fourier_shift.html#scipy.ndimage.fourier_shift
def fourier_gaussian(input, sigma, **kwargs):
    """
    wrapper for scipy.ndimage.fourier_gaussian.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fourier Gaussian x ' + str(sigma) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = np.fft.fft2(array)
        array = scipy.ndimage.fourier_gaussian(array, sigma, **kwargs)
        array = np.fft.ifft2(array).real
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_gradient_magnitude.html#scipy.ndimage.gaussian_gradient_magnitude
def gaussian_gradient_magnitude(input, sigma, **kwargs):
    """
    wrapper for scipy.ndimage.gaussian_gradient_magnitude.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Gaussian Gradient Magnitude x ' + str(sigma) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.gaussian_gradient_magnitude(array, sigma, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_laplace.html#scipy.ndimage.gaussian_laplace
def gaussian_laplace(input, sigma, **kwargs):
    """
    wrapper for scipy.ndimage.gaussian_laplace.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Gaussian Laplace x ' + str(sigma) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.gaussian_laplace(array, sigma, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.laplace.html#scipy.ndimage.laplace
def laplace(input, **kwargs):
    """
    wrapper for scipy.ndimage.sobel.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Laplace Filter]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.laplace(array, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.sobel.html#scipy.ndimage.sobel
def sobel_filter(input, axis=-1, **kwargs):
    """
    wrapper for scipy.ndimage.sobel.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Sobel Filter along axis ' + str(axis) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.sobel(array, axis=axis, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.prewitt.html#scipy.ndimage.prewitt
def prewitt_filter(input, axis=-1, **kwargs):
    """
    wrapper for scipy.ndimage.prewitt.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Prewitt Filter along axis ' + str(axis) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.prewitt(array, axis=axis, **kwargs)
        image.set_array(array)
        _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.median_filter.html#scipy.ndimage.median_filter
def median_filter(input, size=3, **kwargs):
    """
    wrapper for scipy.ndimage.median_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Median Filter with size ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.median_filter(array, size=size, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.percentile_filter.html#scipy.ndimage.percentile_filter
def percentile_filter(input, percentile, **kwargs):
    """
    wrapper for scipy.ndimage.percentile_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Percentile Filter x ' + str(percentile) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.percentile_filter(array, percentile, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.rank_filter.html#scipy.ndimage.rank_filter
def rank_filter(input, rank, **kwargs):
    """
    wrapper for scipy.ndimage.rank_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Rank Filter x ' + str(rank) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.rank_filter(array, rank, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.minimum_filter.html#scipy.ndimage.maximum_filter
def maximum_filter(input, size=3, **kwargs):
    """
    wrapper for scipy.ndimage.maximum_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Maximum Filter x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.maximum_filter(array, size=size, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.minimum_filter.html#scipy.ndimage.minimum_filter
def minimum_filter(input, size=3, **kwargs):
    """
    wrapper for scipy.ndimage.minimum_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Minimum Filter x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.minimum_filter(array, size=size, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.uniform_filter.html#scipy.ndimage.uniform_filter
def uniform_filter(input, size=3, **kwargs):
    """
    wrapper for scipy.ndimage.uniform_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Uniform Filter x ' + str(size) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.uniform_filter(array, size=size, **kwargs)
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered
    

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html#scipy.ndimage.gaussian_filter
def gaussian_filter(input, sigma, **kwargs):
    """
    wrapper for scipy.ndimage.gaussian_filter.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Gaussian Filter x ' + str(sigma) + ' ]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.gaussian_filter(array, sigma, **kwargs)
        image.set_array(array)
        if 'order' in kwargs:
            if kwargs['order'] > 0:
                _reset_window(image, array)
        image.clear()
    input.status.hide()
    return filtered


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.fourier_shift.html#scipy.ndimage.fourier_shift
def fourier_shift(input, shift, **kwargs):
    """
    wrapper for scipy.ndimage.fourier_shift.

    Parameters
    ----------
    input: dbdicom series

    Returns
    -------
    filtered : dbdicom series
    """
    suffix = ' [Fourier Shift]'
    desc = input.instance().SeriesDescription
    filtered = input.copy(SeriesDescription = desc + suffix)
    #images = filtered.instances()
    images = filtered.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Filtering ' + desc)
        image.read()
        array = image.array()
        array = np.fft.fft2(array)
        array = scipy.ndimage.fourier_shift(array, shift, **kwargs)
        array = np.fft.ifft2(array).real
        image.set_array(array)
        image.clear()
    input.status.hide()
    return filtered




# RESCALE AND RESLICE




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
    #images = zoomed.instances()
    images = zoomed.images()
    for i, image in enumerate(images):
        input.status.progress(i+1, len(images), 'Resizing ' + desc)
        image.read()
        array = image.array()
        array = scipy.ndimage.zoom(array, zoom, **kwargs)
        image.set_array(array)
        pixel_spacing = image.PixelSpacing
        image.PixelSpacing = [p/zoom for p in pixel_spacing]
        image.clear()
    input.status.hide()
    return zoomed


def resample(series, voxel_size=[1.0, 1.0, 1.0]):
    series.status.message('Reading transformations..')
    affine_source = series.affine_matrix()
    if affine_source is None:
        return
    if isinstance(affine_source, list):
        mapped_series = []
        for affine_slice_group in affine_source:
            mapped = _resample_slice_group(series, affine_slice_group[0], affine_slice_group[0], voxel_size=voxel_size)
            mapped_series.append(mapped)
        desc = series.instance().SeriesDescription + '[resampled]'
        mapped_series = dbdicom.merge(mapped_series, inplace=True)
        mapped_series.SeriesDescription = desc
    else:
        mapped_series = _resample_slice_group(series, affine_source[0], affine_source[1], voxel_size=voxel_size)
    return mapped_series


def reslice(series, orientation='axial'):

    # Define geometry of axial series (isotropic)
    series.status.message('Reading transformations..')
    affine_source = series.affine_matrix()
    if isinstance(affine_source, list):
        mapped_series = []
        for affine_slice_group in affine_source:
            mapped = _reslice_slice_group(series, affine_slice_group[0], affine_slice_group[0], orientation=orientation)
            mapped_series.append(mapped)
            #slice_group.remove()
        desc = series.instance().SeriesDescription + '['+orientation+']'
        mapped_series = dbdicom.merge(mapped_series, inplace=True)
        mapped_series.SeriesDescription = desc
    else:
        mapped_series = _reslice_slice_group(series, affine_source[0], affine_source[1], orientation=orientation)
    return mapped_series


def _resample_slice_group(series, affine_source, slice_group, voxel_size=[1.0, 1.0, 1.0]):

    # Create new resliced series
    desc = series.instance().SeriesDescription + '[resampled]'
    resliced_series = series.new_sibling(SeriesDescription = desc)

    # Work out the affine matrix of the new series
    p = dbdicom.utils.image.dismantle_affine_matrix(affine_source)
    affine_target = affine_source.copy()
    affine_target[:3, 0] = voxel_size[0] * np.array(p['ImageOrientationPatient'][:3])
    affine_target[:3, 1] = voxel_size[1] * np.array(p['ImageOrientationPatient'][3:]) 
    affine_target[:3, 2] = voxel_size[2] * np.array(p['slice_cosine'])

    # If the series already is in the right orientation, return a copy
    if np.array_equal(affine_source, affine_target):
        series.status.message('Series is already in the right orientation..')
        resliced_series.adopt(slice_group)
        return resliced_series

    # Perform transformation on the arrays to determine the output shape
    dim = [
        array.shape[0] * p['PixelSpacing'][1],
        array.shape[1] * p['PixelSpacing'][0],
        array.shape[2] * p['SliceThickness'],
    ]
    output_shape = [1 + round(dim[i]/voxel_size[i]) for i in range(3)]

    # Determine the transformation matrix and offset
    source_to_target = np.linalg.inv(affine_source).dot(affine_target)
    matrix, offset = nib.affines.to_matvec(source_to_target)
    
    # Get arrays
    array, headers = series.array(['SliceLocation','AcquisitionTime'], pixels_first=True)
    if array is None:
        return resliced_series

    # Perform the affine transformation
    cnt=0
    ns, nt, nk = output_shape[2], array.shape[-2], array.shape[-1]
    pos, loc = dbdicom.utils.image.image_position_patient(affine_target, ns)
    for t in range(nt):
        for k in range(nk):
            cnt+=1
            series.status.progress(cnt, nt*nk, 'Performing transformation..')
            resliced = scipy.ndimage.affine_transform(
                array[:,:,:,t,k],
                matrix = matrix,
                offset = offset,
                output_shape = output_shape,
            )
            resliced_series.set_array(resliced, 
                source = headers[0,t,k],
                pixels_first = True,
                affine_matrix = affine_target,
                ImagePositionPatient = pos,
                SliceLocation = loc,
            )
    series.status.message('Finished mapping..')
    return resliced_series


def _reslice_slice_group(series, affine_source, slice_group, orientation='axial'):

    # Create new resliced series
    desc = series.instance().SeriesDescription + '['+orientation+']'
    resliced_series = series.new_sibling(SeriesDescription = desc)

    # Work out the affine matrix of the new series
    p = dbdicom.utils.image.dismantle_affine_matrix(affine_source)
    image_positions = [s.ImagePositionPatient for s in slice_group]
    rows = slice_group[0].Rows
    columns = slice_group[0].Columns
    box = dbdicom.utils.image.bounding_box(
        p['ImageOrientationPatient'],  
        image_positions,   
        p['PixelSpacing'], 
        rows,
        columns)
    spacing = np.mean([p['PixelSpacing'][0], p['PixelSpacing'][1], p['SliceThickness']])
    affine_target = dbdicom.utils.image.standard_affine_matrix(
        box, 
        [spacing, spacing],
        spacing,
        orientation=orientation)

    # If the series already is in the right orientation, return a copy
    if np.array_equal(affine_source, affine_target):
        series.status.message('Series is already in the right orientation..')
        resliced_series.adopt(slice_group)
        return resliced_series

    #Perform transformation on the arrays to determine the output shape
    if orientation == 'axial':
        dim = [
            np.linalg.norm(np.array(box['RAF'])-np.array(box['LAF'])),
            np.linalg.norm(np.array(box['RAF'])-np.array(box['RPF'])),
            np.linalg.norm(np.array(box['RAF'])-np.array(box['RAH'])),
        ]
    elif orientation == 'coronal':
        dim = [
            np.linalg.norm(np.array(box['RAH'])-np.array(box['LAH'])),
            np.linalg.norm(np.array(box['RAH'])-np.array(box['RAF'])),
            np.linalg.norm(np.array(box['RAH'])-np.array(box['RPH'])),
        ]
    elif orientation == 'sagittal':
        dim = [
            np.linalg.norm(np.array(box['LAH'])-np.array(box['LPH'])),
            np.linalg.norm(np.array(box['LAH'])-np.array(box['LAF'])),
            np.linalg.norm(np.array(box['LAH'])-np.array(box['RAH'])),
        ]
    output_shape = [1 + round(d/spacing) for d in dim]

    # Determine the transformation matrix and offset
    source_to_target = np.linalg.inv(affine_source).dot(affine_target)
    matrix, offset = nib.affines.to_matvec(source_to_target)
    
    # Get arrays
    array, headers = series.array(['SliceLocation','AcquisitionTime'], pixels_first=True)

    # Perform the affine transformation and save results
    cnt=0
    ns, nt, nk = output_shape[2], array.shape[-2], array.shape[-1] 
    pos, loc = dbdicom.utils.image.image_position_patient(affine_target, ns)
    for t in range(nt):
        for k in range(nk):
            cnt+=1
            series.status.progress(cnt, nt*nk, 'Calculating..')
            resliced = scipy.ndimage.affine_transform(
                array[:,:,:,t,k],
                matrix = matrix,
                offset = offset,
                output_shape = output_shape,
            )
            # Saving results at each time to avoid memory problems.
            # Assign acquisition time of slice=0 to all slices
            resliced_series.set_array(resliced, 
                source = headers[0,t,k],
                pixels_first = True,
                affine_matrix = affine_target,
                ImagePositionPatient = pos,
                SliceLocation = loc,
            )
    series.status.message('Finished mapping..')
    return resliced_series



# Helper functions

def _reset_window(image, array):
    min = np.amin(array)
    max = np.amax(array)
    image.WindowCenter= (max+min)/2
    image.WindowWidth = 0.9*(max-min)