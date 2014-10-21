import os

import json
from locust import HttpLocust, TaskSet, task

from lib.baseTaskSet import baseTaskSet

# TODO - make these config-driven
from lib.openstack.keystone import get_auth_token
from lib.openstack.nova import list_images
from lib.openstack.nova import list_images_detail
from lib.openstack.nova import list_image_detail
from lib.openstack.nova import list_image_metadata 
from lib.openstack.nova import update_image_metadata
from lib.openstack.nova import nova_get_image_id

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.keystone_user = "admin"
        self.keystone_pw = "TNETENNBA" 
        self.keystone_tenant = "admin" 
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)
        self.image_id = nova_get_image_id(self)

    @task(5)
    def nova_list_image_metadata(self):
        list_image_metadata(self, self.image_id)

    @task(5)
    def nova_update_image_metadata(self):
        update_image_metadata(self, self.image_id)

    @task(1)
    def update_locust_image_id(self):
        self.image_id = nova_get_image_id(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5
    max_wait=10
