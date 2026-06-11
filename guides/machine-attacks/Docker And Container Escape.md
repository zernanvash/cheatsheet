# Docker And Container Escape

Use after a Linux shell when evidence suggests the user is inside a container or has Docker-related permissions.

## Signals

- Files such as `/.dockerenv`, container hostnames, overlay paths, or restricted process view.
- User belongs to `docker` group.
- Writable `/var/run/docker.sock`.
- Kubernetes/container environment variables or mounted secrets.

## Main Path

```bash
id
ls -la /.dockerenv /var/run/docker.sock 2>/dev/null
cat /proc/1/cgroup
mount
docker ps
docker images
```

If Docker socket/group is available in a lab, inspect whether a host mount can expose proof files or root filesystem access.

## Options To Try

- Search mounted volumes for app configs, credentials, SSH keys, and host paths.
- Check environment variables for service tokens and database credentials.
- Review running containers for internal-only services.
- If Docker CLI is missing but socket exists, use HTTP requests to the socket only in scope.
- Treat Kubernetes secrets and service-account tokens as sensitive and only use them for challenge proof.

## Study Examples

- Sec-Fortress `ZSCTF2`: RCE leads to Docker-based privilege escalation.
- HackMyVM `Pwned`: Docker group membership appears as a Linux escalation route.
