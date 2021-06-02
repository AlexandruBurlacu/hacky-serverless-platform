# Serverless Python

Took ideas and inspiration from the following links:
- https://tomasz.janczuk.org/2018/03/how-to-build-your-own-serverless-platform.html
- https://www.martinfowler.com/articles/serverless.html
- https://www.usenix.org/system/files/conference/atc18/atc18-oakes.pdf
- https://dev.to/aws-builders/redis-exploring-redis-as-serverless-database-to-solve-idempotence-in-apis-2gma

The `gateway.py` is based on https://mleue.com/posts/simple-python-tcp-server/

Supports some 3rd party libs. See `builder/lambda_libs.txt`

## TODO
- **[Done]** Allow any function code to be running on the platform
- **[Done]** Pass in input values to the functions
- **[Done]** Once invoked, return right away
- **[Done]** CRUD operations on serverless submissions and invocations
- **[Done]** Make logs work
- **[Done]** UI
- Kill a function after some time (1 min for example) - https://dev.to/jmarhee/managing-running-container-lifetimes-with-the-docker-python-sdk-ono
- Multi-tenant (users, roles, filter-by-user/owner)
- Docker instance-pool and reuse these (could require security hardening)
