# #!/bin/bash
# # Backup and restore utility for Weather Monitoring App

# set -eo pipefail

# TIMESTAMP=$(date +%Y%m%d-%H%M%S)
# BACKUP_DIR="backups/$TIMESTAMP"

# usage() {
#     echo "Usage: $0 [backup|restore] [sqlite|postgres] [file (for restore)]"
#     exit 1
# }

# backup_sqlite() {
#     mkdir -p "$BACKUP_DIR"
#     cp backend/weather.db "$BACKUP_DIR/weather.db"
#     echo "SQLite backup created: $BACKUP_DIR/weather.db"
# }

# backup_postgres() {
#     if [[ -z "$POSTGRES_HOST" || -z "$POSTGRES_USER" || -z "$POSTGRES_DB" ]]; then
#         echo "PostgreSQL environment variables not set!"
#         exit 1
#     fi
    
#     mkdir -p "$BACKUP_DIR"
#     pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f "$BACKUP_DIR/weather.dump"
#     echo "PostgreSQL backup created: $BACKUP_DIR/weather.dump"
# }

# restore_sqlite() {
#     local file=$1
#     cp "$file" backend/weather.db
#     echo "SQLite database restored from: $file"
# }

# restore_postgres() {
#     local file=$1
#     if [[ -z "$POSTGRES_HOST" || -z "$POSTGRES_USER" || -z "$POSTGRES_DB" ]]; then
#         echo "PostgreSQL environment variables not set!"
#         exit 1
#     fi
    
#     pg_restore -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "$file"
#     echo "PostgreSQL database restored from: $file"
# }

# case "$1" in
#     backup)
#         case "$2" in
#             sqlite) backup_sqlite ;;
#             postgres) backup_postgres ;;
#             *) usage ;;
#         esac
#         ;;
#     restore)
#         if [[ -z "$3" ]]; then
#             echo "Restore file not specified!"
#             usage
#         fi
#         case "$2" in
#             sqlite) restore_sqlite "$3" ;;
#             postgres) restore_postgres "$3" ;;
#             *) usage ;;
#         esac
#         ;;
#     *)
#         usage
#         ;;
# esac



























#!/bin/bash
# Local development backup/restore script (SQLite only)

set -eo pipefail

# Configuration
BACKUP_ROOT="infrastructure/backups"  # Changed to infrastructure/backups
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"
MAX_BACKUPS=7  # Keep last 7 backups
DB_FILE="backend/weather.db"
LOG_FILE="$BACKUP_ROOT/backup.log"

# Ensure backup directory exists
mkdir -p "$BACKUP_ROOT"

# Initialize logging
exec > >(tee -a "$LOG_FILE") 2>&1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

validate_sqlite() {
    if ! command -v sqlite3 &> /dev/null; then
        log "Error: sqlite3 not found. Install with 'sudo apt-get install sqlite3'"
        exit 1
    fi
}

backup_sqlite() {
    log "Starting SQLite backup..."
    mkdir -p "$BACKUP_DIR"
    
    # Use SQLite's native backup command
    if sqlite3 "$DB_FILE" ".backup '$BACKUP_DIR/weather.db'"; then
        log "Backup created: $BACKUP_DIR/weather.db"
    else
        log "Backup failed!"
        exit 1
    fi

    # Verify backup integrity
    if sqlite3 "$BACKUP_DIR/weather.db" "PRAGMA integrity_check" | grep -q "ok"; then
        log "Backup verification passed"
    else
        log "Backup verification failed!"
        exit 1
    fi
}

restore_sqlite() {
    local file="$1"
    log "Starting restore from: $file"
    
    if [[ ! -f "$file" ]]; then
        log "Backup file not found!"
        exit 1
    fi

    # Stop services during restore
    log "Stopping services..."
    docker compose stop backend frontend || true

    # Perform safe restore
    if sqlite3 "$DB_FILE" ".restore '$file'"; then
        log "Restore completed successfully"
    else
        log "Restore failed!"
        exit 1
    fi

    # Restart services
    log "Restarting services..."
    docker compose start backend frontend
}

cleanup_old_backups() {
    log "Cleaning up old backups..."
    find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d -printf "%T@ %p\n" | 
    sort -nr | 
    awk -v max="$MAX_BACKUPS" 'NR > max {print $2}' | 
    xargs rm -rf
}

case "$1" in
    backup)
        validate_sqlite
        backup_sqlite
        cleanup_old_backups
        ;;
    restore)
        validate_sqlite
        if [[ -z "$2" ]]; then
            log "Usage: $0 restore <backup_file>"
            exit 1
        fi
        restore_sqlite "$2"
        ;;
    *)
        echo "Usage: $0 <backup|restore> [backup_file]"
        exit 1
        ;;
esac

log "Operation completed successfully"