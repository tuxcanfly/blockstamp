BASEDIR=$(CURDIR)

HOST=tuxcanfly.me
PORT=774
USER=tuxcanfly

BLOCKSTAMP=/home/tuxcanfly/build/blockstamp
MIGRATIONS=$(BLOCKSTAMP)/stamper/migrations
VIRTUALENV=$(BLOCKSTAMP)/.env

MEDIA=media
DB_FILE=db.sqlite3
HTML=$(MEDIA)/html
MANAGE=$(BLOCKSTAMP)/manage.py
STATIC=$(BLOCKSTAMP)/static

help:
	@echo 'Makefile for blockstamp website                                        '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make init                        initialize project                 '
	@echo '   make clean                       remove the generated files         '
	@echo '   make shell                       drop to server shell               '
	@echo '   make nukedb                      nuked the server db (use CAUTION)  '
	@echo '   make deploy                      deploy the web site via SSH        '
	@echo '                                                                       '

warning:
	@printf "Are you sure? (y/n) "; \
	read reply; \
	if [[ ! $$reply =~ ^[Yy]$$ ]]; then \
		exit 1;\
	fi;

init: clean $(HTML)
	$(MANAGE) migrate

$(HTML):
	mkdir -p $(HTML)

clean:
	rm -r $(MEDIA) $(DB_FILE)

shell:
	ssh -t -p $(PORT) $(USER)@$(HOST) "source $(VIRTUALENV)/bin/activate && $(MANAGE) shell_plus"

nukedb: warning
	ssh -p $(PORT) $(USER)@$(HOST) "cd $(BLOCKSTAMP) && rm -r $(MEDIA) $(DB_FILE)"
	ssh -p $(PORT) $(USER)@$(HOST) "cd $(BLOCKSTAMP) && source $(VIRTUALENV)/bin/activate && $(MANAGE) migrate --no-input"
	ssh -p $(PORT) $(USER)@$(HOST) "cd $(BLOCKSTAMP) && mkdir -p $(HTML)"

deploy:
	ssh -p $(PORT) $(USER)@$(HOST) "cd $(BLOCKSTAMP) && git pull origin master"
	ssh -p $(PORT) $(USER)@$(HOST) "cd $(BLOCKSTAMP) && rm -rf $(STATIC)"
	ssh -p $(PORT) $(USER)@$(HOST) "cd $(BLOCKSTAMP) && npm run build"
	ssh -p $(PORT) $(USER)@$(HOST) "source $(VIRTUALENV)/bin/activate && $(MANAGE) collectstatic --no-input"
	ssh -t -p $(PORT) $(USER)@$(HOST) "sudo supervisorctl restart blockstamp"

.PHONY: init clean deploy
