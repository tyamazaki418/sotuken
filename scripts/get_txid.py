import os
import sys


def load_id_from_fasta(fpath):
    ids = []
    with open(fpath, 'r') as infh:
        for buf in infh:
            if buf[0] == '>':
                ids.append(buf[1:].split(' ')[0])
    return ids



def print_records(ids, fpath):
    with open(fpath, 'r') as infh:
        for buf in infh:
            buf_records = buf.replace('\n', '').split('\t')
            if buf_records[1] in ids:
                print(buf, end = '')
    

if __name__ == '__main__':
    ids = load_id_from_fasta(sys.argv[1])
    print_records(ids, sys.argv[2])
    


