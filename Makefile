CXX = g++
CXXFLAGS = -O2 -Wall -fPIC

SRC_DIR = src
BUILD_DIR = build

SRCS = $(SRC_DIR)/pcg_rng.cpp
OBJS = $(BUILD_DIR)/pcg_rng.o
TARGET = $(BUILD_DIR)/libpcg_rng.so

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) -shared -o $@ $^

$(BUILD_DIR)/pcg_rng.o: $(SRCS)
	mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR)
