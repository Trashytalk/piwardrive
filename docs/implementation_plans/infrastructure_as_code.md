# Infrastructure as Code (IaC) Implementation Plan

## Overview

This plan outlines the implementation of Infrastructure as Code (IaC) for the PiWardrive project using Terraform, Ansible, and Docker to enable consistent, repeatable, and scalable deployments.

## Phase 1: Terraform Infrastructure Setup

### Step 1: Create Terraform Configuration Structure

```bash
# Create directory structure
mkdir -p infrastructure/terraform/{modules,environments,providers}
mkdir -p infrastructure/terraform/modules/{compute,network,storage,monitoring}
mkdir -p infrastructure/terraform/environments/{development,staging,production}
```

### Step 2: Main Terraform Configuration

```hcl
# infrastructure/terraform/main.tf

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
  
  backend "s3" {
    bucket = "piwardrive-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

# Configure providers
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "PiWardrive"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Variables
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "piwardrive"
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-22.04-lts-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Module calls
module "network" {
  source = "./modules/network"
  
  project_name = var.project_name
  environment  = var.environment
  
  vpc_cidr             = "10.0.0.0/16"
  availability_zones   = data.aws_availability_zones.available.names
  private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnet_cidrs  = ["10.0.101.0/24", "10.0.102.0/24"]
}

module "compute" {
  source = "./modules/compute"
  
  project_name = var.project_name
  environment  = var.environment
  
  vpc_id              = module.network.vpc_id
  private_subnet_ids  = module.network.private_subnet_ids
  public_subnet_ids   = module.network.public_subnet_ids
  
  ami_id        = data.aws_ami.ubuntu.id
  instance_type = var.environment == "production" ? "t3.large" : "t3.medium"
  
  key_name = aws_key_pair.deployer.key_name
}

module "storage" {
  source = "./modules/storage"
  
  project_name = var.project_name
  environment  = var.environment
  
  vpc_id = module.network.vpc_id
}

module "monitoring" {
  source = "./modules/monitoring"
  
  project_name = var.project_name
  environment  = var.environment
  
  vpc_id            = module.network.vpc_id
  private_subnet_ids = module.network.private_subnet_ids
  
  instance_ids = module.compute.instance_ids
}

# Key pair for EC2 instances
resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-${var.environment}-deployer"
  public_key = file("~/.ssh/id_rsa.pub")
}

# Outputs
output "vpc_id" {
  value = module.network.vpc_id
}

output "instance_public_ips" {
  value = module.compute.instance_public_ips
}

output "instance_private_ips" {
  value = module.compute.instance_private_ips
}

output "database_endpoint" {
  value     = module.storage.database_endpoint
  sensitive = true
}

output "monitoring_dashboard_url" {
  value = module.monitoring.dashboard_url
}
```

### Step 3: Network Module

```hcl
# infrastructure/terraform/modules/network/main.tf

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-${var.environment}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.project_name}-${var.environment}-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.project_name}-${var.environment}-public-${count.index + 1}"
    Type = "Public"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.project_name}-${var.environment}-private-${count.index + 1}"
    Type = "Private"
  }
}

# NAT Gateways
resource "aws_eip" "nat" {
  count = length(var.public_subnet_cidrs)
  
  domain = "vpc"
  
  tags = {
    Name = "${var.project_name}-${var.environment}-nat-eip-${count.index + 1}"
  }
  
  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "main" {
  count = length(var.public_subnet_cidrs)
  
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {
    Name = "${var.project_name}-${var.environment}-nat-${count.index + 1}"
  }
  
  depends_on = [aws_internet_gateway.main]
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.project_name}-${var.environment}-public-rt"
  }
}

resource "aws_route_table" "private" {
  count = length(var.private_subnet_cidrs)
  
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
  
  tags = {
    Name = "${var.project_name}-${var.environment}-private-rt-${count.index + 1}"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count = length(var.public_subnet_cidrs)
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count = length(var.private_subnet_cidrs)
  
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# Security Groups
resource "aws_security_group" "web" {
  name        = "${var.project_name}-${var.environment}-web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-${var.environment}-web-sg"
  }
}

resource "aws_security_group" "app" {
  name        = "${var.project_name}-${var.environment}-app-sg"
  description = "Security group for application servers"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-${var.environment}-app-sg"
  }
}

resource "aws_security_group" "db" {
  name        = "${var.project_name}-${var.environment}-db-sg"
  description = "Security group for database"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
  
  tags = {
    Name = "${var.project_name}-${var.environment}-db-sg"
  }
}
```

### Step 4: Compute Module

