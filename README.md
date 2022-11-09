# 한국어 노이즈 추가 (noising-korean)
한국어 문서에 노이즈를 추가하는 것을 도와주는 소스 코드입니다. 

이 레퍼지토리는 더이상 관리되지 않으며, 아래 링크에서 개발 및 발전 중입니다.

(PyPI 버전 - https://github.com/wisenut-research/konoise, Python+Rust)

## 실행 방법
```
python run_nosing_text.py --input_dir <input_directory> --output_dir <output_directory> \
--noise_mode spliting_noise --noise_prob 0.1 --prefix noised_ --delimiter \n --num_cores 16
```
- **input_dir**: 입력 파일들이 위치한 폴더의 경로입니다.
- **output_dir**: 출력 파일들이 저장될 폴더의 경로입니다(파일이름:<prefix>+<input_filename>).
- **noise_mode**: 노이즈를 생성하는 방법을 설정합니다(default:'jamo_split', support mode: ['jamo_split', 'vowel_change', 'phonological_change','add_dot','kor2eng', 'yamin']). 
- **noise_prob**: 노이즈가 생성될 확률을 결정합니다(default:0.1(range:[0,1]), 단위 문서에 대해 적용됩니다).
- **prefix**: 출력 파일 앞에 붙는 접두사입니다(default:'').
- **delimiter**: 입력 파일에서 문서의 단위화를 위한 분리 구분자입니다(default:'', 문장이 \n 으로 분리되어 있을 경우 \n으로 설정하여 단위 문장에 대해 노이즈를 추가합니다).
- **num_cores**: 멀티 프로세싱을 위한 cpu core의 개수를 설정합니다(default:사용가능한 모든 core 개수).
  


## 노이즈 생성 방법
노이즈를 생성하는 방법은 총 6가지가 구현되어 있습니다.

**[jamo_split]** 자모 분리(alphabet separation)에 의한 노이즈 추가 방법. 글자의 자음과 모음을 분리합니다. 단, 가독성을 위해 종성이 없으며 중성이  'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅗ' 가 아닐 경우 실행합니다(예: 안녕하세요 > 안녕ㅎㅏㅅㅔ요)

**[vowel_change]** 모음 변형에 의한 노이즈 추가 방법입니다. 글자의 모음을 변형시킵니다. 단, 가독성을 위해 종성이 없으며 중성이 'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ' 일 경우 실행합니다(예: 안녕하세요 > 안녕햐세오).

**[phonological_change]** 음운변화에 의한 노이즈 추가 방법입니다. 발음을 바탕으로 단어를 변형시킵니다(너무 닮았다 > 너무 달맜다).

**[add_noise]** 한국어 텍스트 사이에 온점(.)을 추가합니다(너무 닮았다 > 너.무 닮았.다.).

**[kor2eng]** 중성 중 일부를 영어로 변환합니다(너무 닮았다 > 너무 닮았ㄷr).

**[yamin]** 야민정음으로 일부 글자를 변환합니다. 단, 가독성이 떨어지는 일부 표현은 제외되었습니다(귀여워 > 커여워).



**변형 예시**
```
[original]  행복한 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이유로 불행하다.

[jamo_split, prob=1.] 행복한 ㄱㅏ정은 모두ㄱㅏ 닮았ㅈㅣ만, 불행한 ㄱㅏ정은 모두 ㅈㅓㅁㅏㄷㅏ의 ㅇㅣ유로 불행ㅎㅏㄷㅏ.

[vowel_change, prob=1.] 행복한 갸정은 묘듀갸 닮았지만, 불행한 갸정은 묘듀 져먀댜의 이우료 불행햐댜.

[phonological_change, prob=1.] 행복한 가정은 모두가 달맜지만, 불행한 가정은 모두 저마다의 이유로 불행하다.

[add_dot, prob=1.] 행.복.한. .가.정.은. .모.두.가. .닮.았.지.만.,. .불.행.한. .가.정.은. .모.두. .저.마.다.의. .이.유.로. .불.행.하.다...

[kor2eng, prob=1.] 행복한 ㄱr정은 모두ㄱr 닮았ㅈl만, 불행한 ㄱr정은 모두 저ㅁrㄷr의 ㅇl유로 불행ㅎrㄷr.

[yamin, prob=1.] 행복한 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이윾로 불행하다.

```

## 기타
- 'phonological_change' 방법은 현재 비음화, 유음화, 구개음화, 연음 등을 구현하고 있으며, 추후 확대될 예정입니다(누락된 규칙이 있을 수 있으니, 발견 시 피드백 주시면 감사하겠습니다).
- prob는 변형 가능한 글자들에 대해서 해당 확률만큼 확률적으로 실행됩니다(prob가 1이라고 해서 모든 텍스트가 변경되는 것이 아닙니다).
- 두 개 이상의 방법을 사용할 경우(쉼표로 구분), 한 단위 텍스트에서 두 개의 방법이 사용되는 것이 아니라 각 단위 텍스트마다 랜덤하게 방법을 결정하여 실행합니다. 
