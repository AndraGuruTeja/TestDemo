
#!/bin/sh
# PostgreSQL Backup/Restore Script (Alpine-compatible)

set -eo pipefail

# Load environment variables
[ -f /etc/environment ] && . /etc/environment

# Configuration
BACKUP_ROOT="/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_ROOT/weather_backup_$TIMESTAMP.dump"
MAX_BACKUPS=7
LOG_FILE="$BACKUP_ROOT/backup.log"

# Ensure backup directory exists
mkdir -p "$BACKUP_ROOT"

# Initialize logging
exec >> "$LOG_FILE" 2>&1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

validate_postgres() {
    if ! command -v pg_dump >/dev/null 2>&1; then
        log "Error: pg_dump not found. Install PostgreSQL client tools."
        exit 1
    fi
}

backup_postgres() {
    local retries=5
    local delay=5

    log "Starting PostgreSQL backup..."
    for i in $(seq 1 $retries); do
        if PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -F c -f "$BACKUP_FILE"; then
            log "Backup created: $BACKUP_FILE"
            return 0
        else
            log "Attempt $i failed. Retrying in $delay seconds..."
            sleep $delay
        fi
    done

    log "Failed to create backup after $retries attempts."
    exit 1
}

restore_postgres() {
    local backup_file="$1"
    local retries=5
    local delay=5

    log "Starting PostgreSQL restore from $backup_file..."
    
    # Drop existing connections
    PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres \
        -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = '$POSTGRES_DB' AND pid <> pg_backend_pid();"

    for i in $(seq 1 $retries); do
        if PGPASSWORD="$POSTGRES_PASSWORD" pg_restore -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -F c --clean --create "$backup_file"; then
            log "Restore completed successfully"
            return 0
        else
            log "Attempt $i failed. Retrying in $delay seconds..."
            sleep $delay
        fi
    done

    log "Failed to restore after $retries attempts."
    exit 1
}

cleanup_old_backups() {
    log "Cleaning up old backups..."
    find "$BACKUP_ROOT" -name "weather_backup_*.dump" -type f | \
    sort -r | \
    awk -v max="$MAX_BACKUPS" 'NR > max {print $0}' | \
    xargs rm -f
}

case "$1" in
    backup)
        validate_postgres
        backup_postgres
        cleanup_old_backups
        ;;
    restore)
        validate_postgres
        if [ -z "$2" ]; then
            log "Usage: $0 restore <backup_file>"
            exit 1
        fi
        restore_postgres "$2"
        ;;
    *)
        echo "Usage: $0 <backup|restore> [backup_file]"
        exit 1
        ;;
esac

log "Operation completed successfully"