

## @local generate new constraints file.
generate_constraints:
	uv export --locked --no-hashes --no-emit-project --no-dev --format requirements-txt -o configuration/pip/requirements.txt
	uv export --locked --no-hashes --no-emit-project --only-dev --format requirements-txt -o configuration/pip/requirements-dev.txt
