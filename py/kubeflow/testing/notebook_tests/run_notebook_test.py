"""Runs notebook ipynb as test."""

import datetime
import logging
import os
import uuid
import yaml

import pytest

from kubeflow.testing.notebook_tests import nb_test_util
from kubeflow.testing import util

def test_run_notebook(record_xml_attribute, namespace, # pylint: disable=too-many-branches,too-many-statements
                      image_file, notebook_path, test_target_name,
                      artifacts_gcs):

  if not image_file:
    raise ValueError("image_file must provided")

  notebook_name = os.path.basename(
      notebook_path).replace(".ipynb", "").replace("_", "-")
  junit_name = "_".join(["test", notebook_name])
  util.set_pytest_junit(record_xml_attribute, junit_name, test_target_name)

  name = "-".join([notebook_name,
                   datetime.datetime.now().strftime("%H%M%S"),
                   uuid.uuid4().hex[0:3]])

  logging.info(f"Reading file {image_file}")
  contents = util.read_file(image_file)
  image_data = yaml.load(contents)

  if not "image" in image_data:
    raise ValueError(f"File {image_file} is missing field image containing "
                     f"the URI of the docker image to run the notebook in")

  image = image_data["image"]
  logging.info(f"Using image {image}")
  nb_test_util.run_papermill_job(notebook_path, name, namespace, image,
                                 artifacts_gcs)

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO,
                      format=('%(levelname)s|%(asctime)s'
                              '|%(pathname)s|%(lineno)d| %(message)s'),
                      datefmt='%Y-%m-%dT%H:%M:%S',
                      )
  logging.getLogger().setLevel(logging.INFO)
  pytest.main()
