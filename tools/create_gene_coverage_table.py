# /// script
# dependencies = [
#   "duckdb",
#   "pooch",
# ]
# ///
import duckdb
from pooch import retrieve

# Files
periscope = {
    "A549": (
        "https://raw.githubusercontent.com/broadinstitute/2022_PERISCOPE//632557b77361777b5b728a7534ed8e9d9ed6c090/4_A549_Screen_Summary/outputs/A549_plate_level_median_per_feat_sig_genes_1_FDR_whole_cell_hits.csv",
        "5f2309b4dbb65377dd756ac8bb94a4b8eae70cfb8bc7edd023c06eb6a9392b6b",
    ),
    "HeLa_DMEM": (
        "https://raw.githubusercontent.com/broadinstitute/2022_PERISCOPE/632557b77361777b5b728a7534ed8e9d9ed6c090/2_HeLa_Screens_Summary/outputs/HeLa_DMEM_plate_level_median_per_feat_sig_genes_1_FDR_whole_cell_hits.csv",
        "d4f6a715364749fb01759c078e254d80c4e514fee853edc36af81a0fa36f974c",
    ),
    "HeLa_HPLM": (
        "https://raw.githubusercontent.com/broadinstitute/2022_PERISCOPE/632557b77361777b5b728a7534ed8e9d9ed6c090/2_HeLa_Screens_Summary/outputs/HeLa_HPLM_plate_level_median_per_feat_sig_genes_1_FDR_whole_cell_hits.csv",
        "b5508c768960c1ace5106824eaf8704fc1529b5a2f4154949247c7ec514b5922",
    ),
}
lacoste_url, lacoste_hash = (
    "https://cellpainting-gallery.s3.amazonaws.com/cpg0026-lacoste_haghighi-rare-diseases/broad/workspace/metadata/raw/RC4_IF_standardized_annotations_20180813.xlsx",
    "26ed9fa3b4e8dec9b1f44ffc1c6ce7887ad2df1285298ecad5ee3be10a474563",
)

jump_url, jump_hash = (
    "https://zenodo.org/api/records/13255965/files/babel.db/content",
    "72180e7889c6c0c66a12e976c0645b5b3d873f77fc00ce106ede70c9fba1bfa7",
)

# %% Periscope
local_files = {k: retrieve(url, known_hash=hsh) for k, (url, hsh) in periscope.items()}
csvs = list(local_files.values())
per_tidy = duckdb.sql(
    f"SELECT Gene,'CRISPR_' || split_part(split_part(parse_filename(filename,true),'-',2), '_pl', 1) AS origin FROM read_csv({csvs}, filename=true)"
)
# This will be the table we will join
per_p = duckdb.sql("PIVOT per_tidy ON origin")

# %% JUMP
jump_local = retrieve(
    jump_url,
    known_hash=jump_hash,
    fname="babel",
)
duckdb.sql("INSTALL sqlite; LOAD sqlite;")
duckdb.sql(f"ATTACH IF NOT EXISTS '{jump_local}'")
jump_tidy = duckdb.sql(
    f"SELECT standard_key AS Gene, UPPER(plate_type) || '_JUMP' AS origin FROM babel.babel WHERE plate_type IN ('orf', 'crispr')"
)
jump_p = duckdb.sql("PIVOT jump_tidy ON origin")

merged = duckdb.sql("SELECT * FROM jump_p FULL JOIN per_p USING(Gene) ORDER BY Gene")

# %% Lacoste paper
lacoste_local = retrieve(lacoste_url, known_hash=lacoste_hash)
lacoste_uniq = duckdb.sql(
    f"SELECT DISTINCT Gene,1 AS ORF_Lacoste FROM read_xlsx('{lacoste_local}', all_varchar = true);"
)
merged_last = duckdb.sql(
    "SELECT Gene,COALESCE(COLUMNS(* EXCLUDE(Gene)), 0) FROM merged FULL JOIN lacoste_uniq USING(Gene) ORDER BY Gene"
)

duckdb.sql("COPY merged_last TO 'table.csv'")
