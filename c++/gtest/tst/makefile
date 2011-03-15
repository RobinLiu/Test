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

#includes for all compiles
INCLUDES =\
	-I ./ \
    -I $(GTEST_DIR)/include \
    -I $(SRC_INC_DIR)

LDFLAGS += gtest_main.a -lstdc++ -lrt 

#include ./ComponentMakefile

#---------
#
# ComponentMakefile
#
# Include this file in your makefile
# It makes
#    A static library
#    A test executable
#
# The necessary parameters are shown in 
#    ComponentMakefileExampleParameters
#
#----------

#Helper Functions
get_src_from_dir  = $(wildcard $1/*.cpp)  $(wildcard $1/*.cc) $(wildcard $1/*.c$)
get_src_from_dir_list = $(foreach dir, $1, $(call get_src_from_dir,$(dir)))				        
src_to_o = $(subst .c,.o, $(subst .cpp,.o,$(subst .cc,.o,$1)))
src_to_d = $(subst .c,.d, $(subst .cpp,.d,$(subst .cc,.d,$1)))
#move_file_location = $(patsubst %.d,build/%.d, $1)
src_to = $(subst .c,$1, $(subst .cpp,$1,$2))

#Derived 
SRC = $(call get_src_from_dir_list, $(SRC_DIRS))				        
OBJ = $(call src_to_o,$(SRC))

TEST_SRC = $(call get_src_from_dir_list, $(TEST_SRC_DIRS))
TEST_OBJS = $(call src_to_o,$(TEST_SRC))

ALL_SRC   = $(SRC) $(TEST_SRC)

#DEP_FILES = $(call move_file_location,$(call src_to_d, $(ALL_SRC))) 
DEP_FILES = $(call src_to_d, $(ALL_SRC))

#Test coverage with gcov
GCOV_OUTPUT = gcov_output.txt
GCOV_REPORT = gcov_report.txt
GCOV_ERROR = gcov_error.txt
GCOV_GCDA_FILES = $(call src_to,.gcda, $(ALL_SRC))
GCOV_GCNO_FILES = $(call src_to,.gcno, $(ALL_SRC))
TEST_OUTPUT = $(TEST_TARGET).txt

#Other stuff needed


CPPFLAGS += -Wall $(CXXFLAGS) $(INCLUDES) $(GCOVFLAGS)
CFLAGS += -Wall $(INCLUDES) $(CXXFLAGS)  $(GCOVFLAGS)
LDFLAGS  += -lstdc++

#The gcda files for gcov need to be deleted before each run
#To avoid annoying messages.
GCOV_CLEAN = $(SILENCE)rm -f $(GCOV_GCDA_FILES) $(GCOV_OUTPUT) $(GCOV_REPORT) $(GCOV_ERROR)
RUN_TEST_TARGET = $(SILENCE)  $(GCOV_CLEAN) ; echo "Running $(TEST_TARGET)"; ./$(TEST_TARGET)

# Targets
.PHONY:  all
all: gtest_main.a $(TEST_TARGET) 
	$(RUN_TEST_TARGET)

gtest-all.o : $(GTEST_SRCS_)
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c \
            $(GTEST_DIR)/src/gtest-all.cc

gtest_main.o : $(GTEST_SRCS_)
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c \
            $(GTEST_DIR)/src/gtest_main.cc

gtest.a : gtest-all.o
	$(AR) $(ARFLAGS) $@ $^

gtest_main.a : gtest-all.o gtest_main.o
	$(AR) $(ARFLAGS) $@ $^
	
.PHONY: flags
flags: 
	$(SILENCE)echo Compile with these flags:
	$(SILENCE)for f in $(CPPFLAGS) ; do \
		echo "    C++ $$f" ; \
	done
	$(SILENCE)for f in $(CFLAGS) ; do \
		echo "    C   $$f" ; \
	done
	
$(TEST_TARGET): $(TEST_OBJS) $(TARGET_LIB) 
	$(SILENCE)echo Linking $@
	$(SILENCE)$(CXX) $(CPPFLAGS) $^ $(LDFLAGS) -o $@

$(TARGET_LIB): $(OBJ)
	$(SILENCE)echo Building archive $@
	$(SILENCE)$(AR) $(ARFLAGS) $@ $^

test: $(TEST_TARGET)
	$(RUN_TEST_TARGET) | tee $(TEST_OUTPUT)
	
vtest: $(TEST_TARGET)
	$(RUN_TEST_TARGET) -v  | tee $(TEST_OUTPUT)

%.o: %.cpp
	@echo compiling $(notdir $<)
	$(SILENCE)$(COMPILE.cpp) -M -MF $(subst .o,.d,$@) -MT "$@ $(subst .o,.d,$@)" $<
	$(SILENCE)$(COMPILE.cpp) $(OUTPUT_OPTION) $<

%.o: %.cc
	@echo compiling $(notdir $<)
	$(SILENCE)$(COMPILE.cpp) -M -MF $(subst .o,.d,$@) -MT "$@ $(subst .o,.d,$@)" $<
	$(SILENCE)$(COMPILE.cpp) $(OUTPUT_OPTION) $<	
	
%.o: %.c
	@echo compiling $(notdir $<)
	$(SILENCE)$(COMPILE.cpp) -M -MF $(subst .o,.d,$@) -MT "$@ $(subst .o,.d,$@)" $<
	$(SILENCE)$(COMPILE.c) $(OUTPUT_OPTION) $<

ifneq "$(MAKECMDGOALS)" "clean"
-include $(DEP_FILES)
endif

.PHONY: clean
clean:
	$(SILENCE)echo Making clean
	$(SILENCE)$(RM) \
		$(TEST_TARGET) \
		$(TEST_TARGET).exe \
		$(OBJ) \
		$(TEST_OBJS)\
		$(TARGET_LIB)\
		$(DEP_FILES)\
		$(GCOV_GCNO_FILES)\
		$(GCOV_GCDA_FILES)\
		$(GCOV_ERROR)\
		$(GCOV_REPORT)\
		$(GCOV_OUTPUT)\
		$(TEST_OUTPUT)\
		gtest.a gtest_main.a *.o $(SRC_DIRS)/*.o
		
	$(SILENCE)find ../ -name \*.gcov | xargs rm -f
	$(SILENCE)find ../ -name \*.gcno | xargs rm -f
	$(SILENCE)find ../ -name \*.gcda | xargs rm -f

gcov: test
	$(SILENCE)for d in $(SRC_DIRS) ; do \
		gcov -o $$d $$d/*.c $$d/*.cpp >> $(GCOV_OUTPUT) 2>>$(GCOV_ERROR) ; \
	done
	$(CPPUTEST_HOME)/scripts/filterGcov.sh $(GCOV_OUTPUT) $(GCOV_ERROR) $(GCOV_REPORT) $(TEST_OUTPUT)
	cat $(GCOV_REPORT)



