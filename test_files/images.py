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

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)

    @task(5)
    def nova_list_images(self):
        list_images(self)

    @task(5)
    def nova_list_images_detail(self):
        list_images_detail(self)

    @task(5)
    def nova_list_image_detail(self):
        list_image_detail(self)

    @task(5)
    def nova_list_image_metadata(self):
        list_image_metadata(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5
    max_wait=10
