import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

import task_sets.heat_basic_stress as heat_basic

class HeatBasicTestUser(HttpLocust):
    task_set = heat_basic.HeatBasicStress
    min_wait=500
    max_wait=5000
