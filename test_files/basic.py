import os

import json
from locust import HttpLocust, TaskSet, task

from lib.baseTaskSet import baseTaskSet

# TODO - make these config-driven
from lib.openstack.keystone import get_auth_token
from lib.openstack.nova import list_servers
from lib.openstack.nova import list_servers_detail
from lib.openstack.nova import list_flavors
from lib.openstack.nova import list_flavors_detail
from lib.openstack.nova import list_images
from lib.openstack.nova import list_images_detail
from lib.openstack.nova import list_limits
 

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.keystone_user = "demo"
        self.keystone_pw = "TNETENNBA" 
        self.keystone_tenant = "demo" 
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)

    @task(5)
    def nova_list_servers(self):
        list_servers(self)

    @task(5)
    def nova_list_servers_detail(self):
        list_servers_detail(self)

    @task(5)
    def nova_list_flavors(self):
        list_flavors(self)

    @task(5)
    def nova_list_flavors_detail(self):
        list_flavors_detail(self)

    @task(5)
    def nova_list_limits(self):
        list_limits(self)

    @task(5)
    def nova_list_images(self):
        list_images(self)

    @task(5)
    def nova_list_images_detail(self):
        list_images_detail(self)

    @task(1)
    def keystone_auth(self):
        get_auth_token(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5
    max_wait=10
