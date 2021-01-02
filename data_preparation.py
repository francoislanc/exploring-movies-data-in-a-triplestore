import pandas as pd
import re
from datetime import datetime
from dateutil.parser import parse
from typing import List
import itertools


def clean_str(val: str) -> str:
    return re.sub(r"[^A-Za-z0-9 ]+", "", val)


def parse_list(val: str) -> List[str]:
    if not pd.isna(val):
        return list(map(str.strip, val.split(",")))
    else:
        return []


def parse_date(val: str) -> str:
    return parse(val).isoformat() + "Z"


def parse_duration(val: str) -> int:
    return int(val.replace(" min", ""))


def movie_props(
    title: str, description: str, duration: int, average_rating: float, num_votes: int
) -> List[str]:
    return [
        '/movie<{}> "description"@[] "{}"^^type:text'.format(title, description),
        '/movie<{}> "duration"@[] "{}"^^type:int64'.format(title, duration),
        '/movie<{}> "average_rating"@[] "{}"^^type:float64'.format(
            title, average_rating
        ),
        '/movie<{}> "num_votes"@[] "{}"^^type:int64'.format(title, num_votes),
    ]


def movie_genres(title: str, genres: List[str]) -> List[str]:
    return ['/movie<{}> "genre"@[] "{}"^^type:text'.format(title, g) for g in genres]


def movie_countries(title: str, countries: List[str]) -> List[str]:
    return [
        '/movie<{}> "country"@[] "{}"^^type:text'.format(title, c) for c in countries
    ]


def movie_persons(title: str, directors: List[str], cast: List[str]) -> List[str]:
    d = ['/person<{}> "directed"@[] /movie<{}>'.format(d, title) for d in directors]
    c = ['/person<{}> "played"@[] /movie<{}>'.format(c, title) for c in cast]
    d.extend(c)
    return d


def movie_added_date(title: str, date: str) -> List[str]:
    return ['/platform<Netflix> "added"@[{}] /movie<{}>'.format(date, title)]


if __name__ == "__main__":
    movies = pd.read_csv("movies.csv")

    with open("movies.bql", "w") as f, open("triples.bw", "w") as ft:
        f.write("CREATE GRAPH ?g;\n")
        f.write("INSERT DATA into ?g {\n")
        sep = ""
        for index, row in movies.iterrows():
            (
                m_title,
                m_director,
                m_cast,
                m_country,
                m_date_added,
                m_release_year,
                m_rating,
                m_duration,
                m_listed_in,
                m_description,
                m_average_rating,
                m_num_votes,
                m_primary_title,
                m_original_title,
            ) = row

            m_title = clean_str(m_title)
            m_description = clean_str(m_description)
            m_director = parse_list(m_director)
            m_cast = parse_list(m_cast)
            m_country = parse_list(m_country)
            m_listed_in = parse_list(m_listed_in)
            m_date_added = parse_date(str(m_date_added))
            m_release_year = parse_date(str(m_release_year))
            m_duration = parse_duration(m_duration)

            t_props = movie_props(
                m_title, m_description, m_duration, m_average_rating, m_num_votes
            )

            t_genres = movie_genres(m_title, m_listed_in)

            t_countries = movie_countries(m_title, m_country)

            t_persons = movie_persons(m_title, m_director, m_cast)

            t_added_date = movie_added_date(m_title, m_date_added)

            for t in itertools.chain(
                t_props, t_genres, t_countries, t_persons, t_added_date
            ):
                f.write("{}{}".format(sep, t))
                ft.write("{}\n".format(t))
                sep = ".\n"

            # /platform<Netflix> added (date_added) /movie
            # /person (cast and director) (directored or plays in /movie)
            # /country
            # /genre (listing in)
            # /movie
            # has genre, numVotes, averageRating, desc, duration, title
        f.write("};\n")

        with open("queries.bql", "r") as fq:
            queries = fq.read()
            f.write(queries)