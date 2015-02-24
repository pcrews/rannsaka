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


def get_volume_id(self):
    """ Return a random volume from currently
        available volumes
    """

    response = cinder_request(self, 'volumes', 'get')
    volume_list = json.loads(response.content)['volumes']
    volume_id = random.choice([i['id'] for i in volume_list])
    return volume_id


def get_snapshot_id(self):
    """ Return a random snapshot from currently
        available snapshots
    """

    response = cinder_request(self, 'snapshots', 'get')
    snapshot_list = json.loads(response.content)['snapshots']
    snapshot_id = random.choice([i['id'] for i in snapshot_list])
    return snapshot_id


def get_image_id(self):
    """ Return a random image from currently
        available images
    """

    response = nova_api.nova_request(self, 'images', 'get')
    image_list = json.loads(response.content)['images']
    image_id = random.choice([i['id'] for i in image_list])
    return image_id


def get_server_id(self):
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
        volume_id = get_volume_id(self)
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
        snapshot_id = get_snapshot_id(self)
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
        image_id = get_image_id(self)
    return cinder_request(self,
                       'images/%s' % image_id,
                       'get',
                       'cinder_list_image_detail',
                       locust_name='images/[id]')


def list_image_metadata(self, image_id=None):
    if not image_id:
        image_id = get_image_id(self)
    return cinder_request(self,
                       'images/%s/metadata' % image_id,
                       'get',
                       'cinder_list_image_metadata',
                       locust_name='images/[id]/metadata')


def update_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = get_image_id(self)
    if not metadata:
        metadata = get_test_metadata(self)
    data = {"metadata":metadata}
    return cinder_request(self,
                       'images/%s/metadata' % image_id,
                       'post',
                       'cinder_update_image_metadata',
                       data,
                       locust_name='images/[id]/metadata')


def overwrite_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = get_image_id(self)
    if not metadata:
        metadata = get_test_metadata(self)
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


