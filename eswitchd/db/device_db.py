# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Mellanox Technologies, Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class DeviceDB():
    def __init__(self):
        self.device_db  = {}

    def get_pf(self,fabric):
        return self.device_db[fabric]['pf']

    def add_fabric(self, fabric, pf, pci_id, hca_port, fabric_type, pf_mlx_dev):
        list_keys = ('vfs', 'free_vfs', 'reserved_vfs')
        details = {}
        for key in list_keys:
            details[key]=[]
        details['pf'] = pf
        details['pci_id'] = pci_id
        details['hca_port'] = hca_port
        details['fabric_type'] = fabric_type
        details['pf_mlx_dev'] = pf_mlx_dev
        self.device_db[fabric] = details

    def get_fabric_details(self, fabric):
        return self.device_db[fabric]

    def set_fabric_devices(self, fabric, vfs):
        self.device_db[fabric]['vfs'] = vfs
        self.device_db[fabric]['free_vfs'] = vfs[:]

    def get_free_vfs(self, fabric):
        return self.device_db[fabric]['free_vfs']

    def get_free_devices(self, fabric):
        return self.get_free_vfs(fabric)

    def get_dev_fabric(self,dev):
        for fabric in self.device_db:
            if dev in self.device_db[fabric]['vfs']:
                return fabric

    def allocate_device(self, fabric, dev=None):
        available_resources = self.device_db[fabric]['free_vfs']
        try:
            if dev:
                available_resources.remove(dev)
            else:
                dev = available_resources.pop()
            return dev
        except Exception,e:
            LOG.error("exception on device allocation on dev  %s - No available resources." % dev)
            raise e

    def deallocate_device(self, fabric, dev):
        resources = self.device_db[fabric]['vfs']
        available_resources = self.device_db[fabric]['free_vfs']
        if dev in resources:
            available_resources.append(dev)
            return dev
        else:
            return None

