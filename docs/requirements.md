# Wiz Technical Exercise – Requirements Mapping

This document tracks the official Wiz Technical Exercise v4 requirements and how this project satisfies them.[file:1]

---

## 1. Web Application Environment

### 1.1 Two-tier web application

- Requirement:
  - Deploy a two-tier web application (front-end + database) using several cloud services with intentional configuration weaknesses.[file:1]
- Implementation:
  - Front-end: Containerized web application running on AWS EKS (Kubernetes) in private subnets.
  - Database: MongoDB running on an EC2 virtual machine in the same VPC.

---

## 2. Virtual Machine with MongoDB Database Server

### 2.1 Outdated Linux VM

- Requirement:
  - VM should use a Linux OS version that is at least 1+ years out of date.[file:1]
  - SSH must be exposed to the public internet.[file:1]
  - VM should be granted overly permissive cloud permissions (e.g., able to create VMs).[file:1]
- Implementation plan:
  - Launch EC2 with an older Linux AMI.
  - Security group: inbound SSH (22) from 0.0.0.0/0 (intentional misconfiguration).
  - Attach an overly permissive IAM role (e.g., EC2FullAccess, S3FullAccess or similar).

### 2.2 Outdated MongoDB

- Requirement:
  - MongoDB version must be at least 1+ years out of date.[file:1]
  - Database access must:
    - Be restricted to Kubernetes network access only.
    - Require database authentication.[file:1]
- Implementation plan:
  - Install an older supported MongoDB version on the EC2 instance.
  - Create an application database and user.
  - Use security groups so port 27017 only accepts traffic from EKS worker node security groups.

### 2.3 Automated database backups to object storage

- Requirement:
  - MongoDB must be automatically backed up daily to cloud object storage.
  - Object storage must allow public read and listing (intentional misconfiguration).[file:1]
- Implementation plan:
  - Use `mongodump` on EC2 and a cron job to create daily backups.
  - Upload backups to an S3 bucket.
  - Configure the S3 bucket to allow public read and list access.

---

## 3. Web Application on Kubernetes

### 3.1 Kubernetes cluster networking

- Requirement:
  - Kubernetes cluster must be deployed in a private subnet.[file:1]
- Implementation plan:
  - Deploy EKS worker nodes into private subnets in the VPC.
  - Use a public Application Load Balancer to expose the application.

### 3.2 Application and MongoDB integration

- Requirement:
  - Web application must be containerized and the image must be (re)built by me.
  - Application must use the MongoDB database.
  - MongoDB connection must be configured via an environment variable in Kubernetes.[file:1]
- Implementation plan:
  - Build a simple Mongo-backed web app (e.g., todo list).
  - Store MongoDB connection string (MONGO_URI) as an environment variable sourced from a Secret/ConfigMap in the Deployment.

### 3.3 wizexercise.txt in container image

- Requirement:
  - The container image must contain a file called `wizexercise.txt` that includes my name.
  - I must show how I added the file and prove it exists in the running container.[file:1]
- Implementation plan:
  - Update Dockerfile to create or copy `wizexercise.txt` into the image at build time.
  - During the demo, run `kubectl exec` into a pod and `cat /wizexercise.txt` to verify.

### 3.4 Kubernetes permissions and exposure

- Requirements:
  - Container application must be assigned a cluster-wide Kubernetes admin role and privilege (intentional over-privilege).[file:1]
  - Application must be exposed via a Kubernetes Ingress and cloud provider load balancer.[file:1]
  - Must be able to demonstrate `kubectl` CLI.
  - Must show that web app data is stored in the MongoDB database.[file:1]
- Implementation plan:
  - Create a ServiceAccount for the app and bind it to `cluster-admin` via a ClusterRoleBinding.
  - Create a Service + Ingress that uses an AWS ALB to expose the app publicly.
  - Use `kubectl get`, `logs`, `exec` during the demo.
  - Insert data via the web app and confirm it in MongoDB from the EC2 instance.

---

## 4. Dev(Sec)Ops Requirements

*(Scope may vary by role; some items are bonus but planned.)*[file:1]

### 4.1 VCS / SCM

- Requirement:
  - Push code and configuration to a VCS/SCM (GitHub, GitLab, ADO, etc.).[file:1]
- Implementation:
  - This repository (e.g., GitHub) contains:
    - `app/` – application source and Dockerfile.
    - `k8s/` – Kubernetes manifests.
    - `infra/` – infrastructure code and notes.
    - `docs/` – documentation and diagrams.

### 4.2 CI/CD pipelines

- Requirements:
  - One pipeline to securely deploy infrastructure as code (IaC).
  - One pipeline to build and push the application image and trigger Kubernetes deployment.[file:1]
- Implementation plan:
  - Infra pipeline:
    - Terraform/CloudFormation in `infra/` to create VPC, EKS, EC2, S3, and IAM.
  - App pipeline:
    - Build Docker image from `app/`, scan it, push to ECR, then apply Kubernetes manifests in `k8s/`.

### 4.3 Pipeline security

- Requirement:
  - Implement security controls in the VCS platform:
    - Protect the repository.
    - Scan IaC and container images before deployment.[file:1]
- Implementation plan:
  - Add IaC scanning (e.g., Checkov) on `infra/`.
  - Add image scanning (e.g., Trivy) in the app pipeline before deploy.

### 4.4 Optional simulated attack

- Requirement (optional):
  - Run a simulated attack or behavior in the cloud environment / pipelines to show effectiveness of controls.[file:1]
- Implementation idea:
  - From the over-privileged pod, attempt to use its IAM permissions (e.g., list S3 buckets) and show Security Hub/CloudTrail findings.

---

## 5. Cloud-Native Security Controls

### 5.1 Control plane audit logging

- Requirement:
  - Configure control plane audit logging for the cloud environment.[file:1]
- Implementation plan:
  - Enable EKS control plane logs (audit, api) to CloudWatch Logs.
  - Ensure CloudTrail is enabled for AWS account API activity.

### 5.2 Preventative controls

- Requirement:
  - Implement at least one preventative cloud control.[file:1]
- Implementation ideas:
  - Use AWS Config rules or S3 Block Public Access (and show how the backup bucket violates best practices).
  - Alternatively, use an IAM or org-level control as a “policy guardrail” and discuss how it would normally block some misconfigs.

### 5.3 Detective controls

- Requirement:
  - Implement at least one detective cloud control and demonstrate its impact.[file:1]
- Implementation plan:
  - Enable AWS Config and/or Security Hub/GuardDuty.
  - Highlight findings related to:
    - Public S3 bucket for MongoDB backups.
    - Security group with SSH open to 0.0.0.0/0.

---

## 6. Presentation Expectations

- Requirement:
  - 45-minute presentation + demo, plus Q&A.[file:1]
  - Use a mix of slides and live walkthrough.
  - Show infrastructure functioning.
  - Explain approach, challenges, and adaptations.
  - Detail weak configurations and consequences (for technical roles).
  - Demonstrate security tooling value (for security-focused roles).[file:1]
- Implementation plan:
  - Slides:
    - Architecture diagram.
    - Requirements mapping (based on this document).
    - Misconfigurations and risks.
    - Security controls and coverage.
  - Demo:
    - Web app via ALB.
    - Data flowing into MongoDB.
    - S3 backups visibility.
    - `kubectl` usage and `wizexercise.txt`.
    - Security tooling (CloudTrail/Config/Security Hub).

