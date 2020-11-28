# noising_korean
한국어 문서에 노이즈를 추가하는 것을 도와주는 소스 코드입니다.

## 실행 방법
```
python run_nosing_text.py --input_dir <input_directory> --output_dir <output_directory> \
--noise_mode vowel_noise --noise_prob 0.1 --prefix noised_ --delimiter \n --num_cores 16
```
- input_dir: 입력 파일들이 위치한 폴더의 경로입니다.
- output_dir: 출력 파일들이 저장될 폴더의 경로입니다(파일이름:<prefix>+<input_filename>).
- noise_mode: 노이즈를 생성하는 방법을 설정합니다(default:vowel_noise). 
- noise_prob: 노이즈가 생성될 확률을 결정합니다(default:0.1, 단위 문서에 대해 적용됩니다).
- prefix: 출력 파일 앞에 붙는 접두사입니다(default:'').
- delimiter: 입력 파일에서 문서의 단위화를 위한 분리 구분자입니다(default:'', 문장이 \n 으로 분리되어 있을 경우 \n으로 설정하여 단위 문장에 대해 노이즈를 추가합니다).
- num_cores: 멀티 프로세싱을 위한 cpu core의 개수를 설정합니다(default:사용가능한 모든 core 개수).
