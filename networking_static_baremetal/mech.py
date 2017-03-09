# Copyright 2017, Cisco Systems.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neutron.callbacks import resources
from neutron.db import provisioning_blocks
from neutron.extensions import portbindings
from neutron.plugins.ml2 import driver_api


class StaticMechDriver(driver_api.MechanismDriver):

    def initialize(self):
        pass

    def create_network_precommit(self, context):
        pass

    def create_network_postcommit(self, context):
        pass

    def update_network_precommit(self, context):
        pass

    def update_network_postcommit(self, context):
        pass

    def delete_network_precommit(self, context):
        pass

    def delete_network_postcommit(self, context):
        pass

    def create_subnet_precommit(self, context):
        pass

    def create_subnet_postcommit(self, context):
        pass

    def update_subnet_precommit(self, context):
        pass

    def update_subnet_postcommit(self, context):
        pass

    def delete_subnet_precommit(self, context):
        pass

    def delete_subnet_postcommit(self, context):
        pass

    def create_port_precommit(self, context):
        pass

    def create_port_postcommit(self, context):
        pass

    def update_port_precommit(self, context):
        pass

    def update_port_postcommit(self, context):
        port = context.current
        vnic_type = port['binding:vnic_type']
        if (vnic_type == 'baremetal' and
                port[portbindings.VIF_TYPE] == portbindings.VIF_TYPE_OTHER):
            binding_profile = port['binding:profile']
            local_link_information = binding_profile.get(
                'local_link_information')
            if not local_link_information:
                return
            switch_info = local_link_information[0].get('switch_info')
            if switch_info != 'static':
                return

            provisioning_blocks.provisioning_complete(
                context._plugin_context, port['id'], resources.PORT,
                'STATICLYBOUND')

    def delete_port_precommit(self, context):
        pass

    def delete_port_postcommit(self, context):
        pass

    def bind_port(self, context):
        port = context.current
        binding_profile = port['binding:profile']
        local_link_information = binding_profile.get('local_link_information')
        vnic_type = port['binding:vnic_type']
        if not (vnic_type == 'baremetal' and local_link_information):
            return

        switch_info = local_link_information[0].get('switch_info')
        if switch_info != 'static':
            return

        provisioning_blocks.add_provisioning_component(
            context._plugin_context, port['id'], resources.PORT,
            'STATICALYBOUND')

        segments = context.segments_to_bind
        context.set_binding(segments[0][driver_api.ID],
                            portbindings.VIF_TYPE_OTHER, {})
