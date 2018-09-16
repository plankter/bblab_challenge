#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bblab_challenge` package."""

import pytest
import numpy as np
from click.testing import CliRunner

from bblab_challenge import cli, load_layer, load_mask, get_bgra, get_rgba, apply_mask, calculate_means


def test_load_layer():
    with pytest.raises(ValueError):
        assert load_layer('data/images/Fibronectin(Dy163Di).tiff', 100, 100)
    assert load_layer('data/images/Fibronectin(Dy163Di).tiff', 400, 395).shape == (395, 400)


def test_load_mask():
    assert load_mask('data/single-cell-mask/single_cell_mask.tiff').shape == (395, 400)


def test_get_bgra():
    r = np.array([[1, 1]])
    g = np.array([[2, 2]])
    b = np.array([[3, 3]])
    result = np.array([[[3., 2., 1., 255.],
                        [3., 2., 1., 255.]]])
    assert np.array_equal(get_bgra(r, g, b), result) is True


def test_get_rgba():
    r = np.array([[1, 1]])
    g = np.array([[2, 2]])
    b = np.array([[3, 3]])
    result = np.array([[[1., 2., 3., 255.],
                        [1., 2., 3., 255.]]])
    assert np.array_equal(get_rgba(r, g, b), result) is True


def test_apply_mask():
    src = np.array([[[1., 2., 3., 255.],
                     [1., 2., 3., 255.]]])
    mask = np.array([[0, 0]])
    result = np.array([[[1., 2., 3., 0.],
                        [1., 2., 3., 0.]]])
    assert np.array_equal(apply_mask(src, mask), result) is True


def test_calculate_means():
    red = [[1, 1], [1, 2]]
    green = [[1, 1], [1, 2]]
    blue = [[1, 1], [1, 2]]
    markers = [[1, 1], [1, 1]]
    result = []
    assert np.array_equal(calculate_means(red, green, blue, markers), result) is True


# Disable CLI test as Travis does not allow file operations.
# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     result = runner.invoke(cli.cli, ['--amp',
#                                        '5.0',
#                                       'data/single-cell-mask/single_cell_mask.tiff',
#                                       'data/images/Fibronectin(Dy163Di).tiff',
#                                       'data/images/E-cadherin(Er167Di).tiff',
#                                       'data/images/HistoneH3(Yb176Di).tiff',
#                                       'output/bgra.png',
#                                       'output/masked_bgra.png',
#                                       'output/means.csv'])
#     assert result.exit_code == 0
#     help_result = runner.invoke(cli.cli, ['--help'])
#     assert help_result.exit_code == 0
