Using BASH, navigate to orca-data-to-db/orca-data-to-db/src/ directory. Then, run the command "docker compose --env-file dev.env up", which will start the Docker containers for Mage, PostgreSQL, and pgAdmin.

From there, execute the script "orca_data_to_postgres.py". This should move the ORCA data in your specified .csv files (as produced by https://github.com/pmwaddell/orca-data-extraction) into Postgres. The script will attempt to concatenate all .csv files in the current directory into a single table.

The data can be viewed in Postgres from pgAdmin at localhost:8080, using the login information specified in the dev.env file and registering the appropriate server by giving the host name, username and password from the dev.env file (the default port of 5432 should work). 

Mage can be accessed from localhost:6789. To configure the connection to GCP, create a project and associated Service Account with appropriate Permissions (e.g., BigQuery Admin) and create a key for the account. Place the key in a directory called "personal-gcp.json" in the src directory. Be careful as always not to share this key file unnecessarily. In future, these steps should be covered by Terraform.

The pipeline postgres_to_bq can be run once the ORCA data has been loaded into Postgres. This should create a schema and table in BigQuery containing your data.