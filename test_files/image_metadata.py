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
from lib.openstack.nova import overwrite_image_metadata
from lib.openstack.nova import nova_get_image_id

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.keystone_user = self.get_tempest_config_value('identity', 'admin_username') 
        self.keystone_pw = self.get_tempest_config_value('identity', 'admin_password') 
        self.keystone_tenant = self.get_tempest_config_value('identity', 'admin_tenant_name') 
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)
        self.image_id = nova_get_image_id(self)

    @task(5)
    def nova_list_image_metadata(self):
        list_image_metadata(self, self.image_id)

    @task(5)
    def nova_update_image_metadata(self):
        update_image_metadata(self, self.image_id)

    @task(4)
    def nova_overwrite_image_metadata(self):
        overwrite_image_metadata(self, self.image_id)

    #@task(3)
    def nova_update_image_metadata2(self):
        update_image_metadata(self)

    #@task(2)
    def nova_overwrite_image_metadata2(self):
        overwrite_image_metadata(self)

    @task(1)
    def update_locust_image_id(self):
        self.image_id = nova_get_image_id(self)

    @task(1)
    def keystone_auth_token(self):
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5
    max_wait=10
