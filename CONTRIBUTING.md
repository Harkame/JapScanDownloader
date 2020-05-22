# Contributing

## Dependencies

With the exception of [chromedriver][1], this project uses [pipenv][2] to manage
its dependencies.

- add a dependency: `pipenv install myNewDep`
- add a **dev** dependency: `pipenv install --dev myNewDep`
- remove dependency: `pipenv uninstall myNewDep`

Once you are happy with the content of the `Pipfile` file, run the following
tool to synchronize the dependencies to the packaging `setup.py` file:

```console
$ ./tools/update-dependencies.sh
```

## Testing

We use [nose][3] to run our tests:

```console
$ pipenv run nosetests --verbosity=3
```

To also run the slow tests that require network:

```console
$ TEST_ENABLE_NETWORK=1 pipenv run nosetests --verbosity=3
```

[1]: https://chromedriver.chromium.org
[2]: https://pypi.org/project/pipenv
[3]: https://nose.readthedocs.io/en/latest
