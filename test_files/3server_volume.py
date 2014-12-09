import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

from lib.baseTaskSet import baseTaskSet

# TODO - make these config-driven
from lib.openstack.keystone import get_auth_token
from lib.openstack.cinder_api import list_volumes
from lib.openstack.cinder_api import list_volumes_detail
from lib.openstack.cinder_api import list_volume_detail
from lib.openstack.cinder_api import create_volume 
from lib.openstack.cinder_api import delete_volume
from lib.openstack.cinder_api import cinder_get_volume_id
from lib.openstack.cinder_api import cinder_get_snapshot_id
from lib.openstack.cinder_api import create_snapshot
from lib.openstack.cinder_api import delete_snapshot
from lib.openstack.cinder_api import list_snapshots
from lib.openstack.cinder_api import list_snapshots_detail
from lib.openstack.nova_api import nova_get_image_id
from lib.openstack.nova_api import nova_get_image_id_by_name
from lib.openstack.nova_api import list_limits
from lib.openstack.nova_api import list_servers
from lib.openstack.nova_api import list_servers_detail
from lib.openstack.nova_api import list_server_detail
from lib.openstack.nova_api import create_server
from lib.openstack.nova_api import delete_server
from lib.openstack.nova_api import reboot_server
from lib.openstack.nova_api import resize_server
from lib.openstack.nova_api import confirm_resize_server
from lib.openstack.nova_api import revert_resize_server
from lib.openstack.nova_api import update_server_metadata
from lib.openstack.nova_api import overwrite_server_metadata
from lib.openstack.nova_api import list_limits
from lib.openstack.nova_api import nova_get_server_id
from lib.openstack.nova_api import nova_get_attachment_id

from lib.openstack.nova_api import reboot_server
from lib.openstack.nova_api import attach_volume
from lib.openstack.nova_api import remove_volume
 

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.volume_id = None
        self.volume_count = 0
        self.snapshot_count = 0
        self.min_server_count = 9	 
        self.max_server_count = 13 
        self.min_volume_count = 9 
        self.max_volume_count = 14 
        self.server_count = 0
        self.sleep_times=[0,0,1,1,1,1,3,3,3,5,5,5,5,10,10,30,30]
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)

        # only use certain images
        self.image_names = ['cirros-0.3.2-x86_64-uec']
        self.images=[]
        for image_name in self.image_names:
            self.images.append(nova_get_image_id_by_name(self,image_name))


    def chance(self):
        chances = [1,1,1,1,2]
        if random.choice(chances)%2==0:
            return True
        else:
            return False

    def rand_sleep(self):
        time.sleep(random.choice(self.sleep_times))

#    @task(2)
    def update_volume_id(self):
        self.volume_id = cinder_get_volume_id(self)

    #@task(5)
    def cinder_create_volume(self):
        volume_id=None
        image_id=None
        snapshot_id=None
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
        sizes = [1,1,1,1,1,1,1,1,1,-1,0,99,'a',.5,1.4,2]
        size = random.choice(sizes)
        # description
        # snapshot_id
        if self.chance():
            snapshot_id = cinder_get_snapshot_id(self)
        volume_name = "volume-%s-%s" % (self.id, self.volume_count) 
        self.output("create volume: %s" %volume_name)
        response = create_volume(self,
                                 name=volume_name,
                                 volume_id=volume_id,
                                 image_id=image_id,
                                 bootable=bootable,
                                 size=size)
        volume_id = json.loads(response.content)['volume']['id']
        self.volume_count += 1
        self.rand_sleep()
        self.output("volume id: %s" % volume_id) 

#    @task(4)
    def cinder_create_snapshot(self):
        volume_id = cinder_get_volume_id(self)
        force=False
        # force
        if self.chance():
            force=True
        snapshot_name = "snapshot-%s-%s" %(self.id, self.snapshot_count)
        self.output("create snapshot: %s" %snapshot_name)
        response = create_snapshot(self, volume_id=volume_id,
                                   name=snapshot_name,
                                   description=None,
                                   force=force)
        self.snapshot_count += 1


