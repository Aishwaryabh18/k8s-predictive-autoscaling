#!bin/sh
K8S_MASTER_IP=x.x.x.x;
UNDERLAY_IP=x.x.x.x;
sudo mkdir -pm 777 /var/lib/contrail/kafka-logs;
curl https://raw.githubusercontent.com/aj-ya/k8s-tf/master/tf.yaml | sed "s/{{ K8S_MASTER_IP }}/$K8S_MASTER_IP/g; s/{{ VROUTER_GATEWAY }}/$UNDERLAY_IP/g" | kubectl apply -f 
