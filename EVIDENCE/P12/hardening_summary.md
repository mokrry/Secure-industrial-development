# P12 Hardening summary

## Dockerfile
- Base image pinned (no `latest`)
- Runs as non-root user
- Healthcheck enabled

## Docker Compose
- app: read_only + no-new-privileges + drop ALL caps + tmpfs /tmp
- db: (planned/implemented) no-new-privileges + drop caps + avoid exposing ports

## IaC (K8s sample)
- runAsNonRoot, allowPrivilegeEscalation: false
- readOnlyRootFilesystem: true + tmp volume for /tmp
- seccompProfile: RuntimeDefault
- drop ALL capabilities
- automountServiceAccountToken: false

## Trivy / next steps
- Review HIGH/CRITICAL
- Update base image / OS packages if needed
- Update python deps if CVEs affect used versions
