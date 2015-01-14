import os
import json
import string
import random

import nova_v2_base


def heat_request(self,
                 url_detail,
                 request_type='get',
                 request_name=None,
                 data=None,
                 locust_name=None):
    url = self.get_endpoint('orchestration')
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


def get_stack_id(self):
    """ Return a random stack from currently
        available stacks
    """

    response = heat_request(self, 'stacks', 'get')
    stack_list = json.loads(response.content)['stacks']
    stack_id = random.choice([i['id'] for i in stack_list])
    return stack_id


def get_stack_name(self):
    response = heat_request(self, 'stacks', 'get')
    stack_list = json.loads(response.content)['stacks']
    stack_name = random.choice([i['stack_name'] for i in stack_list])
    return stack_name


def get_stack_name_and_id(self):
    # :/
    response = heat_request(self, 'stacks', 'get')
    stack_list = json.loads(response.content)['stacks']
    stack_choice = random.choice(stack_list)
    stack_name = stack_choice['stack_name']
    stack_id = stack_choice['id']
    return stack_name, stack_id


def get_snapshot_id(self, stack_id=None):
    """ Return a random snapshot from currently
        available snapshots
    """

    stack_name, stack_id = get_stack_name_and_id(self)
    url_path = 'stacks/%s/%s/snapshots' % (stack_name, stack_id)
    response = heat_request(self, url_path, 'get', locust_name='stacks/[name]/[id]/snapshots')
    snapshot_list = json.loads(response.content)['snapshots']
    snapshot_id = random.choice([i['id'] for i in snapshot_list])
    return snapshot_id, stack_name, stack_id


def list_stacks(self):
    return heat_request(self,
                       'stacks',
                       'get',
                       'heat_list_stacks')


def find_stack(self, stack_name=None):
    if not stack_name:
        stack_name = get_stack_name(self)
    return heat_request(self,
                       'stacks/%s' % stack_name,
                       'get',
                       'heat_find_stack',
                       locust_name='stacks/[name]')


def list_stack_detail(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                         'stacks/%s/%s' % (stack_name, stack_id),
                         'get',
                         'heat_list_stack_detail',
                         locust_name='stacks/[name]/[id]')


def list_resource_types(self):
    return heat_request(self,
                       'resource_types',
                       'get',
                       'heat_list_resource_types')


def list_snapshots(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                       '%s/%s/snapshots' % (stack_name, stack_id),
                       'get',
                       'heat_list_snapshots',
                       locust_name='stacks/[name]/[id]/snapshots')


def list_snapshot_detail(self, snapshot_id=None):
    if not snapshot_id:
        snapshot_id, stack_name, stack_id = get_snapshot_id(self)
    return heat_request(self,
                       '%s/%s/snapshots/%s' % (stack_name, stack_id, snapshot_id),
                       'get',
                       'heat_list_snapshot_detail',
                       locust_name='stacks/[name]/[id]/snapshots/[snap_id]')


def find_stack_resources(self, stack_name=None):
    if not stack_name:
        stack_name = get_stack_name(self)
    return heat_request(self,
                       'stacks/%s/resources' % stack_name,
                       'get',
                       'heat_find_stack_resources',
                       locust_name='stacks/[name]/resources')


def list_stack_resources(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                       'stacks/%s/%s/resources' % (stack_name, stack_id),
                       'get',
                       'heat_list_stack_resources',
                       locust_name='stacks/[name]/[id]/resources')


def find_stack_events(self, stack_name=None):
    if not stack_name:
        stack_name = get_stack_name(self)
    return heat_request(self,
                       'stacks/%s/events' % stack_name,
                       'get',
                       'heat_find_stack_events',
                       locust_name='stacks/[name]/events')


def list_stack_events(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                       'stacks/%s/%s/events' % (stack_name, stack_id),
                       'get',
                       'heat_list_stack_events',
                       locust_name='stacks/[name]/[id]/events')


def get_stack_template(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                       'stacks/%s/%s/template' % (stack_name, stack_id),
                       'get',
                       'heat_get_stack_template',
                       locust_name='stacks/[name]/[id]/template')

###################################################################################
def update_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = get_image_id(self)
    if not metadata:
        metadata = get_test_metadata(self)
    data = {"metadata":metadata}
    return heat_request(self,
                       'images/%s/metadata' % image_id,
                       'post',
                       'heat_update_image_metadata',
                       data,
                       locust_name='images/[id]/metadata')


def overwrite_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = get_image_id(self)
    if not metadata:
        metadata = get_test_metadata(self)
    data = {"metadata":metadata}
    return heat_request(self,
                       'images/%s/metadata' % image_id,
                       'put',
                       'heat_overwrite_image_metadata',
                       data,
                       locust_name='images/[id]/metadata')


