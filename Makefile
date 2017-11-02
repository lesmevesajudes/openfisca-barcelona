clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;
dist:
	flake8

test:
	openfisca-run-test --country-package openfisca_barcelona openfisca_barcelona/tests

run:
	openfisca-serve --port 2000

run_new:
	COUNTRY_PACKAGE=openfisca_barcelona gunicorn "openfisca_web_api_preview.app:create_app()" \
	--bind localhost:5000 --workers 3

prod-run:
	openfisca-serve --port ${PORT}

deploy-heroku:
	git push heroku master