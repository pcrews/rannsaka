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
from lib.openstack.nova import list_limits
from lib.openstack.nova import nova_get_server_id
from lib.openstack.nova import create_flavor
from lib.openstack.nova import list_flavors 

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.flavor_count = 0

        # Use admin pw to create test flavors
        self.keystone_user = self.get_tempest_config_value('identity', 'admin_username')
        self.keystone_pw = self.get_tempest_config_value('identity', 'admin_password')
        self.keystone_tenant = self.get_tempest_config_value('identity', 'admin_tenant_name')
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)

    @task(7)
    def create_bad_flavor(self):
        flavor_name = "%s-%s" % ( self.id, self.flavor_count)
        ram = random.choice([0,
                             0,1,-1,'abbazabba',
                             'cupcake-disco-biscuits',
                             '']) 
        vcpus = random.choice([-1,0,'absconding-benefits'])
        id=random.choice([flavor_name,
                          flavor_name,
                          flavor_name,
                          flavor_name,
                          flavor_name,
                          'test-flavor-bob'])
        disk=random.choice([0,'overnumerousness'])
        self.flavor_count += 1
        create_flavor(self, name=flavor_name,
                     ram=ram,
                     vcpus=vcpus,
                     disk=disk,
                     id=id,
                     is_public=True)

    @task(4)
    def list_flavors(self):
        list_flavors(self)

    @task(1)
    def keystone_auth_token(self):
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)
 

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=500
    max_wait=5000
