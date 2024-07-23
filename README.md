# BallParkHousing - MVP

## Start and Enable the Service:

* Reload systemd to recognize the new service:
```sh
sudo systemctl daemon-reload
```
* Start the FastAPI service:

```sh
sudo systemctl start fastapi
```
* Enable the service to start on boot:
```sh
sudo systemctl enable fastapi
```

* Check the logs for any errors:
```sh
sudo journalctl -u fastapi.service -f
```

```sh
sudo systemctl daemon-reload
sudo systemctl restart fastapi
sudo systemctl status fastapi
```

* Test the Nginx configuration and restart Nginx:

```sh
sudo nginx -t
sudo systemctl restart nginx
```