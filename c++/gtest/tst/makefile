#---------
#
# GoogleTest Examples Makefile
#
#----------
#---- Outputs ----#
COMPONENT_NAME = gtest
GTEST_DIR = ../../googletest
SRC_DIRS = ../src
TEST_SRC_DIRS = ./
SRC_INC_DIR = $(SRC_DIRS)


#################### Google settings ###########################

CPPFLAGS += -I$(GTEST_DIR)/include
CXXFLAGS += -g -Wall -Wextra
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h \
                $(GTEST_DIR)/include/gtest/internal/*.h                
GTEST_SRCS_ = $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)

#################### Library ###################################
#Set this to @ to keep the makefile quiet
#SILENCE = @

TARGET_LIB = lib$(COMPONENT_NAME).a
TEST_TARGET = $(COMPONENT_NAME)_tests

CPPFLAGS += -g -I $(GTEST_DIR)/include
CFLAGS += -Werror
CPPFLAGS += -Werror
GCOVFLAGS = -fprofile-arcs -ftest-coverage
CC += -fprofile-arcs -ftest-coverage

#CMM_INC_DIR = $(CMM_HOME)/include

#includes for all compiles
INCLUDES =\
	-I ./ \
    -I $(GTEST_DIR)/include \
    -I $(SRC_INC_DIR)

LDFLAGS += gtest_main.a -lstdc++ -lrt 

include ./ComponentMakefile
GCOV_CLEAN += *.xml
RUN_TEST_TARGET = $(SILENCE)  $(GCOV_CLEAN) ; echo "Running $(TEST_TARGET)"; ./$(TEST_TARGET) -v


