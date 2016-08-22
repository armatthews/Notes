import sys
import math
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('bitext', help='src ||| tgt')
#parser.add_argument('--reverse', '-r', action='store_true')
parser.add_argument('--alpha0', '-a', type=float, default='0.01', help='Dirichlet prior strength')
parser.add_argument('--iterations', '-i', type=int, default='5')
args = parser.parse_args()

src_vocab = set()
tgt_vocab = set()
src_sents = []
tgt_sents = []

with open(args.bitext) as f:
  for line in f:
    src, tgt = line.strip().split('|||')
    src = src.strip().split()
    tgt = tgt.strip().split()
    assert len(src) > 0

    for s in src:
      src_vocab.add(s)
    for t in tgt:
      tgt_vocab.add(t)

    src_sents.append(src)
    tgt_sents.append(tgt)

alignments = [[None for word in tgt] for tgt in tgt_sents]
alpha = defaultdict(lambda: defaultdict(lambda: args.alpha0))
alpha_sums = defaultdict(lambda: args.alpha0 * len(tgt_vocab))
digamma = lambda x: math.lgamma(x)
logsumexp = lambda a: math.log(sum(math.exp(i) for i in a))

for iteration in range(args.iterations):
  new_alpha = defaultdict(lambda: defaultdict(lambda: args.alpha0))
  new_alpha_sums = defaultdict(lambda: args.alpha0 * len(tgt_vocab))
  for src, tgt in zip(src_sents, tgt_sents):
    for t in tgt:
      probs = [digamma(alpha[s][t]) - digamma(alpha_sums[s]) for s in src]
      prob_sum = logsumexp(probs)
      if t == 'bleue':
        print probs

      for s, p in zip(src, probs):
        pd = math.exp(p - prob_sum)
        new_alpha[s][t] += pd
        new_alpha_sums[s] += pd
  alpha = new_alpha
  alpha_sums = new_alpha_sums

for s, d in alpha.iteritems():
  for t, p in d.iteritems():
    print '%s ||| %s ||| %f' % (s, t, p / alpha_sums[s])
