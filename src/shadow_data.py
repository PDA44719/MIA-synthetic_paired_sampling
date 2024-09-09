### Add pipeline to create data for shadow modeling
import pandas as pd
from tqdm import tqdm
from random import sample
from src.generators import Generator

def create_shadow_training_data_membership(df: pd.DataFrame, meta_data: list,
                                target_record: pd.DataFrame, generator: Generator,
                                n_original: int, n_synth: int, n_pos: int, seeds: list) -> tuple:
    datasets = []
    datasets_utility = []
    labels = []
    
    assert len(seeds) == n_pos * 2

    for i in tqdm(range(n_pos)):
        # Random sampling used here
        indices_sub = sample(list(df.index), n_original - 1)
        df_sub = df.loc[indices_sub]
        df_w_target = pd.concat([df_sub, target_record], axis=0)
        indices_wo_target = sample(list(df.index), n_original)
        df_wo_target = df.loc[indices_wo_target]  

        # let's create a synthetic dataset from data with the target record
        synthetic_from_target = generator.fit_generate(dataset=df_w_target, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i])
        datasets.append(synthetic_from_target)
        labels.append(1)

        # let's create a synthetic dataset from data without the target record
        synthetic_wo_target = generator.fit_generate(dataset=df_wo_target, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i + 1])

        datasets.append(synthetic_wo_target)
        labels.append(0)
        
        datasets_utility.append({'Real':{'With':df_w_target,'Without':df_wo_target}, 'Synth':{'With':synthetic_from_target,'Without':synthetic_wo_target}})

    return datasets, labels, datasets_utility

def create_shadow_training_data_membership_paired_sampling(df: pd.DataFrame, meta_data: list,
                                target_record: pd.DataFrame, generator: Generator,
                                n_original: int, n_synth: int, n_pos: int, seeds: list) -> tuple:
    datasets = []
    datasets_utility = []
    labels = []
    
    assert len(seeds) == n_pos * 2

    for i in tqdm(range(n_pos)):
        # Paired Sampling introduced here
        indices_wo_target = sample(list(df.index), n_original)
        df_wo_target = df.loc[indices_wo_target]  
        indices_wo_target.pop()  # Remove the reference record
        df_sub = df.loc[indices_wo_target]
        df_w_target = pd.concat([df_sub, target_record], axis=0)  # Add the target

        # let's create a synthetic dataset from data with the target record
        synthetic_from_target = generator.fit_generate(dataset=df_w_target, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i])
        datasets.append(synthetic_from_target)
        labels.append(1)

        # let's create a synthetic dataset from data without the target record
        synthetic_wo_target = generator.fit_generate(dataset=df_wo_target, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i + 1])

        datasets.append(synthetic_wo_target)
        labels.append(0)
        
        datasets_utility.append({'Real':{'With':df_w_target,'Without':df_wo_target}, 'Synth':{'With':synthetic_from_target,'Without':synthetic_wo_target}})

    return datasets, labels, datasets_utility

def select_fixed_reference(df: pd.DataFrame, target_record: pd.DataFrame):
    while True:
        idx = sample([39435, 1678, 35988, 36838, 6066, 27566, 16525, 43082, 5918, 16249], 1)
        if list(target_record.index.values)[0] != idx[0]:  # Choose another reference if it is equal to the target
            return get_target_record(df, idx[0])

