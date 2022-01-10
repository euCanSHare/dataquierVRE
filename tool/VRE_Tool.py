#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020-2021 Barcelona Supercomputing Center (BSC), Spain
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import time
from glob import glob

from basic_modules.tool import Tool
from basic_modules.metadata import Metadata
from utils import logger


class myTool(Tool):
    """
    This class define dataquieR-app Tool.
    """
    DEFAULT_KEYS = ['execution', 'project', 'description']  # config.json default keys
    R_SCRIPT_PATH = "/AssessDataQuality/dataquieR.R"   # tool application

    def __init__(self, configuration=None):
        """
        Init function

        :param configuration: a dictionary containing parameters that define how the operation should be carried out, 
        which are specific to dataquieR-app tool.
        :type configuration: dict
        """
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        # Init variables
        self.current_dir = os.path.abspath(os.path.dirname(__file__))
        self.parent_dir = os.path.abspath(self.current_dir + "/../")
        self.execution_path = self.configuration.get('execution', '.')
        if not os.path.isabs(self.execution_path):  # convert to abspath if is relpath
            self.execution_path = os.path.normpath(os.path.join(self.parent_dir, self.execution_path))

        self.arguments = dict(
            [(key, value) for key, value in self.configuration.items() if key not in self.DEFAULT_KEYS]
        )

    def run(self, input_files, input_metadata, output_files, output_metadata):
        """
        The main function to run the dataquieR-app tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        :param output_files: Dictionary of the output files locations. Expected to be generated.
        :type output_files: dict
        :param output_metadata: # TODO
        :type output_metadata: list
        :return: # TODO
        :rtype: dict, dict
        """
        try:
            # Set and validate execution directory. If not exists the directory will be created.
            os.makedirs(self.execution_path, exist_ok=True)

            # Set and validate execution parent directory. If not exists the directory will be created.
            execution_parent_dir = os.path.dirname(self.execution_path)
            os.makedirs(execution_parent_dir, exist_ok=True)

            # Update working directory to execution path
            os.chdir(self.execution_path)

            # Tool Execution
            self.toolExecution(input_files, input_metadata)

            # Create and validate the output file from tool execution
            output_id = output_metadata[0]["name"]
            output_type = output_metadata[0]["file"]["file_type"].lower()
            try:
                # TODO: add more output files to save, if it is necessary for you
                #  or create a method to manage more than one output file
                output_file_path = glob(self.execution_path + "/*." + output_type)[0]
                output_files[output_id] = [(output_file_path, "file")]
            except:
                errstr = "Expected output file ("+ output_id +") not found."
                logger.fatal(errstr)
                raise Exception(errstr)

            return output_files, output_metadata

        except:
            errstr = "VRE dataquieR-app tool execution failed. See logs."
            logger.fatal(errstr)
            raise Exception(errstr)

    def toolExecution(self, input_files, input_metadata):
        """
        The main function to run the dataquieR-app tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        """
        try:
            # Set up docker related variables
            docker_data_dir       = os.path.dirname(self.execution_path) # user's workspace 
            docker_volume_remote  = "/shared_volume/"
            docker_image          = "lcodo/dataquier:1.1"
            docker_user           = "root"
            docker_execution_path = os.path.join(docker_volume_remote, os.path.relpath(self.execution_path,docker_data_dir))

            # Get input files
            study_data = input_files.get("study_data")
            if not os.path.isabs(study_data):  # convert to abspath if is relpath
                study_data = os.path.normpath(os.path.join(self.parent_dir, study_data))
            relpath = os.path.relpath(study_data,docker_data_dir)
            study_data  = os.path.join(docker_volume_remote, relpath)

            mdf: Metadata
            mdf = input_metadata.get("study_data")[1]
            study_data_file_type = mdf.file_type

            meta_data = input_files.get("meta_data")
            if not os.path.isabs(meta_data):  # convert to abspath if is relpath
                meta_data = os.path.normpath(os.path.join(self.parent_dir, meta_data))
            relpath = os.path.relpath(meta_data,docker_data_dir)
            meta_data  = os.path.join(docker_volume_remote, relpath)
            mdf = input_metadata.get("meta_data")[1]
            meta_data_file_type = mdf.file_type

            if "consistency_check_table" in input_files:
                checks = input_files.get("consistency_check_table")
                if not os.path.isabs(checks):  # convert to abspath if is relpath
                    checks = os.path.normpath(os.path.join(self.parent_dir, checks))

                relpath = os.path.relpath(checks,docker_data_dir)
                checks  = os.path.join(docker_volume_remote, relpath)
                checks = "checks=" + checks
                mdf = input_metadata.get("consistency_check_table")[1]
                checks_file_type = "checks_file_type=" + mdf.file_type
            else:
                checks = None
                checks_file_type = None

            if "code_labels" in input_files:
                code_labels = input_files.get("code_labels")
                if not os.path.isabs(code_labels):  # convert to abspath if is relpath
                    code_labels = os.path.normpath(os.path.join(self.parent_dir, code_labels))
                relpath = os.path.relpath(code_labels,docker_data_dir)
                code_labels  = os.path.join(docker_volume_remote, relpath)
                code_labels = "code_labels=" + code_labels
                mdf = input_metadata.get("code_labels")[1]
                code_labels_file_type = "code_labels_file_type=" + mdf.file_type
            else:
                code_labels = None
                code_labels_file_type = None

