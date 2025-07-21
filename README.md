# Veho WMS
## Development

To work on this app,
please install and configure docker on your computer.


### To run this locally

```bash
docker compose up devbox
```
This starts up an HTTP server on port 8000 with graphql endpoint at
http://localhost:8000/graphql. Accessing with a browser will render a GraphiQL playground. 


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

- Requirements
  1. Catch code pushes during specific time windows (14:00 - 16:00)
  2. Catch team creation events with 'hacker' prefix
  3. Catch repository lifetime < 10 minutes
- Assumptions
  1. Needs to be idempotent (avoid reprocessing previously sent hooks/payloads)
  2. No need for HMAC authentication (validate payload originated from github)
- Design
  1. Synchronous webhook ingestion and persistence
  2. Async event analysis with ability to look back at aggregates
  3. Extensible to organization and repository specific analyzers
  4. Extensible to further notifiers (only logging for now)
  5. Mixed use of functional and OOP. OOP is nice but over time is difficult to refactor.
  6. Preference on composition over inheritance where possible.
  7. If I had more time I think an event-streaming framework (message queue based) could make more sense here