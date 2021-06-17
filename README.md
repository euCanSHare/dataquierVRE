Depends on: R (>=4.0), from CRAN: dataquieR (>=1.0.5), openxlsx (>=4.2.3)

Better see https://github.com/inab/vre_template_tool

see https://github.com/inab/openVRE/wiki/Bring-your-own-tool#how-to-bring-in-a-new-tool

on a mac, first install https://github.com/user454322/realpath

look at the configure-script for configuration:

```bash
./configure -b /usr/local/ -m /usr/local/man
```

install dependencies, ...

TODOs after the project is initially working:

- [euCanSHAre Github Organization](https://github.com/orgs/euCanSHare/): Move this project this organization

- dataquier execution JSONs: Add the files prepared with Laia, once she resent it. They include the new file formats and data types: "study_data", "study_meta_data", "HTML"

# VRE Sample Tool

A simple example tool that is ready to run a workflow

## Requirements

* Install the dependencies used by the Wrapper.

```bash
sudo apt update
sudo apt install git
sudo apt install docker-ce
```

Remember to add your username to the `docker` group.

 ```bash
 sudo usermod -a -G docker $USER
 ```
 
* Install the Wrapper dependencies.

    - Python 3.6 or +
    - Python3.6-dev and Python3.6-venv or +
    - mg-tool-api: https://github.com/Multiscale-Genomics/mg-tool-api.git
    - cwltool: https://github.com/common-workflow-language/cwltool.git

## Installation

Directly from GitHub:

```bash
cd $HOME

git clone https://github.com/lrodrin/vre_sample_tool.git

cd vre_sample_tool
```

Create the Python environment

```bash
python3 -m venv $HOME/vre_sample_tool/venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Add your ${USER} in `tests/basic/config.json`:

```json 
"arguments": [
  {
      "name": "execution",
      "value": "/home/${USER}/vre_sample_tool/tests/basic/run000"
  }
],
"output_files": [
  {
      "name": "bam_file",
      "required": true,
      "allow_multiple": false,
      "file": {
          "file_path": "/home/${USER}/vre_sample_tool/tests/basic/run000/A.bam"
      }
   }
]
```
and `tests/basic/in_metadata.json`:

```json 
{
    "_id": "unique_file_id_5e14abe0a37012.29503907",
    "file_path": "/home/${USER}/vre_sample_tool/tests/basic/NA12878.bam"
},
{
    "_id": "unique_file_id_5e14abe0a37012.29503908",
    "file_path": "/home/${USER}/vre_sample_tool/tests/basic/hg38.fa"
{
``` 
and `/test/basic/input_basic_example.yml`:

```yaml 
  input_reads: 
    class: File
    location: /home/{USER}/vre_sample_tool/tests/basic/NA12878.bam
  biospecimen_name: "hg38"
  output_basename: "mytest"
  indexed_reference_fasta:
    class: File 
    location: /home/{USER}/vre_sample_tool/tests/basic/hg38.fa
```
## Run the example
```bash
./tests/basic/test_VRE_CWL_RUNNER.sh
```
# VRE template Tool Executor

[![Documentation Status](https://readthedocs.org/projects/vre-template-tool/badge/?version=latest)](https://vre-template-tool.readthedocs.io/en/latest/?badge=latest)

## Requirements

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

Directly from GitHub:

```bash
cd $HOME
git clone https://github.com/inab/vre_template_tool.git
cd vre_template_tool
```

Create the Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade wheel
pip install -r requirements.txt
```

## Run the Wrapper

First, go to [tests/basic/](https://github.com/inab/vre_template_tool/tree/master/tests/basic) to change `config.json` and `in_metadata.json` files.

```bash
./VRE_RUNNER --config tests/basic/config.json --in_metadata tests/basic/in_metadata.json --out_metadata out_metadata.json --log_file VRE_RUNNER.log
```

## License
* © 2020-2021 Barcelona Supercomputing Center (BSC), ES

Licensed under the Apache License, version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>, see the file `LICENSE.txt` for details.
