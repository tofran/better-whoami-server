# Better whoami server

Simple multi-arch Docker image used to test deployments, infra, services, etc.  
It exposes system and request information via a HTTP API.  
I used to use the classic whoami image, but I always felt it lacked:  

- Information about the request connection (ex: connecting ip);
- Internet connectivity checks;
- Way to expose environment variables.
- Info about the server resources (disk, ram, cpu, etc).

Which is exactly what this image does.

## Usage

```
docker run -p 8000:8000 ghcr.io/tofran/better-whoami
# or
docker run -p 8000:8000 tofran/better-whoami
```

And your server with interactive docs will be running at `localhost:8000/`.

<img width="1130" alt="Docs preview" src="https://github.com/user-attachments/assets/5de390d4-7252-4442-9e67-17f4d2c653cf" />
<br>

Example: retrieval of env vars

```
# curl -s http://localhost:8000/envs | jq
{
  "PATH": "/app/.venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  "HOSTNAME": "ed3c3afc7bd7",
  "GPG_KEY": "7169605F62C751356D054A26A821E680E5FA6305",
  "PYTHON_VERSION": "3.13.3",
  "PYTHON_SHA256": "40f868bcbdeb8149a3149580bb9bfd407b3321cd48f0be631af955ac92c0e041",
  "PYTHONUNBUFFERED": "1",
  "VIRTUAL_ENV": "/app/.venv",
  "APP_VERSION": "0.0.1-untagged",
  "HOME": "/root",
  "LC_CTYPE": "C.UTF-8"
}
```


## License

MIT
