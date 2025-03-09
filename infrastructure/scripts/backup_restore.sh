#!/bin/bash
# Backup and restore utility for Weather Monitoring App

set -eo pipefail

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="backups/$TIMESTAMP"

usage() {
    echo "Usage: $0 [backup|restore] [sqlite|postgres] [file (for restore)]"
    exit 1
}

backup_sqlite() {
    mkdir -p "$BACKUP_DIR"
    cp backend/weather.db "$BACKUP_DIR/weather.db"
    echo "SQLite backup created: $BACKUP_DIR/weather.db"
}

backup_postgres() {
    if [[ -z "$POSTGRES_HOST" || -z "$POSTGRES_USER" || -z "$POSTGRES_DB" ]]; then
        echo "PostgreSQL environment variables not set!"
        exit 1
    fi
    
    mkdir -p "$BACKUP_DIR"
    pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f "$BACKUP_DIR/weather.dump"
    echo "PostgreSQL backup created: $BACKUP_DIR/weather.dump"
}

restore_sqlite() {
    local file=$1
    cp "$file" backend/weather.db
    echo "SQLite database restored from: $file"
}

restore_postgres() {
    local file=$1
    if [[ -z "$POSTGRES_HOST" || -z "$POSTGRES_USER" || -z "$POSTGRES_DB" ]]; then
        echo "PostgreSQL environment variables not set!"
        exit 1
    fi
    
    pg_restore -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "$file"
    echo "PostgreSQL database restored from: $file"
}

case "$1" in
    backup)
        case "$2" in
            sqlite) backup_sqlite ;;
            postgres) backup_postgres ;;
            *) usage ;;
        esac
        ;;
    restore)
        if [[ -z "$3" ]]; then
            echo "Restore file not specified!"
            usage
        fi
        case "$2" in
            sqlite) restore_sqlite "$3" ;;
            postgres) restore_postgres "$3" ;;
            *) usage ;;
        esac
        ;;
    *)
        usage
        ;;
esac