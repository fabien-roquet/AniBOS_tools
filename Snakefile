from os import listdir
import os.path
from pathlib import Path
import pandas as pd

DATADIR = Path("data")
SMRUDIR = DATADIR / "smru"
RAWDIR = DATADIR / "raw"

PROCESSDIR = DATADIR / "processed"
MATLABDIR = Path("matlab")
CLIMDIR = Path("clim")
CONFDIR = Path("conf_files")

DATA = Path("data")
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
ALL_EXP = [i for i in listdir(RAW) if (RAW / i).is_dir()]
FIGURES = Path("figures")
FIGURES_PAPER = FIGURES / "paper"
CONFIGURATION = Path("configuration")

exp_configs = []
exp_configs_dict = {}

for exp in ALL_EXP:
    configs = [i for i in listdir(RAW / exp / "Experiments") if "EXP_" in i]
    exp_configs_dict[exp] = configs
    for config in configs:
        exp_configs.append(f"{exp}/{config}")


SECTION_PARAM_LON = CONFIGURATION / "section_longitudes.txt"
with open(SECTION_PARAM_LON) as f:
    lon_sections = [float(i) for i in f.read().splitlines()]
SECTION_PARAM_TIME = CONFIGURATION / "section_times.txt"
with open(SECTION_PARAM_TIME) as f:
    month_sections = [int(i) for i in f.read().splitlines()]

##############################
# RULES                      #
##############################


include: "rules/process.skm"
include: "rules/diags.skm"
include: "rules/plots_config.skm"
include: "rules/plots_exp.skm"
include: "rules/paper.skm"
include: "rules/plots_all.skm"
