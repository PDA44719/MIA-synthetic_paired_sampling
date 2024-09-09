# Paired Sampling Membership Inference Attacks Against Synthetic Data

The code in this repository corresponds to the methodology and results as presented in the following paper: 
**Paired Sampling Technique to Enhance Shadow Modelling-based Membership Inference Attacks.**

This code was built on top of the repository created for the following two papers:

1. ["Achilles' Heels: Vulnerable Record Identification in Synthetic Data Publishing"](https://arxiv.org/abs/2306.10308)
2. ["Synthetic is all you need: removing the auxiliary data assumption for membership inference attacks against synthetic data"](https://arxiv.org/abs/2307.01701)

Please, find the original repository here:
[https://github.com/computationalprivacy/MIA-synthetic.git](https://github.com/computationalprivacy/MIA-synthetic.git)


## (1) Environment setup

The environment setup steps will be the same as the steps detailed in the original repository.
First, run the following commands
- Create and activate the env:
    - `conda create --name mia_synthetic python=3.9`
    - `conda activate mia_synthetic`
- Clone and install the requirements from the [reprosyn repository](https://github.com/alan-turing-institute/reprosyn):
    - `git clone https://github.com/alan-turing-institute/reprosyn`
    - `cd reprosyn`
    - `curl -sSL https://install.python-poetry.org | python3 -`
    - `poetry install -E ektelo`. To install poetry on your system we refer to [their installation instructions](https://python-poetry.org/docs/#installing-with-the-official-installer).
    - Note that, in order to get it to work for continuous attributes as well, you might look into [this raised issue](https://github.com/alan-turing-institute/reprosyn/issues/65).

Then we have to install the C-based optimized QBS which was taken from the following [repository](https://github.com/computationalprivacy/querysnout) (if you use it please cite the [paper](https://dl.acm.org/doi/abs/10.1145/3548606.3560581)):
- `cd src/optimized_qbs/`
- `python setup.py install`

## How to run the Query-Based and Target Attention Attacks

To replicate both the *random sampling* and *paired sampling* attacks for a specific target record, please use the script `scripts/run_experiment_achilles.sh`.
Please refer to the functions `create_shadow_training_data_membership` and  `create_shadow_training_data_membership_paired_sampling` inside `src/shadow_data.py` for further clarification.

This script will first compute the random sampling results for the naive (not explored in the paper), query-based and target attention attacks. Then, it will compute the results for the paired sampling version of the attacks.

To run the script:
> bash scripts/run_experiment_achilles.sh *seed* *target_record*

where *seed* is the seed used for the experiments and *target_record* is the record to be attacked.

## How to run the S1 Black-Box and S2 Published Data experiments

In order to replicate the results of the S1 and S2 experiments presented in the paper, please use the script `scripts/run_experiment_synthetic_only.sh`.
Once more, refer to `create_shadow_training_data_membership` and  `create_shadow_training_data_membership_paired_sampling` inside `src/shadow_data.py` for further clarification.

The code will first compute the *random sampling* results of the attacks, and then the *paired sampling* version.

To run the script:
> bash scripts/run_experiment_synthetic_only.sh *seed* *scenario* *target_record*

where *seed* is the seed used for the experiment, *scenario* is the scenario you want to attack (i.e., this value should be set to either 1 or 2) and *target_record* is the record to be attacked.

## How to run the Alternative/Additional Paired Sampling variations


To replicate both the *fixed reference* and *no reference* paired sampling experiments for a specific target record, please use the script `scripts/run_experiment_achilles_alternative.sh`.
Please refer to the functions `create_shadow_training_data_membership_fixed_reference` and  `create_shadow_training_data_membership_no_reference` inside `src/shadow_data.py` for further clarification.

This script will first compute the no reference paired sampling results of the attacks. Then, it will compute the results for the fixed reference paired sampling version of the attacks.

To run the script:
> bash scripts/run_experiment_achilles_alternative.sh *seed* *target_record*

where *seed* is the seed used for the experiments and *target_record* is the record to be attacked.



## (4) Setting up the data 

Throughout the paper, two tabular datasets have been considered: UK Census and Yahoo Finance. 
For ease of usability, a very small sample of the original data was provided in the `data` folder, along with the corresponding metadata files that are required for the attack to run. 
For full access to the datasets, please refer to the references in the paper. 


