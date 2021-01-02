# Exploring Movies Data In A Triplestore

## Data preparation

- Install python dependencies

```
pip install -r requirements.txt
```

- Create triples and BQL statements. It will generate the "movies.bql" file.

```
python data_preparation.py
```

## Data querying

- Install Badwolf triplestore

```
go build github.com/google/badwolf/tools/vcli/bw
```

- Run query in the BadWolf REPL (`bw bql`)

```
CREATE GRAPH ?g;
load ./movies-triples.txt ?g;
run queries.bql;
```

## Triplestore visualisation
