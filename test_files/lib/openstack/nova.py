import os
import json
import string
import random


def nova_request(self,
                 url_detail,
                 request_type='get',
                 request_name=None,
                 data=None,
                 locust_name=None):
    url = self.get_endpoint('compute')
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


def nova_get_flavor_id(self):
    """ Return a random flavor from currently
        available flavors
    """

    response = nova_request(self, 'flavors', 'get')
    flavor_list = json.loads(response.content)['flavors']
    flavor_id = random.choice([i['id'] for i in flavor_list])
    return flavor_id


def nova_get_image_id(self):
    """ Return a random image from currently
        available images
    """

    response = nova_request(self, 'images', 'get')
    image_list = json.loads(response.content)['images']
    image_id = random.choice([i['id'] for i in image_list])
    return image_id


def nova_get_server_id(self):
    response = nova_request(self, 'servers', 'get')
    server_list = json.loads(response.content)['servers']
    server_id = random.choice([i['id'] for i in server_list])
    return server_id


def nova_get_floating_ip(self):
    response = nova_request(self, 'os-floating-ips', 'get')
    ip_list = json.loads(response.content)['floating_ips']
    floating_ip = random.choice([i['ip'] for i in ip_list])
    return floating_ip


def nova_get_floating_ip_id(self):
    response = nova_request(self, 'os-floating-ips', 'get')
    ip_list = json.loads(response.content)['floating_ips']
    floating_ip_id = random.choice([i['id'] for i in ip_list])
    return floating_ip_id


def nova_get_test_metadata(self):
    """ TODO - allow flag + image_id
        if received, then get actual
        metadata (?)
 
    """
    key_counts = [1,1,1,1,1,
                  3,3,3,3,
                  5,5,5,
                  10,
                  100]
    value_pop = string.ascii_uppercase + string.ascii_lowercase + string.digits
    key_count = random.choice(key_counts)
    metadata = {}
    for i in range(key_count):
        key_name = 'key%s' % i
        #value_len = random.randint(0,199)
        value_len = random.choice(key_counts)
        value = ''.join(random.choice(value_pop) for i in range(value_len))
        metadata[key_name] = value
    print metadata
    return metadata


def list_servers(self):
    return nova_request(self,
                       'servers',
                       'get',
                       'nova_list_servers')


def list_servers_detail(self):
    return nova_request(self,
                       'servers/detail',
                       'get',
                       'nova_list_servers_detail')


def list_server_detail(self, server_id=None):
    if not server_id:
        server_id = nova_get_server_id(self)
    return nova_request(self,
                       'servers/%s' % server_id,
                       'get',
                       'nova_list_server_detail',
                       locust_name='servers/[id]')


def list_flavors(self):
    return nova_request(self,
                       'flavors',
                       'get',
                       'nova_list_flavors')


def list_flavors_detail(self):
    return nova_get_request(self, 'flavors/detail')


def list_flavor_detail(self, flavor_id=None):
    if not flavor_id:
        flavor_id = nova_get_flavor_id(self)
    return nova_request(self,
                       'flavors/%s' % flavor_id,
                       'get',
                       'nova_list_flavor_detail',
                       locust_name='flavors/[id]')


def list_limits(self):
    return nova_request(self,
                       'limits',
                       'get',
                       'nova_list_limits')


def list_images(self):
    return nova_request(self,
                       'images',
                       'get',
                       'nova_list_images')


def list_images_detail(self):
    return nova_request(self,
                       'images/detail',
                       'get',
                       'nova_list_images_detail')


def list_image_detail(self, image_id=None):
    if not image_id:
        # get available images and randomly
        # choose one
        image_id = nova_get_image_id(self) 
    return nova_request(self,
                       'images/%s' % image_id,
                       'get',
                       'nova_list_image_detail',
                       locust_name='images/[id]')


def list_image_metadata(self, image_id=None):
    if not image_id:
        image_id = nova_get_image_id(self)
    return nova_request(self,
                       'images/%s/metadata' % image_id,
                       'get',
                       'nova_list_image_metadata',
                       locust_name='images/[id]/metadata')


def update_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = nova_get_image_id(self)
    if not metadata:
        metadata = nova_get_test_metadata(self)
    data = {"metadata":metadata}
    return nova_request(self,
                       'images/%s/metadata' % image_id,
                       'post',
                       'nova_update_image_metadata',
                       data,
                       locust_name='images/[id]/metadata')


def overwrite_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = nova_get_image_id(self)
    if not metadata:
        metadata = nova_get_test_metadata(self)
    data = {"metadata":metadata}
    return nova_request(self,
                       'images/%s/metadata' % image_id,
                       'put',
                       'nova_overwrite_image_metadata',
                       data,
                       locust_name='images/[id]/metadata')


def create_server(self,
                  image_id=None,
                  flavor_id=None,
                  secgroup=None,
                  name=None,
                  max_count=1,
                  min_count=1
                  ):
    if not image_id:
        image_id = nova_get_image_id(self)
    if not flavor_id:
        flavor_id = nova_get_flavor_id(self)
    if not name:
        name = "server-%s" % uuid.uuid4()
    data = {
           "server": {
                     "name": name,
                     "imageRef": image_id,
                     "flavorRef": flavor_id,
                     "max_count": max_count,
                     "min_count": min_count,
                     "security_groups": [
                         {
                         "name": "default"
                         },
                     ]
                     }
           }
    response = nova_request(self,
                            'servers',
                            'post',
                            'nova_create_server',
                            data)
    # TODO: helper code to parse out
    # server_id's to return as a list?
    return response


