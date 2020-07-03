<!--(https://raw.githubusercontent.com/physiopy/phys2bids/master/docs/_static/phys2bids_card.jpg)-->
<a name="readme"></a>
<img alt="Phys2BIDS" src="https://github.com/physiopy/phys2bids/blob/master/docs/_static/phys2bids_logo1280×640.png" height="150">

phys2bids
=========

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3653153.svg)](https://doi.org/10.5281/zenodo.3653153)
[![Join the chat at Gitter: https://gitter.im/physiopy/phys2bids](https://badges.gitter.im/physiopy/phys2bids.svg)](https://gitter.im/physiopy/phys2bids?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=body_badge)
[![codecov](https://codecov.io/gh/physiopy/phys2bids/branch/master/graph/badge.svg)](https://codecov.io/gh/physiopy/phys2bids)

[![Build Status: Linux](https://travis-ci.org/physiopy/phys2bids.svg?branch=master)](https://travis-ci.org/physiopy/phys2bids)
[![Build Status. Windows](https://dev.azure.com/physiopy/phys2bids/_apis/build/status/physiopy.phys2bids?branchName=master)](https://dev.azure.com/physiopy/phys2bids/_build/latest?definitionId=1&branchName=master)
[![See the documentation at: https://phys2bids.readthedocs.io](https://readthedocs.org/projects/phys2bids/badge/?version=latest)](https://phys2bids.readthedocs.io/en/latest/?badge=latest)
[![Requirements Status](https://requires.io/github/physiopy/phys2bids/requirements.svg?branch=master)](https://requires.io/github/physiopy/phys2bids/requirements/?branch=master)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-14-orange.svg?style=flat)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

``phys2bids`` is a python3 library meant to format physiological files in BIDS.
It was born for AcqKnowledge files (BIOPAC), and at the moment it supports
``.acq`` files as well as ``.txt`` files obtained by labchart
(ADInstruments).
It doesn't support physiological files recorded with the MRI, as you can find a software for it [here](https://github.com/tarrlab/physio2bids).

> If you use ``phys2bids`` in your work, please cite it with the zenodo DOI. You can check it [here](https://zenodo.org/record/3903920)

[Read the latest documentation](https://phys2bids.readthedocs.io/en/latest/) for more information on phys2bids!

Shortcuts:
- [Requirements](https://phys2bids.readthedocs.io/en/latest/installation.html#requirements)
- [Installation](https://phys2bids.readthedocs.io/en/latest/installation.html#linux-and-mac-installation)
- [Usage](https://phys2bids.readthedocs.io/en/latest/cli.html)
- [How to use phys2bids](https://phys2bids.readthedocs.io/en/latest/howto.html)
- [Contributing to phys2bids](https://phys2bids.readthedocs.io/en/latest/contributing.html)
- [Developer installation](https://phys2bids.readthedocs.io/en/latest/contributing.html#linux-and-mac-developer-installation)
- [**Contributor guide**](https://phys2bids.readthedocs.io/en/latest/contributorfile.html)
- [**Code of Conduct**](https://phys2bids.readthedocs.io/en/latest/conduct.html)

## The BrainWeb
BrainWeb participants, welcome!
We have a milestone [here](https://github.com/physiopy/phys2bids/milestone/5) as a collection of issues you could work on with our help. 
Check the issues with a `BrainWeb` label. Of course, they are only suggestions, so feel free to tackle any issue you want, even open new ones!
You can also contact us on Gitter, in the BrainHack Mattermost (<a href="https://mattermost.brainhack.org/brainhack/channels/physiopy">#physiopy</a>), and don't hesitate to contact [Stefano](https://github.com/smoia) in other ways to jump in the development!

**We're looking for code contributors,** but any suggestion/bug report is welcome! Feel free to open issues!

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/danalclop"><img src="https://avatars0.githubusercontent.com/u/38854309?v=4" width="100px;" alt=""/><br /><sub><b>Daniel Alcalá</b></sub></a><br /><a href="#design-danalclop" title="Design">🎨</a></td>
    <td align="center"><a href="https://github.com/AyyagariA"><img src="https://avatars1.githubusercontent.com/u/50453337?v=4" width="100px;" alt=""/><br /><sub><b>Apoorva Ayyagari</b></sub></a><br /><a href="#content-AyyagariA" title="Content">🖋</a> <a href="#data-AyyagariA" title="Data">🔣</a> <a href="https://github.com/physiopy/phys2bids/commits?author=AyyagariA" title="Documentation">📖</a></td>
    <td align="center"><a href="http://brightlab.northwestern.edu"><img src="https://avatars2.githubusercontent.com/u/32640425?v=4" width="100px;" alt=""/><br /><sub><b>Molly Bright</b></sub></a><br /><a href="#content-BrightMG" title="Content">🖋</a> <a href="#data-BrightMG" title="Data">🔣</a> <a href="#ideas-BrightMG" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/CesarCaballeroGaudes"><img src="https://avatars1.githubusercontent.com/u/7611340?v=4" width="100px;" alt=""/><br /><sub><b>Cesar Caballero Gaudes</b></sub></a><br /><a href="#content-CesarCaballeroGaudes" title="Content">🖋</a> <a href="#data-CesarCaballeroGaudes" title="Data">🔣</a> <a href="#ideas-CesarCaballeroGaudes" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/vinferrer"><img src="https://avatars2.githubusercontent.com/u/38909338?v=4" width="100px;" alt=""/><br /><sub><b>Vicente Ferrer</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Avinferrer" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=vinferrer" title="Code">💻</a> <a href="https://github.com/physiopy/phys2bids/commits?author=vinferrer" title="Documentation">📖</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Avinferrer" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="http://soichi.us"><img src="https://avatars3.githubusercontent.com/u/923896?v=4" width="100px;" alt=""/><br /><sub><b>Soichi Hayashi</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Asoichih" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/sangfrois"><img src="https://avatars0.githubusercontent.com/u/38385719?v=4" width="100px;" alt=""/><br /><sub><b>François Lespinasse</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=sangfrois" title="Code">💻</a> <a href="https://github.com/physiopy/phys2bids/commits?author=sangfrois" title="Tests">⚠️</a></td>
    <td align="center"><a href="http://rossmarkello.com"><img src="https://avatars0.githubusercontent.com/u/14265705?v=4" width="100px;" alt=""/><br /><sub><b>Ross Markello</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Armarkello" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=rmarkello" title="Code">💻</a> <a href="#content-rmarkello" title="Content">🖋</a> <a href="#ideas-rmarkello" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-rmarkello" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Armarkello" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/physiopy/phys2bids/commits?author=rmarkello" title="Tests">⚠️</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/smoia"><img src="https://avatars3.githubusercontent.com/u/35300580?v=4" width="100px;" alt=""/><br /><sub><b>Stefano Moia</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=smoia" title="Code">💻</a> <a href="#content-smoia" title="Content">🖋</a> <a href="#data-smoia" title="Data">🔣</a> <a href="#ideas-smoia" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-smoia" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#projectManagement-smoia" title="Project Management">📆</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Asmoia" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/physiopy/phys2bids/commits?author=smoia" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/robertoostenveld"><img src="https://avatars1.githubusercontent.com/u/899043?v=4" width="100px;" alt=""/><br /><sub><b>Robert Oostenveld</b></sub></a><br /><a href="#ideas-robertoostenveld" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Arobertoostenveld" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/tsalo"><img src="https://avatars3.githubusercontent.com/u/8228902?v=4" width="100px;" alt=""/><br /><sub><b>Taylor Salo</b></sub></a><br /><a href="#ideas-tsalo" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/physiopy/phys2bids/commits?author=tsalo" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/RayStick"><img src="https://avatars3.githubusercontent.com/u/50215726?v=4" width="100px;" alt=""/><br /><sub><b>Rachael Stickland</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3ARayStick" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=RayStick" title="Code">💻</a> <a href="#data-RayStick" title="Data">🔣</a> <a href="https://github.com/physiopy/phys2bids/commits?author=RayStick" title="Documentation">📖</a> <a href="#userTesting-RayStick" title="User Testing">📓</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/eurunuela"><img src="https://avatars0.githubusercontent.com/u/13706448?v=4" width="100px;" alt=""/><br /><sub><b>Eneko Uruñuela</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Aeurunuela" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=eurunuela" title="Code">💻</a> <a href="#infra-eurunuela" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Aeurunuela" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/physiopy/phys2bids/commits?author=eurunuela" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/kristinazvolanek"><img src="https://avatars3.githubusercontent.com/u/54590158?v=4" width="100px;" alt=""/><br /><sub><b>Kristina Zvolanek</b></sub></a><br /><a href="#data-kristinazvolanek" title="Data">🔣</a> <a href="#content-kristinazvolanek" title="Content">🖋</a> <a href="https://github.com/physiopy/phys2bids/commits?author=kristinazvolanek" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

License
-------

Copyright 2019-2020, The Phys2BIDS community.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
