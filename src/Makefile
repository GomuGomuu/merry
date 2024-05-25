resetdb:
	export PGPASSWORD="postgres"; psql -p5432 -h merry-postgres -U postgres -d postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"
	python manage.py migrate
	python manage.py init_base