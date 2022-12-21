apiVersion: v1
kind: ConfigMap
metadata:
  name: vault
data:
  init.sh: |
    #!/bin/sh
    until ps -o comm | grep -q vault
    do
        echo "Waiting" 
        sleep 1
    done

    vault operator init -n 1 -t 1 > /tmp/output.txt
    unseal=$(cat /tmp/output.txt | grep "Unseal Key 1:" | sed -e "s/Unseal Key 1: //g")
    root=$(cat /tmp/output.txt | grep "Initial Root Token:" | sed -e "s/Initial Root Token: //g")
    vault operator unseal ${unseal?}

    vault login -no-print ${root?}
    vault auth enable kubernetes
    vault write auth/kubernetes/config \
        token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
        kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
        kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    vault secrets enable -path=secret kv-v2
    vault policy write crossplane - <<EOF
        path "secret/data/*" {
            capabilities = ["create", "read", "update", "delete"]
        }
        path "secret/metadata/*" {
            capabilities = ["create", "read", "update", "delete"]
        }
    EOF

    vault write auth/kubernetes/role/crossplane \
        bound_service_account_names="*" \
        bound_service_account_namespaces=default \
        policies=crossplane \
        ttl=24h
