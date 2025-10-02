import sys
import os
import re
import warnings
import pandas as pd
import numpy as np
import tqdm
import glob
import gzip

def get_pstvd_id(fpath):
    pstvd = []
    with open(fpath, 'r') as infh:
        for buf in infh:
            pstvd.append(buf.split('\t')[0])
    return pstvd


def get_depth_matrix(data_dpath, pstvd, chunk_size=1000000):
    fdata = sorted(glob.glob(os.path.join(data_dpath, '*.depth')))
    fdata.extend(sorted(glob.glob(os.path.join(data_dpath, '*.depth.gz'))))
    fdata_pstvd = []
    for fpath in fdata:
        cleaned = os.path.basename(fpath).replace('.depth.gz', '').replace('.depth', '')
        if cleaned in pstvd:
            fdata_pstvd.append(fpath)
        else:
            print(f"Skipping {os.path.basename(fpath)} -> cleaned: {cleaned}, not in pstvd")
    
    chrom_sizes = {
        'SL4.0ch00': 9643250, 'SL4.0ch01': 90863682, 'SL4.0ch02': 53473368,
        'SL4.0ch03': 65298490, 'SL4.0ch04': 64459972, 'SL4.0ch05': 65269487,
        'SL4.0ch06': 47258699, 'SL4.0ch07': 67883646, 'SL4.0ch08': 63995357,
        'SL4.0ch09': 68513564, 'SL4.0ch10': 64792705, 'SL4.0ch11': 54379777,
        'SL4.0ch12': 66688036,
    }
    
    mat_merged = None
    for mat_key in tqdm.tqdm(chrom_sizes.keys(), desc='Processing chromosomes'):
        chrom_size = chrom_sizes[mat_key]
        mat_df = None
        for start in range(0, chrom_size, chunk_size):
            end = min(start + chunk_size, chrom_size)
            mat = np.zeros((end - start, len(fdata_pstvd)), dtype=np.uint16)
            for i, fpath in enumerate(fdata_pstvd):
                infh = gzip.open(fpath, 'rt') if fpath.endswith('.gz') else open(fpath, 'r')
                for r in infh:
                    if not (r.startswith('chrom') and 'pos' in r):
                        r = r.replace('\n', '').split('\t')
                        if r[0].replace(' ', '') == mat_key:
                            pos = int(r[1]) - 1
                            if start <= pos < end:
                                mat[pos - start, i] = int(r[2])
                infh.close()
            col_name = [os.path.basename(f).replace('.depth.gz', '').replace('.depth', '') for f in fdata_pstvd]
            row_name = [f'{mat_key}__{i+start:010d}' for i in range(end - start) if mat[i, :].sum() > 0]
            chunk_df = pd.DataFrame(mat[mat.sum(axis=1) > 0, :], columns=col_name, index=row_name)
            mat_df = pd.concat([mat_df, chunk_df], axis=0)
            del mat
        mat_merged = pd.concat([mat_merged, mat_df], axis=0)
        del mat_df
    
    mat_merged.index.name = 'position'
    return mat_merged
    

def fold_region(depth_mat):
    n = 0
    start_pos = None
    end_pos = None
    current_pos = -1

    position_ids = depth_mat.index.values
    region_ids = []

    chr_name = None
    for position_id in tqdm.tqdm(position_ids, desc='Folding regions'):
        chr_name, chr_position = position_id.split('__')
        chr_position = int(chr_position)

        if current_pos != chr_position:
            if (start_pos is not None) and (end_pos is not None):
                region_ids.extend(['{0}:{1:010d}-{2:010d}'.format(chr_name, start_pos, end_pos)] * n)

            start_pos = chr_position
            end_pos = None
            n = 0
        else:
            end_pos = chr_position

        current_pos = chr_position + 1
        n = n + 1

    # last region
    if chr_name is not None:
        region_ids.extend(['{0}:{1:010d}-{2:010d}'.format(chr_name, start_pos, end_pos)] * n)

    region_ids = pd.Series(region_ids, index=position_ids).to_frame(name='region_id')
    depth_mat = pd.concat([region_ids, depth_mat], axis=1, sort=False)

    return depth_mat


if __name__ == '__main__':
    
    data_dpath = sys.argv[1]
    pstvdid_fpath = sys.argv[2]
    output_fpath = sys.argv[3]
    
    pstvd = get_pstvd_id(pstvdid_fpath)
    depth_mat = get_depth_matrix(data_dpath, pstvd)
    depth_mat = fold_region(depth_mat)
    
    depth_mat.to_csv(output_fpath, header=True, index=True, sep='\t')
    
