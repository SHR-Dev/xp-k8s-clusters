import subprocess, threading, logging, sys

services = [
    dict(friendly='git', name='mgmt-gitea-http',port=3000),
    dict(friendly='cicd', name='mgmt-argo-workflows-server',port=2746),
    dict(friendly='registry', name='harbor',port=443)
]
def open_port(service,host_port,target_port,friendly):
    cmd = f"kubectl port-forward service/{service} {host_port}:{target_port}"
    print(f"{friendly} -> localhost:{host_port}")
    while True:
        subprocess.call(cmd.split(' '),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    threads = []
    port = 9000
    for service in services:
        # logging.info(f"starting service {service.get('name')}")
        thread = threading.Thread(
            target=open_port, 
            args=(
                service.get('name'),
                port,
                service.get('port',80),
                service.get('friendly')
            ),
            daemon=True)
        thread.start()
        threads += [thread]
        port += 1

    for t in threads:
        t.join()

    