#    @task(2)
    def cinder_delete_snapshot(self):
        snapshot_id = cinder_get_snapshot_id(self)
        self.output("delete snapshot: %s" %snapshot_id)
        response = delete_snapshot(self, snapshot_id=snapshot_id)


    #@task(1)
    def cinder_delete_volume(self):
        volume_id = cinder_get_volume_id(self)
        self.output("delete volume: %s" %volume_id)
        delete_volume(self, volume_id)
        # TODO - test response
        self.rand_sleep()

    @task(1)
    def nova_create_server(self):
        flavor_id = random.choice([42,84])
        image_id = random.choice(self.images)
        response = create_server(self,
                                 flavor_id=flavor_id,
                                 image_id=image_id,
                                 name="server-%s-%s" % (self.id, self.server_count))
        server_id = json.loads(response.content)['server']['id']
        self.server_count += 1
        time.sleep(random.choice([1,1,3,3,5,5,5,5,5,5,10,10,10,10,10,10,10,10,25]))
        #self.nova_resize_server()
        self.output("server id: %s" % server_id)
        self.output("create server: %s" %response.content)

    @task(5)
    def check_volume_pool(self):
        response = list_volumes(self)
        volumes = json.loads(response.content)['volumes']
        if len(volumes) < self.min_volume_count:
            self.cinder_create_volume()

    @task(3)
    def check_server_pool(self):
        response = list_servers(self)
        servers = json.loads(response.content)['servers']
        if len(servers) < self.min_server_count:
            self.nova_create_server()
        elif len(servers) >= self.max_server_count:
            choices = [1,1,1,1,1,1,1,1,1,2]
            choice = random.choice(choices)
            if choice == 2:
                pass

    @task(5)
    def attach_volume(self):
        server_id = nova_get_server_id(self)
        volume_id = cinder_get_volume_id(self)
        devices = ['a','b','b','b','c','c','c','d','d','e','f','g','g','g']
        device = None
        if self.chance(): # generate device id
            device = '/dev/vd%s' % (random.choice(devices)) 
        self.output("attach_volume: %s || %s || %s" % (server_id, volume_id, device))
        response = attach_volume(self,
                                 server_id=server_id,
                                 volume_id=volume_id,
                                 device_path=device)

    @task(2)
    def remove_volume(self):
        server_id = nova_get_server_id(self)
        attachment_id = nova_get_attachment_id(self, server_id)
        self.output("remove_volume: %s || %s" % (server_id, attachment_id))
        response = remove_volume(self,
                                 server_id=server_id,
                                 attachment_id=attachment_id)

    #@task(2)
    def nova_reboot_server(self):
        server_id = nova_get_server_id(self)
        self.output("reboot server: %s" % server_id)
        reboot_server(self, server_id)
        self.rand_sleep()

    @task(1)
    def nova_delete_server(self):
        server_id = nova_get_server_id(self)
        self.output("Delete server: %s" %server_id)
        delete_server(self, server_id)

    #@task(5)
    def nova_resize_server(self):
        server_id = nova_get_server_id(self)
        flavor_id = random.choice([42,84,
                                   9999, 9999, 9999, 9999,
                                   9998, 9998, 9998, 9998,
                                   451, 451, 451])
        self.output("Resize server | %s | %s " % (server_id, flavor_id))
        if server_id:
            resize_server(self, server_id, flavor_id)
            time.sleep(random.choice([5,9,9,9,9,10,10,10,10,25, 50, 65]))
            choices = [1,1,1,1,1,2,2]
            #if random.choice(choices) %2 != 0:
            if choices:
                confirm_resize_server(self, server_id)
            else:
                revert_resize_server(self,server_id)
        else:
            pass

    @task(2)
    def nova_list_servers_detail(self):
        list_servers_detail(self)

    @task(3)
    def cinder_list_volumes(self):
        list_volumes(self)

    @task(2)
    def cinder_list_volumes_detail(self):
        list_volumes_detail(self)

    @task(4)
    def cinder_list_volume_detail(self):
        list_volume_detail(self)

    @task(2)
    def cinder_list_snapshots(self):
        list_snapshots(self)

    @task(1)
    def cinder_list_snapshots_detail(self):
        list_snapshots_detail(self)

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
