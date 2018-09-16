# -*- coding: utf-8 -*-

"""Console script for bblab_challenge."""
import click
import cv2 as cv
import numpy as np

from bblab_challenge import load_mask, load_layer, get_bgra, apply_mask, calculate_markers, prepare_image, \
    calculate_means


@click.command()
@click.argument('mask', type=click.Path(exists=True))
@click.argument('r', type=click.Path(exists=True))
@click.argument('g', type=click.Path(exists=True))
@click.argument('b', type=click.Path(exists=True))
@click.argument('out', type=click.Path(exists=False))
@click.argument('masked_out', type=click.Path(exists=False))
@click.argument('csv', type=click.Path(exists=False))
@click.option('--amp', default=1.0, help='channel intensity amplification')
def cli(mask: str, r: str, g: str, b: str, out: str, masked_out: str, csv: str, amp: float):
    """
    Console script for bblab_challenge.

    List of arguments:

    MASK: mask image filename

    R: red channel image filename

    G: green channel image filename

    B: blue channel image filename

    OUT: layered output image filename

    MASKED_OUT: masked output image filename

    CSV: CSV output data filename
    """
    mask = load_mask(mask)
    image_height, image_width = mask.shape
    red = load_layer(r, image_width, image_height)
    green = load_layer(g, image_width, image_height)
    blue = load_layer(b, image_width, image_height)

    bgra = get_bgra(red, green, blue, amp, amp, amp)
    cv.imwrite(out, bgra)

    masked_bgra = apply_mask(bgra, mask)
    cv.imwrite(masked_out, masked_bgra)

    markers = calculate_markers(masked_bgra, mask)

    img = prepare_image(masked_bgra, mask)
    img[markers == -1] = [255, 0, 0]

    means = calculate_means(red, green, blue, markers)
    np.savetxt(csv, means, header='cell_id;red;green;blue', fmt="%i;%1.4f;%1.4f;%1.4f", comments='')

    return 0
