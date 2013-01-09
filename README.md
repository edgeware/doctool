# Doctool

Small utility to build a single document from multiple Markdown files.

Usage:

    doctool <infile> [outfile]

## Document syntax

Markdown files can included by doing

    <!--include somefile.md-->

Cross-linking to sections is done by adding an anchor to the section headline, e.g.

    ## Some section {#some-section}
    
Which can then be referenced by markdown linking:

    see also []{#some-section}

Inlining of dot and ditaa graphs is supported by surrounding the
graph with

    <dot></dot>
    
or

    <ditaa></ditaa>
    
tags respectively.
