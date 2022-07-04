# Thing Service

This API exposes functionality to store and manage Things, which are JSON objects.

## Setup

This project uses [Pipenv](https://pipenv.pypa.io/en/latest/).

```
# install dependencies
pipenv install

# run unit tests
pipenv run test
```

## Endpoints

### Health Check

```
GET /health
```

```
200 OK
```

### Create a Thing

```
POST /thing

Content-Type: application/json

ThingRequest
```

```
201 Created

Location: /thing/{thingId}
```

### Retrieve All Things

```
GET /thing
```

```
200 OK

Content-Type: application/json

{
    things: Thing[]
}
```

### Retrieve a Thing

```
GET /thing/{thingId}
```

```
200 OK

Content-Type: application/json

Thing
```

### Replace a Thing

```
PUT /thing/{thingId}

Content-Type: application/json

ThingRequest
```

```
204 No Content
```

### Delete a Thing

```
DELETE /thing/{thingId}
```

```
204 No Content
```

## Error Responses

```
400 Bad Request

Content-Type: application/json

ErrorResponse
```

```
404 Not Found

Content-Type: application/json

ErrorResponse
```

```
500 Internal Server Error

Content-Type: application/json

ErrorResponse
```

## Models

### ErrorResponse

```
{
    error: string
}
```

| Field     | Type      | Description
|---        |---        |---
| `error`   | `string`  | Error message indicating which error was thrown

### Thing

```
{
    thingId: string,
    modelKey: string,
    ...
}
```

| Field             | Type          | Description
|---                |---            |---
| `thingId`         | `string`      | Unique identifier for the Thing
| `modelKey`        | `string`      | Key indicating the type of Thing
| Additional fields | (valid JSON)  | Users can specify any additional fields

### ThingRequest

```
{
    modelKey: string,
    ...
}
```

| Field             | Type      | Description
|---                |---        |---
| `modelKey`        | `string`  | Key indicating the type of Thing
| Additional fields | (valid JSON)  | Users can specify any additional fields

The `thingId` field will be ignored in a `ThingRequest` payload if included; use the Replace a Thing (`PUT`) endpoint if you want to create a Thing with a predefined `thingId`.
