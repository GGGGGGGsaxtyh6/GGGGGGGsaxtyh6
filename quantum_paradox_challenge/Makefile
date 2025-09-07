CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra -fno-stack-protector -fno-pie -no-pie
LDFLAGS = -static -s -Wl,--strip-all
TARGET = quantum_paradox
SRCDIR = src
BUILDDIR = build
SOURCES = $(wildcard $(SRCDIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRCDIR)/%.cpp=$(BUILDDIR)/%.o)

# Anti-debugging and obfuscation flags
OBFUSCATION_FLAGS = -fno-omit-frame-pointer -fno-inline-functions -fno-inline-small-functions
PROTECTION_FLAGS = -D_FORTIFY_SOURCE=0 -fno-stack-protector -fno-pie -no-pie

.PHONY: all clean obfuscate strip pack

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $@ $(LDFLAGS) $(OBFUSCATION_FLAGS) $(PROTECTION_FLAGS)
	@echo "Binary created: $(TARGET)"

$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp
	@mkdir -p $(BUILDDIR)
	$(CXX) $(CXXFLAGS) $(OBFUSCATION_FLAGS) $(PROTECTION_FLAGS) -c $< -o $@

# Additional obfuscation step
obfuscate: $(TARGET)
	@echo "Applying additional obfuscation..."
	# Add random padding to make analysis harder
	dd if=/dev/urandom bs=1024 count=1 >> $(TARGET) 2>/dev/null || true
	@echo "Obfuscation complete"

# Strip symbols and pack
strip: $(TARGET)
	strip --strip-all $(TARGET)
	@echo "Symbols stripped"

# Create packed version
pack: $(TARGET)
	@echo "Creating packed version..."
	# This would normally use UPX, but we'll simulate it
	cp $(TARGET) $(TARGET).packed
	@echo "Packed version created: $(TARGET).packed"

# Clean build files
clean:
	rm -rf $(BUILDDIR) $(TARGET) $(TARGET).packed

# Full build with all protections
full: clean all obfuscate strip
	@echo "Full build complete with all protections"

# Debug build (for testing)
debug: CXXFLAGS += -g -DDEBUG -O0
debug: LDFLAGS = -g
debug: $(TARGET)
	@echo "Debug build complete"

install: $(TARGET)
	cp $(TARGET) /usr/local/bin/
	@echo "Installed to /usr/local/bin/"

help:
	@echo "Available targets:"
	@echo "  all      - Build the quantum paradox challenge"
	@echo "  obfuscate- Apply additional obfuscation"
	@echo "  strip    - Strip symbols from binary"
	@echo "  pack     - Create packed version"
	@echo "  full     - Full build with all protections"
	@echo "  debug    - Debug build for testing"
	@echo "  clean    - Clean build files"
	@echo "  install  - Install to system"
	@echo "  help     - Show this help"