import re
import random


class NoiseGenerator(object):

    def __init__(self, path_pairs=None):
        self.consonant = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        self.vowel = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ',
                      'ㅢ', 'ㅣ']
        self.final_consonant = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ',
                                'ㅂ',
                                'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        self.exceptions = ['ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅗ']
        self.pairs = {'ㅏ': 'ㅑ', 'ㅑ': 'ㅏ', 'ㅓ': 'ㅕ', 'ㅕ': 'ㅓ', 'ㅗ': 'ㅛ', 'ㅛ': 'ㅗ', 'ㅜ': 'ㅠ', 'ㅠ': 'ㅜ', }
        self.replace_pair = None
        if path_pairs:
            self.replace_pair = self.load_pairs(path_pairs)

    def load_pairs(self, path):
        with open(path, 'r', encoding='utf-8') as r:
            contents = [l.split('\t') for l in r.read().split('\n')]
        dictionary = {k: v for k, v in contents if k != v and k.strip() != '' and len(k)>1}
        return dictionary

    def jamo_split(self, char):
        base = ord(char) - ord('가')
        c = base // 588
        v = (base - 588 * c) // 28
        f_c = base - 588 * c - 28 * v
        return [self.consonant[c], self.vowel[v], self.final_consonant[f_c]]

    def jamo_merge(self, jamo_list):
        c, v, f_c = [_list.index(j) for _list, j in zip([self.consonant, self.vowel, self.final_consonant], jamo_list)]
        return chr(f_c + 588 * c + 28 * v + ord('가'))

    def consonant_noise(self, content, prob=0.1):
        condition = lambda xlist: ((xlist[-1] == ' ') and (xlist[-2] not in self.exceptions))

        output = [self.jamo_split(ch) if re.match('[가-힣]', ch) else [ch, '', ''] for ch in content]
        output = [''.join(out).strip() if condition(out) and (random.random() < prob) else content[i] for i, out in
                  enumerate(output)]
        return ''.join(output)

    def vowel_noise(self, content, prob=0.1):
        output = [self.jamo_split(ch) if re.match('[가-힣]', ch) else [ch, '', ''] for ch in content]
        condition = lambda xlist: ((xlist[-1] == ' ') and (xlist[-2] in self.pairs))
        output = [
            self.jamo_merge([out[0], self.pairs[out[1]], out[2]]) if condition(out) and (random.random() < prob) else
            content[i] for i, out in enumerate(output)]
        return ''.join(output)

    def pronoun_noise(self, content, prob=0.1):
        assert (self.replace_pair is not None) and isinstance(self.replace_pair, dict)
        index_set = set()
        for key in reversed(sorted(self.replace_pair.keys(), key=len)):
            if key in content:
                idx = content.find(key)
                idxes = [i for i in range(idx, idx + len(key)) if i not in index_set]
                if random.random() < prob and len(idxes) == len(key):
                    content = content.replace(key, self.replace_pair[key])
                    index_set.update(idxes)
        return content
