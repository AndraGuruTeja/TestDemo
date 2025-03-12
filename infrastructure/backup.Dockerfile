
FROM postgres:14-alpine

# Install required tools
RUN apk add --no-cache bash tzdata dcron dos2unix && \
    mkdir -p /scripts /backups && \
    chmod 777 /backups

# Set working directory
WORKDIR /scripts

# Copy backup script
COPY infrastructure/scripts/backup_restore.sh .

# Convert line endings and make executable
RUN dos2unix backup_restore.sh && \
    chmod +x backup_restore.sh

# Setup cron
COPY infrastructure/scripts/backup-cron /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron && \
    touch /var/log/cron.log

# Entrypoint with environment setup
CMD ["sh", "-c", "printenv | grep -E 'POSTGRES_' > /etc/environment && crond -l 8 -f & tail -f /var/log/cron.log"]