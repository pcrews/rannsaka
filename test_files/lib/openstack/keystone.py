import json

def get_auth_token(self):
        url = 'http://192.168.0.5:5000/v2.0/tokens'
        headers = {'Content-Type': 'application/json',
                   #'Accept': 'application/json'}
                   'Accept': 'application/json',
                   'X-Auth-Project-Id': "%s" % self.keystone_tenant}
        auth_json = {"auth": {
                             "tenantName": "%s" % self.keystone_tenant,
                             "passwordCredentials": {
                                                    "username": "%s" % self.keystone_user,
                                                    "password": "%s" % self.keystone_pw
                                                     }
                             }
                    } 
        response = self.client.post(url, data=json.dumps(auth_json), headers=headers)
        print response.content
        data = json.loads(response.content)
        auth_token = data['access']['token']['id']
        tenant_id =  data['access']['token']['tenant']['id']       
        service_catalog = data['access']['serviceCatalog']
        return auth_token, tenant_id, service_catalog

