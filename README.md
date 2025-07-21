# Veho WMS
## Development

To work on this app, please install and configure docker on your computer.


### To run this locally

```bash
docker compose pull
docker compose up devbox
```
This starts up an HTTP server on port 8000 with graphql endpoint at
http://localhost:8000/graphql. Accessing with a browser will render a GraphiQL playground. 

* this implementation uses sqlite for data peristence located at [wms.db](./wms.db)
* upon service start the db will be recreated and reseeded.
  * to prevent re-creation/re-seeding of the db, set the environment variable `SEED_DB` to `false` [here](https://github.com/itamar82/veho-workflow/blob/main/docker-compose.yaml#L5)



### Tests

Tests are located in the `tests` directory.

To run all tests:
```bash
docker compose run test
```

### Lint Checks

Runs lint (isort, black, and flake8)

```bash
docker compose run lint
```

### Overall Design Notes

The [Architecture](./ARCHITECTURE.md) document contains more information about the overall design/structure of the codebase.


#### General Design Approach
1. Used python for this implementation since I'm currently more familiar with it and the implementation intricacies for GraphQL.
   2. I'm fully confident that I could arrive at a similar or better implementation with NodeJS given additional time.
2. Kept the overall design simple and to the point of the exercise
   2. In a more production-like WMS there would be additional considerations and layers required (Location Hierarchy [zone, aisle, shelf, etc], Containers, Inventory, Tasks, Transactions, Purchase Orders, Receipts...)
   3. Leveraged async dataloader pattern to avoid the N+1 problem that GraphQL is notorious for.
   4. Wrap all requests in a db transaction.
   4. Due to the simplicity of the code, integration tests of the graphql mutations/queries is sufficient (80% coverage)
   5. Uses SQLite for the data persistence
   6. Idempotency (of mutations) was not included although this would be needed in a production system

