import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

import task_sets.nova_basic_task_set as nova_basic

class NovaBasicTestUser(HttpLocust):
    task_set = nova_basic.NovaRandomStress 
    min_wait=500
    max_wait=5000
    min_server_count=8
    max_server_count=10
