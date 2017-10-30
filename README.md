# OpenFisca Barcelona

[OpenFisca](https://www.openfisca.fr/) package that model Spain legislation from Barcelona point of view. This project 
is intended to be used as a simulator to determine which benefits can be opted by a person or family.

As domain language Catalan has been choosen as all project documentation and team uses this language. We use English in
all non domain specific documentation to enable collaboration with other openfisca teams and developers in general.

## Installing

> We recommend that you [use a virtualenv](https://doc.openfisca.fr/for_developers.html#create-a-virtualenv) 
to install OpenFisca. If you don't, you may need to add `--user` at the end of all commands starting by `pip`.

To install your country package, run:

```
pip install -e ".[test]"
```

You can make sure that everything is working by running the provided tests:

```sh
make test
```

> [Learn more about tests](https://doc.openfisca.fr/coding-the-legislation/writing_yaml_tests.html)


## Serving with the OpenFisca web API

You can plug the OpenFisca web api to your country package.

First, install the OpenFisca web API:
```sh
pip install -e '.[api]'
```

Then run:
```sh
make run
```

You can make sure that the api is working by requesting:

```sh
curl "http://localhost:2000/api/2/formula/edat?data_naixement=1978-01-15"
```

A more complex example, create this file:
```json
{
  "output_format": "variables",
  "scenarios": [
    {
      "test_case": {
        "families": [
          {
            "adults": ["pare1"],
			"menors": ["infant1"]
          }
        ],
        "persones": [
          {
            "id": "pare1",
            "data_naixement": "1961-01-15",
            "ingressos_disponibles": "7000",
            "es_usuari_serveis_socials": true,
            "ciutat_empadronament": "Barcelona"
          },
          {
            "id": "infant1",
            "data_naixement": "2002-01-15",
            "es_usuari_serveis_socials": true,
            "ciutat_empadronament": "Barcelona"
          }
        ]
      },
      "period": "2017-1"
    }
  ],
  "variables": ["AE_230_mensual"]
}
```
and run:
```sh
curl http://localhost:2000/api/1/calculate -X POST --data @./the_file_you_created.json --header 'Content-type: application/json'
```
> [Learn more about the API](https://doc.openfisca.fr/openfisca-web-api/index.html)
