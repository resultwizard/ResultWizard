# Code structure

We use the clean architecture paradigm. Modules in outer layers are allowed to import from inner layers, but never the other way around. E.g. `api` might need definitions from `domain`, but `domain` must never import anything from `api`. This allows for better separation of concerns and makes it easier to test the code.

From outer layer to inner layer:

- `valuewizard/`: Entrypoint for the PIP package; mainly only import statements
- `api/`: User-facing API, e.g. `res()` and `export()` method
- `application/`: Application code that uses the domain logic to solve specific problems
- `domain/`: Domain logic, e.g. definition of what a `value`, how things are represented internally


## Conventions

- Prepend everything that is not public-facing with an underscore `_`, e.g. `_Result` instead of `Result`. This is to make it clear what is public and what is not as python does not have a concept of private methods or variables.
