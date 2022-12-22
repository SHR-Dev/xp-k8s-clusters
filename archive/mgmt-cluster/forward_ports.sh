(while [ 1 ]; do kubectl port-forward service/harbor 9002:80; done) &
(while [ 1 ]; do kubectl port-forward service/mgmt-argo-workflows-server 9001:2746) &
(while [ 1 ]; do kubectl port-forward service/mgmt-gitea-http 9000:3000) &