def create_shadow_training_data_membership_fixed_reference(overall_df: pd.DataFrame, df: pd.DataFrame, meta_data: list,
                                target_record: pd.DataFrame, generator: Generator,
                                n_original: int, n_synth: int, n_pos: int, seeds: list) -> tuple:
    datasets = []
    datasets_utility = []
    labels = []

    assert len(seeds) == n_pos * 2
    outlier_reference = select_fixed_reference(overall_df, target_record)

    for i in tqdm(range(n_pos)):
        # Fixed reference paired sampling
        indices_wo_target = sample(list(df.index), n_original)
        indices_wo_target.pop()  # Remove the last element from the list
        df_wo_target = df.loc[indices_wo_target]
        df_with_outlier_reference = pd.concat([df_wo_target, outlier_reference], axis=0)
        df_sub = df.loc[indices_wo_target]
        df_w_target = pd.concat([df_sub, target_record], axis=0)

        # let's create a synthetic dataset from data with the target record
        synthetic_from_target = generator.fit_generate(dataset=df_w_target, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i])
        datasets.append(synthetic_from_target)
        labels.append(1)

        # let's create a synthetic dataset from data without the target record
        synthetic_wo_target = generator.fit_generate(dataset=df_with_outlier_reference, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i + 1])

        datasets.append(synthetic_wo_target)
        labels.append(0)

        datasets_utility.append({'Real':{'With':df_w_target,'Without':df_with_outlier_reference}, 'Synth':{'With':synthetic_from_target,'Without':synthetic_wo_target}})

    return datasets, labels, datasets_utility

def create_shadow_training_data_membership_no_reference(df: pd.DataFrame, meta_data: list,
                                target_record: pd.DataFrame, generator: Generator,
                                n_original: int, n_synth: int, n_pos: int, seeds: list) -> tuple:
    datasets = []
    datasets_utility = []
    labels = []

    assert len(seeds) == n_pos * 2

    for i in tqdm(range(n_pos)):
        # No reference paired sampling
        indices_wo_target = sample(list(df.index), n_original)
        indices_wo_target.pop()  # Remove the last element from the list
        df_wo_target = df.loc[indices_wo_target]
        df_sub = df.loc[indices_wo_target]
        df_w_target = pd.concat([df_sub, target_record], axis=0)

        # let's create a synthetic dataset from data with the target record
        synthetic_from_target = generator.fit_generate(dataset=df_w_target, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i])
        datasets.append(synthetic_from_target)
        labels.append(1)

        # let's create a synthetic dataset from data without the target record
        synthetic_wo_target = generator.fit_generate(dataset=df_wo_target, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i + 1])

        datasets.append(synthetic_wo_target)
        labels.append(0)

        datasets_utility.append({'Real':{'With':df_w_target,'Without':df_wo_target}, 'Synth':{'With':synthetic_from_target,'Without':synthetic_wo_target}})

    return datasets, labels, datasets_utility

def create_shadow_training_data_membership_synthetic_only_s3(df: pd.DataFrame, meta_data: list, generator: Generator,
                                n_original: int, n_synth: int, n_pos: int, seeds: list, target_record: pd.DataFrame, m: int) -> tuple:
    
    #df does not contain the target record
    
    test_datasets = []
    clean_datasets = []
    labels = []
    
    assert len(seeds) == n_pos * 2

    for i in tqdm(range(n_pos)):
        #Sample the first N_ORIGINAL-1 record (X_OUT)
        indices_random = sample(list(df.index), n_original)
        random_record = indices_random[n_original-1]
        #same dataset X_OUT
        #add random 
        df_wo_target = df.loc[indices_random]  
        #add target
        indices_wo_target = indices_random[:n_original-1]
        df_sub = df.loc[indices_wo_target]
        df_w_target = pd.concat([df_sub, target_record], axis=0)

        # let's create a synthetic dataset from data with the target record (X_IN)
        synthetic_from_target = generator.fit_generate(dataset=df_w_target, metadata=meta_data,
                                                       size=n_synth, seed = seeds[2 * i])
        test_datasets.append(synthetic_from_target)
        labels.append(1)
        # let's create a synthetic dataset from data without the target record (X_OUT)
        synthetic_wo_target = generator.fit_generate(dataset=df_wo_target, metadata=meta_data,
                                                           size=m*n_synth, seed = seeds[2 * i + 1])

        test_datasets.append(synthetic_wo_target.head(n_synth))
        labels.append(0)
        clean_datasets.append(synthetic_wo_target)
        #We add the same : without the target for clean-fixed. 
        clean_datasets.append(synthetic_wo_target)
    return test_datasets, clean_datasets, labels