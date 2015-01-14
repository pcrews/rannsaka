if __name__ == "__main__" and __package__ is None:
    __package__ = "task_sets.nova_basic_task_set"

import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

from baseTaskSet import baseTaskSet
import task_funcs.keystone_v2_base as keystone_base
import task_funcs.nova_v2_base as nova_base
import task_funcs.nova_v2_utility as nova_util

class basicGet(baseTaskSet):
    """ task set designed to do insane, random, and valid things
        via the nova api

    """

    def on_start(self):
        super(basicGet, self).on_start()
        self.server_count = 0

        # Use admin pw to create test flavors
        self.keystone_user = self.get_tempest_config_value('identity', 'admin_username')
        self.keystone_pw = self.get_tempest_config_value('identity', 'admin_password')
        self.keystone_tenant = self.get_tempest_config_value('identity', 'admin_tenant_name')
        self.auth_token, self.tenant_id, self.service_catalog = keystone_base.get_auth_token(self)
        nova_base.create_flavor(self, name='test1',
                     ram=4096,
                     vcpus=2,
                     disk=0,
                     id=9999,
                     is_public=True)
        nova_base.create_flavor(self, name='test2',
                     ram=2048,
                     vcpus=2,
                     disk=0,
                     id=9998,
                     is_public=True)

        # reset to 'main' test user
        self.keystone_user = self.get_tempest_config_value('identity','username')
        self.keystone_tenant = self.get_tempest_config_value('identity','tenant_name')
        self.keystone_pw = self.get_tempest_config_value('identity','password')
        self.auth_token, self.tenant_id, self.service_catalog = keystone_base.get_auth_token(self)

    tasks =  { nova_base.list_servers: 1,
               nova_base.list_servers_detail: 1,
               nova_base.list_flavors: 1,
               nova_base.list_images: 1,
               nova_base.list_images_detail: 1,
               nova_base.list_image_detail: 1,
               nova_base.list_image_metadata: 1,
               nova_base.list_limits: 1
              }
