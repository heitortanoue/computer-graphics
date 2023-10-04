CXX = g++
CXXFLAGS = -std=c++11 -o3
LDFLAGS = -lglfw -lGL -lGLEW -lm

SRC_DIR = src
INC_DIR = headers
BUILD_DIR = build

SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp,$(BUILD_DIR)/%.o,$(SRCS))
EXEC = main

crun: clean all run

all: $(BUILD_DIR) $(EXEC)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -I$(INC_DIR) -c $< -o $@

run: $(EXEC)
	./$(EXEC)

clean:
	rm -rf $(BUILD_DIR) $(EXEC)
