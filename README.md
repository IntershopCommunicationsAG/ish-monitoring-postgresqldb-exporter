# ISH-Monitoring-PostgreSQLDB Prometheus Exporter
PostgreSQL Exporter for Prometheus in python. Metrics are scraped by scheduler, and the interval is configurable via environment variable


## Integration
Run `docker-compose up`. When the image is not build yet, please run `docker-compose up --build`

After launching up, metrics show up in `http://localhost:8000/metrics`,
by using promql `{__name__=~".+",app="prometheus-postgresql-exporter"}`

To rebuild the image please run `docker-compose up --build`

The default SQL Server is local. If wanted to test with real data, it has to
either pull the data from production or pointing the SQL Server connection to the production one

## Setting up

##### Initialize a virtual environment

Windows:
```
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

Unix/MacOS:
```
$ python3 -m venv venv
$ source venv/bin/activate
```
Learn more in [the documentation](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

Note: if you are using a python before 3.3, it doesn't come with venv. Install [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) with pip instead.

##### (If you're on a Mac) Make sure xcode tools are installed

```
$ xcode-select --install
```

##### Install the dependencies

```
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Set Environment Variables

Please check `config.py`. `config.py` describes the environment, and
by setting `FLASK_CONFIG`  you can decide which environment to pick up, e.g.

`FLASK_CONFIG=config.TestingConfig`

or

`FLASK_CONFIG=config.DevelopmentConfig`

or

`FLASK_CONFIG=config.ProductionConfig`

## Running the app

```
$ source env/bin/activate
$ python3 manage.py runserver
```

## Formatting code

Before you submit changes, you may want to autoformat your code with `python manage.py format`.

## Development
Add new Metrics by extending `AbstractMetric`,
under `app/prom/metrics`, either `general`, which is related to system
or `business` that is related to business logic.

Check existing examples and the tests before adding them.

