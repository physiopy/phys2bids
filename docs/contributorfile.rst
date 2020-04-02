.. _contributorfile:

=================================
How to contribute to ``physiopy``
=================================
Welcome to the physiopy organisation! It’s great news you’re thinking about contributing!
Working with many people from many different places is great, but sometimes this means the code can become messy due to the many different ways a contribution can be made. For this reason, we have set up some guidelines for contributions - to help you get along ASAP!
Before you start you'll need to set up a free `GitHub <https://github.com/>`_ account and sign in. Here are some `instructions <https://help.github.com/articles/signing-up-for-a-new-github-account>`_.
If you lack knowledge in python development / github use / physiological data handling, don’t be scared! Try to jump in anyway. Most of the original contributors learned these things exactly this way - jumping in and hoping to fall in the right way without breaking too many bones.
Do you want to jump in but don’t exactly know where/how? You can drop a few lines in `gitter <https://gitter.im/phys2bids/community>`_, so we can help you find something that suits you!
Already know what you're looking for in this guide? Jump to the following sections:

- `Aims of physiopy <#aims>`_
- `Join the conversation <#joinconvo>`_
- `Contributions <#contributiontypes>`_
   - `Contributing with small documentation changes <#smalldocs>`_
   - `Contributing with User testing <#usertests>`_
   - `Contributing with test files <#testfile>`_
   - `Contributing documentation through GitHub <#documenting>`_
   - `Contributing code through GitHub <#code>`_
   - `Contributing with Pull Requests Review <#reviews>`_
- `Issues and Milestones <#issuesmilestones>`_
- `Labels <#labeltypes>`_
   - `Issues labels <#issuelabel>`_
   - `PRs labels <#prlabel>`_
   - `Issues & PRs labels <#issueprlabels>`_
   - `Good First Issues <#g1i>`_
- `Contribution workflow <#workflow>`_
- `Pull Requests <#pr>`_
- `Style Guide <#styling>`_
- `Automatic Testing <#testing>`_
- `Reviewing PRs <#reviewing>`_
- `Recognizing contributors <#recognising>`_

.. _aims:

Aims of physiopy
----------------
physiopy is a **very** young project developed by a bunch of researchers from the two different sides of the Atlantic Ocean (for now).
Our main goal is to help collect, analyse and share physiological data interfacing with (MRI) neuroimaging. We’re trying to do so by:

1. Write packages to make a user-friendly pipeline to deal with physiological data.
2. Organising a documentation containing tips and strategies on how to collect such data and use our packages.
3. Write packages that take into account the use of such data in combination with neuroimaging (MRI) - by getting everything ready for that analysis.
4. Help set a standard for these data, albeit without forcing users to use it.
5. Be an excuse for educational purposes on topics like Git/GitHub, Python3, physiology and related tools/topics.

.. _joinconvo:

Joining the conversation
------------------------
We’re trying to keep all the conversation related to the project development in GitHub `issues <https://github.com/smoia/phys2bids/issues>`_.
We maintain a `gitter chat room <https://gitter.im/phys2bids/community>`_ for more informal conversations and general project updates.
We also have a dev call once a month - specifically the second Thursday of the month! If you want to participate, drop a line in gitter!
When interacting in the common channels, please adhere to our `code of conduct <conduct.html>`_.

.. _contributiontypes:

Contributions
-------------

.. _smalldocs:

Contributing with small documentation changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you are new to GitHub and just have a small documentation change recommendation (such as: typos detection, small improvements in the content, ...), please open an issue in the relative project, and label it with the “Documentation” label.
Chances are those types of changes are easily doable with the online editor, which means you can do them, or ask for help from the developers!

.. _usertests:

