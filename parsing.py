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

	def parse(self, line):
		line = line.replace("\n", "")

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

				return email1, email2, passwd

		return None, None, None
