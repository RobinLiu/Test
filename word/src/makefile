CXXFLAGS =	-O0 -g3 -Wall -c -fmessage-length=0

OBJS =		help.o word.o CWord.o Cword_list.o

LIBS =

TARGET =	word.exe

$(TARGET):	$(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
