import os
import sys


def load_seq(fpath):
    """
    load viroid sequences from multiple-entry FASTA file.
    Generate an hash with key as viroid accession and value as viroid sequencse.
    """
    
    id2seq = {}
    sid  = ''
    sseq = ''
    with open(fpath, 'r') as infh:
        for fline in infh:
            fline = fline.replace('\n', '')
            
            if fline[0] == '>':
                if sid != '' and sseq != '':
                    id2seq[sid] = sseq
                    sid = ''
                    sseq = ''
                sid = fline[1:].split(' ')[0].split('.')[0]
            else:
                sseq = sseq + fline
    id2seq[sid] = sseq
    
    return id2seq


   
def uniq_seq(id2seq):
    """
    Remove the duplicated sequences.
    Create an hash with key as a sequence and value as a viroid accession numbers.
    Then, create an new hash with key as a viroid accession numbers and value as a sequence.
    """   
    
    # unique sequences
    seq2id = {}
    for sid, sseq in id2seq.items():
        if sseq not in seq2id:
            seq2id[sseq] = []
        seq2id[sseq].append(sid)
    
    
    # generage unique hash of id2seq
    u_id2seq = {}
    for sseq, sids in seq2id.items():
        sid = ' '.join(sorted(sids))
        u_id2seq[sid] = sseq
    
    return u_id2seq



def del_abnormal_len_seq(id2seq):
    """
    Delete viroid sequences with abnormal length (out range of 355-365nt).
    """
    
    for sid in id2seq.keys():
        if not (355 <= len(id2seq[sid]) and len(id2seq[sid]) <= 365):
            del id2seq[sid]
    
    return id2seq
    

def rm_seq(id2seq):
    
    rm_id = ['AF459005', 'AF459006', 'AF459007', 'Z34272',
             'AY937180', 'AY937181', 'AY937182', 'AY937183', 'AY937184', 'AY937185', 'AY937186',
             'AY937194']
    
    for rm_id_ in rm_id:
        if rm_id_ in id2seq:
            del id2seq[rm_id_]
        
        
    return id2seq
    
    

def write_fasta(id2seq, fpath):
    
    with open(fpath, 'w') as outfh:
        for sid in sorted(id2seq.keys()):
            outfh.write('>' + sid + '\n')
            outfh.write(id2seq[sid]+ '\n')
    
    
    

if __name__ == '__main__':
    
    infa_fpath = sys.argv[1]
    outfa_fpath = sys.argv[2]
    
    id2seq = load_seq(infa_fpath)
    id2seq = uniq_seq(id2seq)
    id2seq  = del_abnormal_len_seq(id2seq)
    id2seq  = rm_seq(id2seq)
    write_fasta(id2seq, outfa_fpath)


