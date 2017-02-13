worker_processes 4;

events { worker_connections 1024; }

http {

        upstream beer-list-api {
              least_conn;
              server beer:5000 weight=10 max_fails=3 fail_timeout=30s;
        }
         
        server {
              listen 80;
         
              location / {
                proxy_pass http://beer-list-api;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
              }
        }
}