# Exploring Movies Data In A Triplestore

## Data preparation

- Install python dependencies

```
pip install -r requirements.txt
```

- Create triples and BQL statements. It will generate the "output/movies.bql" and "output/triples.bw" files.

```
python data_preparation.py
```

## Data querying

- Install [Badwolf](http://google.github.io/badwolf/) triplestore

```
go build github.com/google/badwolf/tools/vcli/bw
```

- Run queries in the BadWolf REPL (`bw bql`)
```
CREATE GRAPH ?g;
load ./output/triples.bw ?g;
run ./input/queries.bql;
```

or run the script directly :
```
bw run ./output/movies.bql
```

## Triplestore visualisation

Open `graph_viewer.html` in a browser.
The nodes and edges are manually specified in the html file.