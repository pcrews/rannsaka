import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

from lib.baseTaskSet import baseTaskSet

# TODO - make these config-driven
from lib.openstack.keystone import get_auth_token
from lib.openstack.nova import list_servers
from lib.openstack.nova import list_servers_detail
from lib.openstack.nova import list_server_detail
from lib.openstack.nova import create_server
from lib.openstack.nova import delete_server
from lib.openstack.nova import reboot_server
from lib.openstack.nova import resize_server
from lib.openstack.nova import confirm_resize_server
from lib.openstack.nova import revert_resize_server
from lib.openstack.nova import list_limits
from lib.openstack.nova import create_flavor
 

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.server_id = None
        self.server_count = 0
        # Use admin pw to create test flavors
        self.keystone_user = self.get_tempest_config_value('identity', 'admin_username')
        self.keystone_pw = self.get_tempest_config_value('identity', 'admin_password')
        self.keystone_tenant = self.get_tempest_config_value('identity', 'admin_tenant_name')
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)
        create_flavor(self, name='test1',
                     ram=4096,
                     vcpus=2,
                     disk=0,
                     id=9999,
                     is_public=True)
        create_flavor(self, name='test2',
                     ram=2048,
                     vcpus=2,
                     disk=0,
                     id=9998,
                     is_public=True)

        # reset to 'main' test user
        self.keystone_user = self.get_tempest_config_value('identity','username')
        self.keystone_tenant = self.get_tempest_config_value('identity','tenant_name')
        self.keystone_pw = self.get_tempest_config_value('identity','password')
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)



    @task(10)
    def nova_create_server(self):
        if not self.server_id:
            flavor_id = random.choice([42,42,42,42,42,
                                       84,84,
                                       451
                                       ])
            response = create_server(self,
                                     flavor_id=flavor_id,
                                     name="server-%s-%s" % (self.id, self.server_count))
            self.server_id = json.loads(response.content)['server']['id']
            self.server_count += 1
            time.sleep(10)
            self.nova_resize_server() 
        else:
            self.output('Server already exists, not creating one:')
        self.output("server id: %s" % self.server_id) 

    #@task(4)
    def nova_resize_server(self):
        flavor_id = random.choice([42,84,451,9999,9999,9999,9999,9998,9999,9999,9998,9998,9998])
        self.output("Resize server | %s | %s " % (self.server_id, flavor_id))
        if self.server_id:
            resize_server(self, self.server_id, flavor_id)
            time.sleep(10)
            confirm_resize_server(self, self.server_id)
        else:
            self.output("No server to resize")
            self.output("Creating new one...")
            self.nova_create_server()

    #@task(4)
    def nova_confirm_resize_server(self):
        if self.server_id:
            confirm_resize_server(self, self.server_id)

    def nova_revert_resize_server(self):
        if self.server_id:
            revert_resize_server(self, self.server_id)

    #@task(1)
    #def nova_reboot_server(self):
    #    if self.server_id:
    #        reboot_server(self, self.server_id)
    #    else:
    #        self.output("No server to reboot")
    #        self.output("Creating new one...")
    #        self.nova_create_server()

    @task(1)
    def nova_delete_server(self):
        if self.server_id:
            delete_server(self, self.server_id)
            # TODO - test response
            self.server_id = None
        else:
            self.output("No server to delete")
            self.output("Creating new one...")
            self.nova_create_server()

    #@task(10)
    #def nova_list_servers(self):
    #    list_servers(self)

    #@task(10)
    #def nova_list_servers_detail(self):
    #    list_servers_detail(self)

    #@task(5)
    #def nova_list_limits(self):
    #    list_limits(self)

    @task(5)
    def keystone_auth_token(self):
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)
 

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5
    max_wait=10000