```hcl
# infrastructure/terraform/modules/compute/main.tf

# Launch Template
resource "aws_launch_template" "app" {
  name_prefix   = "${var.project_name}-${var.environment}-"
  image_id      = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  
  vpc_security_group_ids = [var.app_security_group_id]
  
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    project_name = var.project_name
    environment  = var.environment
  }))
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.project_name}-${var.environment}-app"
    }
  }
  
  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name                = "${var.project_name}-${var.environment}-asg"
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300
  
  min_size         = var.environment == "production" ? 2 : 1
  max_size         = var.environment == "production" ? 6 : 2
  desired_capacity = var.environment == "production" ? 2 : 1
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "${var.project_name}-${var.environment}-asg"
    propagate_at_launch = false
  }
  
  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }
}

# Application Load Balancer
resource "aws_lb" "app" {
  name               = "${var.project_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.web_security_group_id]
  subnets            = var.public_subnet_ids
  
  enable_deletion_protection = var.environment == "production"
  
  tags = {
    Name = "${var.project_name}-${var.environment}-alb"
  }
}

# Target Group
resource "aws_lb_target_group" "app" {
  name     = "${var.project_name}-${var.environment}-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }
  
  tags = {
    Name = "${var.project_name}-${var.environment}-tg"
  }
}

# Load Balancer Listener
resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Auto Scaling Policies
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "${var.project_name}-${var.environment}-scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_policy" "scale_down" {
  name                   = "${var.project_name}-${var.environment}-scale-down"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.app.name
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.project_name}-${var.environment}-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
}

resource "aws_cloudwatch_metric_alarm" "cpu_low" {
  alarm_name          = "${var.project_name}-${var.environment}-cpu-low"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "20"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_down.arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
}
```

### Step 5: User Data Script

```bash
# infrastructure/terraform/modules/compute/user_data.sh

#!/bin/bash
set -e

# Update system
apt-get update -y
apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Install CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i amazon-cloudwatch-agent.deb

# Create application directory
mkdir -p /opt/piwardrive
chown ubuntu:ubuntu /opt/piwardrive

# Create systemd service for PiWardrive
cat > /etc/systemd/system/piwardrive.service << EOF
[Unit]
Description=PiWardrive Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/piwardrive
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
systemctl daemon-reload
systemctl enable piwardrive.service

# Signal that the instance is ready
/opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource AutoScalingGroup --region ${AWS::Region}
```

## Phase 2: Ansible Configuration Management

### Step 1: Create Ansible Directory Structure

```bash
mkdir -p ansible/{inventory,playbooks,roles,group_vars,host_vars}
mkdir -p ansible/roles/{common,docker,piwardrive,monitoring}/{tasks,handlers,templates,files,vars,defaults}
```

### Step 2: Main Ansible Playbook

```yaml
# ansible/playbooks/site.yml

---
- name: Configure PiWardrive Infrastructure
  hosts: all
  become: yes
  gather_facts: yes
  
  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"
  
  roles:
    - common
    - docker
    - piwardrive
    - monitoring
  
  post_tasks:
    - name: Ensure all services are running
      service:
        name: "{{ item }}"
        state: started
        enabled: yes
      loop:
        - docker
        - piwardrive
        - cloudwatch-agent
```

### Step 3: Common Role

```yaml
# ansible/roles/common/tasks/main.yml

---
- name: Install required packages
  package:
    name: "{{ item }}"
    state: present
  loop:
    - curl
    - wget
    - unzip
    - git
    - htop
    - vim
    - fail2ban
    - ufw
    - python3-pip
    - python3-venv

- name: Configure firewall
  ufw:
    rule: "{{ item.rule }}"
    port: "{{ item.port }}"
    proto: "{{ item.proto | default('tcp') }}"
    src: "{{ item.src | default('any') }}"
  loop:
    - { rule: "allow", port: "22" }
    - { rule: "allow", port: "80" }
    - { rule: "allow", port: "443" }
    - { rule: "allow", port: "8080" }
  notify: enable firewall

- name: Create piwardrive user
  user:
    name: piwardrive
    system: yes
    shell: /bin/bash
    home: /opt/piwardrive
    createhome: yes

- name: Create application directories
  file:
    path: "{{ item }}"
    state: directory
    owner: piwardrive
    group: piwardrive
    mode: '0755'
  loop:
    - /opt/piwardrive
    - /opt/piwardrive/data
    - /opt/piwardrive/logs
    - /opt/piwardrive/config
    - /opt/piwardrive/backups

- name: Configure log rotation
  template:
    src: logrotate.j2
    dest: /etc/logrotate.d/piwardrive
    mode: '0644'
```

### Step 4: Docker Role

