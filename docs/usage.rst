=====
Usage
=====

To use BBlab package in a project::

    import bblab_challenge


To use BBlab as a command line tool::

    bblab [OPTIONS] MASK R G B OUT MASKED_OUT CSV

To get help for bblab CLI::

    bblab --help

List of arguments:
------------------
    MASK: mask image filename

    R: red channel image filename

    G: green channel image filename

    B: blue channel image filename

    OUT: layered image output filename

    MASKED_OUT: masked image output filename

    CSV: CSV data output filename

Available options:
--------------------------------

    --amp NUMBER: channels intensity amplification