Before implementing a metric please go through the tips that ensure you
follow the [official guideline](https://prometheus.io/docs/practices/instrumentation/#things-to-watch-out-for)

In general the rules are:
#### Labels
- Use labels when required to aggregate the metrics, e.g. http status code should be one metrics with several labels(200, 400, 500)
- Do not use labels when cardinality is more than 100 and will increase more in the future

#### Existing metrics
```
# HELP postgresql_lock
# TYPE postgresql_lock gauge
postgresql_lock{database="azure_maintenance",mode="shareupdateexclusivelock"} 0.0
postgresql_lock{database="azure_maintenance",mode="accessexclusivelock"} 0.0
postgresql_lock{database="azure_maintenance",mode="rowsharelock"} 0.0
postgresql_lock{database="azure_maintenance",mode="sharelock"} 0.0
postgresql_lock{database="azure_maintenance",mode="rowexclusivelock"} 0.0
postgresql_lock{database="azure_maintenance",mode="accesssharelock"} 0.0
postgresql_lock{database="azure_maintenance",mode="sharerowexclusivelock"} 0.0
postgresql_lock{database="azure_maintenance",mode="exclusivelock"} 0.0
postgresql_lock{database="azure_sys",mode="exclusivelock"} 0.0
postgresql_lock{database="azure_sys",mode="accesssharelock"} 0.0
postgresql_lock{database="azure_sys",mode="accessexclusivelock"} 0.0
postgresql_lock{database="azure_sys",mode="shareupdateexclusivelock"} 0.0
postgresql_lock{database="azure_sys",mode="sharerowexclusivelock"} 0.0
postgresql_lock{database="azure_sys",mode="rowsharelock"} 0.0
postgresql_lock{database="azure_sys",mode="rowexclusivelock"} 0.0
postgresql_lock{database="azure_sys",mode="sharelock"} 0.0
postgresql_lock{database="grafana_dev",mode="rowsharelock"} 0.0
postgresql_lock{database="grafana_dev",mode="accessexclusivelock"} 0.0
postgresql_lock{database="grafana_dev",mode="exclusivelock"} 0.0
postgresql_lock{database="grafana_dev",mode="sharelock"} 0.0
postgresql_lock{database="grafana_dev",mode="shareupdateexclusivelock"} 0.0
postgresql_lock{database="grafana_dev",mode="sharerowexclusivelock"} 0.0
postgresql_lock{database="grafana_dev",mode="accesssharelock"} 0.0
postgresql_lock{database="grafana_dev",mode="rowexclusivelock"} 0.0
postgresql_lock{database="grafana_prd",mode="exclusivelock"} 0.0
postgresql_lock{database="grafana_prd",mode="rowsharelock"} 0.0
postgresql_lock{database="grafana_prd",mode="accesssharelock"} 0.0
postgresql_lock{database="grafana_prd",mode="sharelock"} 0.0
postgresql_lock{database="grafana_prd",mode="accessexclusivelock"} 0.0
postgresql_lock{database="grafana_prd",mode="sharerowexclusivelock"} 0.0
postgresql_lock{database="grafana_prd",mode="rowexclusivelock"} 0.0
postgresql_lock{database="grafana_prd",mode="shareupdateexclusivelock"} 0.0
postgresql_lock{database="postgres",mode="shareupdateexclusivelock"} 0.0
postgresql_lock{database="postgres",mode="exclusivelock"} 0.0
postgresql_lock{database="postgres",mode="rowexclusivelock"} 0.0
postgresql_lock{database="postgres",mode="rowsharelock"} 0.0
postgresql_lock{database="postgres",mode="sharerowexclusivelock"} 0.0
postgresql_lock{database="postgres",mode="accesssharelock"} 1.0
postgresql_lock{database="postgres",mode="accessexclusivelock"} 0.0
postgresql_lock{database="postgres",mode="sharelock"} 0.0
postgresql_lock{database="template0",mode="accesssharelock"} 0.0
postgresql_lock{database="template0",mode="rowexclusivelock"} 0.0
postgresql_lock{database="template0",mode="accessexclusivelock"} 0.0
postgresql_lock{database="template0",mode="sharerowexclusivelock"} 0.0
postgresql_lock{database="template0",mode="rowsharelock"} 0.0
postgresql_lock{database="template0",mode="exclusivelock"} 0.0
postgresql_lock{database="template0",mode="shareupdateexclusivelock"} 0.0
postgresql_lock{database="template0",mode="sharelock"} 0.0
postgresql_lock{database="template1",mode="sharelock"} 0.0
postgresql_lock{database="template1",mode="accesssharelock"} 0.0
postgresql_lock{database="template1",mode="rowexclusivelock"} 0.0
postgresql_lock{database="template1",mode="shareupdateexclusivelock"} 0.0
postgresql_lock{database="template1",mode="sharerowexclusivelock"} 0.0
postgresql_lock{database="template1",mode="rowsharelock"} 0.0
postgresql_lock{database="template1",mode="exclusivelock"} 0.0
postgresql_lock{database="template1",mode="accessexclusivelock"} 0.0
# HELP postgresql_stat_activity
# TYPE postgresql_stat_activity gauge
postgresql_stat_activity{database="grafana_prd",state="idle"} 3.0
postgresql_stat_activity{database="grafana_dev",state="idle"} 2.0
postgresql_stat_activity{database="postgres",state="active"} 1.0
postgresql_stat_activity{database="template1",state="active"} 0.0
postgresql_stat_activity{database="azure_maintenance",state="active"} 0.0
postgresql_stat_activity{database="azure_sys",state="active"} 0.0
postgresql_stat_activity{database="grafana_prd",state="disabled"} 0.0
postgresql_stat_activity{database="template0",state="idle"} 0.0
postgresql_stat_activity{database="grafana_prd",state="fastpath function call"} 0.0
postgresql_stat_activity{database="template0",state="idle in transaction (aborted)"} 0.0
postgresql_stat_activity{database="template0",state="active"} 0.0
postgresql_stat_activity{database="template1",state="idle"} 0.0
postgresql_stat_activity{database="azure_sys",state="idle in transaction (aborted)"} 0.0
postgresql_stat_activity{database="azure_maintenance",state="idle"} 0.0
postgresql_stat_activity{database="azure_sys",state="idle"} 0.0
postgresql_stat_activity{database="template1",state="idle in transaction (aborted)"} 0.0
postgresql_stat_activity{database="grafana_prd",state="idle in transaction"} 0.0
postgresql_stat_activity{database="azure_maintenance",state="idle in transaction (aborted)"} 0.0
postgresql_stat_activity{database="grafana_dev",state="idle in transaction"} 0.0
postgresql_stat_activity{database="postgres",state="idle in transaction"} 0.0
postgresql_stat_activity{database="grafana_dev",state="fastpath function call"} 0.0
postgresql_stat_activity{database="postgres",state="disabled"} 0.0
postgresql_stat_activity{database="postgres",state="fastpath function call"} 0.0
postgresql_stat_activity{database="grafana_dev",state="disabled"} 0.0
postgresql_stat_activity{database="template0",state="disabled"} 0.0
postgresql_stat_activity{database="grafana_prd",state="idle in transaction (aborted)"} 0.0
postgresql_stat_activity{database="template1",state="idle in transaction"} 0.0
postgresql_stat_activity{database="template0",state="fastpath function call"} 0.0
postgresql_stat_activity{database="azure_maintenance",state="idle in transaction"} 0.0
postgresql_stat_activity{database="azure_sys",state="idle in transaction"} 0.0
postgresql_stat_activity{database="azure_maintenance",state="disabled"} 0.0
postgresql_stat_activity{database="template1",state="disabled"} 0.0
postgresql_stat_activity{database="grafana_prd",state="active"} 0.0
postgresql_stat_activity{database="azure_sys",state="disabled"} 0.0
postgresql_stat_activity{database="template1",state="fastpath function call"} 0.0
postgresql_stat_activity{database="azure_maintenance",state="fastpath function call"} 0.0
postgresql_stat_activity{database="template0",state="idle in transaction"} 0.0
postgresql_stat_activity{database="azure_sys",state="fastpath function call"} 0.0
postgresql_stat_activity{database="grafana_dev",state="active"} 0.0
postgresql_stat_activity{database="grafana_dev",state="idle in transaction (aborted)"} 0.0
postgresql_stat_activity{database="postgres",state="idle"} 0.0
postgresql_stat_activity{database="postgres",state="idle in transaction (aborted)"} 0.0
# HELP postgresql_stat_bgwriter Statistics about the background writer processes activity
# TYPE postgresql_stat_bgwriter gauge
postgresql_stat_bgwriter{type="checkpoints_timed"} 130.0
postgresql_stat_bgwriter{type="checkpoints_req"} 1.0
postgresql_stat_bgwriter{type="checkpoint_write_time"} 288349.0
postgresql_stat_bgwriter{type="checkpoint_sync_time"} 7542.0
postgresql_stat_bgwriter{type="buffers_checkpoint"} 2334.0
postgresql_stat_bgwriter{type="buffers_clean"} 0.0
postgresql_stat_bgwriter{type="maxwritten_clean"} 0.0
postgresql_stat_bgwriter{type="buffers_backend"} 673.0
postgresql_stat_bgwriter{type="buffers_backend_fsync"} 0.0
postgresql_stat_bgwriter{type="buffers_alloc"} 1429.0
postgresql_stat_bgwriter{type="last_stats_reset_min"} 652.0
# HELP postgresql_stat_database Database-wide statistics
# TYPE postgresql_stat_database gauge
postgresql_stat_database{database="postgres",type="numbackends"} 4.0
postgresql_stat_database{database="postgres",type="xact_commit"} 8920.0
postgresql_stat_database{database="postgres",type="blks_read"} 370.0
postgresql_stat_database{database="postgres",type="blks_hit"} 118596.0
postgresql_stat_database{database="postgres",type="tup_returned"} 724957.0
postgresql_stat_database{database="postgres",type="tup_fetched"} 44826.0
postgresql_stat_database{database="postgres",type="tup_inserted"} 1664.0
postgresql_stat_database{database="postgres",type="tup_updated"} 0.0
postgresql_stat_database{database="postgres",type="tup_deleted"} 0.0
postgresql_stat_database{database="postgres",type="conflicts"} 0.0
postgresql_stat_database{database="postgres",type="temp_files"} 0.0
postgresql_stat_database{database="postgres",type="temp_bytes"} 0.0
postgresql_stat_database{database="postgres",type="deadlocks"} 0.0
postgresql_stat_database{database="postgres",type="blk_read_time"} 5580.114
postgresql_stat_database{database="postgres",type="blk_write_time"} 0.053
postgresql_stat_database{database="postgres",type="last_stats_reset_min"} 652.0
postgresql_stat_database{database="template1",type="numbackends"} 0.0
postgresql_stat_database{database="template1",type="xact_commit"} 0.0
postgresql_stat_database{database="template1",type="blks_read"} 0.0
postgresql_stat_database{database="template1",type="blks_hit"} 0.0
postgresql_stat_database{database="template1",type="tup_returned"} 0.0
postgresql_stat_database{database="template1",type="tup_fetched"} 0.0
postgresql_stat_database{database="template1",type="tup_inserted"} 0.0
postgresql_stat_database{database="template1",type="tup_updated"} 0.0
postgresql_stat_database{database="template1",type="tup_deleted"} 0.0
postgresql_stat_database{database="template1",type="conflicts"} 0.0
postgresql_stat_database{database="template1",type="temp_files"} 0.0
postgresql_stat_database{database="template1",type="temp_bytes"} 0.0
postgresql_stat_database{database="template1",type="deadlocks"} 0.0
postgresql_stat_database{database="template1",type="blk_read_time"} 0.0
postgresql_stat_database{database="template1",type="blk_write_time"} 0.0
postgresql_stat_database{database="template0",type="numbackends"} 0.0
postgresql_stat_database{database="template0",type="xact_commit"} 0.0
postgresql_stat_database{database="template0",type="blks_read"} 0.0
postgresql_stat_database{database="template0",type="blks_hit"} 0.0
postgresql_stat_database{database="template0",type="tup_returned"} 0.0
postgresql_stat_database{database="template0",type="tup_fetched"} 0.0
postgresql_stat_database{database="template0",type="tup_inserted"} 0.0
postgresql_stat_database{database="template0",type="tup_updated"} 0.0
postgresql_stat_database{database="template0",type="tup_deleted"} 0.0
postgresql_stat_database{database="template0",type="conflicts"} 0.0
postgresql_stat_database{database="template0",type="temp_files"} 0.0
postgresql_stat_database{database="template0",type="temp_bytes"} 0.0
postgresql_stat_database{database="template0",type="deadlocks"} 0.0
postgresql_stat_database{database="template0",type="blk_read_time"} 0.0
postgresql_stat_database{database="template0",type="blk_write_time"} 0.0
postgresql_stat_database{database="azure_maintenance",type="numbackends"} 0.0
postgresql_stat_database{database="azure_maintenance",type="xact_commit"} 1298.0
postgresql_stat_database{database="azure_maintenance",type="blks_read"} 164.0
postgresql_stat_database{database="azure_maintenance",type="blks_hit"} 46533.0
postgresql_stat_database{database="azure_maintenance",type="tup_returned"} 686703.0
postgresql_stat_database{database="azure_maintenance",type="tup_fetched"} 8210.0
postgresql_stat_database{database="azure_maintenance",type="tup_inserted"} 0.0
postgresql_stat_database{database="azure_maintenance",type="tup_updated"} 0.0
postgresql_stat_database{database="azure_maintenance",type="tup_deleted"} 0.0
postgresql_stat_database{database="azure_maintenance",type="conflicts"} 0.0
postgresql_stat_database{database="azure_maintenance",type="temp_files"} 0.0
postgresql_stat_database{database="azure_maintenance",type="temp_bytes"} 0.0
postgresql_stat_database{database="azure_maintenance",type="deadlocks"} 0.0
postgresql_stat_database{database="azure_maintenance",type="blk_read_time"} 4240.96
postgresql_stat_database{database="azure_maintenance",type="blk_write_time"} 0.0
postgresql_stat_database{database="azure_maintenance",type="last_stats_reset_min"} 651.0
postgresql_stat_database{database="azure_sys",type="numbackends"} 1.0
postgresql_stat_database{database="azure_sys",type="xact_commit"} 1726.0
postgresql_stat_database{database="azure_sys",type="blks_read"} 140.0
postgresql_stat_database{database="azure_sys",type="blks_hit"} 53996.0
postgresql_stat_database{database="azure_sys",type="tup_returned"} 762026.0
postgresql_stat_database{database="azure_sys",type="tup_fetched"} 11043.0
postgresql_stat_database{database="azure_sys",type="tup_inserted"} 0.0
postgresql_stat_database{database="azure_sys",type="tup_updated"} 0.0
postgresql_stat_database{database="azure_sys",type="tup_deleted"} 0.0
postgresql_stat_database{database="azure_sys",type="conflicts"} 0.0
postgresql_stat_database{database="azure_sys",type="temp_files"} 0.0
postgresql_stat_database{database="azure_sys",type="temp_bytes"} 0.0
postgresql_stat_database{database="azure_sys",type="deadlocks"} 0.0
postgresql_stat_database{database="azure_sys",type="blk_read_time"} 4741.025
postgresql_stat_database{database="azure_sys",type="blk_write_time"} 0.0
postgresql_stat_database{database="azure_sys",type="last_stats_reset_min"} 652.0
postgresql_stat_database{database="grafana_dev",type="numbackends"} 2.0
postgresql_stat_database{database="grafana_dev",type="xact_commit"} 111556.0
postgresql_stat_database{database="grafana_dev",type="blks_read"} 286.0
postgresql_stat_database{database="grafana_dev",type="blks_hit"} 5.904134e+06
postgresql_stat_database{database="grafana_dev",type="tup_returned"} 4.789679e+06
postgresql_stat_database{database="grafana_dev",type="tup_fetched"} 2.699337e+06
postgresql_stat_database{database="grafana_dev",type="tup_inserted"} 0.0
postgresql_stat_database{database="grafana_dev",type="tup_updated"} 60.0
postgresql_stat_database{database="grafana_dev",type="tup_deleted"} 0.0
postgresql_stat_database{database="grafana_dev",type="conflicts"} 0.0
postgresql_stat_database{database="grafana_dev",type="temp_files"} 0.0
postgresql_stat_database{database="grafana_dev",type="temp_bytes"} 0.0
postgresql_stat_database{database="grafana_dev",type="deadlocks"} 0.0
postgresql_stat_database{database="grafana_dev",type="blk_read_time"} 3747.079
postgresql_stat_database{database="grafana_dev",type="blk_write_time"} 0.0
postgresql_stat_database{database="grafana_dev",type="last_stats_reset_min"} 652.0
postgresql_stat_database{database="grafana_prd",type="numbackends"} 3.0
postgresql_stat_database{database="grafana_prd",type="xact_commit"} 122009.0
postgresql_stat_database{database="grafana_prd",type="blks_read"} 373.0
postgresql_stat_database{database="grafana_prd",type="blks_hit"} 8.65481e+06
postgresql_stat_database{database="grafana_prd",type="tup_returned"} 5.701508e+06
postgresql_stat_database{database="grafana_prd",type="tup_fetched"} 4.065872e+06
postgresql_stat_database{database="grafana_prd",type="tup_inserted"} 0.0
postgresql_stat_database{database="grafana_prd",type="tup_updated"} 148.0
postgresql_stat_database{database="grafana_prd",type="tup_deleted"} 0.0
postgresql_stat_database{database="grafana_prd",type="conflicts"} 0.0
postgresql_stat_database{database="grafana_prd",type="temp_files"} 0.0
postgresql_stat_database{database="grafana_prd",type="temp_bytes"} 0.0
postgresql_stat_database{database="grafana_prd",type="deadlocks"} 0.0
postgresql_stat_database{database="grafana_prd",type="blk_read_time"} 8486.385
postgresql_stat_database{database="grafana_prd",type="blk_write_time"} 0.0
postgresql_stat_database{database="grafana_prd",type="last_stats_reset_min"} 652.0
# HELP postgresql_stat_database_conflicts Database-wide statistics about query cancels occurring due to conflicts with recovery on standby servers.
# TYPE postgresql_stat_database_conflicts gauge
postgresql_stat_database_conflicts{database="postgres",type="confl_tablespace"} 0.0
postgresql_stat_database_conflicts{database="postgres",type="confl_lock"} 0.0
postgresql_stat_database_conflicts{database="postgres",type="confl_snapshot"} 0.0
postgresql_stat_database_conflicts{database="postgres",type="confl_bufferpin"} 0.0
postgresql_stat_database_conflicts{database="postgres",type="confl_deadlock"} 0.0
postgresql_stat_database_conflicts{database="template1",type="confl_tablespace"} 0.0
postgresql_stat_database_conflicts{database="template1",type="confl_lock"} 0.0
postgresql_stat_database_conflicts{database="template1",type="confl_snapshot"} 0.0
postgresql_stat_database_conflicts{database="template1",type="confl_bufferpin"} 0.0
postgresql_stat_database_conflicts{database="template1",type="confl_deadlock"} 0.0
postgresql_stat_database_conflicts{database="template0",type="confl_tablespace"} 0.0
postgresql_stat_database_conflicts{database="template0",type="confl_lock"} 0.0
postgresql_stat_database_conflicts{database="template0",type="confl_snapshot"} 0.0
postgresql_stat_database_conflicts{database="template0",type="confl_bufferpin"} 0.0
postgresql_stat_database_conflicts{database="template0",type="confl_deadlock"} 0.0
postgresql_stat_database_conflicts{database="azure_maintenance",type="confl_tablespace"} 0.0
postgresql_stat_database_conflicts{database="azure_maintenance",type="confl_lock"} 0.0
postgresql_stat_database_conflicts{database="azure_maintenance",type="confl_snapshot"} 0.0
postgresql_stat_database_conflicts{database="azure_maintenance",type="confl_bufferpin"} 0.0
postgresql_stat_database_conflicts{database="azure_maintenance",type="confl_deadlock"} 0.0
postgresql_stat_database_conflicts{database="azure_sys",type="confl_tablespace"} 0.0
postgresql_stat_database_conflicts{database="azure_sys",type="confl_lock"} 0.0
postgresql_stat_database_conflicts{database="azure_sys",type="confl_snapshot"} 0.0
postgresql_stat_database_conflicts{database="azure_sys",type="confl_bufferpin"} 0.0
postgresql_stat_database_conflicts{database="azure_sys",type="confl_deadlock"} 0.0
postgresql_stat_database_conflicts{database="grafana_dev",type="confl_tablespace"} 0.0
postgresql_stat_database_conflicts{database="grafana_dev",type="confl_lock"} 0.0
postgresql_stat_database_conflicts{database="grafana_dev",type="confl_snapshot"} 0.0
postgresql_stat_database_conflicts{database="grafana_dev",type="confl_bufferpin"} 0.0
postgresql_stat_database_conflicts{database="grafana_dev",type="confl_deadlock"} 0.0
postgresql_stat_database_conflicts{database="grafana_prd",type="confl_tablespace"} 0.0
postgresql_stat_database_conflicts{database="grafana_prd",type="confl_lock"} 0.0
postgresql_stat_database_conflicts{database="grafana_prd",type="confl_snapshot"} 0.0
postgresql_stat_database_conflicts{database="grafana_prd",type="confl_bufferpin"} 0.0
postgresql_stat_database_conflicts{database="grafana_prd",type="confl_deadlock"} 0.0
# HELP postgresql_up PostgreSQL exporter UP status
# TYPE postgresql_up gauge
postgresql_up 1.0
# HELP postgresql_uptime Gauge metric with uptime in days of the Instance.
# TYPE postgresql_uptime gauge
postgresql_uptime 0.0
```

### Build and Push

```
 docker build -t ishcloudopsicp.azurecr.io/intershop/ish-monitoring-postgresqldb-exporter:latest .
 docker push ishcloudopsicp.azurecr.io/intershop/ish-monitoring-postgresqldb-exporter:latest
```