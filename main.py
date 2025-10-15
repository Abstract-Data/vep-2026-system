from typing import Optional
from sqlmodel import create_engine, SQLModel, text
from pathlib import Path
from tqdm import tqdm
from sqlmodel import Field as SQLModelField, Session, select
from vep_file_loading import CreatePublicModels, CreateRawFileModel
from state_voterfiles.renaming import FieldManager
import time
import threading

bridge_tree_data = (
    Path.home()
    / "Documents"
    / "VEP 2026"
    / "bridgetree-data"
    / "VEP 09.15.2025 (Monday)"
)
public_models = CreatePublicModels()
raw_voterfile_model = CreateRawFileModel(
    schema_name="voterfile", public_models=public_models
)
raw_target_model = CreateRawFileModel(
    schema_name="targetfile", public_models=public_models
)

SUPABASE_DB = "postgresql://postgres:postgres@127.0.0.1:54322/postgres"
engine = create_engine(SUPABASE_DB)
public_models.setup(engine)
raw_voterfile_model.setup(engine)
raw_target_model.setup(engine)


raw_voterfile_model.read_file(
    engine,
    file_path="/Users/johneakin/PyCharmProjects/vep-2024/data/voterfiles/texas/texasnovember2024.csv",
    state_abbreviation="TX",
    vendor_name="Ryan Data",
)
for file in bridge_tree_data.glob("*.csv"):
    raw_target_model.read_file(
        engine, file_path=file, state_abbreviation="TX", vendor_name="Bridge Tree"
    )
