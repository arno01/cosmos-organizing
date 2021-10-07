# Using the parameter change json validator

## What can you use to validate the schema?

### Web-based JSON schema validator (recommended)
Copy the scehma in to this [JSON schema validator](https://www.jsonschemavalidator.net/)

### Using pajv (a node package)
Note that pajv doesn't seem to support the schema spec I'm using (if/else)
Check out [pajv here](https://www.npmjs.com/package/pajv).
You ca use it like this:
```shell
npm install -g pajv
pajv validate -s param-change-proposal-schema.json -d test/valid.json
```