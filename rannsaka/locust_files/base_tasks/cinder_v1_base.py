import os
import json
import string
import random

import nova_v2_base


def cinder_request(self,
                 url_detail,
                 request_type='get',
                 request_name=None,
                 data=None,
                 locust_name=None):
    url = self.get_endpoint('volumev2')
    if url_detail:
        url = os.path.join(url, url_detail)
    headers = {'X-Auth-Project-Id': self.keystone_tenant,
               'X-Auth-Token': self.auth_token,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    if data:
        response = getattr(self.client, request_type)(url,
                                                      headers=headers,
                                                      data=json.dumps(data),
                                                      name=locust_name)
    else:
        response = getattr(self.client, request_type)(url,
                                                      headers=headers,
                                                      name=locust_name)
    self.output(url)
    self.output("Response status code: %s" % response.status_code)
    self.output("Response content: %s" % response.content)
    return response


def cinder_get_volume_id(self):
    """ Return a random volume from currently
        available volumes
    """

    response = cinder_request(self, 'volumes', 'get')
    volume_list = json.loads(response.content)['volumes']
    volume_id = random.choice([i['id'] for i in volume_list])
    return volume_id


def cinder_get_snapshot_id(self):
    """ Return a random snapshot from currently
        available snapshots
    """

    response = cinder_request(self, 'snapshots', 'get')
    snapshot_list = json.loads(response.content)['snapshots']
    snapshot_id = random.choice([i['id'] for i in snapshot_list])
    return snapshot_id


def cinder_get_image_id(self):
    """ Return a random image from currently
        available images
    """

    response = nova_api.nova_request(self, 'images', 'get')
    image_list = json.loads(response.content)['images']
    image_id = random.choice([i['id'] for i in image_list])
    return image_id


def cinder_get_server_id(self):
    response = nova_api.nova_request(self, 'servers', 'get')
    server_list = json.loads(response.content)['servers']
    server_id = random.choice([i['id'] for i in server_list])
    return server_id


def list_volumes(self):
    return cinder_request(self,
                       'volumes',
                       'get',
                       'cinder_list_volumes')


def list_volumes_detail(self):
    return cinder_request(self,
                       'volumes/detail',
                       'get',
                       'cinder_list_volumes_detail')


def list_volume_detail(self, volume_id=None):
    if not volume_id:
        volume_id = cinder_get_volume_id(self)
    return cinder_request(self,
                         'volumes/%s' % volume_id,
                         'get',
                         'cinder_list_volume_detail',
                         locust_name='volumes/[id]')


def list_volume_types(self):
    return cinder_request(self,
                       'types',
                       'get',
                       'cinder_list_volume_types')


def list_snapshots(self):
    return cinder_request(self, 'snapshots', 'get',
                         'cinder_list_snapshots')


def list_snapshots_detail(self):
    return cinder_request(self,
                         'snapshots/detail',
                         'get',
                         'cinder_list_snapshots_detail')


def list_snapshot_detail(self, snapshot_id=None):
    if not snapshot_id:
        snapshot_id = cinder_get_snapshot_id(self)
    return cinder_request(self,
                         'snapshots/%s' %snapshot_id,
                         'get',
                         'cinder_list_snapshot_detail',
                         locust_name='snapshots/[id]')


def list_images(self):
    return cinder_request(self,
                       'images',
                       'get',
                       'cinder_list_images')


def list_images_detail(self):
    return cinder_request(self,
                       'images/detail',
                       'get',
                       'cinder_list_images_detail')


def list_image_detail(self, image_id=None):
    if not image_id:
        # get available images and randomly
        # choose one
        image_id = cinder_get_image_id(self) 
    return cinder_request(self,
                       'images/%s' % image_id,
                       'get',
                       'cinder_list_image_detail',
                       locust_name='images/[id]')


def list_image_metadata(self, image_id=None):
    if not image_id:
        image_id = cinder_get_image_id(self)
    return cinder_request(self,
                       'images/%s/metadata' % image_id,
                       'get',
                       'cinder_list_image_metadata',
                       locust_name='images/[id]/metadata')


def update_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = cinder_get_image_id(self)
    if not metadata:
        metadata = cinder_get_test_metadata(self)
    data = {"metadata":metadata}
    return cinder_request(self,
                       'images/%s/metadata' % image_id,
                       'post',
                       'cinder_update_image_metadata',
                       data,
                       locust_name='images/[id]/metadata')


def overwrite_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = cinder_get_image_id(self)
    if not metadata:
        metadata = cinder_get_test_metadata(self)
    data = {"metadata":metadata}
    return cinder_request(self,
                       'images/%s/metadata' % image_id,
                       'put',
                       'cinder_overwrite_image_metadata',
                       data,
                       locust_name='images/[id]/metadata')


def create_volume(self,
                  volume_id=None,
                  snapshot_id=None,
                  image_id=None,
                  description=None,
                  size=1,
                  name=None,
                  bootable=False,
                  metadata={}
                  ):
    if not name:
        name = "volume-%s" % uuid.uuid4()
    data = {
           "volume": {
                     "source_volid": volume_id,
                     "snapshot_id": snapshot_id,
                     "description": description,
                     "size": size,
                     "name": name,
                     "imageRef": image_id,
                     "bootable": bootable,
                     "metadata": metadata
                     }
           }
    response = cinder_request(self,
                            'volumes',
                            'post',
                            'cinder_create_volume',
                            data)
    return response


def delete_volume(self, volume_id):
    cinder_request(self,
                'volumes/%s' % volume_id,
                'delete',
                'cinder_delete_volume',
                locust_name='volumes/[id]')

def create_snapshot(self,
                    volume_id=None,
                    name=None,
                    force=False,
                    description=None):
    if not name:
        name = "snapshot-%s" % uuid.uuid4()
    if not volume_id:
        volume_id = get_volume_id(self)
    data = { "snapshot": {
                         "name": name,
                         "description": description,
                         "volume_id": volume_id,
                         "force": force
                         }
           }  
    response = cinder_request(self,
                             'snapshots',
                             'post',
                             'cinder_create_snapshot',
                             data)
    return response


def delete_snapshot(self, snapshot_id):
    cinder_request(self,
                  'snapshots/%s' % snapshot_id,
                  'delete',
                  'cinder_delete_snapshot',
                  locust_name='volumes/[id]')


def resize_server(self, server_id, flavor_id=None):
    data = {
           "resize": {
                     "flavorRef": flavor_id
                     }
           }
    cinder_request(self,
                'servers/%s/action' % server_id,
                'post',
                'cinder_resize_server',
                data,
                locust_name='servers/[resize]/[id]')


def confirm_resize_server(self, server_id):
    data = { "confirmResize": None }
    return cinder_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'cinder_confirm_resize_server',
                       data,
                       locust_name='servers/[confirm_resize]/[id]')


