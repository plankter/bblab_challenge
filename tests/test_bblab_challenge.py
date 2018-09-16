#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bblab_challenge` package."""

import pytest

from click.testing import CliRunner

from bblab_challenge import tools
from bblab_challenge import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['--amp',
                                       '5.0',
                                      'data/single-cell-mask/single_cell_mask.tiff',
                                      'data/images/Fibronectin(Dy163Di).tiff',
                                      'data/images/E-cadherin(Er167Di).tiff',
                                      'data/images/HistoneH3(Yb176Di).tiff',
                                      'output/bgra.png',
                                      'output/masked_bgra.png',
                                      'output/means.csv'])
    assert result.exit_code == 0
    help_result = runner.invoke(cli.cli, ['--help'])
    assert help_result.exit_code == 0
