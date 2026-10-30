"""Compare positive-control activity on source_9 COMPOUND and TARGET2 plates.

A normalized average precision of zero indicates chance-level retrieval.
"""

from __future__ import annotations

import duckdb
import polars as pl
from copairs.map import average_precision

DATASETS_REV = "016e865fa0691244e0860943e41c7d6a88ed2580"
METADATA = (
    "https://raw.githubusercontent.com/jump-cellpainting/datasets/"
    f"{DATASETS_REV}/metadata"
)
PROFILES = (
    "https://cellpainting-gallery.s3.amazonaws.com/cpg0016-jump-assembled/"
    "source_all/workspace/profiles_assembled/COMPOUND/v1.0/"
    "profiles_var_mad_int_featselect_harmony.parquet"
)
KEYS = [
    "Metadata_Source",
    "Metadata_Plate",
    "Metadata_Well",
    "Metadata_JCP2022",
]

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs")
feature_names = [
    row[0]
    for row in con.execute(
        f"DESCRIBE SELECT * FROM read_parquet('{PROFILES}')"
    ).fetchall()
    if row[0].startswith("X_")
]
control_ids = con.execute(
    f"""
    SELECT Metadata_JCP2022
    FROM read_csv_auto('{METADATA}/perturbation_control.csv')
    WHERE Metadata_modality = 'compound'
      AND Metadata_pert_type IN ('negcon', 'poscon')
    """
).pl()["Metadata_JCP2022"].to_list()
quoted_ids = ", ".join(f"'{value}'" for value in control_ids)

# Split the wide remote projection to avoid excessive simultaneous HTTP ranges.
parts = []
for names in (feature_names[:400], feature_names[400:]):
    columns = ", ".join(KEYS + names)
    parts.append(
        con.execute(
            f"""
            SELECT {columns}
            FROM read_parquet('{PROFILES}')
            WHERE Metadata_Source = 'source_9'
              AND Metadata_JCP2022 IN ({quoted_ids})
            """
        ).pl()
    )
profiles = parts[0].join(parts[1], on=KEYS, validate="1:1")
plates = con.execute(
    f"""
    SELECT Metadata_Source, Metadata_Plate, Metadata_PlateType
    FROM read_csv_auto('{METADATA}/plate.csv.gz')
    """
).pl()
profiles = profiles.join(plates, on=["Metadata_Source", "Metadata_Plate"]).with_columns(
    pl.when(pl.col("Metadata_JCP2022") == "JCP2022_033924")
    .then(pl.lit("negcon"))
    .otherwise(pl.lit("poscon"))
    .alias("pert_type")
)
# Compare only the seven positive controls present in both plate types.
shared_controls = (
    profiles.filter(pl.col("pert_type") == "poscon")
    .group_by("Metadata_JCP2022")
    .agg(pl.col("Metadata_PlateType").n_unique().alias("plate_types"))
    .filter(pl.col("plate_types") == 2)["Metadata_JCP2022"]
    .to_list()
)
profiles = profiles.filter(
    (pl.col("pert_type") == "negcon")
    | pl.col("Metadata_JCP2022").is_in(shared_controls)
)

rows = []
for (plate_type, plate), frame in profiles.group_by(
    ["Metadata_PlateType", "Metadata_Plate"]
):
    scores = pl.from_pandas(
        average_precision(
            frame.select(["Metadata_JCP2022", "pert_type"]).to_pandas(),
            frame.select(feature_names).to_numpy(),
            pos_sameby=["Metadata_JCP2022"],
            pos_diffby=[],
            neg_sameby=[],
            neg_diffby=["pert_type"],
            progress_bar=False,
        )
    ).filter(pl.col("pert_type") == "poscon")
    rows.append(
        {
            "plate_type": plate_type,
            "plate": plate,
            "median_normalized_ap": scores["normalized_average_precision"].median(),
        }
    )

results = pl.DataFrame(rows).sort(["plate_type", "plate"])
summary = results.group_by("plate_type").agg(
    pl.len().alias("plates"),
    pl.col("median_normalized_ap").median().alias("median_plate_activity"),
)
print(summary.sort("plate_type"))
print(results.filter(pl.col("plate_type") == "TARGET2"))
