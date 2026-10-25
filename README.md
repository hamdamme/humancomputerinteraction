# Human Computer Interaction

A reading index and a small command line tool for summarizing usability session records.

## Contents

- `src/session_summary.py` groups observed outcomes by task and reports completion counts and median time.
- `data/example_sessions.csv` shows the expected input format.
- `SOURCES.md` records the references used for the reading index and method notes.

The summary describes the recorded sessions only. It does not establish that a design is usable for every audience or context. Keep participant identity and sensitive notes out of the input file.

## Run

```sh
python3 src/session_summary.py data/example_sessions.csv
```

The input CSV must contain `session_id`, `task`, `outcome`, and `duration_seconds`. Outcome values are `complete`, `blocked`, or `abandoned`. Duration must be a nonnegative number of seconds. A blank duration is allowed when timing was not recorded.

## Reading

See [SOURCES.md](SOURCES.md). Books and other works remain at their original locations. This repository contains original notes and code, not copies of books.

## License

The code and original notes in this repository are under the MIT License. Source works retain their own terms.
