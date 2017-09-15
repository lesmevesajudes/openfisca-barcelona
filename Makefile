clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;
dist:
	flake8

test:
	openfisca-run-test --country_package openfisca_spain openfisca_spain/tests

run:
	openfisca-serve --port 2000

prod-run:
    openfisca-serve --port 80

deploy-heroku:
    git push heroku master