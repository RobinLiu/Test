TARGET = word.exe
TEST = Test.exe

CPPUTEST = ./CppUTest
CPPFLAGS += -I $(CPPUTEST)/include 
LDLIBS += $(CPPUTEST)/lib/libCppUTest.a -lstdc++
CXXFLAGS +=	-O0 -g3 -Wall -c -fmessage-length=0

SRCOBJ = ./src/word.o ./src/help.o
TESTOBJ = ./tst/test.o ./tst/main.o ./src/help.o

all: $(TARGET) $(TEST)
	./$(TEST) -o junit 

$(TEST): $(TESTOBJ)
	$(CXX) $(CPPFLAGS) -o $(TEST) $(TESTOBJ) $(LDLIBS)

$(TARGET): ${SRCOBJ}
	$(CXX)  -o $(TARGET) $(SRCOBJ)

clean:
	rm -rf $(SRCOBJ) $(TESTOBJ)
	rm -f $(TARGET) $(TEST)


#g++ -O0 -g3 -Wall -c -fmessage-length=0 -osrc\word.o ..\src\word.cpp  #debug
#g++ -O3 -Wall -c -fmessage-length=0 -osrc\word.o ..\src\word.cpp  	   #release