
Cloned from https://github.com/inab/vre_template_tool

see also https://github.com/inab/openVRE/wiki/Bring-your-own-tool#how-to-bring-in-a-new-tool

on a mac, first install realpath from https://github.com/user454322/realpath

look at the configure-script for configuration:

```bash
./configure -b /usr/local/ -m /usr/local/man
```

# TODOs:

- @Laia: Please add the following two data types: 
 - missing_code_label_table
 - consistency_check_table

## Requirements

* Install the dependencies used by the Wrapper.

Depends on: R (>=4.0), from CRAN: dataquieR (>=1.0.5), openxlsx (>=4.2.3)

* Install the Wrapper dependencies.

    - Python 3.6 or +
    - Python3.6-dev and Python3.6-venv or +
    - mg-tool-api: https://github.com/Multiscale-Genomics/mg-tool-api.git

- Python 3.6 or later
- [git](https://git-scm.com/downloads)

```bash
sudo apt update
sudo apt install python3
sudo apt install git
```

In order to install the Python dependencies you need `pip` and `venv` modules.

```bash
sudo apt install python3-pip python3-venv
```


## Installation

```bash
cd $HOME

git clone ...

cd dataquierVRE
```

Create the Python environment

```bash
python3 -m venv $HOME/dataquierVRE/venv
source venv/bin/activate
pip install -r requirements.txt
```

or with relative paths:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade wheel
pip install -r requirements.txt
```

# VRE template Tool Executor

[![Documentation Status](https://readthedocs.org/projects/vre-template-tool/badge/?version=latest)](https://vre-template-tool.readthedocs.io/en/latest/?badge=latest)

## Run the Wrapper

First, go to [tests/basic/](https://github.com/inab/vre_template_tool/tree/master/tests/basic) to change `config.json` and `in_metadata.json` files.

```bash
./VRE_RUNNER --config tests/basic/config.json --in_metadata tests/basic/in_metadata.json --out_metadata out_metadata.json --log_file VRE_RUNNER.log
```

## License
* University Medicine Greifswald 2021

Licensed under the Apache License, version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>, see the file `LICENSE.txt` for details.
