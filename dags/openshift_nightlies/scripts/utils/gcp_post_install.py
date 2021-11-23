#!/usr/bin/env python

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import subprocess
import os
import datetime

def _create_workload_machines(cluster_name):
    my_env = os.environ.copy()
    ocm_create_worker_cmd = ["ocm create machinepool -c " +cluster_name +"\
        --instance-type custom-16-65536 --labels \
        'node-role.kubernetes.io/workload='\
        --taints 'role=workload:NoSchedule' --replicas 3 workload"]
    print ocm_create_worker_cmd
    process = subprocess.Popen(ocm_create_worker_cmd, stdout=subprocess.PIPE,\
        stderr=subprocess.PIPE, shell=True, env=my_env)
    stdout, stderr = process.communicate()
    print "creating machine workload"
    print stdout
    print stderr

def _extend_ocm_lifetime(cluster_name):
    my_env = os.environ.copy()
    timestamp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    tomorrow = timestamp.strftime("%Y-%m-%dT%H:%M:%S%ZZ")
    ocm_extend_lifetime_command = ["ocm patch /api/clusters_mgmt/v1/clusters/" + cluster_name \
        + "\'{\"expiration_timestamp\": \"" + tomorrow + "\"}\'"]
    print ocm_extend_lifetime_command
    process = subprocess.Popen(ocm_extend_lifetime_command, stdout=subprocess.PIPE, \
        stderr=subprocess.PIPE, shell=True, env=my_env)
    stdout, stderr = process.communicate()
    print "extending the lifetime of cluster"
    print stdout
    print stderr

