import os
import sys


def get_ac(entry_id):
    return entry_id[1:].split(' ')[0]
    
    

def parse_fasta(fa_fpath):
    entry_ac = None
    entry_id = None
    entry_seq = None
    
    with open(fa_fpath, 'r') as fafh:
        for fa_data in fafh:
            fa_data = fa_data.replace('\n', '')
            if fa_data[0] == '>':
                if entry_id is not None:
                    yield entry_ac, entry_id, entry_seq
                
                entry_id = fa_data
                entry_ac = get_ac(fa_data)
                entry_seq = ''
            else:
                entry_seq += fa_data
    
    return entry_ac, entry_id, entry_seq
    

def is_PSTVd(entry_id):
    if 'potato spindle tuber viroid' in entry_id.lower() and 'complete' in entry_id.lower():
        return True
    return False





def main(fa_fpath, output_dpath):
    
    seq_dict = {}
    
    for entry_ac, entry_id, entry_seq in parse_fasta(fa_fpath):
        if is_PSTVd(entry_id):
            if entry_seq not in seq_dict:
                seq_dict[entry_seq] = []
            seq_dict[entry_seq].append(entry_ac)
    
    for seq, ids in seq_dict.items():
        if len(ids) > 1:
            print(ids)
     



if __name__ == '__main__':
    
    fa_fpath = sys.argv[1]
    output_dpath = sys.argv[2]
    main(fa_fpath, output_dpath)
    



