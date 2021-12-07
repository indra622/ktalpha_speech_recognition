## Eunsoo Cho
## ASR result postprocessing 


from jamo import j2h 
import csv
start_syllable=['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
vowel=['ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ','ㅐ','ㅒ','ㅔ','ㅖ','ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ']
end_syllable=['ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
start_syllable.extend(end_syllable)
start_syllable=sorted(set(start_syllable))
#print(start_syllable)


def post_processing(string):
    output_string='';i=0
    while i<len(string):
        if (i<len(string)-1) and (string[i] in vowel) and (string[i+1] in end_syllable):
            #print(j2h('ㅇ', string[i],string[i+1]))
            output_string+=(j2h('ㅇ', string[i],string[i+1]))
            i+=2
        elif string[i] in vowel:
            #print(j2h('ㅇ',string[i]))
            output_string+=j2h('ㅇ',string[i])
            i+=1
        elif string[i] in start_syllable:
            i+=1
        if i in range(len(string)):
            output_string+=string[i]
        i+=1;#print(string[i]);print(i);

    return output_string


# 1. Receive input
#string=input("오타가 포함된 문장을 입력해주세요.")
tsv_file=open("final.csv")
tsv_file2=open("final2.csv", "w")
read_tsv=csv.reader(tsv_file, delimiter=",")
for row in read_tsv:
    wr=csv.writer(tsv_file2, delimiter=",")
    wr.writerow([row[0], post_processing(row[1])])

tsv_file.close()
tsv_file2.close()
