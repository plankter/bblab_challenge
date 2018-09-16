# -*- coding: utf-8 -*-

"""Main module."""

from collections import defaultdict
import numpy as np
import cv2 as cv
from skimage.io import imread


def load_mask(fname: str) -> np.ndarray:
    """
    Loads cell mask by PIL plugin as default OpenCV imread implementation has some problems dealing with CCITTRLE
    compressed TIFF files.

    :param fname: file name
    :rtype: NumPy ndarray
    """
    mask = imread(fname, plugin='pil')
    return mask


def load_layer(fname: str, width: int, height: int) -> np.ndarray:
    """
    Loads separate layer with predefined image size

    :param fname: file name
    :param width: image width
    :param height: image height
    :rtype: NumPy ndarray
    """
    layer = imread(fname)
    if (layer.shape != (height, width)):
        raise ValueError(
            'Image size of all layers and a mask should be the same')
    return layer


def get_bgra(red: np.ndarray, green: np.ndarray, blue: np.ndarray,
             red_amp: float = 1.0, green_amp: float = 1.0,
             blue_amp: float = 1.0) -> np.ndarray:
    """
    Generates an image in BGRA format with alpha channel from separate layers.
    CAUTION: OpenCV library operates in BGR mode by default, not RGB!

    :param red: red layer
    :param green: green layer
    :param blue: blue layer
    :param red_amp: red intensity amplifier
    :param green_amp: green intensity amplifier
    :param blue_amp: blue intensity amplifier
    :rtype: NumPy ndarray
    """
    bgra = np.zeros((red.shape[0], red.shape[1], 4))
    bgra[:, :, 0] = blue * blue_amp
    bgra[:, :, 1] = green * green_amp
    bgra[:, :, 2] = red * red_amp
    bgra[:, :, 3] = 255
    return bgra


def get_rgba(red: np.ndarray, green: np.ndarray, blue: np.ndarray,
             red_amp: float = 1.0, green_amp: float = 1.0,
             blue_amp: float = 1.0) -> np.ndarray:
    """
    Generates an image in RGBA format with alpha channel from separate layers. Useful for displaying inline images in
    Jupyter notebooks as they should be provided in RGB mode.

    :param red: red layer
    :param green: green layer
    :param blue: blue layer
    :param red_amp: red intensity amplifier
    :param green_amp: green intensity amplifier
    :param blue_amp: blue intensity amplifier
    :rtype: NumPy ndarray
    """
    rgba = np.zeros((red.shape[0], red.shape[1], 4))
    rgba[:, :, 0] = red * red_amp
    rgba[:, :, 1] = green * green_amp
    rgba[:, :, 2] = blue * blue_amp
    rgba[:, :, 3] = 255
    return rgba


def apply_mask(src: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Applies mask to source image

    :param src: source image
    :param mask: mask image
    :rtype: NumPy ndarray
    """
    masked_rgb = src.copy()
    masked_rgb[:, :, 3] = mask
    return masked_rgb


def prepare_image(src: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Converts source image from BGRA to BGR format and sets Numpy type to uint8 for a proper image segmentation

    :param src: source image
    :param mask: mask image
    :rtype: NumPy ndarray
    """
    tmp = np.uint8(src.copy())
    rgb = cv.cvtColor(tmp, cv.COLOR_BGRA2BGR)
    result = cv.bitwise_and(rgb, rgb, mask=mask)
    return result


def calculate_markers(src: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Performs image segmentation via OpenCV library

    :param src: source image
    :param mask: mask image
    :rtype: NumPy ndarray
    """
    gray = cv.bitwise_not(mask.copy())
    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)

    # Sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=2)

    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.1 * dist_transform.max(), 255, 0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)

    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0

    img = prepare_image(src, mask)
    markers = cv.watershed(img, markers)
    return markers


def calculate_means(red: np.ndarray, green: np.ndarray, blue: np.ndarray, markers: np.ndarray):
    """
    Calculates means for each channel (RGB) for each recognized cell

    :param red: red layer
    :param green: green layer
    :param blue: blue layer
    :param markers: cell markers
    """
    r_dict = defaultdict(list)
    g_dict = defaultdict(list)
    b_dict = defaultdict(list)
    for i, row in enumerate(markers):
        for j, label in enumerate(row):
            if label != -1 and label != 1:
                r_dict[label].append(red[i, j])
                g_dict[label].append(green[i, j])
                b_dict[label].append(blue[i, j])

    result = []
    for label in r_dict.keys():
        r = sum(r_dict[label]) / len(r_dict[label])
        g = sum(g_dict[label]) / len(g_dict[label])
        b = sum(b_dict[label]) / len(b_dict[label])
        result.append([label, r, g, b])
    return result
