clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;
dist:
	flake8

test:
	openfisca-run-test --country-package openfisca_barcelona openfisca_barcelona/tests

test_verbose:
	openfisca-run-test -v --country-package openfisca_barcelona openfisca_barcelona/tests

run:
	openfisca serve --country-package openfisca_barcelona --port 2000

prod-run:
	openfisca serve  --configuration-file production-config/config.py --port ${PORT}

deploy-heroku:
	git push heroku master
