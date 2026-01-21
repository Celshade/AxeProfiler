# AxeProfiler

[![GNU GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/Celshade/AxeProfiler/blob/develop/COPYING)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3-green.svg)](https://www.python.org/)


_AxeProfiler provides a convenient CLI to create/save/apply AxeOS miner configs._

Navigate through a clean and simple CLI to create, save, and then apply various
AxeOS configurations - all from your keyboard. No more tedious clicking through
every device dashboard!
![](demo.gif)

## Requirements
* [python](https://www.python.org/downloads/) >= 3.11
  * requests >= 2.32.5
  * rich >= 14.2.0
  * [optional] pytest >= 9.0.2 (only used when running the test suite - see
  **Testing** section below)

  _The non-optional python libraries are installed automatically during_
  _installation_

## Installation
### [The Way of the Plebb]
**@Mac** | **@Windows** \
Download the appropriate executable from [here](https://github.com/Celshade/AxeProfiler/releases/tag/v1.1.1),
and you should be able to simply double click and run the file to start the
program - or you can call the executable directly from the terminal. See
**NOTES** below.

**@Linux** \
If you're already running Linux, please follow one of the methods found in
_The Way of the Dev_ outlined below. An executable may be added in the future;
however, it's prefable to build from source or simply use python/pip to install
from PYPI.

**NOTES** \
The Windows' executable was generated for Windows 10/11 - support for older OS
is not guaranteed.

The MAC executables are simply UNIX executable files. There is no specific file
extension - _they are **Terminal** apps_, and running them is simply a matter of
retaining (or allowing) the proper file permissions that your system needs to
execute them. Look for the option that says _"Open with Terminal_."

Executables were created via the Python library [pyinstaller](https://pypi.org/project/pyinstaller/)
by running the following command on each respective OS:
```
pyinstaller --onefile src/axeprofiler/__main__.py` (from source root)
```
_This is NOT an installation step - it is only being shared in the spirit of_
_transparency, given the nature of executables. If you don't feel comfortable_
_running them, you are more than welcome to follow **The Way of the Dev**_
_outlined below._

### [The Way of the Dev]
Clone the repo and run `pip install -e .` from the project root directory. This
should install all dependencies and add the `axeprof` command to PATH - allowing
you to call the program from anywhere with that pip environment active.
```
(venv) <axeprofiler_directory>$ pip install -e .
(venv) $ axeprof
```

You can also install the package from PYPI
```
(venv) $ python -m pip install axeprofiler
(venv) $ axeprof
```
Once installed, you may also start the program from inside a python REPL by
importing the entry-point function.
```
>>> # inside python REPL
>>> from axeprofiler.__main__ import main
>>> main()
```

## Testing
_Only available to those cloning from source. The executables will not have_
_access to the `tests` directory_

Requires:
* pytest >= 9.0.2
  - installed via `pip`
    ```
    (venv) $ pip install pytest
    ```

From the project directory, simply call `pytest ./tests` to run all available
tests, or run the `pytest` command and point to a specific test file.

i.e. (showing both options mentioned above)
```
(venv) $ pytest ./tests
(venv) $ pytest ./tests/test_list.py
```

## Notes
* This project is still in active development, and it's possible a few hidden
bugs linger (though, they are actively hunted down).
* While there are confirmation prompts, please do your due diligence to know
which device (IP) you are applying a profile to.
* Deleting a [selected] profile does not remove the configuration from an active
miner running it.

---
_While not expected, any tips/donations [in bitcoin] are greatly appreciated_
_and go a long way in supporting me and my future contributions to this_
_codebase and the bitcoin ecosystem in general. If you feel inclined to do so,_
_please send to the secured address below. Much love <3_

Addr: bc1q4fnuqgy4xlqgw3et76nqwz8u573xyhcgwmac8u
