# PiWardrive Deployment Troubleshooting Guide

This guide provides solutions for common deployment issues encountered when setting up PiWardrive in various environments.

## Table of Contents
- [Container Issues](#container-issues)
- [Database Connection Problems](#database-connection-problems)
- [Network Configuration Issues](#network-configuration-issues)
- [Hardware and Driver Issues](#hardware-and-driver-issues)
- [Performance and Resource Issues](#performance-and-resource-issues)
- [Authentication and Security Issues](#authentication-and-security-issues)
- [Monitoring and Logging Issues](#monitoring-and-logging-issues)
- [Backup and Recovery Issues](#backup-and-recovery-issues)
- [Kubernetes-Specific Issues](#kubernetes-specific-issues)
- [Raspberry Pi Specific Issues](#raspberry-pi-specific-issues)

## Container Issues

### Container Won't Start

**Symptoms:**
- Container exits immediately after starting
- "Container exited with code 1" error
- Service fails to initialize

**Diagnosis:**
```bash
# Check container logs
docker logs piwardrive-api

# Inspect container configuration
docker inspect piwardrive-api

# Check resource constraints
docker stats --no-stream
```

**Solutions:**

1. **Check Environment Variables**
   ```bash
   # Verify required environment variables are set
   docker exec piwardrive-api printenv | grep PIWARDRIVE
   
   # Common missing variables:
   # - PIWARDRIVE_SECRET_KEY
   # - PIWARDRIVE_DATABASE_URL
   # - PIWARDRIVE_WIFI_INTERFACE
   ```

2. **Fix Volume Permissions**
   ```bash
   # Fix data directory permissions
   sudo chown -R 1000:1000 /opt/piwardrive/data
   sudo chmod -R 755 /opt/piwardrive/data
   
   # For SELinux systems
   sudo setsebool -P container_manage_cgroup true
   sudo chcon -Rt svirt_sandbox_file_t /opt/piwardrive/data
   ```

3. **Check Resource Limits**
   ```bash
   # Increase memory limits in docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 2G
         cpus: '2.0'
   ```

### Container Networking Issues

**Symptoms:**
- Cannot access web interface
- API endpoints return connection errors
- Services cannot communicate

**Diagnosis:**
```bash
# Test container networking
docker exec piwardrive-api ping piwardrive-db
docker exec piwardrive-api nslookup piwardrive-db

# Check port bindings
docker port piwardrive-api
netstat -tlnp | grep 8080

# Inspect networks
docker network ls
docker network inspect piwardrive_default
```

**Solutions:**

1. **Fix Network Configuration**
   ```yaml
   # docker-compose.yml
   services:
     piwardrive-api:
       ports:
         - "8080:8080"  # Ensure port is exposed
       networks:
         - piwardrive-network
   
   networks:
     piwardrive-network:
       driver: bridge
   ```

2. **Check Firewall Rules**
   ```bash
   # Allow port through firewall
   sudo ufw allow 8080/tcp
   
   # For iptables
   sudo iptables -I INPUT -p tcp --dport 8080 -j ACCEPT
   ```

3. **Verify Host Network Mode**
   ```yaml
   # For Pi deployments requiring privileged access
   services:
     piwardrive:
       network_mode: host
       privileged: true
   ```

## Database Connection Problems

### PostgreSQL Connection Failures

**Symptoms:**
- "Connection refused" errors
- Database timeout errors
- Application cannot start due to DB issues

**Diagnosis:**
```bash
# Test database connectivity
docker exec piwardrive-db psql -U piwardrive -d piwardrive -c "SELECT 1;"

# Check database logs
docker logs piwardrive-db

# Verify database service is running
docker ps | grep postgres
```

**Solutions:**

1. **Check Connection String**
   ```bash
   # Verify DATABASE_URL format
   PIWARDRIVE_DATABASE_URL=postgresql://username:password@hostname:5432/database
   ```

2. **Wait for Database Initialization**
   ```yaml
   # docker-compose.yml - Add health check dependency
   services:
     piwardrive-api:
       depends_on:
         piwardrive-db:
           condition: service_healthy
     
     piwardrive-db:
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U piwardrive"]
         interval: 5s
         timeout: 5s
         retries: 5
   ```

3. **Reset Database**
   ```bash
   # Drop and recreate database
   docker exec piwardrive-db psql -U piwardrive -d piwardrive -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
   
   # Run migrations
   docker exec piwardrive-api python -m piwardrive.migrations.run
   ```

### SQLite Issues

**Symptoms:**
- Database locked errors
- File permission issues
- Corruption warnings

**Solutions:**

1. **Fix File Permissions**
   ```bash
   # Ensure database file is writable
   sudo chown -R 1000:1000 /opt/piwardrive/data/piwardrive.db
   sudo chmod 664 /opt/piwardrive/data/piwardrive.db
   ```

2. **Check Disk Space**
   ```bash
   # Verify sufficient disk space
   df -h /opt/piwardrive/data
   
   # Clean up old data if needed
   docker exec piwardrive-api python -m piwardrive.maintenance.cleanup
   ```

## Network Configuration Issues

### Wi-Fi Interface Not Detected

**Symptoms:**
- No wireless interfaces available
- "Hardware not found" errors
- Monitor mode initialization fails

**Diagnosis:**
```bash
# Check available interfaces
docker exec piwardrive-api ip link show
docker exec piwardrive-api iwconfig

# Test monitor mode capability
docker exec piwardrive-api iw list | grep -A 8 "Supported interface modes"
```

**Solutions:**

1. **Verify Device Access**
   ```yaml
   # docker-compose.yml - Mount device access
   services:
     piwardrive:
       privileged: true
       volumes:
         - /dev:/dev:ro
   ```

2. **Install Required Drivers**
   ```bash
   # Update container with additional drivers
   docker exec piwardrive-api apt-get update
   docker exec piwardrive-api apt-get install -y wireless-tools aircrack-ng
   ```

3. **Check Interface Configuration**
   ```bash
   # Set correct interface in environment
   PIWARDRIVE_WIFI_INTERFACE=wlan1
   
   # Enable monitor mode
   docker exec piwardrive-api airmon-ng start wlan1
   ```

### DNS Resolution Issues

**Symptoms:**
- External API calls fail
- Container-to-container communication fails
- Service discovery not working

**Solutions:**

1. **Configure DNS in Compose**
   ```yaml
   services:
     piwardrive-api:
       dns:
         - 8.8.8.8
         - 8.8.4.4
   ```

2. **Use Custom Network**
   ```yaml
   networks:
     piwardrive-network:
       driver: bridge
       ipam:
         config:
           - subnet: 172.20.0.0/16
   ```

## Hardware and Driver Issues

### USB Device Recognition

**Symptoms:**
- Wi-Fi adapter not recognized
- GPS device not accessible
- Hardware enumeration fails

**Diagnosis:**
```bash
# Check USB devices
lsusb

# Check kernel messages
dmesg | grep -i usb

# Verify device permissions
ls -la /dev/bus/usb/
```

**Solutions:**

1. **Add USB Device Rules**
   ```bash
   # Create udev rule for Wi-Fi adapter
   sudo tee /etc/udev/rules.d/99-piwardrive-usb.rules > /dev/null <<EOF
   SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="8812", MODE="0666"
   EOF
   
   sudo udevadm control --reload-rules
   ```

2. **Enable USB Passthrough**
   ```yaml
   # docker-compose.yml
   services:
     piwardrive:
       devices:
         - /dev/bus/usb:/dev/bus/usb
   ```

### Monitor Mode Issues

**Symptoms:**
- Cannot enable monitor mode
- "Operation not supported" errors
- Packet capture failures

**Solutions:**

1. **Stop Conflicting Services**
   ```bash
   # Stop network manager
   sudo systemctl stop NetworkManager
   
   # Kill interfering processes
   sudo airmon-ng check kill
   ```

2. **Use Correct Interface**
   ```bash
   # Find monitor-capable interface
   iw list | grep -A 8 "Supported interface modes"
   
   # Enable monitor mode
   sudo airmon-ng start wlan1
   ```

## Performance and Resource Issues

### High Memory Usage

**Symptoms:**
- Out of memory errors
- Container restarts frequently
- System becomes unresponsive

**Diagnosis:**
```bash
# Monitor memory usage
docker stats --no-stream

# Check for memory leaks
docker exec piwardrive-api ps aux --sort=-%mem | head -10
```

**Solutions:**

1. **Increase Memory Limits**
   ```yaml
   # docker-compose.yml
   services:
     piwardrive-api:
       deploy:
         resources:
           limits:
             memory: 2G
   ```

2. **Optimize Database Configuration**
   ```bash
   # Reduce database cache size
   echo "shared_buffers = 128MB" >> /opt/piwardrive/postgres/postgresql.conf
   echo "effective_cache_size = 512MB" >> /opt/piwardrive/postgres/postgresql.conf
   ```

3. **Enable Memory Optimization**
   ```bash
   # Set environment variables
   PIWARDRIVE_MEMORY_LIMIT=1G
   PIWARDRIVE_CACHE_SIZE=100MB
   ```

### Disk Space Issues

**Symptoms:**
- "No space left on device" errors
- Database write failures
- Log files filling disk

**Solutions:**

1. **Clean Up Docker Resources**
   ```bash
   # Remove unused containers and images
   docker system prune -a
   
   # Clean up volumes
   docker volume prune
   ```

2. **Configure Log Rotation**
   ```yaml
   # docker-compose.yml
   services:
     piwardrive-api:
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
   ```

3. **Set Data Retention Policies**
   ```bash
   # Configure automatic cleanup
   PIWARDRIVE_DATA_RETENTION_DAYS=30
   PIWARDRIVE_LOG_RETENTION_DAYS=7
   ```

## Authentication and Security Issues

### SSL Certificate Problems

**Symptoms:**
- Browser security warnings
- Certificate verification failures
- HTTPS connection errors

**Solutions:**

1. **Generate Self-Signed Certificate**
   ```bash
   # Create SSL certificate
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   
   # Mount in container
   volumes:
     - ./ssl:/etc/nginx/ssl:ro
   ```

2. **Use Let's Encrypt**
   ```yaml
   services:
     certbot:
       image: certbot/certbot
       volumes:
         - ./ssl:/etc/letsencrypt
       command: certonly --webroot -w /var/www/html -d your-domain.com
   ```

### Authentication Failures

**Symptoms:**
- Login attempts fail
- Token validation errors
- Session timeouts

**Solutions:**

1. **Reset Admin Password**
   ```bash
   # Reset via container command
   docker exec piwardrive-api python -m piwardrive.auth.reset_password admin
   ```

2. **Check JWT Configuration**
   ```bash
   # Verify JWT secret is set
   docker exec piwardrive-api printenv | grep JWT
   
   # Generate new secret if needed
   PIWARDRIVE_JWT_SECRET=$(openssl rand -hex 32)
   ```

## Monitoring and Logging Issues

### Prometheus Metrics Issues

**Symptoms:**
- Metrics not appearing in Prometheus
- Grafana dashboards empty
- Monitoring alerts not firing

**Solutions:**

1. **Verify Metrics Endpoint**
   ```bash
   # Test metrics endpoint
   curl http://localhost:8080/metrics
   
   # Check Prometheus configuration
   docker exec prometheus cat /etc/prometheus/prometheus.yml
   ```

2. **Fix Prometheus Configuration**
   ```yaml
   # prometheus.yml
   scrape_configs:
     - job_name: 'piwardrive'
       static_configs:
         - targets: ['piwardrive-api:8080']
   ```

### Log Aggregation Issues

**Symptoms:**
- Logs not appearing in centralized system
- Log parsing errors
- Missing log entries

**Solutions:**

1. **Configure Log Format**
   ```yaml
   # docker-compose.yml
   services:
     piwardrive-api:
       environment:
         - PIWARDRIVE_LOG_FORMAT=json
   ```

2. **Fix Log Shipping**
   ```bash
   # Check log driver configuration
   docker info | grep "Logging Driver"
   
   # Restart with correct logging
   docker-compose down
   docker-compose up -d
   ```

## Backup and Recovery Issues

### Database Backup Failures

**Symptoms:**
- pg_dump command fails
- Backup files corrupted
- Insufficient permissions

**Solutions:**

1. **Fix Backup Script**
   ```bash
   #!/bin/bash
   # backup.sh
   BACKUP_DIR="/opt/piwardrive/backups"
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   
   mkdir -p "$BACKUP_DIR"
   
   # Backup with proper error handling
   docker exec piwardrive-db pg_dump -U piwardrive piwardrive | gzip > "$BACKUP_DIR/postgres_$TIMESTAMP.sql.gz"
   
   if [ $? -eq 0 ]; then
     echo "Backup completed successfully"
   else
     echo "Backup failed" >&2
     exit 1
   fi
   ```

2. **Verify Backup Integrity**
   ```bash
   # Test backup file
   gunzip -t /opt/piwardrive/backups/postgres_*.sql.gz
   
   # Test restore process
   gunzip -c backup.sql.gz | docker exec -i piwardrive-db psql -U piwardrive -d piwardrive_test
   ```

## Kubernetes-Specific Issues

### Pod Scheduling Issues

**Symptoms:**
- Pods stuck in "Pending" state
- Resource constraints errors
- Node affinity issues

**Solutions:**

1. **Check Resource Requests**
   ```yaml
   # deployment.yaml
   spec:
     containers:
     - name: piwardrive-api
       resources:
         requests:
           memory: "512Mi"
           cpu: "250m"
         limits:
           memory: "1Gi"
           cpu: "500m"
   ```

2. **Verify Node Resources**
   ```bash
   # Check node capacity
   kubectl describe nodes
   
   # Check resource usage
   kubectl top nodes
   ```

### Service Discovery Issues

**Symptoms:**
- Services cannot communicate
- DNS resolution failures
- Connection timeouts

**Solutions:**

1. **Check Service Configuration**
   ```yaml
   # service.yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: piwardrive-api
   spec:
     selector:
       app: piwardrive-api
     ports:
     - port: 8080
       targetPort: 8080
   ```

2. **Test Service Discovery**
   ```bash
   # Test DNS resolution
   kubectl exec -it piwardrive-api -- nslookup piwardrive-db
   
   # Check service endpoints
   kubectl get endpoints piwardrive-api
   ```

## Raspberry Pi Specific Issues

### GPIO Access Issues

**Symptoms:**
- Cannot access GPIO pins
- Hardware control failures
- Permission denied errors

**Solutions:**

1. **Enable GPIO Access**
   ```yaml
   # docker-compose.pi.yml
   services:
     piwardrive:
       privileged: true
       volumes:
         - /dev/gpiomem:/dev/gpiomem
   ```

2. **Add User to GPIO Group**
   ```bash
   # Add user to gpio group
   sudo usermod -a -G gpio pi
   ```

### Power Management Issues

**Symptoms:**
- Unexpected shutdowns
- USB device disconnections
- System instability

**Solutions:**

1. **Check Power Supply**
   ```bash
   # Monitor power supply voltage
   vcgencmd measure_volts core
   
   # Check for under-voltage warnings
   vcgencmd get_throttled
   ```

2. **Disable USB Power Management**
   ```bash
   # Disable USB power saving
   echo 'ACTION=="add", SUBSYSTEM=="usb", ATTR{power/autosuspend}="-1"' | sudo tee /etc/udev/rules.d/50-usb-power.rules
   ```

### SD Card Issues

**Symptoms:**
- Read-only filesystem errors
- Corruption warnings
- Performance degradation

**Solutions:**

1. **Check SD Card Health**
   ```bash
   # Check filesystem
   sudo fsck /dev/mmcblk0p2
   
   # Check for bad blocks
   sudo badblocks -v /dev/mmcblk0p2
   ```

2. **Optimize for SD Card**
   ```bash
   # Reduce writes to SD card
   echo "tmpfs /tmp tmpfs defaults,noatime,nosuid,size=100m 0 0" >> /etc/fstab
   echo "tmpfs /var/tmp tmpfs defaults,noatime,nosuid,size=30m 0 0" >> /etc/fstab
   ```

## General Troubleshooting Steps

### Systematic Approach

1. **Check System Status**
   ```bash
   # Overall system health
   docker-compose ps
   docker stats --no-stream
   
   # Check logs
   docker-compose logs --tail=50
   ```

2. **Verify Configuration**
   ```bash
   # Environment variables
   docker-compose config
   
   # Network configuration
   docker network ls
   docker network inspect <network_name>
   ```

3. **Test Connectivity**
   ```bash
   # Internal service communication
   docker exec piwardrive-api ping piwardrive-db
   
   # External connectivity
   docker exec piwardrive-api ping 8.8.8.8
   ```

4. **Check Resource Usage**
   ```bash
   # Container resources
   docker stats
   
   # Host resources
   free -h
   df -h
   ```

### Getting Help

When seeking help, provide:
- **Environment details** (OS, Docker version, hardware)
- **Error messages** (full logs, not just snippets)
- **Configuration files** (docker-compose.yml, .env)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**

**Support Resources:**
- 📖 **Documentation**: [docs/](../docs/)
- 💬 **Community**: [GitHub Discussions](https://github.com/username/piwardrive/discussions)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/username/piwardrive/issues)
- 📧 **Support**: support@piwardrive.com

---

*This troubleshooting guide is continuously updated based on common issues reported by the community. If you encounter an issue not covered here, please contribute by documenting your solution.*
