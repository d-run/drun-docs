# d.run Security Whitepaper

The d.run is a computational scheduling and AI open ecosystem platform built on the Kubernetes (K8s) container platform. To ensure the security of the platform, d.run has implemented strict security measures. This whitepaper aims to introduce the platform's security architecture and measures.

## Platform Security Architecture

The d.run adopts a containerized microservice architecture, with application orchestration and management based on Kubernetes. The platform’s security architecture mainly consists of the following parts:

- **Identity Authentication and Access Control**: OAuth2.0 and Role-Based Access Control (RBAC) are used for permission management to ensure that only authorized users can access specific resources.
- **Data Encryption**: All stored and transmitted data are encrypted using AES-256 and TLS 1.3 to prevent data leakage and tampering.
- **Logs and Monitoring**: OpenTelemetry is integrated for comprehensive logging, and Prometheus and Grafana are used for real-time monitoring to ensure traceability of security events.
- **Container Security**: Pod Security Policies limit container permissions, image signing ensures trusted image sources, and runtime security policies prevent malicious code execution.
- **Network Security**: Zero-trust network architecture based on Istio ensures secure communication between microservices, and CNI plugins enhance container network isolation.
- **Model Security**: d.run employs a series of measures to ensure the integrity and trustworthiness of models, especially for large AI models.

## Identity and Access Control

The d.run employs a multi-layer identity authentication mechanism to ensure the security of user identities:

- **OAuth2.0 + OIDC** for Single Sign-On (SSO) authentication, allowing users to securely access multiple services without repeatedly entering credentials.
- **Role-Based Access Control (RBAC)**, allowing administrators to define permissions for different roles, ensuring users can only access resources relevant to their responsibilities.
- **Multi-Factor Authentication (MFA)**, requiring users to provide additional identity verification (such as SMS codes or hardware tokens) to enhance account security.
- **API Access Key Management**, providing short-term tokens and fine-grained permission control to ensure strict API access limitations, preventing unauthorized calls.

## Data Encryption

- **Transmission Encryption**: All API communications are encrypted using TLS 1.3, ensuring that data cannot be intercepted or tampered with during transmission.
- **Storage Encryption**: All stored data is encrypted with AES-256, ensuring data confidentiality, even if disks are stolen or lost, the data remains inaccessible.
- **Key Management**: Kubernetes Secrets and HashiCorp Vault are used for key management, periodically rotating keys and limiting key access.

## Data Backup and Recovery

- **Regular Data Snapshots**: Incremental backups are performed daily, full backups weekly, and stored in multiple geographic regions to prevent data loss.
- **Disaster Recovery (DR) Plan**: Offsite backups and automatic failover strategies are adopted to ensure rapid service recovery in case of a disaster.
- **Data Integrity Checks**: Hash algorithms are used for periodic data integrity verification to prevent tampering or corruption.

## Network Security

The d.run adopts a zero-trust security architecture to ensure the platform's network security:

- **East-West Traffic Security**: Istio Service Mesh uses mTLS (mutual TLS) to encrypt communication between microservices, providing traffic control, authentication, and authorization.
- **North-South Traffic Security**: A Web Application Firewall (WAF) filters malicious traffic, preventing common attacks like SQL injection and XSS.
- **DDoS Protection**: Kubernetes Ingress and CDN are used for traffic cleaning to automatically detect and mitigate Distributed Denial of Service (DDoS) attacks.
- **Firewall Policies**: Kubernetes Network Policy rules restrict access between Pods, ensuring the principle of least privilege.

## Container and Compute Security

The d.run adopts multiple security strategies at the container level to ensure computational security:

- **Image Security**: All container images are scanned with Trivy before deployment to detect known vulnerabilities and apply fixes.
- **Pod Security Policies**: Privileged containers are restricted, and root privileges are avoided to reduce the likelihood of attacks.
- **Sandbox Runtime**: gVisor and Kata Containers are supported to add an additional layer of security between containers and hosts.
- **Real-time Threat Detection**: Falco is used to monitor container runtime behavior, detecting abnormal access, malicious processes, and suspicious network traffic.

## Large Model Security

For AI large models, the d.run has implemented the following security measures:

- **Model Integrity Protection**: Model files are protected with signatures and hash checks to ensure they have not been tampered with.
- **Model Access Control**: RBAC and API access tokens are used to restrict calls to models, preventing unauthorized access.
- **Inference Security**: AI inference tasks are executed in sandbox environments to prevent malicious code from running during inference.
- **Data Privacy Protection**: Homomorphic encryption and differential privacy techniques are used to prevent leakage of AI training data.
- **Adversarial Attack Protection**: Detection and mitigation of adversarial sample attacks to prevent malicious inputs from causing erroneous model inference.

## Monitoring and Auditing

- **Log Collection**: OpenTelemetry is integrated to log all API calls, user actions, and system events to ensure traceability.
- **Security Event Monitoring**: SIEM (Security Information and Event Management) tools analyze logs to detect potential security threats and generate automatic alerts.
- **Anomaly Detection**: AI is used to identify abnormal behaviors, such as unusual logins, privilege escalations, or malicious code execution, and automatically respond.
- **Operational Audits**: All user actions are logged to meet compliance requirements and provide verifiable audit trails.

## Security Certification

The d.run adheres to international and industry security standards and has obtained ISO/IEC 27001:2022 certification.

The d.run employs appropriate security measures that comply with industry standards to ensure the security and stability of the platform in scenarios like computational resource leasing, large model services, and AI application management. We will continue to optimize security mechanisms in the future to address evolving security threats and protect user data and computational security.
