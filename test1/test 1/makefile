all:word.exe

CPPFLAGS = -D__TEST__ -Wall -O0 -g3 -c -fmessage-length=0 
word.exe:  words.h words.o word_list.o VocabularyBase.o test.o words.h
	g++   -D__TEST__ -Wall -O0 -g3 -o  word.exe test.o words.o word_list.o VocabularyBase.o 

clean:
	rm test.o words.o word_list.o VocabularyBase.o word.exe