Contributing with User testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Another, non-coding friendly way to contribute to physiopy is by testing the packages.
There are different kinds of tests, but to simplify things you can think mainly about automatic tests and user tests.
To know more about **Automatic tests**, you can read the `testing section <#testing>`_.
**User testing** are warm, human, emotional and opinionated tests that not only check that the code is doing what it needs to do, but also whether there’s a better way to do it - namely better reports, clearer screen outputs, warnings and exceptions, unexpected bugs that have to be corrected.
If you want to perform one, open an issue on GitHub or drop a comment in Gitter, refer to this `blueprint <https://docs.google.com/document/d/1b6wc7JVDs3vi-2IqGg_Ed_oWKbZ6siboAJHf55nodKo/edit?usp=sharing>`_ and don’t be afraid to ask questions!

.. _testfile:

Contributing with test files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At physiopy we always try to imagine and support every possible setting out there. However, our imagination has a limit - but if you think our packages should process a specific format/setting that you have, we’re more than glad to do so!
To make it happen, we need an example of the file we want to process, so you will have to share it with us (and the rest of the world)! The contribution can be a full file of data that you already acquired, a part of that file (pay attention to what is the minimum you need to share!), or mock data.
The file contribution should come with a json file of the same name that contains the necessary information to run ``phys2bids`` on that file contribution. There is a `json blueprint in OSF <https://mfr.de-1.osf.io/render?url=https://osf.io/jrnxv/?direct%26mode=render%26action=download%26mode=render>`_, you can download it and adapt it. Note that the frequency list **has to be expressed in Hz** as an integer or float.
To contribute with a test file, open an Issue in GitHub and label it with *Test*. We’ll help you add the file in our 
`OSF <https://osf.io/3txqr/>`_ space.
We’re extremely grateful for this type of contribution - so grateful that we asked allcontributors to add a dedicated category!

.. _documenting:

Contributing documentation through GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We use `readthedocs <https://readthedocs.org/>`_ to create our documentation. Every contribution is welcome - and it follows the steps of a code contribution.

.. _code:

Contributing code through GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section covers 90% of the contributions a project like physiopy receives - code, documentation and tests.
The best way to make this kind of contributions, in a nutshell, would be:
1. Open an issue with the intended modifications.
2. Label it, discuss it, (self-)assign it.
3. Open a Pull Request (PR) to resolve the issue and label it.
4. Wait for a review, discuss it or comply, repeat until ready.
Issues and PR chats are great to maintain track of the conversation on the contribution. They are based upon GitHub-flavoured `Markdown <https://daringfireball.net/projects/markdown>`_. GitHub has a helpful page on `getting started with writing and formatting Markdown on GitHub <https://help.github.com/articles/getting-started-with-writing-and-formatting-on-github>`_.

.. _reviews:

Contributing with Pull Requests Reviews
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
One big challenge in this kind of software development is merging code accurately but without waiting too much time.
For this reason, Reviewers for PRs are more than welcome! It is a task that requires quite some experience, but it's very necessary!
Read the `related section below <#reviewing>`_ to start!

.. _issuesmilestones:

Issues and Milestones
---------------------
At physiopy, we use Issues and Milestones to keep track of and organise our workflow.
- **Issues** describe pieces of work that need to be completed to move the project forwards. We try to keep them as simple and clear as possible: an issue should describe a unitary, possibly small piece of work (unless it’s about refactoring). Don’t be scared of opening many issues at once, if it makes sense! Just check that what you’re proposing is not listed in a previous issue (open or closed) yet - we don’t like doubles. Issues get labelled. That helps the contributors to know what they’re about. Check the label list to know what types are there, and use them accordingly! Issues can also be **assigned**. If you want to work on an assigned issue, ask permission first!
- **Milestones** set the higher level workflow. They sketch deadlines and important releases. Issues are assigned to these milestones by the maintainers. If you feel that an issue should be assigned to a specific milestone but the maintainers have not done so, discuss it in the issue chat or in Gitter! We might have just missed it, or we might not (yet) see how it aligns with the overall project structure/milestone.

.. _labeltypes:

Labels
------
The current list of labels are `here <https://github.com/physiopy/phys2bids/labels>`_. They can be used for **Issues**, **PRs**, or both.

.. _issuelabel:

Issues labels
~~~~~~~~~~~~~
-  Bug: Something isn’t working. It either breaks the code or has an unexpected outcome.
-  Discussion: Discussion of a concept or implementation. These Issues are prone to be open ad infinitum. Jump in the conversation if you want!
-  Good first issue: Good for newcomers. These issues calls for a **fairly** easy enhancement, or for a change that helps/requires getting to know the code better. They have educational value, and for this reason, unless urgent, experts in the topic should refrain from closing them - but help newcomers closing them.
-  Hacktoberfest: Dedicated to the hacktoberfest event, so that people can help and feel good about it (and show it with a T-shirt!). **Such commits will not be recognised in the all-contributor table, unless otherwise specified**.
-  Help wanted: Extra attention is needed here! It’s a good place to have a look!
-  Refactoring: Improve nonfunctional attributes. Which means rewriting the code or the documentation to improve performance or just because there’s a better way to express those lines. It might create a ``majormod`` PR.
-  Question: Further information is requested, from users to developers. Try to respond to this!
-  Wontfix: This will not be worked on, until further notice.

.. _prlabel:

PRs labels
~~~~~~~~~~
-  BugFIX: These PRs close an issue labelled ``bug``. they also increase the semantic versioning for fixes (+0.0.1).
-  Invalid: These PRs don't seem right. They actually seem so not right that they won’t be further processed. This label invalidates an Hacktoberfest contribution. If you think this is wrong, start a discussion in the relevant issue (or open one if missing). Reviewers are asked to give an explanation for the use of this label.
-  Majormod: These PRs call for a new major release (+1.0.0). This means that the PR is breaking backward compatibility.
-  Minormod: These PRs call for a new minor release (0.+1.0). This means that the PR is **not** breaking backward compatibility.

.. _issueprlabels:

Issues & PRs labels
~~~~~~~~~~~~~~~~~~~
-  Documentation: Improvements or additions to documentation. This category includes (but is not limited to) docs pages, docstrings, and code comments.
-  Duplicate: Whatever this is, it exists already! Maybe it’s a closed Issue/PR, that should be reopened.
-  Enhancement: New features added or requested. This normally goes with a ``minormod`` label for PRs.
-  Outreach: As part of the scientific community, we care about outreach. Check the relevant section about it, but know that this Issue/PR contains information or tasks about abstracts, talks, demonstrations, papers.
-  Paused: Issue or PR should not be worked on until the resolution of other issues or PRs.
-  Testing: This is for testing features, writing tests or producing testing code. Both user testing and CI testing!
-  Urgent: If you don't know where to start, start here! This is probably related to a milestone due soon!

.. _g1i:

Good First Issues
~~~~~~~~~~~~~~~~~
Good First Issues are issues that are either very simple, or that help knowing the programs or the language better. We use it to help contributors with less experience to learn and familiarise with Git, GitHub, Python3, and physiology.
We invite more expert contributors to avoid those issues, leave them to beginners and possibly help them out in the resolution of the issue. However, if the issue is left unassigned or unattended for long, and it’s considered important or urgent, anyone can tackle it.

.. _workflow:

Contribution workflow
---------------------
There are many descriptions of a good contribution workflow out there. For instance, we suggest to have a look at `tedana's workflow <https://github.com/ME-ICA/tedana/blob/master/CONTRIBUTING.md#making-a-change>`_.
At physiopy, we follow a very similar workflow. The only two differences are:

-  We ask you to test the code locally before merging it, and then, if possible, write some automatic tests for the code to be run in our Continuous Integration! Check the testing section below to know more.
-  We suggest opening a draft PR as soon as you can - so it’s easier for us to help you!

.. _pr:

Pull Requests
-------------
To improve understanding pull requests "at a glance", we use the labels listed above. Multiple labels can be assigned, but it's a good idea to keep different types of contributions separated, unless they are minimal - for instance, you might want to open a PR for code, one for documentation and one for testing.
In general, if you're tempted to assign more than one label that would trigger a release, you might want to split your PR instead.
When opening a pull request, assign it to at least one label.

We encourage you to open a PR as soon as possible - even before you finish working on them. This is useful especially to you - so that you can receive comments and suggestions early on, rather than having to process a lot of comments in the final review step! 
However, if it’s an incomplete PR, please open a **Draft PR**. That helps us process PRs by knowing which one to have a look first - and how picky to be when doing so.

Reviewing PRs is a time consuming task, that can be stressful for both the reviewer and the author. Avoiding wasting time and the need of little fixes - such as fixing grammar mistakes and typos, styling code, or adopting conventions - is a good start for a successful (and quick) review. Before graduating a Draft PR to a PR ready for review, please check that:

- You did all you wanted to include in your PR. If at a later stage you realise something is missing and it's not minor things, you will need to open a new PR
- Your code is harmonious with the rest of the code - no repetitions of any sort!
- Your code respects the `adopted Style <#styling>`_, especially:
    - your code is lintered adequately and respects the `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ convention
    - your docstrings follow the `numpydoc <https://numpydoc.readthedocs.io/en/latest/format.html>`_ convention
    - there is no grammar mistake or typo and the text is fluid
    - the code is sufficiently commented and the comments are clear
    - your PR title is clear enough to be meaningful when appended to the version changelog
- You have the correct labels

To be merged, PRs have to:

1. Pass all the Travis CI tests.
2. Have the necessary amount of approving reviews, even if you’re a long time contributor. You can ask one (or more) contributor to do that review, if you think they align more with the content of your PR. You need **one** review for documentation, tests, and small changes, and **two** reviews for bugs, refactoring and enhancements.
3. Contain at least a unit test for your contribution, if the PR contains code (it would be better if it contains an integration or function test and all the breaking tests necessary). If you’re not confident about writing tests, it is possible to refer to an issue that asks for the test to be written, or another (Draft) PR that contains the tests required.

As we’re trying to maintain at least a 90% code coverance, you’re strongly encouraged to write all the necessary tests not to drop below the threshold. If our coverance becomes too low, you might be asked to add more tests and/or your PR might be rejected.

Remember that the project manager doesn't have to be a reviewer of your PR! 

.. _styling:

Style Guide
-----------
Docstrings should follow `numpydoc <https://numpydoc.readthedocs.io/en/latest/format.html>`_ convention. We encourage extensive documentation.
The python code itself should follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ convention whenever possible: there are continuous integration tests checking that!
You can use linters to help you write your code following style conventions. Linters are add-ons that you can run on the written script file. We suggest the use of **flake8** for Python 3. Many editors (Atoms, VScode, Sublimetext, ...) support addons for online lintering, which means you’ll see warnings and errors while you write the code - check out if your does!
Since we adopt `auto <https://intuit.github.io/auto/home.html>`_, the PR title will be automatically reported as part of the changelog when updating versions. Try to describe in one (short) sentence what your PR is about - possibly using the imperative and starting with a capital letter. For instance, a good PR title could be: ``Implement support for <randomtype> files`` or ``Reorder dictionary entries``, rather than ``<randomtype> support`` or ``reorders keys``.

.. _testing:

Automatic Testing
-----------------
physiopy uses Continuous Integration (CI) to make life easier. In particular, we use the `Travis CI <https://travis-ci.org/>`_ platform to run automatic testing!
**Automatic tests** are cold, robotic, emotionless, and opinionless tests that check that the program is doing what it is expected to. They are written by the developers and run (by Travis CI) every time they send a Pull Request to physiopy repositories. They complement the warm, human, emotional and opinionated **user tests**, as they tell us if a piece of code is failing.
Travis CI uses `pytest <https://docs.pytest.org/en/latest/>`_ to run the tests. The great thing about it is that you can run it in advance on your local version of the code!
We can measure the amount of code that is tested with [codecov]8https://docs.pytest.org/en/latest/), which is an indication of how reliable our packages are! We try to maintain a 90% code coverage, and for this reason, PR should contain tests!
The four main type of tests we use are:

1. Unit tests
    Unit tests check that a minimal piece of code is doing what it should be doing. Normally this means calling a function with some mock parameters and checking that the output is equal to the expected output. For example, to test a function that adds two given numbers together (1 and 3), we would call the function with those parameters, and check that the output is 4.
2. Breaking tests
    Breaking tests are what you expect - they check that the program is breaking when it should. This means calling a function with parameters that are expected **not** to work, and check that it raises a proper error or warning.
3. Integration tests
    Integration tests check that the code has an expected output, being blind to its content. This means that if the program should output a new file, the file exists - even if it’s empty. This type of tests are normally run on real data and call the program itself. For instance, documentation PRs should check that the documentation page is produced!
4. Functional tests
    If integration tests and unit tests could have babies, those would be functional tests. In practice, this kind of tests check that an output is produced, and *also* that it contains what it should contain. If a function should output a new file or an object, this test passes only if the file exists *and* it is like we expect it to be. They are run on real or mock data, and call the program itself or a function.

.. _reviewing:

Reviewing PRs
-------------
Reviewing PRs is an extremely important task in collaborative development. In fact, it is probably the task that requires the most time in the development, and it can be stressful for both the reviewer and the author. Remember that, as a PR Reviewer, you are granting that the codes works and integrates well with the rest of the repository, hence **you are responsible for the quality of the code and its next version release**. If it doesn't, later PR reviewers might have to ask for broader changes than expected.
Due to its importance, there are some good rules of thumbs that we need to follow while reviewing PRs:

- Be respectful to the PR authors - remember that, like you, they are contributing their spare time and doing their best job!
- If there is a Draft PR, you can comment its development in the message board or making "Comment" reviews. Don't ask for changes, and especially, **don't approve the PR**
- If the PR graduated from Draft to full PR, check that it follows the sections `Pull requests <#pr>`_ and `Style Guide <#styling>`_ of these guidelines. If not, invite the author to do so before starting a review.
- Be clear in what you're asking or suggesting.
- **Don't limit your review to the parts that are changed**. Look at the entire file, see if the changes fit well in it, and see if the changes are properly addressed everywhere in the code - in the documentation, in the tests, and in other functions. Sometimes the differences reported don't show enough surroundings!
- Unless it's for typo fixes or similar, invite the author of the PR to make changes before actually doing them yourself.
- If you're asking for changes, **don't approve the PR**. Approve it only after everything was sufficiently addressed. Someone else might merge the PR in taking your word for granted.
- If you're the last reviewer required to approve the PR and there is no review taking place, merge it!

Before approving and/or merging PRs, be sure that:

- all the tests in Travis CI pass without errors
- prefereably, codecov checks pass as well - if they don't, pin the project manager. 
- the title describes the content of the PR clearly enough to be meaningful on its own - remember that it will appear in the version changelog!
- the PR has the appropriate labels to trigger the appropriate version release and update the contributors table.

Remember that the project manager doesn't have to be a reviewer of the PR.

.. _recognising:

Recognising contributors
------------------------
We welcome and recognize `all contributions <https://allcontributors.org/docs/en/specification>`_ from documentation to testing to code development. You can see a list of current contributors in the README (kept up to date by the `all contributors bot <https://allcontributors.org/docs/en/bot/overview>`_).

**Thank you!**

*— Based on contributing guidelines from the `STEMMRoleModels <https://github.com/KirstieJane/STEMMRoleModels>`_ project.* 
