from kubernetes import client, config

config.load_incluster_config()
apps_v1 = client.AppsV1Api()

def scale_deployment(name, namespace, replicas):
    body = {"spec": {"replicas": replicas}}
    apps_v1.patch_namespaced_deployment_scale(name, namespace, body)