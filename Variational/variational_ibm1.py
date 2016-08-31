import sys
import copy
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

print >>sys.stderr, 'Reading data from %s' % args.bitext
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

print >>sys.stderr, 'Read %d sentences with vocab sizes %d/%d' % (len(src_sents), len(src_vocab), len(tgt_vocab))

alignments = [[None for word in tgt] for tgt in tgt_sents]
alpha = defaultdict(lambda: defaultdict(lambda: args.alpha0))
alpha_sums = defaultdict(lambda: args.alpha0 * len(tgt_vocab))
digamma = lambda x: math.lgamma(x)

def logsumexp(probs):
  m = max(probs)
  s = sum(math.exp(p - m) for p in probs)
  return m + math.log(s)
#logsumexp = lambda a: math.log(sum(math.exp(i) for i in a))

# TODO: I wonder if it's  better to just incrementally update alpha
# rather than storing new_alpha and only swapping after each iteration...
for iteration in range(args.iterations):
  print >>sys.stderr, 'Beginning iteration %d' % (iteration + 1)
  new_alpha = copy.deepcopy(alpha)
  new_alpha_sums = copy.deepcopy(alpha_sums)
  for sent_num, (src, tgt) in enumerate(zip(src_sents, tgt_sents)):
    sys.stderr.write('%d/%d\r' % (sent_num, len(src_sents)))
    for t in tgt:
      probs = [digamma(alpha[s][t]) - digamma(alpha_sums[s]) for s in src] 
      prob_sum = logsumexp(probs)

      for s, p in zip(src, probs):
        pd = math.exp(p - prob_sum)
        new_alpha[s][t] += pd
        new_alpha_sums[s] += pd
  print >>sys.stderr, '%d/%d' % (len(src_sents), len(src_sents))
  alpha = new_alpha
  alpha_sums = new_alpha_sums

print >>sys.stderr, 'Done! Dumping ttable...'
for s, d in alpha.iteritems():
  for t, p in d.iteritems():
    if p != 0.0:
      print '%s ||| %s ||| %f' % (s, t, math.log(p) - math.log(alpha_sums[s]))
