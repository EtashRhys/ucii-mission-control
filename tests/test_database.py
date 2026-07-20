import os

from storage.database import engine


def test_database_engine():

    assert engine is not None


def test_database_file_exists():

    assert os.path.exists(
        "storage/mission_control.db"
    )
