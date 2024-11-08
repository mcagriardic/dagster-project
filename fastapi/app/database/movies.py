import pandas as pd
from app.database import session
from sqlalchemy import Boolean, Column, Date, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Movies(Base):
    __tablename__ = "movies"

    id = Column(
        Integer, doc="Unique identifier for each movie.", primary_key=True, index=True
    )
    title = Column(String, doc="Title of the movie.", nullable=False)
    vote_average = Column(
        Float, doc="Average vote or rating given by viewers.", nullable=False
    )
    vote_count = Column(
        Integer, doc="Total count of votes received for the movie.", nullable=False
    )
    status = Column(
        String,
        doc="The status of the movie (e.g., Released, Rumored, Post Production, etc.).",
        nullable=False,
    )
    release_date = Column(Date, doc="Date when the movie was released.", nullable=True)
    revenue = Column(Float, doc="Total revenue generated by the movie.", nullable=False)
    runtime = Column(Integer, doc="Duration of the movie in minutes.", nullable=False)
    adult = Column(
        Boolean,
        doc="Indicates if the movie is suitable only for adult audiences.",
        nullable=False,
    )
    backdrop_path = Column(
        String, doc="URL of the backdrop image for the movie.", nullable=True
    )
    budget = Column(Integer, doc="Budget allocated for the movie.", nullable=False)
    homepage = Column(String, doc="Official homepage URL of the movie.", nullable=True)
    imdb_id = Column(String, doc="IMDb ID of the movie.", nullable=True)
    original_language = Column(
        String, doc="Original language in which the movie was produced.", nullable=False
    )
    original_title = Column(String, doc="Original title of the movie.", nullable=False)
    overview = Column(
        String, doc="Brief description or summary of the movie.", nullable=True
    )
    popularity = Column(Float, doc="Popularity score of the movie.", nullable=False)
    poster_path = Column(String, doc="URL of the movie poster image.", nullable=True)
    tagline = Column(
        String,
        doc="Catchphrase or memorable line associated with the movie.",
        nullable=True,
    )
    genres = Column(
        String,
        doc="List of genres the movie belongs to.",
        nullable=True,
    )
    production_companies = Column(
        String,
        doc="List of production companies involved in the movie.",
        nullable=True,
    )
    production_countries = Column(
        String,
        doc="List of countries involved in the movie production.",
        nullable=True,
    )
    spoken_languages = Column(
        String,
        doc="List of languages spoken in the movie.",
        nullable=True,
    )
    keywords = Column(
        String,
        doc='Keywords associated with the movie. Do `.split(", ")` to convert to a list.',
        nullable=True,
    )

    @classmethod
    def get_all(cls) -> pd.DataFrame:
        with session() as sess:
            return sess.query(cls).limit(250).all()
