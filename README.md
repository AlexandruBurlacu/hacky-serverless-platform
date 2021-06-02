# A hacky serverless platform

But first, I shall try to do a webhook-enabled system.

As of 16 May, 2021, I succeded the above, AND made a little simple serverless Python platform, yay.

---

I like cloud and infrastructure technologies a lot, and Serverless seemed a bit vague for me for a long time. Long story short, I made a minimal, quite hacky [serverless platform](./function_server/README.md).

Right now the platform has no:
- Auth
- Isolation between users, given no auth, that makes sense
- Timeout for a running instance
- Reuse of containers, every time an event is triggered, a new container will be created
- Tests (shame on me)
- Way to install desired libraries, only use what the platform has
- Way of triggering a single handler/serverless submission based on multiple events or regex-style events.

But it has:
- The possibility to create instances on demand based on some triggers, a la serverless platforms
- A very basic (read ugly and not-always-reactive) UI
- Also Swagger
- A way to persist and view logs of running and finished instances
- Reuse of some popular python libraries, to speedup provisioning
- A built-from-scratch persistent Key-Value database, with a TCP server and a client
- A way to pass any input values to the functions

Not only this, but with a few essential services like a message queue (RabbitMQ), a couple of databases (Redis, Postgres, and Mongo) and an Object Store (Minio), and a hacky API Gateway, it is possible to create small serverless programs, a bit like you would do on AWS.


Also, `wh_server` and `recv_server` are a small PoC of a webhook server.

So yeah, more adjustments, maybe improvements, and certainly documentation is comming soon.
