import re
import random


class NoiseGenerator(object):
    def __init__(self):
        self.consonant = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        self.vowel = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ',
                      'ㅢ', 'ㅣ']
        self.final_consonant = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ',
                                'ㅂ',
                                'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        self.exceptions = ['ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅗ']
        self.pairs = {'ㅏ': 'ㅑ', 'ㅑ': 'ㅏ', 'ㅓ': 'ㅕ', 'ㅕ': 'ㅓ', 'ㅗ': 'ㅛ', 'ㅛ': 'ㅗ', 'ㅜ': 'ㅠ', 'ㅠ': 'ㅜ', }

        self.formal_morpheme = [self.jamo_split(mor) for mor in ['이', '을', '를', '은', '았', '었']]
        self.oral_consonant = ['ㄱ', 'ㄷ', 'ㄹ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅎ']
        self.nasal_consonant = ['ㅁ', 'ㄴ', 'ㅇ']
        self.liquid_consonant = ['ㄹ']

    def load_pairs(self, path):
        with open(path, 'r', encoding='utf-8') as r:
            contents = [l.split('\t') for l in r.read().split('\n')]
        dictionary = {k: v for k, v in contents if k != v and k.strip() != ''}
        return dictionary

    def jamo_split(self, char):
        base = ord(char) - ord('가')
        c = base // 588
        v = (base - 588 * c) // 28
        f_c = base - 588 * c - 28 * v
        return [self.consonant[c], self.vowel[v], self.final_consonant[f_c]]

    def jamo_merge(self, jamo_list):
        if jamo_list[1:] == ['', '']:
            return jamo_list[0]
        c, v, f_c = [_list.index(j) for _list, j in zip([self.consonant, self.vowel, self.final_consonant], jamo_list)]
        return chr(f_c + 588 * c + 28 * v + ord('가'))

    def spliting_noise(self, content, prob=0.1):
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
            content[i] for i, out in
            enumerate(output)]
        return ''.join(output)

    def palatalization(self, fc, nc):
        palatal = {'ㄷ': 'ㅈ', 'ㅌ': 'ㅊ'}
        if (fc[-1] in palatal) and nc[:-1] == ['ㅇ', 'ㅣ']:
            nc[0] = palatal[fc[-1]]
            fc[-1] = ' '
        return fc, nc

    def linking(self, fc, nc):
        links = {'ㄻ': 'ㄹㅁ', 'ㅄ': 'ㅂㅆ', 'ㄳ': 'ㄱㅅ', 'ㄽ': 'ㄹㅅ', 'ㅊ': ' ㅊ', 'ㅂ':' ㅂ', 'ㅍ': ' ㅂ'}
        if (fc[-1] in links) and (nc in self.formal_morpheme):
            fc[-1], nc[0] = links[fc[-1]]
        return fc, nc

    def liquidization(self, fc, nc):
        liquid_set = {'ㄴㄹ': 'ㄹㄹ', 'ㄹㄴ': 'ㄹㄹ', 'ㄾㄴ':'ㄹㄹ'}
        exception_set = {'ㄴㄹㅕㄱ':'ㄴㄴ'}

        if fc[-1]+''.join(nc) in exception_set:
            fc[-1], nc[0] = exception_set[fc[-1]+''.join(nc)]
            return fc, nc
        else:
            if fc[-1] + nc[0] in liquid_set:
                fc[-1], nc[0] = liquid_set[fc[-1] + nc[0]]
            return fc, nc

    def nasalization(self, fc, nc):
        nasalization_set = {'ㅂㅁ': 'ㅁㅁ', 'ㄷㄴ': 'ㄴㄴ', 'ㄱㅁ': 'ㅇㅁ', 'ㄱㄴ': 'ㅇㄴ', 'ㅇㄹ': 'ㅇㄴ',
                            'ㅁㄹ': 'ㅁㄴ', 'ㄲㄴ': 'ㅇㄴ', 'ㄱㄹ': 'ㅇㄴ', 'ㅂㄹ': 'ㅁㄴ', 'ㄱㄹ': 'ㅇㄴ',
                            'ㅊㄹ': 'ㄴㄴ', 'ㄺㄴ': 'ㅇㄴ', 'ㅍㄴ': 'ㅁㄴ'}
        fc_c = fc[-1] + nc[0]
        if fc_c in nasalization_set:
            fc[-1], nc[0] = nasalization_set[fc_c]
        return fc, nc

    def assimilation(self, fc, nc):
        # assimilation not employed in the nasalization function. each other has the similar rules.
        reverse_assimil = {'ㄺㄴ':'ㅇㄴ'}
        fc_c = fc[-1] + nc[0]
        if fc_c in reverse_assimil:
            fc[-1], nc[0] = reverse_assimil[fc_c]
        return fc, nc

    def phonological_process(self, content, prob=0.3):
        uncased = [self.jamo_split(ch) if re.match('[가-힣]', ch) else [ch, '', ''] for ch in content]

        for i in range(len(uncased) - 1):
            if random.random() < prob:
                uncased[i], uncased[i + 1] = self.palatalization(uncased[i], uncased[i + 1])
                uncased[i], uncased[i + 1] = self.linking(uncased[i], uncased[i + 1])
                uncased[i], uncased[i + 1] = self.liquidization(uncased[i], uncased[i + 1])
                uncased[i], uncased[i + 1] = self.nasalization(uncased[i], uncased[i + 1])

        content = ''.join([self.jamo_merge(unc) for unc in uncased])
        return content


if __name__=='__main__':
    gen = NoiseGenerator()
    sample_text = '행복한 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이유로 불행하다. '
    sample_text='같이 있을 때. 무릎이 아프다. 앞날이 창창하다. 공권력'
    print('original:', sample_text)
    print('noised1:', gen.spliting_noise(sample_text, prob=1))
    print('noised2:', gen.vowel_noise(sample_text, prob=1))
    print('noised3:', gen.phonological_process(sample_text, prob=1))
