resetdatabase:
	docker exec -it merry-postgres psql -p 5432 -U postgres -d postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"
	python src/manage.py migrate
	python src/manage.py init_base
