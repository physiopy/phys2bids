<!--(https://raw.githubusercontent.com/physiopy/phys2bids/master/docs/_static/phys2bids_card.jpg)-->
<a name="readme"></a>
<img alt="Phys2BIDS" src="https://github.com/physiopy/phys2bids/blob/master/docs/_static/phys2bids_logo1280×640.png" height="150">

phys2bids
=========

[![Latest version](https://img.shields.io/github/v/release/physiopy/phys2bids?style=flat&logo=github&sort=semver)](https://github.com/physiopy/phys2bids/releases)
[![Release date](https://img.shields.io/github/release-date/physiopy/phys2bids?style=flat&logo=github)](https://github.com/physiopy/phys2bids/releases)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?style=flat&colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)

[![See the documentation at: https://phys2bids.readthedocs.io](https://img.shields.io/badge/docs-read%20latest-informational?style=flat&logo=readthedocs)](https://phys2bids.readthedocs.io/en/latest/?badge=latest)
[![Latest DOI](https://zenodo.org/badge/208861898.svg)](https://zenodo.org/badge/latestdoi/208861898)
[![Licensed Apache 2.0](https://img.shields.io/github/license/physiopy/phys2bids?style=flat&logo=apache)](https://github.com/physiopy/phys2bids/blob/master/LICENSE)

[![Codecov](https://img.shields.io/codecov/c/gh/physiopy/phys2bids?style=flat&label=codecov&logo=codecov)](https://codecov.io/gh/physiopy/phys2bids)
[![Build Status](https://img.shields.io/circleci/build/github/physiopy/phys2bids?style=flat&label=circleci&logo=circleci)](https://circleci.com/gh/physiopy/phys2bids)
[![Documentation Status](https://img.shields.io/readthedocs/phys2bids?style=flat&label=readthedocs&logo=readthedocs)](https://phys2bids.readthedocs.io/en/latest/?badge=latest)

[![Latest version](https://img.shields.io/pypi/v/phys2bids?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/phys2bids/)
[![Supports python version](https://img.shields.io/pypi/pyversions/phys2bids?style=flat&logo=python&logoColor=white)](https://pypi.org/project/phys2bids/)

[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto)](https://github.com/intuit/auto)
[![Supports python version](https://img.shields.io/pypi/pyversions/phys2bids)](https://pypi.org/project/phys2bids/)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-22-orange.svg?style=flat)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

``phys2bids`` is a python3 library meant to format physiological files in BIDS.
It was born for AcqKnowledge files (BIOPAC), and at the moment it supports
``.acq`` files as well as ``.txt`` files obtained by labchart
(ADInstruments) and GE MRI files.

> If you use ``phys2bids`` in your work, please support it by citing the zenodo DOI of the version you used. You can find the latest version [here](https://doi.org/10.5281/zenodo.3470091)

> We also support gathering all relevant citations via [DueCredit](http://duecredit.org).

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
- [Developer calls calendar](https://calendar.google.com/calendar/u/0?cid=amoycDQ1MTdhMWdpaHNuNzlnOW1ucHJkMjRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)

## Tested OSs
While all version until `2.6.2` were tested on Linux and Windows, starting from version `2.7` onward we had to **drop Windows testing**. The reason is related to the cost of running such tests: for each Windows test, we can run up to 8 tests on Linux instead. Partial Windows testing might be reintroduced in future releases.

Hence, while **we cannot ensure that phys2bids will run on Windows**, however we don't see any reason it shouldn't. Besides, it will run on Linux Subsistems.

We apologise for the discomfort.


<!-- ## Hacktoberfest
Hacktoberfest participants, welcome!
We have some issues for you [here](https://github.com/physiopy/phys2bids/issues?q=is%3Aissue+is%3Aopen+label%3Ahacktoberfest)!
However, feel free to tackle any issue you'd like. Depending on the issue and extent of contribution, Hacktoberfest related PRs might not count toward being listed as contributors and authors (unless there is the specific interest). You can ask about it in the issue itself!
Feel free to ask help to the contributors over gitter, happy coding and (hopefully) enjoy hour tee (or tree)!

## The BrainWeb
BrainWeb participants, welcome!
We have a milestone [here](https://github.com/physiopy/phys2bids/milestone/5) as a collection of issues you could work on with our help.
Check the issues with a `BrainWeb` label. Of course, they are only suggestions, so feel free to tackle any issue you want, even open new ones!
You can also contact us on Gitter, in the BrainHack Mattermost (<a href="https://mattermost.brainhack.org/brainhack/channels/physiopy">#physiopy</a>), and don't hesitate to contact [Stefano](https://github.com/smoia) in other ways to jump in the development!
-->

**We're looking for code contributors,** but any suggestion/bug report is welcome! Feel free to open issues!

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/danalclop"><img src="https://avatars0.githubusercontent.com/u/38854309?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Daniel Alcalá</b></sub></a><br /><a href="#design-danalclop" title="Design">🎨</a></td>
    <td align="center"><a href="https://github.com/AyyagariA"><img src="https://avatars1.githubusercontent.com/u/50453337?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Apoorva Ayyagari</b></sub></a><br /><a href="#content-AyyagariA" title="Content">🖋</a> <a href="#data-AyyagariA" title="Data">🔣</a> <a href="https://github.com/physiopy/phys2bids/commits?author=AyyagariA" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/62442katieb"><img src="https://avatars1.githubusercontent.com/u/14095475?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Katie Bottenhorn</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=62442katieb" title="Code">💻</a> <a href="#mentoring-62442katieb" title="Mentoring">🧑‍🏫</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3A62442katieb" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="http://brightlab.northwestern.edu"><img src="https://avatars2.githubusercontent.com/u/32640425?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Molly Bright</b></sub></a><br /><a href="#content-BrightMG" title="Content">🖋</a> <a href="#data-BrightMG" title="Data">🔣</a> <a href="#ideas-BrightMG" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/CesarCaballeroGaudes"><img src="https://avatars1.githubusercontent.com/u/7611340?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Cesar Caballero Gaudes</b></sub></a><br /><a href="#content-CesarCaballeroGaudes" title="Content">🖋</a> <a href="#data-CesarCaballeroGaudes" title="Data">🔣</a> <a href="#ideas-CesarCaballeroGaudes" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/ineschh"><img src="https://avatars0.githubusercontent.com/u/72545702?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Inés Chavarría</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=ineschh" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/vinferrer"><img src="https://avatars2.githubusercontent.com/u/38909338?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Vicente Ferrer</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Avinferrer" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=vinferrer" title="Code">💻</a> <a href="https://github.com/physiopy/phys2bids/commits?author=vinferrer" title="Documentation">📖</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Avinferrer" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/physiopy/phys2bids/commits?author=vinferrer" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/yarikoptic"><img src="https://avatars.githubusercontent.com/u/39889?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Yaroslav Halchenko</b></sub></a><br /><a href="#infra-yarikoptic" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
  <tr>
    <td align="center"><a href="http://soichi.us"><img src="https://avatars3.githubusercontent.com/u/923896?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Soichi Hayashi</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Asoichih" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/viacovella"><img src="https://avatars1.githubusercontent.com/u/1639782?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Vittorio Iacovella</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=viacovella" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/sangfrois"><img src="https://avatars0.githubusercontent.com/u/38385719?v=4?s=100" width="100px;" alt=""/><br /><sub><b>François Lespinasse</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=sangfrois" title="Code">💻</a> <a href="https://github.com/physiopy/phys2bids/commits?author=sangfrois" title="Tests">⚠️</a></td>
    <td align="center"><a href="http://rossmarkello.com"><img src="https://avatars0.githubusercontent.com/u/14265705?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ross Markello</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Armarkello" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=rmarkello" title="Code">💻</a> <a href="#content-rmarkello" title="Content">🖋</a> <a href="#ideas-rmarkello" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-rmarkello" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Armarkello" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/physiopy/phys2bids/commits?author=rmarkello" title="Tests">⚠️</a> <a href="#mentoring-rmarkello" title="Mentoring">🧑‍🏫</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/smoia"><img src="https://avatars3.githubusercontent.com/u/35300580?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Stefano Moia</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=smoia" title="Code">💻</a> <a href="#content-smoia" title="Content">🖋</a> <a href="#data-smoia" title="Data">🔣</a> <a href="#ideas-smoia" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-smoia" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#projectManagement-smoia" title="Project Management">📆</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Asmoia" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/physiopy/phys2bids/commits?author=smoia" title="Documentation">📖</a> <a href="#mentoring-smoia" title="Mentoring">🧑‍🏫</a></td>
    <td align="center"><a href="https://github.com/robertoostenveld"><img src="https://avatars1.githubusercontent.com/u/899043?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Robert Oostenveld</b></sub></a><br /><a href="#ideas-robertoostenveld" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Arobertoostenveld" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/drombas"><img src="https://avatars.githubusercontent.com/u/50577357?v=4?s=100" width="100px;" alt=""/><br /><sub><b>David Romero-Bascones</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Adrombas" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=drombas" title="Code">💻</a> <a href="https://github.com/physiopy/phys2bids/commits?author=drombas" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/tsalo"><img src="https://avatars3.githubusercontent.com/u/8228902?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Taylor Salo</b></sub></a><br /><a href="#ideas-tsalo" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/physiopy/phys2bids/commits?author=tsalo" title="Code">💻</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Atsalo" title="Reviewed Pull Requests">👀</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/RayStick"><img src="https://avatars3.githubusercontent.com/u/50215726?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Rachael Stickland</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3ARayStick" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=RayStick" title="Code">💻</a> <a href="#data-RayStick" title="Data">🔣</a> <a href="https://github.com/physiopy/phys2bids/commits?author=RayStick" title="Documentation">📖</a> <a href="#userTesting-RayStick" title="User Testing">📓</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3ARayStick" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/eurunuela"><img src="https://avatars0.githubusercontent.com/u/13706448?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Eneko Uruñuela</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/issues?q=author%3Aeurunuela" title="Bug reports">🐛</a> <a href="https://github.com/physiopy/phys2bids/commits?author=eurunuela" title="Code">💻</a> <a href="#infra-eurunuela" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/physiopy/phys2bids/pulls?q=is%3Apr+reviewed-by%3Aeurunuela" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/physiopy/phys2bids/commits?author=eurunuela" title="Tests">⚠️</a> <a href="#mentoring-eurunuela" title="Mentoring">🧑‍🏫</a></td>
    <td align="center"><a href="https://github.com/merelvdthiel"><img src="https://avatars1.githubusercontent.com/u/72999546?v=4?s=100" width="100px;" alt=""/><br /><sub><b>merelvdthiel</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=merelvdthiel" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/kristinazvolanek"><img src="https://avatars3.githubusercontent.com/u/54590158?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Kristina Zvolanek</b></sub></a><br /><a href="#data-kristinazvolanek" title="Data">🔣</a> <a href="#content-kristinazvolanek" title="Content">🖋</a> <a href="https://github.com/physiopy/phys2bids/commits?author=kristinazvolanek" title="Documentation">📖</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/marcelzwiers"><img src="https://avatars.githubusercontent.com/u/15156015?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Marcel Zwiers</b></sub></a><br /><a href="#plugin-marcelzwiers" title="Plugin/utility libraries">🔌</a></td>
    <td align="center"><a href="https://github.com/victox5"><img src="https://avatars1.githubusercontent.com/u/56017659?v=4?s=100" width="100px;" alt=""/><br /><sub><b>victox5</b></sub></a><br /><a href="https://github.com/physiopy/phys2bids/commits?author=victox5" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
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