def create_stack(self,
                  stack_id=None,
                  snapshot_id=None,
                  image_id=None,
                  description=None,
                  size=1,
                  name=None,
                  bootable=False,
                  metadata={}
                  ):
    if not name:
        name = "stack-%s" % uuid.uuid4()
    data = {
           "stack": {
                     "source_volid": stack_id,
                     "snapshot_id": snapshot_id,
                     "description": description,
                     "size": size,
                     "name": name,
                     "imageRef": image_id,
                     "bootable": bootable,
                     "metadata": metadata
                     }
           }
    response = heat_request(self,
                            'stacks',
                            'post',
                            'heat_create_stack',
                            data)
    return response


def delete_stack(self, stack_id):
    heat_request(self,
                'stacks/%s' % stack_id,
                'delete',
                'heat_delete_stack',
                locust_name='stacks/[id]')

def create_snapshot(self,
                    stack_id=None,
                    name=None,
                    force=False,
                    description=None):
    if not name:
        name = "snapshot-%s" % uuid.uuid4()
    if not stack_id:
        stack_id = get_stack_id(self)
    data = { "snapshot": {
                         "name": name,
                         "description": description,
                         "stack_id": stack_id,
                         "force": force
                         }
           }  
    response = heat_request(self,
                             'snapshots',
                             'post',
                             'heat_create_snapshot',
                             data)
    return response


def delete_snapshot(self, snapshot_id):
    heat_request(self,
                  'snapshots/%s' % snapshot_id,
                  'delete',
                  'heat_delete_snapshot',
                  locust_name='stacks/[id]')


def resize_server(self, server_id, flavor_id=None):
    data = {
           "resize": {
                     "flavorRef": flavor_id
                     }
           }
    heat_request(self,
                'servers/%s/action' % server_id,
                'post',
                'heat_resize_server',
                data,
                locust_name='servers/[resize]/[id]')


def confirm_resize_server(self, server_id):
    data = { "confirmResize": None }
    return heat_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'heat_confirm_resize_server',
                       data,
                       locust_name='servers/[confirm_resize]/[id]')


def revert_resize_server(self, server_id):
    data = { "revertResize": None }
    return heat_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'heat_resize_server',
                       data,
                       locust_name='servers/[revert_resize]/[id]')


def suspend_server(self, server_id):
    data = { "suspend": None }
    return heat_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'heat_suspend_server',
                       data,
                       locust_name='servers/[suspend]/[id]')


def resume_server(self, server_id):
    data = { "resume": None }
    return heat_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'heat_resume_server',
                       data,
                       locust_name='servers/[resume]/[id]')


def update_server_metadata(self, server_id=None, metadata=None):
    if not server_id:
        server_id = get_server_id(self)
    if not metadata:
        metadata = get_test_metadata(self)
    data = {"metadata":metadata}
    return heat_request(self,
                       'servers/%s/metadata' % server_id,
                       'post',
                       'heat_update_server_metadata',
                       data,
                       locust_name='servers/[id]/metadata')


def overwrite_server_metadata(self, server_id=None, metadata=None):
    if not server_id:
        server_id = get_server_id(self)
    if not metadata:
        metadata = get_test_metadata(self)
    data = {"metadata":metadata}
    return heat_request(self,
                       'servers/%s/metadata' % server_id,
                       'put',
                       'heat_overwrite_server_metadata',
                       data,
                       locust_name='servers/[id]/metadata')


def list_flavors(self):
    return heat_request(self,
                       'flavors',
                       'get',
                       'heat_list_flavors')


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
    return heat_request(self,
                       'flavors',
                       'post',
                       'heat_create_flavor',
                       data)


def create_floating_ip(self, pool=None):
    data = {}
    if pool:
        data['pool']= pool
    return heat_request(self,
                       'os-floating-ips',
                       'post',
                       'heat_create_floating_ip',
                       data)


def delete_floating_ip(self, floating_ip_id=None):
    if not floating_ip_id:
        floating_ip_id = get_floating_ip_id(self)
    return heat_request(self,
                       'os-floating-ips/%s' % floating_ip_id,
                       'delete',
                       'heat_delete_floating_ip',
                       locust_name='os-floating-ips/[floating-ip-id]') 


def list_floating_ips(self):
    return heat_request(self,
                        'os-floating-ips',
                        'get',
                        'heat_list_floating_ips')


def assign_floating_ip(self,
                       server_id=None,
                       floating_ip=None,
                       pool=None):
    if not server_id:
        server_id = get_server_id(self)
    if not floating_ip:
        floating_ip = get_floating_ip(self)
    data = {
           "addFloatingIp": {
                            "address": floating_ip 
                            }
           }
    if pool:
        data['addFloatingIp']['pool']=pool
    return heat_request(self,
                       'servers/%s/action' % server_id,
                       'post',
                       'heat_assign_floating_ip',
                       data,
                       locust_name='servers/[server_id]/[assign-floating-ip]')


