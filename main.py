#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from datetime import date, timedelta
from settings import CLIENT_ID, CLIENT_SECRET, CLIENT_IBAN

class Bank(object):
	AUTH_URL = 'https://www.net444.caisse-epargne.fr/login.aspx'
	LOAD_URL = 'https://www.net444.caisse-epargne.fr/Portail.aspx'
	RTRV_URL = 'https://www.net444.caisse-epargne.fr/Pages/telechargement.aspx'

	MAX_DAYS_AGO = 60
	MIN_DAYS_AGO = 1
	def __init__(self, client_id, client_secret, client_iban):
		self.client_id = client_id
		self.client_secret = client_secret
		self.client_iban = client_iban

		self.today = date.today()

		self.request = requests.session()
	def _authenticate(self):
		auth_payload = {
			'codconf': CLIENT_SECRET,
			'nuabbd': CLIENT_ID,
			'ctx': '',
			'ctx_routage': ''
		}
		self.request.post(
			self.AUTH_URL,
			verify=True,
			data=auth_payload
		)
	def _load(self, start, end):
		load_payload = {
			'MM$TELECHARGE_OPERATIONS$ddlChoixLogiciel': '2', # 2 qif, 3 csv
			'MM$TELECHARGE_OPERATIONS$groupeDate': 'fourchette',
			'MM$TELECHARGE_OPERATIONS$m_DateDebut$txtDate': start,
			'MM$TELECHARGE_OPERATIONS$m_DateFin$txtDate': end,
			'MM$TELECHARGE_OPERATIONS$m_ExDDLListeComptes': 'C#{0}#{1}#EUR'.format(self.client_iban, self.today.strftime('%Y%m%d')),
			'__ASYNCPOST': 'true',
			'__EVENTARGUMENT': '',
			'__EVENTTARGET': 'MM$TELECHARGE_OPERATIONS$m_ChoiceBar$lnkRight',
			'__EVENTVALIDATION': '/wEWFwLV69TrAgKmgdyDDwKDm/v8AwKCqKGkDwL/rvvMCALBp+nqBQLClY6BBALDk9inCQLEjq75DAL+66GiDgLvtZeeBQLq2pjnBAKqs4D7CwK4p/LXAwK/pZuhCwK+pZuhCwKipZuhCwK9pZuhCwK8pZuhCwKj2Y/HAQLLw/+/CQK2pfrhDgK6qqWLDA==',
			'__LASTFOCUS': '',
			'__VIEWSTATE': '/wEPDwUJMjMyNDU3NTcyD2QWAgIBD2QWBAIDDw8WBB4RTFBfQ0FSVFJJREdFQ0lCTEUyswwAAQAAAP////8BAAAAAAAAAAwCAAAAS0JBRC5Db21tb24uVG9vbHMsIFZlcnNpb249Mi4wLjAuMjI1MjQsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUBAAAAGkJBRC5Db21tb24uVG9vbHMuRGF0YS5EYXRhAQAAABhEaWN0aW9uYXJ5QmFzZStoYXNodGFibGUDHFN5c3RlbS5Db2xsZWN0aW9ucy5IYXNodGFibGUCAAAACQMAAAAEAwAAABxTeXN0ZW0uQ29sbGVjdGlvbnMuSGFzaHRhYmxlBwAAAApMb2FkRmFjdG9yB1ZlcnNpb24IQ29tcGFyZXIQSGFzaENvZGVQcm92aWRlcghIYXNoU2l6ZQRLZXlzBlZhbHVlcwAAAwMABQULCBxTeXN0ZW0uQ29sbGVjdGlvbnMuSUNvbXBhcmVyJFN5c3RlbS5Db2xsZWN0aW9ucy5JSGFzaENvZGVQcm92aWRlcgjsUTg/HAAAAAoKFwAAAAkEAAAACQUAAAAQBAAAAAkAAAAGBgAAABBTb2xTZWN1cml0eUxldmVsBgcAAAAIRW5yb2xTb2wGCAAAABpTb2xQYXJ0aWN1bGFyU2VjdXJpdHlMZXZlbAYJAAAABG1lbnUGCgAAAAhCQVNFX1VSTAYLAAAABHRhc2sGDAAAAA1Tb2xBYm9ubmVtZW50Bg0AAAAPQXV0aHJBYm9ubmVtZW50Bg4AAAADQ1RYEAUAAAAJAAAACAgAAAAACQ8AAAAICAAAAAAGEAAAAAExBhEAAAAtaHR0cHMlM2ElMmYlMmZ3d3cubmV0NDQ0LmNhaXNzZS1lcGFyZ25lLmZyJTJmBhIAAAAIQ1BURE1URTAJEwAAAAkUAAAABhUAAACzBW1hcj0xMDEmYmFzZV91cmw9aHR0cHMlM2ElMmYlMmZ3d3cubmV0NDQ0LmNhaXNzZS1lcGFyZ25lLmZyJTJmJnJlZz0xNDQ0NSZzYz0yJnR5cHNydj13ZSZwZmw9SkFCQUUwJm5hZz0yMTUmbmFiPTYzZGE0MjM2NTliZDIzZTJjNjgyNzU3YzU5ZWExNjBjJmF1dGg9MSZpc2NpYmxlPXRydWUmdXNlcm5hbWU9TSBKVUxJRU4gTUFJU09OTkVVVkUmY29uc2VpbGxlcm5hbWU9TW9uIGNvbnNlaWxsZXIgOiAgTU1FIEVMTEVOIEdJUkFSRCZuYnJtZXNzYWdlPTAmc2l0ZW5pdjI9MTkmdXBhcmFjdGlmPTEmdXBhcnRyYW5zYWN0PTB8MXwzfDJ8NHwmYmFzZV91cmxfZGVpPWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZiZiYXNlVVJMPWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZiZyZXR1cm5fdXJsPWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZlBvcnRhaWwuYXNweCUzRnRhY2hlJTNEQ1BUU1lOVDAmY2FydHJpZGdlX3VybD1odHRwcyUzYSUyZiUyZnd3dy5uZXQ0NDQuY2Fpc3NlLWVwYXJnbmUuZnIlMmZwYWdlcy9jYXJ0cmlkZ2UuYXNweCUzRmlmciUzRDEmY2FydHJpZGdlaW5kX3VybD1odHRwcyUzYSUyZiUyZnd3dy5uZXQ0NDQuY2Fpc3NlLWVwYXJnbmUuZnIlMmZwYWdlcy9jYXJ0cmlkZ2VpbmQuYXNweCUzRmlmciUzRDEMFgAAAEpCQUQuQkxMLkNvbW1vbiwgVmVyc2lvbj0xMy45LjAuMTc0NDYsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUPAAAAHkJBRC5CTEwuQ29tbW9uLkVFdGF0U2VydmljZVNvbAEAAAAHdmFsdWVfXwAIFgAAAAoAAAAFEwAAACdCQUQuQkxMLkNvbW1vbi5FRXRhdFNvdXNjcmlwdGlvblNlcnZpY2UBAAAAB3ZhbHVlX18ACBYAAAABAAAAARQAAAATAAAAAQAAAAseBFZJRVcFDkNBUlRSSURHRUNJQkxFZBYCZg9kFgJmD2QWBGYPFgIeA3NyYwX7BWh0dHBzOi8vd3d3LmNhaXNzZS1lcGFyZ25lLmZyL1JlZ2lzdGVyQ29udGV4dC5hc3B4P21hcj0xMDEmYmFzZV91cmw9aHR0cHMlM2ElMmYlMmZ3d3cubmV0NDQ0LmNhaXNzZS1lcGFyZ25lLmZyJTJmJnJlZz0xNDQ0NSZzYz0yJnR5cHNydj13ZSZwZmw9SkFCQUUwJm5hZz0yMTUmbmFiPTYzZGE0MjM2NTliZDIzZTJjNjgyNzU3YzU5ZWExNjBjJmF1dGg9MSZpc2NpYmxlPXRydWUmdXNlcm5hbWU9TSBKVUxJRU4gTUFJU09OTkVVVkUmY29uc2VpbGxlcm5hbWU9TW9uIGNvbnNlaWxsZXIgOiAgTU1FIEVMTEVOIEdJUkFSRCZuYnJtZXNzYWdlPTAmc2l0ZW5pdjI9MTkmdXBhcmFjdGlmPTEmdXBhcnRyYW5zYWN0PTB8MXwzfDJ8NHwmYmFzZV91cmxfZGVpPWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZiZiYXNlVVJMPWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZiZyZXR1cm5fdXJsPWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZlBvcnRhaWwuYXNweCUzRnRhY2hlJTNEQ1BUU1lOVDAmY2FydHJpZGdlX3VybD1odHRwcyUzYSUyZiUyZnd3dy5uZXQ0NDQuY2Fpc3NlLWVwYXJnbmUuZnIlMmZwYWdlcy9jYXJ0cmlkZ2UuYXNweCUzRmlmciUzRDEmY2FydHJpZGdlaW5kX3VybD1odHRwcyUzYSUyZiUyZnd3dy5uZXQ0NDQuY2Fpc3NlLWVwYXJnbmUuZnIlMmZwYWdlcy9jYXJ0cmlkZ2VpbmQuYXNweCUzRmlmciUzRDEmaD02MzUxOTUwNTgzODczNDM3NTBkAgIPDxYKHghDc3NDbGFzcwULYm91dG9uLXJvbmQeB1Rvb2xUaXAFD1NlIGTDqWNvbm5lY3Rlch4EVGV4dAWXATxzcGFuIGNsYXNzPSdwaWN0by1kZWNvbm5lY3Rlcic+PGltZyBzcmM9J2h0dHBzOi8vd3d3LmNhaXNzZS1lcGFyZ25lLmZyL2NhY2hlL2NzczEzMDFfaW1nL3RyYW5zcGFyZW50LmdpZicgc3R5bGU9J2JvcmRlcjpub25lJyAvPk1lIGTDqWNvbm5lY3Rlcjwvc3Bhbj4eC0NvbW1hbmROYW1lZR4EXyFTQgICZGQCBQ8PFgYeDExhc3RWaWV3TmFtZQUVVEVMRUNIQVJHRV9PUEVSQVRJT05THgdMUF9NQUlOMt4IAAEAAAD/////AQAAAAAAAAAMAgAAAEtCQUQuQ29tbW9uLlRvb2xzLCBWZXJzaW9uPTIuMC4wLjIyNTI0LCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwFAQAAABpCQUQuQ29tbW9uLlRvb2xzLkRhdGEuRGF0YQEAAAAYRGljdGlvbmFyeUJhc2UraGFzaHRhYmxlAxxTeXN0ZW0uQ29sbGVjdGlvbnMuSGFzaHRhYmxlAgAAAAkDAAAABAMAAAAcU3lzdGVtLkNvbGxlY3Rpb25zLkhhc2h0YWJsZQcAAAAKTG9hZEZhY3RvcgdWZXJzaW9uCENvbXBhcmVyEEhhc2hDb2RlUHJvdmlkZXIISGFzaFNpemUES2V5cwZWYWx1ZXMAAAMDAAUFCwgcU3lzdGVtLkNvbGxlY3Rpb25zLklDb21wYXJlciRTeXN0ZW0uQ29sbGVjdGlvbnMuSUhhc2hDb2RlUHJvdmlkZXII7FE4Px4AAAAKChcAAAAJBAAAAAkFAAAAEAQAAAANAAAABgYAAAAQU29sU2VjdXJpdHlMZXZlbAYHAAAAC0NUWF9ST1VUQUdFBggAAAAaU29sUGFydGljdWxhclNlY3VyaXR5TGV2ZWwGCQAAAAhCQVNFX1VSTAYKAAAAClBvcnRhbEF1dGgGCwAAAAZOVUFCQkQGDAAAAA1OVUFCQkRfQ1JZUFRFBg0AAAAPQXV0aHJBYm9ubmVtZW50Bg4AAAAHQ09EQ09ORgYPAAAAB0NMQVZJRVIGEAAAAAhFbnJvbFNvbAYRAAAAA0NUWAYSAAAADVNvbEFib25uZW1lbnQQBQAAAA0AAAAICAAAAAAGEwAAAAAICAAAAAAGFAAAAC1odHRwcyUzYSUyZiUyZnd3dy5uZXQ0NDQuY2Fpc3NlLWVwYXJnbmUuZnIlMmYGFQAAAAR0cnVlBhYAAAAKNDQxMTM0NDA4NAYXAAAAIDYzZGE0MjM2NTliZDIzZTJjNjgyNzU3YzU5ZWExNjBjCRgAAAAGGQAAAAUyMTg1MwgIAQAAAAkaAAAABhsAAABXbWFyPTEwMSZiYXNlX3VybD1odHRwcyUzYSUyZiUyZnd3dy5uZXQ0NDQuY2Fpc3NlLWVwYXJnbmUuZnIlMmYmcmVnPTE0NDQ1JnNjPTImdHlwc3J2PXdlCRwAAAAMHQAAAEpCQUQuQkxMLkNvbW1vbiwgVmVyc2lvbj0xMy45LjAuMTc0NDYsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUYAAAAJ0JBRC5CTEwuQ29tbW9uLkVFdGF0U291c2NyaXB0aW9uU2VydmljZQEAAAAHdmFsdWVfXwAIHQAAAAEAAAAFGgAAAB5CQUQuQkxMLkNvbW1vbi5FRXRhdFNlcnZpY2VTb2wBAAAAB3ZhbHVlX18ACB0AAAAKAAAAARwAAAAYAAAAAQAAAAsfAQUETUFJTmQWAgIBD2QWAmYPZBYMAgEPFCsAAg8FjAFDO0M6QkFELlVJLldlYi5Db21tb24uQ29udHJvbHMuRHluYW1pY1BsYWNlSG9sZGVyLCBCQUQuVUkuV2ViLkNvbW1vbiwgVmVyc2lvbj0yLjEwLjAuMzE0OTYsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbDtwaE1lbnVfbGVmdBYBDwUlQztVQzpNZW51X0FKQVguYXNjeDovQ29tbW9uO01lbnVfQWpheBYAZBYCZg8PFgQeEExQX01FTlVfVkVSVElDQUwy1gYAAQAAAP////8BAAAAAAAAAAwCAAAAS0JBRC5Db21tb24uVG9vbHMsIFZlcnNpb249Mi4wLjAuMjI1MjQsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUBAAAAGkJBRC5Db21tb24uVG9vbHMuRGF0YS5EYXRhAQAAABhEaWN0aW9uYXJ5QmFzZStoYXNodGFibGUDHFN5c3RlbS5Db2xsZWN0aW9ucy5IYXNodGFibGUCAAAACQMAAAAEAwAAABxTeXN0ZW0uQ29sbGVjdGlvbnMuSGFzaHRhYmxlBwAAAApMb2FkRmFjdG9yB1ZlcnNpb24IQ29tcGFyZXIQSGFzaENvZGVQcm92aWRlcghIYXNoU2l6ZQRLZXlzBlZhbHVlcwAAAwMABQULCBxTeXN0ZW0uQ29sbGVjdGlvbnMuSUNvbXBhcmVyJFN5c3RlbS5Db2xsZWN0aW9ucy5JSGFzaENvZGVQcm92aWRlcgjsUTg/BwAAAAoKCwAA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LWVwYXJnbmUuZnIvcGFydGljdWxpZXJzL2JyZXRhZ25lLXBheXMtZGUtbG9pcmUvdmlzdWVsX2NhcnRlLmFzcHg/dW5pdmVycz1hdXF1b3RpZGllbiZzb3VzdW5pdmVycz1jYXJ0ZXMfBQUjPHNwYW4+UGVyc29ubmFsaXNlciBtYSBjYXJ0ZTwvc3Bhbj4WAh4Hb25jbGljawVHcmV0dXJuIHh0X2NsaWNrKHRoaXMsJ0MnLCcxOScsJ01lbnVfREVJXzo6X1BlcnNvbm5hbGlzZXJfbWFfY2FydGUnLCdOJylkAgQPZBYEZg8VAQBkAgEPDxYEHwwFigFodHRwczovL3d3dy5jYWlzc2UtZXBhcmduZS5mci9wYXJ0aWN1bGllcnMvYnJldGFnbmUtcGF5cy1kZS1sb2lyZS9jb25uZXhpb24tY2FydGUtcmVjaGFyZ2VhYmxlLmFzcHg/dW5pdmVycz1hdXF1b3RpZGllbiZzb3VzdW5pdmVycz1jYXJ0ZXMfBQUoPHNwYW4+Q2FydGUgYmFuY2FpcmUgcmVjaGFyZ2VhYmxlPC9zcGFuPhYCHw4FTHJldHVybiB4dF9jbGljayh0aGlzLCdDJywnMTknLCdNZW51X0RFSV86Ol9DYXJ0ZV9iYW5jYWlyZV9yZWNoYXJnZWFibGUnLCdOJylkAgUPZBYEZg8VAQBkAgEPDxYEHwwFemphdmFzY3JpcHQ6V2ViRm9ybV9Eb1Bvc3RCYWNrV2l0aE9wdGlvbnMobmV3IFdlYkZvcm1fUG9zdEJhY2tPcHRpb25zKCJNTSRNZW51X0FqYXgiLCAiRUNBUlRFIiwgdHJ1ZSwgIiIsICIiLCBmYWxzZSwgdHJ1ZSkpHwUFFDxzcGFuPkUtQ2FydGU8L3NwYW4+ZGQCBg9kFgRmDxUBAGQCAQ8PFgQfDAV8amF2YXNjcmlwdDpXZWJGb3JtX0RvUG9zdEJhY2tXaXRoT3B0aW9ucyhuZXcgV2ViRm9ybV9Qb3N0QmFja09wdGlvbnMoIk1NJE1lbnVfQWpheCIsICJDUkVBQ0RFMCIsIHRydWUsICIiLCAiIiwgZmFsc2UsIHRydWUpKR8FBSc8c3Bhbj5DciZlYWN1dGU7ZGl0IHJlbm91dmVsYWJsZTwvc3Bhbj5kZAIFD2QWBmYPFQEAZAIBDw8WBh8MZR8FBT1Nb24gZm9yZmFpdCBldCBtZXMgc2VydmljZXM8c3BhbiBjbGFzcz0icGljdG8tZmxlY2hlIj48L3NwYW4+HwQFG01vbiBmb3JmYWl0IGV0IG1lcyBzZXJ2aWNlcxYCHw0FDmN1cnNvcjpwb2ludGVyZAIDDxYCHwsCAhYEAgEPZBYEZg8VAQBkAgMPFgIfCwL/////D2QCAg9kFgRmDxUBAGQCAw8WAh8LAv////8PZAIDDxYCHwsCARYCZg9kFgJmDxUDWmh0dHBzOi8vd3d3LmNhaXNzZS1lcGFyZ25lLmZyL3BhcnRpY3VsaWVycy9icmV0YWduZS1wYXlzLWRlLWxvaXJlL2JhbnF1ZS1hdS1xdW90aWRpZW4uYXNweEZyZXR1cm4geHRfY2xpY2sodGhpcywnQycsJzE5JywnTWVudV9ERUlfOjpfTWVzX2Jlc29pbnNfcXVvdGlkaWVuJywnTicpGE1lcyBiZXNvaW5zIGF1IHF1b3RpZGllbmQCBQ8WAh8LZmQCAw8WAh4FY2xhc3MFDGNvbnRlbnQgcGFnZRYEAgEPFCsAAg8FkgFDO0M6QkFELlVJLldlYi5Db21tb24uQ29udHJvbHMuRHluYW1pY1BsYWNlSG9sZGVyLCBCQUQuVUkuV2ViLkNvbW1vbiwgVmVyc2lvbj0yLjEwLjAuMzE0OTYsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbDttX2RwaFRpdHJlQ29udGVudRYAZBYCZg8PFgQeCUxQX0VOVEVURTKQCAABAAAA/////wEAAAAAAAAADAIAAABLQkFELkNvbW1vbi5Ub29scywgVmVyc2lvbj0yLjAuMC4yMjUyNCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsBQEAAAAaQkFELkNvbW1vbi5Ub29scy5EYXRhLkRhdGEBAAAAGERpY3Rpb25hcnlCYXNlK2hhc2h0YWJsZQMcU3lzdGVtLkNvbGxlY3Rpb25zLkhhc2h0YWJsZQIAAAAJAwAAAAQDAAAAHFN5c3RlbS5Db2xsZWN0aW9ucy5IYXNodGFibGUHAAAACkxvYWRGYWN0b3IHVmVyc2lvbghDb21wYXJlchBIYXNoQ29kZVByb3ZpZGVyCEhhc2hTaXplBEtleXMGVmFsdWVzAAADAwAFBQsIHFN5c3RlbS5Db2xsZWN0aW9ucy5JQ29tcGFyZXIkU3lzdGVtLkNvbGxlY3Rpb25zLklIYXNoQ29kZVByb3ZpZGVyCOxROD8PAAAACgoXAAAACQQAAAAJBQAAABAEAAAADgAAAAYGAAAADENPREVGT05DVElPTgYHAAAACEVucm9sU29sBggAAAAaU29sUGFydGljdWxhclNlY3VyaXR5TGV2ZWwGCQAAAAZUQVNLSUQGCgAAAAhBQ0NST0NIRQYLAAAACEJBU0VfVVJMBgwAAAAFUFJJTlQGDQAAAAVUSVRMRQYOAAAADVNvbEFib25uZW1lbnQGDwAAABBDT0RFU09VU0ZPTkNUSU9OBhAAAAAQU29sU2VjdXJpdHlMZXZlbAYRAAAAD0F1dGhyQWJvbm5lbWVudAYSAAAACUNPTk5FWElPTgYTAAAAB1dFTENPTUUQBQAAAA4AAAAGFAAAAAAJFQAAAAgIAAAAAAYWAAAAFVRFTEVDSEFSR0VfT1BFUkFUSU9OUwgBAAYXAAAALWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZggBAAYYAAAAHVTDqWzDqWNoYXJnZXIgZGVzIG9ww6lyYXRpb25zCRkAAAAJFAAAAAgIAAAAAAkbAAAACAEACAEADBwAAABKQkFELkJMTC5Db21tb24sIFZlcnNpb249MTMuOS4wLjE3NDQ2LCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwFFQAAAB5CQUQuQkxMLkNvbW1vbi5FRXRhdFNlcnZpY2VTb2wBAAAAB3ZhbHVlX18ACBwAAAAKAAAABRkAAAAnQkFELkJMTC5Db21tb24uRUV0YXRTb3VzY3JpcHRpb25TZXJ2aWNlAQAAAAd2YWx1ZV9fAAgcAAAAAQAAAAEbAAAAGQAAAAEAAAALHwEFBkVOVEVURWQWBgIFDw8WBB8BZR4HVmlzaWJsZWhkZAILDw9kFgIfDQWbAWxlZnQ6MjVweDt0ZXh0LWFsaWduOmxlZnQ7d2lkdGg6MjAwcHg7ei1pbmRleDozO2ZvbnQtd2VpZ2h0OjcwMDt0ZXh0LWRlY29yYXRpb246bm9uZTtmb250LWZhbWlseTpBcmlhbDtwb3NpdGlvbjphYnNvbHV0ZTt0b3A6OHB4O2NvbG9yOldoaXRlO2ZvbnQtc2l6ZTo4cHQ7ZAIPDxYCHxFoZAIDDxQrAAIPBY4BQztDOkJBRC5VSS5XZWIuQ29tbW9uLkNvbnRyb2xzLkR5bmFtaWNQbGFjZUhvbGRlciwgQkFELlVJLldlYi5Db21tb24sIFZlcnNpb249Mi4xMC4wLjMxNDk2LCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGw7bV9QbGFjZUhvbGRlchYBDwVJQztVQzpUZWxlY2hhcmdlT3BlcmF0aW9uLmFzY3g6L1VzZXJDb250cm9scy9Db21wdGVzO1RFTEVDSEFSR0VfT1BFUkFUSU9OUxYAZBYCZg8PFgweGExQX1RFTEVDSEFSR0VfT1BFUkFUSU9OUzKzDAABAAAA/////wEAAAAAAAAADAIAAABLQkFELkNvbW1vbi5Ub29scywgVmVyc2lvbj0yLjAuMC4yMjUyNCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsBQEAAAAaQkFELkNvbW1vbi5Ub29scy5EYXRhLkRhdGEBAAAAGERpY3Rpb25hcnlCYXNlK2hhc2h0YWJsZQMcU3lzdGVtLkNvbGxlY3Rpb25zLkhhc2h0YWJsZQIAAAAJAwAAAAQDAAAAHFN5c3RlbS5Db2xsZWN0aW9ucy5IYXNodGFibGUHAAAACkxvYWRGYWN0b3IHVmVyc2lvbghDb21wYXJlchBIYXNoQ29kZVByb3ZpZGVyCEhhc2hTaXplBEtleXMGVmFsdWVzAAADAwAFBQsIHFN5c3RlbS5Db2xsZWN0aW9ucy5JQ29tcGFyZXIkU3lzdGVtLkNvbGxlY3Rpb25zLklIYXNoQ29kZVByb3ZpZGVyCOxROD8cAAAACgoXAAAACQQAAAAJBQAAABAEAAAACQAAAAYGAAAAEFNvbFNlY3VyaXR5TGV2ZWwGBwAAAAhFbnJvbFNvbAYIAAAAGlNvbFBhcnRpY3VsYXJTZWN1cml0eUxldmVsBgkAAAAEbWVudQYKAAAACEJBU0VfVVJMBgsAAAAEdGFzawYMAAAADVNvbEFib25uZW1lbnQGDQAAAA9BdXRockFib25uZW1lbnQGDgAAAANDVFgQBQAAAAkAAAAICAAAAAAJDwAAAAgIAAAAAAYQAAAAATEGEQAAAC1odHRwcyUzYSUyZiUyZnd3dy5uZXQ0NDQuY2Fpc3NlLWVwYXJnbmUuZnIlMmYGEgAAAAhDUFRETVRFMAkTAAAACRQAAAAGFQAAALMFbWFyPTEwMSZiYXNlX3VybD1odHRwcyUzYSUyZiUyZnd3dy5uZXQ0NDQuY2Fpc3NlLWVwYXJnbmUuZnIlMmYmcmVnPTE0NDQ1JnNjPTImdHlwc3J2PXdlJnBmbD1KQUJBRTAmbmFnPTIxNSZuYWI9NjNkYTQyMzY1OWJkMjNlMmM2ODI3NTdjNTllYTE2MGMmYXV0aD0xJmlzY2libGU9dHJ1ZSZ1c2VybmFtZT1NIEpVTElFTiBNQUlTT05ORVVWRSZjb25zZWlsbGVybmFtZT1Nb24gY29uc2VpbGxlciA6ICBNTUUgRUxMRU4gR0lSQVJEJm5icm1lc3NhZ2U9MCZzaXRlbml2Mj0xOSZ1cGFyYWN0aWY9MSZ1cGFydHJhbnNhY3Q9MHwxfDN8Mnw0fCZiYXNlX3VybF9kZWk9aHR0cHMlM2ElMmYlMmZ3d3cubmV0NDQ0LmNhaXNzZS1lcGFyZ25lLmZyJTJmJmJhc2VVUkw9aHR0cHMlM2ElMmYlMmZ3d3cubmV0NDQ0LmNhaXNzZS1lcGFyZ25lLmZyJTJmJnJldHVybl91cmw9aHR0cHMlM2ElMmYlMmZ3d3cubmV0NDQ0LmNhaXNzZS1lcGFyZ25lLmZyJTJmUG9ydGFpbC5hc3B4JTNGdGFjaGUlM0RDUFRTWU5UMCZjYXJ0cmlkZ2VfdXJsPWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZnBhZ2VzL2NhcnRyaWRnZS5hc3B4JTNGaWZyJTNEMSZjYXJ0cmlkZ2VpbmRfdXJsPWh0dHBzJTNhJTJmJTJmd3d3Lm5ldDQ0NC5jYWlzc2UtZXBhcmduZS5mciUyZnBhZ2VzL2NhcnRyaWRnZWluZC5hc3B4JTNGaWZyJTNEMQwWAAAASkJBRC5CTEwuQ29tbW9uLCBWZXJzaW9uPTEzLjkuMC4xNzQ0NiwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsBQ8AAAAeQkFELkJMTC5Db21tb24uRUV0YXRTZXJ2aWNlU29sAQAAAAd2YWx1ZV9fAAgWAAAACgAAAAUTAAAAJ0JBRC5CTEwuQ29tbW9uLkVFdGF0U291c2NyaXB0aW9uU2VydmljZQEAAAAHdmFsdWVfXwAIFgAAAAEAAAABFAAAABMAAAABAAAACx4NaU5iSm91cnNIaXN0bwI8HgppSW5kaWNlQ3B0Zh4EZGF0ZQYAAAAAAAAAAB4JSXNBY2NvdW50Zx8BBRVURUxFQ0hBUkdFX09QRVJBVElPTlNkFhgCAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQdsaWJlbGxlHg5EYXRhVmFsdWVGaWVsZAUGdmFsZXVyHgtfIURhdGFCb3VuZGdkEBUEMzA0MzE3NzI2NTQzIC0gQ09NUFRFIENIRVFVRSAtIE1SIE1BSVNPTk5FVVZFIEpVTElFTi4wMDY1Njc5MDYzNiAtIExJVlJFVCBBIC0gTVIgTUFJU09OTkVVVkUgSlVMSUVOMjEwNjU2NzkwNjIwIC0gTElWUkVUIEpFVU5FIC0gTVIgTUFJU09OTkVVVkUgSlVMSUVONDM3NjU2NzkwNjE3IC0gUEFSVFMgU09DSUFMRVMgLSBNUiBNQUlTT05ORVVWRSBKVUxJRU4VBCZDIzE0NDQ1MDA0MDAwNDMxNzcyNjU0MzE2IzIwMTMxMTA4I0VVUh5DIzE0NDQ1MDA0MDAwMDY1Njc5MDYzNjAzIyNFVVIeQyMxNDQ0NTAwNDAwMTA2NTY3OTA2MjAwMSMjRVVSJkMjMTQ0NDUwMDQwMDM3NjU2NzkwNjE3NjkjMjAxMzA5MDkjRVVSFCsDBGdnZ2cWAWZkAgIPZBYIZg9kFgRmDxAPFgIeB0NoZWNrZWRoZGRkZAIBDxYCHxFoZAIBDxAPFgIfGmdkZGRkAgIPFgIfEWdkAgMPDxYCHwUFgwFMZSBub21icmUgZGUgam91cnMgZCdoaXN0b3JpcXVlIHBvc3NpYmxlIGVzdCBkZSA2MCBqb3VycywgYydlc3Qgw6AgZGlyZSBxdWUgdm91cyBuZSBwb3V2ZXogdMOpbMOpY2hhcmdlciBxdSfDoCBwYXJ0aXIgZHUgMDkvMDkvMjAxM2RkAgMPDxYCHwUFCExvZ2ljaWVsZGQCBA8QDxYCHxlnZA8WBWYCAQICAgMCBBYFEAUoRXhjZWwgKCouY3N2LCBzw6lwYXJhdGV1ciBwb2ludCB2aXJndWxlKQUBM2cQBRRBZG9iZSBSZWFkZXIgKCoucGRmKQUBNGcQBRRNb25leSAoZmljaGllciAub2Z4KQUBMGcQBShRdWlja2VuIGRhdGVzIGZyYW7Dp2Fpc2VzIChmaWNoaWVyIC5xaWYpBQExZxAFKVF1aWNrZW4gZGF0ZXMgYW3DqXJpY2FpbmVzIChmaWNoaWVyIC5xaWYpBQEyZ2RkAgYPZBYCAgEPFQEwaHR0cHM6Ly93d3cuY2Fpc3NlLWVwYXJnbmUuZnIvY2FjaGUvY3NzMTMwMV9pbWcvZAIIDw8WBB4NTGVmdExpbmtMYWJlbAUHQW5udWxlch4OUmlnaHRMaW5rTGFiZWwFCUNvbmZpcm1lcmQWAgIBD2QWBgIDDw8WAh4KdGFza0xpbmtlZAUIU1lOVEhFU0VkFgJmDw8WBB8DBRVib3V0b24tcm9uZCBmbG9hdExlZnQfBwICZGQCBQ8PFgofAwUQYm91dG9uLWNhcnJlIG9mZh4QQ2F1c2VzVmFsaWRhdGlvbmgfBQUHQW5udWxlch8HAgIfEWdkZAIHDw8WCh8DBQxib3V0b24tY2FycmUfHmgfBQUJQ29uZmlybWVyHwcCAh8RZ2RkAgkPDxYCHgxFcnJvck1lc3NhZ2UFSkxhIGRhdGUgZGUgZMOpYnV0IGRlIGxhIHDDqXJpb2RlIGRvaXQgw6p0cmUgaW5mw6lyaWV1cmUgw6AgbGEgZGF0ZSBkdSBqb3VyZGQCCg8PFgIfHwVHTGEgZGF0ZSBkZSBmaW4gZGUgbGEgcMOpcmlvZGUgZG9pdCDDqnRyZSBpbmbDqXJpZXVyZSDDoCBsYSBkYXRlIGR1IGpvdXJkZAILDw8WAh8fBTpMYSBkYXRlIGRlIGTDqWJ1dCBkb2l0IMOqdHJlIGFudMOpcmlldXJlIMOgIGxhIGRhdGUgZGUgZmluZGQCDA8PFgIfHwU3Vm91cyBkZXZleiByZW5zZWlnbmVyIGF1IG1vaW5zIHVuIGNyaXTDqHJlIGRlIHJlY2hlcmNoZWRkAg0PDxYCHx8FZlZvdXMgbmUgcG91dmV6IHBhcyByZW5zZWlnbmVyIHBsdXNpZXVycyBjcml0w6hyZXMgw6AgbGEgZm9pcy48YnI+TGVzIHR5cGVzIGRlIHJlY2hlcmNoZSBzb250IGV4Y2x1c2lmc2RkAg4PDxYCHx8FUlZvdXMgZGV2ZXogcmVtcGxpciB1bmUgcMOpcmlvZGUgZGUgZGF0ZXMgT1UgY2hvaXNpciB2b3RyZSBkZXJuaWVyIHTDqWzDqWNoYXJnZW1lbnRkZAIFDxQrAAIPBYkBQztDOkJBRC5VSS5XZWIuQ29tbW9uLkNvbnRyb2xzLkR5bmFtaWNQbGFjZUhvbGRlciwgQkFELlVJLldlYi5Db21tb24sIFZlcnNpb249Mi4xMC4wLjMxNDk2LCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGw7cGhXaWRnZXQWAGRkAgcPFCsAAg8FjQFDO0M6QkFELlVJLldlYi5Db21tb24uQ29udHJvbHMuRHluYW1pY1BsYWNlSG9sZGVyLCBCQUQuVUkuV2ViLkNvbW1vbiwgVmVyc2lvbj0yLjEwLjAuMzE0OTYsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbDtwbmxQb3BpblRhc2sWAGRkAgsPFCsAAg8FkAFDO0M6QkFELlVJLldlYi5Db21tb24uQ29udHJvbHMuRHluYW1pY1BsYWNlSG9sZGVyLCBCQUQuVUkuV2ViLkNvbW1vbiwgVmVyc2lvbj0yLjEwLjAuMzE0OTYsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbDtwbmxFcnJvck1lc3NhZ2UWAGRkAhEPDxYCHwFlZBYCAgIPD2QWAh4DcmVsBQExZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBQUiTU0kY3RsMDEkQnV0dG9uSW1hZ2VGb25kTWVzc2FnZXJpZQUeTU0kY3RsMDEkQnV0dG9uSW1hZ2VNZXNzYWdlcmllBSlNTSRURUxFQ0hBUkdFX09QRVJBVElPTlMkY2hrRGVybmllclRlbGVjaAUpTU0kVEVMRUNIQVJHRV9PUEVSQVRJT05TJGNoa0Rlcm5pZXJUZWxlY2gFIE1NJFRFTEVDSEFSR0VfT1BFUkFUSU9OUyRjaGtEYXRl',
			'm_ScriptManager' :'MM$m_UpdatePanel|MM$TELECHARGE_OPERATIONS$m_ChoiceBar$lnkRight'
		}
		load_headers = {
			'Host': 'www.net444.caisse-epargne.fr',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0 Iceweasel/20.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'X-MicrosoftAjax': 'Delta=true',
			'Cache-Control': 'no-cache',
			'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
			'Referer': 'https://www.net444.caisse-epargne.fr/Portail.aspx',
			'Connection': 'keep-alive',
			'Pragma': 'no-cache'
		}
		self.request.post(
			self.LOAD_URL,
			verify=True,
			data=load_payload,
			headers=load_headers
		)
	def _retrieve(self):
		return self.request.get(self.RTRV_URL, verify=True).text.encode('utf8')
	def get_transactions(self, from_days_ago=MAX_DAYS_AGO, to_days_ago=MIN_DAYS_AGO):
		if from_days_ago < to_days_ago:
			raise Exception("Starting date must be inferior to ending date")
		if to_days_ago < self.MIN_DAYS_AGO:
			raise Exception("Ending date cannot be superior to {0} day(s) ago".format(self.MIN_DAYS_AGO))
		if from_days_ago > self.MAX_DAYS_AGO:
			raise Exception("Cannot retrieve transactions prior to {0} day(s)".format(self.MAX_DAYS_AGO))
		start = (self.today - timedelta(days=from_days_ago)).strftime('%d/%m/%Y')
		end = (self.today - timedelta(days=to_days_ago)).strftime('%d/%m/%Y')

		self._authenticate()
		self._load(start, end)
		return self._retrieve()

# bank = Bank(CLIENT_ID, CLIENT_SECRET, CLIENT_IBAN)
# print bank.get_transactions()

class Parser(object):
	pass