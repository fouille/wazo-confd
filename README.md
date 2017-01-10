XiVO confd
==========

[![Build Status](https://travis-ci.org/wazo-pbx/xivo-confd.png?branch=master)](https://travis-ci.org/wazo-pbx/xivo-confd)

XiVO CONFD is a web server that provides a [RESTful](http://en.wikipedia.org/wiki/Representational_state_transfer)
service for configuring and managing a Wazo server. Further details on how to use the API can be found on
the [Wazo API web site](http://api.wazo.community)


Installing xivo-confd
---------------------

The server is already provided as a part of [Wazo](http://documentation.wazo.community).
Please refer to [the documentation](http://documentation.wazo.community/en/stable/installation/installsystem.html) for
further details on installing one.


Running unit tests
------------------

```
apt-get install libpq-dev python-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py27
```

Running integration tests
-------------------------

You need Docker installed.

You need the repos xivo-manage-db and xivo-provisioning.

To clone them:

```
git clone https://github.com/wazo-pbx/xivo-manage-db
git clone https://github.com/wazo-pbx/xivo-provisioning
```

If you already have them:

1. ensure they are up-to-date
2. change the values for ``PROVD_DIR`` and ``MANAGE_DB_DIR``

Run the tests:

```
cd integration_tests
pip install -U -r test-requirements.txt
make test-setup PROVD_DIR=../../xivo-provisioning MANAGE_DB_DIR=../../xivo-manage-db
make test
```


Development
-----------

### xivo-dao

In case you need to mount xivo_dao inside the xivo-confd container:

* uncomment the confd volumes in ```integration_tests/assets/base/docker-compose.yml```
* set the environment variable:

```
export LOCAL_GIT_REPOS=/parent/directory/to/all/git/repos
```

### Modified database

If you need to run tests against a modified database schema, run:

```
make update-db MANAGE_DB_DIR=../../xivo-manage-db
```

### Quick multiple runs

If you need to run tests more than once (e.g. when developing):

```
make stop
make start
DOCKER=0 nosetests suite
```