```yaml
# ansible/roles/docker/tasks/main.yml

---
- name: Install Docker dependencies
  package:
    name: "{{ item }}"
    state: present
  loop:
    - apt-transport-https
    - ca-certificates
    - curl
    - gnupg
    - lsb-release

- name: Add Docker GPG key
  apt_key:
    url: https://download.docker.com/linux/ubuntu/gpg
    state: present

- name: Add Docker repository
  apt_repository:
    repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_lsb.codename }} stable"
    state: present

- name: Install Docker
  package:
    name: "{{ item }}"
    state: present
  loop:
    - docker-ce
    - docker-ce-cli
    - containerd.io

- name: Add users to docker group
  user:
    name: "{{ item }}"
    groups: docker
    append: yes
  loop:
    - ubuntu
    - piwardrive

- name: Install Docker Compose
  get_url:
    url: "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-linux-x86_64"
    dest: /usr/local/bin/docker-compose
    mode: '0755'

- name: Start and enable Docker service
  service:
    name: docker
    state: started
    enabled: yes

- name: Configure Docker daemon
  template:
    src: daemon.json.j2
    dest: /etc/docker/daemon.json
    mode: '0644'
  notify: restart docker
```

### Step 5: PiWardrive Role

```yaml
# ansible/roles/piwardrive/tasks/main.yml

---
- name: Clone PiWardrive repository
  git:
    repo: "{{ piwardrive_repo_url }}"
    dest: /opt/piwardrive/app
    version: "{{ piwardrive_version | default('main') }}"
    force: yes
  become_user: piwardrive
  notify: restart piwardrive

- name: Copy configuration files
  template:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    owner: piwardrive
    group: piwardrive
    mode: "{{ item.mode | default('0644') }}"
  loop:
    - { src: "piwardrive_config.yaml.j2", dest: "/opt/piwardrive/config/piwardrive_config.yaml" }
    - { src: "docker-compose.yml.j2", dest: "/opt/piwardrive/docker-compose.yml" }
    - { src: "env.j2", dest: "/opt/piwardrive/.env", mode: "0600" }
  notify: restart piwardrive

- name: Create systemd service file
  template:
    src: piwardrive.service.j2
    dest: /etc/systemd/system/piwardrive.service
    mode: '0644'
  notify:
    - reload systemd
    - restart piwardrive

- name: Build and start PiWardrive services
  docker_compose:
    project_src: /opt/piwardrive
    build: yes
    state: present
  become_user: piwardrive

- name: Enable and start PiWardrive service
  service:
    name: piwardrive
    state: started
    enabled: yes
```

### Step 6: Monitoring Role

```yaml
# ansible/roles/monitoring/tasks/main.yml

---
- name: Install CloudWatch agent
  get_url:
    url: "https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb"
    dest: /tmp/amazon-cloudwatch-agent.deb

- name: Install CloudWatch agent package
  apt:
    deb: /tmp/amazon-cloudwatch-agent.deb
    state: present

- name: Configure CloudWatch agent
  template:
    src: amazon-cloudwatch-agent.json.j2
    dest: /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
    mode: '0644'
  notify: restart cloudwatch-agent

- name: Start CloudWatch agent
  service:
    name: amazon-cloudwatch-agent
    state: started
    enabled: yes

- name: Install Prometheus Node Exporter
  get_url:
    url: "https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz"
    dest: /tmp/node_exporter.tar.gz

- name: Extract Node Exporter
  unarchive:
    src: /tmp/node_exporter.tar.gz
    dest: /tmp
    remote_src: yes

- name: Install Node Exporter binary
  copy:
    src: /tmp/node_exporter-1.6.1.linux-amd64/node_exporter
    dest: /usr/local/bin/node_exporter
    mode: '0755'
    remote_src: yes

- name: Create node_exporter user
  user:
    name: node_exporter
    system: yes
    shell: /bin/false
    home: /var/lib/node_exporter
    createhome: no

- name: Create systemd service for Node Exporter
  template:
    src: node_exporter.service.j2
    dest: /etc/systemd/system/node_exporter.service
    mode: '0644'
  notify:
    - reload systemd
    - restart node_exporter

- name: Enable and start Node Exporter
  service:
    name: node_exporter
    state: started
    enabled: yes
```

## Phase 3: Container Orchestration with Docker Compose

### Step 1: Production Docker Compose Configuration