def delete_server(self, server_id):
    # TODO: random server_id selection?
    nova_request(self,
                'servers/%s' % server_id,
                'delete',
                'nova_delete_server',
                locust_name='servers/[id]')


def reboot_server(self, server_id):
    data = {
           "reboot": {
                     "type": "SOFT"
                     }
           }
    nova_request(self,
                'servers/%s/action' % server_id,
                'post',
                'nova_reboot_server',
                data,
                locust_name='servers/[reboot]/[id]')


def resize_server(self, server_id, flavor_id=None):
    data = {
           "resize": {
                     "flavorRef": flavor_id
                     }
           }
    nova_request(self,
                'servers/%s/action' % server_id,
                'post',
                'nova_resize_server',
                data,
                locust_name='servers/[resize]/[id]')


def confirm_resize_server(self, server_id):
    data = { "confirmResize": None }
    return nova_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'nova_confirm_resize_server',
                       data,
                       locust_name='servers/[confirm_resize]/[id]')


def revert_resize_server(self, server_id):
    data = { "revertResize": None }
    return nova_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'nova_resize_server',
                       data,
                       locust_name='servers/[revert_resize]/[id]')


def pause_server(self, server_id):
    data = { "pause": None }
    return nova_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'nova_pause_server',
                       data,
                       locust_name='servers/[pause]/[id]')


def unpause_server(self, server_id):
    data = { "unpause": None }
    return nova_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'nova_unpause_server',
                       data,
                       locust_name='servers/[unpause]/[id]')


def suspend_server(self, server_id):
    data = { "suspend": None }
    return nova_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'nova_suspend_server',
                       data,
                       locust_name='servers/[suspend]/[id]')


def resume_server(self, server_id):
    data = { "resume": None }
    return nova_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'nova_resume_server',
                       data,
                       locust_name='servers/[resume]/[id]')


def update_server_metadata(self, server_id=None, metadata=None):
    if not server_id:
        server_id = nova_get_server_id(self)
    if not metadata:
        metadata = nova_get_test_metadata(self)
    data = {"metadata":metadata}
    return nova_request(self,
                       'servers/%s/metadata' % server_id,
                       'post',
                       'nova_update_server_metadata',
                       data,
                       locust_name='servers/[id]/metadata')


def overwrite_server_metadata(self, server_id=None, metadata=None):
    if not server_id:
        server_id = nova_get_server_id(self)
    if not metadata:
        metadata = nova_get_test_metadata(self)
    data = {"metadata":metadata}
    return nova_request(self,
                       'servers/%s/metadata' % server_id,
                       'put',
                       'nova_overwrite_server_metadata',
                       data,
                       locust_name='servers/[id]/metadata')


def list_flavors(self):
    return nova_request(self,
                       'flavors',
                       'get',
                       'nova_list_flavors')


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
    return nova_request(self,
                       'flavors',
                       'post',
                       'nova_create_flavor',
                       data)


def create_floating_ip(self, pool=None):
    data = {}
    if pool:
        data['pool']= pool
    return nova_request(self,
                       'os-floating-ips',
                       'post',
                       'nova_create_floating_ip',
                       data)


def delete_floating_ip(self, floating_ip_id=None):
    if not floating_ip_id:
        floating_ip_id = nova_get_floating_ip_id(self)
    return nova_request(self,
                       'os-floating-ips/%s' % floating_ip_id,
                       'delete',
                       'nova_delete_floating_ip',
                       locust_name='os-floating-ips/[floating-ip-id]') 


def list_floating_ips(self):
    return nova_request(self,
                        'os-floating-ips',
                        'get',
                        'nova_list_floating_ips')


def assign_floating_ip(self,
                       server_id=None,
                       floating_ip=None,
                       pool=None):
    if not server_id:
        server_id = nova_get_server_id(self)
    if not floating_ip:
        floating_ip = nova_get_floating_ip(self)
    data = {
           "addFloatingIp": {
                            "address": floating_ip 
                            }
           }
    if pool:
        data['addFloatingIp']['pool']=pool
    return nova_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'nova_assign_floating_ip',
                       data,
                       locust_name='servers/[server_id]/[assign-floating-ip]')


def remove_floating_ip(self,
                       server_id=None,
                       floating_ip=None,
                       pool=None):
    # TODO: make this smarter and try
    # to find any floating ips associated
    # with the specified / selected server
    # tests will need to handle doing things
    # that make sense
    if not server_id:
        server_id = nova_get_server_id(self)
    if not floating_ip:
        floating_ip = nova_get_floating_ip(self)
    data = {
           "removeFloatingIp": {
                               "address": floating_ip
                               }
           }
    return nova_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'nova_remove_floating_ip',
                       data,
                       locust_name='servers/[server_id]/[remove-floating-ip]')


def list_server_actions(self,
                        server_id=None):
    if not server_id:
        server_id = nova_get_server_id(self)
    return nova_request(self,
                       'servers/%s/os-instance-actions' % server_id,
                       'get',
                       'nova_list_server_actions',
                       locust_name='servers/[server_id]/[list-actions]')