def revert_resize_server(self, server_id):
    data = { "revertResize": None }
    return cinder_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'cinder_resize_server',
                       data,
                       locust_name='servers/[revert_resize]/[id]')


def suspend_server(self, server_id):
    data = { "suspend": None }
    return cinder_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'cinder_suspend_server',
                       data,
                       locust_name='servers/[suspend]/[id]')


def resume_server(self, server_id):
    data = { "resume": None }
    return cinder_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'cinder_resume_server',
                       data,
                       locust_name='servers/[resume]/[id]')


def update_server_metadata(self, server_id=None, metadata=None):
    if not server_id:
        server_id = cinder_get_server_id(self)
    if not metadata:
        metadata = cinder_get_test_metadata(self)
    data = {"metadata":metadata}
    return cinder_request(self,
                       'servers/%s/metadata' % server_id,
                       'post',
                       'cinder_update_server_metadata',
                       data,
                       locust_name='servers/[id]/metadata')


def overwrite_server_metadata(self, server_id=None, metadata=None):
    if not server_id:
        server_id = cinder_get_server_id(self)
    if not metadata:
        metadata = cinder_get_test_metadata(self)
    data = {"metadata":metadata}
    return cinder_request(self,
                       'servers/%s/metadata' % server_id,
                       'put',
                       'cinder_overwrite_server_metadata',
                       data,
                       locust_name='servers/[id]/metadata')


def list_flavors(self):
    return cinder_request(self,
                       'flavors',
                       'get',
                       'cinder_list_flavors')


def create_flavor(self, name=None,
                 ram=128,
                 vcpus=1,
                 disk=0,
                 id='auto',
                 is_public=False):
    data = {
           "flavor": {
                     "name": name,
                     "ram": ram,
                     "vcpus": vcpus,
                     "disk": disk,
                     "id": id,
                     "os-flavor-access:is_public": is_public 
                     }
          }
    return cinder_request(self,
                       'flavors',
                       'post',
                       'cinder_create_flavor',
                       data)


def create_floating_ip(self, pool=None):
    data = {}
    if pool:
        data['pool']= pool
    return cinder_request(self,
                       'os-floating-ips',
                       'post',
                       'cinder_create_floating_ip',
                       data)


def delete_floating_ip(self, floating_ip_id=None):
    if not floating_ip_id:
        floating_ip_id = cinder_get_floating_ip_id(self)
    return cinder_request(self,
                       'os-floating-ips/%s' % floating_ip_id,
                       'delete',
                       'cinder_delete_floating_ip',
                       locust_name='os-floating-ips/[floating-ip-id]') 


def list_floating_ips(self):
    return cinder_request(self,
                        'os-floating-ips',
                        'get',
                        'cinder_list_floating_ips')


def assign_floating_ip(self,
                       server_id=None,
                       floating_ip=None,
                       pool=None):
    if not server_id:
        server_id = cinder_get_server_id(self)
    if not floating_ip:
        floating_ip = cinder_get_floating_ip(self)
    data = {
           "addFloatingIp": {
                            "address": floating_ip 
                            }
           }
    if pool:
        data['addFloatingIp']['pool']=pool
    return cinder_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'cinder_assign_floating_ip',
                       data,
                       locust_name='servers/[server_id]/[assign-floating-ip]')


