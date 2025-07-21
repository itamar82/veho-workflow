# Veho WMS Architecture

## Current System Architecture

```mermaid
graph TB
    subgraph "API Layer"
        GQL[GraphQL Endpoint]
        SCHEMA[GraphQL Schema]
        RESOLVERS[Resolvers]
        subgraph "Resolver Types"
            QUERY[Query Resolvers]
            MUTATION[Mutation Resolvers]
            LOCATION_R[Location Resolvers]
        end
    end

    subgraph "Service Layer"
        WF_SVC[Workflow Services]
        REPO[WMS Repository]
        CTX[Transaction Context]
    end

    subgraph "Domain Layer"
        subgraph "Core Entities"
            WAREHOUSE[Warehouse]
            LOCATION[Location]
            PALLET[Pallet]
            PACKAGE[Package]
        end
        subgraph "Domain Logic"            
            WF_RULES[Workflow Rules]
        end
    end

    subgraph "Data Layer"
        ORM[SQLAlchemy ORM]
        SCHEMA_DB[Database Schema]
        ENGINE[DB Engine]
    end

    subgraph "Infrastructure"
        FASTAPI[FastAPI App]
        ARIADNE[Ariadne GraphQL]
        SQLITE[SQLite Database]
    end

    %% Current Flow
    GQL --> RESOLVERS
    RESOLVERS --> WF_SVC
    RESOLVERS --> REPO
    WF_SVC --> WAREHOUSE
    WF_SVC --> PACKAGE
    WF_SVC --> PALLET
    WF_SVC --> LOCATION
    REPO --> ORM
    ORM --> SCHEMA_DB
    SCHEMA_DB --> ENGINE
    ENGINE --> SQLITE
    FASTAPI --> ARIADNE
    ARIADNE --> GQL
    MUTATION --> WF_RULES

    %% Context Management
    CTX -.-> REPO
    CTX -.-> GQL
```

## Current Workflow Implementation

* Induction
  * Validate packages exist in the system and haven't been Inducted yet
* Stow
  * Validate the Pallet Location (if pallet id provided otherwise create new one) is in a RECEIVING zone
  * Validate given Packages aren't already STOWED
* Stage
  * Validate Pallet current Location and not already Staged
* Pick
  * Validate that > 0 Packages exist at that Location (and on a Pallet)
  * Decrement # of Packages on that Pallet & dissolve Pallet (delete if empty)
  * Place Packages in a different Pallet (FORK Location) of the User


```mermaid
stateDiagram-v2
    [*] --> PENDING : Package Created
    PENDING --> INDUCTED : Induction Process
    INDUCTED --> STOWED : Stow to Pallet
    STOWED --> STAGED : Pallet (and affected Pallets) moved to Staging location
    STAGED --> PICKED : Packages Picked from Pallet
    PICKED --> [*] : Loaded/Packed/Shipped
    
    note right of INDUCTED : Sets received_timestamp and INDUCTED status.
    note left of STOWED : Assign packages Pallet
    note left of STAGED : Assigns the Pallet to a new Staging Location
    note right of PICKED : Marks Packages as Picked, moved to a FORK Location.
```

## Extensibility Architecture for Full WMS

![wms-architecture.png](wms-architecture.png)

## Key Extensibility Points

### 1. Service Layer Extensions

- Key Points
  - Inventory Service
    - centralized service layer for managing alloperations that affect inventory (induction, movement, cycle counting changes, etc)
    - additional inventory attributes
      - expiration
      - product characteristics (weight, dimensions, description, etc)
    - allocation
  - Location Strategy
    - physical mapping of Facility locations
    - inventory compatibility restrictions (HAZMAT, BIN, BULK)
    - operational restrictions (STORAGE, PICKING, PUTAWAY, REPLEN)
    - capacity restrictions
  - Transaction Ledger
    - all operations performed in the WMS are logged as distinct transactions
  - Picking/Putaway/CycleCounting/Location Strategies
    - optimal routing of pick/put/cycle count paths
  - Task management
    - user assignment and work queue management


## Migration Path

### Phase 1: Current State ✅
- [x] Core domain entities (Warehouse, Location, Package, Pallet)
- [x] Basic workflows (Induct, Stow)
- [x] GraphQL API with proper resolvers
- [x] Transaction management
- [x] Repository pattern

### Phase 2: Service Layer Enhancement
- [ ] Business rules engine
- [ ] Task management system
- [ ] Inventory allocation service
- [ ] Advanced location strategies

### Phase 3: Integration & Scaling
- [ ] External system integrations
- [ ] Message queue architecture
- [ ] Event sourcing implementation
- [ ] Advanced analytics and reporting

### Phase 4: Operations & Monitoring
- [ ] Real-time dashboards
- [ ] Performance optimization
- [ ] Multi-tenant architecture
- [ ] Advanced workflow orchestration


### Scalability
- **Current**: SQLite for development simplicity
- **Future**: PostgreSQL with read replicas, caching layers
- **Extension Point**: Database abstraction allows easy migration

### Performance
- **Current**: Simple repository queries
- **Future**: Query optimization, indexing strategies, caching
- **Extension Point**: Repository pattern abstracts data access

### Reliability
- **Current**: Transaction management with rollback
- **Future**: Circuit breakers, retry policies, dead letter queues, idempotency
- **Extension Point**: Service layer can add reliability patterns

### Observability
- **Current**: Basic logging
- **Future**: Distributed tracing, metrics, alerting
- **Extension Point**: Middleware layers for cross-cutting concerns

