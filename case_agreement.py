from io import open
from conllu import parse_incr
from tqdm import tqdm
import random
from collections import Counter
case_markers = ['은',  '는', '이', '가', '을', '를', '에', '에서',  '으로', '로',  '부터', '까지', '과', 
'와', '이랑', '랑', '하고', '고' '의', '들']
data_file = open("ko_kaist-ud-train.conllu", "r", encoding="utf-8")
def case_agreement(output_file, case, case_marker_to_replace):
    case_marker_dic={'nsubj': ['이', '가'], 'obj':['을', '를']}
    with open(output_file, 'w') as case_agree:
        for tokenlist in tqdm(parse_incr(data_file)):
            original_sent = tokenlist.metadata['text']
            sent = []
            deprel_freq = Counter([tok['deprel'] for tok in tokenlist])
            pos_freq = Counter([tok['upos'] for tok in tokenlist])
            if deprel_freq['nsubj'] ==1 and deprel_freq['obj'] ==1 and pos_freq['VERB']:
                for tok in tokenlist:
                    if len(tok['form'])>1:
                        if tok['form'][-1] in case_markers and tok['deprel']==case:
                            case_particle = random.choice(case_marker_dic[case_marker_to_replace])
                            sent.append(tok['form'][:-1]+case_particle)
                        elif tok['form'][-2:] in case_markers and tok['deprel']==case:
                            case_particle = random.choice(case_marker_dic[case_marker_to_replace])
                            sent.append(tok['form'][:-2]+case_particle)
                        else:
                            sent.append(tok['form'])
                    else:
                        sent.append(tok['form'])

                to_write = ' '.join(sent)
                if ''.join(sent) != ''.join(original_sent.split()):
                    case_agree.write(f'{original_sent}\t{to_write}\n')

case_agreement('case_agreement_nn.txt', 'obj', 'nsubj')
case_agreement('case_agreement_aa.txt', 'nsubj', 'obj')