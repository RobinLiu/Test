CPPUTEST = ../CppUTest
CPPFLAGS += -I $(CPPUTEST)/include
LDLIBS += $(CPPUTEST)/lib/libCppUTest.a -lstdc++
OBJS =		test.o main.o ../src/help.o
TARGET =	TestFirst.exe	
CXXFLAGS =	-O0 -g3 -Wall -c -fmessage-length=0
 
all:	$(TARGET)	
	./$(TARGET)
 
$(TARGET): $(OBJS)
	$(CXX) $(CPPFLAGS) -o TestFirst $(OBJS) $(LDLIBS)
	


clean:
	rm -f $(OBJS) $(TARGET)
