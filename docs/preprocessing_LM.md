전제조건: kaldi_style 전처리가 끝나야댐

참고: uniq word

## 1) sentencepiece를 이용한 분절

```bash
cut -f2- -d ' ' text > corpus
spm_train --character_coverage 1.0 --model_prefix kt_32k --model_type bpe --vocab_size 32000 --input corpus
```

결과 파일: /home/CORPUS/kt/LM/kt_32k{.model,.vocab}, corpus

## 2) 단어 사전 구축

```bash
cut -f1 kt_32k.vocab > vocab
```

vocab에서 ▁ 만 있는 단어를 제거 해야 함

vi 에서 /^▁$ 으로 검색해서 제거함

<s>, </s>, <unk>도 제거

```bash
mkdir -p kaldi/egs/kt/s5/data/local/lm
cat kaldi/egs/kt/s5/data/train_kt/vocab | python g2p_sogang/g2p.py > kaldi/egs/kt/s5/data/local/lm/lexicon_nosil.txt
```

결과 파일: /home/CORPUS/kt/LM/lexicon_nosil.txt vocab, corpus_encoded

## 3) [lm.arpa](http://lm.arpa) 생성

```bash
ngram-count -vocab vocab -text corpus_encoded -order 3 -write count -lm lm.arpa -prune 1e-8 -wbdiscount1 -wbdiscount2 -wbdiscount3
```

결과 파일: /home/CORPUS/kt/LM/lm.arpa, count

## 4) L.fst 생성

```bash
./local/prepare_dict.sh data/local/lm data/local/dict_nosp
./utils/prepare_lang.sh data/local/dict_nosp "<UNK>" data/local/lang_nosp_tmp data/lang_nosp
```

## 5) G.fst  생성

```bash
./local/format_lms.sh data/local/lm
```

## 6) data/train_kt에 있는 text를 분절된 text로 변경

```bash
cut -f1 -d ' ' text | paste -d ' ' - ../local/lm/corpus_encoded > text.tmp && mv text text_origin && mv text.tmp text
```
