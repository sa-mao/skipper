#!/usr/bin/env python
# -*- coding: utf-8

# Copyright 2017-2019 The FIAAS Authors
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import logging

from k8s.models.common import ObjectMeta
from k8s.models.custom_resource_definition import CustomResourceDefinition, CustomResourceDefinitionSpec, \
    CustomResourceDefinitionNames

from ...deploy.bootstrap import BarePodBootstrapper

LOG = logging.getLogger(__name__)


class CrdBootstrapper(BarePodBootstrapper):
    def __init__(self):
        def _create(kind, plural, short_names, group):
            name = "%s.%s" % (plural, group)
            metadata = ObjectMeta(name=name)
            names = CustomResourceDefinitionNames(kind=kind, plural=plural, shortNames=short_names)
            spec = CustomResourceDefinitionSpec(group=group, names=names, version="v1")
            definition = CustomResourceDefinition.get_or_create(metadata=metadata, spec=spec)
            definition.save()
            LOG.info("Created CustomResourceDefinition with name %s", name)

        def bootstrap():
            _create("Application", "applications", ("app", "fa"), "fiaas.schibsted.io")
            _create("ApplicationStatus", "application-statuses", ("status", "appstatus", "fs"), "fiaas.schibsted.io")

        bootstrap()
        super(CrdBootstrapper, self).__init__(cmd_args=["--enable-crd-support"])
