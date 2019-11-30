[![Join the chat at https://gitter.im/ME-ICA/tedana](https://badges.gitter.im/phys2bids/community.svg)](https://gitter.im/phys2bids/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3557379.svg)](https://doi.org/10.5281/zenodo.3557379)

phys2bids

=========
Phys2bids is a python3 library meant to format physiological files in BIDS.
It was born for Acqknowledge files (BIOPAC), and at the moment it supports
``.acq`` files as well as ``.txt`` files obtained by labchart
(ADInstruments).
It doesn't support physiological files recorded with the MRI, as you can find a software for it [here](https://github.com/tarrlab/physio2bids).

It requires python 3.6 or above, as well as the modules:

- `numpy >= 1.9.3`
- `pandas >= 0.10`
- `matplotlib >= 3.1.1`

In order to process ``.acq`` files, it needs [`bioread`](https://github.com/uwmadison-chm/bioread), an excellent module
that can be found at [this link](https://github.com/uwmadison-chm/bioread).

### Linux and mac installation

Donwload the package as zip from github and uncompress or if you have ``git`` use the command:

``git clone https://github.com/smoia/phys2bids.git``

open a terminal in the phy2bids folder and execute the command:

``sudo pip3 install -e .``

type the command:

``phys2bids -v``

if your output is: ``phys2bids 0.4.0`` or similar, phys2bids is ready to be used.

**The project is currently under development**.
Any suggestion/bug report is welcome! Feel free to open an issue.

At the very moment, it assumes all the extracted channels from a file
have the same sampling freq.

License

---

_Copyright 2019, The Phys2BIDS community._

_Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at_

_http://www.apache.org/licenses/LICENSE-2.0_

_Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License._

### Use and contribute to `phys2bids` as a developer

If you aim to contribute to the `phys2bids` code base and/or documentation, please first read the developer installation instructions in [our contributing section](https://github.com/smoia/phys2bids/blob/master/CONTRIBUTING.md). You can then continue to set up your preferred development environment.

### Getting involved

We :yellow_heart: new contributors!
To get started, check out [our contributing guidelines](https://github.com/smoia/phys2bids/blob/master/CONTRIBUTING.md).

Want to learn more about our plans for developing ``phys2bids``?
Have a question, comment, or suggestion?
Open or comment on one of [our issues](https://github.com/smoia/phys2bids/issues)!

If you're not sure where to begin, feel free to pop into [Gitter](https://gitter.im/phys2bids) and introduce yourself!
We will be happy to help you find somewhere to get started.

<!-- We ask that all contributors to ``phys2bids`` across all project-related spaces (including but not limited to: GitHub, Gitter, and project emails), adhere to our [code of conduct](https://github.com/ME-ICA/tedana/blob/master/CODE_OF_CONDUCT.md). -->

<!-- ### Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)): -->