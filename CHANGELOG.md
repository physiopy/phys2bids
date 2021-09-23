# 2.6.0 (Fri Jun 18 2021)

:tada: This release contains work from a new contributor! :tada:

Thank you, Marcel Zwiers ([@marcelzwiers](https://github.com/marcelzwiers)), for all your work!

#### 🚀 Enhancement

- Define previously unspecified Exceptions in the main workflow [#406](https://github.com/physiopy/phys2bids/pull/406) ([@marcelzwiers](https://github.com/marcelzwiers))

#### 📝 Documentation

- Fix bug that would impede building the docs [#399](https://github.com/physiopy/phys2bids/pull/399) ([@eurunuela](https://github.com/eurunuela))

#### Authors: 2

- Eneko Uruñuela ([@eurunuela](https://github.com/eurunuela))
- Marcel Zwiers ([@marcelzwiers](https://github.com/marcelzwiers))

---

# 2.5.0 (Wed May 12 2021)

#### 🚀 Enhancement

- Add additional automatic detection of the trigger based on time-domain analysis [#391](https://github.com/physiopy/phys2bids/pull/391) ([@drombas](https://github.com/drombas))

#### 🏠 Internal

- Upgrade to GitHub-native Dependabot [#395](https://github.com/physiopy/phys2bids/pull/395) ([@dependabot-preview[bot]](https://github.com/dependabot-preview[bot]))

#### Authors: 2

- [@dependabot-preview[bot]](https://github.com/dependabot-preview[bot])
- David Romero-Bascones ([@drombas](https://github.com/drombas))

---

# 2.4.1 (Sun Apr 11 2021)

:tada: This release contains work from a new contributor! :tada:

Thank you, David Romero-Bascones ([@drombas](https://github.com/drombas)), for all your work!

#### 🐛 Bug Fix

- correct chtrig check in phys2bids main workflow [#390](https://github.com/physiopy/phys2bids/pull/390) ([@drombas](https://github.com/drombas))

#### 📝 Documentation

- Clarify installation instructions and tutorial [#382](https://github.com/physiopy/phys2bids/pull/382) ([@drombas](https://github.com/drombas))

#### 🏠 Internal

- Provide the outcome of integration and documentation tests as downloadable artifacts from each Cirrus CI test page [#384](https://github.com/physiopy/phys2bids/pull/384) ([@vinferrer](https://github.com/vinferrer))

#### Authors: 2

- David Romero-Bascones ([@drombas](https://github.com/drombas))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))

---

# 2.4.0 (Wed Feb 17 2021)

#### 🚀 Enhancement

- Auto-detect the trigger channel based on retrieved channel names [#306](https://github.com/physiopy/phys2bids/pull/306) ([@vinferrer](https://github.com/vinferrer) [@smoia](https://github.com/smoia))

#### 🏠 Internal

- Testing: Use only a Windows miniconda image instead of different images for each python version [#381](https://github.com/physiopy/phys2bids/pull/381) ([@vinferrer](https://github.com/vinferrer))

#### Authors: 2

- Stefano Moia ([@smoia](https://github.com/smoia))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))

---

# 2.3.3 (Thu Jan 21 2021)

:tada: This release contains work from a new contributor! :tada:

Thank you, Yaroslav Halchenko ([@yarikoptic](https://github.com/yarikoptic)), for all your work!

#### 🐛 Bug Fix

- Stop using powershell as windows interpreter [#379](https://github.com/physiopy/phys2bids/pull/379) ([@vinferrer](https://github.com/vinferrer))
- Update contributions and remove auto all-contribution plugin [#372](https://github.com/physiopy/phys2bids/pull/372) ([@smoia](https://github.com/smoia))
- Replace utils.check_input_dir() with os.path.abspath() [#368](https://github.com/physiopy/phys2bids/pull/368) ([@vinferrer](https://github.com/vinferrer))

#### ⚠️ Tests

- Add windows CI testing [#366](https://github.com/physiopy/phys2bids/pull/366) ([@vinferrer](https://github.com/vinferrer))
- Correct BIDS validation test names [#365](https://github.com/physiopy/phys2bids/pull/365) ([@vinferrer](https://github.com/vinferrer))

#### 🏠 Internal

- Add .mailmap to improve `git shortlog -sn` output [#378](https://github.com/physiopy/phys2bids/pull/378) ([@yarikoptic](https://github.com/yarikoptic))
- Migrate testing to Cirrus CI [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- create coverage folder only in the makeenv [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add the coverage folder to the shared folder [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- have a common folder with subfolders [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add the coverage folder [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add integration tests [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- do not pip in unittest_37 [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- name task properly [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- use as fingerprint_script [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add coverage [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- don't use makeenv [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- cache name [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- cache enviroment folder [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- use full path in source [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- remove name option [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- save enviroment in working dir [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add source command [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- create conda enviroment [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add sudo comand [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add python 3.7 tests [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- use default WD [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- use 3.7 from miniconda [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- use slim version [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- retry python version [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- change to python 3.7 container [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- change task name and checkout python version [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- check working dir [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- get default phys2bids install path [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- clone done automatically [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- try witout folder command [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add ident [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- put folder in the end so it's created [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- set up working dir and save phys2bids folder for cache [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- delete some identation [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- rename /tmp/src/phys2bids folder to phys2bids [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- eliminate env_script line [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- use name field [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- adding cirrus CI with basic enviroment [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- Merge branch 'master' of https://github.com/physiopy/phys2bids [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- delete test [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))
- add windows docker trial tests [#375](https://github.com/physiopy/phys2bids/pull/375) ([@vinferrer](https://github.com/vinferrer))

#### Authors: 3

- Stefano Moia ([@smoia](https://github.com/smoia))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))
- Yaroslav Halchenko ([@yarikoptic](https://github.com/yarikoptic))

---

# 2.3.2 (Wed Dec 09 2020)

#### 🐛 Bug Fix

- Add 0 before run number to multi-run trigger plot file name [#369](https://github.com/physiopy/phys2bids/pull/369) ([@vinferrer](https://github.com/vinferrer))

#### ⚠️ Tests

- Add test to check that `phys2bids` output is BIDS compatible [#362](https://github.com/physiopy/phys2bids/pull/362) ([@vinferrer](https://github.com/vinferrer))
- Fix call to conda environment reference in the test configuration file [#363](https://github.com/physiopy/phys2bids/pull/363) ([@eurunuela](https://github.com/eurunuela))

#### Authors: 2

- Eneko Uruñuela ([@eurunuela](https://github.com/eurunuela))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))

---

# 2.3.1 (Mon Nov 30 2020)

#### 🐛 Bug Fix

- BlueprintInput deepcopies inputs at initialization [#358](https://github.com/physiopy/phys2bids/pull/358) ([@vinferrer](https://github.com/vinferrer))

#### Authors: 1

- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))

---

# 2.3.0 (Sun Nov 29 2020)

:tada: This release contains work from new contributors! :tada:

Thanks for all your work!

:heart: null[@merelvdthiel](https://github.com/merelvdthiel)

:heart: Inés Chavarría ([@ineschh](https://github.com/ineschh))

:heart: Vittorio Iacovella ([@viacovella](https://github.com/viacovella))

:heart: null[@victox5](https://github.com/victox5)

#### 🚀 Enhancement

- Add support for MATLAB files [#360](https://github.com/physiopy/phys2bids/pull/360) ([@vinferrer](https://github.com/vinferrer))

#### 🐛 Bug Fix

- Refactor `io` functions related to txt file imports. [#349](https://github.com/physiopy/phys2bids/pull/349) ([@vinferrer](https://github.com/vinferrer))
- Refactor phys2bids interfaces into single script `io.py` [#344](https://github.com/physiopy/phys2bids/pull/344) ([@vinferrer](https://github.com/vinferrer))
- Rename `utils.writejson()` to `utils.write_json()` to respect style conventions [#346](https://github.com/physiopy/phys2bids/pull/346) ([@merelvdthiel](https://github.com/merelvdthiel))
- Replace custom function `utils.path_exists_or_make_it()` with core function `os.makedirs()` [#345](https://github.com/physiopy/phys2bids/pull/345) ([@merelvdthiel](https://github.com/merelvdthiel))
- Rename function `utils.writefile` to `utils.write_file` to respect style conventions [#343](https://github.com/physiopy/phys2bids/pull/343) ([@ineschh](https://github.com/ineschh))
- Remove `utils.move_file()` function as it is no longer used in the toolbox [#342](https://github.com/physiopy/phys2bids/pull/342) ([@viacovella](https://github.com/viacovella))
- Updated versions required [#7](https://github.com/physiopy/phys2bids/pull/7) (vic188m@hotmail.com [@victox5](https://github.com/victox5))

#### ⚠️ Pushed to `master`

- Update README.md ([@smoia](https://github.com/smoia))

#### 📝 Documentation

- Add documentation for reviewers and a checklist for PRs [#315](https://github.com/physiopy/phys2bids/pull/315) ([@smoia](https://github.com/smoia) [@RayStick](https://github.com/RayStick))
- Add Windows installation to the documentation [#329](https://github.com/physiopy/phys2bids/pull/329) ([@vinferrer](https://github.com/vinferrer) [@smoia](https://github.com/smoia))
- Update tutorial with latest CLI options and new folder organisation (`output/code/conversion`) [#320](https://github.com/physiopy/phys2bids/pull/320) ([@vinferrer](https://github.com/vinferrer) [@RayStick](https://github.com/RayStick))

#### ⚠️ Tests

- Fix typo in artifact_path [#331](https://github.com/physiopy/phys2bids/pull/331) ([@tsalo](https://github.com/tsalo))

#### 🏠 Internal

- Add more "change type" options [#347](https://github.com/physiopy/phys2bids/pull/347) ([@smoia](https://github.com/smoia))

#### Authors: 9

- [@merelvdthiel](https://github.com/merelvdthiel)
- [@victox5](https://github.com/victox5)
- Inés Chavarría ([@ineschh](https://github.com/ineschh))
- Rachael Stickland ([@RayStick](https://github.com/RayStick))
- Stefano Moia ([@smoia](https://github.com/smoia))
- Taylor Salo ([@tsalo](https://github.com/tsalo))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))
- Victor (vic188m@hotmail.com)
- Vittorio Iacovella ([@viacovella](https://github.com/viacovella))

---

# 2.2.3 (Fri Oct 23 2020)

#### 🐛 Bug Fix

- Update PyYAML minimal requirements to avoid "FullLoader" attribute errors. [#330](https://github.com/physiopy/phys2bids/pull/330) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 2.2.2 (Mon Oct 19 2020)

#### 🐛 Bug Fix

- Fix auto release workflow settings [#323](https://github.com/physiopy/phys2bids/pull/323) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 2.2.1 (Mon Oct 19 2020)

#### 🐛 Bug Fix

- Make sure we delete testing files after finishing tests [#307](https://github.com/physiopy/phys2bids/pull/307) ([@vinferrer](https://github.com/vinferrer))
- Add label colours to set auto labels [#318](https://github.com/physiopy/phys2bids/pull/318) ([@smoia](https://github.com/smoia))
- Reduce `auto` verbosity [#317](https://github.com/physiopy/phys2bids/pull/317) ([@smoia](https://github.com/smoia))

#### 📝 Documentation

- Update badges in README and documentation [#322](https://github.com/physiopy/phys2bids/pull/322) ([@smoia](https://github.com/smoia))
- Update zenodo info [#321](https://github.com/physiopy/phys2bids/pull/321) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- Setup auto release workflow [#313](https://github.com/physiopy/phys2bids/pull/313) ([@smoia](https://github.com/smoia))

#### Authors: 2

- Stefano Moia ([@smoia](https://github.com/smoia))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))

---

# v2.2.0 (Wed Oct 14 2020)

#### 🚀 Enhancement

- Make trigger-based time-offset correction more generalisable (resample time before comparing it to trigger) [#308](https://github.com/physiopy/phys2bids/pull/308) (s.moia@bcbl.eu)
- Format logger to make terminal (stdout) more human readable [#312](https://github.com/physiopy/phys2bids/pull/312) ([@vinferrer](https://github.com/vinferrer))
- Add (resampled) trigger to all output files [#288](https://github.com/physiopy/phys2bids/pull/288) ([@vinferrer](https://github.com/vinferrer))

#### 🐛 Bug Fix

- Skip CI on all-contributors (s.moia@bcbl.eu)
- Explicitly ignore rc files and github folder (s.moia@bcbl.eu)
- Add autorc (s.moia@bcbl.eu)
- Add auto badge to documentation (s.moia@bcbl.eu)
- Add auto badge (s.moia@bcbl.eu)
- Add workflow for auto publishing (s.moia@bcbl.eu)
- Change build shield from Travis to CircleCI [#297](https://github.com/physiopy/phys2bids/pull/297) ([@eurunuela](https://github.com/eurunuela))
- Fix linting errors [#294](https://github.com/physiopy/phys2bids/pull/294) ([@eurunuela](https://github.com/eurunuela))
- Start of sampling time is now the same for all frequencies [#283](https://github.com/physiopy/phys2bids/pull/283) ([@vinferrer](https://github.com/vinferrer))
- Add travis wait command [#284](https://github.com/physiopy/phys2bids/pull/284) ([@eurunuela](https://github.com/eurunuela))
- Correct trigger channel indexing while reading AcqKnowledge files. [#275](https://github.com/physiopy/phys2bids/pull/275) (s.moia@bcbl.eu)

#### ⚠️ Pushed to `master`

- Merge branch 'int/auto' (s.moia@bcbl.eu)
- Update README.md (s.moia@bcbl.eu)
- Update ISSUE_TEMPLATE_MEETING.md (s.moia@bcbl.eu)
- Fix message shown when skipping integration test ([@eurunuela](https://github.com/eurunuela))
- Update .travis.yml ([@eurunuela](https://github.com/eurunuela))
- Update setup.cfg ([@eurunuela](https://github.com/eurunuela))

#### 📝 Documentation

- Update all-contributors [#310](https://github.com/physiopy/phys2bids/pull/310) (s.moia@bcbl.eu)
- Update documentation to reflect change from Travis CI to CircleCI [#290](https://github.com/physiopy/phys2bids/pull/290) ([@eurunuela](https://github.com/eurunuela))

#### ⚠️ Tests

- Add tests for exceptions [#291](https://github.com/physiopy/phys2bids/pull/291) ([@eurunuela](https://github.com/eurunuela))
- Add CircleCI for automatic testing and correct integration test parameters [#286](https://github.com/physiopy/phys2bids/pull/286) ([@eurunuela](https://github.com/eurunuela))
- Switch from Travis to CircleCI for automatic testing [#285](https://github.com/physiopy/phys2bids/pull/285) ([@eurunuela](https://github.com/eurunuela))
- Add integration test for the multi run pipeline [#266](https://github.com/physiopy/phys2bids/pull/266) ([@eurunuela](https://github.com/eurunuela))

#### 🏠 Internal

- Refactor txt.py chtrig parameter to improve code readability [#305](https://github.com/physiopy/phys2bids/pull/305) ([@vinferrer](https://github.com/vinferrer))

#### 🖋️  Outreach

- Add link to Google Calendar [#302](https://github.com/physiopy/phys2bids/pull/302) ([@eurunuela](https://github.com/eurunuela))

#### Authors: 3

- Eneko Uruñuela ([@eurunuela](https://github.com/eurunuela))
- Stefano Moia ([@smoia](https://github.com/smoia))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))

---

# v2.1.0 (Tue Jun 23 2020)

:tada: This release contains work from new contributors! :tada:

Thanks for all your work!

:heart: Taylor Salo ([@tsalo](https://github.com/tsalo))

:heart: François Lespinasse ([@sangfrois](https://github.com/sangfrois))

#### 🚀 Enhancement

- Add the possibility to split multi-run physiological recordings [#206](https://github.com/physiopy/phys2bids/pull/206) ([@sangfrois](https://github.com/sangfrois) [@smoia](https://github.com/smoia) [@rmarkello](https://github.com/rmarkello))
- Create folder code/conversion to store trigger and channel plots, yaml and heuristic files and the call.sh file [#256](https://github.com/physiopy/phys2bids/pull/256) ([@vinferrer](https://github.com/vinferrer) [@eurunuela](https://github.com/eurunuela))
- Add duecredit to handle citations [#249](https://github.com/physiopy/phys2bids/pull/249) ([@tsalo](https://github.com/tsalo) [@smoia](https://github.com/smoia))
- Generate dataset_description.json and README.md when they do not exist and update the json file when the subject is missing [#255](https://github.com/physiopy/phys2bids/pull/255) ([@vinferrer](https://github.com/vinferrer))
- Create bids_ignore directory and redirect channels plot, trigger plot, logger output and subject log file to this directory [#245](https://github.com/physiopy/phys2bids/pull/245) ([@vinferrer](https://github.com/vinferrer) [@smoia](https://github.com/smoia))
- Generate participants.tsv if it doesn't exist or update it if subject is missing in the file [#244](https://github.com/physiopy/phys2bids/pull/244) ([@eurunuela](https://github.com/eurunuela))

#### 🐛 Bug Fix

- Auto [#236](https://github.com/physiopy/phys2bids/pull/236) ([@smoia](https://github.com/smoia))
- Check branch in travisCI [#235](https://github.com/physiopy/phys2bids/pull/235) ([@smoia](https://github.com/smoia))

#### ⚠️ Tests

- Change os path import and linter [#260](https://github.com/physiopy/phys2bids/pull/260) ([@smoia](https://github.com/smoia))
- Remove redundant integration tests [#259](https://github.com/physiopy/phys2bids/pull/259) ([@eurunuela](https://github.com/eurunuela))
- Add unit tests for participants_file and append_list_as_row [#254](https://github.com/physiopy/phys2bids/pull/254) ([@sangfrois](https://github.com/sangfrois) [@eurunuela](https://github.com/eurunuela))
- Update testing to use short files. [#241](https://github.com/physiopy/phys2bids/pull/241) ([@eurunuela](https://github.com/eurunuela))

#### 🏠 Internal

- Add zenodo default to improve automatic release tracking [#261](https://github.com/physiopy/phys2bids/pull/261) ([@smoia](https://github.com/smoia))

#### Authors: 9

- Eneko Uruñuela ([@eurunuela](https://github.com/eurunuela))
- François Lespinasse ([@sangfrois](https://github.com/sangfrois))
- Rachael Stickland ([@RayStick](https://github.com/RayStick))
- Ross Markello ([@rmarkello](https://github.com/rmarkello))
- Stefano Moia ([@smoia](https://github.com/smoia))
- Taylor Salo ([@tsalo](https://github.com/tsalo))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))

---

# v2.0.0 (Mon Jun 15 2020)

:tada: This release contains work from a new contributor! :tada:

Thank you, Molly Bright ([@BrightMG](https://github.com/BrightMG)), for all your work!

#### 💥 Breaking Change

- Make heuristics a simple set of "if .. elif .. else" statements and use a dictionary instead of variables. [#209](https://github.com/physiopy/phys2bids/pull/209) ([@smoia](https://github.com/smoia))

#### 🚀 Enhancement

- Add BIDS-compatible automatic reformatting of units of measure [#222](https://github.com/physiopy/phys2bids/pull/222) ([@vinferrer](https://github.com/vinferrer) [@smoia](https://github.com/smoia) [@eurunuela](https://github.com/eurunuela))
- Add `getitem` and `eq` methods to BlueprintInput for easier slicing and comparing [#213](https://github.com/physiopy/phys2bids/pull/213) ([@smoia](https://github.com/smoia))
- Improve code compliance to BIDS in BlueprintOputput [#189](https://github.com/physiopy/phys2bids/pull/189) ([@smoia](https://github.com/smoia))

#### 🐛 Bug Fix

- Auto [#236](https://github.com/physiopy/phys2bids/pull/236) ([@smoia](https://github.com/smoia))
- Check branch in travisCI [#235](https://github.com/physiopy/phys2bids/pull/235) ([@smoia](https://github.com/smoia))
- Print float to max 4 decimal places [#212](https://github.com/physiopy/phys2bids/pull/212) ([@RayStick](https://github.com/RayStick))
- Enh/bids units [#224](https://github.com/physiopy/phys2bids/pull/224) ([@smoia](https://github.com/smoia))
- Add issue templates [#220](https://github.com/physiopy/phys2bids/pull/220) ([@smoia](https://github.com/smoia))

#### ⚠️ Pushed to `master`

- Update ISSUE_TEMPLATE_MEETING.md ([@smoia](https://github.com/smoia))
- Update badges ([@smoia](https://github.com/smoia))
- Invert Cesar & Vicente, reorganise badges ([@smoia](https://github.com/smoia))
- Update heuristic.rst ([@smoia](https://github.com/smoia))
- Add heuristic link ([@smoia](https://github.com/smoia))
- Update card link ([@smoia](https://github.com/smoia))
- Add card and mattermost channel for BrainWeb ([@smoia](https://github.com/smoia))
- Add card for BrainWeb ([@smoia](https://github.com/smoia))
- Updates for the BrainWeb ([@smoia](https://github.com/smoia))
- Triggger Travis CI ([@smoia](https://github.com/smoia))

#### 📝 Documentation

- Add guidelines for PR reviews. [#197](https://github.com/physiopy/phys2bids/pull/197) ([@smoia](https://github.com/smoia) [@RayStick](https://github.com/RayStick))
- Update reference API [#231](https://github.com/physiopy/phys2bids/pull/231) ([@rmarkello](https://github.com/rmarkello))
- Add "Why BIDS?" page to the documentation [#229](https://github.com/physiopy/phys2bids/pull/229) ([@rmarkello](https://github.com/rmarkello))
- Create LICENSE [#3](https://github.com/physiopy/phys2bids/pull/3) ([@smoia](https://github.com/smoia))
- Fix typos on "Best Practices for Phys Data Collection" [#200](https://github.com/physiopy/phys2bids/pull/200) ([@kristinazvolanek](https://github.com/kristinazvolanek))
- Fix formatting on "Best Practices for Phys Data Collection" [#198](https://github.com/physiopy/phys2bids/pull/198) ([@kristinazvolanek](https://github.com/kristinazvolanek))
- Update trigger detection tutorial [#191](https://github.com/physiopy/phys2bids/pull/191) ([@vinferrer](https://github.com/vinferrer) [@RayStick](https://github.com/RayStick) [@smoia](https://github.com/smoia))
- Add section on "Best Practices for Phys Data Collection" [#177](https://github.com/physiopy/phys2bids/pull/177) ([@AyyagariA](https://github.com/AyyagariA) [@BrightMG](https://github.com/BrightMG))
- Update viz.py docstrings and Inputs [#193](https://github.com/physiopy/phys2bids/pull/193) ([@vinferrer](https://github.com/vinferrer))
- Create README.md [#4](https://github.com/physiopy/phys2bids/pull/4) ([@smoia](https://github.com/smoia))

#### ⚠️ Tests

- Fix azure pipelines non-failure bug [#223](https://github.com/physiopy/phys2bids/pull/223) ([@rmarkello](https://github.com/rmarkello))
- Add Azure Pipelines for Windows CI testing [#208](https://github.com/physiopy/phys2bids/pull/208) ([@rmarkello](https://github.com/rmarkello))

#### 🏠 Internal

- Add required token for Travis to run auto [#240](https://github.com/physiopy/phys2bids/pull/240) ([@smoia](https://github.com/smoia))
- Fix Travis CI environment for auto [#238](https://github.com/physiopy/phys2bids/pull/238) ([@smoia](https://github.com/smoia))
- Fix TravisCI configuration for auto [#237](https://github.com/physiopy/phys2bids/pull/237) ([@smoia](https://github.com/smoia))
- Implement automatic release [#181](https://github.com/physiopy/phys2bids/pull/181) ([@smoia](https://github.com/smoia))
- Move bids-related functions to dedicated file [#234](https://github.com/physiopy/phys2bids/pull/234) ([@smoia](https://github.com/smoia))
- Remove bioread form required dependencies, ease extra modules installation [#214](https://github.com/physiopy/phys2bids/pull/214) ([@smoia](https://github.com/smoia) [@RayStick](https://github.com/RayStick))
- Reordering of import statements in the entire phys2bids project [#195](https://github.com/physiopy/phys2bids/pull/195) ([@eurunuela](https://github.com/eurunuela))

#### Authors: 8

- Apoorva Ayyagari ([@AyyagariA](https://github.com/AyyagariA))
- Eneko Uruñuela ([@eurunuela](https://github.com/eurunuela))
- Kristina Zvolanek ([@kristinazvolanek](https://github.com/kristinazvolanek))
- Molly Bright ([@BrightMG](https://github.com/BrightMG))
- Rachael Stickland ([@RayStick](https://github.com/RayStick))
- Ross Markello ([@rmarkello](https://github.com/rmarkello))
- Stefano Moia ([@smoia](https://github.com/smoia))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))
