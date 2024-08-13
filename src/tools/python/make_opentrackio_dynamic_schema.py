import sys
import json
import camdkit.model

if __name__ == "__main__":
  schema = camdkit.model.Clip.make_opentrackio_dynamic_schema()
  json.dump(schema, sys.stdout, indent=2)
