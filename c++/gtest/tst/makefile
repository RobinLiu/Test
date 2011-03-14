#---------
#
# CppUTest Examples Makefile
#
#----------

#################### System settings ###########################
GTEST_DIR = ../../googletest
CPPFLAGS += -I$(GTEST_DIR)/include
CXXFLAGS += -g -Wall -Wextra
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h \
                $(GTEST_DIR)/include/gtest/internal/*.h
                
GTEST_SRCS_ = $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)

#################### Library ###################################
#Set this to @ to keep the makefile quiet
#SILENCE = @
#---- Outputs ----#
COMPONENT_NAME = gtest
TARGET_LIB = lib$(COMPONENT_NAME).a
TEST_TARGET = \
	$(COMPONENT_NAME)_tests


#--- Inputs ----#
CPPUTEST_HOME = ./
CPP_PLATFORM = Gcc -fprofile-arcs -ftest-coverage

#CFLAGS are set to override malloc and free to get memory leak detection in C programs
CFLAGS += -fprofile-arcs -ftest-coverage
#CFLAGS += -include $(CPPUTEST_HOME)/include/CppUTest/FindLeaksMalloc.h 
#CFLAGS += -Dmalloc=cpputest_malloc -Dfree=cpputest_free
#CFLAGS += -D __CPP_UNIT_TEST__  -DUTEST
CPPFLAGS += -g -I $(GTEST_DIR)/include
CFLAGS += -Werror
CPPFLAGS += -Werror
CPPFLAGS += -fprofile-arcs -ftest-coverage -DUTEST
GCOVFLAGS = -fprofile-arcs -ftest-coverage
CC += -fprofile-arcs -ftest-coverage

#SRC_DIRS is a list of source directories that make up the target library
#If test files are in these directories, their IMPORT_TEST_GROUPs need
#to be included in main to force them to be linked in.  By convention
#put them into an AllTests.h file in each directory
SRC_DIRS = ../src



#TEST_SRC_DIRS is a list of directories including
# - A test main (AllTests.cpp by conventin)
# - OBJ files in these directories are included in the TEST_TARGET
# - Consequently - AllTests.h containing the IMPORT_TEST_GROUPS is not needed
TEST_SRC_DIRS = ./

SRC_INC_DIR = ../src

#CMM_INC_DIR = $(CMM_HOME)/include

#includes for all compiles
INCLUDES =\
	-I ./ \
    -I $(GTEST_DIR)/include \
    -I $(SRC_INC_DIR)


#INCLUDES += $(PLATFORM_INCDIRS)/ $(PLATFORM_INCDIRS)/SS_LDAP/ 
#Flags to pass to ld
#LDFLAGS += -L$(FSAPI_LIBS) 
LDFLAGS += gtest_main.a -lstdc++ -lrt 

include ./ComponentMakefile
GCOV_CLEAN += *.xml
RUN_TEST_TARGET = $(SILENCE)  $(GCOV_CLEAN) ; echo "Running $(TEST_TARGET)"; ./$(TEST_TARGET) -v


