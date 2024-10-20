ENV_PATH = ./config/.env

ifneq (,$(wildcard $(ENV_PATH)))
	include $(ENV_PATH)
	export $(shell sed 's/=.*//' $(ENV_PATH))
endif

DB_DUMP = $(DB_DUMP_PATH)
MEDIA_BACKUP = $(MEDIA_BACKUP_PATH)

MEDIA_DIR = media

.PHONY: resetdb restore restore-db restore-media backup

resetdb:
	export PGPASSWORD=$(DB_PASSWORD); psql -p$(DB_PORT) -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO $(DB_USER); GRANT ALL ON SCHEMA public TO public;"
	python manage.py migrate
	python manage.py init_base

restore: restore-db restore-media
	@echo "Backup restore complete."

restore-db:
	@echo "Cleaning up database..."
	export PGPASSWORD=$(DB_PASSWORD); psql -p$(DB_PORT) -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO $(DB_USER); GRANT ALL ON SCHEMA public TO public;"
	
	@echo "Restoring database..."
	export PGPASSWORD=$(DB_PASSWORD); pg_restore -p$(DB_PORT) -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) --no-owner --no-acl $(DB_DUMP)
	@echo "Database restored from $(DB_DUMP)."

restore-media:
	@echo "Restoring media files..."
	tar -xzvf $(MEDIA_BACKUP) -C $(MEDIA_DIR)

backup:
	@echo "Making database backup..."
	export PGPASSWORD=$(DB_PASSWORD); pg_dump -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -F c -f $(DB_DUMP) --no-owner --no-acl
	@echo "Backup of database saved in $(DB_DUMP)."
	
	@echo "Making media files backup..."
	tar -czvf $(MEDIA_BACKUP) -C $(MEDIA_DIR) .
	@echo "Backup of media files saved in $(MEDIA_BACKUP)."
