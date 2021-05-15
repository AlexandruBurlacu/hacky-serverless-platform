Python workers

https://tomasz.janczuk.org/2018/03/how-to-build-your-own-serverless-platform.html
https://www.martinfowler.com/articles/serverless.html
https://www.usenix.org/system/files/conference/atc18/atc18-oakes.pdf

First only STDLIB, later add core libs, like `requests` and `aiohttp`.

## TODO
- **[Done]** Allow any function code to be running on the platform
- **[Done]** Pass in input values to the functions
- Kill a function after some time (1 min for example)
- Once invoked, return right away