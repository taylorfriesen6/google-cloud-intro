# Tag Counter
This is a simple API which is deployed at <https://tag-counter-319600.wl.r.appspot.com/>. You can send data by making a JSON body POST request to that URL with fields **name** and **value**, for example
```json
{
   "name":"foo",
   "value":5
}
```
If you make a GET request to the same URL, you'll get back a JSON dictionary whose keys are all the names of POST requests that have been made, and where the value associated to each key is the sum of all the values in *all* POST requests that have been made with that name. For more information on the API, see <https://tag-counter-319600.wl.r.appspot.com/docs>

## File Organization
The app itself is contained in `main.py` and the unit tests are contained in `test.py`. Neither of these were large enough that I felt like it was worth splitting the code up further.

## Project Requirements

### Cloud Run, FastAPI, FireStore
The project is deployed on Google Cloud Run, uses FastAPI for its endpoints, and stores its data in Google's FireStore.
### JSON Schema
The project generates an OpenAPI JSON Schema which can be viewed at <https://tag-counter-319600.wl.r.appspot.com/openapi.json>, and a more human-readable form of the same information can be viewed at <https://tag-counter-319600.wl.r.appspot.com/docs>.
### Stackdriver structured logs
The POST request generates a custom Stackdriver log which records the name and value for the tag being submitted, as a JSON object in the jsonPayload field of the log. I did not manage to include the trace value in the logs, however.
### Stackdriver Metric
I made an attempt at creating a log-based metric which sums the values from all submitted tags. I don't think I succeeded because the graphs it generates don't make any sense to me, but it's possible that I successfully created the metric and am just confused by the interface for viewing its associated charts. That's the `aggregate_tag_counter` user-defined metric for the project.
### Testing
`test.py` contains unit tests for the functions for both FastAPI endpoints.