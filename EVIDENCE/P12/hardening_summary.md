# P12 Hardening summary

## Dockerfile
- Base image pinned (python:3.11-slim), no `latest`
- Runs as non-root user (`appuser`)
- Healthcheck on `/health`

## IaC (k8s пример)
- `runAsNonRoot`, `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`
- Drop all Linux capabilities
- `seccompProfile: RuntimeDefault`
- `automountServiceAccountToken: false`

## Next steps
- Review Trivy findings and upgrade base image/packages if needed
- Move DB credentials to Secret/External config (don’t keep passwords in plain env in manifests)
