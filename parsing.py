class parsing():
	def checkEmail(self, email):
		chars = "abcdefghijklmnopqrstuvwxyz."
		userchar = "abcdefghijklmnopqrstuvwxyz._-0123456789"
		if "@" in email and "." in email:
			if len(email.split("@")) == 2:
				dtl = len(email.split(".")[-1])
				if dtl >= 2 and dtl <= 5 : # TLD min 2 (max 63..) greater than 5 is very rare

					for c in email.split("@")[1].lower(): #check domain chars
						if c not in chars:
							return False

					for c in email.split("@")[0].lower(): #Check user chars
						if c not in userchar:
							return False

					return True

		return False


	def parseLink(self, base):
		if "/" in base:
			domain = base.split("/")[0]
			uri = base.split(f"{domain}/")[1]
			return domain.lower() + "/" + uri

		return base.lower()

	def getLink(self, line):
		chars = "abcdefghijklmnopqrstuvwxyz.-0123456789"
		prots = ["http://","https://","ftp://","www.", "android://", "smtp://", "imap://", "oauth://", "moz-proxy://", "chrome-extension://", "mailbox://"]
		limiters = [":", " ", "|", ";", "\n"]
		blackURL = [ '"','<', '>', '\\', '{', '}', '^', '|', '[', ']', '`', ' ', '\t', '\n', '\r']

		link = None

		c = 0
		for prot in prots:
			if prot in line:
				base = line.split(prot)[1]
#				print(base)
				for lim in limiters:
					newLine = False
#					print(base.replace("\n", ""), "->", lim)
					if lim in base:
						rawLink = base.split(lim)[0]

						link = self.parseLink(rawLink)

						isLink = True
						for blackChar in blackURL:
							if blackChar in link:
								isLink = False
								break

						if isLink == False:
							continue

#						print(base.replace("\n", ""), "|", rawLink, "->", lim)

						if f"{prot}{rawLink}{lim}" in line:
							newLine = line.replace(f"{prot}{rawLink}{lim}", "")
						elif f"{lim}{prot}{rawLink}" in line:
							newLine = line.replace(f"{lim}{prot}{rawLink}", "")
						elif f"{prot}{rawLink}" in line:
							newLine = line.replace(f"{prot}{rawLink}", "")

#						else:
#							break

						if prot == "android://":
							try:
								link = link.split("@")[1]
							except IndexError:
								None
						if newLine != False:
#							print(newLine)
							return prot, link, newLine


#				break

			else:
				c += 1

		if c == len(prots):
			for lim in limiters:
				if lim in line:
					uri = ""

					base = line.split(lim)[0]
					domain = base
					if base[:2] == "//":
						domain = base[2:]

					if "/" in base:
						domain = base.split("/")[0]
						uri = "/" + base.split("/")[1]


					if len(domain.split(".")) >= 2 and len(domain.split(".")) <= 4:
						ok = True
						for char in domain:
							if char not in chars:
								ok = False
								break

						if ok:
							link = domain.lower() + uri
							newLine = line.replace(domain + uri + lim, "")
							return prot, link, newLine

		return None, link, line

	def parse(self, line):
		prot, link, newLine = self.getLink(line)

		if link != None:
			line = newLine

		line.replace("\n", "")

		limiters = {
			":":";",  # check ?:? and ?:?;?
			";":":",  # check ?;? and ?;?:?
			" ":" ",  # check ? ? and ? ? ?
			"|":"|"   # check ?|? and ?|?|?
			}



		for k in limiters:
			email1 = None
			email2 = None
			passwd = None


			lim1 = k
			lim2 = limiters[k]

			try:

				if lim1 in line and lim1+lim2 not in line: # if ?:?
					vals = line.split(lim1)

					if self.checkEmail(vals[0]) and vals[1] != "": # if email:passwd
						email1 = vals[0].strip().lower()
						passwd = vals[1]
						if len(passwd.split(";")) == 2:
							if self.checkEmail(passwd.split(";")[0]): # if email:email;passwd
								email2 = passwd.split(";")[0].strip().lower()
								passwd = passwd.split(";")[1]

							elif self.checkEmail(passwd.split(";")[1]): # if email:passwd;email
								email2 = passwd.split(";")[1].strip().lower()
								passwd = passwd.split(";")[0]
						break

					elif self.checkEmail(vals[1]) and vals[0] != "": # if passwd:email
						email1 = vals[0].strip().lower()
						passwd = vals[1]
						break

				if lim1 in line and lim2 in line: # if ?:?;?
					vals = line.split(lim1)
					vals2 = vals[1].split(lim2)

					if self.checkEmail(vals[0]): # if email:?;?
						email1 = vals[0].strip().lower()

						if self.checkEmail(vals2[0]): # if email:email;passwd
							email2 = vals2[0].strip().lower()
							passwd = vals2[1]
							break

						elif self.checkEmail(vals2[1]) and vals2[0] != "": # if email:passwd;email
							email2 = vals2[1].strip().lower()
							passwd = vals2[0]
							break

						else: # ";" is part of passwd | email:pas;word
							passwd = vals[1]
							break

					elif self.checkEmail(vals2[0]) and self.checkEmail(vals2[1]) and vals[0] != "": # if passwd:email;email
						email1 = vals2[0].strip().lower()
						email2 = vals2[1].strip().lower()
						passwd = vals[0]
						break

			except IndexError as e: # Avoid unprogrammed patterns
#				print(e)
				continue


		if email1 != None or email2 != None:
			if passwd != None:
				try:
					if email1[-1] == lim1 or email1[-1] == lim2:
						email1 = email1[:-1]
				except (TypeError, IndexError):
					None
				try:
					if email2[-1] == lim1 or email2[-1] == lim2:
						email2 = email2[:-1]
				except (TypeError, IndexError):
					None

				return prot, link, email1, email2, passwd

		return None, None, None, None, None
