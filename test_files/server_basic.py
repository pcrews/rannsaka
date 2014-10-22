import os
import random

import json
from locust import HttpLocust, TaskSet, task

from lib.baseTaskSet import baseTaskSet

# TODO - make these config-driven
from lib.openstack.keystone import get_auth_token
from lib.openstack.nova import list_servers
from lib.openstack.nova import list_servers_detail
from lib.openstack.nova import list_flavors
from lib.openstack.nova import list_flavors_detail
from lib.openstack.nova import list_flavor_detail
from lib.openstack.nova import list_images
from lib.openstack.nova import list_images_detail
from lib.openstack.nova import list_image_detail
from lib.openstack.nova import list_image_metadata
from lib.openstack.nova import create_server
from lib.openstack.nova import delete_server
from lib.openstack.nova import list_limits
 

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.keystone_user = "demo"
        self.keystone_pw = "TNETENNBA" 
        self.keystone_tenant = "demo" 
        self.server_id = None
        self.server_count = 0
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)

    @task(5)
    def nova_create_server(self):
        if not self.server_id:
            flavor_id = random.choice([42,42,42,84])
            response = create_server(self,
                                     flavor_id=flavor_id,
                                     name="server-%s-%s" % (self.id, self.server_count))
            self.server_id = json.loads(response.content)['server']['id']
            self.server_count += 1
        else:
            self.output('Server already exists, not creating one:')
        self.output("server id: %s" % self.server_id) 

    @task(2)
    def nova_delete_server(self):
        if self.server_id:
            delete_server(self, self.server_id)
            # TODO - test response
            self.server_id = None
        else:
            self.output("No server to delete - pass...")

    @task(5)
    def nova_list_servers(self):
        list_servers(self)

    @task(5)
    def nova_list_servers_detail(self):
        list_servers_detail(self)


    @task(1)
    def nova_list_limits(self):
        list_limits(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5
    max_wait=10
