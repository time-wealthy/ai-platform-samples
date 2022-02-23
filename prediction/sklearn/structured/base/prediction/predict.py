#!/usr/bin/env python
# Copyright 2019 Google LLC
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
# ==============================================================================

from google.api_core.client_options import ClientOptions

import os
import logging
from googleapiclient import discovery

logging.basicConfig()

# In this sample, we will reply on 6 features only:
# trip_miles            trip_seconds        fare
# trip_start_month      trip_start_hour     trip_start_day
instances = [
    [1.1, 420, 625, 8, 16, 3],
    [0.3, 960, 1485, 3, 22, 2],
    [1.0, 300, 505, 1, 1, 1],
]

PROJECT_ID = os.getenv('PROJECT_ID')
MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_VERSION = os.getenv('MODEL_VERSION')
REGION = os.getenv('REGION')

logging.info('PROJECT_ID: %s', PROJECT_ID)
logging.info('MODEL_NAME: %s', MODEL_NAME)
logging.info('MODEL_VERSION: %s', MODEL_VERSION)
logging.info('REGION: %s', REGION)

prefix = "{}-ml".format(REGION) if REGION else "ml"
api_endpoint = "https://{}.googleapis.com".format(prefix)
client_options = ClientOptions(api_endpoint=api_endpoint)

# Use Regional support
service = googleapiclient.discovery.build('ml', 'v1',
                                          cache_discovery=False,
                                          client_options=client_options)
name = 'projects/{}/models/{}/versions/{}'.format(PROJECT_ID, MODEL_NAME,
                                                  MODEL_VERSION)

response = service.projects().predict(
    name=name,
    body={'instances': instances}
).execute()

if 'error' in response:
    logging.error(response['error'])
else:
    print(response['predictions'])
