from config import process_config
from utils import evaluation
from sys import argv,exit
from os.path import exists
from os import makedirs


node = argv[1]

infos = dict()
infos["output_dir"] = process_config.output_dir
infos["node"] = node

#evaluation.evaluation_change_zones_coverage(infos)
evaluation.evaluate_coverage_bins(infos)
