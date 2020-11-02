# 2.2.4 (Mon Nov 02 2020)

:tada: This release contains work from a new contributor! :tada:

Thank you, null[@victox5](https://github.com/victox5), for all your work!

#### 🐛 Bug Fix

- Updated versions required [#7](https://github.com/physiopy/phys2bids/pull/7) (vic188m@hotmail.com [@victox5](https://github.com/victox5))

#### ⚠️ Pushed to `master`

- Update README.md ([@smoia](https://github.com/smoia))

#### 📝 Documentation

- Add Windows installation to the documentation [#329](https://github.com/physiopy/phys2bids/pull/329) ([@vinferrer](https://github.com/vinferrer) [@smoia](https://github.com/smoia))
- Update tutorial with latest CLI options and new folder organisation (`output/code/conversion`) [#320](https://github.com/physiopy/phys2bids/pull/320) ([@vinferrer](https://github.com/vinferrer) [@RayStick](https://github.com/RayStick))

#### ⚠️ Tests

- Fix typo in artifact_path [#331](https://github.com/physiopy/phys2bids/pull/331) ([@tsalo](https://github.com/tsalo))

#### Authors: 6

- [@victox5](https://github.com/victox5)
- Rachael Stickland ([@RayStick](https://github.com/RayStick))
- Stefano Moia ([@smoia](https://github.com/smoia))
- Taylor Salo ([@tsalo](https://github.com/tsalo))
- Vicente Ferrer ([@vinferrer](https://github.com/vinferrer))
- Victor (vic188m@hotmail.com)

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
