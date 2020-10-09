#
# Build the brand images for the project.
#

ORIG=recteq.png

ORIG_URL=https://www.recteq.com/scs/img/Landing%20Pages/recteqWHT.png

IMGS=icon.png icon@2x.png logo.png logo@2x.png

BG="\#333333"

all: $(IMGS)

$(ORIG): Makefile
	curl -s $(ORIG_URL) > $(ORIG)

icon.png: $(ORIG) Makefile
	convert $< -resize 256x256 -background $(BG) -gravity center -extent 256x256 -flatten $@

icon@2x.png: $(ORIG) Makefile
	convert $< -resize 512x512 -background $(BG) -gravity center -extent 512x512 -flatten $@

logo.png: $(ORIG) Makefile
	convert $< -resize x256 -background $(BG) -flatten $@

logo@2x.png: $(ORIG) Makefile
	convert $< -resize x512 -background $(BG) -flatten $@

clean:  
	$(RM) $(ORIG) $(IMGS)

.PHONY: clean

# vim: set noet ts=4 sw=4 :
