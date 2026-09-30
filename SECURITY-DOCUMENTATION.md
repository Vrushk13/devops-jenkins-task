# DevSecOps Security Documentation

## 1. Project Overview

This project is a Flask application deployed using Docker and Jenkins.

The project uses:

* Python
* Flask
* Docker
* Docker Compose
* Jenkins
* GitHub
* Trivy
* Linux
* UFW Firewall

The purpose of this activity was to improve application and infrastructure security using DevSecOps practices.

---

## 2. Issues Identified and Solutions

| Issue                                                        | Solution                                                                    |
| ------------------------------------------------------------ | --------------------------------------------------------------------------- |
| Docker container was running with root privileges            | Created a non-root `appuser` and configured the Dockerfile to use it        |
| Unnecessary files could be copied into Docker image          | Added `.dockerignore`                                                       |
| Python packages could contain known vulnerabilities          | Updated pip, setuptools and wheel and performed Trivy scanning              |
| Docker image contained vulnerable packages                   | Scanned the image with Trivy and investigated HIGH/CRITICAL vulnerabilities |
| Docker container had unnecessary Linux capabilities          | Added `cap_drop: ALL` in Docker Compose                                     |
| Container could potentially gain additional privileges       | Added `no-new-privileges:true`                                              |
| Container filesystem was writable                            | Added `read_only: true`                                                     |
| Application needed temporary storage                         | Added `/tmp` as a `tmpfs`                                                   |
| Linux firewall was not configured                            | Installed and enabled UFW                                                   |
| Automatic security updates needed verification               | Verified `unattended-upgrades` service                                      |
| Sensitive `/etc/shadow` file permissions needed verification | Checked and confirmed restricted permissions                                |
| Jenkins pipeline needed security scanning                    | Added Trivy image scanning to the CI/CD process                             |

---

## 3. Docker Security Improvements

The Dockerfile was improved by creating a dedicated non-root user.

```dockerfile
RUN useradd --create-home --shell /bin/bash appuser

COPY --chown=appuser:appuser . .

USER appuser
```

This prevents the application from running as the root user inside the container.

The Docker image also updates Python packaging tools:

```dockerfile
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
```

---

## 4. Docker Compose Security

The Docker Compose configuration uses additional security controls:

```yaml
security_opt:
  - no-new-privileges:true

cap_drop:
  - ALL

read_only: true

tmpfs:
  - /tmp

user: "appuser"
```

These settings reduce unnecessary container privileges and limit the impact of a possible container compromise.

The application was exposed on host port `3005` because port `3000` was already being used by Grafana.

The application was verified using:

```bash
curl http://localhost:3005
```

Result:

```text
Application is running successfully
```

---

## 5. Trivy Security Scan

Trivy was used to scan the Docker image for vulnerabilities.

Example command:

```bash
trivy image --scanners vuln --severity HIGH,CRITICAL app-image
```

The scan identified HIGH severity vulnerabilities in the base operating system packages.

No CRITICAL vulnerabilities were reported in the scan performed during this activity.

The scan results can change when the Trivy vulnerability database is updated.

Some Python package findings also required investigation because the reported package metadata did not completely match the packages present in the runtime environment.

The findings were therefore investigated instead of blindly installing or downgrading packages.

---

## 6. Linux Security Hardening

The Linux system was checked and basic hardening was performed.

### Package Updates

```bash
sudo apt update
sudo apt upgrade -y
```

### Automatic Security Updates

The `unattended-upgrades` service was verified as active.

### Firewall

UFW was installed and enabled.

Configured ports included:

```text
22/tcp
8080/tcp
3000/tcp
3005/tcp
```

### File Permissions

`/etc/passwd` was checked:

```text
-rw-r--r-- root root
```

`/etc/shadow` was checked:

```text
-rw-r----- root shadow
```

The `/etc/shadow` file does not provide permissions to other users.

### System Logs

Recent warning-level system logs were reviewed using:

```bash
sudo journalctl -p warning -b --no-pager | tail -20
```

The output contained system/virtualization warnings such as Hyper-V storage messages and time synchronization warnings. These were reviewed as part of the security check.

---

## 7. Jenkins CI/CD Security

The Jenkins CI/CD process was reviewed and improved.

The pipeline performs:

1. Python version check
2. Virtual environment creation
3. Dependency installation
4. Flask application testing
5. Docker image build
6. Trivy security scan

Example security scan:

```bash
trivy image --scanners vuln --severity HIGH,CRITICAL app-image
```

This allows security scanning to be performed as part of the CI/CD process.

---

## 8. DevSecOps Flow

The security-focused CI/CD flow is:

```text
Developer
    |
    v
GitHub
    |
    v
Jenkins
    |
    +---- Build
    |
    +---- Test
    |
    +---- Docker Build
    |
    +---- Trivy Security Scan
    |
    v
Secure Docker Image
    |
    v
Deployment
```

Security checks are included in the development and deployment process instead of being performed only at the end.

---

## 9. Main Lessons Learned

During this activity, I learned:

* How to run Docker containers as a non-root user
* How to reduce Docker container privileges
* How to use `.dockerignore`
* How to scan Docker images using Trivy
* How to investigate vulnerability scan results
* How to configure Docker Compose security options
* How to configure UFW
* How to check Linux file permissions
* How to review Linux system warnings
* How security can be integrated into Jenkins CI/CD
* How DevSecOps combines development, operations and security

---

## 10. Conclusion

The application and development environment were reviewed from a security perspective.

Docker security was improved using a non-root user, reduced Linux capabilities, read-only filesystem settings and temporary storage.

Trivy was used to identify vulnerabilities in the Docker image.

Linux security was improved by updating packages, verifying automatic updates, enabling UFW and checking sensitive file permissions.

The security checks and solutions were documented as part of the DevSecOps activity.