```yaml
# docker/docker-compose.production.yml

version: '3.8'

services:
  piwardrive-app:
    build:
      context: ..
      dockerfile: docker/Dockerfile.production
    restart: unless-stopped
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://piwardrive:${DB_PASSWORD}@db:5432/piwardrive
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ../data:/app/data
      - ../logs:/app/logs
      - ../config:/app/config
    networks:
      - piwardrive-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

  piwardrive-webui:
    build:
      context: ..
      dockerfile: docker/Dockerfile.webui
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - piwardrive-app
    volumes:
      - ../config/nginx:/etc/nginx/conf.d
      - ../ssl:/etc/nginx/ssl
    networks:
      - piwardrive-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    restart: unless-stopped
    environment:
      - POSTGRES_DB=piwardrive
      - POSTGRES_USER=piwardrive
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ../config/postgres:/docker-entrypoint-initdb.d
    networks:
      - piwardrive-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U piwardrive"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - piwardrive-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  prometheus:
    image: prom/prometheus:latest
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ../config/prometheus:/etc/prometheus
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    networks:
      - piwardrive-network

  grafana:
    image: grafana/grafana:latest
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ../config/grafana:/etc/grafana/provisioning
    networks:
      - piwardrive-network

  nginx-exporter:
    image: nginx/nginx-prometheus-exporter:latest
    restart: unless-stopped
    ports:
      - "9113:9113"
    command:
      - -nginx.scrape-uri=http://piwardrive-webui/nginx_status
    depends_on:
      - piwardrive-webui
    networks:
      - piwardrive-network

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  piwardrive-network:
    driver: bridge
```

### Step 2: Production Dockerfile

```dockerfile
# docker/Dockerfile.production

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
    g++ \
    make \
    pkg-config \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN useradd --create-home --shell /bin/bash piwardrive

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to application user
RUN chown -R piwardrive:piwardrive /app

# Switch to application user
USER piwardrive

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Command to run the application
CMD ["python", "main.py"]
```

## Phase 4: Kubernetes Configuration (Optional)

### Step 1: Kubernetes Deployment

```yaml
# k8s/deployment.yml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: piwardrive-app
  namespace: piwardrive
  labels:
    app: piwardrive
    component: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: piwardrive
      component: app
  template:
    metadata:
      labels:
        app: piwardrive
        component: app
    spec:
      containers:
      - name: piwardrive
        image: piwardrive:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: piwardrive-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: piwardrive-secrets
              key: redis-url
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: data
          mountPath: /app/data
      volumes:
      - name: config
        configMap:
          name: piwardrive-config
      - name: data
        persistentVolumeClaim:
          claimName: piwardrive-data
```

### Step 2: Kubernetes Service

```yaml
# k8s/service.yml

apiVersion: v1
kind: Service
metadata:
  name: piwardrive-service
  namespace: piwardrive
  labels:
    app: piwardrive
spec:
  selector:
    app: piwardrive
    component: app
  ports:
  - port: 8080
    targetPort: 8080
    protocol: TCP
  type: ClusterIP
```

### Step 3: Kubernetes Ingress

```yaml
# k8s/ingress.yml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: piwardrive-ingress
  namespace: piwardrive
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - piwardrive.example.com
    secretName: piwardrive-tls
  rules:
  - host: piwardrive.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: piwardrive-service
            port:
              number: 8080
```

## Phase 5: CI/CD Pipeline Integration

### Step 1: GitHub Actions for Infrastructure

```yaml
# .github/workflows/infrastructure.yml

name: Infrastructure Deployment

on:
  push:
    branches: [main]
    paths:
      - 'infrastructure/**'
  pull_request:
    branches: [main]
    paths:
      - 'infrastructure/**'

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0
          
      - name: Terraform Format
        run: terraform fmt -check
        working-directory: infrastructure/terraform
        
      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure/terraform
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          
      - name: Terraform Validate
        run: terraform validate
        working-directory: infrastructure/terraform
        
      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: infrastructure/terraform
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply tfplan
        working-directory: infrastructure/terraform
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  
  ansible:
    needs: terraform
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install Ansible
        run: pip install ansible
        
      - name: Run Ansible Playbook
        run: |
          ansible-playbook -i inventory/production playbooks/site.yml
        working-directory: ansible
        env:
          ANSIBLE_HOST_KEY_CHECKING: false
```

This Infrastructure as Code implementation provides:

1. **Terraform Configuration**: Complete infrastructure provisioning for AWS
2. **Ansible Automation**: Configuration management and application deployment
3. **Docker Orchestration**: Production-ready container deployment
4. **Kubernetes Support**: Optional Kubernetes deployment configurations
5. **CI/CD Integration**: Automated infrastructure deployment pipeline
6. **Monitoring Setup**: Integrated monitoring and alerting
7. **Security Configuration**: Proper security groups and access controls
8. **Scalability**: Auto-scaling groups and load balancers

The solution enables consistent, repeatable deployments across multiple environments while maintaining security best practices and monitoring capabilities.
