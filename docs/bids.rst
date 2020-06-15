.. _bids:

======================================
Why use BIDS (for physiological data)?
======================================

What is BIDS?
-------------

The `Brain Imaging Data Standard (BIDS) <https://bids.neuroimaging.io>`_ is the most commonly used standard for organizing neuroimaging data.
Originally introduced in 2016 by `Gorgolewski et al. <https://www.nature.com/articles/sdata201644>`_, BIDS quickly gained popularity, driven largely by the development of downstream `BIDS-Apps <https://bids-apps.neuroimaging.io/>`_ and the standard's mandated use in popular data-sharing repositories like `OpenNeuro <https://openneuro.org>`_.
Since then, the standard has evolved to accommodate additional data modalities and support new extensions (refer to `this site <https://bids-specification.readthedocs.io/en/stable/>`_ for the current version).

At its core, BIDS simply provides a few conventions for how to organize and name directories and data files.
These naming conventions rely on heuristic key-value pairs, such that they are both human- and machine-readable.
Most data files are accompanied by a JSON "sidecar," which provides additional information on the data stored within its partner file.
This relatively lightweight structure makes BIDS incredibly powerful and, importantly, easy to adopt!

Why use BIDS?
-------------

``phys2bids`` was originally designed by neuroscientists who wanted to examine the relationship between physiology and brain function (see :ref:`bestpractice` for more information on why this is important).
Given the preponderance of physiological data formats—which can vary dramatically across acquisition platforms and software—there was no singular software package that could readily accommodate *any* data file thrown at it.
That is, the lack of a standardized data format, and software that made it easy to convert files to that format, seemed to us to be a major limiting factor in the physiological research community.

To attempt to remedy this we decided to rely on BIDS, which had `conventions for physiological data <https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/06-physiological-and-other-continuous-recordings.html>`_ built in since its initial release.
Though the physiological conventions of BIDS are obviously designed to complement neuroimaging data collection, it is by no means required!
Nonetheless, we believe that it is currently the best option for the field.

Beyond ``phys2bids``
--------------------

In our minds, the data format provided by BIDS will allow for the development of robust, community-driven software for working with physiological data.
That is, ``phys2bids`` is merely the first step of what will hopefully become a more comprehensive software suite.
For more on these development, continue to check in on the `physiopy organization <https://github.com/physiopy>`_ on GitHub.
New contributors are always welcome!
