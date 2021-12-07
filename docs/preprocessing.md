## 1) json list 불러오기

```bash
find .json /home/CORPUS/kt/DATASET/TRAIN_0{1,2,3}_JSON_ALL > jsonpath
```

결과 파일:  /home/CORPUS/kt/kaldi_style/jsonlist

## 2) pcm list 불러오기

```bash
find .pcm /home/CORPUS/kt/DATASET/TRAIN_0{1,2,3}_PCM > wavpath
```

결과 파일:  /home/CORPUS/kt/kaldi_style/wavlist

## 3) json list로부터 transcript 읽어오기.

JSON parsing을 실시함

$sudo apt-get install jq 써서 jq 설치한다음에 사용함

```bash
cat jsonlist | while read line; do cat $line | jq .script.script_TN >> transcript;done
```

결과 파일: /home/CORPUS/kt/kaldi_style/transcript

## 4) 발성 안하는 단어 제외

### 61768번째 utterance

"미 존스홉킨스대학은 이십 구 일 ( 현지시간) 미국의 [코로나 일 구] 사망자 수를 [삼천 칠백 이십 오 명]으로 집계했다." 

'현지시간' 발성안하는거 확인함. 지워야됨

## 5) 특수문자 제외

vi editor 사용함

```bash
:%s/[^가-힣a-zA-Z0-9 ]/ /g
:%s/  / /g
```

## 6) 바뀌어있지 않은 영어, 숫자 찾아서 바꿈

### Transcription 중 숫자, 영어가 바뀌지 않은 것에 대한 단어사전

TV → 티브이

B조 → 비조

PIN → 핀

AS → 에이에스

GS홈쇼핑 → 지에스홈쇼핑

n (\n이 있었는데 \이 지워진거) → 삭제

LG전자 → 엘지전자

1위 → 일위

4만 → 사만

28일 → 이십팔일

2시 → 두시

3층 → 삼층

3 회 초 → 삼 회 초

43.5% → 사십삼점오 퍼센트

결과 파일: /home/CORPUS/kt/kaldi_style/transcript_refine

## 6) PCM이랑 JSON 동기화 및 path-transcription matching

경로에서 JSON_ALL을 PCM으로, .json을 .pcm으로, .JSON을 .PCM으로 변경

```bash
:%s/JSON_ALL/PCM/g
:%s/\.json/\.pcm/g
:%s/\.JSON/\.PCM/g
```

결과 파일: /home/CORPUS/kt/kaldi_style/json_to_pcm_list

경로와 transcript를 key value 형식으로 연결

```bash
paste -d ' ' json_to_pcm_list transcript_refine > text_origin
```

결과 파일: /home/CORPUS/kt/kaldi_style/text_origin

## 7) 불량파일검출

직접 들어보고 실제 음성이 녹음되어있지 않은 불량 파일을 제거함

결과:183496 →183,483줄

파일명:     

- DATASET/TRAIN_02_PCM/001/CARDINAL_1875_F_50_SEOUL_SEOUL_NORMAL_SMARTPHONE_612C896756ACD13EF76903AA
- TRAIN_02_PCM/001/CARDINAL_1937_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_612C890C56ACD13EF769039A.PCM
- TRAIN_02_PCM/001/CARDINAL_2024_M_30대_SEOUL_SEOUL_NORMAL_SMARTPHONE_613F6F25F1E6FFAD61AB0602
- TRAIN_02_PCM/001/CARDINAL_1875_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_612C896756ACD13EF76903AA.PCM
- TRAIN_02_PCM/001/CARDINAL_1937_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_612C890C56ACD13EF769039A
- TRAIN_02_PCM/004/CARDINAL_39523_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_6156B86DD3BE79D9D458E351
- TRAIN_02_PCM/004/CARDINAL_39550_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_6156B8E6D3BE79D9D458E3A9
- TRAIN_02_PCM/004/CARDINAL_39551_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_6156B8E8C109293D7ED02185
- TRAIN_03_PCM/002/UNIT_13369_M_30대_SEOUL_SEOUL_NORMAL_SMARTPHONE_613f492c444e25fb2fcbbcb9
- TRAIN_03_PCM/003/UNIT_13656_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_614c1608679bc111c0022f3e
- TRAIN_03_PCM/003/UNIT_14188_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_614bd9c27efa3083a4040bcb
- TRAIN_03_PCM/003/UNIT_14333_F_40대_CHUNGCHEONG_SEOUL_NORMAL_SMARTPHONE_61318cb70e32cbb720282d63
- TRAIN_03_PCM/004/UNIT_15132_F_40대_SEOUL_SEOUL_NORMAL_SMARTPHONE_61318d169cecb711c7560bb
- TRAIN_02_PCM/003/CARDINAL_36771_F_30대_SEOUL_GYEONGSANG_NORMAL_SMARTPHONE_61513DACDA98AD2315BA9E5B.PCM
- TRAIN_02_PCM/001/CARDINAL_1493_F_50대_SEOUL_SEOUL_NORMAL_SMARTPHONE_612C898EC8EA0427F63033B8.PCM

결과 파일: /home/CORPUS/kt/kaldi_style/text

## 7) Kaldi-style conversion

필요 준비물: wav.scp, text, utt2spk, spk2utt

kaldi는 정렬이 되어있지 않은 경우 정상적으로 작동하지 않음

이유는 모르겠지만 linux sort로는 안되니 vi의 sort로 함

text로부터 key값을 추출하고 wav.scp로 함

path가 그대로 key가 됨 (이유: ID값이 고유하지 않음...)

덩달아 utt2spk, spk2utt도 wav.scp와 같은 값을 가지게 됨

```bash
:sort
cut -f1 -d ' ' text > key && paste -d ' ' key key > wav.scp
cp wav.scp utt2spk
cp wav.scp spk2utt
```

결과 파일: /home/CORPUS/kt/kaldi_style/{key,wav.scp,utt2spk,spk2utt}

## 8) SGspeech-style conversion

필요 준비물: text, utt2dur

duration을 구할 방법은 여러 가지가 있으나 MFCC 뽑으면 kaldi가 해주기 때문에 MFCC뽑으면서 나온걸 그대로 사용할 거임

SGspeech-style data는  path\tduration\ttranscription으로 이루어짐

그리고 음절 기반으로 하면 output node가 너무 많아지기 때문에 grapheme으로 바꾸고 사용할 거임

utt2dur의 delimiter는 space이므로, \t로 변경한 뒤 사용

```bash
cp utt2dur ut && vi ut
:%s/ /\t/g
cut -f2- -d ' ' text | paste -d '\t' ut - > transcripts_origin.tsv
```

transcripts_origin.tsv상태에서 다시 분리한 뒤, grapheme으로 변환함

```python
# tograp.py
# jamo install: pip install jamo
import sys
from jamo import h2j, j2hcj

with open(sys.argv[1], 'rt') as f:
	lines = f.readlines()
	for line in lines:
		jamo_str = j2hcj(h2j(line))
		print(jamo_str.strip())
```

```python
cut -f3- transcripts_origin.tsv > only_trans
python tograp.py only_trans > grap_trans
cut -f1,2 transcripts_origin.tsv | paste -d '\t' - grap_trans > transcripts.tsv
```
