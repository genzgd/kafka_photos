Checkout the repo

In the project directory, install the requirements by running

`pip install -r requirements.txt`

Set the environment variables

`export KAFKA_API_KEY=<Kafka API key>`
`export KAFKA_API_SECRET=<Kafka API secret>`

Make `watcher.py` executable and start it by `./watcher.py`, or run it with `python watcher.py`

Drop JPEG files into the projects `uploads` directory.  These will be produced to Kafka on the `singapore_photos` topic.

You'll have to use ctrl-C to exit the watcher.

In ClickPipes you'll have to set your schema registry to `https://psrc-gk071.us-east-2.aws.confluent.cloud/schemas/ids/100084`
and use the Schema Registry key and secret.