import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

from lib.baseTaskSet import baseTaskSet

# TODO - make these config-driven
from lib.openstack.keystone import get_auth_token
from lib.openstack.cinder import list_volumes
from lib.openstack.cinder import list_volumes_detail
from lib.openstack.cinder import list_volume_detail
from lib.openstack.cinder import create_volume 
from lib.openstack.cinder import delete_volume
from lib.openstack.cinder import cinder_get_volume_id
from lib.openstack.nova import nova_get_image_id
from lib.openstack.nova import list_limits
 

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.volume_id = None
        self.volume_count = 0
        self.sleep_times=[0,0,1,1,1,1,3,3,3,5,5,5,5,10,10,30,30]
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)

    def chance(self):
        chances = [1,1,1,1,2]
        if random.choice(chances)%2==0:
            return True
        else:
            return False

    def rand_sleep(self):
        time.sleep(random.choice(self.sleep_times))

    @task(2)
    def update_volume_id(self):
        self.volume_id = cinder_get_volume_id(self)

    @task(5)
    def cinder_create_volume(self):
        if not self.volume_id:
            volume_id=None
            image_id=None
            bootable=False
            size=1
            # volume_id
            if self.chance():
                volume_id = cinder_get_volume_id(self)
            # image_id
            if self.chance():
                image_id = nova_get_image_id(self)
            # bootable
            if self.chance():
                bootable=True
            # metadata
            # size
            sizes = [1,1,1,3,3,5,5,2.5,100,99,'a','abbazabba',-1,0]
            size = random.choice(sizes)
            # description
            # snapshot_id
            response = create_volume(self,
                                     name="volume-%s-%s" % (self.id, self.volume_count),
                                     volume_id=volume_id,
                                     image_id=image_id,
                                     bootable=bootable,
                                     size=size)
            print response.content
            print '!'*80
            self.volume_id = json.loads(response.content)['volume']['id']
            self.volume_count += 1
            self.rand_sleep()
        else:
            self.output('Volume already exists, not creating one:')
        self.output("volume id: %s" % self.volume_id) 

    @task(2)
    def cinder_delete_volume(self):
        if self.volume_id:
            delete_volume(self, self.volume_id)
            # TODO - test response
            self.volume_id = None
            self.rand_sleep()
        else:
            self.cinder_create_volume()

    @task(5)
    def cinder_list_volumes(self):
        list_volumes(self)

    @task(5)
    def cinder_list_volumes_detail(self):
        list_volumes_detail(self)

    @task(4)
    def cinder_list_volume_detail(self):
        list_volume_detail(self)

    @task(1)
    def nova_list_limits(self):
        list_limits(self)

    @task(1)
    def keystone_get_auth(self):
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=500
    max_wait=1000
