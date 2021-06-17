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
    This class define <myTool> Tool.
    """
    DEFAULT_KEYS = ['execution', 'project', 'description']  # config.json default keys
    R_SCRIPT_PATH = "/AssessDataQuality/dataquieR.R"   # tool application

    def __init__(self, configuration=None):
        """
        Init function

        :param configuration: a dictionary containing parameters that define how the operation should be carried out, 
        which are specific to <myTool> tool.
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
        The main function to run the <myTool> tool.

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
            output_file_path = glob(self.execution_path + "/*." + output_type)[0]
            output_files[output_id] = [(output_file_path, "file")]
            # TODO: add more output files to save, if it is necessary for you
            #  or create a method to manage more than one output file

            return output_files, output_metadata

        except:
            errstr = "VRE <myTool> tool execution failed. See logs."
            logger.fatal(errstr)
            raise Exception(errstr)

    def toolExecution(self, input_files, input_metadata):
        """
        The main function to run the <myTool> tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        """
        try:
            # Get input files
            study_data = input_files.get("study_data")
            if not os.path.isabs(study_data):  # convert to abspath if is relpath
                study_data = os.path.normpath(os.path.join(self.parent_dir, study_data))

            mdf: Metadata
            mdf = input_metadata.get("study_data")[1]
            study_data_file_type = mdf.file_type

            meta_data = input_files.get("meta_data")
            if not os.path.isabs(meta_data):  # convert to abspath if is relpath
                meta_data = os.path.normpath(os.path.join(self.parent_dir, meta_data))

            mdf = input_metadata.get("meta_data")[1]
            meta_data_file_type = mdf.file_type


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

            # TODO: add more input files to use, if it is necessary for you

            # Get arguments
            label_col = self.arguments.get("label_col")
            # TODO: add more arguments to use, if it is necessary for you

            # Tool execution
            cmd = [
                'Rscript',
                self.parent_dir + self.R_SCRIPT_PATH,  # dataquieR.R
                study_data,             # study_data
                study_data_file_type,   # file type
                meta_data,              # meta_data
                meta_data_file_type,    # file type
                label_col,              # label_col argument, default: VAR_NAMES
                "checks=42",
                "code_labels=64"
            ]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # TODO: change command line to run <myApplication>

            # Sending the stdout to the log file
            for line in iter(process.stderr.readline, b''):
                print(line.rstrip().decode("utf-8").replace("", " "))

            rc = process.poll()
            while rc is None:
                rc = process.poll()
                time.sleep(0.1)

            if rc is not None and rc != 0:
                logger.progress("Something went wrong inside the <myApplication> execution. See logs.", status="WARNING")
            else:
                logger.progress("<myApplication> execution finished successfully.", status="FINISHED")

        except:
            errstr = "<myApplication> execution failed. See logs."
            logger.error(errstr)
            raise Exception(errstr)