#            meta_data = input_files.get("meta_data")
#            if not os.path.isabs(meta_data):  # convert to abspath if is relpath
#                meta_data = os.path.normpath(os.path.join(self.parent_dir, meta_data))
#
#            mdf = input_metadata.get("meta_data")[1]
#            meta_data_file_type = mdf.file_type
#
#            meta_data = input_files.get("meta_data")
#            if not os.path.isabs(meta_data):  # convert to abspath if is relpath
#                meta_data = os.path.normpath(os.path.join(self.parent_dir, meta_data))
#
#            mdf = input_metadata.get("meta_data")[1]
#            meta_data_file_type = mdf.file_type

            # Get arguments
            label_col = self.arguments.get("label_col")

            # Tool execution
            R_cmd = [
                'Rscript',
                self.parent_dir + self.R_SCRIPT_PATH,  # dataquieR.R
                study_data,             # study_data
                study_data_file_type,   # file type
                meta_data,              # meta_data
                meta_data_file_type,    # file type
                label_col,              # label_col argument, default: VAR_NAMES
                checks,                 # checks=[FILE_PATH]
                checks_file_type,       # checks_file_type=XLSX
                code_labels,            # code_labels=[FILE_PATH]
                code_labels_file_type,  # code_labels_file_type=XLSX
            ]

            cmd = [
                'docker', 'run',
                '-v',        docker_data_dir + ":" + docker_volume_remote,
                '--workdir', docker_execution_path,
                '--user',    docker_user,
                '--name',    "dataquier_run",
                docker_image,
            ] + R_cmd 

            self._cleanExitedContainers()

            logger.info("Launching execution at the dataquieR container");
            logger.info(" ".join([x for x in cmd if x is not None]));
            
            process = subprocess.Popen([x for x in cmd if x is not None],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # TODO: change command line to run dataquieR-app

            # Sending the stdout to the log file
            for line in iter(process.stderr.readline, b''):
                print(line.rstrip().decode("utf-8").replace("", " "))

            rc = process.poll()
            while rc is None:
                rc = process.poll()
                time.sleep(0.1)

            if rc is not None and rc != 0:
                logger.progress("Something went wrong inside the dataquieR-app execution. See logs.", status="WARNING")
            else:
                _cleanExitedContainers()
                logger.progress("dataquieR-app execution finished successfully.", status="FINISHED")

        except:
            errstr = "dataquieR-app execution failed. See logs."
            logger.error(errstr)
            raise Exception(errstr)


    def _cleanExitedContainers(self):
        try:
            logger.info("Cleaning exited containers")
            #cmd = "docker rm $(docker ps -a -q  --filter 'exited=0') "  # clean successfully finished
            cmd = "docker rm $(docker ps -a -q  --filter 'status=exited') "
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = p.communicate()

        except:
            errstr = "dataquieR-app execution failed. See logs."
            logger.error("Cannot clean exited containers.")
            logger.error(output)
            logger.error(error)
            raise Exception(error)
