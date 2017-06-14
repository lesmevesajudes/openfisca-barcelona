clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;
dist:
	flake8

test:
	openfisca-run-test --country_package openfisca_spain openfisca_spain/tests